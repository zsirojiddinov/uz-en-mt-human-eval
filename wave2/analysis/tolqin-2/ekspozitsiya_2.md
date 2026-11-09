# EKSPOZITSIYA-2 — natija (2026-10-20)

Reja: `ekspozitsiya_2_reja.md` (commit `5d5f2a9`, natijadan oldin). Skript `ekspozitsiya_2.py`, to'liq natija `ekspozitsiya_2.json` (sha256 `a8dda687879bdd03076a96344de38a3cfa9f9fc32f82f1d3d929c9deafb130d6`). Faqat MANBA gaplar; tizim javoblari ochilmagan; gap matni yo'q — faqat ID.

Ijobiy nazorat: 472 nishonning har biri o'zini aniq topadi (472/472), tasodifiy nazorat gapi 0; git skanida eval72 72/72 topildi (skan ishlaydi).

## Xulosa
- **A-qavat (400, FLORES dev): ekspozitsiya 0** — nomlangan to'plamlar, ishchi daraxtlar, git tarixi, commit xabarlari: aniq 0, yaqin 0.
- **eval72 (72): hammasi repoda bor** (prereg §2.1 dagi OCHIQ ekspozitsiya tasdiqlanadi). KKT ishlab chiqish populyatsiyalarida (2 119 / 2 477 / 2 597 / 3 301) faqat train 24 + gold 12 = **36** (FLORES 36 ning birortasi YO'Q); FLORES 36 faqat evaluation/analysis natija fayllarida.

## 1. Gap to'plamlari bilan kesishma

| to'plam | element | aniq | yaqin | A-qavat | eval72 (flores/train/gold) |
|---|---|---|---|---|---|
| 2119 (echo1_skan.json) | 2119 | 36 | 0 | 0 | 0/24/12 |
| 2477 vaqt (merge-1008/surat.py gaplar(): 2119+58+300; icite-2026 imlo_radius normallashtir_ms) | 2477 | 36 | 0 | 0 | 0/24/12 |
| 2597 (triaj-1/db-sifat-1 populyatsiyasi: 2477 + sinov-4 120) | 2597 | 36 | 0 | 0 | 0/24/12 |
| 3301 imlo darvozasi (imlo-2/surat.py kirishlar()) | 3301 | 36 | 0 | 0 | 0/24/12 |
| SINOV-4 (sinov-4/toplam.jsonl) | 120 | 0 | 0 | 0 | 0/0/0 |
| SINOV-5 (sinov-5/toplam.jsonl) | 120 | 0 | 0 | 0 | 0/0/0 |
| SINOV-6 (gaplar yig'ilmagan: MANIFEST.json, README.md, yigish.py) | 0 | 0 | 0 | 0 | 0/0/0 |
| SINOV-7 (gaplar yig'ilmagan: MANIFEST.json, README.md, yigish.py) | 0 | 0 | 0 | 0 | 0/0/0 |

- 2 119, 2 477, 2 597, 3 301 dagi 36 ID (to'rtalasida bir xil): gold-00, gold-01, gold-02, gold-03, gold-04, gold-05, gold-06, gold-07, gold-08, gold-09, gold-10, gold-11, train-00, train-01, train-02, train-03, train-04, train-05, train-06, train-07, train-08, train-09, train-10, train-11, train-12, train-13, train-14, train-15, train-16, train-17, train-18, train-19, train-20, train-21, train-22, train-23.
- 2 597 joyi: `analysis/triaj-1/report.md` §3 — populyatsiya 2 119 · 58 · sinov 300 · sinov-4 120 (db-sifat-1 `radius.gaplar()` dan sinov-5 siz) = `merge-1008/surat.py gaplar()` (2 477) + `sinov-4/toplam.jsonl`. 2 477 «vaqt» = `merge-1008/surat.py gaplar()` (`icite-2026/imlo_radius.py` `normallashtir_ms`). 3 301 = `imlo-2/surat.py kirishlar()`.
- SINOV-6, SINOV-7: gaplar hali yig'ilmagan (papkada faqat MANIFEST.json, README.md, yigish.py).
- Barcha boshqa fayllar (ishchi daraxtlar: main + 20 worktree/qo'shimcha; 105694 matnli fayl, 9722 noyob mazmun): topilgan fayl 520; A-qavat 0; eval72 aniq 72, faqat yaqin 0.

## 2. Kod/data tarixi (git, barcha branchlar)
- Ko'rilgan: 16011 nomzod obyekt (rev-list --all --objects, matnli), topilgan blob 538; commit xabarlari 1645 — topilgan **0**.
- A-qavat: **0**. eval72: 72/72.
- eval72 gold (12): birinchi commit `5a7c272` 2026-06-02 (`oltin_korpus.json`).
- eval72 train (24): birinchi commit `17ee420` 2026-06-10 (`corpus/uz_en_scitech.train.json`).
- eval72 flores (36): birinchi commit `1a4a11f` 2026-06-16 (`evaluation/results/blind_diagnoz.json`).
- Toifalar bo'yicha (8+ so'zli bo'lak yoki to'liq gap):
  - data/rules: `data/rules/clause_connectors_t5.json` — birinchi `2424d18` 2026-06-12; aniq —; yaqin train-18
  - data/rules: `data/rules/articles_t2.json` — birinchi `5e5524f` 2026-06-12; aniq gold-02; yaqin —
  - database: `database/echo_batch1_TASDIQ_korib_chiqilgan.csv` — birinchi `b269281` 2026-08-10; aniq —; yaqin train-23
  - test fixture: `analysis/lex-kontekst-1/test_asos.json` — birinchi `9c7d77e` 2026-10-15; aniq train-05, train-11; yaqin —
  - test fixture: `analysis/bolak-1/test_asos.json` — birinchi `5da78fc` 2026-10-16; aniq train-06, train-13, train-18; yaqin —
  - `tests/` papkasi: 0. Qolgan topilmalar analysis/ (72), evaluation/ (72), corpus/ (train 24: `corpus/uz_en_scitech.train.json` 17ee420 2026-06-10), ildizdagi `oltin_korpus*.json` (gold 12, 5a7c272 2026-06-02).

## 3. FLORES umuman (1–2-banddagi joylarda)
- FLORES-200 uzn_Latn (dev 997 + devtest 1 012) dan: aniq **679** (dev 50, devtest 629), faqat yaqin 5.
- Joy bo'yicha: ishchi daraxtlar aniq 679 / yaqin 5; git blob'lar aniq 679 / yaqin 5; commit xabarlari 0.
- dev 50 = YOQISH-2 `analysis/yoqish-2/held_out.json` (shu faylda dev aniq 50; A-qavatdan oldindan chiqarilgan). Nomlangan to'plamlarda FLORES 0.

## Qaror qoidasi qo'llanishi (reja)
- Prereg ustun; asosiy tahlil O'ZGARMAYDI.
- A-qavat: ekspozitsiya 0 — sezgirlik tahlili kerak emas (prereg §4 dagi 78 so'zli KKT ajratmasi o'z holicha qoladi).
- B-qavat: so'zma-so'z ta'rifda 72/72 uchragan — chiqarilgandan keyin gap qolmaydi. Qo'shimcha sezgirlik uchun ajratish: KKT ishlab chiqish populyatsiyalarida uchragan 36 (train 24 + gold 12) va faqat natija fayllarida uchragan FLORES 36. Maqolada son va ID lar (yuqorida) ko'rsatiladi.

## Cheklovlar
- SQLite `.db` va boshqa binar fayllar (xlsx/docx/pptx dan tashqari) skanerlanmadi; repo tashqarisidagi papkalar (~/baho_*, Desktop) skanerlanmadi.
- `ekspozitsiya_2.json` dagi `toifa` evristikasi yo'l nomiga qaraydi (masalan, `analysis/lugat_shift_output/` «data/lug'at» deb belgilangan) — yuqoridagi ro'yxat yo'l bo'yicha qo'lda aniqlangan.

## Yakun (2026-10-20, tuzatish 4 bilan)
- Qayta yurish (commit qilingan `ekspozitsiya_2.py`, 3e0ae5d): bayt-aynan EMAS — farq faqat ikki sanoqda:
  `git.blob_korildi` 16 011 -> 16 032 va `git.commit_xabar_korildi` 1 645 -> 1 646 (orada 3e0ae5d commitining o'zi
  qo'shildi). Barcha topilmalar (ID, fayl, birinchi commit, FLORES) aynan. Commitdagi `ekspozitsiya_2.json` saqlandi.
- SQLite (`ekspozitsiya_2_db.py`, `ekspozitsiya_2_db.json`): 21 noyob DB (production 732a97a5 + zaxiralar + worktree
  DB lari + ~/kkt_db_zaxira_20260817.db), nusxadan `immutable` o'qish, barcha TEXT qiymatlar — A-qavat 0, eval72 0
  (aniq va yaqin). Ijobiy nazorat: DB dan olingan 5 qiymat 5/5 topildi.
- ~/baho_claude (34 fayl): A 0; eval72 yaqin 2 (train-14, train-20; `lex3_dev.md`). ~/baho_gemini (6), ~/baho_gpt (9): 0.
- c9639e1 ajdodi: 5e5524f, 2424d18, b269281 — HA (fayllar c9639e1 da mos bo'lak bilan bor); 9c7d77e, 5da78fc — YO'Q.
