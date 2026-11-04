# 17 · Orbita Logo

- **Жанр:** Моушен-дизайн
- **Источник:** оригинал. HTML + SVG.
- **Формат выхода:** HTML + SVG
- **Волна:** 3
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Animated logo reveal for a fictional studio "ORBITA", single HTML with inline SVG, 4s: orbit circle draws on (stroke-dasharray), a planet travels along it (offset-path), letters drop with staggered elastic easing, light sweep over the wordmark, then idle micro-motion loop. Pure CSS + SVG. Replay button.
```
