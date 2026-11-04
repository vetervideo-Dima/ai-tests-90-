#!/usr/bin/env python3
"""Записывает расход субагента в tests/NN-*/meta.json и строку в COSTS.md.

python3 tools/record_usage.py NN <subagent_tokens> <tool_uses> <duration_ms> [--stage v1+v2]

Стоимость — оценка (API-эквивалент), модель расчёта — tools/cost.py.
"""
import json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(ROOT / "tools"))
from cost import estimate

n = int(sys.argv[1]); tokens = int(sys.argv[2]); tools = int(sys.argv[3]); ms = int(sys.argv[4])
stage = sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "v1+v2"
folder = next((ROOT / "tests").glob(f"{n:02d}-*"))
mp = folder / "meta.json"
meta = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
usage = meta.get("usage", {})
runs = usage.get("runs", [])
runs.append({"stage": stage, "subagent_tokens": tokens, "tool_uses": tools, "duration_ms": ms})
tot_ms = sum(r["duration_ms"] for r in runs)
meta["usage"] = {
    "runs": runs,
    "total_tokens": sum(r["subagent_tokens"] for r in runs),
    "processed_tokens": sum(estimate(r, cfg)[1] for r in runs),
    "total_minutes": round(tot_ms / 60000, 1),
    "est_usd": round(sum(estimate(r, cfg)[0] for r in runs), 2),
    "note": "оценка: API-эквивалент по модели tools/cost.py, не реальное списание",
}
mp.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

costs = ROOT / "COSTS.md"
line = (f"| {folder.name} | {cfg.get('model') or '—'} | {meta.get('effort', 'high')} | {stage} | {tokens:,} | "
        f"{tools} | {ms/60000:.1f} | ≈${estimate(runs[-1], cfg)[0]:.2f} | {datetime.date.today()} |\n").replace(",", " ")
with costs.open("a", encoding="utf-8") as f:
    f.write(line)
print(folder.name, meta["usage"])
