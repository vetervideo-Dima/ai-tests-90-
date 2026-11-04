# 37 · Neon Life

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал. HTML + WebGL.
- **Формат выхода:** HTML + WebGL
- **Волна:** 2
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Conway's Game of Life as neon art, single HTML, WebGL: 1024x1024 toroidal grid, cells glow with fading age-colored trails, bloom, auto-reseeds with famous patterns (glider guns, pulsars, R-pentomino) when activity drops, click to draw. Must run forever.
```
