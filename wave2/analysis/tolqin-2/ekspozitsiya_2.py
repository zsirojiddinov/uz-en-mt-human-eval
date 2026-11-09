# -*- coding: utf-8 -*-
"""TOLQIN-2 — EKSPOZITSIYA-2 (reja: ekspozitsiya_2_reja.md, 5d5f2a9). READ-ONLY; faqat ekspozitsiya_2.json yozadi.
Gap MATNI hech qayerga yozilmaydi va chiqarilmaydi — faqat ID, son, yo'l, commit.

    python3 analysis/tolqin-2/ekspozitsiya_2.py

Nishon: 472 manba gap (a_qavat_400.json 400 + evaluation/eval72/sentences.json 72) — ID (toplam, id).
Qo'shimcha nishon (3-band): FLORES-200 uzn_Latn dev 997 + devtest 1 012 (tar keshidan).
Normallashtirish: apostrof variantlari -> ', kichik harf, Unicode P*/S* -> bo'shliq (so'z ichidagi ' saqlanadi),
bo'shliqlar yig'iladi. Aniq = normallashtirilgan matn teng; yaqin = 5-gram Jaccard >= 0,5 (ikkalasi >= 5 so'z) YOKI
8+ so'zli umumiy uzluksiz ketma-ketlik.
1-band: nomlangan to'plamlar (2 119, 2 477, 2 597, 3 301, SINOV-4…7) o'z kodlari/fayllaridan + barcha ishchi
daraxtlardagi (main, git worktree'lar, ~/kkt_arxiv, ~/kkt_langarlar, ~/kkt_morf2_kalit) matnli fayllar
(json/jsonl/gz/tsv/csv/txt/md/py/…, xlsx/docx ichidagi matn) — har fayl bir «to'plam», kontent sha256 bo'yicha takrorsiz.
2-band: git rev-list --all --objects dagi barcha blob'lar (= git log --all -p dagi barcha qo'shilgan/o'chirilgan
mazmun) + barcha commit xabarlari; topilgan ID uchun birinchi commit (--find-object, eng eski).
Chiqarib tashlanadi (ta'rifan mos): analysis/tolqin-2/**, evaluation/eval72/sentences.json, FLORES keshi.
"""
import gzip
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]                              # tolqin-2 worktree
MAIN = Path.home() / 'PyCharmMiscProject'
QOSHIMCHA = [Path.home() / n for n in ('kkt_arxiv', 'kkt_langarlar', 'kkt_morf2_kalit')]
APOS = dict.fromkeys(map(ord, "ʻʼ‘’`´′ʹʽ‛"), "'")
TASHLA_PAPKA = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.idea', '.pytest_cache', '.mypy_cache'}
MATN_KENG = {'.json', '.jsonl', '.tsv', '.csv', '.txt', '.md', '.py', '.sh', '.html', '.yml', '.yaml', '.xml', '.tex',
             '.log', '.sql', '.js', '.dart', '.ipynb', '.cfg', '.ini', '.toml', '.sha256', ''}
MAX_BAYT = 200_000_000


def norm_tok(s):
    s = unicodedata.normalize('NFC', s).translate(APOS).lower()
    s = ''.join(' ' if (unicodedata.category(c)[0] in 'PS' and c != "'") else c for c in s)
    return [t.strip("'") for t in s.split() if t.strip("'")]


def chiqarilgan(yol):
    y = str(yol).replace('\\', '/')
    oz = f'{SIKL.parent.name}/{SIKL.name}'          # o'z sikl papkasi (tolqin-2)
    return (y.startswith(oz + '/') or f'/{oz}/' in y or y.endswith('evaluation/eval72/sentences.json')
            or '_flores_cache' in y or 'flores200_dataset' in y)


class Indeks:
    def __init__(self, nishonlar):                  # nishonlar: {ID: matn}
        self.aniq, self.g5, self.g8, self.n5 = defaultdict(set), defaultdict(set), defaultdict(set), {}
        for i, m in nishonlar.items():
            t = norm_tok(m)
            self.aniq[' '.join(t)].add(i)
            s5 = {tuple(t[k:k + 5]) for k in range(len(t) - 4)}
            self.n5[i] = len(s5)
            for g in s5:
                self.g5[g].add(i)
            for k in range(len(t) - 7):
                self.g8[tuple(t[k:k + 8])].add(i)

    def mos(self, matn):
        """-> (aniq ID lar, yaqin ID lar)"""
        t = norm_tok(matn)
        if not t:
            return set(), set()
        a = set(self.aniq.get(' '.join(t), ()))
        y = set()
        for k in range(len(t) - 7):
            y |= self.g8.get(tuple(t[k:k + 8]), set())
        if len(t) >= 5:
            s5 = {tuple(t[k:k + 5]) for k in range(len(t) - 4)}
            ov = defaultdict(int)
            for g in s5:
                for i in self.g5.get(g, ()):
                    ov[i] += 1
            for i, o in ov.items():
                if self.n5[i] and o / (len(s5) + self.n5[i] - o) >= 0.5:
                    y.add(i)
        return a, y - a


def satrlar(b, nom):
    """bayt -> matn bo'laklari (nomzodlar). Binar -> []."""
    nom = nom.lower()
    if nom.endswith('.gz'):
        try:
            b = gzip.decompress(b)
        except Exception:
            return []
        nom = nom[:-3]
    if nom.endswith(('.xlsx', '.docx', '.pptx')):
        try:
            z = zipfile.ZipFile(io.BytesIO(b))
            out = []
            for n in z.namelist():
                if n.endswith('.xml'):
                    x = z.read(n).decode('utf-8', 'replace')
                    out += [m for m in re.findall(r'>([^<>]+)<', x) if m.strip()]
                    for p in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):     # paragraf butun holda
                        out.append(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
            return out
        except Exception:
            return []
    if b'\x00' in b[:8192]:
        return []
    try:
        s = b.decode('utf-8')
    except UnicodeDecodeError:
        s = b.decode('utf-8', 'replace')
    out = []
    if nom.endswith(('.json', '.ipynb')):
        try:
            def yur(o):
                if isinstance(o, str):
                    out.append(o)
                elif isinstance(o, dict):
                    for k, v in o.items():
                        out.append(k)
                        yur(v)
                elif isinstance(o, list):
                    for v in o:
                        yur(v)
            yur(json.loads(s))
            return out
        except Exception:
            pass
    for q in s.splitlines():
        out.append(q)
        if '\t' in q:
            out += q.split('\t')
        if nom.endswith('.jsonl'):
            try:
                o = json.loads(q)
                out += [v for v in (o.values() if isinstance(o, dict) else []) if isinstance(v, str)]
            except Exception:
                pass
    return out


def skan(b, nom, ix):
    a, y = set(), set()
    for m in satrlar(b, nom):
        if len(m) < 15:
            continue
        aa, yy = ix.mos(m)
        a |= aa
        y |= yy
    return a, y - a


def _modul(yol, nom):
    sp = importlib.util.spec_from_file_location(nom, str(yol))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def nomlangan():
    """{nom: [(kalit, matn)]} — nomlangan to'plamlar o'z kodlari/fayllaridan (main daraxt)."""
    for y in (MAIN, MAIN / 'analysis', MAIN / 'analysis' / 'versiya-1', MAIN / 'analysis' / '_konvensiya'):
        sys.path.insert(0, str(y))
    out = {}
    pop = json.loads((MAIN / 'analysis/echo1_skan.json').read_text(encoding='utf-8'))['gaplar']
    out['2119 (echo1_skan.json)'] = [(f"{g['toplam']}|{g['indeks']}", g['uz']) for g in pop]
    m1008 = _modul(MAIN / 'analysis/merge-1008/surat.py', 'm1008_surat').gaplar()
    out['2477 vaqt (merge-1008/surat.py gaplar(): 2119+58+300; icite-2026 imlo_radius normallashtir_ms)'] = \
        [(f'{t}|{k}', g) for t, k, g in m1008]
    s4 = [json.loads(q) for q in (MAIN / 'analysis/sinov-4/toplam.jsonl').read_text(encoding='utf-8').splitlines() if q.strip()]
    out['2597 (triaj-1/db-sifat-1 populyatsiyasi: 2477 + sinov-4 120)'] = \
        out['2477 vaqt (merge-1008/surat.py gaplar(): 2119+58+300; icite-2026 imlo_radius normallashtir_ms)'] + \
        [(f"s4|{g['id']}", g['matn']) for g in s4]
    cwd = os.getcwd()
    os.chdir(MAIN)
    try:
        kir = _modul(MAIN / 'analysis/imlo-2/surat.py', 'imlo2_surat').kirishlar()
    finally:
        os.chdir(cwd)
    out['3301 imlo darvozasi (imlo-2/surat.py kirishlar())'] = [(k, t['text']) for k, _, t in kir]
    out['SINOV-4 (sinov-4/toplam.jsonl)'] = [(str(g['id']), g['matn']) for g in s4]
    s5 = [json.loads(q) for q in (MAIN / 'analysis/sinov-5/toplam.jsonl').read_text(encoding='utf-8').splitlines() if q.strip()]
    out['SINOV-5 (sinov-5/toplam.jsonl)'] = [(str(g['id']), g['matn']) for g in s5]
    for s in ('sinov-6', 'sinov-7'):
        f = sorted(p.name for p in (MAIN / 'analysis' / s).iterdir())
        out[f'{s.upper()} (gaplar yig\'ilmagan: {", ".join(f)})'] = []
    return out


def daraxtlar():
    r = subprocess.run(['git', '-C', str(MAIN), 'worktree', 'list', '--porcelain'], capture_output=True, text=True, check=True)
    w = [Path(q.split(' ', 1)[1]) for q in r.stdout.splitlines() if q.startswith('worktree ')]
    return w + [p for p in QOSHIMCHA if p.exists()]


def toifa(yol):
    y = yol.lower()
    if y.startswith('tests/') or 'fixture' in y or '/test_' in y or y.startswith('test_'):
        return 'test/fixture'
    if y.startswith(('data/', 'database/')) or 'lugat' in y or "lug'at" in y or y.endswith('.db'):
        return "data/lug'at"
    if y.startswith(('services/', 'app', 'routes/', 'models/')):
        return 'kod'
    bosh = y.split('/', 1)[0]
    return bosh if bosh in ('analysis', 'evaluation', 'corpus') and '/' in y else 'boshqa'


def main():
    ab = (SIKL / 'a_qavat_400.json').read_bytes()
    eb = (REPO / 'evaluation/eval72/sentences.json').read_bytes()
    assert hashlib.sha256(ab).hexdigest() == '1e37f431c86a0b1c505655144806fbf2b37f31d445258c6a0d0b476e0604827c'
    assert hashlib.sha256(eb).hexdigest() == '29cf6da34dbfa207a234bc08c25bd34b4171f5f5c1db9aca407c117140abf0ce'
    N = {f"a_qavat|{r['id']}": r['uz'] for r in json.loads(ab)}
    N.update({f"eval72|{r['id']}": r['uz'] for r in json.loads(eb)})
    assert len(N) == 472
    ix = Indeks(N)
    F = {}
    with tarfile.open(MAIN / 'evaluation/corpus/_flores_cache/flores200_dataset.tar.gz') as tf:
        for m in tf.getmembers():
            for bo in ('dev', 'devtest'):
                if m.name.endswith(f'{bo}/uzn_Latn.{bo}'):
                    for i, q in enumerate(tf.extractfile(m).read().decode('utf-8').splitlines()):
                        F[f'{bo}|{i}'] = q
    assert len(F) == 997 + 1012, len(F)
    fx = Indeks(F)
    # ijobiy nazorat: nishonning o'zi topiladi, tasodifiy gap topilmaydi
    assert all(i in ix.mos(m)[0] for i, m in N.items())
    assert ix.mos('Bu gap hech qayerda yo\'q va shunchaki nazorat uchun yozilgan tasodifiy matn bo\'lagi.') == (set(), set())
    nat = {'reja_commit': '5d5f2a9', 'nishon': {'a_qavat': 400, 'eval72': 72}, 'flores': len(F)}

    # 1-band (a): nomlangan to'plamlar
    nom = {}
    for k, el in nomlangan().items():
        a, y = set(), set()
        el_a = el_y = 0
        for _, m in el:
            aa, yy = ix.mos(m)
            el_a += bool(aa)
            el_y += bool(yy - aa) and not aa
            a |= aa
            y |= yy
        fa, fy = set(), set()
        for _, m in el:
            aa, yy = fx.mos(m)
            fa |= aa
            fy |= yy
        nom[k] = {'element': len(el), 'aniq_id': sorted(a), 'yaqin_id': sorted(y - a), 'aniq_element': el_a,
                  'yaqin_element': el_y, 'flores_aniq': len(fa), 'flores_yaqin': len(fy - fa)}
        print(f'[1a] {k}: element {len(el)} · aniq {len(a)} · yaqin {len(y - a)} · FLORES {len(fa)}/{len(fy - fa)}', flush=True)
    nat['nomlangan'] = nom

    # 1-band (b): ishchi daraxtlar
    korilgan, fayl_nat = {}, {}
    flores_d = (set(), set())
    jami_fayl = 0
    for d in daraxtlar():
        for dp, dn, fn in os.walk(d):
            dn[:] = [x for x in dn if x not in TASHLA_PAPKA]
            for f in fn:
                p = Path(dp) / f
                rel = str(p.relative_to(d))
                kn = p.suffix.lower()
                if chiqarilgan(rel) or not (kn in MATN_KENG or f.endswith(('.gz', '.xlsx', '.docx', '.pptx'))):
                    continue
                try:
                    if p.is_symlink() or p.stat().st_size > MAX_BAYT:
                        continue
                    b = p.read_bytes()
                except OSError:
                    continue
                jami_fayl += 1
                h = hashlib.sha256(b).hexdigest()
                joy = f'{d.name}:{rel}'
                if h in korilgan:
                    if korilgan[h] in fayl_nat:
                        fayl_nat[korilgan[h]]['nusxa'].append(joy)
                    continue
                korilgan[h] = joy
                a, y = skan(b, f, ix)
                fa, fy = skan(b, f, fx)
                flores_d[0].update(fa)
                flores_d[1].update(fy)
                if a or y:
                    fayl_nat[joy] = {'aniq_id': sorted(a), 'yaqin_id': sorted(y), 'nusxa': [], 'toifa': toifa(rel)}
    nat['ishchi_daraxt'] = {'daraxtlar': [str(d) for d in daraxtlar()], 'fayl_korildi': jami_fayl,
                            'noyob_mazmun': len(korilgan), 'topilgan_fayl': fayl_nat,
                            'flores_aniq': len(flores_d[0]), 'flores_yaqin': len(flores_d[1] - flores_d[0])}
    print(f'[1b] fayl {jami_fayl} · noyob {len(korilgan)} · topilgan {len(fayl_nat)}', flush=True)

    # 2-band: git tarixi (barcha blob'lar) + commit xabarlari
    G = ['git', '-C', str(MAIN)]
    obj = subprocess.run(G + ['rev-list', '--all', '--objects'], capture_output=True, text=True, check=True).stdout
    yol = {}
    for q in obj.splitlines():
        if ' ' in q:
            s, p = q.split(' ', 1)
            yol.setdefault(s, p)
    nomzod = [(s, p) for s, p in yol.items() if not chiqarilgan(p)
              and (Path(p).suffix.lower() in MATN_KENG or p.endswith(('.gz', '.xlsx', '.docx', '.pptx')))]
    bat = subprocess.Popen(G + ['cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    blob_nat, gf = {}, (set(), set())
    for s, p in nomzod:
        bat.stdin.write((s + '\n').encode())
        bat.stdin.flush()
        bosh = bat.stdout.readline().split()
        if len(bosh) < 3:                            # «<sha> missing»
            continue
        n = int(bosh[2])
        b = bat.stdout.read(n)                      # mazmun HAR DOIM o'qiladi (tree ham) — oqim siljimasin
        bat.stdout.read(1)
        if bosh[1] != b'blob' or n > MAX_BAYT:
            continue
        a, y = skan(b, p, ix)
        fa, fy = skan(b, p, fx)
        gf[0].update(fa)
        gf[1].update(fy)
        if a or y:
            blob_nat[s] = {'yol': p, 'aniq_id': sorted(a), 'yaqin_id': sorted(y), 'toifa': toifa(p)}
    bat.stdin.close()
    bat.wait()
    print(f'[2] blob {len(nomzod)} · topilgan {len(blob_nat)}', flush=True)
    birinchi = {}
    for s in blob_nat:
        r = subprocess.run(G + ['log', '--all', '--format=%h %cI', f'--find-object={s}'], capture_output=True, text=True).stdout.split('\n')
        r = [x for x in r if x.strip()]
        if r:
            birinchi[s] = min(r, key=lambda x: x.split()[1])
            blob_nat[s]['birinchi_commit'] = birinchi[s]
    idlar = defaultdict(list)
    for s, v in blob_nat.items():
        for i in v['aniq_id'] + v['yaqin_id']:
            idlar[i].append((v.get('birinchi_commit', '? ?').split()[1], v.get('birinchi_commit', '? ?').split()[0], v['yol'], v['toifa'],
                             'aniq' if i in v['aniq_id'] else 'yaqin'))
    id_birinchi = {i: min(v) for i, v in idlar.items()}
    toifa_id = defaultdict(set)
    for s, v in blob_nat.items():
        for i in v['aniq_id'] + v['yaqin_id']:
            toifa_id[v['toifa']].add(i)
    log = subprocess.run(G + ['log', '--all', '--format=%h%x00%cI%x00%B%x1e'], capture_output=True, text=True, check=True).stdout
    xabar = {}
    xf = (set(), set())
    nxabar = 0
    for blk in log.split('\x1e'):
        if '\x00' not in blk:
            continue
        nxabar += 1
        h, t, m = blk.strip('\n').split('\x00', 2)
        a, y = set(), set()
        for q in [m] + m.splitlines():
            if len(q) >= 15:
                aa, yy = ix.mos(q)
                a |= aa
                y |= yy
                fa, fy = fx.mos(q)
                xf[0].update(fa)
                xf[1].update(fy)
        if a or y:
            xabar[h] = {'sana': t, 'aniq_id': sorted(a), 'yaqin_id': sorted(y - a)}
    nat['git'] = {'blob_korildi': len(nomzod), 'blob_topilgan': blob_nat, 'id_birinchi': {i: list(v) for i, v in id_birinchi.items()},
                  'toifa_id': {k: sorted(v) for k, v in toifa_id.items()}, 'commit_xabar_korildi': nxabar, 'commit_xabar_topilgan': xabar,
                  'flores_blob_aniq': len(gf[0]), 'flores_blob_yaqin': len(gf[1] - gf[0]),
                  'flores_xabar_aniq': len(xf[0]), 'flores_xabar_yaqin': len(xf[1] - xf[0])}
    fl_all = (flores_d[0] | gf[0] | xf[0])
    fl_yaq = (flores_d[1] | gf[1] | xf[1]) - fl_all
    nat['flores_umumiy'] = {'aniq': len(fl_all), 'yaqin': len(fl_yaq),
                            'aniq_dev': sum(i.startswith('dev|') for i in fl_all), 'aniq_devtest': sum(i.startswith('devtest|') for i in fl_all)}
    print(f'[2] xabar {nxabar} · topilgan {len(xabar)}; FLORES aniq {len(fl_all)} yaqin {len(fl_yaq)}', flush=True)
    b = (json.dumps(nat, ensure_ascii=False, indent=1, sort_keys=True) + '\n').encode('utf-8')
    (SIKL / 'ekspozitsiya_2.json').write_bytes(b)
    print('ekspozitsiya_2.json sha256', hashlib.sha256(b).hexdigest())


if __name__ == '__main__':
    main()
