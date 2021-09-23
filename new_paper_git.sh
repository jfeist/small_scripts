#!/usr/bin/env bash

if [[ $# == 0 ]]; then
    echo usage: "$0 paper_name"
    exit 1
fi

name="$1"; shift

gh repo create -y --gitignore TeX --private "tex.papers.${name}"
mv "tex.papers.${name}" "$name"
cd "$name"

cat > .gitattributes <<EOF
*.tex diff=tex
EOF

git add .gitattributes

git ci --amend -m 'initial commit with only .gitignore/.gitattributes'
git push -f
