# 78 · Kaleidoscope Crystal

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №28 + 41 (оригинал — промпт для Runway / Kling (видео: зум в кристалл, плазма)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Fragment shader in one HTML file (WebGL): an endless zoom into a kaleidoscopic crystal-and-plasma mandala — 6- to 12-fold mirror symmetry, faceted crystal refraction look, neon plasma streams flowing between facets, palette drifting from pastel to neon. Ethereal, dreamy, hypnotic; never visibly repeats. Click to change the symmetry order.
```
