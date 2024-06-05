#!/usr/bin/env python3

""" Convert multiple files in Sango to a DIC file. Accepts basic lexicon files
    and simple wordlist files.
    Assumes the same affixes as defined in the sg-CF.aff file.
"""

import argparse
import unicodedata
from pathlib import Path

from tools import replace_in_list
from tools import sango_sort
from tools import strip_diacritics


def main():
    parser = argparse.ArgumentParser(
        description='DIC contents are printed to STDOUT'
    )
    parser.add_argument('infiles', metavar='FILEPATH', nargs='+')
    parser.add_argument('-s', '--simple', action='store_true')
    args = parser.parse_args()

    # Set whether or not to create simple (non-1984) spellchecker.
    simple = False
    if args.simple:
        simple = True

    entry_lines = []
    # for infile in sys.argv[1:]:
    for infile in args.infiles:
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
                if simple:  # remove diacritics & make lowercase
                    line_text = strip_diacritics(line_text).lower()
            else:
                parts = ll.split('\t')
                if len(parts) < 2:  # no part of speech given
                    continue
                words = parts[0]
                ps = parts[1]
                wd1 = words.split(' ')[0]
                line_text = unicodedata.normalize('NFD', wd1)
                if simple:  # remove diacritics & make lowercase
                    line_text = strip_diacritics(line_text).lower()

                # Add affix markers to entries.
                affixes = set()
                if 'Adjective' in ps:
                    affixes.add("A")  # plural prefix
                if 'Noun' in ps:
                    affixes.add("A")  # plural prefix
                if not simple and 'Verb' in ps:
                    affixes.add("B")  # noun-subject prefix
                if not simple and wd1 in ['mbï', 'mo', 'âla', 'lo', 'ï']:  # noqa: E501
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
