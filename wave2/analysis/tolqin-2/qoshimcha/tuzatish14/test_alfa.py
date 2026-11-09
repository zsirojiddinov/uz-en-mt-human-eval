# -*- coding: utf-8 -*-
"""TOLQIN-2 — tuzatish 14 (Q15, 3-band): tahlil.kripp_alpha_ordinal tekshiruvi.

    ~/.venvs/tolqin2_comet/bin/python analysis/tolqin-2/qoshimcha/tuzatish14/test_alfa.py

Holatlar:
  K2011 — Krippendorff, K. (2011). Computing Krippendorff's alpha-reliability (Annenberg School, U. Pennsylvania),
          4 kodlovchi × 12 birlik, yo'q qiymatlar bilan; nashr etilgan ordinal α = 0,815 (3 xona).
  sintetik — to'liq kelishuv (α = 1); 2 baholovchi, bo'sh katak bilan to'liq kelishuv (α = 1); juftlangan baholarda
          bitta qiymat (aniqlanmaydi, nan); 3 baholovchi, bitta birlikda bitta baho (birlik tashlanadi — natija
          o'sha birliksiz hisob bilan teng).
"""
import importlib.util
import math
from pathlib import Path

# Krippendorff (2011), reliability data matrix: qatorlar — kodlovchilar A–D, ustunlar — birliklar 1–12; None — yo'q
_K2011 = [
    [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None],
    [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3],
    [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None],
    [1, 2, 3, 3, 2, 4, 4, 1, 2, 5, 1, None],
]


def _birlik(matritsa):
    return [[r[j] for r in matritsa if r[j] is not None] for j in range(len(matritsa[0]))]


def hammasi(alfa):
    out = []

    def yoz(holat, kutilgan, x, shart):
        out.append({'holat': holat, 'kutilgan': kutilgan, 'hisoblangan': x, 'otdi': bool(shart)})

    x = alfa(_birlik(_K2011))
    yoz('K2011 ordinal (4×12, yo\'q qiymatlar)', '0,815', x, round(x, 3) == 0.815)
    x = alfa([[1, 1, 1], [2, 2, 2], [5, 5, 5], [3, 3, 3]])
    yoz("to'liq kelishuv, 3 baholovchi", '1', x, abs(x - 1) < 1e-12)
    x = alfa([[1, 1], [2, 2], [4], [5, 5]])
    yoz("to'liq kelishuv, 2 baholovchi + bo'sh katak", '1', x, abs(x - 1) < 1e-12)
    x = alfa([[3, 3], [3, 3], [3]])
    yoz('juftlangan baholarda bitta qiymat', 'nan', x, math.isnan(x))
    a = alfa([[1, 2, 2], [3, 3, 4], [5, 4, 5], [2]])
    b = alfa([[1, 2, 2], [3, 3, 4], [5, 4, 5]])
    yoz('m < 2 birlik tashlanadi', f'{b:.6f}', a, abs(a - b) < 1e-12)
    return out


if __name__ == '__main__':
    SIKL = Path(__file__).resolve().parents[2]
    sp = importlib.util.spec_from_file_location('tahlil_t', str(SIKL / 'tahlil.py'))
    T = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(T)
    r = hammasi(T.kripp_alpha_ordinal)
    for c in r:
        print(('OK  ' if c['otdi'] else 'XATO') + f"  {c['holat']}: kutilgan {c['kutilgan']}, hisoblangan {c['hisoblangan']}")
    assert all(c['otdi'] for c in r), 'α testi yiqildi'
