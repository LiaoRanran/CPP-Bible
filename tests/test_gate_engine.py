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
    monkeypatch.setattr(ge, "MISCONCEPTIONS", tmp_path / "misconceptions")
    (tmp_path / "atoms").mkdir()
    (tmp_path / "evidence").mkdir()
    (tmp_path / "misconceptions").mkdir()
    return tmp_path


def _write_mis(base: Path, mid: str, **over: str) -> Path:
    d = base / "misconceptions"
    d.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": mid, "name": "某误解", "level": "deep", "domain": "MEM",
        "trigger_patterns": '\n  - "触发 1"',
        "refutations": '\n  - "反例 1"\n  - "反例 2"',
        "source": "ch1.md ⑯",
        "related_atoms": "[]",
    }
    fields.update(over)
    p = d / f"{mid}.md"
    p.write_text("---\n" + "".join(_kv(k, v) for k, v in fields.items()) + "---\n",
                 encoding="utf-8")
    return p


# ── G5：全局误解库 + 认知适切维度的回归锁 ──────────────────────────────────
def test_mis_library_deep_needs_two_refutations(sandbox: Path):
    """误解库自身：deep 类反例 <2 / level 非法 → block；合规 → 放行。

    误解库是 G5 大规模生产的前置资产，条目写歪会污染全库，故与原子**双向**校验。
    """
    _write_mis(sandbox, "MIS-MEM-001", refutations='\n  - "只有一条反例"')
    hits = ge.check_mis_library()
    assert any(h.rule_id == "MIS-LIBRARY" and "反例不足" in h.message for h in hits), \
        "deep 类只有 1 条反例必须被拦"

    _write_mis(sandbox, "MIS-MEM-001", level="wat")
    assert any("level 非法" in h.message for h in ge.check_mis_library())

    _write_mis(sandbox, "MIS-MEM-001", source="")            # 缺出处 → warn（不阻断）
    assert any(h.severity == "warn" and "source" in h.message
               for h in ge.check_mis_library())

    _write_mis(sandbox, "MIS-MEM-001")
    assert ge.check_mis_library() == [], "合规条目必须放行"


def test_misconception_ref_must_exist(sandbox: Path):
    """原子引用的误解 ID 必须存在——引用不存在的 ID 等于引用了一个不存在的反例。"""
    _write_mis(sandbox, "MIS-MEM-001")
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                pedagogy="\n  misconceptions: [MIS-MEM-001, MIS-MEM-999]")
    hits = ge.check_misconception_ref()
    assert len(hits) == 1 and "MIS-MEM-999" in hits[0].message

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                pedagogy="\n  misconceptions: [MIS-MEM-001]")
    assert ge.check_misconception_ref() == []


def test_audience_required_and_beginner_needs_analogy(sandbox: Path):
    """认知适切：audience / cognitive_load 必须合法声明；beginner 正文须有类比/直觉段。"""
    # 缺失 → 记债（warn）：G5 迁移期渐进标注，未标注不该阻断最小合规原子
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem")     # 两者都缺
    hits = ge.check_audience()
    assert sum(h.rule_id == "ATOM-AUDIENCE" for h in hits) == 2, "缺两个字段应报两条"
    assert all(h.severity == "warn" for h in hits), "缺失只记债、不阻断"

    # 写了但值非法 → block（路径排序会拿到非法值）
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                audience="novice", cognitive_load="medium")
    assert any(h.severity == "block" for h in ge.check_audience())

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                audience="intermediate", cognitive_load="medium")
    assert ge.check_audience() == [], "合规声明必须放行"

    p = _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                    audience="beginner", cognitive_load="low")
    assert any(h.severity == "warn" and "类比" in h.message
               for h in ge.check_audience()), "beginner 无直觉入口应告警"

    p.write_text(p.read_text(encoding="utf-8") + "\n## 类比\n把它想象成搬家。\n",
                 encoding="utf-8")
    assert ge.check_audience() == [], "补上类比段后应放行"


def test_prereq_readable_declaration_must_match_reality(sandbox: Path):
    """`prerequisites_readable` 声明须与实算一致——否则学习路径排序依据失真。"""
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                prerequisites_readable="true",
                relations="\n  - {type: prerequisite, target: ATOM-MEM-VALUE-001}")
    hits = ge.check_prereq_readable()
    assert len(hits) == 1 and "与实算不符" in hits[0].message, "声明可读但前置未锻造须报"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                prerequisites_readable="false",
                relations="\n  - {type: prerequisite, target: ATOM-MEM-VALUE-001}")
    assert ge.check_prereq_readable() == [], "诚实声明 false 应放行"

    # 前置被锻造后，实算翻为 True —— 仍声明 false 就又不一致了（双向都查）
    _write_atom(sandbox, "ATOM-MEM-VALUE-001.md", "mem", id="ATOM-MEM-VALUE-001")
    hits = ge.check_prereq_readable()
    assert len(hits) == 1 and "与实算不符" in hits[0].message, "实算翻正后旧声明须报"


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


def test_misconception_levels_blocks_and_passes(sandbox: Path):
    """误解分层：非结构化项 / 层非法 / deep 反例不足 → block；合规 → 放行。

    deep 须 ≥2 反例是调研核心结论（surface 一次纠正即可），故为 block 而非 advice。
    """
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                pedagogy="\n  misconception:\n    - \"std::move 会移动对象\"")
    assert any(h.rule_id == "ATOM-MISCONCEPTION-LEVELS"
               for h in ge.check_misconception_levels()), "字符串列表必须被拦"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                pedagogy="\n  misconception:\n    - {level: deep, text: 移动后源一定是空的}")
    hits = ge.check_misconception_levels()
    assert any("反例不足" in h.message for h in hits), "deep 无反例必须被拦"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem",
                pedagogy=("\n  misconception:\n    - {level: surface, text: move 会移动对象}\n"
                          "    - {level: deep, text: 移动后源一定是空的, "
                          "refutations: [EV-MEM-001, EV-MEM-002]}"))
    assert ge.check_misconception_levels() == [], "合规分层必须放行"


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
