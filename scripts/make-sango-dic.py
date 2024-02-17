#!/usr/bin/env python3

""" Convert multiple files in Sango to a DIC file. Accepts basic lexicon files
    and simple wordlist files.
    Assumes the same affixes as defined in the sg-CF.aff file.
"""

import sys
import unicodedata
from pathlib import Path

from tools import replace_in_list
from tools import sango_sort


def main():
    if len(sys.argv) < 2:
        print("Error: Need at least 1 lexicon or wordlist file.")
        exit(1)
    elif sys.argv[1] in ['-h', '--help']:
        print(
            f"usage: {sys.argv[0]} INFILE [INFILE...]\n\n"
            "DIC contents are printed to stdout"
        )
        exit()

    entry_lines = []
    for infile in sys.argv[1:]:
        infile = Path(infile)
        if not infile.is_file():
            print(f"Skipping non-file argument: {infile}")
            continue
        with infile.open() as f:
            text_lines = f.readlines()
        filetype = 'wordlist'
        if len(text_lines[0].split()) > 1:
            filetype = 'lexicon'
        for ll in text_lines:
            if filetype == 'wordlist':
                wd1 = ll.strip()
                line_text = unicodedata.normalize('NFD', wd1)
            else:
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
            entry_lines.append(line_text)
        del text_lines

    # Deduplicate words, preferring lexicon entries to wordlist entries.
    deduped_lines = []
    for line in entry_lines:
        entrytype = 'wordlist'
        line_parts = line.split('/')
        if len(line_parts) > 1:
            entrytype = 'lexicon'
        word = line_parts[0]
        # if word not in deduped_lines:
        found = False
        for dl in deduped_lines:
            if dl.startswith(word):
                found = True
                break
        if not found:
            deduped_lines.append(line)
        elif entrytype == 'lexicon':
            replace_in_list(deduped_lines, word, line)
    del entry_lines
    dic_lines = sango_sort(list(set(deduped_lines)))
    del deduped_lines
    dic_ct = str(len(dic_lines))
    dic_lines.insert(0, dic_ct)
    print("\n".join(dic_lines))


if __name__ == '__main__':
    main()
