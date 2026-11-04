# 73 · Smoke Words

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №22 + 40 (оригинал — промпт для Runway Gen-3 (видео: дым складывается в слово)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
GPU smoke simulation in one HTML file (stable-fluids on WebGL ping-pong framebuffers). Scene 1: an industrial cyberpunk wall with symmetrically arranged pipes venting yellow smoke; the smoke is steered toward a target field so it forms the word "FUTURE" in glowing bold letters, which glow, grow, flicker and dissipate. Scene 2: candles on black emit colorful smoke that billows into the word "PEACE" and then disperses. Button to switch scenes, mouse stirs the smoke, looping forever.
```
