"""557 Part A · 人审分桶器回归（fast）：四桶正确 / 桶②刻意排除识别 / 排序确定 / 空集不崩。

只测**分桶逻辑**：用 Finding 替身与 tmp 卡，不跑真编译、不写受控目录。
"""
from __future__ import annotations

import json

import gate_engine as ge
import review_triage as rt


def _F(rule: str, sev: str = "warn", target: str = "x.md", msg: str = "m"):
    return ge.Finding(rule, sev, target, msg)


def test_bucket1_migration_rules():
    """桶①：两条新规则的存量迁移债。"""
    assert rt.bucket_of(_F("ATOM-CLAIM-CONCEPT-NORMALIZED"), frozenset()) == "B1"
    assert rt.bucket_of(_F("INFERENCE-NOT-MACHINE-VERIFIED"), frozenset()) == "B1"


def test_bucket2_design_exclusion_vs_real(tmp_path, monkeypatch):
    """桶②：(a) 锚落在被刻意排除的 actual 段 ⇒ 预期； (b) 处处不足两锚 ⇒ 真信号转桶③。"""
    monkeypatch.setattr(rt, "ROOT", tmp_path)
    d = tmp_path / "ev"
    d.mkdir()
    # (a) body 1 锚 + 被排除段 1 锚 = 2 ⇒ 算上被排除段就成立 ⇒ 纯设计排除造成
    (d / "A.md").write_text(
        "---\nid: A\ncompiler: [gcc, clang]\nnote: Examples/a.out\n"
        "actual:\n  run_match_file: Examples/b.out\n---\n", encoding="utf-8")
    kind, ev = rt.matrix_kind("ev/A.md")
    assert kind == "a_design" and "would-be-backed" in ev
    assert rt.bucket_of(_F("EV-MATRIX-UNBACKED", "warn", "ev/A.md"), frozenset(),
                        (kind, ev)) == "B2"
    # (b) 仅被排除段 1 锚 ⇒ 仍 <2 ⇒ 真信号
    (d / "B.md").write_text(
        "---\nid: B\ncompiler: [gcc, clang]\nactual:\n  run_match_file: Examples/b.out\n---\n",
        encoding="utf-8")
    kind2, ev2 = rt.matrix_kind("ev/B.md")
    assert kind2 == "b_real" and "no-two-anchors-anywhere" in ev2
    assert rt.bucket_of(_F("EV-MATRIX-UNBACKED", "warn", "ev/B.md"), frozenset(),
                        (kind2, ev2)) == "B3"
    # (b) 完全无锚
    (d / "C.md").write_text("---\nid: C\ncompiler: [gcc, clang]\n---\n", encoding="utf-8")
    assert rt.matrix_kind("ev/C.md")[0] == "b_real"


def test_bucket3_unknown_and_exempt():
    """桶③真信号（含 advice 规则）；未知规则默认真信号（可见优先）；已豁免 → 桶④。"""
    assert rt.bucket_of(_F("EV-OUT-UNDECLARED-KEY"), frozenset()) == "B3"
    assert rt.bucket_of(_F("EV-ENV-DEPENDENT-KEY", "advice"), frozenset()) == "B3"
    assert rt.bucket_of(_F("BRAND-NEW-RULE"), frozenset()) == "B3"
    assert rt.bucket_of(_F("EV-SERVES-EXIST"), frozenset({"EV-SERVES-EXIST"})) == "B4"


def test_triage_reconciles_and_is_deterministic():
    """四桶之和 == 输入数（不漏不重）；两次运行逐字一致；完全重复 → 桶④。"""
    fs = [
        _F("ATOM-CLAIM-CONCEPT-NORMALIZED", target="a.md", msg="1"),
        _F("INFERENCE-NOT-MACHINE-VERIFIED", target="b.md", msg="2"),
        _F("EV-OUT-UNDECLARED-KEY", target="c.md", msg="3"),
        _F("EV-ENV-DEPENDENT-KEY", "advice", target="d.md", msg="4"),
        _F("EV-OUT-UNDECLARED-KEY", target="c.md", msg="3"),               # 完全重复 → B4
        _F("ATOM-CLAIM-CONCEPT-NORMALIZED", target="a.md", msg="1"),       # 完全重复 → B4
    ]
    r1, r2 = rt.triage(fs), rt.triage(fs)
    assert json.dumps(r1, sort_keys=True, ensure_ascii=False) == \
        json.dumps(r2, sort_keys=True, ensure_ascii=False), "分桶必须确定性"
    assert sum(r1["counts"].values()) == len(fs), "四桶之和须等于输入总数"
    assert r1["counts"]["B1"] == 2 and r1["counts"]["B3"] == 2 and r1["counts"]["B4"] == 2
    assert r1["totals"]["warn"] == 5 and r1["totals"]["advice"] == 1


def test_empty_findings_no_crash():
    """空 Finding 集：不崩、四桶全 0、对账闭合。"""
    r = rt.triage([])
    assert sum(r["counts"].values()) == 0 and r["totals"]["non_block"] == 0


def test_review_order_deterministic():
    """桶③排序确定性（与输入顺序无关）：权重降序 → 卡 id。"""
    items = [{"rule": "EV-SERVES-EXIST", "card": "z.md", "message": "m"},
             {"rule": "EV-OUT-UNDECLARED-KEY", "card": "a.md", "message": "m"},
             {"rule": "EV-OUT-UNDECLARED-KEY", "card": "b.md", "message": "m"}]
    o1, o2 = rt.review_order(items), rt.review_order(list(reversed(items)))
    assert o1 == o2, "排序必须与输入顺序无关"
    assert o1[0]["rule"] == "EV-OUT-UNDECLARED-KEY", "权重 90 的规则应排最前"
