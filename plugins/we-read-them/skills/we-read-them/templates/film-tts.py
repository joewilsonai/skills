#!/usr/bin/env python3
"""Narration with the designed ElevenLabs voice "Record Narrator" -> audio/vo/<id>.wav + dur.json (same outputs as core/tts/tts.py).
Needs ELEVENLABS_API_KEY in the environment. Usage: tts_el.py [ids...] (default: all lines)."""
import json, os, sys, urllib.request, subprocess
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE, MODEL = 'TVtDNgumMv4lb9zzFzA2', 'eleven_multilingual_v2'   # "Smith" (ElevenLabs library, cloned from a real narrator); settings = take C
SETTINGS = {'stability': 0.5, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True, 'speed': 1.07}
SAY = [('F.B.I.', 'FBI')]   # names and abbreviations: ElevenLabs pronunciation dictionary "What the record says" (../pron-dict.json)
PD = json.load(open(f'{D}/../pron-dict.json')); PRON = [{'pronunciation_dictionary_id': PD['id'], 'version_id': PD['version_id']}]
L = json.load(open(f'{D}/audio/lines.json')); want = set(sys.argv[1:])
os.makedirs(f'{D}/audio/vo', exist_ok=True)
for l in L:
    if want and l['id'] not in want: continue
    say = l['text']
    for a, b in SAY: say = say.replace(a, b)
    body = json.dumps({'text': say, 'model_id': MODEL, 'voice_settings': SETTINGS, 'pronunciation_dictionary_locators': PRON}).encode()
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_192', data=body,
                                 headers={'xi-api-key': os.environ['ELEVENLABS_API_KEY'], 'Content-Type': 'application/json'})
    mp3 = f'{D}/audio/vo/{l["id"]}.mp3'; open(mp3, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
    # trim leading/trailing silence, write 24 kHz mono wav
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ac', '1', '-ar', '24000', f'{D}/audio/vo/{l["id"]}.wav'], check=True); os.remove(mp3)
    print(l['id'], 'ok')
dur = {}
for l in L:
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'{D}/audio/vo/{l["id"]}.wav'], capture_output=True, text=True).stdout
    dur[l['id']] = round(float(out), 3)
json.dump(dur, open(f'{D}/audio/vo/dur.json', 'w'), indent=1); print(dur)
