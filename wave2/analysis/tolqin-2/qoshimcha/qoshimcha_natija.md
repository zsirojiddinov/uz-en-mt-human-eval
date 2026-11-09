# TOLQIN-2 — qo'shimcha tahlil (qoshimcha_tahlil.py)

**natijadan keyingi, qo'shimcha; prereg'da yo'q; tadqiqotchi so'rovi 2026-10-27**. Tasdiqlovchi emas.
Element 355 (71 gap, gold-00 siz); bootstrap 1000, seed 20261027, gap bo'yicha.

## asosiy B,C,D

### (a) baholovchi × tizim o'rtachasi (mazmun / ravonlik)

| baholovchi | KKT | Gemini | Claude | GPT | GT | tartib (mazmun) | KKT eng past (m / r) |
|---|---|---|---|---|---|---|---|
| B | 1.817 / 1.690 | 4.071 / 3.914 | 3.857 / 3.757 | 3.789 / 3.690 | 3.887 / 3.901 | Gemini > GT > Claude > GPT > KKT | ha / ha |
| C | 4.070 / 3.915 | 4.310 / 4.183 | 4.282 / 4.155 | 4.310 / 4.183 | 4.282 / 4.169 | Gemini > GPT > Claude > GT > KKT | ha / ha |
| D | 4.437 / 4.690 | 4.817 / 4.972 | 4.817 / 4.958 | 4.845 / 4.986 | 4.817 / 4.957 | GPT > Gemini > Claude > GT > KKT | ha / ha |

### (b) kelishuv, 95 % CI

| o'lchov | α (ordinal) [CI] | B–C | B–D | C–D |
|---|---|---|---|---|
| mazmun | 0.115 [0.025; 0.196] | 0.312 [0.176; 0.427] | 0.355 [0.270; 0.443] | 0.333 [0.247; 0.412] |
| ravonlik | -0.079 [-0.157; -0.003] | 0.279 [0.120; 0.418] | 0.254 [0.125; 0.368] | 0.186 [0.114; 0.261] |

## E bilan B,C,D,E

### (a) baholovchi × tizim o'rtachasi (mazmun / ravonlik)

| baholovchi | KKT | Gemini | Claude | GPT | GT | tartib (mazmun) | KKT eng past (m / r) |
|---|---|---|---|---|---|---|---|
| B | 1.817 / 1.690 | 4.071 / 3.914 | 3.857 / 3.757 | 3.789 / 3.690 | 3.887 / 3.901 | Gemini > GT > Claude > GPT > KKT | ha / ha |
| C | 4.070 / 3.915 | 4.310 / 4.183 | 4.282 / 4.155 | 4.310 / 4.183 | 4.282 / 4.169 | Gemini > GPT > Claude > GT > KKT | ha / ha |
| D | 4.437 / 4.690 | 4.817 / 4.972 | 4.817 / 4.958 | 4.845 / 4.986 | 4.817 / 4.957 | GPT > Gemini > Claude > GT > KKT | ha / ha |
| E | 2.479 / 1.718 | 4.915 / 4.901 | 4.901 / 4.901 | 4.887 / 4.915 | 4.690 / 4.831 | Gemini > Claude > GPT > GT > KKT | ha / ha |

### (b) kelishuv, 95 % CI

| o'lchov | α (ordinal) [CI] | B–C | B–D | B–E | C–D | C–E | D–E |
|---|---|---|---|---|---|---|---|
| mazmun | 0.203 [0.146; 0.258] | 0.312 [0.176; 0.427] | 0.355 [0.270; 0.443] | 0.566 [0.493; 0.633] | 0.333 [0.247; 0.412] | 0.192 [0.102; 0.272] | 0.389 [0.283; 0.504] |
| ravonlik | 0.085 [0.035; 0.138] | 0.279 [0.120; 0.418] | 0.254 [0.125; 0.368] | 0.580 [0.520; 0.647] | 0.186 [0.114; 0.261] | 0.212 [0.107; 0.308] | 0.310 [0.170; 0.445] |

## (c) ball tarqalishi (360 element, fayl bo'yicha)

| baholovchi | o'lchov | 1 | 2 | 3 | 4 | 5 | yo'q | 5 ulushi |
|---|---|---|---|---|---|---|---|---|
| B | mazmun | 61 | 17 | 67 | 109 | 104 | 2 | 29.1% |
| B | ravonlik | 66 | 25 | 68 | 96 | 103 | 2 | 28.8% |
| C | mazmun | 4 | 4 | 0 | 238 | 114 | 0 | 31.7% |
| C | ravonlik | 4 | 5 | 4 | 273 | 74 | 0 | 20.6% |
| D | mazmun | 0 | 1 | 10 | 67 | 282 | 0 | 78.3% |
| D | ravonlik | 0 | 0 | 6 | 19 | 334 | 1 | 93.0% |
| E | mazmun | 12 | 37 | 16 | 32 | 263 | 0 | 73.1% |
| E | ravonlik | 46 | 14 | 5 | 29 | 266 | 0 | 73.9% |
