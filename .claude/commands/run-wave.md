Запусти волну тестов $ARGUMENTS (номер волны из waves.md или номер одного теста).
1. Прочитай CLAUDE.md и waves.md, определи список папок.
2. Для каждого теста запусти отдельного субагента (не больше 3 одновременно) и передай ему CLAUDE.md и путь к папке. Субагент: v1 → проверка → v2 → README → meta.json.
3. Сам код тестов в свой контекст не загружай — только координируй.
4. В конце обнови галерею и COSTS.md, закоммить и напиши сводку: что получилось, что сломалось, что стоит переделать.

Технически:
- Шаблон задания субагенту — `tools/subagent-prompt.md` (подставить NN-slug и порт 8100+NN). effort субагента — high.
- Когда субагент завершился, запиши его usage (subagent_tokens, tool_uses, duration_ms) командой
  `python3 tools/record_usage.py NN <subagent_tokens> <tool_uses> <duration_ms>` — она обновит meta.json и COSTS.md.
- Коммить каждый тест отдельно (`git add tests/NN-slug`), сайт — `python3 tools/build.py`.
