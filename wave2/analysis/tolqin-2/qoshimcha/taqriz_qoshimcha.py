# -*- coding: utf-8 -*-
"""TOLQIN-2 — taqriz uchun qo'shimcha hisoblar va faktlar. NATIJADAN KEYINGI, TAQRIZGA JAVOB, 2026-10-29. Tasdiqlovchi emas.
Muzlatilgan tahlil.py ga tegmaydi — undan yukla(), korpus(), gap_bleu(), spearman(), kripp_alpha_ordinal(), oqi_xlsx(), e_xom(),
_i, _BLEU, _CHRF, CHIQ7, TIZIMLAR import qilinadi; normallashtirish — ekspozitsiya_2.norm_tok (etalon_tekshir.py dagidek).
natija/ va etalon/ faqat O'QILADI.

    python3 analysis/tolqin-2/qoshimcha/taqriz_qoshimcha.py   # bir marta; taqriz_qoshimcha.json mavjud bo'lsa TO'XTAYDI

1. Har tizim: korpus-BLEU va chrF2 FAQAT T1 ga nisbatan (T1 bor 71 gap); T1 bilan aynan mos gaplar (xom va normallashtirilgan);
   T1 ga eng yaqin ikki tizim (BLEU bo'yicha; chrF2 bo'yicha ham).
2. FLORES etaloniga aynan va deyarli mos gaplar: deyarli = gap-chrF2 ≥ 95 VA gap-BLEU (exp) ≥ 90 (aynanlar ham kiradi);
   A-qavat (400, en_ref) va B-FLORES (36, ref_en) alohida.
3. Neyron tizim ichida ρ(gap-BLEU_1ref, adequacy) — natija/tahlil_natija.json H4 «tizim ichida» dan (ASOSIY 71, bootstrap CI).
4. α (ordinal): baholovchi to'plamlari B,C,D · B,C,D,E · leave-one-out (C,D; B,D; B,C) · qolgan juftliklar (B,E; C,E; D,E) ×
   element qism-to'plami (hammasi / KKT / neyron) × qatlam (hammasi / flores / train / gold) × (mazmun, ravonlik).
   Element to'plami ASOSIY 71 (gold-00 siz, 355 element); yo'q kataklar juftlik bo'yicha chiqariladi (tuzatish 10 (g)).
   Tekshiruv: B,C,D · hammasi · hammasi = H7 ASOSIY; B,C,D,E = «E bilan» H7 ASOSIY (assert).
5. Har baholovchi: o'z mazmun bali ≥ 4,5 (ya'ni 5) bo'lgan elementlar (ASOSIY 71): soni (tizim bo'yicha) va korpus-BLEU (1 etalon).
6. Faktlar — tekshiruv hisoblari bilan (55-gap, signatura, smoothing, (c)-darvoza, etalon_tekshir aynanlari).
Chiqish: qoshimcha/taqriz_qoshimcha.json, .md.
"""
import importlib.util
import json
import sys
from pathlib import Path

import sacrebleu

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parent


def _mod(nom):
    sp = importlib.util.spec_from_file_location(f'{nom}_m', str(SIKL / f'{nom}.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _mod('tahlil')
EK = _mod('ekspozitsiya_2')
NEY = ('Gemini', 'Claude', 'GPT', 'GT')
DAR = (('mazmun', 0, 'adequacy'), ('ravonlik', 1, 'fluency'))
n = lambda s: ' '.join(EK.norm_tok(s))


def main():
    if (CHIQ / 'taqriz_qoshimcha.json').exists():
        sys.exit("TO'XTA: qoshimcha/taqriz_qoshimcha.json mavjud — bir marta yuriladi")
    A, B, chiq, Tr, kbt, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))
    et = json.loads((SIKL / 'etalon' / 'etalon_tekshir.json').read_text(encoding='utf-8'))
    b_id = [r['id'] for r in B]
    ref = {r['id']: r['ref_en'] for r in B}
    lay = {r['id']: r['layer'] for r in B}
    t1 = Tr['T1']
    R = {'maqom': "natijadan keyingi, taqrizga javob, 2026-10-29; tasdiqlovchi emas"}

    # 1. T1 ga nisbatan
    i71 = [i for i in b_id if t1.get(i)]
    r1 = {}
    for t in T.TIZIMLAR:
        h = [chiq[t][('eval72', i)] for i in i71]
        k = T.korpus(h, [[t1[i] for i in i71]])
        r1[t] = {'bleu': k['bleu'], 'chrf2': k['chrf2'], 'n': len(i71),
                 'aynan_xom': sum(h[j] == t1[i] for j, i in enumerate(i71)),
                 'aynan_norm': sum(n(h[j]) == n(t1[i]) for j, i in enumerate(i71))}
    for t in T.TIZIMLAR:
        assert r1[t]['aynan_norm'] == et['tarjimon']['T1']['aynan_soni'][t], f'{t}: etalon_tekshir aynan bilan teng emas'
    R['1_T1_ga_nisbatan'] = {'tizim': r1, 'n_gap': len(i71), 'bosh_gap': [i for i in b_id if not t1.get(i)],
                             'eng_yaqin_ikki_bleu': sorted(T.TIZIMLAR, key=lambda t: -r1[t]['bleu'])[:2],
                             'eng_yaqin_ikki_chrf2': sorted(T.TIZIMLAR, key=lambda t: -r1[t]['chrf2'])[:2]}

    # 2. FLORES etaloniga aynan / deyarli
    def mos(pairs):
        out = {}
        for t in T.TIZIMLAR:
            ay = de = 0
            for key, rf in pairs:
                h = chiq[t][key]
                a = n(h) == n(rf)
                d = T._CHRF.sentence_score(h, [rf]).score >= 95 and T.gap_bleu(h, [rf]) >= 90
                ay += a
                de += a or d
            out[t] = {'aynan_norm': ay, 'deyarli_jami': de, 'aynan_xom': sum(chiq[t][key] == rf for key, rf in pairs)}
        return {'n': len(pairs), 'tizim': out}
    R['2_FLORES_moslik'] = {'mezon': "aynan: norm_tok bo'yicha teng; deyarli: aynan YOKI (gap-chrF2 >= 95 VA gap-BLEU exp >= 90)",
                            'A-qavat (400)': mos([(('a_qavat', r['id']), r['en_ref']) for r in A]),
                            'B-FLORES (36)': mos([(('eval72', i), ref[i]) for i in b_id if lay[i] == 'flores'])}

    # 3. H4 dan
    h4 = nat['jadvallar'][[k for k in nat['jadvallar'] if k.startswith('H4') and 'ASOSIY' in k][0]]
    R['3_tizim_ichida_rho'] = {'manba': 'natija/tahlil_natija.json H4 ASOSIY 71, «tizim ichida: X»',
                               'tizim': {t: h4[f'tizim ichida: {t}'] for t in ('KKT',) + NEY}}

    # baholar
    kb = kbt['elementlar']
    bh = {}
    for x in ('B', 'C', 'D'):
        q = T.oqi_xlsx(SIKL / 'qaytgan' / f'baho_{x}.xlsx', ('Element', 'Adequacy', 'Fluency'))
        bh[x] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in q}
    qE, _ = T.e_xom(SIKL)
    bh['E'] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in qE}
    eids = sorted(e for e in kb if kb[e]['id'] not in T.CHIQ7)

    # 4. α matritsasi
    toplam = {'B,C,D': 'BCD', 'B,C,D,E': 'BCDE', 'C,D (B siz)': 'CD', 'B,D (C siz)': 'BD', 'B,C (D siz)': 'BC',
              'B,E': 'BE', 'C,E': 'CE', 'D,E': 'DE'}
    qism = {'hammasi': lambda e: True, 'KKT': lambda e: kb[e]['tizim'] == 'KKT', 'neyron': lambda e: kb[e]['tizim'] != 'KKT'}
    qatlam = {'hammasi': lambda e: True, **{L: (lambda L: lambda e: lay[kb[e]['id']] == L)(L) for L in ('flores', 'train', 'gold')}}
    M = {}
    for tn, ish in toplam.items():
        for qn, qf in qism.items():
            for ln, lf in qatlam.items():
                ee = [e for e in eids if qf(e) and lf(e)]
                for d, k, _ in DAR:
                    u = [[bh[x][e][k] for x in ish if bh[x][e][k] is not None] for e in ee]
                    M.setdefault(tn, {}).setdefault(qn, {}).setdefault(ln, {})[d] = {
                        'alfa': T.kripp_alpha_ordinal(u), 'element': len(ee),
                        'qiymatlar': sorted({v for w in u if len(w) >= 2 for v in w})}
    for tn, jd in (('B,C,D', nat['jadvallar']), ('B,C,D,E', nat['inson_E_bilan']['jadvallar'])):
        h7 = jd[[k for k in jd if k.startswith('H7') and 'ASOSIY' in k][0]]
        for d, _, hk in DAR:
            assert abs(M[tn]['hammasi']['hammasi'][d]['alfa'] - h7[hk]) < 1e-9, f'{tn} {d}: H7 ASOSIY bilan teng emas'
    R['4_alfa'] = {'element_toplami': 'ASOSIY 71 (355 element)', 'matritsa': M,
                   'nan_kataklar': [f'{a} · {b} · {c} · {d}: qiymatlar {z["qiymatlar"]}' for a, v in M.items() for b, w in v.items()
                                    for c, u in w.items() for d, z in u.items() if z['alfa'] != z['alfa']],
                   'nan_sabab': "α aniqlanmaydi: juftlangan baholarda bitta qiymat — kutilgan nomuvofiqlik De = 0 (0/0); katak bo'sh emas, "
                                "ta'rif bo'yicha hisoblanmaydi"}

    # 5. o'z ≥ 4,5 to'plami
    r5 = {}
    for x in ('B', 'C', 'D', 'E'):
        ee = [e for e in eids if bh[x][e][0] is not None and bh[x][e][0] >= 4.5]
        k = T.korpus([chiq[kb[e]['tizim']][('eval72', kb[e]['id'])] for e in ee], [[ref[kb[e]['id']] for e in ee]])
        r5[x] = {'n': len(ee), 'bleu_1ref': k['bleu'], 'chrf2_1ref': k['chrf2'],
                 'tizim_n': {t: sum(kb[e]['tizim'] == t for e in ee) for t in T.TIZIMLAR}}
    R['5_oz_4_5'] = {'izoh': "baholovchi bali butun son, shuning uchun ≥ 4,5 = 5; ASOSIY 71", 'baholovchi': r5}

    # 6. faktlar (tekshiruv hisoblari)
    i55 = [i for i in b_id if not t1.get(i)][0]
    h55 = chiq['Claude'][('eval72', i55)]
    s_none = T._BLEU._extract_corpus_statistics([h55], [[ref[i55]], [None]])
    s_one = T._BLEU._extract_corpus_statistics([h55], [[ref[i55]]])
    b_r3 = sacrebleu.metrics.BLEU(tokenize='13a')
    c_r3 = sacrebleu.metrics.CHRF()
    hh = [chiq['KKT'][('eval72', i)] for i in b_id]
    rr = [[ref[i] for i in b_id], [t1.get(i) for i in b_id]]
    b_r3.corpus_score(hh, rr)
    c_r3.corpus_score(hh, rr)
    R['6_faktlar'] = {
        'a_55_gap': {'gap': i55, 'r3_dagi_qiymat': 'None (T1 etaloni yo\'q)',
                     'sacrebleu': "_cache_references: «lines = [x for x in refs if x is not None]» — None tashlanadi; shu gap 1 etalon "
                                  "(asl) bilan; bo'sh satr ham, asl takrori ham EMAS",
                     'tekshiruv_statistika_teng': s_none == s_one,
                     'haqiqiy_signatura_bleu': str(b_r3.get_signature()), 'haqiqiy_signatura_chrf': str(c_r3.get_signature()),
                     'comet': "comet_qoshimcha.py: T1 etaloni yo'q gap T1 ballidan tashlanadi (T1_n = 71)"},
        'b_gap_bleu_smoothing': "sacrebleu.sentence_bleu(h, refs, smooth_method='exp') — smooth_value None, use_effective_order True "
                                "(sacreBLEU 2.6.0 sukutlari); korpus-BLEU ham smooth:exp (signatura)",
        'c_darvoza': "prereg §2.5 (c): «ketma-ket bir xil (adequacy, fluency) juftligi qatori ≥ 12 bo'lsa belgilanadi»; tahlil.darvoza: "
                     "c_belgi = eng >= 12 — 12 ning o'zi belgilanadi (13 dan emas)",
        'd_etalon_aynan': {'T1_aynan_soni': et['tarjimon']['T1']['aynan_soni'], 'max_tizim': max(et['tarjimon']['T1']['aynan_soni'],
                                                                                            key=et['tarjimon']['T1']['aynan_soni'].get)},
        'e_iyul_2_38_2_35': "ombordan topilmadi (asosiy ombordagi tahlil va baholash papkalari, git tarixi, Desktop hujjatlari) — manba kerak"}
    (CHIQ / 'taqriz_qoshimcha.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    md(R)
    print('qoshimcha/: taqriz_qoshimcha.json, .md')


def md(R):
    f = lambda v: 'nan' if v != v else f'{v:.3f}'
    f2 = lambda v: f'{v:.2f}'
    L = ['# TOLQIN-2 — taqriz uchun qo\'shimcha (taqriz_qoshimcha.py)', '', f"**{R['maqom']}**.", '',
         f"## 1. Faqat T1 ga nisbatan ({R['1_T1_ga_nisbatan']['n_gap']} gap; bo'sh: {', '.join(R['1_T1_ga_nisbatan']['bosh_gap'])})", '',
         '| tizim | BLEU | chrF2 | aynan (xom) | aynan (norm) |', '|---|---|---|---|---|']
    for t, v in R['1_T1_ga_nisbatan']['tizim'].items():
        L.append(f"| {t} | {f2(v['bleu'])} | {f2(v['chrf2'])} | {v['aynan_xom']} | {v['aynan_norm']} |")
    L += ['', f"Eng yaqin ikki: BLEU — {', '.join(R['1_T1_ga_nisbatan']['eng_yaqin_ikki_bleu'])}; chrF2 — "
          f"{', '.join(R['1_T1_ga_nisbatan']['eng_yaqin_ikki_chrf2'])}.", '',
          '## 2. FLORES etaloniga moslik', '', R['2_FLORES_moslik']['mezon'], '',
          '| tizim | A (400): aynan | A: deyarli (jami) | B-FLORES (36): aynan | B-FLORES: deyarli (jami) |', '|---|---|---|---|---|']
    a, b = R['2_FLORES_moslik']['A-qavat (400)']['tizim'], R['2_FLORES_moslik']['B-FLORES (36)']['tizim']
    for t in a:
        L.append(f"| {t} | {a[t]['aynan_norm']} | {a[t]['deyarli_jami']} | {b[t]['aynan_norm']} | {b[t]['deyarli_jami']} |")
    L += ['', '## 3. Tizim ichida ρ(gap-BLEU_1ref, adequacy) — H4 ASOSIY 71', '', '| tizim | n | ρ | 95 % CI |', '|---|---|---|---|']
    for t, v in R['3_tizim_ichida_rho']['tizim'].items():
        L.append(f"| {t} | {v['n']} | {f(v['spearman'])} | [{f(v['ci95'][0])}; {f(v['ci95'][1])}] |")
    L += ['', '## 4. Krippendorff α (ordinal), ASOSIY 71 — mazmun / ravonlik', '',
          '| baholovchilar | qism | hammasi | flores | train | gold |', '|---|---|---|---|---|---|']
    for tn, v in R['4_alfa']['matritsa'].items():
        for qn, w in v.items():
            L.append(f'| {tn} | {qn} | ' + ' | '.join(f"{f(w[ln]['mazmun']['alfa'])} / {f(w[ln]['ravonlik']['alfa'])}"
                                                      for ln in ('hammasi', 'flores', 'train', 'gold')) + ' |')
    L += ['', f"Element soni (hammasi / KKT / neyron × hammasi, flores, train, gold): "
          + '; '.join(f"{qn}: " + ', '.join(str(w[ln]['mazmun']['element']) for ln in ('hammasi', 'flores', 'train', 'gold'))
                      for qn, w in R['4_alfa']['matritsa']['B,C,D'].items()) + '.',
          f"nan kataklar: {'; '.join(R['4_alfa']['nan_kataklar']) or 'yo‘q'}. {R['4_alfa']['nan_sabab']}.", '',
          '## 5. Har baholovchining o\'z ≥ 4,5 (= 5) to\'plami — mazmun, ASOSIY 71', '',
          '| baholovchi | n | BLEU (1 etalon) | chrF2 | ' + ' | '.join(R['5_oz_4_5']['baholovchi']['B']['tizim_n']) + ' |', '|---|---|---|---|' + '---|' * 5]
    for x, v in R['5_oz_4_5']['baholovchi'].items():
        L.append(f"| {x} | {v['n']} | {f2(v['bleu_1ref'])} | {f2(v['chrf2_1ref'])} | " + ' | '.join(str(c) for c in v['tizim_n'].values()) + ' |')
    F = R['6_faktlar']
    L += ['', '## 6. Faktlar', '',
          f"(a) 55-gap ({F['a_55_gap']['gap']}): r3 da {F['a_55_gap']['r3_dagi_qiymat']}. {F['a_55_gap']['sacrebleu']}. "
          f"Tekshiruv (None bilan = 1 etalon statistikasi): {F['a_55_gap']['tekshiruv_statistika_teng']}. Haqiqiy signatura: "
          f"`{F['a_55_gap']['haqiqiy_signatura_bleu']}`, `{F['a_55_gap']['haqiqiy_signatura_chrf']}`. {F['a_55_gap']['comet']}.",
          f"(b) {F['b_gap_bleu_smoothing']}.", f"(c) {F['c_darvoza']}.",
          f"(d) etalon_tekshir T1 aynan soni: {F['d_etalon_aynan']['T1_aynan_soni']} — 6 ta {F['d_etalon_aynan']['max_tizim']} niki.",
          f"(e) {F['e_iyul_2_38_2_35']}."]
    (CHIQ / 'taqriz_qoshimcha.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
