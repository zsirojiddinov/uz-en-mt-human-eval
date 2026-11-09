# Tuzatish 12 — tuzatish 10 (h) ga xronologik aniqlik (NATIJADAN KEYINGI)
Sana: 2026-10-29. Prereg §3 tuzatish qoidasi bo'yicha **«natijadan keyingi»** (natija/ — 93111a5). Hech narsa o'chirilmaydi:
tuzatish 10 matni o'zgarishsiz qoladi, bu tuzatish u bilan birga o'qiladi. Tahlil, skript va natijalarga ta'siri yo'q.

## 1. Aniqlik
Tuzatish 10 (h): «Bu kattaliklar (a), (b), (g) qarorlariga asos bo'lmagan (tadqiqotchi bayonoti)».
Xronologiya (2-bo'lim) bo'yicha (a), (b) va (g) qarorlari kalitsiz kattaliklar hisoblangan kundan (2026-10-26) KEYIN,
2026-10-27 da qabul qilingan. Shuning uchun:
- «asos bo'lmagan» — faqat tadqiqotchi bayonoti; uni vaqt tartibi bilan tasdiqlab bo'lmaydi;
- (g) qarori (B, D bo'sh kataklari qayta so'ralmaydi; juftlik bo'yicha chiqarish) kalitsiz α / Spearman hisoblangandan
  KEYIN qabul qilingan;
- (g) mazmunidagi juftlik chiqarish g'oyasi birinchi marta 2026-10-26 19:39 da taklif qilingan (tuzatish 9, 4-bo'lim (c) —
  o'shanda prereg qoidasi amal qilishi qayd etilgan); kalitsiz hisobning soati qayd etilmagani uchun bu taklif hisobdan
  oldinmi yoki keyinmi — aniqlanmaydi;
- (d) to'ldirilishi («E bilan» sezgirlik bitta yurishda) va (i) (muddatdan oldin tahlil) ham kalitsiz kattaliklardan KEYIN
  (2026-10-27 18:20); E ni chiqarish qarori (tuzatish 9, 2026-10-26 22:17 commit) bilan kalitsiz hisobning tartibi aniqlanmaydi.
Maqolada (tuzatish 10 (h) jumlasi o'rniga): «Baholovchilar o'rtasidagi kelishuv (α, juftlik Spearman; tizim kalitisiz)
2026-10-26 da hisoblandi; ma'lumot bilan ishlash qarorlari (T1 71/72, T2 yo'q, bo'sh kataklar, muddatdan oldin tahlil)
undan keyin, 2026-10-27 da qabul qilindi.»

## 2. Xronologiya (+05:00)
Manbalar: git (commit vaqti), qaytgan/qabul_jurnal.csv, fayl mtime, qaytgan/kalitsiz_tekshiruv/README.md, Claude Code sessiya
jurnalidagi tadqiqotchi xabarlari vaqti (ombordan tashqarida; vaqt UTC dan o'girilgan).

| vaqt | voqea | manba |
|---|---|---|
| 2026-10-26 17:17:28 | B qaytarmasi (fayl mtime) | qabul_jurnal.csv |
| 2026-10-26 19:18:20 | D qaytarmasi (fayl mtime) — kalitsiz hisob kirishlaridan oxirgisi | qabul_jurnal.csv |
| 2026-10-26 19:18:20 dan keyin, 2026-10-26 ichida (soat qayd etilmagan) | kalitsiz moslik hisobi (rejalashtiruvchi, ombordan tashqarida) | moslik_kalitsiz_20261026.*, tuzatish 10 (h); chiqish xom/ dagi asl B, C, D, E bilan bayt-aynan |
| 2026-10-26 19:39:13 | tadqiqotchi xabari (Q1): E ni chiqarish, bo'sh kataklarni juftlik bo'yicha chiqarish, T1 № 55 — taklif | sessiya jurnali |
| 2026-10-26 19:42:08 | qabul.py (B, C, D, E, T1) | qabul_jurnal.csv |
| 2026-10-26 21:05:17 | commit 38a0202 — Q1 qabul (qabul jurnali) | git |
| 2026-10-26 22:17:39 | commit dcb7190 — tuzatish 9 (E chiqariladi; juftlik chiqarish — prereg qoidasi bor, yozilmadi) | git |
| 2026-10-27 12:13:35 | tadqiqotchi xabari (Q1b): (a) T1 71/72, (b) T2 yopildi — «tadqiqotchi qarori, 2026-10-27» | sessiya jurnali |
| 2026-10-27 16:22:34 | tadqiqotchi xabari (Q1c yakuniy): **(g)** — baholovchilar qayta so'ralmaydi | sessiya jurnali |
| 2026-10-27 16:23:44 | commit 0774fc4 — Q1c | git |
| 2026-10-27 17:12:54 | tadqiqotchi xabari: (h) matni — kalitsiz kattaliklar sessiyada birinchi marta | sessiya jurnali |
| 2026-10-27 17:54:44 | kalitsiz chiqish fayli Desktop da saqlangan (mtime; hisob vaqti emas) | fayl mtime, kalitsiz_tekshiruv/README.md |
| 2026-10-27 18:20:59 | tadqiqotchi xabari (Q2): **(i)** va **(d)** to'ldirilishi | sessiya jurnali |
| 2026-10-27 18:25:03 | commit 165e895 — tuzatish 10 | git |
| 2026-10-27 18:32:33 | commit 93111a5 — natija (tahlil.py, etalon, COMET) | git |

| qaror | sana-soat | kalitsiz hisobga nisbatan |
|---|---|---|
| tuzatish 10 (a), (b) | 2026-10-27 12:13 | KEYIN |
| tuzatish 10 (g) | 2026-10-27 16:22 | KEYIN |
| tuzatish 10 (d) to'ldirilishi | 2026-10-27 18:20 | KEYIN |
| tuzatish 10 (i) | 2026-10-27 18:20 | KEYIN |
| tuzatish 9 (E chiqariladi) | taklif 2026-10-26 19:39, commit 22:17 | aniqlanmaydi (hisob soati yo'q) |
