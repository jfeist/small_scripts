#!/bin/sh
jq -r 'def banner: "\(.) " + (28-(.|length))*"-";
("Non-cell info" | banner), del(.cells), "",
(.cells[] |  ("\(.cell_type) cell" | banner),
	     "\(.source|add)",
	     if ($show_output == "1") then
                 "",
		 ( select(.cell_type=="code" and (.outputs|length)>0) |
		   ("output" | banner),
		   (.outputs[] |
		    (select(.text) | "\(.text|add)" | rtrimstr("\n")),
		    (select(.traceback) | (.traceback|join("\n"))),
		    (select(.text or .traceback|not) | "(Non-plaintext output)")
		   ),
		   ""
		 )
              else ""
	      end
)' "$@" --arg show_output 1
