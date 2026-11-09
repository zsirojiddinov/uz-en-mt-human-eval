# -*- coding: utf-8 -*-
"""TOLQIN-2 — 2-rasm: gap-BLEU (1 etalon) va asosiy guruh o'rtacha mazmuni, 5 panel (tizim bo'yicha). NATIJADAN KEYINGI,
qo'lyozma v1.2 rasmi, tadqiqotchi so'rovi 2026-10-29 (Q11); yangi statistika yo'q. Muzlatilgan tahlil.py ga tegmaydi — undan
yukla(), gap_bleu(), ort10(), spearman(), TIZIMLAR, CHIQ7 import qilinadi. natija/ va qoshimcha/taqriz_qoshimcha.json faqat O'QILADI.

    ~/.venvs/tolqin2_rasm/bin/python -I analysis/tolqin-2/qoshimcha/fig2_bleu_adequacy.py   # bir marta; rasm/*.json mavjud bo'lsa TO'XTAYDI

Muhit: ~/.venvs/tolqin2_rasm (Python 3.9.6; sacrebleu 2.6.0, openpyxl 3.1.5, numpy 1.26.4, matplotlib 3.9.4) — COMET venv'iga
matplotlib qo'shilmadi.
Nuqtalar: ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7), har tizimda 71 element. x = gap-BLEU_1ref (eval72 ref_en, tahlil.gap_bleu);
y = asosiy guruh (natija «ishlatilgan»: B, C, D) mazmun o'rtachasi, yo'q kataklar chiqarilgan (tuzatish 10 (g), tahlil.ort10).
Har panelda ρ va 95 % CI — Q10 3-band (taqriz_qoshimcha.json = natija H4 ASOSIY 71, «tizim ichida»); qayta hisoblangan ρ shu
qiymat bilan tekshiriladi (assert). Bootstrap qayta yurilmaydi.
Chiqish: qoshimcha/rasm/fig2_bleu_adequacy.png (300 dpi), qoshimcha/rasm/fig2_bleu_adequacy.json (nuqtalar va ρ).
"""
import importlib.util
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CHIQ = Path(__file__).resolve().parent
SIKL = CHIQ.parent
RASM = CHIQ / 'rasm'
_sp = importlib.util.spec_from_file_location('tahlil_muzlatilgan', str(SIKL / 'tahlil.py'))
T = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(T)
RANG = '#2a5d8f'


def main():
    if (RASM / 'fig2_bleu_adequacy.json').exists():
        sys.exit("TO'XTA: qoshimcha/rasm/fig2_bleu_adequacy.json mavjud — bir marta yuriladi")
    _, B, chiq, _, kb, xom, *_ = T.yukla(SIKL, T.REPO / 'evaluation/eval72/sentences.json')
    nat = json.loads((SIKL / 'natija' / 'tahlil_natija.json').read_text(encoding='utf-8'))
    q10 = json.loads((CHIQ / 'taqriz_qoshimcha.json').read_text(encoding='utf-8'))['3_tizim_ichida_rho']['tizim']
    ish = nat['baholovchilar']['ishlatilgan']
    assert ish == ['B', 'C', 'D']
    ref = {r['id']: r['ref_en'] for r in B}
    bh = {x: {str(r[0]): (T._i(r[1]), T._i(r[2])) for r in xom[x]} for x in ish}
    el = kb['elementlar']
    R = {'maqom': "natijadan keyingi, qo'lyozma rasmi, 2026-10-29; yangi statistika yo'q",
         'baholovchilar': ish, 'toplam': 'ASOSIY 71 (gold-00 chiqarilgan)', 'rho_manba': 'qoshimcha/taqriz_qoshimcha.json 3-band (= natija H4 ASOSIY 71)',
         'tizim': {}}
    for t in T.TIZIMLAR:
        ee = sorted(e for e in el if el[e]['tizim'] == t and el[e]['id'] not in T.CHIQ7)
        x = [T.gap_bleu(chiq[t][('eval72', el[e]['id'])], [ref[el[e]['id']]]) for e in ee]
        y = [T.ort10(bh, ish, e, 0) for e in ee]
        rho = T.spearman(x, y)
        assert len(ee) == q10[t]['n'] == 71 and abs(rho - q10[t]['spearman']) < 1e-12, f'{t}: Q10 ρ bilan teng emas'
        R['tizim'][t] = {'n': len(ee), 'spearman': q10[t]['spearman'], 'ci95': q10[t]['ci95'],
                         'nuqtalar': [{'element': e, 'id': el[e]['id'], 'gap_bleu': a, 'mazmun': b} for e, a, b in zip(ee, x, y)]}

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.linewidth': 0.6,
                         'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'svg.hashsalt': 'tolqin2'})
    fig, ax = plt.subplots(1, 5, figsize=(7.2, 1.9), sharex=True, sharey=True)
    for a, t in zip(ax, T.TIZIMLAR):
        v = R['tizim'][t]
        a.scatter([p['gap_bleu'] for p in v['nuqtalar']], [p['mazmun'] for p in v['nuqtalar']],
                  s=5, color=RANG, alpha=0.7, linewidths=0, clip_on=False)
        a.set_title(t, fontsize=8.5, pad=14)
        f = lambda z: f'{z:.2f}'.replace('-', '−')
        a.text(0.5, 1.02, f"ρ = {f(v['spearman'])} [{f(v['ci95'][0])}, {f(v['ci95'][1])}]", transform=a.transAxes,
               ha='center', va='bottom', fontsize=6.5, color='#444444')
        a.set_xlim(-3, 103)
        a.set_ylim(0.85, 5.15)
        a.set_xticks([0, 50, 100])
        a.set_yticks([1, 2, 3, 4, 5])
        a.grid(color='#e3e3e3', linewidth=0.4)
        a.set_axisbelow(True)
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
    ax[0].set_ylabel('Mean adequacy (B, C, D)')
    fig.supxlabel('Sentence BLEU (1 reference)', fontsize=8, y=0.02)
    fig.tight_layout(pad=0.4, w_pad=0.6)
    RASM.mkdir(exist_ok=True)
    fig.savefig(RASM / 'fig2_bleu_adequacy.png', dpi=300, metadata={'Software': None})
    (RASM / 'fig2_bleu_adequacy.json').write_text(json.dumps(R, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    print('qoshimcha/rasm/: fig2_bleu_adequacy.png, .json')


if __name__ == '__main__':
    main()
