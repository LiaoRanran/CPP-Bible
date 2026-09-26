"""647 A2 · DecisionEvent 严格模式回归锁（fail-open 修复 2）。

病（642 B3 审计 FO-B，实测）：`from_dict({})` ⇒ `result=APPROVE` + `decision_origin=human_observed`
（不完整事件被自动解释成"人观察过"）+ 未知字段静默丢弃。

647 A2 修法：**两个显式入口** —— `from_dict_strict()`（新事件）/ `from_dict_lenient()`（历史）。
本文件锁（编号 A2-1..A2-9）：
  * strict 缺任一必填字段 / 未知字段 / 空 dict / 非 dict / 枚举非法 ⇒ 抛 `StrictEventError`；
  * strict 不再把 `decision_origin` 默认成 `human_observed`；
  * **历史 452 条 lenient 可导入**（链有效、哈希不变、账本文件字节不变）；
  * lenient 历史语义**保留**（`from_dict` = `from_dict_lenient`，642 FO-B 复现路径仍成立）。
"""
from __future__ import annotations

import hashlib
import json

import pytest

import decision_event_v2_626 as D

FULL = {"operation": "CREATE", "result": "APPROVE", "target_type": "edge",
        "target_id": "ae-647", "review_method": "ITEM_BLIND",
        "decision_origin": "human_observed", "reviewer": "A", "decided_at": "2026-09-26"}


# ── A2-1：strict 接受完整事件；字段集与 schema 常量自洽 ─────────────────────────
def test_a2_1_strict_accepts_complete_event():
    e = D.DecisionEvent.from_dict_strict(dict(FULL))
    assert e.target_id == "ae-647" and e.result == "APPROVE"
    assert set(D.REQUIRED_FIELDS) <= set(D.KNOWN_FIELDS)
    assert "decision_origin" in D.REQUIRED_FIELDS


# ── A2-2：缺任一必填字段 ⇒ 抛（不再用默认值补全）────────────────────────────────
@pytest.mark.parametrize("field", D.REQUIRED_FIELDS)
def test_a2_2_strict_rejects_each_missing_required_field(field: str):
    d = {k: v for k, v in FULL.items() if k != field}
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict(d)


# ── A2-3：`decision_origin` 不再默认 human_observed ─────────────────────────────
def test_a2_3_decision_origin_no_longer_defaulted():
    d = {k: v for k, v in FULL.items() if k != "decision_origin"}
    with pytest.raises(D.StrictEventError) as ei:
        D.DecisionEvent.from_dict_strict(d)
    assert "decision_origin" in str(ei.value)


# ── A2-4：未知字段 ⇒ 抛（不再静默丢弃）─────────────────────────────────────────
def test_a2_4_strict_rejects_unknown_field():
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict({**FULL, "decision_origins": "human_observed"})


# ── A2-5：空 dict / 非 dict / 枚举非法 ⇒ 抛（FO-B 的三种形态）───────────────────
def test_a2_5_strict_rejects_empty_and_bad_events():
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict({})
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict([])          # type: ignore[arg-type]
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict({**FULL, "result": "BOGUS"})
    # MODIFY 缺 modification / REPLACE 缺 supersedes（复用 validate 口径）
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict({**FULL, "result": "MODIFY"})
    with pytest.raises(D.StrictEventError):
        D.DecisionEvent.from_dict_strict({**FULL, "operation": "REPLACE"})


# ── A2-6：lenient 历史语义保留（642 B3 FO-B 复现路径不能被这次修复"洗掉"）───────
def test_a2_6_lenient_semantics_preserved():
    e = D.DecisionEvent.from_dict({})
    assert e.result == "APPROVE" and e.decision_origin == "human_observed"
    assert D.DecisionEvent.from_dict_lenient({}).review_method == "BATCH_AUTH"
    assert D.DecisionEvent.from_dict({"target_id": "z"}).target_id == "z"


# ── A2-7：历史 452 条 lenient 可导入，链有效，且**账本文件字节不变** ────────────
def test_a2_7_history_imports_lenient_and_file_unchanged():
    import os
    path = D.LEDGER_PATH
    before = hashlib.sha256(open(path, "rb").read()).hexdigest()
    led = D.load_ledger(path)                       # 默认 lenient
    assert len(led) == 452, len(led)
    assert led.verify_chain(), "历史哈希链必须仍有效"
    after = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert before == after, "读取历史账本不得写入"
    assert os.path.getsize(path) > 0


# ── A2-8：strict 导入一旦遇到不完整行 ⇒ 抛（不静默降级）─────────────────────────
def test_a2_8_strict_import_raises_on_incomplete_line(tmp_path):
    good = D.DecisionEvent(**FULL).to_dict()
    bad = {"operation": "CREATE", "result": "APPROVE"}      # 缺大半字段
    p = tmp_path / "l.jsonl"
    p.write_text(json.dumps(good, ensure_ascii=False) + "\n"
                 + json.dumps(bad, ensure_ascii=False) + "\n", encoding="utf-8")
    assert len(D.AuthorityLedger.import_jsonl(str(p), strict=False)) == 2   # 宽容：能读
    with pytest.raises(D.StrictEventError):
        D.AuthorityLedger.import_jsonl(str(p), strict=True)


# ── A2-9：append_strict 走严格入口且哈希链正常 ─────────────────────────────────
def test_a2_9_append_strict_builds_valid_chain():
    led = D.AuthorityLedger()
    h = led.append_strict(dict(FULL))
    assert len(h) == 64 and led.verify_chain()
    with pytest.raises(D.StrictEventError):
        led.append_strict({"result": "APPROVE"})
    assert len(led) == 1, "非法事件不得入账"
    assert D.selftest() == 0
