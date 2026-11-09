# -*- coding: utf-8 -*-
"""TOLQIN-2 — veb/LLM kirish to'plamlari (tuzatish 1). READ-ONLY (faqat veb/kirish/ va veb/kalit.json yozadi).

    python3 analysis/tolqin-2/veb_paket.py

472 gap = `a_qavat_400.json` (400, fayl tartibida) + `evaluation/eval72/sentences.json` (72, fayl tartibida);
`random.Random(20261016).shuffle` bilan aralashtiriladi. Bitta aralash tartib ikkala to'plam turiga:
  - `veb/kirish/llm_01.txt` … `llm_12.txt` — 40 tadan (oxirgisi 32), qator `N. <o'zbekcha>` (N 1 dan);
  - `veb/kirish/gt_01.txt` … `gt_19.txt` — 25 tadan (oxirgisi 22), raqamsiz, har gap alohida qatorda.
Fayl UTF-8, `\n` bilan, oxirida `\n`. Belgi soni (Python `len`, oxirgi `\n` siz) > 5 000 bo'lsa ekranga
chiqariladi (to'plam hajmi o'zgartirilmaydi).
`veb/kalit.json`: fayl -> qator raqami -> {toplam, id}; har fayl sha256 va belgi soni.
"""
import hashlib
import json
import random
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
A_QAVAT, A_SHA = SIKL / 'a_qavat_400.json', '1e37f431c86a0b1c505655144806fbf2b37f31d445258c6a0d0b476e0604827c'
EVAL72, E_SHA = REPO / 'evaluation/eval72/sentences.json', '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
SEED = 20261016
VEB = SIKL / 'veb'
KIRISH = VEB / 'kirish'
TURLAR = (('llm', 40, 12), ('gt', 25, 19))
CHEGARA = 5000


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ab, eb = A_QAVAT.read_bytes(), EVAL72.read_bytes()
    assert sha(ab) == A_SHA and sha(eb) == E_SHA, 'kirish sha256 mos emas'
    gaplar = [('a_qavat', r['id'], r['uz']) for r in json.loads(ab)] + \
             [('eval72', r['id'], r['uz']) for r in json.loads(eb)]
    assert len(gaplar) == 472 and len({(t, i) for t, i, _ in gaplar}) == 472
    assert all('\n' not in u and u.strip() == u and u for _, _, u in gaplar), 'gapda qator ichi belgisi'
    random.Random(SEED).shuffle(gaplar)
    KIRISH.mkdir(parents=True, exist_ok=True)
    kalit = {'seed': SEED, 'jami': len(gaplar), 'fayllar': {}}
    for tur, hajm, soni in TURLAR:
        bolaklar = [gaplar[i:i + hajm] for i in range(0, len(gaplar), hajm)]
        assert len(bolaklar) == soni, (tur, len(bolaklar))
        for n, bolak in enumerate(bolaklar, 1):
            qatorlar = [f'{k}. {u}' if tur == 'llm' else u for k, (_, _, u) in enumerate(bolak, 1)]
            matn = '\n'.join(qatorlar)
            b = (matn + '\n').encode('utf-8')
            nom = f'{tur}_{n:02d}.txt'
            (KIRISH / nom).write_bytes(b)
            kalit['fayllar'][nom] = {'sha256': sha(b), 'qator_soni': len(bolak), 'belgi': len(matn),
                                     'qator': {str(k): {'toplam': t, 'id': i} for k, (t, i, _) in enumerate(bolak, 1)}}
            if len(matn) > CHEGARA:
                print(f'OSHDI: {nom} {len(matn)} belgi > {CHEGARA}')
    kb = (json.dumps(kalit, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    (VEB / 'kalit.json').write_bytes(kb)
    for tur, _, _ in TURLAR:
        b = [v['belgi'] for k, v in kalit['fayllar'].items() if k.startswith(tur + '_')]
        print(f'{tur}: {len(b)} fayl · belgi max {max(b)} · min {min(b)} · > {CHEGARA}: {sum(x > CHEGARA for x in b)}')
    print(f'kalit.json sha256 {sha(kb)}')


if __name__ == '__main__':
    main()
