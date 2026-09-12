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


# ── PED-MISCONCEPTION：三种合法写法兼容（369 任务2，P1-4）────────────────
def test_ped_misconception_singular_not_reported(sandbox: Path):
    """单数写法（历史形态，CONC 三颗）：不该报。"""
    _write_atom(sandbox, "ATOM-MEM-T1.md", "mem",
                pedagogy="\n  misconception:\n    - {level: surface, text: t, refutations: [EV-X]}")
    assert ge._misconception_gap() == [], "pedagogy.misconception 非空不该报"


def test_ped_misconception_plural_not_reported(sandbox: Path):
    """复数写法（**阴性毒样例**：26 颗原子中 22 颗用此形态）：不该报。"""
    _write_atom(sandbox, "ATOM-MEM-T2.md", "mem",
                pedagogy="\n  misconceptions: [MIS-MEM-001]")
    assert ge._misconception_gap() == [], "pedagogy.misconceptions 非空不该报"


def test_ped_misconception_top_level_not_reported(sandbox: Path):
    """顶层写法（4 颗折叠字符串 pedagogy 的原子）：不该报。"""
    _write_atom(sandbox, "ATOM-MEM-T3.md", "mem",
                pedagogy="一段教学散文（折叠字符串，无子字段）",
                misconceptions="[MIS-MEM-001]")
    assert ge._misconception_gap() == [], "顶层 misconceptions 非空不该报"


def test_ped_misconception_missing_reported(sandbox: Path):
    """三处皆空（阳性）：必须报，且 severity=advice（不阻断）。"""
    _write_atom(sandbox, "ATOM-MEM-T4.md", "mem", pedagogy="\n  motivation: m")
    hits = ge._misconception_gap()
    assert hits and hits[0].rule_id == "PED-MISCONCEPTION"
    assert hits[0].severity == "advice"


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
def test_atom_id_unique_pair(sandbox: Path):
    """身份唯一：stem≠id / id 重复 → block；对齐且唯一 → 放行（369 任务3，P1-5）。"""
    _write_atom(sandbox, "ATOM-MEM-RAII-001.md", "mem", id="ATOM-MEM-RAII-001")
    assert ge.check_atom_id_unique() == [], "stem==id 且唯一应放行"

    _write_atom(sandbox, "ATOM-ZZ-TMP-001.md", "mem", id="ATOM-MEM-RAII-001")
    hits = ge.check_atom_id_unique()
    assert all(h.severity == "block" for h in hits)
    assert any("stem" in h.message for h in hits), "stem≠id 必须拦"
    assert any("重复" in h.message for h in hits), "id 撞车必须拦"


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


# ── G6：四级状态 + DAL（「放权」体系的三条反作弊锁，解锁前必须先上锁）───────
_PROMOTED = ("\n  - {level: draft, at: legacy, by: writer:agent}"
             "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}"
             "\n  - {level: human-verified, at: 2026-09-12, by: human:liaoranran}")


def _verified_atom(base: Path, name: str = "ATOM-MEM-MOVE-001.md", **over: str) -> Path:
    """一颗「本应放行」的人级原子；各用例只改一个字段演反例。"""
    fields: dict[str, str] = {
        "status": "human-verified", "evidence": "[EV-1]", "first_hand": "true",
        "superiority": "s", "dal": "B", "human_review": "required",
        "status_history": _PROMOTED, "verified_by": "human:liaoranran",
    }
    fields.update(over)
    return _write_atom(base, name, "mem", **fields)


def test_status_enum_single_source_of_truth():
    """枚举单点化：`verified` 是历史别名 = human-verified；三级都算「已验证」。

    这条锁的是**静默失效**——散落的 `status == "verified"` 在新枚举下不报错、
    直接不拦，等于把 S1/S2/证据边界一起关掉。
    """
    assert ge.is_verified({"status": "verified"}), "历史别名必须等价 human-verified"
    assert ge.is_verified({"status": "machine-verified"})
    assert ge.is_verified({"status": "red-team-verified"})
    assert not ge.is_verified({"status": "draft"})
    assert ge.level_of({"status": "verified"}) == ge.level_of({"status": "human-verified"}) == 3


def test_status_value_pair(sandbox: Path):
    """枚举外取值必须显式拦（它会让所有等值判断静默漏过）。"""
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="wat")
    assert any(h.rule_id == "ATOM-STATUS-VALUE" for h in ge.check_status_value())

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="draft")
    assert ge.check_status_value() == []


def test_status_transition_pair(sandbox: Path):
    """跃迁链：草稿免报；缺链/链尾不符/前缀不符/人级无机器前驱 → block。"""
    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="draft")
    assert ge.check_status_transition() == [], "草稿不要求晋升历史"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="machine-verified")
    assert any("无 status_history" in h.message for h in ge.check_status_transition())

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="human-verified",
                status_history="\n  - {level: draft, at: legacy, by: writer:agent}"
                               "\n  - {level: human-verified, at: 2026-09-12, by: human:liaoranran}")
    assert any("无 machine/red-team 级" in h.message for h in ge.check_status_transition()), \
        "人级直签（跳过全部非人级核查）必须拦"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="red-team-verified",
                status_history=_PROMOTED)
    assert any("链尾" in h.message for h in ge.check_status_transition())

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="human-verified",
                status_history=_PROMOTED.replace("human:liaoranran", "writer:agent"))
    assert any("by 前缀" in h.message for h in ge.check_status_transition()), \
        "人级由 Agent 签必须拦"

    _verified_atom(sandbox)
    assert ge.check_status_transition() == [], "合规链（含 draft legacy）必须放行"


def test_dal_match_pair(sandbox: Path):
    """DAL：已入库必填；A/B 须人级 + human_review；C/D/E 免人审但**须人签豁免**。"""
    _verified_atom(sandbox, dal="")
    assert any("缺合法 dal" in h.message for h in ge.check_dal_match())

    _verified_atom(sandbox, human_review="optional")
    assert any("human_review: required" in h.message for h in ge.check_dal_match())

    _verified_atom(sandbox, status="machine-verified", verified_by="machine:gate")
    assert any("须 human-verified" in h.message for h in ge.check_dal_match()), \
        "DAL A/B 停机器级 = 未人审即入库"

    _verified_atom(sandbox, dal="C", human_review="optional", status="machine-verified",
                   verified_by="machine:gate")
    assert any("dal_reviewed_by" in h.message for h in ge.check_dal_match()), \
        "Writer 自定 dal: C 绕过人审必须拦（放权不得变权力反转）"

    _verified_atom(sandbox, dal="C", human_review="optional", status="machine-verified",
                   verified_by="machine:gate", dal_reviewed_by="human:liaoranran")
    assert ge.check_dal_match() == [], "人签豁免后 C 级放行"

    _write_atom(sandbox, "ATOM-MEM-MOVE-001.md", "mem", status="draft")
    assert ge.check_dal_match() == [], "草稿期不要求分级"


def test_s1_signoff_prefix_matches_level(sandbox: Path):
    """S1 级别化：前缀须与状态级别匹配；人级的「唯人可置」语义不变。"""
    _verified_atom(sandbox, status="machine-verified", verified_by="machine:gate")
    assert ge.check_s1_human_signoff() == []

    _verified_atom(sandbox, status="machine-verified", verified_by="human:liaoranran")
    assert any(h.rule_id == "S1-AUTHOR-SELF-VERIFY" for h in ge.check_s1_human_signoff())

    _verified_atom(sandbox, verified_by="machine:gate")
    assert any(h.rule_id == "S1-AUTHOR-SELF-VERIFY" for h in ge.check_s1_human_signoff()), \
        "人级却由机器签必须拦"
