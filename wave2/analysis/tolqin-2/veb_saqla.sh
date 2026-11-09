#!/bin/sh
# TOLQIN-2 — veb javobini clipboard'dan saqlash (tuzatish 1). Javob MATNI ekranga CHIQARILMAYDI.
#
#   sh analysis/tolqin-2/veb_saqla.sh <tizim> <NN>      # tizim: gpt | gemini | claude | gt;  NN: 01, 02, …
#
# Javob oynasida Copy ni bosing, shu terminalga qaytib FAQAT Enter bosing. Skript:
#   - clipboard'ni (pbpaste) veb/javob/<tizim>_NN.txt ga tahrirsiz yozadi (mv -n); fayl allaqachon bo'lsa — USTIGA
#     YOZMAYDI va jurnal.csv ga «RAD: allaqachon bor» qatori qo'shiladi;
#   - veb/jurnal.csv ga qator qo'shadi: tizim, fayl, boshlanish (bo'sh), tugash (saqlash vaqti), izoh;
#   - tekshir_javob.py ni shu faylga yurgizib faqat «OK» yoki muammoni (masalan «yetishmaydi: 7, 12») chiqaradi.
# Bufer bo'sh yoki kirish matnining o'zi (prompt bilan boshlanadi) bo'lsa — saqlamaydi, qayta so'raydi.
set -eu
SIKL=$(cd "$(dirname "$0")" && pwd)
VEB="$SIKL/veb"
tizim="${1:-}"; nn="${2:-}"
case "$tizim" in gpt|gemini|claude|gt) ;; *) echo "tizim: gpt | gemini | claude | gt"; exit 2 ;; esac
case "$nn" in [0-9][0-9]) ;; *) echo "NN ikki xonali bo'lsin (01, 02, …)"; exit 2 ;; esac
fayl="${tizim}_${nn}.txt"
nishon="$VEB/javob/$fayl"
vaqt() { python3 -c "import datetime as d; print(d.datetime.now().astimezone().isoformat(timespec='seconds'))"; }
rad() { printf '%s,%s,,%s,RAD: %s — yozilmadi (veb_saqla.sh)\n' "$tizim" "$fayl" "$(vaqt)" "$1" >> "$VEB/jurnal.csv"; }
if [ -e "$nishon" ]; then
  echo "OGOHLANTIRISH: $fayl allaqachon bor — ustiga yozilmaydi (qayta so'rov bo'lsa — alohida nom bilan qo'lda, jurnalga izoh)"
  rad "allaqachon bor"
  exit 1
fi
tmp=$(mktemp "$VEB/javob/.${fayl}.XXXXXX")
trap 'rm -f "$tmp"' EXIT
while :; do
  printf "%s: Copy ni bosing, keyin shu yerga qaytib FAQAT Enter bosing... " "$fayl"
  read _
  pbpaste > "$tmp"
  b=$(wc -c < "$tmp" | tr -d ' ')
  if [ "$b" -eq 0 ]; then echo "bufer bo'sh — qaytadan"; continue; fi
  if head -c 40 "$tmp" | grep -q '^Translate each numbered'; then
    echo "buferda kirish matni (prompt) — javobni nusxalang, qaytadan"; continue
  fi
  break
done
if [ -e "$nishon" ]; then echo "OGOHLANTIRISH: $fayl shu orada paydo bo'ldi — ustiga yozilmaydi"; rad "shu orada paydo bo'ldi"; exit 1; fi
mv -n "$tmp" "$nishon"
if [ -e "$tmp" ]; then echo "OGOHLANTIRISH: $fayl yozilmadi (mv -n)"; rad "mv -n: nishon bor"; exit 1; fi
trap - EXIT
printf '%s,%s,,%s,veb; clipboard (veb_saqla.sh); bayt %s\n' "$tizim" "$fayl" "$(vaqt)" "$b" >> "$VEB/jurnal.csv"
natija=$(python3 "$SIKL/tekshir_javob.py" "$nishon" 2>&1 | tail -1) || true
echo "${natija#*— }"
