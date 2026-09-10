"""门禁引擎 M4 的毒样例回归：每条规则**正例触发 + 反例不触发**（元门禁：误报/漏报回归）。

覆盖：
  * 事实规则：必填字段 / verified 绑定 / DAG 环 / ID 格式 / 证伪对照 / 灰色地带标注
  * 误报回归锁：「待补」是合法缺口留痕，不得被判占位符
  * severity 语义：advice 规则永不阻断（只建议不改文）
  * 规则自身约束：ID 唯一、教学/文学规则必须标学习科学依据
  * 真实仓库：双清单零漂移（ADR-0004 收敛后应恒为 0）
"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge


def _kv(k: str, v: object) -> str:
    """值以换行开头 → YAML 嵌套块；否则内联标量。"""
    return f"{k}:{v}\n" if str(v).startswith("\n") else f"{k}: {v}\n"


def _write_atom(base: Path, name: str, domain_dir: str, **over: str) -> Path:
    d = base / "atoms" / domain_dir
    d.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": "ATOM-MEM-MOVE-001", "title": "t", "domain": "MEM", "type": "mechanism",
        "status": "draft", "claim": "c", "claim_boundary": "b", "relations": "[]",
        "evidence": "[]", "sources": "[{kind: iso, ref: X, independent: true}]",
        "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
    }
    fields.update(over)
    path = d / name
    path.write_text("---\n" + "".join(_kv(k, v) for k, v in fields.items()) + "---\n",
                    encoding="utf-8")
    return path


@pytest.fixture()
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    return tmp_path


# ── 必填字段：正例触发 / 反例不触发 ────────────────────────────────────────
def test_atom_missing_field_triggers(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", title="")          # title 空
    hits = ge.check_atom_frontmatter()
    assert len(hits) == 1 and hits[0].rule_id == "ATOM-FM-REQUIRED"
    assert "title" in hits[0].message


def test_atom_complete_does_not_trigger(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem")
    assert ge.check_atom_frontmatter() == []


def test_atom_empty_sources_still_triggers(sandbox: Path):
    """多源精炼要求 ≥1 个来源——空 sources 必须拦（区别于空 relations 的合法）。"""
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", sources="[]")
    hits = ge.check_atom_frontmatter()
    assert any("sources" in h.message for h in hits)


# ── verified 声明-证据绑定 ────────────────────────────────────────────────
def test_verified_without_evidence_blocks(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="verified",
                evidence="[]", first_hand="false", superiority="")
    hits = ge.check_verified_bound()
    assert len(hits) == 1
    assert "evidence[] 为空" in hits[0].message
    assert "first_hand 非 true" in hits[0].message


def test_verified_with_evidence_passes(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="verified",
                evidence="[EV-MEM-001]", first_hand="true", superiority="多给了汇编证据")
    assert ge.check_verified_bound() == []


# ── DAG 无环 ──────────────────────────────────────────────────────────────
def test_dag_cycle_blocks(sandbox: Path):
    rel_a = "[{type: prerequisite, target: ATOM-MEM-MOVE-002}]"
    rel_b = "[{type: prerequisite, target: ATOM-MEM-MOVE-001}]"
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", relations=rel_a)
    _write_atom(sandbox, "ATOM-MEM-MOVE-002.md", "mem", id="ATOM-MEM-MOVE-002",
                relations=rel_b)
    hits = ge.check_relations_dag()
    assert len(hits) == 1 and hits[0].rule_id == "ATOM-REL-DAG"
    assert "环" in hits[0].message


def test_dag_acyclic_passes(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                relations="[{type: prerequisite, target: ATOM-MEM-MOVE-002}]")
    _write_atom(sandbox, "ATOM-MEM-MOVE-002.md", "mem", id="ATOM-MEM-MOVE-002")
    assert ge.check_relations_dag() == []


# ── ID 格式与目录一致 ─────────────────────────────────────────────────────
def test_bad_id_and_wrong_dir_block(sandbox: Path):
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "stl")                    # 目录与域不符
    hits = ge.check_atom_id_format()
    assert any("不一致" in h.message for h in hits)
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", id="ATOM-FOO-BAR-001")
    assert any("不在 16 域内" in h.message for h in ge.check_atom_id_format())


# ── 证据卡：证伪对照 / 灰色地带 ────────────────────────────────────────────
def _write_ev(base: Path, **over: str) -> Path:
    d = base / "evidence" / "mem"
    d.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": "EV-MEM-001", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
        "command": "echo hi", "fixture": "Examples/x.cpp", "artifact": "a.asm",
        "artifact_sha256": "0" * 64, "actual": "{run_case: A}", "kind": "run",
        "falsification": "对照 B 输出 1",
    }
    fields.update(over)
    p = d / "EV-MEM-001.md"
    p.write_text("---\n" + "".join(_kv(k, v) for k, v in fields.items()) + "---\n",
                 encoding="utf-8")
    return p


def test_missing_falsification_blocks(sandbox: Path):
    _write_ev(sandbox, falsification="")
    hits = ge.check_evidence_falsification()
    assert len(hits) == 1 and "证伪" in hits[0].message


def test_falsification_present_passes(sandbox: Path):
    _write_ev(sandbox)
    assert ge.check_evidence_falsification() == []


def test_matrix_missing_keys_blocks(sandbox: Path):
    _write_ev(sandbox, matrix="\n  compiler: [GCC 15.3.0]")     # 缺 std/opt
    hits = ge.check_evidence_matrix()
    assert len(hits) == 1 and "std" in hits[0].message and "opt" in hits[0].message
    _write_ev(sandbox, matrix="\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]")
    assert ge.check_evidence_matrix() == []


def test_ub_atom_requires_gray_zone(sandbox: Path):
    _write_atom(sandbox, "ATOM-UB-ALIAS-001.md", "ub", id="ATOM-UB-ALIAS-001",
                domain="UB", type="pitfall")
    assert any("gray_zone" in h.message for h in ge.check_atom_gray_zone())
    _write_atom(sandbox, "ATOM-UB-ALIAS-001.md", "ub", id="ATOM-UB-ALIAS-001",
                domain="UB", type="pitfall", gray_zone="ub")
    assert ge.check_atom_gray_zone() == []


# ── 误报回归锁：「待补」是合法留痕 ─────────────────────────────────────────
def test_daibu_is_not_placeholder(sandbox: Path):
    p = sandbox / "evidence" / "mem" / "EV-MEM-001.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("---\nid: EV-MEM-001\n---\n\n## 待补\n- Clang 列需 CI 补齐\n",
                 encoding="utf-8")
    assert ge.check_zero_placeholder() == []
    p.write_text("---\nid: EV-MEM-001\n---\nTODO: 补命令\n", encoding="utf-8")
    assert len(ge.check_zero_placeholder()) == 1


# ── severity 语义：advice 永不阻断 ────────────────────────────────────────
def test_advice_rules_never_block(sandbox: Path):
    """教学/文学规则命中时 severity=advice，不得影响 --check 的红绿。"""
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem")        # 无 pedagogy 子字段
    hits = ge.run(include_advice=True)
    assert all(h.severity != "block" for h in hits if h.rule_id.startswith("PED-"))
    assert not any(h.severity == "block" for h in ge.run(include_advice=False))


# ── 元门禁：规则自身约束 ──────────────────────────────────────────────────
def test_rule_ids_unique_and_pedagogy_has_basis():
    ids = [r.id for r in ge.RULES]
    assert len(ids) == len(set(ids)), "规则 ID 必须唯一"
    for r in ge.RULES:
        if r.kind in ("pedagogy", "literature"):
            assert r.basis, f"{r.id} 缺学习科学依据（只建议不改文的前提）"


def test_duplicate_rule_registration_rejected():
    with pytest.raises(ValueError):
        ge.register(ge.Rule("ATOM-FM-REQUIRED", "dup", "fact", "programmatic", "block", "atom"))
    with pytest.raises(ValueError):
        ge.register(ge.Rule("PED-X", "有依据缺失的教学规则", "pedagogy",
                            "programmatic", "advice", "atom"))


# ── 真实仓库：双清单零漂移（ADR-0004 收敛后恒 0） ──────────────────────────
def test_manifest_has_no_drift_in_repo():
    assert ge.check_manifest_consistency() == [], \
        "pyproject:quality_gates 与 cppbible cmd_check 必须一一对应（ADR-0004）"
