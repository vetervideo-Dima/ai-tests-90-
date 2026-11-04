# 08 · Remotion Countdown

- **Жанр:** Видео (код или промпты)
- **Источник:** известный тест (гайд Remotion). React/Remotion.
- **Формат выхода:** React / Remotion
- **Волна:** 5
- **Корректировка для облачного режима:** Remotion: код + попытка рендера в MP4 (Chromium: `/opt/pw-browsers/chromium`); если headless Chrome недоступен — команда для локального рендера.

## Промпт

```
System: You are a Remotion component generator. Generate a single React component that uses Remotion. Rules: Export the component as a named export called "MyComposition"; Use useCurrentFrame() and useVideoConfig() from "remotion"; Prefer interpolate() with Easing over spring() unless physics-based motion is explicitly requested; Only output the code.
User: Create a countdown from 5 to 1 with smooth motion
```

Вариант (вторая композиция): `Create a text animation that types out "Hello World" letter by letter`
