#!/usr/bin/env python3

import re
import unicodedata


def generate_sorted_set_output(in_set):
    return '\n'.join(sorted(list(in_set), key=str.lower))

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

def str_to_words(text_string):
    raw_words = text_string.split(' ')
    return raw_words_to_nfd(raw_words)
    # for w in raw_words:
    #     punctuated_word = w.strip()

    #     # Perform punctuation-based filtering.
    #     if re.match(r'\(.*\)', punctuated_word):
    #         continue

    #     # Remove punctuation.
    #     text_word = re.sub(r'[^\w-]', '', punctuated_word)

    #     # Perform text-based filtering.
    #     if len(text_word) == 0: # empty words
    #         continue
    #     if re.match(r'^[0-9]', text_word): # numbers
    #         continue

    #     nfd_word = unicodedata.normalize('NFD', text_word)
    #     nfd_words.add(nfd_word)
    # return nfd_words
