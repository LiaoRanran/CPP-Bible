"""609 A3 · W2 重算集成回归锁（--include-human-reviewed + 判决翻转列表）。

**向后兼容是硬要求**：不加人审标注时，结果与 596/594 实证**逐字段一致**
（节点 121 · IN 79 / OUT 42 / UNDEC 0 · 击败边 194/388 · 3 轮收敛）。

权重规则（只改**权重输入**，W2 击败规则 `cred(A) > cred(B)` 一行未动）：
    approve ⇒ 可信度升一级（当前全盘 low ⇒ low→medium）
    reject  ⇒ 从攻击图移除
    modify  ⇒ **按 `--modify-mode` 决定**（611 B1 起默认 `keep-low` = 不生效；`upgrade-medium` 才落档）
    未审    ⇒ 原样保留

> ⚠️ 611 B1 改了 modify 的**默认**口径（`upgrade-medium` → `keep-low`，对齐入库权威产物）。
> 因此需要"modify 落档"语义的用例必须**显式**传 `modify_mode="upgrade-medium"`
> —— 见 `test_modify_sets_exact_confidence_and_kind_normalization`。

实测翻转（**真实跑出来的数，不是估计**）：
  * 单条 approve（`ae-ATOM-CONC-RACE-001::prop-1->MIS-CONC-003`）⇒ 该边 low→medium
    ⇒ 误解 `MIS-CONC-003` 的可信度被抬到与命题同档 ⇒ 不再被击败 ⇒ **OUT→IN**（1 处翻转）；
  * 单条 reject ⇒ 387 条边、**0 处翻转**（该误解仍有其他攻击者，不足以改变标签）；
  * 拒掉 `MIS-CONC-003` 的全部 3 条攻击边 ⇒ 它失去**全部**攻击者 ⇒ **OUT→IN**（触发边 3 条）。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_cli as hrc
import weighted_af_solver as w2

EDGES = w2.load_edges()
FIRST = EDGES[0]
FIRST_ID = str(FIRST["id"])
TARGET_MIS = str(FIRST["target"])          # 实测 = MIS-CONC-003
REASON = "人审确认：该攻击关系成立且反驳证据可核（609 A3 自测用理由，长度达标）"
BASE = {"IN": 79, "OUT": 42, "UNDEC": 0, "nodes": 121}


def _ann(p: Path, rows: list[dict]) -> Path:
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                 encoding="utf-8", newline="\n")
    return p


def _rec(edge_id: str, kind: str, **extra) -> dict:
    return {"edge_id": edge_id, "kind": kind, "reviewer": "human",
            "timestamp": "2026-09-19T10:00:00+08:00", "reason": REASON, **extra}


# ── 1. 向后兼容 ───────────────────────────────────────────────────────────────
def test_no_human_review_equals_596_baseline():
    doc = w2.solve(EDGES)                       # 不加人审 ⇒ 596 口径
    assert doc["summary"]["IN"] == BASE["IN"]
    assert doc["summary"]["OUT"] == BASE["OUT"]
    assert doc["summary"]["UNDEC"] == BASE["UNDEC"]
    assert doc["summary"]["nodes"] == BASE["nodes"]
    assert doc["defeating_edges"] == 194 and doc["edges"] == 388
    assert doc["rounds"] == 3
    assert w2.check(doc) == [], "596/594 口径被改坏了（这是硬回归）"


def test_cli_no_human_reviewed_matches_baseline(tmp_path: Path, capsys):
    out = tmp_path / "w2.json"
    ann = _ann(tmp_path / "ann.jsonl", [])
    # ⚠️ argparse 坑：子命令自己的 --out/--annotations 默认值会覆盖父 parser 的值
    # ⇒ 这些参数必须写在**子命令之后**（写前面会被默认值吃掉 ⇒ 打真实 DEFAULT_OUT）。
    assert w2.main(["solve", "--no-human-reviewed", "--annotations", str(ann),
                    "--out", str(out)]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["summary"]["IN"] == 79
    assert "IN 79 / OUT 42 / UNDEC 0（3 轮 · 击败边 194/388）" in capsys.readouterr().out


# ── 2. approve 权重升级 + 后果 ────────────────────────────────────────────────
def test_single_approve_promotes_weight_and_flips_verdict():
    anns = [_rec(FIRST_ID, "approve")]
    eff, changes = w2.reviewed_edges(EDGES, anns)
    ch = changes[FIRST_ID]
    assert (ch["action"], ch["old_confidence"], ch["new_confidence"]) == ("promote", "low", "medium")
    if_changed = {str(e["id"]): e for e in eff}[FIRST_ID]
    assert if_changed["confidence"] == "medium" and if_changed["human_reviewed"] == "approve"
    assert len(eff) == 388, "approve 不得删边"
    doc = w2.solve(eff)
    d = w2.diff_verdicts(w2.solve(EDGES), doc, edges=EDGES, changes=changes)
    # 640 A1 更新：签署后命题可信度 high（human: 签），单条 approve 把误解边抬到
    # medium 也无法再击败 high 命题 ⇒ 609 时代的 OUT→IN 翻转不再发生（翻转=0）。
    # approve 的**机制**（promote low→medium、留痕、不删边）仍由上方断言锁住；
    # 翻转归因路径由 reject 系列（移除全部攻击者 ⇒ OUT→IN）继续覆盖。
    assert d["flipped"] == 0
    assert d["flips"] == []


# ── 3. reject 移除边 ──────────────────────────────────────────────────────────
def test_single_reject_drops_edge_without_flip():
    anns = [_rec(FIRST_ID, "reject")]
    eff, changes = w2.reviewed_edges(EDGES, anns)
    assert len(eff) == 387 and changes[FIRST_ID]["action"] == "drop"
    doc = w2.solve(eff)
    d = w2.diff_verdicts(w2.solve(EDGES), doc, edges=EDGES, changes=changes)
    assert d["flipped"] == 0, "单条 reject 实测不改变任何标签（该误解仍有其他攻击者）"


def test_rejecting_all_attackers_flips_misconception():
    attackers = [str(e["id"]) for e in EDGES
                 if e["direction"] == "prop_to_mis" and str(e["target"]) == TARGET_MIS]
    assert len(attackers) == 3, f"实测 {TARGET_MIS} 的攻击者数变了：{len(attackers)}"
    anns = [_rec(i, "reject") for i in attackers]
    eff, changes = w2.reviewed_edges(EDGES, anns)
    doc = w2.solve(eff)
    d = w2.diff_verdicts(w2.solve(EDGES), doc, edges=EDGES, changes=changes)
    assert d["flipped"] == 1 and d["flips"][0]["node_id"] == TARGET_MIS
    assert d["flips"][0]["trigger_edge_count"] == 3
    assert d["flips"][0]["trigger_kinds"] == {"reject": 3}


# ── 4. diff 子命令（CLI 层）────────────────────────────────────────────────────
def test_cli_diff_lists_flips_with_reasons(tmp_path: Path, capsys):
    baseline = tmp_path / "base.json"
    ann = _ann(tmp_path / "ann.jsonl", [_rec(FIRST_ID, "reject")])
    assert w2.main(["solve", "--no-human-reviewed", "--annotations", str(ann),
                    "--out", str(baseline)]) == 0
    attackers = [str(e["id"]) for e in EDGES
                 if e["direction"] == "prop_to_mis" and str(e["target"]) == TARGET_MIS]
    capsys.readouterr()                      # 清掉 solve 的输出，保证 stdout 是纯 JSON
    assert w2.main(["diff", "--annotations", str(ann), "--baseline", str(baseline),
                    "--json"]) == 0
    d = json.loads(capsys.readouterr().out)
    assert d["flipped"] == 0 and d["base_edges"] == 388 and d["new_edges"] == 387

    _ann(ann, [_rec(i, "reject") for i in attackers])
    capsys.readouterr()
    assert w2.main(["diff", "--annotations", str(ann), "--baseline", str(baseline)]) == 0
    out = capsys.readouterr().out
    assert "翻转 1 个节点" in out and TARGET_MIS in out
    assert "OUT → IN" in out and "触发人审边 3 条" in out


# ── 5. stats --include-human-reviewed ─────────────────────────────────────────
def test_cli_stats_reports_progress_and_influence(tmp_path: Path, capsys):
    attackers = [str(e["id"]) for e in EDGES
                 if e["direction"] == "prop_to_mis" and str(e["target"]) == TARGET_MIS]
    ann = _ann(tmp_path / "ann.jsonl", [_rec(i, "reject") for i in attackers])
    assert w2.main(["stats", "--annotations", str(ann), "--json"]) == 0
    st = json.loads(capsys.readouterr().out)
    assert st["review_progress"] == {"total": 388, "reviewed": 3, "pending": 385,
                                     "annotations": 3, "reviewed_rate": 0.0077}
    assert st["review_changes"] == 3 and st["flipped_nodes"] == 1
    assert st["flips"][0]["node_id"] == TARGET_MIS

    capsys.readouterr()
    assert w2.main(["stats", "--annotations", str(ann)]) == 0
    txt = capsys.readouterr().out
    assert "人审进度 3/388" in txt and "判决影响：1 个节点翻转" in txt


def test_modify_sets_exact_confidence_and_kind_normalization(tmp_path: Path):
    """modify 落档（**显式 upgrade-medium**）；且 596 的 `action` 字段必须被归一化识别。

    611 B1 起 modify 的**默认**是 `keep-low`（不落档）⇒ 本用例显式要 `upgrade-medium`
    才测得到"直接落档"这条语义（默认档由 611 的新用例覆盖）。
    """
    old = [_rec(FIRST_ID, "modify", confidence="high")]
    eff, changes = w2.reviewed_edges(EDGES, old, modify_mode="upgrade-medium")
    assert changes[FIRST_ID]["new_confidence"] == "high"

    legacy = [{"edge_id": FIRST_ID, "action": "modify", "new_confidence": "medium",
               "reviewer": "human", "timestamp": "2026-09-19T10:00:00+08:00", "reason": REASON}]
    ann = _ann(tmp_path / "legacy.jsonl", legacy)
    eff2, ch2 = w2.reviewed_edges(EDGES, hrc.load_annotations(ann),
                                  modify_mode="upgrade-medium")
    assert ch2[FIRST_ID]["new_confidence"] == "medium", "596 action 字段应被归一化识别"
    assert len(eff2) == 388
