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
    """628 A1 更新：**粒度偏差已被归一化解决**（627 A1 + 628 A1 flag 真接入）。

    626 时投影以 edge_id 为节点（519）与 grounded_labels（121）粒度不同——该偏差
    曾在此锁定。627 A1 归一化 + 628 A1 flag 真接入后，compile_w2 在 V1/V2 两种模式
    下都返回 121 节点并与 grounded_labels 逐节点一致，故本测试改为锁定"已对齐"。
    """
    c = _compiler()
    w2 = c.compile_w2()
    import json
    g = json.load(open(os.path.join(ROOT, "data", "grounded_labels_w2.json"),
                       encoding="utf-8"))
    gs = g.get("summary", {})
    assert gs.get("nodes") == 121
    assert len(w2) == gs.get("nodes")          # 归一化后节点数一致
    expected = {k: v["label"] for k, v in g["nodes"].items()}
    assert w2 == expected                      # 逐节点标签一致（V1 模式）


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
    """628 A1 更新：V1 模式下 W2 读 legacy grounded_labels（与 ledger 无关）；
    V2 模式下空 ledger ⇒ 全部节点 IN（无生效攻击）。两者都不抛异常即可。"""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "empty.jsonl")
        open(p, "w").close()
        c = P.AuthorityProjectionCompiler(p)
        assert isinstance(c.compile_w2(), dict)   # V1：grounded_labels 兜底
        assert c.verify_determinism()
        os.environ[P.ENV_FLAG] = "1"
        try:
            c2 = P.AuthorityProjectionCompiler(p)
            assert isinstance(c2.compile_w2(), dict)   # V2：空 ledger 不抛异常
        finally:
            os.environ.pop(P.ENV_FLAG, None)


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
