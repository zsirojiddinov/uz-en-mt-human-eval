# -*- coding: utf-8 -*-
"""TOLQIN-2 — QO'SHIMCHA TAHLIL. NATIJADAN KEYINGI, QO'SHIMCHA; PREREG'DA YO'Q; tadqiqotchi so'rovi 2026-10-27.
Tasdiqlovchi emas. Muzlatilgan tahlil.py ga tegmaydi — undan faqat funksiyalar (spearman, kripp_alpha_ordinal, oqi_xlsx,
e_xom, ort10 qoidasi) va konstantalar import qilinadi. natija/* faqat O'QILADI (H7 nuqtaviy qiymati bilan solishtirish).

    python3 analysis/tolqin-2/qoshimcha_tahlil.py      # bir marta; qoshimcha/qoshimcha_natija.json mavjud bo'lsa TO'XTAYDI

Ikki to'plam — asosiy (B, C, D) va «E bilan» (B, C, D, E; E — qaytgan/xom/E__baho_E.xlsx), tuzatish 10 (d), (g) bo'yicha;
element to'plami — ASOSIY 71 gap (gold-00 siz, tuzatish 7), 355 element. Yo'q kataklar (tuzatish 10 (g)) juftlik bo'yicha chiqariladi.
(a) baholovchi × tizim o'rtachalari (mazmun, ravonlik), har baholovchining tizim tartibi, KKT eng pastmi;
(b) Krippendorff α (ordinal) va juftlik Spearman: bootstrap 1000, seed 20261027, GAP bo'yicha qayta tanlash (tanlangan gapning
    5 elementi birga), persentil 95 % CI;
(c) har baholovchining ball tarqalishi (1…5 soni va ulushi), 360 element (H1 kabi fayl bo'yicha).
Chiqish: qoshimcha/qoshimcha_natija.json, qoshimcha/qoshimcha_natija.md.
"""
import importlib.util
import json
import random
import sys
from pathlib import Path

SIKL = Path(__file__).resolve().parent
CHIQ = SIKL / 'qoshimcha'
SEED, BOOT = 20261027, 1000
_sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))
T = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(T)


def baholar():
    """{X: {element: (mazmun|None, ravonlik|None)}} — qaytgan/baho_{B,C,D}.xlsx va E asl fayli (tahlil.py bilan bir xil o'qish)."""
    bh = {}
    for x in ('B', 'C', 'D'):
        q = T.oqi_xlsx(SIKL / 'qaytgan' / f'baho_{x}.xlsx', ('Element', 'Adequacy', 'Fluency'))
        bh[x] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in q}
    qE, _ = T.e_xom(SIKL)
    bh['E'] = {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in qE}
    return bh


def ort(v):
    v = [a for a in v if a is not None]
    return sum(v) / len(v) if v else float('nan')


def kelishuv(bh, ish, gaplar, el_gap, k):
    ee = [e for g in gaplar for e in el_gap[g]]
    alfa = T.kripp_alpha_ordinal([[bh[x][e][k] for x in ish if bh[x][e][k] is not None] for e in ee])
    sp = {}
    for i, x in enumerate(ish):
        for y in ish[i + 1:]:
            jj = [e for e in ee if bh[x][e][k] is not None and bh[y][e][k] is not None]
            sp[f'{x}–{y}'] = T.spearman([bh[x][e][k] for e in jj], [bh[y][e][k] for e in jj])
    return alfa, sp


def ci(v):
    v = sorted(a for a in v if a == a)
    return [v[int(0.025 * len(v))], v[min(len(v) - 1, int(0.975 * len(v)))]] if len(v) >= BOOT // 2 else [float('nan')] * 2


def main():
    if (CHIQ / 'qoshimcha_natija.json').exists():
        sys.exit("TO'XTA: qoshimcha/qoshimcha_natija.json mavjud — bir marta yuriladi")
    kb = json.loads((SIKL / 'paket' / 'kalit_baho.json').read_text(encoding='utf-8'))
    el = kb['elementlar']
    tiz = {e: v['tizim'] for e, v in el.items()}
    bh = baholar()
    el_gap = {}
    for e in sorted(el):
        if el[e]['id'] not in T.CHIQ7:
            el_gap.setdefault(el[e]['id'], []).append(e)
    gaplar = sorted(el_gap)
    eids = [e for g in gaplar for e in el_gap[g]]
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))
    R = {'maqom': "natijadan keyingi, qo'shimcha; prereg'da yo'q; tadqiqotchi so'rovi 2026-10-27",
         'element': len(eids), 'gap': len(gaplar), 'bootstrap': {'n': BOOT, 'seed': SEED, 'birlik': 'gap'}, 'tarqalish': {}, 'toplam': {}}
    for x in ('B', 'C', 'D', 'E'):                                  # (c) — 360 element, fayl bo'yicha
        R['tarqalish'][x] = {d: {'soni': {s: sum(v[k] == s for v in bh[x].values()) for s in range(1, 6)},
                                 'yoq': sum(v[k] is None for v in bh[x].values()),
                                 'ulush_5': sum(v[k] == 5 for v in bh[x].values()) / sum(v[k] is not None for v in bh[x].values())}
                             for d, k in (('mazmun', 0), ('ravonlik', 1))}
    for nom, ish, h7 in (('asosiy B,C,D', ['B', 'C', 'D'], nat['jadvallar']),
                         ('E bilan B,C,D,E', ['B', 'C', 'D', 'E'], nat['inson_E_bilan']['jadvallar'])):
        S = R['toplam'][nom] = {'baholovchilar': ish, 'a': {}, 'b': {}}
        for x in ish:                                               # (a)
            m = {t: {d: ort([bh[x][e][k] for e in eids if tiz[e] == t]) for d, k in (('mazmun', 0), ('ravonlik', 1))}
                 for t in T.TIZIMLAR}
            S['a'][x] = {'ortacha': m,
                         'tartib': {d: sorted(T.TIZIMLAR, key=lambda t: -m[t][d]) for d in ('mazmun', 'ravonlik')},
                         'KKT_eng_past': {d: all(m['KKT'][d] < m[t][d] for t in T.TIZIMLAR if t != 'KKT') for d in ('mazmun', 'ravonlik')}}
        h7k = [k for k in h7 if k.startswith('H7') and 'ASOSIY' in k][0]
        for d, k in (('mazmun', 0), ('ravonlik', 1)):              # (b)
            a0, s0 = kelishuv(bh, ish, gaplar, el_gap, k)
            rnd = random.Random(SEED)
            av, sv = [], {p: [] for p in s0}
            for _ in range(BOOT):
                gg = [gaplar[rnd.randrange(len(gaplar))] for _ in gaplar]
                a, s = kelishuv(bh, ish, gg, el_gap, k)
                av.append(a)
                for p in s:
                    sv[p].append(s[p])
            S['b'][d] = {'alfa': a0, 'alfa_ci95': ci(av),
                         'alfa_tahlil_py_H7': h7[h7k]['adequacy' if k == 0 else 'fluency'],
                         'spearman': {p: {'rho': s0[p], 'ci95': ci(sv[p])} for p in s0}}
            assert abs(a0 - S['b'][d]['alfa_tahlil_py_H7']) < 1e-9, f'{nom} {d}: α tahlil.py H7 bilan teng emas'
    CHIQ.mkdir()
    (CHIQ / 'qoshimcha_natija.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    f = lambda v: f'{v:.3f}' if isinstance(v, float) else str(v)
    L = ['# TOLQIN-2 — qo\'shimcha tahlil (qoshimcha_tahlil.py)', '', f"**{R['maqom']}**. Tasdiqlovchi emas.",
         f"Element {R['element']} (71 gap, gold-00 siz); bootstrap {BOOT}, seed {SEED}, gap bo'yicha.", '']
    for nom, S in R['toplam'].items():
        L += [f'## {nom}', '', '### (a) baholovchi × tizim o\'rtachasi (mazmun / ravonlik)', '',
              '| baholovchi | ' + ' | '.join(T.TIZIMLAR) + ' | tartib (mazmun) | KKT eng past (m / r) |',
              '|---|' + '---|' * (len(T.TIZIMLAR) + 2)]
        for x, v in S['a'].items():
            L.append(f'| {x} | ' + ' | '.join(f"{f(v['ortacha'][t]['mazmun'])} / {f(v['ortacha'][t]['ravonlik'])}" for t in T.TIZIMLAR)
                     + f" | {' > '.join(v['tartib']['mazmun'])} | {'ha' if v['KKT_eng_past']['mazmun'] else 'YO‘Q'} / "
                     f"{'ha' if v['KKT_eng_past']['ravonlik'] else 'YO‘Q'} |")
        L += ['', '### (b) kelishuv, 95 % CI', '', '| o\'lchov | α (ordinal) [CI] | ' + ' | '.join(S['b']['mazmun']['spearman']) + ' |',
              '|---|---|' + '---|' * len(S['b']['mazmun']['spearman'])]
        for d, v in S['b'].items():
            L.append(f"| {d} | {f(v['alfa'])} [{f(v['alfa_ci95'][0])}; {f(v['alfa_ci95'][1])}] | "
                     + ' | '.join(f"{f(s['rho'])} [{f(s['ci95'][0])}; {f(s['ci95'][1])}]" for s in v['spearman'].values()) + ' |')
        L.append('')
    L += ['## (c) ball tarqalishi (360 element, fayl bo\'yicha)', '', '| baholovchi | o\'lchov | 1 | 2 | 3 | 4 | 5 | yo\'q | 5 ulushi |',
          '|---|---|---|---|---|---|---|---|---|']
    for x, v in R['tarqalish'].items():
        for d, w in v.items():
            L.append(f'| {x} | {d} | ' + ' | '.join(str(w['soni'][s]) for s in range(1, 6)) + f" | {w['yoq']} | {w['ulush_5']:.1%} |")
    (CHIQ / 'qoshimcha_natija.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('qoshimcha/: json, md')


if __name__ == '__main__':
    main()
