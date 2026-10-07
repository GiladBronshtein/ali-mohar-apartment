#!/bin/bash
# Re-render the 17 gallery images with the current model: Cycles on the GPU (Metal), resumable (logs/gallery_progress.txt).
# Needs apartment.glb + views.json from exportglb.mjs (server on :8765 serving source/, assets symlinked).
cd "$(dirname "$0")"; export GPU=1; PY=.venv-bpy/bin/python; SPP=${SPP:-128}
mkdir -p logs out; touch logs/gallery_progress.txt
run() { grep -q "^$1-$2 done" logs/gallery_progress.txt && return
  m=$2; [ "$4" = lit ] && m=lit
  $PY cycles_render.py $1 $m $SPP 1440 900 out/gal-$1-$2.png $3 > logs/gal-$1-$2.log 2>&1 &&
  python3 -c "from PIL import Image; Image.open('out/gal-$1-$2.png').convert('RGB').save('../renders/$1-$2.jpg', quality=90, optimize=True)" &&
  echo "$1-$2 done $(date +%T)" >> logs/gallery_progress.txt; }
run kitchen day 2.7; run kitchen2 day 2.7; run kitchen3 day 2.7; run island day 2.7; run storage day 2.7; run hall day 2.7
run master day 2.7; run entry day 2.7; run tvwall eve -0.3; run shower day 0.45 lit; run bath2 day 0.45 lit
run room2 day 2.7; run room3 day 0.6 lit; run balcony day 1.6; run balcony2 day 1.6; run view day 1.6; run entry eve -0.3
echo "ALLDONE $(date +%T)" >> logs/gallery_progress.txt
