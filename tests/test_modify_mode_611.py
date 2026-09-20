"""611 B1 · modify 口径**双模式**（610 交人项 ①：口径冲突只做工具支持，不擅自统一）。

背景（610 实测，非估计）：388 条人审里 34 条 `modify` 的 `new_confidence` **全是 medium**。
  * `keep-low`（**611 起默认**）：modify 不改变生效权重 —— 入库产物 `data/grounded_labels_w2.json`
    就是这个口径 ⇒ **IN114 / OUT7 / 击败边 17**；
  * `upgrade-medium`（609 A3 原语义）：modify 采纳 `confidence`/`new_confidence` ⇒
    **IN121 / OUT0 / 击败边 0**（42 个 MIS 与命题同档 ⇒ 一条击败边都不剩）。

锁六件事：
  1. **默认 = keep-low**，且默认现算值 == 入库权威产物（IN/OUT/UNDEC/击败边**逐项**相等）；
  2. `upgrade-medium` == 609 A3 的口径（121/0/0）⇒ 旧语义没被删掉，只是不再默认；
  3. `--modify-mode` CLI 两档都能跑，且 stderr 标明"多少条 modify 未生效"；
  4. **归因不误算**：keep-low 下被忽略的 modify（`effective=False`）**不得**出现在
     `diff.flips[*].trigger_edge_ids` 里（它什么都没改）；
  5. 指标 `metrics_610.collect_modify_mode()` / `two_mode_verdicts()` 把分歧**量化**记账；
  6. 非法 mode ⇒ 立刻 `ValueError`（fail-closed，不静默退回默认档）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import human_review_cli as hrc  # noqa: E402
import metrics_610 as m610  # noqa: E402
import weighted_af_solver as w2  # noqa: E402

REASON = "611 B1 测试：口径双模式锁（modify 档位口径由 --modify-mode 决定）"


def _ann(tmp: Path, rows: list[dict]) -> Path:
    p = tmp / "ann.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return p


def test_default_mode_is_keep_low_and_matches_authoritative():
    assert w2.DEFAULT_MODIFY_MODE == "keep-low"
    assert w2.MODIFY_MODES == ("keep-low", "upgrade-medium")
    edges = w2.load_edges()
    anns = hrc.load_annotations()
    eff, changes = w2.reviewed_edges(edges, anns)                    # 不传 ⇒ 默认档
    doc = w2.solve(eff)
    art = json.loads((ROOT / "data" / "grounded_labels_w2.json").read_text(encoding="utf-8"))
    assert (doc["summary"]["IN"], doc["summary"]["OUT"], doc["summary"]["UNDEC"]) == (114, 7, 0)
    assert doc["defeating_edges"] == 17 and doc["edges"] == 388 and doc["rounds"] == 3
    assert doc["summary"]["IN"] == art["summary"]["IN"]
    assert doc["summary"]["OUT"] == art["summary"]["OUT"]
    assert doc["defeating_edges"] == art["defeating_edges"]
    # keep-low 下 modify 全部"未生效"，但**留痕**（人审过 / 理由在 / 记了被哪档忽略）
    mods = [k for k, v in changes.items() if v["kind"] == "modify"]
    assert len(mods) == 34, mods[:3]
    assert all(changes[k]["effective"] is False for k in mods)
    assert all(changes[k]["action"] == "keep" for k in mods)
    assert all("keep-low" in changes[k]["why"] for k in mods)
    assert all(changes[k]["declared_confidence"] == "medium" for k in mods)
    ignored = [e for e in eff if e.get("modify_ignored_by") == "keep-low"]
    assert len(ignored) == 34
    assert all(str(e["confidence"]) == "low" for e in ignored), "keep-low 不许改权重"


def test_upgrade_mode_reproduces_609_caliber():
    edges = w2.load_edges()
    anns = hrc.load_annotations()
    eff, changes = w2.reviewed_edges(edges, anns, modify_mode="upgrade-medium")
    doc = w2.solve(eff)
    assert (doc["summary"]["IN"], doc["summary"]["OUT"], doc["summary"]["UNDEC"]) == (121, 0, 0)
    assert doc["defeating_edges"] == 0 and doc["rounds"] == 2
    mods = [k for k, v in changes.items() if v["kind"] == "modify"]
    assert all(changes[k]["effective"] is True for k in mods)
    assert all(changes[k]["new_confidence"] == "medium" for k in mods)


def test_invalid_mode_fails_closed():
    """非法档位 ⇒ 立刻 ValueError（**不静默退回默认档** —— 静默退回等于偷换口径）。"""
    for bad in ("keep_low", "UPGRADE-MEDIUM", "", "keep-low "):
        with pytest.raises(ValueError):
            w2.reviewed_edges(w2.load_edges(), hrc.load_annotations(), modify_mode=bad)


def test_cli_both_modes_and_reports_noop_count(capsys):
    assert w2.main(["stats", "--no-human-reviewed", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["by_label"]["IN"] == 79
    # 默认档（keep-low）：stderr 必须写明"34 条 modify 未生效"
    assert w2.main(["stats", "--json"]) == 0
    err = capsys.readouterr().err
    assert "modify 口径 keep-low" in err and "34 条 modify 未生效" in err
    # 显式 upgrade-medium
    assert w2.main(["stats", "--modify-mode", "upgrade-medium", "--json"]) == 0
    out = capsys.readouterr()
    assert "modify 口径 upgrade-medium" in out.err and "0 条 modify 未生效" in out.err
    assert json.loads(out.out)["by_label"]["IN"] == 121


def test_diff_does_not_blame_ignored_modify(tmp_path: Path, capsys):
    """keep-low 下被忽略的 modify 不该被算成"触发翻转的人审"（它没改任何权重）。"""
    edges = w2.load_edges()
    anns = hrc.load_annotations()
    baseline = w2.solve(edges)                                   # 无人审基线
    eff, changes = w2.reviewed_edges(edges, anns)                # 默认 keep-low
    doc = w2.solve(eff)
    d = w2.diff_verdicts(baseline, doc, edges=edges, changes=changes)
    # 无人审图 = IN79（79 命题 + **0** 误解）/OUT42；keep-low = IN114（79 命题 + **35** 误解）/OUT7
    # ⇒ 翻转 = 42 - 7 = **35** 个误解（剩下的 7 个仍 OUT）
    assert d["flipped"] == 35, f"keep-low 相对无审核应翻 35 个误解 ⇒ 实得 {d['flipped']}"
    ignored = {k for k, v in changes.items() if not v.get("effective", True)}
    for f in d["flips"]:
        assert not (set(f.get("trigger_edge_ids") or []) & ignored), (
            f"翻转归因把未生效的 modify 算成了触发者：{f['node_id']}")
    # 纯 modify 的图（无 approve）：keep-low 下判决应与"完全无人审"一致
    only_mod = [a for a in anns if hrc.kind_of(a) == "modify"]
    eff2, ch2 = w2.reviewed_edges(edges, only_mod)
    assert w2.solve(eff2)["summary"] == baseline["summary"], "keep-low 下 modify 不该动判决"
    assert all(not v.get("effective", True) for v in ch2.values())
    assert w2.solve(eff2)["defeating_edges"] == baseline["defeating_edges"]


def test_metrics_record_two_mode_divergence():
    out = m610.collect_modify_mode({})
    assert out["current_mode"] == "keep-low"
    assert set(out["modes"]) == {"keep-low", "upgrade-medium"}
    lo, up = out["modes"]["keep-low"], out["modes"]["upgrade-medium"]
    assert (lo["in"], lo["out"], lo["defeating_edges"]) == (114, 7, 17)
    assert (up["in"], up["out"], up["defeating_edges"]) == (121, 0, 0)
    assert out["divergence"] is True
    assert out["divergence_detail"] == {"in": 7, "out": -7, "defeating_edges": -17}
    assert "两档口径判决不同" in out["note"] and "必须标明" in out["note"]
    # grounded_status 采集器：默认档与权威产物一致 + 分歧仍显形（不掩盖）
    g = m610.collect_grounded_status({})
    assert g["default_modify_mode"] == "keep-low"
    assert g["default_matches_artifact"] is True
    assert g["divergence"] is True
    assert "需监工裁决" in g["divergence_note"] and "modify 保持 low" in g["divergence_note"]
    assert g["solver_recompute"]["in"] == 121          # 610 字段语义未变（= 609 A3 口径）
    assert g["solver_recompute_default"]["in"] == 114  # 新字段 = 默认档现算
