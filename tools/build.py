#!/usr/bin/env python3
"""Собирает сайт: tests/index.json, index.html (галерея) и tests/NN-slug/index.html (страница теста).

Источники: tools/catalog.json (список тестов из gen_prompts.py), tests/*/PROMPT.md, README.md, meta.json.
Запуск: python3 tools/build.py
"""
import html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cost import estimate

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "tools/catalog.json").read_text(encoding="utf-8"))
WAVE_NAMES = {}
for line in (ROOT / "waves.md").read_text(encoding="utf-8").splitlines():
    if line[:2].strip(". ").isdigit() and ". " in line:
        num, rest = line.split(". ", 1)
        WAVE_NAMES[int(num)] = rest.split(":")[0].strip()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" '
         'href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?'
         'family=Unbounded:wght@300;500;800&family=Manrope:wght@400;600;800&family=JetBrains+Mono:wght@400;600'
         '&display=swap" rel="stylesheet">')


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


def status_of(meta):
    if not meta:
        return "pending"
    if meta.get("status") in ("ok", "partial", "broken"):
        return meta["status"]
    return "ok" if meta.get("worked") else "broken"


def collect():
    items = []
    for c in CATALOG:
        d = ROOT / "tests" / c["slug"]
        meta = json.loads(read(d / "meta.json") or "null")
        entries = {}
        if meta and isinstance(meta.get("entry"), dict):
            for k, v in meta["entry"].items():
                if v and (d / v).exists():
                    entries[k] = v
        shots = {}
        for k in ("v1", "v2"):
            if (d / k / "screenshot.png").exists():
                shots[k] = f"{k}/screenshot.png"
        shot = "screenshot.png" if (d / "screenshot.png").exists() else (shots.get("v2") or shots.get("v1"))
        usage = (meta or {}).get("usage") or {}
        items.append({
            **c,
            "wave_name": WAVE_NAMES.get(c["wave"], ""),
            "status": status_of(meta),
            "entries": entries,
            "shots": shots,
            "shot": shot,
            "date": (meta or {}).get("date"),
            "v1_worked": (meta or {}).get("v1_worked"),
            "notes": (meta or {}).get("notes", ""),
            "v1_issues": (meta or {}).get("v1_issues", ""),
            "v2_changes": (meta or {}).get("v2_changes", ""),
            "effort": (meta or {}).get("effort") or CFG.get("effort"),
            "model": (meta or {}).get("model") or CFG.get("model"),
            "tokens": usage.get("total_tokens"),
            "minutes": usage.get("total_minutes"),
            "usd": round(sum(estimate(r, CFG)[0] for r in usage.get("runs", [])), 2) if usage.get("runs") else None,
            "runs": usage.get("runs", []),
            "files": sorted(str(p.relative_to(d)) for p in d.rglob("*")
                            if p.is_file() and "node_modules" not in p.parts and p != d / "index.html"),
        })
    return items


def page(title, body, depth, extra_head=""):
    pre = "../" * depth
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{FONTS}
<link rel="stylesheet" href="{pre}assets/site.css">
{extra_head}
</head>
<body>
{body}
</body>
</html>
"""


def build():
    items = collect()
    done = [i for i in items if i["status"] != "pending"]
    summary = {
        "total": len(items), "done": len(done),
        "ok": sum(i["status"] == "ok" for i in items),
        "v1_ok": sum(i["v1_worked"] is True for i in items),
        "tokens": sum(i["tokens"] or 0 for i in items),
        "usd": round(sum(i["usd"] or 0 for i in items), 2),
        "minutes": round(sum(i["minutes"] or 0 for i in items), 1),
    }
    site = {"config": CFG, "summary": summary, "waves": WAVE_NAMES}
    (ROOT / "tests/index.json").write_text(
        json.dumps({"site": site, "tests": [{k: v for k, v in i.items() if k != "files"} for i in items]},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    data = json.dumps({"site": site, "tests": items}, ensure_ascii=False).replace("</", "<\\/")
    gallery = f"""<div id="app"></div>
<script id="data" type="application/json">{data}</script>
<script type="module" src="assets/gallery.js"></script>"""
    (ROOT / "index.html").write_text(page(CFG["site_title"], gallery, 0), encoding="utf-8")

    for idx, i in enumerate(items):
        d = ROOT / "tests" / i["slug"]
        payload = {
            "site": site, "test": i,
            "prompt_md": read(d / "PROMPT.md"),
            "readme_md": read(d / "README.md"),
            "prev": items[idx - 1]["slug"] if idx > 0 else None,
            "next": items[idx + 1]["slug"] if idx + 1 < len(items) else None,
            "prev_title": items[idx - 1]["title"] if idx > 0 else None,
            "next_title": items[idx + 1]["title"] if idx + 1 < len(items) else None,
        }
        js = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
        body = f"""<div id="app"></div>
<script id="data" type="application/json">{js}</script>
<script type="module" src="../../assets/test.js"></script>"""
        (d / "index.html").write_text(page(f"{i['n']:02d} · {i['title']} — {CFG['site_title']}", body, 2),
                                      encoding="utf-8")
    print(f"built: {summary}")


if __name__ == "__main__":
    build()
