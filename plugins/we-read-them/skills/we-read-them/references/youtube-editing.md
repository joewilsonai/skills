# Editing a We Read Them film for YouTube

Use the treatment to plan what a viewer will see, hear and learn. A sourced story gives the editor more choices than a stack of fact cards.

## Build the story across all ten

Draft the [countdown treatment](../templates/countdown-treatment.md) before recording. Choose a question small enough that the final chapter has evidence to answer it. An investigation might follow how a decision was made. A tribute might ask what someone did when winning cost them something. A process story might follow what happens to one object as responsibility for it changes hands. Let the records suggest the structure.

Read the ten discoveries in order without saying their numbers. At each join, ask what the viewer now wants to know. One chapter might establish the public result, the next reveal the choice that produced it, and the next let the person who lived with that choice explain the cost. A new witness can also challenge the previous account. Identify that disagreement explicitly. A chronological neighbor or a similar-looking image alone establishes no causal link.

Try moving a middle entry. If the surrounding chapters express the same idea either way, give the entry a distinct job, place it where it answers a live question, or reconsider the selection. Preserve a documented ranking and any order Joe has chosen. When that order is fixed, connect the ideas in the writing and shot choices. A Short’s opening names the person, place or object so a viewer can enter there. In the film, the preceding shot or thought gives that same opening a second purpose.

## Find the opening before recording

Write the episode’s promise in one sentence. Pick the first image and the first line together. Give the viewer a person, an action and a reason to stay. Name the subject early enough that someone arriving from the thumbnail knows they have the right film. Pay off one part of the promise in the opening, then leave the larger question to the countdown. Branding can ride on that first shot.

Script the moment after the hook. If the first shot is a photo finish, give viewers a moment to pick the winner. The next image could reveal the official time or a second camera angle. That changes what they know and gives the narrator a reason to continue. A reveal in the first chapter can also work when the intro establishes exactly what the viewer is waiting to see. Trim repeated setup where the intro meets number ten.

For a Warner tribute, start on the real photograph of him holding the Lombardi Trophy. “We’re looking at Kurt Warner’s choices on and off the field to see who he made time for when it counted. In his memoir, he remembers asking his agent to wait the night he won the Super Bowl. He wanted to call his kids.” Move to the actual memoir page as the narrator identifies whose account it is. Save Zack’s answer for the chapter if the opening has already delivered another concrete detail. The photograph establishes the win. The memoir establishes the call. [The Warners’ memoir, printed pages 3–4](https://files.tyndale.com/thpdata/firstChapters/978-1-4143-3406-6.pdf)

## Cut each chapter around a change

In the existing treatment or shot list, mark the setup, the instant something changes, and the image or voice that earns the payoff. Give each cut a job. The same shot can carry several sentences when the action unfolds continuously.

| What the viewer needs | Picture and sound |
| --- | --- |
| See a play, a reaction or a process | Let the source occupy the useful width of the frame. Start early enough to establish the action and stay through its consequence. Keep a subject, ball or significant gesture visible in the portrait crop. Use a fitted wide inset when the geography would disappear in a tight crop. |
| Read a consequential line | Establish who wrote it and where it appears. Then enlarge the original passage, preserve surrounding qualifiers and hold it through an unhurried read. When the male narrator reads the passage, label it “read from the record.” For original audio, identify the recorded speaker. |
| Understand a comparison or a mechanism | Put the items on the same scale or diagram the movement the source supports. Keep units, dates and attribution close to the evidence. Reveal each step when the voice reaches it. |
| Hear a person settle the question | Identify the speaker and make room for the original sentence. Carry genuine room tone into or out of that same scene when it smooths the edit. Hold a beat on the speaker or the real consequence before the narrator resumes. |

Let the label, number and type carry the series identity. Bring the claim card back when there is a claim to test. Keep original color where jersey, document or object details depend on it. For a grayscale case treatment, test that those details still read. A slow move on a still should reveal a person or detail the viewer was looking for. An actual archival shot already has its own camera movement. A practice photograph can introduce a coach and a later interview can identify a witness. Date them on screen. For a youth game without showable footage, use a sourced route diagram for the play and a separately credited adult interview or coach photograph.

## Use the AI Builders Club broadcast identity

Use the Club’s live-show graphics as the visual reference for the series. They share their headline and label families with the Club’s field guide, which also supplies its body type. Apply these roles to the intro, each rank, diagrams, subtitles, chaptered film, Shorts and thumbnails. Give archive footage, photographs and original documents their source colors and typography. Label an editorial recreation so the viewer can tell who designed it.

When the Club refreshes its identity, check `work/ai-builders-club/studio/src/base.css` and `work/ai-builders-club/banner/field-guide.html` in the operations workspace. The related ink-and-paper contrast colors come from `app/globals.css` in the Club’s public-site project. Update the shared manifest and inspect a representative export before adopting new values.

| Role | Club treatment |
| --- | --- |
| Background and main text | Ink `#141312` and cream `#EFE6D2`. Put caption text on a background that stays readable as the picture moves. |
| Secondary information | Muted cream `#B8AD96` for readable attribution. Use rule `#2B2824` where dividing two areas helps the eye. |
| Accent | Stamp red `#C4302B` for an occasional rank mark, pointer or other emphasis. Keep essential small wording in cream or muted cream. Give a chart an identifying label or line pattern as well as color. |
| Titles and decisive numbers | Archivo Black, regular (400). Use it for the few words that deserve emphasis. |
| Short editorial labels | Special Elite, regular (400). Use Inter for long credits or a name that needs a glyph the label face lacks. |
| Captions and explanation | Inter, regular (400) or semibold (600). Use the same caption role in both aspect ratios. |

Use the [shared brand manifest](../templates/aibc-brand/brand.json) for browser, custom video and thumbnail renderers. Copy the entire `aibc-brand/` folder beside `source-edit.js` in each new project, including its licensed fonts. For a custom renderer, load the listed font files and weights before measuring lines. Inspect a rendered title, an accented name and a caption in both aspect ratios, plus the thumbnail at feed size. Check a plain background against the specified color in a pre-encode frame and inspect the compressed output for contrast, clipping and letterforms. A topic can supply a new photograph, diagram or map while the viewer still recognizes the Club.

## Give the viewer one place to look

Name what the viewer should notice on this beat. It might be the front foot landing, a witness’s expression, a word in a memo, or the gap between two bars. Build the frame around that detail. Show the rank when entering its chapter. Let the narrator introduce the idea and the captions carry the spoken words. A sidebar repeating the same sentence adds another place to read.

Give interviews and demonstrations the useful width of the frame. A brief name and role can establish a new speaker. Keep attribution near a disputed claim and a denominator near a survey result. Move extended source details to the credits. When a source carries its own captions, check them alongside the episode captions. Choose a clean source or a framing that preserves the speaker, gesture and evidentiary details. If both captions must stay, make clear which belongs to the source.

A comparison earns two items on screen together when the viewer needs to see their difference. Introduce each at its spoken cue, then hold the completed comparison long enough to read. Give a document the screen when its wording matters. The next beat can return to the person or action.

In the edit review, play a footage shot and the densest graphic beat once at phone width with captions on. Ask the reviewer what they looked at first and what they learned by the cut. If reading a side panel made them miss the action, remove the repeated copy or put the evidence in the following shot. Recheck the same cue for speaker identity, source attribution and qualifications after simplifying it.

## Use the scene templates

Copy [source-edit.js](../templates/source-edit.js) beside each `index.html` and set `window.WRT_SOURCE_EDIT` in a script tag before the page’s main script. The [portrait footage page](../templates/reel-page-footage.html), [document page](../templates/reel-page.html), [intro page](../templates/intro-page.html) and [widescreen page](../templates/reel-page-wide.html) accept the same edit and approved `takes.json`. Paths are relative to the page. For new countdowns, set `presentation: "quiet"`. It shows a brief rank at chapter entry and keeps source credit, captions and comparison details visible when they apply.

For a clock-tower scene, give the viewer the outside dial to inspect. Let the spoken word “four” point them to the four strokes on this particular clock. Then move inside for the last shot, where the photographer found a person working behind the clock face. Carol M. Highsmith photographed both views at the Old Post Office in Washington, D.C. [Clock face](https://www.loc.gov/item/2013634622/) · [Repair inside the tower](https://www.loc.gov/item/2011635878/)

```html
<script>
window.WRT_SOURCE_EDIT = {
  rank: 1, slug: "clock-tower", title: "Behind the clock face",
  presentation: "quiet", endCard: "source",
  assets: {
    dial: { image: "assets/clock-face.jpg" },
    inside: { image: "assets/clock-repair.jpg" }
  },
  scenes: [
    { at: 0, layout: "immersive", asset: "dial", fit: "cover",
      portrait: { fit: "contain" }, credit: "Carol M. Highsmith · Library of Congress" },
    { at: { take: 1 }, layout: "reveal", asset: "dial",
      credit: "Carol M. Highsmith · Library of Congress",
      detail: { at: { take: 1, word: "four", occurrence: 2 },
                crop: [.635, .405, .32, .291] },
      portrait: { detail: { crop: [.658, .423, .284, .279] } } },
    { at: { take: 2 }, layout: "immersive", asset: "inside",
      fit: "contain", portrait: { fit: "cover", crop: [.508, 0, .39, 1], focus: [.68, .45] },
      credit: "Carol M. Highsmith · Library of Congress" }
  ]
};
</script>
```

An immersive shot gives the picture the screen and carries its source credit and timed captions. `contain` keeps the whole selected area clear of those overlays. `cover` fills the frame. Check the right edge and lower controls on a phone before choosing that crop. A `reveal` first shows the context, outlines the selected pixels on the spoken cue, then enlarges those same pixels beside the context in widescreen or below it in portrait. Use an optional `detail.mark: [x,y,width,height]` for the precise passage to underline in a document. All crop, mark and focus coordinates are fractions of the original source. Choose a detail crop that retains dates, units, nearby qualifiers or relevant action. A cue can use seconds or a zero-based take with an optional word, one-based occurrence and offset in seconds. For speech with no word timings, use a verified time in seconds.

When the spoken and printed word counts differ, add `display_words` to the affected take in `takes.json`. Give each printed token, including punctuation, its first spoken onset and its last spoken end in seconds from the start of the chapter mix. Match tokens in order against the approved speech and verify each expansion against the audio. In the LLM opening, “Chat G P T” spans 10.469–11.334. The next sentence starts with “A” at 11.786. The corresponding entries are `["ChatGPT.", 10.469, 11.334]` and `["A", 11.786, 11.873]`. Include an entry for every printed token in that take. After export, check the start of the caption containing the acronym and the first caption after it. Older takes without this field retain their previous caption timing.

A `compare` scene accepts a `heading` and optional `note`. A frame sequence uses `{ dir: "assets/play", frames: 90, fps: 30 }` and starts at `001.jpg`. Set `speaker` for an original recording, or `reader` for a spoken document. Align the shot to its [original audio onset](voice-mix-render.md#matching-original-speech-to-its-picture).

For a full release, `endCard: "source"` holds the last picture and its credit through the ending. With the quiet presentation, the final image holds with its source credit. The original immersive presentation also carries a small series signature. Write `window.WRT_CHAPTER_META` to `wide/meta.json` for the normal stitch. For a custom mix, set `audioEnd` to its measured duration in seconds. The default is `takes.dur + .8`. Omitting `endCard` retains the original series slate. Use `endCard: false` to end a standalone excerpt at the approved audio tail.

## Make the master flow and the Shorts stand alone

A Short can begin mid-action if its first image and line establish the person and stakes. End on the result. Budget the final frame for the payoff before any invitation to watch more. Frame a face, quote and caption together on a phone. Allow space for the player’s right-side controls and bottom metadata according to the actual preview.

In the long-form cut, group adjacent chapters by a question or relationship. Use the outgoing image or sound to set up the idea in the next chapter. A call home after a championship can lead into the first time father and son met. Keep the shared approved spoken cues and chapter timing. Carry the visual transition across the existing chapter boundary, and let the stitcher remove intermediate Shorts end cards. For the finale, stay on the person or evidence that answers the opening question.

## Write the conclusion alongside the opening

Number one carries two responsibilities. Resolve its own story for a viewer arriving through the Short. Then put that specific outcome in the context of the question the full film opened with. Give the last word to the person who experienced the consequence when you have a suitable recording. A dated result, a choice captured on film or a return to an object seen in the opening can carry the same weight. For an unresolved case, name the finding the record does support and the precise question that survives it.

Write the final line over the final shot. Try reading it over an unrelated episode’s ending. If it fits equally well there, replace it with a detail only this story could earn. Let the audience hear the end of the sentence and see the result at normal speed. Place any branding, credits or invitation after that beat, or keep a quiet source credit on the closing image. When the witness or the image already supplies the answer, let it finish the film.

## Review the edit as a viewer

When the narrator asks viewers to watch a movement, play the exported shot from the cue through the result in both formats. Can you point to the moving part and see where it ends? A shoe can leave a portrait crop just before it lands. Fit the wider source into the frame or change the shot, then replay the same cue in the repaired export.

Follow each on-screen name through the cuts inside the source footage. If the camera cuts from a pitcher to the batter, someone seeing the game for the first time may read the pitcher’s name as the batter’s. End the name card at the cut, identify the new person, or hold a verified shot of the person named.

Check accented names in the typeface that draws each caption, title and source credit. Collect the actual strings for each role, apply the renderer’s casing, and check their Unicode characters against that font’s character map. For example, the font that draws Nāgasena also needs Ā if the design uppercases the name. Choose a legible companion that includes any missing characters. Inspect the accented words in an encoded phone-size frame. A clean transcript or a pixel comparison with the same faulty font can miss squares in the picture.

Play the complete master at normal speed with the treatment closed. Write down the question you carried out of the intro, the moment a middle chapter changed your expectation, and the detail that answered the question at the end. For an unresolved story, write what you know now and what still lacks evidence. Replay any stretch that felt like starting the film over. Check whether a new witness, action, object or sentence would make the next chapter feel necessary.

Play a middle Short on its own, then between its neighbors in the film. Check that someone can identify the subject and get a complete payoff in the Short. Watch the decisive shot at phone size with sound off. Also view the widescreen share copy at about 400 pixels wide, as it appears on an upright phone. Put a rank needed to follow the countdown and any qualifier needed to interpret a number beside the headline or figure in clearly readable type. Reserve small mastheads and footers for secondary information. Then listen to the opening and ending with the screen out of view. The picture should show the discovery and the words should make its significance clear. Repair a missing step in the story before polishing transitions or music.

Use the [sound and mix guide](voice-mix-render.md) for the dialogue and score, the [landscape guide](landscape-longform.md) for implementation, and the [YouTube publishing guide](youtube-publishing.md) for title and thumbnail pairs and interpreting actual viewer retention.
