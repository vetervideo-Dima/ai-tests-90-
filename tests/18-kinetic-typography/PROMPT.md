# 18 · Kinetic Typography

- **Жанр:** Моушен-дизайн
- **Источник:** оригинал. HTML + GSAP.
- **Формат выхода:** HTML + GSAP
- **Волна:** 3
- **Корректировка для облачного режима:** GSAP — из `vendor/gsap/`, не с CDN. Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Kinetic typography in one HTML file with GSAP (CDN) for: "Make the thing. Break the thing. Make it better." 20s, 16:9. Each word gets its own motion idea (split letters, scale slams, mask wipes, color inversions) synced to a 120 BPM beat generated with Web Audio (start on click). Bold grotesk, black/acid-yellow, timeline scrubber.
```
