#!/usr/bin/env python3
"""patch_note.py NN "текст" — дописать пометку в meta.json → usage.note (например, о прерванном прогоне)."""
import json, sys
from pathlib import Path
d = next((Path(__file__).resolve().parent.parent / "tests").glob(f"{int(sys.argv[1]):02d}-*"))
m = json.loads((d / "meta.json").read_text(encoding="utf-8"))
m.setdefault("usage", {})["note"] = m["usage"].get("note", "") + " " + sys.argv[2]
(d / "meta.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
