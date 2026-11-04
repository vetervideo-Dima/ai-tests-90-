# 31 · Mandelbulb Audio

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** известный тест (Awesome Gemini 3 Prompts). HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Микрофон необязателен, по умолчанию — генерируемый drone. На GitHub Pages (https) микрофон доступен. Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Create a raymarched Mandelbulb fractal (GLSL on a fullscreen quad in Three.js) surrounded by thousands of audio-reactive instanced particles with UnrealBloomPass, all in a single HTML file. Audio: microphone or a generated Web Audio drone. Slow orbital camera, fractal power animating 6→10, iridescent orbit-trap coloring.
```
