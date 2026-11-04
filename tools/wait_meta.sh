#!/bin/bash
# Координатор: ждёт до $1 секунд появления нового meta.json в tests/ (для фоновых прогонов).
cd "$(dirname "$0")/.." || exit 1
start=$(ls tests/*/meta.json 2>/dev/null | wc -l)
for ((i=0;i<$1;i+=10)); do
  now=$(ls tests/*/meta.json 2>/dev/null | wc -l)
  if [ "$now" -gt "$start" ]; then echo "new meta.json: $(git status --porcelain tests | grep meta.json)"; exit 0; fi
  sleep 10
done
echo "timeout; meta count $start"
