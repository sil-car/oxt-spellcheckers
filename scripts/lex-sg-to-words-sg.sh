#!/bin/bash

# Strip out non-sg words from sg lexicon (KOYT: Illustrated Bilingual Lexicon...)
# zunda ôônë (Pandôo) : Echinops longifolius (Echinops longifolius, Asteraceae) (Noun)

title="Illustrated Bilingual Lexicon Sängö English English Sängö version augmentée"
dir="$(realpath "$(find .. -iname 'sg-CF_sango_1984' -type d)")"
file="${dir}/documents/transitional/${title}_lex-sg.txt"
if [[ ! -f "$file" ]]; then
    echo "Error: File not found: $file"
    exit 1
fi
# Ignore lines with no ':'; keep only words before 1st '('.
grep ':' "$file" | sed -E 's/^([^(]+) \(.*$/\1/'
