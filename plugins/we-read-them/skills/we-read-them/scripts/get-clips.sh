#!/bin/sh
# Download news clips for commentary (fair use) into <raw dir>. Usage: get-clips.sh <raw dir> <youtube id> [...]
# If YouTube says "confirm you're not a bot": you are on a datacenter IP (VPN / exit node). Download from a home IP.
# Subtitles are best effort: YouTube rate-limits them (HTTP 429), and a failed subtitle must not stop the batch.
D=$1; shift; mkdir -p "$D"; cd "$D" || exit 1
for id in "$@"; do
  [ -f "$id.mp4" ] && { echo "have $id"; continue; }
  yt-dlp --no-playlist -f 'bv*[height<=1080]+ba/b' --merge-output-format mp4 -o '%(id)s.%(ext)s' --write-info-json \
    --sleep-requests 1 "https://www.youtube.com/watch?v=$id" || echo "FAILED $id"
done
ls "$D"/*.mp4 2>/dev/null | wc -l
