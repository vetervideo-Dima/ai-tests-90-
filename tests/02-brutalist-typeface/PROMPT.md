# 02 · Brutalist Typeface

- **Жанр:** Сайты и лендинги
- **Источник:** Brutalist website for a typeface maker (известный тест, Design Arena / HN). HTML.
- **Формат выхода:** HTML
- **Волна:** 3
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Build a brutalist website for a typeface maker. Single HTML file. Fictional foundry "Grotesk & Sons". Include a live type tester (editable text, size/weight/tracking sliders on a variable Google Font), a glyph grid that zooms on hover, exposed grid lines, monospace metadata, harsh black/white with one signal color.
```
