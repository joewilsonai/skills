# Two outputs from one case: vertical shorts and the landscape long-form

Joe, 11/22/2026: "we could use the intro as a short but then the whole thing as longform." A full Top Ten case ships both:
- **Shorts (9:16, 1080x1920):** the intro and the ten countdown reels, each its own upload. Built first (SKILL.md loop).
- **Long-form (16:9, 1920x1080):** the same eleven pieces laid out wide and stitched into one YouTube video with chapters. Same voice, same timings, same mix, same facts. Only the picture is laid out again, and footage is re-cut wide from the original clips.

## What carries over and what doesn't
| Piece | Wide version |
|---|---|
| `voice.wav`, `takes.json`, `out/mix.wav` | reused as is (symlink `takes.json`; mux with `../out/mix.wav`) |
| `fonts/`, document pages, the note image, stat values, `FACTS.md` rows | reused (symlink `wide/assets/shared -> ../../assets`) |
| footage jpg sequences | **re-cut**: the vertical cuts are cropped tall and too small for a 1160 px band. Use the same in/out points from the vertical page's prep notes, retain source credit and evidentiary lower thirds, apply the same privacy edits, scale for the largest box the shot occupies, preserve the case’s color treatment, use 30 fps, and put the frames into `wide/assets/<key>/`. Contact-sheet the first 10 frames of every cut. |
| picture code | **re-laid out** from `templates/reel-page-wide.html`: every coordinate comes from `L` (left rail: header, number, claim card; the 16:9 band for evidence; captions centred at the bottom; `L.full` for wall/timeline/end card) |

## The chapter rail and evidence band
Use the rail when the viewer needs a claim, comparison or score beside the evidence. Give a play, testimony or original passage a larger view at the decisive moment. Return to the rail when the coming line needs it. [Editing for YouTube](youtube-editing.md#cut-each-chapter-around-a-change)

- Left rail x 80-620: "WE READ THEM" + case line, red number (mono 210), claim card (sans 700, 46 px, struck in red on the record's answer), mono label under it.
- Band x 680-1840, y 140-792 (1160x652, 16:9): footage, document pages with highlights, stats (`stat()`), the victim's photo (colour, contain-fit, `photo()`), name cards (`namecard()`, lower-left inside the band). Source tag above the band at y 124.
- Captions: centred on the frame at y 960, two lines max; "read from the record" / "original sound" label in red at y 900.
- Full-stage scenes (`L.full`, x 80-1840, y 140-860) for the wall of pages, timelines, the title card; the rail can be hidden for these.
- A custom storyboard can use `endcard(t, ENDCARD_AT, photoImg)`. Record its start in `wide/meta.json`. The stitcher removes interior standalone cards and plays the complete final widescreen reel.

### Author the final shot

Choose the person, action or source detail that answers the opening question. Land on it as the last line earns it. Let the viewer see the consequence and hear the end of the approved mix. On a source-edit page, `endCard: 'source'` continues the last evidence in the usual ending interval with its source credit and the series mark. Supply `audioEnd` in seconds when the approved mix has a purposeful tail. Write the page’s `window.WRT_CHAPTER_META.endcard_at` to the usual wide metadata. The stitch command stays the same.

In a legacy hand-built storyboard, author the concluding source, action or approved photograph directly into the final wide reel. Give acknowledgements and attributions their intended time. For the established true-crime treatment, keep the approved victim photograph in colour, its identification and the authored photo-and-series card where the story calls for them. The complete #1 picture, credits and sound all survive the stitch. Play the approach to the last image and the ending at normal speed, then seek to the last frame in the master and preview. Confirm the intended evidence or acknowledgements remain visible and the last sound resolves.

## Per reel
1. `mkdir rN/wide`; symlink `fonts`, `takes.json`; `assets/shared -> ../../assets`; copy `templates/reel-page-wide.html` to `wide/index.html`.
2. Re-cut footage wide (same spans, same privacy edits: blurs, crops, no pageant b-roll, no minors, no house numbers).
3. Choose the widescreen composition for each scene. Use the `L` boxes for the chapter rail and evidence band or the source-first layouts in the [YouTube edit guide](youtube-editing.md). Keep every beat on the same word timing; keep every on-screen fact identical (no new facts in the wide cut).
4. Stills at 6-10 times with `--size 1920x1080`, read them, fix overlaps; then `video.mjs <rN/wide> --size 1920x1080`, `mux.sh <wide/out/video.mp4> ../out/mix.wav <wide/reel-NN-<slug>-wide.mp4> 30 0`.
5. `wide/meta.json`: `{"slug": "...", "chapter": "#N · Title", "endcard_at": <seconds>}` (r0: `"chapter": "Intro"`).

## Stitch

After a restart, reconcile any open narration receipt before sending a provider request. Match each portrait and widescreen export to the current chapter mix, captions and picture inputs using its saved render hashes. Resume the missing or outdated layouts, then stitch the checked chapters and rebuild the share copy and Shorts archive. A file modification time cannot tell you whether a render includes the latest pickup.

`~/lemo-opuscar/.venv/bin/python scripts/longform.py <case>/reels "<Case Name>" --preview` creates the widescreen MP4, embeds the chapter track, writes `final/chapters.txt` for YouTube and optionally makes a phone preview. The chapter starts use the same 30 fps frame boundaries as the edit. At each interior join the stitcher protects the latest utterance or timed word endpoint in `rN/takes.json` (or the copy in `rN/wide`). Only the remaining tail can fade, for up to 350 ms. A line that ends exactly at the cut plays at full level. Older reels without timing files keep the existing 350 ms fade. If a labelled cut falls before timed speech, move the standalone card after the affected line, rerender the wide reel and update `endcard_at`. This matters for a legacy intro whose series card appears while the narrator is still speaking. `--preset veryfast` is available for a quicker encode. Check chapter counts and titles with `ffprobe -v error -show_chapters -of json <master>`, view both sides of the joins and measure true peak.

When reusing H.264 picture streams to speed up a stitch, inspect the first video timestamp in each wide file. AAC encoder priming can give the muxed file an audio packet before the first picture and shift the concatenated film. Strip the audio from the intermediate picture copies, concatenate the video at its frame-derived chapter lengths, and build the master audio from the approved 48 kHz mixes. At 30 fps each video frame accounts for 1,600 audio samples. Verify the first picture and both sides of every join in the chaptered export.

An MP4 can contain a chapter list and a separate QuickTime text chapter track. Check both in the master and the share copy. The first command shows the chapter labels and times. The second reports the native text track’s media clock and sample count.

```sh
ffprobe -v error -show_chapters -of json "$master"
ffprobe -v error -select_streams d -show_entries stream=codec_tag_string,time_base,nb_frames -of json "$master"
```

Expect the intro followed by #10 through #1 and 11 samples in the track with the `text` codec tag. If a player exposes a chapter menu, jump to #1. A test MP4 with a 55-second finale and a movie timescale of 48,000,000 advertised all 11 chapters while its native text track ended at #2. Frame-derived chapter metadata with `TIMEBASE=1/30` and the FFmpeg output option `-movie_timescale 48000` preserved all 11 samples and titles. This clock can represent both a 30 fps frame and a 48 kHz audio sample exactly. The stitcher checks the separate text-track count before replacing either delivery file.

When a compact export stream-copies AAC, map the audio from the final master and retain its movie timescale. Compare `ffprobe -v error -select_streams a:0 -count_packets -show_entries stream=time_base,duration_ts,nb_read_packets -of json "$file"` on both exports. Also compare the hashes from `ffmpeg -v error -i "$file" -map 0:a:0 -c:a pcm_s32le -f hash -hash sha256 -` using the same decoder. An intermediate share copy inherited a 1,000-tick movie clock. Its AAC packet hash matched the master, but its edit list shortened the audio duration by 32 samples. Require both the stream measurements and the decoded PCM hashes to match for a stream-copy delivery.

After a factual correction, update the source exhibit, narration, word timings and captions together. Re-export both layouts, rebuild the master and refresh its chapter times. Play the corrected line from the stitched master and check that the closing words survive the final cut. For a local handoff, include the master, the intro and ten individual Shorts, sources and footage credits.

## Publishing
For a YouTube release, draft the title and thumbnail pairs, description, chapter labels and sources in `final/youtube.md`. Follow the [publishing guide](youtube-publishing.md) and Joe’s authorization for that episode before any upload or visibility change.

## Compare the master with the reviewed Shorts

Run the comparison after the final mux, using the same vertical files that passed pronunciation review.

```sh
~/lemo-opuscar/.venv/bin/python scripts/check_master_speech.py \
    "$master" "$case_dir/reels" --report "$case_dir/research/master-speech-check.json"
```

The command pairs all eleven embedded chapters with the intro and countdown in order. It decodes the master and the reviewed Shorts to 12 kHz mono, aligns the spoken audio within 80 ms, and checks every utterance, every available timed word and overlapping windows across each chapter. It checks each interior cut against its recorded end-card time and preserves audible sound after the last word of the finale. It checks matching quiet intervals and allows the interior ending fade. Listen to the last timed word across a tight join and compare the sound level with the reviewed take. Original recordings without individual word times still receive the whole-utterance and window checks. A failed check exits with status 1 and identifies the rank and affected interval. The optional JSON report includes the master hash and per-chapter results. Listen to a flagged interval in both exports to diagnose it. This comparison verifies that the reviewed performance survived stitching. The pronunciation review evaluates the performance itself.
