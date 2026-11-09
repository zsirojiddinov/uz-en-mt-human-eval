# -*- coding: utf-8 -*-
"""TOLQIN-2 — qaytgan fayllarni qabul qilish (prereg §3 (7); tuzatish 6). MUZLATILADI. Matn ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/qabul.py tarjimon T1|T2 FAYL.xlsx [--almashtir]
    python3 analysis/tolqin-2/qabul.py baho B|C|D|E FAYL.xlsx [--almashtir]

Kirish fayli nomi har qanday. Xom fayl qaytgan/xom/<X>__<asl nom> ga bayt-aynan nusxalanadi (sha256, mtime qayd).
Chiqish: qaytgan/TX.xlsx yoki qaytgan/baho_X.xlsx — tahlil.py formatida. Chiqish allaqachon bo'lsa — TO'XTAYDI;
--almashtir (prereg §4: bir marta to'ldirishga qaytarilgan fayl) eski chiqishni qaytgan/arxiv/ ga ko'chiradi.
Jurnal: qaytgan/qabul_jurnal.csv (vaqt, tur, X, kelgan nom, mtime, xom/chiqish sha256, holat, o'zgarishlar JSON) — matnsiz.

TARJIMON: «Tarjima» varag'i (№ | Manba | Tarjima), 72 qator; № -> paket/kalit_tarjimon.json. Tekshiruv: Manba NFC dan
keyin asl (evaluation/eval72/sentences.json) bilan aynan; Tarjima 72/72 to'ldirilgan (normallashtirishdan keyin).
Normallashtirish FAQAT «Tarjima» da: NFC; tipografik qo'shtirnoq “ ” „ ‟ « » -> "; tipografik apostrof ‘ ’ ‚ ‛ -> ';
NBSP (U+00A0, U+202F, U+2007) -> bo'shliq; bosh/oxir bo'shliqlar. Chiqishda Manba = asl matn (kalit bo'yicha).
Deklaratsiya varag'i: to'ldirilgan maydonlar soni va «Roziman» qiymati (ha/yo'q/bo'sh) jurnalga; ism yozilmaydi.
BAHO: «Baholash» varag'i (Element | O'zbekcha gap | Inglizcha tarjima | Mazmun (1-5) | Ravonlik (1-5)), 360 qator;
Element to'plami paket/kalit_baho.json bilan aynan; matn ustunlari paketdagi bilan solishtiriladi (farq soni).
Baholar O'ZGARTIRILMAYDI; qator tartibi saqlanadi (darvoza (c) uchun). Chiqish: Element | Adequacy | Fluency.
Darvozalar (prereg §2.5 (a)–(e), kalitsiz) tahlil.darvoza bilan hisoblanib jurnalga yoziladi.
"""
import csv
import hashlib
import io
import json
import shutil
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
QAYTGAN = SIKL / 'qaytgan'
EVAL72 = REPO / 'evaluation/eval72/sentences.json'
QOSH = dict.fromkeys(map(ord, '“”„‟«»'), '"')
APOS = dict.fromkeys(map(ord, '‘’‚‛'), "'")
NBSP = dict.fromkeys(map(ord, '   '), ' ')
BAHO_SAR = ('Element', "O'zbekcha gap", 'Inglizcha tarjima', 'Mazmun (1-5)', 'Ravonlik (1-5)')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def normal(s, son):
    s0 = '' if s is None else str(s)
    s1 = unicodedata.normalize('NFC', s0)
    son['nfc'] += s1 != s0
    s2 = s1.translate(QOSH)
    son['qoshtirnoq'] += sum(a != b for a, b in zip(s1, s2))
    s3 = s2.translate(APOS)
    son['apostrof'] += sum(a != b for a, b in zip(s2, s3))
    s4 = s3.translate(NBSP)
    son['nbsp'] += sum(a != b for a, b in zip(s3, s4))
    s5 = s4.strip()
    son['bosh_oxir'] += s5 != s4
    return s5


def jurnal(qator):
    QAYTGAN.mkdir(exist_ok=True)
    p = QAYTGAN / 'qabul_jurnal.csv'
    yangi = not p.exists()
    with open(p, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        if yangi:
            w.writerow(['vaqt', 'tur', 'x', 'kelgan_nom', 'kelgan_mtime', 'xom_sha256', 'chiqish_sha256', 'holat', 'tafsilot'])
        w.writerow(qator)


def tarjimon(x, b):
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(b), data_only=True)
    if 'Tarjima' not in wb.sheetnames:
        return None, "«Tarjima» varag'i yo'q", {}
    q = [list(r[:3]) for r in wb['Tarjima'].iter_rows(values_only=True)]
    if [str(v).strip() if v is not None else '' for v in q[0]] != ['№', 'Manba', 'Tarjima']:
        return None, 'sarlavha № | Manba | Tarjima emas', {}
    q = [r for r in q[1:] if any(v not in (None, '') for v in r)]
    kalit = json.loads((SIKL / 'paket' / 'kalit_tarjimon.json').read_text(encoding='utf-8'))
    uz = {r['id']: r['uz'] for r in json.loads(EVAL72.read_text(encoding='utf-8'))}
    son = {'nfc': 0, 'qoshtirnoq': 0, 'apostrof': 0, 'nbsp': 0, 'bosh_oxir': 0}
    nomlar = [str(r[0]).strip() for r in q]
    if sorted(nomlar, key=lambda v: int(v) if v.isdigit() else 0) != [str(i) for i in range(1, 73)] or len(q) != 72:
        return None, f'№ 1..72 emas (qator {len(q)})', son
    mos_emas = [n for (n, m, _) in q if unicodedata.normalize('NFC', str(m or '')).strip()
                != unicodedata.normalize('NFC', uz[kalit['qator'][str(n).strip()]['id']]).strip()]
    if mos_emas:
        return None, f'Manba asl bilan mos emas: {len(mos_emas)} qator (№ {", ".join(map(str, mos_emas[:10]))})', son
    tar = {str(n).strip(): normal(t, son) for n, _, t in q}
    bosh = [n for n, t in tar.items() if not t and (x, n) not in {('T1', '55')}]   # tuzatish 10 (a): T1 № 55
    if bosh:
        return None, f'Tarjima bo\'sh: {len(bosh)} qator (№ {", ".join(bosh[:10])})', son
    dek = {}
    if 'Deklaratsiya' in wb.sheetnames:
        d = {str(r[0]).strip(): r[1] for r in wb['Deklaratsiya'].iter_rows(min_row=2, values_only=True) if r and r[0]}
        dek = {'toldirilgan': sum(bool(str(d.get(k) or '').strip()) for k in ('Ism-familiya', 'Sarflangan vaqt (taxminan)',
                                                                          "Roziman (ha/yo'q)", 'Sana', 'Imzo')),
               'roziman': str(d.get("Roziman (ha/yo'q)") or '').strip().lower() or "bo'sh"}
    out = openpyxl.Workbook()
    ws = out.active
    ws.title = 'Tarjima'
    ws.append(['№', 'Manba', 'Tarjima'])
    for n in range(1, 73):
        ws.append([n, uz[kalit['qator'][str(n)]['id']], tar[str(n)]])
    buf = io.BytesIO()
    out.save(buf)
    return buf.getvalue(), 'OK', dict(son, deklaratsiya=dek)


def baho(x, b):
    import openpyxl
    import importlib.util
    wb = openpyxl.load_workbook(io.BytesIO(b), data_only=True)
    if 'Baholash' not in wb.sheetnames:
        return None, "«Baholash» varag'i yo'q", {}
    q = [list(r[:5]) for r in wb['Baholash'].iter_rows(values_only=True)]
    if tuple(str(v).strip() if v is not None else '' for v in q[0]) != BAHO_SAR:
        return None, 'sarlavha paketdagidek emas', {}
    q = [r for r in q[1:] if any(v not in (None, '') for v in r)]
    kb = json.loads((SIKL / 'paket' / 'kalit_baho.json').read_text(encoding='utf-8'))
    if [str(r[0]).strip() for r in q] and {str(r[0]).strip() for r in q} != set(kb['elementlar']):
        return None, f"Element to'plami kalit bilan mos emas (qator {len(q)})", {}
    pk = openpyxl.load_workbook(SIKL / 'paket' / 'baholovchi' / f'baho_{x}.xlsx', read_only=True)
    asl = {str(r[0]): (r[1], r[2]) for r in list(pk['Baholash'].iter_rows(values_only=True))[1:]}
    matn_farq = sum((r[1], r[2]) != asl.get(str(r[0]).strip()) for r in q)
    tartib_farq = sum(str(r[0]).strip() != e for r, e in zip(q, list(asl)))
    sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))
    T = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(T)
    rows = [[str(r[0]).strip(), r[3], r[4]] for r in q]
    dv = T.darvoza(rows, len(kb['elementlar']))
    out = openpyxl.Workbook()
    ws = out.active
    ws.title = 'Baholash'
    ws.append(['Element', 'Adequacy', 'Fluency'])
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    out.save(buf)
    return buf.getvalue(), 'OK', {'matn_ustun_farq': matn_farq, 'tartib_farq': tartib_farq, 'darvoza': dv}


def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if len(a) != 3 or a[0] not in ('tarjimon', 'baho') or \
            (a[0] == 'tarjimon' and a[1] not in ('T1', 'T2')) or (a[0] == 'baho' and a[1] not in ('B', 'C', 'D', 'E')):
        sys.exit(__doc__.split('\n\n')[1])
    tur, x, fayl = a[0], a[1], Path(a[2]).expanduser()
    nishon = QAYTGAN / (f'{x}.xlsx' if tur == 'tarjimon' else f'baho_{x}.xlsx')
    b = fayl.read_bytes()
    vaqt = datetime.now().astimezone().isoformat(timespec='seconds')
    mt = datetime.fromtimestamp(fayl.stat().st_mtime).astimezone().isoformat(timespec='seconds')
    if nishon.exists() and '--almashtir' not in sys.argv:
        jurnal([vaqt, tur, x, fayl.name, mt, sha(b), '', 'RAD: chiqish allaqachon bor (--almashtir yo\'q)', ''])
        sys.exit(f"TO'XTA: {nishon.name} allaqachon bor — qayta qabul faqat --almashtir bilan")
    chiq, holat, taf = (tarjimon if tur == 'tarjimon' else baho)(x, b)
    (QAYTGAN / 'xom').mkdir(parents=True, exist_ok=True)
    xom = QAYTGAN / 'xom' / f'{x}__{fayl.name}'
    k = 1
    while xom.exists() and xom.read_bytes() != b:
        xom = QAYTGAN / 'xom' / f'{x}__{k}__{fayl.name}'
        k += 1
    xom.write_bytes(b)
    if chiq is None:
        jurnal([vaqt, tur, x, fayl.name, mt, sha(b), '', f'RAD: {holat}', json.dumps(taf, ensure_ascii=False, default=str)])
        sys.exit(f'RAD: {holat}')
    if nishon.exists():
        (QAYTGAN / 'arxiv').mkdir(exist_ok=True)
        shutil.move(str(nishon), str(QAYTGAN / 'arxiv' / f'{nishon.stem}__{vaqt.replace(":", "")}.xlsx'))
    nishon.write_bytes(chiq)
    jurnal([vaqt, tur, x, fayl.name, mt, sha(b), sha(chiq), holat, json.dumps(taf, ensure_ascii=False, default=str)])
    print(f'{nishon.name}: {holat} · {json.dumps(taf, ensure_ascii=False, default=str)}')


if __name__ == '__main__':
    main()
