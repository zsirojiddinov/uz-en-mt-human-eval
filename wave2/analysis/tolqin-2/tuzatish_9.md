# Tuzatish 9 — qaytgan fayllar: prereg'da qoidasi YO'Q holatlar (NATIJADAN KEYINGI)
Sana: 2026-10-26. Prereg §3 tuzatish qoidasi bo'yicha bu tuzatish **«natijadan keyingi»**: baholovchi (B, C, D, E) va
T1 fayllari shu commitdan OLDIN kelgan va muzlatilgan `qabul.py` dan o'tkazilgan (`qaytgan/qabul_jurnal.csv`,
2026-10-26T19:42+05:00). Tizim kaliti (`paket/kalit_baho.json` elementlar -> tizim) bilan hech qanday hisob yuritilmagan;
`tahlil.py`, `etalon_tekshir.py`, `comet_qoshimcha.py` yurmagan; `natija/` yo'q. `tahlil.py`, `qabul.py` o'zgartirilmagan.
Faqat prereg (va tuzatish 1–8) sukut saqlagan holatlar; qoida BOR holatlar 4-bo'limda — ular uchun tuzatish yozilmadi.

## 1. E — o'zini «[AI]» deb belgilagan fayl (prereg'da qoida yo'q)
Fakt (fayldan, matnsiz): qaytgan `baho_E.xlsx` (sha256 d2f285b531b97ae54b20858b503403e2295e610f303305db56adf847cc30c505)
«Baholash» sarlavhasi D1 = «Mazmun (1-5) [AI]», E1 = «Ravonlik (1-5) [AI]». Generator shablonida (`paket_baho.py`, `SAR`) va
tarqatilgan faylda (`paket/baholovchi/baho_E.xlsx` = `E.zip` ichidagi, sha256 f84b6121…2d642) «[AI]» YO'Q — belgi tarqatishdan
KEYIN, qaytgan faylda qo'shilgan; bizning generator qo'ymagan. Fayl Excel emas, openpyxl asosidagi dastur bilan saqlangan
(docProps/app.xml), ikkala varaq himoyasi olib tashlangan; boshqa matn kataklari paketdagi bilan aynan. Kim qo'ygani fayldan
aniqlanmaydi. Baholovchidan AI ishlatilmagani haqida deklaratsiya yo'q (baholovchi paketida deklaratsiya varag'i yo'q).
Muzlatilgan `qabul.py` E ni mustaqil ravishda RAD qildi («sarlavha paketdagidek emas») — `qaytgan/baho_E.xlsx` yo'q.

Qaror: E **asosiy inson tahlilidan chiqariladi** (H2–H9, darvoza natijalaridan qat'i nazar).
Sezgirlik «E bilan» — talab qilingan; lekin uni hisoblash yo'li (qabul.py RAD qilgan faylni tahlil.py ga berish) bu
tuzatishda BELGILANMAGAN — Q2 dan oldin alohida sanali qaror (tahlil.py faqat `qaytgan/baho_E.xlsx` ni o'qiydi).
Ma'lumot uchun (tahlil.darvoza, kalitsiz): (a) o'tdi, (b) o'tdi, (c) eng uzun 17 — belgi, (d) 0,772, (e) 0,733.

## 2. Tahlildan oldin ko'rilgan narsalar (prereg'da qoida yo'q)
2026-10-26, tizim kalitisiz: har qaytgan baho faylidagi ball qiymatlari soni (1–5, adequacy va fluency birga, fayl bo'yicha),
bo'sh kataklar soni va element ID si, darvoza (c)–(e) statistikalari (yuqorida va qabul jurnalida), fayl metama'lumoti
(dastur, saqlash vaqti, himoya). Element -> tizim kaliti ochilmagan; tizim yoki gap bo'yicha hech qanday o'rtacha ko'rilmagan.
Maqolada: «Baholovchilar ballarining umumiy taqsimoti (tizim kalitisiz) tahlil qarorlaridan oldin ko'rildi.»

## 3. T1 deklaratsiyasi (prereg'da qoida yo'q)
«Deklaratsiya» varag'ida 5 maydondan 0 to'ldirilgan, «Roziman» bo'sh (imzosiz). Cheklov sifatida yoziladi.
(T1 fayli qabul.py da RAD — 4-bo'lim (d).)

## 4. Taklif qilingan, lekin prereg'da qoidasi BOR — tuzatish YOZILMADI (prereg qoidasi amal qiladi)
(b) D: D darvoza (a) dan o'tmadi (E019 fluency bo'sh) — prereg §2.5 (a), §4 (bir marta to'ldirishga qaytariladi),
    tuzatish 5.6 ((a) dan o'tmagan fayl hisoblanmaydi). «Prereg darvozasi bo'lmasa» sharti bajarilmadi. D fayl
    metama'lumoti (openpyxl asosidagi dastur; saqlash vaqti 2026-10-20T17:04Z) — faqat qayd, qaror emas.
(c) Bo'sh kataklarni juftlik bo'yicha chiqarish: prereg §2.5 (a), §4, tuzatish 5.6 — B (E159, E219 ikkala shkala) va
    D (E019) to'ldirishga qaytariladi; qaytmasa/ikkinchi marta o'tmasa — chiqariladi.
(d) T1 № 55 faqat asl etalon bilan: prereg §2.4 (qabul 72/72), §4 (to'liq bo'lmasa qaytariladi); tahlil.py ham 72/72 talab qiladi.
(e) T2 olinmadi: prereg §3 to'xtash qoidasi (muddat D gacha 2 etalon; kam bo'lsa D bir marta 7 kunga uzaytiriladi);
    tuzatish 8 §2. B, D berilgan 2026-10-21 -> D = 2026-11-04; C, E, T1, T2 uchun `tarqatish_jurnali.csv` da berilgan sana bo'sh.
