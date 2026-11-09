# -*- coding: utf-8 -*-
"""TOLQIN-2 — baholovchi paketlari R1/R2 (prereg §2.5, §3 (4); tuzatish 6). Matn ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/paket_baho.py            # paket/baholovchi/baho_{B,C,D,E}.xlsx + paket/kalit_baho.json
    python3 analysis/tolqin-2/paket_baho.py --tekshir  # yozmaydi; qayta yasash bayt-aynan + 0-tekshiruvlar

Elementlar: 5 tizim × eval72 (72) = 360. Tizim chiqishi — tahlil.py bilan bir xil o'qish (kkt_chiqish.json, veb/javob/*).
Tasodif (seed 20261016, bitta random.Random, ketma-ket): (1) neytral ID — 360 element aralashtirilib E001…E360;
(2) R1 tartibi; (3) R2 tartibi. R1 -> B, D; R2 -> C, E (prereg §2.5). Kalit paket/kalit_baho.json (paketga kirmaydi):
{elementlar:{EID:{tizim,id}}, tartib:{B:R1,…}, R1:[EID…], R2:[EID…]} — tahlil.py formati.
Paket (1-to'lqin rater_*.xlsx tuzilishi): «Yo'riqnoma» varag'i A1:A31 = 1-to'lqin matni AYNAN (sha256 e3c4c800…
tekshiriladi), A33 = prereg §2.5 «tizimni taxmin qilmang» bandi; «Baholash» varag'i:
Element | O'zbekcha gap | Inglizcha tarjima | Mazmun (1-5) | Ravonlik (1-5); baho katakchalari — butun son 1–5
validatsiyasi, ochiq; qolgani himoyalangan (parolsiz). Tizim nomi, qavat, ID paketda YO'Q — 0 tekshiruvi.
"""
import hashlib
import io
import json
import random
import sys
import zipfile
from datetime import datetime
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
EVAL72 = REPO / 'evaluation/eval72/sentences.json'
RATER_A = REPO / 'evaluation/eval72/rater_A.xlsx'
E_SHA = '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
KORSATMA_SHA = 'e3c4c800024faf9d5bcd3274922117a4c68cc63df5587b06a5cf1374af216c56'
SEED = 20261016
TIZIMLAR = ('KKT', 'Gemini', 'Claude', 'GPT', 'GT')
LLM = {'Gemini': 'gemini', 'Claude': 'claude', 'GPT': 'gpt'}
TARTIB = {'B': 'R1', 'C': 'R2', 'D': 'R1', 'E': 'R2'}
QOSHIMCHA_BAND = "  - Tizimni taxmin qilmang."
SAR = ('Element', "O'zbekcha gap", 'Inglizcha tarjima', 'Mazmun (1-5)', 'Ravonlik (1-5)')
QAT = datetime(2026, 10, 20, 0, 0, 0)
ZIPT = (2026, 10, 20, 0, 0, 0)
PAKET = SIKL / 'paket'


def chiqishlar():
    """{tizim: {eval72 id: tarjima}} — tahlil.py yukla() bilan bir xil o'qish (faqat eval72)."""
    kalit = json.loads((SIKL / 'veb' / 'kalit.json').read_text(encoding='utf-8'))
    out = {t: {} for t in TIZIMLAR}
    kkt = json.loads((SIKL / 'kkt_chiqish.json').read_text(encoding='utf-8'))
    out['KKT'] = {i: v['translation'] for i, v in kkt['eval72'].items()}
    for t, pre in LLM.items():
        for nn in range(1, 13):
            k = kalit['fayllar'][f'llm_{nn:02d}.txt']['qator']
            for q in (SIKL / 'veb' / 'javob' / f'{pre}_{nn:02d}.txt').read_text(encoding='utf-8').split('\n'):
                q = q.rstrip('\r')
                if not q.strip():
                    continue
                n, _, matn = q.strip().partition('.')
                g = k[n]
                if g['toplam'] == 'eval72':
                    out[t][g['id']] = matn.strip()
    for nn in range(1, 20):
        k = kalit['fayllar'][f'gt_{nn:02d}.txt']['qator']
        qq = [q.rstrip('\r') for q in (SIKL / 'veb' / 'javob' / f'gt_{nn:02d}.txt').read_text(encoding='utf-8').split('\n') if q.strip()]
        assert len(qq) == len(k)
        for j, q in enumerate(qq, 1):
            if k[str(j)]['toplam'] == 'eval72':
                out['GT'][k[str(j)]['id']] = q.strip()
    for t in TIZIMLAR:
        assert len(out[t]) == 72, (t, len(out[t]))
    return out


def korsatma():
    import openpyxl
    ws = openpyxl.load_workbook(RATER_A, read_only=True)["Yo'riqnoma"]
    col = [r[0] for r in ws.iter_rows(min_col=1, max_col=1, values_only=True)]
    qq = ['' if v is None else str(v) for v in col[:31]]
    assert hashlib.sha256('\n'.join(qq).encode('utf-8')).hexdigest() == KORSATMA_SHA, "ko'rsatma sha256 mos emas — TO'XTA"
    return col[:31]


def _qatiy_zip(b):
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


def yasa():
    import openpyxl
    from openpyxl.styles import Alignment, Font, Protection
    from openpyxl.worksheet.datavalidation import DataValidation
    eb = EVAL72.read_bytes()
    assert hashlib.sha256(eb).hexdigest() == E_SHA
    E = json.loads(eb)
    uz = {r['id']: r['uz'] for r in E}
    ch = chiqishlar()
    el = [(t, r['id']) for t in TIZIMLAR for r in E]
    rnd = random.Random(SEED)
    nid = el[:]
    rnd.shuffle(nid)
    eid = {e: f'E{k:03d}' for k, e in enumerate(nid, 1)}
    kalit = {'seed': SEED, 'elementlar': {eid[e]: {'tizim': e[0], 'id': e[1]} for e in sorted(el, key=lambda e: eid[e])}}
    tartiblar = {}
    for R in ('R1', 'R2'):
        t = sorted(kalit['elementlar'])
        rnd.shuffle(t)
        tartiblar[R] = t
    kalit.update(tartib=TARTIB, R1=tartiblar['R1'], R2=tartiblar['R2'])
    kors = korsatma()
    fayl = {'kalit_baho.json': (json.dumps(kalit, ensure_ascii=False, indent=1) + '\n').encode('utf-8')}
    for x, R in TARTIB.items():
        wb = openpyxl.Workbook()
        wb.properties.creator = 'TOLQIN-2'
        wb.properties.created = QAT
        wb.properties.modified = QAT
        y = wb.active
        y.title = "Yo'riqnoma"
        for v in kors:
            y.append([v])
        y.append([None])
        y.append([QOSHIMCHA_BAND])
        y.column_dimensions['A'].width = 110
        y.protection.sheet = True
        ws = wb.create_sheet('Baholash')
        ws.append(list(SAR))
        for c in ws[1]:
            c.font = Font(bold=True)
        for e in tartiblar[R]:
            g = kalit['elementlar'][e]
            ws.append([e, uz[g['id']], ch[g['tizim']][g['id']], None, None])
        n = len(tartiblar[R]) + 1
        dv = DataValidation(type='whole', operator='between', formula1='1', formula2='5', allow_blank=True,
                            showErrorMessage=True, errorTitle='1–5', error='Faqat 1, 2, 3, 4 yoki 5 (butun son).')
        dv.add(f'D2:E{n}')
        ws.add_data_validation(dv)
        for r in ws.iter_rows(min_row=2):
            for c in r[1:3]:
                c.alignment = Alignment(wrap_text=True, vertical='top')
            r[3].protection = Protection(locked=False)
            r[4].protection = Protection(locked=False)
        for col, w in zip('ABCDE', (9, 60, 60, 13, 14)):
            ws.column_dimensions[col].width = w
        ws.protection.sheet = True
        buf = io.BytesIO()
        wb.save(buf)
        fayl[f'baholovchi/baho_{x}.xlsx'] = _qatiy_zip(buf.getvalue())
    return E, ch, kalit, fayl


def nol_tekshiruv(E, ch, kalit, fayl):
    """Paket ichida tizim nomi, qavat nomi, gap ID — 0; kalit va tarkib mosligi."""
    import openpyxl
    taqiq = list(TIZIMLAR) + ['Google', 'Translate', 'flores', 'train', 'gold', 'eval72', 'a_qavat', 'layer'] + [r['id'] for r in E]
    natija = {}
    for x in TARTIB:
        b = fayl[f'baholovchi/baho_{x}.xlsx']
        z = zipfile.ZipFile(io.BytesIO(b))
        meta = ''.join(z.read(n).decode('utf-8', 'replace') for n in z.namelist() if 'sharedStrings' not in n and 'sheet' not in n)
        wb = openpyxl.load_workbook(io.BytesIO(b), read_only=True)
        q = list(wb['Baholash'].iter_rows(values_only=True))
        kors = [r[0] for r in wb["Yo'riqnoma"].iter_rows(values_only=True)]
        # ID/qavat/tizim — Element ustuni, sarlavha va metadata ichida (tarjima/manba matnining o'zi tizim chiqishi)
        tashqi = ' '.join(str(r[0]) for r in q) + meta + ' '.join(map(str, q[0]))
        topildi = sorted({t for t in taqiq if t.lower() in tashqi.lower()})
        # matn ustunlarida tizim/qavat nomi so'z sifatida: hisobot uchun (manba/tarjimaning o'zida bo'lishi mumkin)
        ichki = {t: sum(t.lower() in (str(r[1]) + ' ' + str(r[2])).lower().split() for r in q[1:]) for t in TIZIMLAR + ('Google',)}
        mos = all(kalit['elementlar'][r[0]] and r[2] == ch[kalit['elementlar'][r[0]]['tizim']][kalit['elementlar'][r[0]]['id']]
                  for r in q[1:])
        natija[x] = {'element': len(q) - 1, 'tartib': TARTIB[x], 'kalitga_mos': mos and [r[0] for r in q[1:]] == kalit[TARTIB[x]],
                     'tashqi_taqiq_topildi': topildi, 'matn_ichida_soz': {k: v for k, v in ichki.items() if v},
                     'korsatma_31_aynan': hashlib.sha256('\n'.join('' if v is None else str(v) for v in kors[:31]).encode()).hexdigest() == KORSATMA_SHA,
                     'qoshimcha_band': kors[32] == QOSHIMCHA_BAND}
    return natija


def main():
    E, ch, kalit, fayl = yasa()
    n = nol_tekshiruv(E, ch, kalit, fayl)
    ok = all(v['element'] == 360 and v['kalitga_mos'] and not v['tashqi_taqiq_topildi'] and v['korsatma_31_aynan']
             and v['qoshimcha_band'] for v in n.values())
    print('tekshiruv:', json.dumps(n, ensure_ascii=False))
    if '--tekshir' in sys.argv:
        farq = [k for k, b in fayl.items() if not (PAKET / k).exists() or (PAKET / k).read_bytes() != b]
        print('diskdagi bilan bayt-aynan:', 'HA' if not farq else f'FARQ {farq}')
        sys.exit(0 if ok and not farq else 1)
    if not ok:
        sys.exit("TO'XTA: tekshiruv o'tmadi — hech narsa yozilmadi")
    for k, b in fayl.items():
        (PAKET / k).parent.mkdir(parents=True, exist_ok=True)
        (PAKET / k).write_bytes(b)
        print(f'{k} {hashlib.sha256(b).hexdigest()}')


if __name__ == '__main__':
    main()
