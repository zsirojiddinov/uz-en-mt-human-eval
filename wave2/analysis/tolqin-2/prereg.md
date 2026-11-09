# TOLQIN-2 — Preregistratsiya
Sana: commit sanasi. Mualliflar: Z. Sirojiddinov, M. Xakimov. Holat: ma'lumot yig'ishdan OLDIN.
Oldingi ish: 1-to'lqin (evaluation/eval72, 72 gap, 2 to'liq baholovchi) — pilot. Uning 2- va
3-tuzatishlari git'da baholovchi fayllari kelganidan keyin commit qilingan (fayllar 9–10-iyul,
tuzatishlar 14-iyul; matndagi 11-iyul sanasi git bilan tasdiqlanmaydi). Shuning uchun 1-to'lqin
yangi maqolada faqat pilot va qo'shimcha tahlil sifatida keltiriladi.

## 1. Savollar va gipotezalar
S1 (ko'p etalon). Bitta etalonli korpus-BLEU ko'p etalonli (3) korpus-BLEU'dan qanchaga past?
   Asosiy kattalik P1: har tizim uchun Δ = BLEU_3ref − BLEU_1ref (72 gap). Kutilma: barcha
   neyron tizimlarda Δ > 0; son oldindan aytilmaydi.
S2 (absolyut daraja). Inson adequacy o'rtachasi ≥ 4,5 bo'lgan chiqishlar 1 etalonda qanday
   korpus-BLEU oladi? Tavsifiy kalibrovka; 1-to'lqindagi «≈41» gap-BLEU o'rtachasi edi, endi
   korpus-BLEU va gap-BLEU o'rtachasi alohida, nomi bilan beriladi.
S3 (nisbiy tartib). Tizim ICHIDAGI ρ(BLEU_1ref, adequacy) (har tizim, n = 72) umumiy (360 element)
   ρ dan qanchaga past? P2: ikkalasi CI bilan. Kutilma: ichki ρ umumiydan sezilarli past.
S4 (tartib ta'siri). Ikki tasodifiy tartib guruhi orasidagi baho farqi — tadqiqiy.
P3: baholovchilar kelishuvi — juftlik Spearman va Krippendorff α (ordinal), adequacy va fluency.

## 2. Materiallar
2.1 B-qavat (inson): evaluation/eval72/sentences.json, sha256 29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce. O'zgarmaydi. KKT uchun
    ekspozitsiya OCHIQ: FLORES 36 gapning 9 tasida 2026-06-16 lug'at ro'yxatidagi so'z bor;
    ilmiy 24 pattern-mining'da, oddiy 12 regressiya darvozasida ishlatilgan. Neyron tizimlar
    uchun ekspozitsiya: FLORES ommaviy (pretraining ehtimoli) — cheklov sifatida yoziladi.
2.2 A-qavat (avtomatik): FLORES-200 dev'dan 400 gap; YOQISH-2 dagi 50 gap chiqariladi
    (analysis/yoqish-2/held_out.json); qolgan 947 dan seed 20261016 bilan tasodifiy; inglizcha
    etalon rasmiy FLORES-200 relizidan; ro'yxat + sha256 muzlatiladi. Held-out holati: repoda
    ishlatilmagan (INVENTAR-2, 1-band). KKT uchun ekspozitsiya: 78 so'z bo'yicha gap-ma-gap belgi.
2.3 Tizimlar (5): KKT — commit c9639e1 (2026.10.14-52), bitta holat; Gemini, Claude, GPT,
    Google Translate — faqat API, model identifikatori va so'rov sanasi qayd etiladi, temperature
    0 (mavjud bo'lsa), bitta kun ichida, bir xil prompt (matni 2.6). Xom javoblar saqlanadi.
    Qoida: API orqali olib bo'lmagan tizim VEB bilan almashtirilmaydi — chiqarib tashlanadi va
    bu hujjatga tuzatish sifatida yoziladi.
2.4 Etalonlar: 2 mustaqil tarjimon (T1, T2), o'zbekcha→inglizcha, 72 gap; ular tizim
    chiqishlarini va mavjud etalonni ko'rmaydi, baholovchi emas; ko'rsatma: tabiiy, ravon,
    manbaga sodiq inglizcha; post-editing emas. Qabul: 72/72 to'liq; fayl sha256 qabul kuni.
2.5 Baholovchilar: 4 to'liq (B, C — 1-to'lqindan; D, E — yangi; kamida biri ingliz tili
    o'qituvchisi; IELTS ≥ 7,0), bir-biridan xabarsiz. Elementlar: 72 × 5 = 360, neytral ID.
    Ikki tasodifiy tartib (seed 20261016): R1 → B, D; R2 → C, E — tarqatishdan oldin belgilangan.
    Shkalalar: adequacy 1–5, fluency 1–5; ko'rsatma — 1-to'lqin matni (sha256 e3c4c800024faf9d5bcd3274922117a4c68cc63df5587b06a5cf1374af216c56 — rater_A/B/C.xlsx «Yo'riqnoma» varag'i A ustunining 31 qatori, "\n" bilan birlashtirilgan, UTF-8 matni) +
    «tizimni taxmin qilmang» bandi. Yaxlitlik darvozalari (kalitsiz hisoblanadi, chegaralar shu hujjatda belgilanadi):
    (a) to'liqlik — 360/360 element, ikkala shkala; (b) diapazon — faqat 1, 2, 3, 4, 5 butun
    qiymatlar; (c) avtopilot — ketma-ket bir xil (adequacy, fluency) juftligi qatori ≥ 12 bo'lsa
    belgilanadi; (d) ichki izchillik — Spearman(adequacy, fluency) [0,30; 0,95] oralig'idan tashqarida
    bo'lsa belgilanadi; (e) nusxa — adequacy = fluency bo'lgan elementlar ulushi ≥ 0,90 bo'lsa
    belgilanadi. Belgilangan fayl bir marta to'ldirishga/izohga qaytariladi (4-bo'lim).
2.6 Tarjima prompti (neyron tizimlar uchun, aynan): "Translate the following Uzbek sentence into
    English. Output only the translation." Har gap alohida so'rov.
2.7 Metrikalar: sacreBLEU 2.6.0, tokenizatsiya 13a; korpus-BLEU ASOSIY; gap-BLEU o'rtachasi
    (smoothing exp) ikkilamchi; chrF (chrF2); ko'p etalon — sacreBLEU'ning ko'p etalon rejimi.
    COMET (wmt22-comet-da) — o'rnatilsa, ikkilamchi; o'rnatilmasa chiqarib tashlanadi, yoziladi.
2.8 LLM-hakam (tadqiqiy): imlo mexanizmi 1–5 shkalaga moslanadi; 2 hakam-model, 360 element,
    ikki tartib; inson o'rtachasiga qarshi Spearman. Model identifikatorlari qayd etiladi.

## 3. Tartib (bajarilish ketma-ketligi, har qadam commit bilan)
(1) prereg commit → (2) A-qavat ro'yxati + sha256 → (3) chiqishlar, MANIFEST (model id, sana,
sha256) → (4) paketlar: T1/T2 fayli (faqat manba), R1/R2 paketlari, kalit; kalit sha256 commit →
(5) TAHLIL SKRIPTI yoziladi va commit qilinadi — TARQATISHDAN OLDIN → (6) tarqatish →
(7) qaytgan har fayl: kelgan vaqt (email/fayl mtime) qayd, darvozalar kalitsiz → (8) to'xtash
qoidasi → (9) skript bir marta yuriladi, natija commit.
To'xtash qoidasi: tarqatish kunidan 14 kun — muddat D. D gacha ≥ 3 to'liq baholovchi fayli va 2
etalon fayli bo'lsa, asosiy tahlil shu fayllar bilan yakuniy; kam bo'lsa D bir marta 7 kunga
uzaytiriladi; undan keyin kelgan fayllar faqat qo'shimcha tahlilga.
Tuzatish qoidasi: har tuzatish sanali commit; tegishli ma'lumot fayli kelgan vaqtdan KEYIN
commit qilingan tuzatish «natijadan keyingi» deb belgilanadi va shunday hisobot qilinadi.

## 4. Tahlil rejasi (skript shu bo'yicha, bir marta)
A-qavat: 5 tizim × 400: korpus-BLEU, gap-BLEU o'rtachasi, chrF (COMET bo'lsa); KKT uchun
  ekspozitsiyali/ekspozitsiyasiz gaplar alohida.
B-qavat: 5 tizim × 72: 1 va 3 etalonda korpus-BLEU va chrF (P1); gap darajasida 1 va 3 etalonli
  BLEU; inson adequacy/fluency o'rtachasi (4 baholovchi); S2 kalibrovkasi (adequacy ≥ 4,5).
Korrelyatsiya: umumiy (360) va tizim ichida (72 × 5), qatlam bo'yicha; Spearman, bootstrap 1000,
  95 % CI; past ball rejimida (BLEU_1ref < 10) Kendall τ.
Kelishuv: juftlik Spearman, Krippendorff α (ordinal); tartib guruhlari farqi (R1 vs R2) — tadqiqiy.
LLM-hakam: inson o'rtachasiga qarshi Spearman, tizim bo'yicha; tadqiqiy.
Istisno: darvozadan o'tmagan fayl bir marta to'ldirishga qaytariladi; ikkinchi marta o'tmasa
  chiqariladi va hisobot qilinadi. Tarjimon fayli to'liq bo'lmasa qaytariladi.

## 5. Oldindan ma'lum cheklovlar
KKT ekspozitsiyasi (2.1); FLORES ommaviyligi; bitta til jufti; 72 gap inson qavati; 1-to'lqin
tuzatishlari vaqti; 1-to'lqin raqamlari gap-BLEU o'rtachasi bo'lgani (yangi maqolada tuzatiladi).
