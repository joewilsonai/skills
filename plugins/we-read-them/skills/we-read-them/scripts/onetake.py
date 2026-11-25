#!/usr/bin/env python3
"""One-take narration for a reel (the playbook's voice step).
<reel>/one/config.json: {"tempo": 1.12, "extra": {"TikTok.": .9, ...}, "segments": [[start word, display text], ...]}
<reel>/one/script.txt: the whole narration with v3 tags ([somber], [quietly], [pause]).
Steps: reuse each one/takeN.mp3 unless selected for revoicing -> pitch-preserving tempo ->
stretch the named gaps with the gap's own room sound -> Whisper word timings -> <reel>/voice.wav, voice.mp3, takes.json."""
import argparse, fcntl, hashlib, json, os, re, shutil, subprocess, sys, tempfile, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('reel')
selection = parser.add_mutually_exclusive_group()
selection.add_argument('--revoice', action='store_true', help='replace every synthesized voice block')
selection.add_argument('--revoice-block', metavar='N', type=int, action='append', default=[],
                       help='replace only this zero-based takeN.mp3 (repeatable)')
args = parser.parse_args()
R = str(Path(args.reel).expanduser().resolve()); O = os.path.join(R, 'one'); C = json.load(open(os.path.join(O, 'config.json'))); SR = 44100
run_lock = open(os.path.join(O, '.onetake.lock'), 'a')
try:
    fcntl.flock(run_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    sys.exit(f'Another one-take build is active in {R}')
# R marks an attributed reading by the episode narrator; C is an original recording.
BLOCKS = []
for line in open(os.path.join(O, 'script.txt')).read().strip().split('\n'):
    who = 'R' if line.startswith('R:') else 'C' if line.startswith('C:') else 'N'; text = line[2:].strip() if who in ('R', 'C') else line.strip()
    if not text: continue
    if BLOCKS and BLOCKS[-1][0] == who and who != 'C': BLOCKS[-1][1] += ' ' + text   # two C: lines in a row are two clips, never one path
    else: BLOCKS.append([who, text])
def _find_pd():
    for d in (Path(R), *Path(R).parents):
        p = d / 'pron-dict.json'
        if p.is_file(): return p
    sys.exit('pron-dict.json not found above ' + R + ' (create the case dictionary first)')
pd = json.load(open(_find_pd())); PRON = [{'pronunciation_dictionary_id': pd['id'], 'version_id': pd['version_id']}]
NARRATOR = ('TVtDNgumMv4lb9zzFzA2', 'eleven_v3', {'stability': .5, 'similarity_boost': .8, 'speed': 1.1})
VOICE = {'N': NARRATOR, 'R': NARRATOR}

def narrator_reading_is_cached(index, source):
    if not source.is_file() or source.stat().st_size == 0:
        return False
    audio_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    for receipt_path in (Path(O) / 'voice-receipts').glob(f'take{index}-*/receipt.json'):
        receipt = json.loads(receipt_path.read_text())
        if (receipt.get('status') == 'installed' and receipt.get('role') == 'R'
                and receipt.get('voice_id') == NARRATOR[0] and receipt.get('audio_sha256') == audio_hash):
            return True
    return False

selected = set(args.revoice_block)
for index in selected:
    if index < 0 or index >= len(BLOCKS) or BLOCKS[index][0] == 'C':
        parser.error(f'block {index} is not synthesized narration or a reading')
if selected:
    for index, (role, _) in enumerate(BLOCKS):
        source = Path(O) / f'take{index}.mp3'
        if role != 'C' and index not in selected and not (source.is_file() and source.stat().st_size):
            parser.error(f'block {index} has no cached take; include it with --revoice-block to generate it')
        if role == 'R' and index not in selected and not narrator_reading_is_cached(index, source):
            parser.error(f'include --revoice-block {index} to update this reading to the episode narrator')

def _save_receipt(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)

def _install_take(receipt_path, receipt, target):
    downloaded = receipt_path.parent / 'received.mp3'
    if downloaded.is_file():
        if hashlib.sha256(downloaded.read_bytes()).hexdigest() != receipt['audio_sha256']:
            sys.exit(f'Audio checksum differs from its receipt: {downloaded}')
        try:
            subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', str(downloaded), '-map', '0:a:0', '-f', 'null', '-'], check=True)
        except subprocess.CalledProcessError:
            receipt['status'] = 'invalid_audio'
            _save_receipt(receipt_path, receipt)
            raise
        downloaded.replace(target)
    elif not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != receipt['audio_sha256']:
        sys.exit(f'Received audio is missing. Check ElevenLabs history for the ID in {receipt_path}')
    receipt['status'] = 'installed'
    _save_receipt(receipt_path, receipt)

def _request_take(index, who, text, target):
    """Keep request receipts, the received audio and any replaced take under one/."""
    vid, model, settings = VOICE[who]
    body = json.dumps({'text': text, 'model_id': model, 'voice_settings': settings,
                       'pronunciation_dictionary_locators': PRON}).encode()
    request_hash = hashlib.sha256(body).hexdigest()
    records = Path(O) / 'voice-receipts'
    records.mkdir(exist_ok=True)
    for prior in records.glob(f'take{index}-*/receipt.json'):
        previous = json.loads(prior.read_text())
        if previous['status'] == 'received':
            if previous['request_sha256'] == request_hash and previous.get('voice_id') == vid:
                _install_take(prior, previous, target)
                return
            previous['status'] = 'superseded'
            _save_receipt(prior, previous)
        if previous['status'] in ('submitted', 'uncertain'):
            sys.exit(f'Inspect the existing request in {prior} before generating block {index} again. '
                     'Recover any downloaded audio or reconcile the request against provider history.')
    request = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_192',
                                     data=body, headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    directory = Path(tempfile.mkdtemp(prefix=f'take{index}-', dir=records))
    receipt_path = directory / 'receipt.json'
    receipt = {'status': 'submitted', 'time_utc': datetime.now(timezone.utc).isoformat(), 'block': index,
               'role': who, 'model': model, 'voice_id': vid, 'characters': len(text),
               'request_sha256': request_hash, 'text_sha256': hashlib.sha256(text.encode()).hexdigest()}
    if target.exists():
        shutil.copy2(target, directory / 'previous.mp3')
        receipt['previous_sha256'] = hashlib.sha256((directory / 'previous.mp3').read_bytes()).hexdigest()
    _save_receipt(receipt_path, receipt)
    downloaded = directory / 'received.mp3'
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            receipt.update(request_id=response.headers.get('request-id'), history_item_id=response.headers.get('history-item-id'),
                           credits=response.headers.get('character-cost'))
            with downloaded.open('wb') as stream:
                shutil.copyfileobj(response, stream)
            declared = response.headers.get('Content-Length')
            if declared and downloaded.stat().st_size != int(declared):
                raise IOError('Incomplete ElevenLabs audio response')
    except urllib.error.HTTPError as error:
        receipt.update(status='rejected' if 400 <= error.code < 500 else 'uncertain', http_status=error.code)
        _save_receipt(receipt_path, receipt)
        raise
    except Exception as error:
        receipt.update(status='uncertain', error=type(error).__name__)
        _save_receipt(receipt_path, receipt)
        raise
    receipt.update(status='received', audio_sha256=hashlib.sha256(downloaded.read_bytes()).hexdigest())
    _save_receipt(receipt_path, receipt)
    _install_take(receipt_path, receipt, target)
    print(f'Generated block {index} ({who}); receipt: {receipt_path}', flush=True)
parts, PLACE = [], []   # PLACE: (who, start, end) of each block in take.wav, in samples
def _pos(): return sum(len(q) for q in parts)
for k, (who, text) in enumerate(BLOCKS):
    if who == 'C':   # an original-sound clip (news footage audio), placed as is: "C: <path to wav>"
        y, sr0 = sf.read(text if os.path.isabs(text) else os.path.join(R, text)); y = y if y.ndim == 1 else y.mean(1)
        if sr0 != SR: subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', text if os.path.isabs(text) else os.path.join(R, text), '-ac', '1', '-ar', str(SR), os.path.join(O, f'clip{k}.wav')], check=True); y, _ = sf.read(os.path.join(O, f'clip{k}.wav'))
        y = y / (np.sqrt(np.mean(y[np.abs(y) > .01] ** 2)) + 1e-9) * .1; f = int(.04 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
        PLACE.append(('C', _pos(), _pos() + len(y))); parts += [y, np.zeros(int(C.get('block_gap', .55) * SR))]; continue
    mp3 = os.path.join(O, f'take{k}.mp3')
    if (args.revoice or k in selected or not os.path.isfile(mp3) or os.path.getsize(mp3) == 0
            or (who == 'R' and not narrator_reading_is_cached(k, Path(mp3)))):
        _request_take(k, who, text, Path(mp3))
    tempo = C.get('tempo', 1.0) if who == 'N' else C.get('reader_tempo', 1.0)
    w = os.path.join(O, f'take{k}.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', f"atempo={tempo},silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-55dB:start_silence=0.12,areverse,afade=t=in:d=0.02,areverse,afade=t=in:d=0.08,areverse", '-ac', '1', '-ar', str(SR), w], check=True)
    y, _ = sf.read(w); y = y / (np.sqrt(np.mean(y[np.abs(y) > .01] ** 2)) + 1e-9) * .1
    PLACE.append((who, _pos(), _pos() + len(y))); parts += [y, np.zeros(int(C.get('block_gap', .55) * SR))]
sf.write(os.path.join(O, 'take.wav'), np.concatenate(parts[:-1]), SR)
M = WhisperModel('small.en', compute_type='int8')
def _words1(p, off=0.0): s, _ = M.transcribe(p, word_timestamps=True, condition_on_previous_text=False); return [[w.word.strip(), round(w.start + off, 2), round(w.end + off, 2)] for g in s for w in g.words]
def words(p):
    # Whisper drops whole phrases from a long file ("The affidavits say his phone stopped in" vanished from a 40 s take), so transcribe
    # pieces of <= ~14 s cut at the quietest point near each target, and offset the times back.
    a, sr = sf.read(p); a = a if a.ndim == 1 else a.mean(1); hop = int(.02 * sr)
    if len(a) < 16 * sr: return _words1(p)
    e = np.sqrt(np.convolve(a ** 2, np.ones(int(.25 * sr)) / int(.25 * sr), 'same'))[::hop]
    cuts, s0 = [0], 0
    while len(a) - s0 > 16 * sr:
        lo, hi = (s0 + 7 * sr) // hop, (s0 + 14 * sr) // hop; c = (lo + int(np.argmin(e[lo:hi]))) * hop; cuts.append(c); s0 = c
    cuts.append(len(a)); out = []
    for c0, c1 in zip(cuts, cuts[1:]):
        q = os.path.join(O, '_chunk.wav'); sf.write(q, a[c0:c1], sr); out += _words1(q, c0 / sr)
    return out
x, _ = sf.read(os.path.join(O, 'take.wav')); xw = x.copy()
for who, a, b in PLACE:
    if who == 'C': xw[a:b] = 0   # muted for Whisper: phone/news audio throws it off (drifted times, no punctuation, so 'extra' keys never matched)
sf.write(os.path.join(O, 'take_noclips.wav'), xw, SR); W = words(os.path.join(O, 'take_noclips.wav'))
input_clips = [(a, b) for who, a, b in PLACE if who == 'C']
out, prev, INS = [], 0, []   # INS: (cut sample, inserted samples) so clip placements can be mapped into voice.wav
for i, w in enumerate(W[:-1]):
    if w[0] not in C.get('extra', {}): continue
    left = max(prev, int(w[2] * SR)); right = min(len(x), int(W[i + 1][1] * SR))
    # Muting a clip for ASR can make the word gap straddle the entire clip.
    for a, b in input_clips:
        if left < b and a < right:
            if a <= left: left = b
            else: right = a; break
    n = int(C['extra'][w[0]] * SR)
    if right <= left or n <= 0: continue
    c = (left + right) // 2; out.append(x[prev:c])
    q = x[max(left, c - int(.1 * SR)):min(right, c + int(.1 * SR))]
    reps = np.tile(q, n // len(q) + 1)[:n]; f = min(int(.03 * SR), n // 2)
    if f:
        reps[:f] *= np.linspace(0, 1, f); reps[-f:] *= np.linspace(1, 0, f)
    out.append(reps * .9); prev = c; INS.append((c, n))
out.append(x[prev:]); y = np.concatenate([np.zeros(int(.3 * SR))] + out + [np.zeros(int(.8 * SR))])
staging_dir = tempfile.TemporaryDirectory(prefix='.voice-build-', dir=O)
staging = Path(staging_dir.name)
sf.write(staging / 'voice.wav', y / max(1, np.abs(y).max() / .9), SR)
def vt(smp, is_end=False):
    added = sum(n for c, n in INS if c < smp or (c == smp and not is_end))
    return (smp + int(.3 * SR) + added) / SR
CLIPS = [(vt(a), vt(b, is_end=True)) for a, b in input_clips]
# Whisper loses its place inside phone/news audio and drifts the narration after it, so time the words on a copy with the clips muted
yw = y.copy()
for a, b in CLIPS: yw[int(a * SR):int(b * SR)] = 0
sf.write(os.path.join(O, 'voice_noclips.wav'), yw / max(1, np.abs(yw).max() / .9), SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(staging / 'voice.wav'), '-b:a', '192k', str(staging / 'voice.mp3')], check=True)
NUM = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen', '16': 'sixteen', '17': 'seventeen', '18': 'eighteen', '19': 'nineteen', '20': 'twenty', '30th': 'thirtieth', '1st': 'first', '400': 'four'}
def norm(t): t = t.strip('.,?!:;…-').lower(); return NUM.get(t, t)
def keytoks(st): return [norm(t) for t in re.split(r'[\s-]+', st) if t.strip('-')]   # 'seven-page' -> seven, page (Whisper writes 'seven -page')
WW = words(os.path.join(O, 'voice_noclips.wav')); idx, j = [], 0
WW = [w for w in WW if not any(a + .05 <= w[1] and w[2] <= b - .05 for a, b in CLIPS)]   # Whisper invents "You" in the muted clip spans; it stretched the line before the clip
# Whisper drops short words at the very start of a long file ("Number nine."): if the first segment isn't heard, time the opening on its own clip
first = keytoks(C['segments'][0][0])
if not any([norm(w[0]) for w in WW[i:i + len(first)]] == first for i in range(len(WW))):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(O, 'voice_noclips.wav'), '-t', '3', os.path.join(O, 'head.wav')], check=True)
    hw = words(os.path.join(O, 'head.wav')); hm = next((i for i in range(len(hw)) if [norm(w[0]) for w in hw[i:i + len(first)]] == first), None)
    if hm is not None:   # Whisper merged "Number ten" into one word ("10."): take the head's words and drop what they cover
        hw = hw[:hm + len(first)]; WW = hw + [w for w in WW if w[1] >= hw[-1][2] - .02]
    else: WW = [w for w in hw if w[2] < WW[0][1] - .05] + WW
for k, (st, *rest) in enumerate(C['segments']):
    toks = keytoks(st); j0 = j
    while j <= len(WW) and [norm(w[0]) for w in WW[j:j + len(toks)]] != toks: j += 1
    if j > len(WW) and k == 0 and len(toks) > 1:   # "Number six." often comes back as just "6.": match the opening on its last word
        j = j0
        while j <= len(WW) and [norm(w[0]) for w in WW[j:j + 1]] != toks[-1:]: j += 1
    if rest[1:2] == ['C']: idx.append(None); j = j0; continue      # clips are muted for Whisper; placed from the build below
    if j > len(WW):      # a clip Whisper couldn't hear: placed between its neighbours below
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
        ci = sum(1 for s in C['segments'][:k] if s[2:3] == ['C'])
        if ci < len(CLIPS): a, b = CLIPS[ci]
        else: a = takes[k - 1]['t1'] + .25 if k else .3; b = next(t['t0'] for t in takes[k + 1:] if t) - .25
        takes[k] = {'i': k, 'who': 'C', 'text': C['segments'][k][1], 't0': round(a, 2), 't1': round(b, 2), 'heard': '(clip)', 'words': []}
for k, tk in enumerate(takes):   # a narration segment never runs into the clip after it (Whisper can invent a word in the muted span)
    if tk['who'] != 'C' and k + 1 < len(takes) and takes[k + 1]['who'] == 'C' and tk['t1'] > takes[k + 1]['t0']:
        tk['words'] = [w for w in tk['words'] if w[1] < takes[k + 1]['t0']] or tk['words'][:1]; tk['t1'] = tk['words'][-1][2]; tk['heard'] = ' '.join(w[0] for w in tk['words'])
# Whisper often starts a line's first word at the end of the previous silence (up to ~1.5 s early). Snap each spoken
# segment's start (and its first word) forward to the real speech onset: first 10 ms frame within 1.8 s above -38 dB of the take's peak.
_vy, _ = sf.read(staging / 'voice.wav'); _vy = _vy if _vy.ndim == 1 else _vy.mean(1)
_env = np.sqrt(np.convolve(np.asarray(_vy, float) ** 2, np.ones(int(.01 * SR)) / int(.01 * SR), 'same')); _thr = _env.max() * 10 ** (-38 / 20)
for tk in takes:
    if not tk or tk['who'] == 'C' or not tk['words']: continue
    a = int(tk['t0'] * SR); first_end = tk['words'][0][2]
    if len(tk['words']) > 1: first_end = min(first_end, tk['words'][1][1])
    b = min(len(_env), int(min(tk['t0'] + 1.8, first_end) * SR))
    if a >= b or _env[a] > _thr: continue   # the first word may already be speaking
    _w = int(.06 * SR); _ab = (_env[a:b] > _thr).astype(int)   # sustained: 60 ms above threshold, so a breath or click doesn't count
    hit = np.nonzero(np.convolve(_ab, np.ones(_w, int), 'valid') == _w)[0] if len(_ab) >= _w else []
    if len(hit):
        on = round((a + hit[0]) / SR - .03, 2)
        if tk['t0'] + .05 < on < first_end: tk['t0'] = on; tk['words'][0][1] = on
(staging / 'takes.json').write_text(json.dumps({'dur': round(len(y) / SR, 3), 'takes': takes}, indent=1))
# Publish only after caption matching succeeds. Roll back an ordinary filesystem
# failure mid-publish so existing consumers keep the previous complete set.
names = ('voice.wav', 'voice.mp3', 'takes.json')
for name in names:
    if (Path(R) / name).exists(): os.link(Path(R) / name, staging / ('previous-' + name))
published = []
try:
    for name in names:
        (staging / name).replace(Path(R) / name)
        published.append(name)
except OSError:
    for name in reversed(published):
        original = staging / ('previous-' + name)
        if original.exists(): original.replace(Path(R) / name)
        else: (Path(R) / name).unlink()
    raise
staging_dir.cleanup()
for t in takes: print(t['i'], t['t0'], t['t1'], t['heard'])
print('dur', round(len(y) / SR, 2))
