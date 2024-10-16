- Prioritize ILA lexicons.
  1. Lexique de l'urbanisme
  1. Lexique des Finances
  1. Lexique de sante
  1. Lexique de l'elevage
  1. Lexique de l'exploitation forestiere
  1. Lexique des terms juridiques et administratifs
  1. Lexique de linguistique
  1. Lexique de suite bureautique
- For each lexicon:
  - Split each lexicon into single-column pages.
  - OCR the text & clean it up.
  - Convert the text to TSV files for marking parts of speech.
  - Share files with Kim.
  - Convert TSV files w/ parts of speech to lexicon text files.
  - Add lexicon text files to DIC file; rebuild spellchecker.

| Lexicon      | prep 1-col. pg. | run OCR | cleanup OCR | convert to TSV | share file | add parts | create lexicon TXT |
| ---          | :-:             | --:     | --:         | :-:            | :-:        | --:       | :-:                |
| urbanisme    | +               | +       | +           | +              | +          | +         | +                  |
| finances     | +               | 10      | 30          | +              | +          |           |                    |
| santé        | +               | 10      | 120         | +              |            |           |                    |
| élévage      | +               | 25      | 60          | +              |            |           |                    |
| forestière   | +               | 5       | 10          | +              |            |           |                    |
| juridiques   | +               |         |             |                |            |           |                    |
| linguistique | +               |         |             |                |            |           |                    |
| bureautique  |                 |         |             |                |            |           |                    |

### Missing words
| Sango | French | Document | Comment | Resolution |
|:--|:--|:--|:--|:--|
| äpe | non (neg.) | Tract: Ala gi Yanga ti Nzapa | DicoPlus entry for “non” is only “en-en”. KOYT spells the neg. as äpe. ||
| bâda | parlementaire (sanctuaire) | Tract: Ala gi Yanga ti Nzapa | DP and KOYT spell this ‘bâda’ (though DP does not have a direct entry). Corrector suggests capital B, as in ‘Bâda’. ||
| fûu | fou | Tract: Ala gi Yanga ti Nzapa | DicoPlus entry “interner” translates as the phrase ‘zîa na da tî fûu’. But the word ‘fûu’ does not appear in the spellchecker. ||
| gi | chercher | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus was skipped somehow. ||
| ï | nous | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus is the other one (ë). Maybe we should add this anyway. ||
| Jesus | Jésus | Tract: Ala gi Yanga ti Nzapa | Spellchecker marks ‘Jesus’ as incorrect; it proposes ‘Jésus’. (Jesus/Jésus does not appear in DicoPlus.) Since it appears at all, better to appear without an accent. ||
| kandâa | cependant (however) | Tract: Ala gi Yanga ti Nzapa | No occurrence of this word in DicoPlus. Entry of ‘cependant’ in DicoPlus is kamême or kamëme. KOYT says ‘kandâa’ is ‘however/while’. ||
| kânga | fermer | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus was skipped somehow. ||
| kua | travail | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus was skipped somehow. ||
| mbëtï | papier | Tract: Ala gi Yanga ti Nzapa | DP and KOYT have this spelling but the spellchecker proposes other tones. ||
| me | mais (but) | Tract: Ala gi Yanga ti Nzapa | No entry in DicoPlus, but is spelled without an accent in KOYT. ||
| ndokua | entreprise | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus was skipped somehow. AND suggested word “ndökua” does not seem to exist in DicoPlus. ||
| (fün) sen | répugner | Tract: Ala gi Yanga ti Nzapa | Entry in DicoPlus was skipped somehow. ||
| sïönî | vil | Tract: Ala gi Yanga ti Nzapa | Corrector proposes ‘sïönï’ and ‘sîönî’, neither of which occur in KOYT and not in the entry ‘vil/vile’ in DP. ||
| süä, sûâ | aiguille | Tract: Ala gi Yanga ti Nzapa | Both spellings of ‘needle’ appear in DicoPlus (although the entry for ‘aiguille’ is sûâ). KOYT and the tract both use süä. Add both to spellchecker? ||
| zo | personne | Tract: Ala gi Yanga ti Nzapa | No entry in DicoPlus, but is spelled without an accent in KOYT. ||

