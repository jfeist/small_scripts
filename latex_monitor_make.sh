#!/opt/local/bin/bash

for ARG in "$@"; do
    all+=("\"$ARG\"")
done
a="${all[@]}"

temp_file=$(mktemp)

cat > $temp_file <<EOF
(start-process "latexmk" "latexmk" "latexmk" "-pvc" "$1");
(start-process "monitor" "monitor" "monitor_latex_changes.sh" ${all[@]});
(split-window-right);
(switch-to-buffer "latexmk");
(other-window 1);
(switch-to-buffer "monitor");
EOF

emacs -nw -l $temp_file

rm $temp_file
