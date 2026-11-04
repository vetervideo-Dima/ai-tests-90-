# 32 · Mandelbrot Zoom

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал. HTML + WebGL2.
- **Формат выхода:** HTML + WebGL2
- **Волна:** 2
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Infinite Mandelbrot zoom, single HTML, WebGL2 fragment shader: auto-zoom into Seahorse Valley, smooth coloring with cosine palettes, double-float emulation to go past 1e-6; when precision runs out, crossfade to a new target. Never-ending.
```
