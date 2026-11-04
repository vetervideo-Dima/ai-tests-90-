# 90 · Pattern Studio

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №16 + 17 + 33 + 45 (оригинал — промпт для Midjourney --tile / SD tiling). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML → SVG
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Single HTML "Pattern Studio" that generates seamless, tileable SVG patterns: (1) vintage watercolor flowers and birds (SVG turbulence/displacement for a watercolor look), (2) Seigaiha waves in alcohol-ink blue and gold, (3) minimalist pastel geometric shapes, (4) a green-blue fractal texture. A live 3×3 tiling preview proves the seams are invisible. Seed and palette controls, "Download SVG tile" and "Download PNG tile" buttons.
```
