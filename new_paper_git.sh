#!/opt/local/bin/bash

if [[ $# == 0 ]]; then
    echo usage: "$0 paper_name"
    exit 1
fi

name="$1"; shift
mkdir "$name"
cd "$name"
git init

cat > .gitignore <<EOF
*~
diff.html

*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.rel
*.synctex.gz
*.tps
*.upb
*Notes.bib
EOF

cat > .gitattributes <<EOF
*.tex diff=tex
EOF

git add .gitignore
git add .gitattributes
git ci -m 'initial commit with only .gitignore/.gitattributes'
hub create -p "tex.papers.${name}"
git remote rename origin jf
git push -u jf master
