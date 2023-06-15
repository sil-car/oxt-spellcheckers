#!/bin/bash

if [[ ! -d "$1" ]]; then
    echo "Error: Please provide base directory; e.g. sg-CF_sango."
    exit 1
else
    dir="$(realpath "$1")"
fi
# E = extended regex; o = only show matched text
find "${dir}/documents" -maxdepth 1 -type f -exec grep -Eo '\w+' {} \; | grep -v '^[0-9]' | sort -fu
