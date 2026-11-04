# 43 · Voxel Pagoda

- **Жанр:** Игры и симуляции
- **Источник:** известный тест (Awesome Gemini 3 Prompts №8). HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Design a richly crafted voxel-art environment featuring an ornate pagoda set within a vibrant garden.
Include diverse vegetation—especially cherry blossom trees—and make sure the composition feels lively, colorful, and visually striking.
Use any voxel or WebGL libraries you prefer, but deliver the entire project as a single, self-contained HTML file that I can paste and open directly in Chrome.
```
