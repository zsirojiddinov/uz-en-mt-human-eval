#!/bin/sh
# TOLQIN-2 — GT «Documents» rejimi natijasini olish (tuzatish 3). Javob MATNI ekranga CHIQARILMAYDI.
#
#   sh analysis/tolqin-2/gt_doc_ol.sh <NN>        # NN: 01..19
#
# translate.google.com «Documents» da veb/kirish/gt_NN.txt (yoki undan yasalgan .docx) yuklanadi, «Download translation»
# bosiladi; keyin shu skript:
#   - ~/Downloads dagi nomi gt_NN bilan boshlanadigan eng yangi .txt yoki .docx faylni oladi (nomi, yoshi va sha256 ekranga — matn emas);
#     kirish faylining o'zi (bayt-aynan gt_NN.txt yoki gt_NN.docx) bo'lsa — rad etadi;
#   - xom faylni veb/javob_xom/gt_NN.<ext> ga KO'CHIRADI (mv -n; Downloads'da qolmaydi);
#   - .txt — bayt-aynan, .docx — word/document.xml paragraflari (har paragraf bir qator, «\n», oxirida «\n»)
#     -> veb/javob/gt_NN.txt (mv -n);
#   - nishon (javob yoki xom) allaqachon bor bo'lsa — HECH NARSA yozmaydi/ko'chirmaydi, jurnal.csv ga RAD qatori;
#   - jurnal.csv ga qator; tekshir_javob.py — faqat «OK» yoki muammo (masalan «qator soni 23 != 25»).
# Yuklamalar papkasi: YUKLAMA muhit o'zgaruvchisi (sukut ~/Downloads).
set -eu
SIKL=$(cd "$(dirname "$0")" && pwd)
VEB="$SIKL/veb"
YUK="${YUKLAMA:-$HOME/Downloads}"
nn="${1:-}"
case "$nn" in 0[1-9]|1[0-9]) ;; *) echo "NN: 01..19"; exit 2 ;; esac
[ "$nn" -le 19 ] || { echo "NN: 01..19"; exit 2; }
fayl="gt_${nn}.txt"
nishon="$VEB/javob/$fayl"
vaqt() { python3 -c "import datetime as d; print(d.datetime.now().astimezone().isoformat(timespec='seconds'))"; }
jurnal() { printf 'gt,%s,,%s,%s\n' "$fayl" "$(vaqt)" "$(printf '%s' "$1" | tr ',' ';')" >> "$VEB/jurnal.csv"; }

# faqat nomi gt_NN bilan boshlanadigan fayl (masalan gt_01.txt, gt_01 (1).docx) — begona hujjat OLINMAYDI
manba=$(ls -t "$YUK"/gt_"$nn"*.txt "$YUK"/gt_"$nn"*.docx "$YUK"/gt_"$nn"*.TXT "$YUK"/gt_"$nn"*.DOCX 2>/dev/null | head -1 || true)
if [ -z "$manba" ]; then echo "$YUK da gt_${nn}*.txt / gt_${nn}*.docx yo'q (boshqa nomli fayllar olinmaydi)"; exit 1; fi
nom=$(basename "$manba")
ext=$(printf '%s' "${nom##*.}" | tr 'A-Z' 'a-z')
xom="$VEB/javob_xom/gt_${nn}.${ext}"
sha=$(shasum -a 256 "$manba" | cut -d' ' -f1)
yosh=$(( $(date +%s) - $(stat -f %m "$manba") ))
echo "manba: $nom · ${yosh} s oldin · sha256 $sha"
for k in "$VEB/kirish/gt_${nn}.txt" "$VEB/kirish/gt_${nn}.docx"; do
  if cmp -s "$manba" "$k"; then echo "RAD: bu kirish faylining o'zi ($(basename "$k")) — tarjima emas"; exit 1; fi
done
for x in "$nishon" "$VEB/javob_xom/gt_${nn}".*; do
  if [ -e "$x" ]; then
    echo "OGOHLANTIRISH: $(basename "$x") allaqachon bor — hech narsa yozilmadi/ko'chirilmadi"
    jurnal "RAD: $(basename "$x") allaqachon bor — yozilmadi (gt_doc_ol.sh; manba $nom sha256 $sha)"
    exit 1
  fi
done
mkdir -p "$VEB/javob_xom"
mv -n "$manba" "$xom"
[ -e "$xom" ] && [ ! -e "$manba" ] || { echo "XATO: $nom ko'chirilmadi"; exit 1; }
tmp=$(mktemp "$VEB/javob/.${fayl}.XXXXXX")
trap 'rm -f "$tmp"' EXIT
case "$ext" in
  txt) cat "$xom" > "$tmp" ;;
  docx) python3 - "$xom" "$tmp" <<'PY'
import re, sys, zipfile
from xml.sax.saxutils import unescape
x = zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8')
body = x.split('<w:body', 1)[1]
qator = []
for p in re.findall(r'<w:p[ >].*?</w:p>|<w:p/>', body, re.S):
    s = ''
    for tok in re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>|<w:t/>|(<w:tab/>)|(<w:br/>)', p, re.S):
        s += unescape(tok[0], {'&quot;': '"', '&apos;': "'"}) if tok[0] else ('\t' if tok[1] else '\n' if tok[2] else '')
    qator.append(s)
while qator and qator[-1] == '':
    qator.pop()
open(sys.argv[2], 'wb').write(('\n'.join(qator) + '\n').encode('utf-8'))
PY
  ;;
  *) echo "kengaytma $ext"; exit 1 ;;
esac
if [ -e "$nishon" ]; then echo "OGOHLANTIRISH: $fayl shu orada paydo bo'ldi — yozilmadi"; jurnal "RAD: $fayl shu orada paydo bo'ldi — yozilmadi"; exit 1; fi
mv -n "$tmp" "$nishon"
[ ! -e "$tmp" ] || { echo "XATO: $fayl yozilmadi"; exit 1; }
trap - EXIT
b=$(wc -c < "$nishon" | tr -d ' ')
jurnal "veb Documents (gt_doc_ol.sh); yuklangan $nom ($ext) sha256 $sha -> javob_xom/gt_${nn}.${ext}; bayt $b"
natija=$(python3 "$SIKL/tekshir_javob.py" "$nishon" 2>&1 | tail -1) || true
echo "${natija#*— }"
