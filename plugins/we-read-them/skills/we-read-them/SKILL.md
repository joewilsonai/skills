---
name: we-read-them
description: Produce evidence-led We Read Them videos on any subject for a general audience. Use for a series investigation, a sourced Top Ten countdown, an independent script review, a researched video comparison scorecard, an edit and re-review loop, portrait Shorts, or a chaptered YouTube documentary.
---

# We Read Them

**WE READ THEM.** Joe named the series on 11/3/2026. Follow a question viewers can recognize to a record they can see and read for themselves. Case 1: Gabby Petito (film + 11 reels). Case 2: Hailey Dunn (11 reels, built start to finish by this skill in one night: one session wrote and verified the scripts, five builders ran two reels each).

## Plan the whole countdown before writing the Shorts

Choose the organizing question to suit the subject. A portrait can follow choices that reveal character, a how-to can follow one task, and an investigation can follow a claim back to its source. Ask two questions while writing. What can the record show? In what situation would this viewer care about the answer? For a sports portrait, a fan who remembers the trophy might want to know who shared the night with the winner. A call home can change whom they picture the next time they see that photograph.

Once the ten are chosen, use the [countdown treatment](templates/countdown-treatment.md) for `film/TREATMENT.md`. Start with the question the viewer will carry into the film. Choose the first shot and the final piece of evidence together. Write the first and last lines out loud. The ending should let someone answer the opening question more precisely than they could at the start.

Give each rank one discovery, its source, and a reason the next chapter belongs there. Introduce the viewer’s situation in the opening. At a middle discovery, let them see the choice or consequence that gives it weight. At the ending, show what this lets them do, notice or understand differently. Let a scene or change of perspective carry the idea wherever it lands naturally. Keep a historically or numerically defined ranking intact. Use a returning person, action, object or question to connect the chapters when the order is fixed. Share this treatment with every chapter builder.

Give the first spoken beat a purpose. Say what we’re doing with this subject and why the answer matters. Over the first shot, name the choices we’ll trace, the records we’ll compare or the action we’ll test. Promise only what those sources can show. In a portrait, the choices someone made under pressure can show what they put first. Counting ten career highlights leaves that question open. Let the first scene deliver one discovery. At number one, show the evidence that earns the answer, then leave time to take in the final image or voice. Put any invitation to subscribe after that moment. [Opening, chapter order and conclusion](references/youtube-editing.md#build-the-story-across-all-ten)

## Benchmark each episode against comparable videos

Use the **AI Builders Club broadcast identity** for graphics across every topic. Build the intro, countdown cards, diagrams, captions, thumbnails and both video formats from the same palette and font roles. Let the subject change the evidence and imagery. [Broadcast colors, type and export checks](references/youtube-editing.md#use-the-ai-builders-club-broadcast-identity)

For a new countdown or a request to score an existing video, research popular and well-made examples for that topic, audience and format. Use the [comparison guide](references/video-benchmarking.md) and the [scorecard](templates/video-scorecard.md). Score the opening, individual ranks, middle, conclusion, clarity and production choices against specific peer moments. Measure how much screen time uses filmed footage, interviews, photographs, documents, animations and other graphics. Log overlapping treatments separately. At planning time choose what the episode needs, at script review evaluate the proposed story, and at rough cut score what a viewer actually sees and hears. Record the findings and the most useful edit in `film/BENCHMARK.md`.

## Run the edit loop

When producing or revising a video, act on the most consequential scorecard finding. Define what the audience should understand, make a reversible edit, render a comparable excerpt, and have independent readers test the actual change. Keep the version supported by the viewer’s answer and the affected quality checks. Revert a weaker or tied edit. If the requested scope is the whole episode, apply the winner to the working sources, rebuild the affected deliverables and verify the result there. Continue only while a consequential finding has a specific repair to test. [Edit loop and commands](references/edit-loop.md)

For a playback test, let a fresh viewer watch once and explain the scene before showing them the question you want answered. Record what they understood unaided, what took a prompt or replay, and what they missed. The skill includes a local player that presents the two cuts in either order. [First-view test](references/edit-loop.md#test-what-survives-one-viewing)

When the audience loses the point of the film, test the opening, the middle turn and the ending together before polishing another rank. Use the viewer’s explanation to locate the first missing link. [Choose the viewer problem](references/edit-loop.md#1-choose-the-viewer-problem)

## Review the complete script before recording

Once the intro, chapters and ending are written, run the [two-family review](scripts/review_script.py) from the skill directory. Give it one audience-facing draft with the intended audience, public title, narration, quoted sound, screen labels and visible action in viewing order. Keep the treatment, rationale and prior critiques out of the packet.

```sh
python3 scripts/review_script.py film/SCRIPT.md --output film/script-reviews
```

Use the actual paths for the episode. The runner extracts spoken paragraphs from a `## Opening` section containing separate `*On screen` cues. For a speech-only opening or another layout, pass `--intro-file` with the entire spoken opening. Check it against the draft yourself in those layouts. The runner verifies that the supplied passages occur verbatim in order. Use the default full review for the first complete episode draft. For an opening pickup, add `--scope opening` to review its purpose and fit with the full sequence. For a revision focused on why viewers care, add `--scope viewer-stakes` to check how the opening, middle and ending carry that idea through the full packet. Each reader retells the opening before seeing the title, graphics or follow-up questions. The runner then sends the full packet and the [script reviewer’s criteria](references/script-reviewer.md). It saves the exact draft, prompts, provider receipts, verified models, retellings, recommendations and verdicts under the draft and prompt hashes.

The runner uses separate Gemini and Claude sessions through `agy`. To choose other available models, repeat `--model` with two IDs from different families listed by `agy models`. Rerunning the same inputs reuses completed reads. If one reader failed, inspect the saved error and receipts, correct the cause and use `--retry-failed` for missing work. A malformed verdict is archived and retried from the saved cold read. If the verified retry contains one valid JSON report plus a separate formatting note, the editor may validate the fenced report, check the surrounding words for a changed decision, and log the original provider response and that verification in the panel. Conflicting or incomplete judgments need another read. A model-identity mismatch requires a fresh session. If this provider is unavailable, dispatch the same staged [reviewer instructions](references/script-reviewer.md) to independent companion models. Verify the actual family of each responder and give an incomplete panel its actual coverage.

The agent producing the episode owns the revision loop. On **REVISE** (exit 2), inspect each quoted cue in the frozen script, compare the unaided retellings, and check proposed factual changes against `film/FACTS.md`. Apply grounded repairs to the working words and screen labels, regenerate the audience-facing draft, then run the same command again. Each distinct revision gets fresh readers. Record how each consequential finding was resolved. If a recommendation would introduce an error, change the supported explanation or verify the disputed cue against the source before another round. If successive rounds return the same unresolved objection and the record supplies no new evidence or supported edit, preserve the findings and report the specific blocker. **INCOMPLETE** (exit 1) leaves review open.

On **PASS** (exit 0), record the review scope, exact script hash, panel path, actual models and editorial decisions in `film/SCRIPT-REVIEW.md`. Continue the assigned production from that revision through voice, picture and delivery as requested. Uploading or publishing requires the producer’s authorization for the destination. For a review-only assignment, return the panel and editorial decision. In delegated production, routine edits and re-reviews belong to the producing agent. Stop for a producer decision only when the producer has expressly reserved it for this task. Later changes to meaning, order or first-use explanations reopen review before pickups. A single Short gets a review of its own setup, discovery and payoff.

**Choose the reference for the work at hand.**
- [Editing for YouTube](references/youtube-editing.md) covers the opening promise, shot choices, chapter handoffs and how to review a rough cut. Use it while planning the story and again before delivery.
- [Research and footage](references/research-and-footage.md) covers sourcing, exhibits and credits. For a sports tribute, use the [game-footage and oral-history checks](references/research-and-footage.md#college-basketball-footage-and-oral-histories).
- For family scenes, memoir excerpts and broadcast calls, use the [first-person sourcing guide](references/research-and-footage.md#first-person-accounts-and-broadcast-calls).
- For philosophy and intellectual history, use the [text and illustration guide](references/research-and-footage.md#philosophical-texts-and-their-illustrations). Let viewers try a thought experiment before revealing its result.
- [Pronunciation](references/pronunciation.md) covers the spoken script, source pronunciations and the word-by-word listening check on the final export.
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
Reel dir: `index.html` (picture), `mix.py`, `one/script.txt`, `one/config.json`, `assets/`, `fonts/`, output `reel-NN.mp4` + `-phone.mp4`. For an opening or chapter built around an original image or action, start from the [source-scene templates](references/youtube-editing.md#use-the-scene-templates). `reel-page.html` supports document-led chapters. `intro-page.html` and `intro-mix.py` implement the true-crime opening described below.

## Show the people (Joe, 11/3, after case 2: "people want to see who we are talking about")
Choose footage where a viewer can see who did what. In business or sports, open on the transaction, play or decision that poses the question. Follow the people who carried it out, then reveal the record that changes how the viewer understands it. In a crime case, show the victim, the people speaking on camera, reporters describing the public account, police at the podium and the places involved.
- **In a crime case, show the victim.** Her photo as it appears in news clips, the public missing poster, the official cold-case/police photo. Not: standalone family snapshots lifted from social media, funeral or memorial footage, remains or crime scene.
- **Show the real person, place and action.** Seek original footage for every reel. The series target of 30–50% applies when suitable footage exists. If an event was never recorded or the footage cannot be shown, use a credited photograph, firsthand page or source-based diagram. Label its actual occasion and use the person’s own voice where available.
- **When TV shaped the story, show the coverage.** Use the cable segments (Grace, HLN, network packages) as "what TV said," then answer them with the record.
- Crop or blur home addresses, private bystanders and minors other than the victim. For youth sports, a coach-only crop, a later adult interview and a sourced play diagram can tell the story. Use the original producer’s material for footage.

## True-crime intro (Hailey v2, Joe: "that was fucking awesome")
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
**Retrofitting an old intro (Gabby, 11/4):** keep the approved voice take and swap only the picture. Opening photo for 2 to 3.5 s of the first line, then the old first scene; put footage on the lines that name people. Keep a copy of the old reel in `r0/v1/`, then rebuild the compilation.
**Where the victim photo comes from:** the official poster first. FBI posters: Wayback `id_` capture of `fbi.gov/wanted/.../download.pdf`, then `pdfimages -png` pulls the photos at full size. Police and DPS cold-case pages often embed the photo as base64 in the HTML. Otherwise, a clean frame from a news clip.
**Date the footage from the original record.** Follow the date and attribution checks in [Research and footage](references/research-and-footage.md) before labelling a clip.
**End card photo:** keep it above the title (x 700, y 250, 320x400) so it never covers WE READ.
Helpers in the template: `vid(k, t0, X, Y, w, h, {z})` plays a jpg sequence (cover-fit, freezes on its last frame; uses the global `TNOW`), `photo(img, X, Y, w, h, k)` is the colour push-in, `CLIPN` lists each clip's frame count. Cut clips 1.5-4 s; find frames with a contact sheet (`ffmpeg -vf "fps=1/3,scale=240:-1,tile=8x5"`) before cutting.

## Two outputs (Joe, 11/22/2026)
A full Top Ten case ships **vertical shorts** (intro + 10 countdown reels, 1080x1920, built first with the loop below) **and a landscape long-form** (the same eleven pieces laid out at 1920x1080 and stitched into one YouTube video with chapters). The long-form reuses the voice, timings, mix and facts; only the picture is laid out again from `templates/reel-page-wide.html` and footage is re-cut wide. Read `references/landscape-longform.md` before starting it; stitch with `scripts/longform.py`. A request for a single chapter or editorial sample uses just the outputs requested.

## Publishing on the producer’s channel
Build three different ways into the finished film from the opening, evidence and payoff. Use the [thumbnail workshop](references/thumbnail-workshop.md) to check source rights, compose each title and Club-branded cover together, preview them at feed size and select a launch pair after a blind read. Save the selected public-use credit beside the exports.

Verify the producer’s authorized channel name and ID in Studio before release. For the original series, Joe’s channel is We Read Them (@wereadthem, UC_eh0wcerneJqMiQcLiQXgw). Follow the [YouTube publishing playbook](references/youtube-publishing.md) for a new upload or a catalog refresh. Use its [publication record](templates/youtube-publication.md) to choose one or two phrases a viewer would use, write a unique opening description, and check what Studio saved and what a viewer actually sees. Refresh an existing upload by its video ID. Check access for the specific feature you need and use the approved release time.

## The loop (one reel at a time)
1. **Research once per case** (references/research-and-footage.md). FACTS.md is the gate: nothing airs without a row.
2. **Script.** Hook in 2 s → "Number N." as its own beat → the record → our take → closing line. Have an opinion grounded in what's on screen (Joe: "we shouldn't be so pc pilled"); explain what the evidence supports and what could reasonably explain it. In crime cases, include the innocent explanation and avoid alleging an uncharged crime as fact. Plan shots around the [turn in the story](references/youtube-editing.md#cut-each-chapter-around-a-change). Several lines can play over one unfolding action. Time a new image to what the viewer needs to discover. Stats: one per full screen, big number + plain label + source tag, spoken, and **held** long enough to read.
3. **Review and prepare the spoken script.** Assemble the episode and run the [independent script review](#review-the-complete-script-before-recording). Then write out amounts, dates and initials, verify unfamiliar names from a recording by the person or organization, and update the pronunciation dictionary for the forms that need it.
4. **Voice** the episode with one male narrator. Smith on ElevenLabs reads the narration and every written quotation, including the intro and closing. If the production uses a fallback such as Gemini’s Charon, keep that voice throughout. In `scripts/onetake.py <reel>`, use `R:` for a written passage, credit its author or document on screen and label it “read from the record.” Use `C:` for a genuine source recording. Record connected sentences together, place delivery tags at meaningful turns, and build holds from natural gaps. Start the narration at tempo 1.12 and let dense quotations breathe.
5. **Audio review.** Check the voice against the reviewed script. Send a listening copy for approval when Joe has reserved that decision for the episode. In delegated production, correct delivery issues and continue.
6. **Picture.** Open on the strongest available action, person or artifact. Give each spoken beat one place for the eye to land. When a face or action carries the scene, give it room and clear the chapter furniture after its introduction. When the viewer needs to read a record or compare figures, give that evidence its own shot. Keep captions, essential qualifications and compact attribution legible in both formats. [Editing for visual clarity](references/youtube-editing.md#give-the-viewer-one-place-to-look)
7. **Review and revise the cut.** Run the [edit loop](references/edit-loop.md) on actionable findings. Update the comparison scorecard and picture mix against the actual export. Play the chaptered master straight through. Identify the opening question, where the evidence changes the story and the detail on which the ending depends. Check the handoffs at normal speed. Play a middle Short on its own to confirm its subject and payoff are clear. Inspect decisive frames in both layouts. [Viewer review](references/youtube-editing.md#review-the-edit-as-a-viewer)
8. **Mix, render and master** (limiter .42, true peak ≤ −1.2 dB, bt709, faststart). Check every narrated and quoted word in the exported audio against the spoken script. Replay doubtful words in context, correct confirmed errors, then verify the correction in the Short and the stitched film. Check both sides of every chapter transition. Follow the [pronunciation review](references/pronunciation.md#review-every-word-in-the-export), then [compare the stitched audio with the reviewed Shorts](references/landscape-longform.md#compare-the-master-with-the-reviewed-shorts).
9. **Deliver** the verified file in the requested surface. In a local chat, link the playable master and the Shorts. For an authorized attachment, use a downloadable copy so the audio is easy to check.
10. **Log** in the playbook status table and today's daily note.

The intro reel (r0) leads directly into number ten. Write its last line for this subject. Each ranked Short identifies its subject and delivers its own discovery. Number one also closes the film. At the end, `final/` gets numbered copies and one compilation.

## Scripts (`scripts/`)
| Script | Does |
|---|---|
| `onetake.py <reel>` | one-take narration → voice.wav/mp3 + takes.json (word timings per segment) |
| `voice.py <dir> [idx]` | per-line takes from script.json (single fixes, legacy) |
| `get-clips.sh <raw> <ids>` | yt-dlp news clips + info + auto subs |
| `vault-get.sh <path> <out>` | FBI Vault PDF through the Wayback Machine |
| `wall.py <out> <pdfs> --key n=i:p` | thumbnail wall of text-only record pages |
| `thumbnail_proof.py --duration M:SS --out-dir review --pair IMAGE TITLE` | previews up to three long-form covers at feed size with the duration badge, with and without their titles |
| `longform.py <reels> "<Case>" [--preview]` | stitches the wide reels into the long-form cut, drops the inner end cards, writes chapters.txt and a Telegram-size preview |
| `visual_mix.py LOG.tsv --duration SECONDS --method timeline\|sample` | totals primary footage and overlapping visual layers from a timed edit log or weighted samples |
| `edit_trial.py prepare / playback / decide` | stages neutral versions, makes local first-view test pages for video, and records the selected edit and evidence |
| `check_master_speech.py <master.mp4> <reels> [--report path.json]` | compares the finished chapter audio with the reviewed Shorts, including original-sound cues and word windows |
Run Python with `~/lemo-opuscar/.venv/bin/python` (faster_whisper, soundfile, soxr). Needs `ELEVENLABS_API_KEY` in the environment.

**If `LOCAL.md` exists next to this file, read it first** for machine-specific paths, channel preferences and network notes. Load credentials through environment variables or a secret manager.

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
- `onetake.py` resolves the reel directory before searching for its case pronunciation dictionary. When a correction affects one spoken block, use `--revoice-block N` with its zero-based index. Recheck the edited words in the final mix.
- onetake's start-snapping can put a line's start one phrase late; builders patched it with `fix-takes.py` (see `work/ai-builders-club/we-read-them-jonbenet-ramsey/reels/r6/tools/` and `r7/fix_takes.py`). Check the printed starts every time.
- Whisper writes "JonBenét" as "John Bonet" and spells "grand jury's" differently between takes; after a revoice, re-check every start word.
- A cut can carry a few frames of the source's previous shot: contact-sheet the first 10 frames of every cut (case 3 had 4 frames of an unnamed woman at the head of a page shot, and a dissolve into a childhood photo at the tail of another).
- When no transcription model agrees on a word in a C: clip, caption it as "…", never the likelier guess.
- Cases where the family is alive and has sued (case 3): no line implies anyone killed her; every theory attributed with the record's answer on screen; the victim's sibling never as a child; no pageant footage.
- Phone delivery: files over 30 MB need a `-small` re-encode (CRF 25). Use the producer’s requested delivery surface. For a size-limited attachment, make a smaller 720p preview and keep the full-resolution master.
