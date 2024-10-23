#!/usr/bin/env python3

import argparse
import regex as re
import unidecode

from pathlib import Path
from pypdf import PdfReader

from tools import Lexicon
from tools import sango_sort
from tools import raw_words_to_nfd


limits = {
    'L': {
        'x': {
            'min': 305,
            'max': 430,
        },
        'y': {
            'min': 100,
            'max': 742,
        },
    },
    'R': {
        'x': {
            'min': 320,
            'max': 440,
        },
        'y': {
            'min': 40,
            'max': 742,
        },
    },
}

y_jump = 10


class DicoPart():
    def __init__(self, chunks=None):
        self.parts_of_speech_dict = {
            "mbaseli": "Adverb",
            # "mbulango": "Mark of ipseity",
            "ngema": "Interjection",
            # "noun": "Noun",
            "pali": "Verb",
            "pandoo": "Noun",
            # "pahunda": "Adjective",
            "pasunda": "Adjective",
            "polipa": "Pronoun",
            # "pomapande": "Other",
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
        self.lexicon_entries = dict()
        self.chunks = chunks
        self.all_words = set()
        if self.chunks:
            self.parse_dico_chunks()

    def parse_dico_chunks(self):
        self.chunks = sort_chunks(self.chunks)
        parts_of_speech_idxs = []
        for i, c in enumerate(self.chunks):
            words = set()
            if c[2] is not None:
                # Strip random prefix from font name;
                # e.g. /RLVMBC+TimesNewRomanPSMT -> TimesNewRomanPSMT
                base_font = re.sub(r'/.+\+', '', c[2].get('/BaseFont'))
                valid_font_names = [
                    'TimesNewRomanPSMT',
                    'TimesNewRomanPS-BoldMT',
                    'TimesNewRomanPS-BoldItalicMT',
                    'TimesNewRomanPS-ItalicMT',
                ]
                if base_font == 'TimesNewRomanPS-BoldItalicMT':
                    parts_of_speech_idxs.append(i)
                if base_font in valid_font_names:
                    words = clean_words(set(c[0].split()))

            words = raw_words_to_nfd(words)
            for w in words:
                self.all_words.add(w)

        for i in parts_of_speech_idxs:
            b = 1
            part_of_speech = clean_text_chunk(self.chunks[i][0])
            if not part_of_speech:
                continue
            gloss_sg = None
            if i == 0:  # gloss is irretrievable if POS is in initial chunk
                continue
            # Loop backwards from i to find previous gloss text.
            while b <= i:
                c = self.chunks[i-b]
                base_font = None
                if c[2]:
                    base_font = re.sub(r'/.+\+', '', c[2].get('/BaseFont'))
                    if base_font == 'TimesNewRomanPS-BoldMT':
                        text = clean_text_chunk(c[0])
                        if text and not text.startswith('kt'):
                            gloss_sg = text
                            break
                b += 1

            if part_of_speech and gloss_sg:
                # print(f"{c[0] = }; {part_of_speech = }; {gloss_sg = }")
                # Take only 1st word of gloss.
                gloss_sg = clean_text_chunk(gloss_sg.split()[0])
                # "Translate" the part of speech.
                part_of_speech_sg = clean_text_chunk(re.split(r' |\.', part_of_speech)[0])  # noqa: E501
                part_of_speech_sg = unidecode.unidecode(part_of_speech_sg.lower())  # noqa: E501
                part_of_speech = self.parts_of_speech_dict.get(part_of_speech_sg)  # noqa: E501
                # print(f"> {gloss_sg}, {part_of_speech}")
                if part_of_speech and gloss_sg:  # check again after edits
                    len_short_key = min(
                        (len(k) for k in self.parts_of_speech_dict.keys())
                    )
                    if (
                        len(gloss_sg) < 2
                        or len(part_of_speech) < len_short_key
                    ):
                        continue
                    if self.lexicon_entries.get(gloss_sg) is None:
                        self.lexicon_entries[gloss_sg] = []
                    self.lexicon_entries[gloss_sg].append(part_of_speech)

    def parse_dico_entry(self):
        """ gbadara (tî) [t¤ gbàdàrà]
            I pasûndâ 1 sô abâa ngbadara
            ngîâ tî gbadara sô anzere na bê tî
            âzo mîngi 2 ngîâ (tî) [t¤ ng¤á]
            pasûndâ Sô asâra sï zo ahe ngîâ.
            Âzo kûê asumba na mängö tënë tî
            ngîâ sô.
        """
        # Need to identify:
        # - gloss_sg
        # - parts_of_speech
        defs = {}
        for c in self.chunks:
            words = set()
            t = c[0].strip()
            t = re.sub(r'[0-9]', '', t)  # remove numbers
            t = t.strip()
            t = re.sub(r'^I+', '', t)  # remove Roman numerals
            t = t.strip()
            t = re.sub(r'\[*(.+)\]*', r'\1', t)  # remove brackets (PDF typo)
            t = t.strip()
            t = re.sub(r'\W*(.+)\W*', r'\1', t)  # strip bad chars
            t = t.strip()  # strip any remaining whitespace (redundant?)
            # if re.search(r'\W', t): # ignore chunk containing bad chars
            #     continue
            if len(t) < 2:  # filter out empty strings and single chars
                continue
            font = c[2].get('/BaseFont')
            # print(f"{font}, {t}")

            if font == '/FGMFOM+TimesNewRomanPS-BoldMT':
                if defs.get('glosses') is None:
                    defs['glosses'] = []
                defs['glosses'].append(t)
                words = clean_words(set(t.split()))
            elif font == '/FGMFOL+LanguageLanguageSILDoulosBold':
                if defs.get('pronunciations') is None:
                    defs['pronunciations'] = []
                defs['pronunciations'].append(t)
            elif font == '/FGMGAA+TimesNewRomanPS-BoldItalicMT':
                if defs.get('parts-of-speech') is None:
                    defs['parts-of-speech'] = []
                defs['parts-of-speech'].append(unidecode.unidecode(t.lower()))
            elif font == '/FGMFON+TimesNewRomanPSMT':
                if defs.get('definitions') is None:
                    defs['definitions'] = []
                defs['definitions'].append(t)
                words = clean_words(set(t.split()))
            elif font == '/FGMFOI+TimesNewRomanPS-ItalicMT':
                if defs.get('examples') is None:
                    defs['examples'] = []
                defs['examples'].append(t)
                words = clean_words(set(t.split()))
            for w in words:
                self.all_words.add(w)
        # print(defs)
        if defs.get('glosses') is None or defs.get('parts-of-speech') is None:
            return

        if len(defs.get('glosses')) == len(defs.get('parts-of-speech')):
            glosses_sg = [g.split()[0] for g in defs.get('glosses')]
            parts_of_speech = [
                self.parts_of_speech_dict.get(re.split(r' |\.', p)[0])
                for p in defs.get('parts-of-speech')
            ]
            lexicon_entries = zip(glosses_sg, parts_of_speech)
            self.lexicon_entries = []
            for g, p in lexicon_entries:
                if g is None or len(g) < 2 or p is None:
                    continue
                self.lexicon_entries.append((g, p))


def visitor_body(text, cm, tm, font_dict, font_size):
    global chunks
    global limits
    global side
    x = tm[4]
    y = tm[5]
    if (
        x > limits[side]['x']['min'] and x < limits[side]['x']['max']
        and y > limits[side]['y']['min'] and y < limits[side]['y']['max']
    ):
        chunks.append((text, tm, font_dict))


def get_sango_chunks_by_page(page):
    global chunks
    global side
    chunks = []
    # print(page.page_number)
    if page.page_number % 2 == 0:  # even index
        side = 'R'  # 1st page of PDF is an R page
    elif page.page_number % 2 == 1:  # odd index
        side = 'L'
    page.extract_text(visitor_text=visitor_body)
    return chunks


def sort_chunks(chunks):
    """ Order chunks first by y coord. then by x coord. """
    def get_xcoord(chunk):
        return chunk[1][4]

    def get_ycoord(chunk):
        return chunk[1][5]

    # Sort by y-coord.
    x_sorted_chunks = sorted(chunks, key=get_xcoord)
    xy_sorted_chunks = sorted(x_sorted_chunks, key=get_ycoord, reverse=True)
    return xy_sorted_chunks


def split_chunks_into_entries(chunks):
    """ chunk -> (text, tm_coords) """
    global y_jump
    # Check the y-jump distance to find gloss breaks.
    # TODO: Add a test based on brackets.
    chunks_by_entry = []
    entry_chunks = []
    y_last = None
    for c in chunks:
        y = c[1][5]
        if y_last is None:
            y_last = y
            entry_chunks.append(c)
            continue
        if y_last - y > y_jump:  # big gap; start new entry
            # Add last chunk to entries list.
            chunks_by_entry.append(entry_chunks)
            # Reset current chunks list.
            entry_chunks = [c]
        else:  # small gap; add to current entry
            entry_chunks.append(c)
        y_last = y
    return chunks_by_entry


def show_chunks(chunks):
    for c in chunks:
        t = c[0].strip()
        if len(t) < 1:
            continue
        print(round(c[1][4], 1), round(c[1][5], 1), t, c[2].get('/BaseFont'))
    print()


def clean_words(set_of_words):
    set_of_clean_words = set()
    for w in set_of_words:
        w = clean_text_chunk(w)
        if len(w) > 0:
            set_of_clean_words.add(w)
    return set_of_clean_words


def clean_text_chunk(text):
    """ Strip (i.e. from the ends) all non-word characters & remove numbers.
    """
    extras_group = r'[♦,.;:!?)\[\]-]'
    text = re.sub(r'[0-9]', '', text)  # remove numbers
    text = text.strip()
    text = re.sub(r'\W*(.+)\W*', r'\1', text)  # strip non-word chars
    text = text.strip()
    text = re.sub(rf'^{extras_group}+', '', text)  # rm punct. from the begin.
    text = text.strip()
    text = re.sub(rf'{extras_group}+$', '', text)  # rm punct. from the end
    text = text.strip()
    text = re.sub(r'^I+(?!=[a-z])', '', text)  # remove Roman numerals
    text = text.strip()
    return text


def get_pronunciation_guides(chunks_by_page):
    ct = 0
    prons = set()
    for chunks in chunks_by_page:
        for c in chunks:
            pfont = '/FGMFOL+LanguageLanguageSILDoulosBold'
            if c[2] is not None and c[2].get('/BaseFont') == pfont:
                ct += 1
                prons.add(c[0])
    return ct, prons


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--bounds', '-b', nargs=8, type=float,
        help="set non-default page boundaries (requires all 8 numbers)",
    )
    parser.add_argument(
        '--check', '-c', action='store_true',
        help="check text extraction output",
    )
    parser.add_argument(
        '--num-prons', '-n', action='store_true',
        help="count the number of pronunciaton guides in the text",
    )
    parser.add_argument(
        '--page-range', '-p', nargs=2, type=int,
        help="choose a range of pages (1 or 2 args)",
    )
    parser.add_argument(
        '--wordlist', '-w', action='store_true',
        help="output Sango words, 1 word per line",
    )
    parser.add_argument(
        '--y-jump', '-y', nargs=1, type=float,
        help="set a non-default value for the distance between page entries",
    )
    parser.add_argument(
        'file', nargs=1, type=Path,
        help="PDF file to be parsed",
    )
    return parser.parse_args()


def main():
    args = get_args()
    pdf_file = args.file[0].expanduser().resolve()
    if not pdf_file.is_file():
        print("Error: Not a valid file: {pdf_file}")
        exit(1)

    if args.bounds:
        global limits
        limits['L']['x']['min'] = args.bounds[0]
        limits['L']['x']['max'] = args.bounds[1]
        limits['L']['y']['min'] = args.bounds[2]
        limits['L']['y']['max'] = args.bounds[3]
        limits['R']['x']['min'] = args.bounds[4]
        limits['R']['x']['max'] = args.bounds[5]
        limits['R']['y']['min'] = args.bounds[6]
        limits['R']['y']['max'] = args.bounds[7]

    if args.y_jump:
        global y_jump
        y_jump = args.y_jump[0]

    global pdf_obj
    pdf_obj = PdfReader(pdf_file)

    # Set extraction range.
    pgi_i = 0
    pgi_f = len(pdf_obj.pages) - 1
    if args.page_range and len(args.page_range) > 1:
        pgi_i = args.page_range[0] - 1
        pgi_f = args.page_range[1] - 1
    pg_range = [pgi_i, pgi_f]

    # Extract info from PDF.
    # print(pdf_obj.pages[20].extract_text())
    # finds all text, but hard to filter for Sango
    sango_chunks_by_page = (
        get_sango_chunks_by_page(p)
        for p in pdf_obj.pages[pg_range[0]:pg_range[1]+1]
    )

    if args.num_prons:
        ct, prons = get_pronunciation_guides(sango_chunks_by_page)
        for p in prons:
            print(p)
        print(f"unique terms: {len(prons)}")
        print(f"total terms:  {ct}")
        exit()

    lexicon = Lexicon()
    wordlist = set()
    for chunks in sango_chunks_by_page:
        chunks = sort_chunks(chunks)
        if args.check:
            show_chunks(chunks)
            continue

        dico_part = DicoPart(chunks)
        for w in dico_part.all_words:
            wordlist.add(w.lower())
        for glo, pos in dico_part.lexicon_entries.items():
            lexicon.add_entry((glo.lower(), pos))

    if args.check:
        exit()

    if args.wordlist:
        for w in sango_sort(list(wordlist)):
            print(w)
    else:  # print lexicon entries
        print(lexicon.get_output_text())


if __name__ == '__main__':
    main()
