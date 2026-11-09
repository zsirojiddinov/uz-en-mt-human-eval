# -*- coding: utf-8 -*-
"""TOLQIN-2 — ikki to'lqinni solishtirish (iyul RW1 · oktyabr TOLQIN-2). NATIJADAN KEYINGI, QO'SHIMCHA, PREREG'DA YO'Q;
tadqiqotchi so'rovi 2026-10-28. Tasdiqlovchi emas. Muzlatilgan tahlil.py ga tegmaydi — undan faqat yukla(), korpus(),
spearman(), kripp_alpha_ordinal(), oqi_xlsx(), e_xom(), _i va TIZIMLAR import qilinadi. natija/ faqat O'QILADI (assert).

    python3 analysis/tolqin-2/qoshimcha/tolqinlar_solishtirish.py   # bir marta; tolqinlar_solishtirish.json mavjud bo'lsa TO'XTAYDI

Iyul manbasi (faqat o'qish): evaluation/eval72/ — sentences.json (72 gap, ref_en), s1_outputs.json, s2_outputs.json,
s3_gemini_outputs.json, blind_key.json (IT -> gap, tizim), returns/rater_{B,C}_filled.xlsx («Baholash»: item_id, Mazmun, Ravonlik).
Oktyabr: kkt_tolqin2 — tahlil.yukla() chiqishlari, qaytgan/baho_{B,C,D}.xlsx, E asl qaytarmasi (qaytgan/xom/, tuzatish 10 (d)).
Iyul va oktyabr baholovchilari BOSHQA odamlar (tadqiqotchi, 2026-10-28) — harflar ustma-ust tushsa ham bir xil deb olinmaydi;
shuning uchun harflar «iyul B», «okt B» ko'rinishida yuritiladi.
Element to'plami: oktyabr — 72 gap (360 element; SEZGIRLIK 72, iyul bilan taqqoslanuvchan); iyul — 216 item (72 gap × 3).
Yo'q kataklar juftlik bo'yicha chiqariladi (tuzatish 10 (g)). Bootstrap yo'q (faqat nuqtaviy qiymat).
1) MT metrikalari tahlil.korpus() bilan (sacreBLEU 2.6.0, 13a; chrF2; gap-BLEU exp), 1 etalon = ref_en; oktyabr KKT/Gemini
   qiymatlari natija/tahlil_natija.json B1 «1ref» bilan tekshiriladi (assert). KKT iyul (s1) va oktyabr chiqishi bayt-aynan
   gaplar soni — faqat tizim shu 72 gapda qancha o'zgarganini ko'rsatish uchun.
2) Baholovchi × tizim o'rtachalari va ball tarqalishi (iyul 216 item, oktyabr 360 element — fayl bo'yicha).
3) Kelishuv: juftlik Spearman va Krippendorff α (ordinal) qism-to'plamlar bo'yicha + har baholovchining SD si (diapazon torayishi).
   Oktyabr guruh α (B,C,D va B,C,D,E; hammasi) tahlil.py H7 SEZGIRLIK 72 bilan tekshiriladi (assert).
4) Baholovchilar jadvali — ombordagi yozuvlardan (quyida QAYD); ismsiz.
Chiqish: qoshimcha/tolqinlar_solishtirish.json, qoshimcha/tolqinlar_solishtirish.md.
"""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parent
_sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))
T = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(T)
IYUL = T.REPO / 'evaluation' / 'eval72'
IYUL_TIZ = ('s1', 's2', 'gemini')
DAR = (('mazmun', 0), ('ravonlik', 1))

# 4-band: ombordagi yozuvlar (2026-10-28 da qidirilgan: rw1_prereg_analysis_plan.md, results/rw1_report.md,
# results/human_eval_results.md, prereg.md, tuzatish_1..10.md, tarqatish_jurnali.csv, qaytgan/qabul_jurnal.csv, ikkala ombor git tarixi).
QAYD = {
    'iyul B': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q",
               'tarqatish': "qayd yo'q (rater_B.xlsx yaratilgan 2026-07-02, b37a4da)",
               'qaytish': "qayd yo'q (returns/rater_B_filled.xlsx: docProps modified 2026-07-09T13:15:54Z; omborga 2026-07-14, 0ab3ee2)"},
    'iyul C': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q",
               'tarqatish': "qayd yo'q (rater_C.xlsx yaratilgan 2026-07-02, b37a4da)",
               'qaytish': "2026-07-06 qabul (rw1_prereg_analysis_plan.md, 2026-07-07 tuzatishi); docProps modified 2026-07-04T16:41:34Z; omborga 2026-07-07, d54be48"},
    'okt B': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q", 'tarqatish': '2026-10-21',
              'qaytish': 'kelgan fayl mtime 2026-10-26T17:17:28+05:00; qabul 2026-10-26T19:42 (qabul_jurnal.csv)'},
    'okt C': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q", 'tarqatish': "2026-10-20..21 (aniq kun qayd etilmagan)",
              'qaytish': 'kelgan fayl mtime 2026-10-21T17:37:58+05:00; qabul 2026-10-26T19:42'},
    'okt D': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q", 'tarqatish': '2026-10-21',
              'qaytish': 'kelgan fayl mtime 2026-10-26T19:18:20+05:00; qabul 2026-10-26T19:42'},
    'okt E': {'daraja': "qayd yo'q", 'kasb': "qayd yo'q", 'tarqatish': "2026-10-20..21 (aniq kun qayd etilmagan)",
              'qaytish': 'kelgan fayl mtime 2026-10-22T14:12:04+05:00; qabul.py RAD 2026-10-26T19:42 (chiqarilgan, tuzatish 9/10 (d))'},
}
QAYD_IZOH = [
    "Ombordagi yagona daraja yozuvi: iyul A-rol o'rnini bosgan baholovchi — «ingliz tili o'qituvchisi, IELTS 7.0», QISMAN 127/216, "
    "asosiy tahlilga kirmagan (rw1_prereg_analysis_plan.md, 2026-07-11 tuzatishi; rw1_report.md).",
    "«7.5 / 7.0» yozilgan README omborda (asosiy va kkt_tolqin2, git tarixi bilan) topilmadi.",
    "prereg §2.5: «4 to'liq (B, C — 1-to'lqindan; D, E — yangi; kamida biri ingliz tili o'qituvchisi; IELTS ≥ 7,0)» — bu talab, yozuv emas; "
    "tadqiqotchi 2026-10-28: iyul va oktyabr baholovchilari boshqa odamlar — prereg matni bilan mos emas, bu yerda tuzatilmaydi.",
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sd(v):
    v = [a for a in v if a is not None]
    m = sum(v) / len(v)
    return math.sqrt(sum((a - m) ** 2 for a in v) / len(v))


def ort(v):
    v = [a for a in v if a is not None]
    return sum(v) / len(v) if v else float('nan')


def iyul_baho(p):
    import openpyxl
    q = list(openpyxl.load_workbook(p, read_only=True, data_only=True)['Baholash'].iter_rows(values_only=True))
    sar = [str(x).strip() if x is not None else '' for x in q[0]]
    ci, cm, cr = sar.index('item_id'), sar.index('Mazmun (1-5)'), sar.index('Ravonlik (1-5)')
    return {str(r[ci]): (T._i(r[cm]), T._i(r[cr])) for r in q[1:] if r[ci]}


def kelishuv(bh, ish, ee):
    """ish baholovchilari, ee elementlar: juftlik Spearman, juftlik α va guruh α, har baholovchi SD (juftlikdagi elementlarda)."""
    out = {}
    for d, k in DAR:
        r = {'juftlik': {}, 'sd': {x: sd([bh[x][e][k] for e in ee]) for x in ish}}
        for i, x in enumerate(ish):
            for y in ish[i + 1:]:
                jj = [e for e in ee if bh[x][e][k] is not None and bh[y][e][k] is not None]
                r['juftlik'][f'{x}–{y}'] = {'n': len(jj), 'spearman': T.spearman([bh[x][e][k] for e in jj], [bh[y][e][k] for e in jj]),
                                            'alfa': T.kripp_alpha_ordinal([[bh[x][e][k], bh[y][e][k]] for e in jj])}
        if len(ish) > 2:
            r['guruh_alfa'] = T.kripp_alpha_ordinal([[bh[x][e][k] for x in ish if bh[x][e][k] is not None] for e in ee])
        out[d] = r
    return out


def main():
    if (CHIQ / 'tolqinlar_solishtirish.json').exists():
        sys.exit("TO'XTA: qoshimcha/tolqinlar_solishtirish.json mavjud — bir marta yuriladi")
    _, B, chiq, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))
    kirish = {f'iyul/{n}': sha(IYUL / n) for n in ('sentences.json', 's1_outputs.json', 's2_outputs.json', 's3_gemini_outputs.json',
                                                     'blind_key.json', 'returns/rater_B_filled.xlsx', 'returns/rater_C_filled.xlsx')}
    S = json.loads((IYUL / 'sentences.json').read_text(encoding='utf-8'))
    assert [r['id'] for r in S] == [r['id'] for r in B] and [r['ref_en'] for r in S] == [r['ref_en'] for r in B]
    ids = [r['id'] for r in S]
    lay = {r['id']: r['layer'] for r in S}
    ref = {r['id']: r['ref_en'] for r in S}
    io = {t: json.loads((IYUL / f).read_text(encoding='utf-8'))
          for t, f in (('s1', 's1_outputs.json'), ('s2', 's2_outputs.json'), ('gemini', 's3_gemini_outputs.json'))}
    R = {'maqom': "natijadan keyingi, qo'shimcha, prereg'da yo'q; tadqiqotchi so'rovi 2026-10-28",
         'baholovchilar_izoh': "iyul va oktyabr baholovchilari BOSHQA odamlar (tadqiqotchi, 2026-10-28)",
         'kirish_sha256': kirish, 'iyul_meta': {t: io[t].get('_meta') for t in io}, 'mt': {}, 'kkt_aynan': {}, 'baho': {}, 'tarqalish': {},
         'kelishuv': {}, 'baholovchilar': QAYD, 'baholovchilar_izohlar': QAYD_IZOH}
    # 1) MT metrikalari
    b1 = nat['jadvallar'][[k for k in nat['jadvallar'] if k.startswith('B1')][0]]
    b1q = {'hammasi': 'hammasi', 'flores': 'qatlam flores', 'train': 'qatlam train', 'gold': 'qatlam gold'}
    qat = {'hammasi': ids, **{L: [i for i in ids if lay[i] == L] for L in ('flores', 'train', 'gold')}}
    for L, ii in qat.items():
        rr = [[ref[i] for i in ii]]
        R['mt'][L] = {'iyul s1 (KKT)': T.korpus([io['s1'][i] for i in ii], rr), 'iyul gemini': T.korpus([io['gemini'][i] for i in ii], rr)}
        for t in ('KKT', 'Gemini'):
            k = T.korpus([chiq[t][('eval72', i)] for i in ii], rr)
            for m in ('bleu', 'chrf2', 'gap_bleu_ortacha_exp'):
                assert abs(k[m] - b1[b1q[L]][t]['1ref'][m]) < 1e-9, f'{L} {t} {m}: B1 bilan teng emas'
            R['mt'][L][f'okt {t}'] = k
        R['kkt_aynan'][L] = {'n': len(ii), 's1_okt_KKT': sum(io['s1'][i] == chiq['KKT'][('eval72', i)] for i in ii),
                             's2_okt_KKT': sum(io['s2'][i] == chiq['KKT'][('eval72', i)] for i in ii)}
    # 2) baholar
    bk = json.loads((IYUL / 'blind_key.json').read_text(encoding='utf-8'))
    bhI = {f'iyul {x}': iyul_baho(IYUL / 'returns' / f'rater_{x}_filled.xlsx') for x in ('B', 'C')}
    assert all(set(v) == set(bk) for v in bhI.values())
    kb = json.loads((SIKL / 'paket' / 'kalit_baho.json').read_text(encoding='utf-8'))['elementlar']
    bhO = {}
    for x in ('B', 'C', 'D'):
        q = T.oqi_xlsx(SIKL / 'qaytgan' / f'baho_{x}.xlsx', ('Element', 'Adequacy', 'Fluency'))
        bhO[f'okt {x}'] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in q}
    qE, _ = T.e_xom(SIKL)
    bhO['okt E'] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in qE}
    assert all(set(v) == set(kb) for v in bhO.values())
    bh = {**bhI, **bhO}
    for x, v in bhI.items():
        R['baho'][x] = {t: {d: ort([v[e][k] for e in bk if bk[e]['system'] == t]) for d, k in DAR} for t in IYUL_TIZ}
    for x, v in bhO.items():
        R['baho'][x] = {t: {d: ort([v[e][k] for e in kb if kb[e]['tizim'] == t]) for d, k in DAR} for t in ('KKT', 'Gemini')}
    for x, v in bh.items():
        R['tarqalish'][x] = {d: {'n': len(v), 'yoq': sum(a[k] is None for a in v.values()),
                                 'soni': {s: sum(a[k] == s for a in v.values()) for s in range(1, 6)}, 'sd': sd([a[k] for a in v.values()]),
                                 'ortacha': ort([a[k] for a in v.values()])} for d, k in DAR}
    # 3) kelishuv
    iq = {'hammasi': sorted(bk), 'KKT (s1+s2)': sorted(e for e in bk if bk[e]['system'] in ('s1', 's2')),
          'gemini': sorted(e for e in bk if bk[e]['system'] == 'gemini')}
    R['kelishuv']['iyul'] = {q: {'n': len(ee), **kelishuv(bh, ['iyul B', 'iyul C'], ee)} for q, ee in iq.items()}
    oq = {'hammasi': sorted(kb), 'KKT': sorted(e for e in kb if kb[e]['tizim'] == 'KKT'),
          'neyron': sorted(e for e in kb if kb[e]['tizim'] != 'KKT'), 'Gemini': sorted(e for e in kb if kb[e]['tizim'] == 'Gemini')}
    R['kelishuv']['okt B,C,D'] = {q: {'n': len(ee), **kelishuv(bh, ['okt B', 'okt C', 'okt D'], ee)} for q, ee in oq.items()}
    R['kelishuv']['okt B,C,D,E'] = {q: {'n': len(ee), **kelishuv(bh, ['okt B', 'okt C', 'okt D', 'okt E'], ee)} for q, ee in oq.items()}
    for nom, jd in (('okt B,C,D', nat['jadvallar']), ('okt B,C,D,E', nat['inson_E_bilan']['jadvallar'])):
        h7 = jd[[k for k in jd if k.startswith('H7') and 'SEZGIRLIK' in k][0]]
        for d, hk in (('mazmun', 'adequacy'), ('ravonlik', 'fluency')):
            assert abs(R['kelishuv'][nom]['hammasi'][d]['guruh_alfa'] - h7[hk]) < 1e-9, f'{nom} {d}: H7 SEZGIRLIK 72 bilan teng emas'
    (CHIQ / 'tolqinlar_solishtirish.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    md(R)
    print('qoshimcha/: tolqinlar_solishtirish.json, .md')


def md(R):
    f = lambda v: f'{v:.3f}' if isinstance(v, float) else str(v)
    f2 = lambda v: f'{v:.2f}'
    L = ["# TOLQIN-2 — ikki to'lqinni solishtirish (tolqinlar_solishtirish.py)", '', f"**{R['maqom']}**. Tasdiqlovchi emas.",
         f"{R['baholovchilar_izoh']}; harflar «iyul X» / «okt X». Oktyabr: 72 gap (360 element); iyul: 216 item. Bootstrap yo'q.",
         f"Iyul tizimlari: s1 {R['iyul_meta']['s1']}, gemini {R['iyul_meta']['gemini']}.", '',
         '## 1. MT metrikalari (1 etalon ref_en; korpus-BLEU / chrF2 / gap-BLEU o\'rtachasi)', '',
         '| qatlam | n | iyul s1 (KKT) | okt KKT | iyul gemini | okt Gemini | KKT aynan (s1 = okt) |', '|---|---|---|---|---|---|---|']
    for Lq, v in R['mt'].items():
        c = lambda k: f"{f2(v[k]['bleu'])} / {f2(v[k]['chrf2'])} / {f2(v[k]['gap_bleu_ortacha_exp'])}"
        a = R['kkt_aynan'][Lq]
        L.append(f"| {Lq} | {a['n']} | {c('iyul s1 (KKT)')} | {c('okt KKT')} | {c('iyul gemini')} | {c('okt Gemini')} | {a['s1_okt_KKT']}/{a['n']} |")
    L += ['', "KKT aynan ustuni faqat tizim shu 72 gapda qancha o'zgarganini ko'rsatadi (s2 = okt: "
          f"{R['kkt_aynan']['hammasi']['s2_okt_KKT']}/72).", '',
          '## 2. Baholovchi × tizim o\'rtachasi (mazmun / ravonlik)', '', '| baholovchi | tizim | mazmun | ravonlik |', '|---|---|---|---|']
    for x, v in R['baho'].items():
        for t, w in v.items():
            L.append(f"| {x} | {t} | {f2(w['mazmun'])} | {f2(w['ravonlik'])} |")
    L += ['', '### Ball tarqalishi (iyul 216, oktyabr 360 — fayl bo\'yicha)', '',
          '| baholovchi | o\'lchov | 1 | 2 | 3 | 4 | 5 | yo\'q | o\'rtacha | SD |', '|---|---|---|---|---|---|---|---|---|---|']
    for x, v in R['tarqalish'].items():
        for d, w in v.items():
            L.append(f"| {x} | {d} | " + ' | '.join(str(w['soni'][s]) for s in range(1, 6)) + f" | {w['yoq']} | {f2(w['ortacha'])} | {f2(w['sd'])} |")
    L += ['', '## 3. Kelishuv (juftlik Spearman ρ · juftlik α ordinal; guruh α; SD — har baholovchi, shu qism-to\'plamda)', '']
    for nom, v in R['kelishuv'].items():
        L += [f'### {nom}', '', '| qism-to\'plam | n | o\'lchov | ' + ' | '.join(next(iter(v.values()))['mazmun']['juftlik'])
              + ' | guruh α | SD |', '|---|---|---|' + '---|' * (len(next(iter(v.values()))['mazmun']['juftlik']) + 2)]
        for q, w in v.items():
            for d in ('mazmun', 'ravonlik'):
                u = w[d]
                L.append(f"| {q} | {w['n']} | {d} | " + ' | '.join(f"{f(p['spearman'])} · {f(p['alfa'])}" for p in u['juftlik'].values())
                         + f" | {f(u.get('guruh_alfa', float('nan'))) if 'guruh_alfa' in u else '—'} | "
                         + ', '.join(f"{x.split()[-1]} {f2(s)}" for x, s in u['sd'].items()) + ' |')
        L.append('')
    L += ['## 4. Baholovchilar (ombordagi yozuvlardan, ismsiz)', '', '| baholovchi | daraja | kasb | tarqatish | qaytish |', '|---|---|---|---|---|']
    for x, v in R['baholovchilar'].items():
        L.append(f"| {x} | {v['daraja']} | {v['kasb']} | {v['tarqatish']} | {v['qaytish']} |")
    L += [''] + [f'- {s}' for s in R['baholovchilar_izohlar']]
    (CHIQ / 'tolqinlar_solishtirish.md').write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
