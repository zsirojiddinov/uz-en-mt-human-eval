# -*- coding: utf-8 -*-
"""TOLQIN-2 — B-qavat tizim × qatlam, Claude ustunligi. NATIJADAN KEYINGI, EKSPLORATIV, PREREG'DA YO'Q; tadqiqotchi so'rovi
2026-10-28. Tasdiqlovchi emas. B1 jadvali (korpus-BLEU, chrF2; 1 etalon va asl+T1) natija/tahlil_natija.json dan O'QILADI;
ustunlik va CI — yangi hisob. Sabab ajratilmaydi: qatlamlar janr va qiyinlik bo'yicha ham farq qiladi, FLORES ochiqligi
(pretraining ehtimoli) yagona izoh emas. Muzlatilgan tahlil.py ga tegmaydi — undan faqat yukla(), bleu_stat(), bleu_stat_ball(),
_CHRF va TIZIMLAR import qilinadi. natija/ ga yozilmaydi.

    python3 analysis/tolqin-2/qoshimcha/qatlam_ustunlik.py   # bir marta; qatlam_ustunlik.json mavjud bo'lsa TO'XTAYDI

Qatlamlar (eval72 `layer`; prereg §2.2): flores 36, train = ilmiy 24, gold = oddiy 12 (beqaror, < 20), train+gold 36.
Ustunlik = Claude − o'rtacha(Gemini, GPT, GT) va Claude − max(Gemini, GPT, GT); etalon: 1 etalon (eval72 ref_en) va asl+T1
(tuzatish 10 (a), (b): № 55 da faqat asl etalon). flores − train farqining 95 % CI: bootstrap, har qatlam ichida gap bo'yicha
qayta tanlash (flores 36, train 24), seed 20261028; BLEU 1000 tanlov (bleu_stat yig'indisi), chrF2 300 tanlov (har tanlovda
korpus chrF2 qayta hisoblanadi — sekin). Persentil CI. Nuqtaviy BLEU/chrF2 B1 bilan tekshiriladi (assert).
Chiqish: qoshimcha/qatlam_ustunlik.json, qoshimcha/qatlam_ustunlik.md.
"""
import importlib.util
import json
import random
import sys
from pathlib import Path

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parent
SEED, BOOT = 20261028, {'bleu': 1000, 'chrf2': 300}
NEY = ('Gemini', 'GPT', 'GT')
_sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))
T = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(T)


def main():
    if (CHIQ / 'qatlam_ustunlik.json').exists():
        sys.exit("TO'XTA: qoshimcha/qatlam_ustunlik.json mavjud — bir marta yuriladi")
    _, B, chiq, Tr, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    ids = {L: [r['id'] for r in B if r['layer'] == L] for L in ('flores', 'train', 'gold')}
    ids['train+gold'] = ids['train'] + ids['gold']
    ref = {r['id']: r['ref_en'] for r in B}
    oq = {'1ref': lambda i: [ref[i]], 'asl+T1': lambda i: [ref[i], Tr['T1'].get(i)]}   # B1 dagi «3ref» = asl+T1
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))['jadvallar']
    b1 = nat[[k for k in nat if k.startswith('B1')][0]]
    b1q = {'flores': 'qatlam flores', 'train': 'qatlam train', 'gold': 'qatlam gold', 'train+gold': 'B-KKT (train+gold)'}
    b1o = {'1ref': '1ref', 'asl+T1': '3ref'}

    def hyp(t, ii):
        return [chiq[t][('eval72', i)] for i in ii]

    def refs(ii, o):
        return [list(x) for x in zip(*[oq[o](i) for i in ii])]

    ST = {o: {L: {t: T.bleu_stat(hyp(t, ids[L]), refs(ids[L], o)) for t in T.TIZIMLAR} for L in ids} for o in oq}

    def ball(m, o, L, t, ix=None):
        ix = range(len(ids[L])) if ix is None else ix
        if m == 'bleu':
            return T.bleu_stat_ball(ST[o][L][t], ix)
        ii = [ids[L][k] for k in ix]
        return T._CHRF.corpus_score(hyp(t, ii), refs(ii, o)).score

    def ust(m, o, L, ix=None):
        s = {t: ball(m, o, L, t, ix) for t in ('Claude',) + NEY}
        return s['Claude'] - sum(s[t] for t in NEY) / 3, s['Claude'] - max(s[t] for t in NEY)

    for o in oq:                                                   # nuqtaviy qiymatlar = B1
        for L in ids:
            for t in T.TIZIMLAR:
                for m in ('bleu', 'chrf2'):
                    assert abs(ball(m, o, L, t) - b1[b1q[L]][t][b1o[o]][m]) < 1e-9, f'{o} {L} {t} {m}: B1 bilan teng emas'
    R = {'maqom': "natijadan keyingi, eksplorativ, prereg'da yo'q; tadqiqotchi so'rovi 2026-10-28; B1 jadvali tahlil_natija.json dan, "
                  "ustunlik va CI yangi hisob; sabab ajratilmaydi",
         'bootstrap': {'seed': SEED, 'n': BOOT, 'birlik': "gap, qatlam ichida (flores 36, train 24)", 'ci': 'persentil 95 %'},
         'qatlam_n': {L: len(v) for L, v in ids.items()},
         'B1': {o: {L: {t: {m: b1[b1q[L]][t][b1o[o]][m] for m in ('bleu', 'chrf2')} for t in T.TIZIMLAR} for L in ids} for o in oq},
         'ustunlik': {}}
    for o in oq:
        for m in ('bleu', 'chrf2'):
            r = {L: ust(m, o, L) for L in ids}
            rnd = random.Random(SEED)
            dd = []
            for _ in range(BOOT[m]):
                fx = [rnd.randrange(len(ids['flores'])) for _ in ids['flores']]
                tx = [rnd.randrange(len(ids['train'])) for _ in ids['train']]
                f, tr = ust(m, o, 'flores', fx), ust(m, o, 'train', tx)
                dd.append((f[0] - tr[0], f[1] - tr[1]))
            ci = []
            for k in (0, 1):
                v = sorted(x[k] for x in dd)
                ci.append([v[int(0.025 * len(v))], v[int(0.975 * len(v)) - 1]])
            R['ustunlik'][f'{o} {m}'] = {'ortachaga_qarshi': {L: r[L][0] for L in ids}, 'eng_yaxshiga_qarshi': {L: r[L][1] for L in ids},
                                         'flores_minus_train': [r['flores'][0] - r['train'][0], r['flores'][1] - r['train'][1]],
                                         'ci95': ci, 'boot': BOOT[m]}
    (CHIQ / 'qatlam_ustunlik.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    f = lambda v: f'{v:.2f}'
    L = ['# TOLQIN-2 — B-qavat tizim × qatlam, Claude ustunligi (qatlam_ustunlik.py)', '', f"**{R['maqom']}**. Tasdiqlovchi emas.",
         f"Qatlamlar: flores 36 · train (ilmiy) 24 · gold (oddiy) 12, beqaror · train+gold 36. asl+T1: № 55 da faqat asl etalon.",
         f"Bootstrap: seed {SEED}; BLEU {BOOT['bleu']}, chrF2 {BOOT['chrf2']} tanlov; qatlam ichida gap bo'yicha; persentil 95 % CI.", '',
         '## B1 — korpus-BLEU / chrF2 (natija/tahlil_natija.json dan)', '',
         '| qatlam | etalon | ' + ' | '.join(T.TIZIMLAR) + ' |', '|---|---|' + '---|' * len(T.TIZIMLAR)]
    for Lq in ids:
        for o in oq:
            L.append(f'| {Lq} | {o} | ' + ' | '.join(f"{f(R['B1'][o][Lq][t]['bleu'])} / {f(R['B1'][o][Lq][t]['chrf2'])}" for t in T.TIZIMLAR) + ' |')
    L += ['', '## Claude ustunligi (o\'rtachaga / eng yaxshiga qarshi; Gemini, GPT, GT)', '',
          '| o\'lchov | flores | train | gold | train+gold | flores − train | 95 % CI | tanlov |', '|---|---|---|---|---|---|---|---|']
    for k, v in R['ustunlik'].items():
        L.append(f'| {k} | ' + ' | '.join(f"{f(v['ortachaga_qarshi'][Lq])} / {f(v['eng_yaxshiga_qarshi'][Lq])}" for Lq in ids)
                 + f" | {f(v['flores_minus_train'][0])} / {f(v['flores_minus_train'][1])}"
                 + f" | [{f(v['ci95'][0][0])}; {f(v['ci95'][0][1])}] / [{f(v['ci95'][1][0])}; {f(v['ci95'][1][1])}] | {v['boot']} |")
    L += ['', 'Sabab ajratilmaydi: qatlamlar janr va qiyinlik bo\'yicha ham farq qiladi. 1 etalonli FLORES qatlamida etalon — FLORES asl',
          'ingliz matni (yodlash ehtimoliga eng sezgir). asl+T1 da GPT FLORES BLEU 37,19 -> 62,26 (boshqalardan ancha katta o\'sish).']
    (CHIQ / 'qatlam_ustunlik.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('qoshimcha/: qatlam_ustunlik.json, .md')


if __name__ == '__main__':
    main()
