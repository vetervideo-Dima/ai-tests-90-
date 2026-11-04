# 76 · Fireflies Hope

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №25 (оригинал — промпт для Runway Gen-3 (видео: светлячки)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js night forest clearing, single HTML file: procedural trees, moonlight, ground fog. Thousands of fireflies with blinking bioluminescent glow wander on curl noise, then swarm together to form the word "HOPE" in soft golden light, twinkle, and dissolve back into the forest. Slow cinematic pan, bloom, ambient Web Audio crickets and wind (click to start).
```
