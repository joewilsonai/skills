#!/usr/bin/env python3
"""Stitch the wide (1920x1080) reels into the long-form YouTube cut, with chapters.

Usage: longform.py <case reels dir> "<Case name>" [--preview] [--preset veryfast]
Reads <reels>/r0/wide, r10/wide ... r1/wide (countdown order). Each wide/ holds:
  meta.json  {"slug": "the-numbers", "chapter": "#10 · The numbers", "endcard_at": 54.1}
  reel-NN-<slug>-wide.mp4   (muxed master)
Interior reels cut at endcard_at, with up to 350 ms of fade after the last timed speech.
The final wide reel plays through its complete picture and sound, including its authored source hold or card. Writes into <reels>/final/:
  "We Read Them - <Case> (long-form).mp4", "chapters.txt" (YouTube timestamps), and with --preview a 2-pass 720p copy
  under 48 MB for Telegram (the bot upload limit is 50 MB).
"""
import argparse, json, math, os, re, subprocess, tempfile
from pathlib import Path

def verify_chapter_track(path, expected_titles):
    probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_chapters', '-show_entries',
                                     'chapter_tags=title:stream=codec_type,codec_tag_string,nb_frames',
                                     '-of', 'json', path])
    info = json.loads(probe)
    titles = [chapter.get('tags', {}).get('title') for chapter in info.get('chapters', [])]
    counts = [track.get('nb_frames') for track in info.get('streams', [])
              if track.get('codec_type') == 'data' and track.get('codec_tag_string') == 'text']
    if titles != expected_titles or counts != [str(len(expected_titles))]:
        raise ValueError(f'{path}: expected {len(expected_titles)} titled QuickTime chapters, '
                         f'found {len(titles)} chapter titles and native text sample counts {counts}')


def join_fade(reel, samples, sample_rate):
    """Use only the available post-speech tail for an interior chapter's fade."""
    duration = min(round(.35 * sample_rate), samples)
    timing = next((p for p in (reel / 'takes.json', reel / 'wide' / 'takes.json') if p.is_file()), None)
    if timing is not None:
        rows = json.loads(timing.read_text(encoding='utf-8'))['takes']
        ends = [float(row['t1']) for row in rows]
        ends.extend(float(word[2]) for row in rows for word in row.get('words') or [] if len(word) >= 3)
        if any(not math.isfinite(t) or t < 0 for t in ends):
            raise ValueError(f'{timing}: invalid speech end time')
        last_speech = math.ceil(max(ends, default=0) * sample_rate - 1e-7)
        if last_speech > samples:
            raise ValueError(f'{reel.name}: chapter cut at {samples / sample_rate:.4f}s precedes '
                             f'timed speech ending at {last_speech / sample_rate:.4f}s')
        duration = min(duration, samples - last_speech)
    return f',afade=t=out:ss={samples-duration}:ns={duration}' if duration else ''

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('reels_dir')
parser.add_argument('case_name')
parser.add_argument('--preview', action='store_true')
parser.add_argument('--preset', default='slow', choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'])
options = parser.parse_args()
R = os.path.abspath(options.reels_dir); CASE = options.case_name; PREVIEW = options.preview
order = ['r0'] + [f'r{n}' for n in range(10, 0, -1)]
items = []
for r in order:
    d = os.path.join(R, r, 'wide'); meta = json.load(open(os.path.join(d, 'meta.json')))
    mp4 = [f for f in os.listdir(d) if f.endswith('-wide.mp4')]
    if len(mp4) != 1: raise SystemExit(f'{d}: expected one *-wide.mp4, found {mp4}')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(d, mp4[0])], capture_output=True, text=True).stdout)
    items.append((r, os.path.join(d, mp4[0]), meta, dur))
fps = 30
sample_rate = 48000
args, fc, frame_cursor, chapters = [], [], 0, []
metadata = [';FFMETADATA1']
for i, (r, f, meta, dur) in enumerate(items):
    last = i == len(items) - 1
    end = dur if last else float(meta['endcard_at'])
    if not 0 < end <= dur: raise SystemExit(f'{r}: endcard_at {end} outside 0..{dur}')
    frames = max(1, round(end * fps))
    samples = frames * (sample_rate // fps)
    args += ['-threads', '2', '-i', f]
    fc.append(f'[{i}:v]fps={fps},trim=end_frame={frames},setpts=PTS-STARTPTS[v{i}]')
    fade = '' if last else join_fade(Path(R) / r, samples, sample_rate)
    fc.append(f'[{i}:a]aresample={sample_rate},apad=whole_len={samples},atrim=end_sample={samples},asetpts=PTS-STARTPTS{fade}[a{i}]')
    label = meta['chapter']
    m, s = divmod(frame_cursor // fps, 60)
    chapters.append(f'{m}:{s:02d} {label}')
    escaped = re.sub(r'([\\=;#])', r'\\\1', label.replace('\n', ' ').replace('\r', ' '))
    metadata.extend(['[CHAPTER]', f'TIMEBASE=1/{fps}', f'START={frame_cursor}', f'END={frame_cursor + frames}', f'title={escaped}'])
    frame_cursor += frames
fc.append(''.join(f'[v{i}][a{i}]' for i in range(len(items))) + f'concat=n={len(items)}:v=1:a=1[v][a]')
os.makedirs(os.path.join(R, 'final'), exist_ok=True)
out = os.path.join(R, 'final', f'We Read Them - {CASE} (long-form).mp4')
t = frame_cursor / fps
with tempfile.TemporaryDirectory(prefix='.stitch-', dir=os.path.dirname(out)) as work:
    chapters_input = os.path.join(work, 'chapters.ffmeta')
    with open(chapters_input, 'w', encoding='utf-8') as chapter_file:
        chapter_file.write('\n'.join(metadata) + '\n')
    staged = os.path.join(work, 'master.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-f', 'ffmetadata', '-i', chapters_input,
                    '-filter_complex_threads', '3', '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
                    '-map_chapters', str(len(items)), '-c:v', 'libx264', '-crf', '18', '-preset', options.preset,
                    '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
                    '-c:a', 'aac', '-b:a', '192k', '-movie_timescale', str(sample_rate),
                    '-movflags', '+faststart', staged], check=True)
    expected_titles = [meta['chapter'] for _, _, meta, _ in items]
    verify_chapter_track(staged, expected_titles)
    os.replace(staged, out)
open(os.path.join(R, 'final', 'chapters.txt'), 'w').write('\n'.join(chapters) + '\n')
print('long-form', out, f'{t:.1f}s'); print('\n'.join(chapters))
if PREVIEW:
    pv = os.path.join(R, 'final', f'We Read Them - {CASE} (long-form preview).mp4'); vb = int((46 * 8 * 1024 * 1024 / t - 96000) / 1000)
    common = ['-vf', 'scale=1280:720', '-c:v', 'libx264', '-preset', options.preset, '-b:v', f'{vb}k']
    with tempfile.TemporaryDirectory(prefix='.preview-', dir=os.path.dirname(pv)) as work:
        passlog = os.path.join(work, 'encode')
        staged = os.path.join(work, 'preview.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, *common, '-pass', '1', '-passlogfile', passlog,
                        '-an', '-f', 'null', '/dev/null'], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, *common, '-pass', '2', '-passlogfile', passlog,
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movie_timescale', str(sample_rate),
                        '-movflags', '+faststart', staged], check=True)
        verify_chapter_track(staged, expected_titles)
        os.replace(staged, pv)
    print('preview', pv, f'{os.path.getsize(pv) / 1048576:.1f} MB')
