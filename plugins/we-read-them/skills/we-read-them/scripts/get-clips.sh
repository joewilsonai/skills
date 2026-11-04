#!/bin/sh
# Download news clips for commentary (fair use) into <raw dir>. Usage: get-clips.sh <raw dir> <youtube id> [...]
# If YouTube says "confirm you're not a bot": you are on a datacenter IP (VPN / exit node). Download from a home IP.
set -e
D=$1; shift; mkdir -p "$D"; cd "$D"
for id in "$@"; do
  yt-dlp --no-playlist -f 'bv*[height<=1080]+ba/b' --merge-output-format mp4 -o '%(id)s.%(ext)s' --write-info-json \
    --write-auto-subs --sub-langs en --convert-subs srt "https://www.youtube.com/watch?v=$id"
done
