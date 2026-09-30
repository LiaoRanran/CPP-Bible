# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""667 阶段2 · 判决页数据工具（`tools/web_verdicts_667.py`）回归锁。

锁的不是"当前数字是多少"，而是**不变量**（666 A2 的三选一原则：写死口径，不写死测量值）：
  ① 判决历史只收**有逐条结果**的产物，聚合型样本必须登记进 `excluded`；
  ② 每个比率都带分母，且**能按分母重算出来**（R1）；
  ③ 漂移是**关系**不是常量：`drift == (stored != fresh)`，人裁决后自动翻转；
  ④ 缺失项记 None 并进 `unavailable`，不用 0 / 占位值冒充；
  ⑤ `--write` 后 `--check` 一致（幂等）。
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402
import gate_engine as ge  # noqa: E402
import web_verdicts_667 as V  # noqa: E402

FOUR_STATES = {"pass", "pass_with_exception", "fail", "unknown"}


def test_selftest_passes():
    assert V.selftest() == 0


def test_dashboard_matches_fact_sources():
    d = V.build()
    m = d["dashboard"]
    assert m["cards_real"] == counts.ATOMS_REAL
    assert m["cards_draft"] == counts.ATOMS_DRAFT
    assert m["cards_total"] == counts.ATOMS_TOTAL
    assert m["rules_total"] == len(ge.RULES)


def test_ledger_count_matches_file():
    m = V.build()["dashboard"]
    n = sum(1 for ln in open(os.path.join(ROOT, "data/646_authority_rule_annotation.jsonl"),
                             encoding="utf-8") if ln.strip())
    assert m["ledger_events"] == n


def test_verdicts_only_from_per_item_sources():
    d = V.build()
    rows = d["verdicts"]
    assert rows, "判决历史不应为空"
    for r in rows:
        assert r["state"] in FOUR_STATES, f"{r['id']} 的四态不在四态集合里"
        assert r["when"] and r["source"] and r["repro"]
    # 聚合型样本不许被编造成逐条行 ⇒ 必须出现在 excluded 里
    joined = " ".join(d["excluded"])
    assert "holdout_reveal_3_665.json" in joined
    assert "external_corpus_reveal_665.json" in joined
    assert "counterfactual_cases_665.json" in joined


def test_verdicts_sorted_time_desc():
    rows = V.build()["verdicts"]
    assert all(rows[i]["when"] >= rows[i + 1]["when"] for i in range(len(rows) - 1))


def test_external_rate_is_arithmetically_consistent():
    """R1：比率必须能按它自己声明的分母**重算出来**。"""
    e = V.build()["dashboard"]["external"]
    assert e["den"] == e["catch"] + e["miss"]
    assert e["rate_pct"] == round(e["catch"] / e["den"] * 100, 1)
    assert e["rate_pct_all"] == round(e["catch"] / e["total"] * 100, 1)
    assert "denominator" in e and e["denominator"]


def test_drift_is_a_relation_not_a_constant():
    """漂移是**关系**：落盘值 != 现算值 ⇒ 必须标 drift。人裁决后自动翻转（不锁死数字）。"""
    h = V.build()["dashboard"]["holdout"]
    assert h["drift"] == (h.get("stored_rate_pct") != h.get("rate_pct"))
    assert h["den"] == h["catch"] + h["miss"]
    assert "denominator" in h


def test_compare_rows_carry_kind_and_note():
    for r in V.build()["compare"]:
        assert r["kind"] in {"drift", "caliber", "frozen", "ok"}
        assert r["note"] and r["metric"] and r["left"] and r["right"]


def test_missing_items_are_registered_not_faked():
    d = V.build()
    assert isinstance(d["unavailable"], list)
    m = d["dashboard"]
    for k, v in m.items():
        if v is None:
            assert d["unavailable"], f"{k} 为 None 却没有任何 unavailable 登记（不许用 0/占位值冒充）"


def test_write_then_check_is_idempotent(tmp_path, monkeypatch):
    out = tmp_path / "verdicts_667.json"
    monkeypatch.setattr(V, "OUT", str(out))
    assert V.main(["--write"]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema"] == "queyi-web-verdicts/667"
    assert data["verdicts_total"] == len(data["verdicts"])
    assert V.main(["--check"]) == 0


def test_check_detects_tampering(tmp_path, monkeypatch):
    """射程自检（R4）：改一个数字必须变红 —— 否则这个 --check 就是假绿。"""
    out = tmp_path / "verdicts_667.json"
    monkeypatch.setattr(V, "OUT", str(out))
    assert V.main(["--write"]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    data["dashboard"]["holdout"]["rate_pct"] = 99.9
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    assert V.main(["--check"]) == 1, "改了检出率却仍报绿 ⇒ --check 没进射程"
