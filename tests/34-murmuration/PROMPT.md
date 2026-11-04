# 34 · Murmuration

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал (boids Рейнольдса). HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 2
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Starling murmuration at sunset in Three.js, one HTML file: 5,000+ boids (separation, alignment, cohesion + a predator hawk), spatial hashing, tiny dark instanced birds against a gradient sky, slow cinematic camera, sliders for the rules.
```
