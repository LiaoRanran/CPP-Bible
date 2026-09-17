"""412 成本追踪回归锁：record/report/cpva/backfill 与 token 估算口径。"""
from __future__ import annotations

import json
from pathlib import Path

import cost_tracker as ct
import pytest


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ct, "COST_DIR", tmp_path / "cost")
    return tmp_path


def test_token_estimation():
    """chars=3000 → tokens_est=1000（chars/3 口径）。"""
    assert ct.tokens_est(3000) == 1000
    assert ct.tokens_est(3) == 1


def test_record_and_report(sb: Path):
    ct.record("ATOM-T-001", "fixture", 15000, windows=2, duration_min=30)
    ct.record("ATOM-T-001", "redteam", 30000)
    d = ct.report("ATOM-T-001")
    assert d["stages"]["fixture"]["tokens_est"] == 5000
    assert d["total_chars"] == 45000
    assert d["total_tokens_est"] == 15000
    assert d["total_windows"] == 3 and d["total_duration_min"] == 30
    assert d["cpva"] == 15000


def test_record_accumulates_same_stage(sb: Path):
    ct.record("ATOM-T-002", "gate_fix", 3000)
    ct.record("ATOM-T-002", "gate_fix", 6000, windows=2)
    d = ct.report("ATOM-T-002")
    assert d["stages"]["gate_fix"]["chars"] == 9000
    assert d["stages"]["gate_fix"]["windows"] == 3


def test_cpva_calculation(sb: Path):
    for i, (aid, dom, chars) in enumerate(
            [("ATOM-A", "mem", 9000), ("ATOM-B", "mem", 12000), ("ATOM-C", "conc", 6000)]):
        ct.record(aid, "fixture", chars)
        f = ct.COST_DIR / f"{aid}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        d["domain"] = dom
        f.write_text(json.dumps(d), encoding="utf-8")
    c = ct.cpva()
    assert c["total_verified_atoms"] == 3
    assert c["total_tokens_est"] == 9000
    assert c["cpva_overall"] == 3000
    assert c["cpva_by_domain"]["mem"] == 3500 and c["cpva_by_domain"]["conc"] == 2000
    assert c["cpva_by_stage"]["fixture"] == 3000
    assert c["trend"] in ("improving", "stable", "worsening")


def test_backfill_from_git(sb: Path):
    """对真实原子回填（git log 粗估）——数据非空且落盘。"""
    d = ct.backfill("ATOM-MEM-RAII-001")
    assert d["total_tokens_est"] > 0
    assert d["stages"]["fixture"]["windows"] >= 1
    assert (ct.COST_DIR / "ATOM-MEM-RAII-001.json").is_file()


def test_json_report_format(sb: Path):
    r = ct.report()
    assert r["tool"] == "cost_tracker" and "timestamp" in r
    assert "atoms" in r and "total_tokens_est" in r


# ── 530 T6：阶段补全（revision + rounds）+ 占比/端到端成本 + 向后兼容 ─────────


def test_stages_include_revision_and_e2e_chain():
    """T6：stage 枚举含 revision；E2E 链路 = fixture→redteam→revision→human_review。"""
    assert "revision" in ct.STAGES
    assert ct.E2E_STAGES == ("fixture", "redteam", "revision", "human_review")
    # 421 的辅助阶段不得被删（存量 27 条记录与既有测试在用）
    for s in ("evidence_cards", "gate_fix", "human_review", "other"):
        assert s in ct.STAGES


def test_record_rounds_accumulate(sb: Path):
    """T6：轮次 rounds 与 windows 同款累加，并汇总到 total_rounds。"""
    ct.record("ATOM-T-R1", "redteam", 3000, rounds=1)
    ct.record("ATOM-T-R1", "redteam", 6000, rounds=2)
    d = ct.report("ATOM-T-R1")
    assert d["stages"]["redteam"]["rounds"] == 3
    assert d["total_rounds"] == 3
    # 落盘也要有（供下轮复读）
    raw = json.loads((ct.COST_DIR / "ATOM-T-R1.json").read_text(encoding="utf-8"))
    assert raw["total_rounds"] == 3


def test_revision_stage_recordable(sb: Path):
    """T6 新增阶段 revision 可 record（返修轮不是"未知名"）。"""
    ct.record("ATOM-T-R2", "revision", 9000, rounds=1)
    d = ct.report("ATOM-T-R2")
    assert d["stages"]["revision"]["tokens_est"] == 3000
    assert d["stage_share"] == {"revision": 100.0}


def test_report_stage_share_and_e2e_cost(sb: Path):
    """T6：report 给每阶段占比 + 端到端成本（只累 E2E 四阶段，缺则不算齐全）。"""
    ct.record("ATOM-T-R3", "fixture", 3000)          # 1000 tok
    ct.record("ATOM-T-R3", "redteam", 6000)          # 2000 tok
    ct.record("ATOM-T-R3", "revision", 3000)         # 1000 tok
    d = ct.report("ATOM-T-R3")
    assert d["total_tokens_est"] == 4000
    # 每阶段占比（1000/2000/1000 在 4000 里 = 25/50/25）
    assert d["stage_share"] == {"fixture": 25.0, "redteam": 50.0, "revision": 25.0}
    assert abs(sum(d["stage_share"].values()) - 100.0) < 0.05
    # human_review 未记 ⇒ E2E 不齐全，cpva_e2e < total
    assert d["e2e_stages_recorded"] == ["fixture", "redteam", "revision"]
    assert d["e2e_complete"] is False
    assert d["cpva_e2e"] == 4000
    ct.record("ATOM-T-R3", "human_review", 6000)     # 2000 tok
    d2 = ct.report("ATOM-T-R3")
    assert d2["e2e_complete"] is True
    assert d2["cpva_e2e"] == d2["total_tokens_est"] == 6000


def test_legacy_fixture_only_record_reads_back(sb: Path):
    """T6 硬要求：421 老记录（仅 fixture、无 rounds/total_rounds）照读不崩、不丢数。

    同时钉死 report 是**只读计算视图**——读一遍不得改动磁盘文件一个字节。
    """
    sb.joinpath("cost").mkdir(parents=True, exist_ok=True)
    legacy = {
        "atom_id": "ATOM-LEGACY-001", "created_at": "2026-09-13",
        "stages": {"fixture": {"chars": 11560, "windows": 3, "tokens_est": 3853}},
        "domain": "conc",
        "backfill": {"method": "git_log_numstat", "chars": 11560, "commits": 3},
        "total_chars": 11560, "total_tokens_est": 3853, "total_windows": 3,
        "total_duration_min": 0, "cpva": 3853,
    }
    f = ct.COST_DIR / "ATOM-LEGACY-001.json"
    f.write_text(json.dumps(legacy, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    before = f.read_bytes()
    d = ct.report("ATOM-LEGACY-001")
    assert d["total_tokens_est"] == 3853          # 原有数字不丢
    assert d["total_rounds"] == 0                 # 缺键按 0，不臆造
    assert d["stage_share"] == {"fixture": 100.0}
    assert d["e2e_complete"] is False and d["cpva_e2e"] == 3853
    assert f.read_bytes() == before, "report 不得改写成本文件"
    # 更老的形态：连 total_* 都没有（更早期手写记录）
    older = {"atom_id": "ATOM-LEGACY-002",
             "stages": {"fixture": {"chars": 900, "windows": 1}}}
    (ct.COST_DIR / "ATOM-LEGACY-002.json").write_text(
        json.dumps(older, ensure_ascii=False), encoding="utf-8")
    r = ct.report()
    assert r["atoms"] == 2
    # 无 total 键 ⇒ 由 stages 现算；而该阶段连 tokens_est 都没有 ⇒ 计 0（不臆造 chars/3）
    assert r["total_tokens_est"] == 3853
    assert r["cpva_by_atom"]["ATOM-LEGACY-001"] == 3853
    assert r["cpva_by_atom"]["ATOM-LEGACY-002"] == 0
    assert ct.cpva()["total_verified_atoms"] == 2


def test_report_all_atoms_has_per_atom_and_share(sb: Path):
    """T6：全量 report 给"每颗原子端到端成本"与每阶段占比。"""
    ct.record("ATOM-T-A", "fixture", 3000)   # 1000 tok
    ct.record("ATOM-T-B", "fixture", 9000)   # 3000 tok
    r = ct.report()
    assert r["atoms"] == 2
    assert r["cpva_by_atom"] == {"ATOM-T-A": 1000, "ATOM-T-B": 3000}
    assert r["cpva_per_atom"] == 2000
    assert r["stage_tokens_est"] == {"fixture": 4000}
    assert r["stage_share"] == {"fixture": 100.0}


def test_cpva_stage_share_and_rounds(sb: Path):
    """T6：cpva 增补阶段总量/占比与轮次；421 的 `cpva_by_stage`（每颗均值）口径不变。"""
    ct.record("ATOM-T-C1", "fixture", 3000, rounds=1)
    ct.record("ATOM-T-C1", "redteam", 6000, rounds=2)
    ct.record("ATOM-T-C2", "fixture", 9000, rounds=1)
    c = ct.cpva()
    # 421 口径 = 阶段内**每颗原子**均值：C1 fixture 1000、C2 fixture 3000 ⇒ (1000+3000)/2
    assert c["cpva_by_stage"]["fixture"] == 2000
    assert c["cpva_by_stage_total"] == {"fixture": 4000, "redteam": 2000}
    assert c["cpva_by_stage_share"] == {"fixture": 66.7, "redteam": 33.3}
    assert c["total_rounds"] == 4


def test_unknown_stage_rejected(sb: Path):
    """非法阶段仍拒绝（不得静默吞掉拼错的阶段名）。"""
    with pytest.raises(SystemExit):
        ct.record("ATOM-T-X", "redteem", 1000)


def test_cli_json_flag_in_both_positions(sb: Path, capsys: pytest.CaptureFixture):
    """T6：`--json` 前置与后置都要认（cppbible.py:650-654 走的是后置形态）。"""
    ct.record("ATOM-T-D", "revision", 3000, rounds=2)
    assert ct.main(["--json", "report", "--atom", "ATOM-T-D"]) == 0
    front = json.loads(capsys.readouterr().out)
    assert front["total_rounds"] == 2 and front["stage_share"] == {"revision": 100.0}
    assert ct.main(["report", "--atom", "ATOM-T-D", "--json"]) == 0
    back = json.loads(capsys.readouterr().out)
    assert back["total_rounds"] == front["total_rounds"] == 2
    # 不带 --json ⇒ 人读摘要（含占比与端到端），不再是裸 JSON
    assert ct.main(["report", "--atom", "ATOM-T-D"]) == 0
    text = capsys.readouterr().out
    assert "端到端" in text and "占比" in text and "100.0%" in text
    with pytest.raises(json.JSONDecodeError):
        json.loads(text)
