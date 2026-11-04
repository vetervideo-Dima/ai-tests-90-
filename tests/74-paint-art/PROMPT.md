# 74 · Paint Art

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №23 (оригинал — промпт для Runway Gen-3 (видео: струи краски)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Slow-motion fluid paint in one HTML file (WebGL): on a black background, streams of red, blue and yellow paint pour from above and flow into the word "ART" in marbled, calligraphic letters. Colors mix like real paint (no muddy RGB averaging), glossy wet highlights from the surface gradient, drips and tendrils. Holds the word, then slowly marbles away; click to pour again.
```
