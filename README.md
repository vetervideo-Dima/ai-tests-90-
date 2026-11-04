# Один промпт — один результат

Коллекция визуальных тестов нейросети (3D/Three.js, шейдеры, сайты, моушен, вектор, игры, видео-код).
Каждый тест — папка `tests/NN-slug/`: `PROMPT.md` (дословно), `v1/` (честный one-shot), `v2/` (доработка после
самопроверки), скриншоты, `README.md`, `meta.json` (статус, расход токенов, оценка стоимости).

**Галерея:** https://vetervideo-dima.github.io/ai-tests-90-/

- Правила прогона — [CLAUDE.md](CLAUDE.md), волны — [waves.md](waves.md), расход — [COSTS.md](COSTS.md)
- Исходный план — [docs/HANDOFF.md](docs/HANDOFF.md)
- Сборка сайта: `python3 tools/gen_prompts.py` (промпты) → `python3 tools/build.py` (галерея и страницы тестов)
- Библиотеки — локально в [vendor/](vendor/README.md), без CDN
