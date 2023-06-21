#!/usr/bin/env python3

""" Convert a basic lexicon file in Sango to a DIC file using the given AFF file.
"""

import sys
from pathlib import Path

from tools import sango_sort


def main():
    if len(sys.argv) < 2:
        print("Error: Need lexicon file.")
        exit(1)
    infile = Path(sys.argv[1])
    if not infile.is_file():
        print(f"Error: File not found: {infile}")
        exit(1)

    with infile.open() as f:
        lex_lines = f.readlines()

    dic_lines = []
    for ll in lex_lines:
        words, ps = ll.split('\t')
        wd1 = words.split(' ')[0]
        line_text = f"{wd1}"

        # Add affix markers to entries.
        affixes = []
        if 'Noun' in ps:
            affixes.append("A")
        if 'Verb' in ps:
            affixes.append("B")
        if len(affixes) > 0:
            string = '/'
            for a in affixes:
                string += a
            line_text += string
        dic_lines.append(line_text)

    dic_lines = sango_sort(list(set(dic_lines)))
    dic_ct = str(len(dic_lines))
    dic_lines.insert(0, dic_ct)
    print("\n".join(dic_lines))

if __name__ == '__main__':
    main()
