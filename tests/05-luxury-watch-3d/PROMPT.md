# 05 · Luxury Watch 3d

- **Жанр:** Сайты и лендинги
- **Источник:** расширение строки из галереи Gemini 3 Website Prompts. HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Design a 3D product experience page for a luxury wristwatch (fictional "Meridian No. 7"). Build the watch procedurally in Three.js (case, engraved bezel, sapphire glass with transmission, hands showing the real current time). Scroll drives the camera: hero 3/4 view → exploded movement → dial macro → strap options (click to swap materials). Studio lighting, soft shadows, film grain. Single HTML, Three.js via import map.
```
