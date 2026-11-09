# Kalitsiz moslik tekshiruvi — tuzatish 10 (h) hujjati
Rejalashtiruvchi (Claude) 2026-10-26 da ombordan tashqarida yurgizgan hisob; fayllar tadqiqotchidan
(Desktop/untitled folder, 2026-10-27 17:54 da saqlangan), bayt-aynan nusxa.

| fayl | sha256 |
|---|---|
| moslik_kalitsiz_20261026.py | 6ee7342763d328da069cc8f4e9476b541866bf9d26638e0bc082c5f206c7ff21 |
| moslik_kalitsiz_20261026_chiqish.txt | 04f2a95764b695e18b4b6ba05d32dfc857e1075f26da401c234dda9c1c7713c3 |

**Kirish.** Chiqish faylida kirish sha256 lari YO'Q — to'g'ridan-to'g'ri xesh solishtiruvi mumkin emas. O'rniga qayta hisob:
`~/.venvs/tolqin2_comet/bin/python -I moslik_kalitsiz_20261026.py qaytgan/xom` (numpy 1.26.4, scipy 1.13.1, openpyxl 3.1.5;
loyiha .venv ida scipy yo'q) 2026-10-27 da — chiqish `moslik_kalitsiz_20261026_chiqish.txt` bilan **BAYT-AYNAN**.
Kirish = `xom/` dagi asl qaytarmalar: B 6c721e0c…bab8, C ce00983e…bc5e, D 3d0ab310…3ad1, E d2f285b5…c505.
Nazorat: 2026-10-27 dagi tadqiqotchi tahriri fayllari (`tadqiqotchi_tahriri/`) bilan chiqish FARQ qiladi (B n 317 -> 318) —
saqlangan chiqish tahrir fayllaridan emas, asl qaytarmalardan.

**Kalitsizlik.** Skript `paket/kalit_baho.json` ni o'qimaydi; elementlar (manba gap, tarjima) matn juftligi bo'yicha tekislanadi.
**Usul cheklovi.** 360 elementda noyob (manba, tarjima) juftligi 319: 29 juftlik takror (bir necha tizim bir xil tarjima bergan),
41 element ustma-ust tushadi — har baholovchi uchun shu juftlikning OXIRGI qatoridagi ball olinadi (`dict` ustiga yozish).
Shuning uchun bu α / Spearman tahlil.py dagi H6/H7 (360 / 355 element, element kodi bo'yicha) bilan bir xil kattalik emas.
