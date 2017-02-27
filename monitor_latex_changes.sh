#!/opt/local/bin/bash

if [[ $# == 0 ]]; then
    echo usage: "$0 main_tex_file extra_tex_files (supplemental etc)"
    exit 1
fi

main=""
journal=PRL
while [[ $# > 0 ]]; do
    ARG="$1"; shift
    if [[ "$ARG" == "-j" ]]; then
	journal="$1"; shift
    else
	all+=("${ARG%.tex}")
    fi
done
main="${all[0]}"

(fswatch $(git ls-files) .git/refs/heads/master | while read fi; do
    git dwf | ansi2html.sh --bg=dark | sed 's/<pre>/<pre style="white-space: pre-wrap;">/' > diff.html
    open -g -a Safari diff.html
    echo "new diff!"
done)&

(fswatch "$main.tex" | while read fi; do
    apslen=$(aps-length -j "$journal" -f identify "$main.tex")
    echo "$apslen"
    notif=$(echo "$apslen" | grep currently)
    osascript -e "display notification \"${notif}\" with title \"aps-length\""
done)&

(fswatch "${all[@]/%/.tex}" /Users/feist/Documents/work/tex/mendeley/library_clean.bib | while read fi; do
    # sleep until aux files are more than 1 second old, i.e., latexmk has really finished with them
    while :; do
        allold="yes"
        for fi in "${all[@]/%/.aux}"; do
            [[ $((`date +%s` - `stat -f %m -t %s "$fi"`)) -le 1 ]] && allold="no"
        done
        [[ $allold == "yes" ]] && break || sleep 1
    done
    make_latex_references.py "${all[@]}"
    echo "new references!"
done)&

# wait until all background shells have finished (so the script can be cancelled by Ctrl-C)
wait
