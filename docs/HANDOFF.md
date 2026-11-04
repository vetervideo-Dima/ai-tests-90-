# HANDOFF: репозиторий «50 красивых тестов для нейросетей»

Этот файл — перенос контекста из чата claude.ai. Прочитай его целиком и выполни раздел «Первый запуск».

## 1. Цель

Владелец — Дмитрий, видеопродюсер, YouTube-автор, преподаёт vibe coding и промпт-инжиниринг.
Задача: прогнать коллекцию визуально эффектных тестов нейросетей («один промпт — один результат», без computer use и MCP) на Claude Opus 5.5 с высоким effort. Результаты собрать в одном репозитории, по отдельным папкам, с галереей на GitHub Pages — для видео, шортов и курсов.

Вкус владельца: прежде всего красивые 3D/Three.js-сцены и симуляции (в духе тестов 41, 43, 45, 46, 47, 48).

Бюджет: около $900 облачного использования Opus. Ориентиры по цене (Opus 5.5: $4 вход / $20 выход за MTok, чтение кэша $0.20):
- лёгкий тест ≈ $0.4–1;
- средний ≈ $1–2;
- тяжёлый 3D ≈ $2–5;
- полный проход всех 50 ≈ $80–120.

После первого теста сверить реальный расход и записать его в `COSTS.md`.

## 2. Принятые решения

- **Структура:** одна папка на тест — `tests/NN-slug/`. Внутри:
  - `PROMPT.md` — промпт дословно, не редактировать;
  - `v1/` — чистый one-shot;
  - `v2/` — доработка;
  - `README.md`;
  - `meta.json`;
  - `screenshot.png` (если удалось).
- **v1 — честный тест.** Его делает субагент, который видит только PROMPT.md и CLAUDE.md, без чужих тестов.
- **v2 — доработка** после самопроверки: ошибки, свет, анимация, производительность, мобильная версия. Суть задачи не меняется.
- **Библиотеки** (three.js, gsap, p5, lottie-web и т.д.) ставятся через npm и копируются в `vendor/`. Страницы подключают их по относительному пути через importmap. CDN не используем: песочница может их не пускать, а на GitHub Pages всё работает и так.
- **Один субагент на тест**, не больше 3 одновременно. Главная сессия только координирует и не тащит в контекст код тестов.
- **Волны** можно запускать параллельно в разных облачных сессиях. Каждая работает в своей ветке и делает свой PR. Общий `index.html` обновляется последним.
- **GitHub Pages:** main, корень. В корне `index.html` — галерея всех тестов: карточка, скриншот, ссылки на v1/v2, отметка «работает/нет».

## 3. Первый запуск (выполнить сейчас)

1. Создай файлы из раздела 4: `CLAUDE.md`, `.claude/commands/run-wave.md`, `waves.md`, `COSTS.md` (пустая таблица: тест, модель, effort, примерная стоимость, заметки).
2. Создай 50 папок `tests/NN-slug/` и в каждой `PROMPT.md` с промптом из раздела 6 (дословно). В шапку PROMPT.md добавь: название, жанр, источник, формат выхода и корректировку из раздела 5, если она есть.
3. Поставь npm-зависимости и разложи build-файлы в `vendor/`: three (вместе с examples/jsm/addons), gsap, p5, lottie-web.
4. Сделай заготовку `index.html` с галереей, которая строится из списка тестов (простой JSON `tests/index.json`).
5. Закоммить, ничего ещё не генерируя. Напиши, что готово, и предложи пилот: `/run-wave 41`.

## 4. Файлы

### CLAUDE.md
```markdown
# Репозиторий тестов нейросетей
Каждая папка tests/NN-name/ — один тест. Промпт — PROMPT.md, его НЕ редактировать.

Правила для каждого теста:
1. v1: результат строго по PROMPT.md, как ответ на одно сообщение. Без подсматривания в другие тесты.
2. Один самодостаточный файл (обычно v1/index.html). Библиотеки только из /vendor по относительному пути. Никаких CDN.
3. Проверка: локальный сервер (python -m http.server), headless-браузер (playwright), screenshot.png, проверка консоли на ошибки. Если браузер не ставится — проверка синтаксиса через node и честная отметка в README.
4. v2: исправь найденные ошибки и улучши визуал (свет, анимация, производительность, мобильная версия). Суть задачи не меняй.
5. README.md: 3–5 строк — что получилось, как открыть, что не удалось. meta.json: model, effort, date, worked (true/false), notes.
6. Python / Manim / Remotion / POV-Ray: код + попытка рендера; если не вышло — команда для локального запуска в README.
7. После волны: обнови tests/index.json и index.html, добавь строки в COSTS.md, закоммить.
```

### .claude/commands/run-wave.md
```markdown
Запусти волну тестов $ARGUMENTS (номер волны из waves.md или номер одного теста).
1. Прочитай CLAUDE.md и waves.md, определи список папок.
2. Для каждого теста запусти отдельного субагента (не больше 3 одновременно) и передай ему CLAUDE.md и путь к папке. Субагент: v1 → проверка → v2 → README → meta.json.
3. Сам код тестов в свой контекст не загружай — только координируй.
4. В конце обнови галерею и COSTS.md, закоммить и напиши сводку: что получилось, что сломалось, что стоит переделать.
```

### waves.md
```markdown
1. Флагманы 3D: 41, 43, 45, 46, 47, 48, 5, 6, 31, 35, 42, 21
2. Генеративка и шейдеры: 30, 32, 33, 34, 36, 37, 29
3. Сайты и моушен: 1, 2, 3, 4, 7, 17, 18, 19, 22
4. Вектор и игры: 23, 24, 25, 26, 27, 28, 38, 39, 40, 44, 49
5. Видео-код и прочее: 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 50
6. Новый 3D-пакет: см. раздел 7 HANDOFF.md (сначала создать PROMPT.md, потом прогнать)
7. Сравнение effort: 41, 42, 43, 45, 46, 31, 35, 5, 6, 21 — v1 при effort high против максимального, в папки v1-high/ и v1-max/
```

## 5. Корректировки для облачного режима

- **4:** вместо фото — сгенерированные SVG/CSS-заглушки.
- **8–10 (Remotion):** код + попытка рендера в MP4; если headless Chrome недоступен — команда для локального рендера.
- **11–12 (Manim):** код + попытка рендера; если LaTeX не ставится — команда для локального запуска.
- **13–15:** текстовые результаты в `result.md`. Карточка в галерее — текстовая.
- **20 (Lottie):** JSON + страница-плеер на lottie-web из vendor, проверка валидности JSON.
- **27 (POV-Ray):** .pov + попытка `apt install povray` и рендера; иначе команда для локального запуска.
- **31:** микрофон необязателен, по умолчанию генерируемый drone. GitHub Pages работает по https, так что микрофон там будет доступен.
- **36:** шейдер обернуть в HTML-просмотрщик (WebGL, uniform iTime/iResolution); исходник mainImage — отдельным файлом.
- **39, 40, 50 (Python desktop/terminal):** оригинал на Python; в v2 добавить веб-порт на p5.js или canvas для галереи.
- **Все HTML:** библиотеки только из vendor (это правило важнее того, что написано в промпте).

## 6. Пятьдесят тестов (промпты дословно)

Общий системный промпт для HTML-тестов — добавлять в начало каждого PROMPT.md, если это HTML:
```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```
(В этом репозитории вместо CDN — vendor/, см. раздел 5.)

### Жанр 1. Сайты и лендинги

**01-halcyon-landing** — Awwwards-лендинг с анти-slop брифом (по мотивам статьи Anthropic «Improving frontend design through Skills»). HTML.
```
Design a single-file landing page for "Halcyon", a fictional maker of handmade analog synthesizers. Commit to ONE bold aesthetic: Swiss-brutalist editorial meets 1970s Japanese hi-fi catalogues. No Inter/Roboto/Arial — distinctive Google Fonts with extreme weight contrast (100 vs 900); one dominant color + one sharp accent as CSS variables; no purple gradients, no generic rounded cards. Sections: full-viewport hero with an animated canvas oscilloscope line reacting to mouse; staggered scroll-reveal product grid (IntersectionObserver); horizontally scrolling "patch notes" timeline; specs table styled like a printed manual; footer with a giant outlined wordmark. Purposeful micro-interactions on every button. No frameworks.
```

**02-brutalist-typeface** — Brutalist website for a typeface maker (известный тест, Design Arena / HN). HTML.
```
Build a brutalist website for a typeface maker. Single HTML file. Fictional foundry "Grotesk & Sons". Include a live type tester (editable text, size/weight/tracking sliders on a variable Google Font), a glyph grid that zooms on hover, exposed grid lines, monospace metadata, harsh black/white with one signal color.
```

**03-retro-arcade-noir** — известный тест из OpenAI Cookbook «Frontend coding with GPT-5». HTML. v2 = второе сообщение.
```
Make me landing page for a retro-games store. Retro-arcade noir some might say
```
Второе сообщение (для v2): `Make it light, more pastel coloured & flowery`

**04-photo-portfolio-3d** — известный тест (commandcode.ai). HTML.
```
Create an elegant minimalist single-file HTML photography portfolio landing page for "Elena Voss Photography". Tailwind CSS. Hero: full bleed hero image with 3D floating frame effect around the main photo (CSS 3D + JS). Infinite scroll masonry grid that loads more images with smooth fade-ins. Clicking an image opens a 3D lightbox gallery. About section with subtle parallax. Journal / Stories section with scroll horizontal cards. Contact with elegant form. Use soft elegant typography, lots of whitespace, and tasteful 3D interactions. Very high aesthetic quality. Output complete HTML. Use generated SVG/CSS placeholders instead of photos.
```

**05-luxury-watch-3d** — расширение строки из галереи Gemini 3 Website Prompts. HTML + three.
```
Design a 3D product experience page for a luxury wristwatch (fictional "Meridian No. 7"). Build the watch procedurally in Three.js (case, engraved bezel, sapphire glass with transmission, hands showing the real current time). Scroll drives the camera: hero 3/4 view → exploded movement → dial macro → strap options (click to swap materials). Studio lighting, soft shadows, film grain. Single HTML, Three.js via import map.
```

**06-cloth-lab** — известный промпт (Medium, @augustozz). Бренд заменён на выдуманный. HTML, raw WebGL.
```
Create a complete, self-contained interactive demo as exactly one HTML file. Build a polished one-page "Interactive Cloth Lab" website with a dark cinematic UI, inspired by a high-end physics showcase. The page should feature a large wind-blown cloth flag/banner with the text "WINDHALL" mapped onto it. The cloth should feel physical, dimensional, and satisfying to watch. Do not use React, JSX, npm, bundlers, imports, modules, or external dependencies. Raw WebGL rendering. Control panel with sliders for turbulence, stiffness, and sheen; mouse drag pushes or tears the cloth.
```

**07-history-of-light** — оригинал. HTML.
```
Build a scroll-driven editorial longread "A Short History of Light" as one HTML file: 7 chapters (fire, candle, gas lamp, bulb, neon, LED, laser), each with a pinned full-screen canvas scene morphing by scroll progress, large serif drop caps, a progress bar shaped like a spectrum; page color temperature shifts per chapter. No libraries.
```

### Жанр 2. Видео (код или промпты)

**08-remotion-countdown** — известный тест (гайд Remotion). React/Remotion.
```
System: You are a Remotion component generator. Generate a single React component that uses Remotion. Rules: Export the component as a named export called "MyComposition"; Use useCurrentFrame() and useVideoConfig() from "remotion"; Prefer interpolate() with Easing over spring() unless physics-based motion is explicitly requested; Only output the code.
User: Create a countdown from 5 to 1 with smooth motion
```
Вариант (вторая композиция): `Create a text animation that types out "Hello World" letter by letter`

**09-remotion-record-store** — по мотивам документации плагина Remotion. Remotion-проект.
```
Write a complete Remotion project (Root.tsx + one composition, 1080x1920, 30fps, 15s) promoting a fictional record store "Groove Basement": vinyl spinning in with motion blur, kinetic typography of three taglines, a grid of 9 CSS/SVG album covers, price-tag stamp, logo outro. spring() for impacts, interpolate() for pans. Deterministic, no external assets. Full code with file paths.
```

**10-remotion-bar-chart** — известный тест (гайд Remotion).
```
Create a bouncy bar chart showing quarterly sales data — Remotion, 1920x1080, 8s: staggered spring bars, counting numbers, axis draw-in, glow on the best quarter. Named export MyComposition.
```

**11-manim-pythagoras** — известный промпт (блог Madio). Python/Manim.
```
Write a Manim Community Edition script: show the Pythagorean theorem visually, with a right triangle, squares on each side, and a morph showing a^2 + b^2 = c^2. Then a rearrangement proof (four triangles sliding inside a big square). Dark background, 3Blue1Brown-like palette, MathTex labels, ~40s. One Scene, include the render command.
```

**12-manim-fourier** — по мотивам 3brown1blue. Python/Manim.
```
Write a Manim CE script (one file, 3 Scenes) explaining the Fourier transform: (1) a signal built from 3 sines; (2) winding it around a circle at varying frequencies with a moving center-of-mass dot; (3) spectrum spikes appearing. On-screen captions. No deprecated APIs. Include render commands.
```

**13-tokyo-street-prompts** — известный промпт со страницы запуска Sora. Текст → result.md.
```
Here is a famous text-to-video prompt: "A stylish woman walks down a Tokyo street filled with warm glowing neon and animated city signage. She wears a black leather jacket, a long red dress, and black boots, and carries a black purse. She wears sunglasses and red lipstick. She walks confidently and casually. The street is damp and reflective, creating a mirror effect of the colorful lights. Many pedestrians walk about." Rewrite it for Veo, Kling, Seedance and Runway separately (shot type, lens, camera move, lighting, motion beats, ambience/audio line, negative cues), then write a 6-shot sequel storyboard as a numbered list.
```

**14-mammoths-storyboard** — по мотивам промпта Sora. Текст → result.md.
```
Take the Sora demo prompt about giant wooly mammoths treading through a snowy meadow under snow-capped mountains in warm mid-afternoon light. Turn it into a 30-second nature-documentary sequence: 8 shots with duration, framing, lens, camera move and a one-sentence image-to-video prompt each, plus voice-over and music cues, with continuity notes (light direction, fur color, snow density).
```

**15-spaghetti-test** — по мотивам «спагетти-теста», с оригинальным персонажем. Текст → result.md.
```
Write 5 escalating-difficulty text-to-video prompts that test what the "eating spaghetti" meme benchmark tests (hands, fork, noodle physics, chewing, identity stability) with an ORIGINAL character: a silver-haired retired opera singer in a tiny Napoli trattoria. Level 1: static medium shot; Level 5: handheld, twirling, laughing, lip-synced talk with the waiter, sauce splashes. List the failure to watch for at each level.
```

**16-coffee-pirates-canvas** — по мотивам промпта Sora. HTML → WebM.
```
Recreate as a 20-second looping Canvas 2D "video" in one HTML file: two stylized pirate ships battling inside a cup of coffee seen from 3/4 above; swirling latte foam (curl noise), bobbing on procedural waves, cannon puffs, milk splashes, steam, slow push-in. Add a "Record" button using MediaRecorder to download .webm.
```

### Жанр 3. Моушен-дизайн

**17-orbita-logo** — оригинал. HTML + SVG.
```
Animated logo reveal for a fictional studio "ORBITA", single HTML with inline SVG, 4s: orbit circle draws on (stroke-dasharray), a planet travels along it (offset-path), letters drop with staggered elastic easing, light sweep over the wordmark, then idle micro-motion loop. Pure CSS + SVG. Replay button.
```

**18-kinetic-typography** — оригинал. HTML + GSAP.
```
Kinetic typography in one HTML file with GSAP (CDN) for: "Make the thing. Break the thing. Make it better." 20s, 16:9. Each word gets its own motion idea (split letters, scale slams, mask wipes, color inversions) synced to a 120 BPM beat generated with Web Audio (start on click). Bold grotesk, black/acid-yellow, timeline scrubber.
```

**19-css-loaders** — оригинал. HTML.
```
A gallery of 12 original, beautiful CSS-only loading animations in named cards: liquid fill, orbiting dots, morphing blob, DNA helix, pendulum, ink bloom, pixel snake, breathing ring, gooey merge (SVG filter), equalizer, folding cube, typewriter dots. Seamless loops. Only JS allowed: a dark/light toggle.
```

**20-lottie-coffee** — по мотивам академических Lottie-бенчмарков. JSON + плеер.
```
Write a valid Lottie (Bodymovin) JSON animation, 512x512, 60 frames at 30fps, looping: a coffee cup with three steam curves rising and fading, the cup gently squashing (squash & stretch). Shape layers only, no images or expressions. Output only the JSON.
```

**21-cinematic-intro** — оригинал. HTML + WebGL.
```
A 12-second cinematic title sequence in WebGL, one HTML file, for a fictional sci-fi film "THE LONG QUIET": drift through volumetric dust with depth of field, anamorphic flare, letters assembling from particles, chromatic aberration, film grain, a Web Audio drone (click to start), 2.39:1 letterbox, final title hold.
```

**22-pelican-animated** — по мотивам теста Уиллисона. SVG.
```
Generate an animated SVG of a pelican riding a bicycle: wheels spin, cranks rotate, the pelican's legs follow the pedals, its neck bobs, parallax hills scroll. SMIL or CSS inside the SVG, seamless 2-second loop.
```

### Жанр 4. Векторная графика

**23-pelican-bicycle** — известный тест (Simon Willison, октябрь 2024). SVG.
```
Generate an SVG of a pelican riding a bicycle
```

**24-pelican-california** — известный усложнённый вариант (восстановлен по пересказу AI Weekly). SVG.
```
Generate an SVG of a California brown pelican riding a bicycle. The bicycle must have spokes and a correctly shaped bicycle frame. The pelican must have its characteristic large pouch, and there should be a clear indication of feathers. The pelican must be clearly pedaling the bicycle. The pelican should show the plumage of the full breeding season.
```

**25-octopus-pipe-organ** — известный тест (бенчмарк Тома Галли). SVG.
```
Generate an SVG of an octopus operating a pipe organ
```

**26-gally-six-scenes** — промпты из бенчмарка Галли. 6 SVG + HTML-сетка.
```
Generate six separate SVGs (each in its own code block, 400x400): a hedgehog playing an accordion; a starfish driving a bulldozer; a penguin juggling chainsaws; a chameleon tuning a grand piano; a lobster polishing a harp; a sloth steering an excavator.
```

**27-pelican-povray** — известный вариант (BeetleB). .pov.
```
Write a POV-Ray file that shows a pelican riding on a bicycle
```

**28-isometric-icons** — оригинал. HTML + SVG.
```
A cohesive set of 12 isometric SVG icons for a fictional "home studio" app (microphone, camera, softbox, laptop, headphones, tripod, mug, plant, mixer, speaker, clapperboard, hard drive): same 30° grid, 3-tone shading from one defined palette, 2px stroke, 128x128 viewBox. One HTML grid page plus each SVG separately.
```

**29-truchet-poster** — оригинал. HTML → SVG.
```
Single HTML file that generates a printable A2 SVG poster from multi-scale Truchet tiles (quadtree subdivision), seeded randomness, 5 curated palettes, size/density sliders, "Regenerate" and "Download SVG" buttons. Every regeneration must be gallery-worthy.
```

### Жанр 5. Бесконечная и генеративная визуализация

**30-flow-field** — оригинал. HTML.
```
Infinite generative flow-field artwork in one HTML file (Canvas 2D or p5.js): 20k particles following curl noise, additive blending on dark, slowly fading trails, palette drifting every 30s, evolving noise so it never repeats. S = save PNG, Space = new seed. Fullscreen 60 FPS.
```

**31-mandelbulb-audio** — известный тест (Awesome Gemini 3 Prompts). HTML + three.
```
Create a raymarched Mandelbulb fractal (GLSL on a fullscreen quad in Three.js) surrounded by thousands of audio-reactive instanced particles with UnrealBloomPass, all in a single HTML file. Audio: microphone or a generated Web Audio drone. Slow orbital camera, fractal power animating 6→10, iridescent orbit-trap coloring.
```

**32-mandelbrot-zoom** — оригинал. HTML + WebGL2.
```
Infinite Mandelbrot zoom, single HTML, WebGL2 fragment shader: auto-zoom into Seahorse Valley, smooth coloring with cosine palettes, double-float emulation to go past 1e-6; when precision runs out, crossfade to a new target. Never-ending.
```

**33-reaction-diffusion** — оригинал. HTML + WebGL.
```
Gray-Scott reaction-diffusion on the GPU (WebGL ping-pong framebuffers), one HTML file: presets coral, mitosis, fingerprints, worms; mouse paints chemical B; colormap with "wet" specular lighting from the gradient; slowly morphs between presets forever.
```

**34-murmuration** — оригинал (boids Рейнольдса). HTML + three.
```
Starling murmuration at sunset in Three.js, one HTML file: 5,000+ boids (separation, alignment, cohesion + a predator hawk), spatial hashing, tiny dark instanced birds against a gradient sky, slow cinematic camera, sliders for the rules.
```

**35-endless-terrain** — оригинал. HTML + three.
```
Endless procedural terrain flythrough in Three.js (single HTML): chunks generated from fractal noise ahead and recycled behind, height biomes (sand, grass, rock, snow), instanced trees, fresnel water, fog, a full day/night cycle every 2 minutes with stars. Screensaver mode, runs forever.
```

**36-alpine-shader** — известный промпт (README gokayfem/shader-skills). GLSL + HTML-просмотрщик.
```
Create a Shadertoy shader (mainImage) of an alpine valley with snow, a winding river and atmospheric depth: raymarched fbm heightfield, soft shadows, aerial perspective, sun glints on the river, slow camera dolly with iTime. Single pass, no textures.
```

**37-neon-life** — оригинал. HTML + WebGL.
```
Conway's Game of Life as neon art, single HTML, WebGL: 1024x1024 toroidal grid, cells glow with fading age-colored trails, bloom, auto-reseeds with famous patterns (glider guns, pulsars, R-pentomino) when activity drops, click to draw. Must run forever.
```

### Жанр 6. Игры и симуляции

**38-hexagon-ball** — известный тест (Flavio Adamo, январь 2025). Python; в v2 веб-порт.
```
write a Python program that shows a ball bouncing inside a spinning hexagon. The ball should be affected by gravity and friction, and it must bounce off the rotating walls realistically
```

**39-heptagon-20-balls** — известный тест KCORES LLM Arena. Python; в v2 веб-порт.
```
Write a Python program that shows 20 balls bouncing inside a spinning heptagon:
- All balls have the same radius.
- All balls have a number on it from 1 to 20.
- All balls drop from the heptagon center when starting.
- Colors are: #f8b862, #f6ad49, #f39800, #f08300, #ec6d51, #ee7948, #ed6d3d, #ec6800, #ec6800, #ee7800, #eb6238, #ea5506, #ea5506, #eb6101, #e49e61, #e45e32, #e17b34, #dd7a56, #db8449, #d66a35
- The balls should be affected by gravity and friction, and they must bounce off the rotating walls realistically. There should also be collisions between balls.
- The material of all the balls determines that their impact bounce height will not exceed the radius of the heptagon, but higher than ball radius.
- All balls rotate with friction, the numbers on the ball can be used to indicate the spin of the ball.
- The heptagon is spinning around its center, and the speed of spinning is 360 degrees per 5 seconds.
- The heptagon size should be large enough to contain all the balls.
- Do not use the pygame library; implement collision detection algorithms and collision response etc. by yourself. The following Python libraries are allowed: tkinter, math, numpy, dataclasses, typing, sys.
- All codes should be put in a single Python file.
```

**40-nested-hexagons** — известный промпт (Mervin Praison, LLM Test Questions). Python; в v2 веб-порт.
```
Write a Python script that visually simulates five differently colored balls dynamically bouncing within multiple nested, rotating hexagons. Each hexagon rotates at a distinct speed, creating an engaging, mesmerizing pattern. All nested hexagons, except the outermost one, must have exactly one randomly selected missing wall, allowing balls to seamlessly pass between inner and outer hexagons. The balls initially start within the innermost hexagon. Implement realistic physics by incorporating gravity, friction, and angular momentum. Provide adjustable parameters for gravity strength, friction level, rotation speeds, and hexagon sizes. Make it minimal
```

**41-flight-sim** — известный тест (промпт @levelsio, демо Philipp Schmid, март 2025). HTML + three.
```
In pure three.js, without downloading any assets or textures, create a flight simulator game where i can fly an airplane. Make sure it runs in the browser.
```

**42-minecraft-clone** — известный промпт (gist cedrickchee). HTML + three.
```
Create a 3D Minecraft clone.
Core Features: procedural tree generation; smooth terrain generation; basic gameplay (movement, interaction, terrain manipulation).
Project Structure: single HTML with full-page canvas; basic UI controls; full-screen 3D styles.
Player Controls: WASD; mouse look with pointer lock; jump; fly; gravity; collision detection.
Technology Stack: JavaScript; Three.js as ES Module via importmap from jsdelivr.
```

**43-voxel-pagoda** — известный тест (Awesome Gemini 3 Prompts №8). HTML + three.
```
Design a richly crafted voxel-art environment featuring an ornate pagoda set within a vibrant garden.
Include diverse vegetation—especially cherry blossom trees—and make sure the composition feels lively, colorful, and visually striking.
Use any voxel or WebGL libraries you prefer, but deliver the entire project as a single, self-contained HTML file that I can paste and open directly in Chrome.
```

**44-neon-snake** — известный тест (OpenAI Cookbook). HTML.
```
Make me a snake game. It should be futuristic, neon, cyberpunk style. Make sure the typography is suitably cool.
```

**45-solar-system** — оригинал. HTML + three.
```
Interactive solar system in Three.js, single HTML: shader Sun with corona, 8 planets with procedural textures, correct relative orbital periods (time-scale slider), Saturn's rings, the Moon, orbit lines, "pretty" vs "true scale" toggle, click a planet to fly to it with an info card.
```

### Жанр 7. Объяснялки, dataviz, звук

**46-earth-magnetic-field** — по мотивам симуляций @renderfiction. HTML + three.
```
Interactive Three.js visualization of Earth's magnetic field, one HTML file: procedural Earth, dipole field lines computed from the dipole formula, solar-wind particles spiraling along field lines into aurora ovals, solar-wind slider, 11° pole-tilt toggle, side panel explaining it in 4 short paragraphs.
```

**47-sorting-sound** — оригинал. HTML.
```
Sorting visualizer with sound, one HTML file: 8 algorithms (bubble, insertion, selection, merge, quick, heap, radix, shell) racing side by side on the same array, each comparison plays a Web Audio tone mapped to value, comparison/swap counters, speed slider, pseudo-code panel highlighting the current line.
```

**48-ambient-machine** — оригинал. HTML.
```
Generative ambient music machine, one HTML file, Web Audio only: never-repeating modal chord progressions, a 16-step sequencer mutating every 8 bars, FM pad + plucked arp, reverb from a generated noise impulse, tape delay; circular spectrum analyzer colored by the current chord; mood/tempo controls, big Start button.
```

### Жанр 8. UI-клоны и ASCII

**49-linux-desktop** — известный промпт (BridgeBench Community prompts). HTML.
```
Build a web-based Linux desktop replica as a SINGLE self-contained HTML file (all CSS and JavaScript inline, no external dependencies, no build step, no server — it must run by double-clicking the .html file in a browser). Include draggable/resizable windows, a taskbar with clock, a working terminal (ls, cd, cat, mkdir, echo over an in-memory file system), text editor, file manager, settings with wallpaper/theme switching, a tiny paint app. Persist to localStorage.
```

**50-ascii-donut** — по мотивам donut.c. Python; в v2 веб-порт.
```
Single Python 3 file (stdlib only) rendering at 30 FPS in the terminal: a rotating ASCII torus lit with the ramp ".,-~:;=!*#$@", an orbiting ASCII planet, a twinkling starfield, ANSI 256 colors for depth, z-buffer, resize handling, clean Ctrl+C exit, 10-line math comment at the top.
```

## 7. Волна 6: новый 3D-пакет (промпты пока не написаны)

Когда владелец попросит, напиши 20 сильных самодостаточных промптов в стиле тестов 41–48 и создай папки `tests/51-…` — `tests/70-…`. Сам выход, уровень детализации и требование «single HTML, Three.js» — как в тестах выше. Идеи:
- чёрная дыра с гравитационным линзированием и аккреционным диском;
- ночной процедурный город под дождём с отражениями;
- океан со шторм-волнами (FFT/Gerstner) и лодкой;
- формирование спиральной галактики из частиц;
- капли дождя на стекле с преломлением;
- аквариум с рыбами-boids и каустиками;
- кубик Рубика, который сам себя собирает;
- двойная спираль ДНК с репликацией;
- тектоника плит на процедурной планете;
- северное сияние над фьордом;
- вулкан с лавой и пеплом;
- лес с процедурными деревьями и сменой сезонов;
- голографический интерфейс космического корабля;
- маятники и хаос (двойной маятник, сотни траекторий);
- стеклянная мраморная дорожка (marble run) с физикой;
- процедурная планета с полётом от орбиты до поверхности;
- кораллы и рост L-систем;
- синтез звука, управляющий 3D-ландшафтом;
- песочные часы с физикой песка;
- космическая станция в разрезе, которую можно облететь.

## 8. Контент-идеи (для владельца, не для генерации)

- Видео «Битва моделей»: 23, 38, 42 на разных моделях, сплит-экран, цена в центах.
- Шорты: 30, 33, 34, 37, 19, 17 — бесконечные петли.
- Курс:
  - «бриф решает» — 3 против 1;
  - «спецификация против свободы» — 38 против 39;
  - лестница сложности — 44 → 41 → 42.
- Волна 7 (high против max effort) — отдельный сюжет.

---

## Дополнения после первой сессии (2026-11-04)

- Репозиторий переименован в `ai-tests-90-`, GitHub Pages включены (main, root): https://vetervideo-dima.github.io/ai-tests-90-/
- Добавлены тесты 71–96 — адаптации подборки ChatGPT (промпты для генераторов картинок/видео переведены в code-тесты), волны 8–10 в `waves.md`. Номера 51–70 оставлены под волну 6.
- Отброшены из подборки ChatGPT (не code-тесты или дубли): 1, 2, 5 (фотореализм → только текстовый тест 96), 14, 26, 32, 36, 37, 43, 44, 46, 48.
- Идеи для волны 6 (раздел 7) дополнены: соларпанк-город (ChatGPT №9) и киберпанк-город с летающими машинами (ChatGPT №50) — вместе с «ночным городом под дождём».
- Исключение из правила «без CDN»: Google Fonts. Tailwind (тест 04) — `vendor/tailwindcss/`. p5 — ветка 1.x (1.11.13).
- Стоимость на сайте — оценка (API-эквивалент) по общему числу токенов субагента; см. COSTS.md.
