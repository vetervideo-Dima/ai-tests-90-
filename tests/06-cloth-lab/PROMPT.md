# 06 · Cloth Lab

- **Жанр:** Сайты и лендинги
- **Источник:** известный промпт (Medium, @augustozz). Бренд заменён на выдуманный. HTML, raw WebGL.
- **Формат выхода:** HTML, raw WebGL
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Create a complete, self-contained interactive demo as exactly one HTML file. Build a polished one-page "Interactive Cloth Lab" website with a dark cinematic UI, inspired by a high-end physics showcase. The page should feature a large wind-blown cloth flag/banner with the text "WINDHALL" mapped onto it. The cloth should feel physical, dimensional, and satisfying to watch. Do not use React, JSX, npm, bundlers, imports, modules, or external dependencies. Raw WebGL rendering. Control panel with sliders for turbulence, stiffness, and sheen; mouse drag pushes or tears the cloth.
```
