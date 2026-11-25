# Make a cover a viewer can understand at a glance

Start from the final cut. Choose the question in the opening, the most revealing piece of evidence in the middle and the payoff at the end. For each, write down the time, what the film can establish, and one reason a viewer might click. These are three ways into the episode. If changing the picture would leave the same promise three times, choose a different moment.

## Design the title and cover together

Sketch one focal point per cover. A portrait can invite a question about a person. One figure with its denominator can make a decision concrete. A simple diagram can put the viewer inside a game, experiment or process. Let the title name the subject and supply whatever the image cannot tell a stranger. Put the important words near the front so they survive a narrow feed. Write the handful of words the composition needs, and also try the picture alone.

1. **Check the picture’s origin.** Record the depicted person, date, photographer or creator, source URL, and permission for public thumbnail use. For an open license, keep its URL and the required credit. Describe a crop, added typography or other changes in the publication description when the license calls for it. An earlier uniform, a later portrait or an illustration can identify a subject. Check whether the combination with the words puts them at a particular incident. Build an original diagram from sourced facts when an appropriate picture has no usable publication rights.
2. **Compose with the shared Club kit.** Keep space around the decisive face, hand, object or figure. Use the studio ink and cream, reserve stamp red for the detail the eye should notice, and load the actual Archivo Black face for headline text. Bring in Inter for an essential qualifier. A club mark needs enough room to read. On an already strong portrait, the type and color can carry the identity. [Brand manifest and fonts](../templates/aibc-brand/brand.json)
3. **Export a clean master for each idea.** Use a 16:9 RGB JPEG or PNG for long-form. YouTube recommends 3840 × 2160. Start from the original photograph or artwork, check its effective resolution in the crop and verify the file size against the intended upload surface. A simulated player badge belongs only in the review proof. [YouTube thumbnail specifications](https://support.google.com/youtube/answer/72431) · [YouTube API thumbnail upload](https://developers.google.com/youtube/v3/docs/thumbnails/set)

## Test the actual exports

Run the proof maker with the video’s actual duration and its proposed titles. Use the production Python environment with Pillow installed. It writes an artwork-only contact sheet and a second sheet with the titles. Both show 168- and 320-pixel feed mockups with a duration badge in the lower-right corner. These are editorial test sizes. YouTube surfaces vary.

```sh
python3 scripts/thumbnail_proof.py --duration 8:25 --out-dir release/thumbnail-review \
  --pair release/A.jpg "First proposed title" \
  --pair release/B.jpg "Second proposed title" \
  --pair release/C.jpg "Third proposed title"
```

Give an independent reviewer the artwork-only sheet first. Ask what they saw first and what story they expect to watch. Save the answer, then reveal the titles. Ask which pair they would open for this audience, which words or subjects are hard to read, and what claim they think the film will establish. Match that answer to the opening and the exact payoff cue. A question can still imply wrongdoing when its picture points at an identifiable person or institution. Replace an ambiguous image, repair a missing denominator, or simplify copy and repeat the check on the revised JPEG.

Choose the pair whose unaided reading and paired title best fit the whole film. Have the production agent save its filename, title, publication credit, the two alternatives, and the selection reasoning. Verify the applied image and title on the actual upload. When Studio offers A/B testing, compare genuinely different pairs from the same cut. Record the platform’s watch-time outcome and impression context. An editorial selection or an inconclusive test supplies no measured click lift. [YouTube title and thumbnail guidance](https://support.google.com/youtube/answer/12340300) · [YouTube Studio A/B tests](https://support.google.com/youtube/answer/16391400)
