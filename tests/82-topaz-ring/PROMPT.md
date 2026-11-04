# 82 · Topaz Ring

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №4 (оригинал — промпт для SDXL / DALL·E 3 (каталожное фото кольца)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js macro product shot, single HTML file: an 18-karat gold ring with an oval 8×6 mm blue topaz in a halo of eight small diamonds, lying on bleached linen with a visible weave (procedural texture). Shot from above at a 30° angle; two soft lights at 45° from either side remove shadows; pure white background. The topaz is perfectly clear with internal reflections and sparkle, polished gold shows sharp highlights. Macro depth of field, drag to rotate.
```
