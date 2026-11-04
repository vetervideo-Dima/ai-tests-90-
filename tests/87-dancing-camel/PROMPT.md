# 87 · Dancing Camel

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №47 (оригинал — промпт для DreamFusion (text-to-3D, glTF)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js, single HTML file: a cartoon camel built procedurally (no assets) with a real skeleton (SkinnedMesh + bones), performing a looping keyframed dance synced to a generated Web Audio beat (click to start). Toon shading, a desert stage with spotlights and a starry sky. An "Export glTF" button downloads the animated model via GLTFExporter.
```
