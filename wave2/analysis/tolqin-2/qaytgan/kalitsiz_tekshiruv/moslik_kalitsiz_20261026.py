"""TOLQIN-2 — baholovchilar mosligi, tizim KALITISIZ (tuzatish 10, (h) band).

2026-10-26 da rejalashtiruvchi (Claude) tomonidan ombordan tashqarida yurgizilgan hisobning aynan nusxasi.
Kirish: to'rt qaytarma (baho_B/C/D/E.xlsx, 26-oktyabrdagi asl fayllar), 'Baholash' varag'i:
  Element | O'zbekcha gap | Inglizcha tarjima | Mazmun (1-5) | Ravonlik (1-5)
Elementlar paketlar bo'ylab (manba gap, tarjima) juftligi bo'yicha tekislanadi — element kodi va tizim
kaliti ishlatilmaydi. Chiqish: har baholovchi tarqalishi, juftlik Spearman, Krippendorff α (ordinal).

Ishga tushirish: python3 -I moslik_kalitsiz_20261026.py <papka>   (papkada baho_*.xlsx)
"""
import glob, itertools, os, sys
import numpy as np
import openpyxl
from scipy.stats import spearmanr


def yukla(papka):
    data = {}
    for f in sorted(glob.glob(os.path.join(papka, '*baho_*.xlsx'))):
        r = os.path.basename(f).split('baho_')[1][0]
        ws = openpyxl.load_workbook(f, data_only=True)['Baholash']
        d = {}
        for row in ws.iter_rows(min_row=2, values_only=True):
            key = (str(row[1]).strip(), str(row[2]).strip())
            m = int(row[3]) if row[3] not in (None, '') else np.nan
            fl = int(row[4]) if row[4] not in (None, '') else np.nan
            d[key] = (m, fl)
        data[r] = d
    return data


def kripp_alpha_ordinal(mat):
    """mat: baholovchilar x elementlar, nan = yo'q ma'lumot. Krippendorff α, ordinal metrika."""
    vals = sorted(set(v for v in mat.flatten() if not np.isnan(v)))
    idx = {c: i for i, c in enumerate(vals)}
    o = np.zeros((len(vals), len(vals)))
    for j in range(mat.shape[1]):
        col = mat[:, j]; col = col[~np.isnan(col)]; m = len(col)
        if m < 2:
            continue
        for p in range(m):
            for q in range(m):
                if p != q:
                    o[idx[col[p]], idx[col[q]]] += 1 / (m - 1)
    n = o.sum(); nc = o.sum(1)

    def delta(i, j):
        if i == j:
            return 0.0
        lo, hi = min(i, j), max(i, j)
        return (nc[lo:hi + 1].sum() - (nc[lo] + nc[hi]) / 2) ** 2

    Do = sum(o[i, j] * delta(i, j) for i in range(len(vals)) for j in range(len(vals)))
    De = sum(nc[i] * nc[j] * delta(i, j) for i in range(len(vals)) for j in range(len(vals))) / (n - 1)
    return 1 - Do / De


def main(papka):
    data = yukla(papka)
    raters = sorted(data)
    keys = sorted(set.intersection(*[set(d) for d in data.values()]))
    print('baholovchilar:', raters, '| umumiy tekislangan elementlar:', len(keys))

    def vec(r, i):
        return np.array([data[r][k][i] for k in keys], float)

    for r in raters:
        for i, nm in enumerate(['Mazmun', 'Ravonlik']):
            v = vec(r, i); vv = v[~np.isnan(v)]
            dist = {int(c): int((vv == c).sum()) for c in sorted(set(vv))}
            print(f'  {r} {nm}: n={len(vv)} mean={vv.mean():.2f} sd={vv.std():.2f} tarqalish={dist}')
    print('juftlik Spearman (Mazmun | Ravonlik):')
    for a, b in itertools.combinations(raters, 2):
        out = []
        for i in (0, 1):
            x, y = vec(a, i), vec(b, i); ok = ~np.isnan(x) & ~np.isnan(y)
            out.append(f'{spearmanr(x[ok], y[ok]).correlation:.3f}')
        print(f'  {a}-{b}: {out[0]} | {out[1]}')
    for i, nm in enumerate(['Mazmun', 'Ravonlik']):
        for grp in [''.join(raters), 'BCD', 'BC', 'BCE']:
            if all(g in raters for g in grp):
                mat = np.array([vec(g, i) for g in grp])
                print(f'  alpha(ordinal) {nm} {grp}: {kripp_alpha_ordinal(mat):.3f}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
