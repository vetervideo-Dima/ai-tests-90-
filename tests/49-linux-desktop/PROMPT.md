# 49 · Linux Desktop

- **Жанр:** UI-клоны и ASCII
- **Источник:** известный промпт (BridgeBench Community prompts). HTML.
- **Формат выхода:** HTML
- **Волна:** 4
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Build a web-based Linux desktop replica as a SINGLE self-contained HTML file (all CSS and JavaScript inline, no external dependencies, no build step, no server — it must run by double-clicking the .html file in a browser). Include draggable/resizable windows, a taskbar with clock, a working terminal (ls, cd, cat, mkdir, echo over an in-memory file system), text editor, file manager, settings with wallpaper/theme switching, a tiny paint app. Persist to localStorage.
```
