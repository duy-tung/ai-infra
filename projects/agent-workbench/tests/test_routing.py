from agent_workbench.routing import ModelRouter


def test_heavy_task_routes_to_opus():
    r = ModelRouter()
    d = r.route("refactor the payment service to use idempotency keys")
    assert d.model == "claude-opus-4-8"


def test_short_classification_routes_to_haiku():
    r = ModelRouter()
    d = r.route("classify this comment as positive or negative")
    assert d.model == "claude-haiku-4-5"


def test_general_task_routes_to_sonnet():
    r = ModelRouter()
    d = r.route("explain how postgres MVCC works in a few paragraphs")
    assert d.model == "claude-sonnet-4-6"


def test_long_classification_is_not_cheap():
    # Long prompts go to balanced even if they mention a cheap keyword.
    r = ModelRouter()
    long_task = "summarize " + ("x " * 200)
    d = r.route(long_task)
    assert d.model == "claude-sonnet-4-6"


def test_heavy_keyword_beats_cheap_keyword():
    r = ModelRouter()
    d = r.route("review and classify this migration")
    assert d.model == "claude-opus-4-8"  # 'review'/'migration' win


def test_blended_price_orders_models():
    r = ModelRouter()
    assert r.blended_price("claude-haiku-4-5") < r.blended_price("claude-sonnet-4-6")
    assert r.blended_price("claude-sonnet-4-6") < r.blended_price("claude-opus-4-8")
