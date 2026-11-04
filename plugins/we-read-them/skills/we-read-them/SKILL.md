---
name: we-read-them
description: Use when Joe wants a true-crime explainer — the "We Read Them" series (vertical reels for Shorts/Reels/TikTok, a Dateline-style full film, or a top-10 countdown) built from the primary record of a real case. Triggers: "true crime video", "We Read Them", "do another case", "top 10 things you didn't know about <case>", "find footage for", "make reels of", "what the record says". Covers case pick, research agents, FACTS gate, finding and cutting real news footage and FBI/court documents, pronunciation, one-take ElevenLabs narration, picture in lemo-opuscar, mix, render, and delivery.
---

# We Read Them

Series (Joe named it 11/3/2026): **WE READ THEM.** We read the public record of a famous case so viewers don't have to, and show what it says against what everyone thinks they know. Case 1: Gabby Petito (film + 11 reels). Case 2: Hailey Dunn (11 reels, built start to finish by this skill in one night: one session wrote and verified the scripts, five builders ran two reels each).

**Before anything, read the reference you need:**
- `references/research-and-footage.md` — picking the case, the three research agents, FACTS.md, getting FBI Vault / deposition PDFs, downloading and cutting news clips, privacy rules.
- `references/pronunciation.md` — what needs a dictionary rule before voicing.
- `references/voice-mix-render.md` — voices, one-take tool, mix, lemo-opuscar render/master, sending.
- `references/example-FACTS-petito.md` — what a finished FACTS gate looks like.

## Layout of a case
```
work/<bucket>/<case>/
  research/ primary-facts.md sleuths.md rights.md deep-dive.md
  CANDIDATE-10.md   pron-dict.json   pron-rules.json
  film/  FACTS.md TREATMENT.md index.html tools/ audio/ raw/ assets/
  reels/ r0 (intro) r10 … r1, tools -> skill scripts, final/
```
Reel dir: `index.html` (picture), `mix.py`, `one/script.txt`, `one/config.json`, `assets/`, `fonts/`, output `reel-NN.mp4` + `-phone.mp4`. Start from `templates/` (`reel-page.html` = document-led, `reel-page-footage.html` = clip-led, `intro-page.html` + `intro-mix.py` = series intro with the page wall and stat screens).

## Show the people (Joe, 11/3, after case 2: "people want to see who we are talking about")
Footage-forward, the way Nancy Grace and Dateline do it: the victim's face, the people in the case talking on camera, TV hosts and reporters saying what TV said, police at the podium, the places. Documents prove the point; footage is what people watch.
- **Show the victim.** Her photo as it appears in news clips, the public missing poster, the official cold-case/police photo. Not: standalone family snapshots lifted from social media, funeral or memorial footage, remains or crime scene.
- **Every reel gets real footage** (target 30-50% of runtime): the person the reel is about, on camera, in their own voice where it exists. A quote card is the fallback when no footage exists, not the default.
- **TV is a character.** Use the cable segments (Grace, HLN, network packages) as "what TV said," then answer them with the record.
- Still never: minors other than the victim (blur or cut), home addresses, private bystanders, other creators' commentary videos.

## The intro that works (Hailey v2, Joe: "that was fucking awesome")
Template: `templates/intro-page.html` + `intro-mix.py` + `intro-config.json` + `intro-script.txt`. The beats, in order:
1. **Open on the victim:** the official photo (police / cold-case / missing poster) in **colour**, slow push-in, name and age card. She is the only colour in the reel; everything else is greyscale.
2. **"Never came home":** the missing billboard or flyer footage, then search footage.
3. **The suspect on camera:** his own interview footage under the line that names him, with a name card ("her mother's live-in boyfriend").
4. **The hook from the record:** a paper card of the affidavit line, highlighted as it's said.
5. **The place:** location footage (the lake sign), then the schematic map.
6. **His own voice:** a `C:` clip of his denial, on camera, labelled "original sound".
7. **Charged and dropped:** booking photo pinned over the indictment page with a stamp, then the dismissal page.
8. **"Solved?":** the attention stats (what the crowd believes), then the wall of real pages and the list of what we read.
9. **WE READ THEM card with her photo beside it**, then "10 things you probably don't know."
Helpers in the template: `vid(k, t0, X, Y, w, h, {z})` plays a jpg sequence (cover-fit, freezes on its last frame; uses the global `TNOW`), `photo(img, X, Y, w, h, k)` is the colour push-in, `CLIPN` lists each clip's frame count. Cut clips 1.5-4 s; find frames with a contact sheet (`ffmpeg -vf "fps=1/3,scale=240:-1,tile=8x5"`) before cutting.

## The loop (one reel at a time)
1. **Research once per case** (references/research-and-footage.md). FACTS.md is the gate: nothing airs without a row.
2. **Script.** Hook in 2 s → "Number N." as its own beat → the record → our take → closing line. Have an opinion grounded in what's on screen (Joe: "we shouldn't be so pc pilled"); name the innocent explanation, then why it still looks bad; never assert an uncharged crime. **Make every line visual**: find the real thing for each line (stat slams, timestamps, map, document line, quote card, clip, contradiction). Stats: one per full screen, big number + plain label + source tag, spoken, and **held** long enough to read.
3. **Pronunciation pass** → add rules → bump dictionary version.
4. **Voice** with `scripts/onetake.py <reel>`: one continuous Smith take on eleven_v3 with tags I place, Harper reads record text (`R:` lines, labelled "read from the record" on screen), holds by stretching natural gaps. Never stitch sentence takes ("choppy"), never force dramatic splits ("trying too hard"), keep it fast (tempo 1.12).
5. **Audio to Joe** as mp3 download → OK. (Skip once Joe says to run the rest autonomously; he did on 11/3 after three reels.)
6. **Picture**: 1080×1920, "WE READ THEM" header, red countdown number, claim card struck the moment the record answers it, evidence band y 720–1440, captions y 1620, real document pages with highlights, clips ≤10 s cropped and greyscale, "Full film" end card. No dead screens.
7. **Stills check** at 6–8 times: overlaps, clipped highlights, captions duplicating on-screen text, anything private in frame.
8. **Mix, render, master** (limiter .42, true peak ≤ −1.2 dB, bt709, faststart).
9. **Send** the phone copy with `SendUserFile` `display: attach` (inline players start muted).
10. **Log** in the playbook status table and today's daily note.

The intro reel (r0) ends "Here are ten things you probably don't know." and cuts. Countdown reels follow 10 → 1. At the end, `final/` gets numbered copies and one compilation.

## Scripts (`scripts/`)
| Script | Does |
|---|---|
| `onetake.py <reel>` | one-take narration → voice.wav/mp3 + takes.json (word timings per segment) |
| `voice.py <dir> [idx]` | per-line takes from script.json (single fixes, legacy) |
| `get-clips.sh <raw> <ids>` | yt-dlp news clips + info + auto subs |
| `vault-get.sh <path> <out>` | FBI Vault PDF through the Wayback Machine |
| `wall.py <out> <pdfs> --key n=i:p` | thumbnail wall of text-only record pages |
Run Python with `~/lemo-opuscar/.venv/bin/python` (faster_whisper, soundfile, soxr). Needs `ELEVENLABS_API_KEY` in the environment.

**If `LOCAL.md` exists next to this file, read it first** (machine-specific paths, keys, network notes; not published).

## Running it in parallel (case 2)
Lock every script and the FACTS gate yourself first, build the intro yourself (it sets the case's look: header, helpers, fonts), then hand builders two reels each with: the locked script, their FACTS rows, the r0 folder as the look, `--workers 2` for renders. Builders verify their own VERIFY rows before voicing and may change a word only to fix a fact (they caught four: "two cities" → three, "believed he was" → "may have been", "three days later" → that same night, "all evidence" → some). Review each finished reel's frames before sending.

## Traps that already cost us
- Whisper drops "Number" at the start of a take and writes "Hailey" as "Haley", "2021" as digits, "seven-page" as "seven -page": start words must match what Whisper writes (onetake normalizes numbers 1-20 and hyphens; use a bare "five" when "Number five" isn't heard).
- Whisper starts a line at the end of the previous silence; onetake snaps each line to the real speech onset. Still glance at the printed starts.
- Check the true peak after every mux: soft clicks and the AAC encoder can push a -1.2 dB master over 0. A second limiter pass in mix.py, or softer clicks, fixes it.
- Case 2 shipped with almost no footage (4 of 11 reels) and no photo of the victim because of an over-cautious rule. Don't repeat it: plan the footage per reel at script time.
- YouTube / fbi.gov bot checks → you're on a VPN or datacenter exit; download from a home IP.
- Agents' page citations can be wrong → verify every quote on the page image.
- "Gabby misk", "U ESSSS PS" → dictionary rules (`Misc`→miscellaneous, `USPS`→U.S.P.S.).
- Whisper hears "10" as "ten" → normalize numbers when matching segments.
- Privacy in frame: channel names on FBI pages, other creators' arrows, plates, weapon lines on receipts, any photo of the victim.
- "No sound" = muted inline player, not the file.
- Biggest stat isn't the one to use; the defensible one is (650M+ TikTok views, not 1.2B).
