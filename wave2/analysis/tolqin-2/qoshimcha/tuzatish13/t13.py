# -*- coding: utf-8 -*-
"""TOLQIN-2 — Q13 / tuzatish 13: taqriz-asosli sezgirlik tahlillari. NATIJADAN KEYINGI, TAQRIZGA JAVOB, 2026-11-06.
Barcha natija EXPLORATORY. Muzlatilgan tahlil.py ga tegmaydi — undan yukla(), korpus(), gap_bleu(), spearman(),
kripp_alpha_ordinal(), oqi_xlsx(), bleu_stat(), _BLEU, CHIQ7, TIZIMLAR import qilinadi; normallashtirish — ekspozitsiya_2.norm_tok.
natija/ va etalon/ faqat O'QILADI (sha256 MANIFEST qiymatlari bilan tekshiriladi).

    ~/.venvs/tolqin2_comet/bin/python analysis/tolqin-2/qoshimcha/tuzatish13/t13.py   # Q13_natija.json mavjud bo'lsa TO'XTAYDI

sacreBLEU 2.6.0 (signaturalar §3.5: BLEU nrefs:1|var, case:mixed, eff:no, tok:13a, smooth:exp; chrF2). Bootstrap seed 20261106,
10 000 qayta tanlash, birlik — gap (gap-klaster: bir gapning 5 elementi birga).

1. T1 sezgirligi (T1 bor 71 gap): (a) asl / asl+T1 / faqat T1 — 5 tizim korpus BLEU va neyron reyting; (b) biror tizim chiqishi bilan
   aynan (norm_tok) bir xil T1 gaplari; (c) shu gaplarsiz uchala shart; (d) leave-one-sentence-out (asl+T1, 4 neyron tartibi).
2. P1 beshta o'sishi (asl+T1 − asl, 72 gap; prereg P1 ta'rifi) uchun Bonferroni 99 % juftlashgan bootstrap oraliqlari (persentil).
3. BCa 95 % (scipy.stats.bootstrap, method='BCa'): panel α (B,C,D; ASOSIY 71; mazmun, ravonlik) va 4 tizim-ichi ρ.
4. Pooled neyron ρ (284 element, KKT siz) gap-BLEU_1ref vs B,C,D mazmun o'rtachasi, 95 % persentil; η² (bir omilli, tizim).
5. Ravonlik (va mazmun) juftlik ρ: B–C, C–D (B–D ham), KKT ichida va neyron ichida (SEZGIRLIK 72).
6. α implementatsiyasi tavsifi.
Chiqish: qoshimcha/tuzatish13/Q13_natija.json, Q13_natija.md.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import sacrebleu
import scipy
from scipy import stats

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parents[1]
SEED, NB = 20261106, 10_000
NEY = ('Gemini', 'Claude', 'GPT', 'GT')
MUZLATILGAN = {  # MANIFEST (Q2, 93111a5) qiymatlari
    'natija/tahlil_natija.json': '24ff6007c7b7b0addbbd325174116d4d40eb1a0bf6f3f6d1778a1af707ef23d0',
    'natija/tahlil_natija.md': '1145540c73b7e5d7675c3179e5da6ea687fec63333da78b485b34c39843dfb8d',
    'natija/comet_natija.json': '062bd1f6bde715e6bed566ce6fd38855ec1fe7284cdd938e45a772596eefa4d4',
    'etalon/etalon_tekshir.json': 'a6c03c1188f6e90396193fabcd0fab75aad97c46328d8c317773de36dd31002b',
}


def _mod(nom):
    sp = importlib.util.spec_from_file_location(f'{nom}_m', str(SIKL / f'{nom}.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


T = _mod('tahlil')
EK = _mod('ekspozitsiya_2')
nrm = lambda s: ' '.join(EK.norm_tok(s))


def sha_tekshir():
    for p, h in MUZLATILGAN.items():
        assert hashlib.sha256((SIKL / p).read_bytes()).hexdigest() == h, f'{p}: sha256 MANIFEST bilan teng emas — TO\'XTA'


def bleu(h, refs):
    return T._BLEU.corpus_score(h, refs).score


def reyting(d):
    return sorted(NEY, key=lambda t: -d[t])


def stat_arr(h, refs):
    return np.array(T.bleu_stat(h, refs), dtype=float)


def ball(st_sum):
    return T._BLEU._compute_score_from_stats([float(x) for x in st_sum]).score


def main():
    if (CHIQ / 'Q13_natija.json').exists():
        sys.exit("TO'XTA: tuzatish13/Q13_natija.json mavjud — bir marta yuriladi")
    assert sacrebleu.__version__ == '2.6.0', sacrebleu.__version__
    sha_tekshir()
    A, B, chiq, Tr, kbt, xom, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))
    J = nat['jadvallar']
    jk = lambda pre, tag: J[[k for k in J if k.startswith(pre) and tag in k][0]]
    b_id = [r['id'] for r in B]
    ref = {r['id']: r['ref_en'] for r in B}
    t1 = Tr['T1']
    h = lambda t, ids: [chiq[t][('eval72', i)] for i in ids]
    R = {'maqom': "natijadan keyingi, taqriz-asosli (Gemini 3 Pro va ChatGPT taqrizlari, 2026-11-06); EXPLORATORY; muzlatilgan "
                  "natija/ va etalon/ fayllari o'zgarmagan",
         'muhit': {'sacrebleu': sacrebleu.__version__, 'numpy': np.__version__, 'scipy': scipy.__version__,
                   'python': sys.version.split()[0]},
         'seed': SEED, 'qayta_tanlash': NB}

    # ---------------------------------------------------------------- 1. T1 sezgirligi
    i71 = [i for i in b_id if t1.get(i)]
    assert len(i71) == 71

    def uch_shart(ids):
        out = {}
        for nom, rr in (('asl', [[ref[i] for i in ids]]), ('asl+T1', [[ref[i] for i in ids], [t1[i] for i in ids]]),
                        ('faqat_T1', [[t1[i] for i in ids]])):
            d = {t: bleu(h(t, ids), rr) for t in T.TIZIMLAR}
            out[nom] = {'bleu': d, 'neyron_reyting': reyting(d)}
        out['delta_aslT1_minus_asl'] = {t: out['asl+T1']['bleu'][t] - out['asl']['bleu'][t] for t in T.TIZIMLAR}
        out['n'] = len(ids)
        return out

    a = uch_shart(i71)
    ayn = []
    for i in i71:
        ts = [t for t in T.TIZIMLAR if nrm(chiq[t][('eval72', i)]) == nrm(t1[i])]
        if ts:
            ayn.append({'id': i, 'tizimlar': ts, 'aynan_xom': [t for t in ts if chiq[t][('eval72', i)] == t1[i]]})
    et = json.loads((SIKL / 'etalon' / 'etalon_tekshir.json').read_text(encoding='utf-8'))['tarjimon']['T1']['aynan_soni']
    for t in T.TIZIMLAR:
        assert sum(t in x['tizimlar'] for x in ayn) == et[t], f'{t}: aynan soni etalon_tekshir bilan teng emas'
    ayn_set = {x['id'] for x in ayn}
    c = uch_shart([i for i in i71 if i not in ayn_set])
    # (d) leave-one-sentence-out
    st = {t: stat_arr(h(t, i71), [[ref[i] for i in i71], [t1[i] for i in i71]]) for t in NEY}
    tot = {t: st[t].sum(0) for t in NEY}
    to_liq = {t: ball(tot[t]) for t in NEY}
    assert all(abs(to_liq[t] - a['asl+T1']['bleu'][t]) < 1e-9 for t in NEY)
    r0 = reyting(to_liq)
    ozgargan = []
    for k, i in enumerate(i71):
        d = {t: ball(tot[t] - st[t][k]) for t in NEY}
        r = reyting(d)
        if r != r0:
            pos0 = {t: j for j, t in enumerate(r0)}
            jf = sorted({tuple(sorted((x, y))) for x in NEY for y in NEY if x != y
                         and (pos0[x] < pos0[y]) != (r.index(x) < r.index(y))})
            ozgargan.append({'tashlangan_gap': i, 'reyting': r, 'almashgan_juftlik': [f'{x}–{y}' for x, y in jf]})
    R['1_T1_sezgirlik'] = {
        'a_same71': a,
        'b_aynan_T1_gaplari': {'mezon': 'ekspozitsiya_2.norm_tok bo\'yicha teng (etalon_tekshir.py dagidek)', 'gaplar': ayn,
                               'noyob_gap_soni': len(ayn_set), 'tizim_boyicha': {t: et[t] for t in T.TIZIMLAR}},
        'c_minus_overlap': c,
        'd_leave_one_out': {'asos_reyting_aslT1': r0, 'tashlashlar': 71, 'reyting_ozgargan_soni': len(ozgargan),
                            'ozgarishlar': ozgargan}}

    # ---------------------------------------------------------------- 2. P1 Bonferroni 99 %
    r1 = [ref[i] for i in b_id]
    r3 = [r1, [t1.get(i) for i in b_id]]  # tuzatish 10: None = etalon yo'q (55-gap)
    p1n = jk('B2', 'P1')
    rng = np.random.default_rng(SEED)
    W = np.stack([np.bincount(rng.integers(0, 72, 72), minlength=72) for _ in range(NB)]).astype(float)
    p1 = {}
    for t in T.TIZIMLAR:
        s1, s3 = stat_arr(h(t, b_id), [r1]), stat_arr(h(t, b_id), r3)
        d0 = ball(s3.sum(0)) - ball(s1.sum(0))
        assert abs(d0 - p1n[t]['delta_bleu_3ref_minus_1ref']) < 1e-9, f'{t}: P1 Δ muzlatilgan qiymatga teng emas'
        v = np.sort(np.array([ball(w @ s3) - ball(w @ s1) for w in W]))
        p1[t] = {'delta': d0, 'ci99_bonferroni': [float(np.quantile(v, 0.005)), float(np.quantile(v, 0.995))],
                 'ci95_shu_namunadan': [float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))],
                 'nol_ichidami_99': bool(np.quantile(v, 0.005) <= 0 <= np.quantile(v, 0.995))}
    R['2_P1_bonferroni'] = {'izoh': "5 taqqoslash, oilaviy α 0,05 -> har biriga 0,01 (99 %); juftlashgan: bir xil gap qayta tanlash "
                                    "1 va 2 etalon uchun; persentil; 72 gap (prereg P1)", 'tizim': p1}

    # ---------------------------------------------------------------- baholar
    kb = kbt['elementlar']
    bh = {x: {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in xom[x]} for x in ('B', 'C', 'D')}
    hamma = sorted(kb)
    eids = [e for e in hamma if kb[e]['id'] not in T.CHIQ7]
    assert len(eids) == 355
    tiz = {e: kb[e]['tizim'] for e in hamma}
    gid = {e: kb[e]['id'] for e in hamma}
    ort = lambda e, k: (lambda v: sum(v) / len(v))([bh[x][e][k] for x in 'BCD' if bh[x][e][k] is not None])
    hm = {e: ort(e, 0) for e in hamma}
    gb = {e: T.gap_bleu(chiq[tiz[e]][('eval72', gid[e])], [ref[gid[e]]]) for e in hamma}
    g71 = sorted({gid[e] for e in eids})
    el_gap = {g: [e for e in eids if gid[e] == g] for g in g71}

    # ---------------------------------------------------------------- 3. BCa 95 %
    def bca(n, fn):
        res = stats.bootstrap((np.arange(n),), lambda ix: fn([int(i) for i in ix]), n_resamples=NB, method='BCa',
                              confidence_level=0.95, vectorized=False, random_state=np.random.default_rng(SEED))
        lo, hi = res.confidence_interval
        return [float(lo), float(hi)]

    h7 = jk('H7', 'ASOSIY')
    alfa = {}
    for d, k, hk in (('mazmun', 0, 'adequacy'), ('ravonlik', 1, 'fluency')):
        def af(ix, k=k):
            return T.kripp_alpha_ordinal([[bh[x][e][k] for x in 'BCD' if bh[x][e][k] is not None]
                                          for j in ix for e in el_gap[g71[j]]])
        a0 = af(range(71))
        assert abs(a0 - h7[hk]) < 1e-9, f'α {d}: H7 ASOSIY ga teng emas'
        alfa[d] = {'alfa': a0, 'bca95': bca(71, af)}
    h4 = jk('H4', 'ASOSIY')
    rho = {}
    for t in NEY:
        ee = [e for e in eids if tiz[e] == t]
        x, y = [gb[e] for e in ee], [hm[e] for e in ee]
        r_ = T.spearman(x, y)
        assert abs(r_ - h4[f'tizim ichida: {t}']['spearman']) < 1e-9, f'ρ {t}: H4 ga teng emas'
        rho[t] = {'n': len(ee), 'rho': r_, 'bca95': bca(len(ee), lambda ix: T.spearman([x[i] for i in ix], [y[i] for i in ix])),
                  'persentil95_H4_1000': h4[f'tizim ichida: {t}']['ci95']}
    R['3_BCa'] = {'izoh': "scipy.stats.bootstrap, method='BCa', 10 000; α — gap-klaster (71 gap, har birida 5 element); ρ — tizim "
                          "ichida har gapda bitta element, shuning uchun element = gap", 'alfa_BCD': alfa, 'tizim_ichi_rho': rho}

    # ---------------------------------------------------------------- 4. pooled neyron ρ va η²
    ne = [e for e in eids if tiz[e] != 'KKT']
    assert len(ne) == 284
    ne_gap = {g: [e for e in ne if gid[e] == g] for g in g71}

    def prho(ix):
        ee = [e for j in ix for e in ne_gap[g71[j]]]
        return T.spearman([gb[e] for e in ee], [hm[e] for e in ee])
    p0 = prho(range(71))
    rng4 = np.random.default_rng(SEED)
    v = np.array([prho(rng4.integers(0, 71, 71)) for _ in range(NB)])
    v = np.sort(v[~np.isnan(v)])

    def eta2(ee):
        y = np.array([hm[e] for e in ee])
        g = [np.array([hm[e] for e in ee if tiz[e] == t]) for t in sorted({tiz[e] for e in ee})]
        ssb = sum(len(x) * (x.mean() - y.mean()) ** 2 for x in g)
        return float(ssb / ((y - y.mean()) ** 2).sum())
    R['4_pooled_neyron'] = {'n_element': len(ne), 'n_gap': 71, 'rho': p0,
                            'persentil95_gap_klaster': [float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))],
                            'eta2_tizim': {'neyron_4_tizim_284': eta2(ne), 'hammasi_5_tizim_355': eta2(eids)},
                            'izoh': "y — B,C,D mazmun o'rtachasi (yo'q kataklar chiqarilgan); η² = SS_tizim / SS_jami"}

    # ---------------------------------------------------------------- 5. juftlik ρ (SEZGIRLIK 72)
    h6 = jk('H6', 'SEZGIRLIK')
    jf = {}
    for d, k, hk in (('ravonlik', 1, 'fluency'), ('mazmun', 0, 'adequacy')):
        for x, y in (('B', 'C'), ('C', 'D'), ('B', 'D')):
            ee_all = [e for e in hamma if bh[x][e][k] is not None and bh[y][e][k] is not None]
            r_all = T.spearman([bh[x][e][k] for e in ee_all], [bh[y][e][k] for e in ee_all])
            assert abs(r_all - h6[f'{hk}: {x}–{y}']) < 1e-9, f'{d} {x}–{y}: H6 SEZGIRLIK ga teng emas'
            for qn, qf in (('KKT', lambda e: tiz[e] == 'KKT'), ('neyron', lambda e: tiz[e] != 'KKT')):
                ee = [e for e in ee_all if qf(e)]
                jf.setdefault(d, {}).setdefault(f'{x}–{y}', {})[qn] = {
                    'n': len(ee), 'rho': T.spearman([bh[x][e][k] for e in ee], [bh[y][e][k] for e in ee])}
            jf[d][f'{x}–{y}']['hammasi_H6'] = {'n': len(ee_all), 'rho': r_all}
    R['5_juftlik_rho'] = {'element_toplami': 'SEZGIRLIK 72 (360 element; yo\'q kataklar juftlik bo\'yicha chiqarilgan)', 'jadval': jf}

    # ---------------------------------------------------------------- 6. α implementatsiyasi
    R['6_alfa_implementatsiya'] = (
        "Krippendorff α o'z kodi bilan hisoblangan (tahlil.kripp_alpha_ordinal, sof Python; tashqi paket yo'q). Birlik — element "
        "(gap × tizim chiqishi), qiymatlar — baholovchilar balli (1–5). Har birlikdagi mavjud baholar o'zaro juftlanib, "
        "koinsidensiya matritsasi 1/(m−1) vazni bilan to'planadi (m — birlikdagi baholar soni); m < 2 bo'lgan birlik tashlanadi. "
        "Masofa — ordinal (Krippendorff 2004/2011): δ²(c,k) = (Σ_{g=c..k} n_g − (n_c + n_k)/2)², n_g — qiymatning chegaraviy "
        "chastotasi. α = 1 − (n−1)·D_o / D_e. Bo'sh kataklar (B: E159, E219; D: E019) «yo'q ma'lumot» sifatida chiqariladi "
        "(tuzatish 10 (g)); juftlangan baholarda bitta qiymat qolsa D_e = 0 va α aniqlanmaydi (nan). Bootstrap (Q13, 3-band) gap "
        "darajasida qayta tanlaydi: tanlangan gapning barcha 5 elementi birga olinadi (gap-klaster), shuning uchun bir gapning "
        "tizimlar orasidagi bog'liqligi saqlanadi.")

    (CHIQ / 'Q13_natija.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    md(R)
    sha_tekshir()
    print('tuzatish13/: Q13_natija.json, Q13_natija.md')


def md(R):
    f2 = lambda v: f'{v:.2f}'
    f3 = lambda v: 'nan' if v != v else f'{v:.3f}'
    ci = lambda c, f=f3: f'[{f(c[0])}; {f(c[1])}]'
    S = R['1_T1_sezgirlik']
    L = ['# TOLQIN-2 — Q13 natijalari (t13.py)', '', f"**{R['maqom']}**.", '',
         f"Muhit: sacreBLEU {R['muhit']['sacrebleu']}, numpy {R['muhit']['numpy']}, scipy {R['muhit']['scipy']}, Python "
         f"{R['muhit']['python']}. Seed {R['seed']}, {R['qayta_tanlash']} qayta tanlash.", '']

    def jad(blok, sar):
        out = [f'### {sar} (n = {blok["n"]})', '', '| tizim | asl | asl+T1 | faqat T1 | Δ (asl+T1 − asl) |', '|---|---|---|---|---|']
        for t in T.TIZIMLAR:
            out.append(f"| {t} | {f2(blok['asl']['bleu'][t])} | {f2(blok['asl+T1']['bleu'][t])} | {f2(blok['faqat_T1']['bleu'][t])} | "
                       f"{f2(blok['delta_aslT1_minus_asl'][t])} |")
        out += ['', 'Neyron reyting: ' + '; '.join(f"{k} — {' > '.join(blok[k]['neyron_reyting'])}" for k in ('asl', 'asl+T1', 'faqat_T1')), '']
        return out
    L += ['## 1. T1 sezgirligi', ''] + jad(S['a_same71'], '1a. T1 bor 71 gap')
    b = S['b_aynan_T1_gaplari']
    L += [f"### 1b. Biror tizim chiqishi bilan aynan T1 gaplari ({b['mezon']})", '',
          f"Noyob gaplar: {b['noyob_gap_soni']}. Tizim bo'yicha: " + ', '.join(f'{t} {v}' for t, v in b['tizim_boyicha'].items()) + '.', '',
          '| gap | tizimlar (norm) | aynan xom |', '|---|---|---|']
    L += [f"| {x['id']} | {', '.join(x['tizimlar'])} | {', '.join(x['aynan_xom']) or '—'} |" for x in b['gaplar']] + ['']
    L += jad(S['c_minus_overlap'], '1c. Aynan gaplarsiz')
    d = S['d_leave_one_out']
    L += ['### 1d. Leave-one-sentence-out (asl+T1, 4 neyron)', '',
          f"Asos reyting: {' > '.join(d['asos_reyting_aslT1'])}. {d['tashlashlar']} tashlashdan reyting o'zgargani: "
          f"{d['reyting_ozgargan_soni']}.", '']
    if d['ozgarishlar']:
        L += ['| tashlangan gap | reyting | almashgan juftlik |', '|---|---|---|']
        L += [f"| {x['tashlangan_gap']} | {' > '.join(x['reyting'])} | {', '.join(x['almashgan_juftlik'])} |" for x in d['ozgarishlar']]
        L.append('')
    L += ['## 2. P1: Bonferroni 99 % juftlashgan bootstrap (72 gap)', '', R['2_P1_bonferroni']['izoh'] + '.', '',
          '| tizim | Δ | 99 % (Bonferroni) | 95 % (shu namuna) | 0 ichida (99 %) |', '|---|---|---|---|---|']
    for t, v in R['2_P1_bonferroni']['tizim'].items():
        L.append(f"| {t} | {f2(v['delta'])} | {ci(v['ci99_bonferroni'], f2)} | {ci(v['ci95_shu_namunadan'], f2)} | "
                 f"{'ha' if v['nol_ichidami_99'] else 'yo‘q'} |")
    B3 = R['3_BCa']
    L += ['', '## 3. BCa 95 %', '', B3['izoh'] + '.', '', '| kattalik | qiymat | BCa 95 % |', '|---|---|---|']
    for dn, v in B3['alfa_BCD'].items():
        L.append(f"| α (B,C,D) {dn} | {f3(v['alfa'])} | {ci(v['bca95'])} |")
    for t, v in B3['tizim_ichi_rho'].items():
        L.append(f"| ρ tizim ichida {t} (n {v['n']}) | {f3(v['rho'])} | {ci(v['bca95'])} (H4 persentil: {ci(v['persentil95_H4_1000'])}) |")
    P = R['4_pooled_neyron']
    L += ['', '## 4. Pooled neyron ρ va η²', '',
          f"ρ(gap-BLEU_1ref, mazmun o'rtachasi), {P['n_element']} element / {P['n_gap']} gap: {f3(P['rho'])}, 95 % (gap-klaster "
          f"persentil) {ci(P['persentil95_gap_klaster'])}.",
          f"η² (tizim): neyron 4 tizim (284) {f3(P['eta2_tizim']['neyron_4_tizim_284'])}; hammasi 5 tizim (355) "
          f"{f3(P['eta2_tizim']['hammasi_5_tizim_355'])}. {P['izoh']}.", '',
          f"## 5. Juftlik Spearman — {R['5_juftlik_rho']['element_toplami']}", '',
          '| o\'lchov | juftlik | KKT (n) | neyron (n) | hammasi (H6) |', '|---|---|---|---|---|']
    for dn, v in R['5_juftlik_rho']['jadval'].items():
        for jn, w in v.items():
            L.append(f"| {dn} | {jn} | {f3(w['KKT']['rho'])} ({w['KKT']['n']}) | {f3(w['neyron']['rho'])} ({w['neyron']['n']}) | "
                     f"{f3(w['hammasi_H6']['rho'])} ({w['hammasi_H6']['n']}) |")
    L += ['', '## 6. α implementatsiyasi', '', R['6_alfa_implementatsiya']]
    (CHIQ / 'Q13_natija.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
