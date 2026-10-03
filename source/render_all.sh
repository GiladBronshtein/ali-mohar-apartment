#!/bin/bash
# full re-render after the plan details + physical audit. Bathrooms and the mamad: daylight + interior lights on ('lit').
cd "$(dirname "$0")"
run() { grep -q "^$1 $2 done" logs/progress.txt 2>/dev/null && [ -f renders/$1-$2.jpg ] && return
  m=$2; [ "$4" = lit ] && m=lit
  python3 cycles_render.py $1 $m 48 1440 900 out/final-$1-$2.png $3 > logs/$1-$2.log 2>&1 &&
  python3 -c "from PIL import Image; Image.open('out/final-$1-$2.png').convert('RGB').save('renders/$1-$2.jpg', quality=90, optimize=True)" &&
  echo "$1 $2 done $(date +%T)" >> logs/progress.txt; }
touch logs/progress.txt
run kitchen day 2.7
run kitchen2 day 2.7
run kitchen3 day 2.7
run island day 2.7
run storage day 2.7
run hall day 2.7
run entry day 2.7
run tvwall eve -0.3
run master day 2.7
run shower day 0.45 lit
run bath2 day 0.45 lit
run bath day 0.45 lit
run room1 day 2.7
run room2 day 2.7
run room3 day 0.6 lit
run balcony day 1.6
run balcony2 day 1.6
run view day 1.6
run entry eve -0.3
echo ALLDONE >> logs/progress.txt
