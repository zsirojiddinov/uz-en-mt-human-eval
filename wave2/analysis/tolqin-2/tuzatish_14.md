# Tuzatish 14 — yozuv tuzatishlari va taqriz-asosli tahlillar, Q15 (NATIJADAN KEYINGI, EXPLORATORY)
Sana: 2026-11-07. Prereg §3 tuzatish qoidasi bo'yicha **«natijadan keyingi»** (natija/ — 93111a5). Asos: qo'lyozma v1.6 ga
2-davr taqrizlari (Gemini 3 Pro — major revision; ChatGPT — reject), 2026-11-06. Hech narsa o'chirilmaydi; prereg gipotezalari
va muzlatilgan natijalar o'zgarmaydi.

## 1. Yozuv tuzatishlari (Q14 — ombordan, faqat o'qish)
(a) **Claude chiqishlari qanday olingan.** Tuzatish 1: «Claude — alohida Claude Code sessiyalari, bo'sh papkada, faqat ko'rsatma va
kirish fayli; model identifikatori sessiya transkriptidan». `claude_yigish.sh` va `veb/jurnal.csv` (har `claude_NN.txt` qatorida
sessiya id, model `claude-opus-5-5`, transkript nomi) buni tasdiqlaydi. Tadqiqotchining 2026-11-06 dagi og'zaki eslashi
(«claude.ai veb») ombor yozuviga zid; ombor yozuvi amal qiladi.
(b) **Partiyalar.** Tuzatish 1: 472 gap (A-qavat 400 + eval72) seed 20261016 bilan aralashtirilgan; LLM'lar uchun 40 talik
12 to'plam (oxirgisi 32), Google Translate uchun 25 talik 19 to'plam (oxirgisi 22). `veb/kalit.json` bo'yicha har to'plamda A va
B qatlamlari (flores / train / gold) aralash — korpus tartibida ham, qatlam bo'yicha bir jinsli ham emas.
(c) **Ilmiy (train) qatlam etalonlari.** `evaluation/eval72/select_72.py`: train 24 gap `corpus/uz_en_scitech.train.json` dan;
`corpus/HARVEST_REPORT.md`: manba — inlibrary.uz (ochiq OJS platformasi, uch tilli annotatsiyalar, OAI-PMH). Inglizcha etalon —
maqolalarning nashr etilgan inglizcha annotatsiyasi, gap darajasida tekislangan. Manba ochiq — neyron tizimlar uchun ekspozitsiya
ehtimoli cheklov sifatida yoziladi.
(d) **etalon_tekshir «farq_1_2».** O'rtacha gap-chrF2 (hyp = T1, ref = tizim), 71 gap; eng yaqin GPT, ikkinchi **Gemini**
(farq 5,51). Qo'lyozmadagi «GPT va Google Translate» — noto'g'ri; T1-only korpus BLEU farqi (GPT − GT 9,15) boshqa kattalik.

## 2. Tahlillar (Q15)
Skript `qoshimcha/tuzatish14/t14.py`, test `qoshimcha/tuzatish14/test_alfa.py`; natijalar `Q15_natija.md`, `.json`.
Muhit `~/.venvs/tolqin2_comet` (sacreBLEU 2.6.0, numpy 1.26.4, scipy 1.13.1); seed 20261106, 10 000.
1. 71 gapda juftlashgan o'sishlar (asl+T1 − asl), 95 % juftlashgan bootstrap.
2. Kendall W — har tizim ichida B, C, D tartibi (mazmun, ravonlik), gap bootstrap 95 %.
3. α implementatsiyasi tekshiruvi — Krippendorff (2011) nashr etilgan namunasi (ordinal α = 0,815) va sintetik holatlar.
4. etalon_tekshir mezonining qayta hisobi (1(d)).
5. Ilmiy qatlamda tizim chiqishlarining etalon bilan aynan / deyarli mosligi.

## 3. Tekshiruvlar (assert)
natija/ va etalon/ sha256 — yurishdan oldin va keyin; 1-band nuqtaviy qiymatlari = Q13 1a; 4-band chrF qiymatlari va farq_1_2 =
`etalon/etalon_tekshir.json`; α testlari o'tdi. Ikki yurish bayt-aynan.

## 4. Og'ishlar va bajarilmagan
- Barcha tahlillar prereg'da yo'q, taqrizdan keyin tanlangan — exploratory.
- Q15 3-bandidagi krippendorff PyPI paketi bilan solishtirish **bajarilmadi**: paketni o'rnatish shu sessiyada ruxsat etilmadi.
  O'rniga nashr etilgan namuna bilan tekshirildi (aynan 0,815).

## 5. Fayllar (sha256)
| fayl | sha256 |
|---|---|
| qoshimcha/tuzatish14/t14.py | d600719a1ffd6ed3b298ea65cb4bc2a7fe92e5a4a76508a20045be49d3f602e6 |
| qoshimcha/tuzatish14/test_alfa.py | 697b28f587f8ef0a1b464e4b6056c33012f7a6cc0947aedf1a286e892390c4cb |
| qoshimcha/tuzatish14/Q15_natija.json | a83a04ce181bed2ee0c273f27fbaeba706e7363daed8ab66df6f0757dc89b2a2 |
| qoshimcha/tuzatish14/Q15_natija.md | f2b3774097b922332e3a948aa28c63071556d1e19ef1e00b323f8a605edfd647 |
