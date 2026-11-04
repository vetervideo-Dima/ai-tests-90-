# 44 · Neon Snake

- **Жанр:** Игры и симуляции
- **Источник:** известный тест (OpenAI Cookbook). HTML.
- **Формат выхода:** HTML
- **Волна:** 4
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Make me a snake game. It should be futuristic, neon, cyberpunk style. Make sure the typography is suitably cool.
```
