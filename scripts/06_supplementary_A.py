# -*- coding: utf-8 -*-
"""RW1 — A-QISMAN SUPPLEMENTARY TAHLIL (post-hoc, asosiy tahlilga KIRMAYDI).

Pre-reg band: "Sanali tuzatish 2026-07-11 — A-rol baholovchisi" (analysis/rw1_prereg_analysis_plan.md).
Faqat A to'ldirgan itemlar kesimida:
  (a) juft Spearman kelishuvlar A-B, A-C (mazmun va ravonlik alohida);
  (b) o'sha kesimda metrika-korrelyatsiyalar: B+C (asosiy tarkib) vs A+B+C (uch baholovchi
      o'rtachasi) — farqlar faqat MA'LUMOT uchun.
analyze_human_eval.py (muzlatilgan) dan statistika-funksiyalar import qilinadi — unga TEGILMAYDI.

Chiqish: evaluation/eval72/results/supplementary_A_partial.md
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze_human_eval import (spearman, read_rater_xlsx, load_context, METRICS)

RESULTS = os.path.join(HERE, 'results')
os.makedirs(RESULTS, exist_ok=True)

metric, blind, layer = load_context()

A, errsA = read_rater_xlsx(os.path.join(HERE, 'supplementary', 'rater_A_partial.xlsx'))
B, _ = read_rater_xlsx(os.path.join(HERE, 'returns', 'rater_B_filled.xlsx'))
C, _ = read_rater_xlsx(os.path.join(HERE, 'returns', 'rater_C_filled.xlsx'))

# A to'ldirgan itemlar kesimi (mazmun ham ravonlik ham bor)
subset = [i for i in blind if i in A and A[i][0] is not None and A[i][1] is not None
          and i in B and B[i][0] is not None and i in C and C[i][0] is not None]
nA = len(subset)

# A ravonlik==mazmun tekshiruvi (sifat-qayd)
rav_eq = sum(1 for i in subset if A[i][0] == A[i][1])

# (a) juft kelishuvlar
def pair_sp(X, Y, which):
    return round(spearman([X[i][which] for i in subset], [Y[i][which] for i in subset]), 3)

agree = {
    'A-B': {'mazmun': pair_sp(A, B, 0), 'ravonlik': pair_sp(A, B, 1)},
    'A-C': {'mazmun': pair_sp(A, C, 0), 'ravonlik': pair_sp(A, C, 1)},
    'B-C (shu kesim)': {'mazmun': pair_sp(B, C, 0), 'ravonlik': pair_sp(B, C, 1)},
}

# (b) metrika-korrelyatsiyalar shu kesimda: B+C vs A+B+C
def human_mean(raters, i):
    return sum(r[i][0] for r in raters) / len(raters)

def corr_table(raters):
    out = {}
    hv = [human_mean(raters, i) for i in subset]
    for mkey, mname in METRICS:
        mv = [metric[f"{blind[i]['gap_id']}::{blind[i]['system']}"][mkey] for i in subset]
        out[mname] = round(spearman(mv, hv), 3)
    return out

corr_bc = corr_table([B, C])
corr_abc = corr_table([A, B, C])

# asosiy (to'liq 216, B+C) qiymatlar — faqat taqqoslash uchun o'qiladi
main_tbl = json.load(open(os.path.join(HERE, 'results_tables.json'), encoding='utf-8'))['main']
corr_main = {mn: main_tbl['segment_spearman'][mn]['rho'] for _, mn in METRICS}

# kesim-tarkibi (qatlam/tizim bo'yicha — to'ldirish tasodifiymi ko'rish uchun)
from collections import Counter
lay_cnt = Counter(layer[blind[i]['gap_id']] for i in subset)
sys_cnt = Counter(blind[i]['system'] for i in subset)

L = []
L.append("# RW1 — A-QISMAN SUPPLEMENTARY TAHLIL")
L.append("")
L.append("> **POST-HOC QO'SHIMCHA, asosiy tahlilga kirmaydi.** Asosiy konfirmator natija —")
L.append("> `results/human_eval_results.md` (B+C, 216 item). Bu hujjat pre-reg 2026-07-11")
L.append("> A-bandi bo'yicha faqat A to'ldirgan itemlar kesimidagi qo'shimcha tahlil.")
L.append("")
L.append(f"**Kesim:** A to'liq to'ldirgan {nA} item (216 dan). "
         f"Qatlam: {dict(lay_cnt)}. Tizim: {dict(sys_cnt)}.")
L.append("")
L.append(f"**Sifat-qayd:** A faylida ravonlik ustuni {rav_eq}/{nA} itemda mazmun bilan AYNAN bir xil — "
         "A ning ravonlik-bahosi mustaqil signal emas (bitta umumiy ball berilgan ko'rinadi). "
         "Ravonlik-kelishuvlari shu ogohlantirish bilan o'qilsin.")
L.append("")
L.append("## (a) Juft kelishuvlar (Spearman, shu kesimda)")
L.append("")
L.append("| Juftlik | Mazmun | Ravonlik |")
L.append("|---|---|---|")
for k, v in agree.items():
    L.append(f"| {k} | {v['mazmun']} | {v['ravonlik']} |")
L.append("")
L.append("## (b) Metrika-korrelyatsiyalar (inson-Mazmun o'rtachasi ↔ metrika, Spearman)")
L.append("")
L.append(f"| Metrika | Asosiy B+C (n=216) | B+C (kesim, n={nA}) | A+B+C (kesim, n={nA}) | Δ(A qo'shilgani) |")
L.append("|---|---|---|---|---|")
for _, mn in METRICS:
    d = round(corr_abc[mn] - corr_bc[mn], 3)
    L.append(f"| {mn} | {corr_main[mn]} | {corr_bc[mn]} | {corr_abc[mn]} | {d:+} |")
L.append("")
L.append("Δ = shu kesimda A ni qo'shish korrelyatsiyani qancha o'zgartirgani (faqat ma'lumot uchun; ")
L.append("bootstrap-CI hisoblanmagan, konfirmator maqomi YO'Q).")
L.append("")
open(os.path.join(RESULTS, 'supplementary_A_partial.md'), 'w', encoding='utf-8').write("\n".join(L))
print(f"Yozildi: {os.path.join(RESULTS, 'supplementary_A_partial.md')}")
print(f"kesim n={nA}, kelishuvlar: {agree}")
print(f"korrelyatsiyalar B+C kesim: {corr_bc}")
print(f"korrelyatsiyalar A+B+C kesim: {corr_abc}")
