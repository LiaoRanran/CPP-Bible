"""626 D1 · Authority→Projection Compiler 回归测试（≥12 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import authority_projection_compiler_626 as P  # noqa: E402
import decision_event_v2_626 as D  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")


def _compiler() -> P.AuthorityProjectionCompiler:
    return P.AuthorityProjectionCompiler()


def test_selftest_passes():
    assert P.selftest() == 0


def test_w2_projection_computable():
    c = _compiler()
    w2 = c.compile_w2()
    assert len(w2) > 0
    s = c.w2_summary()
    assert s["IN"] + s["OUT"] + s["UNDEC"] == len(w2)


def test_w2_projection_vs_grounded_labels_deviation_registered():
    """偏差登记：投影与现有 grounded_labels 的**节点粒度不同**，数值不可直接等同。

    grounded_labels：121 节点（79 命题 + 35 MIS + 7 OUT）——命题/MIS 级。
    本投影：以 Authority ledger 的 **edge_id 为节点**（含 ::prop-N 后缀）⇒ 粒度更细。
    两者**尚未数值对齐**（留 627 做节点归一化）。本测试锁定"差异存在且已被记录"这一事实。
    """
    c = _compiler()
    w2 = c.compile_w2()
    import json
    g = json.load(open(os.path.join(ROOT, "data", "grounded_labels_w2.json"),
                       encoding="utf-8"))
    gs = g.get("summary", {})
    assert gs.get("nodes") == 121
    assert len(w2) != gs.get("nodes")          # 粒度不同 ⇒ 数量不同（诚实）


def test_pck_projection_all_83():
    c = _compiler()
    p = c.compile_pck_all()
    assert p["count"] == 83


def test_pck_projection_has_both_policies():
    c = _compiler()
    p = c.compile_pck_all()
    assert "strict_authorized" in p and "relaxed_authorized" in p
    assert p["delta_relaxed_minus_strict"] == (
        p["relaxed_authorized"] - p["strict_authorized"])


def test_pck_cross_granularity_warning():
    """判据 7：只有 edge-level authority 时不自动升级为 authorized。"""
    c = _compiler()
    p = c.compile_pck_all()
    assert "cross_granularity_warned" in p
    r = c.compile_pck("ATOM-CONC-RACE-001")
    assert "cross_granularity_warning" in r
    # 无 card-level authority ⇒ 不得为 authorized
    assert r["strict"]["status"] != "authorized"


def test_determinism():
    c = _compiler()
    assert c.verify_determinism()
    assert c._digest({"w2": c.compile_w2()}) == c._digest({"w2": c.compile_w2()})


def test_traceability():
    c = _compiler()
    tr = c.trace_projection("W2", list(c.compile_w2())[0])
    assert isinstance(tr, list)
    p = c.compile_pck("ATOM-CONC-RACE-001")
    assert isinstance(p["source_authority_events"], list)


def test_readonly_ledger_unchanged():
    c = _compiler()
    n = len(c.ledger)
    c.compile_all()
    assert len(c.ledger) == n
    assert c.ledger.verify_chain()


def test_empty_ledger_handled():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "empty.jsonl")
        open(p, "w").close()
        c = P.AuthorityProjectionCompiler(p)
        assert c.compile_w2() == {}
        assert c.verify_determinism()


def test_feature_flag_default_off():
    """向后兼容：默认未启用 V2 关键路径（环境变量默认 0）。"""
    assert P.ENV_FLAG == "QUEYI_AUTHORITY_V2"
    prev = os.environ.get(P.ENV_FLAG)
    os.environ.pop(P.ENV_FLAG, None)
    assert P.v2_enabled() is False
    os.environ[P.ENV_FLAG] = "1"
    assert P.v2_enabled() is True
    if prev is None:
        os.environ.pop(P.ENV_FLAG, None)
    else:
        os.environ[P.ENV_FLAG] = prev


def test_compile_all_returns_five_projections():
    c = _compiler()
    r = c.compile_all()
    for k in ("W2", "PCK", "GOLDEN", "DASHBOARD", "TEXTBOOK_SAMPLE"):
        assert k in r
    assert r["projection_rules_version"] == P.PROJECTION_RULES_VERSION


def test_integration_with_decision_event_v2():
    c = _compiler()
    evs = c.ledger.all_events()
    assert all(isinstance(e, D.DecisionEvent) for e in evs)
    assert c.ledger.independent_human_review_count() == 0
