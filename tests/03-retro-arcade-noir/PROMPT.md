# 03 · Retro Arcade Noir

- **Жанр:** Сайты и лендинги
- **Источник:** известный тест из OpenAI Cookbook «Frontend coding with GPT-5». HTML. v2 = второе сообщение.
- **Формат выхода:** HTML (v2 — второе сообщение)
- **Волна:** 3
- **Корректировка для облачного режима:** Все HTML: библиотеки только из `vendor/` по относительному пути (importmap), без CDN — это правило важнее того, что написано в промпте. Исключение: Google Fonts.

## Системный промпт

```
You are a world-class creative technologist. Output exactly one complete, self-contained file in a single code block. No explanations. For HTML: inline all CSS/JS; CDN libraries only if explicitly allowed (ES module import maps from jsdelivr/unpkg). Must run by double-clicking in Chrome. Target 60 FPS, handle resize, use devicePixelRatio.
```

## Промпт

```
Make me landing page for a retro-games store. Retro-arcade noir some might say
```

Второе сообщение (для v2): `Make it light, more pastel coloured & flowery`
