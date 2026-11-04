#!/usr/bin/env python3
"""One-take narration for a reel (the playbook's voice step).
<reel>/one/config.json: {"tempo": 1.12, "extra": {"TikTok.": .9, ...}, "segments": [[start word, display text], ...]}
<reel>/one/script.txt: the whole narration with v3 tags ([somber], [quietly], [pause]).
Steps: voice once on eleven_v3 (unless one/take.wav exists and --revoice is not given) -> pitch-preserving tempo ->
stretch the named gaps with the gap's own room sound -> Whisper word timings -> <reel>/voice.wav, voice.mp3, takes.json."""
import json, os, subprocess, sys, urllib.request
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
R = sys.argv[1]; O = os.path.join(R, 'one'); C = json.load(open(os.path.join(O, 'config.json'))); SR = 44100
# script.txt: narration blocks; a line starting "R:" is a block Harper reads from the record (her own take, a deliberate voice change)
BLOCKS = []
for line in open(os.path.join(O, 'script.txt')).read().strip().split('\n'):
    who = 'R' if line.startswith('R:') else 'C' if line.startswith('C:') else 'N'; text = line[2:].strip() if who in ('R', 'C') else line.strip()
    if not text: continue
    if BLOCKS and BLOCKS[-1][0] == who: BLOCKS[-1][1] += ' ' + text
    else: BLOCKS.append([who, text])
def _find_pd():
    for d in (R, os.path.dirname(R), os.path.dirname(os.path.dirname(R)), os.path.dirname(os.path.dirname(os.path.dirname(R)))):
        p = os.path.join(d, 'pron-dict.json')
        if os.path.exists(p): return p
    sys.exit('pron-dict.json not found above ' + R + ' (create the case dictionary first)')
pd = json.load(open(_find_pd())); PRON = [{'pronunciation_dictionary_id': pd['id'], 'version_id': pd['version_id']}]
VOICE = {'N': ('TVtDNgumMv4lb9zzFzA2', 'eleven_v3', {'stability': .5, 'similarity_boost': .8, 'speed': 1.1}),
         'R': ('Fihx1nL7DQV0DEuFJSG1', 'eleven_multilingual_v2', {'stability': .7, 'similarity_boost': .8, 'style': 0.0, 'use_speaker_boost': True, 'speed': .95})}
parts = []
for k, (who, text) in enumerate(BLOCKS):
    if who == 'C':   # an original-sound clip (news footage audio), placed as is: "C: <path to wav>"
        y, sr0 = sf.read(text if os.path.isabs(text) else os.path.join(R, text)); y = y if y.ndim == 1 else y.mean(1)
        if sr0 != SR: subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', text if os.path.isabs(text) else os.path.join(R, text), '-ac', '1', '-ar', str(SR), os.path.join(O, f'clip{k}.wav')], check=True); y, _ = sf.read(os.path.join(O, f'clip{k}.wav'))
        y = y / (np.sqrt(np.mean(y[np.abs(y) > .01] ** 2)) + 1e-9) * .1; f = int(.04 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        parts += [y, np.zeros(int(C.get('block_gap', .55) * SR))]; continue
    mp3 = os.path.join(O, f'take{k}.mp3')
    if '--revoice' in sys.argv or not os.path.exists(mp3):
        vid, model, vs = VOICE[who]
        req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_192', data=json.dumps({'text': text, 'model_id': model, 'voice_settings': vs, 'pronunciation_dictionary_locators': PRON}).encode(),
                                     headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
        open(mp3, 'wb').write(urllib.request.urlopen(req, timeout=180).read())
    tempo = C.get('tempo', 1.0) if who == 'N' else C.get('reader_tempo', 1.0)
    w = os.path.join(O, f'take{k}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', f"atempo={tempo},silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.12,areverse,afade=t=in:d=0.02,areverse,afade=t=in:d=0.08,areverse", '-ac', '1', '-ar', str(SR), w], check=True)
    y, _ = sf.read(w); y = y / (np.sqrt(np.mean(y[np.abs(y) > .01] ** 2)) + 1e-9) * .1
    parts += [y, np.zeros(int(C.get('block_gap', .55) * SR))]
sf.write(os.path.join(O, 'take.wav'), np.concatenate(parts[:-1]), SR)
M = WhisperModel('small.en', compute_type='int8')
def words(p): s, _ = M.transcribe(p, word_timestamps=True); return [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for g in s for w in g.words]
x, _ = sf.read(os.path.join(O, 'take.wav')); W = words(os.path.join(O, 'take.wav'))
out, prev = [], 0
for i, w in enumerate(W[:-1]):
    if w[0] not in C.get('extra', {}): continue
    c = int((w[2] + W[i + 1][1]) / 2 * SR); out.append(x[prev:c]); q = x[c - int(.1 * SR):c + int(.1 * SR)].copy()
    n = int(C['extra'][w[0]] * SR); reps = np.tile(q, n // len(q) + 2)[:n]; f = int(.03 * SR); reps[:f] *= np.linspace(0, 1, f); reps[-f:] *= np.linspace(1, 0, f)
    out.append(reps * .9); prev = c
out.append(x[prev:]); y = np.concatenate([np.zeros(int(.3 * SR))] + out + [np.zeros(int(.8 * SR))])
sf.write(os.path.join(R, 'voice.wav'), y / max(1, np.abs(y).max() / .9), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(R, 'voice.wav'), '-b:a', '192k', os.path.join(R, 'voice.mp3')], check=True)
NUM = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten', '14': 'fourteen', '30th': 'thirtieth', '1st': 'first', '400': 'four'}
def norm(t): t = t.strip('.,?!:;…').lower(); return NUM.get(t, t)
WW = words(os.path.join(R, 'voice.wav')); idx, j = [], 0
# Whisper drops short words at the very start of a long file ("Number nine."): if the first segment isn't heard, time the opening on its own clip
first = [norm(t) for t in C['segments'][0][0].split()]
if not any([norm(w[0]) for w in WW[i:i + len(first)]] == first for i in range(len(WW))):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(R, 'voice.wav'), '-t', '3', os.path.join(O, 'head.wav')], check=True)
    head = [w for w in words(os.path.join(O, 'head.wav')) if w[2] < WW[0][1] - .05]
    WW = head + WW
for k, (st, *rest) in enumerate(C['segments']):
    toks = [norm(t) for t in st.split()]; j0 = j
    while j <= len(WW) and [norm(w[0]) for w in WW[j:j + len(toks)]] != toks: j += 1
    if j > len(WW):
        if rest[1:2] == ['C']: idx.append(None); j = j0; continue      # a clip Whisper couldn't hear: placed between its neighbours below
        sys.exit(f'segment start not heard: {st!r} (heard: {" ".join(w[0] for w in WW)})')
    idx.append(j); j += 1
takes = []
known = [i for i in idx if i is not None]
for k, i0 in enumerate(idx):
    if i0 is None: takes.append(None); continue
    nxt = next((i for i in idx[k + 1:] if i is not None), len(WW)); ws = WW[i0:nxt]
    takes.append({'i': k, 'who': C['segments'][k][2] if len(C['segments'][k]) > 2 else 'N', 'text': C['segments'][k][1], 't0': ws[0][1], 't1': ws[-1][2], 'heard': ' '.join(w[0] for w in ws), 'words': ws})
for k, tk in enumerate(takes):
    if tk is None:
        a = takes[k - 1]['t1'] + .25 if k else .3; b = next(t['t0'] for t in takes[k + 1:] if t) - .25
        takes[k] = {'i': k, 'who': 'C', 'text': C['segments'][k][1], 't0': round(a, 2), 't1': round(b, 2), 'heard': '(clip)', 'words': []}
json.dump({'dur': round(len(y) / SR, 3), 'takes': takes}, open(os.path.join(R, 'takes.json'), 'w'), indent=1)
for t in takes: print(t['i'], t['t0'], t['t1'], t['heard'])
print('dur', round(len(y) / SR, 2))
