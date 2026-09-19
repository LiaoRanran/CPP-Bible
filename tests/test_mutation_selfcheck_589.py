"""589 任务 1 · 确定性自检「全算子 + 固定小卡集」回归锁。

快测用合成报告（monkeypatch `_run_jobs`/`selfcheck_determinism`），不跑真沙箱；
真小卡集的 clean/覆盖用 `@pytest.mark.slow`（串行 ≈ 2 分钟）。
"""
from __future__ import annotations

import mutation_fuzz as mf
import pytest

OPS7 = ("M1", "M2", "M3", "M4", "M5", "M6", "M7")


def _cards_rel():
    return [c.relative_to(mf.ROOT).as_posix() for c in mf._load_selfcheck_cards()]


def _mk_results(cards, ops, verdicts=None):
    res = []
    for c in cards:
        for op in ops:
            for i in range(2):
                point = f"pt{i}"
                v = "blocked"
                if verdicts and (c, op, point) in verdicts:
                    v = verdicts[(c, op, point)]
                res.append({"card": c, "op": op, "point": point, "verdict": v,
                            "kind": "strict", "why": None,
                            "new_block": ["X:t"] if v == "blocked" else [],
                            "new_warn": [], "replay_skipped": None, "equivalent": False})
    return res


def _fake_rep(results):
    return {"cards": [], "results": results, "variants": len(results),
            "blocked": sum(1 for r in results if r["verdict"] == "blocked"),
            "escaped": sum(1 for r in results if r["verdict"] == "escaped"),
            "n_a": sum(1 for r in results if r["verdict"] == "n_a"),
            "malformed": 0, "out_of_scope": 0, "equivalent": 0, "equivalent_invalid": 0,
            "strict_blocked": 0, "strict_rate": 0.0, "treated_rate": 0.0,
            "rates": {}, "by_operator_rates": {}, "rate_flags": [],
            "by_operator": {}, "by_card": {}, "elapsed_s": 0.0, "ge_runs": 0,
            "replay_runs": 0, "replay_skipped": 0, "escaped_list": [],
            "equivalent_keys": [], "equivalent_invalid_list": [], "jobs": 1,
            "parallel": False, "parallel_baseline_scans": 0, "root_fingerprint_ok": True}


# ── (d) 自检算子覆盖 == 全 7 算子 ───────────────────────────────────────────────
def test_selfcheck_ops_is_all_seven():
    assert tuple(mf.MUTATORS) == OPS7, "MUTATORS 不是 7 算子"
    assert mf._SELFCHECK_OPS == OPS7, "自检算子集被改回子集（须为全 7 算子）"


# ── (c) 覆盖断言 fail-loud（可证伪：缺一个算子的 blocked 即报错）───────────────
def test_coverage_ok_on_synthetic():
    rep = _fake_rep(_mk_results(_cards_rel(), OPS7))
    mf._assert_selfcheck_coverage(rep, list(OPS7))          # 不应抛


def test_coverage_fail_loud_when_op_missing():
    res = _mk_results(_cards_rel(), OPS7,
                      verdicts=None)
    # 把 M5 全部改成 escaped ⇒ M5 0 blocked
    res = [dict(r, verdict=("escaped" if r["op"] == "M5" else r["verdict"])) for r in res]
    with pytest.raises(mf.SelfcheckCoverageError):
        mf._assert_selfcheck_coverage(_fake_rep(res), list(OPS7))


# ── (a) 干净态：两次跑一致 ⇒ (True, []) ────────────────────────────────────────
def test_determinism_clean_synthetic(monkeypatch):
    base = _fake_rep(_mk_results(_cards_rel(), OPS7))
    monkeypatch.setattr(mf, "_run_jobs", lambda *a, **k: base)
    ok, diffs = mf.selfcheck_determinism([], [], 0, base, jobs=4)
    assert ok is True and diffs == []


# ── (b) 可证伪反例：第二次跑在某变体上偏斜 ⇒ (False, 非空 diffs) ───────────────
def test_determinism_falsifiable_skew(monkeypatch):
    cards_rel = _cards_rel()
    base = _fake_rep(_mk_results(cards_rel, OPS7))
    calls = {"n": 0}

    def fake_run_jobs(cards, ops, limit, jobs=1, progress=False):
        calls["n"] += 1
        if calls["n"] <= 1:
            return base
        skew = {(cards_rel[0], "M3", "pt0"): "escaped"}
        return _fake_rep(_mk_results(cards_rel, OPS7, verdicts=skew))

    monkeypatch.setattr(mf, "_run_jobs", fake_run_jobs)
    ok, diffs = mf.selfcheck_determinism([], [], 0, base, jobs=4)
    assert ok is False and diffs, "偏斜未被检出（自检绿得没判别力）"
    assert any("M3" in d and "pt0" in d for d in diffs), diffs


# ── (b') CLI：偏斜 ⇒ exit2；覆盖失效 ⇒ exit2 ───────────────────────────────────
def _stub_main(monkeypatch, tmp_path, selfcheck):
    monkeypatch.setattr(mf, "pick_cards", lambda spec: [mf.ROOT / "evidence/conc/EV-CONC-003.md"])
    monkeypatch.setattr(mf, "_run_jobs", lambda *a, **k: _fake_rep([]))
    monkeypatch.setattr(mf, "selfcheck_determinism", selfcheck)
    return mf.main(["--cards", "all", "--limit", "999", "--selfcheck-determinism",
                    "--report", str(tmp_path / "r.json")])


def test_cli_exit2_on_skew(monkeypatch, tmp_path):
    rc = _stub_main(monkeypatch, tmp_path,
                    lambda *a, **k: (False, ["[jobs1（串行对账）] x · M3 · pt0"]))
    assert rc == 2


def test_cli_exit2_on_coverage_error(monkeypatch, tmp_path):
    def boom(*a, **k):
        raise mf.SelfcheckCoverageError("M5 在自检卡集上 0 blocked")
    rc = _stub_main(monkeypatch, tmp_path, boom)
    assert rc == 2


# ── 真小卡集：覆盖 + clean（慢）───────────────────────────────────────────────
@pytest.mark.slow
def test_selfcheck_live_clean_and_coverage():
    sc = mf._load_selfcheck_cards()
    ops = list(mf._SELFCHECK_OPS)
    base = mf._run_jobs(sc, ops, len(sc), jobs=4)
    # 覆盖：每算子 ≥1 blocked（否则 fail-loud）
    mf._assert_selfcheck_coverage(base, ops)
    eq = sum(1 for r in base["results"] if r.get("equivalent"))
    assert eq >= 1, "小卡集缺少 M6 flow 等价样本（equivalent 路径未被覆盖）"
    ok, diffs = mf.selfcheck_determinism([], [], 0, base, jobs=4)
    assert ok is True, f"真小卡集两次跑不一致：{diffs[:5]}"
    assert not diffs
