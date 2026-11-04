# 83 · Barbershop Night

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №11 (оригинал — промпт для SDXL / Nano Banana Pro (ночная вывеска)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js night street, single HTML file: a small European street with wet cobblestones reflecting the lights. Center: a barbershop entrance — wooden door with frosted glass, above it a rectangular patinated brass sign with embossed letters "BARBERIAN", to the right a classic red-white-blue barber pole spinning and lit from within. Warm orange interior light and silhouettes of people behind the window, light rain. Slow dolly-in; the sign text must be crisp and undistorted.
```
