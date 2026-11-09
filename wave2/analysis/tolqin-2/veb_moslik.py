# -*- coding: utf-8 -*-
"""TOLQIN-2 — veb javoblari moslik tekshiruvi (tuzatish 1). READ-ONLY (faqat veb/moslik.md dagi o'z bo'limini yozadi).
Javob MATNI hech qayerga CHIQARILMAYDI — faqat sonlar.

    python3 analysis/tolqin-2/veb_moslik.py gpt     # gpt_01..12
    python3 analysis/tolqin-2/veb_moslik.py gt      # gt_01..19

Har javob qatori `veb/kalit.json` orqali gap kalitiga ((toplam, id)) bog'lanadi: LLM fayl — `N.` raqami bo'yicha
(kirish `llm_NN.txt`), gt — qator o'rni bo'yicha (kirish `gt_NN.txt`). Tayanch: `claude_*` va `gemini_*` (gap kaliti
bo'yicha).
  1) jurnal.csv: shu tizim fayllari uchun bir nechta qator (vaqtlari) + fayl birth/mtime;
  2) dublikat: tizim fayllari orasida bayt-aynan juftlar (sha256) va eng o'xshash juft (butun matn chrF);
  3) moslik: fayl NN «o'z jufti» = qatorlari shu kirish gaplarining claude/gemini tarjimalari bilan (gap-chrF o'rtachasi);
     «boshqa» = fayl kirish MM (MM != NN) javobi deb faraz qilinib, qator i <-> MM kirishining i-gapi claude/gemini
     tarjimasi. OK — o'z jufti (claude ham, gemini ham) eng yaqin boshqadan katta; aks holda SHUBHA.
Natija `veb/moslik.md` dagi `<!-- tizim -->` bo'limiga (boshqa bo'limlar saqlanadi); ekranga shu bo'lim.
"""
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from itertools import combinations
from pathlib import Path

from sacrebleu.metrics import CHRF

SIKL = Path(__file__).resolve().parent
VEB = SIKL / 'veb'
RAQAM = re.compile(r'^\s*(\d+)\.\s*(.*)$')
TURLAR = {'gpt': ('llm', 12), 'claude': ('llm', 12), 'gemini': ('llm', 12), 'gt': ('gt', 19)}
chrf = CHRF()


def qatorlar(yol):
    m = yol.read_bytes().decode('utf-8')
    return [q.rstrip('\r') for q in m.split('\n') if q.strip()]


def oqi(tizim, nn, kalit):
    """{qator_o'rni(1..): gap_kaliti} va {gap_kaliti: matn}."""
    tur = TURLAR[tizim][0]
    k = kalit['fayllar'][f'{tur}_{nn}.txt']['qator']
    out = {}
    for i, q in enumerate(qatorlar(VEB / 'javob' / f'{tizim}_{nn}.txt'), 1):
        if tur == 'llm':
            r = RAQAM.match(q)
            if not r:
                continue
            i, q = int(r.group(1)), r.group(2)
        if str(i) in k:
            out.setdefault((k[str(i)]['toplam'], k[str(i)]['id']), q.strip())
    return out


def ort(juftlar):
    s = [chrf.sentence_score(h, [r]).score for h, r in juftlar]
    return sum(s) / len(s) if s else 0.0


def main():
    tizim = sys.argv[1] if len(sys.argv) > 1 else ''
    assert tizim in ('gpt', 'gt'), 'tizim: gpt | gt'
    tur, soni = TURLAR[tizim]
    kalit = json.loads((VEB / 'kalit.json').read_text(encoding='utf-8'))
    nnlar = [f'{i:02d}' for i in range(1, soni + 1)]
    bor = [nn for nn in nnlar if (VEB / 'javob' / f'{tizim}_{nn}.txt').exists()]
    tayanch = {}
    for t in ('claude', 'gemini'):
        tayanch[t] = {}
        for i in range(1, 13):
            if (VEB / 'javob' / f'{t}_{i:02d}.txt').exists():
                tayanch[t].update(oqi(t, f'{i:02d}', kalit))
    # kirish fayli -> qator o'rni -> gap kaliti
    kir = {nn: {int(i): (v['toplam'], v['id']) for i, v in kalit['fayllar'][f'{tur}_{nn}.txt']['qator'].items()}
           for nn in nnlar}
    L = [f'<!-- {tizim} -->', f'## {tizim} ({len(bor)}/{soni} fayl; tayanch claude {len(tayanch["claude"])}, '
                              f'gemini {len(tayanch["gemini"])} gap)', '']

    # 1) jurnal
    L.append('### 1. jurnal.csv')
    with open(VEB / 'jurnal.csv', encoding='utf-8', newline='') as f:
        jq = [r for r in csv.DictReader(f) if r['tizim'] == tizim]
    kop = {}
    for r in jq:
        kop.setdefault(r['fayl'], []).append(r['tugash'] or r['boshlanish'])
    L.append(f'- {tizim} qatorlari: {len(jq)} (fayl {len(kop)})')
    for fayl, v in sorted(kop.items()):
        if len(v) > 1:
            st = (VEB / 'javob' / fayl).stat()
            t = lambda x: dt.datetime.fromtimestamp(x).astimezone().isoformat(timespec='seconds')
            L.append(f'- {fayl}: {len(v)} qator — {", ".join(v)}; fayl birth {t(st.st_birthtime)}, mtime {t(st.st_mtime)}')
    L.append('')

    # 2) dublikat
    L.append('### 2. dublikat')
    sha = {nn: hashlib.sha256((VEB / 'javob' / f'{tizim}_{nn}.txt').read_bytes()).hexdigest() for nn in bor}
    aynan = [(a, b) for a, b in combinations(bor, 2) if sha[a] == sha[b]]
    L.append(f'- bayt-aynan juftlar: {len(aynan)}' + (': ' + ', '.join(f'{a}={b}' for a, b in aynan) if aynan else ''))
    matn = {nn: '\n'.join(qatorlar(VEB / 'javob' / f'{tizim}_{nn}.txt')) for nn in bor}
    oxsh = sorted(((chrf.sentence_score(matn[a], [matn[b]]).score, a, b) for a, b in combinations(bor, 2)), reverse=True)
    if oxsh:
        L.append(f'- eng o\'xshash juft (butun matn chrF): {oxsh[0][1]}–{oxsh[0][2]} {oxsh[0][0]:.1f}; '
                 f'ikkinchisi {oxsh[1][1]}–{oxsh[1][2]} {oxsh[1][0]:.1f}' if len(oxsh) > 1 else '')
        L.append(f'- chrF >= 60 juftlar: {sum(s >= 60 for s, _, _ in oxsh)}')
    L.append('')

    # 3) moslik
    L.append('### 3. moslik (gap-chrF o\'rtachasi)')
    L.append('')
    shubha = 0
    for nn in bor:
        j = oqi(tizim, nn, kalit)
        orni = {i: j[g] for i, g in kir[nn].items() if g in j}           # qator o'rni -> javob
        oz = {t: ort([(orni[i], tayanch[t][kir[nn][i]]) for i in orni if kir[nn][i] in tayanch[t]])
              for t in ('claude', 'gemini')}
        boshqa = []
        for mm in nnlar:
            if mm == nn:
                continue
            for t in ('claude', 'gemini'):
                jj = [(orni[i], tayanch[t][kir[mm][i]]) for i in orni if i in kir[mm] and kir[mm][i] in tayanch[t]]
                if jj:
                    boshqa.append((ort(jj), f'{t}_{mm}'))
        eng = max(boshqa) if boshqa else (0.0, '-')
        ok = min(oz.values()) > eng[0]
        shubha += not ok
        L.append(f'- {nn}: o\'z jufti claude {oz["claude"]:.1f} / gemini {oz["gemini"]:.1f}, '
                 f'eng yaqin boshqa {eng[0]:.1f} ({eng[1]}) — {"OK" if ok else "SHUBHA"}')
    L += ['', f'Jami: OK {len(bor) - shubha}, SHUBHA {shubha}', f'<!-- /{tizim} -->']

    bolim = '\n'.join(L)
    md = VEB / 'moslik.md'
    eski = md.read_text(encoding='utf-8') if md.exists() else \
        '# TOLQIN-2 — veb javoblari moslik tekshiruvi\n\n`veb_moslik.py` chiqishi; javob matni yo\'q, faqat sonlar.\n'
    naqsh = re.compile(rf'<!-- {tizim} -->.*?<!-- /{tizim} -->', re.S)
    yangi = naqsh.sub(lambda _: bolim, eski) if naqsh.search(eski) else eski.rstrip('\n') + '\n\n' + bolim
    md.write_text(yangi.rstrip('\n') + '\n', encoding='utf-8')
    print(bolim)


if __name__ == '__main__':
    main()
