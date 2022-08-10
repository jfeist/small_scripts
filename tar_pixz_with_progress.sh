#!/bin/sh

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 TARGET OUTFILE" >&2
  exit 1
fi

TARGET=$1; shift
OUTFILE=$1; shift

BYTES="$(du -sb ${TARGET}/ | cut -f1)"
tar -cf - "$TARGET" \
  | tqdm --bytes --total "$BYTES" --desc Processing | pixz -9 -p 6 \
  | tqdm --bytes --total "$BYTES" --desc Compressed --position 1 \
  > "$OUTFILE"
