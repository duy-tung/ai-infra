import json
from pathlib import Path

from agent_workbench.config import Settings
from agent_workbench.tracing import Tracer, Usage, cost_of


def test_cost_of_basic():
    # 1M input @ $5 + 1M output @ $25 = $30
    usage = Usage(input_tokens=1_000_000, output_tokens=1_000_000)
    price = {"input": 5.0, "output": 25.0}
    assert round(cost_of(usage, price), 2) == 30.00


def test_cache_reads_are_cheaper():
    usage = Usage(input_tokens=0, cache_read_input_tokens=1_000_000)
    price = {"input": 5.0, "output": 25.0}
    # cache read is 0.1x input price -> $0.50
    assert round(cost_of(usage, price), 2) == 0.50


def test_tracer_writes_jsonl_and_totals(tmp_path: Path):
    settings = Settings(model="claude-opus-4-8", trace_dir=tmp_path)
    tracer = Tracer(settings)
    tracer.run_start("do a thing")
    tracer.llm_call(Usage(input_tokens=1000, output_tokens=200), "tool_use", 0.5)
    tracer.tool_call("read_file", {"path": "x"}, "allow", "read-only tool", "data", False, 0.01)
    tracer.run_end("completed", "done")

    lines = tracer.path.read_text(encoding="utf-8").strip().splitlines()
    events = [json.loads(line)["event"] for line in lines]
    assert events == ["run_start", "llm_call", "tool_call", "run_end"]

    end = json.loads(lines[-1])
    assert end["totals"]["llm_calls"] == 1
    assert end["totals"]["tool_calls"] == 1
    assert end["totals"]["cost_usd"] > 0
