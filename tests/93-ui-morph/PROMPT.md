# 93 · Ui Morph

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №30 (оригинал — промпт для Runway Gen-4 (UI motion)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + GSAP
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
UI motion design in one HTML file with GSAP: a 15-second sequence showing the evolution of an interface — a phone app screen morphs into a tablet layout and then a desktop web layout, cards reflowing with FLIP transitions, smooth camera moves, minimal text, polished easing. Timeline scrubber and replay button.
```
