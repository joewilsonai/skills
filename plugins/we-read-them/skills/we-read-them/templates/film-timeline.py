#!/usr/bin/env python3
"""Timeline for "What the record says: Gabby Petito" -> film.json (sections, voice starts, clips, subtitles).
Voice durations come from audio/vo/dur.json; subtitle cues are cut at sentence ends using audio/vo/words.json."""
import json, os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = json.load(open(f'{D}/audio/vo/dur.json'))
OLD = json.load(open(f'{D}/audio/vo-kokoro/dur.json'))  # durations the picture was first timed to
WORDS = json.load(open(f'{D}/audio/vo/words.json'))
LINES = {l['id']: l for l in json.load(open(f'{D}/audio/lines.json'))}

# sections: id -> [start, end]
SEC = {
 'cold': [0, 7.0], 'title': [7.0, 16.0], 's10': [16.0, 30.0], 's9': [30.0, 42.5], 's8': [42.5, 54.0],
 's7': [54.0, 63.0], 's6': [63.0, 74.5], 's5': [74.5, 88.5], 's4': [88.5, 109.0], 's3': [109.0, 122.5],
 's2': [122.5, 143.5], 's1': [143.5, 165.5], 'end': [165.5, 175.0]}
VO = {'v0': 3.0, 'v1': 7.4, 'v2': 16.4, 'v3': 30.4, 'v4': 42.9, 'v5': 54.4, 'v6': 63.4, 'v7': 74.9, 'v8': 85.9,
      'v9': 88.9, 'v10': 98.8, 'v11': 109.4, 'v12': 122.9, 'v13': 131.4, 'v14': 143.9}
# original-sound clips: name -> [film start, duration, subtitle]
CLIPS = {
 'van':    [43.4, 7.0, None],
 'chief':  [77.8, 2.0, '[Police chief] "All I\'m gonna say is I know where Brian\'s at."'],
 'taylor': [80.1, 5.5, '[Police] "We thought that we\'d seen Brian come back into that home."'],
 'moab':   [126.5, 4.5, '[Bodycam] "We got a call about a male hitting a female..."'],
 'father': [157.4, 7.4, '[Joseph Petito] "...it\'s not just Gabby that deserves that."'],
}
# ── Time warp: the picture is drawn on the original clock ("old"); each narration stretch grows to the new voice,
# footage clips keep real speed, gaps keep their length. film.json carries the map so the page and the mix share it.
ANCH = sorted(set([b for v in SEC.values() for b in v] + [t for k, t in VO.items()] + [t + OLD[k] for k, t in VO.items()]
                  + [c[0] for c in CLIPS.values()] + [c[0] + c[1] for c in CLIPS.values()]))
def scale(a, b):
    for k, t in VO.items():
        if a >= t - 1e-6 and b <= t + OLD[k] + 1e-6: return DUR[k] / OLD[k]
    return 1.0
WARP = [[0.0, 0.0]]
for a, b in zip(ANCH, ANCH[1:]): WARP.append([round(WARP[-1][0] + (b - a) * scale(a, b), 4), b])
def new(t):
    for (n0, o0), (n1, o1) in zip(WARP, WARP[1:]):
        if o0 <= t <= o1: return n0 + (t - o0) * (n1 - n0) / (o1 - o0)
    return WARP[-1][0] + t - WARP[-1][1]
# ── The opening (animated open, setup over the route map, tease), placed before everything above ──
OPEN = 5.2
I = {'i1': OPEN + .2}; I['i2'] = round(I['i1'] + DUR['i1'] + .5, 3); INTRO = round(I['i2'] + DUR['i2'] + .9, 3)
def wordat(vid, w, nth=0):
    hits = [x for x in WORDS[vid] if x[0].strip('.,:').lower() == w.lower()]
    return round(I[vid] + max(0, hits[nth][1]), 3)
INTRO_EV = {'home': wordat('i1', 'home'), 'watching': wordat('i1', 'watching'), 'file': wordat('i2', 'file'),
            'box': wordat('i2', 'box'), 'father': wordat('i2', 'father'), 'fbi': wordat('i2', 'FBI')}
VO_OLD = dict(VO); VO = {k: round(new(t) + INTRO, 3) for k, t in VO.items()}
VO.update(I)
MAXC = 74  # characters per subtitle line (one line, ~30 px sans)

def fix(t):
    for a, b in [('Laundry', 'Laundrie'), ('Northport', 'North Port'), ('a thousand', '1,000'), ('Item number 30.', 'Item 30.'), ('Northport', 'North Port'), ('3 a.m. September 1, $14.10.', '3 a.m., September 1st. $14.10.'), ('August 29,', 'August 29th,')]:
        t = t.replace(a, b)
    return t

def cues_for(vid):
    """Split one voice line into cues at sentence ends (and at commas when too long), timed by its words."""
    t0 = VO[vid]; words = WORDS[vid]; text = fix(LINES[vid]['asr'])
    toks = text.split(); out = []; cur = []; i = 0
    # walk display tokens alongside ASR words (same count is not guaranteed: fall back to proportional timing)
    n, m = len(toks), len(words)
    def wt(k):  # time of display token k
        j = min(m - 1, round(k * (m - 1) / max(1, n - 1)))
        return words[j]
    start = 0
    for k, tk in enumerate(toks):
        cur.append(tk)
        s = ' '.join(cur)
        end_sent = re.search(r'[.?!]$', tk) and not re.fullmatch(r'\d+\.', tk)
        nxt = ' '.join(cur + toks[k + 1:k + 2])
        rest = ' '.join(toks[k + 1:])
        if k < n - 1 and len(rest) < 24 and len(s) + 1 + len(rest) <= 96: continue  # absorb a short tail
        if end_sent and len(s) > 40 or len(nxt) > MAXC or k == n - 1:
            a = t0 + max(0, wt(start)[1]); b = t0 + wt(k)[2]
            out.append([round(a, 2), round(b, 2), s]); cur = []; start = k + 1
    # merge a tiny trailing number cue ("10.") into the next
    res = []
    for c in out:
        if res and re.fullmatch(r'\d+\.', res[-1][2]): c = [res[-1][0], c[1], res[-1][2] + ' ' + c[2]]; res[-1] = c
        else: res.append(c)
    return res

subs = []
for v in VO: subs += cues_for(v)  # includes the opening lines
for k, (t, d, s) in CLIPS.items():
    if s: subs.append([round(new(t) + INTRO, 2), round(new(t) + INTRO + d, 2), s])
subs.sort()
# hold every cue >= max(1.8 s, its own length + 0.6 s), never past the next cue
for i, c in enumerate(subs):
    need = max(1.8, c[1] - c[0] + 0.6)
    nxt = subs[i + 1][0] - 0.05 if i + 1 < len(subs) else 999
    c[1] = round(min(max(c[1] + 0.4, c[0] + need), nxt), 2)
film = {'intro': INTRO, 'intro_ev': INTRO_EV, 'dur': round(new(SEC['end'][1]) + INTRO, 3), 'sections': SEC, 'vo': {k: [v, DUR[k]] for k, v in VO.items()}, 'clips': {k: v[:2] for k, v in CLIPS.items()},
        'clips_new': {k: [round(new(v[0]) + INTRO, 3), v[1]] for k, v in CLIPS.items()}, 'warp': WARP, 'subs': subs}
json.dump(film, open(f'{D}/film.json', 'w'), indent=1)
long = [s for s in subs if len(s[2]) > 100]
print(len(subs), 'cues; dur', film['dur'], '; overlong:', len(long))
for a, b, s in subs: print(f'{a:6.2f}-{b:6.2f} {b-a:4.1f}s  {s}')
