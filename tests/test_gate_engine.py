"""门禁引擎 M4 的毒样例回归：每条规则**正例触发 + 反例不触发**（元门禁：误报/漏报回归）。

覆盖：
  * 事实规则：必填字段 / verified 绑定 / DAG 环 / ID 格式 / 证伪对照 / 灰色地带标注
  * 误报回归锁：「待补」是合法缺口留痕，不得被判占位符
  * severity 语义：advice 规则永不阻断（只建议不改文）
  * 规则自身约束：ID 唯一、教学/文学规则必须标学习科学依据
  * 真实仓库：双清单零漂移（ADR-0004 收敛后应恒为 0）
"""
from __future__ import annotations

import os
import time
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


def test_s3_run_match_file_clean_passes(sandbox: Path):
    """阴样例（369 任务8，P1-12）：期望值只在 .out、夹具用格式串+变量 → 不得误报。"""
    d = sandbox / "evidence"
    of = d / "x.out"
    of.write_text("total=100000\n", encoding="utf-8")
    fx = d / "_fx_clean.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("total=%d\\n", 100000); }\n',
                  encoding="utf-8")
    _write_ev(sandbox, fixture=fx.as_posix(),
              actual=f"\n  run_match_file: {of.as_posix()}\n  run_match_keys: [total]")
    assert ge.check_s3_hardcoded_expected() == [], "格式串+变量不应误报（合法格式串豁免）"


def test_s3_run_match_file_hardcoded_blocks(sandbox: Path):
    """阳性（369 任务8，P1-12）：期望值硬编码进夹具字面量（.out 只是抄回来）→ block。"""
    d = sandbox / "evidence"
    of = d / "x.out"
    of.write_text("total=100000\n", encoding="utf-8")
    fx = d / "_fx_poison.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("total=100000\\n"); }\n',
                  encoding="utf-8")
    _write_ev(sandbox, fixture=fx.as_posix(),
              actual=f"\n  run_match_file: {of.as_posix()}\n  run_match_keys: [total]")
    hits = ge.check_s3_hardcoded_expected()
    assert hits and hits[0].severity == "block"
    assert "x.out" in hits[0].message, "命中须标注来源（run_match_file 出处）"


def test_out_undeclared_key_warns(sandbox: Path):
    """阳性（373-B3 窄化）：.out 出现未声明的 `key=value` 行 → warn。

    未声明读数 = 门禁视野外的自由区：S3/恒真观测都不扫它、expected 也约束不到，
    独立渗透的编造载荷（`fabricated_leak=64`）正是这一形态。
    """
    of = sandbox / "evidence" / "x.out"
    of.write_text("total=100000\nfabricated_leak=64\n", encoding="utf-8")
    _write_ev(sandbox, actual=f"\n  run_match_file: {of.as_posix()}\n"
                              "  run_match_keys: [total]")
    hits = ge.check_evidence_out_undeclared_key()
    assert hits and hits[0].rule_id == "EV-OUT-UNDECLARED-KEY"
    assert "fabricated_leak" in hits[0].message
    assert hits[0].severity == "warn", "与编造键结构上不可区分 ⇒ 只 warn，不阻断存量"


def test_out_declared_keys_pass(sandbox: Path):
    """阴性：键全部声明，且注释行/散文行不判 → 放行（不得恒红）。"""
    of = sandbox / "evidence" / "x.out"
    of.write_text("# 注释行\n这是散文行没有等号\ntotal=100000\n", encoding="utf-8")
    _write_ev(sandbox, actual=f"\n  run_match_file: {of.as_posix()}\n"
                              "  run_match_keys: [total]")
    assert ge.check_evidence_out_undeclared_key() == []


def _write_ev_with_artifact(sandbox: Path, fx_text: str, art_text: str,
                            asserts: str, **over: str) -> None:
    """写一张带真实夹具/工件文件的证据卡（断言映射检查需要读文件内容）。"""
    fx = sandbox / "fx.cpp"
    fx.write_text(fx_text, encoding="utf-8")
    art = sandbox / "a.asm"
    art.write_text(art_text, encoding="utf-8")
    _write_ev(sandbox, fixture=fx.as_posix(), artifact=art.as_posix(),
              artifact_assert="\n" + asserts, **over)


def test_assert_universal_symbol_blocks(sandbox: Path):
    """阳性（373-B2）：断言锚定 `main` 这类无判别力符号 → block（恒真载荷）。"""
    _write_ev_with_artifact(sandbox, "void f(){}\n", "f:\n\tret\n",
                            '  - {kind: contains, text: "main"}')
    hits = ge.check_evidence_assert_symbol_mapped()
    assert hits and hits[0].severity == "block", "通用符号断言必须拦（零判别力）"


def test_assert_symbol_without_source_warns(sandbox: Path):
    """阳性（373-B2）：符号在夹具/工件中均无出处 → warn（拼错或平台专属拼写）。"""
    _write_ev_with_artifact(sandbox, "void f(){}\n", "f:\n\tret\n",
                            '  - {kind: contains, text: "_Znotexist"}')
    hits = ge.check_evidence_assert_symbol_mapped()
    assert hits and hits[0].severity == "warn", "无出处的符号名必须可见（不阻断，但别装作有校验）"


def test_assert_symbol_mapped_passes(sandbox: Path):
    """阴性：符号在工件里有出处 → 放行。"""
    _write_ev_with_artifact(sandbox, "void f(){}\n", "_Znwy:\n\tret\n",
                            '  - {kind: contains, text: "_Znwy"}')
    assert ge.check_evidence_assert_symbol_mapped() == []


def test_assert_symbol_map_declared_passes(sandbox: Path):
    """阴性：卡内**显式** symbol_map 声明夹具名→工件符号 → 放行（工具不做模糊匹配）。"""
    _write_ev_with_artifact(sandbox, "void spin_plain(){ }\n", "spin_other:\n\tret\n",
                            '  - {kind: contains, text: "_Z10spin_plainv"}',
                            symbol_map="\n  spin_plain: _Z10spin_plainv")
    assert ge.check_evidence_assert_symbol_mapped() == []


def test_assert_prose_skipped(sandbox: Path):
    """阴性：纯散文断言不由本规则拦（裁决 §2.2 交红队/人审），不得误报。"""
    _write_ev_with_artifact(sandbox, "void f(){}\n", "f:\n\tret\n",
                            '  - {kind: contains, text: "空壳工件"}')
    assert ge.check_evidence_assert_symbol_mapped() == []


def test_assert_universal_symbol_blocks_even_if_in_artifact(sandbox: Path):
    """阳性（373 绕过测试 2a/2b 深化）：通用符号即便在工件里出现也 block（零判别力）。"""
    _write_ev_with_artifact(sandbox, "int main(){}\n", "main:\n\tcall foo\n\tret\n",
                            '  - {kind: contains, text: "main"}')
    hits = ge.check_evidence_assert_symbol_mapped()
    assert hits and hits[0].severity == "block", "main 在工件里也须拦（恒真断言）"


def test_assert_symbol_in_comment_not_treated_as_source(sandbox: Path):
    """阳性（373 绕过测试 2c）：夹具注释里出现符号名不能算"有出处"（absent 不再被蒙混）。"""
    _write_ev_with_artifact(sandbox, "// _Znwm\nint main(){}\n", "other:\n\tret\n",
                            '  - {kind: absent, text: "_Znwm"}')
    hits = ge.check_evidence_assert_symbol_mapped()
    assert any(h.rule_id == "EV-ASSERT-SYMBOL-MAPPED" for h in hits), "注释伪造出处须被拦"


def test_artifact_producer_missing_on_new_card_blocks(sandbox: Path):
    """阳性（373-N4）：名单外的卡缺 `artifact_producer` → block。

    这一条不能做成"缺字段就放过"——否则攻击者只要不写字段就能绕过整条规则。
    """
    _write_ev(sandbox, id="EV-MEM-NEWPROD")
    hits = ge.check_evidence_artifact_producer()
    assert hits and hits[0].severity == "block"


def test_artifact_producer_non_compiler_blocks(sandbox: Path):
    """阳性（373-N4 借工件）：`cp`/脚本复制他人工件 ≠ 亲自编译 → block。"""
    _write_ev(sandbox, artifact_producer="cp Examples/atoms/other.asm a.asm")
    hits = ge.check_evidence_artifact_producer()
    assert hits and hits[0].severity == "block"


def test_artifact_producer_compiler_passes(sandbox: Path):
    """阴性：声明编译器命令且其段逐字在 command 中、-o==artifact → 放行（含带路径/带 .exe）。"""
    prod = "C:/Qt/Tools/mingw1530_64/bin/g++.exe -S x.cpp -o a.asm"
    _write_ev(sandbox, command=prod, artifact_producer=prod)
    assert ge.check_evidence_artifact_producer() == []


def test_artifact_producer_exempt_existing_card_passes(sandbox: Path):
    """阴性：迁移名单内的存量卡缺字段 → 放行（名单 = 可审计的迁移积压）。"""
    _write_ev(sandbox, id="EV-MEM-001")
    assert ge.check_evidence_artifact_producer() == []


def test_artifact_producer_decoupled_from_command_blocks(sandbox: Path):
    """阳性（373 绕过测试 3d）：producer 声明编译、command 实际 cp 借工件 → block。"""
    _write_ev(sandbox, command="cp Examples/atoms/other.asm a.asm",
              artifact_producer="g++ -S x.cpp -o a.asm")
    hits = ge.check_evidence_artifact_producer()
    assert any(h.severity == "block" for h in hits), "producer 不在 command 须拦"


def test_artifact_producer_o_target_mismatch_blocks(sandbox: Path):
    """阳性（373 绕过测试 3d）：producer 在 command 但 -o 目标≠artifact → block。"""
    prod = "g++ -S x.cpp -o b.asm"          # -o b.asm ≠ 卡 artifact a.asm
    _write_ev(sandbox, command=prod, artifact_producer=prod)
    hits = ge.check_evidence_artifact_producer()
    assert any(h.severity == "block" for h in hits), "-o 目标须 == artifact"


def test_artifact_producer_consistent_passes(sandbox: Path):
    """阴性：producer 逐字在 command 且 -o==artifact → 不报（含带路径/带 .exe）。"""
    prod = "C:/Qt/Tools/mingw1530_64/bin/g++.exe -S x.cpp -o a.asm"
    _write_ev(sandbox, command=prod, artifact_producer=prod)
    assert ge.check_evidence_artifact_producer() == []


def test_evidence_id_duplicate_blocks(sandbox: Path):
    """阳性（373-N2）：同 id 的两张卡 → block（按 id 取 verdict 的下游会静默覆盖）。"""
    _write_ev(sandbox, id="EV-MEM-DUP")
    (sandbox / "evidence" / "mem" / "EV-MEM-DUP2.md").write_text(
        (sandbox / "evidence" / "mem" / "EV-MEM-001.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    hits = ge.check_evidence_id_unique()
    assert any("重复" in h.message for h in hits)
    assert all(h.severity == "block" for h in hits)


def test_evidence_id_unique_passes(sandbox: Path):
    """阴性：stem==id 且唯一 → 放行。"""
    _write_ev(sandbox, id="EV-MEM-001")
    assert ge.check_evidence_id_unique() == []


def test_relations_mapping_form_is_normalized(sandbox: Path):
    """373-N1：mapping 写法 `- prerequisite: X` 归一后必须参与判据（此前静默跳过）。"""
    _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                relations="\n  - prerequisite: ATOM-MEM-002")
    _write_atom(sandbox, "ATOM-MEM-002.md", "mem", id="ATOM-MEM-002",
                relations="\n  - prerequisite: ATOM-MEM-001")      # 环
    hits = ge.check_relations_dag()
    assert hits and "环" in hits[0].message, "归一后环必须可见（此前三条规则都跳过）"


def test_relations_mapping_form_existing_target_passes(sandbox: Path):
    """阴性：mapping 写法指向已存在目标 → 放行（归一不得制造误报）。"""
    _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                relations="\n  - prerequisite: ATOM-MEM-002")
    _write_atom(sandbox, "ATOM-MEM-002.md", "mem", id="ATOM-MEM-002", relations="[]")
    assert ge.check_relations_dag() == []
    assert ge.check_relations_target_exists() == []


# ── 415 D1：relations 矛盾检测（ATOM-REL-CONFLICT）──────────────────────────────
class TestAtomRelConflict:
    def test_prerequisite_contradicts_blocks(self, sandbox: Path):
        """阳例：A.prereq=B 且 B.contradicts=A → block。"""
        _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                    relations="\n  - prerequisite: ATOM-MEM-002")
        _write_atom(sandbox, "ATOM-MEM-002.md", "mem", id="ATOM-MEM-002",
                    relations="\n  - contradicts: ATOM-MEM-001")
        hits = ge.check_atom_rel_conflict()
        assert any(h.rule_id == "ATOM-REL-CONFLICT" for h in hits), hits

    def test_self_contradicts_blocks(self, sandbox: Path):
        """阳例：A.contradicts=A → block（自相矛盾）。"""
        _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                    relations="\n  - contradicts: ATOM-MEM-001")
        hits = ge.check_atom_rel_conflict()
        assert any(h.rule_id == "ATOM-REL-CONFLICT" for h in hits), hits

    def test_contrasts_not_conflict(self, sandbox: Path):
        """阴例：contrasts 不是矛盾关系 → 不 block。"""
        _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                    relations="\n  - prerequisite: ATOM-MEM-002\n  - contrasts: ATOM-MEM-003")
        _write_atom(sandbox, "ATOM-MEM-002.md", "mem", id="ATOM-MEM-002",
                    relations="\n  - contrasts: ATOM-MEM-001")
        assert ge.check_atom_rel_conflict() == []

    def test_dict_form_contradicts_blocks(self, sandbox: Path):
        """阳例：dict 写法 {type: contradicts, target: X} 也必须被检。"""
        _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                    relations="\n  - {type: prerequisite, target: ATOM-MEM-002}")
        _write_atom(sandbox, "ATOM-MEM-002.md", "mem", id="ATOM-MEM-002",
                    relations="\n  - {type: contradicts, target: ATOM-MEM-001}")
        assert ge.check_atom_rel_conflict() != []


# ── 414 P1-8（F07）：纯标量 relations 不得静默丢弃 ──────────────────────────────
def test_relations_scalar_warns(sandbox: Path):
    """阳例：relations: [PERF-001]（纯标量）必须 warn，不能静默跳过。"""
    _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001",
                relations="[PERF-001]")
    hits = ge.check_relations_target_exists()
    assert any(h.rule_id == "ATOM-REL-TARGET" and "纯标量" in h.message for h in hits), hits


def test_relations_empty_no_scalar_warn(sandbox: Path):
    """阴例：标准空 relations `[]` 不得误报标量 warn。"""
    _write_atom(sandbox, "ATOM-MEM-001.md", "mem", id="ATOM-MEM-001", relations="[]")
    hits = ge.check_relations_target_exists()
    assert not any("纯标量" in h.message for h in hits), hits


# ── 414 P0-1（F08）：poison exit 逻辑不得对未覆盖规则放行 ──────────────────────
def test_poison_exit_code():
    """全过且无未覆盖 → 0；否则 → 1（修复前 1 or x 恒 1 且忽略 uncovered）。"""
    import poison_drill as pd
    assert pd.gate_exit_code(5, 5, []) == 0
    assert pd.gate_exit_code(5, 4, []) == 1
    assert pd.gate_exit_code(5, 5, ["SOME-RULE"]) == 1


def test_matrix_command_is_not_a_trace_anchor(sandbox: Path):
    """373-N3：编译命令文本不再算留痕（旧锚 `g++ … -o` 让声明结构上恒绿）。"""
    _write_ev(sandbox, command="g++ -O2 x.cpp -o x.exe",
              falsification="对照输出 1",
              matrix="\n  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]\n"
                     "  std: [c++17]\n  opt: [-O2]")
    hits = ge.check_evidence_matrix_backed()
    assert hits and hits[0].rule_id == "EV-MATRIX-UNBACKED"


def test_matrix_two_traces_passes(sandbox: Path):
    """阴性：两处可核对留痕（双平台 .out）→ 放行。"""
    _write_ev(sandbox, falsification="对照见 Examples/atoms/a.out 与 build/b.out 两处 1",
              matrix="\n  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]\n"
                     "  std: [c++17]\n  opt: [-O2]")
    assert ge.check_evidence_matrix_backed() == []


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


# ── 零诊断类判据须 -Werror（W3）────────────────────────────────────────────
def test_zero_diag_requires_werror(sandbox: Path):
    """falsification 写"无警告/零诊断"但 command 无 -Werror → block（472 P1-1 升格）。

    371 报告 W3：replay 的 compile_rc 只看退出码、警告不影响 rc，故此体裁的判据
    不补 -Werror 就是"写得漂亮但机器看不见"。本回归锁三态：缺 → 报；有 → 放行；
    普通判据（无零诊断措辞）→ 不误报。
    472 P1-1：级别 warn → block（不可复算判据不得放行；存量 0 命中，零误伤）。
    """
    _write_ev(sandbox, falsification="若编译产生任何警告（非零诊断）→ 判 refute")
    hits = ge.check_evidence_zero_diag_werror()
    assert len(hits) == 1, hits
    assert hits[0].rule_id == "EV-ZERO-DIAG-WERROR" and hits[0].severity == "block"

    _write_ev(sandbox, command="g++ -Wall -Wextra -Werror -c x.cpp",
              falsification="若编译产生任何警告（非零诊断）→ 判 refute")
    assert ge.check_evidence_zero_diag_werror() == [], "带 -Werror 应放行"

    _write_ev(sandbox, falsification="对照 B 输出 1（非 0）")
    assert ge.check_evidence_zero_diag_werror() == [], "普通判据不得误报"

    _write_ev(sandbox, falsification="若出现 no warning 之外的任何输出 → refute")
    assert len(ge.check_evidence_zero_diag_werror()) == 1, "英文措辞同受约束"


def test_zero_diag_rule_declared_block():
    """规则声明级别与 Finding 实际级别必须一致（472 P1-1 升 block 后）。"""
    r = next(x for x in ge.RULES if x.id == "EV-ZERO-DIAG-WERROR")
    assert r.severity == "block", r


# ── A3：.out 两处盲区（P7 锚不得自证 / P6 视野纳入 .out）────────────────────
def test_matrix_anchor_not_self_proving(sandbox: Path):
    """P7 留痕锚必须出现在 **actual 段之外**（声明 ≠ 留痕，A3①）。"""
    base = {
        "actual": "\n  run_match_file: Examples/atoms/_x.out\n  run_match_keys:\n    - k",
        "matrix": "\n  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]\n"
                  "  std: [c++17]\n  opt: [-O2]",
    }
    p = _write_ev(sandbox, **base)
    assert any(h.rule_id == "EV-MATRIX-UNBACKED" for h in ge.check_evidence_matrix_backed()), \
        "锚只出现在 actual 段 = 自证，必须报"
    with p.open("a", encoding="utf-8") as fh:
        # 373-N3：单一留痕撑不起"多编译器矩阵" ⇒ 只补一处**仍须报**
        fh.write("\n## 复算留痕\nWSL（GCC 13.3）留痕：`Examples/atoms/_x_wsl.out`\n")
    assert any(h.rule_id == "EV-MATRIX-UNBACKED" for h in ge.check_evidence_matrix_backed()), \
        "373-N3：只一处留痕不足以支撑多平台声明"
    with p.open("a", encoding="utf-8") as fh:      # 补第二处（双平台各一份）⇒ 放行
        fh.write("MinGW（GCC 15.3）留痕：`Examples/atoms/_x_mingw.out`\n")
    assert ge.check_evidence_matrix_backed() == [], "两处可核对留痕应放行（门禁不得恒红）"


def test_trivial_observation_scans_out_file(sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """P6 视野纳入 `run_match_file` 指向的 `.out`（A3②）。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    out = sandbox / "Examples" / "atoms" / "_x.out"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("k=1\n", encoding="utf-8")
    _write_ev(sandbox, **{
        "actual": "\n  run_match_file: Examples/atoms/_x.out\n  run_match_keys:\n    - k",
    })
    assert ge.check_evidence_trivial_observation() == [], "普通读数不该报"
    out.write_text("k=not null=1\n", encoding="utf-8")
    hits = ge.check_evidence_trivial_observation()
    assert hits and hits[0].rule_id == "EV-TRIVIAL-OBSERVATION", \
        ".out 里的恒真型读数必须在视野内（此前是盲区）"


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


# ── 373-P0-B9：署名实名制（前缀命中 ≠ 实名签署）───────────────────────────
def test_principal_ok_is_single_point():
    """实名制单点判定：前缀 + 非空实名 + 人级在册，三个条件缺一不可。"""
    assert ge.principal_ok("machine:gate", ("machine:",))[0]
    assert not ge.principal_ok("machine:", ("machine:",))[0], "空名不算签署"
    assert ge.principal_ok("writer:agent", ())[0], "draft 级只要求非空留痕"
    assert not ge.principal_ok("", ())[0], "draft 级也不能空"
    assert not ge.principal_ok("human:   ", ("human:",))[0], "纯空格不算签署"
    assert not ge.principal_ok("human:attacker", ("human:",))[0], "不在册不得签人级"
    assert ge.principal_ok("human:liaoranran", ("human:",))[0]


def test_signoff_requires_real_name_not_just_prefix(sandbox: Path):
    """S1：`human:` 前缀命中不等于实名签署（373 实测逃逸的最短路径）。"""
    for bad in ("human:", "human:   ", "human:attacker"):
        _verified_atom(sandbox, verified_by=bad)
        assert any(h.rule_id == "S1-AUTHOR-SELF-VERIFY"
                   for h in ge.check_s1_human_signoff()), \
            f"verified_by={bad!r} 必须拦（前缀命中 ≠ 实名签署）"

    _verified_atom(sandbox)
    assert ge.check_s1_human_signoff() == [], "在册实名仍须放行（不得误伤存量）"


def test_status_history_and_dal_signoff_require_real_name(sandbox: Path):
    """B9 同源另两处：status_history 的 by、DAL 豁免的人签，都必须实名。"""
    empty_tail = ("\n  - {level: draft, at: legacy, by: writer:agent}"
                  "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}"
                  "\n  - {level: human-verified, at: 2026-09-12, by: human:}")
    _verified_atom(sandbox, status_history=empty_tail)
    assert any("缺实名" in h.message for h in ge.check_status_transition()), \
        "status_history 里 by: human:（空名）必须拦"

    _verified_atom(sandbox, dal="C", human_review="optional",
                   status="machine-verified", verified_by="machine:gate",
                   dal_reviewed_by="human:")
    assert any("dal_reviewed_by" in h.message for h in ge.check_dal_match()), \
        "DAL C/D/E 豁免人审的人签为空名必须拦"

    _verified_atom(sandbox, dal="C", human_review="optional",
                   status="machine-verified", verified_by="machine:gate",
                   dal_reviewed_by="human:liaoranran")
    assert ge.check_dal_match() == [], "人签实名后 C 级仍须放行"


# ── 414 P0-2（F01）：MSVC 卡免检链 ──────────────────────────────────────────
# 注意：勿与上方既有 _write_ev(base, **over) 同名——模块级后定义会覆盖前者。
def _write_card(base: Path, name: str, **over: str) -> Path:
    d = base / "evidence" / "mem"
    d.mkdir(parents=True, exist_ok=True)
    fields = {
        "id": "EV-MEM-TEST", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
        "command": "cl /std:c++17 /c fx.cpp", "verdict": "confirm",
    }
    fields.update(over)
    p = d / name
    p.write_text("---\n" + "".join(_kv(k, v) for k, v in fields.items()) + "---\n",
                 encoding="utf-8")
    return p


def test_cl_card_confirm_is_blocked(sandbox: Path):
    """F01 正例：含 cl 的卡标 verdict:confirm → EV-MSCV-NO-VERIFY block。

    replay 对 cl 卡只能给 infra_error（MSVC 永久边界，从未复算），卡面宣称
    confirm 即「不可验证的卡被当成已验证」，一次 accept 永久挂账。
    """
    _write_card(sandbox, "EV-MEM-CL1.md")
    who = {f.rule_id for f in ge.check_evidence_msvc_no_verify()}
    assert "EV-MSCV-NO-VERIFY" in who, "cl 卡标 confirm 必须拦"


def test_cl_card_non_confirm_passes(sandbox: Path):
    """F01 阴性：cl 卡不宣称 confirm（unverified/refute）→ 放行。"""
    _write_card(sandbox, "EV-MEM-CL2.md", verdict="unverified")
    _write_card(sandbox, "EV-MEM-CL3.md", verdict="refute",
              id="EV-MEM-CL3", command="cl /c fx.cpp")
    assert ge.check_evidence_msvc_no_verify() == [], "不宣称已复算的 cl 卡不得拦"


def test_gcc_card_confirm_not_flagged(sandbox: Path):
    """F01 误伤回归：g++ 卡（可复算）标 confirm → 放行。"""
    _write_card(sandbox, "EV-MEM-GCC.md", command="g++ -std=c++17 -c fx.cpp")
    _write_card(sandbox, "EV-MEM-GCC2.md", id="EV-MEM-GCC2",
              command="C:/Qt/Tools/mingw1530_64/bin/g++.exe -S fx.cpp -o fx.asm")
    assert ge.check_evidence_msvc_no_verify() == [], "g++ 卡不得误拦"


# ── 414 P0-3（F02）：编译后覆写时序约束 ────────────────────────────────────
_PROD = "g++ -std=c++17 -O2 -S fx.cpp -o fx.asm"


def _temporal_ev(sandbox: Path, name: str, tail: str) -> Path:
    return _write_card(sandbox, name, command=_PROD + tail,
                     artifact_producer=_PROD, artifact="fx.asm")


def test_temporal_python_overwrite_blocked(sandbox: Path):
    """F02 正例：编译后 python 改写工件（402 F02 攻击载荷）→ block。"""
    _temporal_ev(sandbox, "EV-MEM-T1.md",
                 " && python -c \"shutil.copy('other.asm', 'fx.asm')\"")
    hits = [f for f in ge.check_evidence_artifact_producer() if f.severity == "block"]
    assert hits, "编译后 python 覆写必须 block"


def test_temporal_powershell_overwrite_blocked(sandbox: Path):
    _temporal_ev(sandbox, "EV-MEM-T2.md",
                 " && powershell -Command Copy-Item other.asm fx.asm")
    hits = [f for f in ge.check_evidence_artifact_producer() if f.severity == "block"]
    assert hits, "编译后 powershell Copy-Item 覆写必须 block"


def test_temporal_cp_and_redirect_blocked(sandbox: Path):
    _temporal_ev(sandbox, "EV-MEM-T3.md", " && cp other.asm fx.asm")
    _temporal_ev(sandbox, "EV-MEM-T4.md", " && echo staged > fx.asm")
    hits = [f for f in ge.check_evidence_artifact_producer() if f.severity == "block"]
    assert len(hits) >= 2, "cp 与 > 重定向覆写都必须 block"


def test_temporal_pre_compile_overwrite_passes(sandbox: Path):
    """F02 阴性：覆写在编译**前**（会被编译覆盖）→ 放行。"""
    _write_card(sandbox, "EV-MEM-T5.md", command="cp other.asm fx.asm && " + _PROD,
              artifact_producer=_PROD, artifact="fx.asm")
    blocks = [f for f in ge.check_evidence_artifact_producer() if f.severity == "block"]
    assert not blocks, "编译前的覆写会被编译覆盖，不得拦"


def test_temporal_post_read_passes(sandbox: Path):
    """F02 阴性：编译后显式读程序（type/grep）→ 不拦也不 warn。"""
    _temporal_ev(sandbox, "EV-MEM-T6.md", " && type fx.asm")
    _temporal_ev(sandbox, "EV-MEM-T7.md", " && grep foo fx.asm")
    assert ge.check_evidence_artifact_producer() == [], "编译后读取不得拦/不得 warn"


# ── 414 P1-4~7：F03 contains_in text / F04 全角键 / F06 陈旧 mtime / F09 重复键 ──
def test_contains_in_text_empty_or_cjk_blocked(sandbox: Path):
    """F03：contains_in/absent_in 的 text=空 / 纯中文 → block（结构性无判别力）。

    注：414 原案「通用助记符一律 block」实测误伤存量 4 处（区间语义下
    `absent_in je` 是强断言、`contains_in je` 是活性对照），收窄为空/纯中文
    block + contains_in 通用助记符 advice。
    """
    _write_card(sandbox, "EV-MEM-F3B.md",
              artifact_assert="\n  - {kind: absent_in, symbol: asm, text: 纯中文断言}")
    _write_card(sandbox, "EV-MEM-F3C.md", id="EV-MEM-F3C",
              artifact_assert='\n  - {kind: contains_in, symbol: asm, text: ""}')
    hits = [f for f in ge.check_evidence_assert_symbol_mapped() if f.severity == "block"]
    assert len(hits) >= 2, "text 空/纯中文必须 block"


def test_contains_in_text_generic_mnemonic_advice(sandbox: Path):
    """F03：contains_in 的 text=通用助记符 → advice（弱断言不阻断）。

    载荷用 `ret`（在 UNIVERSAL_SYMBOLS 中；`mov` 不在集合里，只有 movq/movl）。"""
    _write_card(sandbox, "EV-MEM-F3A.md",
              artifact_assert="\n  - {kind: contains_in, symbol: asm, text: ret}")
    hits = [f for f in ge.check_evidence_assert_symbol_mapped()
            if f.severity == "advice"]
    assert hits, "contains_in+通用助记符须至少给 advice"


def test_contains_in_text_specific_passes(sandbox: Path):
    """F03 阴性：text 有判别力（工件可定位的字面文本）→ 不因 F03 拦。"""
    _write_card(sandbox, "EV-MEM-F3D.md",
              artifact_assert="\n  - {kind: contains_in, symbol: asm, text: vmovaps xmm0}")
    hits = [f for f in ge.check_evidence_assert_symbol_mapped()
            if f.severity in ("block", "advice") and "text=" in f.message]
    assert not hits, "有判别力 text 不得拦/不得建议"


# ── 500 任务 1：_assert_haystack 空路径守卫（整仓 rglob 性能 + 假阴性双修）──────
def test_haystack_empty_fields_do_not_scan_repo(
        sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """500 任务1（阳性）：空 fixture/artifact 不得把**仓库根**当 haystack。

    修复前 `_add("")` ⇒ `ROOT / ""` = 仓库根（`is_dir()` 真）⇒ 落入 rglob 分支，
    把整仓 28588 个文件全文读入：①单测白烧 42–80s（3 张卡合计 174.7s）；
    ②haystack 退化为整仓 ⇒ **任何**符号都"找得到出处"⇒ 下述断言（其 text 在仓库
    别处存在、但本卡夹具/工件中并无）被静默放行（假阴性）。修复后 haystack 为空。
    """
    monkeypatch.setattr(ge, "ROOT", sandbox)
    # 载荷刻意选用「真实存在于仓库别处」（gate 源码里就有这个规则 ID）但不在本卡
    # 夹具/工件中的字符串：修复前会被整仓 haystack 兜住而静默通过。
    _write_card(sandbox, "EV-MEM-H1.md", id="EV-MEM-H1",
                artifact_assert="\n  - {kind: contains, text: EV-ASSERT-SYMBOL-MAPPED}")
    p = sandbox / "evidence" / "mem" / "EV-MEM-H1.md"
    assert ge._assert_haystack(ge._meta(p)) == "", \
        "空 fixture/artifact 的 haystack 必须是空串（不得退化为整仓）"
    warns = [h for h in ge.check_evidence_assert_symbol_mapped()
             if h.severity == "warn"]
    assert any("EV-ASSERT-SYMBOL-MAPPED" in h.message for h in warns), \
        "无出处断言必须 warn（修复前因整仓 haystack 假阴性放行）"


def test_haystack_fixture_symbol_is_mappable(
        sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """500 任务1（阴性）：有 fixture 且符号能在其中定位 ⇒ 不命中（正常搜索不受影响）。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    (sandbox / "fx500.cpp").write_text("int zzz_fixture_symbol_500 = 1;\n",
                                       encoding="utf-8")
    _write_card(sandbox, "EV-MEM-H2.md", id="EV-MEM-H2", fixture="fx500.cpp",
                artifact_assert="\n  - {kind: contains, text: zzz_fixture_symbol_500}")
    p = sandbox / "evidence" / "mem" / "EV-MEM-H2.md"
    assert "zzz_fixture_symbol_500" in ge._assert_haystack(ge._meta(p)), \
        "有 fixture 时应正常读入其文本（守卫不得误伤正常路径）"
    warns = [h for h in ge.check_evidence_assert_symbol_mapped()
             if h.severity == "warn" and "zzz_fixture_symbol_500" in h.message]
    assert not warns, "符号可在 fixture 中定位 ⇒ 不得 warn"


def test_haystack_both_empty_all_asserts_warn(
        sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """500 任务1（边界）：fixture 与 artifact 双空 ⇒ haystack 为空，所有断言都 warn。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    toks = ("alpha_tok_500", "beta_tok_500")
    for i, txt in enumerate(toks, start=1):
        _write_card(sandbox, f"EV-MEM-H3{i}.md", id=f"EV-MEM-H3{i}",
                    artifact_assert=f"\n  - {{kind: contains, text: {txt}}}")
        p = sandbox / "evidence" / "mem" / f"EV-MEM-H3{i}.md"
        assert ge._assert_haystack(ge._meta(p)) == "", "双空 ⇒ haystack 必须为空串"
    warns = [h.message for h in ge.check_evidence_assert_symbol_mapped()
             if h.severity == "warn"]
    for txt in toks:
        assert any(txt in m for m in warns), f"双空卡的断言 {txt} 必须 warn"


def test_out_key_unicode_detected(sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """F04：全角键（`ｎｐｒｏｃ=`）也计入未声明读数键。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    (sandbox / "fx.out").write_text("ｎｐｒｏｃ=1\n", encoding="utf-8")
    _write_card(sandbox, "EV-MEM-F4A.md",
              actual="\n  run_match_file: fx.out\n  run_match_keys: []")
    hits = ge.check_evidence_out_undeclared_key()
    assert hits and "ｎｐｒｏｃ" in hits[0].message, "全角键必须计入"


def test_out_key_ascii_declared_passes(sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """F04 阴性：ASCII 已声明键 → 不 warn（误伤回归）。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    (sandbox / "fx2.out").write_text("threads=4\n", encoding="utf-8")
    _write_card(sandbox, "EV-MEM-F4B.md",
              actual="\n  run_match_file: fx2.out\n  run_match_keys: [threads]")
    assert ge.check_evidence_out_undeclared_key() == [], "已声明键不得 warn"


def test_out_stale_mtime_warns(sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """F06：.out 明显旧于夹具（>5s 宽容差）→ warn。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    (sandbox / "_fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    outp = sandbox / "fx.out"
    outp.write_text("x=1\n", encoding="utf-8")
    past = time.time() - 600
    os.utime(outp, (past, past))
    _write_card(sandbox, "EV-MEM-F6A.md", fixture="_fx.cpp",
              actual="\n  run_match_file: fx.out\n  run_match_keys: []")
    hits = ge.check_evidence_out_stale_mtime()
    assert hits and hits[0].severity == "advice", ".out 旧于夹具须 advice（启发式不进债桶）"


def test_out_fresh_mtime_passes(sandbox: Path, monkeypatch: pytest.MonkeyPatch):
    """F06 阴性：.out 晚于夹具 → 放行。"""
    monkeypatch.setattr(ge, "ROOT", sandbox)
    (sandbox / "_fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    (sandbox / "fx.out").write_text("x=1\n", encoding="utf-8")
    _write_card(sandbox, "EV-MEM-F6B.md", fixture="_fx.cpp",
              actual="\n  run_match_file: fx.out\n  run_match_keys: []")
    assert ge.check_evidence_out_stale_mtime() == [], "新鲜的 .out 不得 warn"


def test_fm_duplicate_key_blocked(sandbox: Path):
    """F09：双 verdict（refute+confirm）after-wins 遮蔽 → block。"""
    d = sandbox / "evidence" / "mem"
    d.mkdir(parents=True, exist_ok=True)
    (d / "EV-MEM-F9A.md").write_text(
        "---\nid: EV-MEM-F9A\nverdict: refute\nverdict: confirm\n"
        "hypothesis: h\nfalsification: f\n---\n", encoding="utf-8")
    who = [f.rule_id for f in ge.check_frontmatter_duplicate_key()]
    assert "EV-FM-DUP-KEY" in who, "重复 verdict 键必须拦"


def test_fm_unique_keys_pass(sandbox: Path):
    """F09 阴性：键唯一 → 放行。"""
    _write_card(sandbox, "EV-MEM-F9B.md")
    assert ge.check_frontmatter_duplicate_key() == [], "唯一键不得拦"
