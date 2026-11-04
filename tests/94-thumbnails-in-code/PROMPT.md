# 94 · Thumbnails In Code

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №6 + 7 (оригинал — промпт для SDXL / GPT Image / Ideogram (обложки)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Single HTML file producing two thumbnails in pure HTML/CSS/SVG (no photos — illustrated people): (1) YouTube 1920×1080: gradient from deep navy on the left to black on the right, a surprised 30-year-old man's face in the left third lit by cool blue monitor light, big bold white headline "ChatGPT vs Gemini", smaller grey subtitle "Кто лучше в 2026?", a yellow lightning bolt in the bottom right; (2) Reels 1080×1920: a smiling 25-year-old woman in a vivid yellow oversized sweater on pure white, the top third holding the headline «КАК Я ПОХУДЕЛА НА 8 КГ» in two lines of bold black sans-serif, the bottom quarter empty for captions. Both legible at small size; "Download PNG" buttons.
```
