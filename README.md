# Spellcheck extensions for LibreOffice (OXT)

## Downloads

Users can download the Sango spellchecker from
[its page on the LibreOffice Extensions site](https://extensions.libreoffice.org/en/extensions/show/34153).

## Using an OXT extension.

1. Download the above OXT file to your computer.
1. Open LibreOffice (can be installed from https://www.libreoffice.org/download/download-libreoffice/).  
![no Sango](data/2023-06-22_002.png)  
1. Install the extension in LibreOffice using "Tools" > "Extension Manager..."  
![](data/2023-06-22_003.png)  
1. Click "Add" button.  
![](data/2023-06-22_004.png)  
1. Select downloaded OXT file.  
![](data/2023-06-22_005.png)  
1. Accept the license.  
![](data/2023-06-22_006.png)  
1. Close the Extension Manager.  
![](data/2023-06-22_007.png)  
1. Restart LibreOffice when prompted.  
![](data/2023-06-22_008.png)  
1. Set document language (e.g. "Sango") to use new spell checker using "Tools" > "Language" > "For the whole text" > "Sango" (or maybe via "More..." if "Sango" doesn't appear there).  
   More instructions can be found on the LibreOffice help site at [Selecting the Document Language](https://help.libreoffice.org/7.5/en-US/text/shared/guide/language_select.html)  
![](data/2023-06-22_009.png)  
![](data/2023-06-22_010.png)  


## Creating an OXT extension.

1. Prepare basic lexicon file.
   1. Convert original lexicon(s) to plaintext or LIFT files.
   1. Convert file(s) to basic lexicon format; e.g. each line has: `word[tab]Noun Verb Adjective`
   1. Consider adding additional wordlist files and/or including their parts of speech.
1. Prepare AFF file.
   1. Include all affixes and their usage rules.
1. Convert basic lexicon file(s) to DIC file using affixes from AFF file; e.g. `scripts/make-sango-dic.py *-lexicon.txt *-wordlist.txt`
1. Build OXT file; e.g. `scripts/aff-dic-to-oxt.sh -d description.xml sg-CF.aff`
1. Upload OXT file to [extensions.libreoffice.org](https://extensions.libreoffice.org).

## References

- https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
- https://www.systutorials.com/docs/linux/man/4-hunspell/
- ```$ man 5 hunspell```
- ```$ man hunspell```
- ```$ hunspell -h```
