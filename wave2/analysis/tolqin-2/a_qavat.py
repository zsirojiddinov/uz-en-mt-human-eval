# -*- coding: utf-8 -*-
"""TOLQIN-2 — A-qavat: FLORES-200 dev dan 400 gap (prereg 2.2). READ-ONLY (faqat a_qavat_400.json yozadi).

    python3 analysis/tolqin-2/a_qavat.py           # -> analysis/tolqin-2/a_qavat_400.json (+ sha256 ekranga)

Manba: `evaluation/corpus/_flores_cache/flores200_dataset.tar.gz` (git-ignored; eval72 va savol-1 MANIFEST'idagi
kesh; asl manzil https://dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz), a'zolar
`flores200_dataset/dev/uzn_Latn.dev` va `flores200_dataset/dev/eng_Latn.dev` (997 qator, bir xil tartib).
Har uchala sha256 tekshiriladi.

Chiqarish: YOQISH-2 dagi 50 FLORES dev gapi — `analysis/yoqish-2/uzun.json` (`qator`, 1 dan) va
`analysis/yoqish-2/held_out.json` (`manba == flores_dev`, `uz`). Ikkala kalit bir xil 50 qatorni berishi,
qolgan pool aynan 947 bo'lishi SHART (aks holda to'xtaydi).

Tanlov: pool dev fayl tartibida; `random.Random(20261016).sample(pool, 400)`, so'ng dev qatori bo'yicha
saralanadi. `id` = `dev-NNN` (NNN — dev faylidagi 1 dan boshlangan qator raqami, 3 xonali).

Ekspozitsiya (KKT): `database/oov_florescl.json` dagi 78 so'z (2026-06-16, merge 1a4a11f). Tokenlash:
probel bo'yicha, kichik harf, tutuq belgilari ʻ ʼ ‘ ’ ` -> ', chekka tinish belgilari olib tashlanadi
(TOLQIN-2 INVENTAR-2 §2 bilan aynan). `aynan` — token so'zga teng; `prefiks` — so'z >= 4 harf va token
shu so'z bilan boshlanadi (aynanni ham o'z ichiga oladi).
"""
import hashlib
import json
import random
import tarfile
from pathlib import Path

SIKL = Path(__file__).resolve().parent
REPO = SIKL.parents[1]
TAR = REPO / 'evaluation/corpus/_flores_cache/flores200_dataset.tar.gz'
TAR_SHA = 'b8b0b76783024b85797e5cc75064eb83fc5288b41e9654dabc7be6ae944011f6'
UZ_A, UZ_SHA = 'flores200_dataset/dev/uzn_Latn.dev', '08175c04d6d4518108245e89c89bc5789515f335677729715a784def4fc1c7d7'
EN_A, EN_SHA = 'flores200_dataset/dev/eng_Latn.dev', '51a25f527fd81f428b6933d85a2f5e5544af92aa82042c7fbf0c4120327fba0a'
SOZLAR = REPO / 'database/oov_florescl.json'
SOZLAR_SHA = '62c052fc988ec5dd7325f6bdc21e5c30828cb67e1e26d0684ecbefe8f227a013'
SEED, N, POOL_N = 20261016, 400, 947
CHIQ = SIKL / 'a_qavat_400.json'
TUTUQ = 'ʻʼ‘’`'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def norm(s):
    return ' '.join((s or '').strip().lower().split())


def tokenlar(uz):
    out = []
    for t in uz.split():
        t = t.lower()
        for a in TUTUQ:
            t = t.replace(a, "'")
        out.append(t.strip('.,;:()"!?«»“”[]-—–'))
    return out


def dev_qatorlar():
    assert sha(TAR.read_bytes()) == TAR_SHA, 'tar sha256 mos emas'
    with tarfile.open(TAR, 'r:gz') as tar:
        def oqi(nom, kutilgan):
            try:
                m = tar.getmember(nom)
            except KeyError:
                m = tar.getmember('./' + nom)
            b = tar.extractfile(m).read()
            assert sha(b) == kutilgan, f'{nom} sha256 mos emas'
            return b.decode('utf-8').split('\n')[:-1] if b.endswith(b'\n') else b.decode('utf-8').split('\n')
        uz, en = oqi(UZ_A, UZ_SHA), oqi(EN_A, EN_SHA)
    assert len(uz) == len(en) == 997, (len(uz), len(en))
    return [(i + 1, u.strip(), e.strip()) for i, (u, e) in enumerate(zip(uz, en))]


def chiqariladigan(dev):
    uzun = json.load(open(REPO / 'analysis/yoqish-2/uzun.json', encoding='utf-8'))['gaplar']
    ho = [g for g in json.load(open(REPO / 'analysis/yoqish-2/held_out.json', encoding='utf-8'))['gaplar']
          if g['manba'] == 'flores_dev']
    by_qator = {g['qator'] for g in uzun}
    matn = {norm(g['uz']) for g in ho}
    by_matn = {q for q, u, _ in dev if norm(u) in matn}
    assert len(uzun) == len(ho) == 50, (len(uzun), len(ho))
    assert by_qator == by_matn and len(by_qator) == 50, (len(by_qator), len(by_matn), len(by_qator ^ by_matn))
    return by_qator


def main():
    dev = dev_qatorlar()
    chiq = chiqariladigan(dev)
    pool = [r for r in dev if r[0] not in chiq]
    if len(pool) != POOL_N:
        raise SystemExit(f'TO\'XTA: pool {len(pool)} != {POOL_N}')
    tanlov = sorted(random.Random(SEED).sample(pool, N), key=lambda r: r[0])
    sb = SOZLAR.read_bytes()
    assert sha(sb) == SOZLAR_SHA, 'oov_florescl.json sha256 mos emas'
    sozlar = sorted({e['uz'].lower().replace('ʻ', "'").replace('’', "'") for e in json.loads(sb)['entries']})
    assert len(sozlar) == 78, len(sozlar)
    out = []
    for q, uz, en in tanlov:
        t = tokenlar(uz)
        aynan = sorted({w for w in sozlar if w in t})
        prefiks = sorted({w for w in sozlar if len(w) >= 4 and any(x.startswith(w) for x in t)} | set(aynan))
        out.append({'id': f'dev-{q:03d}', 'uz': uz, 'en_ref': en,
                    'ekspozitsiya': {'aynan': aynan, 'prefiks': prefiks}})
    b = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    CHIQ.write_bytes(b)
    print(f'chiqarildi {len(chiq)} · pool {len(pool)} · tanlandi {len(out)} · '
          f'aynan {sum(bool(r["ekspozitsiya"]["aynan"]) for r in out)} · '
          f'prefiks {sum(bool(r["ekspozitsiya"]["prefiks"]) for r in out)} · sha256 {sha(b)}')


if __name__ == '__main__':
    main()
