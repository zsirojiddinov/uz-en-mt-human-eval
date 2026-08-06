# -*- coding: utf-8 -*-
"""RW1 — yakuniy hisobot yig'uvchi (results/rw1_report.md).

Konfirmator raqamlar results_tables.json dan (muzlatilgan analyze_human_eval.py chiqishi)
KO'CHIRILADI — qayta hisoblanmaydi. Qo'shimcha TAVSIFIY bloklar (ravonlik-korrelyatsiya,
s1-s2 juft-taqqoslash, rater-tavsif) shu yerda hisoblanadi va shunday belgilanadi.
"""
import json, os, sys
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from analyze_human_eval import spearman, read_rater_xlsx, load_context, METRICS

RESULTS = os.path.join(HERE, 'results')
metric, blind, layer = load_context()
tbl = json.load(open(os.path.join(HERE, 'results_tables.json'), encoding='utf-8'))
main = tbl['main']

B, _ = read_rater_xlsx(os.path.join(HERE, 'returns', 'rater_B_filled.xlsx'))
C, _ = read_rater_xlsx(os.path.join(HERE, 'returns', 'rater_C_filled.xlsx'))
items = [i for i in blind if B[i][0] is not None and C[i][0] is not None]

# --- tavsifiy: rater o'rtachalari ---
def rater_stats(R):
    m = [R[i][0] for i in items]; r = [R[i][1] for i in items]
    return (round(float(np.mean(m)), 2), round(float(np.std(m)), 2),
            round(float(np.mean(r)), 2), round(float(np.std(r)), 2))

# --- tavsifiy: ravonlik-korrelyatsiya (B+C o'rtacha ravonlik vs metrika) ---
rav_mean = {i: (B[i][1] + C[i][1]) / 2 for i in items}
rav_corr = {}
for mkey, mname in METRICS:
    mv = [metric[f"{blind[i]['gap_id']}::{blind[i]['system']}"][mkey] for i in items]
    rav_corr[mname] = round(spearman(mv, [rav_mean[i] for i in items]), 3)

# --- tavsifiy: s1 vs s2 juft-taqqoslash (gap-daraja, inson-Mazmun B+C o'rtacha) ---
rev = {}
for iid, meta in blind.items():
    rev.setdefault(meta['gap_id'], {})[meta['system']] = iid
adeq = {i: (B[i][0] + C[i][0]) / 2 for i in items}
w = t = l = 0
diffs = []
for g, m in rev.items():
    if 's1' in m and 's2' in m and m['s1'] in adeq and m['s2'] in adeq:
        d = adeq[m['s1']] - adeq[m['s2']]
        diffs.append(d)
        if d > 0: w += 1
        elif d < 0: l += 1
        else: t += 1
n_eff = w + l
# ikki tomonlama aniq sign-test
p_sign = (sum(comb(n_eff, k) for k in range(0, min(w, l) + 1)) * 2 / 2 ** n_eff) if n_eff else float('nan')
p_sign = min(1.0, p_sign)

mb, sb, rb, srb = rater_stats(B)
mc, sc, rc, src = rater_stats(C)

sup_path = os.path.join(RESULTS, 'supplementary_A_partial.md')

L = []
L.append("# RW1 — YAKUNIY HISOBOT (asosiy tahlil B+C, yakuniy maqom)")
L.append("")
L.append("**Sana:** 2026-07-14 (tahlil pre-reg 2026-07-11 erta-ishga-tushirish bandi bo'yicha). "
         "**Pre-reg:** `analysis/rw1_prereg_analysis_plan.md`. **Muzlatilgan skript:** "
         "`analyze_human_eval.py` (bir marta yuritildi). **Konfirmator manba:** "
         "`results/human_eval_results.md` + `results/results_tables.json`.")
L.append("")
L.append("## 1. Dizayn va baholovchilar")
L.append("")
L.append("- 216 item = 72 gap (LOCK, seed 72: flores 36 / train 24 / gold 12) × 3 tizim "
         "(s1, s2, gemini); bitta global blind aralashtirish (seed 216), tizim baholovchiga ko'rinmaydi.")
L.append("- **Rater B** — asosiy, to'liq 216/216. **Rater C** — asosiy, to'liq 216/216 "
         "(2026-07-06 qabul). **Rater A** — dastlabki mutaxassis chiqib ketdi (pre-reg 2026-07-11 bandi); "
         "o'rniga jalb qilingan mustaqil ingliz tili o'qituvchisi (IELTS 7.0) QISMAN 127/216 to'ldirdi → "
         "faqat supplementary (`supplementary_A_partial.md`), asosiy tahlilga kirmaydi.")
L.append("- Pilot (18 item, PIT-prefiks) — jarayon-arxivi, asosiy tahlilga aloqasi yo'q.")
L.append("- Asosiy tahlil 2026-07-07 stopping-qoidasi 3-bandi bo'yicha IKKI to'liq fayl (B+C) bilan "
         "yakuniy; uchinchi fayl keyin kelsa — faqat sensitivity-ilova.")
L.append("")
L.append("**Blind sifat-darvozalari (tahlildan oldin, tizim-kalitsiz): B PASS, C PASS.** "
         "216/216 to'liq (B da IT003 ham), barcha ballar 1-5 butun, eng uzun bir xil juftlik-seriya "
         "B=5 / C=6 (chegara 10), mazmun-ravonlik ichki Spearman B=0.666 / C=0.904 (oraliq 0.2-0.95).")
L.append("")
L.append("| Rater | Mazmun o'rt (σ) | Ravonlik o'rt (σ) |")
L.append("|---|---|---|")
L.append(f"| B | {mb} ({sb}) | {rb} ({srb}) |")
L.append(f"| C | {mc} ({sc}) | {rc} ({src}) |")
L.append("")
L.append("## 2. Baholovchilararo kelishuv (konfirmator)")
L.append("")
L.append("| Juftlik | Mazmun | Ravonlik |")
L.append("|---|---|---|")
for k, v in tbl['consensus']['pair'].items():
    L.append(f"| {k} | {v['mazmun']} | {v['ravonlik']} |")
L.append("")
L.append("Pre-reg outlier-band ishga tushmadi. s1==s2 bayt-aynan probasi (52 juftlik): "
         "Mazmun-farq o'rtachasi B=0.538, C=0.0.")
L.append("")
L.append("## 3. ASOSIY NATIJA — metrika ↔ inson korrelyatsiyasi (n=216, bootstrap 1000)")
L.append("")
L.append("**Inson-Mazmun (konfirmator, muzlatilgan skriptdan):**")
L.append("")
L.append("| Metrika | Spearman ρ | 95% CI | Pearson r | Ravonlik ρ (tavsifiy) |")
L.append("|---|---|---|---|---|")
for _, mn in METRICS:
    s = main['segment_spearman'][mn]
    L.append(f"| {mn} | {s['rho']} | [{s['ci95'][0]}, {s['ci95'][1]}] | "
             f"{main['segment_pearson'][mn]} | {rav_corr[mn]} |")
L.append("")
L.append("**Pre-reg muvaffaqiyat-mezoni (farq-CI 0 ni istisno qilsa v2 aniq ustun):**")
L.append("")
L.append("| Farq | Δρ | 95% CI | 0 istisno? | Talqin |")
L.append("|---|---|---|---|---|")
for k, v in main['diff_ci'].items():
    talqin = ("v2 ustun" if v['delta'] > 0 else "**TESKARI — bazaviy metrika ustun**") if v['excludes_0'] else "farq ishonchsiz"
    L.append(f"| {k} | {v['delta']} | [{v['ci95'][0]}, {v['ci95'][1]}] | "
             f"{'HA' if v['excludes_0'] else 'yo'+chr(39)+'q'} | {talqin} |")
L.append("")
L.append("**Xulosa (halollik §6 — kamayish yashirilmaydi):** pre-reg gipoteza TASDIQLANMADI. "
         "KKT-RS-v2 inson-mazmun bilan BLEU va chrF dan STATISTIK ANIQ PASTROQ korrelyatsiya qiladi "
         "(Δρ CI lari 0 ni istisno qiladi, manfiy tomonda). v2 v1 dan ancha yaxshi (0.569 vs 0.223) — "
         "MV2 modal-anker tuzatishi ishlagan, lekin umumiy-maqsadli sifat-bashoratchi sifatida v2 "
         "BLEU/chrF o'rnini bosa olmaydi. KKT-RS diagnostik/strukturaviy vosita maqomida qoladi.")
L.append("")
L.append("**Per-qatlam Spearman (Mazmun):**")
L.append("")
L.append("| Qatlam | n | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |")
L.append("|---|---|---|---|---|---|")
for Lr in ('flores', 'train', 'gold'):
    pl = main['per_layer'][Lr]
    L.append(f"| {Lr} | {pl['n']} | {pl['BLEU']} | {pl['chrF']} | {pl['KKT-RS-v1']} | {pl['KKT-RS-v2']} |")
L.append("")
L.append(f"BLEU<10 past-ball rejimda (n={main['low_bleu_kendall']['n']}) Kendall-τ: "
         + ", ".join(f"{mn}={main['low_bleu_kendall'][mn]}" for _, mn in METRICS)
         + " — past-ball zonada BLEU ham v2 ham kuchsiz, chrF deyarli signalsiz.")
L.append("")
L.append("## 4. Tizim-darajali natija")
L.append("")
L.append("| Tizim | n | inson-Mazmun | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |")
L.append("|---|---|---|---|---|---|---|")
for sysn, rec in main['system_level'].items():
    L.append(f"| {sysn} | {rec['n']} | {rec['human_mazmun']} | {rec['BLEU']} | {rec['chrF']} | "
             f"{rec['KKT-RS-v1']} | {rec['KKT-RS-v2']} |")
L.append("")
L.append("**s1 vs s2 juft-taqqoslash (tavsifiy; gap-daraja, inson-Mazmun B+C o'rtacha):** "
         f"s1 yutdi {w} / durang {t} / s2 yutdi {l} (72 gap); o'rtacha farq "
         f"{round(float(np.mean(diffs)), 3):+} ball; aniq sign-test p={round(p_sign, 3)} — "
         "farq ahamiyatsiz, s1≈s2 (52/72 gapda chiqish bayt-aynan edi).")
L.append("")
L.append("## 5. A-qisman supplementary")
L.append("")
L.append("`results/supplementary_A_partial.md` (POST-HOC, asosiy tahlilga kirmaydi): A-B mazmun 0.571, "
         "A-C mazmun 0.861; A qo'shilганда kesim-korrelyatsiyalar deyarli qimirlamaydi "
         "(BLEU 0.804→0.823, v2 0.601→0.608) — asosiy xulosa barqaror. Ogohlantirish: A ravonlik "
         "ustuni 127/127 mazmun bilan aynan bir xil (mustaqil ravonlik-signali yo'q).")
L.append("")
open(os.path.join(RESULTS, 'rw1_report.md'), 'w', encoding='utf-8').write("\n".join(L))
print(f"Yozildi: {os.path.join(RESULTS, 'rw1_report.md')}")
print(f"rater B: mazmun {mb}, ravonlik {rb}; rater C: mazmun {mc}, ravonlik {rc}")
print(f"s1 vs s2: W{w}/T{t}/L{l}, mean diff {round(float(np.mean(diffs)),3)}, p_sign={round(p_sign,3)}")
print(f"ravonlik-korrelyatsiya: {rav_corr}")
