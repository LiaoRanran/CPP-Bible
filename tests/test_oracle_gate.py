"""574 任务 D 回归锁：信任放权门 —— **只写不读**、默认不放权。

最关键的锁：给卡/命题填上 `verified_by_oracle`（哪怕填成"最强 oracle 已验证"），
**gate 的 block/warn 集合与 replay 的 verdict 必须逐字不变** —— 一旦变了就是偷偷放权。
放权开关（G-iso / oracle_auto_accept / llm_as_judge）必须全 OFF。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay   # noqa: E402
import gate_engine as ge                # noqa: E402
import metrics_collector as mc          # noqa: E402
import mutation_fuzz as mf              # noqa: E402

ORACLE_BLOCK = ("verified_by_oracle:\n"
                "  oracle: gcc\n"
                "  version: 99.0.0        # 故意写一个谁都还没认可的新版本\n"
                "  verified_at: 2026-09-17\n"
                "  scope: all\n")


def _key(fs) -> list:
    """只比 (规则 id, 严重度, 卡基名)——沙箱路径不同，故取基名。"""
    return sorted({(f.rule_id, f.severity, str(f.target).replace("\\", "/").split("/")[-1])
                   for f in fs})


def test_574_oracle_field_does_not_change_gate_verdicts():
    base = _key(ge.run(include_advice=False))
    with mf.sandbox() as tmp:
        card = next(iter(sorted((tmp / "atoms").rglob("ATOM-*.md"))), None)
        assert card is not None, "沙箱里应有原子卡"
        raw = card.read_text(encoding="utf-8")
        card.write_text(raw.replace("---\n", "---\n" + ORACLE_BLOCK, 1), encoding="utf-8")
        after = _key(ge.run(include_advice=False))
    assert after == base, "填了 verified_by_oracle 后门禁判决必须逐字不变（只写不读是硬不变量）"


def test_574_oracle_field_does_not_change_replay_verdict():
    p = ROOT / "evidence" / "conc" / "EV-CONC-001.md"
    v0, _ = replay.replay_card(p, do_sanitizer=False)
    assert v0 == "confirm", v0
    with mf.sandbox() as tmp:
        sp = tmp / "evidence" / "conc" / "EV-CONC-001.md"
        raw = p.read_text(encoding="utf-8")
        sp.write_text(raw.replace("---\n", "---\n" + ORACLE_BLOCK, 1), encoding="utf-8")
        v1, _ = replay.replay_card(sp, do_sanitizer=False)
    assert v1 == v0, "填了 verified_by_oracle 后复算判决必须不变"


def test_574_stale_is_report_layer_only():
    """报告层：版本对不上 ⇒ stale；对得上 ⇒ 不 stale；没填 ⇒ 记 missing_field。"""
    rep = mc.oracle_report([
        {"id": "C1", "verified_by_oracle": {"oracle": "gcc", "version": "15.3.0"}},
        {"id": "C2", "verified_by_oracle": {"oracle": "gcc", "version": "14.0.0"}},
        {"id": "C3", "verified_by_oracle": {"oracle": "not-in-registry", "version": "1"}},
        {"id": "C4"},
    ])
    stale = {e["card"] for e in rep["stale"]}
    assert stale == {"C2", "C3"}, rep
    assert rep["missing_field"] == 1
    assert "gcc" in rep["current_oracles"]


def test_574_delegation_switches_are_all_off():
    """放权开关一律 OFF（本任务不实现任何机器自动接受）。"""
    assert mc.DELEGATION_SWITCHES and all(not v for v in mc.DELEGATION_SWITCHES.values()), \
        mc.DELEGATION_SWITCHES
    # registry 里的开关也必须是关的（防有人只改一处）
    import json
    reg = json.loads(mc.ORACLE_REGISTRY.read_text(encoding="utf-8"))
    sw = (reg.get("delegation") or {}).get("switches") or {}
    assert sw and all(not v for v in sw.values()), sw
