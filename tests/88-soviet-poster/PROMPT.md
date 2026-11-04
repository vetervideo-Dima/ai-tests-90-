# 88 · Soviet Poster

- **Жанр:** Вектор, моушен, обложки, текст (адаптация)
- **Источник:** Адаптация подборки ChatGPT №10 (оригинал — промпт для SD / DALL·E 3 (ретро-плакат)). Сюжет тот же, но результат — код, а не растровая картинка/видео.
- **Формат выхода:** HTML + SVG
- **Волна:** 10
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Single HTML file with an inline SVG poster (A2 proportions) in 1930s Soviet constructivist style: a worker in overalls holding a laptop with an outstretched arm, gazing into the distance; strong diagonal composition; limited palette of red, white, black and ochre. Large headline «АВТОМАТИЗИРУЙ!» in bold era-appropriate lettering, small text at the bottom «Нейросеть — инструмент нового времени». Worn paper texture via SVG filters. All Cyrillic lettering crisp and undistorted. A "Download SVG" button.
```
