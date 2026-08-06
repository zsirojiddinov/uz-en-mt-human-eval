# -*- coding: utf-8 -*-
"""AN1 — RW1 INSON-BAHOLASH TO'LIQ TAHLIL-QUVURI (bitta buyruq, uch bosqich).

Pre-registratsiya: `analysis/rw1_prereg_analysis_plan.md` dagi qulflangan qarorlar.
Bu skript inson-datadan OLDIN quriladi/muzlatiladi; data kelgach FAQAT ishga tushiriladi.
Tizim kodi/DB/metric-freeze TEGILMAYDI. scipy'siz (numpy + qo'l-statistika).

Kirish:
  evaluation/eval72/returns/rater_*_filled.xlsx   (2 yoki 3; "Baholash" varag'i)
  evaluation/eval72/metric_scores.json            (216: BLEU/chrF/KKT-v1/KKT-v2)
  evaluation/eval72/blind_key.json                (item_id -> gap_id, system)

Chiqish:
  analysis/human_eval_results.md + evaluation/eval72/results_tables.json

Ishlatish:
  python evaluation/eval72/analyze_human_eval.py            # real (returns/ dan)
  python evaluation/eval72/analyze_human_eval.py --dry-run  # SINTETIK mexanika-sinovi
"""
import json, os, sys, glob, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RETURNS = os.path.join(HERE, 'returns')
N_ITEMS = 216
BOOT_N = 1000
BOOT_SEED = 20260703
DRY_SEED = 4242

_YOQ = "yo'q"
METRICS = [('bleu', 'BLEU'), ('chrf', 'chrF'), ('kkt_rs_v1', 'KKT-RS-v1'), ('kkt_rs_v2', 'KKT-RS-v2')]
SYSTEMS = ['s1', 's2', 'gemini', 'google_translate', 'claude', 'chatgpt']  # metric_scores'da bor tizimlar

# ---------------------------------------------------------------------------
# STATISTIKA (scipy'siz)
# ---------------------------------------------------------------------------
def _ranks(a):
    a = np.asarray(a, float); n = len(a)
    order = np.argsort(a, kind='mergesort'); r = np.empty(n)
    i = 0
    while i < n:
        j = i
        while j + 1 < n and a[order[j + 1]] == a[order[i]]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1
        i = j + 1
    return r


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 2 or x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    if len(x) < 2:
        return float('nan')
    return pearson(_ranks(x), _ranks(y))


def kendall_tau(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    if n < 2:
        return float('nan')
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])
            if s > 0:
                c += 1
            elif s < 0:
                d += 1
    return (c - d) / (0.5 * n * (n - 1)) if n > 1 else float('nan')


def bootstrap_ci(fn, n_items, n=BOOT_N, seed=BOOT_SEED):
    """fn(idx_array)->skalyar; item-resample percentil 95% CI (2.5, 97.5)."""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        idx = rng.integers(0, n_items, n_items)
        v = fn(idx)
        if v == v:  # not nan
            vals.append(v)
    if not vals:
        return (float('nan'), float('nan'))
    return (round(float(np.percentile(vals, 2.5)), 3), round(float(np.percentile(vals, 97.5)), 3))


# ---------------------------------------------------------------------------
# KIRISH
# ---------------------------------------------------------------------------
def load_context():
    metric = json.load(open(os.path.join(HERE, 'metric_scores.json'), encoding='utf-8'))
    blind = json.load(open(os.path.join(HERE, 'blind_key.json'), encoding='utf-8'))
    layer = {r['id']: r['layer'] for r in json.load(open(os.path.join(HERE, 'sentences.json'), encoding='utf-8'))}
    return metric, blind, layer


def read_rater_xlsx(path):
    """{'item_id': (mazmun|None, ravonlik|None)} + xatolar ro'yxati."""
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb['Baholash'] if 'Baholash' in wb.sheetnames else wb[wb.sheetnames[-1]]
    hdr = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    def col(name):
        return next((i + 1 for i, h in enumerate(hdr) if h and name.lower() in str(h).lower()), None)
    ci, cm, cr = col('item_id'), col('Mazmun'), col('Ravonlik')
    out, errs = {}, []
    for row in range(2, ws.max_row + 1):
        iid = ws.cell(row, ci).value if ci else None
        if not iid:
            continue
        def val(cc):
            v = ws.cell(row, cc).value if cc else None
            if v is None or (isinstance(v, str) and not v.strip()):
                return None, 'bo\'sh'
            try:
                iv = int(v)
            except (ValueError, TypeError):
                return None, f'son emas ({v!r})'
            if iv < 1 or iv > 5:
                return None, f'1-5 dan tashqari ({iv})'
            return iv, None
        m, em = val(cm); r, er = val(cr)
        if em:
            errs.append((str(iid), 'Mazmun', em))
        if er:
            errs.append((str(iid), 'Ravonlik', er))
        out[str(iid)] = (m, r)
    return out, errs


def load_raters(dry_run, blind):
    """{rater_id: {item_id: (mazmun,ravonlik)}}, per_rater_errors. Dry-run: sintetik."""
    if dry_run:
        rng = random.Random(DRY_SEED)
        raters = {}
        for R in ('A', 'B', 'C'):
            raters[R] = {iid: (rng.randint(1, 5), rng.randint(1, 5)) for iid in blind}
        return raters, {R: [] for R in raters}, 'SINTETIK (dry-run)'
    files = sorted(glob.glob(os.path.join(RETURNS, 'rater_*_filled.xlsx')))
    raters, errors = {}, {}
    for f in files:
        rid = os.path.basename(f).replace('rater_', '').replace('_filled.xlsx', '')
        data, errs = read_rater_xlsx(f)
        # item_id qamrovi
        missing = [i for i in blind if i not in data]
        for i in missing:
            errs.append((i, '-', 'qator yo\'q'))
        raters[rid] = data
        errors[rid] = errs
    return raters, errors, 'REAL'


# ---------------------------------------------------------------------------
# BOSQICHLAR
# ---------------------------------------------------------------------------
def stage_validate(raters, errors, blind):
    """Nuqsonli itemlar (biror baholovchida bo'sh/xato Mazmun) -> asosiy hisobdan chiqadi."""
    defective = set()
    for rid, errs in errors.items():
        for iid, field, _ in errs:
            if field in ('Mazmun', '-'):
                defective.add(iid)
    valid = [i for i in blind if i not in defective]
    return valid, sorted(defective), errors


def _human_mazmun(raters, valid, use=None):
    """{item_id: o'rtacha Mazmun} — use=None (hammasi) yoki baholovchi ro'yxati."""
    rids = use if use is not None else list(raters)
    out = {}
    for iid in valid:
        vals = [raters[r][iid][0] for r in rids if iid in raters[r] and raters[r][iid][0] is not None]
        if vals:
            out[iid] = sum(vals) / len(vals)
    return out


def stage_consensus(raters, valid):
    rids = sorted(raters)
    def col(rid, which):  # which: 0 mazmun, 1 ravonlik
        return [raters[rid][i][which] for i in valid]
    pair = {}
    for a in range(len(rids)):
        for b in range(a + 1, len(rids)):
            ra, rb = rids[a], rids[b]
            xa = [raters[ra][i][0] for i in valid]; xb = [raters[rb][i][0] for i in valid]
            ya = [raters[ra][i][1] for i in valid]; yb = [raters[rb][i][1] for i in valid]
            pair[f"{ra}-{rb}"] = {'mazmun': round(spearman(xa, xb), 3), 'ravonlik': round(spearman(ya, yb), 3)}
    # har baholovchining o'rtacha juftlik-Spearman (mazmun)
    mean_pair = {}
    for r in rids:
        vals = [v['mazmun'] for k, v in pair.items() if r in k.split('-')]
        mean_pair[r] = round(sum(vals) / len(vals), 3) if vals else float('nan')
    # PRE-REG outlier-band: 1 baholovchi <0.40 va qolgan juftliklar >=0.60
    trigger = None
    for r in rids:
        others = [v['mazmun'] for k, v in pair.items() if r not in k.split('-')]
        if mean_pair[r] < 0.40 and others and min(others) >= 0.60:
            trigger = r
    return pair, mean_pair, trigger


def stage_probe_s1s2(raters, blind):
    """s1==s2 bayt-aynan gaplarda baholovchi-izchillik: bir xil chiqishga Mazmun-farqi o'rtachasi."""
    s1 = {k: v for k, v in json.load(open(os.path.join(HERE, 's1_outputs.json'))).items() if k != '_meta'}
    s2 = {k: v for k, v in json.load(open(os.path.join(HERE, 's2_outputs.json'))).items() if k != '_meta'}
    same_gaps = [g for g in s1 if s1[g] == s2.get(g)]
    # gap -> (item_s1, item_s2)
    rev = {}
    for iid, meta in blind.items():
        rev.setdefault(meta['gap_id'], {})[meta['system']] = iid
    diffs = {r: [] for r in raters}
    npairs = 0
    for g in same_gaps:
        m = rev.get(g, {})
        if 's1' in m and 's2' in m:
            npairs += 1
            for r in raters:
                a = raters[r].get(m['s1'], (None,))[0]; b = raters[r].get(m['s2'], (None,))[0]
                if a is not None and b is not None:
                    diffs[r].append(abs(a - b))
    return {r: (round(sum(d) / len(d), 3) if d else float('nan')) for r, d in diffs.items()}, npairs


def stage_correlation(raters, valid, metric, blind, layer, use_raters, tag):
    human = _human_mazmun(raters, valid, use=use_raters)
    hum_rav = {iid: (lambda v: sum(v) / len(v) if v else None)(
        [raters[r][iid][1] for r in (use_raters or raters) if iid in raters[r] and raters[r][iid][1] is not None])
        for iid in valid}
    items = [i for i in valid if i in human]

    def metvec(mkey, idx):
        return [metric[f"{blind[items[k]]['gap_id']}::{blind[items[k]]['system']}"][mkey] for k in idx]

    def humvec(idx):
        return [human[items[k]] for k in idx]

    allidx = np.arange(len(items))
    tables = {'tag': tag, 'n_items': len(items), 'boot_seed': BOOT_SEED, 'boot_n': BOOT_N,
              'segment_spearman': {}, 'segment_pearson': {}, 'per_layer': {}, 'diff_ci': {},
              'low_bleu_kendall': {}, 'system_level': {}}
    # asosiy: segment-Spearman + Pearson + bootstrap CI
    rho = {}
    for mkey, mname in METRICS:
        mv, hv = metvec(mkey, allidx), humvec(allidx)
        sp = spearman(mv, hv); pe = pearson(mv, hv)
        ci = bootstrap_ci(lambda idx, mk=mkey: spearman(metvec(mk, idx), humvec(idx)), len(items))
        rho[mkey] = sp
        tables['segment_spearman'][mname] = {'rho': round(sp, 3), 'ci95': ci}
        tables['segment_pearson'][mname] = round(pe, 3)
    # farq-CI (v2 - BLEU, v2 - chrF) — pre-reg muvaffaqiyat-mezoni
    for other in ('bleu', 'chrf'):
        oname = dict(METRICS)[other]
        d = rho['kkt_rs_v2'] - rho[other]
        ci = bootstrap_ci(lambda idx, o=other: spearman(metvec('kkt_rs_v2', idx), humvec(idx))
                          - spearman(metvec(o, idx), humvec(idx)), len(items))
        tables['diff_ci'][f'KKT-RS-v2 − {oname}'] = {'delta': round(d, 3), 'ci95': ci,
                                                     'excludes_0': (ci[0] > 0 or ci[1] < 0)}
    # per-qatlam
    for L in ('flores', 'train', 'gold'):
        lidx = [k for k in range(len(items)) if layer[blind[items[k]]['gap_id']] == L]
        tables['per_layer'][L] = {'n': len(lidx)}
        for mkey, mname in METRICS:
            if len(lidx) >= 3:
                tables['per_layer'][L][mname] = round(spearman([metvec(mkey, [k])[0] for k in lidx],
                                                                [humvec([k])[0] for k in lidx]), 3)
            else:
                tables['per_layer'][L][mname] = None
    # BLEU<10 kichik-to'plam Kendall-tau (past-ball rejim)
    low = [k for k in range(len(items)) if metric[f"{blind[items[k]]['gap_id']}::{blind[items[k]]['system']}"]['bleu'] < 10]
    tables['low_bleu_kendall']['n'] = len(low)
    if len(low) >= 3:
        for mkey, mname in METRICS:
            tables['low_bleu_kendall'][mname] = round(kendall_tau([metvec(mkey, [k])[0] for k in low],
                                                                  [humvec([k])[0] for k in low]), 3)
    # tizim-darajali: har tizim o'rtacha inson-Mazmun + metrika o'rtachalari
    for sysn in SYSTEMS:
        s_items = [k for k in range(len(items)) if blind[items[k]]['system'] == sysn]
        if not s_items:
            continue
        rec = {'n': len(s_items), 'human_mazmun': round(np.mean([humvec([k])[0] for k in s_items]), 3)}
        for mkey, mname in METRICS:
            rec[mname] = round(np.mean([metvec(mkey, [k])[0] for k in s_items]), 3)
        tables['system_level'][sysn] = rec
    return tables, hum_rav


# ---------------------------------------------------------------------------
# HISOBOT
# ---------------------------------------------------------------------------
def write_report(md_path, json_path, ctx, dry_run):
    banner = ("> ⚠️ **SYNTHETIC DRY-RUN — mexanika sinovi, natija EMAS.** Ballar tasodifiy "
              f"(seed={DRY_SEED}) generatsiya qilingan; hech qanday inson-baho emas.\n\n") if dry_run else ""
    L = []
    L.append(f"# RW1 — INSON-BAHOLASH TAHLIL NATIJALARI{' (DRY-RUN)' if dry_run else ''}\n")
    L.append(banner)
    L.append(f"**Rejim:** {ctx['tag']} · **Sana:** 2026-07-03 · **Baholovchilar:** {', '.join(ctx['raters'])} "
             f"· pre-reg: `analysis/rw1_prereg_analysis_plan.md`\n")
    L.append("## 0. Validatsiya\n")
    L.append(f"- Baholovchi fayllari: {len(ctx['raters'])} ta.")
    L.append(f"- Nuqsonli item (biror baholovchida Mazmun bo'sh/xato) -> asosiy hisobdan chiqdi: "
             f"**{len(ctx['defective'])}** ({', '.join(ctx['defective'][:15]) or _YOQ}).")
    L.append(f"- Valid item: **{ctx['n_valid']}** / {N_ITEMS}.")
    for rid, errs in ctx['errors'].items():
        if errs:
            L.append(f"  - rater {rid}: {len(errs)} xato-katak -> {errs[:8]}")
    L.append("\n## 1. Baholovchilararo kelishuv (juftlik-Spearman)\n")
    L.append("| Juftlik | Mazmun | Ravonlik |\n|---|---|---|")
    for k, v in ctx['pair'].items():
        L.append(f"| {k} | {v['mazmun']} | {v['ravonlik']} |")
    L.append(f"\nHar baholovchi o'rtacha juftlik-Spearman (Mazmun): {ctx['mean_pair']}")
    if ctx['trigger']:
        L.append(f"\n**★ PRE-REG OUTLIER-BAND ISHGA TUSHDI:** baholovchi **{ctx['trigger']}** "
                 f"(o'rtacha <0.40, qolgan juftlik ≥0.60). Asosiy=3 baholovchi + sensitivity={ctx['trigger']}siz "
                 "(ikkalasi quyida). Vaznlash YO'Q.")
    else:
        L.append("\nPre-reg outlier-band ishga tushmadi (chetlashtirish yo'q).")
    L.append(f"\ns1==s2 bayt-aynan probasi ({ctx['probe_n']} juftlik): baholovchi Mazmun-farqi o'rtachasi "
             f"{ctx['probe']} (0 ga yaqin = izchil).\n")

    def corr_block(t, title):
        out = [f"## {title}  (n={t['n_items']}, bootstrap {t['boot_n']}, seed={t['boot_seed']})\n"]
        out.append("**Table 2 — Segment-daraja korrelyatsiya (inson Mazmun ↔ metrika):**\n")
        out.append("| Metrika | Spearman ρ | 95% CI | Pearson r |\n|---|---|---|---|")
        for _, mn in METRICS:
            s = t['segment_spearman'][mn]; p = t['segment_pearson'][mn]
            out.append(f"| {mn} | {s['rho']} | [{s['ci95'][0]}, {s['ci95'][1]}] | {p} |")
        out.append("\n**Farq-CI (pre-reg muvaffaqiyat-mezoni — 0 ni istisno qilsa v2 aniq ustun):**\n")
        out.append("| Farq | Δρ | 95% CI | 0 istisno? |\n|---|---|---|---|")
        for k, v in t['diff_ci'].items():
            out.append(f"| {k} | {v['delta']} | [{v['ci95'][0]}, {v['ci95'][1]}] | {'HA' if v['excludes_0'] else _YOQ} |")
        out.append("\n**Per-qatlam Spearman (Mazmun):**\n")
        out.append("| Qatlam | n | " + " | ".join(mn for _, mn in METRICS) + " |\n|" + "---|" * (2 + len(METRICS)))
        for Lr in ('flores', 'train', 'gold'):
            pl = t['per_layer'][Lr]
            out.append(f"| {Lr} | {pl['n']} | " + " | ".join(str(pl[mn]) for _, mn in METRICS) + " |")
        out.append(f"\n**BLEU<10 kichik-to'plam Kendall-τ (past-ball rejim, n={t['low_bleu_kendall'].get('n')}):** "
                   + ", ".join(f"{mn}={t['low_bleu_kendall'].get(mn)}" for _, mn in METRICS))
        out.append("\n\n**Table 3 — Tizim-darajali (o'rtacha inson-Mazmun vs metrika o'rtachalari):**\n")
        out.append("| Tizim | n | inson-Mazmun | " + " | ".join(mn for _, mn in METRICS) + " |\n|"
                   + "---|" * (3 + len(METRICS)))
        for sysn, rec in t['system_level'].items():
            out.append(f"| {sysn} | {rec['n']} | {rec['human_mazmun']} | "
                       + " | ".join(str(rec[mn]) for _, mn in METRICS) + " |")
        return "\n".join(out) + "\n"

    L.append(corr_block(ctx['main'], "2. KORRELYATSIYA — ASOSIY (barcha baholovchi)"))
    if ctx.get('sensitivity'):
        L.append(banner)  # dry-run bo'lsa har sahifada
        L.append(corr_block(ctx['sensitivity'], f"3. SENSITIVITY — {ctx['trigger']}siz (pre-reg band)"))

    open(md_path, 'w', encoding='utf-8').write("\n".join(L))
    json.dump({'main': ctx['main'], 'sensitivity': ctx.get('sensitivity'),
               'consensus': {'pair': ctx['pair'], 'mean_pair': ctx['mean_pair'], 'trigger': ctx['trigger']},
               'validation': {'defective': ctx['defective'], 'n_valid': ctx['n_valid']},
               'dry_run': dry_run}, open(json_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main():
    dry_run = '--dry-run' in sys.argv
    metric, blind, layer = load_context()

    if not dry_run and not (os.path.isdir(RETURNS) and glob.glob(os.path.join(RETURNS, 'rater_*_filled.xlsx'))):
        print(">>> INSON-DATA YO'Q (evaluation/eval72/returns/rater_*_filled.xlsx topilmadi).")
        print(">>> Quvur MUZLATILGAN va tayyor. Data kelgach shu buyruqni ishga tushiring.")
        print(">>> Mexanika sinovi uchun: --dry-run")
        return

    raters, errors, tag = load_raters(dry_run, blind)
    if len(raters) < 2:
        print(f"XATO: kamida 2 baholovchi kerak (topildi: {len(raters)}).")
        return

    valid, defective, errors = stage_validate(raters, errors, blind)
    pair, mean_pair, trigger = stage_consensus(raters, valid)
    probe, probe_n = stage_probe_s1s2(raters, blind)

    main_tbl, _ = stage_correlation(raters, valid, metric, blind, layer, use_raters=None, tag=tag)
    sens_tbl = None
    if trigger:
        keep = [r for r in raters if r != trigger]
        sens_tbl, _ = stage_correlation(raters, valid, metric, blind, layer, use_raters=keep, tag=tag + f" (−{trigger})")

    ctx = {'tag': tag, 'raters': sorted(raters), 'defective': defective, 'n_valid': len(valid),
           'errors': errors, 'pair': pair, 'mean_pair': mean_pair, 'trigger': trigger,
           'probe': probe, 'probe_n': probe_n, 'main': main_tbl, 'sensitivity': sens_tbl}

    suffix = '_dryrun' if dry_run else ''
    md = os.path.join(ROOT, 'analysis', f'human_eval_results{suffix}.md')
    js = os.path.join(HERE, f'results_tables{suffix}.json')
    write_report(md, js, ctx, dry_run)
    print(f"Yozildi: {md}\n         {js}")

    if dry_run:
        # PASS-tekshiruvlar, keyin _dryrun fayllarni O'CHIRISH
        checks = []
        checks.append(('validatsiya bosqichi', len(valid) == N_ITEMS))  # sintetikda hammasi valid
        checks.append(('kelishuv (3 juftlik)', len(pair) == 3))
        checks.append(('probe hisoblandi', probe_n > 0))
        checks.append(('asosiy jadval (4 metrika)', len(main_tbl['segment_spearman']) == 4))
        checks.append(('farq-CI (2)', len(main_tbl['diff_ci']) == 2))
        checks.append(('per-qatlam (3)', len(main_tbl['per_layer']) == 3))
        checks.append(('tizim-daraja', len(main_tbl['system_level']) >= 3))
        checks.append(('md+json yozildi', os.path.exists(md) and os.path.exists(js)))
        ok = all(v for _, v in checks)
        print("\n=== DRY-RUN PASS-TEKSHIRUV ===")
        for name, v in checks:
            print(f"  [{'PASS' if v else 'FAIL'}] {name}")
        print(f"NATIJA: {'DRY-RUN PASS ✓' if ok else 'DRY-RUN FAIL ✗'}")
        os.remove(md); os.remove(js)
        print("(_dryrun fayllar o'chirildi — sintetik natija saqlanmaydi)")
        return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main() or 0)
