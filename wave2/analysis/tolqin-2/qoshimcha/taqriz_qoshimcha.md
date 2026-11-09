# TOLQIN-2 — taqriz uchun qo'shimcha (taqriz_qoshimcha.py)

**natijadan keyingi, taqrizga javob, 2026-10-29; tasdiqlovchi emas**.

## 1. Faqat T1 ga nisbatan (71 gap; bo'sh: train-21)

| tizim | BLEU | chrF2 | aynan (xom) | aynan (norm) |
|---|---|---|---|---|
| KKT | 4.21 | 42.48 | 1 | 1 |
| Gemini | 37.13 | 64.31 | 4 | 4 |
| Claude | 36.12 | 63.67 | 1 | 3 |
| GPT | 46.46 | 71.29 | 6 | 6 |
| GT | 37.32 | 65.02 | 2 | 3 |

Eng yaqin ikki: BLEU — GPT, GT; chrF2 — GPT, GT.

## 2. FLORES etaloniga moslik

aynan: norm_tok bo'yicha teng; deyarli: aynan YOKI (gap-chrF2 >= 95 VA gap-BLEU exp >= 90)

| tizim | A (400): aynan | A: deyarli (jami) | B-FLORES (36): aynan | B-FLORES: deyarli (jami) |
|---|---|---|---|---|
| KKT | 0 | 0 | 0 | 0 |
| Gemini | 4 | 4 | 0 | 0 |
| Claude | 27 | 32 | 2 | 2 |
| GPT | 7 | 7 | 0 | 0 |
| GT | 7 | 7 | 0 | 0 |

## 3. Tizim ichida ρ(gap-BLEU_1ref, adequacy) — H4 ASOSIY 71

| tizim | n | ρ | 95 % CI |
|---|---|---|---|
| KKT | 71 | 0.546 | [0.327; 0.714] |
| Gemini | 71 | 0.116 | [-0.127; 0.359] |
| Claude | 71 | -0.109 | [-0.358; 0.143] |
| GPT | 71 | -0.007 | [-0.250; 0.274] |
| GT | 71 | -0.063 | [-0.298; 0.198] |

## 4. Krippendorff α (ordinal), ASOSIY 71 — mazmun / ravonlik

| baholovchilar | qism | hammasi | flores | train | gold |
|---|---|---|---|---|---|
| B,C,D | hammasi | 0.115 / -0.079 | 0.089 / -0.151 | 0.028 / -0.145 | -0.154 / -0.221 |
| B,C,D | KKT | 0.052 / -0.151 | -0.202 / -0.350 | 0.001 / -0.320 | -0.226 / -0.226 |
| B,C,D | neyron | 0.045 / -0.136 | 0.013 / -0.209 | -0.043 / -0.192 | -0.125 / -0.211 |
| B,C,D,E | hammasi | 0.203 / 0.085 | 0.194 / 0.047 | 0.139 / 0.059 | 0.000 / -0.088 |
| B,C,D,E | KKT | 0.142 / -0.005 | -0.152 / -0.235 | 0.062 / -0.203 | 0.011 / -0.022 |
| B,C,D,E | neyron | 0.026 / -0.092 | -0.004 / -0.158 | -0.044 / -0.112 | -0.019 / -0.130 |
| C,D (B siz) | hammasi | 0.047 / -0.452 | -0.140 / -0.712 | -0.045 / -0.626 | 0.000 / nan |
| C,D (B siz) | KKT | 0.505 / -0.090 | 0.333 / -0.340 | 0.395 / -0.260 | nan / nan |
| C,D (B siz) | neyron | -0.112 / -0.580 | -0.315 / -0.832 | -0.192 / -0.787 | 0.000 / nan |
| B,D (C siz) | hammasi | -0.073 / -0.345 | 0.028 / -0.309 | -0.278 / -0.421 | -0.218 / -0.368 |
| B,D (C siz) | KKT | -0.377 / -0.621 | -0.697 / -0.810 | -0.458 / -0.742 | -0.382 / -0.382 |
| B,D (C siz) | neyron | -0.163 / -0.406 | -0.054 / -0.356 | -0.387 / -0.506 | -0.159 / -0.350 |
| B,C (D siz) | hammasi | 0.198 / 0.171 | 0.161 / 0.100 | 0.161 / 0.098 | -0.321 / -0.368 |
| B,C (D siz) | KKT | -0.123 / -0.232 | -0.546 / -0.682 | -0.150 / -0.623 | -0.382 / -0.382 |
| B,C (D siz) | neyron | 0.205 / 0.162 | 0.192 / 0.086 | 0.163 / 0.165 | -0.292 / -0.350 |
| B,E | hammasi | 0.303 / 0.322 | 0.386 / 0.365 | 0.243 / 0.361 | 0.067 / -0.044 |
| B,E | KKT | 0.351 / 0.613 | -0.126 / -0.023 | 0.099 / 0.465 | 0.386 / 0.402 |
| B,E | neyron | -0.208 / -0.261 | -0.158 / -0.301 | -0.345 / -0.251 | -0.101 / -0.245 |
| C,E | hammasi | 0.083 / 0.015 | -0.046 / -0.165 | 0.021 / -0.046 | -0.048 / -0.058 |
| C,E | KKT | 0.062 / -0.133 | -0.480 / -0.692 | -0.053 / -0.626 | -0.165 / -0.231 |
| C,E | neyron | -0.259 / -0.435 | -0.441 / -0.734 | -0.363 / -0.539 | -0.012 / -0.012 |
| D,E | hammasi | 0.359 / 0.150 | 0.354 / 0.178 | 0.320 / 0.113 | 0.246 / -0.058 |
| D,E | KKT | -0.205 / -0.543 | -0.647 / -0.765 | -0.377 / -0.737 | -0.165 / -0.231 |
| D,E | neyron | 0.121 / -0.011 | 0.069 / 0.035 | 0.101 / -0.080 | 0.651 / -0.012 |

Element soni (hammasi / KKT / neyron × hammasi, flores, train, gold): hammasi: 355, 180, 120, 55; KKT: 71, 36, 24, 11; neyron: 284, 144, 96, 44.
nan kataklar: C,D (B siz) · hammasi · gold · ravonlik: qiymatlar [5]; C,D (B siz) · KKT · gold · mazmun: qiymatlar [5]; C,D (B siz) · KKT · gold · ravonlik: qiymatlar [5]; C,D (B siz) · neyron · gold · ravonlik: qiymatlar [5]. α aniqlanmaydi: juftlangan baholarda bitta qiymat — kutilgan nomuvofiqlik De = 0 (0/0); katak bo'sh emas, ta'rif bo'yicha hisoblanmaydi.

## 5. Har baholovchining o'z ≥ 4,5 (= 5) to'plami — mazmun, ASOSIY 71

| baholovchi | n | BLEU (1 etalon) | chrF2 | KKT | Gemini | Claude | GPT | GT |
|---|---|---|---|---|---|---|---|---|
| B | 101 | 47.88 | 72.62 | 6 | 30 | 23 | 20 | 22 |
| C | 109 | 40.43 | 70.54 | 21 | 22 | 22 | 22 | 22 |
| D | 277 | 43.11 | 70.01 | 36 | 59 | 59 | 61 | 62 |
| E | 259 | 48.80 | 73.09 | 8 | 66 | 65 | 64 | 56 |

## 6. Faktlar

(a) 55-gap (train-21): r3 da None (T1 etaloni yo'q). _cache_references: «lines = [x for x in refs if x is not None]» — None tashlanadi; shu gap 1 etalon (asl) bilan; bo'sh satr ham, asl takrori ham EMAS. Tekshiruv (None bilan = 1 etalon statistikasi): True. Haqiqiy signatura: `nrefs:var|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0`, `nrefs:var|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0`. comet_qoshimcha.py: T1 etaloni yo'q gap T1 ballidan tashlanadi (T1_n = 71).
(b) sacrebleu.sentence_bleu(h, refs, smooth_method='exp') — smooth_value None, use_effective_order True (sacreBLEU 2.6.0 sukutlari); korpus-BLEU ham smooth:exp (signatura).
(c) prereg §2.5 (c): «ketma-ket bir xil (adequacy, fluency) juftligi qatori ≥ 12 bo'lsa belgilanadi»; tahlil.darvoza: c_belgi = eng >= 12 — 12 ning o'zi belgilanadi (13 dan emas).
(d) etalon_tekshir T1 aynan soni: {'Claude': 3, 'GPT': 6, 'GT': 3, 'Gemini': 4, 'KKT': 1} — 6 ta GPT niki.
(e) ombordan topilmadi (asosiy ombordagi tahlil va baholash papkalari, git tarixi, Desktop hujjatlari) — manba kerak.
