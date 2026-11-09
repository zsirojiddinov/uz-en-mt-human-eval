# -*- coding: utf-8 -*-
"""TOLQIN-2 — Q15 / tuzatish 14: yozuv tuzatishlari bilan birga taqriz-asosli tahlillar. NATIJADAN KEYINGI, 2026-11-07.
Barcha natija EXPLORATORY. Muzlatilgan tahlil.py / etalon_tekshir.py ga tegmaydi (import qilinadi). natija/ va etalon/ faqat
O'QILADI (sha256 MANIFEST bilan, yurishdan oldin va keyin).

    ~/.venvs/tolqin2_comet/bin/python analysis/tolqin-2/qoshimcha/tuzatish14/t14.py   # Q15_natija.json mavjud bo'lsa TO'XTAYDI

1. T1 bor 71 gapda juftlashgan o'sishlar (asl+T1 − asl), 5 tizim, 95 % juftlashgan bootstrap (gap qayta tanlash, 10 000).
2. Kendall W: har tizim ichida (71 gap) B, C, D ning mazmun va ravonlik tartibi (bog'lanish tuzatishi bilan); yo'q katakli gap
   shu tizim/o'lchovda chiqariladi; gap bootstrap 95 % persentil.
3. α tekshiruvi: tahlil.kripp_alpha_ordinal Krippendorff (2011) nashr etilgan namunasi bilan (ordinal α = 0,815) va sintetik
   holatlar bilan — test_alfa.py da. (krippendorff PyPI paketi bilan solishtirish BAJARILMADI — 6-bandga qarang.)
4. etalon_tekshir.py «farq_1_2» mezoni: metrika, yo'nalish, signatura; 5,51 qayta hisoblanadi (assert); T1-only korpus BLEU
   farqi bilan solishtiriladi.
5. Ilmiy qatlam (train, 24 gap): har tizim chiqishining nashr etilgan inglizcha annotatsiya etaloni bilan aynan / deyarli
   (gap-chrF2 ≥ 95 VA gap-BLEU exp ≥ 90) mosligi — taqriz_qoshimcha 2-band mezoni.
Chiqish: qoshimcha/tuzatish14/Q15_natija.json, Q15_natija.md.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import sacrebleu
import scipy
from sacrebleu.metrics import CHRF

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parents[1]
SEED, NB = 20261106, 10_000
NEY = ('Gemini', 'Claude', 'GPT', 'GT')
MUZLATILGAN = {
    'natija/tahlil_natija.json': '24ff6007c7b7b0addbbd325174116d4d40eb1a0bf6f3f6d1778a1af707ef23d0',
    'natija/tahlil_natija.md': '1145540c73b7e5d7675c3179e5da6ea687fec63333da78b485b34c39843dfb8d',
    'natija/comet_natija.json': '062bd1f6bde715e6bed566ce6fd38855ec1fe7284cdd938e45a772596eefa4d4',
    'etalon/etalon_tekshir.json': 'a6c03c1188f6e90396193fabcd0fab75aad97c46328d8c317773de36dd31002b',
}


def _mod(nom, ild=SIKL):
    sp = importlib.util.spec_from_file_location(f'{nom}_m14', str(ild / f'{nom}.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _mod('tahlil')
EK = _mod('ekspozitsiya_2')
PB = _mod('paket_baho')
nrm = lambda s: ' '.join(EK.norm_tok(s))


def sha_tekshir():
    for p, h in MUZLATILGAN.items():
        assert hashlib.sha256((SIKL / p).read_bytes()).hexdigest() == h, f"{p}: sha256 MANIFEST bilan teng emas — TO'XTA"


def stat_arr(h, refs):
    return np.array(T.bleu_stat(h, refs), dtype=float)


def ball(s):
    return T._BLEU._compute_score_from_stats([float(x) for x in s]).score


def kendall_w(M):
    """M: (n obyekt, m baholovchi) ballar. Har baholovchi ichida o'rtacha rang; bog'lanish tuzatishi bilan W."""
    n, m = M.shape
    R = np.column_stack([T.rang(list(M[:, j])) for j in range(m)])
    S = ((R.sum(1) - m * (n + 1) / 2) ** 2).sum()
    tie = 0.0
    for j in range(m):
        _, c = np.unique(M[:, j], return_counts=True)
        tie += (c ** 3 - c).sum()
    den = m ** 2 * (n ** 3 - n) - m * tie
    return float(12 * S / den) if den else float('nan')


def main():
    if (CHIQ / 'Q15_natija.json').exists():
        sys.exit("TO'XTA: tuzatish14/Q15_natija.json mavjud — bir marta yuriladi")
    assert sacrebleu.__version__ == '2.6.0'
    sha_tekshir()
    A, B, chiq, Tr, kbt, xom, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    b_id = [r['id'] for r in B]
    ref = {r['id']: r['ref_en'] for r in B}
    lay = {r['id']: r['layer'] for r in B}
    t1 = Tr['T1']
    h = lambda t, ids: [chiq[t][('eval72', i)] for i in ids]
    R = {'maqom': "natijadan keyingi, taqriz-asosli (2-davr taqrizlari, 2026-11-06); EXPLORATORY; natija/ va etalon/ o'zgarmagan",
         'muhit': {'sacrebleu': sacrebleu.__version__, 'numpy': np.__version__, 'scipy': scipy.__version__,
                   'python': sys.version.split()[0]}, 'seed': SEED, 'qayta_tanlash': NB}

    # 1. 71 gapda juftlashgan o'sish
    i71 = [i for i in b_id if t1.get(i)]
    assert len(i71) == 71
    rng = np.random.default_rng(SEED)
    W = np.stack([np.bincount(rng.integers(0, 71, 71), minlength=71) for _ in range(NB)]).astype(float)
    r1 = {}
    for t in T.TIZIMLAR:
        s1 = stat_arr(h(t, i71), [[ref[i] for i in i71]])
        s2 = stat_arr(h(t, i71), [[ref[i] for i in i71], [t1[i] for i in i71]])
        d0 = ball(s2.sum(0)) - ball(s1.sum(0))
        v = np.array([ball(w @ s2) - ball(w @ s1) for w in W])
        r1[t] = {'asl': ball(s1.sum(0)), 'asl+T1': ball(s2.sum(0)), 'delta': d0,
                 'ci95': [float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))]}
    q13 = json.loads((SIKL / 'qoshimcha/tuzatish13/Q13_natija.json').read_text(encoding='utf-8'))
    for t in T.TIZIMLAR:
        assert abs(r1[t]['delta'] - q13['1_T1_sezgirlik']['a_same71']['delta_aslT1_minus_asl'][t]) < 1e-9, f'{t}: Q13 1a bilan teng emas'
    R['1_juftlashgan_71'] = {'n': 71, 'izoh': "95 % persentil, juftlashgan gap bootstrap; nuqtaviy qiymat = Q13 1a (assert)", 'tizim': r1}

    # 2. Kendall W
    kb = kbt['elementlar']
    bh = {x: {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in xom[x]} for x in ('B', 'C', 'D')}
    eids = [e for e in sorted(kb) if kb[e]['id'] not in T.CHIQ7]
    rng2 = np.random.default_rng(SEED)
    kw = {}
    for t in T.TIZIMLAR:
        ee = [e for e in eids if kb[e]['tizim'] == t]
        for d, k in (('mazmun', 0), ('ravonlik', 1)):
            e2 = [e for e in ee if all(bh[x][e][k] is not None for x in 'BCD')]
            M = np.array([[bh[x][e][k] for x in 'BCD'] for e in e2], dtype=float)
            w0 = kendall_w(M)
            n = len(e2)
            v = np.array([kendall_w(M[rng2.integers(0, n, n)]) for _ in range(NB)])
            v = v[~np.isnan(v)]
            kw.setdefault(t, {})[d] = {'n': n, 'W': w0, 'ci95': [float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))],
                                       'chiqarilgan_yoq_katak': len(ee) - n}
    R['2_kendall_W'] = {'izoh': "B, C, D; ASOSIY 71; har tizim ichida gap tartibi; o'rtacha rang, bog'lanish tuzatishi; gap bootstrap 95 %",
                        'tizim': kw}

    # 3. α tekshiruvi (test_alfa.py bilan bir xil holatlar)
    TA = _mod('test_alfa', CHIQ)
    R['3_alfa_tekshiruv'] = TA.hammasi(T.kripp_alpha_ordinal)

    # 4. etalon_tekshir «farq_1_2»
    et = json.loads((SIKL / 'etalon' / 'etalon_tekshir.json').read_text(encoding='utf-8'))['tarjimon']['T1']
    ch = PB.chiqishlar()
    chrf = CHRF()
    ids = sorted(t1)
    cf = {t: sum(chrf.sentence_score(t1[i], [ch[t][i]]).score for i in ids) / len(ids) for t in PB.TIZIMLAR}
    tart = sorted(cf, key=cf.get, reverse=True)
    for t in PB.TIZIMLAR:
        assert abs(cf[t] - et['chrf_ortacha'][t]) < 1e-9, f'{t}: chrF etalon_tekshir bilan teng emas'
    b_t1 = {t: T._BLEU.corpus_score(h(t, i71), [[t1[i] for i in i71]]).score for t in T.TIZIMLAR}
    R['4_etalon_tekshir_mezoni'] = {
        'metrika': "o'rtacha gap-chrF2 (sacreBLEU CHRF sukut: char_order 6, word_order 0, beta 2), 71 gap",
        'yonalish': "hyp = T1 tarjimasi, ref = tizim chiqishi (etalon_tekshir.py: chrf.sentence_score(T[x][i], [ch[t][i]]))",
        'signatura': str(chrf.get_signature()), 'chrf_ortacha': cf, 'eng_yaqin': tart[0], 'ikkinchi': tart[1],
        'farq_1_2': cf[tart[0]] - cf[tart[1]], 'etalon_tekshir_farq_1_2': et['farq_1_2'],
        'T1_only_korpus_BLEU': b_t1, 'T1_only_BLEU_GPT_minus_GT': b_t1['GPT'] - b_t1['GT'],
        'T1_only_BLEU_GPT_minus_Gemini': b_t1['GPT'] - b_t1['Gemini'],
        'izoh': "ikki kattalik turli: (i) o'rtacha gap-chrF, hyp = T1; (ii) korpus BLEU, hyp = tizim, ref = T1. "
                "chrF bo'yicha ikkinchi eng yaqin tizim — Gemini (GT emas)"}
    assert abs(R['4_etalon_tekshir_mezoni']['farq_1_2'] - et['farq_1_2']) < 1e-9

    # 5. ilmiy qatlam (train 24)
    tr = [i for i in b_id if lay[i] == 'train']
    assert len(tr) == 24
    m5 = {}
    for t in T.TIZIMLAR:
        ay = de = axom = 0
        for i in tr:
            hh, rf = chiq[t][('eval72', i)], ref[i]
            a = nrm(hh) == nrm(rf)
            d = T._CHRF.sentence_score(hh, [rf]).score >= 95 and T.gap_bleu(hh, [rf]) >= 90
            ay += a
            de += a or d
            axom += hh == rf
        m5[t] = {'aynan_norm': ay, 'deyarli_jami': de, 'aynan_xom': axom}
    R['5_ilmiy_qatlam_moslik'] = {'n': 24, 'etalon': "ref_en (inlibrary.uz nashr etilgan inglizcha annotatsiya, gap darajasida)",
                                  'mezon': "aynan: norm_tok bo'yicha teng; deyarli: aynan YOKI (gap-chrF2 >= 95 VA gap-BLEU exp >= 90)",
                                  'tizim': m5}
    R['6_bajarilmagan'] = ("3-band: krippendorff PyPI paketi bilan solishtirish bajarilmadi — paketni o'rnatish sessiyada ruxsat "
                           "etilmadi (2026-11-07). O'rniga Krippendorff (2011) nashr etilgan namunasi (ordinal α = 0,815) va "
                           "sintetik holatlar bilan tekshirildi.")

    (CHIQ / 'Q15_natija.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    md(R)
    sha_tekshir()
    print('tuzatish14/: Q15_natija.json, Q15_natija.md')


def md(R):
    f2 = lambda v: f'{v:.2f}'
    f3 = lambda v: 'nan' if v != v else f'{v:.3f}'
    ci = lambda c, f=f3: f'[{f(c[0])}; {f(c[1])}]'
    L = ['# TOLQIN-2 — Q15 natijalari (t14.py)', '', f"**{R['maqom']}**.", '',
         f"Muhit: sacreBLEU {R['muhit']['sacrebleu']}, numpy {R['muhit']['numpy']}, scipy {R['muhit']['scipy']}, Python "
         f"{R['muhit']['python']}. Seed {R['seed']}, {R['qayta_tanlash']} qayta tanlash.", '',
         '## 1. T1 bor 71 gap: juftlashgan o\'sish (asl+T1 − asl)', '', R['1_juftlashgan_71']['izoh'] + '.', '',
         '| tizim | asl | asl+T1 | Δ | 95 % |', '|---|---|---|---|---|']
    for t, v in R['1_juftlashgan_71']['tizim'].items():
        L.append(f"| {t} | {f2(v['asl'])} | {f2(v['asl+T1'])} | {f2(v['delta'])} | {ci(v['ci95'], f2)} |")
    L += ['', '## 2. Kendall W (B, C, D; tizim ichida)', '', R['2_kendall_W']['izoh'] + '.', '',
          '| tizim | o\'lchov | n | W | 95 % | chiqarilgan (yo\'q katak) |', '|---|---|---|---|---|---|']
    for t, v in R['2_kendall_W']['tizim'].items():
        for d, w in v.items():
            L.append(f"| {t} | {d} | {w['n']} | {f3(w['W'])} | {ci(w['ci95'])} | {w['chiqarilgan_yoq_katak']} |")
    L += ['', '## 3. α implementatsiyasi tekshiruvi', '', '| holat | kutilgan | hisoblangan | o\'tdi |', '|---|---|---|---|']
    for c in R['3_alfa_tekshiruv']:
        L.append(f"| {c['holat']} | {c['kutilgan']} | {f3(c['hisoblangan'])} | {'ha' if c['otdi'] else 'YO‘Q'} |")
    E = R['4_etalon_tekshir_mezoni']
    L += ['', '## 4. etalon_tekshir «farq_1_2» mezoni', '', f"Metrika: {E['metrika']}. Yo'nalish: {E['yonalish']}. Signatura: "
          f"`{E['signatura']}`.", '', '| tizim | o\'rtacha gap-chrF2 (hyp T1) | T1-only korpus BLEU (hyp tizim) |', '|---|---|---|']
    for t in E['chrf_ortacha']:
        L.append(f"| {t} | {f2(E['chrf_ortacha'][t])} | {f2(E['T1_only_korpus_BLEU'][t])} |")
    L += ['', f"Eng yaqin: {E['eng_yaqin']}; ikkinchi: {E['ikkinchi']}; farq_1_2 = {f2(E['farq_1_2'])} (etalon_tekshir: "
          f"{f2(E['etalon_tekshir_farq_1_2'])}). T1-only BLEU: GPT − GT = {f2(E['T1_only_BLEU_GPT_minus_GT'])}; GPT − Gemini = "
          f"{f2(E['T1_only_BLEU_GPT_minus_Gemini'])}. {E['izoh']}.", '',
          f"## 5. Ilmiy qatlam (train, {R['5_ilmiy_qatlam_moslik']['n']} gap) — etalon bilan moslik", '',
          f"Etalon: {R['5_ilmiy_qatlam_moslik']['etalon']}. Mezon: {R['5_ilmiy_qatlam_moslik']['mezon']}.", '',
          '| tizim | aynan (norm) | deyarli (jami) | aynan (xom) |', '|---|---|---|---|']
    for t, v in R['5_ilmiy_qatlam_moslik']['tizim'].items():
        L.append(f"| {t} | {v['aynan_norm']} | {v['deyarli_jami']} | {v['aynan_xom']} |")
    L += ['', '## 6. Bajarilmagan', '', R['6_bajarilmagan']]
    (CHIQ / 'Q15_natija.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
