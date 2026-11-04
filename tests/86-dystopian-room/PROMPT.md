# 86 · Dystopian Room

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №31 (оригинал — промпт для NeRF / 3D (антиутопическая комната)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js, single HTML file: an abandoned room in a dystopian city — overturned furniture, dust motes in light shafts, a cold blue neon sign flickering on the wall, a broken window revealing a ruined skyline with smoke, searchlights and distant lightning. Fully procedural, volumetric light, a 360° orbit camera the user can drag.
```
