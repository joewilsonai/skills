# Voice, mix, render

## Voices (ElevenLabs; key in `ELEVENLABS_API_KEY`)
| Role | Voice | Model | Settings |
|---|---|---|---|
| Narrator | Smith `TVtDNgumMv4lb9zzFzA2` (library) | eleven_v3 | stability .5, similarity .8, speed 1.1; then atempo 1.12 |
| Reader of the record | Harper `Fihx1nL7DQV0DEuFJSG1` | eleven_multilingual_v2 | stability .7, speed .95 |
Joe rejected Kokoro, every designed voice ("sound fake") and stock premades. Don't re-audition unless he asks.

## Pronunciation dictionary
Per series/case, `pron-dict.json` (`{"id", "version_id"}`) sits in the project root; the tools find it by walking up from the reel dir. Rules live in `pron-rules.json`. For a new case create a new dictionary (POST `/v1/pronunciation-dictionaries/add-from-rules`), add rules with `/add-rules`, store the new version_id. Scan every script with `pronunciation.md` first.

## One-take narration (`scripts/onetake.py <reel dir>`)
`<reel>/one/script.txt`: lines; plain = Smith, `R:` = Harper reads the record, `C: path.wav` = original-sound clip. Smith blocks carry v3 tags I write: `[somber]`, `[quietly]`, `[pause]`. Countdown number is its own sentence: "Number six."
`<reel>/one/config.json`: `tempo` (1.12), `reader_tempo`, `block_gap`, `extra` {"start word of gap": seconds to add}, `segments` [[start words, display caption, who]].
Output: `voice.wav`, `voice.mp3`, `takes.json` (segment start/end + words). Rerun without `--revoice` to re-time from the cached take. Holds are made by looping the gap's own room tone, never digital silence or a new take.
Captions use the script text with digits, never Whisper's spelling. Numbers are normalized for matching (10 ↔ ten).
`scripts/voice.py` = older per-line takes (script.json); use only for a single Harper line or a fix.

## Audio check
Whisper the final file (small.en) and diff against the script; listen to every line that has a dictionary rule. Send the mp3 to the producer as a download unless he's said to run autonomously.

## Mix (`mix.py` per reel, from `templates/reel-mix.py`)
Low D bed, hits on strike / reveal / turn, paper and shutter foley (`core.audio` sampler/sfx in lemo-opuscar), music ducked under voice, clip audio at its cut points. Limiter .42 → master true peak ≤ −1.2 dB, −14 LUFS.

## Render and master (lemo-opuscar, `~/lemo-opuscar`)
```
node core/render/still.mjs <reel> 6 12 20 --size 1080x1920        # stills check first
node core/render/video.mjs <reel> --fps 30 --workers 5 --size 1080x1920
LEMO_COLOR=bt709 sh core/render/mux.sh <video> <mix.wav> <out.mp4> 30 0
ffmpeg -i out.mp4 -c copy -movflags +faststart reel-NN-phone.mp4
```
Page contract: `window.render(t)`, `window.DUR`, `window.READY`, `window.TEXTS(t)`; Canvas 2D, deterministic, no wall clock. `readcheck.mjs` checks text on screen long enough to read; `sheet.py` makes a contact sheet; `srt.py` the captions file.
Send videos as downloads: inline players start muted and Joe twice heard "no sound".

## Compilation
Concat the phone copies in order with a `list.txt` (`ffmpeg -f concat -safe 0 -i list.txt -c copy`), make a 720p preview for phones.
