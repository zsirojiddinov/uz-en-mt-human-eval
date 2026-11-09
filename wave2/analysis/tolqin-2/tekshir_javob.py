# -*- coding: utf-8 -*-
"""TOLQIN-2 — veb/API javob fayllari tekshiruvi (tuzatish 1). READ-ONLY. Javob MATNI HECH QAYERGA CHIQARILMAYDI.

    python3 analysis/tolqin-2/tekshir_javob.py            # veb/javob/ dagi hamma javob fayllari (*_matnrejim.txt siz)
    python3 analysis/tolqin-2/tekshir_javob.py FAYL ...   # faqat berilgan fayllar

Javob nomi `<tizim>_NN.txt`: tizim ∈ claude, gpt, gemini (kirish `veb/kirish/llm_NN.txt`) yoki gt
(kirish `veb/kirish/gt_NN.txt`). Kirish sha256 `veb/kalit.json` bilan tekshiriladi.
Tekshiruv (oxirgi bitta `\n` va qator oxiridagi `\r` hisobga olinmaydi):
  - bo'sh qator yo'q;
  - qatorlar soni = kirishdagi gaplar soni;
  - LLM: har qator `N.` bilan boshlanadi (N butun son), raqamlar 1…N to'liq, takrorsiz va tartibda.
Chiqish: `fayl — OK` yoki `fayl — <muammo>` (faqat raqamlar va sonlar). Oxirida yo'q fayllar soni.
Exit 1 — kamida bitta fayl OK emas.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SIKL = Path(__file__).resolve().parent
VEB = SIKL / 'veb'
LLM = ('claude', 'gpt', 'gemini')
NOM = re.compile(r'^(claude|gpt|gemini|gt)_(\d{2})\.txt$')
RAQAM = re.compile(r'^(\d+)\.(\s|$)')


def tekshir(yol, kalit):
    m = NOM.match(yol.name)
    if not m:
        return 'nomi <tizim>_NN.txt emas'
    tizim, nn = m.groups()
    kir = f"{'gt' if tizim == 'gt' else 'llm'}_{nn}.txt"
    if kir not in kalit['fayllar']:
        return f'kirish {kir} yo\'q'
    kb = (VEB / 'kirish' / kir).read_bytes()
    assert hashlib.sha256(kb).hexdigest() == kalit['fayllar'][kir]['sha256'], f'{kir} sha256 mos emas'
    n = kalit['fayllar'][kir]['qator_soni']
    try:
        matn = yol.read_bytes().decode('utf-8')
    except UnicodeDecodeError:
        return 'UTF-8 emas'
    if matn.endswith('\n'):
        matn = matn[:-1]
    qatorlar = [q.rstrip('\r') for q in matn.split('\n')] if matn else []
    muammo = []
    bosh = [i for i, q in enumerate(qatorlar, 1) if not q.strip()]
    if bosh:
        muammo.append(f'bo\'sh qator: {len(bosh)} ta (qator {", ".join(map(str, bosh[:10]))}{" …" if len(bosh) > 10 else ""})')
    toliq = [q for q in qatorlar if q.strip()]
    if len(toliq) != n:
        muammo.append(f'qator soni {len(toliq)} != {n}')
    if tizim in LLM:
        raqamlar, raqamsiz = [], 0
        for q in toliq:
            r = RAQAM.match(q.strip())
            if r:
                raqamlar.append(int(r.group(1)))
            else:
                raqamsiz += 1
        if raqamsiz:
            muammo.append(f'raqamsiz qator: {raqamsiz} ta')
        kutilgan = set(range(1, n + 1))
        yoq = sorted(kutilgan - set(raqamlar))
        ortiq = sorted({x for x in raqamlar if x not in kutilgan})
        takror = sorted({x for x in raqamlar if raqamlar.count(x) > 1})
        if yoq:
            muammo.append(f'yetishmaydi: {", ".join(map(str, yoq))}')
        if ortiq:
            muammo.append(f'ortiqcha raqam: {", ".join(map(str, ortiq))}')
        if takror:
            muammo.append(f'takror: {", ".join(map(str, takror))}')
        if not (yoq or ortiq or takror) and raqamlar != sorted(raqamlar):
            muammo.append('tartib buzilgan')
    return 'OK' if not muammo else '; '.join(muammo)


def main():
    kalit = json.loads((VEB / 'kalit.json').read_text(encoding='utf-8'))
    fayllar = [Path(a) for a in sys.argv[1:]] or sorted(f for f in (VEB / 'javob').glob('*.txt')
                                                        if not f.stem.endswith('_matnrejim'))  # tuzatish 3: tahlilga kirmaydi
    yomon = 0
    for f in fayllar:
        h = tekshir(f, kalit)
        yomon += h != 'OK'
        print(f'{f.name} — {h}')
    if len(sys.argv) == 1:
        bor = {f.name for f in fayllar}
        for tizim, soni in (('claude', 12), ('gpt', 12), ('gemini', 12), ('gt', 19)):
            kerak = [f'{tizim}_{i:02d}.txt' for i in range(1, soni + 1)]
            print(f'{tizim}: {sum(k in bor for k in kerak)}/{soni} fayl bor')
    sys.exit(1 if yomon else 0)


if __name__ == '__main__':
    main()
