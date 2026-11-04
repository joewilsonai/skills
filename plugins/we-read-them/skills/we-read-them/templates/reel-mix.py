#!/usr/bin/env python3
"""Reel 10 mix: voice + D-minor bed, hits on the number, the strike, the "1", each page, and the turn."""
import json, os, sys, numpy as np, soundfile as sf, soxr
sys.path.insert(0, os.path.expanduser('~/lemo-opuscar'))
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, noise, env_exp, t_, whoosh, thump, norm, limit, brown
TK = json.load(open('takes.json')); T = TK['takes']; DUR = TK['dur'] + .8; N = int(DUR * SR)
mus = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32); voc = np.zeros((N, 2), np.float32); S.seed(11)
strike = T[1]['t1'] - .2; tOne, tMap, tRiv, tRead, tGnv, tEnd = T[2]['t0'], T[3]['t0'], T[4]['t0'], T[5]['t0'], T[6]['t0'], T[7]['t0']
ev = [(0.0, 'timpani', 'D2', 1.6, .7, 0, .6), (0.0, 'contrabass', 'D2', tRead, .45, -.2, .42), (0.0, 'cellos', 'A2', tRead, .36, .2, .32),
      (strike, 'timpani', 'A2', .8, .5, 0, .4), (tOne, 'timpani', 'D2', 1.2, .65, 0, .55),
      (tRead, 'violins_trem', 'E5', tGnv - tRead, .2, .3, .13), (tRead, 'violins_trem', 'F5', tGnv - tRead, .2, -.3, .11), (tRead, 'contrabass', 'Bb2', tGnv - tRead, .4, -.2, .38),
      (tGnv, 'contrabass', 'D2', tEnd - tGnv, .42, -.2, .4), (tGnv, 'cellos', 'F3', tEnd - tGnv, .32, .2, .28),
      (tEnd, 'gran_cassa', 'hit', 1.8, .7, 0, .6), (tEnd, 'contrabass', 'D2', DUR - tEnd, .4, 0, .38), (tEnd, 'cellos', 'D3', DUR - tEnd, .32, 0, .28), (tEnd, 'violas', 'A3', DUR - tEnd, .26, 0, .2)]
mus += S.render(ev, dur=DUR, master=False)[:N]; mus = S.room(mus, size=.5, mix=.2)
def paper(v=1.0): d = .25; return bp(noise(d), 1200, 6000) * env_exp(d, .05) * (1 - np.exp(-t_(d) / .01)) * v
def shutter(v=1.0):
    d = .09; a = hp(noise(d), 2000) * env_exp(d, .006); b = np.pad(hp(noise(.05), 1500) * env_exp(.05, .005), (int(.045 * SR), 0))[:len(a)]; return norm(a + b * .8) * v
def pencil(d=.35, v=1.0): return bp(noise(d), 2500, 7000) * (np.sin(np.pi * t_(d) / d) ** .5) * .5 * v
add(fx, pencil(.3), strike, .4); add(fx, thump(.5, 60), strike, .3); add(fx, shutter(1), tOne, .45); add(fx, pencil(2.0), tMap + .4, .25)
for tt in (tRead, tGnv): add(fx, shutter(1), tt, .45); add(fx, paper(1), tt + .04, .35)
add(fx, whoosh(.3, 1), tEnd - .1, .25)
fx += np.repeat(lp(brown(DUR), 400)[:N, None] * .012, 2, axis=1).astype(np.float32)
x, sr = sf.read('voice.wav'); x = x if x.ndim == 1 else x.mean(1); x = soxr.resample(x, sr, SR); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .11
add(voc, x, 0.0, 1.0, 0)
from scipy.ndimage import uniform_filter1d, maximum_filter1d
g = np.where(np.abs(voc[:, 0]) > .01, .35, 1.0); g = uniform_filter1d(1 - maximum_filter1d(1 - g, int(.4 * SR)), int(.25 * SR)); mus *= g[:, None]
out = mus * 3.0 + fx * .8 + voc; tail = int(1.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
out = np.stack([limit(out[:, c], .42) for c in range(2)], 1); os.makedirs('out', exist_ok=True); sf.write('out/mix.wav', out.astype(np.float32), SR); print('mix ok', round(DUR, 2))
