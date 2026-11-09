# EKSPOZITSIYA-2 — reja (natijadan OLDIN, 2026-10-20)

Maqsad: TOLQIN-2 ning 472 manba gapi (A-qavat `a_qavat_400.json` 400 + B-qavat `evaluation/eval72/sentences.json` 72)
repodagi boshqa gap to'plamlarida, kod/data tarixida va commit xabarlarida uchraganmi — faqat MANBA (o'zbekcha) gaplar.
Tizim javoblari (`veb/javob*`, `kkt_chiqish.json`) ochilmaydi va tekshirilmaydi.

## Normallashtirish
1. Apostrof variantlari (ʻ ʼ ‘ ’ ` ´ ′ va h.k.) → `'`.
2. Kichik harf (Unicode `lower`).
3. Tinish belgilari olib tashlanadi (Unicode toifasi P* va S*; `'` so'z ichida saqlanadi).
4. Bo'shliqlar bitta bo'shliqqa yig'iladi, chetlar kesiladi. So'z = bo'shliq bilan ajratilgan token.

## Moslik
- Aniq: normallashtirilgan matnlar teng.
- Yaqin (aniq bo'lmaganlar orasida): so'z 5-gramlari to'plamlari Jaccard ≥ 0,5 YOKI 8+ so'zli umumiy uzluksiz
  ketma-ketlik. Har ikki gapda ≥ 5 so'z bo'lmasa Jaccard hisoblanmaydi (faqat 8+ ketma-ketlik va aniq).
- Har to'plam uchun: aniq soni, yaqin soni, 472 dan qaysi ID lar (to'plam, id).

## Qamrov
1. Gap to'plamlari: `analysis/` va `evaluation/`, `corpus/`, `data/` dagi barcha o'zbekcha gap ro'yxatlari (json/jsonl/tsv/csv/txt),
   jumladan 2 119 (`echo1_skan.json`), 2 597 (joyi aniqlanadi), imlo darvozasi 3 301, vaqt 2 477, SINOV-4…7.
   TOLQIN-2 ning o'z fayllari (`analysis/tolqin-2/`) va manbalarning o'zi (`evaluation/eval72/sentences.json`,
   FLORES keshi) kesishmadan chiqariladi — ular ta'rifan mos.
2. Git tarixi: `git log --all -p` (barcha branchlar) — qo'shilgan/o'chirilgan qatorlar va commit xabarlari; 472 gapdan
   birortasi yoki uning 8+ so'zli bo'lagi. Topilsa — birinchi commit, sanasi, fayl yo'li toifasi (test/fixture,
   data/lug'at, analysis, boshqa). Gap matni hisobotga yozilmaydi — faqat ID.
3. FLORES umuman: 1–2-banddagi joylarda FLORES-200 dev (997) va devtest (1 012) uzn_Latn gaplaridan nechtasi
   (aniq + yaqin) bor — TOLQIN-2 ga kirmaganlari ham; faqat son.

## Qaror qoidasi
- Prereg ustun: §2.1 (B-qavat KKT ekspozitsiyasi OCHIQ — cheklov), §2.2 va §4 (A-qavatda KKT uchun 78 so'z bo'yicha
  ekspozitsiyali/ekspozitsiyasiz gaplar alohida). Bu reja ularni o'zgartirmaydi, faqat to'ldiradi.
- Ekspozitsiyaga uchragan gap topilsa: asosiy tahlil prereg bo'yicha O'ZGARMAYDI; qo'shimcha ravishda shu gaplar
  chiqarilgan sezgirlik tahlili hisobot qilinadi; maqolada ularning soni va ID lari ko'rsatiladi.
- Natija `analysis/tolqin-2/ekspozitsiya_2.md`; skript bir marta yuriladi, natija commit.
