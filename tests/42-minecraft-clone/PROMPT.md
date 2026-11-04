# 42 · Minecraft Clone

- **Жанр:** Игры и симуляции
- **Источник:** известный промпт (gist cedrickchee). HTML + three.
- **Формат выхода:** HTML + three
- **Волна:** 1
- **Корректировка для облачного режима:** Three.js — из `vendor/` через importmap (не jsdelivr). Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Create a 3D Minecraft clone.
Core Features: procedural tree generation; smooth terrain generation; basic gameplay (movement, interaction, terrain manipulation).
Project Structure: single HTML with full-page canvas; basic UI controls; full-screen 3D styles.
Player Controls: WASD; mouse look with pointer lock; jump; fly; gravity; collision detection.
Technology Stack: JavaScript; Three.js as ES Module via importmap from jsdelivr.
```
