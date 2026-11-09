# -*- coding: utf-8 -*-
"""TOLQIN-2 — MUZLATILGAN TAHLIL SKRIPTI (prereg.md §4; tuzatish_1, _3, _4, _5). Ma'lumot yig'ilishidan OLDIN commit.
Commitdan keyin o'zgartirilmaydi; o'zgarsa — sanali tuzatish va sabab (prereg §3, tuzatish qoidasi).
O'ZGARISH 2026-10-20 (birinchi va yagona; sabab — tuzatish_7.md): muzlatilgan versiya sha256
d867e101063325483e26da641abb9e9ae9eec6d22454c6d9cbac99d840e3b718 (1d29166). Inson baholariga tayanadigan barcha
jadvallar (H2–H9) ikki marta: ASOSIY — 71 gap (gold-00 chiqarilgan), SEZGIRLIK — 72. Darvozalar (H1) va avtomatik
metrikalar (A1, A2, B1, B2 P1, X1; COMET — comet_qoshimcha.py) o'zgarmaydi (72 / 400).
TUZATISH 7a (2026-10-20): P1 (B2) — avtomatik metrika, prereg bo'yicha faqat 72; 1e8c1a9 dagi 71 varianti olib tashlandi.

    python3 analysis/tolqin-2/tahlil.py --yurish            # haqiqiy, BIR MARTA (prereg §3 (9)); natija/ mavjud bo'lsa TO'XTAYDI
    python3 analysis/tolqin-2/tahlil.py --sintetik DIR      # smoke-test: DIR ga sintetik kirishlar yasaydi va ular ustida yuradi

KIRISH FORMATLARI (ildiz = shu papka; --sintetik da DIR):
  a_qavat_400.json                 [{id, uz, en_ref, ekspozitsiya:{aynan:[..], prefiks:[..]}}] — 400, sha256 MANIFEST'da
  eval72.json (yoki repo evaluation/eval72/sentences.json)  [{id, layer ∈ flores|train|gold, uz, ref_en, …}] — 72
  kkt_chiqish.json                 {_meta, a_qavat:{id:{translation,…}}, eval72:{id:{translation,…}}}
  veb/kalit.json                   {fayllar:{llm_NN.txt|gt_NN.txt:{qator:{"k":{toplam,id}}}}}
  veb/javob/gemini_NN.txt, claude_NN.txt, gpt_NN.txt (NN 01..12)  qator «N. tarjima»; N -> kalit (llm_NN.txt)
  veb/javob/gt_NN.txt (NN 01..19)  k-qator = kalit gt_NN.txt qator k  (*_matnrejim.txt — tuzatish 3: o'qilmaydi)
  paket/kalit_tarjimon.json        {seed, qator:{"№":{toplam:"eval72", id}}}
  qaytgan/T1.xlsx, qaytgan/T2.xlsx 1-varaq, sarlavha qatori + «№ | Manba | Tarjima»; 72/72 to'liq bo'lishi SHART
  paket/kalit_baho.json            {elementlar:{EID:{tizim, id}}, tartib:{B|C|D|E: R1|R2}}  (tizim: KKT|Gemini|Claude|GPT|GT)
  qaytgan/baho_<X>.xlsx (X ∈ B,C,D,E)  1-varaq, sarlavha + «Element | Adequacy | Fluency», qatorlar TAQDIM tartibida
  qaytgan/chiqarilgan.json         (ixtiyoriy) {X: sabab} — prereg §4 istisnosi (ikkinchi marta darvozadan o'tmagan)
  qaytgan/hakam_<model>_<R1|R2>.csv  (ixtiyoriy, LLM-hakam) ustunlar: element,adequacy,fluency (1–5)
CHIQISH: natija/tahlil_natija.json, natija/tahlil_natija.md (jadvallar). Tizim nomlari: KKT, Gemini, Claude, GPT, GT.

METRIKALAR (prereg §2.7): sacreBLEU 2.6.0, tokenizatsiya 13a; korpus-BLEU ASOSIY; «gap-BLEU o'rtachasi
(sentence_bleu, smooth_method=exp)» ikkilamchi; chrF2 (sacreBLEU CHRF, char_order 6, word_order 0, beta 2);
ko'p etalon — sacreBLEU ko'p etalon rejimi (B: 1 etalon = eval72 ref_en; 3 etalon = ref_en + T1 + T2).
COMET (wmt22-comet-da) — `comet` o'rnatilgan bo'lsa ikkilamchi, aks holda chiqarib tashlanadi va yoziladi.
Bootstrap: 1000, seed 20261016, persentil 95 % CI (birlik — element/gap). Spearman (o'rtacha rang), Kendall τ-b,
Krippendorff α (ordinal, kelishuv matritsasi) — sof Python.
Qatlamlar (tuzatish 5): asosiy tavsifiy — eval72 `layer` (flores 36 / train 24 / gold 12); qo'shimcha tavsifiy —
tuzatish 4: B-KKT = train+gold (36), B-FLORES = flores (36). Noyob gap < 20 bo'lgan qatlam «beqaror» belgilanadi
(gold, n = 12). A-qavat KKT ekspozitsiyasi (prereg §2.2/§4): «aynan» va «prefiks» belgilari ikkalasi ko'rsatiladi.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import shutil
import sys
from pathlib import Path

import sacrebleu
from sacrebleu.metrics import BLEU, CHRF

assert sacrebleu.__version__ == '2.6.0', f'sacreBLEU {sacrebleu.__version__} != 2.6.0 (prereg §2.7)'
SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
TIZIMLAR = ('KKT', 'Gemini', 'Claude', 'GPT', 'GT')
LLM = {'Gemini': 'gemini', 'Claude': 'claude', 'GPT': 'gpt'}
BAHOLOVCHI = ('B', 'C', 'D', 'E')
SEED, BOOT = 20261016, 1000
A_SHA = '1e37f431c86a0b1c505655144806fbf2b37f31d445258c6a0d0b476e0604827c'
E_SHA = '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
BEQAROR_N = 20
# Tuzatish 7 (2026-10-20, birinchi va yagona sanali o'zgarish): gold-00 baholovchi yo'riqnomasi misolida bor —
# inson baholariga tayanadigan barcha jadvallar: ASOSIY = 71 gap (gold-00 siz), SEZGIRLIK = 72 (P1 — 72, tuzatish 7a).
CHIQ7 = {'gold-00'}
# Tuzatish 10 (2026-10-27, ikkinchi sanali o'zgarish): T1 71/72 (№ 55 bo'sh — shu gapda faqat asl etalon), T2 yo'q.
BOSH10 = {('T1', '55')}
# Tuzatish 10 (g): B, D qayta qaytarilmadi — shu kataklar «yo'q ma'lumot», element bo'yicha juftlik chiqarish.
BOSH10_BAHO = {('B', 'E159'), ('B', 'E219'), ('D', 'E019')}
_i = lambda v: None if v in (None, '') else int(v)


def toliq10(x, q, el):
    """(a) dan faqat BOSH10_BAHO dagi kataklar sabab o'tmagan fayl — tuzatish 10 (g) bo'yicha ishlatiladi."""
    return len(q) == len(el) and {str(r[0]) for r in q} == set(el) and \
        all((x, str(r[0])) in BOSH10_BAHO for r in q if r[1] in (None, '') or r[2] in (None, ''))


def ort10(bh, ish, e, k):
    """Element e, o'lchov k bo'yicha mavjud baholar o'rtachasi (tuzatish 10 (g))."""
    v = [bh[x][e][k] for x in ish if bh[x][e][k] is not None]
    return sum(v) / len(v)


E_XOM = 'xom/E__baho_E.xlsx'                          # tuzatish 10 (d): «E bilan» sezgirlik — asl qaytarma (qabul.py RAD qilgan)


def e_xom(ild):
    p = ild / 'qaytgan' / E_XOM
    if not p.exists():
        return None, None
    import openpyxl
    q = list(openpyxl.load_workbook(p, read_only=True, data_only=True)['Baholash'].iter_rows(values_only=True))
    return [[str(r[0]).strip(), r[3], r[4]] for r in q[1:] if any(x not in (None, '') for x in r[:5])], sha(p)
ASOSIY = 'ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)'
SEZGIR = "SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)"
_BLEU = BLEU(tokenize='13a')
_CHRF = CHRF()                                       # chrF2: char_order 6, word_order 0, beta 2


# ---------------------------------------------------------------- statistika (sof Python)
def rang(x):
    t = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(t):
        j = i
        while j + 1 < len(t) and x[t[j + 1]] == x[t[i]]:
            j += 1
        for k in range(i, j + 1):
            r[t[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx == 0 or sy == 0:
        return float('nan')
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def spearman(x, y):
    return pearson(rang(x), rang(y)) if len(x) >= 3 else float('nan')


def kendall_b(x, y):
    n = len(x)
    c = d = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = x[i] - x[j], y[i] - y[j]
            if a == 0 and b == 0:
                continue
            if a == 0:
                tx += 1
            elif b == 0:
                ty += 1
            elif (a > 0) == (b > 0):
                c += 1
            else:
                d += 1
    den = math.sqrt((c + d + tx) * (c + d + ty))
    return (c - d) / den if den else float('nan')


def kripp_alpha_ordinal(birliklar):
    """birliklar: [[qiymat, …], …] (har birlikda >= 2 baho juftlanadi). Qiymatlar butun 1..5."""
    qiym = sorted({v for u in birliklar for v in u})
    o = {(c, k): 0.0 for c in qiym for k in qiym}
    for u in birliklar:
        m = len(u)
        if m < 2:
            continue
        for i in range(m):
            for j in range(m):
                if i != j:
                    o[(u[i], u[j])] += 1 / (m - 1)
    nc = {c: sum(o[(c, k)] for k in qiym) for c in qiym}
    n = sum(nc.values())
    if n <= 1 or len(qiym) < 2:
        return float('nan')

    def d2(c, k):
        a, b = min(c, k), max(c, k)
        return (sum(nc[g] for g in qiym if a <= g <= b) - (nc[a] + nc[b]) / 2) ** 2
    do = sum(o[(c, k)] * d2(c, k) for c in qiym for k in qiym)
    de = sum(nc[c] * nc[k] * d2(c, k) for c in qiym for k in qiym)
    return 1 - (n - 1) * do / de if de else float('nan')


def boot_ci(n, fn, seed=SEED):
    """fn(indekslar) -> son; elementlar bo'yicha bootstrap (n element), 95 % persentil."""
    rnd = random.Random(seed)
    v = []
    for _ in range(BOOT):
        s = fn([rnd.randrange(n) for _ in range(n)])
        if not math.isnan(s):
            v.append(s)
    if len(v) < BOOT * 0.5:
        return [float('nan'), float('nan')]
    v.sort()
    return [v[int(0.025 * len(v))], v[min(len(v) - 1, int(0.975 * len(v)))]]


# ---------------------------------------------------------------- MT metrikalari
def korpus(hyp, refs):
    """hyp: [str]; refs: [[str]*n] (etalon oqimlari). -> dict"""
    return {'bleu': _BLEU.corpus_score(hyp, refs).score, 'chrf2': _CHRF.corpus_score(hyp, refs).score,
            'gap_bleu_ortacha_exp': sum(sacrebleu.sentence_bleu(h, [r[i] for r in refs], smooth_method='exp').score
                                        for i, h in enumerate(hyp)) / len(hyp), 'n': len(hyp)}


def gap_bleu(h, rr):
    return sacrebleu.sentence_bleu(h, rr, smooth_method='exp').score


def bleu_stat(hyp, refs):
    return _BLEU._extract_corpus_statistics(hyp, refs)


def bleu_stat_ball(st, idx):
    s = [sum(st[i][k] for i in idx) for k in range(len(st[0]))]
    return _BLEU._compute_score_from_stats(s).score


def imzolar():
    """sacreBLEU imzolari: 1 va 3 etalon (namuna baholashdan keyin olinadi)."""
    out = {}
    for n in (1, 3):
        b, c = BLEU(tokenize='13a'), CHRF()
        b.corpus_score(['a b c d'], [['a b c d']] * n)
        c.corpus_score(['a b c d'], [['a b c d']] * n)
        out[f'{n}ref'] = {'bleu': str(b.get_signature()), 'chrf': str(c.get_signature())}
    return out


def comet_holat():
    try:
        import comet  # noqa: F401
        return 'o\'rnatilgan'
    except ImportError:
        return "o'rnatilmagan — prereg §2.7 bo'yicha chiqarib tashlandi"


# ---------------------------------------------------------------- kirishlar
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def oqi_xlsx(p, ustunlar):
    import openpyxl
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    q = list(ws.iter_rows(values_only=True))
    sar = [str(x).strip() if x is not None else '' for x in q[0]]
    assert sar[:len(ustunlar)] == list(ustunlar), f'{p.name}: sarlavha {sar[:len(ustunlar)]} != {list(ustunlar)}'
    return [list(r[:len(ustunlar)]) for r in q[1:] if any(x not in (None, '') for x in r[:len(ustunlar)])]


def yukla(ild, eval72_yol):
    a_b = (ild / 'a_qavat_400.json').read_bytes()
    e_b = Path(eval72_yol).read_bytes()
    A = json.loads(a_b)
    B = json.loads(e_b)
    assert len(A) == 400 and len(B) == 72
    tekshir = {'a_qavat_400.json': hashlib.sha256(a_b).hexdigest(), 'eval72': hashlib.sha256(e_b).hexdigest()}
    kalit = json.loads((ild / 'veb' / 'kalit.json').read_text(encoding='utf-8'))
    chiq = {t: {} for t in TIZIMLAR}
    kkt = json.loads((ild / 'kkt_chiqish.json').read_text(encoding='utf-8'))
    for top in ('a_qavat', 'eval72'):
        for i, v in kkt[top].items():
            chiq['KKT'][(top, i)] = v['translation']
    for t, pre in LLM.items():
        for nn in range(1, 13):
            k = kalit['fayllar'][f'llm_{nn:02d}.txt']['qator']
            for q in (ild / 'veb' / 'javob' / f'{pre}_{nn:02d}.txt').read_text(encoding='utf-8').split('\n'):
                q = q.rstrip('\r')
                if not q.strip():
                    continue
                n, _, matn = q.strip().partition('.')
                assert n.isdigit() and n in k, f'{pre}_{nn:02d}: raqamsiz/ortiqcha qator'
                g = k[n]
                assert (g['toplam'], g['id']) not in chiq[t], f'{t}: takror {g}'
                chiq[t][(g['toplam'], g['id'])] = matn.strip()
    for nn in range(1, 20):
        k = kalit['fayllar'][f'gt_{nn:02d}.txt']['qator']
        qq = [q.rstrip('\r') for q in (ild / 'veb' / 'javob' / f'gt_{nn:02d}.txt').read_text(encoding='utf-8').split('\n') if q.strip()]
        assert len(qq) == len(k), f'gt_{nn:02d}: {len(qq)} != {len(k)}'
        for j, q in enumerate(qq, 1):
            g = k[str(j)]
            chiq['GT'][(g['toplam'], g['id'])] = q.strip()
    for t in TIZIMLAR:
        assert len(chiq[t]) == 472, f'{t}: {len(chiq[t])}/472 — TO\'XTA'
    # tarjimonlar
    kt = json.loads((ild / 'paket' / 'kalit_tarjimon.json').read_text(encoding='utf-8'))
    uz = {r['id']: r['uz'] for r in B}
    T = {}
    for x in ('T1', 'T2'):
        p = ild / 'qaytgan' / f'{x}.xlsx'
        if not p.exists():                                # tuzatish 10 (b): T2 olinmadi
            continue
        qq = oqi_xlsx(p, ('№', 'Manba', 'Tarjima'))
        m = {}
        for no, manba, tar in qq:
            g = kt['qator'][str(int(no))]
            assert str(manba).strip() == uz[g['id']].strip(), f'{x}: № {no} manba kalitga mos emas'
            if tar is None or not str(tar).strip():       # tuzatish 10 (a): T1 № 55 — faqat asl etalon
                assert (x, str(int(no))) in BOSH10, f'{x}: № {no} tarjima bo\'sh — prereg §4: qaytariladi'
                continue
            m[g['id']] = str(tar).strip()
        assert len(m) in (72, 72 - sum(t == x for t, _ in BOSH10)), f'{x}: {len(m)}/72 — prereg §2.4; tuzatish 10'
        T[x] = m
        tekshir[f'qaytgan/{x}.xlsx'] = sha(p)
    # baholovchilar
    kb = json.loads((ild / 'paket' / 'kalit_baho.json').read_text(encoding='utf-8'))
    baho, xom = {}, {}
    for x in BAHOLOVCHI:
        p = ild / 'qaytgan' / f'baho_{x}.xlsx'
        if not p.exists():
            continue
        xom[x] = oqi_xlsx(p, ('Element', 'Adequacy', 'Fluency'))
        tekshir[f'qaytgan/baho_{x}.xlsx'] = sha(p)
    ch_p = ild / 'qaytgan' / 'chiqarilgan.json'
    chiqarilgan = json.loads(ch_p.read_text(encoding='utf-8')) if ch_p.exists() else {}
    hakam = {}
    for p in sorted((ild / 'qaytgan').glob('hakam_*_R[12].csv')):
        model, tartib = p.stem[len('hakam_'):].rsplit('_', 1)
        with open(p, encoding='utf-8', newline='') as f:
            hakam[(model, tartib)] = {r['element']: (float(r['adequacy']), float(r['fluency'])) for r in csv.DictReader(f)}
        tekshir[f'qaytgan/{p.name}'] = sha(p)
    return A, B, chiq, T, kb, xom, chiqarilgan, hakam, tekshir


# ---------------------------------------------------------------- darvozalar (prereg §2.5, kalitsiz)
def darvoza(qatorlar, n_kutilgan):
    adq = [r[1] for r in qatorlar]
    flu = [r[2] for r in qatorlar]
    ok = lambda v: isinstance(v, (int, float)) and float(v).is_integer() and 1 <= v <= 5
    a = len({r[0] for r in qatorlar}) == n_kutilgan and len(qatorlar) == n_kutilgan and \
        all(v is not None and v != '' for v in adq + flu)
    b = all(ok(v) for v in adq + flu if v not in (None, ''))
    eng, joriy = 1, 1
    for i in range(1, len(qatorlar)):
        joriy = joriy + 1 if (adq[i], flu[i]) == (adq[i - 1], flu[i - 1]) else 1
        eng = max(eng, joriy)
    jj = [(x, y) for x, y in zip(adq, flu) if ok(x) and ok(y)]
    rho = spearman([x for x, _ in jj], [y for _, y in jj]) if jj else float('nan')
    ulush = sum(x == y for x, y in jj) / len(jj) if jj else float('nan')
    return {'a_toliqlik': a, 'b_diapazon': b, 'c_avtopilot_eng_uzun': eng, 'c_belgi': eng >= 12,
            'd_spearman_adq_flu': rho, 'd_belgi': not (0.30 <= rho <= 0.95) if not math.isnan(rho) else True,
            'e_teng_ulush': ulush, 'e_belgi': ulush >= 0.90 if not math.isnan(ulush) else True}


# ---------------------------------------------------------------- tahlil
def inson(J, tnom, eids, hm, tiz, gid, gb, bh, ishlat, kb, hakam, chiq, r1, pos, qatlamlar):
    """Inson baholariga tayanadigan jadvallar (H2–H9) — berilgan element to'plami bo'yicha (tuzatish 7)."""
    J[f'H2 Inson adequacy/fluency o\'rtachasi (tizim bo\'yicha) — {tnom}'] = {
        t: {'adequacy': sum(hm[e][0] for e in eids if tiz[e] == t) / sum(tiz[e] == t for e in eids),
            'fluency': sum(hm[e][1] for e in eids if tiz[e] == t) / sum(tiz[e] == t for e in eids),
            'n': sum(tiz[e] == t for e in eids), 'baholovchi': len(ishlat)} for t in TIZIMLAR} if hm else {}
    # S2
    s2 = {}
    for t in list(TIZIMLAR) + ['hammasi']:
        ee = [e for e in eids if hm and hm[e][0] >= 4.5 and (t == 'hammasi' or tiz[e] == t)]
        s2[t] = korpus([chiq[tiz[e]][('eval72', gid[e])] for e in ee], [[r1[pos[gid[e]]] for e in ee]]) if ee else {'n': 0}
    J[f'H3 S2 kalibrovka: adequacy o\'rtachasi >= 4,5 bo\'lgan chiqishlar, 1 etalon — {tnom}'] = s2
    # S3 korrelyatsiya
    def kor(ee):
        x, y = [gb[e] for e in ee], [hm[e][0] for e in ee]
        return {'n': len(ee), 'noyob_gap': len({gid[e] for e in ee}), 'spearman': spearman(x, y),
                'ci95': boot_ci(len(ee), lambda ix: spearman([x[i] for i in ix], [y[i] for i in ix])),
                'beqaror': len({gid[e] for e in ee}) < BEQAROR_N}
    s3 = {}
    if hm:
        s3['umumiy'] = kor(eids)
        for t in TIZIMLAR:
            s3[f'tizim ichida: {t}'] = kor([e for e in eids if tiz[e] == t])
        for qn, ids in qatlamlar.items():
            if qn == 'hammasi':
                continue
            ss = set(ids)
            s3[f'{qn}: umumiy'] = kor([e for e in eids if gid[e] in ss])
            for t in TIZIMLAR:
                s3[f'{qn}: {t}'] = kor([e for e in eids if gid[e] in ss and tiz[e] == t])
    J[f'H4 S3 ρ(gap-BLEU_1ref, adequacy): umumiy, tizim ichida, qatlam bo\'yicha (bootstrap 1000) — {tnom}'] = s3
    past = {}
    if hm:
        for t in list(TIZIMLAR) + ['hammasi']:
            ee = [e for e in eids if gb[e] < 10 and (t == 'hammasi' or tiz[e] == t)]
            past[t] = {'n': len(ee), 'kendall_tau_b': kendall_b([gb[e] for e in ee], [hm[e][0] for e in ee]) if len(ee) >= 3 else float('nan')}
    J[f'H5 Past ball rejimi (gap-BLEU_1ref < 10): Kendall τ-b — {tnom}'] = past
    # P3 kelishuv
    jt = {}
    for d, k in (('adequacy', 0), ('fluency', 1)):
        for i, x in enumerate(ishlat):
            for y in ishlat[i + 1:]:
                ee = [e for e in eids if bh[x][e][k] is not None and bh[y][e][k] is not None]   # tuzatish 10 (g)
                jt[f'{d}: {x}–{y}'] = spearman([bh[x][e][k] for e in ee], [bh[y][e][k] for e in ee])
    J[f'H6 P3 juftlik Spearman — {tnom}'] = jt
    J[f'H7 P3 Krippendorff α (ordinal) — {tnom}'] = {d: kripp_alpha_ordinal([[bh[x][e][k] for x in ishlat if bh[x][e][k] is not None] for e in eids]) if len(ishlat) >= 2 else float('nan')
                                           for d, k in (('adequacy', 0), ('fluency', 1))}
    # S4 tartib ta'siri
    s4 = {}
    g1 = [x for x in ishlat if kb['tartib'][x] == 'R1']
    g2 = [x for x in ishlat if kb['tartib'][x] == 'R2']
    if g1 and g2:
        for d, k in (('adequacy', 0), ('fluency', 1)):
            for t in list(TIZIMLAR) + ['hammasi']:
                ee = [e for e in eids if (t == 'hammasi' or tiz[e] == t)
                      and any(bh[x][e][k] is not None for x in g1) and any(bh[x][e][k] is not None for x in g2)]
                _g = lambda g, e: (lambda v: sum(v) / len(v))([bh[x][e][k] for x in g if bh[x][e][k] is not None])
                df = [_g(g1, e) - _g(g2, e) for e in ee]
                s4[f'{d}: {t}'] = {'R1_minus_R2': sum(df) / len(df), 'ci95': boot_ci(len(df), lambda ix: sum(df[i] for i in ix) / len(ix)),
                                   'R1': g1, 'R2': g2}
    J[f'H8 S4 tartib ta\'siri R1 − R2 (tadqiqiy) — {tnom}'] = s4
    # LLM-hakam (prereg §2.8, tadqiqiy)
    lh = {}
    for (model, tartib), v in sorted(hakam.items()):
        for d, k in (('adequacy', 0), ('fluency', 1)):
            for t in list(TIZIMLAR) + ['hammasi']:
                ee = [e for e in eids if e in v and (t == 'hammasi' or tiz[e] == t)]
                if hm and len(ee) >= 3:
                    lh[f'{model} {tartib} · {d} · {t}'] = {'n': len(ee), 'spearman': spearman([v[e][k] for e in ee], [hm[e][k] for e in ee])}
    J[f'H9 LLM-hakam vs inson o\'rtachasi: Spearman (tadqiqiy) — {tnom}'] = lh


def tahlil(ild, eval72_yol):
    A, B, chiq, T, kb, xom, chiqarilgan, hakam, tekshir = yukla(ild, eval72_yol)
    R = {'kirish_sha256': tekshir, 'sacrebleu': sacrebleu.__version__, 'imzo': imzolar(), 'comet': comet_holat(), 'jadvallar': {}}
    J = R['jadvallar']
    a_id = [r['id'] for r in A]
    a_ref = [[r['en_ref'] for r in A]]
    # --- A-qavat (5 × 400)
    J['A1 A-qavat (5 × 400, 1 etalon FLORES)'] = {t: korpus([chiq[t][('a_qavat', i)] for i in a_id], a_ref) for t in TIZIMLAR}
    eks = {}
    for tur in ('aynan', 'prefiks'):
        for bor in (True, False):
            idx = [k for k, r in enumerate(A) if bool(r['ekspozitsiya'][tur]) == bor]
            eks[f'{tur}: {"ekspozitsiyali" if bor else "ekspozitsiyasiz"}'] = korpus(
                [chiq['KKT'][('a_qavat', a_id[k])] for k in idx], [[A[k]['en_ref'] for k in idx]])
    J['A2 A-qavat KKT ekspozitsiyali/ekspozitsiyasiz (78 so\'z; aynan va prefiks)'] = eks
    # --- B-qavat
    b_id = [r['id'] for r in B]
    lay = {r['id']: r['layer'] for r in B}
    r1 = [r['ref_en'] for r in B]
    r3 = [r1] + [[T[x].get(i) for i in b_id] for x in ('T1', 'T2') if x in T]   # tuzatish 10: None = etalon yo'q
    R['kop_etalon'] = {'oqimlar': ['ref_en'] + [x for x in ('T1', 'T2') if x in T], 'bosh': sorted(BOSH10),
                       'izoh': "«3ref» kalitlari = ko'p etalon (oqimlar ro'yxati bo'yicha), tuzatish 10"}
    qatlamlar = {'hammasi': b_id}
    for L in ('flores', 'train', 'gold'):
        qatlamlar[f'qatlam {L}'] = [i for i in b_id if lay[i] == L]
    qatlamlar['B-KKT (train+gold)'] = [i for i in b_id if lay[i] in ('train', 'gold')]
    qatlamlar['B-FLORES (flores)'] = [i for i in b_id if lay[i] == 'flores']
    pos = {i: k for k, i in enumerate(b_id)}
    jb = {}
    for qn, ids in qatlamlar.items():
        for t in TIZIMLAR:
            h = [chiq[t][('eval72', i)] for i in ids]
            k1 = korpus(h, [[r1[pos[i]] for i in ids]])
            k3 = korpus(h, [[s[pos[i]] for i in ids] for s in r3])
            jb.setdefault(qn, {})[t] = {'1ref': k1, '3ref': k3, 'beqaror': len(ids) < BEQAROR_N}
    J['B1 B-qavat (5 × 72): 1 va 3 etalon (asosiy: hammasi; qatlamlar tavsifiy)'] = jb
    p1 = {}                                                       # tuzatish 7a: P1 avtomatik — 72 (prereg)
    for t in TIZIMLAR:
        h = [chiq[t][('eval72', i)] for i in b_id]
        s1, s3 = bleu_stat(h, [r1]), bleu_stat(h, r3)
        d = bleu_stat_ball(s3, range(72)) - bleu_stat_ball(s1, range(72))
        p1[t] = {'delta_bleu_3ref_minus_1ref': d,
                 'ci95_bootstrap_gap': boot_ci(72, lambda ix: bleu_stat_ball(s3, ix) - bleu_stat_ball(s1, ix))}
    J['B2 P1: Δ = BLEU_3ref − BLEU_1ref (72 gap)'] = p1
    # --- inson baholari
    el = kb['elementlar']
    dv = {x: darvoza(q, len(el)) for x, q in xom.items()}
    J['H1 Yaxlitlik darvozalari (prereg §2.5 (a)–(e), kalitsiz)'] = dv
    ishlat = [x for x in BAHOLOVCHI if x in xom and (dv[x]['a_toliqlik'] or toliq10(x, xom[x], el)) and dv[x]['b_diapazon']
              and x not in chiqarilgan
              and {str(r[0]) for r in xom[x]} == set(el)]
    R['baholovchilar'] = {'kelgan': sorted(xom), 'ishlatilgan': ishlat, 'chiqarilgan': chiqarilgan,
                          'toxtash_qoidasi_>=3': len(ishlat) >= 3}
    bh = {x: {str(r[0]): (_i(r[1]), _i(r[2])) for r in xom[x]} for x in ishlat}      # tuzatish 10 (g): None = yo'q
    R['baholovchilar']['yoq_malumot'] = sorted([x, e, k] for x in ishlat for e, v in bh[x].items() for k in (0, 1) if v[k] is None)
    hamma = sorted(el)
    hm = {e: (ort10(bh, ishlat, e, 0), ort10(bh, ishlat, e, 1)) for e in hamma} if ishlat else {}
    tiz = {e: el[e]['tizim'] for e in hamma}
    gid = {e: el[e]['id'] for e in hamma}
    gb = {e: gap_bleu(chiq[tiz[e]][('eval72', gid[e])], [r1[pos[gid[e]]]]) for e in hamma}   # gap-BLEU 1ref element bo'yicha
    for tnom, eids in ((ASOSIY, [e for e in hamma if gid[e] not in CHIQ7]), (SEZGIR, hamma)):   # tuzatish 7
        inson(J, tnom, eids, hm, tiz, gid, gb, bh, ishlat, kb, hakam, chiq, r1, pos, qatlamlar)
    # Tuzatish 10 (d): «E bilan» sezgirlik — shu yurishda; E (a)/(b) asl faylda, chiqarilgan.json faqat shu variantda e'tiborsiz
    R['inson'] = {'ishlatilgan': ishlat, 'jadvallar': [k for k in J if k[:2] in ('H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9')]}
    xE, shE = (xom['E'], None) if 'E' in xom else e_xom(ild)
    J2 = {}
    R['inson_E_bilan'] = {'jadvallar': J2, 'E_manba': 'qaytgan/baho_E.xlsx' if 'E' in xom else E_XOM, 'E_sha256': shE}
    if xE:
        dE = darvoza(xE, len(el))
        okE = dE['a_toliqlik'] and dE['b_diapazon'] and {str(r[0]) for r in xE} == set(el)
        ishE = [x for x in BAHOLOVCHI if x in ishlat or (x == 'E' and okE)]
        bhE = dict(bh, **({'E': {str(r[0]): (_i(r[1]), _i(r[2])) for r in xE}} if okE else {}))
        hmE = {e: (ort10(bhE, ishE, e, 0), ort10(bhE, ishE, e, 1)) for e in hamma}
        R['inson_E_bilan'].update(darvoza_E=dE, ishlatilgan=ishE)
        for tnom, eids in ((ASOSIY, [e for e in hamma if gid[e] not in CHIQ7]), (SEZGIR, hamma)):
            inson(J2, tnom, eids, hmE, tiz, gid, gb, bhE, ishE, kb, hakam, chiq, r1, pos, qatlamlar)
    # Eksplorativ (tuzatish 4 c)
    ha = [chiq['KKT'][('a_qavat', i)] for i in a_id]
    fl = qatlamlar['B-FLORES (flores)']
    hb = [chiq['KKT'][('eval72', i)] for i in fl]
    rb = [[r1[pos[i]] for i in fl]]
    sa, sb = bleu_stat(ha, a_ref), bleu_stat(hb, rb)
    ka, kbm = korpus(ha, a_ref), korpus(hb, rb)
    rnd = random.Random(SEED)
    v = []
    for _ in range(BOOT):
        ia = [rnd.randrange(len(ha)) for _ in ha]
        ib = [rnd.randrange(len(hb)) for _ in hb]
        v.append(bleu_stat_ball(sb, ib) - bleu_stat_ball(sa, ia))
    v.sort()
    J['X1 EKSPLORATIV: KKT B-FLORES − A (1 etalon; tasdiqlovchi test EMAS)'] = {
        'A': ka, 'B-FLORES': kbm, 'bleu_farq_B_minus_A': kbm['bleu'] - ka['bleu'],
        'chrf2_farq_B_minus_A': kbm['chrf2'] - ka['chrf2'], 'bleu_farq_ci95_bootstrap': [v[int(0.025 * BOOT)], v[int(0.975 * BOOT) - 1]]}
    return R


def md(R):
    L = ['# TOLQIN-2 — tahlil natijasi (tahlil.py)', '', f"sacreBLEU {R['sacrebleu']} · imzolar `{json.dumps(R['imzo'], ensure_ascii=False)}`",
         f"COMET: {R['comet']}", '']
    if 'baholovchilar' in R:
        L += [f"Baholovchilar: {json.dumps(R['baholovchilar'], ensure_ascii=False)}", '']
    for nom, j in R['jadvallar'].items():
        if nom.startswith('X'):
            L += ['# EKSPLORATIV (tuzatish 4 c — tasdiqlovchi test emas)', '']
        L += [f'## {nom}', '']
        L += ['```', json.dumps(j, ensure_ascii=False, indent=1, sort_keys=True, default=str), '```', '']
    if R.get('inson_E_bilan', {}).get('jadvallar'):                 # tuzatish 10 (d)
        v = R['inson_E_bilan']
        L += ['# SEZGIRLIK «E bilan» (tuzatish 10 (d))', '', f"Baholovchilar: {json.dumps(v['ishlatilgan'], ensure_ascii=False)}"
              f" · E manba {v['E_manba']} · E darvoza {json.dumps(v['darvoza_E'], ensure_ascii=False, default=str)}", '']
        for nom, j in v['jadvallar'].items():
            L += [f'## {nom} [E bilan]', '', '```', json.dumps(j, ensure_ascii=False, indent=1, sort_keys=True, default=str), '```', '']
    return '\n'.join(L) + '\n'


# ---------------------------------------------------------------- sintetik smoke-test
def sintetik(d):
    d = Path(d)
    assert not d.exists() or not any(d.iterdir()), f'{d} bo\'sh emas'
    rnd = random.Random(7)
    (d / 'veb' / 'javob').mkdir(parents=True)
    (d / 'paket').mkdir()
    (d / 'qaytgan').mkdir()
    shutil.copyfile(SIKL / 'a_qavat_400.json', d / 'a_qavat_400.json')
    shutil.copyfile(REPO / 'evaluation/eval72/sentences.json', d / 'eval72.json')
    shutil.copyfile(SIKL / 'veb' / 'kalit.json', d / 'veb' / 'kalit.json')
    A = json.loads((d / 'a_qavat_400.json').read_text(encoding='utf-8'))
    B = json.loads((d / 'eval72.json').read_text(encoding='utf-8'))
    ref = {('a_qavat', r['id']): r['en_ref'] for r in A}
    ref.update({('eval72', r['id']): r['ref_en'] for r in B})

    def buz(s, p):                                    # sintetik «tarjima»: etalondan so'z tashlash/almashtirish
        w = s.split()
        return ' '.join(x if rnd.random() > p else rnd.choice(['the', 'a', 'of', 'xyz']) for x in w) or 'x'
    sifat = {'KKT': 0.6, 'Gemini': 0.15, 'Claude': 0.1, 'GPT': 0.12, 'GT': 0.25}
    kkt = {'_meta': {'sintetik': True}, 'a_qavat': {}, 'eval72': {}}
    for (top, i), s in ref.items():
        kkt[top][i] = {'translation': buz(s, sifat['KKT'])}
    (d / 'kkt_chiqish.json').write_text(json.dumps(kkt, ensure_ascii=False), encoding='utf-8')
    kalit = json.loads((d / 'veb' / 'kalit.json').read_text(encoding='utf-8'))
    for f, v in kalit['fayllar'].items():
        q = v['qator']
        if f.startswith('llm_'):
            for t, pre in LLM.items():
                (d / 'veb' / 'javob' / f.replace('llm', pre)).write_text(
                    '\n'.join(f'{k}. {buz(ref[(q[k]["toplam"], q[k]["id"])], sifat[t])}' for k in sorted(q, key=int)) + '\n', encoding='utf-8')
        else:
            (d / 'veb' / 'javob' / f).write_text('\n'.join(buz(ref[(q[k]['toplam'], q[k]['id'])], sifat['GT'])
                                                           for k in sorted(q, key=int)) + '\n', encoding='utf-8')
    import openpyxl
    tartib = list(range(72))
    random.Random(SEED).shuffle(tartib)
    kt = {'seed': SEED, 'qator': {str(n): {'toplam': 'eval72', 'id': B[k]['id']} for n, k in enumerate(tartib, 1)}}
    (d / 'paket' / 'kalit_tarjimon.json').write_text(json.dumps(kt, ensure_ascii=False), encoding='utf-8')
    for x in ('T1', 'T2'):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['№', 'Manba', 'Tarjima'])
        for n, k in enumerate(tartib, 1):
            ws.append([n, B[k]['uz'], buz(B[k]['ref_en'], 0.2)])
        wb.save(d / 'qaytgan' / f'{x}.xlsx')
    el = {}
    for t in TIZIMLAR:
        for r in B:
            el[f'E{len(el) + 1:03d}'] = {'tizim': t, 'id': r['id']}
    kb = {'elementlar': el, 'tartib': {'B': 'R1', 'C': 'R2', 'D': 'R1', 'E': 'R2'}}
    (d / 'paket' / 'kalit_baho.json').write_text(json.dumps(kb, ensure_ascii=False), encoding='utf-8')
    asos = {e: 5 - 4 * sifat[v['tizim']] for e, v in el.items()}
    for x in BAHOLOVCHI:
        ee = sorted(el)
        rnd.shuffle(ee)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['Element', 'Adequacy', 'Fluency'])
        for e in ee:
            a = min(5, max(1, round(asos[e] + rnd.gauss(0, 0.8))))
            ws.append([e, a, min(5, max(1, round(a + rnd.gauss(0, 0.9))))])
        wb.save(d / 'qaytgan' / f'baho_{x}.xlsx')
    for m in ('hakamA', 'hakamB'):
        for tr in ('R1', 'R2'):
            with open(d / 'qaytgan' / f'hakam_{m}_{tr}.csv', 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerow(['element', 'adequacy', 'fluency'])
                for e in sorted(el):
                    w.writerow([e, min(5, max(1, round(asos[e] + rnd.gauss(0, 1)))), min(5, max(1, round(asos[e] + rnd.gauss(0, 1))))])
    return d


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--yurish', action='store_true')
    g.add_argument('--sintetik')
    a = ap.parse_args()
    if a.sintetik:
        d = sintetik(a.sintetik)
        R = tahlil(d, d / 'eval72.json')
        chiqish = d / 'natija'
    else:
        chiqish = SIKL / 'natija'
        if chiqish.exists():
            sys.exit("TO'XTA: natija/ mavjud — skript bir marta yuriladi (prereg §3 (9))")
        R = tahlil(SIKL, REPO / 'evaluation/eval72/sentences.json')
        assert R['kirish_sha256']['a_qavat_400.json'] == A_SHA and R['kirish_sha256']['eval72'] == E_SHA, 'kirish sha256'
    chiqish.mkdir()
    (chiqish / 'tahlil_natija.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True, default=str) + '\n', encoding='utf-8')
    (chiqish / 'tahlil_natija.md').write_text(md(R), encoding='utf-8')
    bosh = [k for k, v in R['jadvallar'].items() if not v]
    print(f"jadval: {len(R['jadvallar'])} · bo'sh: {len(bosh)}{' (' + ', '.join(bosh) + ')' if bosh else ''} -> {chiqish}")


if __name__ == '__main__':
    main()
