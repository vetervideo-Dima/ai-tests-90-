# 79 · Fractal Valley

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №34 (оригинал — промпт для Kaiber.ai (видео: фрактальная долина)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + WebGL
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Raymarched psychedelic fractal landscape in one HTML file (WebGL fragment shader): the camera flies forever through a valley of folded-space fractal mountains (kaleidoscopic IFS), with glowing rivers in the canyon floor, volumetric fog and a slowly cycling color palette. No visible repetition. Adaptive resolution to hold 60 FPS.
```
