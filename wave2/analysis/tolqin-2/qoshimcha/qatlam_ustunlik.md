# TOLQIN-2 — B-qavat tizim × qatlam, Claude ustunligi (qatlam_ustunlik.py)

**natijadan keyingi, eksplorativ, prereg'da yo'q; tadqiqotchi so'rovi 2026-10-28; B1 jadvali tahlil_natija.json dan, ustunlik va CI yangi hisob; sabab ajratilmaydi**. Tasdiqlovchi emas.
Qatlamlar: flores 36 · train (ilmiy) 24 · gold (oddiy) 12, beqaror · train+gold 36. asl+T1: № 55 da faqat asl etalon.
Bootstrap: seed 20261028; BLEU 1000, chrF2 300 tanlov; qatlam ichida gap bo'yicha; persentil 95 % CI.

## B1 — korpus-BLEU / chrF2 (natija/tahlil_natija.json dan)

| qatlam | etalon | KKT | Gemini | Claude | GPT | GT |
|---|---|---|---|---|---|---|
| flores | 1ref | 1.60 / 39.65 | 40.37 / 65.87 | 61.73 / 79.86 | 37.19 / 65.02 | 41.49 / 67.20 |
| flores | asl+T1 | 2.62 / 41.31 | 57.31 / 70.64 | 72.10 / 81.57 | 62.26 / 74.45 | 56.69 / 71.08 |
| train | 1ref | 6.77 / 50.56 | 51.28 / 75.27 | 47.40 / 74.13 | 47.58 / 73.49 | 59.50 / 78.96 |
| train | asl+T1 | 7.35 / 51.06 | 58.70 / 77.97 | 56.70 / 76.74 | 64.39 / 79.20 | 70.27 / 82.38 |
| gold | 1ref | 50.07 / 80.90 | 52.28 / 83.90 | 66.49 / 87.72 | 48.22 / 82.99 | 60.11 / 79.09 |
| gold | asl+T1 | 59.70 / 81.44 | 69.33 / 89.49 | 78.40 / 91.07 | 72.81 / 88.14 | 66.06 / 83.68 |
| train+gold | 1ref | 12.00 / 53.80 | 51.45 / 76.21 | 49.15 / 75.60 | 48.25 / 74.52 | 59.55 / 78.97 |
| train+gold | asl+T1 | 13.63 / 54.30 | 59.74 / 79.20 | 58.76 / 78.26 | 65.24 / 80.18 | 69.99 / 82.52 |

## Claude ustunligi (o'rtachaga / eng yaxshiga qarshi; Gemini, GPT, GT)

| o'lchov | flores | train | gold | train+gold | flores − train | 95 % CI | tanlov |
|---|---|---|---|---|---|---|---|
| 1ref bleu | 22.05 / 20.24 | -5.39 / -12.10 | 12.95 / 6.38 | -3.94 / -10.41 | 27.43 / 32.34 | [20.02; 34.36] / [22.96; 41.19] | 1000 |
| 1ref chrf2 | 13.83 / 12.66 | -1.78 / -4.83 | 5.73 / 3.82 | -0.97 / -3.37 | 15.61 / 17.49 | [11.72; 19.66] / [12.33; 22.23] | 300 |
| asl+T1 bleu | 13.35 / 9.84 | -7.76 / -13.57 | 9.00 / 5.59 | -6.23 / -11.23 | 21.10 / 23.41 | [13.48; 27.44] / [14.15; 33.45] | 1000 |
| asl+T1 chrf2 | 9.51 / 7.12 | -3.11 / -5.65 | 3.97 / 1.58 | -2.37 / -4.26 | 12.62 / 12.77 | [7.96; 16.77] / [6.93; 18.57] | 300 |

Sabab ajratilmaydi: qatlamlar janr va qiyinlik bo'yicha ham farq qiladi. 1 etalonli FLORES qatlamida etalon — FLORES asl
ingliz matni (yodlash ehtimoliga eng sezgir). asl+T1 da GPT FLORES BLEU 37,19 -> 62,26 (boshqalardan ancha katta o'sish).
