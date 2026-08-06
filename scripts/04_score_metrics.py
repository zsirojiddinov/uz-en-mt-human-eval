# -*- coding: utf-8 -*-
"""CE1 — SKORING: (a) har tizim ref-ga nisbatan sentence-BLEU(smoothed)+chrF+KKT-RS,
(b) tizim-vs-tizim o'zaro-BLEU/chrF matritsasi, (c) qatlam kesimi. TALQIN YOZILMAYDI.

Tizimlar: s1(joriy), s2(M1-oldingi), gemini + manual_fill.csv to'ldirilgan ustunlar
(google/claude/chatgpt). To'ldirilmagan ustun O'TKAZILADI (qayd bilan).

KKT-RS h2_metric.score_sentence bilan (source-subject/predicate uz-dan). Tashqi
chiqishda komponent degenerat bo'lsa — qayd etiladi (yashirilmaydi).
"""
import json, os, sys, csv
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
import sacrebleu
from dotenv import load_dotenv; load_dotenv()
from app import create_app
from services.sentence_translator_v2 import sentence_translator_v2 as ST, split_clauses
import analysis.h2_metric as H2

rows = json.load(open(os.path.join(HERE, 'sentences.json'), encoding='utf-8'))
REF = {r['id']: r['ref_en'] for r in rows}
LAYER = {r['id']: r['layer'] for r in rows}
IDS = [r['id'] for r in rows]


def load_outputs():
    outs = {}
    for name, fn in [('s1', 's1_outputs.json'), ('s2', 's2_outputs.json'),
                     ('gemini', 's3_gemini_outputs.json')]:
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8'))
            outs[name] = {k: v for k, v in d.items() if k != '_meta'}
    # manual CSV columns
    csvp = os.path.join(HERE, 'manual_fill.csv')
    if os.path.exists(csvp):
        cols = {'gt_english': 'google', 'claude_english': 'claude', 'chatgpt_english': 'chatgpt'}
        acc = {v: {} for v in cols.values()}
        with open(csvp, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                for c, name in cols.items():
                    if (row.get(c) or '').strip():
                        acc[name][row['id']] = row[c].strip()
        for name, d in acc.items():
            if len(d) == len(IDS):
                outs[name] = d
            elif d:
                print(f"[QAYD] manual '{name}': {len(d)}/{len(IDS)} to'ldirilgan -> O'TKAZILDI (to'liq emas)")
    return outs


def sb(hyp, ref):
    return sacrebleu.sentence_bleu(hyp or '', [ref or ''], smooth_method='exp').score


def sc(hyp, ref):
    return sacrebleu.sentence_chrf(hyp or '', [ref or '']).score


def score_vs_ref(outs, app):
    res = {}
    with app.app_context():
        for name, d in outs.items():
            per = {}
            kkt_deg = defaultdict(int)
            for r in rows:
                i = r['id']; hyp = d.get(i, ''); ref = REF[i]
                rec = {'bleu': sb(hyp, ref), 'chrf': sc(hyp, ref)}
                try:
                    se, pe, vo = H2.source_subject_predicate(r['uz'], ST, split_clauses)
                    ks = H2.score_sentence(r['uz'], hyp, ref, se, pe, vo)
                    rec.update({'kkt_rs': ks['kkt_rs'], 'ega': ks['ega'], 'kesim': ks['kesim'],
                                'np_order': ks['np_order'], 'qamrov': ks['qamrov']})
                    if not se: kkt_deg['ega(source-subj yo\'q)'] += 1
                except Exception as e:
                    rec['kkt_rs'] = None; kkt_deg[f'exception:{type(e).__name__}'] += 1
                per[i] = rec
            res[name] = {'per': per, 'kkt_degenerate': dict(kkt_deg)}
    return res


def agg(per, ids):
    ids = [i for i in ids if i in per]
    if not ids:
        return {}
    def m(k):
        vals = [per[i][k] for i in ids if per[i].get(k) is not None]
        return round(sum(vals) / len(vals), 2) if vals else None
    return {'n': len(ids), 'bleu': m('bleu'), 'chrf': m('chrf'), 'kkt_rs': m('kkt_rs'),
            'ega': m('ega'), 'kesim': m('kesim'), 'np_order': m('np_order'), 'qamrov': m('qamrov')}


def cross_matrix(outs):
    names = list(outs)
    mat_b = {}; mat_c = {}
    for a in names:
        mat_b[a] = {}; mat_c[a] = {}
        for b in names:
            if a == b:
                mat_b[a][b] = None; mat_c[a][b] = None; continue
            bl = [sb(outs[a].get(i, ''), outs[b].get(i, '')) for i in IDS]
            ch = [sc(outs[a].get(i, ''), outs[b].get(i, '')) for i in IDS]
            mat_b[a][b] = round(sum(bl) / len(bl), 2)
            mat_c[a][b] = round(sum(ch) / len(ch), 2)
    return names, mat_b, mat_c


def main():
    app = create_app()
    outs = load_outputs()
    print("Tizimlar:", list(outs))
    res = score_vs_ref(outs, app)

    summary = {'vs_ref': {}, 'vs_ref_by_layer': {}, 'cross_bleu': None, 'cross_chrf': None,
               'kkt_degenerate': {n: res[n]['kkt_degenerate'] for n in res}}
    print("\n=== (a) REF-GA NISBATAN (jami 72) ===")
    print(f"{'sys':10}{'BLEU':>7}{'chrF':>7}{'KKT-RS':>8}{'EGA':>6}{'KESIM':>7}{'NP':>6}{'QAMR':>6}")
    for name in outs:
        a = agg(res[name]['per'], IDS); summary['vs_ref'][name] = a
        print(f"{name:10}{a['bleu']:>7}{a['chrf']:>7}{str(a['kkt_rs']):>8}{a['ega']:>6}{a['kesim']:>7}{a['np_order']:>6}{a['qamrov']:>6}")

    print("\n=== (a) QATLAM KESIMI (BLEU / chrF) ===")
    for layer in ('flores', 'train', 'gold'):
        lids = [i for i in IDS if LAYER[i] == layer]
        print(f"-- {layer} (n={len(lids)}) --")
        summary['vs_ref_by_layer'][layer] = {}
        for name in outs:
            a = agg(res[name]['per'], lids); summary['vs_ref_by_layer'][layer][name] = a
            print(f"   {name:10} BLEU={a['bleu']:>6}  chrF={a['chrf']:>6}  KKT-RS={a['kkt_rs']}")

    names, mb, mc = cross_matrix(outs)
    summary['cross_bleu'] = mb; summary['cross_chrf'] = mc
    print("\n=== (b) O'ZARO-BLEU MATRITSA (qator=hyp, ustun=ref) ===")
    print(f"{'':10}" + ''.join(f"{n:>9}" for n in names))
    for a in names:
        print(f"{a:10}" + ''.join(f"{(str(mb[a][b]) if mb[a][b] is not None else '—'):>9}" for b in names))
    print("\n=== (b) O'ZARO-chrF MATRITSA ===")
    print(f"{'':10}" + ''.join(f"{n:>9}" for n in names))
    for a in names:
        print(f"{a:10}" + ''.join(f"{(str(mc[a][b]) if mc[a][b] is not None else '—'):>9}" for b in names))

    print("\n=== KKT-RS degenerat komponentlar (tashqi chiqish) ===")
    for n in res:
        if res[n]['kkt_degenerate']:
            print(f"   {n}: {res[n]['kkt_degenerate']}")

    json.dump(summary, open(os.path.join(HERE, 'scores.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    json.dump({n: res[n]['per'] for n in res},
              open(os.path.join(HERE, 'scores_detail.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"\nSaqlandi: scores.json + scores_detail.json")


if __name__ == '__main__':
    main()
