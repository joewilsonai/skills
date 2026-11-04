#!/usr/bin/env python3
"""Reel 0 mix (Hailey Dunn intro): voice + D-minor bed, a pen-scratch under the polygraph, hits on the county, the charge, the dismissal, the stats and the title."""
import json, os, sys, numpy as np, soundfile as sf, soxr
sys.path.insert(0, os.path.expanduser('~/lemo-opuscar'))
from core.audio import sampler as S
from core.audio.sfx import SR, add, bp, hp, lp, noise, env_exp, t_, whoosh, thump, norm, limit, brown
TK = json.load(open('takes.json')); T = TK['takes']; DUR = TK['dur'] + .8; N = int(DUR * SR)
mus = np.zeros((N, 2), np.float32); fx = np.zeros((N, 2), np.float32); voc = np.zeros((N, 2), np.float32); S.seed(11)
def w(i, word): return next((x[1] for x in T[i]['words'] if x[0].strip('.,?').lower() == word), T[i]['t0'])
tScur, tFound, tCh, tDis, tWall, tEnd, tTen = w(3, 'scurry'), T[5]['t0'], w(9, 'murder'), w(10, 'dropped'), T[14]['t0'], T[19]['t0'], T[20]['t0']
STAT = [T[11]['t0'], T[12]['t0'] - .05, T[13]['t0'] - .05]
ev = [(0.2, 'contrabass', 'D2', tScur, .42, -.2, .4), (0.2, 'cellos', 'A2', tScur, .34, .2, .3), (0.3, 'timpani', 'D2', 1.6, .5, 0, .4), (0.4, 'violins_trem', 'A4', 6.5, .18, .2, .12),
      (tScur, 'violins_trem', 'F5', 3.0, .22, .3, .15), (tScur, 'contrabass', 'D2', tFound - tScur, .42, 0, .38),
      (tFound, 'timpani', 'D2', 1.4, .7, 0, .6), (tFound, 'contrabass', 'C2', tCh - tFound, .42, 0, .38), (tFound + .3, 'violins_trem', 'E5', 3, .22, -.3, .13),
      (tCh, 'timpani', 'F2', 1.2, .65, 0, .55), (tCh, 'contrabass', 'F2', tDis - tCh, .4, 0, .35), (tDis, 'gran_cassa', 'hit', 1.6, .7, 0, .6), (tDis, 'contrabass', 'D2', STAT[0] - tDis, .4, 0, .35)]
for i in range(3): ev += [(STAT[i], 'timpani', ['D2', 'F2', 'A2'][i], 1.2, .6, 0, .5), (STAT[i], 'contrabass', ['D2', 'F2', 'A2'][i], (STAT[i + 1] if i < 2 else tWall) - STAT[i], .4, 0, .35)]
WD = T[15]['t0'] + .6 - tWall
ev += [(tWall, 'contrabass', 'D2', tEnd - tWall, .45, -.2, .42), (tWall, 'cellos', 'D3', tEnd - tWall, .35, .2, .3), (tWall, 'violins_trem', 'A4', WD + 2, .2, .3, .14)]
for j, i in enumerate((15, 16, 17, 18)): ev.append((T[i]['t0'], 'glockenspiel', ['D6', 'F6', 'A6', 'D7'][j], 1.0, .45, -.2 + .15 * j, .35))
ev += [(tEnd, 'gran_cassa', 'hit', 2.0, .85, 0, .75), (tEnd, 'timpani', 'D2', 2.2, .8, 0, .7), (tTen, 'timpani', 'A2', 1.4, .6, 0, .5)]
for p, pan in [('D2', 0), ('D3', -.2), ('A3', .2), ('E4', -.3), ('F4', .3)]: ev.append((tEnd + .1, 'cellos' if p != 'D2' else 'contrabass', p, DUR - tEnd, .32, pan, .3))
mus += S.render(ev, dur=DUR, master=False)[:N]; mus = S.room(mus, size=.5, mix=.2)
def paper(v=1.0): d = .25; return bp(noise(d), 1200, 6000) * env_exp(d, .05) * (1 - np.exp(-t_(d) / .01)) * v
def shutter(v=1.0):
    d = .09; a = hp(noise(d), 2000) * env_exp(d, .006); b = np.pad(hp(noise(.05), 1500) * env_exp(.05, .005), (int(.045 * SR), 0))[:len(a)]; return norm(a + b * .8) * v
def pen(d, v=1.0): tt = t_(d); return bp(noise(d), 3000, 8000) * (.55 + .45 * np.sin(2 * np.pi * 2.1 * tt) ** 2) * .35 * v
def stampfx(v=1.0): a = thump(1, 60)[:int(.12 * SR)]; return norm(a + (bp(noise(.12), 300, 3000) * env_exp(.12, .02) * .6)[:len(a)]) * v
add(fx, shutter(1), T[1]['t0'], .4); add(fx, shutter(1), T[2]['t0'], .4); add(fx, shutter(1), T[3]['t0'], .4); add(fx, paper(.8), T[3]['t0'] + .05, .3); add(fx, shutter(.8), T[7]['t0'], .35); add(fx, shutter(.8), T[8]['t0'], .35); add(fx, thump(.8, 50), tFound, .4)
add(fx, shutter(1), T[9]['t0'], .4); add(fx, stampfx(1), tCh, .6); add(fx, shutter(1), T[10]['t0'], .4); add(fx, stampfx(1), tDis, .7)
for i in range(3): add(fx, shutter(1), STAT[i], .45); add(fx, thump(.7, 52), STAT[i], .35)
for k in range(40): add(fx, paper(.5 + .5 * k / 40), tWall + WD * (k / 40) ** .55, .12 + .1 * k / 40, float(np.sin(k)) * .5)
add(fx, whoosh(.3, 1), tEnd - .1, .3); add(fx, thump(.9, 48), tEnd, .5)
fx += np.repeat(lp(brown(DUR), 400)[:N, None] * .012, 2, axis=1).astype(np.float32)
x, sr = sf.read('voice.wav'); x = x if x.ndim == 1 else x.mean(1); x = soxr.resample(x, sr, SR); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .11
add(voc, x, 0.0, 1.0, 0)
from scipy.ndimage import uniform_filter1d, maximum_filter1d
g = np.where(np.abs(voc[:, 0]) > .01, .35, 1.0); g = uniform_filter1d(1 - maximum_filter1d(1 - g, int(.4 * SR)), int(.25 * SR)); mus *= g[:, None]
out = mus * 3.0 + fx * .8 + voc; tail = int(1.0 * SR); out[-tail:] *= np.linspace(1, 0, tail)[:, None]
out = np.stack([limit(out[:, c], .42) for c in range(2)], 1); os.makedirs('out', exist_ok=True); sf.write('out/mix.wav', out.astype(np.float32), SR); print('mix ok', round(DUR, 2))
