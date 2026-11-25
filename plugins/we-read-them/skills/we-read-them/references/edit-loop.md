# Turn a scorecard finding into a verified edit

Run this loop during an authorized edit or production. “Run the edit loop on this rank” is enough to start from the existing scorecard and cut. For a request scoped to scoring, return the priority finding and proposed test. For an excerpt trial, deliver the compared excerpts and decision. For an episode revision, carry a winning change into the actual edit and verify the affected deliverables.

## 1. Choose the viewer problem

Read the current `film/BENCHMARK.md` and the latest script or cut it identifies. Inspect the actual cue. Start with a factual mistake, a failed newcomer retelling, or a missing opening payoff. Next choose the change likely to help the most viewers understand the episode. A peer’s higher score is a reason to inspect a moment. The editor needs to identify what someone actually misses.

Record the stage, baseline file or revision, timestamp, scorecard row and observed problem. If an approved script revision already fixes a line, test that script at its own stage. Existing audio and a newly reviewed script are different baselines.

If the complaint is “I understood the facts but lost the point,” play the opening, the middle discovery and the conclusion in order. Locate the first place the viewer has to supply the connection themselves. Did the opening give them a recognizable situation? Did a middle scene show what a choice cost or changed? Did the ending give them something to take back to that situation? Repair that cue. A repeated slogan at each rank gives the editor ten copies of the same problem. A three-excerpt preview can isolate a missing idea. When the complaint concerns pacing or transitions, include the joins or watch the full cut. A request about one specific shot can go directly to that shot.

## 2. Set the test before changing the edit

Write **one editor-only success check** and **one neutral viewer question**. For a source comparison the check might be “the viewer identifies which record supplies each number.” The question might be “Where did each number come from?” Give the viewer room to say they could not tell.

Pick the smallest change that could resolve the problem and the cheapest artifact that can test it honestly. Compare wording on a frozen script, a crop in decoded portrait frames, a reveal in a timed clip, and a pause with audible lead-in and tail. Keep factors unrelated to the finding comparable. Include the neighboring cue when a transition is the problem. Record which variables intentionally change.

For an opening-picture test, stop at the first complete thought before a later line names the subject. That isolates what the opening lets a viewer infer. Check that a spoken reference such as “these two” still points to something visible. Check the ending, too. If the closing line depends on seeing a name or result for the first time, introduce the puzzle without giving that reveal away.

The pre-recording script panel still reviews a meaningful change to a claim, story order or first-use explanation. Follow the producer’s current recording or publication decision. A visual test can use a previously approved performance.

## 3. Make a candidate and compare it blind

Preserve the current working source and baseline export. Edit a separate version of the relevant shot, line or sound cue and render the intended viewing size. For a screen demonstration or diagram, credit the observed data and label any authored reconstruction. Use the same time span, aspect ratio, playback rate and audio on a picture-only trial when the timing is part of the control.

Use the bundled helper for neutral file labels and a resumable record. Choose a new directory per distinct attempt. The editor keeps the expected answer and baseline mapping in `edit.json`. Only share audience-facing material from `review/` with the reader. The filenames do not conceal identifying titles visibly burned into the media, so check the exports first.

```sh
python3 scripts/edit_trial.py prepare film/edit-trials/source-line-01 \
  baseline.mp4 candidate.mp4 \
  --question "Where did each number come from?" \
  --check "The viewer can name the source of each number and point to its line."
```

Give each reader the target audience. Keep the editor’s expected answer, edit history, prior notes and scores private. Alternate which version comes first or use fresh readers for each first exposure. Preserve each first response separately from any later comparison. Use the existing two-family panel for script edits.

### Test what survives one viewing

For a finished video cue, start with ordinary playback on the intended screen. Let the viewer watch before they see a question that could direct their attention. Ask what happened in their own words first. When the same viewer assesses both cuts, save each retelling before showing the trial question. Only their first clip is a cold exposure to the idea. For an explanation, design the question to test the relationship the viewer learned. For a profile, ask which choice changed their impression of the person and why. For a whole countdown, ask what they expected at the opening, what changed their mind in the middle and what the ending settled. If testing why the film matters to them, a neutral follow-up is “What, if anything, would you take from this, and which moment gave you that idea?” Keep that answer separate from the first retelling.

When a viewer is available, generate local browser pages from a prepared video trial:

```sh
python3 scripts/edit_trial.py playback film/edit-trials/source-line-01
```

Open `review/watch-A-first.html` for one viewer and `review/watch-B-first.html` for the next. Each page uses the two media files beside it and lets the viewer save their responses locally. Record subject familiarity and prior exposure to the material. A producer who knows the expected answer can spot an editing defect. A fresh viewer can also tell you what the film taught them unaided.

For a portable viewer packet, zip both neutral videos and the two HTML pages together. Unzip them into one folder before opening a page in a browser. Keep the editor’s notes, mapping and prewritten prompt out of this packet.

In the scorecard, record **understood unaided**, **understood after a prompt or replay**, **missed**, or **unmeasured** for the particular takeaway. Quote the answer or point to the missing connection. Record the playback conditions and whether the reader was human or a model. A preview playing successfully proves it can play. Frame samples can settle a crop, label or position. Actual first-view answers establish what those particular viewers understood. Keep editing with the evidence available and leave audience comprehension open when it has yet to be tested.

When answers come back, match the trial identifier and first-clip label to the packet. Grade the unaided retelling against the private criterion before reading preference or prompted answers. Report how many first-time viewers made the connection out of how many saw that cut first. Preserve the actual misconception even if the viewer liked the edit.

## 4. Make the editorial decision

Check the viewer’s answer against the specified task. Compare the affected row on the same 1–5 scale, against the same reference cue and at the same stage. Explain any difference with a line, frame or timestamp. Check factual meaning, affected captions and source visibility. Listen for a compromised word or join when the sound or timing has changed. Record the evidence and any disagreement in the existing scorecard.

After the first-view retellings, ask each reviewer what the other cut made easier to see or hear. A simpler graphic may reveal a sequence while hiding a close alternative or a source qualifier. If that missing detail changes the claim, revise the edit. Otherwise record the tradeoff with the decision.

Use the retelling to choose the next change. If the viewer has the sequence right but thinks the winning option was a certainty, test a visible runner-up. If they miss a reveal because the narration and picture draw attention at different times, test the timing while holding the content fixed. When two changes travel together, the result applies to that combination. Stop polishing a passage once the intended idea and any essential qualification come through.

| Evidence | Decision and next step |
| --- | --- |
| The candidate solves the viewer problem and passes the affected checks | Select its neutral label. Keep the exact source revision and the checked artifact. |
| The baseline works better or the two versions perform equally | Select the baseline’s label or record `tie`. Keep the baseline and close this attempt. |
| Neither version solves a consequential problem, and the review reveals a concrete new repair | Record `revise`. Keep the baseline as the working copy. Open a new attempt with the new hypothesis. |
| Evidence, authorization or a necessary input is missing | Record `blocked` with the missing condition. Report the open issue at its actual stage. |

```sh
python3 scripts/edit_trial.py decide film/edit-trials/source-line-01 \
  --choice B --review editorial-review.md \
  --reason "The viewer associated both numbers with the correct records at their first appearance."
```

Use the label supported by the actual review. The helper resolves it to baseline or candidate and saves the supplied evidence. A score can stay the same while a specific mistake disappears. Record that repair. Likewise, a higher score cannot excuse a false claim or an unreadable source.

## 5. Carry the result through the requested scope

For a sample, label the winner as the **selected excerpt**. For a full-production edit, apply the winning change to the case’s canonical source, render the affected portrait and widescreen chapters, and rebuild dependent masters, captions, chapter times, share copies and archives where applicable. Review the changed cue in those actual exports, including the display size for each layout and both sides of an affected join. Recheck the visual-mix log when picture categories or timings changed. Preserve the last verified delivery until the replacement passes. If the full render loses the improvement or introduces a new defect, restore the verified version and reopen the specific issue.

Return to the open scorecard findings. Stop when the consequential issues in the requested scope are resolved. If another pass would only chase a point or repeat an unsuccessful idea, close the attempt and name any remaining limitation. A remaining factual or comprehension failure stays open even if no candidate is ready. On restart, read the trial record and inspect the staged hashes before resuming. An excerpt selection, a promoted edit and a verified episode delivery are separate outcomes.

When new viewer evidence arrives after a decision, append it to the scorecard with the exact cut reviewed. If it exposes a misunderstanding that changes the decision, open a new attempt and test that specific repair. After release, use the relevant timestamps to inspect first-30-second retention and local dips or spikes. A replay can signal either interest or confusion. Use the viewer’s explanation to choose what to investigate. [YouTube’s retention guide](https://support.google.com/youtube/answer/9314415?hl=en)
