# 48 · Ambient Machine

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
Generative ambient music machine, one HTML file, Web Audio only: never-repeating modal chord progressions, a 16-step sequencer mutating every 8 bars, FM pad + plucked arp, reverb from a generated noise impulse, tape delay; circular spectrum analyzer colored by the current chord; mood/tempo controls, big Start button.
```
