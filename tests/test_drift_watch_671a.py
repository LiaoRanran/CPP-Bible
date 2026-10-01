# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_drift_watch_671a.py — 671a B 的回归测试（>=20 例）。

四组新判据各有正/反例：论文↔产物、前端↔产物、baseline 三臂、门禁规则；
再加跨时间协议的边界（正好 ±10% 不判、越阈值 + 有实验记录 ⇒ justified）。
全部在 tmp_path 里构造最小仓库，不触碰真实仓库。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import drift_watch_671a as D  # noqa: E402


@pytest.fixture(autouse=True)
def _clean_engine_module_cache():
    """每个用例后清掉 `gate_engine` 的模块缓存。

    为什么：`drift_watch_670c.metric_rules()` 是**按名字** `import gate_engine`，
    而 tmp 夹具里也有 `tools/gate_engine.py`（假引擎，2 条规则）。用例跑完后这个假模块
    会留在全局缓存里，害得**真实仓库**的规则数读成 2（67 → 2 ⇒ -97% 假漂移）。
    工具侧已有 `unpoison_engine_cache()` 护栏，这里再保证会话干净。
    """
    yield
    sys.modules.pop("gate_engine", None)


# ─────────────────────────────────────────────────────────────────────────────
# helper
# ─────────────────────────────────────────────────────────────────────────────

def wj(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")


def wt(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def arm_block(k: int, miss: int, total: int) -> dict:
    n = k + miss
    return {"catch": k, "miss": miss, "unknown": total - n, "not_error": 0, "total": total,
            "all_samples": {"k": k, "n": total, "numerator": k, "denominator": total,
                            "point": k / total},
            "measurable": {"k": k, "n": n, "numerator": k, "denominator": n,
                           "point": (k / n) if n else None}}


def mk_root(tmp: Path, *, paper_pct: float = 87.5, web_pct: float = 87.5,
            rules_block: int = 1, rules_n: int = 2) -> Path:
    # 产物 + 三方配置（guard 的那份配置复用，保证两工具口径一致）
    wj(tmp / "data" / "prod_a.json", {"catch": 14, "miss": 2})
    wj(tmp / "data" / "guard_artifacts_671a.json", {
        "metrics": [{"key": "rate_a", "kind": "rate",
                     "artifact": {"path": "data/prod_a.json", "k": "catch",
                                  "n_sum": ["catch", "miss"]},
                     "paper": {"path": "research/paper_v0.8.md", "k": 14, "n": 16},
                     "web": [{"path": "web/data/metrics.json", "pointer": "metrics.rate_a"}]}],
    })
    wt(tmp / "research" / "paper_v0.8.md", f"检出率 {paper_pct}%（14/16，95% CI）。\n")
    wj(tmp / "web" / "data" / "metrics.json", {"metrics": {"rate_a": web_pct}})
    # baseline 三臂：同一批样本（holdout 17 / corpus 40）
    wj(tmp / "data" / "experiments" / "baseline_fd.json",
       {"arm": "fd", "holdout": arm_block(14, 2, 17), "corpus": arm_block(14, 18, 40)})
    wj(tmp / "data" / "experiments" / "baseline_static.json",
       {"arm": "static", "holdout": arm_block(1, 15, 17), "corpus": arm_block(4, 28, 40)})
    wj(tmp / "data" / "experiments" / "baseline_random.json",
       {"arm": "random", "holdout": arm_block(1, 15, 17), "corpus": arm_block(1, 31, 40)})
    # 门禁规则：engine（执行权威）+ 缓存 + 文档声明
    wt(tmp / "tools" / "gate_engine.py",
       "RULES = [\n"
       + "".join(f'    {{"rule": "R{i}", "severity": "block"}},\n' for i in range(rules_block))
       + "".join(f'    {{"rule": "W{i}", "severity": "warn"}},\n'
                 for i in range(max(0, rules_n - rules_block)))
       + "]\n")
    wj(tmp / "data" / "_gate_rules.json",
       [{"rule": f"R{i}", "severity": "block"} for i in range(rules_block)]
       + [{"rule": f"W{i}", "severity": "warn"} for i in range(max(0, rules_n - rules_block))])
    wj(tmp / "web" / "data" / "status.json",
       {"rules": {"rules_total": rules_n, "rules_block": rules_block}})
    # 跨时间核心数字的四个来源（其余采集器缺文件 ⇒ 记 unavailable，不影响用例）
    wj(tmp / "data" / "holdout_reveal_3_665.json",
       {"error_subset": {"catch": 14, "miss": 2}})
    wj(tmp / "data" / "external_corpus_reveal_665.json", {"catch": 14, "miss": 18})
    wj(tmp / "data" / "656_mutation_report_core.json", {"killed": 110, "survived": 3})
    return tmp


def out_of(tmp: Path) -> Path:
    return tmp / D.DEFAULT_OUT


def ev(tmp: Path, **kw):
    kw.setdefault("write", True)
    return D.evaluate(tmp, out_of(tmp), **kw)


def touch_future(p: Path, delta: float = 30.0) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('{"experiment": "x"}\n', encoding="utf-8")
    t = time.time() + delta
    os.utime(p, (t, t))


# ─────────────────────────────────────────────────────────────────────────────
# ① 阈值/相对变化（与 670c 同协议）
# ─────────────────────────────────────────────────────────────────────────────

def test_threshold_boundary():
    assert D.rel_change(100, 110) == 0.1
    assert D.over_threshold(D.rel_change(100, 110), 0.10) is False, "正好 10% 不算漂移"
    assert D.over_threshold(D.rel_change(100, 110.01), 0.10) is True
    assert D.over_threshold(D.rel_change(None, 5), 0.10) is False, "缺一侧 ⇒ 不可比"
    assert D.over_threshold(D.rel_change(0, 3), 0.10) is True, "0 → 非 0 ⇒ 从无到有"


# ─────────────────────────────────────────────────────────────────────────────
# ② 论文版本选择 + 论文↔产物
# ─────────────────────────────────────────────────────────────────────────────

def test_paper_files_picks_latest_only(tmp_path):
    root = mk_root(tmp_path)
    wt(root / "research" / "paper_v0.7.md", "旧稿 66.7%（14/21）。\n")
    wt(root / "research" / "paper_v0.9.md", "新稿 87.5%（14/16）。\n")
    files, ignored = D.paper_files(root)
    assert [f.name for f in files] == ["paper_v0.9.md"], "只判当前稿（版本号最大）"
    assert "paper_v0.8.md" in ignored and "paper_v0.7.md" in ignored
    allf, ign2 = D.paper_files(root, all_versions=True)
    assert len(allf) == 3 and ign2 == []


def test_paper_consistent_passes(tmp_path):
    root = mk_root(tmp_path)
    got = D.check_paper(root, 0.5)
    assert got["status"] == D.PASS and len(got["matched"]) >= 1
    assert got["matched"][0]["ok"] is True


def test_paper_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path, paper_pct=80.0)
    got = D.check_paper(root, 0.5)
    assert got["status"] == D.DRIFT
    assert got["drifts"][0]["kind"] == "paper_vs_product"
    assert "差" in got["drifts"][0]["message"]


def test_paper_within_tolerance_passes(tmp_path):
    """43.8%（14/32）与产物 14/32=43.75% 属同一数字的不同写法（差 0.05pp）。"""
    root = mk_root(tmp_path, paper_pct=43.8)
    wj(root / "data" / "prod_a.json", {"catch": 14, "miss": 18})       # 14/32 = 43.75%
    wt(root / "research" / "paper_v0.8.md", "corpus 43.8%（14/32，CP 95%）。\n")
    got = D.check_paper(root, 0.5)
    assert got["status"] == D.PASS
    assert any(m["k"] == 14 and m["n"] == 32 for m in got["matched"])


def test_paper_unmatched_recorded_not_drift(tmp_path):
    root = mk_root(tmp_path)
    wt(root / "research" / "paper_v0.8.md", "引用外部文献 76%（38/50）。\n检出率 87.5%（14/16）。\n")
    got = D.check_paper(root, 0.5)
    assert got["status"] == D.PASS
    assert any(u["k"] == 38 and u["n"] == 50 for u in got["unmatched"]), "找不到对应产物的率要登记"


def test_paper_candidates_cover_three_sources(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "data" / "experiments" / "corpus_layered_670a.json",
       {"layers": {"sanitizer": {"numerator": 10, "denominator": 14}}})
    cands, problems = D.paper_candidates(root)
    groups = {c["group"] for c in cands}
    assert {"guard_artifacts", "baseline_arm", "corpus_layer"} <= groups
    assert not problems


def test_paper_candidates_report_missing_product(tmp_path):
    root = mk_root(tmp_path)
    (root / "data" / "prod_a.json").unlink()
    cands, problems = D.paper_candidates(root)
    assert problems and not any(c["group"] == "guard_artifacts" for c in cands)


# ─────────────────────────────────────────────────────────────────────────────
# ③ 前端：声明指针 + 扫描
# ─────────────────────────────────────────────────────────────────────────────

def test_web_declared_consistent(tmp_path):
    root = mk_root(tmp_path)
    got = D.check_web(root, 0.5, None, 0.10, [])
    assert got["status"] == D.PASS
    assert got["declared"][0]["ok"] is True


def test_web_declared_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path, web_pct=80.0)
    got = D.check_web(root, 0.5, None, 0.10, [])
    assert got["status"] == D.DRIFT
    assert got["drifts"][0]["kind"] == "web_vs_product"


def test_web_missing_pointer_is_drift(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"other": 1}})
    got = D.check_web(root, 0.5, None, 0.10, [])
    assert got["status"] == D.DRIFT
    assert got["drifts"][0]["kind"] == "web_missing_pointer"


def test_web_missing_file_is_drift(tmp_path):
    root = mk_root(tmp_path)
    (root / "web" / "data" / "metrics.json").unlink()
    got = D.check_web(root, 0.5, None, 0.10, [])
    assert got["status"] == D.DRIFT
    assert got["drifts"][0]["kind"] == "web_missing_file"


def test_scan_web_rates_finds_nested_and_named_rates(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": 87.5, "carry_rate_pct": 1.0},
        "deep": {"nested": {"x_pct": 2.0}}, "count": 5})
    rows, flat = D.scan_web_rates(root)
    keys = set(flat)
    assert "web/data/metrics.json.metrics.carry_rate_pct" in keys
    assert "web/data/metrics.json.deep.nested.x_pct" in keys
    assert all("count" not in k for k in keys), "不带 pct/rate 的键不是率"


def test_web_rate_changed_over_time_is_drift(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": 87.5}, "extra_rate_pct": 10.0})
    r1 = ev(root)
    assert r1["overall"] == D.FIRST_RUN, "首跑只标定"
    wj(root / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": 87.5}, "extra_rate_pct": 20.0})     # +100%
    r2 = ev(root)
    assert r2["overall"] == D.DRIFT
    assert any(d["kind"] == "web_rate_changed" for d in r2["deterministic_drifts"])


def test_web_rate_change_with_fresh_experiment_is_justified(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": 87.5}, "extra_rate_pct": 10.0})
    ev(root)
    wj(root / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": 87.5}, "extra_rate_pct": 20.0})
    touch_future(root / "data" / "experiments" / "671a_exp.json")
    r2 = ev(root)
    assert r2["overall"] == D.PASS, "有更新的实验记录 ⇒ 跨时间变化有据可查"
    assert r2["drifted_justified"], "justified 仍要打印（不静默）"


# ─────────────────────────────────────────────────────────────────────────────
# ④ baseline 三臂一致性
# ─────────────────────────────────────────────────────────────────────────────

def test_baseline_arms_consistent(tmp_path):
    root = mk_root(tmp_path)
    got = D.check_baseline_arms(root)
    assert got["status"] == D.PASS
    assert got["arms"]["fd"]["holdout"]["n"] == 16


def test_baseline_arm_sample_count_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path)
    blk = arm_block(1, 19, 40)
    blk["measurable"]["n"] = 18                       # 分母与 catch+miss 不符
    blk["measurable"]["denominator"] = 18
    wj(root / "data" / "experiments" / "baseline_random.json",
       {"arm": "random", "holdout": arm_block(1, 15, 17), "corpus": blk})
    got = D.check_baseline_arms(root)
    assert got["status"] == D.DRIFT
    assert any(d["kind"] == "baseline_denominator_mismatch" for d in got["drifts"])


def test_baseline_all_samples_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path)
    blk = arm_block(14, 2, 17)
    blk["all_samples"]["n"] = 16                      # 全样本口径与 total 不符
    wj(root / "data" / "experiments" / "baseline_fd.json",
       {"arm": "fd", "holdout": blk, "corpus": arm_block(14, 18, 40)})
    got = D.check_baseline_arms(root)
    assert any(d["kind"] == "baseline_all_samples_mismatch" for d in got["drifts"])


def test_baseline_arm_total_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "data" / "experiments" / "baseline_static.json",
       {"arm": "static", "holdout": arm_block(1, 15, 20), "corpus": arm_block(4, 28, 40)})
    got = D.check_baseline_arms(root)
    assert any(d["kind"] == "baseline_sample_mismatch" for d in got["drifts"]), \
        "三臂样本数不一致 ⇒ 配对可比的前提不成立"


def test_baseline_rate_not_reproducible_is_drift(tmp_path):
    root = mk_root(tmp_path)
    blk = arm_block(14, 2, 17)
    blk["measurable"]["point"] = 0.99                       # 写死的数与 k/n 不符
    wj(root / "data" / "experiments" / "baseline_fd.json",
       {"arm": "fd", "holdout": blk, "corpus": arm_block(14, 18, 40)})
    got = D.check_baseline_arms(root)
    assert any(d["kind"] == "baseline_rate_not_reproducible" for d in got["drifts"])


def test_baseline_missing_arm_is_drift(tmp_path):
    root = mk_root(tmp_path)
    (root / "data" / "experiments" / "baseline_random.json").unlink()
    got = D.check_baseline_arms(root)
    assert any(d["kind"] == "baseline_arm_missing" for d in got["drifts"])


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 门禁规则漂移
# ─────────────────────────────────────────────────────────────────────────────

def test_gate_rules_consistent(tmp_path):
    root = mk_root(tmp_path)
    got = D.check_gate_rules(root)
    assert got["status"] == D.PASS
    assert got["engine_rules"] == got["dump_rules"] == 2
    assert got["severity"] == {"block": 1, "warn": 1}


def test_gate_rules_count_mismatch_is_drift(tmp_path):
    """engine（执行权威）比缓存/文档多一条 ⇒ 数量对不上，必须红。"""
    root = mk_root(tmp_path, rules_n=2)
    wt(root / "tools" / "gate_engine.py",
       'RULES = [\n'
       '    {"rule": "R0", "severity": "block"},\n'
       '    {"rule": "W0", "severity": "warn"},\n'
       '    {"rule": "NEW", "severity": "warn"},\n'
       ']\n')
    got = D.check_gate_rules(root)
    assert got["status"] == D.DRIFT
    assert any(d["kind"] == "gate_rules_count_mismatch" for d in got["drifts"])
    assert any(d["kind"] == "gate_severity_distribution_mismatch" for d in got["drifts"]), \
        "severity 分布也要比（warn 1 → 2）"


def test_gate_severity_doc_mismatch_is_drift(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "web" / "data" / "status.json", {"rules": {"rules_total": 2, "rules_block": 2}})
    got = D.check_gate_rules(root)
    assert any(d["kind"] == "gate_severity_doc_mismatch" for d in got["drifts"])


def test_gate_engine_unreadable_is_drift(tmp_path):
    root = mk_root(tmp_path)
    wt(root / "tools" / "gate_engine.py", "def f(:\n")          # 语法错误
    got = D.check_gate_rules(root)
    assert got["status"] == D.DRIFT
    assert any(d["kind"] == "gate_engine_unreadable" for d in got["drifts"])


# ─────────────────────────────────────────────────────────────────────────────
# ⑥ 主流程 / CLI / 基线生命周期
# ─────────────────────────────────────────────────────────────────────────────

def test_first_run_writes_baseline_and_exit_0(tmp_path):
    root = mk_root(tmp_path)
    rep = ev(root)
    assert rep["overall"] == D.FIRST_RUN and rep["baseline_found"] is False
    assert out_of(root).is_file(), "首跑要落盘基线"
    assert "web_rates" in json.loads(out_of(root).read_text(encoding="utf-8"))


def test_corrupt_previous_report_is_first_run(tmp_path):
    root = mk_root(tmp_path)
    out_of(root).parent.mkdir(parents=True, exist_ok=True)
    out_of(root).write_text("{ 不是 JSON", encoding="utf-8")
    rep = ev(root)
    assert rep["overall"] == D.FIRST_RUN


def test_cli_exit_1_on_drift_and_0_on_pass(tmp_path, capsys):
    root = mk_root(tmp_path)
    capsys.readouterr()
    assert D.main(["--root", str(root), "--out", str(out_of(root))]) == 0
    wt(root / "research" / "paper_v0.8.md", "检出率 80.0%（14/16）。\n")
    capsys.readouterr()
    assert D.main(["--root", str(root), "--out", str(out_of(root))]) == 1, "确定式不一致必须 exit 1"


def test_report_schema_keys(tmp_path, capsys):
    root = mk_root(tmp_path)
    capsys.readouterr()
    assert D.main(["--root", str(root), "--out", str(out_of(root)), "--json"]) == 0
    d = json.loads(capsys.readouterr().out)
    for k in ("schema", "tool", "generated_at", "threshold", "threshold_pct", "tolerance_pp",
              "overall", "metrics", "values", "checks", "deterministic_drifts", "ok",
              "drifted_unjustified", "drifted_justified", "experiments", "notes",
              "baseline_values_for_next_run", "web_rates_for_next_run"):
        assert k in d, f"报告缺字段 {k}"
    assert d["schema"] == D.SCHEMA
    assert set(d["checks"]) == {"paper", "web", "baseline_arms", "gate_rules"}
    assert d["threshold"] == 0.10


def test_threshold_flag_percent_form(tmp_path, capsys):
    root = mk_root(tmp_path)
    capsys.readouterr()
    D.main(["--root", str(root), "--out", str(out_of(root)), "--threshold", "5", "--json"])
    d = json.loads(capsys.readouterr().out)
    assert d["threshold"] == 0.05 and d["threshold_pct"] == 5.0


def test_deterministic_drifts_are_not_excused_by_experiments(tmp_path):
    """确定式不一致（论文与产物矛盾）**不接受**实验记录豁免。"""
    root = mk_root(tmp_path)
    ev(root)
    touch_future(root / "data" / "experiments" / "fresh.json")
    wt(root / "research" / "paper_v0.8.md", "检出率 80.0%（14/16）。\n")
    rep = ev(root)
    assert rep["overall"] == D.DRIFT, "有实验记录也不能让「两处互相矛盾」变绿"


# ─────────────────────────────────────────────────────────────────────────────
# ⑦ 真实仓库（现状态无漂移）
# ─────────────────────────────────────────────────────────────────────────────

def test_real_repo_paper_scan_no_drift():
    got = D.check_paper(ROOT, D.DEFAULT_TOL_PP)
    assert got["status"] == D.PASS, f"论文与产物出现漂移：{got['drifts'][:3]}"
    assert len(got["matched"]) >= 5
    latest, ignored = D.paper_files(ROOT)
    assert got["files"] == [str(latest[0].relative_to(ROOT).as_posix())], \
        "只判当前稿（版本号最大的那一份）；历史稿只列出不判红"
    assert got["ignored_versions"], "仓库里有历史稿 ⇒ 必须列出被忽略的版本"


def test_real_repo_baseline_arms_and_gate_rules_consistent():
    arms = D.check_baseline_arms(ROOT)
    assert arms["status"] == D.PASS, arms["drifts"]
    gates = D.check_gate_rules(ROOT)
    assert gates["status"] == D.PASS, gates["drifts"]
    assert gates["engine_rules"] == gates["dump_rules"] == 67


def test_real_repo_no_drift():
    rep = D.evaluate(ROOT, ROOT / D.DEFAULT_OUT, write=False)
    assert rep["overall"] == D.PASS, f"真实仓库出现漂移：{rep['deterministic_drifts'][:2]}"
    assert rep["drifted_unjustified"] == []


# ─────────────────────────────────────────────────────────────────────────────
# ⑧ 跨测试 import 污染（实测踩到：tmp 的假 gate_engine 把真实规则数读成 2）
# ─────────────────────────────────────────────────────────────────────────────

def test_engine_cache_poisoning_is_detected_and_cleaned(tmp_path):
    sys.modules.pop("gate_engine", None)
    root = mk_root(tmp_path, rules_n=2)                  # tmp 里有假的 tools/gate_engine.py
    D.core_metrics(root)                                 # 670c 的按名 import 会缓存假引擎
    assert "gate_engine" in sys.modules, "前提：这一步确实会污染模块缓存"
    vals = {m["key"]: m for m in D.core_metrics(ROOT)}   # 护栏应在这一跳生效
    assert vals["rules_total"]["value"] == 67, "护栏之后规则数必须是真实值（不是假引擎的 2）"
    assert vals["rules_total"].get("cache_note"), "清缓存这件事要写进指标明细（不许静默）"
    assert D.unpoison_engine_cache(ROOT) is None, "已清干净 ⇒ 不重复报（避免狼来了）"


def test_engine_cache_clean_when_already_correct(tmp_path):
    """缓存里就是本仓库的 gate_engine 时，护栏不该报「清过」（避免狼来了）。"""
    D.core_metrics(ROOT)
    assert D.unpoison_engine_cache(ROOT) is None


def test_selftest_passes(capsys):
    assert D.selftest() == 0
    assert "selftest: PASS" in capsys.readouterr().out
