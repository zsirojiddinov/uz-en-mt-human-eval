# Tuzatish 13 — taqriz-asosli sezgirlik tahlillari, Q13 (NATIJADAN KEYINGI, EXPLORATORY)
Sana: 2026-11-06. Prereg §3 tuzatish qoidasi bo'yicha **«natijadan keyingi»** (natija/ — 93111a5). Asos: qo'lyozma v1.4 ga
ikki taqriz (Gemini 3 Pro — major revision; ChatGPT Think — reject), 2026-11-06. Barcha natija **exploratory**, tasdiqlovchi emas;
prereg gipotezalari va ularning muzlatilgan natijalari o'zgarmaydi. Hech narsa o'chirilmaydi.

## 1. Nima qilindi
Skript `qoshimcha/tuzatish13/t13.py` (bir marta; chiqish mavjud bo'lsa to'xtaydi). Muzlatilgan `tahlil.py` ga tegilmagan — undan
yuklash, metrika va α funksiyalari import qilingan. `natija/*` va `etalon/*` faqat o'qilgan; ularning sha256 qiymatlari MANIFEST
(Q2, 93111a5) bilan yurishdan oldin va keyin tekshirilgan (assert). Muhit `~/.venvs/tolqin2_comet`: sacreBLEU 2.6.0,
numpy 1.26.4, scipy 1.13.1, Python 3.9.6. Bootstrap seed 20261106, 10 000 qayta tanlash, gap darajasida.

Bandlar (natijalar — `qoshimcha/tuzatish13/Q13_natija.md`, `.json`):
1. T1 sezgirligi (T1 bor 71 gap): asl / asl+T1 / faqat T1; T1 ning tizim chiqishi bilan aynan gaplari; ularsiz qayta hisob;
   leave-one-sentence-out (asl+T1, 4 neyron tizim tartibi).
2. P1 ning beshta o'sishi uchun Bonferroni 99 % juftlashgan bootstrap oraliqlari (72 gap, prereg P1 ta'rifi).
3. BCa 95 % (scipy.stats.bootstrap): panel α (B, C, D; ASOSIY 71; mazmun, ravonlik) va to'rt tizim-ichi ρ.
4. Pooled neyron ρ (284 element, KKT siz) va η² (tizim, bir omilli).
5. Juftlik Spearman B–C, C–D, B–D — KKT ichida va neyron ichida (SEZGIRLIK 72).
6. α implementatsiyasi tavsifi.

## 2. Tekshiruvlar (assert)
- T1 aynan soni (tizim bo'yicha) = `etalon/etalon_tekshir.json`.
- 71 gapdagi asl+T1 korpus-BLEU leave-one-out yig'indisi bilan teng.
- P1 Δ (5 tizim) = `natija/tahlil_natija.json` B2.
- α (B, C, D) mazmun va ravonlik = H7 ASOSIY; tizim-ichi ρ = H4 ASOSIY; juftlik ρ (hammasi) = H6 SEZGIRLIK.
- Ikkinchi yurish birinchisi bilan bayt-aynan (`Q13_natija.json`, `.md`).

## 3. Og'ishlar va cheklovlar
- Bu tahlillar prereg'da yo'q va taqrizlardan keyin, natijalarni bilgan holda tanlangan — shuning uchun faqat exploratory.
- 1-band (d) va 1-band (c) T1 ning MT/LLM ishlatmaganini isbotlamaydi: T1 deklaratsiyasi imzosiz (tuzatish 9, 3-band) — cheklov
  o'z kuchida.
- 4-band persentil oraliq gap-klaster bootstrap bilan (BCa emas).
- Q13 topshirig'ida chiqishlar `qoshimcha/tuzatish13/` ga; ushbu hujjat oldingi tuzatishlar qatorida (`tuzatish_13.md`) saqlandi.

## 4. Fayllar (sha256)
| fayl | sha256 |
|---|---|
| qoshimcha/tuzatish13/t13.py | 5d46c5d160b002e05e29a1633bb038335021df7269a253194eef4cb8be81cd92 |
| qoshimcha/tuzatish13/Q13_natija.json | 264b682c8a672d4d9aaf16193cb7d50a38eef668c1ab6812376fb5c974a75b39 |
| qoshimcha/tuzatish13/Q13_natija.md | 0aeeccfb354ff11ff9aeb39fbb62b4b884ec1bcac0b364e9e70c4b4de2d392f9 |
| natija/tahlil_natija.json (o'zgarmagan) | 24ff6007c7b7b0addbbd325174116d4d40eb1a0bf6f3f6d1778a1af707ef23d0 |
| etalon/etalon_tekshir.json (o'zgarmagan) | a6c03c1188f6e90396193fabcd0fab75aad97c46328d8c317773de36dd31002b |
