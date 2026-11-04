# 84 · Japandi Room

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №13 + 49 (оригинал — промпт для SDXL / Imagen (интерьер Japandi, лофт)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Architectural visualization in Three.js, single HTML file: a spacious 40 m² Japandi living room with 3 m ceilings — light oak floor, a low wooden sofa with cream linen upholstery and three beige cushions, an oak-and-black-metal coffee table with a ceramic vase holding one eucalyptus branch and a stack of books, a rice-paper floor lamp, a large abstract watercolor in a thin frame, a floor-to-ceiling window with blurred greenery outside. Soft natural daylight, ambient occlusion feel, everything modeled procedurally. Orbit camera, a day/evening toggle and a "loft" variant (exposed brick, leather couch, Edison bulbs, plants).
```
