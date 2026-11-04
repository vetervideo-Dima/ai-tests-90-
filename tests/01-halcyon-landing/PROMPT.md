# 01 · Halcyon Landing

- **Жанр:** Сайты и лендинги
- **Источник:** Awwwards-лендинг с анти-slop брифом (по мотивам статьи Anthropic «Improving frontend design through Skills»). HTML.
- **Формат выхода:** HTML
- **Волна:** 3
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Design a single-file landing page for "Halcyon", a fictional maker of handmade analog synthesizers. Commit to ONE bold aesthetic: Swiss-brutalist editorial meets 1970s Japanese hi-fi catalogues. No Inter/Roboto/Arial — distinctive Google Fonts with extreme weight contrast (100 vs 900); one dominant color + one sharp accent as CSS variables; no purple gradients, no generic rounded cards. Sections: full-viewport hero with an animated canvas oscilloscope line reacting to mouse; staggered scroll-reveal product grid (IntersectionObserver); horizontally scrolling "patch notes" timeline; specs table styled like a printed manual; footer with a giant outlined wordmark. Purposeful micro-interactions on every button. No frameworks.
```
