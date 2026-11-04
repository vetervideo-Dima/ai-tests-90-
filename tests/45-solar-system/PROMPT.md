# 45 · Solar System

- **Жанр:** Игры и симуляции
- **Источник:** оригинал. HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Interactive solar system in Three.js, single HTML: shader Sun with corona, 8 planets with procedural textures, correct relative orbital periods (time-scale slider), Saturn's rings, the Moon, orbit lines, "pretty" vs "true scale" toggle, click a planet to fly to it with an info card.
```
