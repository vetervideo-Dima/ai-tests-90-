# 04 · Photo Portfolio 3d

- **Жанр:** Сайты и лендинги
- **Источник:** известный тест (commandcode.ai). HTML.
- **Формат выхода:** HTML (Tailwind)
- **Волна:** 3
- **Корректировка для облачного режима:** Вместо фото — сгенерированные SVG/CSS-заглушки. Tailwind — из `vendor/tailwindcss/tailwind.browser.js`. Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Create an elegant minimalist single-file HTML photography portfolio landing page for "Elena Voss Photography". Tailwind CSS. Hero: full bleed hero image with 3D floating frame effect around the main photo (CSS 3D + JS). Infinite scroll masonry grid that loads more images with smooth fade-ins. Clicking an image opens a 3D lightbox gallery. About section with subtle parallax. Journal / Stories section with scroll horizontal cards. Contact with elegant form. Use soft elegant typography, lots of whitespace, and tasteful 3D interactions. Very high aesthetic quality. Output complete HTML. Use generated SVG/CSS placeholders instead of photos.
```
