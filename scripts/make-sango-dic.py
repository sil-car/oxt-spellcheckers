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

    # Set whether or not to create simple (non-official) spellchecker.
    simple = False
    if args.simple:
        simple = True

    wordlist_files = [Path(f) for f in args.infiles if f.endswith('wordlist.txt')]  # noqa: E501
    lexicon_files = [Path(f) for f in args.infiles if f.endswith('lexicon.txt')]  # noqa: E501

    wordlist_lines = set()
    for infile in wordlist_files:
        if not infile.is_file():
            print(f"Skipping non-file argument: {infile}")
            continue
        with infile.open() as f:
            text_lines = f.readlines()
        for line in text_lines:
            wd1 = line.strip()
            line_text = unicodedata.normalize('NFD', wd1)
            if simple:  # remove diacritics & make lowercase
                line_text = strip_diacritics(line_text).lower()
            wordlist_lines.add(line_text)

    lexicon_lines = set()
    for infile in lexicon_files:
        if not infile.is_file():
            print(f"Skipping non-file argument: {infile}")
            continue
        with infile.open() as f:
            text_lines = f.readlines()
        for line in text_lines:
            parts = line.split('\t')
            if len(parts) < 2:  # no part of speech given
                continue
            words = parts[0]
            ps = parts[1]
            # NOTE: This assumes the first word is the primary word.
            wd1 = words.split(' ')[0]
            line_text = unicodedata.normalize('NFD', f"{wd1}\t{ps}")
            if simple:  # remove diacritics & make lowercase
                line_text = strip_diacritics(line_text).lower()
            if wd1 in [text.split('\t')[0] for text in lexicon_lines]:
                # TODO: Combine parts of speech.
                pass
            lexicon_lines.add(line_text)

    # Prepare initial entry list.
    entry_lines = [line for line in wordlist_lines]
    del wordlist_lines

    for line in lexicon_lines:
        parts = line.split('\t')
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
        if not simple and wd1 in ['mbï', 'mo', 'âla', 'lo', 'ï']:
            affixes.add("M")  # -mvenî suffix
        if len(affixes) > 0:
            string = '/'
            for a in sorted(list(affixes)):
                string += a
            line_text += string
        entry_lines.append(line_text)

    # Deduplicate words, preferring lexicon entries to wordlist entries.
    deduped_lines = []
    for line in entry_lines:
        entrytype = 'wordlist'
        line_parts = line.split('/')
        if len(line_parts) > 1:
            entrytype = 'lexicon'
        word = line_parts[0]
        found = False
        for dl in deduped_lines:
            if dl == word:
                found = True
                break
        if not found:
            deduped_lines.append(line)
        elif entrytype == 'lexicon':
            # NOTE: Only works if lexicon entry comes after wordlist entry.
            replace_in_list(deduped_lines, word, line)
    del entry_lines
    dic_lines = sango_sort(list(set(deduped_lines)))
    del deduped_lines
    dic_ct = str(len(dic_lines))
    dic_lines.insert(0, dic_ct)
    print("\n".join(dic_lines))


if __name__ == '__main__':
    main()
