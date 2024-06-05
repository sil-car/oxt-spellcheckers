#!/usr/bin/env python3
"""Convert lines of text from the Weston Lexicon into a basic lexicon with
word + parts of speech.
"""

import sys

from tools import Entry
from tools import eprint
from tools import Lexicon


class WestonEntry(Entry):
    """Basic structure:
    WESTON:
        1   {a} a VP  WHO [subject pronoun]

    LEXICON:
        a   Verb
    """

    def __init__(self, weston_lines=None):
        super().__init__(input_lines=weston_lines)
        self.parts_of_speech_dict = {
            'ADJ': 'Adjective',
            'ADV': 'Adverb',
            'ART': None,
            'CONJ': 'Conjuction',
            'CP': None,
            'CS': None,
            'G': None,
            'INTERJ': 'Interjection',
            'N': 'Noun',
            'NV': None,
            'PHRASE': None,
            'PN': None,
            'PREFIX': 'Prefix',
            'PREP': 'Preposition',
            'PRON': 'Pronoun',
            'SUFFIX': 'Suffix',
            'V': 'Verb',
            'VI': 'Verb',
            'VP': 'Verb',
            'VT': 'Verb',
        }
        if weston_lines is not None and len(weston_lines) > 0:
            self.parse_weston_text()

    def parse_weston_text(self):
        for ln in self.input_lines:
            parts = ln.split('\t')
            wd = None
            ps = None
            if len(parts) >= 4:
                wd = parts[2]
                ps = parts[3]

            if ps:
                k = self.parts_of_speech_dict.get(ps)
                if k:
                    self.parts_of_speech.add(k)
                else:
                    eprint(f"No corresponding Part of Speech for \"{ps}\"")

            if wd:
                self.gloss_sg = wd
            else:
                self.gloss = ''


def main():
    infile = sys.argv[1]
    with open(infile) as f:
        weston_lines = f.readlines()

    lexicon = Lexicon()
    for ln in weston_lines:
        try:  # skip lines not starting with digit
            int(ln[0])
        except ValueError:
            continue

        lexicon.add_entry(WestonEntry([ln]).as_tuple())

    print(lexicon.get_output_text())


if __name__ == '__main__':
    main()
