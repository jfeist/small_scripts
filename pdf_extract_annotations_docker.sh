#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 PDFFILE" >&2
  exit 1
fi

PDFFILE=$1; shift

docker run -it --rm -e PDF_PAGESHIFT="${PDF_PAGESHIFT:-0}" -v "${PWD}:/tmp" jfeist/pdf_extract_annotations "${PDFFILE}" | grep -v '^"Error: ' | unicodeit.py | ansi2html.sh > annot.html
