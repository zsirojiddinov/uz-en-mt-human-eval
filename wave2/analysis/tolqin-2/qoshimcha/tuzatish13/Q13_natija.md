# TOLQIN-2 — Q13 natijalari (t13.py)

**natijadan keyingi, taqriz-asosli (Gemini 3 Pro va ChatGPT taqrizlari, 2026-11-06); EXPLORATORY; muzlatilgan natija/ va etalon/ fayllari o'zgarmagan**.

Muhit: sacreBLEU 2.6.0, numpy 1.26.4, scipy 1.13.1, Python 3.9.6. Seed 20261106, 10000 qayta tanlash.

## 1. T1 sezgirligi

### 1a. T1 bor 71 gap (n = 71)

| tizim | asl | asl+T1 | faqat T1 | Δ (asl+T1 − asl) |
|---|---|---|---|---|
| KKT | 6.55 | 7.95 | 4.21 | 1.40 |
| Gemini | 44.14 | 57.76 | 37.13 | 13.62 |
| Claude | 56.64 | 67.18 | 36.12 | 10.54 |
| GPT | 40.94 | 63.26 | 46.46 | 22.31 |
| GT | 47.99 | 61.44 | 37.32 | 13.45 |

Neyron reyting: asl — Claude > GT > Gemini > GPT; asl+T1 — Claude > GPT > GT > Gemini; faqat_T1 — GPT > GT > Gemini > Claude

### 1b. Biror tizim chiqishi bilan aynan T1 gaplari (ekspozitsiya_2.norm_tok bo'yicha teng (etalon_tekshir.py dagidek))

Noyob gaplar: 7. Tizim bo'yicha: KKT 1, Gemini 4, Claude 3, GPT 6, GT 3.

| gap | tizimlar (norm) | aynan xom |
|---|---|---|
| flores-08 | Gemini, GPT | Gemini, GPT |
| flores-09 | GT | GT |
| train-06 | GPT | GPT |
| gold-05 | GPT | GPT |
| gold-06 | Gemini, Claude, GPT | Gemini, GPT |
| gold-07 | Gemini, Claude, GPT, GT | Gemini, GPT, GT |
| gold-08 | KKT, Gemini, Claude, GPT, GT | KKT, Gemini, Claude, GPT |

### 1c. Aynan gaplarsiz (n = 64)

| tizim | asl | asl+T1 | faqat T1 | Δ (asl+T1 − asl) |
|---|---|---|---|---|
| KKT | 5.48 | 6.74 | 3.00 | 1.26 |
| Gemini | 44.30 | 57.41 | 36.04 | 13.11 |
| Claude | 56.48 | 66.82 | 35.24 | 10.34 |
| GPT | 40.80 | 62.16 | 44.75 | 21.36 |
| GT | 48.22 | 61.28 | 36.33 | 13.06 |

Neyron reyting: asl — Claude > GT > Gemini > GPT; asl+T1 — Claude > GPT > GT > Gemini; faqat_T1 — GPT > GT > Gemini > Claude

### 1d. Leave-one-sentence-out (asl+T1, 4 neyron)

Asos reyting: Claude > GPT > GT > Gemini. 71 tashlashdan reyting o'zgargani: 0.

## 2. P1: Bonferroni 99 % juftlashgan bootstrap (72 gap)

5 taqqoslash, oilaviy α 0,05 -> har biriga 0,01 (99 %); juftlashgan: bir xil gap qayta tanlash 1 va 2 etalon uchun; persentil; 72 gap (prereg P1).

| tizim | Δ | 99 % (Bonferroni) | 95 % (shu namuna) | 0 ichida (99 %) |
|---|---|---|---|---|
| KKT | 1.37 | [0.67; 2.29] | [0.80; 2.05] | yo‘q |
| Gemini | 13.33 | [9.23; 18.02] | [10.11; 16.90] | yo‘q |
| Claude | 10.28 | [6.61; 14.41] | [7.31; 13.36] | yo‘q |
| GPT | 21.76 | [16.28; 27.73] | [17.44; 26.12] | yo‘q |
| GT | 13.14 | [9.05; 17.50] | [9.95; 16.43] | yo‘q |

## 3. BCa 95 %

scipy.stats.bootstrap, method='BCa', 10 000; α — gap-klaster (71 gap, har birida 5 element); ρ — tizim ichida har gapda bitta element, shuning uchun element = gap.

| kattalik | qiymat | BCa 95 % |
|---|---|---|
| α (B,C,D) mazmun | 0.115 | [0.031; 0.204] |
| α (B,C,D) ravonlik | -0.079 | [-0.151; 0.002] |
| ρ tizim ichida Gemini (n 71) | 0.116 | [-0.121; 0.347] (H4 persentil: [-0.127; 0.359]) |
| ρ tizim ichida Claude (n 71) | -0.109 | [-0.343; 0.151] (H4 persentil: [-0.358; 0.143]) |
| ρ tizim ichida GPT (n 71) | -0.007 | [-0.256; 0.248] (H4 persentil: [-0.250; 0.274]) |
| ρ tizim ichida GT (n 71) | -0.063 | [-0.308; 0.201] (H4 persentil: [-0.298; 0.198]) |

## 4. Pooled neyron ρ va η²

ρ(gap-BLEU_1ref, mazmun o'rtachasi), 284 element / 71 gap: -0.019, 95 % (gap-klaster persentil) [-0.196; 0.159].
η² (tizim): neyron 4 tizim (284) 0.005; hammasi 5 tizim (355) 0.299. y — B,C,D mazmun o'rtachasi (yo'q kataklar chiqarilgan); η² = SS_tizim / SS_jami.

## 5. Juftlik Spearman — SEZGIRLIK 72 (360 element; yo'q kataklar juftlik bo'yicha chiqarilgan)

| o'lchov | juftlik | KKT (n) | neyron (n) | hammasi (H6) |
|---|---|---|---|---|
| ravonlik | B–C | 0.588 (72) | 0.216 (286) | 0.294 (358) |
| ravonlik | C–D | 0.322 (72) | 0.080 (287) | 0.188 (359) |
| ravonlik | B–D | 0.192 (72) | 0.071 (285) | 0.254 (357) |
| mazmun | B–C | 0.651 (72) | 0.262 (286) | 0.322 (358) |
| mazmun | C–D | 0.576 (72) | 0.249 (288) | 0.338 (360) |
| mazmun | B–D | 0.373 (72) | 0.181 (286) | 0.357 (358) |

## 6. α implementatsiyasi

Krippendorff α o'z kodi bilan hisoblangan (tahlil.kripp_alpha_ordinal, sof Python; tashqi paket yo'q). Birlik — element (gap × tizim chiqishi), qiymatlar — baholovchilar balli (1–5). Har birlikdagi mavjud baholar o'zaro juftlanib, koinsidensiya matritsasi 1/(m−1) vazni bilan to'planadi (m — birlikdagi baholar soni); m < 2 bo'lgan birlik tashlanadi. Masofa — ordinal (Krippendorff 2004/2011): δ²(c,k) = (Σ_{g=c..k} n_g − (n_c + n_k)/2)², n_g — qiymatning chegaraviy chastotasi. α = 1 − (n−1)·D_o / D_e. Bo'sh kataklar (B: E159, E219; D: E019) «yo'q ma'lumot» sifatida chiqariladi (tuzatish 10 (g)); juftlangan baholarda bitta qiymat qolsa D_e = 0 va α aniqlanmaydi (nan). Bootstrap (Q13, 3-band) gap darajasida qayta tanlaydi: tanlangan gapning barcha 5 elementi birga olinadi (gap-klaster), shuning uchun bir gapning tizimlar orasidagi bog'liqligi saqlanadi.
