# -*- coding: utf-8 -*-
"""TOLQIN-2 — GT Documents uchun kirish .docx (tuzatish 3: .txt qabul qilinmadi). Matn ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/gt_docx.py            # veb/kirish/gt_NN.txt -> gt_NN.docx (01..19) + gt_docx_sha256.json
    python3 analysis/tolqin-2/gt_docx.py --tekshir  # yozmaydi; diskdagi .docx qaytish tekshiruvi va sha256

Har `gt_NN.txt` qatori — bitta paragraf (`<w:p><w:r><w:t xml:space="preserve">…`), matn bayt-aynan (faqat XML
qochirish & < >); uslub, shrift, sarlavha, raqamlash YO'Q (styles.xml yo'q — Word sukuti). Paket: [Content_Types].xml,
_rels/.rels, word/document.xml; zip vaqti 1980-01-01, tartib qat'iy -> sha256 qayta yasashda o'zgarmaydi.
Qaytish tekshiruvi mustaqil (xml.etree): paragraflar -> qatorlar, `.txt` qatorlari bilan bayt-aynan; mos kelmasa —
TO'XTAYDI (exit 1, sha256 json yozilmaydi).
"""
import hashlib
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

SIKL = Path(__file__).resolve().parent
KIRISH = SIKL / 'veb' / 'kirish'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
CT = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Override PartName="/word/document.xml" '
      'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
RELS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/></Relationships>')


def qatorlar(txt):
    m = txt.read_bytes().decode('utf-8')
    assert m.endswith('\n') and '\r' not in m, f'{txt.name}: kutilgan format emas'
    return m[:-1].split('\n')


def yasa(qq):
    body = ''.join(f'<w:p><w:r><w:t xml:space="preserve">{escape(q)}</w:t></w:r></w:p>' for q in qq)
    doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:document xmlns:w="{W}"><w:body>{body}'
           '</w:body></w:document>')
    import io
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        for nom, mat in (('[Content_Types].xml', CT), ('_rels/.rels', RELS), ('word/document.xml', doc)):
            zi = zipfile.ZipInfo(nom, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, mat.encode('utf-8'))
    return buf.getvalue()


def qaytar(docx_bytes):
    """Mustaqil o'qish: har w:p -> uning barcha w:t matnlari ketma-ket."""
    import io
    x = zipfile.ZipFile(io.BytesIO(docx_bytes)).read('word/document.xml')
    root = ET.fromstring(x)
    return [''.join(t.text or '' for t in p.iter(f'{{{W}}}t')) for p in root.iter(f'{{{W}}}p')]


def main():
    tekshir = '--tekshir' in sys.argv
    sha, yomon = {}, 0
    for i in range(1, 20):
        txt, dx = KIRISH / f'gt_{i:02d}.txt', KIRISH / f'gt_{i:02d}.docx'
        qq = qatorlar(txt)
        b = dx.read_bytes() if tekshir else yasa(qq)
        q2 = qaytar(b)
        mos = sum(a.encode('utf-8') == c.encode('utf-8') for a, c in zip(qq, q2))
        ok = len(q2) == len(qq) and mos == len(qq)
        if tekshir:
            ok = ok and b == yasa(qq)                      # qayta yasash ham bayt-aynan
        yomon += not ok
        sha[dx.name] = {'sha256': hashlib.sha256(b).hexdigest(), 'paragraf': len(q2),
                        'manba': txt.name, 'manba_sha256': hashlib.sha256(txt.read_bytes()).hexdigest()}
        print(f'{dx.name}: qaytish {mos}/{len(qq)} (paragraf {len(q2)}) — {"OK" if ok else "MOS EMAS"}')
        if not ok and not tekshir:
            raise SystemExit(f"TO'XTA: {dx.name} qaytish tekshiruvi mos emas — hech narsa yozilmadi (oldingilar ham)")
        if not tekshir:
            sha[dx.name]['_bayt'] = b
    if tekshir:
        sys.exit(1 if yomon else 0)
    for nom, v in sha.items():                               # hammasi OK bo'lgandan keyingina yoziladi
        (KIRISH / nom).write_bytes(v.pop('_bayt'))
    (KIRISH / 'gt_docx_sha256.json').write_text(json.dumps(sha, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'19/19 OK; gt_docx_sha256.json yozildi')


if __name__ == '__main__':
    main()
