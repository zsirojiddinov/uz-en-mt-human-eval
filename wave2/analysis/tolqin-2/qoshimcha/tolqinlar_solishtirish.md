# TOLQIN-2 — ikki to'lqinni solishtirish (tolqinlar_solishtirish.py)

**natijadan keyingi, qo'shimcha, prereg'da yo'q; tadqiqotchi so'rovi 2026-10-28**. Tasdiqlovchi emas.
iyul va oktyabr baholovchilari BOSHQA odamlar (tadqiqotchi, 2026-10-28); harflar «iyul X» / «okt X». Oktyabr: 72 gap (360 element); iyul: 216 item. Bootstrap yo'q.
Iyul tizimlari: s1 {'system': 'kkt_sentence_translator_v2', 'commit': 'e099ff4'}, gemini {'system': 'gemini', 'model': 'gemini-2.5-flash', 'temperature': 0.0, 'prompt': 'neutral: Translate ... Output ONLY the translation'}.

## 1. MT metrikalari (1 etalon ref_en; korpus-BLEU / chrF2 / gap-BLEU o'rtachasi)

| qatlam | n | iyul s1 (KKT) | okt KKT | iyul gemini | okt Gemini | KKT aynan (s1 = okt) |
|---|---|---|---|---|---|---|
| hammasi | 72 | 5.87 / 43.42 / 13.26 | 6.52 / 45.99 / 13.94 | 38.99 / 68.38 / 40.99 | 44.98 / 70.57 / 42.42 | 11/72 |
| flores | 36 | 1.18 / 36.51 / 3.91 | 1.60 / 39.65 / 4.92 | 34.30 / 62.72 / 29.47 | 40.37 / 65.87 / 34.14 | 0/36 |
| train | 24 | 6.43 / 48.54 / 8.48 | 6.77 / 50.56 / 9.02 | 43.12 / 73.37 / 44.59 | 51.28 / 75.27 / 49.85 | 0/24 |
| gold | 12 | 50.07 / 80.36 / 50.85 | 50.07 / 80.90 / 50.85 | 65.83 / 89.91 / 68.33 | 52.28 / 83.90 / 52.37 | 11/12 |

KKT aynan ustuni faqat tizim shu 72 gapda qancha o'zgarganini ko'rsatadi (s2 = okt: 11/72).

## 2. Baholovchi × tizim o'rtachasi (mazmun / ravonlik)

| baholovchi | tizim | mazmun | ravonlik |
|---|---|---|---|
| iyul B | s1 | 3.60 | 3.68 |
| iyul B | s2 | 3.56 | 3.58 |
| iyul B | gemini | 4.12 | 4.15 |
| iyul C | s1 | 2.42 | 1.64 |
| iyul C | s2 | 2.42 | 1.64 |
| iyul C | gemini | 4.99 | 5.00 |
| okt B | KKT | 1.85 | 1.72 |
| okt B | Gemini | 4.08 | 3.93 |
| okt C | KKT | 4.08 | 3.93 |
| okt C | Gemini | 4.32 | 4.19 |
| okt D | KKT | 4.44 | 4.69 |
| okt D | Gemini | 4.82 | 4.97 |
| okt E | KKT | 2.50 | 1.76 |
| okt E | Gemini | 4.92 | 4.90 |

### Ball tarqalishi (iyul 216, oktyabr 360 — fayl bo'yicha)

| baholovchi | o'lchov | 1 | 2 | 3 | 4 | 5 | yo'q | o'rtacha | SD |
|---|---|---|---|---|---|---|---|---|---|
| iyul B | mazmun | 0 | 10 | 77 | 84 | 45 | 0 | 3.76 | 0.83 |
| iyul B | ravonlik | 0 | 6 | 70 | 100 | 40 | 0 | 3.81 | 0.76 |
| iyul C | mazmun | 44 | 44 | 26 | 13 | 89 | 0 | 3.27 | 1.63 |
| iyul C | ravonlik | 110 | 12 | 2 | 4 | 88 | 0 | 2.76 | 1.92 |
| okt B | mazmun | 61 | 17 | 67 | 109 | 104 | 2 | 3.50 | 1.40 |
| okt B | ravonlik | 66 | 25 | 68 | 96 | 103 | 2 | 3.41 | 1.44 |
| okt C | mazmun | 4 | 4 | 0 | 238 | 114 | 0 | 4.26 | 0.63 |
| okt C | ravonlik | 4 | 5 | 4 | 273 | 74 | 0 | 4.13 | 0.60 |
| okt D | mazmun | 0 | 1 | 10 | 67 | 282 | 0 | 4.75 | 0.51 |
| okt D | ravonlik | 0 | 0 | 6 | 19 | 334 | 1 | 4.91 | 0.34 |
| okt E | mazmun | 12 | 37 | 16 | 32 | 263 | 0 | 4.38 | 1.16 |
| okt E | ravonlik | 46 | 14 | 5 | 29 | 266 | 0 | 4.26 | 1.41 |

## 3. Kelishuv (juftlik Spearman ρ · juftlik α ordinal; guruh α; SD — har baholovchi, shu qism-to'plamda)

### iyul

| qism-to'plam | n | o'lchov | iyul B–iyul C | guruh α | SD |
|---|---|---|---|---|---|
| hammasi | 216 | mazmun | 0.530 · 0.451 | — | B 0.83, C 1.63 |
| hammasi | 216 | ravonlik | 0.487 · 0.317 | — | B 0.76, C 1.92 |
| KKT (s1+s2) | 144 | mazmun | 0.529 · 0.177 | — | B 0.81, C 1.33 |
| KKT (s1+s2) | 144 | ravonlik | 0.512 · -0.215 | — | B 0.73, C 1.33 |
| gemini | 72 | mazmun | 0.031 · -0.439 | — | B 0.74, C 0.12 |
| gemini | 72 | ravonlik | nan · -0.474 | — | B 0.70, C 0.00 |

### okt B,C,D

| qism-to'plam | n | o'lchov | okt B–okt C | okt B–okt D | okt C–okt D | guruh α | SD |
|---|---|---|---|---|---|---|---|
| hammasi | 360 | mazmun | 0.322 · 0.209 | 0.357 · -0.069 | 0.338 · 0.057 | 0.122 | B 1.40, C 0.63, D 0.51 |
| hammasi | 360 | ravonlik | 0.294 · 0.187 | 0.254 · -0.341 | 0.188 · -0.437 | -0.071 | B 1.44, C 0.60, D 0.34 |
| KKT | 72 | mazmun | 0.651 · -0.108 | 0.373 · -0.365 | 0.576 · 0.514 | 0.062 | B 1.36, C 0.95, D 0.62 |
| KKT | 72 | ravonlik | 0.588 · -0.207 | 0.192 · -0.614 | 0.322 · -0.077 | -0.141 | B 1.23, C 0.92, D 0.62 |
| neyron | 288 | mazmun | 0.262 · 0.219 | 0.181 · -0.157 | 0.249 · -0.101 | 0.053 | B 1.06, C 0.50, D 0.45 |
| neyron | 288 | ravonlik | 0.216 · 0.179 | 0.071 · -0.401 | 0.080 · -0.565 | -0.126 | B 1.14, C 0.47, D 0.17 |
| Gemini | 72 | mazmun | 0.325 · 0.294 | 0.191 · -0.008 | 0.306 · -0.030 | 0.129 | B 0.99, C 0.47, D 0.42 |
| Gemini | 72 | ravonlik | 0.231 · 0.199 | 0.096 · -0.322 | 0.079 · -0.567 | -0.097 | B 1.10, C 0.43, D 0.16 |

### okt B,C,D,E

| qism-to'plam | n | o'lchov | okt B–okt C | okt B–okt D | okt B–okt E | okt C–okt D | okt C–okt E | okt D–okt E | guruh α | SD |
|---|---|---|---|---|---|---|---|---|---|---|
| hammasi | 360 | mazmun | 0.322 · 0.209 | 0.357 · -0.069 | 0.564 · 0.305 | 0.338 · 0.057 | 0.193 · 0.088 | 0.388 · 0.358 | 0.207 | B 1.40, C 0.63, D 0.51, E 1.16 |
| hammasi | 360 | ravonlik | 0.294 · 0.187 | 0.254 · -0.341 | 0.579 · 0.321 | 0.188 · -0.437 | 0.221 · 0.026 | 0.310 · 0.152 | 0.090 | B 1.44, C 0.60, D 0.34, E 1.41 |
| KKT | 72 | mazmun | 0.651 · -0.108 | 0.373 · -0.365 | 0.644 · 0.376 | 0.576 · 0.514 | 0.588 · 0.072 | 0.508 · -0.197 | 0.151 | B 1.36, C 0.95, D 0.62, E 1.22 |
| KKT | 72 | ravonlik | 0.588 · -0.207 | 0.192 · -0.614 | 0.633 · 0.634 | 0.322 · -0.077 | 0.653 · -0.085 | 0.388 · -0.518 | 0.011 | B 1.23, C 0.92, D 0.62, E 1.29 |
| neyron | 288 | mazmun | 0.262 · 0.219 | 0.181 · -0.157 | 0.183 · -0.203 | 0.249 · -0.101 | 0.091 · -0.248 | 0.124 · 0.122 | 0.032 | B 1.06, C 0.50, D 0.45, E 0.44 |
| neyron | 288 | ravonlik | 0.216 · 0.179 | 0.071 · -0.401 | 0.175 · -0.255 | 0.080 · -0.565 | 0.091 · -0.420 | 0.008 · -0.010 | -0.086 | B 1.14, C 0.47, D 0.17, E 0.35 |
| Gemini | 72 | mazmun | 0.325 · 0.294 | 0.191 · -0.008 | 0.300 · -0.158 | 0.306 · -0.030 | 0.187 · -0.276 | 0.173 · 0.147 | 0.084 | B 0.99, C 0.47, D 0.42, E 0.32 |
| Gemini | 72 | ravonlik | 0.231 · 0.199 | 0.096 · -0.322 | 0.213 · -0.172 | 0.079 · -0.567 | 0.153 · -0.400 | -0.055 · -0.059 | -0.059 | B 1.10, C 0.43, D 0.16, E 0.30 |

## 4. Baholovchilar (ombordagi yozuvlardan, ismsiz)

| baholovchi | daraja | kasb | tarqatish | qaytish |
|---|---|---|---|---|
| iyul B | qayd yo'q | qayd yo'q | qayd yo'q (rater_B.xlsx yaratilgan 2026-07-02, b37a4da) | qayd yo'q (returns/rater_B_filled.xlsx: docProps modified 2026-07-09T13:15:54Z; omborga 2026-07-14, 0ab3ee2) |
| iyul C | qayd yo'q | qayd yo'q | qayd yo'q (rater_C.xlsx yaratilgan 2026-07-02, b37a4da) | 2026-07-06 qabul (rw1_prereg_analysis_plan.md, 2026-07-07 tuzatishi); docProps modified 2026-07-04T16:41:34Z; omborga 2026-07-07, d54be48 |
| okt B | qayd yo'q | qayd yo'q | 2026-10-21 | kelgan fayl mtime 2026-10-26T17:17:28+05:00; qabul 2026-10-26T19:42 (qabul_jurnal.csv) |
| okt C | qayd yo'q | qayd yo'q | 2026-10-20..21 (aniq kun qayd etilmagan) | kelgan fayl mtime 2026-10-21T17:37:58+05:00; qabul 2026-10-26T19:42 |
| okt D | qayd yo'q | qayd yo'q | 2026-10-21 | kelgan fayl mtime 2026-10-26T19:18:20+05:00; qabul 2026-10-26T19:42 |
| okt E | qayd yo'q | qayd yo'q | 2026-10-20..21 (aniq kun qayd etilmagan) | kelgan fayl mtime 2026-10-22T14:12:04+05:00; qabul.py RAD 2026-10-26T19:42 (chiqarilgan, tuzatish 9/10 (d)) |

- Ombordagi yagona daraja yozuvi: iyul A-rol o'rnini bosgan baholovchi — «ingliz tili o'qituvchisi, IELTS 7.0», QISMAN 127/216, asosiy tahlilga kirmagan (rw1_prereg_analysis_plan.md, 2026-07-11 tuzatishi; rw1_report.md).
- «7.5 / 7.0» yozilgan README omborda (asosiy va kkt_tolqin2, git tarixi bilan) topilmadi.
- prereg §2.5: «4 to'liq (B, C — 1-to'lqindan; D, E — yangi; kamida biri ingliz tili o'qituvchisi; IELTS ≥ 7,0)» — bu talab, yozuv emas; tadqiqotchi 2026-10-28: iyul va oktyabr baholovchilari boshqa odamlar — prereg matni bilan mos emas, bu yerda tuzatilmaydi.
