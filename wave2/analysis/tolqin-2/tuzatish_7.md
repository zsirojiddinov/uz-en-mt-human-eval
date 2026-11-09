# Tuzatish 7 — gold-00 (ma'lumotdan va tarqatishdan oldin)
Sana: 2026-10-20. Tarjimon va baholovchi paketlari hali tarqatilmagan; hech qanday baho/tarjima fayli kelmagan.

Sabab: baholovchi yo'riqnomasi (prereg §2.5; 1-to'lqin matni, sha256 e3c4c800024faf9d5bcd3274922117a4c68cc63df5587b06a5cf1374af216c56,
`rater_A.xlsx` «Yo'riqnoma» A21–A22) misolidagi o'zbekcha gap eval72 ning **gold-00** gapi bilan aynan; misolda shu gapning
ikki inglizcha tarjimasi Mazmun/Ravonlik ballari bilan ko'rsatilgan.

1. Yo'riqnoma matni O'ZGARMAYDI (prereg §2.5). gold-00 paketlarda qoladi (72 gap, 360 element) — 1-to'lqin bilan
   taqqoslanuvchanlik va §2.5 darvozalari uchun.
2. Mexanik tekshiruv (matnsiz, 2026-10-20): gold-00 uchun 5 tizim chiqishidan **3 tasi** yo'riqnomadagi ikki namunaviy
   tarjimadan biriga normallashtirilgan holda aynan teng (chrF ≥ 90 bo'yicha ham 3; normallashtirish —
   ekspozitsiya_2_reja.md).
3. tahlil.py — birinchi va yagona sanali o'zgarish (2026-10-20):
   - eski sha256 d867e101063325483e26da641abb9e9ae9eec6d22454c6d9cbac99d840e3b718 (1d29166);
   - yangi sha256 56522a2b0aed1261feb9a6138351f07c1db8f80213a1a08430b2e58f36870e16;
   - P1 (B2) va inson baholariga tayanadigan barcha natijalar (H2 inson o'rtachalari, H3 S2, H4 S3/P2, H5 Kendall,
     H6–H7 P3, H8 S4, H9 LLM-hakam): ASOSIY — 71 gap (gold-00 chiqarilgan; 355 element); SEZGIRLIK — 72 (360 element);
   - 1-to'lqin bilan taqqoslash (S-savollar, B va C barqarorligi) — 72, 1-to'lqindagidek: SEZGIRLIK 72 jadvallari
     shu taqqoslash uchun (tahlil.py da 1-to'lqin bilan to'g'ridan-to'g'ri taqqoslash hisobi yo'q);
   - §2.5 darvozalari (H1) — 72 (360 element, fayl bo'yicha), o'zgarmaydi;
   - avtomatik metrikalar (A1, A2, B1, X1; COMET — comet_qoshimcha.py) o'zgarmaydi (72 / 400).
   Smoke-test (sintetik, repoga kirmagan): 23 jadval, bo'sh 0; 71 va 72 jadvallari ikkalasi chiqdi.
4. R1 → B, D / R2 → C, E taqsimoti prereg §2.5 da («Ikki tasodifiy tartib (seed 20261016): R1 → B, D; R2 → C, E —
   tarqatishdan oldin belgilangan»).

Maqola uchun cheklov matni:
«Baholovchi yo'riqnomasi 1-to'lqin bilan aynanlik uchun o'zgartirilmadi. Uning misolida baholanadigan gaplardan biri
(gold-00) bor — besh tizimdan uchtasining shu gap uchun chiqishi misoldagi namunaviy tarjimalardan biriga teng. Shu
sababli bu gap tasdiqlovchi tahlildan chiqarildi (71 gap); 72 gaplik natijalar sezgirlik tahlili sifatida va 1-to'lqin
bilan taqqoslash uchun beriladi.»

## 7a (2026-10-20; ma'lumotdan va tarqatishdan oldin)
Sabab: rejalashtiruvchi ko'rsatmasidagi xato — P1 (Δ = BLEU_3ref − BLEU_1ref) avtomatik metrika; baholovchi
yo'riqnomasining ta'siri unga tegmaydi. Tuzatish 7 faqat inson baholariga tayanadigan natijalarga qo'llanadi.
- P1 (B2) — prereg bo'yicha 72 (ASOSIY); 1e8c1a9 dagi 71 varianti olib tashlandi (P1 kodi 1d29166 dagi bilan aynan).
- H2–H9 (inson baholari) — o'zgarishsiz: ASOSIY 71 / SEZGIRLIK 72. H1 darvozalar va avtomatik jadvallar — 72 / 400.
- 1-to'lqin bilan taqqoslash uchun yangi hisob QO'SHILMAYDI (prereg'da yo'q); 3-banddagi jumla o'z holicha qoladi.
- tahlil.py sha256: eski 56522a2b0aed1261feb9a6138351f07c1db8f80213a1a08430b2e58f36870e16 (1e8c1a9) ->
  yangi e3c36ead544567d461ded320b503413743b15e15829b13b7a7c5f5afe5178db1.
- Smoke-test (sintetik, repoga kirmagan): 22 jadval, bo'sh 0; P1 bitta (72), H2–H9 71 va 72.
