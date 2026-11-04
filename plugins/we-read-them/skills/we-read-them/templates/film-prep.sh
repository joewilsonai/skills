#!/bin/sh
# raw/ -> assets/: news-clip frames (30 fps, greyscale, channel bugs cropped), clip audio, FBI and deposition pages.
set -e
D=$(cd "$(dirname "$0")/.." && pwd); cd "$D"
A=assets; R=raw
ff() { ffmpeg -v error -y "$@"; }
clip() { # name src start dur cropfilter
  mkdir -p $A/$1; rm -f $A/$1/*.jpg
  ff -ss $3 -t $4 -i $R/$2 -an -vf "$5,scale=1280:-2:flags=lanczos,format=gray,fps=30" -q:v 3 $A/$1/%03d.jpg
  ff -ss $3 -t $4 -i $R/$2 -vn -ac 1 -ar 48000 $A/snd/$1.wav
}
# Bethune GoPro (WFLA raw), the van at Spread Creek; crop the right side (their arrow) and their logo
clip van   lkZOmm28zXg.mp4 103.0 11.0 "crop=iw*0.62:ih*0.86:0:0"
# North Port chief, Sept 16 2021: "All I'm gonna say is I know where Brian's at." (FOX 13 bug cropped)
clip chief 9wWJsp6tjxY.mp4 43.45 2.0  "crop=iw:ih*0.80:0:0"
# North Port PD spokesman Josh Taylor: "We thought that we'd seen Brian initially come back into that home on that Wednesday."
clip taylor 9wWJsp6tjxY.mp4 60.5 5.5  "crop=iw:ih*0.74:0:0"
# Moab bodycam (Times-Independent raw upload), Aug 12 2021 16:48: "we got a call about a male hitting a female..."
clip moab  v5ZTa7RqHcU.mp4 60.15 4.5  "crop=iw:ih:0:0"
# Joseph Petito, family news conference, Sept 27 2021 (CBS New York): "...it's not just Gabby that deserves that."
clip father oa9JwNZg2ec.mp4 877.9 7.4 "crop=iw*0.8:ih*0.72:iw*0.1:ih*0.09"
# Documents: FBI Vault part 01 p.81 (FD-302 Gainesville), p.292 (FD-597 receipt); depositions
pdftoppm -r 200 -gray -f 81 -l 81 -png -singlefile $R/docs/vault-01.pdf $A/fbi_p81
pdftoppm -r 200 -gray -f 292 -l 292 -png -singlefile $R/docs/vault-01.pdf $A/fbi_p292
for f in van chief taylor moab father; do printf "%s %s  " $f "$(ls $A/$f | wc -l)"; done; echo
