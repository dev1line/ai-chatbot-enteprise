from __future__ import annotations

from collections.abc import Sequence


def estimate_tokens(text: str) -> int:
    """Cheap token estimate for budgeting without external tokenizer.

    For mixed EN/VI chat text, ~4 chars/token is a practical approximation.
    """
    if not text:
        return 0
    return max(1, len(text) // 4)


def trim_messages_to_budget(
    messages: Sequence[dict[str, str]],
    max_context_tokens: int,
    completion_token_reserve: int,
) -> list[dict[str, str]]:
    """Keep newest messages that fit the context budget.

    We trim from oldest to newest while preserving message order in the output.
    """
    budget = max(1, max_context_tokens - completion_token_reserve)
    kept: list[dict[str, str]] = []
    used = 0

    for msg in reversed(messages):
        cost = estimate_tokens(msg.get("content", "")) + 4
        if used + cost > budget:
            continue
        kept.append(msg)
        used += cost

    kept.reverse()
    return kept
