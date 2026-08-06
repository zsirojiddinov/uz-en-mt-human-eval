# RW1 — INSON-BAHOLASH PRE-REGISTRATSIYA & TAHLIL-REJASI

**Maqsad:** KKT-RS metrikasi (v1/v2) va boshqa avtomatik metrikalarning inson-bahosi bilan
korrelyatsiyasini o'lchash. Bu hujjat **inson-data yig'ilmasidan OLDIN** qulflanadi (halollik
protokoli §1 ruhi: qaror data'ni ko'rmasdan). Har band SANASI bilan; band qo'shilgach
o'zgartirilmaydi.

**Muzlatilgan asos:** `git tag metric-freeze-v1v2` (2026-07-02) — h2_metric v1(manba-anker) +
v2(referens-anker, modal-fix) ta'riflari inson-data tahlili tugaguncha o'zgartirilmaydi.

---

## Qulflangan qarorlar (sana bilan)

**[2026-07-02 · MV1/MV2 · commit `1a1c154`/`b37a4da`]**
- **Asosiy gipoteza-metrikasi = KKT-RS v2** (referens-anker, sinonim-tolerant). **v1 = ablation**.
  Ikkala versiya inson-data bilan skorlanadi (`ce2_score.py` / `metric_scores.json` da v1 ham v2 ham bor).
- Solishtiriladigan avtomatik metrikalar: sentence-BLEU (exp-smoothing), chrF, KKT-RS-v1, KKT-RS-v2.

**[2026-07-02 · RW1 · commit `b37a4da`]**
- **216 item** = 72 gap (LOCK, `sentences.json`) × 3 tizim (s1/s2/gemini). BITTA global blind
  aralashtirish, **seed=216**, bir xil tartib har uch baholovchiga (`rater_A/B/C.xlsx`).
- Har item ikki o'lchov: **Mazmun (adequacy) 1-5** va **Ravonlik (fluency) 1-5**.
- Blind: baholovchi tizimni ko'rmaydi; `blind_key.json` (item_id→gap/tizim) MAXFIY.
- Korrelyatsiya inson-ball vs `metric_scores.json` (blind_key orqali) bo'yicha hisoblanadi.
- Pilot (`pilot.xlsx`, 18 item, LOCK'dan tashqari 6 gap) — jarayon-sinovi; ballari asosiy
  tahlilga KIRMAYDI.

---

## Baholovchilararo ishonchlilik va sensitivity (yangi band)

**[2026-07-03]**
> **Baholovchi-chetlashtirish sensitivity qoidasi (adequacy):** Agar BITTA baholovchining
> boshqa baholovchilar bilan **o'rtacha juftlik-Spearman'i (adequacy bo'yicha) < 0.40** bo'lsa-yu
> **qolgan juftlik-Spearman'lar ≥ 0.60** bo'lsa, u holda:
> - **Asosiy natija — UCHALA baholovchi bilan** (chetlashtirishsiz) hisoblanadi va beriladi;
> - **QO'SHIMCHA sensitivity-tahlil — o'sha bitta baholovchisiz** hisoblanadi;
> - **IKKALASI ham hisobotda** ochiq ko'rsatiladi.
> - **Vaznlash (weighting) QILINMAYDI** — baholovchilar teng, faqat to'liq-to'plam va
>   chetlashtirilgan-to'plam ikki variantda taqqoslanadi.
>
> *Izoh:* "o'rtacha juftlik-Spearman" = o'sha baholovchining qolgan har bir baholovchi bilan
> item-daraja adequacy-ballari Spearman korrelyatsiyalarining o'rtachasi. Shart faqat bitta
> baholovchi past + qolganlar mustahkam bo'lganda ishlaydi (bittalik chetki holat); ikkidan
> ortiq past bo'lsa bu band qo'llanmaydi (alohida qaror talab qilinadi, data'dan oldin
> belgilanmagan → o'sha holatda YANGI pre-registratsiya bandi kerak).

---

## Tahlil-skripti muzlatilishi (yangi band)

**[2026-07-03]** Tahlil-skripti (`evaluation/eval72/analyze_human_eval.py`, commit **`973eb09`**)
inson-datadan OLDIN qurildi, dry-run bilan sinaldi (SYNTHETIC mexanika-sinovi PASS 8/8) va
**MUZLATILDI**. Data kelgach skript FAQAT ishga tushiriladi (`python evaluation/eval72/
analyze_human_eval.py`); tahlil-mantig'iga har qanday o'zgartirish inson-datani ko'rmasdan
qo'yiladigan YANGI SANALI band talab qiladi (halollik §1 held-out ruhi). Skript uch bosqichni
(ingest+validatsiya / kelishuv+outlier-band / korrelyatsiya+bootstrap) yuqoridagi qulflangan
qarorlar bo'yicha bajaradi. Dry-run tafsiloti: `analysis/an1_pipeline_report.md`.

---

## Amalga oshirish (data kelgach)

1. `rater_A/B/C.xlsx` "Baholash" varaqlaridan (item_id, Mazmun, Ravonlik) o'qiladi.
2. Juftlik-Spearman (adequacy) matritsasi (A-B, A-C, B-C) + har baholovchining o'rtachasi.
3. Yuqoridagi band shartiga ko'ra: asosiy (3 baholovchi) + kerak bo'lsa sensitivity (chetlashgan).
4. Inson-ball (o'rtacha) vs metric_scores (BLEU/chrF/KKT-v1/KKT-v2) — Spearman/Pearson,
   jami + per-qatlam, v2 asosiy / v1 ablation.

**Bu hujjatdan keyin (2026-07-03) inson-data kelgunicha yangi tahlil-qarori BELGILANMAYDI;
belgilansa — yangi sanali band sifatida, data'ni ko'rmasdan.**

---

## Sanali tuzatish 2026-07-07 — javob-muddati va stopping-qoida (KO'R holatda)

Holat: rater_C_filled.xlsx qabul qilingan (2026-07-06), TAHLIL QILINMAGAN
(faqat to'liqlik-tekshiruvi blind holatda). Rater A va B fayllari kutilmoqda.
Ushbu band hech qanday baholovchi-natijaga qaralmasdan kiritildi.

Qoida:
1. Rater A va B fayllari 2026-07-14 23:59 (Toshkent) gacha kutiladi.
2. Muddatgacha UCHALA fayl kelsa — asosiy tahlil asl reja bo'yicha (3 rater).
3. Muddatgacha IKKITA fayl bo'lsa — asosiy tahlil shu ikkitasi bilan yuritiladi
   va yakuniy hisoblanadi; uchinchisining yo'qligi hisobotda ochiq qayd etiladi;
   u keyin kelsa — faqat sensitivity-ilova sifatida.
4. Muddatgacha faqat rater C bo'lsa — muddat BIR marta 2026-07-21 gacha
   uzaytiriladi. Shunda ham yolg'iz qolsa — konfirmator da'vo qilinmaydi:
   tahlil tavsifiy/eksplorator maqomida beriladi.
5. analyze_human_eval.py asosiy rejimda BIR marta yuritiladi.

---

## Sanali tuzatish 2026-07-11 — A-rol baholovchisi (KO'R holatda)
Dastlab A-rol uchun mo'ljallangan mutaxassis oilaviy vaziyat (tug'ruq, statsionar)
tufayli ishtirok eta olmadi. A-rol talabiga (ingliz tili o'qituvchisi) to'liq javob
beradigan boshqa mustaqil mutaxassis (ingliz tili o'qituvchisi, IELTS 7.0) jalb
qilindi va B-shablon tartibidagi faylni QISMAN (~60-70%) to'ldirib topshirdi.
Ushbu band kiritilgan paytda uning ballari ko'rilmagan. Qoidalar:
1) Asosiy konfirmator-tahlil 2026-07-07 stopping-qoidasi bo'yicha TO'LIQ ikki
   fayl (B+C) bilan bajariladi va yakuniy hisoblanadi.
2) A-qisman fayl returns/ ga QO'YILMAYDI; u
   evaluation/eval72/supplementary/rater_A_partial.xlsx sifatida saqlanadi.
3) A bo'yicha oldindan belgilangan QO'SHIMCHA-tahlil o'tkaziladi (faqat
   to'ldirilgan itemlar kesimida: A-B va A-C juft kelishuvlari hamda A
   qo'shilganda asosiy korrelyatsiyalarning o'zgarishi) va natija-maqolada
   asosiy tahlildan aniq ajratib beriladi.

---

## Sanali tuzatish 2026-07-11 — asosiy tahlilni erta ishga tushirish (KO'R)
Dastlabki A-mutaxassisning muddatgacha (2026-07-14) fayl topshira olmasligi
2026-07-11 da tashqi sabab bilan uzil-kesil ma'lum bo'ldi; bu hech qanday
baholash-ma'lumotiga asoslanmagan fakt. Stopping-qoidaning yagona ochiq
noaniqligi shu tarzda hal bo'lgani uchun asosiy tahlil (qoidaning "ikkita
to'liq fayl" bandi bo'yicha, B+C bilan, yakuniy maqomda) 2026-07-15 o'rniga
2026-07-11 da bajariladi. Keyin keladigan har qanday fayl — faqat
sensitivity-ilova.
