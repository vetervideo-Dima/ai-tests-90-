# 35 · Endless Terrain

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал. HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Endless procedural terrain flythrough in Three.js (single HTML): chunks generated from fractal noise ahead and recycled behind, height biomes (sand, grass, rock, snow), instanced trees, fresnel water, fog, a full day/night cycle every 2 minutes with stars. Screensaver mode, runs forever.
```
