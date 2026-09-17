"""573 任务 A 回归锁：三曲线升 v2 + overturned 事件通道（fail-closed）+ survival 只数 M3。

硬不变量：**系统绝不自动产生推翻** —— 事件只能来自人/异族的显式动作，且 `human:<名>`
必须与被推翻对象所在卡的最后一次 git 提交作者一致，否则**拒绝写入**（不是"记下来再说"）。
"""
from __future__ import annotations

import json

import gate_engine as ge
import metrics_collector as mc
import pytest

CARD = "ATOM-LANG-INLINE-001"      # 573：必须用**真实存在**的卡（核验要解析到文件）


@pytest.fixture(autouse=True)
def _git_author(monkeypatch):
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("LiaoRanran", "liao@example.com"))


def test_574_escape_rate_uses_v3(tmp_path, monkeypatch):
    """逃逸率必须读 **v3**（574 修 M5 尺子 + 572 收 M3 后），且 C-P 用 stat_bounds 重算一致。"""
    from stat_bounds import proportion
    c = mc.collect_curves()
    r = c["mutation_escape_rate"]
    assert r["source"].endswith("full_baseline_v3.json"), r
    d = json.load(open(r["source"], encoding="utf-8"))
    judged = d["blocked"] + d["escaped"]
    exp = proportion(d["escaped"], judged)
    assert (r["numerator"], r["denominator"]) == (exp["numerator"], exp["denominator"])
    assert r["point"] == round(exp["point"], 6)
    assert (r["cp_low"], r["cp_high"]) == (round(exp["cp_low"], 6), round(exp["cp_high"], 6))
    # v1 只能作**历史时点**，不许被当成当前口径
    hist = c["mutation_escape_rate_history"]
    assert hist and hist[0]["source"].endswith("full_baseline_v1.json")


def test_573_overturned_human_signed_is_logged(tmp_path):
    ev = mc.log_overturned("ATOM-MEM-MOVE-001/prop-1", "confirm", "refute:new_evidence",
                           "human:LiaoRanran", "更强的证据推翻", card=CARD,
                           path=tmp_path / "ev.jsonl")
    assert ev["by"] == "human:LiaoRanran" and ev["card"] == CARD
    assert ev["old_verdict"] == "confirm" and ev["new_verdict"] == "refute:new_evidence"
    assert mc.read_overturned_events(tmp_path / "ev.jsonl") == [ev]


def test_573_overturned_impersonation_refused(tmp_path):
    """冒名（不是该卡 git 作者）⇒ **拒绝写入**（fail-closed），且不落任何行。"""
    with pytest.raises(ValueError, match="不是该卡最后一次 git 提交的作者"):
        mc.log_overturned("ATOM-MEM-MOVE-001/prop-1", "confirm", "refute:x",
                          "human:Attacker", "理由", card=CARD, path=tmp_path / "ev.jsonl")
    assert not (tmp_path / "ev.jsonl").exists()


def test_573_overturned_unsigned_or_incomplete_refused(tmp_path, monkeypatch):
    """git 不可用 ⇒ 无法核验 ⇒ 拒绝；缺字段 / by 形态不对 ⇒ 拒绝。"""
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: None)
    with pytest.raises(ValueError, match="git 不可用"):
        mc.log_overturned("t", "confirm", "refute:x", "human:LiaoRanran", "r",
                          card=CARD, path=tmp_path / "ev.jsonl")
    with pytest.raises(ValueError, match="均不可为空"):
        mc.log_overturned("", "confirm", "refute:x", "adversary:redteam-v1", "r",
                          card=CARD, path=tmp_path / "ev.jsonl")
    with pytest.raises(ValueError, match="human:|adversary:"):
        mc.log_overturned("t", "confirm", "refute:x", "bot:someone", "r",
                          card=CARD, path=tmp_path / "ev.jsonl")
    with pytest.raises(ValueError, match="卡解析不到"):
        mc.log_overturned("t", "confirm", "refute:x", "adversary:redteam-v1", "r",
                          card="ATOM-NOT-EXIST", path=tmp_path / "ev.jsonl")


def test_573_overturned_adversary_is_logged_without_signature(tmp_path):
    """异族没有 git 身份 ⇒ 只登记、不核签（这是明确的例外，不是漏检）。"""
    ev = mc.log_overturned("ATOM-MEM-MOVE-001/prop-1", "confirm", "refute:x",
                           "adversary:redteam-v1", "异族实测", card=CARD,
                           path=tmp_path / "ev.jsonl")
    assert ev["by"] == "adversary:redteam-v1"
    assert mc.read_overturned_events(tmp_path / "ev.jsonl") == [ev]


def test_573_curves_count_events(tmp_path, monkeypatch):
    """collect_curves 的 overturned 计数**来自事件流**（不是写死的 0）。"""
    p = tmp_path / "ev.jsonl"
    mc.log_overturned("a/prop-1", "confirm", "refute:x", "adversary:redteam-v1", "r",
                      card=CARD, path=p)
    monkeypatch.setattr(mc, "OVERTURNED_FILE", p)
    c = mc.collect_curves()
    assert c["overturned_by_stronger_verifier"] == 1
    assert c["overturned_recent"][-1]["target"] == "a/prop-1"


def test_573_survival_only_counts_m3():
    """survival 只数 M3 那 52 条（571→572）；M2 是尺子 bug 的假逃逸 ⇒ null，其余 null。"""
    s = mc.collect_curves()["escape_survival_batches"]
    assert s["M3"]["batches"] == 1 and s["M3"]["escapes"] == 52
    assert s["M3"]["produced_in"] == "571" and s["M3"]["closed_in"] == "572"
    assert s["M2"] is None and s["others"] is None
