# Wave 2 (TOLQIN-2, October 2026): five systems, two references, a new rater panel

Materials accompanying the manuscript

> Sirojiddinov, Z. Sh., & Khakimov, M. Kh. *What Single-Reference BLEU and Small Rater Panels Can and Cannot Show:
> Two Blind Human Evaluations of Uzbek–English Machine Translation.* (Manuscript submitted.)

Wave 1 (July 2026) is in the repository root (`data/`, `ratings/`, `scripts/`, `results/`, `preregistration/`).
This folder adds the second wave. It keeps the original repository-relative paths, so every frozen script runs
unchanged from `wave2/` (Python 3.9, sacreBLEU 2.6.0, openpyxl, numpy; scipy for amendments 13–14).

Working files, plans and amendments are written in Uzbek, as they were kept during the study; file and field names
are Uzbek (e.g. *tuzatish* = amendment, *natija* = result, *qaytgan* = returned, *baho* = rating, *etalon* = reference,
*paket* = package, *veb* = neural outputs, *qoshimcha* = supplementary).

## Layout

```
evaluation/eval72/sentences.json    frozen 72-sentence corpus (identical to data/corpus_72.json of wave 1)
analysis/tolqin-2/
  prereg.md                          analysis plan, committed before data
  tuzatish_1.md … tuzatish_14.md     dated amendments (before data / after data), deviation register
  MANIFEST.json                      stage log with commits and SHA-256 of every frozen file
  a_qavat_400.json                   A-layer: 400 held-out FLORES-200 dev sentences (+ exposure flags)
  veb/kirish/                        numbered input batches (LLM: 12 × 40; Google Translate: 19 × 25) and prompt
  veb/javob/, veb/javob_xom/         neural outputs as returned (Gemini raw API responses; GT documents)
  veb/jurnal.csv, veb/kalit.json     access route, model identifier, timestamps per batch; batch key
  kkt_chiqish.json                   rule-based system outputs (A and B layers)
  paket/                             blank rater / translator packages as distributed, rating key
  qaytgan/T1.xlsx                    second reference (translator T1, 71/72)
  qaytgan/baho_B.xlsx, _C, _D        rating files (primary panel), as accepted by qabul.py
  qaytgan/xom/E__baho_E.xlsx         fourth rater's file with its altered header — excluded from the primary analysis
  qaytgan/qabul_jurnal.csv           acceptance log;  qaytgan/kalitsiz_tekshiruv/  key-free agreement check (26 Oct)
  qabul.py, etalon_tekshir.py, tahlil.py, comet_qoshimcha.py   frozen scripts (one run each)
  etalon/etalon_tekshir.json         reference-independence check
  natija/                            frozen results (tahlil_natija.json/.md, comet_natija.json)
  qoshimcha/                         post-data, exploratory and review-driven analyses with their code
    tuzatish13/, tuzatish14/         amendments 13–14 (T1 sensitivity, Bonferroni/BCa intervals, Kendall W,
                                     α validation against Krippendorff 2011)
SHA256SUMS.json                      checksums of every file in wave2/
```

## Reproducing the primary analysis

```
cd wave2/analysis/tolqin-2
mv natija natija_released
python tahlil.py --yurish
```

The script checks input hashes and writes `natija/`. Compared with `natija_released/`, the result tables are
byte-identical; two metadata fields differ by construction: `comet` (whether COMET is installed in the running
environment) and `E_sha256` (the fourth rater's file is released in anonymized form, see below).

## What was changed or withheld for release

- **Anonymization.** Raw returned workbooks carried personal metadata (document author / computer names) and are not
  released. `T1.xlsx` and `baho_B/C/D.xlsx` are the files rewritten by `qabul.py` on acceptance (no personal
  metadata; hashes as in `MANIFEST.json`). The fourth rater's file (`qaytgan/xom/E__baho_E.xlsx`) is released as a
  cell-by-cell copy with metadata removed; its header (including the `[AI]` tag) and all scores are unchanged, but its
  SHA-256 differs from the one recorded internally.
- **Researcher-edited copies** of three rating files (27 Oct) are described in `qaytgan/tadqiqotchi_tahriri/README.md`
  but not released; they were never used as data.
- **Not released:** the rule-based system's source code and lexical base, the script that invokes the system
  (`kkt_chiqish.py`; its outputs are in `kkt_chiqish.json`), and the lexical-database exposure check
  (`ekspozitsiya_2_db.*`). Everything reported in the paper is recomputable from the released outputs.
- Local absolute paths inside text files were replaced by `~`.

## Participants and consent

Raters and the reference translator took part voluntarily and agreed to the public release of their anonymized
work. They are identified by letters only. The translator's tool-use declaration was not completed (see
`tuzatish_9.md`, §3); the manuscript treats this as a limitation.

## Licences

Data, ratings and results: CC BY 4.0 (`LICENSE-DATA`). Scripts: MIT (`LICENSE`). FLORES-200 material
(`a_qavat_400.json`, FLORES layer of the corpus): its original licence, CC BY-SA 4.0. Neural system outputs are
provided for research reproducibility.
