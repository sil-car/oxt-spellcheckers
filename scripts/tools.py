#!/usr/bin/env python3

import regex as re
import sys
import unicodedata
import unidecode


class Lexicon():
    def __init__(self, entries=None):
        self.entries = dict()
        # if entries is not None and len(entries) > 0:
        #     self.entries = entries
        self.glosses = self.get_glosses()
        self.size = self.get_size()

    def add_entry(self, entry_tuple):
        if len(entry_tuple) != 2:
            return
        gloss = entry_tuple[0]
        parts_of_speech = set(entry_tuple[1])
        if gloss not in self.entries.keys():
            # Create new entry.
            self.entries[gloss] = Entry()
            self.entries[gloss].gloss_sg = gloss
            self.entries[gloss].parts_of_speech = parts_of_speech
        else:
            # Update entry.
            for p in parts_of_speech:
                self.entries[gloss].parts_of_speech.add(p)

    def get_glosses(self):
        return [k for k in self.entries.keys()]

    def get_size(self):
        return len(self.entries)

    def get_output_text(self):
        # return '\n'.join(sango_sort(list(set(e.as_lexicon_line() for e in self.entries if e.gloss_sg is not None))))
        return '\n'.join(sango_sort(list(set(e.as_lexicon_line() for e in self.entries.values() if e.gloss_sg is not None))))

class Entry():
    """ Basic details: Sango text, parts of speech; e.g.
    LEXICON:
        nï  Pronoun Verb
    """
    def __init__(self, input_lines=None):
        self.gloss_sg = None
        self.parts_of_speech = set()
        if input_lines is not None and len(input_lines) > 0:
            self.input_lines = input_lines

    def as_tuple(self):
        return (self.gloss_sg, self.parts_of_speech)

    def as_lexicon_line(self):
        return f"{self.gloss_sg}\t{' '.join(self.parts_of_speech)}"


def key_from_value(dict, value):
    # This only works with a 1:1 dictionary; i.e. it only returns the first match.
    # return list(dict.keys())[list(dict.values()).index(value)]
    return next((k for k, v in dict.items() if v == value), None)

def generate_sorted_set_output(in_set):
    return '\n'.join(sorted(list(in_set), key=str.lower))

def eprint(*a):
    print(*a, file=sys.stderr)

def print_sorted_set(in_set):
    print(generate_sorted_set_output(in_set))

def write_sorted_set(in_set, out_file):
    with out_file.open('w') as f:
        f.write('\n'.join(sorted(list(in_set), key=str.lower)))

def raw_words_to_nfd(words):
    nfd_words = set()
    for w in words:
        punctuated_word = w.strip()

        # Perform punctuation-based filtering.
        if re.match(r'\(.*\)', punctuated_word):
            continue

        # Remove punctuation.
        text_word = re.sub(r'[^\w-]', '', punctuated_word)

        # Perform text-based filtering.
        if len(text_word) == 0: # empty words
            continue
        if re.match(r'^[0-9]', text_word): # numbers
            continue

        nfd_word = unicodedata.normalize('NFD', text_word)
        nfd_words.add(nfd_word)

    return nfd_words

def sango_sort(in_list):
    def fmt(string):
        return unidecode.unidecode(string.lower())
    return sorted(in_list, key=fmt)

def str_to_words(text_string):
    raw_words = text_string.split(' ')
    return raw_words_to_nfd(raw_words)

