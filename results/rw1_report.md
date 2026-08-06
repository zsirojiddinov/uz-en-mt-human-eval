# RW1 — YAKUNIY HISOBOT (asosiy tahlil B+C, yakuniy maqom)

**Sana:** 2026-07-14 (tahlil pre-reg 2026-07-11 erta-ishga-tushirish bandi bo'yicha). **Pre-reg:** `analysis/rw1_prereg_analysis_plan.md`. **Muzlatilgan skript:** `analyze_human_eval.py` (bir marta yuritildi). **Konfirmator manba:** `results/human_eval_results.md` + `results/results_tables.json`.

## 1. Dizayn va baholovchilar

- 216 item = 72 gap (LOCK, seed 72: flores 36 / train 24 / gold 12) × 3 tizim (s1, s2, gemini); bitta global blind aralashtirish (seed 216), tizim baholovchiga ko'rinmaydi.
- **Rater B** — asosiy, to'liq 216/216. **Rater C** — asosiy, to'liq 216/216 (2026-07-06 qabul). **Rater A** — dastlabki mutaxassis chiqib ketdi (pre-reg 2026-07-11 bandi); o'rniga jalb qilingan mustaqil ingliz tili o'qituvchisi (IELTS 7.0) QISMAN 127/216 to'ldirdi → faqat supplementary (`supplementary_A_partial.md`), asosiy tahlilga kirmaydi.
- Pilot (18 item, PIT-prefiks) — jarayon-arxivi, asosiy tahlilga aloqasi yo'q.
- Asosiy tahlil 2026-07-07 stopping-qoidasi 3-bandi bo'yicha IKKI to'liq fayl (B+C) bilan yakuniy; uchinchi fayl keyin kelsa — faqat sensitivity-ilova.

**Blind sifat-darvozalari (tahlildan oldin, tizim-kalitsiz): B PASS, C PASS.** 216/216 to'liq (B da IT003 ham), barcha ballar 1-5 butun, eng uzun bir xil juftlik-seriya B=5 / C=6 (chegara 10), mazmun-ravonlik ichki Spearman B=0.666 / C=0.904 (oraliq 0.2-0.95).

| Rater | Mazmun o'rt (σ) | Ravonlik o'rt (σ) |
|---|---|---|
| B | 3.76 (0.83) | 3.81 (0.76) |
| C | 3.27 (1.63) | 2.76 (1.92) |

## 2. Baholovchilararo kelishuv (konfirmator)

| Juftlik | Mazmun | Ravonlik |
|---|---|---|
| B-C | 0.53 | 0.487 |

Pre-reg outlier-band ishga tushmadi. s1==s2 bayt-aynan probasi (52 juftlik): Mazmun-farq o'rtachasi B=0.538, C=0.0.

## 3. ASOSIY NATIJA — metrika ↔ inson korrelyatsiyasi (n=216, bootstrap 1000)

**Inson-Mazmun (konfirmator, muzlatilgan skriptdan):**

| Metrika | Spearman ρ | 95% CI | Pearson r | Ravonlik ρ (tavsifiy) |
|---|---|---|---|---|
| BLEU | 0.766 | [0.713, 0.805] | 0.662 | 0.771 |
| chrF | 0.698 | [0.618, 0.758] | 0.699 | 0.675 |
| KKT-RS-v1 | 0.223 | [0.08, 0.354] | 0.31 | 0.177 |
| KKT-RS-v2 | 0.569 | [0.469, 0.658] | 0.583 | 0.591 |

**Pre-reg muvaffaqiyat-mezoni (farq-CI 0 ni istisno qilsa v2 aniq ustun):**

| Farq | Δρ | 95% CI | 0 istisno? | Talqin |
|---|---|---|---|---|
| KKT-RS-v2 − BLEU | -0.197 | [-0.288, -0.112] | HA | **TESKARI — bazaviy metrika ustun** |
| KKT-RS-v2 − chrF | -0.129 | [-0.22, -0.038] | HA | **TESKARI — bazaviy metrika ustun** |

**Xulosa (halollik §6 — kamayish yashirilmaydi):** pre-reg gipoteza TASDIQLANMADI. KKT-RS-v2 inson-mazmun bilan BLEU va chrF dan STATISTIK ANIQ PASTROQ korrelyatsiya qiladi (Δρ CI lari 0 ni istisno qiladi, manfiy tomonda). v2 v1 dan ancha yaxshi (0.569 vs 0.223) — MV2 modal-anker tuzatishi ishlagan, lekin umumiy-maqsadli sifat-bashoratchi sifatida v2 BLEU/chrF o'rnini bosa olmaydi. KKT-RS diagnostik/strukturaviy vosita maqomida qoladi.

**Per-qatlam Spearman (Mazmun):**

| Qatlam | n | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |
|---|---|---|---|---|---|
| flores | 108 | 0.66 | 0.557 | -0.053 | 0.473 |
| train | 72 | 0.726 | 0.667 | -0.115 | 0.482 |
| gold | 36 | 0.289 | 0.302 | 0.232 | 0.222 |

BLEU<10 past-ball rejimda (n=112) Kendall-τ: BLEU=0.156, chrF=0.018, KKT-RS-v1=-0.015, KKT-RS-v2=0.142 — past-ball zonada BLEU ham v2 ham kuchsiz, chrF deyarli signalsiz.

## 4. Tizim-darajali natija

| Tizim | n | inson-Mazmun | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |
|---|---|---|---|---|---|---|
| s1 | 72 | 3.007 | 13.258 | 47.447 | 0.584 | 0.62 |
| s2 | 72 | 2.986 | 12.933 | 47.219 | 0.577 | 0.609 |
| gemini | 72 | 4.556 | 40.989 | 70.325 | 0.579 | 0.804 |

**s1 vs s2 juft-taqqoslash (tavsifiy; gap-daraja, inson-Mazmun B+C o'rtacha):** s1 yutdi 18 / durang 40 / s2 yutdi 14 (72 gap); o'rtacha farq +0.021 ball; aniq sign-test p=0.597 — farq ahamiyatsiz, s1≈s2 (52/72 gapda chiqish bayt-aynan edi).

## 5. A-qisman supplementary

`results/supplementary_A_partial.md` (POST-HOC, asosiy tahlilga kirmaydi): A-B mazmun 0.571, A-C mazmun 0.861; A qo'shilганда kesim-korrelyatsiyalar deyarli qimirlamaydi (BLEU 0.804→0.823, v2 0.601→0.608) — asosiy xulosa barqaror. Ogohlantirish: A ravonlik ustuni 127/127 mazmun bilan aynan bir xil (mustaqil ravonlik-signali yo'q).
