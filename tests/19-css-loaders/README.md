# 19 · CSS Loaders
Галерея из 12 CSS-лоадеров в именованных карточках (liquid fill, orbiting dots, morphing blob, DNA helix, Newton's cradle, ink bloom, pixel snake, breathing ring, gooey merge через SVG-фильтр, equalizer, folding cube, typewriter dots); JS — только переключатель тёмной/светлой темы.
Открыть: `v1/index.html` (one-shot) или `v2/index.html` (доработка) — работает и двойным кликом, внешних библиотек нет (только Google Fonts с fallback).
v1 работал без ошибок консоли, но был тяжёлым (backdrop-filter, fixed-фон, анимация `top`) и орбитальные точки слипались в комок.
v2: анимации только на transform/translate, `content-visibility` для карточек, цветное свечение карточек, ступени у спирали ДНК, тема ставится до первой отрисовки, плавная смена темы, мобильная сетка 2×N.
