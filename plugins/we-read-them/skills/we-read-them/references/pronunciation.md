# Pronunciation: what needs a rule before it's voiced

ElevenLabs dictionary **"What the record says"** (`pron-dict.json` holds the id and current version; `pron-rules.json` the rules). Every voice script attaches it. Screen text never changes; only the spoken form does.

**Workflow:** before voicing a script, scan it for anything in the list below. Add a rule (alias) for each hit, bump the dictionary version, then voice it. Rules are case-sensitive: add each capitalization that appears.

## What to look for

| Type | Examples | What breaks | Rule |
|---|---|---|---|
| Initialisms read letter by letter | USPS, MMIP, DV, EC, ME, PD, ATF | letters stretch or blur ("U ESSSS PS") | alias with periods: `USPS` → `U.S.P.S.` (Joe picked this form 11/3) |
| Common ones it already knows | FBI, CNN, TV, NYPD | usually fine | test once; no rule unless it stumbles |
| Acronyms spoken as words | NASA, GRAMA (Utah's records law) | may get spelled out instead | alias to the word: `GRAMA` → `gramma` |
| Abbreviations that should expand | Misc, Dept., St., Ave., No., pp., approx. | read as a fake word ("misk") | alias to the full word: `Misc` → `miscellaneous` |
| State and month abbreviations | Fla., Wyo., Calif., Sept., Aug. | read literally | write the full word in the voice script, or alias |
| Names with non-obvious sounds | Laundrie (LAWN-dree), Bethune, Myakkahatchee, Petito, Ratcliffe | Americanized or anglicized wrong | alias to a phonetic spelling; confirm by ear with Joe |
| Form and case numbers | FD-597, FD-302, 70A-DN-3494764 | read as one long number or skipped | alias to how a person says it: `F D five ninety-seven` |
| Statutes and bills | 18 U.S.C. § 1029(a)(2), S.B. 117 | symbols and dotted letters garble | alias, or reword the script ("federal fraud law") |
| Symbols | §, ≈, %, #, &, / | skipped or read oddly | spell out in the script ("section", "about", "percent") |
| Money, times, dates | $14.10, 3:00:17 AM, 9/20/2021 | inconsistent reading | write it as spoken in the voice script ("fourteen dollars and ten cents"); captions keep the digits |
| Ordinals and countdown numbers | 10th, "Number six" | runs into the next word | own sentence plus a held pause ("Number six.") |
| Brand and channel names | Red, White & Bethune, TikTok | "&" or casing trips it | write "and" in the voice script |

## Check after voicing
Run the speech check on every take (`asr_check.py --model small.en`), and for any line with a rule, listen once. The speech model can't hear a stretched letter, so the ear is the real test.
