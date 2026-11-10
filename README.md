# Joe Wilson's skills

Skills for Claude Code that came out of real work. Each one was built while doing the job, then written down so the next run starts where the last one ended. They're updated here as they improve.

## Install

In Claude Code:

```
/plugin marketplace add joewilsonai/skills
/plugin install we-read-them@joewilson-skills
```

Update later with `/plugin marketplace update joewilson-skills`.

## Skills

| Skill | What it makes | Version |
|---|---|---|
| [we-read-them](plugins/we-read-them/skills/we-read-them/SKILL.md) | True-crime reels and films built from the primary record of a real case | 1.3.1 |

### we-read-them

True-crime explainers built from the public record, not from the retelling. The series is called **We Read Them**: we read the FBI file, the depositions and the bodycam so you don't have to, and show what they say against what everyone thinks they know.

Once it's installed, ask Claude Code for it in plain words: "We Read Them on <case>", "make reels of <case>", "top 10 things you didn't know about <case>". The skill picks up from there.

It runs a case end to end:

- **Research:** three agents in parallel (primary sources, Reddit and web sleuths, footage rights), then a deep read of the documents. Nothing airs without a row in `FACTS.md`, and every quote is checked against the page image.
- **Documents and footage:** FBI Vault parts through the Wayback Machine, deposition PDFs, news clips cut with Whisper word timings, channel bugs and private details cropped out, every clip short and under commentary.
- **Voice:** one continuous ElevenLabs take for the narrator with delivery tags, a second voice that reads the record aloud, and a pronunciation dictionary so names and initialisms come out right.
- **Picture:** vertical 1080×1920 reels rendered in code (Canvas, deterministic) with [lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar), real document pages highlighted on screen, stats that hold long enough to read.
- **Mix and master:** bed, hits and foley under the voice, −14 LUFS, true peak ≤ −1.2 dB.

Case 1: Gabby Petito, a 3:44 film and eleven reels. Case 2: Hailey Dunn, eleven reels built start to finish by the skill in one night, with builders running in parallel. November 2026. A finished facts gate from case 1 is in [`references/example-FACTS-petito.md`](plugins/we-read-them/skills/we-read-them/references/example-FACTS-petito.md).

**You need:** `ffmpeg`, `yt-dlp`, `poppler` (`pdftoppm`), Node, Python with `faster-whisper`, `soundfile`, `numpy`, `scipy` and `Pillow`, an ElevenLabs key in `ELEVENLABS_API_KEY`, and lemo-opuscar for rendering. ElevenLabs bills your account for each take.

**Limits:** the skill is written the way its author works, so it names his folder layout and expects lemo-opuscar's Python environment. Put your own paths and keys in a `LOCAL.md` next to `SKILL.md`; the skill reads it first. YouTube and fbi.gov block many VPN and datacenter addresses, so download from a home connection.

## License

[MIT](LICENSE)
