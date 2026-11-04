# 80 · Neon Audio Grid

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №38 + 39 + 42 (оригинал — промпт для Firefly / Runway (видео: неон, сетка, музыка)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Audio-reactive neon light show in one HTML file: a generated 128 BPM techno track in Web Audio (kick, hats, bass, a simple lead; click to start). Three.js scene: a synthwave wireframe grid receding to the horizon, glowing purple, blue and pink lines and geometric shapes that pulse and dance to the analyser bands, a sun on the horizon, bloom, the camera bumping on every kick.
```
