# Pronunciation before recording and in the final export

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
| Names with non-obvious sounds | Laundrie (LAWN-dree), Bethune, Myakkahatchee, Petito, Ratcliffe | Americanized or anglicized wrong | match a first-party spoken example and test a phonetic alias |
| Words whose sound depends on context | *read* in “we read the filings” | Present and past tense share the same spelling | Make the intended tense audible before recording, for example “we checked the filings.” |
| Word endings next to similar consonants | *tipped deliveries* | The ending can disappear into the next word | For narration, use an equivalent phrase such as “deliveries with tips.” Preserve actual quotations and adjust the read or spacing. |
| Form and case numbers | FD-597, FD-302, 70A-DN-3494764 | read as one long number or skipped | alias to how a person says it: `F D five ninety-seven` |
| Statutes and bills | 18 U.S.C. § 1029(a)(2), S.B. 117 | symbols and dotted letters garble | alias, or reword the script ("federal fraud law") |
| Symbols | §, ≈, %, #, &, / | skipped or read oddly | spell out in the script ("section", "about", "percent") |
| Money, times, dates | $14.10, 3:00:17 AM, 9/20/2021 | inconsistent reading | write it as spoken in the voice script ("fourteen dollars and ten cents"); captions keep the digits |
| Ordinals and countdown numbers | 10th, "Number six" | runs into the next word | own sentence plus a held pause ("Number six.") |
| Brand and channel names | Red, White & Bethune, TikTok | "&" or casing trips it | write "and" in the voice script |

## Review every word in the export

1. Lock the spoken-form script before synthesizing. Write out dates, decimals, money, percentages, ordinals and initialisms as the speaker should say them. Keep matching display captions with the customary digits and spelling. When a number ends one sentence and another begins the next, set enough space for the listener to hear two statements. Test the join without showing the text. For an unfamiliar name or technical term, check how the person, company or relevant authority says it. Save that recording and note any accepted regional variant. If the stress is disputed, compare the same name in the source and the export, then give a listener an isolated clip without the spelling.
2. Decode the **complete audio track of the final exported file**. Listen from the first frame through the final word and tail. A sound-capable reviewer can use contiguous, timestamped sections that cover the whole track. Compare **every spoken word** with the locked spoken-form script, including ordinary words, each countdown number and each quoted word. Check syllables, stress, missing consonants, stretched letters, decimal points, units, speaker changes and sentence endings. Record the role, time range, words as heard, and the disposition of each discrepancy.
3. Generate an independent transcript and align it to the approved words. Use timestamps to return to discrepancies in the actual encoded audio. A recognizer can spell a homophone differently, guess a familiar brand or normalize a number. Listen again around the word with enough neighboring speech to identify it. Classify the result as a clear error, an accepted pronunciation, an ASR ambiguity, or unresolved. Where doubt remains, replay the surrounding phrase without giving the listener the expected answer. Verify any proposed change against the locked script and the exhibited source. An evaluator can accurately hear a year and still flag the wrong year as the target. If direct sound review is unavailable, state which seconds received ASR-only review and keep the listening check open.
4. After changing a take, script, cut, tempo, music mix or join, listen to the affected words in their final context and verify adjoining speech on both sides. Check the first and last sentences of each exported short. In the stitched long-form, check every chapter transition and the final word. Retain the corrected script, export identity and timecoded pronunciation findings together so the next cut can be checked against the same target.

When word alignment stops one word short, play the end of the original take and ask a listener to write down the final two words without showing the script. If both are audible, measure the last word against the waveform and save its onset and end beside the take’s filename. Map those times through trimming and tempo changes, then replay the word with its caption in the encoded cut. If the word is missing from the audio, repair the take before building captions.

## Transliterated names and translated readings

For transliterated historical names, look for a recording by a teacher or scholar familiar with the language and note the pronunciation used in this episode. Save spoken aliases separately from the correctly accented display spelling. Replay the name inside its sentence, especially when a recognizer splits it into familiar English words. If a listener’s phonetic spelling is ambiguous, ask which familiar word rhymes with the syllable and compare the audible vowel with the reference. For a translated text, distinguish the series reader’s voice from the historical author on screen.

## Sports names and archival quotations

For a sports name, look up the team’s broadcast pronunciation guide and compare it with a player introduction or interview. For an original-sound quotation, transcribe the exact excerpt you cut. If the speaker starts over, caption the words present in the selected audio.

If the listener hears a different vowel after a dictionary change, use a familiar rhyming word in the voice prompt and replay the result blind beside the original broadcast. Keep the correct spelling in the caption. Check official tournament names for small changes in wording. If the short name is better known, verify its letters in the recording.
