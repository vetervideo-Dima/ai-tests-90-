# 95 · Fitness Landing Short

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №29 (оригинал — промпт для MS Designer / Uizard (макет сайта)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Website homepage design: a modern landing page for a fitness app. Header banner with gym image, clear CTA buttons. Color scheme: yellow and gray. Style: minimal flat design with clean UI.
```
