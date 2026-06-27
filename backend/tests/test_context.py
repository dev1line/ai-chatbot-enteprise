from app.orchestration.context import trim_messages_to_budget


def test_trim_messages_to_budget_keeps_recent_messages():
    messages = [
        {"role": "user", "content": "A" * 300},
        {"role": "assistant", "content": "B" * 300},
        {"role": "user", "content": "C" * 40},
    ]

    trimmed = trim_messages_to_budget(
        messages,
        max_context_tokens=120,
        completion_token_reserve=40,
    )

    assert trimmed
    assert trimmed[-1]["content"] == "C" * 40
    assert all(msg["content"] != "A" * 300 for msg in trimmed)
