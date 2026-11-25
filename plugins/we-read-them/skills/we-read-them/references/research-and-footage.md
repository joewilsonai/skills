# Research and footage

## 1. Pick the case
- Choose a recognizable question with a public record that can answer it. For a business or sports story, start with a purchase, play, ruling or other concrete moment. For true crime, recent cases that attracted national attention and have released investigative records are a good fit.
- Each countdown item should reveal something the viewer can verify. Frame an untested assumption as a question. Attribute a claim about what people believe to the poll, coverage or community that actually expressed it.

When choosing a topic for search demand, compare candidate names or phrases in Google Trends for the intended audience’s country and the same date range. For a YouTube release, inspect YouTube Search and Web Search separately. Keep terms together on one chart when comparing their scores. The 0–100 index is relative to the chart’s peak, and small samples may display as zero. Save the comparison links and date range. [How Google Trends measures interest](https://support.google.com/trends/answer/4365533)

Compare a full week with the previous week, then look for movement on the latest reported days. Flag a partial day. Read the rising related queries for the actual question people are asking. Verify the date of a release, hearing or other event that coincides with a spike before pitching it. Recommend the story that can answer that question with accessible records in time for the intended release.

## 2. Research (three agents in parallel, then a deep dive)
Spawn three research agents in one message, each writing a file in `research/`:
1. **primary-facts.md** records the timeline, claim, source URL and exact wording. Choose records with firsthand access to the event, such as filings, league rulings, game footage, testimony or an agency report. For true crime, keep the investigative, court and medical sources with their original attribution.
2. **sleuths.md** records specific beliefs and where they appear. Use relevant communities, contemporary broadcasts and documentaries. A fan thread, employee anecdote or Websleuths discussion can establish what someone said. Verify the underlying event independently.
3. **rights.md** records each candidate clip, original producer, rights holder if known, source URL, excerpt time and intended use. A library, hosting platform or repost may supply a copy. Record its role separately from the owner, plus any license, permission or editorial basis and required credit. For a crime case, include the victim’s public missing or cold-case photo and identify who actually appears in each clip.

Then read the primary record yourself. For a document quote, verify the wording on the actual page image and note both printed and PDF page numbers if they differ. For a spoken quotation, listen to the source recording at the cited time.

When a conversation or hearing changes audiences, check who was present for the exact words. A judge may discuss one answer with lawyers and deliver a different instruction when the jurors return. For verdicts and other formal decisions, pair the form with the decision read aloud. Label an unmarked form or editorial annotation visibly and give the exact finding and its limits in plain language.

Then `CANDIDATE-10.md`: 15+ candidates scored on surprise, proof on screen, visual. Joe picks / OKs the ten.

## 3. FACTS.md (the gate)
Every spoken or displayed claim gets a row in `film/FACTS.md` with its source, page or clip time, and supported wording. Mark allegations, findings, company statements and editorial inferences explicitly. Keep a “left out on purpose” list. [Example from the Petito case](example-FACTS-petito.md).

- For a figure, capture its unit, denominator or comparison baseline, geography and reporting period. Inspect the exact page or frame going into the edit, including column headers, footnotes and the settled value of an animated counter. Check the captions and voice against that exhibit.
- Trace apparent confirmations back to their source. A calculation that reuses a book’s figures can check the math in that book. Two articles can quote the same witness. When that distinction changes what viewers would believe or repeat, show where both accounts got their information and say what question is still open.
- A publisher’s article, broadcast graphic and narration can differ. Record which version supports each number and date. If the periods or figures cannot be reconciled, narrow the wording to what the exhibited source establishes. Carry a correction into the affected voice take, captions, picture, both aspect ratios and chapter copy.
- After a script reviewer changes a physical detail, replay the shot at the revised words. Verify the object, viewpoint and time in the actual crop, along with its caption. A verified photo of the correct building can still show the wrong doorway. If footage of the exact detail is unavailable, use the source passage or a plainly labeled question.
- Follow the parties through the claim. In a business story the brand on the vehicle, the driver’s employer, the carrier and the owner of the goods can all differ. Identify the role the source actually establishes. A complaint, court finding and settlement each support different wording.

For a filmed software experiment, save the exact input, tool or model version, relevant settings and observed output. A seeded draw from a shortlist and the model’s probabilities across its full vocabulary have different denominators. Label which the viewer sees. In a controlled comparison, keep the rest of the input fixed so the stated change is visible. Identify an editorial diagram or protocol illustration beside a measured result. When two primary records disagree, show each with its own label and report the precision they jointly support.

## 4. Getting the documents
- **FBI Vault** blocks scripts. Use the Wayback Machine: `scripts/vault-get.sh <vault path> out.pdf` (CDX lookup, `id_` capture of `/at_download/file`). Page counts per part from the Vault listing.
- **Depositions / court filings**: news sites often host the PDF statically (the Fox depositions were plain static PDFs); CourtListener for federal dockets.
- Render pages with `pdftoppm -r 150 -png -f N -l N`. Read the page image before quoting.
- Wall shot: `scripts/wall.py <assets dir> a.pdf b.pdf --key name=0:81` (text pages only, no photos of people).

## 5. Getting footage
- `scripts/get-clips.sh raw/ <youtube ids>`. Prefer the station's own raw upload (longest, least edited, burned timestamps) over packaged segments.
- **Bot check ("confirm you're not a bot") = you're on a datacenter IP** (VPN or exit node). Turn it off for the download, then back on. Never borrow browser cookies.
- Date the recorded event from the original caption, program or other contemporaneous record. An upload date establishes when that copy appeared.
- Label footage or audio of the event with its original source. If another facility, a stock clip, a demonstration, or a recreated order illustrates the process, identify it on screen as such. For a redrawn chart, name the data publisher and preserve the units and reporting period.
- Use Whisper word timings on the source audio to locate a candidate passage. Listen at both cut points and leave the consonants, breath and room tone needed for a natural entry and exit. For game action, also confirm the movement starts and finishes inside the picture edit.
- Prepare the source frames at 30 fps and the clip audio at 48 kHz. Preserve required credit, dates, units and meaningful lower thirds. Crop or blur private identifiers. Use the case’s color treatment. For the series’ short commentary excerpts, keep each cut within 10 seconds and any narrower source permission. Narration can introduce an original quote or call, then leave it audible on its own. Use the [edit guide](youtube-editing.md) to plan a truthful alternative when moving footage is unavailable.

## College basketball footage and oral histories

- For a game clip, match the opponent, season and tournament round against the game book. Check the score and clock in the actual excerpt. One program can play the same opponent several times in a season. Label footage from a later season when it first appears.
- When a player remembers what happened in a huddle, attribute the account to that player. If participants remember the exact words differently, paraphrase the point they agree on or quote one identified account.
- A dedication can shape which moment closes the film. Look for a concrete link between a game and the person’s life beyond it. Verify the object, place or people shown in the closing shot.

## Philosophical texts and their illustrations

Read the passage in context. Record the author, the character making the claim, the edition or translator, and a location readers can find across editions. A king in a literary dialogue, a judge in a hypothetical case and the philosopher who wrote the case each have a different role. Preserve the conditions that make the example work. Foot gives the decision to a driver and pairs it with a judge facing five hostages. Changing the driver to a bystander or dropping the judge changes the question the chapter answers.

Identify the particular object on screen. A dated handscroll can document how a later artist read a dialogue. A photograph of an inscription establishes the survival of the stone. Tie a specific sentence to that stone only if a catalog or editor identifies the fragment. When editions differ, quote the one on screen, credit the translator for a reading and carry any uncertainty in reconstructed words into the fact notes.

Design the invitation and reveal as two separate beats. For the duck-rabbit, keep the original orientation in both formats, crop the printed answer for the opening and leave time to see the other animal. Check the first frame, thumbnail and captions for an accidental early reveal.

## First-person accounts and broadcast calls

- When the story follows an informal hiring block, date the worker’s eligibility, each employer’s documented action and the participant’s account of private conversations. A survey of employers can establish how much interest respondents expressed at that moment. A claim of coordination needs a source who could know what was communicated between the decision-makers.
- When one person credits another with teaching them, recover the learner’s own description of what they asked and tried. Keep that testimony attached to its date and event. A later promotion, contract or winning performance can show where the learner went next. To say the lesson caused the result, find evidence for that additional step.
- For an anecdote in a coauthored memoir, identify who narrates the chapter and who could hear or see the event. Read the surrounding page in the publisher’s edition. Log the edition, printed page and PDF page, and save the exact excerpt used on screen. If a writer reconstructs one side of a phone call, attribute the recollection to that writer and paraphrase the other person’s part only when the text supports it.
- Start with family members’ own published interviews. Give the person whose life is at issue room to speak. A resident explaining a routine on camera can show what an ordinary day there looks like. Identify a model apartment, a later practice, a family photograph or an actor’s reenactment according to what the picture shows.
- Match a repeat event such as a charity home furnishing to its date, participants and original report. Check who purchased or built the home, who provided its contents and which detail the homeowner actually shared. Preserve the homeowner’s own actions in the script.
- Check a claimed first or turning point against a dated, contemporary account. An interview about making art at a milestone birthday may describe a craft the person already practiced. When someone describes plans for an upcoming ceremony, attribute that intention and find a dated photograph or account before saying what happened there.
- For a sports call, identify the game, original TV or radio outlet and individual commentator from the source program or credits. League libraries can package a play with a different network’s call, later interviews or added narration. Listen to the exact excerpt and compare its score, clock and visible play. An interview sound bite gets the same check for speaker, first and last words, and the matching source picture.
- When a broadcast word is uncertain, compare the full exchange, the cut audio and the station’s embedded caption track. Live roll-up captions can arrive several seconds late and simplify repetitions. Mark an uncertain word in the notes or select a different complete sentence that expresses what the speaker meant.

## 6. Privacy and fairness (publish gate)
- In true-crime cases, show the victim (news clips, public missing/cold-case poster). No standalone family snapshots, funeral/memorial footage, weapons, journal text, or remains details.
- Crop: license plates, house numbers, channel names on FBI pages, private individuals' names in documents unless already public in coverage.
- For allegations of wrongdoing, give the affected party’s material response and the status of the allegation. In a true-crime case, address the innocent explanation and avoid stating an uncharged crime as fact.
