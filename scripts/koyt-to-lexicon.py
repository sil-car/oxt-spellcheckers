#!/usr/bin/env python3

""" Convert Mme KOYT's lexicon document (exported as text) to a basic lexicon format:
        i.e. [word] [[parts of speech] [...]]
"""

import regex as re
# import re
import sys
import unicodedata
import unidecode

from pathlib import Path

from tools import Entry
from tools import key_from_value
from tools import Lexicon
from tools import sango_sort


class KoytEntry(Entry):
    """ Basic details: Sango text, parts of speech; e.g.
    KOYT:
        nï  1 (Polïpa) : he, him, she (indirect discourse) (Pronoun)
            2 (Palî) :  1 to defecate, to urinate (Verb)
                        2 to rain abundantly (Verb)
    LEXICON:
        nï  Pronoun Verb
    """

    def __init__(self, koyt_lines=None):
        super().__init__(input_lines=koyt_lines)
        self.parts_of_speech_dict = {
            "mbaseli": "Adverb",
            "mbulango": "Mark of ipseity",
            "ngema": "Interjection",
            "noun": "Noun",
            "pali": "Verb",
            "pandoo": "Noun",
            "pahunda": "Adjective",
            "pasunda": "Adjective",
            "polipa": "Pronoun",
            "pomapande": "Other",
            "sete": "Connective",
            "tahuzu": "Preposition",
            "X01": "Coordinating connective",
            "X02": "Demonstrative",
            "X03": "Existential marker",
            "X04": "Formule d'acceptation",
            "X05": "Formule de desapprobation",
            "X06": "Ideophone",
            "X07": "Interrogative pro-form",
            "X08": "Locative",
            "X09": "Marqueur d'hypothese",
            "X10": "Particle",
            "X11": "Quantifier",
            "X12": "Subordinating connective",
            "X13": "Tense_aspect_modality",
        }
        if koyt_lines is not None and len(koyt_lines) > 0:
            self.parse_koyt_text()

    def parse_koyt_text(self):
        """ nï  1 (Polïpa) : he, him, she (indirect discourse) (Pronoun)
                2 (Palî) :  1 to defecate, to urinate (Verb)
                          2 to rain abundantly (Verb)
        """
        def parse_part_of_speech(self, string):
            m = re.search(r'\(\w+\)', string) # re's \w doesn't work with NFD chars, but regex's does
            # Remove parentheses.
            if m:
                m = m.group(0)[1:-1]
                ps = m.split(',')
                # print(ps)
                for p in ps:
                     # "lower" & "unidecode" avoid inconsistencies in original text.
                    k = self.parts_of_speech_dict.get(unidecode.unidecode(p.strip().lower()))
                    if k:
                        self.parts_of_speech.add(k)
                    else:
                        print(f"No corresponding Part of Speech for \"{p}\"")

        for l in self.input_lines:
            if not ':' in l:
                continue
            sango_text = l.split(':')[0]
            parse_part_of_speech(self, sango_text)
            if re.search(r'^[a-z]', sango_text.lower()):
                # Line starts with Sango gloss.
                m = re.search(r'^([^\(0-9]+)', sango_text)
                self.gloss_sg = m.group(0).strip() if m else ''


def main():
    koyt_lexicon_file = Path(sys.argv[1])
    with koyt_lexicon_file.open(encoding="utf-8-sig") as f:
        koyt_lines = f.readlines()

    lexicon = Lexicon()
    entry_lines = None
    for l in koyt_lines:
        nfd_l = unicodedata.normalize('NFD', l).strip()
        if len(nfd_l) < 1:
            # Skip empty lines.
            continue
        elif re.match(r'^[a-z]', nfd_l.lower()):
            if entry_lines is not None:
                # Add previous entry.
                lexicon.entries.add(KoytEntry(entry_lines))
            entry_lines = [nfd_l]
        else:
            entry_lines.append(nfd_l)
    # Add final entry.
    lexicon.entries.add(KoytEntry(entry_lines))
    
    outdir = koyt_lexicon_file.parents[2]
    outfile = outdir / "KOYT lexicon.txt"
    outfile.write_text(lexicon.get_output_text())


if __name__ == '__main__':
    main()
