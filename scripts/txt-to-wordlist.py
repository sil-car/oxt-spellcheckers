#!/usr/bin/env python3

import sys
import unicodedata

from pathlib import Path

import tools


error_msg = "Error: Please provide base directory; e.g. sg-CF_sango."
if len(sys.argv) < 2:
    print(error_msg)
    exit(1)

input_arg = Path(sys.argv[1]).resolve()
if not input_arg.is_dir():
    print(error_msg)
    exit(1)
else:
    dir = input_arg

# find "${dir}/documents" -maxdepth 1 -type f -exec grep -Eo '\w+' {} \; | grep -v '^[0-9]' | sort -fu
words = set()
for child in dir.iterdir():
    if child.is_dir():
        continue
    with child.open() as f:
        lines = f.readlines()
    for l in lines:
        wds = l.split()
        nfd_wds = tools.raw_words_to_nfd(wds)
        words.update(nfd_wds)

tools.print_sorted_set(words)
