# -*- coding: utf-8 -*-
"""TOLQIN-2 — GPT/Gemini veb uchun to'liq kirish fayllari (tuzatish 1). Matn ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/veb_toliq.py            # -> veb/kirish/llm_NN_toliq.txt (01..12)
    python3 analysis/tolqin-2/veb_toliq.py --tekshir  # yozmaydi; diskdagi bilan va javob_xom/gemini_NN.json dagi
                                                      # sorov_sha256 bilan bayt-aynan

Fayl = PROMPT (tuzatish 1, AYNAN — `gemini_ol.py` dagi bilan bir xil) + "\\n\\n" + `veb/kirish/llm_NN.txt` (bayt-aynan),
ya'ni Gemini API ga yuborilgan ko'rinishning o'zi. Kirish sha256 `veb/kalit.json` bilan tekshiriladi.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SIKL = Path(__file__).resolve().parent
KIRISH = SIKL / 'veb' / 'kirish'
PROMPT = ('Translate each numbered Uzbek sentence into English. Keep the numbering. '
          'Output only the numbered translations, one per line.')


def main():
    t = (SIKL / 'tuzatish_1.md').read_text(encoding='utf-8')
    assert ' '.join(re.search(r'"(Translate each.*?)"', t, re.S).group(1).split()) == PROMPT, 'prompt tuzatish 1 ga mos emas'
    kalit = json.loads((SIKL / 'veb' / 'kalit.json').read_text(encoding='utf-8'))
    tekshir = '--tekshir' in sys.argv
    yomon = 0
    for i in range(1, 13):
        kir = KIRISH / f'llm_{i:02d}.txt'
        kb = kir.read_bytes()
        assert hashlib.sha256(kb).hexdigest() == kalit['fayllar'][kir.name]['sha256'], f'{kir.name} sha256 mos emas'
        b = PROMPT.encode('utf-8') + b'\n\n' + kb
        f = KIRISH / f'llm_{i:02d}_toliq.txt'
        if tekshir:
            ok = f.exists() and f.read_bytes() == b
            xom = SIKL / 'veb' / 'javob_xom' / f'gemini_{i:02d}.json'
            gem = ''
            if xom.exists():                                    # Gemini'ga yuborilgan so'rov bilan aynanmi
                g = json.loads(xom.read_text(encoding='utf-8')).get('sorov_sha256') == hashlib.sha256(b).hexdigest()
                ok = ok and g
                gem = f' · Gemini so\'rovi sha256 {"aynan" if g else "FARQ"}'
            yomon += not ok
            print(f'{f.name} — {"AYNAN" if ok else "FARQ"}{gem}')
        else:
            f.write_bytes(b)
            print(f'{f.name} {hashlib.sha256(b).hexdigest()}')
    sys.exit(1 if yomon else 0)


if __name__ == '__main__':
    main()
