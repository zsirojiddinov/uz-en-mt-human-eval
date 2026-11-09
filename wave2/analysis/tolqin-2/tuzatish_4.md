# Tuzatish 4 (ekspozitsiya natijasidan keyin, tizim ballaridan oldin)
Sana: 2026-10-20. Asos: EKSPOZITSIYA-2 (reja `ekspozitsiya_2_reja.md`, 5d5f2a9; natija `ekspozitsiya_2.md`,
`ekspozitsiya_2.json`, `ekspozitsiya_2_db.json`). Bu tuzatish tizim javoblari ochilmasdan va ball hisoblanmasdan
oldin yozildi.

a) Oldindan ko'rilmagan to'plam bo'yicha barcha da'volar faqat A-qavatga (FLORES dev 400) tayanadi. A-qavat
   ekspozitsiyasi 0: gap to'plamlari (2 119, 2 477, 2 597, 3 301, SINOV-4/5), ishchi daraxtlar, git tarixi
   (barcha branchlar), commit xabarlari, barcha SQLite DB (production 732a97a5 bilan birga, 21 noyob) va
   ~/baho_* — aniq 0, yaqin 0.

b) B (eval72) prereg §2.1 bo'yicha ochiq qatlam. Reja qoidasidagi chiqarib tashlash B ga qo'llanmaydi (aks holda
   72/72 chiqib ketadi). B o'zining 1-to'lqindan beri mavjud manba qatlamlari bo'yicha FAQAT tavsifiy hisobot
   qilinadi:
   - B-KKT = train 24 + gold 12 (ishlab chiqish to'plamlarida bor: 2 119 / 2 477 / 2 597 / 3 301);
   - B-FLORES = 36 (2026-06-16 dan, 1a4a11f, faqat baholash/diagnostika fayllarida; ishlab chiqish
     to'plamlarida 0).

c) Eksplorativ: KKT ning A va B-FLORES dagi farqi — baholash natijalarini ko'rib tuzatish ta'sirining taxmini
   (manba bir xil: FLORES dev va devtest). Tasdiqlovchi test emas.

d) Rule data fayllaridagi topilmalar: `data/rules/articles_t2.json` — gold-02 aniq (5e5524f, 2026-06-12);
   `data/rules/clause_connectors_t5.json` — train-18 yaqin (2424d18, 2026-06-12);
   `database/echo_batch1_TASDIQ_korib_chiqilgan.csv` — train-23 yaqin (b269281, 2026-08-10). Uchala commit
   c9639e1 (muzlatilgan KKT chiqishi) ning AJDODI va uchala fayl c9639e1 daraxtida o'sha mos bo'lak bilan bor;
   c9639e1 kodida `articles_t2.json` faqat izohda («A8 misollaridan»), qolgan ikkisining nomi services/app da
   uchramaydi. Test fixture'lar `analysis/lex-kontekst-1/test_asos.json` (9c7d77e) va
   `analysis/bolak-1/test_asos.json` (5da78fc) c9639e1 ning ajdodi EMAS — muzlatilgan chiqishga ta'sir qilmagan.
   3-band (FLORES umuman): repoda FLORES-200 uzn_Latn dan aniq 679 (dev 50 = YOQISH-2 held_out, devtest 629),
   yaqin 5.

e) Cheklov: A-qavat KKT ishlab chiqishiga nisbatan yopiq, lekin FLORES 2022 dan ochiq. Gemini, Claude, GPT va GT
   uni o'qitish jarayonida ko'rgan bo'lishi mumkin — bu ularning foydasiga, KKT ga qarshi siljish.
