#!/usr/bin/env python3

""" Convert multiple basic lexicon files in Sango to a DIC file.
    Assumes the same affixes as defined in the sg-CF.aff file.
"""

import sys
import unicodedata
from pathlib import Path

from tools import sango_sort


def main():
    if len(sys.argv) < 2:
        print("Error: Need at least 1 lexicon file.")
        exit(1)
    elif sys.argv[1] in ['-h', '--help']:
        print(
            f"usage: {sys.argv[0]} lexicon.txt [lexicon.txt...]\n\n"
            "DIC contents are printed to stdout"
        )
        exit()

    dic_lines = []
    for infile in sys.argv[1:]:
        infile = Path(infile)
        if not infile.is_file():
            print(f"Error: File not found: {infile}")
            exit(1)
        with infile.open() as f:
            lex_lines = f.readlines()
        for ll in lex_lines:
            words, ps = ll.split('\t')
            wd1 = words.split(' ')[0]
            line_text = unicodedata.normalize('NFD', wd1)

            # Add affix markers to entries.
            affixes = set()
            if 'Adjective' in ps:
                affixes.add("A")  # plural prefix
            if 'Noun' in ps:
                affixes.add("A")  # plural prefix
            if 'Verb' in ps:
                affixes.add("B")  # noun-subject prefix
            if wd1 in ['mbï', 'mo', 'âla', 'lo', 'ï']:
                affixes.add("M")  # -mvenî suffix
            if len(affixes) > 0:
                string = '/'
                for a in sorted(list(affixes)):
                    string += a
                line_text += string
            dic_lines.append(line_text)

    dic_lines = sango_sort(list(set(dic_lines)))
    dic_ct = str(len(dic_lines))
    dic_lines.insert(0, dic_ct)
    print("\n".join(dic_lines))


if __name__ == '__main__':
    main()
