from agent_workbench.governor import Budget, Governor
from agent_workbench.tracing import RunTotals


def _totals(cost=0.0, in_tok=0, out_tok=0, tools=0):
    t = RunTotals()
    t.cost_usd = cost
    t.input_tokens = in_tok
    t.output_tokens = out_tok
    t.tool_calls = tools
    return t


def test_under_budget_not_exceeded():
    g = Governor(Budget(max_usd=1.0, max_total_tokens=1000, max_tool_calls=10))
    assert not g.check(_totals(cost=0.5, in_tok=100, out_tok=100, tools=3)).exceeded


def test_cost_over_budget():
    g = Governor(Budget(max_usd=0.10))
    st = g.check(_totals(cost=0.25))
    assert st.exceeded and "cost" in st.reason


def test_tokens_over_budget():
    g = Governor(Budget(max_total_tokens=500))
    st = g.check(_totals(in_tok=400, out_tok=200))
    assert st.exceeded and "tokens" in st.reason


def test_tool_calls_over_budget():
    g = Governor(Budget(max_tool_calls=2))
    st = g.check(_totals(tools=3))
    assert st.exceeded and "tool calls" in st.reason


def test_no_limits_never_exceeds():
    g = Governor(Budget())
    assert not g.check(_totals(cost=999, in_tok=10**9, tools=10**6)).exceeded
