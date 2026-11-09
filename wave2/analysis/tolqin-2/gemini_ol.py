# -*- coding: utf-8 -*-
"""TOLQIN-2 — Gemini chiqishlari API orqali (tuzatish 1). Javob matni ekranga CHIQARILMAYDI.

    python3 analysis/tolqin-2/gemini_ol.py [NN ...]     # sukut: 01..12

Har `veb/kirish/llm_NN.txt` alohida so'rov (yangi suhbat, tarixsiz): prompt (tuzatish 1, aynan) + "\n\n" +
kirish fayli matni (bayt-aynan). Model `gemini-3.5-flash` (gemini_model.md), temperature 0, `google.generativeai`.
Kalit — asosiy daraxtdagi `.env` dan (`GEMINI_API_KEY`; qiymat chop etilmaydi).
Yoziladi: `veb/javob/gemini_NN.txt` (`response.text` tahrirsiz), `veb/javob_xom/gemini_NN.json`
(`response.to_dict()` + so'rov meta), `veb/jurnal.csv` ga qator.
Vaqtinchalik xato (API istisnosi) — 3 martagacha qayta urinish (30/60/90 s); oxirgisi ham 429 bo'lsa — TO'XTAYDI.
Mazmun bo'yicha qayta so'rov (yetishmagan raqamlar) avtomatik QILINMAYDI.
"""
import csv
import datetime as dt
import hashlib
import json
import sys
import time
from pathlib import Path

SIKL = Path(__file__).resolve().parent
VEB = SIKL / 'veb'
ENV = Path.home() / 'PyCharmMiscProject' / '.env'
MODEL = 'gemini-3.5-flash'
QAYTA = 3
PROMPT = ('Translate each numbered Uzbek sentence into English. Keep the numbering. '
          'Output only the numbered translations, one per line.')


def vaqt():
    return dt.datetime.now().astimezone().isoformat(timespec='seconds')


def main():
    import google.generativeai as genai
    from dotenv import dotenv_values
    kalit_api = dotenv_values(ENV).get('GEMINI_API_KEY')
    assert kalit_api, 'GEMINI_API_KEY topilmadi'
    genai.configure(api_key=kalit_api)
    model = genai.GenerativeModel(MODEL, generation_config={'temperature': 0.0, 'max_output_tokens': 32768})
    kalit = json.loads((VEB / 'kalit.json').read_text(encoding='utf-8'))
    (VEB / 'javob_xom').mkdir(exist_ok=True)
    nnlar = sys.argv[1:] or [f'{i:02d}' for i in range(1, 13)]
    for nn in nnlar:
        kir = VEB / 'kirish' / f'llm_{nn}.txt'
        kb = kir.read_bytes()
        assert hashlib.sha256(kb).hexdigest() == kalit['fayllar'][kir.name]['sha256'], f'{kir.name} sha256'
        sorov = PROMPT + '\n\n' + kb.decode('utf-8')
        urinish = []
        for k in range(QAYTA + 1):
            boshi = vaqt()
            try:
                r = model.generate_content(sorov)
                oxiri = vaqt()
                break
            except Exception as e:  # vaqtinchalik xato
                kod = getattr(e, 'code', None) or type(e).__name__
                urinish.append(f'{boshi} {kod}')
                print(f'gemini_{nn}: urinish {k + 1} xato {kod}')
                if k == QAYTA:
                    with open(VEB / 'jurnal.csv', 'a', newline='', encoding='utf-8') as f:
                        csv.writer(f).writerow(['gemini', f'gemini_{nn}.txt', urinish[0].split()[0], vaqt(),
                                                f'API; model {MODEL}; XATO, javob yo\'q; urinishlar: {" | ".join(urinish)}'])
                    raise SystemExit(f"TO'XTA: gemini_{nn} {QAYTA + 1} urinishda ham xato ({kod})")
                time.sleep(30 * (k + 1))
        d = r.to_dict()
        nomzod = (d.get('candidates') or [{}])[0]
        finish = nomzod.get('finish_reason')
        versiya = d.get('model_version') or ''
        try:
            matn = r.text
        except Exception as e:  # bloklangan / bo'sh
            matn = None
            finish = f'{finish} ({type(e).__name__})'
        xom = {'urinishlar_xato': urinish, 'model_sorov': MODEL, 'model_version': versiya, 'temperature': 0.0, 'boshi': boshi, 'oxiri': oxiri,
               'kirish': kir.name, 'kirish_sha256': hashlib.sha256(kb).hexdigest(),
               'sorov_sha256': hashlib.sha256(sorov.encode('utf-8')).hexdigest(), 'javob': d}
        (VEB / 'javob_xom' / f'gemini_{nn}.json').write_text(json.dumps(xom, ensure_ascii=False, indent=1) + '\n',
                                                              encoding='utf-8')
        if matn is not None:
            (VEB / 'javob' / f'gemini_{nn}.txt').write_bytes(matn.encode('utf-8'))
        with open(VEB / 'jurnal.csv', 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(['gemini', f'gemini_{nn}.txt', boshi, oxiri,
                                    f'API; model {MODEL}; model_version {versiya}; temperature 0; finish {finish}'
                                    + (f'; oldingi urinishlar: {" | ".join(urinish)}' if urinish else '')])
        u = d.get('usage_metadata') or {}
        print(f'gemini_{nn}: {boshi}..{oxiri} · versiya {versiya} · finish {finish} · '
              f'matn {"bor" if matn else "YO‘Q"} · token chiqish {u.get("candidates_token_count")}')


if __name__ == '__main__':
    main()
