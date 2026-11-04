#!/bin/sh
# Fetch an FBI Vault PDF part. vault.fbi.gov blocks scripts, so go through the Wayback Machine's capture of the download.
# Usage: vault-get.sh <vault path, e.g. brian-laundrie/brian-laundrie-part-05> <out.pdf>
set -e
P=$1; OUT=$2
TS=$(curl -s -m 60 "https://web.archive.org/cdx/search/cdx?url=vault.fbi.gov/$P/at_download/file&output=json&filter=statuscode:200&filter=mimetype:application/pdf&limit=1" | python3 -c "import json,sys; r=json.load(sys.stdin); print(r[1][1] if len(r)>1 else '')")
[ -n "$TS" ] || { echo "no archived PDF capture for $P"; exit 1; }
curl -sL -m 300 -o "$OUT" "https://web.archive.org/web/${TS}id_/https://vault.fbi.gov/$P/at_download/file"
file "$OUT" | grep -q PDF && echo "ok $OUT ($TS)" || { echo "not a PDF"; exit 1; }
