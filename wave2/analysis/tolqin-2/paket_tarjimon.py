# -*- coding: utf-8 -*-
"""TOLQIN-2 — tarjimon paketlari T1/T2 (prereg §2.4, tuzatish 5 band 1). Gap matni ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/paket_tarjimon.py            # paket/T1/, paket/T2/, paket/kalit_tarjimon.json
    python3 analysis/tolqin-2/paket_tarjimon.py --tekshir  # yozmaydi; qayta yasash bayt-aynan + qaytish tekshiruvi

To'plam: evaluation/eval72/sentences.json (72 gap, sha256 prereg §2.1); tartib random.Random(20261016).shuffle
(fayl tartibidan), ikkala tarjimonga bir xil. Paketda FAQAT o'zbekcha manba va № — qavat, ID, tizim chiqishi,
FLORES/mavjud inglizcha etalon YO'Q. Kalit (№ -> toplam, id) paket/kalit_tarjimon.json da, paketga kirmaydi.
Har paket: tarjima_TX.xlsx (1-varaq «Tarjima»: № | Manba | Tarjima [bo'sh]; 2-varaq «Deklaratsiya»; varaqlar parolsiz
himoyalangan — ochiq faqat «Tarjima» ustuni va Deklaratsiya qiymat katakchalari),
tarjima_TX.docx (jadval № | Manba | Tarjima [bo'sh] + deklaratsiya), YORIQNOMA.md. Qaytariladigan fayl — .xlsx
(qabul.py -> qaytgan/TX.xlsx). Fayllar deterministik (vaqt belgilari qat'iy) — qayta yasash bayt-aynan.
"""
import hashlib
import io
import json
import random
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
EVAL72 = REPO / 'evaluation/eval72/sentences.json'
E_SHA = '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
SEED = 20261016
PAKET = SIKL / 'paket'
QAT = datetime(2026, 10, 20, 0, 0, 0)
ZIPT = (2026, 10, 20, 0, 0, 0)
DEKL = 'Tarjimani o\'zim, mashina tarjimasi va LLM yordamisiz bajardim.'

YORIQNOMA = """# Tarjima bo'yicha yo'riqnoma ({x})

Sizga 72 ta o'zbekcha gap berilgan (`tarjima_{x}.xlsx`; xuddi shu gaplar o'qish/chop etish uchun
`tarjima_{x}.docx` da ham bor). Har bir gapni ingliz tiliga tarjima qiling.

## Qanday tarjima qilish
- Tarjima tabiiy, ravon va manbaga sodiq ingliz tilida bo'lsin. Bu tahrir (post-editing) emas — har gapni
  o'zingiz noldan tarjima qiling.
- Tarjimani `tarjima_{x}.xlsx` faylining «Tarjima» varag'idagi **Tarjima** ustuniga yozing — har gap o'z
  qatoriga.
- **№ raqamini saqlang.** Gap qo'shmang, gaplarni birlashtirmang va bo'lmang: bitta manba qatori — bitta
  tarjima qatori. Qatorlar tartibini o'zgartirmang, «№» va «Manba» ustunlarini tahrirlamang.
- 72 ta gapning hammasi tarjima qilinishi kerak (bo'sh qator qolmasin).

## Taqiqlar
- Tarjima nazorat ostida, bir o'tirishda bajariladi.
- Ishni **yakka** bajaring. Ikkinchi tarjimon bilan (yoki boshqa biror kishi bilan) gaplar va tarjimalarni
  muhokama qilmang.
- **Mashina tarjimasi** (Google Translate, Yandex, DeepL va h.k.), **LLM / sun'iy intellekt** (ChatGPT, Gemini,
  Claude, Copilot va h.k.) va boshqa **onlayn tarjimonlar TAQIQLANADI** — bitta so'z yoki ibora uchun ham.
- Lug'atdan (qog'oz yoki onlayn lug'at — so'z ma'nosini ko'rish uchun) foydalanish **mumkin**.

## Vaqt va deklaratsiya
- Tarjimaga sarflangan vaqtni taxminan yozing (soat/daqiqa) — «Deklaratsiya» varag'iga.
- Oxirida deklaratsiyani to'ldiring va imzolang (ism, sana, imzo):
  «{dekl}»

## Qaytarish
- To'ldirilgan `tarjima_{x}.xlsx` faylini (deklaratsiya varag'i bilan) qaytaring. Fayl nomini o'zgartirmang.
"""


def toplam():
    b = EVAL72.read_bytes()
    assert hashlib.sha256(b).hexdigest() == E_SHA, 'eval72 sha256'
    E = json.loads(b)
    assert len(E) == 72
    tartib = list(range(72))
    random.Random(SEED).shuffle(tartib)
    return E, tartib


def xlsx(x, E, tartib):
    import openpyxl
    from openpyxl.styles import Alignment, Font, Protection
    wb = openpyxl.Workbook()
    wb.properties.creator = 'TOLQIN-2'
    wb.properties.created = QAT
    wb.properties.modified = QAT
    ws = wb.active
    ws.title = 'Tarjima'
    ws.append(['№', 'Manba', 'Tarjima'])
    for c in ws[1]:
        c.font = Font(bold=True)
    for n, k in enumerate(tartib, 1):
        ws.append([n, E[k]['uz'], None])
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 80
    ws.column_dimensions['C'].width = 80
    for r in ws.iter_rows(min_row=2):
        for c in r[1:]:
            c.alignment = Alignment(wrap_text=True, vertical='top')
        r[2].protection = Protection(locked=False)       # faqat «Tarjima» ochiq
    ws.protection.sheet = True                           # parolsiz himoya: № va Manba tahrirlanmaydi
    d = wb.create_sheet('Deklaratsiya')
    for q in (['Maydon', 'Qiymat'], ['Tarjimon', x], ['Ism-familiya', None], ['Sarflangan vaqt (taxminan)', None],
              ['Deklaratsiya', DEKL], ['Roziman (ha/yo\'q)', None], ['Sana', None], ['Imzo', None]):
        d.append(q)
    for r in (3, 4, 6, 7, 8):                            # to'ldiriladigan katakchalar
        d.cell(r, 2).protection = Protection(locked=False)
    d.protection.sheet = True
    d.column_dimensions['A'].width = 30
    d.column_dimensions['B'].width = 70
    buf = io.BytesIO()
    wb.save(buf)
    return _qatiy_zip(buf.getvalue())


def _qatiy_zip(b):
    """zip ichidagi vaqt belgilarini qat'iylash (openpyxl joriy vaqtni yozadi)."""
    zi = zipfile.ZipFile(io.BytesIO(b))
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in zi.namelist():
            i = zipfile.ZipInfo(n, date_time=ZIPT)
            i.compress_type = zipfile.ZIP_DEFLATED
            i.external_attr = 0o644 << 16
            m = zi.read(n)
            if n == 'docProps/core.xml':                 # openpyxl saqlashda «modified» ni joriy vaqtga qo'yadi
                import re
                m = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', rb'\g<1>2026-10-20T00:00:00Z\g<2>', m)
            z.writestr(i, m)
    return out.getvalue()


W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def _p(t, qalin=False):
    r = '<w:rPr><w:b/></w:rPr>' if qalin else ''
    return f'<w:p><w:r>{r}<w:t xml:space="preserve">{escape(t)}</w:t></w:r></w:p>'


def _hujayra(t, en, qalin=False):
    return f'<w:tc><w:tcPr><w:tcW w:w="{en}" w:type="dxa"/></w:tcPr>{_p(t, qalin)}</w:tc>'


def docx(x, E, tartib):
    chegara = ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                      for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    qator = [f'<w:tr>{_hujayra("№", 600, True)}{_hujayra("Manba", 4400, True)}{_hujayra("Tarjima", 4400, True)}</w:tr>']
    qator += [f'<w:tr>{_hujayra(str(n), 600)}{_hujayra(E[k]["uz"], 4400)}{_hujayra("", 4400)}</w:tr>'
              for n, k in enumerate(tartib, 1)]
    jad = (f'<w:tbl><w:tblPr><w:tblW w:w="9400" w:type="dxa"/><w:tblBorders>{chegara}</w:tblBorders></w:tblPr>'
           f'<w:tblGrid><w:gridCol w:w="600"/><w:gridCol w:w="4400"/><w:gridCol w:w="4400"/></w:tblGrid>{"".join(qator)}</w:tbl>')
    body = (_p(f'Tarjima ({x}) — 72 gap', True) + _p('Qaytariladigan fayl: tarjima_' + x + '.xlsx (bu .docx — o\'qish/chop '
            'etish uchun nusxa). Yo\'riqnoma: YORIQNOMA.md.') + jad + _p('') + _p('Deklaratsiya', True) + _p(DEKL)
            + _p('Ism-familiya: ____________________   Sarflangan vaqt (taxminan): __________')
            + _p('Sana: ______________   Imzo: ______________'))
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document xmlns:w="{W}"><w:body>{body}'
           '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
           'w:header="0" w:footer="0" w:gutter="0"/></w:sectPr></w:body></w:document>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" '
          'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/></Relationships>')
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, m in (('[Content_Types].xml', ct), ('_rels/.rels', rels), ('word/document.xml', doc)):
            i = zipfile.ZipInfo(n, date_time=ZIPT)
            i.compress_type = zipfile.ZIP_DEFLATED
            i.external_attr = 0o644 << 16
            z.writestr(i, m.encode('utf-8'))
    return out.getvalue()


def yasa():
    E, tartib = toplam()
    fayl = {'kalit_tarjimon.json': (json.dumps({'seed': SEED, 'manba': 'evaluation/eval72/sentences.json', 'manba_sha256': E_SHA,
                                                'qator': {str(n): {'toplam': 'eval72', 'id': E[k]['id']} for n, k in enumerate(tartib, 1)}},
                                               ensure_ascii=False, indent=1) + '\n').encode('utf-8')}
    for x in ('T1', 'T2'):
        fayl[f'{x}/tarjima_{x}.xlsx'] = xlsx(x, E, tartib)
        fayl[f'{x}/tarjima_{x}.docx'] = docx(x, E, tartib)
        fayl[f'{x}/YORIQNOMA.md'] = YORIQNOMA.format(x=x, dekl=DEKL).encode('utf-8')
    return E, tartib, fayl


def qaytish(E, tartib, fayl):
    """Paketni o'qib kalit bilan solishtirish (tahlil.py o'quvchisi bilan) — matn chiqarilmaydi."""
    import openpyxl
    import re
    k = json.loads(fayl['kalit_tarjimon.json'])
    uz = {r['id']: r['uz'] for r in E}
    natija = {}
    for x in ('T1', 'T2'):
        wb = openpyxl.load_workbook(io.BytesIO(fayl[f'{x}/tarjima_{x}.xlsx']), read_only=True)
        q = list(wb.worksheets[0].iter_rows(values_only=True))
        ok_x = q[0][:3] == ('№', 'Manba', 'Tarjima') and len(q) == 73 and all(
            uz[k['qator'][str(r[0])]['id']] == r[1] and r[2] is None for r in q[1:])
        x_doc = zipfile.ZipFile(io.BytesIO(fayl[f'{x}/tarjima_{x}.docx'])).read('word/document.xml').decode('utf-8')
        tr = re.findall(r'<w:tr>(.*?)</w:tr>', x_doc, re.S)
        hj = [[re.sub(r'<[^>]+>', '', c) for c in re.findall(r'<w:tc>(.*?)</w:tc>', t, re.S)] for t in tr]
        from xml.sax.saxutils import unescape
        ok_d = len(hj) == 73 and all(unescape(h[1]) == uz[k['qator'][h[0]]['id']] and h[2] == '' for h in hj[1:])
        ichida = b''.join(v for n, v in fayl.items() if n.startswith(x + '/'))
        taqiq = sum(r['ref_en'][:30].encode('utf-8') in ichida for r in E) + sum(r['id'].encode() in ichida for r in E)
        natija[x] = {'xlsx': ok_x, 'docx': ok_d, 'etalon_yoki_id_paketda': taqiq}
    natija['tartib_bir_xil'] = True                     # bitta tartib ikkala paketga (yasa)
    return natija


def main():
    E, tartib, fayl = yasa()
    q = qaytish(E, tartib, fayl)
    ok = all(v['xlsx'] and v['docx'] and v['etalon_yoki_id_paketda'] == 0 for x, v in q.items() if x in ('T1', 'T2'))
    print('qaytish tekshiruvi:', json.dumps(q, ensure_ascii=False))
    if '--tekshir' in sys.argv:
        farq = [n for n, b in fayl.items() if not (PAKET / n).exists() or (PAKET / n).read_bytes() != b]
        print('diskdagi bilan bayt-aynan:', 'HA' if not farq else f'FARQ {farq}')
        sys.exit(0 if ok and not farq else 1)
    if not ok:
        sys.exit("TO'XTA: qaytish tekshiruvi o'tmadi — hech narsa yozilmadi")
    for n, b in fayl.items():
        (PAKET / n).parent.mkdir(parents=True, exist_ok=True)
        (PAKET / n).write_bytes(b)
        print(f'{n} {hashlib.sha256(b).hexdigest()}')


if __name__ == '__main__':
    main()
