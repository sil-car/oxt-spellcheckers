## Spellcheck extensions for LibreOffice (OXT)

REF:
- https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
- https://www.systutorials.com/docs/linux/man/4-hunspell/
- ```$ man 5 hunspell```
- ```$ man hunspell```
- ```$ hunspell -h```

### Using an OXT extension.

1. Download OXT file to your computer.
1. Install in LibreOffice using Extension Manager.
1. Set document language (e.g. "Sango") to use/test spell checker.

### Creating an OXT extension.

1. Prepare basic lexicon file.
  1. Convert original lexicon(s) to plaintext or LIFT files.
  1. Convert file(s) to basic lexicon format; e.g. each line has: `word[tab]Noun Verb Adjective`
  1. Consider adding additional wordlist files and/or including their parts of speech.
1. Prepare AFF file.
  1. Include all affixes and their usage rules.
1. Convert basic lexicon file(s) to DIC file using affixes from AFF file.
1. Build OXT file; e.g. `scripts/aff-dic-to-oxt.sh sg-CF.aff`
1. Ensure correct info in `description.xml`; e.g. `identfier`

1. Convert original publications to text files.
1. Remove any foreign words from text files (e.g. `scripts/lexicon-to-words.py`).
1. Run `scripts/txt-to-wordlist.sh` to convert to wordlist.
1. Run other conversions on wordlist file (e.g. merge a prefixes).
1. Create DIC and AFF files.
1. Run `aff-dic-to-oxt.sh` to create OXT module.
