# TOLQIN-2 — tahlil natijasi (tahlil.py)

sacreBLEU 2.6.0 · imzolar `{"1ref": {"bleu": "nrefs:1|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0", "chrf": "nrefs:1|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0"}, "3ref": {"bleu": "nrefs:3|case:mixed|eff:no|tok:13a|smooth:exp|version:2.6.0", "chrf": "nrefs:3|case:mixed|eff:yes|nc:6|nw:0|space:no|version:2.6.0"}}`
COMET: o'rnatilmagan — prereg §2.7 bo'yicha chiqarib tashlandi

Baholovchilar: {"kelgan": ["B", "C", "D"], "ishlatilgan": ["B", "C", "D"], "chiqarilgan": {"E": "asosiy inson tahlilidan chiqarilgan — qaytgan fayl (xom/E__baho_E.xlsx, sha256 d2f285b5…c505) o'zini «[AI]» deb belgilagan, deklaratsiya yo'q; 2026-10-26 (tuzatish 9 (a), dcb7190); qayd 2026-10-27 (Q1c)"}, "toxtash_qoidasi_>=3": true, "yoq_malumot": [["B", "E159", 0], ["B", "E159", 1], ["B", "E219", 0], ["B", "E219", 1], ["D", "E019", 1]]}

## A1 A-qavat (5 × 400, 1 etalon FLORES)

```
{
 "Claude": {
  "bleu": 61.003161912811215,
  "chrf2": 79.40576710601835,
  "gap_bleu_ortacha_exp": 57.20486158344523,
  "n": 400
 },
 "GPT": {
  "bleu": 40.50609581706736,
  "chrf2": 66.59203604616387,
  "gap_bleu_ortacha_exp": 38.06273148802879,
  "n": 400
 },
 "GT": {
  "bleu": 45.022126299350376,
  "chrf2": 68.7031981694496,
  "gap_bleu_ortacha_exp": 42.18800532285023,
  "n": 400
 },
 "Gemini": {
  "bleu": 43.32669391635356,
  "chrf2": 68.29788764850277,
  "gap_bleu_ortacha_exp": 40.970246207850636,
  "n": 400
 },
 "KKT": {
  "bleu": 2.771892377488271,
  "chrf2": 38.63787853704114,
  "gap_bleu_ortacha_exp": 5.232674687538626,
  "n": 400
 }
}
```

## A2 A-qavat KKT ekspozitsiyali/ekspozitsiyasiz (78 so'z; aynan va prefiks)

```
{
 "aynan: ekspozitsiyali": {
  "bleu": 2.4624295779086127,
  "chrf2": 40.602370623587476,
  "gap_bleu_ortacha_exp": 4.862906782269769,
  "n": 29
 },
 "aynan: ekspozitsiyasiz": {
  "bleu": 2.7941578485344003,
  "chrf2": 38.482350522793155,
  "gap_bleu_ortacha_exp": 5.261578378246972,
  "n": 371
 },
 "prefiks: ekspozitsiyali": {
  "bleu": 2.296221012822373,
  "chrf2": 39.747123762874466,
  "gap_bleu_ortacha_exp": 4.936994765294994,
  "n": 75
 },
 "prefiks: ekspozitsiyasiz": {
  "bleu": 2.865237619949204,
  "chrf2": 38.34921528829417,
  "gap_bleu_ortacha_exp": 5.300908515748695,
  "n": 325
 }
}
```

## B1 B-qavat (5 × 72): 1 va 3 etalon (asosiy: hammasi; qatlamlar tavsifiy)

```
{
 "B-FLORES (flores)": {
  "Claude": {
   "1ref": {
    "bleu": 61.72691205757368,
    "chrf2": 79.86142110903066,
    "gap_bleu_ortacha_exp": 55.88092120591328,
    "n": 36
   },
   "3ref": {
    "bleu": 72.10449037549641,
    "chrf2": 81.5671530472533,
    "gap_bleu_ortacha_exp": 68.30392194565505,
    "n": 36
   },
   "beqaror": false
  },
  "GPT": {
   "1ref": {
    "bleu": 37.18693748361596,
    "chrf2": 65.02261496401165,
    "gap_bleu_ortacha_exp": 33.98050368590251,
    "n": 36
   },
   "3ref": {
    "bleu": 62.26118712815007,
    "chrf2": 74.44667351294663,
    "gap_bleu_ortacha_exp": 59.83546317620759,
    "n": 36
   },
   "beqaror": false
  },
  "GT": {
   "1ref": {
    "bleu": 41.48612752214944,
    "chrf2": 67.1996693402565,
    "gap_bleu_ortacha_exp": 37.00272075556968,
    "n": 36
   },
   "3ref": {
    "bleu": 56.69430669605444,
    "chrf2": 71.080904588198,
    "gap_bleu_ortacha_exp": 52.38968723931956,
    "n": 36
   },
   "beqaror": false
  },
  "Gemini": {
   "1ref": {
    "bleu": 40.370926776531235,
    "chrf2": 65.86841384050832,
    "gap_bleu_ortacha_exp": 34.14202567808729,
    "n": 36
   },
   "3ref": {
    "bleu": 57.31186458415483,
    "chrf2": 70.64315903822825,
    "gap_bleu_ortacha_exp": 52.18485800999684,
    "n": 36
   },
   "beqaror": false
  },
  "KKT": {
   "1ref": {
    "bleu": 1.5991899787889943,
    "chrf2": 39.65075512529217,
    "gap_bleu_ortacha_exp": 4.921457796274801,
    "n": 36
   },
   "3ref": {
    "bleu": 2.621902259976031,
    "chrf2": 41.31008357823275,
    "gap_bleu_ortacha_exp": 6.42784247256365,
    "n": 36
   },
   "beqaror": false
  }
 },
 "B-KKT (train+gold)": {
  "Claude": {
   "1ref": {
    "bleu": 49.146760821270625,
    "chrf2": 75.59898111405931,
    "gap_bleu_ortacha_exp": 53.56807394658827,
    "n": 36
   },
   "3ref": {
    "bleu": 58.7626285432993,
    "chrf2": 78.26101059919142,
    "gap_bleu_ortacha_exp": 64.06233945395068,
    "n": 36
   },
   "beqaror": false
  },
  "GPT": {
   "1ref": {
    "bleu": 48.25150161243571,
    "chrf2": 74.52459675555122,
    "gap_bleu_ortacha_exp": 49.121868678031,
    "n": 36
   },
   "3ref": {
    "bleu": 65.2430450636353,
    "chrf2": 80.18425788631366,
    "gap_bleu_ortacha_exp": 67.57470115511752,
    "n": 36
   },
   "beqaror": false
  },
  "GT": {
   "1ref": {
    "bleu": 59.554737861186105,
    "chrf2": 78.97267987044971,
    "gap_bleu_ortacha_exp": 58.46498459782231,
    "n": 36
   },
   "3ref": {
    "bleu": 69.99476726372146,
    "chrf2": 82.51859700567745,
    "gap_bleu_ortacha_exp": 66.91405022301463,
    "n": 36
   },
   "beqaror": false
  },
  "Gemini": {
   "1ref": {
    "bleu": 51.44549340630639,
    "chrf2": 76.20633293143896,
    "gap_bleu_ortacha_exp": 50.69168027163146,
    "n": 36
   },
   "3ref": {
    "bleu": 59.735064716423274,
    "chrf2": 79.20351119434203,
    "gap_bleu_ortacha_exp": 60.88627841588042,
    "n": 36
   },
   "beqaror": false
  },
  "KKT": {
   "1ref": {
    "bleu": 11.995447933995848,
    "chrf2": 53.80151745976932,
    "gap_bleu_ortacha_exp": 22.964505794413164,
    "n": 36
   },
   "3ref": {
    "bleu": 13.62728878878267,
    "chrf2": 54.30415086480311,
    "gap_bleu_ortacha_exp": 26.36748025660988,
    "n": 36
   },
   "beqaror": false
  }
 },
 "hammasi": {
  "Claude": {
   "1ref": {
    "bleu": 56.673825552480906,
    "chrf2": 77.92369372089544,
    "gap_bleu_ortacha_exp": 54.72449757625078,
    "n": 72
   },
   "3ref": {
    "bleu": 66.95851851518397,
    "chrf2": 80.0494744246553,
    "gap_bleu_ortacha_exp": 66.18313069980287,
    "n": 72
   },
   "beqaror": false
  },
  "GPT": {
   "1ref": {
    "bleu": 41.711846212825684,
    "chrf2": 69.32453306807328,
    "gap_bleu_ortacha_exp": 41.55118618196676,
    "n": 72
   },
   "3ref": {
    "bleu": 63.473597403732576,
    "chrf2": 77.02317405709859,
    "gap_bleu_ortacha_exp": 63.705082165662574,
    "n": 72
   },
   "beqaror": false
  },
  "GT": {
   "1ref": {
    "bleu": 49.14911717991948,
    "chrf2": 72.55639618605643,
    "gap_bleu_ortacha_exp": 47.73385267669599,
    "n": 72
   },
   "3ref": {
    "bleu": 62.29166627246257,
    "chrf2": 76.31792719341156,
    "gap_bleu_ortacha_exp": 59.65186873116708,
    "n": 72
   },
   "beqaror": false
  },
  "Gemini": {
   "1ref": {
    "bleu": 44.97993562821502,
    "chrf2": 70.56828168040732,
    "gap_bleu_ortacha_exp": 42.41685297485938,
    "n": 72
   },
   "3ref": {
    "bleu": 58.31403895885283,
    "chrf2": 74.53331789342677,
    "gap_bleu_ortacha_exp": 56.535568212938614,
    "n": 72
   },
   "beqaror": false
  },
  "KKT": {
   "1ref": {
    "bleu": 6.5192883865680855,
    "chrf2": 45.99203389281121,
    "gap_bleu_ortacha_exp": 13.942981795343982,
    "n": 72
   },
   "3ref": {
    "bleu": 7.893087285914736,
    "chrf2": 47.09511997991382,
    "gap_bleu_ortacha_exp": 16.397661364586764,
    "n": 72
   },
   "beqaror": false
  }
 },
 "qatlam flores": {
  "Claude": {
   "1ref": {
    "bleu": 61.72691205757368,
    "chrf2": 79.86142110903066,
    "gap_bleu_ortacha_exp": 55.88092120591328,
    "n": 36
   },
   "3ref": {
    "bleu": 72.10449037549641,
    "chrf2": 81.5671530472533,
    "gap_bleu_ortacha_exp": 68.30392194565505,
    "n": 36
   },
   "beqaror": false
  },
  "GPT": {
   "1ref": {
    "bleu": 37.18693748361596,
    "chrf2": 65.02261496401165,
    "gap_bleu_ortacha_exp": 33.98050368590251,
    "n": 36
   },
   "3ref": {
    "bleu": 62.26118712815007,
    "chrf2": 74.44667351294663,
    "gap_bleu_ortacha_exp": 59.83546317620759,
    "n": 36
   },
   "beqaror": false
  },
  "GT": {
   "1ref": {
    "bleu": 41.48612752214944,
    "chrf2": 67.1996693402565,
    "gap_bleu_ortacha_exp": 37.00272075556968,
    "n": 36
   },
   "3ref": {
    "bleu": 56.69430669605444,
    "chrf2": 71.080904588198,
    "gap_bleu_ortacha_exp": 52.38968723931956,
    "n": 36
   },
   "beqaror": false
  },
  "Gemini": {
   "1ref": {
    "bleu": 40.370926776531235,
    "chrf2": 65.86841384050832,
    "gap_bleu_ortacha_exp": 34.14202567808729,
    "n": 36
   },
   "3ref": {
    "bleu": 57.31186458415483,
    "chrf2": 70.64315903822825,
    "gap_bleu_ortacha_exp": 52.18485800999684,
    "n": 36
   },
   "beqaror": false
  },
  "KKT": {
   "1ref": {
    "bleu": 1.5991899787889943,
    "chrf2": 39.65075512529217,
    "gap_bleu_ortacha_exp": 4.921457796274801,
    "n": 36
   },
   "3ref": {
    "bleu": 2.621902259976031,
    "chrf2": 41.31008357823275,
    "gap_bleu_ortacha_exp": 6.42784247256365,
    "n": 36
   },
   "beqaror": false
  }
 },
 "qatlam gold": {
  "Claude": {
   "1ref": {
    "bleu": 66.48956422508215,
    "chrf2": 87.71838947940401,
    "gap_bleu_ortacha_exp": 67.8612180397655,
    "n": 12
   },
   "3ref": {
    "bleu": 78.39979161182306,
    "chrf2": 91.06680070926238,
    "gap_bleu_ortacha_exp": 77.73663069949572,
    "n": 12
   },
   "beqaror": true
  },
  "GPT": {
   "1ref": {
    "bleu": 48.220775903709345,
    "chrf2": 82.98895144987667,
    "gap_bleu_ortacha_exp": 50.138744246049505,
    "n": 12
   },
   "3ref": {
    "bleu": 72.80712450692455,
    "chrf2": 88.13914232725315,
    "gap_bleu_ortacha_exp": 70.70779654682573,
    "n": 12
   },
   "beqaror": true
  },
  "GT": {
   "1ref": {
    "bleu": 60.10696391440652,
    "chrf2": 79.08865950131631,
    "gap_bleu_ortacha_exp": 60.85781190206779,
    "n": 12
   },
   "3ref": {
    "bleu": 66.0647186714979,
    "chrf2": 83.67620303627041,
    "gap_bleu_ortacha_exp": 66.094053554946,
    "n": 12
   },
   "beqaror": true
  },
  "Gemini": {
   "1ref": {
    "bleu": 52.28498882615261,
    "chrf2": 83.89695898909804,
    "gap_bleu_ortacha_exp": 52.3719247052301,
    "n": 12
   },
   "3ref": {
    "bleu": 69.3304105431019,
    "chrf2": 89.48910348531838,
    "gap_bleu_ortacha_exp": 66.81353991734808,
    "n": 12
   },
   "beqaror": true
  },
  "KKT": {
   "1ref": {
    "bleu": 50.06999877139851,
    "chrf2": 80.90032910348697,
    "gap_bleu_ortacha_exp": 50.84538119922075,
    "n": 12
   },
   "3ref": {
    "bleu": 59.69813870102649,
    "chrf2": 81.44407594013259,
    "gap_bleu_ortacha_exp": 59.67261160368466,
    "n": 12
   },
   "beqaror": true
  }
 },
 "qatlam train": {
  "Claude": {
   "1ref": {
    "bleu": 47.39765836914062,
    "chrf2": 74.12786692024753,
    "gap_bleu_ortacha_exp": 46.42150189999965,
    "n": 24
   },
   "3ref": {
    "bleu": 56.695142939249465,
    "chrf2": 76.73576594830335,
    "gap_bleu_ortacha_exp": 57.22519383117816,
    "n": 24
   },
   "beqaror": false
  },
  "GPT": {
   "1ref": {
    "bleu": 47.57710509902845,
    "chrf2": 73.4922616116489,
    "gap_bleu_ortacha_exp": 48.613430894021754,
    "n": 24
   },
   "3ref": {
    "bleu": 64.38953284750328,
    "chrf2": 79.19685967422865,
    "gap_bleu_ortacha_exp": 66.00815345926343,
    "n": 24
   },
   "beqaror": false
  },
  "GT": {
   "1ref": {
    "bleu": 59.49678399459072,
    "chrf2": 78.95931198167236,
    "gap_bleu_ortacha_exp": 57.26857094569957,
    "n": 24
   },
   "3ref": {
    "bleu": 70.26586455897562,
    "chrf2": 82.38088456094836,
    "gap_bleu_ortacha_exp": 67.32404855704895,
    "n": 24
   },
   "beqaror": false
  },
  "Gemini": {
   "1ref": {
    "bleu": 51.28272101117945,
    "chrf2": 75.27452093526212,
    "gap_bleu_ortacha_exp": 49.85155805483216,
    "n": 24
   },
   "3ref": {
    "bleu": 58.69650841443472,
    "chrf2": 77.96970918754779,
    "gap_bleu_ortacha_exp": 57.9226476651466,
    "n": 24
   },
   "beqaror": false
  },
  "KKT": {
   "1ref": {
    "bleu": 6.767669048716307,
    "chrf2": 50.564918188325834,
    "gap_bleu_ortacha_exp": 9.024068092009374,
    "n": 24
   },
   "3ref": {
    "bleu": 7.350742780411027,
    "chrf2": 51.06136066358145,
    "gap_bleu_ortacha_exp": 9.714914583072487,
    "n": 24
   },
   "beqaror": false
  }
 }
}
```

## B2 P1: Δ = BLEU_3ref − BLEU_1ref (72 gap)

```
{
 "Claude": {
  "ci95_bootstrap_gap": [
   7.330459506336609,
   13.48769265773445
  ],
  "delta_bleu_3ref_minus_1ref": 10.284692962703062
 },
 "GPT": {
  "ci95_bootstrap_gap": [
   17.736724884923106,
   26.267375779078243
  ],
  "delta_bleu_3ref_minus_1ref": 21.761751190906892
 },
 "GT": {
  "ci95_bootstrap_gap": [
   10.04780264226288,
   16.407820930324917
  ],
  "delta_bleu_3ref_minus_1ref": 13.142549092543092
 },
 "Gemini": {
  "ci95_bootstrap_gap": [
   10.305705018660618,
   16.862478856761193
  ],
  "delta_bleu_3ref_minus_1ref": 13.33410333063781
 },
 "KKT": {
  "ci95_bootstrap_gap": [
   0.8204715757405814,
   2.0928738576336006
  ],
  "delta_bleu_3ref_minus_1ref": 1.3737988993466503
 }
}
```

## H1 Yaxlitlik darvozalari (prereg §2.5 (a)–(e), kalitsiz)

```
{
 "B": {
  "a_toliqlik": false,
  "b_diapazon": true,
  "c_avtopilot_eng_uzun": 5,
  "c_belgi": false,
  "d_belgi": false,
  "d_spearman_adq_flu": 0.884870997120301,
  "e_belgi": false,
  "e_teng_ulush": 0.7094972067039106
 },
 "C": {
  "a_toliqlik": true,
  "b_diapazon": true,
  "c_avtopilot_eng_uzun": 13,
  "c_belgi": true,
  "d_belgi": false,
  "d_spearman_adq_flu": 0.7519771533893713,
  "e_belgi": false,
  "e_teng_ulush": 0.8777777777777778
 },
 "D": {
  "a_toliqlik": false,
  "b_diapazon": true,
  "c_avtopilot_eng_uzun": 19,
  "c_belgi": true,
  "d_belgi": false,
  "d_spearman_adq_flu": 0.5482547287882759,
  "e_belgi": false,
  "e_teng_ulush": 0.8161559888579387
 }
}
```

## H2 Inson adequacy/fluency o'rtachasi (tizim bo'yicha) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "Claude": {
  "adequacy": 4.32394366197183,
  "baholovchi": 3,
  "fluency": 4.293427230046947,
  "n": 71
 },
 "GPT": {
  "adequacy": 4.314553990610328,
  "baholovchi": 3,
  "fluency": 4.286384976525822,
  "n": 71
 },
 "GT": {
  "adequacy": 4.328638497652584,
  "baholovchi": 3,
  "fluency": 4.340375586854461,
  "n": 71
 },
 "Gemini": {
  "adequacy": 4.401408450704224,
  "baholovchi": 3,
  "fluency": 4.359154929577465,
  "n": 71
 },
 "KKT": {
  "adequacy": 3.44131455399061,
  "baholovchi": 3,
  "fluency": 3.431924882629109,
  "n": 71
 }
}
```

## H3 S2 kalibrovka: adequacy o'rtachasi >= 4,5 bo'lgan chiqishlar, 1 etalon — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "Claude": {
  "bleu": 53.462314023148224,
  "chrf2": 76.86879293246523,
  "gap_bleu_ortacha_exp": 51.31061953372153,
  "n": 27
 },
 "GPT": {
  "bleu": 42.42517357384537,
  "chrf2": 71.55712466317023,
  "gap_bleu_ortacha_exp": 43.537581467721594,
  "n": 24
 },
 "GT": {
  "bleu": 42.57187767429302,
  "chrf2": 67.74063010023825,
  "gap_bleu_ortacha_exp": 46.2659669885098,
  "n": 29
 },
 "Gemini": {
  "bleu": 48.413641076895324,
  "chrf2": 73.32077096370267,
  "gap_bleu_ortacha_exp": 46.18837708751669,
  "n": 33
 },
 "KKT": {
  "bleu": 32.01941279533056,
  "chrf2": 68.8952285680366,
  "gap_bleu_ortacha_exp": 40.31657428280199,
  "n": 11
 },
 "hammasi": {
  "bleu": 46.0029911529021,
  "chrf2": 72.0494251944169,
  "gap_bleu_ortacha_exp": 46.28790714759241,
  "n": 124
 }
}
```

## H4 S3 ρ(gap-BLEU_1ref, adequacy): umumiy, tizim ichida, qatlam bo'yicha (bootstrap 1000) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "B-FLORES (flores): Claude": {
  "beqaror": false,
  "ci95": [
   -0.544592909787311,
   0.12767737727339806
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.22727282725781275
 },
 "B-FLORES (flores): GPT": {
  "beqaror": false,
  "ci95": [
   -0.30338084357726663,
   0.44576037540994284
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.08912496301848635
 },
 "B-FLORES (flores): GT": {
  "beqaror": false,
  "ci95": [
   -0.4830331721802036,
   0.25107513767296635
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.13936741578273734
 },
 "B-FLORES (flores): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3387279527004312,
   0.3870817751839765
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.026422135756482237
 },
 "B-FLORES (flores): KKT": {
  "beqaror": false,
  "ci95": [
   -0.1353537962526291,
   0.5330179473318197
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.2102081496918898
 },
 "B-FLORES (flores): umumiy": {
  "beqaror": false,
  "ci95": [
   0.22052675328226173,
   0.5038839434432448
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.3739539262201052
 },
 "B-KKT (train+gold): Claude": {
  "beqaror": false,
  "ci95": [
   -0.35325162208869393,
   0.3218798267614794
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": -0.011182650664349671
 },
 "B-KKT (train+gold): GPT": {
  "beqaror": false,
  "ci95": [
   -0.49978197180055534,
   0.15086420171506942
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": -0.1994806770908986
 },
 "B-KKT (train+gold): GT": {
  "beqaror": false,
  "ci95": [
   -0.4511484707788226,
   0.29508048818030946
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": -0.06381998058952625
 },
 "B-KKT (train+gold): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.1699561292224434,
   0.4580251092405812
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": 0.14345740173691646
 },
 "B-KKT (train+gold): KKT": {
  "beqaror": false,
  "ci95": [
   0.5021353917772721,
   0.8199033055872758
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": 0.692517769471753
 },
 "B-KKT (train+gold): umumiy": {
  "beqaror": false,
  "ci95": [
   0.11959263540653511,
   0.41922768541320093
  ],
  "n": 175,
  "noyob_gap": 35,
  "spearman": 0.2760276325721424
 },
 "qatlam flores: Claude": {
  "beqaror": false,
  "ci95": [
   -0.544592909787311,
   0.12767737727339806
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.22727282725781275
 },
 "qatlam flores: GPT": {
  "beqaror": false,
  "ci95": [
   -0.30338084357726663,
   0.44576037540994284
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.08912496301848635
 },
 "qatlam flores: GT": {
  "beqaror": false,
  "ci95": [
   -0.4830331721802036,
   0.25107513767296635
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.13936741578273734
 },
 "qatlam flores: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3387279527004312,
   0.3870817751839765
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.026422135756482237
 },
 "qatlam flores: KKT": {
  "beqaror": false,
  "ci95": [
   -0.1353537962526291,
   0.5330179473318197
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.2102081496918898
 },
 "qatlam flores: umumiy": {
  "beqaror": false,
  "ci95": [
   0.22052675328226173,
   0.5038839434432448
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.3739539262201052
 },
 "qatlam gold: Claude": {
  "beqaror": true,
  "ci95": [
   -0.6154888549862174,
   0.6817541583256873
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.03216429268095617
 },
 "qatlam gold: GPT": {
  "beqaror": true,
  "ci95": [
   -0.9128709291752769,
   0.6316515722272893
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.11829695303011788
 },
 "qatlam gold: GT": {
  "beqaror": true,
  "ci95": [
   -0.36041073479162716,
   0.8863856206142559
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": 0.42745377260790174
 },
 "qatlam gold: Gemini": {
  "beqaror": true,
  "ci95": [
   -0.7909440037459108,
   0.5533985905294664
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.18975834751777035
 },
 "qatlam gold: KKT": {
  "beqaror": true,
  "ci95": [
   -0.1272301701150957,
   0.810240562932375
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": 0.41160105651381795
 },
 "qatlam gold: umumiy": {
  "beqaror": true,
  "ci95": [
   -0.15939594323175768,
   0.36926288599923857
  ],
  "n": 55,
  "noyob_gap": 11,
  "spearman": 0.11744686396214342
 },
 "qatlam train: Claude": {
  "beqaror": false,
  "ci95": [
   -0.6125449369145903,
   0.27262998803360045
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.21430365340039062
 },
 "qatlam train: GPT": {
  "beqaror": false,
  "ci95": [
   -0.7069199034508571,
   0.14231884032058173
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.32422270327584896
 },
 "qatlam train: GT": {
  "beqaror": false,
  "ci95": [
   -0.7833606804590525,
   -0.0912453978985071
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.48341279286108
 },
 "qatlam train: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.10863499448493706,
   0.6456664857796244
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.2802896040972745
 },
 "qatlam train: KKT": {
  "beqaror": false,
  "ci95": [
   -0.07658136145871244,
   0.6819890564246985
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.37370125142347155
 },
 "qatlam train: umumiy": {
  "beqaror": false,
  "ci95": [
   0.05952122689103681,
   0.4508501607055431
  ],
  "n": 120,
  "noyob_gap": 24,
  "spearman": 0.2645234432453639
 },
 "tizim ichida: Claude": {
  "beqaror": false,
  "ci95": [
   -0.3584387662990896,
   0.14308778173139428
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": -0.1094132923529904
 },
 "tizim ichida: GPT": {
  "beqaror": false,
  "ci95": [
   -0.24994716061481712,
   0.27425620871222256
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": -0.006526518894412453
 },
 "tizim ichida: GT": {
  "beqaror": false,
  "ci95": [
   -0.29773485811177564,
   0.19771138324373685
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": -0.06313069986009343
 },
 "tizim ichida: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.12666999752051414,
   0.3586392198983612
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.1159392928428154
 },
 "tizim ichida: KKT": {
  "beqaror": false,
  "ci95": [
   0.326588026633569,
   0.7137166660183705
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.5457469168962422
 },
 "umumiy": {
  "beqaror": false,
  "ci95": [
   0.2370000444760684,
   0.45424250242080844
  ],
  "n": 355,
  "noyob_gap": 71,
  "spearman": 0.3515016015758524
 }
}
```

## H5 Past ball rejimi (gap-BLEU_1ref < 10): Kendall τ-b — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "Claude": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GPT": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GT": {
  "kendall_tau_b": NaN,
  "n": 2
 },
 "Gemini": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "KKT": {
  "kendall_tau_b": 0.109361287979375,
  "n": 52
 },
 "hammasi": {
  "kendall_tau_b": 0.05142043924705198,
  "n": 57
 }
}
```

## H6 P3 juftlik Spearman — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "adequacy: B–C": 0.31163426183100984,
 "adequacy: B–D": 0.35478975840973187,
 "adequacy: C–D": 0.33284525383107266,
 "fluency: B–C": 0.2794365780047855,
 "fluency: B–D": 0.2535420317324254,
 "fluency: C–D": 0.18636325061554326
}
```

## H7 P3 Krippendorff α (ordinal) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "adequacy": 0.1150611870018956,
 "fluency": -0.07930923555846325
}
```

## H8 S4 tartib ta'siri R1 − R2 (tadqiqiy) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{
 "adequacy: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.06338028169014084,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.09859154929577464,
   0.19718309859154928
  ]
 },
 "adequacy: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.007042253521126761,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.14788732394366197,
   0.1619718309859155
  ]
 },
 "adequacy: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.07042253521126761,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.1267605633802817,
   0.2605633802816901
  ]
 },
 "adequacy: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.14084507042253522,
  "R2": [
   "C"
  ],
  "ci95": [
   0.007042253521126761,
   0.2746478873239437
  ]
 },
 "adequacy: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.9436619718309859,
  "R2": [
   "C"
  ],
  "ci95": [
   -1.1267605633802817,
   -0.7323943661971831
  ]
 },
 "adequacy: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1323943661971831,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.2211267605633803,
   -0.04929577464788732
  ]
 },
 "fluency: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.2112676056338028,
  "R2": [
   "C"
  ],
  "ci95": [
   0.04225352112676056,
   0.36619718309859156
  ]
 },
 "fluency: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.15492957746478872,
  "R2": [
   "C"
  ],
  "ci95": [
   0.0,
   0.3028169014084507
  ]
 },
 "fluency: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.2535211267605634,
  "R2": [
   "C"
  ],
  "ci95": [
   0.07746478873239436,
   0.4084507042253521
  ]
 },
 "fluency: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.2676056338028169,
  "R2": [
   "C"
  ],
  "ci95": [
   0.11267605633802817,
   0.4154929577464789
  ]
 },
 "fluency: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.7253521126760564,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.9225352112676056,
   -0.5
  ]
 },
 "fluency: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.0323943661971831,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.04929577464788732,
   0.11267605633802817
  ]
 }
}
```

## H9 LLM-hakam vs inson o'rtachasi: Spearman (tadqiqiy) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7)

```
{}
```

## H2 Inson adequacy/fluency o'rtachasi (tizim bo'yicha) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "Claude": {
  "adequacy": 4.333333333333333,
  "baholovchi": 3,
  "fluency": 4.30324074074074,
  "n": 72
 },
 "GPT": {
  "adequacy": 4.3240740740740735,
  "baholovchi": 3,
  "fluency": 4.296296296296297,
  "n": 72
 },
 "GT": {
  "adequacy": 4.333333333333335,
  "baholovchi": 3,
  "fluency": 4.344907407407408,
  "n": 72
 },
 "Gemini": {
  "adequacy": 4.409722222222221,
  "baholovchi": 3,
  "fluency": 4.3680555555555545,
  "n": 72
 },
 "KKT": {
  "adequacy": 3.4583333333333335,
  "baholovchi": 3,
  "fluency": 3.4490740740740753,
  "n": 72
 }
}
```

## H3 S2 kalibrovka: adequacy o'rtachasi >= 4,5 bo'lgan chiqishlar, 1 etalon — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "Claude": {
  "bleu": 53.92713663426037,
  "chrf2": 77.2161056514961,
  "gap_bleu_ortacha_exp": 53.049525978945766,
  "n": 28
 },
 "GPT": {
  "bleu": 42.89807561937972,
  "chrf2": 71.99570462800993,
  "gap_bleu_ortacha_exp": 44.8354209516191,
  "n": 25
 },
 "GT": {
  "bleu": 42.525206701387035,
  "chrf2": 67.64700901469266,
  "gap_bleu_ortacha_exp": 46.14805811021359,
  "n": 30
 },
 "Gemini": {
  "bleu": 48.2305180123681,
  "chrf2": 73.17509709640393,
  "gap_bleu_ortacha_exp": 45.78480104222238,
  "n": 34
 },
 "KKT": {
  "bleu": 31.30098473235858,
  "chrf2": 68.77687378550165,
  "gap_bleu_ortacha_exp": 38.869983798119684,
  "n": 12
 },
 "hammasi": {
  "bleu": 46.062182236687605,
  "chrf2": 72.12886481653116,
  "gap_bleu_ortacha_exp": 46.6188917482199,
  "n": 129
 }
}
```

## H4 S3 ρ(gap-BLEU_1ref, adequacy): umumiy, tizim ichida, qatlam bo'yicha (bootstrap 1000) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "B-FLORES (flores): Claude": {
  "beqaror": false,
  "ci95": [
   -0.544592909787311,
   0.12767737727339806
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.22727282725781275
 },
 "B-FLORES (flores): GPT": {
  "beqaror": false,
  "ci95": [
   -0.30338084357726663,
   0.44576037540994284
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.08912496301848635
 },
 "B-FLORES (flores): GT": {
  "beqaror": false,
  "ci95": [
   -0.4830331721802036,
   0.25107513767296635
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.13936741578273734
 },
 "B-FLORES (flores): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3387279527004312,
   0.3870817751839765
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.026422135756482237
 },
 "B-FLORES (flores): KKT": {
  "beqaror": false,
  "ci95": [
   -0.1353537962526291,
   0.5330179473318197
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.2102081496918898
 },
 "B-FLORES (flores): umumiy": {
  "beqaror": false,
  "ci95": [
   0.22052675328226173,
   0.5038839434432448
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.3739539262201052
 },
 "B-KKT (train+gold): Claude": {
  "beqaror": false,
  "ci95": [
   -0.2810098408716255,
   0.3823425529337565
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.0423734628062838
 },
 "B-KKT (train+gold): GPT": {
  "beqaror": false,
  "ci95": [
   -0.45888007989289115,
   0.20504365163126398
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.14791006554857072
 },
 "B-KKT (train+gold): GT": {
  "beqaror": false,
  "ci95": [
   -0.45664944410701125,
   0.3042499121005639
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.07140005118453246
 },
 "B-KKT (train+gold): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.2263890495503716,
   0.4241356808778445
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.10719280556036154
 },
 "B-KKT (train+gold): KKT": {
  "beqaror": false,
  "ci95": [
   0.5225285856347074,
   0.8166988388235332
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.6985909919281914
 },
 "B-KKT (train+gold): umumiy": {
  "beqaror": false,
  "ci95": [
   0.12555598175780563,
   0.42619326390448026
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.2783088274969841
 },
 "qatlam flores: Claude": {
  "beqaror": false,
  "ci95": [
   -0.544592909787311,
   0.12767737727339806
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.22727282725781275
 },
 "qatlam flores: GPT": {
  "beqaror": false,
  "ci95": [
   -0.30338084357726663,
   0.44576037540994284
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.08912496301848635
 },
 "qatlam flores: GT": {
  "beqaror": false,
  "ci95": [
   -0.4830331721802036,
   0.25107513767296635
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.13936741578273734
 },
 "qatlam flores: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3387279527004312,
   0.3870817751839765
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.026422135756482237
 },
 "qatlam flores: KKT": {
  "beqaror": false,
  "ci95": [
   -0.1353537962526291,
   0.5330179473318197
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.2102081496918898
 },
 "qatlam flores: umumiy": {
  "beqaror": false,
  "ci95": [
   0.22052675328226173,
   0.5038839434432448
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.3739539262201052
 },
 "qatlam gold: Claude": {
  "beqaror": true,
  "ci95": [
   -0.5268938410366768,
   0.6754803951696564
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.032762546404063626
 },
 "qatlam gold: GPT": {
  "beqaror": true,
  "ci95": [
   -0.8716019289105664,
   0.6500015491546096
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": -0.05851968289429745
 },
 "qatlam gold: GT": {
  "beqaror": true,
  "ci95": [
   -0.3651062626494241,
   0.8769028133059115
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.40680264750167855
 },
 "qatlam gold: Gemini": {
  "beqaror": true,
  "ci95": [
   -0.8001811389132237,
   0.5199469468957452
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": -0.21281413268968716
 },
 "qatlam gold: KKT": {
  "beqaror": true,
  "ci95": [
   -0.20884165363581805,
   0.7479461901272993
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.360248004759387
 },
 "qatlam gold: umumiy": {
  "beqaror": true,
  "ci95": [
   -0.1185944557370853,
   0.3923288879595045
  ],
  "n": 60,
  "noyob_gap": 12,
  "spearman": 0.14532288186838258
 },
 "qatlam train: Claude": {
  "beqaror": false,
  "ci95": [
   -0.6125449369145903,
   0.27262998803360045
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.21430365340039062
 },
 "qatlam train: GPT": {
  "beqaror": false,
  "ci95": [
   -0.7069199034508571,
   0.14231884032058173
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.32422270327584896
 },
 "qatlam train: GT": {
  "beqaror": false,
  "ci95": [
   -0.7833606804590525,
   -0.0912453978985071
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.48341279286108
 },
 "qatlam train: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.10863499448493706,
   0.6456664857796244
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.2802896040972745
 },
 "qatlam train: KKT": {
  "beqaror": false,
  "ci95": [
   -0.07658136145871244,
   0.6819890564246985
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.37370125142347155
 },
 "qatlam train: umumiy": {
  "beqaror": false,
  "ci95": [
   0.05952122689103681,
   0.4508501607055431
  ],
  "n": 120,
  "noyob_gap": 24,
  "spearman": 0.2645234432453639
 },
 "tizim ichida: Claude": {
  "beqaror": false,
  "ci95": [
   -0.31828682637715366,
   0.1803223266804536
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": -0.0726605274266656
 },
 "tizim ichida: GPT": {
  "beqaror": false,
  "ci95": [
   -0.2272011505234355,
   0.2772499026319041
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.023493813904777606
 },
 "tizim ichida: GT": {
  "beqaror": false,
  "ci95": [
   -0.29540318252108344,
   0.2038064050680516
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": -0.06395459677251271
 },
 "tizim ichida: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.1278037590890163,
   0.32940829339654226
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.10451008543408544
 },
 "tizim ichida: KKT": {
  "beqaror": false,
  "ci95": [
   0.340169887122718,
   0.7160313516096555
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.5613076860517641
 },
 "umumiy": {
  "beqaror": false,
  "ci95": [
   0.24808243068735533,
   0.4480790712956643
  ],
  "n": 360,
  "noyob_gap": 72,
  "spearman": 0.3538876096985904
 }
}
```

## H5 Past ball rejimi (gap-BLEU_1ref < 10): Kendall τ-b — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "Claude": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GPT": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GT": {
  "kendall_tau_b": NaN,
  "n": 2
 },
 "Gemini": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "KKT": {
  "kendall_tau_b": 0.109361287979375,
  "n": 52
 },
 "hammasi": {
  "kendall_tau_b": 0.05142043924705198,
  "n": 57
 }
}
```

## H6 P3 juftlik Spearman — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "adequacy: B–C": 0.32212227614926897,
 "adequacy: B–D": 0.35744441920861264,
 "adequacy: C–D": 0.33751811399576115,
 "fluency: B–C": 0.29364880056344356,
 "fluency: B–D": 0.25396589155704635,
 "fluency: C–D": 0.18836092075310462
}
```

## H7 P3 Krippendorff α (ordinal) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "adequacy": 0.12222186906589394,
 "fluency": -0.0706907162856425
}
```

## H8 S4 tartib ta'siri R1 − R2 (tadqiqiy) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{
 "adequacy: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.0625,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.0763888888888889,
   0.2013888888888889
  ]
 },
 "adequacy: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.006944444444444444,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.14583333333333334,
   0.1597222222222222
  ]
 },
 "adequacy: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.0625,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.13194444444444445,
   0.24305555555555555
  ]
 },
 "adequacy: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.1388888888888889,
  "R2": [
   "C"
  ],
  "ci95": [
   0.006944444444444444,
   0.2708333333333333
  ]
 },
 "adequacy: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.9375,
  "R2": [
   "C"
  ],
  "ci95": [
   -1.1180555555555556,
   -0.7430555555555556
  ]
 },
 "adequacy: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.13333333333333333,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.22083333333333333,
   -0.05
  ]
 },
 "fluency: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.20833333333333334,
  "R2": [
   "C"
  ],
  "ci95": [
   0.041666666666666664,
   0.3680555555555556
  ]
 },
 "fluency: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.1527777777777778,
  "R2": [
   "C"
  ],
  "ci95": [
   0.006944444444444444,
   0.2986111111111111
  ]
 },
 "fluency: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.24305555555555555,
  "R2": [
   "C"
  ],
  "ci95": [
   0.06944444444444445,
   0.4097222222222222
  ]
 },
 "fluency: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.2638888888888889,
  "R2": [
   "C"
  ],
  "ci95": [
   0.13194444444444445,
   0.4166666666666667
  ]
 },
 "fluency: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.7222222222222222,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.9097222222222222,
   -0.5208333333333334
  ]
 },
 "fluency: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.029166666666666667,
  "R2": [
   "C"
  ],
  "ci95": [
   -0.05694444444444444,
   0.11527777777777778
  ]
 }
}
```

## H9 LLM-hakam vs inson o'rtachasi: Spearman (tadqiqiy) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan)

```
{}
```

# EKSPLORATIV (tuzatish 4 c — tasdiqlovchi test emas)

## X1 EKSPLORATIV: KKT B-FLORES − A (1 etalon; tasdiqlovchi test EMAS)

```
{
 "A": {
  "bleu": 2.771892377488271,
  "chrf2": 38.63787853704114,
  "gap_bleu_ortacha_exp": 5.232674687538626,
  "n": 400
 },
 "B-FLORES": {
  "bleu": 1.5991899787889943,
  "chrf2": 39.65075512529217,
  "gap_bleu_ortacha_exp": 4.921457796274801,
  "n": 36
 },
 "bleu_farq_B_minus_A": -1.1727023986992768,
 "bleu_farq_ci95_bootstrap": [
  -1.8428699022809818,
  -0.562045162914909
 ],
 "chrf2_farq_B_minus_A": 1.0128765882510322
}
```

# SEZGIRLIK «E bilan» (tuzatish 10 (d))

Baholovchilar: ["B", "C", "D", "E"] · E manba xom/E__baho_E.xlsx · E darvoza {"a_toliqlik": true, "b_diapazon": true, "c_avtopilot_eng_uzun": 17, "c_belgi": true, "d_spearman_adq_flu": 0.7724074866340501, "d_belgi": false, "e_teng_ulush": 0.7333333333333333, "e_belgi": false}

## H2 Inson adequacy/fluency o'rtachasi (tizim bo'yicha) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "Claude": {
  "adequacy": 4.46830985915493,
  "baholovchi": 4,
  "fluency": 4.446009389671361,
  "n": 71
 },
 "GPT": {
  "adequacy": 4.457746478873239,
  "baholovchi": 4,
  "fluency": 4.443661971830986,
  "n": 71
 },
 "GT": {
  "adequacy": 4.419014084507042,
  "baholovchi": 4,
  "fluency": 4.462441314553991,
  "n": 71
 },
 "Gemini": {
  "adequacy": 4.529342723004695,
  "baholovchi": 4,
  "fluency": 4.495305164319248,
  "n": 71
 },
 "KKT": {
  "adequacy": 3.2007042253521125,
  "baholovchi": 4,
  "fluency": 3.0035211267605635,
  "n": 71
 }
}
```

## H3 S2 kalibrovka: adequacy o'rtachasi >= 4,5 bo'lgan chiqishlar, 1 etalon — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "Claude": {
  "bleu": 54.57196308598297,
  "chrf2": 75.88164294084336,
  "gap_bleu_ortacha_exp": 51.122301390250435,
  "n": 43
 },
 "GPT": {
  "bleu": 39.55903800510428,
  "chrf2": 68.10753995917042,
  "gap_bleu_ortacha_exp": 39.3257307095553,
  "n": 41
 },
 "GT": {
  "bleu": 45.877134170736284,
  "chrf2": 71.75193298645266,
  "gap_bleu_ortacha_exp": 47.93848590292225,
  "n": 49
 },
 "Gemini": {
  "bleu": 46.031188452222096,
  "chrf2": 72.34017333583631,
  "gap_bleu_ortacha_exp": 44.382080570580996,
  "n": 47
 },
 "KKT": {
  "bleu": 36.26545607359976,
  "chrf2": 72.77964848056368,
  "gap_bleu_ortacha_exp": 44.17458733952129,
  "n": 12
 },
 "hammasi": {
  "bleu": 46.49986863651519,
  "chrf2": 72.09794947891743,
  "gap_bleu_ortacha_exp": 45.70652376566301,
  "n": 192
 }
}
```

## H4 S3 ρ(gap-BLEU_1ref, adequacy): umumiy, tizim ichida, qatlam bo'yicha (bootstrap 1000) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "B-FLORES (flores): Claude": {
  "beqaror": false,
  "ci95": [
   -0.568367416827161,
   0.08925664467858266
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.273323363329881
 },
 "B-FLORES (flores): GPT": {
  "beqaror": false,
  "ci95": [
   -0.2864729360873194,
   0.48465960001908776
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.13929188743674326
 },
 "B-FLORES (flores): GT": {
  "beqaror": false,
  "ci95": [
   -0.48545721373574213,
   0.24998334405146477
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.12107782147605414
 },
 "B-FLORES (flores): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3327714056489656,
   0.38603685217589345
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.043789542800117015
 },
 "B-FLORES (flores): KKT": {
  "beqaror": false,
  "ci95": [
   0.015082167299145759,
   0.6808484625615054
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.36593107892643845
 },
 "B-FLORES (flores): umumiy": {
  "beqaror": false,
  "ci95": [
   0.2763059285109592,
   0.5568573067502685
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.42499613306043893
 },
 "B-KKT (train+gold): Claude": {
  "beqaror": false,
  "ci95": [
   -0.3505916177682167,
   0.3330793729356224
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": -0.0050464986460037825
 },
 "B-KKT (train+gold): GPT": {
  "beqaror": false,
  "ci95": [
   -0.4788696809042512,
   0.19670516910325742
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": -0.14984328431136493
 },
 "B-KKT (train+gold): GT": {
  "beqaror": false,
  "ci95": [
   -0.2774560013596644,
   0.46127985385828485
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": 0.1056501134747893
 },
 "B-KKT (train+gold): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.1699561292224434,
   0.4581119991902806
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": 0.1431372262713199
 },
 "B-KKT (train+gold): KKT": {
  "beqaror": false,
  "ci95": [
   0.520406702687197,
   0.8145182253268224
  ],
  "n": 35,
  "noyob_gap": 35,
  "spearman": 0.7089992978237253
 },
 "B-KKT (train+gold): umumiy": {
  "beqaror": false,
  "ci95": [
   0.1769533994947015,
   0.4851127898357939
  ],
  "n": 175,
  "noyob_gap": 35,
  "spearman": 0.3361815549297228
 },
 "qatlam flores: Claude": {
  "beqaror": false,
  "ci95": [
   -0.568367416827161,
   0.08925664467858266
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.273323363329881
 },
 "qatlam flores: GPT": {
  "beqaror": false,
  "ci95": [
   -0.2864729360873194,
   0.48465960001908776
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.13929188743674326
 },
 "qatlam flores: GT": {
  "beqaror": false,
  "ci95": [
   -0.48545721373574213,
   0.24998334405146477
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.12107782147605414
 },
 "qatlam flores: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3327714056489656,
   0.38603685217589345
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.043789542800117015
 },
 "qatlam flores: KKT": {
  "beqaror": false,
  "ci95": [
   0.015082167299145759,
   0.6808484625615054
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.36593107892643845
 },
 "qatlam flores: umumiy": {
  "beqaror": false,
  "ci95": [
   0.2763059285109592,
   0.5568573067502685
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.42499613306043893
 },
 "qatlam gold: Claude": {
  "beqaror": true,
  "ci95": [
   -0.6154888549862174,
   0.6817541583256873
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.03216429268095617
 },
 "qatlam gold: GPT": {
  "beqaror": true,
  "ci95": [
   -0.9128709291752769,
   0.6316515722272893
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.11829695303011788
 },
 "qatlam gold: GT": {
  "beqaror": true,
  "ci95": [
   -0.13406480813794908,
   0.9617334967033845
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": 0.5928141120356123
 },
 "qatlam gold: Gemini": {
  "beqaror": true,
  "ci95": [
   -0.7909440037459108,
   0.5533985905294664
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": -0.18975834751777035
 },
 "qatlam gold: KKT": {
  "beqaror": true,
  "ci95": [
   -0.13213749452868195,
   0.7974837287258641
  ],
  "n": 11,
  "noyob_gap": 11,
  "spearman": 0.44730152327606215
 },
 "qatlam gold: umumiy": {
  "beqaror": true,
  "ci95": [
   -0.12245549260708807,
   0.41227939196027386
  ],
  "n": 55,
  "noyob_gap": 11,
  "spearman": 0.1605058022714613
 },
 "qatlam train: Claude": {
  "beqaror": false,
  "ci95": [
   -0.6125449369145903,
   0.284084607374495
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.20643049804774094
 },
 "qatlam train: GPT": {
  "beqaror": false,
  "ci95": [
   -0.6950536821847101,
   0.2806600645822985
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.23920607337169011
 },
 "qatlam train: GT": {
  "beqaror": false,
  "ci95": [
   -0.7228583264893773,
   0.10995397647205447
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.33582345291730514
 },
 "qatlam train: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.10863499448493706,
   0.6441835802628162
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.27919489750885323
 },
 "qatlam train: KKT": {
  "beqaror": false,
  "ci95": [
   -0.11970361158904975,
   0.6400978424504555
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.3266362307147263
 },
 "qatlam train: umumiy": {
  "beqaror": false,
  "ci95": [
   0.12405168229869043,
   0.5101791145424703
  ],
  "n": 120,
  "noyob_gap": 24,
  "spearman": 0.3364008659178739
 },
 "tizim ichida: Claude": {
  "beqaror": false,
  "ci95": [
   -0.3718908719802253,
   0.12180048224746953
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": -0.1303634896753909
 },
 "tizim ichida: GPT": {
  "beqaror": false,
  "ci95": [
   -0.20413980059979772,
   0.3179747533062382
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.05109169611207544
 },
 "tizim ichida: GT": {
  "beqaror": false,
  "ci95": [
   -0.2470700764340226,
   0.27835448036426497
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.012360503177857026
 },
 "tizim ichida: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.11296200069818178,
   0.3678833006968567
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.12885475445104747
 },
 "tizim ichida: KKT": {
  "beqaror": false,
  "ci95": [
   0.384319823086481,
   0.7509531884463284
  ],
  "n": 71,
  "noyob_gap": 71,
  "spearman": 0.5896308644692548
 },
 "umumiy": {
  "beqaror": false,
  "ci95": [
   0.2877346594017027,
   0.5006103774042883
  ],
  "n": 355,
  "noyob_gap": 71,
  "spearman": 0.40004223055525384
 }
}
```

## H5 Past ball rejimi (gap-BLEU_1ref < 10): Kendall τ-b — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "Claude": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GPT": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GT": {
  "kendall_tau_b": NaN,
  "n": 2
 },
 "Gemini": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "KKT": {
  "kendall_tau_b": 0.1866065989481959,
  "n": 52
 },
 "hammasi": {
  "kendall_tau_b": 0.09600807573139718,
  "n": 57
 }
}
```

## H6 P3 juftlik Spearman — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "adequacy: B–C": 0.31163426183100984,
 "adequacy: B–D": 0.35478975840973187,
 "adequacy: B–E": 0.5662472999524747,
 "adequacy: C–D": 0.33284525383107266,
 "adequacy: C–E": 0.1921546834970063,
 "adequacy: D–E": 0.3889908742444725,
 "fluency: B–C": 0.2794365780047855,
 "fluency: B–D": 0.2535420317324254,
 "fluency: B–E": 0.5800437265464476,
 "fluency: C–D": 0.18636325061554326,
 "fluency: C–E": 0.21229622331753606,
 "fluency: D–E": 0.3097447770823856
}
```

## H7 P3 Krippendorff α (ordinal) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "adequacy": 0.20324708498005406,
 "fluency": 0.08530551526891372
}
```

## H8 S4 tartib ta'siri R1 − R2 (tadqiqiy) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{
 "adequacy: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.24647887323943662,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.3873239436619718,
   -0.11267605633802817
  ]
 },
 "adequacy: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.28169014084507044,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.4225352112676056,
   -0.14084507042253522
  ]
 },
 "adequacy: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.13380281690140844,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.30985915492957744,
   0.014084507042253521
  ]
 },
 "adequacy: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1619718309859155,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2746478873239437,
   -0.04929577464788732
  ]
 },
 "adequacy: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.14788732394366197,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2887323943661972,
   0.0
  ]
 },
 "adequacy: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.19436619718309858,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2577464788732394,
   -0.1352112676056338
  ]
 },
 "fluency: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1619718309859155,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.30985915492957744,
   -0.02112676056338028
  ]
 },
 "fluency: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.2112676056338028,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.352112676056338,
   -0.07042253521126761
  ]
 },
 "fluency: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.07746478873239436,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.21830985915492956,
   0.056338028169014086
  ]
 },
 "fluency: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.09154929577464789,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2323943661971831,
   0.035211267605633804
  ]
 },
 "fluency: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.3732394366197183,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   0.21830985915492956,
   0.5352112676056338
  ]
 },
 "fluency: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.03380281690140845,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.09859154929577464,
   0.029577464788732393
  ]
 }
}
```

## H9 LLM-hakam vs inson o'rtachasi: Spearman (tadqiqiy) — ASOSIY 71 (gold-00 chiqarilgan; tuzatish 7) [E bilan]

```
{}
```

## H2 Inson adequacy/fluency o'rtachasi (tizim bo'yicha) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "Claude": {
  "adequacy": 4.475694444444445,
  "baholovchi": 4,
  "fluency": 4.453703703703703,
  "n": 72
 },
 "GPT": {
  "adequacy": 4.465277777777778,
  "baholovchi": 4,
  "fluency": 4.451388888888889,
  "n": 72
 },
 "GT": {
  "adequacy": 4.423611111111111,
  "baholovchi": 4,
  "fluency": 4.466435185185186,
  "n": 72
 },
 "Gemini": {
  "adequacy": 4.53587962962963,
  "baholovchi": 4,
  "fluency": 4.502314814814814,
  "n": 72
 },
 "KKT": {
  "adequacy": 3.21875,
  "baholovchi": 4,
  "fluency": 3.0277777777777777,
  "n": 72
 }
}
```

## H3 S2 kalibrovka: adequacy o'rtachasi >= 4,5 bo'lgan chiqishlar, 1 etalon — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "Claude": {
  "bleu": 54.78418841473052,
  "chrf2": 76.05614066834256,
  "gap_bleu_ortacha_exp": 52.23315817683565,
  "n": 44
 },
 "GPT": {
  "bleu": 39.82459871936174,
  "chrf2": 68.35233529691376,
  "gap_bleu_ortacha_exp": 40.19853637278396,
  "n": 42
 },
 "GT": {
  "bleu": 45.84337357584092,
  "chrf2": 71.68476212425881,
  "gap_bleu_ortacha_exp": 47.83429019765628,
  "n": 50
 },
 "Gemini": {
  "bleu": 45.9801307161584,
  "chrf2": 72.2502997614298,
  "gap_bleu_ortacha_exp": 44.133845382600356,
  "n": 48
 },
 "KKT": {
  "bleu": 35.369129818761046,
  "chrf2": 72.46563307398472,
  "gap_bleu_ortacha_exp": 42.54250281083614,
  "n": 13
 },
 "hammasi": {
  "bleu": 46.52941862286393,
  "chrf2": 72.14042843179193,
  "gap_bleu_ortacha_exp": 45.93801579810256,
  "n": 197
 }
}
```

## H4 S3 ρ(gap-BLEU_1ref, adequacy): umumiy, tizim ichida, qatlam bo'yicha (bootstrap 1000) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "B-FLORES (flores): Claude": {
  "beqaror": false,
  "ci95": [
   -0.568367416827161,
   0.08925664467858266
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.273323363329881
 },
 "B-FLORES (flores): GPT": {
  "beqaror": false,
  "ci95": [
   -0.2864729360873194,
   0.48465960001908776
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.13929188743674326
 },
 "B-FLORES (flores): GT": {
  "beqaror": false,
  "ci95": [
   -0.48545721373574213,
   0.24998334405146477
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.12107782147605414
 },
 "B-FLORES (flores): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3327714056489656,
   0.38603685217589345
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.043789542800117015
 },
 "B-FLORES (flores): KKT": {
  "beqaror": false,
  "ci95": [
   0.015082167299145759,
   0.6808484625615054
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.36593107892643845
 },
 "B-FLORES (flores): umumiy": {
  "beqaror": false,
  "ci95": [
   0.2763059285109592,
   0.5568573067502685
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.42499613306043893
 },
 "B-KKT (train+gold): Claude": {
  "beqaror": false,
  "ci95": [
   -0.2791846254508485,
   0.38790734558932116
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.047994942657718934
 },
 "B-KKT (train+gold): GPT": {
  "beqaror": false,
  "ci95": [
   -0.43531073380225077,
   0.25668587395935666
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.10171359526988538
 },
 "B-KKT (train+gold): GT": {
  "beqaror": false,
  "ci95": [
   -0.29634274298158364,
   0.44208499723610845
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.0948375599847547
 },
 "B-KKT (train+gold): Gemini": {
  "beqaror": false,
  "ci95": [
   -0.2249393495427554,
   0.41510231878124115
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.10677294098590473
 },
 "B-KKT (train+gold): KKT": {
  "beqaror": false,
  "ci95": [
   0.5288818156279607,
   0.8252516748947879
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.7192831354311264
 },
 "B-KKT (train+gold): umumiy": {
  "beqaror": false,
  "ci95": [
   0.19357116649421202,
   0.4803031867404965
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.3394992763749489
 },
 "qatlam flores: Claude": {
  "beqaror": false,
  "ci95": [
   -0.568367416827161,
   0.08925664467858266
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.273323363329881
 },
 "qatlam flores: GPT": {
  "beqaror": false,
  "ci95": [
   -0.2864729360873194,
   0.48465960001908776
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.13929188743674326
 },
 "qatlam flores: GT": {
  "beqaror": false,
  "ci95": [
   -0.48545721373574213,
   0.24998334405146477
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": -0.12107782147605414
 },
 "qatlam flores: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.3327714056489656,
   0.38603685217589345
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.043789542800117015
 },
 "qatlam flores: KKT": {
  "beqaror": false,
  "ci95": [
   0.015082167299145759,
   0.6808484625615054
  ],
  "n": 36,
  "noyob_gap": 36,
  "spearman": 0.36593107892643845
 },
 "qatlam flores: umumiy": {
  "beqaror": false,
  "ci95": [
   0.2763059285109592,
   0.5568573067502685
  ],
  "n": 180,
  "noyob_gap": 36,
  "spearman": 0.42499613306043893
 },
 "qatlam gold: Claude": {
  "beqaror": true,
  "ci95": [
   -0.5268938410366768,
   0.6754803951696564
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.032762546404063626
 },
 "qatlam gold: GPT": {
  "beqaror": true,
  "ci95": [
   -0.8716019289105664,
   0.6500015491546096
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": -0.05851968289429745
 },
 "qatlam gold: GT": {
  "beqaror": true,
  "ci95": [
   -0.15685660980641014,
   0.9535352589297225
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.5644660654374936
 },
 "qatlam gold: Gemini": {
  "beqaror": true,
  "ci95": [
   -0.8001811389132237,
   0.5199469468957452
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": -0.21281413268968716
 },
 "qatlam gold: KKT": {
  "beqaror": true,
  "ci95": [
   -0.09393364366277242,
   0.7576044600931726
  ],
  "n": 12,
  "noyob_gap": 12,
  "spearman": 0.4393567470120815
 },
 "qatlam gold: umumiy": {
  "beqaror": true,
  "ci95": [
   -0.06647540195812263,
   0.42930232441960303
  ],
  "n": 60,
  "noyob_gap": 12,
  "spearman": 0.1964878899458326
 },
 "qatlam train: Claude": {
  "beqaror": false,
  "ci95": [
   -0.6125449369145903,
   0.284084607374495
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.20643049804774094
 },
 "qatlam train: GPT": {
  "beqaror": false,
  "ci95": [
   -0.6950536821847101,
   0.2806600645822985
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.23920607337169011
 },
 "qatlam train: GT": {
  "beqaror": false,
  "ci95": [
   -0.7228583264893773,
   0.10995397647205447
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": -0.33582345291730514
 },
 "qatlam train: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.10863499448493706,
   0.6441835802628162
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.27919489750885323
 },
 "qatlam train: KKT": {
  "beqaror": false,
  "ci95": [
   -0.11970361158904975,
   0.6400978424504555
  ],
  "n": 24,
  "noyob_gap": 24,
  "spearman": 0.3266362307147263
 },
 "qatlam train: umumiy": {
  "beqaror": false,
  "ci95": [
   0.12405168229869043,
   0.5101791145424703
  ],
  "n": 120,
  "noyob_gap": 24,
  "spearman": 0.3364008659178739
 },
 "tizim ichida: Claude": {
  "beqaror": false,
  "ci95": [
   -0.33162938815144727,
   0.1470628010888903
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": -0.09261233970050049
 },
 "tizim ichida: GPT": {
  "beqaror": false,
  "ci95": [
   -0.18596329900413383,
   0.3383894422474888
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.07889768507197875
 },
 "tizim ichida: GT": {
  "beqaror": false,
  "ci95": [
   -0.2377292847848286,
   0.29917332817669745
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.010846932122281026
 },
 "tizim ichida: Gemini": {
  "beqaror": false,
  "ci95": [
   -0.10810832955403149,
   0.33986600484474144
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.11697540291620985
 },
 "tizim ichida: KKT": {
  "beqaror": false,
  "ci95": [
   0.39709421072424567,
   0.7604005319169014
  ],
  "n": 72,
  "noyob_gap": 72,
  "spearman": 0.6041900069748236
 },
 "umumiy": {
  "beqaror": false,
  "ci95": [
   0.30130380531673984,
   0.4972279155889276
  ],
  "n": 360,
  "noyob_gap": 72,
  "spearman": 0.4028595258082223
 }
}
```

## H5 Past ball rejimi (gap-BLEU_1ref < 10): Kendall τ-b — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "Claude": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GPT": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "GT": {
  "kendall_tau_b": NaN,
  "n": 2
 },
 "Gemini": {
  "kendall_tau_b": NaN,
  "n": 1
 },
 "KKT": {
  "kendall_tau_b": 0.1866065989481959,
  "n": 52
 },
 "hammasi": {
  "kendall_tau_b": 0.09600807573139718,
  "n": 57
 }
}
```

## H6 P3 juftlik Spearman — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "adequacy: B–C": 0.32212227614926897,
 "adequacy: B–D": 0.35744441920861264,
 "adequacy: B–E": 0.5640117600032513,
 "adequacy: C–D": 0.33751811399576115,
 "adequacy: C–E": 0.19263590439685424,
 "adequacy: D–E": 0.3881503065036364,
 "fluency: B–C": 0.29364880056344356,
 "fluency: B–D": 0.25396589155704635,
 "fluency: B–E": 0.5792960431182232,
 "fluency: C–D": 0.18836092075310462,
 "fluency: C–E": 0.22124413573892723,
 "fluency: D–E": 0.3104755890870448
}
```

## H7 P3 Krippendorff α (ordinal) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "adequacy": 0.20709223059755255,
 "fluency": 0.09048077884498196
}
```

## H8 S4 tartib ta'siri R1 − R2 (tadqiqiy) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{
 "adequacy: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.24305555555555555,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.375,
   -0.1111111111111111
  ]
 },
 "adequacy: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.2777777777777778,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.4166666666666667,
   -0.1388888888888889
  ]
 },
 "adequacy: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1388888888888889,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.3125,
   0.020833333333333332
  ]
 },
 "adequacy: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1597222222222222,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2708333333333333,
   -0.04861111111111111
  ]
 },
 "adequacy: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.14583333333333334,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2777777777777778,
   -0.020833333333333332
  ]
 },
 "adequacy: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.19305555555555556,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.25833333333333336,
   -0.12916666666666668
  ]
 },
 "fluency: Claude": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.1597222222222222,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.3055555555555556,
   -0.020833333333333332
  ]
 },
 "fluency: GPT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.20833333333333334,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.3472222222222222,
   -0.0763888888888889
  ]
 },
 "fluency: GT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.08333333333333333,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.2152777777777778,
   0.041666666666666664
  ]
 },
 "fluency: Gemini": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.09027777777777778,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.20833333333333334,
   0.027777777777777776
  ]
 },
 "fluency: KKT": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": 0.3611111111111111,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   0.20833333333333334,
   0.5138888888888888
  ]
 },
 "fluency: hammasi": {
  "R1": [
   "B",
   "D"
  ],
  "R1_minus_R2": -0.03611111111111111,
  "R2": [
   "C",
   "E"
  ],
  "ci95": [
   -0.09861111111111111,
   0.030555555555555555
  ]
 }
}
```

## H9 LLM-hakam vs inson o'rtachasi: Spearman (tadqiqiy) — SEZGIRLIK 72 (1-to'lqin bilan taqqoslanuvchan) [E bilan]

```
{}
```

