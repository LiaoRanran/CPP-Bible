"""642 A5 · mdl_gate_642 单测（admit/reject 边界 / 豁免率 / 热力图缺失 / 不删规则）。
编号 A5-1..A5-8。
"""
from __future__ import annotations

import json
import os

import mdl_gate_642 as M

_HM = dict(M.shadow.heatmap())
_HM.update(M.SYNTH_HEATMAP)
_EX = M.existing_rule_ids()


# A5-1：已在册规则 ⇒ REFUSE（只对新规则准入，绝不改动现有 67 条）
def test_existing_rule_is_refused():
    d = M.admit_new_rule(_EX[0], "T", hm=_HM, existing=_EX)
    assert d["decision"] == "REFUSE_已有规则"
    assert len(_EX) == 67


# A5-2：热力图缺失 ⇒ 必 reject（实测 4 条不在热力图）
def test_missing_heatmap_is_rejected():
    real = M.shadow.heatmap()
    missing = [r["id"] for r in M.shadow.rules() if r["id"] not in real]
    assert len(missing) == 4
    d = M.admit_new_rule("CAND-NEWDIR-X", "T", hm=_HM, existing=_EX,
                         declared_exempt_rate=0.0)
    assert d["decision"] == "REJECT_热力图缺失"
    # 零触达同样 reject
    zero = [r["id"] for r in M.shadow.rules()
            if M.shadow.samples_explained(r["id"], real) == 0]
    assert len(zero) == 33


# A5-3：编码长度边界（savings ≤ cost ⇒ reject；savings > cost ⇒ 可 admit）
def test_encoding_length_boundary():
    long_title = "长标题" * 400
    rej = M.admit_new_rule("CAND-LONG-001", long_title, hm=_HM, existing=_EX,
                           declared_exempt_rate=0.1)
    assert rej["decision"] == "REJECT_编码长度"
    assert rej["savings_bits"] <= rej["cost_bits"]
    ok = M.admit_new_rule("CAND-SHORT-001", "短", hm=_HM, existing=_EX,
                          declared_exempt_rate=0.1)
    assert ok["decision"] == "ADMIT"
    assert ok["savings_bits"] > ok["cost_bits"]


# A5-4：豁免率计算（未触达轮占比）与阈值边界（>= 阈值即 reject）
def test_exempt_rate_and_threshold():
    er = M.exempt_rate("ATOM-FM-REQUIRED", M.shadow.heatmap())
    assert er is not None and 0.0 <= er <= 1.0
    assert M.exempt_rate("__nope__", M.shadow.heatmap()) is None
    assert M.admit_new_rule("CAND-SHORT-001", "短", hm=_HM, existing=_EX,
                            declared_exempt_rate=M.EXEMPT_RATE_THRESHOLD)["decision"] \
        == "REJECT_豁免率"
    assert M.admit_new_rule("CAND-SHORT-001", "短", hm=_HM, existing=_EX,
                            declared_exempt_rate=0.2999)["decision"] == "ADMIT"


# A5-5：无豁免率数据 ⇒ PENDING_HUMAN（不代决，也不静默 reject）
def test_pending_human_when_no_exempt_data():
    d = M.admit_new_rule("CAND-NODATA-001", "T", hm=_HM, existing=_EX,
                         declared_exempt_rate=None)
    assert d["decision"] == "PENDING_HUMAN"


# A5-6：636 的「通过率」与 642 的「豁免率」是两个量，不可混用
def test_admit_rate_and_exempt_rate_are_distinct():
    s = M.trial_stats()
    assert (s["admitted"], s["rejected"]) == (30, 37)
    assert (s["early_rate_pct"], s["recent_rate_pct"]) == (66.7, 23.5)
    # 636 的 66.7/23.5 是**通过率**（admit_rate），不是豁免率
    assert M.EXEMPT_RATE_REFERENCE == 0.235
    assert s["exempt_mean"] is not None
    assert 0.0 <= s["exempt_mean"] <= 1.0
    assert s["exempt_known"] == s["heatmap_rules"]


# A5-7：侧车元数据只记新规则，被拒规则保留（不删除）
def test_metric_sidecar_keeps_rejected_rules(tmp_path, monkeypatch):
    rows = M.run_admission()["rows"]
    out = tmp_path / "adm.json"
    monkeypatch.setattr(M, "OUT_JSON", str(out))
    M.write_meta(rows)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["existing_rules_untouched"] is True
    decisions = [d["decision"] for d in payload["decisions"]]
    assert "REJECT_编码长度" in decisions, "被拒规则必须保留在侧车里（不删除）"
    assert all(d["rule_id"] not in _EX for d in payload["decisions"]
               if d["decision"] != "REFUSE_已有规则")
    assert os.path.basename(M.OUT_MD) == "642_mdl_admission.md"


# A5-8：六种结论全覆盖 + --check 自检
def test_all_decisions_reachable_and_selftest():
    assert set(M.run_admission()["by_decision"]) == set(M.DECISIONS)
    assert M.selftest() == 0
