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

## Дополнения (облачный режим)

**Библиотеки** — см. `vendor/README.md`. Из `tests/NN-slug/v1/index.html` путь к vendor: `../../../vendor/…`.
Importmap для three: `"three": "../../../vendor/three/build/three.module.js"`, `"three/addons/": "../../../vendor/three/examples/jsm/"`.
Правило «только vendor» важнее того, что написано в промпте (там, где промпт просит CDN/jsdelivr).

**Исключение — шрифты:** разрешены Google Fonts (`fonts.googleapis.com` / `fonts.gstatic.com`). Всегда указывай fallback-стек.

**v1 — честный one-shot.** Напиши v1 один раз, целиком, и заморозь ДО любой проверки. После проверки v1 не правится —
даже если сломан. Скриншот v1 → `v1/screenshot.png`. Все исправления — только в v2.

**v2** — копия v1 + исправления и улучшения. Исключение: тест 03 — v2 делается по второму сообщению из PROMPT.md.
Python-тесты (38, 39, 40, 50): в v2 — оригинал на Python (исправленный) + веб-порт `v2/index.html` (canvas или p5).

**Проверка в браузере** (Chromium и Playwright уже установлены; `playwright install` НЕ запускать):
```bash
cd <корень репозитория> && python3 -m http.server <порт 8100+NN> &   # сервер из КОРНЯ, чтобы работал ../../../vendor
NODE_PATH=$(npm root -g) node tools/check.mjs http://localhost:<порт>/tests/NN-slug/v1/index.html tests/NN-slug/v1/screenshot.png
```
`tools/check.mjs` печатает ошибки консоли, исключения, 404 и FPS; снимает скриншот 1280×720 (WebGL через SwiftShader —
FPS в песочнице ниже реального, это нормально). Опции: `--wait 4000`, `--click` (кликнуть в центр для старта
аудио/игры), `--mobile` (390×844). Не забудь потом убить свой сервер.

**Файлы теста:**
```
tests/NN-slug/
  PROMPT.md          — не трогать
  v1/                — one-shot (index.html или другой выход) + v1/screenshot.png
  v2/                — доработка + v2/screenshot.png
  screenshot.png     — главный скриншот для галереи (обычно = v2)
  README.md          — 3–5 строк
  meta.json          — см. схему ниже
  result.md          — только для текстовых тестов
```

**meta.json:**
```json
{
  "model": null,
  "effort": "high",
  "date": "YYYY-MM-DD",
  "worked": true,
  "v1_worked": true,
  "kind": "html | svg | video | text | python",
  "entry": { "v1": "v1/index.html", "v2": "v2/index.html" },
  "notes": "коротко: что работает, что нет",
  "v1_issues": "что было сломано в v1 (или пусто)",
  "v2_changes": "что сделано в v2"
}
```
`worked` — работает ли итоговый v2, `v1_worked` — работал ли v1 как есть. `model` оставь `null` — модель указывается централизованно в `site.config.json`. Поле `usage` (токены, время, оценка
стоимости) дописывает координатор — не трогай.
`entry` — путь относительно папки теста к тому, что открывать в просмотрщике (html, svg, mp4 или md).

**Тяжёлые файлы:** видео (mp4/webm) ≤ 15 МБ, без node_modules и промежуточных файлов рендера в git.

**Сайт:** `python3 tools/build.py` пересобирает `tests/index.json`, `index.html` и страницы `tests/NN-slug/index.html`.
Запускает координатор, а не субагент.
