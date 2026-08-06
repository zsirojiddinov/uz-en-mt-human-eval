# -*- coding: utf-8 -*-
"""RW1 — baholovchi-jadvallar + blind-kalit + metric_scores (216 item = 72 gap × 3 tizim).

- metric_scores.json: har item uchun sentence-BLEU(smoothed)+chrF+KKT-RS-v1+v2.
- blind_key.json: item_id(tasodifiy kod) -> (gap_id, tizim). ALOHIDA — baholovchilarga BERILMAYDI.
- rater_A/B/C.xlsx: 1-varaq yo'riqnoma, 2-varaq baholash (item_id|uz|en|Mazmun|Ravonlik),
  data-validation 1-5. BITTA global aralashtirish (seed hujjatlangan), bir xil tartib hammaga.

Ishlatish: python evaluation/eval72/build_rw1.py
"""
import json, os, sys, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
from dotenv import load_dotenv; load_dotenv()
import sacrebleu
from app import create_app
from services.sentence_translator_v2 import sentence_translator_v2 as ST, split_clauses
import analysis.h2_metric as H2
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font, Alignment, PatternFill

SHUFFLE_SEED = 216
rows = json.load(open(os.path.join(HERE, 'sentences.json'), encoding='utf-8'))
OUTS = {n: {k: v for k, v in json.load(open(os.path.join(HERE, f))).items() if k != '_meta'}
        for n, f in [('s1', 's1_outputs.json'), ('s2', 's2_outputs.json'), ('gemini', 's3_gemini_outputs.json')]}

INSTRUCTIONS = [
    ("INSON BAHOLASH YO'RIQNOMASI (RW1)", True),
    ("", False),
    ("Siz o'zbekcha gaplarning inglizcha tarjimalarini baholaysiz. Har tarjima uchun IKKI ball bering:", False),
    ("", False),
    ("1) MAZMUN (adekvatlik) — 1..5: inglizcha tarjima o'zbekcha gapning MA'NOSINI qanchalik to'liq yetkazadi?", False),
    ("     5 = to'liq ma'no, hech narsa yo'qolmagan/qo'shilmagan", False),
    ("     4 = ma'no asosan to'liq, kichik noaniqlik", False),
    ("     3 = asosiy ma'no bor, lekin muhim qism yo'qolgan/noto'g'ri", False),
    ("     2 = ma'noning kichik qismigina yetkazilgan", False),
    ("     1 = ma'no umuman yetkazilmagan / noto'g'ri", False),
    ("", False),
    ("2) RAVONLIK (tabiiylik) — 1..5: tarjima INGLIZ TILIDA qanchalik tabiiy va grammatik?", False),
    ("     (o'zbekcha ma'noga QARAMASDAN, faqat inglizchaning o'zi sifatida)", False),
    ("     5 = mukammal, ona tili darajasida ravon", False),
    ("     4 = ravon, kichik xato", False),
    ("     3 = tushunarli, lekin g'aliz/grammatik xatolar bor", False),
    ("     2 = qiyin tushuniladi, ko'p xato", False),
    ("     1 = tushunib bo'lmaydi / grammatik buzuq", False),
    ("", False),
    ("MISOLLAR (o'zbekcha -> inglizcha, Mazmun/Ravonlik):", False),
    ("  'Mutaxassis modelni o'rgatdi' -> 'The specialist trained the model'  =>  Mazmun 5 / Ravonlik 5", False),
    ("  'Mutaxassis modelni o'rgatdi' -> 'The specialist taught the model'   =>  Mazmun 4 / Ravonlik 5  (o'rgat=train, teach yaqin)", False),
    ("  'Til tabiiy ham bo'lishi mumkin' -> 'Language natural being possible' =>  Mazmun 3 / Ravonlik 2  (ma'no qisman, grammatik buzuq)", False),
    ("", False),
    ("QOIDALAR:", False),
    ("  - Har QATORNI mustaqil baholang (qaysi tizim ekanini bilmaysiz — bu ataylab).", False),
    ("  - Ikkala ustunni ham to'ldiring (Mazmun va Ravonlik), 1..5 butun son.", False),
    ("  - Tartibni O'ZGARTIRMANG, qatorlarni o'chirmang.", False),
    ("  - Ikkilanib qolsangiz — o'rta ball (3) bering, izoh shart emas.", False),
    ("", False),
    ("Eslatma: bu yo'riqnoma protokol §6 sxemasi (Mazmun/Ravonlik 1-5) asosida tuzilgan.", False),
]


def build_sheet(path, items, title):
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Yo'riqnoma"
    for r, (txt, bold) in enumerate(INSTRUCTIONS, 1):
        c = ws1.cell(row=r, column=1, value=txt)
        c.font = Font(bold=bold, size=13 if bold else 11)
        c.alignment = Alignment(wrap_text=True, vertical='top')
    ws1.column_dimensions['A'].width = 110
    ws2 = wb.create_sheet("Baholash")
    hdr = ['item_id', "O'zbekcha gap", 'Inglizcha tarjima', 'Mazmun (1-5)', 'Ravonlik (1-5)']
    fill = PatternFill('solid', fgColor='DDDDDD')
    for c, h in enumerate(hdr, 1):
        cell = ws2.cell(row=1, column=c, value=h)
        cell.font = Font(bold=True); cell.fill = fill
    for r, it in enumerate(items, 2):
        ws2.cell(row=r, column=1, value=it['item_id'])
        ws2.cell(row=r, column=2, value=it['uz']).alignment = Alignment(wrap_text=True)
        ws2.cell(row=r, column=3, value=it['hyp']).alignment = Alignment(wrap_text=True)
    dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True)
    dv.error = "1 dan 5 gacha butun son kiriting"; dv.errorTitle = "Noto'g'ri ball"
    ws2.add_data_validation(dv)
    dv.add(f"D2:E{len(items)+1}")
    ws2.column_dimensions['A'].width = 14
    ws2.column_dimensions['B'].width = 55
    ws2.column_dimensions['C'].width = 55
    ws2.column_dimensions['D'].width = 13
    ws2.column_dimensions['E'].width = 14
    ws2.freeze_panes = 'A2'
    wb.save(path)


def main():
    app = create_app()
    ref = {r['id']: r['ref_en'] for r in rows}
    uz = {r['id']: r['uz'] for r in rows}
    layer = {r['id']: r['layer'] for r in rows}

    # --- metric_scores (216) ---
    metric = {}
    with app.app_context():
        for r in rows:
            se, pe, vo = H2.source_subject_predicate(r['uz'], ST, split_clauses)
            for sysn, d in OUTS.items():
                hyp = d.get(r['id'], '')
                v2 = H2.score_sentence(r['uz'], hyp, r['ref_en'], se, pe, vo, v2=True)
                v1 = H2.score_sentence(r['uz'], hyp, r['ref_en'], se, pe, vo, v2=False)
                metric[f"{r['id']}::{sysn}"] = {
                    'gap_id': r['id'], 'system': sysn, 'layer': layer[r['id']],
                    'bleu': round(sacrebleu.sentence_bleu(hyp, [r['ref_en']], smooth_method='exp').score, 3),
                    'chrf': round(sacrebleu.sentence_chrf(hyp, [r['ref_en']]).score, 3),
                    'kkt_rs_v1': v1['kkt_rs'], 'kkt_rs_v2': v2['kkt_rs']}
    json.dump(metric, open(os.path.join(HERE, 'metric_scores.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # --- blind shuffle (216) — bitta global tartib ---
    pairs = [(r['id'], s) for r in rows for s in ('s1', 's2', 'gemini')]
    rng = random.Random(SHUFFLE_SEED)
    rng.shuffle(pairs)
    blind_key = {}
    items = []
    for k, (gid, sysn) in enumerate(pairs):
        iid = f"IT{k:03d}"
        blind_key[iid] = {'gap_id': gid, 'system': sysn}
        items.append({'item_id': iid, 'uz': uz[gid], 'hyp': OUTS[sysn].get(gid, '')})
    json.dump(blind_key, open(os.path.join(HERE, 'blind_key.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    for rater in ('A', 'B', 'C'):
        build_sheet(os.path.join(HERE, f'rater_{rater}.xlsx'), items, f'RW1 rater {rater}')

    print(f"metric_scores.json: {len(metric)} item")
    print(f"blind_key.json: {len(blind_key)} item (seed={SHUFFLE_SEED}) — MAXFIY, baholovchilarga BERILMAYDI")
    print(f"rater_A/B/C.xlsx: {len(items)} qator (bir xil blind tartib)")


if __name__ == '__main__':
    main()
