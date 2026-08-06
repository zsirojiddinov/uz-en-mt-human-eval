# RW1 — INSON-BAHOLASH TAHLIL NATIJALARI


**Rejim:** REAL · **Sana:** 2026-07-03 · **Baholovchilar:** B, C · pre-reg: `analysis/rw1_prereg_analysis_plan.md`

## 0. Validatsiya

- Baholovchi fayllari: 2 ta.
- Nuqsonli item (biror baholovchida Mazmun bo'sh/xato) -> asosiy hisobdan chiqdi: **0** (yo'q).
- Valid item: **216** / 216.

## 1. Baholovchilararo kelishuv (juftlik-Spearman)

| Juftlik | Mazmun | Ravonlik |
|---|---|---|
| B-C | 0.53 | 0.487 |

Har baholovchi o'rtacha juftlik-Spearman (Mazmun): {'B': 0.53, 'C': 0.53}

Pre-reg outlier-band ishga tushmadi (chetlashtirish yo'q).

s1==s2 bayt-aynan probasi (52 juftlik): baholovchi Mazmun-farqi o'rtachasi {'B': 0.538, 'C': 0.0} (0 ga yaqin = izchil).

## 2. KORRELYATSIYA — ASOSIY (barcha baholovchi)  (n=216, bootstrap 1000, seed=20260703)

**Table 2 — Segment-daraja korrelyatsiya (inson Mazmun ↔ metrika):**

| Metrika | Spearman ρ | 95% CI | Pearson r |
|---|---|---|---|
| BLEU | 0.766 | [0.713, 0.805] | 0.662 |
| chrF | 0.698 | [0.618, 0.758] | 0.699 |
| KKT-RS-v1 | 0.223 | [0.08, 0.354] | 0.31 |
| KKT-RS-v2 | 0.569 | [0.469, 0.658] | 0.583 |

**Farq-CI (pre-reg muvaffaqiyat-mezoni — 0 ni istisno qilsa v2 aniq ustun):**

| Farq | Δρ | 95% CI | 0 istisno? |
|---|---|---|---|
| KKT-RS-v2 − BLEU | -0.197 | [-0.288, -0.112] | HA |
| KKT-RS-v2 − chrF | -0.129 | [-0.22, -0.038] | HA |

**Per-qatlam Spearman (Mazmun):**

| Qatlam | n | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |
|---|---|---|---|---|---|
| flores | 108 | 0.66 | 0.557 | -0.053 | 0.473 |
| train | 72 | 0.726 | 0.667 | -0.115 | 0.482 |
| gold | 36 | 0.289 | 0.302 | 0.232 | 0.222 |

**BLEU<10 kichik-to'plam Kendall-τ (past-ball rejim, n=112):** BLEU=0.156, chrF=0.018, KKT-RS-v1=-0.015, KKT-RS-v2=0.142


**Table 3 — Tizim-darajali (o'rtacha inson-Mazmun vs metrika o'rtachalari):**

| Tizim | n | inson-Mazmun | BLEU | chrF | KKT-RS-v1 | KKT-RS-v2 |
|---|---|---|---|---|---|---|
| s1 | 72 | 3.007 | 13.258 | 47.447 | 0.584 | 0.62 |
| s2 | 72 | 2.986 | 12.933 | 47.219 | 0.577 | 0.609 |
| gemini | 72 | 4.556 | 40.989 | 70.325 | 0.579 | 0.804 |
