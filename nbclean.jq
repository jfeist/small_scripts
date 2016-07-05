#!/usr/bin/env bash

jqprog='((.cells[].outputs | select(.)) |= []) | ((.cells[].execution_count | select(.)) |= null) |
        del(.metadata.widgets) | del(.metadata.toc) | del(.metadata.toc_position) | del(.metadata.nav_menu)'

if [[ "$1" = "--flatten" ]]; then
    shift
    jq -r "$jqprog" "$@" | nbflatten.jq
else
    jq -r "$jqprog" "$@"
fi
