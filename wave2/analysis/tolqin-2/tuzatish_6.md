# Tuzatish 6 (ma'lumotdan oldin: tarjimon va baholovchi fayllari hali tarqatilmagan va kelmagan)
Sana: 2026-10-20. tahlil.py (1d29166) o'zgartirilmagan.

A) COMET (prereg §2.7). O'rnatish urinishi 2026-10-20 15:07:41–15:12:43 (`veb/jurnal.csv`): alohida venv
   `~/.venvs/tolqin2_comet` (loyiha .venv iga tegilmagan), unbabel-comet 2.2.7, model Unbabel/wmt22-comet-da
   (etalonli; model.ckpt sha256 e213091c…f2af) — O'RNATILDI; 3 sintetik juftda ishladi. Shuning uchun COMET prereg
   §2.7 bo'yicha IKKILAMCHI metrika sifatida alohida muzlatilgan `comet_qoshimcha.py` (4d67147) bilan hisoblanadi:
   A — 5 × 400, FLORES etalon; B — 5 × 72, har etalon (ref_en, T1, T2) bilan alohida va uchalasining o'rtachasi.
   Cheklov: wmt22-comet-da o'qitish ma'lumotida o'zbek tili yo'q. Tartib: avval `tahlil.py --yurish`, keyin
   `comet_qoshimcha.py --yurish` (tahlil.py natija/ mavjud bo'lsa to'xtaydi). tahlil.py natijasidagi «COMET
   o'rnatilmagan» yozuvi loyiha muhitiga tegishli; COMET qiymati faqat `natija/comet_natija.json` dan olinadi.

B) Tarjimon paketlari (1214067): xlsx varaqlari parolsiz himoyalangan — ochiq faqat «Tarjima» ustuni va Deklaratsiya
   qiymat katakchalari; gaplar, tartib va kalit o'zgarmagan. Qabul — muzlatilgan `qabul.py`: Manba NFC dan keyin asl
   bilan aynan, 72/72 to'ldirilgan; normallashtirish FAQAT Tarjima da (NFC; “ ” „ ‟ « » -> "; ‘ ’ ‚ ‛ -> ';
   NBSP/U+202F/U+2007 -> bo'shliq; bosh/oxir bo'shliq), har tur soni `qaytgan/qabul_jurnal.csv` ga (matnsiz).
   ʻ (U+02BB) va ʼ (U+02BC) tipografik belgi emas — o'zgartirilmaydi. Chiqish qaytgan/TX.xlsx (Manba = asl matn).

C) Baholovchi paketlari (aeca30d): 360 element; seed 20261016 bilan bitta RNG ketma-ket — neytral ID, R1, R2;
   R1 -> B, D; R2 -> C, E. Varaqlar 1-to'lqin `rater_*.xlsx` tuzilishida (Yo'riqnoma matni «Mazmun»/«Ravonlik»
   ustunlariga tayanadi): Element | O'zbekcha gap | Inglizcha tarjima | Mazmun (1-5) | Ravonlik (1-5); etalon
   ko'rsatilmaydi (1-to'lqindagidek). Yo'riqnoma A1:A31 — 1-to'lqin matni aynan (sha256 e3c4c800…); prereg §2.5
   dagi «tizimni taxmin qilmang» bandi A33 da: «  - Tizimni taxmin qilmang.». Baho katakchalari butun 1–5
   validatsiyali, qolgani himoyalangan. `qabul.py baho X` qaytgan faylni tahlil.py formatiga (Element | Adequacy |
   Fluency) o'tkazadi; baholar va qator tartibi o'zgarmaydi; matn ustuni/tartib farqi va darvozalar (a)–(e) jurnalga
   yoziladi (fayl rad etilmaydi — prereg §4 istisnosi bo'yicha qaror alohida, `qaytgan/chiqarilgan.json`).
