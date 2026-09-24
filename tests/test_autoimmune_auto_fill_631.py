"""631 B1 · auto 42 条 liveness 填充 单测（6 例）。

**绝不落盘真实卡**：填充行为用 `apply(dry_run=True)` 与纯函数 `apply_edit_to_text` 验证。
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_auto_fill_631 as F

SAMPLE_FM = """---
id: ATOM-X-001
claim_structured:
  - id: prop-1
    subject: S
    predicate: P
    object: O
    claim_type: observation
    statement: 单行陈述
  - id: prop-2
    subject: S2
---
正文
"""


def _deliverable() -> dict:
    import json as _json
    return _json.load(open(os.path.join(F.ROOT, "data",
                                        "autoimmune_auto_fill_631.json"),
                           encoding="utf-8"))


def test_plan_auto_contract_and_deliverable_records_42():
    """plan_auto 是「当前还需自动填充的项」（实时重推导）；填充落地后应为 0（幂等）。

    42 条真实填充以**已提交的交付记录**为准，不依赖实时推导（§十 F1 诚实登记）。
    """
    items = F.plan_auto()
    assert isinstance(items, list)
    assert all(i["field"] == "liveness" and i["mode"] == "auto" for i in items), \
        "若有残留，必须全是 liveness/auto"
    d = _deliverable()
    assert d["fill"]["cards"] == 23 and d["fill"]["edits"] == 42, \
        "已提交交付记录必须记录 42 条填充 / 23 张卡"
    assert d["fill"]["unexpected_diffs"] == [], "填充必须零意外差异"
    assert d["after"]["rate_pct"] == 100.0 and d["after"]["warn_rules_total"] == 92


def test_sources_are_verifiable():
    """符号必须能从引用卡 artifact_assert 复核出来（§零.14）。

    用一张**真实已填**卡片的三元组做机制验证，不依赖实时 plan_auto 的条数。
    """
    it = {"card_rel": "atoms/conc/ATOM-CONC-FENCE-001.md",
          "prop_id": "prop-1", "value": {"symbol": "_Z10spin_plainv"}}
    s = F.verify_source(it)
    assert s["ok"], s.get("reason")
    assert s["symbol"] and s["found_in"]
    # 负例：错误符号必须判 False
    bad = {**it, "value": {"symbol": "_NOPE_not_real"}}
    assert F.verify_source(bad)["ok"] is False


def test_edit_is_insert_then_replace():
    lines = SAMPLE_FM.split("\n")
    ed = F.edit_for_lines(lines, "prop-1", "_Zsym")
    assert ed and ed["mode"] == "insert_after"
    filled = F.apply_edit_to_text(SAMPLE_FM, ed).split("\n")
    again = F.edit_for_lines(filled, "prop-1", "_Zsym")
    assert again["mode"] == "replace", "重复填充必须改为替换（不重复插入）"
    # 插在块内最后一个键行之后（不插进多行 statement 中间）
    assert filled[ed["line"] + 1] == F.liveness_line("_Zsym")


def test_apply_edit_is_idempotent():
    ed1 = F.edit_for_lines(SAMPLE_FM.split("\n"), "prop-1", "_Zsym")
    once = F.apply_edit_to_text(SAMPLE_FM, ed1)
    ed2 = F.edit_for_lines(once.split("\n"), "prop-1", "_Zsym")
    twice = F.apply_edit_to_text(once, ed2)
    assert once == twice, "施加两次必须与一次完全相同（幂等）"


def test_diff_structure_flags_only_non_liveness_changes():
    ed = F.edit_for_lines(SAMPLE_FM.split("\n"), "prop-1", "_Zsym")
    after = F.apply_edit_to_text(SAMPLE_FM, ed)
    assert F.diff_structure(SAMPLE_FM, after) == [], "只改 liveness ⇒ 零副作用"
    tampered = after.replace("claim_type: observation", "claim_type: inference")
    assert F.diff_structure(SAMPLE_FM, tampered), "非 liveness 变化必须被抓到"


def test_dry_run_does_not_touch_cards_and_check_passes():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain", "--", "atoms"],
                           cwd=F.ROOT, capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    res = F.apply(dry_run=True)
    assert snap() == before, "dry_run 不得写盘"
    # 填充已落地 ⇒ 实时方案可填项应为 0（幂等），且不产生意外差异
    assert res["edits"] == 0 and not res["unexpected_diffs"]
    # 已提交交付记录证明 42 条填充真实发生
    assert _deliverable()["fill"]["edits"] == 42
    assert F.selftest() == 0
