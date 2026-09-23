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


def test_plan_auto_is_42_liveness_items():
    items = F.plan_auto()
    assert len(items) == 42
    assert all(i["field"] == "liveness" and i["mode"] == "auto" for i in items)
    assert all(i["rule"] == "OBSERVATION-LIVENESS" for i in items)
    assert len({i["card_rel"] for i in items}) == 23


def test_sources_are_verifiable():
    """抽查 3 条：符号必须能从引用卡 artifact_assert 复核出来（§零.14）。"""
    for it in F.plan_auto()[:3]:
        s = F.verify_source(it)
        assert s["ok"], f"{it['card_id']}/{it['prop_id']}: {s.get('reason')}"
        assert s["symbol"] and s["found_in"]


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
    assert res["cards"] == 23 and res["edits"] == 42
    assert not res["unexpected_diffs"]
    assert F.selftest() == 0
