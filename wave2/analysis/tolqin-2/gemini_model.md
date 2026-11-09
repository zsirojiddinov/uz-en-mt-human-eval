# Gemini model tanlovi (chiqishdan OLDIN)

- So'ralgan model: Gemini 3.5 Flash.
- Identifikator: `models/gemini-3.5-flash` (so'rovda `gemini-3.5-flash`); ro'yxatdagi `version`: `3.5-flash-05-2026`;
  `display_name` «Gemini 3.5 Flash». Holat: **stable** (nomida `preview`/`exp` yo'q; shu oilaning preview varianti
  ro'yxatda yo'q). «Gemini 3.5 Pro» ro'yxatda yo'q.
- Ro'yxat: `gemini_modellar.json` (63 model), olingan 2026-10-16T12:25:07+05:00, `google-generativeai 0.8.3`
  `list_models()`; sha256 `b32e847d11fb95ddd0462b6be4a5f7d66376557e4ae2c792027d6071008422d8`.
  Model kartasi: input_token_limit 1 048 576, output_token_limit 65 536, sukut temperature 1.0, max 2.0.
- Parametrlar: temperature **0** (prereg 2.3), max_output_tokens **32768**; system-instruction yo'q;
  boshqa parametrlar sukut.
- So'rov: har `veb/kirish/llm_NN.txt` (01…12) alohida so'rov, alohida suhbat (tarixsiz). Matn =
  prompt + `"\n\n"` + kirish fayli matni (bayt-aynan).
- Prompt (Tuzatish 1, aynan):
  "Translate each numbered Uzbek sentence into English. Keep the numbering. Output only the
  numbered translations, one per line."
- Xato: vaqtinchalik xatoda 3 martagacha qayta urinish; oxirgisi ham 429 bo'lsa — to'xtaladi.
