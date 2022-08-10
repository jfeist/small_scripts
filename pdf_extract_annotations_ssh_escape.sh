#!/bin/sh

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 PDFFILE" >&2
  exit 1
fi

PDFFILE=$1; shift
SSHCMD="PDF_PAGESHIFT=${PDF_PAGESHIFT:-0} pdf_extract_annotations.py ${PDFFILE} | unicodeit.py | ansi2html.sh > annot.html"

export GITSTATUS_LOG_LEVEL=NONE

rsync -avz "${PDFFILE}" escape:
ssh escape "zsh -ic '$SSHCMD'" &> /dev/null
rsync -avz escape:annot.html .
ssh escape "rm '$PDFFILE'"
