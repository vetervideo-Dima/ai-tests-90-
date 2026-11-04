# 81 · Perfume Shot

- **Жанр:** 3D-предметка и интерьеры (адаптация)
- **Источник:** Адаптация подборки ChatGPT №3 (оригинал — промпт для Flux / SDXL (рекламное фото парфюма)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + three
- **Волна:** 9
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Three.js product shot, single HTML file: a premium men's perfume bottle — dark matte rectangular glass with a gold metallic cap — centered on a 20×20 cm black polished acrylic pedestal that shows a crisp mirror reflection. A soft backlight creates a halo around the bottle, a narrow side light from the left emphasizes its edges, the background is pure deep black. Three dark burgundy rose petals lie casually beside it. Physically based materials (transmission, roughness, clearcoat), slow turntable, a button to cycle lighting presets. No text, no logos.
```
