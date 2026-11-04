# 85 · Space Kids Room

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №15 (оригинал — промпт для SDXL / Midjourney (детская комната)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js, single HTML file: a 7-year-old's space-themed bedroom — dark blue ceiling with twinkling star lights and a pink-purple nebula projection, a built-in white rocket-shaped capsule bed with orange accents and a round porthole nightlight, pull-out drawers, a large solar-system mural with labels, light grey carpet, a desk with a lamp by the window. Soft evening light, magazine-quality styling. Click the nightlight to switch to night mode where the ceiling becomes a planetarium.
```
