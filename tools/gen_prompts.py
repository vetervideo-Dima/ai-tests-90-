#!/usr/bin/env python3
"""Генерирует tests/NN-slug/PROMPT.md.

01–50: промпты дословно из docs/HANDOFF.md (раздел 6) + корректировки раздела 5.
71–96: адаптации подборки ChatGPT (сюжеты для генераторов картинок/видео, переведённые в code-тесты).
Существующие PROMPT.md не перезаписываются (флаг --force — перезаписать).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = (ROOT / "docs/HANDOFF.md").read_text(encoding="utf-8")
FORCE = "--force" in sys.argv

SYSTEM = ("You are a world-class creative technologist. Output exactly one complete, self-contained file in a single "
          "code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module "
          "import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use "
          "devicePixelRatio.")

VENDOR_NOTE = ("Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее "
               "того, что написано в промпте. Исключение: Google Fonts.")

CORRECTIONS = {
    4: "Вместо фото — сгенерированные SVG/CSS-заглушки. Tailwind — из `vendor/tailwindcss/tailwind.browser.js`.",
    8: "Remotion: код + попытка рендера в MP4 (Chromium: `/opt/pw-browsers/chromium`); если headless Chrome недоступен — команда для локального рендера.",
    9: "Remotion: код + попытка рендера в MP4 (Chromium: `/opt/pw-browsers/chromium`); если headless Chrome недоступен — команда для локального рендера.",
    10: "Remotion: код + попытка рендера в MP4 (Chromium: `/opt/pw-browsers/chromium`); если headless Chrome недоступен — команда для локального рендера.",
    11: "Manim: код + попытка рендера; если LaTeX не ставится — команда для локального запуска.",
    12: "Manim: код + попытка рендера; если LaTeX не ставится — команда для локального запуска.",
    13: "Текстовый результат — в `result.md`. Карточка в галерее — текстовая.",
    14: "Текстовый результат — в `result.md`. Карточка в галерее — текстовая.",
    15: "Текстовый результат — в `result.md`. Карточка в галерее — текстовая.",
    18: "GSAP — из `vendor/gsap/`, не с CDN.",
    20: "JSON + страница-плеер на lottie-web из `vendor/`, проверка валидности JSON.",
    27: "`.pov` + рендер POV-Ray (установлен: `povray`); иначе команда для локального запуска.",
    31: "Микрофон необязателен, по умолчанию — генерируемый drone. На GitHub Pages (https) микрофон доступен.",
    36: "Шейдер обернуть в HTML-просмотрщик (WebGL, uniform iTime/iResolution); исходник mainImage — отдельным файлом.",
    38: "Оригинал на Python; в v2 — добавить веб-порт на canvas или p5.js для галереи.",
    39: "Оригинал на Python; в v2 — добавить веб-порт на canvas или p5.js для галереи.",
    40: "Оригинал на Python; в v2 — добавить веб-порт на canvas или p5.js для галереи.",
    42: "Three.js — из `vendor/` через importmap (не jsdelivr).",
    50: "Оригинал на Python; в v2 — добавить веб-порт на canvas или p5.js для галереи.",
}

WAVES = {
    1: [41, 43, 45, 46, 47, 48, 5, 6, 31, 35, 42, 21],
    2: [30, 32, 33, 34, 36, 37, 29],
    3: [1, 2, 3, 4, 7, 17, 18, 19, 22],
    4: [23, 24, 25, 26, 27, 28, 38, 39, 40, 44, 49],
    5: [8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 50],
    8: list(range(71, 81)),
    9: list(range(81, 88)),
    10: list(range(88, 97)),
}
WAVE_OF = {n: w for w, ns in WAVES.items() for n in ns}

FORMATS = {
    1: "HTML", 2: "HTML", 3: "HTML (v2 — второе сообщение)", 4: "HTML (Tailwind)", 5: "HTML + three",
    6: "HTML, raw WebGL", 7: "HTML", 8: "React / Remotion", 9: "Remotion-проект", 10: "Remotion",
    11: "Python / Manim", 12: "Python / Manim", 13: "Текст → result.md", 14: "Текст → result.md",
    15: "Текст → result.md", 16: "HTML → WebM", 17: "HTML + SVG", 18: "HTML + GSAP", 19: "HTML",
    20: "Lottie JSON + плеер", 21: "HTML + WebGL", 22: "SVG (анимированный)", 23: "SVG", 24: "SVG", 25: "SVG",
    26: "6 SVG + HTML-сетка", 27: ".pov (POV-Ray)", 28: "HTML + SVG", 29: "HTML → SVG", 30: "HTML",
    31: "HTML + three", 32: "HTML + WebGL2", 33: "HTML + WebGL", 34: "HTML + three", 35: "HTML + three",
    36: "GLSL + HTML-просмотрщик", 37: "HTML + WebGL", 38: "Python; в v2 веб-порт",
    39: "Python; в v2 веб-порт", 40: "Python; в v2 веб-порт", 41: "HTML + three", 42: "HTML + three",
    43: "HTML + three", 44: "HTML", 45: "HTML + three", 46: "HTML + three", 47: "HTML", 48: "HTML",
    49: "HTML", 50: "Python; в v2 веб-порт",
}


def kind_of(n, fmt):
    f = fmt.lower()
    if n in (13, 14, 15, 96):
        return "text"
    if n in (8, 9, 10, 11, 12):
        return "video"
    if n == 27:
        return "image"
    if n in (38, 39, 40, 50):
        return "python"
    if f.startswith("svg"):
        return "svg"
    return "html"


def parse_handoff():
    sec = HANDOFF.split("## 6.")[1].split("## 7.")[0]
    genre = ""
    tests = {}
    lines = sec.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        g = re.match(r"### Жанр \d+\. (.+)", ln)
        if g:
            genre = g.group(1).strip()
        m = re.match(r"\*\*(\d\d)-([a-z0-9-]+)\*\* — (.+)", ln)
        if m:
            n, slug, desc = int(m.group(1)), m.group(2), m.group(3).strip()
            # блок кода
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            k = j + 1
            body = []
            while not lines[k].startswith("```"):
                body.append(lines[k])
                k += 1
            # хвост до следующего теста/жанра
            tail = []
            t = k + 1
            while t < len(lines) and not lines[t].startswith("**") and not lines[t].startswith("###"):
                if lines[t].strip():
                    tail.append(lines[t].strip())
                t += 1
            tests[n] = dict(n=n, slug=f"{n:02d}-{slug}", genre=genre, desc=desc, prompt="\n".join(body), extra=tail)
            i = t
            continue
        i += 1
    return tests


# ---------------------------------------------------------------- 71–96
G_MATTER = "Материя складывается в слово / бесконечные шейдеры (адаптация)"
G_PRODUCT = "3D-предметка и интерьеры (адаптация)"
G_VECTOR = "Вектор, моушен, обложки, текст (адаптация)"
NEW = [
    (71, "bubbles-my-way", G_MATTER, 20, "Runway Gen-3 (видео: текст из мыльных пузырей)", "HTML + three",
     "Slow-motion macro in Three.js, single HTML file: soap bubbles drift on a pure black background. Each bubble has physically inspired thin-film iridescence (view-dependent interference colors, fresnel rim, subtle wobbling surface, faint reflections). The bubbles gather and merge into the words \"MY WAY\" built from many small bubbles, hold and wobble, then pop and drift apart into rainbow chaos. Shallow depth of field, soft bokeh, seamless 12-second loop, click to replay."),
    (72, "lava-lamp-love", G_MATTER, 21, "Runway Gen-3 (видео: лава-лампа)", "HTML + WebGL",
     "Raymarched lava lamp, single HTML file (WebGL fragment shader or Three.js full-screen quad): a glass lava lamp in a dark room, glowing wax blobs as smooth-min SDF metaballs that rise, stretch and sink with buoyancy, warm red-orange subsurface glow lighting the glass. Every cycle the blobs flow together and form the word \"LOVE\", hold for a moment, then melt apart. Cinematic close-up, slow orbit, bloom, hypnotic and seamless."),
    (73, "smoke-words", G_MATTER, "22 + 40", "Runway Gen-3 (видео: дым складывается в слово)", "HTML + WebGL",
     "GPU smoke simulation in one HTML file (stable-fluids on WebGL ping-pong framebuffers). Scene 1: an industrial cyberpunk wall with symmetrically arranged pipes venting yellow smoke; the smoke is steered toward a target field so it forms the word \"FUTURE\" in glowing bold letters, which glow, grow, flicker and dissipate. Scene 2: candles on black emit colorful smoke that billows into the word \"PEACE\" and then disperses. Button to switch scenes, mouse stirs the smoke, looping forever."),
    (74, "paint-art", G_MATTER, 23, "Runway Gen-3 (видео: струи краски)", "HTML + WebGL",
     "Slow-motion fluid paint in one HTML file (WebGL): on a black background, streams of red, blue and yellow paint pour from above and flow into the word \"ART\" in marbled, calligraphic letters. Colors mix like real paint (no muddy RGB averaging), glossy wet highlights from the surface gradient, drips and tendrils. Holds the word, then slowly marbles away; click to pour again."),
    (75, "diamonds-love", G_MATTER, 24, "Runway Gen-3 (видео: бриллианты складываются в слово)", "HTML + three",
     "Three.js, single HTML file: start with an extreme macro of a faceted brilliant-cut diamond with real refraction and dispersion (custom shader with internal ray bounces and rainbow fire). The camera slowly pulls back to reveal dozens of diamonds arranged to spell \"LOVE\" in large letters. Swirling mist, black background, sparkling highlights, bloom. 15-second seamless loop."),
    (76, "fireflies-hope", G_MATTER, 25, "Runway Gen-3 (видео: светлячки)", "HTML + three",
     "Three.js night forest clearing, single HTML file: procedural trees, moonlight, ground fog. Thousands of fireflies with blinking bioluminescent glow wander on curl noise, then swarm together to form the word \"HOPE\" in soft golden light, twinkle, and dissolve back into the forest. Slow cinematic pan, bloom, ambient Web Audio crickets and wind (click to start)."),
    (77, "powers-of-ten-zoom", G_MATTER, 27, "Kling AI Infinite Zoom (видео)", "HTML + WebGL",
     "Infinite zoom loop in one HTML file (WebGL): start with Earth from space and zoom continuously into a coastline, a city, a single leaf, plant cells, a molecule, then into a swirling cosmic fractal that becomes a galaxy and finally Earth again — a seamless, never-ending loop. Every level is procedural; transitions are hidden inside the motion. A small scale label shows 10^n meters."),
    (78, "kaleidoscope-crystal", G_MATTER, "28 + 41", "Runway / Kling (видео: зум в кристалл, плазма)", "HTML + WebGL",
     "Fragment shader in one HTML file (WebGL): an endless zoom into a kaleidoscopic crystal-and-plasma mandala — 6- to 12-fold mirror symmetry, faceted crystal refraction look, neon plasma streams flowing between facets, palette drifting from pastel to neon. Ethereal, dreamy, hypnotic; never visibly repeats. Click to change the symmetry order."),
    (79, "fractal-valley", G_MATTER, 34, "Kaiber.ai (видео: фрактальная долина)", "HTML + WebGL",
     "Raymarched psychedelic fractal landscape in one HTML file (WebGL fragment shader): the camera flies forever through a valley of folded-space fractal mountains (kaleidoscopic IFS), with glowing rivers in the canyon floor, volumetric fog and a slowly cycling color palette. No visible repetition. Adaptive resolution to hold 60 FPS."),
    (80, "neon-audio-grid", G_MATTER, "38 + 39 + 42", "Firefly / Runway (видео: неон, сетка, музыка)", "HTML + three",
     "Audio-reactive neon light show in one HTML file: a generated 128 BPM techno track in Web Audio (kick, hats, bass, a simple lead; click to start). Three.js scene: a synthwave wireframe grid receding to the horizon, glowing purple, blue and pink lines and geometric shapes that pulse and dance to the analyser bands, a sun on the horizon, bloom, the camera bumping on every kick."),
    (81, "perfume-shot", G_PRODUCT, 3, "Flux / SDXL (рекламное фото парфюма)", "HTML + three",
     "Three.js product shot, single HTML file: a premium men's perfume bottle — dark matte rectangular glass with a gold metallic cap — centered on a 20×20 cm black polished acrylic pedestal that shows a crisp mirror reflection. A soft backlight creates a halo around the bottle, a narrow side light from the left emphasizes its edges, the background is pure deep black. Three dark burgundy rose petals lie casually beside it. Physically based materials (transmission, roughness, clearcoat), slow turntable, a button to cycle lighting presets. No text, no logos."),
    (82, "topaz-ring", G_PRODUCT, 4, "SDXL / DALL·E 3 (каталожное фото кольца)", "HTML + three",
     "Three.js macro product shot, single HTML file: an 18-karat gold ring with an oval 8×6 mm blue topaz in a halo of eight small diamonds, lying on bleached linen with a visible weave (procedural texture). Shot from above at a 30° angle; two soft lights at 45° from either side remove shadows; pure white background. The topaz is perfectly clear with internal reflections and sparkle, polished gold shows sharp highlights. Macro depth of field, drag to rotate."),
    (83, "barbershop-night", G_PRODUCT, 11, "SDXL / Nano Banana Pro (ночная вывеска)", "HTML + three",
     "Three.js night street, single HTML file: a small European street with wet cobblestones reflecting the lights. Center: a barbershop entrance — wooden door with frosted glass, above it a rectangular patinated brass sign with embossed letters \"BARBERIAN\", to the right a classic red-white-blue barber pole spinning and lit from within. Warm orange interior light and silhouettes of people behind the window, light rain. Slow dolly-in; the sign text must be crisp and undistorted."),
    (84, "japandi-room", G_PRODUCT, "13 + 49", "SDXL / Imagen (интерьер Japandi, лофт)", "HTML + three",
     "Architectural visualization in Three.js, single HTML file: a spacious 40 m² Japandi living room with 3 m ceilings — light oak floor, a low wooden sofa with cream linen upholstery and three beige cushions, an oak-and-black-metal coffee table with a ceramic vase holding one eucalyptus branch and a stack of books, a rice-paper floor lamp, a large abstract watercolor in a thin frame, a floor-to-ceiling window with blurred greenery outside. Soft natural daylight, ambient occlusion feel, everything modeled procedurally. Orbit camera, a day/evening toggle and a \"loft\" variant (exposed brick, leather couch, Edison bulbs, plants)."),
    (85, "space-kids-room", G_PRODUCT, 15, "SDXL / Midjourney (детская комната)", "HTML + three",
     "Three.js, single HTML file: a 7-year-old's space-themed bedroom — dark blue ceiling with twinkling star lights and a pink-purple nebula projection, a built-in white rocket-shaped capsule bed with orange accents and a round porthole nightlight, pull-out drawers, a large solar-system mural with labels, light grey carpet, a desk with a lamp by the window. Soft evening light, magazine-quality styling. Click the nightlight to switch to night mode where the ceiling becomes a planetarium."),
    (86, "dystopian-room", G_PRODUCT, 31, "NeRF / 3D (антиутопическая комната)", "HTML + three",
     "Three.js, single HTML file: an abandoned room in a dystopian city — overturned furniture, dust motes in light shafts, a cold blue neon sign flickering on the wall, a broken window revealing a ruined skyline with smoke, searchlights and distant lightning. Fully procedural, volumetric light, a 360° orbit camera the user can drag."),
    (87, "dancing-camel", G_PRODUCT, 47, "DreamFusion (text-to-3D, glTF)", "HTML + three",
     "Three.js, single HTML file: a cartoon camel built procedurally (no assets) with a real skeleton (SkinnedMesh + bones), performing a looping keyframed dance synced to a generated Web Audio beat (click to start). Toon shading, a desert stage with spotlights and a starry sky. An \"Export glTF\" button downloads the animated model via GLTFExporter."),
    (88, "soviet-poster", G_VECTOR, 10, "SD / DALL·E 3 (ретро-плакат)", "HTML + SVG",
     "Single HTML file with an inline SVG poster (A2 proportions) in 1930s Soviet constructivist style: a worker in overalls holding a laptop with an outstretched arm, gazing into the distance; strong diagonal composition; limited palette of red, white, black and ochre. Large headline «АВТОМАТИЗИРУЙ!» in bold era-appropriate lettering, small text at the bottom «Нейросеть — инструмент нового времени». Worn paper texture via SVG filters. All Cyrillic lettering crisp and undistorted. A \"Download SVG\" button."),
    (89, "train-and-wolf", G_VECTOR, "18 + 19", "VectorFusion / Firefly Vector", "SVG",
     "Generate two separate SVGs, each in its own code block: (1) a train — minimal flat 2D vector icon, lineal color, on a white background; (2) a vector logo: an arctic wolf silhouette with elements of the northern lights, minimalist flat colors, sharp geometry. Clean, scalable paths."),
    (90, "pattern-studio", G_VECTOR, "16 + 17 + 33 + 45", "Midjourney --tile / SD tiling", "HTML → SVG",
     "Single HTML \"Pattern Studio\" that generates seamless, tileable SVG patterns: (1) vintage watercolor flowers and birds (SVG turbulence/displacement for a watercolor look), (2) Seigaiha waves in alcohol-ink blue and gold, (3) minimalist pastel geometric shapes, (4) a green-blue fractal texture. A live 3×3 tiling preview proves the seams are invisible. Seed and palette controls, \"Download SVG tile\" and \"Download PNG tile\" buttons."),
    (91, "fox-watercolor", G_VECTOR, 8, "Midjourney / SDXL (детская акварель)", "SVG",
     "Generate an SVG illustration (1200×900) for a children's book (ages 6+): a fox girl in a blue apron and white blouse sits in a big armchair by a roaring fireplace, wrapped in a checkered blanket, reading a thick open book. A stack of books and a steaming mug of tea on the floor; through the window, a snowy winter evening. Warm firelight on the fur and walls. Watercolor look (SVG filters: turbulence, displacement, soft edges), warm palette of ochre, terracotta and cream, gentle line work, a subtle animated firelight flicker."),
    (92, "whiteboard-doodle", G_VECTOR, 35, "Veed / Doodle AI (дудл-анимация)", "HTML + SVG",
     "Whiteboard doodle animation in one HTML file with inline SVG: a hand-drawn black marker sketches a smiley face, a heart and the word \"HELLO\" (stroke draw-on, slightly wobbly boiling line), a marker cursor follows the stroke, then all three converge and morph into a single combined image. 10-second loop, replay button."),
    (93, "ui-morph", G_VECTOR, 30, "Runway Gen-4 (UI motion)", "HTML + GSAP",
     "UI motion design in one HTML file with GSAP: a 15-second sequence showing the evolution of an interface — a phone app screen morphs into a tablet layout and then a desktop web layout, cards reflowing with FLIP transitions, smooth camera moves, minimal text, polished easing. Timeline scrubber and replay button."),
    (94, "thumbnails-in-code", G_VECTOR, "6 + 7", "SDXL / GPT Image / Ideogram (обложки)", "HTML",
     "Single HTML file producing two thumbnails in pure HTML/CSS/SVG (no photos — illustrated people): (1) YouTube 1920×1080: gradient from deep navy on the left to black on the right, a surprised 30-year-old man's face in the left third lit by cool blue monitor light, big bold white headline \"ChatGPT vs Gemini\", smaller grey subtitle \"Кто лучше в 2026?\", a yellow lightning bolt in the bottom right; (2) Reels 1080×1920: a smiling 25-year-old woman in a vivid yellow oversized sweater on pure white, the top third holding the headline «КАК Я ПОХУДЕЛА НА 8 КГ» in two lines of bold black sans-serif, the bottom quarter empty for captions. Both legible at small size; \"Download PNG\" buttons."),
    (95, "fitness-landing-short", G_VECTOR, 29, "MS Designer / Uizard (макет сайта)", "HTML",
     "Website homepage design: a modern landing page for a fitness app. Header banner with gym image, clear CTA buttons. Color scheme: yellow and gray. Style: minimal flat design with clean UI."),
    (96, "photo-prompt-doctor", G_VECTOR, "1 + 2 + 5", "SDXL / Nano Banana Pro / Midjourney (фото-промпты)", "Текст → result.md",
     "Here are three photo prompts written for image models:\n"
     "(1) \"A business portrait of a 38-year-old female executive with European features: shoulder-length straight dark hair, wearing a smart black jacket with a thin white stripe and small gold stud earrings. She looks calmly confident into the camera. Studio lighting: a large softbox to the left and a narrow rim light on the right to highlight facial contours. Neutral dark gray seamless background. Shot with an 85mm lens at f/2.0 for shallow depth of field (focus on eyes, slight blur on ears/shoulders). Skin is highly detailed (visible pores, minimal smoothing).\"\n"
     "(2) \"A 32-year-old fair-skinned man with a three-day red stubble and slightly tousled hair, wearing a white linen shirt with rolled-up sleeves. He is seated by a large window, looking thoughtfully just off camera. Morning diffuse light enters from the left, casting soft shadows on the right side of his face. In the background, a café interior is visible out of focus (warm wood tones). Shot on 50mm at f/1.8. Cinematic color grading: cool blue in shadows, warm creamy highlights.\"\n"
     "(3) \"A pair of clean white low-top sneakers on a wet dark asphalt at night. Shot from ground level at a 10° upward angle, emphasizing the sole and silhouette. The wet pavement shows blurred reflections of city lights. Background: a defocused city street at night – warm orange street lamps on the right, cool blue shop window light on the left, large soft bokeh. Backlighting from a street lamp behind-left creates a glowing rim along the top edge of the sole. Shot on 35mm f/1.4.\"\n"
     "For each prompt: give a short critique (what is strong, what is ambiguous or will likely fail), then rewrite it separately for Nano Banana Pro, Midjourney v7, Flux and GPT Image, using each model's preferred structure and parameters, with a negative-cue line where the model supports it. Finish with a one-paragraph checklist of the 7 most important rules for photoreal prompts."),
]


def write_prompt(t):
    folder = ROOT / "tests" / t["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    p = folder / "PROMPT.md"
    if p.exists() and not FORCE:
        return
    is_html = t["fmt"].startswith("HTML")
    lines = [f"# {t['n']:02d} · {t['title']}", ""]
    lines += [f"- **Жанр:** {t['genre']}",
              f"- **Источник:** {t['source']}",
              f"- **Формат выхода:** {t['fmt']}",
              f"- **Волна:** {t['wave'] if t['wave'] else '—'}"]
    corr = CORRECTIONS.get(t["n"])
    notes = [c for c in (corr, VENDOR_NOTE if is_html else None) if c]
    if notes:
        lines.append("- **Корректировка для облачного режима:** " + " ".join(notes))
    lines.append("")
    if is_html:
        lines += ["## Системный промпт", "", "```", SYSTEM, "```", ""]
    lines += ["## Промпт", "", "```", t["prompt"], "```", ""]
    for e in t.get("extra", []):
        lines += [e, ""]
    p.write_text("\n".join(lines), encoding="utf-8")


def title_of(slug):
    return " ".join(w.capitalize() if not w.isdigit() else w for w in slug.split("-")[1:])


def main():
    tests = []
    for n, t in sorted(parse_handoff().items()):
        fmt = FORMATS[n]
        tests.append(dict(n=n, slug=t["slug"], title=title_of(t["slug"]), genre=t["genre"],
                          source=t["desc"], fmt=fmt, prompt=t["prompt"], extra=t["extra"],
                          kind=kind_of(n, fmt), wave=WAVE_OF.get(n)))
    for n, slug, genre, orig, src, fmt, prompt in NEW:
        full = f"{n:02d}-{slug}"
        tests.append(dict(n=n, slug=full, title=title_of(full), genre=genre,
                          source=f"Адаптация подборки ChatGPT №{orig} (оригинал — промпт для {src}). "
                                 f"Сюжет тот же, но результат — код, а не растровая картинка/видео.",
                          fmt=fmt, prompt=prompt, extra=[], kind=kind_of(n, fmt), wave=WAVE_OF.get(n)))
    for t in tests:
        write_prompt(t)
    catalog = [{k: t[k] for k in ("n", "slug", "title", "genre", "source", "fmt", "kind", "wave")} for t in tests]
    (ROOT / "tools/catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(tests)} tests")


if __name__ == "__main__":
    main()
