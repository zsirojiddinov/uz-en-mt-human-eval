#!/bin/sh
# TOLQIN-2 — Claude Code sessiyalari javoblarini yig'ish (tuzatish 1). Javob MATNI ekranga CHIQARILMAYDI.
#
#   sh analysis/tolqin-2/claude_yigish.sh            # NN = 01..12
#   sh analysis/tolqin-2/claude_yigish.sh 03 07      # faqat berilganlar
#
# Har NN uchun:
#   - ~/tarjima_claude/javob_NN.txt -> veb/javob/claude_NN.txt (bayt-aynan). Nishon bor va aynan — o'tkaziladi;
#     bor va FARQLI — ustiga yozilmaydi, ogohlantiradi;
#   - ~/.claude/projects/ ostidagi tarjima_claude papkasiga tegishli sessiya transkriptlari (*.jsonl, papka nomi
#     `-Users-<foydalanuvchi>-tarjima-claude…`) ichidan javob_NN.txt ni YOZGAN sessiya topiladi (Write/Edit/Bash
#     tool_use kirishida `javob_NN.txt`); undan model identifikatori (assistant `message.model`), sessiya id va vaqt
#     (birinchi/oxirgi yozuv) olinib veb/jurnal.csv ga qator qo'shiladi (claude_NN.txt qatori allaqachon bo'lsa — qo'shilmaydi);
#   - tekshir_javob.py — faqat «OK» yoki muammo (masalan «yetishmaydi: 7, 12»).
set -eu
SIKL=$(cd "$(dirname "$0")" && pwd)
exec python3 - "$SIKL" "$@" <<'PY'
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

SIKL = Path(sys.argv[1])
VEB = SIKL / 'veb'
MANBA = Path.home() / 'tarjima_claude'
LOYIHA = Path.home() / '.claude' / 'projects'
nnlar = sys.argv[2:] or [f'{i:02d}' for i in range(1, 13)]
prefiks = str(MANBA).replace('/', '-').replace('_', '-')     # ~/tarjima_claude -> -Users-…-tarjima-claude


def mahalliy(ts):
    return dt.datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone().isoformat(timespec='seconds')


def sessiyalar():
    """{NN: [(sessiya, modellar, boshi, oxiri, transkript)]} — javob_NN.txt ni yozgan sessiyalar."""
    out = {}
    papkalar = [p for p in LOYIHA.glob('*') if p.is_dir() and (p.name == prefiks or p.name.startswith(prefiks + '-'))]
    for jl in sorted(f for p in papkalar for f in p.glob('*.jsonl')):
        modellar, vaqtlar, yozgan, sid = [], [], set(), None
        for q in jl.read_text(encoding='utf-8', errors='replace').splitlines():
            try:
                d = json.loads(q)
            except ValueError:
                continue
            if d.get('timestamp'):
                vaqtlar.append(d['timestamp'])
            sid = sid or d.get('sessionId')
            m = d.get('message') if isinstance(d.get('message'), dict) else {}
            if d.get('type') == 'assistant' and m.get('model') and m['model'] != '<synthetic>':
                if m['model'] not in modellar:
                    modellar.append(m['model'])
            for c in m.get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'tool_use':
                    kir = json.dumps(c.get('input', {}), ensure_ascii=False)
                    for nn in nnlar:
                        if f'javob_{nn}.txt' in kir:
                            yozgan.add(nn)
        for nn in yozgan:
            out.setdefault(nn, []).append((sid or jl.stem, modellar, min(vaqtlar) if vaqtlar else '',
                                           max(vaqtlar) if vaqtlar else '', jl))
    return out


jurnal = VEB / 'jurnal.csv'
mavjud = {q.split(',')[1] for q in jurnal.read_text(encoding='utf-8').splitlines()[1:] if q.count(',') >= 1}
ses = sessiyalar()
yomon = 0
for nn in nnlar:
    fayl = f'claude_{nn}.txt'
    manba, nishon = MANBA / f'javob_{nn}.txt', VEB / 'javob' / fayl
    if not manba.exists():
        print(f"{fayl}: manba yo'q (~/tarjima_claude/javob_{nn}.txt)")
        continue
    if nishon.exists() and nishon.read_bytes() != manba.read_bytes():
        print(f'{fayl}: OGOHLANTIRISH — veb/javob da bor va FARQLI, ustiga yozilmaydi')
        yomon += 1
        continue
    if not nishon.exists():
        nishon.write_bytes(manba.read_bytes())
    s = ses.get(nn, [])
    if fayl not in mavjud:
        if s:
            sid, modellar, boshi, oxiri, jl = s[-1]
            mtn = ' + '.join(modellar) or "noma'lum"
            izoh = (f'Claude Code sessiya {sid}; model {mtn}; transkript {jl.name}'
                    + (f'; javob_{nn}.txt ni yozgan sessiyalar {len(s)} ta' if len(s) > 1 else ''))
            qator = ['claude', fayl, mahalliy(boshi) if boshi else '', mahalliy(oxiri) if oxiri else '', izoh]
        else:
            qator = ['claude', fayl, '', '', 'Claude Code; transkript topilmadi (model noma\'lum)']
        with open(jurnal, 'a', encoding='utf-8') as f:
            f.write(','.join(x.replace(',', ';') for x in qator) + '\n')
    r = subprocess.run([sys.executable, str(SIKL / 'tekshir_javob.py'), str(nishon)], capture_output=True, text=True)
    h = (r.stdout.strip().splitlines() or ['?'])[-1].split('— ', 1)[-1]
    yomon += h != 'OK'
    model = ' + '.join(s[-1][1]) if s and s[-1][1] else "transkript yo'q"
    print(f'{fayl}: {h} · model {model}' + (f' · sessiya {len(s)} ta' if len(s) > 1 else ''))
sys.exit(1 if yomon else 0)
PY
