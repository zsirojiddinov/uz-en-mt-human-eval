# -*- coding: utf-8 -*-
"""TOLQIN-2 — HELD-OUT XESH RO'YXATI. READ-ONLY; faqat held_out_hash.json yozadi.
Gap MATNI chiqarilmaydi va yozilmaydi (yagona istisno — o'ylab topilgan «nazorat» gapi).

    python3 analysis/tolqin-2/held_out_hash.py

Maqsad: boshqa sessiya (main) hook'i matn ko'rmasdan held-out gaplarni ushlashi uchun xeshlar.
Normallashtirish: ekspozitsiya_2.py dagi `norm_tok` (ekspozitsiya_2_reja.md) — import qilinadi, nusxa emas.
Gap xeshi = sha256(' '.join(norm_tok(gap)).encode('utf-8')); oyna xeshi = har 8 ketma-ket token uchun xuddi shunday.
  qattiq: a_qavat_400 (400) + FLORES-200 dev uzn_Latn (997, hammasi) + nazorat gapi
  kirish: eval72 (72) + FLORES-200 devtest uzn_Latn (1 012, hammasi)
Oxirida 10 holatli hook sinovi (tekshir() — hook uchun namunaviy mantiq); 10/10 bo'lmasa fayl yozilmaydi.
"""
import hashlib
import importlib.util
import inspect
import json
import sys
import tarfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
MAIN = Path.home() / 'PyCharmMiscProject'
TAR = MAIN / 'evaluation/corpus/_flores_cache/flores200_dataset.tar.gz'
CHIQ = SIKL / 'held_out_hash.json'
OYNA = 8
NAZORAT = "Qashqadaryo vohasidagi keksa bog'bon har bahorda o'rik ko'chatlarini kumush rangli ip bilan bog'lab chiqadi."

_spec = importlib.util.spec_from_file_location('ekspozitsiya_2', SIKL / 'ekspozitsiya_2.py')
_eks = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_eks)
norm_tok = _eks.norm_tok


def sha(b):
    return hashlib.sha256(b).hexdigest()


def gap_xesh(tok):
    return sha(' '.join(tok).encode('utf-8'))


def oynalar(tok):
    return {gap_xesh(tok[k:k + OYNA]) for k in range(len(tok) - OYNA + 1)}


def royxat(gaplar):
    g, o, qisqa = set(), set(), 0
    for m in gaplar:
        t = norm_tok(m)
        assert t, 'bo\'sh gap'
        g.add(gap_xesh(t))
        o |= oynalar(t)
        qisqa += len(t) < OYNA
    return g, o, qisqa


def tekshir(matn, ro):
    """Hook mantiqi namunasi: -> {'qattiq'|'kirish': 'gap'|'oyna'} (bo'sh = toza).
    Har qator va butun matn gap xeshi bilan; butun matn token oqimi 8-oynalar bilan."""
    t = norm_tok(matn)
    gx = {gap_xesh(norm_tok(q)) for q in [matn, *matn.splitlines()] if norm_tok(q)}
    ox = oynalar(t)
    nat = {}
    for k, v in ro.items():
        if gx & set(v['gap']):
            nat[k] = 'gap'
        elif ox & set(v['oyna']):
            nat[k] = 'oyna'
    return nat


def main():
    ab = (SIKL / 'a_qavat_400.json').read_bytes()
    eb = (REPO / 'evaluation/eval72/sentences.json').read_bytes()
    tb = TAR.read_bytes()
    assert sha(ab) == '1e37f431c86a0b1c505655144806fbf2b37f31d445258c6a0d0b476e0604827c'
    assert sha(eb) == '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
    A = [r['uz'] for r in json.loads(ab)]
    E = [r['uz'] for r in json.loads(eb)]
    assert (len(A), len(E)) == (400, 72)
    F, fsha = {}, {}
    with tarfile.open(TAR) as tf:
        for m in tf.getmembers():
            for bo in ('dev', 'devtest'):
                if m.name.endswith(f'{bo}/uzn_Latn.{bo}'):
                    b = tf.extractfile(m).read()
                    fsha[m.name] = sha(b)
                    F[bo] = b.decode('utf-8').splitlines()
    assert (len(F['dev']), len(F['devtest'])) == (997, 1012)

    # nazorat gapi hech bir to'plamda (gap ham, oyna ham) yo'qligi
    hamma = A + E + F['dev'] + F['devtest']
    ng, no, _ = royxat([NAZORAT])
    hg, ho, _ = royxat(hamma)
    assert len(norm_tok(NAZORAT)) >= OYNA and not (ng & hg) and not (no & ho)

    qg, qo, qq = royxat(A + F['dev'] + [NAZORAT])
    kg, ko, kq = royxat(E + F['devtest'])
    to = {}
    for nom, gaplar in (('a_qavat_400', A), ('flores_dev', F['dev']), ('eval72', E), ('flores_devtest', F['devtest'])):
        g, o, q = royxat(gaplar)
        to[nom] = {'gap': len(gaplar), 'gap_xesh_takrorsiz': len(g), 'oyna_xesh_takrorsiz': len(o),
                   f'qisqa_lt_{OYNA}_soz': q}
    ro = {'qattiq': {'gap': sorted(qg), 'oyna': sorted(qo)}, 'kirish': {'gap': sorted(kg), 'oyna': sorted(ko)}}

    # hook sinovi — 10 holat (matn chop etilmaydi)
    import random
    r = random.Random(20261020)
    a, fd = r.choice(A), r.choice([q for q in F['dev'] if q not in set(A)])
    e, fdt = r.choice(E), r.choice([q for q in F['devtest'] if len(norm_tok(q)) >= 12])
    tdt = fdt.split()
    sinov = [
        ('nazorat aynan', NAZORAT, {'qattiq': 'gap'}),
        ('nazorat boshqa matn ichida', 'Kecha yozdim: ' + NAZORAT + ' Keyin uxladim.', {'qattiq': 'oyna'}),
        ('a_qavat gapi', a, {'qattiq': 'gap'}),
        ('FLORES dev (a_qavatdan tashqari)', fd, {'qattiq': 'gap'}),
        ('a_qavat gapi: katta harf, ’ apostrof, tinish', a.upper().replace("'", '’') + ' !!', {'qattiq': 'gap'}),
        ('eval72 gapi', e, {'kirish': 'gap'}),
        ('FLORES devtest gapi', fdt, {'kirish': 'gap'}),
        ('devtest 9 so\'zli bo\'lagi matn ichida', 'Masalan, ' + ' '.join(tdt[1:10]) + ' degan edi.', {'kirish': 'oyna'}),
        ('nazoratning 7 so\'zli bo\'lagi', ' '.join(NAZORAT.split()[:7]), {}),
        ('o\'ylab topilgan toza matn', "Bugun ertalab kutubxonaga borib, yangi lug'at kitobini varaqlab ko'rdim.", {}),
    ]
    ok = 0
    for i, (nom, matn, kut) in enumerate(sinov, 1):
        nat = tekshir(matn, ro)
        ok += nat == kut
        print(f'[hook {i:2d}] {"OK  " if nat == kut else "FAIL"} {nom}: kutilgan {kut} · natija {nat}')
    print(f'hook {ok}/{len(sinov)}')
    if ok != len(sinov):
        sys.exit(1)

    chiq = {
        'sikl': 'tolqin-2',
        'sana': datetime.now(timezone(timedelta(hours=5))).isoformat(timespec='seconds'),
        'skript': 'analysis/tolqin-2/held_out_hash.py',
        'normallashtirish': {
            'manba': 'analysis/tolqin-2/ekspozitsiya_2.py: norm_tok (ekspozitsiya_2_reja.md, «Normallashtirish»)',
            'tavsif': ("NFC; apostrof variantlari ʻʼ‘’`´′ʹʽ‛ -> '; Unicode lower; Unicode P*/S* toifasi (' dan tashqari) "
                       "-> bo'shliq; bo'shliq bo'yicha bo'linadi; tokenlar chetidagi ' kesiladi, bo'sh tokenlar tashlanadi"),
            'kod': ('import unicodedata\nAPOS = ' + inspect.getsource(_eks).split('APOS = ', 1)[1].split('\n', 1)[0]
                    + '\n\n' + inspect.getsource(norm_tok)),
            'gap_xesh': "sha256(' '.join(norm_tok(gap)).encode('utf-8')).hexdigest()",
            'oyna_xesh': f"har k uchun sha256(' '.join(norm_tok(gap)[k:k+{OYNA}]).encode('utf-8')).hexdigest(); "
                         f"< {OYNA} tokenli gapda oyna yo'q (faqat gap xeshi)",
            'hook_tavsiya': ("matnning har qatori va butun matni gap xeshi bilan, butun matn token oqimi "
                             f"{OYNA}-oynalar bilan solishtiriladi (held_out_hash.py: tekshir)"),
        },
        'manba_sha256': {
            'analysis/tolqin-2/a_qavat_400.json': sha(ab),
            'evaluation/eval72/sentences.json': sha(eb),
            'evaluation/corpus/_flores_cache/flores200_dataset.tar.gz': sha(tb),
            **{f'tar:{k}': v for k, v in sorted(fsha.items())},
        },
        'toplamlar': to,
        'royxat_soni': {
            'qattiq': {'toplamlar': ['a_qavat_400', 'flores_dev', 'nazorat'], 'gap_xesh': len(qg), 'oyna_xesh': len(qo),
                       f'qisqa_lt_{OYNA}_soz': qq},
            'kirish': {'toplamlar': ['eval72', 'flores_devtest'], 'gap_xesh': len(kg), 'oyna_xesh': len(ko),
                       f'qisqa_lt_{OYNA}_soz': kq},
        },
        'nazorat': {'matn': NAZORAT, 'gap_xesh': sorted(ng)[0], 'oyna_xesh': sorted(no),
                    'izoh': "o'ylab topilgan; 4 to'plamning hech birida gap ham, 8-oyna ham yo'q (tekshirildi); "
                            "xeshlari «qattiq» ro'yxatda"},
        'hook_sinov': f'{ok}/{len(sinov)}',
        'qattiq': ro['qattiq'],
        'kirish': ro['kirish'],
    }
    CHIQ.write_text(json.dumps(chiq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{CHIQ.name} sha256 {sha(CHIQ.read_bytes())}')
    print(json.dumps({'toplamlar': to, 'royxat_soni': chiq['royxat_soni']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
