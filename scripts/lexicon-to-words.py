#!/usr/bin/env python3

import re
import sys
# import unicodedata

from pathlib import Path

from tools import str_to_words
from tools import write_sorted_set


# Prepare input and output files.
repo_dir = Path(__file__).resolve().parents[1]

if len(sys.argv) < 2:
    print("Error: No lexicon file given.")
    exit(1)
elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print(f"Usage: {sys.argv[0]} LEXICON_FILE.TXT")
    exit(0)
else:
    input_arg = Path(sys.argv[1]).resolve()

if input_arg.is_file():
    input_file = input_arg
else:
    print(f"Error: Not a valid file: {input_arg}")
    exit(1)

input_lexicon = input_file.name.split('_')[1]
output_dir = input_file.parents[1]  # documents/
oxt_dir = output_dir.parent
lang = oxt_dir.name.split('_')[0]
output_file = output_dir / f"{input_file.stem}-only-{lang}.txt"

if input_lexicon == 'lex-sg.txt':
    index = 0
elif input_lexicon == 'lex-en.txt':
    index = 1
else:
    print(
        "Error: File name needs either \"_lex-sg.txt\" or \"_lex-en.txt\""
        " appended to the end."
    )
    exit(1)

with input_file.open() as f:
    lines = f.readlines()

output_words = set()
for ln in lines:
    parts = ln.split(':')
    if len(parts) > index:
        keep_part = parts[index].strip()

        # Perform line-based filtering.
        if re.match(r'^[0-9]', keep_part):
            continue
        if re.match(r'^cf', keep_part):
            continue

        output_words.update(str_to_words(keep_part))

write_sorted_set(output_words, output_file)
# with output_file.open('w') as f:
#     f.write('\n'.join(sorted(list(output_words), key=str.lower)))
