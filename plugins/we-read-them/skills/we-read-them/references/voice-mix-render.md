# Voice, mix, render

## Voices (ElevenLabs; key in `ELEVENLABS_API_KEY`)
| Role | Voice | Model | Settings |
|---|---|---|---|
| Narrator | Smith `TVtDNgumMv4lb9zzFzA2` (library) | eleven_v3 | stability .5, similarity .8, speed 1.1; then atempo 1.12 |
| Reader of a written record | Same Smith voice as narrator | eleven_v3 | Same generation settings, then apply the reel’s `reader_tempo` (default 1.0) |
Use one male narrator for the film, its Shorts and any pickups. Identify each written quotation by speaker or document on screen. Credit a genuine source recording to its original speaker. When a different provider supplies the narration, lock both spoken roles to the same male voice and check its identifier in the receipts for the intro, all ranks and the finale.

Joe also approved Azure AI Speech as an optional narration provider. When selecting it for an episode, record the male voice’s exact provider identifier, locale and speaking rate. Audition the opening and the hardest proper name before recording the countdown. If a provider fails after a voice has been chosen, first recover completed takes and check whether that same voice is available for the remaining lines. Listen across adjacent chapters for changes in pace or timbre.

Joe rejected Kokoro, every designed voice ("sound fake") and stock premades. Don't re-audition unless he asks.

## Pronunciation dictionary
Per series/case, `pron-dict.json` (`{"id", "version_id"}`) sits in the project root; the tools find it by walking up from the reel dir. Rules live in `pron-rules.json`. For a new case create a new dictionary (POST `/v1/pronunciation-dictionaries/add-from-rules`), add rules with `/add-rules`, store the new version_id. Scan every script with `pronunciation.md` first.

## One-take narration (`scripts/onetake.py <reel dir>`)
`<reel>/one/script.txt`: lines; plain = Smith narrates, `R:` = Smith reads a credited written passage, `C: path.wav` = a clip of the original sound. Smith blocks carry v3 tags I write: `[somber]`, `[quietly]`, `[pause]`. Countdown number is its own sentence: "Number six."
`<reel>/one/config.json`: `tempo` (1.12), `reader_tempo`, `block_gap`, `extra` {"start word of gap": seconds to add}, `segments` [[start words, display caption, who]].
The reel path may be absolute or relative, including `.` when run inside the reel. Each uninterrupted run of lines in the same role gets one cached `one/takeN.mp3`. An original-sound `C:` line occupies a block number of its own.

- For a single correction, update the script and caption text, then run `onetake.py <reel> --revoice-block N`. **N is the zero-based block in the script**, the number in `takeN.mp3`. Repeat the option for multiple corrections. All unselected voice blocks must already have a cached take. When updating an older episode, also select any written readings whose audio has no matching receipt for the current narrator. A changed role or added clip can shift subsequent block numbers.
- A plain run reuses available narration, generates missing takes and replaces written readings whose installed audio has no matching receipt for the current narrator. `--revoice` replaces all synthesized blocks. Original-sound clips are read from their own files with either flag. After a partially completed full revoice, check the receipts and select only the outstanding blocks.
- Each generation gets a private `one/voice-receipts/takeN-*/receipt.json` with the UTC time, hashes, voice, model, and available provider request ID, history ID and credit count. A replacement saves the previously cached MP3 beside its receipt before dispatch. Historical receipts stay with the reel. A missing credit header means the charge still needs checking against provider history.
- The current take changes only after the full response decodes. If an interruption leaves a validated response awaiting installation, repeat the same selected block and the saved response will be used. When request delivery is uncertain, compare provider history with the UTC time, voice and text hash before sending another request. Record the actual outcome in that receipt. Recover a completed take by its history ID, or record a verified missing request as `reconciled_missing` before retrying.

The local build stages `voice.wav`, `voice.mp3`, and `takes.json` together and publishes them after caption matching succeeds. Holds use room sound between recognized words and outside original clips. An onset adjustment must stay within the first word.

When using ElevenLabs’ optional `with-timestamps` endpoint in a separate production workflow, save the original character alignment with each block. To place a timestamp in the final mix, subtract the block's trimmed input start, divide by the applied tempo, then add its actual output start, including earlier clip durations, inter-block gaps and any inserted holds before the timestamp. Recalculate times after cutting out words. Check each changed phrase against decoded final audio.
Captions use the script text with digits, never Whisper's spelling. Numbers are normalized for matching (10 ↔ ten).
The older `scripts/voice.py` works from `script.json` for individual pickups. Both roles use Smith on `eleven_multilingual_v2`. The cache for written readings includes the voice ID. A complete response awaiting a successful trim stays beside the cache as a request-specific `.received` file. Retry the same line and settings to finish that trim locally.

## Matching original speech to its picture

For a one- or two-word reply, start and end the excerpt in room tone so the preceding speaker’s final syllable stays out of the cut. Ask a fresh listener to transcribe the exact exported reply without a script. Then listen to the longer source exchange to verify who answered and which question it answered. Preserve both time ranges for the editor and replay the reply where it joins the narrator in the finished film.

Keep a broadcaster’s visible lower third when it identifies someone on camera. Its original closed captions may also travel invisibly as ATSC A/53 frame side data. If the new edit supplies burned captions and its own subtitle track, suppress that legacy stream when encoding. On Mac, `-a53cc 0` is an output option for `h264_videotoolbox`. If VideoToolbox still rejects the frames, encode those inputs with software H.264 and the same caption policy. Decode the export across the station clip and verify the visible lower third, the new captions, the audio and the intended subtitle stream. Keep the source file available for checking the station’s own captions.

Keep archival speech at its recorded speed whenever the picture uses the source timing. Bypass FFmpeg’s `atempo` filter when the requested rate is 1.0. Its overlap processing can shift parts of the waveform by several milliseconds even at that setting. For a clip already produced through `atempo=1.0`, first verify the unprocessed excerpt against the source. Then run a second reference through the actual trim, filter and resampling settings and compare it to the delivered waveform. Measure picture sync against that processed audio onset and the corresponding original frames.

Keep the source video, its in and out points, the extracted audio, the speaker’s name, and the exact words of the excerpt together. When a quoted speaker is visible, start the picture on the frame that matches the first audio sample in the mix. A trimmed clip can contain room tone before the first spoken word. If your timing file gives a word onset, subtract that lead-in to recover the clip start. Time the caption to the word and the mouth to the audio. Check the first consonant in the vertical export and in the widescreen chapter.

If a game clip or source photo arrives after a render has started, compare the exported shot with the final shot list at its assigned cue. Rebuild each affected layout and the stitched film. Generate credits from assets actually used in the cut, including the original audio sources. A render that started before a pickup can finish after it. Record the hash of the mix and timed script when the render starts. If another version lands while it runs, decode the exported AAC and compare the revised passage with the new mix before stitching. A newer MP4 timestamp alone cannot establish which take it contains.

At each chapter boundary, listen beyond the last scripted word through the first word of the next chapter. A transcript can be perfect while a stray burst or partial sound interrupts the pause. If one boundary contains a burst, check every take made with the same recording chain. Preserve the original. Fade in the verified quiet interval after the complete word, retain the sample count, and listen to the repaired join in both exports.

## Audio check
Listen through every word of narration and record quotations in the exported MP4. Independently transcribe the audio and investigate differences against the source and the approved spoken form. Save timecodes for questions and their resolutions. After a change, rebuild affected captions and both formats, review the corrected passage with the words on each side, and check the long-form chapter joins. The [word-by-word review](pronunciation.md#review-every-word-in-the-export) describes how to handle homophones, unfamiliar names and spoken numbers. Send the MP3 to the producer as a download when a listen is part of the agreed workflow.

## Mix (`mix.py` per reel, from `templates/reel-mix.py`)

Decide what the listener should hear at the turn. A drum can give a football play momentum. In a kitchen interview, the change from close narration to a homeowner’s voice can carry the turn on its own. Let the first consonant or breath arrive cleanly. If music has a reason to enter, bring it in on the action or after the first phrase. Keep one score idea across adjacent shots that belong to the same scene. A change of camera angle or a new caption rarely needs its own accent.

For example, Warner #6 ends with the narrator’s “Miriam remembered walking in” and her own “I was shocked.” In the Short the narrator finishes at 31.01 s and Miriam begins at 31.41 s. To let her take over, finish the music under the narrator, keep that small gap and let the ABC15 recording carry her sentence through “going on.” Its location sound already travels with her voice in `voice.wav`. If you extend the room around a cut, take a clean piece from that same recording, listen for a reporter or embedded music and trim it clear of the original clip. A gentle edge fade belongs on the room tone, clear of the speaker’s first consonant.

The template retains the eight-beat document score when `scene_audio` is absent. To score a new reel by scene, set `scene_audio` in its `one/config.json`. An empty list gives you voice and original clips alone. Each cue uses a prepared mono or stereo audio file relative to the reel, a zero-based take from `takes.json`, an optional offset in seconds from its start, and a linear gain. The mixer keeps stereo placement, fades the cue edges and ducks the cue under speech. This example places a short pulse 350 ms into take 2, on the decision it marks.

```json
{"scene_audio":[{"take":2,"offset":0.35,"file":"assets/decision-pulse.wav","gain":0.20}]}
```

Play the transition once at low volume in mono. A deep bass cue may disappear on a phone. If the listener needs that cue to recognize the action, choose a sound with an audible midrange detail from the scene. If it masks the first word, lower it or end it earlier. Keep the existing mix limiter at .42 and verify −14 LUFS and true peak ≤ −1.2 dB in the encoded master.

## Render and master (lemo-opuscar, `~/lemo-opuscar`)
```
node core/render/still.mjs <reel> 6 12 20 --size 1080x1920        # stills check first
node core/render/video.mjs <reel> --fps 30 --workers 5 --size 1080x1920
LEMO_COLOR=bt709 sh core/render/mux.sh <video> <mix.wav> <out.mp4> 30 0
ffmpeg -i out.mp4 -c copy -movflags +faststart reel-NN-phone.mp4
```
Page contract: `window.render(t)`, `window.DUR`, `window.READY`, `window.TEXTS(t)`; Canvas 2D, deterministic, no wall clock. `readcheck.mjs` checks text on screen long enough to read; `sheet.py` makes a contact sheet; `srt.py` the captions file.

### Fit evidence cards in the portrait layout

Before rendering, enumerate the distinct evidence cards in the actual shot list, including beat-specific overrides. Use the production fonts, anchors and wrapped lines to measure each visible glyph bounding box at both export widths. Compare the lowest headline glyph with the top of the divider stroke and the first supporting glyph. Check the bottom of the supporting text against the safe area. Reserve space for any divider. Reduce the headline size or reposition the support text when their bounds touch. In the Coach K layout an 18-pixel gap at full resolution kept the headline clear of the divider. Other layouts can choose a gap appropriate to their type size. Inspect the longest cards in both formats at actual viewing size, including a decoded frame from each card that needed resizing.

### Check the exported picture at shot changes

Play the actual MP4 across a cut from a graphic to camera footage. When FFmpeg composites a separately timed caption or header layer, inconsistent color metadata across the joined shots can restart the filter graph and temporarily drop the layer. Make the shot inputs share dimensions, frame rate, sample aspect ratio, pixel format, range, primaries, transfer and matrix before compositing. For BT.709 masters, convert the pixels to the intended range/matrix as needed, then consistently tag the outputs. Once the inputs agree, `-reinit_filter 0` on the concat inputs keeps the overlay clock continuous. Decode the affected cut after exporting both layouts.

If the design has a persistent graphic, point `scripts/check_overlay.py` at a small solid interior patch. It checks every decoded frame and reports missing intervals. Choose coordinates separately for each layout and restrict the time range if the design intentionally hides the graphic. A passing mark check covers layer continuity. Read actual captions and source labels on representative frames as a separate check.

```sh
python3 scripts/check_overlay.py reel.mp4 --region 62 86 4 6 --color FF4A2E
```

Review the shot on the spoken word it illustrates. A clip described as a van shot can spend its first seconds on roadside scenery. For exhibits, inspect the final phone-size crop with its column headings, unit, date and source still legible. Measure loudness and true peak on the encoded AAC as well as the mix.
Send videos as downloads: inline players start muted and Joe twice heard "no sound".

## Compilation
Concat the phone copies in order with a `list.txt` (`ffmpeg -f concat -safe 0 -i list.txt -c copy`), make a 720p preview for phones.
