# -*- coding: utf-8 -*-
"""CE1 — 72-gap tanlovi + PROVENANCE ISBOTI + LOCK (halollik protokol §2).

Qatlamlar (uzunlik-stratifikatsiya: qisqa <10 / o'rta 10-20 / uzun >20 uz-so'z):
  - FLORES devtest 36 (12/12/12) — TEST1-5 va flores_sentence_corpus dan TASHQARI
    (isbotlanadi). FLORES referens hech qachon tuning/lug'atda ishlatilmagan
    (oov_flores_extract FAQAT token-chastota oldi, referens/ma'no EMAS — o'z sarlavhasi).
  - train 24 (8/8/8) — inlibrary in-domen; train pattern-mining uchun ishlatilgan,
    referens-tuning EMAS (tuning=dev). Ceiling in-domen qatlami.
  - oltin 12 (4/4/4) — oltin_korpus_200 (tizim regressiya-gate'da KO'RGAN qatlam, kontrast).

Seed = 72 (hujjatlangan, reproduksiyalanadi). Chiqish: sentences.json + LOCK.txt.
BU GAPLAR BUNDAN KEYIN HECH QANDAY SOZLASHDA ISHLATILMAYDI.
"""
import json, os, sys, random, tarfile

SEED = 72
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.dirname(os.path.abspath(__file__))
TAR = os.path.join(ROOT, 'evaluation', 'corpus', '_flores_cache', 'flores200_dataset.tar.gz')


def norm(s):
    return ' '.join((s or '').strip().lower().split())


def wc(s):
    return len((s or '').split())


def length_bin(s):
    n = wc(s)
    return 'short' if n < 10 else ('medium' if n <= 20 else 'long')


def load_flores_devtest():
    with tarfile.open(TAR, 'r:gz') as tar:
        def lines(name):
            try:
                m = tar.getmember(name)
            except KeyError:
                m = tar.getmember('./' + name)
            return [ln.strip() for ln in tar.extractfile(m).read().decode('utf-8').splitlines() if ln.strip()]
        uz = lines("flores200_dataset/devtest/uzn_Latn.devtest")
        en = lines("flores200_dataset/devtest/eng_Latn.devtest")
    return list(zip(uz, en))


def load_exclusion():
    """TEST1-5 + flores_sentence_corpus barcha uz — FLORES tanlovidan chiqariladi."""
    excl = set()
    files = ['flores_test_corpus', 'flores_test2_corpus', 'flores_test3_corpus',
             'flores_test4_corpus', 'flores_test5_corpus', 'flores_sentence_corpus']
    per = {}
    for f in files:
        p = os.path.join(ROOT, 'evaluation', 'corpus', f + '.json')
        d = json.load(open(p, encoding='utf-8'))
        s = {norm(x['uzbek']) for x in d}
        per[f] = len(s)
        excl |= s
    return excl, per


def stratified_sample(pool, per_bin, rng):
    """pool: list of (uz, en). per_bin: {short,medium,long} soni. Har binda random.sample."""
    bins = {'short': [], 'medium': [], 'long': []}
    for uz, en in pool:
        bins[length_bin(uz)].append((uz, en))
    out = []
    for b, k in per_bin.items():
        avail = bins[b]
        if len(avail) < k:
            raise SystemExit(f"YETARLI EMAS bin={b}: kerak {k}, bor {len(avail)}")
        out += [(uz, en, b) for uz, en in rng.sample(avail, k)]
    return out


def main():
    rng = random.Random(SEED)
    excl, per = load_exclusion()

    # FLORES pool = devtest \ exclusion
    devtest = load_flores_devtest()
    flores_pool = [(uz, en) for uz, en in devtest if norm(uz) not in excl]
    flores = stratified_sample(flores_pool, {'short': 12, 'medium': 12, 'long': 12}, rng)

    # train (inlibrary in-domen)
    train = json.load(open(os.path.join(ROOT, 'corpus', 'uz_en_scitech.train.json'), encoding='utf-8'))
    train_pool = [(d['uz'], d['en']) for d in train]
    tr = stratified_sample(train_pool, {'short': 8, 'medium': 8, 'long': 8}, rng)

    # oltin (gold)
    gold = json.load(open(os.path.join(ROOT, 'oltin_korpus_200.json'), encoding='utf-8'))
    gold_pool = [(g[0], g[1]) if isinstance(g, list) else (g['uz'], g['en']) for g in gold]
    # oltin_korpus_200 BUTUNLAY qisqa (max 6 uz-so'z, sof-SVO) — stratifikatsiya
    # qo'llanmaydi (halol qayd); 12 qisqa gap olinadi.
    go = stratified_sample(gold_pool, {'short': 12, 'medium': 0, 'long': 0}, rng)

    rows = []
    for layer, sel in [('flores', flores), ('train', tr), ('gold', go)]:
        for i, (uz, en, b) in enumerate(sel):
            rows.append({'id': f"{layer}-{i:02d}", 'layer': layer, 'length_bin': b,
                         'uz_word_count': wc(uz), 'uz': uz, 'ref_en': en})

    # === PROVENANCE ISBOTI ===
    flores_uz = [norm(r['uz']) for r in rows if r['layer'] == 'flores']
    leaked = [u for u in flores_uz if u in excl]
    assert not leaked, f"BUZILISH: {len(leaked)} FLORES gap TEST1-5 da!"
    print("=== PROVENANCE ISBOTI ===")
    print(f"Exclusion to'plami (TEST1-5 + flores_sentence): {sum(per.values())} yozuv, {len(excl)} unik uz")
    for f, n in per.items():
        print(f"   {f}: {n}")
    print(f"FLORES devtest jami: {len(devtest)} | exclusion-dan tashqari pool: {len(flores_pool)}")
    print(f"Tanlangan 36 FLORES: {len(leaked)} tasi TEST1-5 da (0 kutiladi) -> ISBOT: TOZA held-out")
    print(f"FLORES referens tuning/lug'atda ishlatilmagan (oov_flores_extract token-only).")
    # length taqsimoti
    from collections import Counter
    for layer in ('flores', 'train', 'gold'):
        c = Counter(r['length_bin'] for r in rows if r['layer'] == layer)
        print(f"{layer}: n={sum(1 for r in rows if r['layer']==layer)}  bins={dict(c)}")

    json.dump(rows, open(os.path.join(OUT, 'sentences.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, 'LOCK.txt'), 'w', encoding='utf-8') as f:
        f.write("CE1 72-gap LOCK (halollik protokol §2)\n")
        f.write(f"Seed={SEED}. Tanlangan: 36 FLORES + 24 train + 12 oltin = {len(rows)} gap.\n")
        f.write("Bu gaplar BUNDAN KEYIN HECH QANDAY SOZLASH/tuning/lug'atda ISHLATILMAYDI.\n")
        f.write("FLORES 36: TEST1-5 + flores_sentence_corpus dan TASHQARI (isbotlangan).\n")
    print(f"\nSaqlandi: {OUT}/sentences.json ({len(rows)} gap) + LOCK.txt")


if __name__ == '__main__':
    main()
