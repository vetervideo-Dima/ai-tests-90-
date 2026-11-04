# 41 · Flight Sim

- **Жанр:** Игры и симуляции
- **Источник:** известный тест (промпт @levelsio, демо Philipp Schmid, март 2025). HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
In pure three.js, without downloading any assets or textures, create a flight simulator game where i can fly an airplane. Make sure it runs in the browser.
```
