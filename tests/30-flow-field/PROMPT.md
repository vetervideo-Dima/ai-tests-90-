# 30 · Flow Field

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал. HTML.
- **Формат выхода:** HTML
- **Волна:** 2
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Infinite generative flow-field artwork in one HTML file (Canvas 2D or p5.js): 20k particles following curl noise, additive blending on dark, slowly fading trails, palette drifting every 30s, evolving noise so it never repeats. S = save PNG, Space = new seed. Fullscreen 60 FPS.
```
