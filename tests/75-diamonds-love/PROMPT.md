# 75 · Diamonds Love

- **Жанр:** Материя складывается в слово / бесконечные шейдеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №24 (оригинал — промпт для Runway Gen-3 (видео: бриллианты складываются в слово)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 8
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js, single HTML file: start with an extreme macro of a faceted brilliant-cut diamond with real refraction and dispersion (custom shader with internal ray bounces and rainbow fire). The camera slowly pulls back to reveal dozens of diamonds arranged to spell "LOVE" in large letters. Swirling mist, black background, sparkling highlights, bloom. 15-second seamless loop.
```
