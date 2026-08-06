# Uzbek–English MT: Pre-Registered Blind Human Evaluation

Evaluation materials accompanying the paper:

> Sirojiddinov, Z. Sh., & Khakimov, M. Kh. *What Single-Reference BLEU Cannot Show:
> A Pre-Registered Blind Human Evaluation of Uzbek–English Machine Translation.*
> (Manuscript under review.)

This repository contains everything needed to reproduce the numbers reported in
the paper: the frozen 72-sentence corpus, all 216 system outputs, the blinding
key, the anonymized human ratings, the frozen analysis script, and the dated
pre-registration plan with its amendments.

---

## 1. What this study measures

Under a **single reference**, does BLEU reflect the *absolute* quality of
Uzbek–English machine translation? Two systems (a rule-based system grounded in
the KKT / Extensible Input Language formalism, included with two frozen states as
an internal reliability control, and a large neural system) were rated blind by
two independent raters on adequacy and fluency (1–5).

Headline result: outputs rated **4.56/5** by humans obtain only **41 BLEU**
against the single reference. A low BLEU score is the *normal* condition in this
setting, not evidence of poor quality. BLEU nevertheless tracks *relative*
ranking well (Spearman ρ = 0.77).

---

## 2. Repository layout

```
data/
  corpus_72.json          72 source sentences + single reference, 3 stylistic layers
  outputs_s1.json         rule-based system, frozen state 1
  outputs_s2.json         rule-based system, frozen state 2
  outputs_gemini.json     neural system outputs
  blind_key.json          item_id -> (sentence_id, system); withheld from raters
  metric_scores.json      per-item BLEU / chrF (sacreBLEU 13a)
  CORPUS_LOCK.txt         corpus lock statement (held-out guarantee)

ratings/
  rater_B.xlsx            216 ratings, anonymized (item_id, adequacy, fluency)
  rater_C.xlsx            216 ratings, anonymized

scripts/
  01_select_corpus.py     stratified sampling of the 72 sentences
  02_collect_outputs.py   collection of system outputs
  03_build_blind_sheets.py construction of the blind rating sheets
  04_score_metrics.py     BLEU / chrF computation
  05_analyze_FROZEN.py    PRIMARY ANALYSIS — frozen, executed exactly once
  06_supplementary_A.py   pre-registered supplementary analysis (partial rater)
  07_build_report.py      report tables

results/
  human_eval_results.md   main results
  rw1_report.md           full evaluation report
  results_tables.json     machine-readable tables
  supplementary_A_partial.md  supplementary analysis

preregistration/
  analysis_plan.md        pre-registration plan with dated amendments
  COMMIT_HISTORY.txt      timestamped commits proving the plan preceded the data

SHA256SUMS.json           checksums of every file in this release
```

---

## 3. Corpus

72 sentences in three stylistic layers:

| Layer | n | Source |
|---|---|---|
| News / journalistic | 36 | FLORES-200 (held out) |
| Scientific abstract | 24 | in-domain scientific prose |
| Simple control | 12 | low-complexity control sentences |

The corpus was locked at construction (`data/CORPUS_LOCK.txt`): **no sentence was
used for system tuning or as a lexical source**. Separation of the FLORES subset
from every tuning and lexicon-sourcing step was verified programmatically.

Each item is one (sentence × system) pair: 72 × 3 = **216 items**.

---

## 4. Reproducing the analysis

Requirements: Python 3.9+, `openpyxl`, `scipy`, `sacrebleu`.

```bash
pip install openpyxl scipy sacrebleu
python scripts/05_analyze_FROZEN.py
```

`05_analyze_FROZEN.py` is the pre-registered primary analysis script. It was
frozen before the ratings were collected (see `preregistration/COMMIT_HISTORY.txt`)
and executed exactly once. Re-running it on this data reproduces the tables in
`results/`.

To recompute the automatic metrics from scratch:

```bash
python scripts/04_score_metrics.py
```

---

## 5. Pre-registration

The analysis plan was frozen in version control before data collection. Three
dated, outcome-blind amendments were used and are documented in full:

1. **Stopping rule** — deadline and the two-file rule fixed without inspecting
   file contents.
2. **Rater substitution** — when the planned teacher-rater withdrew for family
   reasons, a qualified substitute meeting the same role requirement was accepted
   for a partial set, entering the supplementary analysis only.
3. **Early execution** — once non-arrival of the third file became definitive
   through an external fact unrelated to any rating content, the primary analysis
   was executed ahead of the deadline under the existing two-file rule.

`COMMIT_HISTORY.txt` gives the commit hashes and timestamps proving that each
amendment preceded the data it concerns.

---

## 6. Ratings and anonymization

Raters participated voluntarily and were informed of the study's purpose. The
released rating files contain **only** `item_id`, `adequacy` and `fluency`;
rater identities, source text, system outputs and file metadata were stripped.
Raters are identified in the paper only by role and qualification (B: IELTS 7.5;
C: IELTS 7.0).

---

## 7. What is *not* in this repository

This release covers the **evaluation study only**. It deliberately does not
include:

- the full source code of the rule-based translation system,
- the 26,978-entry lexical–morphological database,
- the held-out test sets used in ongoing system-level evaluation cycles.

These are the subject of a separate system paper and of ongoing evaluation work;
releasing the held-out sets now would destroy their held-out status. They will be
released once those cycles conclude, and are available to editors and reviewers
on request in the meantime.

---

## 8. Licence

- **Data, ratings, results:** CC BY 4.0
- **Scripts:** MIT

The FLORES-200 subset is redistributed under the terms of its original licence
(CC BY-SA 4.0); see the FLORES-200 / NLLB release for details.

---

## 9. Citation

```bibtex
@misc{sirojiddinov2026uzeneval,
  author       = {Sirojiddinov, Ziyoviddin Sh. and Khakimov, Muftakh Kh.},
  title        = {Uzbek--English MT: Pre-Registered Blind Human Evaluation
                  (corpus, outputs, ratings, scripts)},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.XXXXXXX}
}
```

Replace the DOI with the one minted for this release.

---

## 10. Contact

Ziyoviddin Sh. Sirojiddinov — Innovation Development Center, Kapital Insurance
JSC, Tashkent, Uzbekistan. ORCID [0000-0002-6249-032X](https://orcid.org/0000-0002-6249-032X)
