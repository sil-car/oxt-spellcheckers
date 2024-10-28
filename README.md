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

1. Ensure dependencies are installed.
  ```
  $ python3 -m venv env
  (env)$ python -m pip install -r requirements.txt
  (env)$ which makeoxt
  /home/user/oxt-spellcheckers/env/bin/makeoxt
  ```
1. Prepare basic lexicon file.
   1. Convert original lexicon(s) to plaintext or LIFT files.
   1. Convert file(s) to basic lexicon format; e.g. each line has: `word[tab]Noun Verb Adjective`
   1. Consider adding additional wordlist files and/or including their parts of speech.
1. Prepare AFF file.
   1. Include all affixes and their usage rules.
1. Convert basic lexicon file(s) to DIC file using affixes from AFF file:
   ```
   # from sg-CF_sango-1948 for official orthography:
   ../scripts/make-sango-dic.py *-lexicon.txt *-wordlist.txt > sg-CF.dic
   # from sg-CF_sango-simple for more permissive, common orthography
   ../scripts/make-sango-dic.py -s ../sg-CF_sango-1984/*-lexicon.txt ../sg-CF_sango-1984/*-wordlist.txt *-lexicon.txt *-wordlist.txt > sg-CM.dic
   ```
1. Build OXT file:
   ```
   # from sg-CF_sango-1948 for official orthography:
   ../scripts/aff-dic-to-oxt.sh -d description.xml sg-CF.aff
   # from sg-CF_sango-simple for more permissive, common orthography
   ../scripts/aff-dic-to-oxt.sh -d description.xml sg-CM.aff
   ```
1. Install OXT file: `unopkg add --suppress-license --force ./dict-sango-*`
1. Upload OXT file to [extensions.libreoffice.org](https://extensions.libreoffice.org).
1. Create a Release on GitHub.
1. Use GitHub API to get permalink:
   ```
   # Find correct release and related .assets[0].url
   curl -Ls https://api.github.com/repos/sil-car/oxt-spellcheckers/releases | jq '.[] | .tag_name, .assets.[0].url'
   ```
1. Update `updates/<OXT-FILE>.updates.xml` with correct version and assets URL.
1. Push updated XML file(s) to GitHub.

## References

- https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
- https://www.systutorials.com/docs/linux/man/4-hunspell/
- ```$ man 5 hunspell```
- ```$ man hunspell```
- ```$ hunspell -h```
