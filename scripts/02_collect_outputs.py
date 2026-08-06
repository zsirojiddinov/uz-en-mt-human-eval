# -*- coding: utf-8 -*-
"""CE1 — tizim chiqishlarini yig'ish (72 gap).

  --system system  : joriy KKT tizimi (sentence_translator_v2). Worktree'da ham
                     ishlatiladi (S2 = M1-oldingi commit).
  --system gemini  : Gemini (NEYTRAL qat'iy prompt, system-instruction YO'Q,
                     temperature=0). Model/sana hujjatlanadi.
  --out PATH       : chiqish JSON {id: translation, ...} + _meta.

Ishlatish:
  python evaluation/eval72/collect_outputs.py --system system --out .../s1_outputs.json
  python evaluation/eval72/collect_outputs.py --system gemini --out .../gemini_outputs.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
SENTS = os.path.join(HERE, 'sentences.json')

GEMINI_PROMPT = ("Translate the following Uzbek sentence to English. "
                 "Output ONLY the translation.\n\n{uz}")


def collect_system(rows):
    from dotenv import load_dotenv
    load_dotenv()
    from app import create_app
    from services.sentence_translator_v2 import sentence_translator_v2 as ST
    import subprocess
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=ROOT).decode().strip()
    app = create_app()
    out = {}
    with app.app_context():
        for r in rows:
            out[r['id']] = (ST.translate(r['uz']).get('translation') or '').strip()
    return out, {'system': 'kkt_sentence_translator_v2', 'commit': commit}


def collect_gemini(rows):
    from dotenv import load_dotenv
    load_dotenv()
    import google.generativeai as genai
    MODEL = 'gemini-2.5-flash'
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel(
        model_name=MODEL,
        generation_config=genai.types.GenerationConfig(temperature=0.0, max_output_tokens=1024),
    )
    out = {}
    for r in rows:
        resp = model.generate_content(GEMINI_PROMPT.format(uz=r['uz']))
        out[r['id']] = (resp.text or '').strip()
    return out, {'system': 'gemini', 'model': MODEL, 'temperature': 0.0,
                 'prompt': 'neutral: Translate ... Output ONLY the translation'}


def main():
    system = sys.argv[sys.argv.index('--system') + 1]
    outp = sys.argv[sys.argv.index('--out') + 1]
    sents = sys.argv[sys.argv.index('--sents') + 1] if '--sents' in sys.argv else SENTS
    rows = json.load(open(sents, encoding='utf-8'))
    if system == 'system':
        out, meta = collect_system(rows)
    elif system == 'gemini':
        out, meta = collect_gemini(rows)
    else:
        raise SystemExit('--system system|gemini')
    out['_meta'] = meta
    json.dump(out, open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"Saqlandi: {outp}  ({len(rows)} gap)  meta={meta}")


if __name__ == '__main__':
    main()
