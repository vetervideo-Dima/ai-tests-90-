# 77 · Powers Of Ten Zoom

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №27 (оригинал — промпт для Kling AI Infinite Zoom (видео)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Infinite zoom loop in one HTML file (WebGL): start with Earth from space and zoom continuously into a coastline, a city, a single leaf, plant cells, a molecule, then into a swirling cosmic fractal that becomes a galaxy and finally Earth again — a seamless, never-ending loop. Every level is procedural; transitions are hidden inside the motion. A small scale label shows 10^n meters.
```
