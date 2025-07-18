#!/bin/sh

set -e
# set -x

# from https://unix.stackexchange.com/questions/230047/how-to-list-all-targets-in-make

depfile=LATEX_DEPENDENCIES

latexmk -deps-out="${depfile}" "$@" > /dev/null

targets=$(make -qp -f "${depfile}" | awk -F':' '/^[a-zA-Z0-9][^$#\t=]*:([^=]|$)/ {split($1,A,/ /);for(i in A)print A[i]}' | sort -u | grep -v -e "${depfile}" -e '.*Notes.bib')

texpdfs=$(grep '\.tex$' <<< "$targets" | sed 's/\.tex$/.pdf/')

# print the list of targets without the pdf files generated from .tex files
echo "$targets" | grep -v -e "${texpdfs}"

rm ${depfile}