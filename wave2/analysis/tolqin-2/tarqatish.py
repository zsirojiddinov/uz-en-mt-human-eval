# -*- coding: utf-8 -*-
"""TOLQIN-2 — tarqatish to'plamlari (prereg §3 (6) oldidan). Gap matni ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/tarqatish.py [ROL …]   # ~/Downloads/TOLQIN2_tarqatish/{T1,T2,B,C,D,E}.zip + tarqatish_jurnali.csv
    (ROL berilsa — faqat shular qayta yasaladi; mavjud zip ~/Downloads/TOLQIN2_tarqatish/eski/ ga ko'chiriladi, jurnalda
    faqat shu qatorlarning zip_sha256 i yangilanadi)

Tarjimon zip: tarjima_TX.xlsx (paket/TX/) + YORIQNOMA_tarjimon.pdf (paket/TX/YORIQNOMA.md matni, cupsfilter text->pdf).
Baholovchi zip: baho_X.xlsx (paket/baholovchi/) + YORIQNOMA_baholovchi.pdf (xlsx «Yo'riqnoma» varag'i A ustuni aynan).
Tekshiruvlar: (1) PDF matni (pdfminer) manba matni bilan bo'shliqsiz belgilar ketma-ketligi bo'yicha aynan;
(2) zip ichida fayl soni 2, nomida «kalit» yoki .json yo'q; (3) mazmunda (xlsx XML + PDF matni) gap ID (eval72,
a_qavat), qavat nomi (flores/train/gold — so'z sifatida), «eval72»/«a_qavat»/«kalit», tizim nomi — 0. Istisno: tarjimon
YORIQNOMA taqiqlar ro'yxatidagi vosita nomlari (Google Translate, ChatGPT, Gemini, Claude …) — alohida sanaladi.
zip ichidagi vaqt belgilari qat'iy. tarqatish_jurnali.csv: rol, zip_sha256, berilgan_sana, qaytgan_sana, qabul_natijasi.
"""
import csv
import hashlib
import io
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
CHIQ = Path.home() / 'Downloads' / 'TOLQIN2_tarqatish'
ZIPT = (2026, 10, 20, 0, 0, 0)
TIZIM = ('KKT', 'Gemini', 'Claude', 'GPT', 'ChatGPT', 'Google', 'Translate')


def pdf(matn):
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / 'y.txt'
        p.write_text(matn, encoding='utf-8')
        r = subprocess.run(['cupsfilter', '-i', 'text/plain', '-m', 'application/pdf', str(p)], capture_output=True)
        assert r.returncode == 0 and r.stdout.startswith(b'%PDF'), r.stderr[-300:]
        return r.stdout


def pdf_matn(b):
    from pdfminer.high_level import extract_text
    return extract_text(io.BytesIO(b))


def xlsx_matn(b):
    z = zipfile.ZipFile(io.BytesIO(b))
    return ' '.join(re.sub(r'<[^>]+>', ' ', z.read(n).decode('utf-8', 'replace')) for n in z.namelist() if n.endswith('.xml'))


def zipla(fayllar):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, b in fayllar:
            i = zipfile.ZipInfo(n, date_time=ZIPT)
            i.compress_type = zipfile.ZIP_DEFLATED
            i.external_attr = 0o644 << 16
            z.writestr(i, b)
    return out.getvalue()


def taqiqlar():
    E = json.loads((REPO / 'evaluation/eval72/sentences.json').read_text(encoding='utf-8'))
    A = json.loads((SIKL / 'a_qavat_400.json').read_text(encoding='utf-8'))
    idlar = [r['id'] for r in E] + [r['id'] for r in A]
    return idlar


def tekshir(zb, rol, idlar):
    z = zipfile.ZipFile(io.BytesIO(zb))
    nomlar = z.namelist()
    natija = {'fayl_soni': len(nomlar), 'nomda_kalit_yoki_json': sum('kalit' in n.lower() or n.lower().endswith('.json') for n in nomlar)}
    matnlar = {}
    for n in nomlar:
        b = z.read(n)
        matnlar[n] = xlsx_matn(b) if n.endswith('.xlsx') else pdf_matn(b)
    def sana(m, so_zlar):
        return {s: len(re.findall(rf'(?<![\w-]){re.escape(s)}(?![\w-])', m, flags=re.I)) for s in so_zlar}
    for n, m in matnlar.items():
        id_s = sum(v for v in sana(m, idlar).values())
        qavat = sana(m, ('flores', 'train', 'gold', 'eval72', 'a_qavat', 'kalit', 'layer'))
        tiz = sana(m, TIZIM)
        natija[n] = {'gap_id': id_s, 'qavat_va_kalit_sozlari': sum(qavat.values()), 'tizim_nomi': sum(tiz.values()),
                     'tizim_nomi_tafsil': {k: v for k, v in tiz.items() if v}}
    return natija, matnlar


def main():
    CHIQ.mkdir(parents=True, exist_ok=True)
    idlar = taqiqlar()
    import openpyxl
    import sys
    import shutil
    from datetime import datetime
    rollar = [a for a in sys.argv[1:] if a in ('T1', 'T2', 'B', 'C', 'D', 'E')] or ['T1', 'T2', 'B', 'C', 'D', 'E']
    jp = SIKL / 'tarqatish_jurnali.csv'
    eski = {r[0]: r for r in csv.reader(open(jp, encoding='utf-8'))} if jp.exists() else {}
    jurnal, hisobot = [], {}
    for x in rollar:
        if (CHIQ / f'{x}.zip').exists():
            (CHIQ / 'eski').mkdir(exist_ok=True)
            shutil.move(str(CHIQ / f'{x}.zip'), str(CHIQ / 'eski' / f'{x}__{datetime.now().strftime("%Y%m%dT%H%M%S")}.zip'))
        if x.startswith('T'):
            xl = (SIKL / 'paket' / x / f'tarjima_{x}.xlsx').read_bytes()
            yo = (SIKL / 'paket' / x / 'YORIQNOMA.md').read_text(encoding='utf-8')
            fayllar = [(f'tarjima_{x}.xlsx', xl), ('YORIQNOMA_tarjimon.pdf', pdf(yo))]
        else:
            xl = (SIKL / 'paket' / 'baholovchi' / f'baho_{x}.xlsx').read_bytes()
            ws = openpyxl.load_workbook(io.BytesIO(xl), read_only=True)["Yo'riqnoma"]
            yo = '\n'.join('' if r[0] is None else str(r[0]) for r in ws.iter_rows(min_col=1, max_col=1, values_only=True)) + '\n'
            fayllar = [(f'baho_{x}.xlsx', xl), ('YORIQNOMA_baholovchi.pdf', pdf(yo))]
        zb = zipla(fayllar)
        nat, matnlar = tekshir(zb, x, idlar)
        pdf_nom = fayllar[1][0]
        nat['pdf_matn_aynan'] = ''.join(matnlar[pdf_nom].split()) == ''.join(yo.split())
        nat['xlsx_bayt_aynan_paket'] = zipfile.ZipFile(io.BytesIO(zb)).read(fayllar[0][0]) == xl
        (CHIQ / f'{x}.zip').write_bytes(zb)
        h = hashlib.sha256(zb).hexdigest()
        nat.update(zip_bayt=len(zb), zip_sha256=h)
        hisobot[x] = nat
        eski[x] = [x, h] + (eski[x][2:] if x in eski else ['', '', ''])
    with open(jp, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['rol', 'zip_sha256', 'berilgan_sana', 'qaytgan_sana', 'qabul_natijasi'])
        w.writerows(eski[x] for x in ('T1', 'T2', 'B', 'C', 'D', 'E') if x in eski)
    print(json.dumps(hisobot, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
