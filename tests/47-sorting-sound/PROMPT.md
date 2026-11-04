# 47 · Sorting Sound

- **Жанр:** Объяснялки, dataviz, звук
- **Источник:** оригинал. HTML.
- **Формат выхода:** HTML
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Sorting visualizer with sound, one HTML file: 8 algorithms (bubble, insertion, selection, merge, quick, heap, radix, shell) racing side by side on the same array, each comparison plays a Web Audio tone mapped to value, comparison/swap counters, speed slider, pseudo-code panel highlighting the current line.
```
