"""626 D2 · Projection 扩展（golden/dashboard/textbook）回归测试（≥10 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import authority_projection_compiler_626 as P  # noqa: E402


def _c() -> P.AuthorityProjectionCompiler:
    return P.AuthorityProjectionCompiler()


def test_selftest_passes():
    assert P.selftest() == 0


def test_compile_all_has_five():
    r = _c().compile_all()
    for k in ("W2", "PCK", "GOLDEN", "DASHBOARD", "TEXTBOOK_SAMPLE"):
        assert k in r


def test_golden_never_auto_accepts_legacy():
    """核心规则：不自动采纳 legacy。"""
    g = _c().compile_golden()
    assert "accepted_legacy" in g
    assert "自动采纳" in g["rule"] and "必须关闭" in g["rule"]
    # 只有 warn_disposition + scope=accept_legacy + APPROVE 才算采纳
    assert g["accepted_legacy"] <= g["warn_disposition_events"]


def test_dashboard_statistics():
    d = _c().compile_dashboard()
    assert d["review_items_unique"] == 93            # 判据 2
    assert "review_method_distribution" in d
    assert "decision_origin_distribution" in d
    assert "ambiguity_distribution" in d
    assert d["independent_human_review_count"] == 0  # 判据 1
    assert sum(d["by_status"].values()) > 0


def test_dashboard_v2_flag_exposed():
    d = _c().compile_dashboard()
    assert "v2_enabled" in d      # dashboard 路径默认启用 V2（由环境变量控制）


def test_textbook_five_render_states():
    states = {"CERTIFIED", "CONDITIONALLY_VERIFIED", "ABSTAIN", "DISPUTED", "UNVERIFIED"}
    c = _c()
    for aid in ("ATOM-CONC-RACE-001", "ATOM-MEM-MOVE-002", "NO-SUCH-ATOM-999"):
        r = c.compile_textbook(aid)
        assert r["render_state"] in states, f"{aid}: {r['render_state']}"
        assert r["atom_id"] == aid


def test_textbook_unknown_atom_is_unverified():
    r = _c().compile_textbook("NO-SUCH-ATOM-999")
    assert r["render_state"] == "UNVERIFIED"


def test_all_projections_traceable():
    c = _c()
    g = c.compile_golden()
    assert "source_authority_events" in g
    t = c.compile_textbook("ATOM-CONC-RACE-001")
    assert "source_authority_events" in t


def test_all_projections_deterministic():
    c = _c()
    a = c._digest({"g": c.compile_golden(), "d": c.compile_dashboard(),
                   "t": c.compile_textbook("ATOM-CONC-RACE-001")})
    c2 = P.AuthorityProjectionCompiler()
    b = c2._digest({"g": c2.compile_golden(), "d": c2.compile_dashboard(),
                    "t": c2.compile_textbook("ATOM-CONC-RACE-001")})
    assert a == b


def test_empty_ledger_all_projections():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "e.jsonl")
        open(p, "w").close()
        c = P.AuthorityProjectionCompiler(p)
        assert c.compile_golden()["warn_disposition_events"] == 0
        assert c.compile_dashboard()["authority_events"] == 0
        assert c.compile_textbook("X")["render_state"] == "UNVERIFIED"


def test_textbook_does_not_touch_controlled_dirs():
    """受控目录零污染：textbook 是只读投影。"""
    before = os.path.exists(os.path.join(ROOT, "Book"))
    _c().compile_textbook("ATOM-CONC-RACE-001")
    assert os.path.exists(os.path.join(ROOT, "Book")) == before
