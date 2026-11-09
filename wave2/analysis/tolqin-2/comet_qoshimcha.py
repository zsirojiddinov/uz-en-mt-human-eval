# -*- coding: utf-8 -*-
"""TOLQIN-2 — COMET (ikkilamchi metrika; prereg §2.7; tuzatish 6). MUZLATILADI. Ma'lumot yig'ilishidan OLDIN commit.

    ~/.venvs/tolqin2_comet/bin/python analysis/tolqin-2/comet_qoshimcha.py --yurish       # BIR MARTA, tahlil.py dan KEYIN
    ~/.venvs/tolqin2_comet/bin/python analysis/tolqin-2/comet_qoshimcha.py --sintetik DIR [--n 5]   # smoke-test

Muhit: alohida venv (~/.venvs/tolqin2_comet: unbabel-comet 2.2.7, torch 2.8.0) — loyiha .venv iga tegilmaydi.
Model: Unbabel/wmt22-comet-da (etalonli; src + mt + ref). predict(batch_size=16, gpus=0, num_workers=1) — CPU.
Kirishlar (tahlil.py bilan bir xil o'qish): a_qavat_400.json, eval72, kkt_chiqish.json, veb/kalit.json, veb/javob/*,
qaytgan/T1.xlsx, qaytgan/T2.xlsx (qabul.py chiqishi).
A-qavat: 5 tizim × 400, etalon FLORES (en_ref). B-qavat: 5 tizim × 72, har etalon bilan ALOHIDA (ref_en, T1, T2) va
uchalasining o'rtachasi (gap bo'yicha uch ball o'rtachasi, so'ng tizim o'rtachasi).
Maqomi: ikkilamchi metrika. Cheklov: wmt22-comet-da o'qitish ma'lumotida (WMT DA) o'zbek tili yo'q.
Run-once: natija/comet_natija.json mavjud bo'lsa TO'XTAYDI; natija/tahlil_natija.json yo'q bo'lsa ham TO'XTAYDI
(tahlil.py --yurish natija/ mavjud bo'lsa to'xtaydi — shuning uchun tartib: avval tahlil.py, keyin shu skript).
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
MODEL = 'Unbabel/wmt22-comet-da'
SOZLAMA = {'batch_size': 16, 'gpus': 0, 'num_workers': 1, 'progress_bar': False}
_sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))


def tahlil_moduli():
    T = importlib.util.module_from_spec(_sp)
    _sp.loader.exec_module(T)
    return T


def kirishlar(T, ild, eval72_yol):
    """tahlil.yukla — xuddi shu o'qish (tizimlar, tarjimonlar); baholovchi fayllari COMET da ishlatilmaydi."""
    A, B, chiq, Tr, _, _, _, _, tekshir = T.yukla(ild, eval72_yol)
    return A, B, chiq, Tr, tekshir


def hisobla(model, A, B, chiq, Tr, tizimlar, n=None):
    A = A[:n] if n else A
    B = B[:n] if n else B
    out = {'A': {}, 'B': {}}
    for t in tizimlar:
        d = [{'src': r['uz'], 'mt': chiq[t][('a_qavat', r['id'])], 'ref': r['en_ref']} for r in A]
        o = model.predict(d, **SOZLAMA)
        out['A'][t] = {'tizim_ball': float(sum(o.scores) / len(o.scores)), 'n': len(d)}
        etalon = {'ref_en': [r['ref_en'] for r in B], **{x: [Tr[x].get(r['id']) for r in B] for x in ('T1', 'T2') if x in Tr}}
        seg = {}                                          # tuzatish 10: T2 yo'q; T1 № 55 da etalon yo'q (None) — gap tashlanadi
        for e, refs in etalon.items():
            jj = [(k, r, rf) for k, (r, rf) in enumerate(zip(B, refs)) if rf is not None]
            d = [{'src': r['uz'], 'mt': chiq[t][('eval72', r['id'])], 'ref': rf} for _, r, rf in jj]
            seg[e] = dict(zip([k for k, _, _ in jj], [float(x) for x in model.predict(d, **SOZLAMA).scores]))
        ort = [(lambda v: sum(v) / len(v))([seg[e][k] for e in etalon if k in seg[e]]) for k in range(len(B))]
        out['B'][t] = {**{f'{e}_tizim_ball': sum(v.values()) / len(v) for e, v in seg.items()},
                       **{f'{e}_n': len(v) for e, v in seg.items()},
                       'uch_etalon_ortacha': sum(ort) / len(ort), 'etalonlar': list(etalon), 'n': len(B)}
    return out


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--yurish', action='store_true')
    g.add_argument('--sintetik')
    ap.add_argument('--n', type=int, default=5)
    a = ap.parse_args()
    import comet
    from comet import download_model, load_from_checkpoint
    T = tahlil_moduli()
    if a.sintetik:
        d = T.sintetik(a.sintetik)
        ild, ev, chiqish, n = d, d / 'eval72.json', d / 'natija', a.n
        chiqish.mkdir(exist_ok=True)
    else:
        ild, ev, chiqish, n = SIKL, REPO / 'evaluation/eval72/sentences.json', SIKL / 'natija', None
        if (chiqish / 'comet_natija.json').exists():
            sys.exit("TO'XTA: natija/comet_natija.json mavjud — skript bir marta yuriladi")
        if not (chiqish / 'tahlil_natija.json').exists():
            sys.exit("TO'XTA: avval tahlil.py --yurish (natija/tahlil_natija.json yo'q)")
    A, B, chiq, Tr, tekshir = kirishlar(T, ild, ev)
    yol = download_model(MODEL)
    model = load_from_checkpoint(yol)
    R = {'model': MODEL, 'checkpoint': str(Path(yol).relative_to(Path(yol).parents[2])) if len(Path(yol).parents) > 2 else yol,
         'checkpoint_sha256': hashlib.sha256(Path(yol).read_bytes()).hexdigest(), 'comet_versiya': getattr(comet, '__version__', '2.2.7'),
         'sozlama': SOZLAMA, 'kirish_sha256': tekshir, 'maqom': 'ikkilamchi metrika (prereg §2.7)',
         'cheklov': "wmt22-comet-da o'qitish ma'lumotida o'zbek tili yo'q", 'sintetik': bool(a.sintetik), 'n_cheklov': n,
         'natija': hisobla(model, A, B, chiq, Tr, T.TIZIMLAR, n)}
    (chiqish / 'comet_natija.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    print(f"COMET: A {len(R['natija']['A'])} tizim · B {len(R['natija']['B'])} tizim (etalon 3 + o'rtacha) -> {chiqish / 'comet_natija.json'}")


if __name__ == '__main__':
    main()
