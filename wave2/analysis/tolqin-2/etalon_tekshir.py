# -*- coding: utf-8 -*-
"""TOLQIN-2 — etalon mustaqilligi tekshiruvi (tuzatish 8). MUZLATILADI, BIR MARTA. Matn CHIQARILMAYDI — faqat sonlar.

    python3 analysis/tolqin-2/etalon_tekshir.py --yurish            # qabul.py dan KEYIN, tahlil.py dan OLDIN
    python3 analysis/tolqin-2/etalon_tekshir.py --sintetik DIR      # smoke-test (DIR — tolqin-2 nusxasi ildizi)

Kirish: qaytgan/T1.xlsx, qaytgan/T2.xlsx (qabul.py chiqishi; № -> paket/kalit_tarjimon.json), tizim chiqishlari eval72
(paket_baho.chiqishlar — tahlil.py bilan bir xil o'qish). Chiqish: etalon/etalon_tekshir.json (natija/ EMAS — tahlil.py
natija/ mavjud bo'lsa to'xtaydi); fayl mavjud bo'lsa TO'XTAYDI.
Har tarjimon (T1, T2), 72 gap, har tizim (KKT, Gemini, Claude, GPT, GT) bilan:
  (a) normallashtirilgan aynan moslik ulushi (normallashtirish — ekspozitsiya_2_reja.md: apostrof variantlari -> ',
      kichik harf, Unicode P*/S* -> bo'shliq, bo'shliqlar yig'iladi);
  (b) o'rtacha gap-chrF (sacreBLEU CHRF, chrF2; hyp = tarjimon, ref = tizim); eng yaqin va ikkinchi eng yaqin tizim farqi;
  (c) T1–T2 o'rtacha gap-chrF (hyp = T1, ref = T2) — tavsifiy.
Bayroq: (a) biror tizim bilan >= 18/72 (25 %) YOKI (b) farq >= 12 ball. Bayroq ayblov emas (tuzatish 8).
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

SIKL = Path(__file__).resolve().parent
AYNAN_CHEGARA, FARQ_CHEGARA = 18, 12.0


def _mod(ild, nom):
    sp = importlib.util.spec_from_file_location(f'{nom}_m', str(ild / f'{nom}.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def tekshir(ild):
    import openpyxl
    from sacrebleu.metrics import CHRF
    PB, EK = _mod(ild, 'paket_baho'), _mod(ild, 'ekspozitsiya_2')
    ch = PB.chiqishlar()
    kalit = json.loads((ild / 'paket' / 'kalit_tarjimon.json').read_text(encoding='utf-8'))
    T, sha = {}, {}
    for x in ('T1', 'T2'):
        p = ild / 'qaytgan' / f'{x}.xlsx'
        if not p.exists():                                # tuzatish 10 (b): T2 olinmadi
            continue
        sha[x] = hashlib.sha256(p.read_bytes()).hexdigest()
        q = list(openpyxl.load_workbook(p, read_only=True).worksheets[0].iter_rows(values_only=True))
        assert tuple(q[0][:3]) == ('№', 'Manba', 'Tarjima'), f'{x}: sarlavha'
        T[x] = {kalit['qator'][str(int(r[0]))]['id']: str(r[2]).strip() for r in q[1:]
                if r[0] is not None and r[2] not in (None, '')}      # tuzatish 10 (a): T1 № 55 bo'sh — gap tashlanadi
        assert len(T[x]) == 72 or (x == 'T1' and len(T[x]) == 71), f'{x}: 72/72 emas (tuzatish 10: T1 71)'
    chrf = CHRF()
    n = lambda s: ' '.join(EK.norm_tok(s))
    natija = {}
    for x in T:
        ids = sorted(T[x])
        aynan = {t: sum(n(T[x][i]) == n(ch[t][i]) for i in ids) for t in PB.TIZIMLAR}
        cf = {t: sum(chrf.sentence_score(T[x][i], [ch[t][i]]).score for i in ids) / len(ids) for t in PB.TIZIMLAR}
        tart = sorted(cf, key=cf.get, reverse=True)
        farq = cf[tart[0]] - cf[tart[1]]
        b_a = max(aynan.values()) >= AYNAN_CHEGARA
        b_b = farq >= FARQ_CHEGARA
        natija[x] = {'aynan_soni': aynan, 'aynan_ulush': {t: v / len(ids) for t, v in aynan.items()},
                     'chrf_ortacha': cf, 'eng_yaqin': tart[0], 'ikkinchi': tart[1], 'farq_1_2': farq,
                     'bayroq_a_aynan>=18': b_a, 'bayroq_b_farq>=12': b_b, 'BAYROQ': b_a or b_b}
    ids = sorted(set(T['T1']) & set(T.get('T2', {})))
    t12 = sum(chrf.sentence_score(T['T1'][i], [T['T2'][i]]).score for i in ids) / len(ids) if ids else None
    return {'kirish_sha256': sha, 'n_gap': {x: len(v) for x, v in T.items()}, 'mezon': {'aynan_min': AYNAN_CHEGARA, 'farq_min': FARQ_CHEGARA},
            'tarjimon': natija, 'T1_T2_chrf_ortacha': t12}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--yurish', action='store_true')
    g.add_argument('--sintetik')
    a = ap.parse_args()
    ild = Path(a.sintetik) if a.sintetik else SIKL
    chiq = ild / 'etalon' / 'etalon_tekshir.json'
    if chiq.exists():
        sys.exit("TO'XTA: etalon/etalon_tekshir.json mavjud — skript bir marta yuriladi")
    if not a.sintetik and (SIKL / 'natija').exists():
        sys.exit("TO'XTA: natija/ mavjud — etalon tekshiruvi tahlil.py dan OLDIN yuriladi (tuzatish 8)")
    R = tekshir(ild)
    chiq.parent.mkdir(exist_ok=True)
    chiq.write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    for x, v in R['tarjimon'].items():
        b = 'HA' if v['BAYROQ'] else "yo'q"
        print(f"{x}: aynan max {max(v['aynan_soni'].values())}/{R['n_gap'][x]} · farq_1_2 {v['farq_1_2']:.1f} · BAYROQ {b}")
    print(f"T1–T2 chrF {R['T1_T2_chrf_ortacha']} -> {chiq}")


if __name__ == '__main__':
    main()
