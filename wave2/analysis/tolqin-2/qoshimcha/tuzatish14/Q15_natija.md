# TOLQIN-2 — Q15 natijalari (t14.py)

**natijadan keyingi, taqriz-asosli (2-davr taqrizlari, 2026-11-06); EXPLORATORY; natija/ va etalon/ o'zgarmagan**.

Muhit: sacreBLEU 2.6.0, numpy 1.26.4, scipy 1.13.1, Python 3.9.6. Seed 20261106, 10000 qayta tanlash.

## 1. T1 bor 71 gap: juftlashgan o'sish (asl+T1 − asl)

95 % persentil, juftlashgan gap bootstrap; nuqtaviy qiymat = Q13 1a (assert).

| tizim | asl | asl+T1 | Δ | 95 % |
|---|---|---|---|---|
| KKT | 6.55 | 7.95 | 1.40 | [0.82; 2.09] |
| Gemini | 44.14 | 57.76 | 13.62 | [10.33; 17.23] |
| Claude | 56.64 | 67.18 | 10.54 | [7.51; 13.73] |
| GPT | 40.94 | 63.26 | 22.31 | [18.02; 26.60] |
| GT | 47.99 | 61.44 | 13.45 | [10.13; 16.72] |

## 2. Kendall W (B, C, D; tizim ichida)

B, C, D; ASOSIY 71; har tizim ichida gap tartibi; o'rtacha rang, bog'lanish tuzatishi; gap bootstrap 95 %.

| tizim | o'lchov | n | W | 95 % | chiqarilgan (yo'q katak) |
|---|---|---|---|---|---|
| KKT | mazmun | 71 | 0.681 | [0.580; 0.764] | 0 |
| KKT | ravonlik | 71 | 0.572 | [0.471; 0.651] | 0 |
| Gemini | mazmun | 70 | 0.507 | [0.425; 0.586] | 1 |
| Gemini | ravonlik | 70 | 0.415 | [0.337; 0.486] | 1 |
| Claude | mazmun | 70 | 0.525 | [0.425; 0.615] | 1 |
| Claude | ravonlik | 70 | 0.443 | [0.353; 0.524] | 1 |
| GPT | mazmun | 71 | 0.409 | [0.318; 0.496] | 0 |
| GPT | ravonlik | 71 | 0.406 | [0.326; 0.478] | 0 |
| GT | mazmun | 71 | 0.463 | [0.367; 0.552] | 0 |
| GT | ravonlik | 70 | 0.369 | [0.280; 0.455] | 1 |

## 3. α implementatsiyasi tekshiruvi

| holat | kutilgan | hisoblangan | o'tdi |
|---|---|---|---|
| K2011 ordinal (4×12, yo'q qiymatlar) | 0,815 | 0.815 | ha |
| to'liq kelishuv, 3 baholovchi | 1 | 1.000 | ha |
| to'liq kelishuv, 2 baholovchi + bo'sh katak | 1 | 1.000 | ha |
| juftlangan baholarda bitta qiymat | nan | nan | ha |
| m < 2 birlik tashlanadi | 0.842912 | 0.843 | ha |

## 4. etalon_tekshir «farq_1_2» mezoni

Metrika: o'rtacha gap-chrF2 (sacreBLEU CHRF sukut: char_order 6, word_order 0, beta 2), 71 gap. Yo'nalish: hyp = T1 tarjimasi, ref = tizim chiqishi (etalon_tekshir.py: chrf.sentence_score(T[x][i], [ch[t][i]])). Signatura: `nrefs:1|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0`.

| tizim | o'rtacha gap-chrF2 (hyp T1) | T1-only korpus BLEU (hyp tizim) |
|---|---|---|
| KKT | 43.05 | 4.21 |
| Gemini | 67.70 | 37.13 |
| Claude | 66.31 | 36.12 |
| GPT | 73.21 | 46.46 |
| GT | 66.86 | 37.32 |

Eng yaqin: GPT; ikkinchi: Gemini; farq_1_2 = 5.51 (etalon_tekshir: 5.51). T1-only BLEU: GPT − GT = 9.15; GPT − Gemini = 9.33. ikki kattalik turli: (i) o'rtacha gap-chrF, hyp = T1; (ii) korpus BLEU, hyp = tizim, ref = T1. chrF bo'yicha ikkinchi eng yaqin tizim — Gemini (GT emas).

## 5. Ilmiy qatlam (train, 24 gap) — etalon bilan moslik

Etalon: ref_en (inlibrary.uz nashr etilgan inglizcha annotatsiya, gap darajasida). Mezon: aynan: norm_tok bo'yicha teng; deyarli: aynan YOKI (gap-chrF2 >= 95 VA gap-BLEU exp >= 90).

| tizim | aynan (norm) | deyarli (jami) | aynan (xom) |
|---|---|---|---|
| KKT | 0 | 0 | 0 |
| Gemini | 1 | 1 | 1 |
| Claude | 3 | 3 | 3 |
| GPT | 3 | 3 | 3 |
| GT | 3 | 3 | 3 |

## 6. Bajarilmagan

3-band: krippendorff PyPI paketi bilan solishtirish bajarilmadi — paketni o'rnatish sessiyada ruxsat etilmadi (2026-11-07). O'rniga Krippendorff (2011) nashr etilgan namunasi (ordinal α = 0,815) va sintetik holatlar bilan tekshirildi.
