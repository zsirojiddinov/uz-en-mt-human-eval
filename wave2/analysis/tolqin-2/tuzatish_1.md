# Tuzatish 1 (neyron chiqishlar olinishidan oldin)
Sabab: Anthropic, OpenAI va Google Cloud API kalitlari uchun vaqt va mablag' yo'q.
2.3 va 2.6 o'rniga: Gemini — API (mavjud kalit), model identifikatori qayd etiladi.
Claude — alohida Claude Code sessiyalari, bo'sh papkada, faqat ko'rsatma va kirish fayli;
model identifikatori sessiya transkriptidan. GPT — ChatGPT veb, vaqtinchalik chat (xotira va
tarixsiz); interfeysdagi model nomi va tanlov oynasi skrinshoti qayd etiladi, texnik
identifikator qayd etilmaydi. Google Translate — translate.google.com veb; versiyasi qayd
etib bo'lmaydi. Paketlash: 472 gap (A-qavat 400 + eval72) seed 20261016 bilan aralashtirilib,
LLM'lar uchun 40 talik (12 ta), Google Translate uchun 25 talik (19 ta) raqamlangan to'plamga
bo'linadi; uchala LLM (Gemini ham) bir xil to'plam va bir xil prompt bilan:
"Translate each numbered Uzbek sentence into English. Keep the numbering. Output only the
numbered translations, one per line." Har to'plam yangi chat/sessiyada. Barcha neyron
chiqishlar bitta kalendar kun ichida olinadi, har to'plam vaqti qayd etiladi. Javob tahrirsiz
saqlanadi; yetishmagan/buzilgan raqamlar faqat yangi chatda qayta so'raladi va qayd etiladi.
2.3 dagi «veb bilan almashtirilmaydi» qoidasi shu tuzatish bilan o'rnini bo'shatadi; bu
maqolada cheklov sifatida yoziladi.
