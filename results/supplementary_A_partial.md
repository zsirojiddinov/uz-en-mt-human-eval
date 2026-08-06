# RW1 — A-QISMAN SUPPLEMENTARY TAHLIL

> **POST-HOC QO'SHIMCHA, asosiy tahlilga kirmaydi.** Asosiy konfirmator natija —
> `results/human_eval_results.md` (B+C, 216 item). Bu hujjat pre-reg 2026-07-11
> A-bandi bo'yicha faqat A to'ldirgan itemlar kesimidagi qo'shimcha tahlil.

**Kesim:** A to'liq to'ldirgan 127 item (216 dan). Qatlam: {'flores': 66, 'gold': 18, 'train': 43}. Tizim: {'gemini': 43, 's2': 43, 's1': 41}.

**Sifat-qayd:** A faylida ravonlik ustuni 127/127 itemda mazmun bilan AYNAN bir xil — A ning ravonlik-bahosi mustaqil signal emas (bitta umumiy ball berilgan ko'rinadi). Ravonlik-kelishuvlari shu ogohlantirish bilan o'qilsin.

## (a) Juft kelishuvlar (Spearman, shu kesimda)

| Juftlik | Mazmun | Ravonlik |
|---|---|---|
| A-B | 0.571 | 0.497 |
| A-C | 0.861 | 0.869 |
| B-C (shu kesim) | 0.501 | 0.492 |

## (b) Metrika-korrelyatsiyalar (inson-Mazmun o'rtachasi ↔ metrika, Spearman)

| Metrika | Asosiy B+C (n=216) | B+C (kesim, n=127) | A+B+C (kesim, n=127) | Δ(A qo'shilgani) |
|---|---|---|---|---|
| BLEU | 0.766 | 0.804 | 0.823 | +0.019 |
| chrF | 0.698 | 0.761 | 0.767 | +0.006 |
| KKT-RS-v1 | 0.223 | 0.274 | 0.28 | +0.006 |
| KKT-RS-v2 | 0.569 | 0.601 | 0.608 | +0.007 |

Δ = shu kesimda A ni qo'shish korrelyatsiyani qancha o'zgartirgani (faqat ma'lumot uchun; 
bootstrap-CI hisoblanmagan, konfirmator maqomi YO'Q).
