# Research and footage

## 1. Pick the case
- Recent (last ~5 years), had the nation's attention, has a **public primary record** (FBI Vault release, depositions, bodycam, court filings, an independent review). No record = no series; the format is "we read them".
- Angle: "what you think you know vs. what the record says". Top-10 countdown, each item a thing the public narrative got wrong or never heard.

## 2. Research (three agents in parallel, then a deep dive)
Spawn three research agents in one message, each writing a file in `research/`:
1. **primary-facts.md**: official timeline from primary sources (FBI final update, police reports, court records, autopsy summary as reported, legislation passed after). Each row: claim, source URL, exact wording.
2. **sleuths.md**: Reddit (r/UnresolvedMysteries, case subs), Websleuths threads, YouTube true-crime channels, documentaries. What the crowd believes, what it got right, what it got wrong. Use the OpenTabs Reddit tools or old.reddit `.json` endpoints.
3. **rights.md**: every footage source (news clips, bodycam, 911 audio, family press conferences), who owns it, where to download, and the fair-use posture (commentary, short excerpts, transformative). Photos of the victim belong to the family: none.

Then a **deep-dive** on the primary documents themselves (download, read the page images, pull quotes with page numbers). Agents' page cites are often wrong (the Petito deep-dive had two): every quote that airs is checked against the page image by me.

Then `CANDIDATE-10.md`: 15+ candidates scored on surprise, proof on screen, visual. Joe picks / OKs the ten.

## 3. FACTS.md (the gate)
Every claim on screen or in the voice gets a row: claim, source, wording. Nothing airs that isn't in FACTS. Stats too (attention stats: use the defensible figure, note the bigger one you didn't use). Mark inferences and our summaries as such. Keep a "left out on purpose" list. Example: `example-FACTS-petito.md`.

## 4. Getting the documents
- **FBI Vault** blocks scripts. Use the Wayback Machine: `scripts/vault-get.sh <vault path> out.pdf` (CDX lookup, `id_` capture of `/at_download/file`). Page counts per part from the Vault listing.
- **Depositions / court filings**: news sites often host the PDF statically (the Fox depositions were plain static PDFs); CourtListener for federal dockets.
- Render pages with `pdftoppm -r 150 -png -f N -l N`. Read the page image before quoting.
- Wall shot: `scripts/wall.py <assets dir> a.pdf b.pdf --key name=0:81` (text pages only, no photos of people).

## 5. Getting footage
- `scripts/get-clips.sh raw/ <youtube ids>`. Prefer the station's own raw upload (longest, least edited, burned timestamps) over packaged segments.
- **Bot check ("confirm you're not a bot") = you're on a datacenter IP** (VPN or exit node). Turn it off for the download, then back on. Never borrow browser cookies.
- Find cut points with Whisper word timings on the clip's audio (faster_whisper in `~/lemo-opuscar/.venv`), not by ear. Cut 0.1 s before the first word, 0.25 s after the last.
- Prep (`templates/film-prep.sh` pattern): crop out channel bugs, lower-thirds, plates, other creators' arrows and names; greyscale; 30 fps JPG sequence + mono 48 kHz wav per clip. ≤10 s per clip, always under commentary, source tag on screen.

## 6. Privacy and fairness (publish gate)
- No image of the victim. No weapons, journal/notebook text, or remains details.
- Crop: license plates, house numbers, channel names on FBI pages, private individuals' names in documents unless already public in coverage.
- Never state an uncharged crime as fact. Opinion is wanted, built on what's on screen; name the innocent explanation, then say why it still looks bad.
