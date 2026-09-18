"""583 任务 3（N3）回归锁：`tools/oracle_rotation.py` 换代影响面（只读）。

任务书 §任务 3 的四条验收：
  ① 与 `metrics_collector.oracle_report()` 的 stale 计数**逐条相等**（双实现对账）；
  ② 只读：源码不含判决入口（`gate_engine.run` / `replay.replay_card`）与写操作；
  ③ 两次跑 stdout 一致；④ registry 只读、**不跑**那三份 `--check`。
另加：`--to` 形态校验（坏值 exit 2）与"无法细分 ⇒ 全体强制重验"的诚实文案。
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import metrics_collector as mc  # noqa: E402
import oracle_rotation as orot  # noqa: E402


def test_583_rotation_matches_oracle_report():
    """① 双实现对账：缺字段 / stale 两类计数与参考实现**逐条相等**（不一致即失败）。"""
    rep = orot.build_report(None)
    ref = mc.oracle_report(orot._load_cards())
    assert rep["counts"]["cards_missing_oracle"] == ref["missing_field"], (rep["counts"], ref)
    assert rep["counts"]["cards_mismatch"] == len(ref["stale"]), (rep["counts"], ref)
    # 逐条（不只是计数）：stale 的卡集合一致
    assert {d["card"] for d in rep["mismatch"]} == {e["card"] for e in ref["stale"]}


def test_583_rotation_source_is_read_only_and_runs_nothing():
    """② 只读 + 不跑任何检查：源码无写操作、无 subprocess、无判决入口调用。"""
    raw = pathlib.Path(orot.__file__).read_text(encoding="utf-8")
    body = raw.split('"""', 2)[-1] if raw.startswith(('#!/usr/bin/env python3\n"""', '"""')) else raw
    code = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith("#"))
    for bad in ("write_text(", "open(", "mkdir(", "unlink(", "subprocess", "os.system",
                "gate_engine.run", "replay_card", "import gate_engine"):
        assert bad not in code, f"只读工具里不许出现 {bad!r}"


def test_583_rotation_two_runs_identical(capsys):
    """③ 两次跑 stdout 逐字相同（确定性）。"""
    assert orot.main(["--json"]) == 0
    a = capsys.readouterr().out
    assert orot.main(["--json"]) == 0
    b = capsys.readouterr().out
    assert a == b and a.strip().startswith("{")


def test_583_rotation_does_not_touch_registry_or_run_checks():
    """④ registry 只读（跑前跑后字节相同）；报告只**列**需重跑的清单，不执行。"""
    reg = ROOT / "data" / "oracle_registry.json"
    before = reg.read_bytes()
    assert orot.main(["--check-registry"]) == 0
    assert reg.read_bytes() == before, "registry 必须只读"
    rep = orot.build_report(None)
    assert len(rep["recheck_checklist"]) >= 3
    for item in rep["recheck_checklist"]:
        assert item["command"].startswith("python tools/"), item


def test_583_rotation_conservative_when_cannot_split():
    """⑤ 无法细分（registry 无 judges/invalidates_on_change）⇒ **全体强制重验** + 说人话。"""
    rep = orot.build_report("gcc=16.0.0")
    if not rep["registry_has_split_fields"]:
        assert rep["counts"]["cards_force_revalidate"] == rep["counts"]["cards_total"], rep["counts"]
    else:                                   # 若将来 registry 补了细分字段，本用例退化为"子集"断言
        assert 0 < rep["counts"]["cards_force_revalidate"] <= rep["counts"]["cards_total"]
    assert "缺口未补的代价" in rep["honest_note"]
    assert "fail-closed" in rep["stance"], "立场必须写进报告（本批不实现继承逻辑）"
    # 换代目标版本要如实回显（不编造）
    assert rep["asked_to"].get("gcc") == "16.0.0"


def test_583_rotation_rejects_bad_to():
    """坏 `--to` 形态 ⇒ exit 2（不静默当成默认）。"""
    with pytest.raises(SystemExit) as ei:
        orot.main(["--to", "gcc"])          # 缺 `=版本`
    assert ei.value.code == 2


def test_583_rotation_json_is_stable_payload(capsys):
    """JSON 载荷含四段：计数 / 强制重验清单 / 缺字段清单 / 重跑清单（机器可读）。"""
    assert orot.main(["--json", "--check-registry"]) == 0
    payload = json.loads(capsys.readouterr().out)
    for key in ("counts", "force_revalidate_cards", "missing_oracle_cards", "recheck_checklist"):
        assert key in payload, key
    assert isinstance(payload["force_revalidate_cards"], list)
