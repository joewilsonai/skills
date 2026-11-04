#!/usr/bin/env python3
"""Voice one reel from its script.json -> voice.wav, voice.mp3, takes.json (take start/end in seconds, with word timings).
script.json: [{"who": "N"|"R", "text": "...", "pause": seconds after, "speed": optional override}]  N = Smith (narrator), R = Harper (reads the record).
Takes are voiced with neighbouring lines as context; every call attaches the pronunciation dictionary.
Usage: voice.py <reel dir> [take indexes to regenerate]   (default: all; existing takes are reused otherwise)"""
import json, os, subprocess, sys, urllib.request
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); KEY = os.environ['ELEVENLABS_API_KEY']
V = {'N': 'TVtDNgumMv4lb9zzFzA2', 'R': 'Fihx1nL7DQV0DEuFJSG1'}
S = {'N': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.2, 'use_speaker_boost': True, 'speed': 1.12},
     'R': {'stability': 0.7, 'similarity_boost': 0.8, 'style': 0.0, 'use_speaker_boost': True, 'speed': 0.95}}
D0 = sys.argv[1]
PDP = next((os.path.join(d, 'pron-dict.json') for d in (D0, os.path.dirname(D0), os.path.dirname(os.path.dirname(D0))) if os.path.exists(os.path.join(d, 'pron-dict.json'))), None)
PD = json.load(open(PDP)); PRON = [{'pronunciation_dictionary_id': PD['id'], 'version_id': PD['version_id']}]
RETRIM = '--retrim' in sys.argv; ARGS = [a for a in sys.argv[1:] if a != '--retrim']
D = ARGS[0]; ONLY = {int(a) for a in ARGS[1:]}
SC = json.load(open(os.path.join(D, 'script.json'))); os.makedirs(os.path.join(D, 'takes'), exist_ok=True); SR = 44100
def tts(i, who, text):
    prev = ' '.join(s['text'] for s in SC[:i] if s['who'] == who)[-300:]; nxt = ' '.join(s['text'] for s in SC[i + 1:] if s['who'] == who)[:300]
    vs = dict(S[who]); vs['speed'] = SC[i].get('speed', vs['speed'])   # a line can ask for its own speed (a title, a hard fact)
    body = {'text': text, 'model_id': 'eleven_multilingual_v2', 'voice_settings': vs, 'previous_text': prev, 'next_text': nxt, 'pronunciation_dictionary_locators': PRON}
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{V[who]}?output_format=mp3_44100_192', data=json.dumps(body).encode(), headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    mp3 = os.path.join(D, f'takes/t{i}.mp3')
    if not (RETRIM and os.path.exists(mp3)): open(mp3, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', 'silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.12,areverse,afade=t=in:d=0.02,areverse,afade=t=in:d=0.08,areverse', '-ac', '1', '-ar', str(SR), os.path.join(D, f'takes/t{i}.wav')], check=True)
out, t, takes = [np.zeros(int(.3 * SR))], .3, []
from faster_whisper import WhisperModel
M = WhisperModel('small.en', compute_type='int8')
for i, s in enumerate(SC):
    w = os.path.join(D, f'takes/t{i}.wav')
    if not os.path.exists(w) or not ONLY or i in ONLY:
        if ONLY and i not in ONLY and os.path.exists(w): pass
        else: tts(i, s['who'], s['text'])
    x, _ = sf.read(w); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .1; d = len(x) / SR
    seg, _ = M.transcribe(w, word_timestamps=True); words = [[ww.word.strip(), round(t + ww.start, 2), round(t + ww.end, 2)] for g in seg for ww in g.words]
    takes.append({'i': i, 'who': s['who'], 'text': s['text'], 't0': round(t, 3), 't1': round(t + d, 3), 'heard': ' '.join(x[0] for x in words), 'words': words})
    out += [x, np.zeros(int(s['pause'] * SR))]; t += d + s['pause']
y = np.concatenate(out); sf.write(os.path.join(D, 'voice.wav'), y / max(1, np.abs(y).max() / .9), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'voice.wav'), '-b:a', '192k', os.path.join(D, 'voice.mp3')], check=True)
json.dump({'dur': round(t, 3), 'takes': takes}, open(os.path.join(D, 'takes.json'), 'w'), indent=1)
for k in takes: print(f"{k['i']} {k['who']} {k['t0']:6.2f}-{k['t1']:6.2f}  heard: {k['heard']}")
print('dur', round(t, 2))
