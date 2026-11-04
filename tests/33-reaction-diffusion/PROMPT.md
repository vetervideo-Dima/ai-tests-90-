# 33 · Reaction Diffusion

- **Жанр:** Бесконечная и генеративная визуализация
- **Источник:** оригинал. HTML + WebGL.
- **Формат выхода:** HTML + WebGL
- **Волна:** 2
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Gray-Scott reaction-diffusion on the GPU (WebGL ping-pong framebuffers), one HTML file: presets coral, mitosis, fingerprints, worms; mouse paints chemical B; colormap with "wet" specular lighting from the gradient; slowly morphs between presets forever.
```
