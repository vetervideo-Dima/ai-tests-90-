#!/bin/bash
# Координатор: finish_test.sh N tokens tool_uses duration_ms — записать расход и закоммитить тест.
cd "$(dirname "$0")/.." || exit 1
python3 tools/record_usage.py "$1" "$2" "$3" "$4" >/dev/null || exit 1
d=$(ls -d tests/$(printf %02d $1)-*)
find "$d" -name node_modules -prune -o -type f -size +15M -print | sed 's/^/BIG: /'
git add "$d" COSTS.md && git commit -q -m "Test $(basename $d): v1 + v2

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01YPyUzrxfpeEHgdbMWAR9Wk" && echo "committed $(basename $d) $(du -sh $d | cut -f1) worked=$(python3 -c "import json;m=json.load(open('$d/meta.json'));print(m.get('worked'), 'v1:', m.get('v1_worked'))")"
