# 71 · Bubbles My Way

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №20 (оригинал — промпт для Runway Gen-3 (видео: текст из мыльных пузырей)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Slow-motion macro in Three.js, single HTML file: soap bubbles drift on a pure black background. Each bubble has physically inspired thin-film iridescence (view-dependent interference colors, fresnel rim, subtle wobbling surface, faint reflections). The bubbles gather and merge into the words "MY WAY" built from many small bubbles, hold and wobble, then pop and drift apart into rainbow chaos. Shallow depth of field, soft bokeh, seamless 12-second loop, click to replay.
```
