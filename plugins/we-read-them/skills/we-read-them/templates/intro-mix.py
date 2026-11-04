#!/usr/bin/env python3
"""Reel 0 mix (series intro): voice + D-minor bed, ticks on the stats, hits on the file and each tease flash, the "10" at the end."""
import json, os, sys, numpy as np, soundfile as sf, soxr
sys.path.insert(0, os.path.expanduser('~/lemo-opuscar'))
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, noise, env_exp, t_, whoosh, thump, norm, limit, brown
TK = json.load(open('takes.json')); T = TK['takes']; DUR = TK['dur'] + .8; N = int(DUR * SR)
mus = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32); voc = np.zeros((N, 2), np.float32); S.seed(10)
tFile = T[7]['t0']; tBox, tDad, tFbi, tEnd = T[9]['t0'], T[10]['t0'], T[11]['t0'], T[12]['t0']; STAT = [T[4]['t0'] - .05, T[5]['t0'] - .05, T[6]['t0'] - .05]
home = next(w[1] for w in T[1]['words'] if w[0].strip('.,').lower() == 'home')
ev = [(0.3, 'contrabass', 'D2', STAT[0] - .3, .45, -.2, .42), (0.3, 'cellos', 'A2', STAT[0] - .3, .36, .2, .32), (0.3, 'timpani', 'D2', 1.6, .55, 0, .45),
      (home, 'violins_trem', 'F5', 3.0, .22, .3, .15), (home + .4, 'violins_trem', 'E5', 2.6, .22, -.3, .13)]
for i in range(3): ev += [(STAT[i], 'timpani', ['D2', 'F2', 'A2'][i], 1.2, .65, 0, .55), (STAT[i], 'contrabass', ['D2', 'F2', 'A2'][i], (STAT[i + 1] if i < 2 else tFile) - STAT[i], .4, 0, .35)]
ev += [(tFile, 'contrabass', 'D2', tBox - tFile, .45, -.2, .42), (tFile, 'cellos', 'D3', tBox - tFile, .35, .2, .3)]
WD = (T[8]['t0'] + 1.4) - tFile; WE = T[8]['t1'] + .1
ev += [(tFile, 'violins_trem', 'A4', WD, .2, .3, .14), (tFile + WD * .4, 'violins_trem', 'D5', WD * .6, .25, -.3, .14), (tFile, 'cellos', 'A2', WD + 1.0, .32, 0, .28)]
for j in range(3): ev.append((WE + .15 + j * .3, 'glockenspiel', ['D6', 'F6', 'A6'][j], 1.0, .5, -.2 + .2 * j, .4))
for tt in (tBox, tDad, tFbi): ev += [(tt, 'timpani', 'D2', 1.0, .6, 0, .45), (tt, 'contrabass', 'D2', 1.6, .4, 0, .35)]
ev += [(tEnd, 'gran_cassa', 'hit', 2.0, .85, 0, .75), (tEnd, 'timpani', 'D2', 2.2, .8, 0, .7), (T[13]['t0'], 'timpani', 'A2', 1.4, .6, 0, .5)]
for p, pan in [('D2', 0), ('D3', -.2), ('A3', .2), ('E4', -.3), ('F4', .3)]: ev.append((tEnd + .1, 'cellos' if p != 'D2' else 'contrabass', p, DUR - tEnd, .32, pan, .3))
mus += S.render(ev, dur=DUR, master=False)[:N]; mus = S.room(mus, size=.5, mix=.2)
def paper(v=1.0): d = .25; return bp(noise(d), 1200, 6000) * env_exp(d, .05) * (1 - np.exp(-t_(d) / .01)) * v
def shutter(v=1.0):
    d = .09; a = hp(noise(d), 2000) * env_exp(d, .006); b = np.pad(hp(noise(.05), 1500) * env_exp(.05, .005), (int(.045 * SR), 0))[:len(a)]; return norm(a + b * .8) * v
def pencil(d=.35, v=1.0): return bp(noise(d), 2500, 7000) * (np.sin(np.pi * t_(d) / d) ** .5) * .5 * v
def tick(v=1.0, f=2400): d = .03; tt = t_(d); return (hp(noise(d), 1800) * env_exp(d, .003) + np.sin(2 * np.pi * f * tt) * env_exp(d, .004) * .6) * v
add(fx, pencil(1.4), T[0]['t0'] + .6, .25); add(fx, pencil(1.2), home, .3)
for i in range(3): add(fx, shutter(1), STAT[i], .5); add(fx, thump(.7, 52), STAT[i], .35)
for k in range(40): add(fx, paper(.5 + .5 * k / 40), tFile + WD * (k / 40) ** .55, .12 + .1 * k / 40, float(np.sin(k)) * .5)   # pages landing, faster and faster
for tt in (tBox, tDad, tFbi): add(fx, shutter(1), tt, .45); add(fx, paper(.8), tt + .05, .3)
add(fx, whoosh(.3, 1), tEnd - .1, .3); add(fx, thump(.9, 48), tEnd, .5)
fx += np.repeat(lp(brown(DUR), 400)[:N, None] * .012, 2, axis=1).astype(np.float32)
x, sr = sf.read('voice.wav'); x = x if x.ndim == 1 else x.mean(1); x = soxr.resample(x, sr, SR); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .11
add(voc, x, 0.0, 1.0, 0)
from scipy.ndimage import uniform_filter1d, maximum_filter1d
g = np.where(np.abs(voc[:, 0]) > .01, .35, 1.0); g = uniform_filter1d(1 - maximum_filter1d(1 - g, int(.4 * SR)), int(.25 * SR)); mus *= g[:, None]
out = mus * 3.0 + fx * .8 + voc; tail = int(1.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
out = np.stack([limit(out[:, c], .42) for c in range(2)], 1); os.makedirs('out', exist_ok=True); sf.write('out/mix.wav', out.astype(np.float32), SR); print('mix ok', round(DUR, 2))
