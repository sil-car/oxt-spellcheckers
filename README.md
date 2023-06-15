## Spellcheck extensions for LibreOffice (OXT)

REF:
- https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
- https://www.systutorials.com/docs/linux/man/4-hunspell/
- ```$ man 5 hunspell```
- ```$ man hunspell```
- ```$ hunspell -h```

### Steps

1. Convert original publications to text files.
1. Remove any foreign words from text files.
1. Run `scripts/txt-to-wordlist.sh` to convert to wordlist.
1. Run other conversions on wordlist file (e.g. merge a prefixes).
1. Create DIC and AFF files.
1. Run `aff-dic-to-oxt.sh` to create OXT module.
