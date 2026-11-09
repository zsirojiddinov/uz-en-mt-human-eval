# TOLQIN-2 — veb javoblari moslik tekshiruvi

`veb_moslik.py` chiqishi; javob matni yo'q, faqat sonlar.

<!-- gpt -->
## gpt (12/12 fayl; tayanch claude 472, gemini 472 gap)

### 1. jurnal.csv
- gpt qatorlari: 13 (fayl 12)
- gpt_03.txt: 2 qator — 2026-10-16T15:13:10+05:00, 2026-10-16T15:14:09+05:00; fayl birth 2026-10-16T15:14:04+05:00, mtime 2026-10-16T15:14:09+05:00

### 2. dublikat
- bayt-aynan juftlar: 0
- eng o'xshash juft (butun matn chrF): 03–11 48.2; ikkinchisi 09–11 47.6
- chrF >= 60 juftlar: 0

### 3. moslik (gap-chrF o'rtachasi)

- 01: o'z jufti claude 80.2 / gemini 79.3, eng yaqin boshqa 18.3 (claude_03) — OK
- 02: o'z jufti claude 74.8 / gemini 76.3, eng yaqin boshqa 17.6 (gemini_07) — OK
- 03: o'z jufti claude 76.1 / gemini 79.1, eng yaqin boshqa 18.7 (gemini_12) — OK
- 04: o'z jufti claude 79.1 / gemini 83.2, eng yaqin boshqa 18.2 (claude_12) — OK
- 05: o'z jufti claude 75.8 / gemini 79.5, eng yaqin boshqa 18.3 (gemini_12) — OK
- 06: o'z jufti claude 78.6 / gemini 78.2, eng yaqin boshqa 17.4 (gemini_03) — OK
- 07: o'z jufti claude 78.9 / gemini 78.6, eng yaqin boshqa 17.8 (gemini_05) — OK
- 08: o'z jufti claude 81.4 / gemini 81.5, eng yaqin boshqa 18.3 (gemini_12) — OK
- 09: o'z jufti claude 78.6 / gemini 80.4, eng yaqin boshqa 18.8 (gemini_12) — OK
- 10: o'z jufti claude 78.8 / gemini 79.4, eng yaqin boshqa 18.7 (gemini_01) — OK
- 11: o'z jufti claude 76.9 / gemini 78.5, eng yaqin boshqa 18.6 (gemini_05) — OK
- 12: o'z jufti claude 72.9 / gemini 73.5, eng yaqin boshqa 18.1 (gemini_05) — OK

Jami: OK 12, SHUBHA 0
<!-- /gpt -->

## Izoh (qo'lda, 2026-10-16) — gpt_03 ikki qatori
- Hozirgi `gpt_03.txt` birth 15:14:04 — bu ikkinchi `veb_saqla.sh` yurishining `mktemp` vaqti (fayl `mv` bilan
  tmp'dan o'tadi, birth saqlanadi). Skript yurish boshida va `mv` dan oldin nishon borligini tekshiradi, demak
  15:14:04 da `gpt_03.txt` YO'Q edi: 15:13:10 da saqlangan birinchi fayl shu oraliqda skriptdan tashqarida o'chirilgan/
  ko'chirilgan. Loglardan kim/nima o'chirgani aniqlanmadi (zsh tarixi 14:17 dan keyin diskka yozilmagan, ~/.Trash o'qilmaydi,
  git stash/reflog da iz yo'q). `veb/javob/.DS_Store` mtime 15:14:24 (Finder shu papkada ochiq bo'lgan).
- Ikkala yozuvda bayt 5650 — birinchi faylning mazmuni saqlanmagan, aynanligini tasdiqlab bo'lmaydi.
- «allaqachon bor» ogohlantirishi jurnalga yozilmaydi — shuning uchun u jurnalda ko'rinmaydi.
- Moslik: gpt_03 o'z jufti bilan OK (yuqorida), dublikat yo'q.
- Foydalanuvchi javobi (15:13:10 dagi birinchi `gpt_03.txt` ni skriptdan tashqarida o'chirganmi/ko'chirganmi):
  **ha** — foydalanuvchi birinchi faylni o'zi o'chirgan (2026-10-16 javobi). Skript ustiga yozmagan; ikkinchi
  yurish bo'sh joyga saqlagan.
- Rejada (hali QILINMAGAN): `veb_saqla.sh` da `mv -n` va «allaqachon bor» holatini `jurnal.csv` ga yozish — GT
  tashxisidan keyin, bitta commit bilan.

## GT matn rejimi tashxisi (qo'lda, 2026-10-16) — gt_01–03, 23 qator / 25
Usul: javob qatorlari kirish qatorlariga monoton DP bilan moslandi (1:1, 2:1, 3:1, kirish yo'qolishi); ball — gap-chrF,
tayanch claude_* va gemini_* (kalit.json orqali gap id bo'yicha). Birlashish javob qatori dumining 2-kirish tarjimasiga
mosligi (chrF 58,7–85,9; 1-kirishga 7,7–28,1) va uzunligi bilan tasdiqlandi.
- gt_01: javob 7 = kirish 7+8; javob 15 = kirish 16+17; qolgan 21 qator 1:1. Yo'qolgan kirish 0.
- gt_02: javob 9 = kirish 9+10; javob 17 = kirish 18+19; qolgan 21 qator 1:1. Yo'qolgan kirish 0.
- gt_03: javob 10 = kirish 10+11; javob 16 = kirish 17+18; qolgan 21 qator 1:1. Yo'qolgan kirish 0.
- Umumiy belgi (nuqtasiz tugash, qo'shtirnoq, raqam, qisqa gap, ichki gap chegarasi, `:`/`;`, kichik harf, chetdagi
  bo'shliq): TOPILMADI — birlashgan 12 kirish qatorining 11 tasi nuqta bilan tugaydi; qo'shtirnoq 0 (qolganlarda 2–3).
- Qator sanash: har faylda LF 22, oxirgi qator LF'siz -> 23; CR 0, bo'sh qator 0; jurnal bayti = fayl hajmi.
- Qaror: Tuzatish 3 (Documents rejimi).

<!-- gt -->
## gt (19/19 fayl; tayanch claude 472, gemini 472 gap)

### 1. jurnal.csv
- gt qatorlari: 32 (fayl 23)
- gt_01.txt: 8 qator — 2026-10-16T15:24:17+05:00, 2026-10-16T15:42:52+05:00, 2026-10-16T15:43:14+05:00, 2026-10-16T15:43:46+05:00, 2026-10-16T15:44:02+05:00, 2026-10-16T15:44:20+05:00, 2026-10-16T15:53:29+05:00, 2026-10-16T16:36:31+05:00; fayl birth 2026-10-16T16:36:31+05:00, mtime 2026-10-16T16:36:31+05:00
- gt_02.txt: 2 qator — 2026-10-16T15:24:48+05:00, 2026-10-16T16:36:31+05:00; fayl birth 2026-10-16T16:36:31+05:00, mtime 2026-10-16T16:36:31+05:00
- gt_03.txt: 2 qator — 2026-10-16T15:25:18+05:00, 2026-10-16T16:36:32+05:00; fayl birth 2026-10-16T16:36:31+05:00, mtime 2026-10-16T16:36:32+05:00

### 2. dublikat
- bayt-aynan juftlar: 0
- eng o'xshash juft (butun matn chrF): 14–18 44.4; ikkinchisi 01–10 43.9
- chrF >= 60 juftlar: 0

### 3. moslik (gap-chrF o'rtachasi)

- 01: o'z jufti claude 78.1 / gemini 81.0, eng yaqin boshqa 19.3 (claude_19) — OK
- 02: o'z jufti claude 77.6 / gemini 77.7, eng yaqin boshqa 18.2 (claude_14) — OK
- 03: o'z jufti claude 75.3 / gemini 81.0, eng yaqin boshqa 17.3 (claude_18) — OK
- 04: o'z jufti claude 77.9 / gemini 77.0, eng yaqin boshqa 18.4 (gemini_08) — OK
- 05: o'z jufti claude 75.9 / gemini 77.6, eng yaqin boshqa 18.9 (gemini_19) — OK
- 06: o'z jufti claude 79.0 / gemini 84.0, eng yaqin boshqa 18.5 (claude_18) — OK
- 07: o'z jufti claude 78.5 / gemini 79.2, eng yaqin boshqa 16.6 (claude_12) — OK
- 08: o'z jufti claude 80.6 / gemini 77.2, eng yaqin boshqa 18.9 (gemini_04) — OK
- 09: o'z jufti claude 77.7 / gemini 81.9, eng yaqin boshqa 17.2 (claude_18) — OK
- 10: o'z jufti claude 80.5 / gemini 83.8, eng yaqin boshqa 17.5 (claude_18) — OK
- 11: o'z jufti claude 77.1 / gemini 81.0, eng yaqin boshqa 17.5 (claude_03) — OK
- 12: o'z jufti claude 77.3 / gemini 79.9, eng yaqin boshqa 18.1 (claude_18) — OK
- 13: o'z jufti claude 76.9 / gemini 81.6, eng yaqin boshqa 18.9 (claude_14) — OK
- 14: o'z jufti claude 79.9 / gemini 82.7, eng yaqin boshqa 19.6 (gemini_19) — OK
- 15: o'z jufti claude 78.7 / gemini 81.9, eng yaqin boshqa 18.8 (gemini_14) — OK
- 16: o'z jufti claude 76.2 / gemini 74.8, eng yaqin boshqa 18.7 (claude_18) — OK
- 17: o'z jufti claude 77.5 / gemini 80.6, eng yaqin boshqa 18.5 (claude_13) — OK
- 18: o'z jufti claude 80.7 / gemini 80.4, eng yaqin boshqa 18.1 (claude_14) — OK
- 19: o'z jufti claude 75.0 / gemini 77.3, eng yaqin boshqa 17.9 (gemini_14) — OK

Jami: OK 19, SHUBHA 0
<!-- /gt -->
