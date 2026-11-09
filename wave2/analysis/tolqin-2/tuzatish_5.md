# Tuzatish 5 (tahlil skripti va tarjimon paketlaridan oldin; tarjimon/baholovchi ma'lumoti hali yo'q)
Sana: 2026-10-20. Prereg sukut saqlagan yoki ikki xil o'qiladigan joylar — foydalanuvchi qarori bilan.

1. Tarjimon to'plami (prereg §2.4): eval72 ning 72 gapi; tartib prereg'da yo'q — `random.Random(20261016).shuffle`
   (`evaluation/eval72/sentences.json` fayl tartibidan), ikkala tarjimonga (T1, T2) bir xil. Kalit
   `paket/kalit_tarjimon.json` (№ -> qavat, ID), paketga kirmaydi.
2. «Korrelyatsiya … qatlam bo'yicha» (prereg §4): ikkala ajratma, tanlanmaydi — asosiy tavsifiy: eval72 `layer`
   (flores 36 / train 24 / gold 12); qo'shimcha tavsifiy: tuzatish 4 (B-KKT = train+gold 36, B-FLORES = flores 36).
   Noyob gap < 20 bo'lgan qatlam (gold, n = 12) CI bilan va «beqaror» belgisi bilan beriladi.
3. Kelishuv (prereg §1 P3, §4): faqat juftlik Spearman va Krippendorff α (ordinal). κ va AC1 kiritilmaydi.
4. A-qavat KKT ekspozitsiyasi (prereg §2.2, §4: «78 so'z bo'yicha gap-ma-gap belgi»): `a_qavat_400.json` dagi
   ikkala belgi — «aynan» (29 gap) va «prefiks» (75 gap) — ikkalasi ko'rsatiladi.
5. Ketma-ketlik (prereg §3): (5) tahlil skripti (4) paketlardan OLDIN commit qilinadi; ikkalasi tarqatishdan oldin.
6. Skript tafsilotlari (prereg matnini to'ldiradi): S3 va past ball rejimidagi BLEU = gap-BLEU_1ref
   (sentence_bleu, smooth exp); past ball rejimi = gap-BLEU_1ref < 10. P1 (Δ), S4 (R1 − R2) va eksplorativ farq
   uchun ham bootstrap 1000 CI beriladi (qo'shimcha, tavsifiy). Darvoza (c)–(e) bilan belgilangan fayl tahlilda
   qoladi; prereg §4 istisnosi bo'yicha chiqarilgani `qaytgan/chiqarilgan.json` da qayd etiladi; (a) yoki (b) dan
   o'tmagan fayl hisoblanmaydi. LLM-hakam: har (model, tartib) va har o'lchov (adequacy, fluency) uchun inson
   o'rtachasiga qarshi Spearman, tizim bo'yicha va umumiy. Kirish formatlari `tahlil.py` boshida.
