# Tuzatish 8 — etalon mustaqilligi tekshiruvi (ma'lumotdan oldin)
Sana: 2026-10-20. Tarjimon fayllari hali kelmagan (`qaytgan/` yo'q); tarqatish jurnalida berilgan sana bo'sh.

1. Tekshiruv — `etalon_tekshir.py` (muzlatiladi, bir marta; sha256 17ce8799d81f93436767dfdfde95219c570c37e57586ac84025c128ae3880cc1). Har tarjimon (T1, T2) uchun 72 gapda,
   har tizim (KKT, Gemini, Claude, GPT, GT) bilan:
   (a) normallashtirilgan aynan moslik ulushi (normallashtirish — ekspozitsiya_2_reja.md);
   (b) o'rtacha gap-chrF (chrF2; hyp = tarjimon, ref = tizim); eng yaqin va ikkinchi eng yaqin tizim orasidagi farq;
   (c) T1–T2 o'rtacha gap-chrF (tavsifiy).
   BAYROQ: (a) biror tizim bilan >= 25 % (18/72) YOKI (b) farq >= 12 ball. Natija — faqat sonlar va bayroq,
   `etalon/etalon_tekshir.json`.
2. Oqibat (oldindan belgilangan): bayroqli tarjimon etaloni ASOSIY tahlildan chiqariladi va sezgirlikda ko'rsatiladi;
   o'rniga yangi tarjimon jalb qilinadi (xuddi shu paket, xuddi shu tekshiruv). Ikkinchisi ham bayroqli bo'lsa — faqat
   mavjud etalon (FLORES/korpus) bilan, cheklov sifatida. Bayroq ayblov emas — maqolada neytral: «etalon
   mustaqilligi tekshiruvi». tahlil.py o'zgartirilmaydi (u qaytgan/T1.xlsx, T2.xlsx ni o'qiydi): bayroq chiqsa,
   bayroqli etalon bilan sezgirlik hisobi va «faqat mavjud etalon» varianti mexanizmi tahlil.py yurishidan OLDIN
   alohida sanali tuzatishda belgilanadi.
3. Tartib: qabul.py -> etalon_tekshir.py -> tahlil.py -> comet_qoshimcha.py. etalon_tekshir.py natija/ mavjud bo'lsa
   to'xtaydi.
4. Tarjimon YORIQNOMA.md ga «Taqiqlar» bo'limi boshiga bitta jumla qo'shildi: «Tarjima nazorat ostida, bir o'tirishda
   bajariladi.» Paket xlsx/docx o'zgarmagan (bayt-aynan); T1/T2 zip'lari qayta yasaldi (eski zip'lar
   ~/Downloads/TOLQIN2_tarqatish/eski/ da), tarqatish_jurnali.csv dagi T1/T2 zip_sha256 yangilandi; B–E o'zgarmagan.
5. Smoke-test (sintetik, scratchpad, repoga kirmagan): tizim nusxasi bo'lgan etalon BAYROQ = HA, mustaqil etalon
   BAYROQ = yo'q; run-once himoya ishladi.
