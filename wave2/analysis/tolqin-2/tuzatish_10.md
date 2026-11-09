# Tuzatish 10 — T1 71/72, T2 yo'q, B/D qayta qaytarilmadi; muzlatilgan skriptlarga sanali o'zgarish (NATIJADAN KEYINGI)
Sana: 2026-10-27 (commit). Qarorlar sanasi: 2026-10-27 (tadqiqotchi).
Prereg §3 tuzatish qoidasi bo'yicha **«natijadan keyingi»**: T1 (2026-10-26) va baholovchi fayllari (B, C, D, E) bu commitdan
oldin kelgan va qabul qilingan (qaytgan/qabul_jurnal.csv; tuzatish 9; Q1c). Qarorlar paytida element -> tizim kaliti bilan hech
qanday hisob yuritilmagan; tahlil.py, etalon_tekshir.py, comet_qoshimcha.py yurmagan; natija/ va etalon/ yo'q. Tahlildan oldin
kalitsiz ko'rilgan narsalar — tuzatish 9, 2-band.
Muddat (prereg §3): tarqatish 2026-10-20..21 (aniq kun qayd etilmagan; tarqatish_jurnali.csv) -> D = 2026-11-04 (kechroq sana
bo'yicha); D gacha 2 etalon yo'q -> D bir marta uzaytiriladi -> 2026-11-11. Tahlil shu muddatdan OLDIN yuriladi — (i).

## (a) T1 — 71/72 qabul qilinadi
Tadqiqotchi qarori (2026-10-27). № 55 bo'sh; shu gap uchun ko'p etalonli avtomatik metrikalar faqat asl etalon (eval72 ref_en)
bilan. Og'ish: prereg §2.4 («Qabul: 72/72 to'liq») va §4 («Tarjimon fayli to'liq bo'lmasa qaytariladi») — T1 qaytarilmadi.
T1 deklaratsiyasi imzosiz (tuzatish 9, 3-band) — cheklov.

## (b) T2 — olinmadi
Qidiruv 2026-10-27 da yopildi (tadqiqotchi qarori); T2 tarqatilmagan (tarqatish_jurnali.csv). Ko'p etalonli avtomatik metrikalar
= asl + T1 (2 etalon; № 55 da 1). P1 (prereg §1: Δ = BLEU_3ref − BLEU_1ref) endi Δ = BLEU_(asl+T1) − BLEU_1ref; natija
jadvallaridagi «3ref» va COMET dagi «uch_etalon_ortacha» kalitlari shu ma'noda (oqimlar natijada: tahlil — R['kop_etalon'],
COMET — 'etalonlar'). Etalon mustaqilligi tekshiruvi (tuzatish 8) faqat T1 uchun; T1–T2 chrF hisoblanmaydi (null).
Og'ish: prereg §2.4 (2 tarjimon), §3 (2 etalon), tuzatish 8 §2 (bayroq bo'lsa yangi tarjimon).

## (g) B va D — bo'sh kataklar qayta qaytarilmadi
Tadqiqotchi qarori (2026-10-27): baholovchilar qayta so'ralmaydi. Bo'sh kataklar: B — E159 (adequacy, fluency), E219
(adequacy, fluency); D — E019 (fluency). Xabar orqali olingan B E159 va D E019 qiymatlari hujjatlanmagan — ishlatilmaydi
(Q1c; qaytgan/tadqiqotchi_tahriri/README.md). Ma'lumot — 2026-10-26 asl qaytarmalar (qaytgan/xom/, qaytgan/baho_{B,D}.xlsx).
Og'ish: prereg §2.5 (a) va §4 (bir marta to'ldirishga qaytariladi) hamda tuzatish 5.6 («(a) dan o'tmagan fayl hisoblanmaydi»).
Yangi qoida: fayllar saqlanadi; shu 5 katak «yo'q ma'lumot»; element bo'yicha juftlik chiqarish — inson o'rtachasi (H2–H5)
mavjud baholar bo'yicha, juftlik Spearman (H6) ikkala baho bor elementlarda, Krippendorff α (H7) har birlikda mavjud baholar
bilan (α ning standart yo'q ma'lumot ishlovi), S4 (H8) har guruhda kamida bitta baho bor elementlarda.
H1 darvoza natijalari o'zgarmaydi: B va D uchun (a) = o'tmadi, shunday hisobot qilinadi.
Ruxsat faqat shu 5 katak uchun (BOSH10_BAHO): boshqa bo'sh katak bo'lsa fayl avvalgidek ishlatilmaydi.
Natijada asosiy inson tahlili: **B, C, D** (R1: B, D; R2: C).

## (d) E — chiqarilgan
Tuzatish 9 (a) o'zgarishsiz; qaytgan/chiqarilgan.json (Q1c). Asl qaytarma (sarlavhasi «[AI]» bilan) — qaytgan/xom/E__baho_E.xlsx.
2026-10-27 dagi tadqiqotchi tahriri (sarlavhadan «[AI]» olib tashlangan) ma'lumot emas — qaytgan/tadqiqotchi_tahriri/.
Sezgirlik «E bilan» (tuzatish 9 (a)) BITTA yurishda hisoblanadi: tahlil.py H2–H9 ni ikki to'plamda chiqaradi — asosiy
ishlat = B, C, D (R['jadvallar']; ro'yxati R['inson']); sezgirlik ishlat_E = B, C, D, E (R['inson_E_bilan'], natija .md da
alohida bo'lim). E manbasi — asl qaytarma qaytgan/xom/E__baho_E.xlsx («Baholash» varag'i, 1-, 4-, 5-ustunlar; sarlavha matni
o'qilmaydi), sha256 natijada. E uchun (a)/(b) darvozalari shu asl faylda tekshiriladi (R['inson_E_bilan']['darvoza_E']);
qaytgan/chiqarilgan.json faqat shu variantda e'tiborga olinmaydi. H1 jadvali o'zgarmaydi (E qabul.py da RAD — H1 da yo'q).
Bu to'ldirish (h) dagi kattaliklar ma'lum bo'lgandan KEYIN qabul qilingan (2026-10-27).

## (h) Tahlildan oldin hisoblangan kelishuv (tuzatish 9, 2-bandni TO'LDIRADI)
Tahlildan oldin, 2026-10-26, rejalashtiruvchi (Claude) ombordan tashqarida, tizim kalitisiz, to'rt qaytarmaning (B, C, D, E)
o'zaro mosligini hisobladi: Krippendorff α (ordinal) mazmun ≈ 0,20, ravonlik ≈ 0,09 (319 tekislangan element); juftlik Spearman
0,15–0,59; baholovchi tarqalishlari. Tizim bo'yicha hech qanday natija ko'rilmagan. Bu kattaliklar (a), (b), (g) qarorlariga asos
bo'lmagan (tadqiqotchi bayonoti); H6/H7 natijalari shu ma'lumot bilan o'qilishi kerak.
Izoh: tuzatish 9 (dcb7190), 2-band bu hisobni sanamagan — u faqat qabul sessiyasida ko'rilganlarni (ball qiymatlari soni, bo'sh
kataklar, darvoza (c)–(e), fayl metama'lumoti) qayd etgan; to'liq ro'yxat = tuzatish 9, 2-band + shu band.
Hujjat: qaytgan/kalitsiz_tekshiruv/ — qayta hisoblandi. Skript moslik_kalitsiz_20261026.py (sha256 6ee73427…ff21), chiqish
moslik_kalitsiz_20261026_chiqish.txt (04f2a957…13c3). Chiqishda kirish sha256 lari yo'q; qayta hisob qaytgan/xom/ dagi asl
B, C, D, E da (2026-10-27) — chiqish BAYT-AYNAN; 2026-10-27 tadqiqotchi tahriri fayllari bilan farq qiladi (asl fayldan ekani tasdiqlandi).
Skript tizim kalitini o'qimaydi. Usul cheklovi: (manba, tarjima) matn juftligi bo'yicha tekislash — 360 elementdan 319 noyob juftlik,
41 element ustma-ust (bir xil tarjima bergan tizimlar; har baholovchida oxirgi qator bali olinadi) — shuning uchun H6/H7 bilan
bir xil kattalik emas. Aniq qiymatlar: α (ordinal) mazmun BCDE 0,198 · BCD 0,103; ravonlik BCDE 0,085 · BCD −0,088;
juftlik Spearman 0,152–0,598.
Maqolada: «Baholovchilar o'rtasidagi kelishuv (α, juftlik Spearman; tizim kalitisiz) tahlil qarorlaridan oldin ko'rildi.»

## (i) Asosiy tahlil muddatdan OLDIN
Asosiy tahlil prereg §3 uzaytirilgan muddati (2026-11-11) dan OLDIN, 2026-10-27 da yurgiziladi — tadqiqotchi qarori (2026-10-27).
Sabab: T2 qidiruvi yopilgan (b), baholovchilar qayta so'ralmaydi (g) — boshqa fayl kutilmaydi. Shu kundan keyin kelgan har qanday
fayl faqat qo'shimcha tahlilga (§3 ning muddatdan keyingi qoidasi bilan bir xil). Og'ish: prereg §3 (to'xtash qoidasi muddatdan
oldin yopishni nazarda tutmaydi — Q1b hisoboti, 2026-10-27). Bu qaror (h) dagi kattaliklar ma'lum bo'lgandan keyin qabul qilingan.

## (c) Muzlatilgan skriptlarga o'zgarish
Sabab: muzlatilgan versiyalar T1 va T2 ni 72/72 va baholovchi fayllarini to'liq (a) holatda talab qiladi — (a), (b), (g) bilan
yurmaydi (tahlil.py T1 № 55 da assert bilan to'xtaydi). O'zgarishlar faqat kirishlarni o'qish, ko'p etalon oqimlarini yig'ish
va yo'q ma'lumotni o'tkazish hamda (d) «E bilan» variantini shu inson() funksiyasi bilan ikkinchi to'plamda chiqarish bilan
cheklangan; metrikalar, bootstrap, darvoza va jadval tuzilishi tegilmagan.
tahlil.py uchun bu IKKINCHI sanali o'zgarish (birinchisi — tuzatish 7/7a); qolgan uchtasi uchun birinchi.

| fayl | eski sha256 (HEAD) | yangi sha256 | mazmun |
|---|---|---|---|
| tahlil.py | e3c36ead544567d461ded320b503413743b15e15829b13b7a7c5f5afe5178db1 | aaf37cda525c194fe0d59f456421cd55e7852ec9a6b0b6146f6f1f68daffa20c | BOSH10 = {(T1, 55)}, BOSH10_BAHO (5 katak), toliq10(), ort10(); yo'q T2 fayli o'tkaziladi; r3 = asl + mavjud tarjimonlar, yo'q etalon None; bh da None; H2–H8 da juftlik chiqarish; (d) E_XOM, e_xom(), R['inson'], R['inson_E_bilan'] (+ md bo'limi); R['kop_etalon'], R['baholovchilar']['yoq_malumot'] |
| qabul.py | 35eed7e503b99e7d369542120d9fbbb676dc3568ca18154efdfac5c31e030a53 | 8a4ff76100ae6ebdee3fd2f64e5a34a4b91186daaa8dae58d023f5b7fc466966 | T1 № 55 bo'sh bo'lsa RAD qilinmaydi (bir qator) |
| etalon_tekshir.py | 17ce8799d81f93436767dfdfde95219c570c37e57586ac84025c128ae3880cc1 | 99d43bb9f2239282bf51e24b47bf06473ffe59b93172de27c0ab19fb26003eb3 | T2 yo'q -> o'tkaziladi; T1 71 (bo'sh gap tashlanadi); n_gap tarjimon bo'yicha; T1–T2 chrF faqat ikkalasi bo'lsa. Bayroq chegarasi (a) 18 gap — o'zgarmagan |
| comet_qoshimcha.py | 6c11058578f8988a4aa12382a4b699b19df4ffa3a87dc4e6f8f236a30e351680 | c6e58e9031cc7bc4bca9665c1b831b02529dc3f72a75d52c60c9671e01c975c3 | etalonlar = ref_en + mavjud tarjimonlar; yo'q etalonli gap shu etalon ballidan tashlanadi; gap o'rtachasi mavjud etalonlar bo'yicha; {e}_n, 'etalonlar' |

Diff: tuzatish_10.patch (to'rt fayl). sacreBLEU 2.6.0 `_cache_references`: «A particular reference segment can be '' or None to
allow the use of variable number of references per segment».

Smoke-test (sintetik, scratchpad, repoga kirmagan; real tizim chiqishlari ishlatilmagan — O3):
- T1+T2 to'liq, bo'sh katak yo'q: tahlil.py, etalon_tekshir.py, comet_qoshimcha.py natijalari eski versiyalar bilan BAYT-AYNAN
  (faqat qo'shilgan kalitlardan tashqari: kop_etalon, yoq_malumot, inson, inson_E_bilan, n_gap, {e}_n, etalonlar); .md da eski
  matn yangisining boshi; E asosiyda ham bo'lsa «E bilan» jadvallari asosiy bilan aynan;
- T1 71 + T2 yo'q + B (E159, E219) va D (E019) bo'sh + E chiqarilgan, E faqat xom/ da (5 ustun, «[AI]» sarlavha): 22 jadval,
  bo'sh 0; asosiy B, C, D; «E bilan» B, C, D, E — 16 jadval, bo'sh 0; H1 da E yo'q; H1 (a) B, D = o'tmadi; eski tahlil.py
  shu kirishda to'xtaydi;
- ro'yxatda yo'q bo'sh katak (B E001): B ishlatilmaydi (C, D);
- etalon_tekshir: T1 71 gap, T1–T2 = null; comet (soxta model): ref_en_n 72, T1_n 71.

## Bajarilish tartibi (2026-10-27, (i))
1. Shu tuzatish + to'rt skript o'zgarishi + qaytgan/kalitsiz_tekshiruv/ — bitta commit.
2. `qabul.py tarjimon T1 xom/T1__tarjima_T1 (1) (1).xlsx` -> qaytgan/T1.xlsx (71/72).
3. etalon_tekshir.py --yurish -> tahlil.py --yurish -> comet_qoshimcha.py --yurish (har biri bir marta).
