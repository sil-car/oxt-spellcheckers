#!/usr/bin/env python3

""" Convert a text file with lines in "ILA format" (sango gloss : french gloss) to TSV format.
"""

import csv
import sys

from pathlib import Path

def main():
    txt_file = Path(sys.argv[1])
    tsv_file = txt_file.with_suffix('.tsv')
    with txt_file.open() as f:
        txt_lines = f.readlines()

    tsv_rows = [[
        'Sango',
        'French',
        'Parts of Speech (e.g. Adj, N, V)',
    ]]
    for line in txt_lines:
        parts = line.split(':')
        if len(parts) < 2:
            continue
        sg_text = parts[0].strip()
        fr_text = parts[1].strip()
        tsv_rows.append([sg_text, fr_text])

    with tsv_file.open('w', newline='') as f:
        writer = csv.writer(f, dialect='excel-tab')
        writer.writerows(tsv_rows)

if __name__ == '__main__':
    main()
