# 72 · Lava Lamp Love

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №21 (оригинал — промпт для Runway Gen-3 (видео: лава-лампа)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Raymarched lava lamp, single HTML file (WebGL fragment shader or Three.js full-screen quad): a glass lava lamp in a dark room, glowing wax blobs as smooth-min SDF metaballs that rise, stretch and sink with buoyancy, warm red-orange subsurface glow lighting the glass. Every cycle the blobs flow together and form the word "LOVE", hold for a moment, then melt apart. Cinematic close-up, slow orbit, bloom, hypnotic and seamless.
```
