#!/usr/bin/env python3
"""Thumbnail wall of real record pages (the "1,000+ pages nobody read" shot).
Usage: wall.py <out_dir> <pdf> [<pdf> ...] [--key name=pdfindex:page ...]
Text pages only (mean > 215, dark share < 12%): photos of people never land in the wall.
Writes <out_dir>/wall.jpg (20x15 tiles of 54x70) and wall.json (key tile positions + reveal order)."""
import glob, json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
args = sys.argv[1:]; out = args.pop(0); keys = {}
pdfs = [a for a in args if not a.startswith('--') and '=' not in a]
for a in args:
    if '=' in a: n, v = a.split('='); keys[n] = v
tmp = tempfile.mkdtemp()
for i, p in enumerate(pdfs): subprocess.run(['pdftoppm', '-gray', '-scale-to-x', '108', '-scale-to-y', '140', '-png', p, f'{tmp}/p{i}'], check=True)
files = sorted(glob.glob(f'{tmp}/*.png'))
keep = [f for f in files if (lambda a: a.mean() > 215 and (a < 120).mean() < .12)(np.asarray(Image.open(f).convert('L'), float))]
COLS, ROWS, TW, TH = 20, 15, 54, 70; n = COLS * ROWS; rng = np.random.default_rng(3)
slots = [(5, 4), (13, 7), (8, 11), (16, 2), (3, 12)]; grid = [None] * n; info = {}
for (name, v), (c, r) in zip(keys.items(), slots):
    pi, pg = v.split(':'); f = [x for x in files if os.path.basename(x).startswith(f'p{pi}-') and int(x.rsplit('-', 1)[1][:-4]) == int(pg)][0]
    grid[r * COLS + c] = f; info[name] = [c, r]
others = [f for f in keep if f not in grid]; it = iter(rng.choice(others, min(len(others), n), replace=len(others) < n))
for i in range(n):
    if grid[i] is None: grid[i] = next(it)
atlas = Image.new('L', (COLS * TW, ROWS * TH), 20)
for i, f in enumerate(grid): atlas.paste(Image.open(f).convert('L').resize((TW - 4, TH - 4), Image.LANCZOS), ((i % COLS) * TW + 2, (i // COLS) * TH + 2))
os.makedirs(out, exist_ok=True); atlas.save(f'{out}/wall.jpg', quality=88)
json.dump({'cols': COLS, 'rows': ROWS, 'tw': TW, 'th': TH, 'key': info, 'order': [int(x) for x in rng.permutation(n)]}, open(f'{out}/wall.json', 'w'))
print('pages', len(files), 'text pages', len(keep), '->', out)
