# Joe Wilson's skills

Skills for Claude Code that came out of real work. Each one was built while doing the job, then written down so the next run starts where the last one ended. They're updated here as they improve.

## Install

In Claude Code:

```
/plugin marketplace add joewilsonai/skills
/plugin install we-read-them@joewilson-skills
```

For an existing installation, refresh the marketplace with `claude plugin marketplace update joewilson-skills`, then run `claude plugin update we-read-them@joewilson-skills` and restart Claude Code.

## Skills

| Skill | What it makes | Version |
|---|---|---|
| [we-read-them](plugins/we-read-them/skills/we-read-them/SKILL.md) | Sourced YouTube documentaries and portrait Shorts with independent script and first-view edit reviews | 1.12.0 |

### we-read-them

**We Read Them turns one question into a YouTube documentary and ten standalone Shorts.** Give it a question about sports, business, technology, history or true crime. It checks claims against original records and footage, then builds a countdown where each finding helps answer the question. Viewers see the evidence on screen and hear why it matters.

Before recording, two independent AI reviewers explain the opening in their own words and flag unfamiliar terms or gaps in the story. The producing agent revises the script, checks pronunciation in the finished audio and prepares chapters, captions and thumbnails.

See how one investigation works at two lengths. [Watch the 8-minute Karen Read documentary](https://www.youtube.com/watch?v=8j7-IBt2jno) or [watch the 39-second Short about the jury’s question](https://www.youtube.com/shorts/kR4Rx8rfev0).

Once it's installed, ask Claude Code for it in plain words: "We Read Them on <case>", "make reels of <case>", "top 10 things you didn't know about <case>". The skill picks up from there.

It runs a case end to end:

- **Story.** Plan what makes the opening question matter to the viewer, which discovery lets them see the consequences, and what the ending changes for them. [Countdown treatment](plugins/we-read-them/skills/we-read-them/templates/countdown-treatment.md)
- **Edit loop.** Run the highest-impact finding through a reversible edit and independent re-review. The winning change is verified in the requested deliverables. [Edit workflow](plugins/we-read-them/skills/we-read-them/references/edit-loop.md)
- **Video comparison.** Research similar releases, score their openings, middle chapters and endings against ours, and measure how much of the picture is footage, documents, photographs or designed graphics. [Comparison guide](plugins/we-read-them/skills/we-read-them/references/video-benchmarking.md)
- **Script review.** With the authenticated Antigravity CLI (`agy`), Gemini and Claude each retell the spoken opening before seeing the full script. The runner archives their exact reads and recommendations. The producing agent applies supported repairs and reruns review on the revised draft. An opening pickup can be reviewed against the rest of the film without reopening unrelated chapters. [Review command and workflow](plugins/we-read-them/skills/we-read-them/SKILL.md#review-the-complete-script-before-recording)

- **Research:** three agents in parallel (primary sources, Reddit and web sleuths, footage rights), then a deep read of the documents. Nothing airs without a row in `FACTS.md`, and every quote is checked against the page image.
- **Documents and footage:** FBI Vault parts through the Wayback Machine, deposition PDFs, news clips cut with Whisper word timings, on-screen evidence and source credits retained, private details cropped or blurred, every clip short and under commentary.
- **Voice.** One male narrator carries the countdown and reads written quotations. The screen credits the source. Delivery cues, a pronunciation dictionary and a word-by-word audio review cover names, numbers and initialisms.
- **Picture:** vertical 1080×1920 reels rendered in code (Canvas, deterministic) with [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), credited archive scenes, readable document excerpts and comparison graphics, plus a 1920×1080 cut with embedded chapters. The [YouTube editing guide](plugins/we-read-them/skills/we-read-them/references/youtube-editing.md) includes a matching portrait and widescreen example.
- **Mix and master.** Score a scene with specified sound cues, use the existing document score, or leave the witness on their own. Match the house loudness and true-peak targets across the chaptered film.

Case 1: Gabby Petito, a 3:44 film and eleven reels. Case 2: Hailey Dunn, eleven reels built start to finish by the skill in one night, with builders running in parallel. November 2026. A finished facts gate from case 1 is in [`references/example-FACTS-petito.md`](plugins/we-read-them/skills/we-read-them/references/example-FACTS-petito.md).

**You need:** `ffmpeg`, `yt-dlp`, `poppler` (`pdftoppm`), Node, Python with `faster-whisper`, `soundfile`, `numpy`, `scipy` and `Pillow`, an ElevenLabs key in `ELEVENLABS_API_KEY`, and lemo-opuscar for rendering. ElevenLabs bills your account for each take.

**Limits:** the skill is written the way its author works, so it names his folder layout and expects lemo-opuscar's Python environment. Use the git-ignored `LOCAL.md` next to `SKILL.md` for local paths and channel preferences. Supply API credentials through environment variables or your secret manager. The quiet-layout templates load the included `aibc-brand/` fonts beside `source-edit.js`. The legacy templates expect the original renderer’s fonts and assets. YouTube and fbi.gov block many VPN and datacenter addresses, so download from a home connection.

## License

The skill’s code and documentation use the [MIT license](LICENSE). See the bundled font licenses for [Archivo Black](plugins/we-read-them/skills/we-read-them/templates/aibc-brand/ArchivoBlack-OFL.txt), [Inter](plugins/we-read-them/skills/we-read-them/templates/aibc-brand/Inter-OFL.txt), and [Special Elite](plugins/we-read-them/skills/we-read-them/templates/aibc-brand/SpecialElite-LICENSE.txt).
