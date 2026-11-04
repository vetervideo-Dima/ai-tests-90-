# 46 · Earth Magnetic Field

- **Жанр:** Объяснялки, dataviz, звук
- **Источник:** по мотивам симуляций @renderfiction. HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Interactive Three.js visualization of Earth's magnetic field, one HTML file: procedural Earth, dipole field lines computed from the dipole formula, solar-wind particles spiraling along field lines into aurora ovals, solar-wind slider, 11° pole-tilt toggle, side panel explaining it in 4 short paragraphs.
```
