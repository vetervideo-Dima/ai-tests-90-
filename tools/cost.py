"""Оценка стоимости прогона субагента (API-эквивалент).

Система сообщает по завершении субагента `subagent_tokens`, `tool_uses`, `duration_ms`. Опыт показал, что
`subagent_tokens` — это итоговый размер контекста субагента (у пустого субагента «ответь ok» ≈ 54k — это его
стартовые инструкции), а не сумма токенов по всем запросам. Поэтому стоимость восстанавливается моделью:

  ходов           T = tool_uses + 1
  чтение кэша     T × (B + F) / 2        — каждый ход перечитывает контекст, растущий от B до F
  запись кэша     (F − B)                — всё новое в контексте записывается в кэш один раз
  выход           out_share × (F − B)    — доля сгенерированного (код, рассуждения) в приросте контекста

B = baseline_tokens (стартовый контекст), F = subagent_tokens. Цены — из site.config.json (Opus 5.5:
$4 вход / $20 выход / $0.20 чтение кэша / $5 запись кэша за MTok). Это оценка, а не счёт.
"""


def estimate(run, cfg):
    p = cfg["pricing"]
    B = cfg["baseline_tokens"]
    F = max(run["subagent_tokens"], B)
    T = run["tool_uses"] + 1
    grow = F - B
    reads = T * (B + F) / 2
    usd = (reads * p["cache_read"] + grow * p["cache_write"] + cfg["out_share"] * grow * p["output"]) / 1e6
    return round(usd, 2), int(reads + grow)
