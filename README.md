# Joe Wilson's skills

Skills for Claude Code that came out of real work. Each one was built while doing the job, then written down so the next run starts where the last one ended. They're updated here as they improve.

## Install

```
/plugin marketplace add joewilsonai/skills
/plugin install we-read-them@joewilson-skills
```

Update later with `/plugin marketplace update joewilson-skills`.

## Skills

### we-read-them
True-crime explainers built from the public record, not from the retelling. The series is called **We Read Them**: we read the FBI file, the depositions and the bodycam so you don't have to, and show what they say against what everyone thinks they know.

The skill runs a case end to end:
- **Research:** three agents in parallel (primary sources, Reddit and web sleuths, footage rights), then a deep read of the documents. Nothing airs without a row in `FACTS.md`, and every quote is checked against the page image.
- **Documents and footage:** FBI Vault parts through the Wayback Machine, deposition PDFs, news clips cut with Whisper word timings, channel bugs and private details cropped out, every clip short and under commentary.
- **Voice:** one continuous ElevenLabs take for the narrator with delivery tags, a second voice that reads the record aloud, and a pronunciation dictionary so names and initialisms come out right.
- **Picture:** vertical 1080×1920 reels rendered in code (Canvas, deterministic) with [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), real document pages highlighted on screen, stats that hold long enough to read.
- **Mix and master:** bed, hits and foley under the voice, −14 LUFS, true peak ≤ −1.2 dB.

First case: Gabby Petito. A 3:44 film and eleven reels (intro plus a ten-to-one countdown), November 2026.

Requires: `ffmpeg`, `yt-dlp`, `poppler` (pdftoppm), Node, Python with `faster-whisper`, `soundfile`, `numpy`, `Pillow`, an ElevenLabs key in `ELEVENLABS_API_KEY`, and lemo-opuscar for rendering.

## License
MIT
