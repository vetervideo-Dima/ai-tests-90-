# 92 · Whiteboard Doodle

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №35 (оригинал — промпт для Veed / Doodle AI (дудл-анимация)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + SVG
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Whiteboard doodle animation in one HTML file with inline SVG: a hand-drawn black marker sketches a smiley face, a heart and the word "HELLO" (stroke draw-on, slightly wobbly boiling line), a marker cursor follows the stroke, then all three converge and morph into a single combined image. 10-second loop, replay button.
```
