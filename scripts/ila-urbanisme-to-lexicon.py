#!/usr/bin/env python3

""" Convert ILA's "Lexique de l'urbanisme" document (exported as text) to a
basic lexicon format:
    i.e. [word]\t[[parts of speech] [...]]
"""

# import regex as re
# import re
import sys
import unicodedata
# import unidecode

from pathlib import Path

from tools import Entry
from tools import eprint
# from tools import key_from_value
from tools import Lexicon
# from tools import sango_sort

"""
Pd. = pandôo (noun)
Pl. = palî (verb)
Ppd. = tatë pandôo (compund noun; treat like noun)
Ps. = pasûndâ (adjective)
Ppl. = penze palî (compound verb; treat like verb)
"""


class IlaEntry(Entry):
    def __init__(self, ila_lines=None):
        super().__init__(input_lines=ila_lines)
        self.parts_of_speech_dict = {
            "pd.": "Noun",
            "pl.": "Verb",
            "ppd.": "Noun",
            "ppl.": "Verb",
            "ps.": "Adjective",
        }
        if ila_lines is not None and len(ila_lines) > 0:
            self.parse_ila_text()

    def parse_ila_text(self):
        """ Basic details: Sango text, parts of speech; e.g.
        ILA:
            Dakpälë tî Lëkërëngö-da na tî
                Lëkërëngö-yâ tî Ködörö Ppd.
                Ministère de l'Habitat et de
                l'Urbanisme
        LEXICON:
            dakpälë  Noun
        """
        for ln in self.input_lines:
            for w in ln.split():
                # Convert to lowercase; take only 1st part if hyphenated.
                w = w.split('-')[0].lower()
                # Use only 1st word as gloss_sg.
                if self.gloss_sg is None:
                    self.gloss_sg = w
                if w in self.parts_of_speech_dict.keys():
                    self.parts_of_speech.add(self.parts_of_speech_dict.get(w))


def main():
    if len(sys.argv) < 2:
        eprint("Error: No input file given.")
        exit(1)
    lexicon_file = Path(sys.argv[1])
    with lexicon_file.open(encoding="utf-8-sig") as f:
        ila_lines = f.readlines()

    lexicon = Lexicon()
    entry_lines = None
    for ln in ila_lines:
        nfd_l = unicodedata.normalize('NFD', ln).rstrip()
        if len(nfd_l) < 2:
            # Skip empty and single-letter lines.
            continue
        elif nfd_l[0] != '\t':
            if entry_lines is not None:
                # Add previous entry.
                entry = IlaEntry(entry_lines)
                glosses = [e.gloss_sg for e in lexicon.entries]
                if entry.gloss_sg not in glosses:
                    lexicon.entries.add(entry)
            entry_lines = [nfd_l]
        else:  # continuation line
            entry_lines.append(nfd_l.lstrip())
    entry = IlaEntry(entry_lines)
    glosses = [e.gloss_sg for e in lexicon.entries]
    if entry.gloss_sg not in glosses:
        lexicon.entries.add(entry)
    
    print(lexicon.get_output_text())


if __name__ == '__main__':
    main()
