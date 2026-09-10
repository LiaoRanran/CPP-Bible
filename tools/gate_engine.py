#!/usr/bin/env python3
"""门禁引擎（M4）：统一 Rule 接口 + 单一注册中心 + 四象限分流 + 可执行工单。

设计要点（ADR-0004 / ADR-0005）：
  * **不另起 CI**：`--gates` 把注册规则导出为 `(name, [cmd...])` 元组，供
    `cppbible.py:cmd_check` 现有执行循环消费；规则可注册、可插拔。
  * **收敛双清单**：`--manifest-check` 用 AST 解析 `cppbible.py` 的 quality 元组，
    与 `pyproject.toml:quality_gates` 比对，把"两份清单各自漂移"变成可拦项。
  * **四象限**：programmatic（机器可判，进 CI）· llm（语义判定，本轮不接模型 → 人工队列）·
    hybrid（机器初筛 + 人工裁定）· human（纯人工裁定）。
  * **三 severity**：block（阻断，exit 1）· warn（记债，报告但不红）· advice（教学/文学
    建议，**只建议不改文**——铁律）。

用法：
    python tools/gate_engine.py --list                     # 规则全集（含未自动化的象限）
    python tools/gate_engine.py --run                      # 执行 + 打印可执行工单
    python tools/gate_engine.py --run --advice             # 附带教学/文学建议
    python tools/gate_engine.py --run --json build/gate_report.json
    python tools/gate_engine.py --check                    # 任一 block 违规即 exit 1（CI 用）
    python tools/gate_engine.py --manifest-check           # 双清单一致性
    python tools/gate_engine.py --gates                    # 导出 cmd_check 元组
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay  # noqa: E402  复用 frontmatter 解析（单一实现）

ATOMS = ROOT / "atoms"
EVIDENCE = ROOT / "evidence"
PYPROJECT = ROOT / "pyproject.toml"
CPPBIBLE = ROOT / "tools/cppbible.py"

# 16 域（唯一来源：知识地图工具），用于校验原子 ID 中段与目录归属
from atom_coverage_map import DOMAIN_OF_PREFIX  # noqa: E402
DOMAINS = {v for v in DOMAIN_OF_PREFIX.values()}

ATOM_REQUIRED = ("id", "title", "domain", "type", "status", "claim", "claim_boundary",
                 "relations", "evidence", "sources", "first_hand", "superiority",
                 "depth", "pedagogy")
EV_REQUIRED = ("id", "serves", "hypothesis", "command", "fixture", "artifact",
               "artifact_sha256", "actual")
EV_KINDS = {"run", "asm", "layout", "abi", "symbol", "bench", "sanitizer", "godbolt",
            "traceable_argument"}
ATOM_TYPES = {"concept", "mechanism", "rule", "idiom", "anti_pattern", "pitfall",
              "contrast", "evolution", "decision", "experiment"}
DAG_REL = {"prerequisite", "specializes", "realizes", "evolved_from"}
BANNED_SUPERIORITY = ("讲解更详细", "更通俗易懂", "更全面", "更加深入", "帮助读者理解", "结合实际")
# 注意：「待补/待補」**不在**占位符之列 —— 在本项目它是**合法的缺口留痕**
# （证据卡 `## 待补`、M2「待确认」都是显式记账，不是未填内容），误报会逼人删掉真信息。
PLACEHOLDER_RE = re.compile(r"(TODO|TBD|FIXME|XXX|占位|placeholder)", re.I)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    target: str
    message: str
    fix_hint: str = ""


@dataclass(frozen=True)
class Rule:
    """统一规则接口：selector（scope）→ check → severity → message → fix_hint。"""

    id: str
    title: str
    kind: str                                  # fact | pedagogy | literature | meta
    quadrant: str                              # programmatic | llm | hybrid | human
    severity: str                              # block | warn | advice
    scope: str                                 # atom | evidence | repo
    check: Callable[[], list[Finding]] | None = None
    basis: str = ""                            # 教学/文学规则的"学习科学依据"（必填）
    fix_hint: str = ""
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def automated(self) -> bool:
        return self.check is not None


RULES: list[Rule] = []


def register(rule: Rule) -> Rule:
    if any(r.id == rule.id for r in RULES):
        raise ValueError(f"规则 ID 重复：{rule.id}")
    if rule.kind in ("pedagogy", "literature") and not rule.basis:
        raise ValueError(f"教学/文学规则必须标注学习科学依据：{rule.id}")
    RULES.append(rule)
    return rule


# ── 扫描与解析 ────────────────────────────────────────────────────────────
def _cards(root: Path, pattern: str) -> list[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.rglob(pattern) if not p.name.startswith("README"))


def _meta(p: Path) -> dict[str, Any]:
    try:
        return replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return {}


def _rel(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def _as_list(v: Any) -> list[Any]:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# ── FACT 规则（程序化）────────────────────────────────────────────────────
def check_atom_frontmatter() -> list[Finding]:
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        # 只判「字段是否存在」；空列表（relations/evidence 在 draft 期合法）不算缺失
        missing = [k for k in ATOM_REQUIRED if meta.get(k) in (None, "")]
        if not _as_list(meta.get("sources")):
            missing.append("sources[]（多源精炼要求 ≥1 个来源）")
        if missing:
            out.append(Finding("ATOM-FM-REQUIRED", "block", _rel(p),
                               f"原子卡缺必填字段：{', '.join(missing)}",
                               "按 docs/kernel/G1_layout.md §3 字段标准补齐"))
    return out


def check_atom_id_format() -> list[Finding]:
    out: list[Finding] = []
    pat = re.compile(r"^ATOM-([A-Z]+)-([A-Z0-9]+)-(\d{3})$")
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        aid = str(meta.get("id") or p.stem)
        m = pat.match(aid)
        if not m:
            out.append(Finding("ATOM-ID-FORMAT", "block", _rel(p),
                               f"ID 不合规：{aid}（应为 ATOM-{{DOMAIN}}-{{TOPIC}}-{{NNN}}）",
                               "改名并同步 atoms/id_migrations.json（入库后 ID 永久不变）"))
            continue
        dom, typ = m.group(1), str(meta.get("type") or "")
        if dom not in DOMAINS:
            out.append(Finding("ATOM-ID-FORMAT", "block", _rel(p),
                               f"ID 域 {dom} 不在 16 域内", "见 G1_knowledge_map.md §2"))
        elif p.parent.name.upper() != dom:
            out.append(Finding("ATOM-ID-FORMAT", "block", _rel(p),
                               f"目录 {p.parent.name}/ 与 ID 域 {dom} 不一致",
                               f"移入 atoms/{dom.lower()}/ 或改 ID"))
        if typ and typ not in ATOM_TYPES:
            out.append(Finding("ATOM-ID-FORMAT", "block", _rel(p),
                               f"type={typ} 不在 10 类原子类型内",
                               "见 M1_ontology.md §2"))
    return out


def check_verified_bound() -> list[Finding]:
    """G1_layout 硬约束：status=verified ⟹ evidence 非空 ∧ first_hand ∧ superiority 非空。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        if str(meta.get("status")) != "verified":
            continue
        gaps = []
        if not _as_list(meta.get("evidence")):
            gaps.append("evidence[] 为空")
        if meta.get("first_hand") is not True:
            gaps.append("first_hand 非 true")
        if not str(meta.get("superiority") or "").strip():
            gaps.append("superiority 为空")
        if gaps:
            out.append(Finding("ATOM-VERIFIED-BOUND", "block", _rel(p),
                               "status=verified 但 " + "；".join(gaps),
                               "补证据或降级 status=draft（S2 声明-证据绑定）"))
    return out


def check_no_unverified_status() -> list[Finding]:
    """DRQ-4 红线：新体系原子不得停留在 unverified/UNVERIFIED。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        st = str(_meta(p).get("status") or "").lower()
        if "unverified" in st or "needs" in st:
            out.append(Finding("ATOM-NO-UNVERIFIED", "block", _rel(p),
                               f"status={st} 违规（新原子禁未验证）",
                               "完成验证置 verified，或标 draft/rejected"))
    return out


def check_relations_target_exists() -> list[Finding]:
    ids = {str(_meta(p).get("id") or p.stem) for p in _cards(ATOMS, "ATOM-*.md")}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        for rel in _as_list(_meta(p).get("relations")):
            if isinstance(rel, dict):
                tgt = str(rel.get("target") or "")
                if tgt and tgt not in ids:
                    out.append(Finding("ATOM-REL-TARGET", "warn", _rel(p),
                                       f"关系目标不存在：{tgt}",
                                       "补目标原子或改用已存在 ID（尚未锻造的先记债）"))
    return out


def check_relations_dag() -> list[Finding]:
    """DAG 关系（prerequisite/specializes/realizes/evolved_from）必须无环。"""
    graph: dict[str, list[str]] = {}
    owner: dict[str, Path] = {}
    for p in _cards(ATOMS, "ATOM-*.md"):
        aid = str(_meta(p).get("id") or p.stem)
        owner[aid] = p
        edges = []
        for rel in _as_list(_meta(p).get("relations")):
            if isinstance(rel, dict) and str(rel.get("type")) in DAG_REL:
                edges.append(str(rel.get("target") or ""))
        graph[aid] = [e for e in edges if e]

    out: list[Finding] = []
    color: dict[str, int] = {}

    def dfs(node: str, stack: list[str]) -> None:
        color[node] = 1
        for nxt in graph.get(node, []):
            if color.get(nxt) == 1:
                cyc = " → ".join([*stack, node, nxt])
                out.append(Finding("ATOM-REL-DAG", "block", _rel(owner.get(nxt, ROOT / "atoms")),
                                   f"学习路径 DAG 出现环：{cyc}",
                                   "拆分或调整 prerequisite 方向（环路=内容切分有问题）"))
            elif color.get(nxt, 0) == 0 and nxt in graph:
                dfs(nxt, [*stack, node])
        color[node] = 2

    for n in list(graph):
        if color.get(n, 0) == 0:
            dfs(n, [])
    return out


def check_superiority_banned_words() -> list[Finding]:
    """M3 §4 禁词表：零信息增量的 superiority 表述 → 打回。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        text = str(_meta(p).get("superiority") or "")
        hit = [w for w in BANNED_SUPERIORITY if w in text]
        if hit:
            out.append(Finding("ATOM-SUPERIORITY-WORDS", "block", _rel(p),
                               f"superiority 命中禁词：{', '.join(hit)}",
                               "改写成可验证增量（多给了哪个实验/汇编/反例/数字/边界）"))
    return out


def check_evidence_frontmatter() -> list[Finding]:
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        missing = [k for k in EV_REQUIRED if meta.get(k) in (None, "")]
        actual = meta.get("actual") or {}
        if isinstance(actual, dict) and not any(k.startswith("run") for k in actual):
            missing.append("actual.run_*")
        if missing:
            out.append(Finding("EV-FM-REQUIRED", "block", _rel(p),
                               f"证据卡缺必填字段：{', '.join(missing)}",
                               "按 M2 §1 实验卡字段补齐"))
        kind = str(meta.get("kind") or "")
        if kind and kind not in EV_KINDS:
            out.append(Finding("EV-KIND-ENUM", "block", _rel(p),
                               f"kind={kind} 不在枚举内", f"取值：{sorted(EV_KINDS)}"))
    return out


def check_evidence_falsification() -> list[Finding]:
    """M2 §3 证伪导向：每个论断必须配一个「让它失败」的对照，只演示成立=恒真测试。"""
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        if not str(_meta(p).get("falsification") or "").strip():
            out.append(Finding("EV-FALSIFICATION", "block", _rel(p),
                               "缺 falsification（证伪对照）",
                               "补上「让它失败的实验」及其结果（M2 §3）"))
    return out


def check_evidence_matrix() -> list[Finding]:
    """版本矩阵：matrix 必须写清 compiler/std/opt（M2 §2 两档与选取规则）。"""
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        mx = _meta(p).get("matrix")
        if not isinstance(mx, dict):
            out.append(Finding("EV-MATRIX", "block", _rel(p),
                               "matrix 缺失或非映射",
                               "按 M2 §1 写 {compiler, std, opt, arch}"))
            continue
        miss = [k for k in ("compiler", "std", "opt") if not mx.get(k)]
        if miss:
            out.append(Finding("EV-MATRIX", "block", _rel(p),
                               f"matrix 缺 {'/'.join(miss)}",
                               "补齐后证据才可跨版本复算"))
    return out


def check_atom_gray_zone() -> list[Finding]:
    """灰色地带标注：UB 域原子必须声明五类归属（M2 §7 决策树）。"""
    gray = {"defined", "unspecified", "implementation_defined", "ub", "abi_dependent"}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        if str(meta.get("domain")) != "UB":
            continue
        got = str(meta.get("gray_zone") or "")
        if got not in gray:
            out.append(Finding("ATOM-GRAY-ZONE", "block", _rel(p),
                               f"UB 域原子须标 gray_zone（当前：{got or '空'}）",
                               f"取值 {sorted(gray)}（M2 §7 判定流程）"))
    return out


# ── 制衡层 S1/S2/S3（机器可判定部分；S4/S5/S6 为独立工具）──────────────────
def check_s1_human_signoff() -> list[Finding]:
    """S1 三权分立：Agent 无权定 golden —— verified 必须带人工签收。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        if str(meta.get("status")) != "verified":
            continue
        by = str(meta.get("verified_by") or "")
        if not by.startswith("human:"):
            out.append(Finding("S1-AUTHOR-SELF-VERIFY", "block", _rel(p),
                               "status=verified 但缺 verified_by: human:*（Agent 无权自证）",
                               "由人复核后写入 verified_by / verified_at"))
    return out


def check_s2_evidence_verdict() -> list[Finding]:
    """S2 声明-证据绑定：verified 原子引用的证据必须 verdict=confirm（作者自述无效）。"""
    verdicts = {str(_meta(p).get("id") or p.stem): str(_meta(p).get("verdict") or "")
                for p in _cards(EVIDENCE, "EV-*.md")}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        if str(_meta(p).get("status")) != "verified":
            continue
        for ev in _as_list(_meta(p).get("evidence")):
            key = str(ev)
            v = verdicts.get(key)
            if v is None:
                out.append(Finding("S2-EVIDENCE-VERDICT", "block", _rel(p),
                                   f"引用的证据卡不存在：{key}",
                                   "补卡或改引用（不许引用不存在的证据）"))
            elif v != "confirm":
                out.append(Finding("S2-EVIDENCE-VERDICT", "block", _rel(p),
                                   f"证据 {key} verdict={v or '空'}（verified 只能绑 confirm）",
                                   "证据被 refute 时原子必须回到 draft"))
    return out


def check_s3_hardcoded_expected() -> list[Finding]:
    """S3 伪证据检测：期望输出**硬编码进夹具字符串字面量**（打印常量冒充观测）→ 作弊级阻断。

    只查字符串字面量：`//@ 注释`与 printf 的 %ld 格式串都不含"带实测数字"的片段，不误报。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        fixture = meta.get("fixture")
        actual = meta.get("actual")
        if not fixture or not isinstance(actual, dict):
            continue
        fx = ROOT / str(fixture)
        if not fx.is_file():
            continue
        src = fx.read_text(encoding="utf-8", errors="replace")
        literals = [m.group(1) for m in re.finditer(r'"([^"\n]*)"', src)]
        for v in actual.values():
            for seg in (t.strip() for t in str(v).split("|")):
                if len(seg) >= 6 and any(seg in lit for lit in literals):
                    out.append(Finding("S3-EXPECTED-HARDCODED", "block", _rel(p),
                                       f"期望片段被硬编码进夹具字面量：{seg[:40]!r}",
                                       "观测必须来自运行时（计数器/输出），打印常量=伪证据"))
                    break
    return out


def check_evidence_serves_exist() -> list[Finding]:
    """证据服务的原子应存在（G4 前原子未锻造 → warn，不阻断）。"""
    ids = {str(_meta(p).get("id") or p.stem) for p in _cards(ATOMS, "ATOM-*.md")}
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        for tgt in _as_list(_meta(p).get("serves")):
            if str(tgt) and str(tgt) not in ids:
                out.append(Finding("EV-SERVES-EXIST", "warn", _rel(p),
                                   f"服务的原子尚未锻造：{tgt}",
                                   "G4 锻造该原子后此债自动清零"))
    return out


def check_zero_placeholder() -> list[Finding]:
    """新体系（atoms/ + evidence/）零占位符；Book 存量债不在此列（避免一波爆量）。"""
    out: list[Finding] = []
    for root in (ATOMS, EVIDENCE):
        for p in root.rglob("*.md") if root.exists() else []:
            if p.name.startswith("README"):
                continue
            for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace")
                                   .split("\n"), 1):
                m = PLACEHOLDER_RE.search(ln)
                if m:
                    out.append(Finding("DOC-ZERO-PLACEHOLDER", "block", f"{_rel(p)}:{i}",
                                       f"占位符 {m.group(1)}", "补齐内容或删除该行"))
    return out


# ── 教学 / 文学规则（advice：只建议不改文，须标学习科学依据）──────────────
def _pedagogy_gap(field_name: str, rule_id: str, message: str) -> Callable[[], list[Finding]]:
    def _check() -> list[Finding]:
        out: list[Finding] = []
        for p in _cards(ATOMS, "ATOM-*.md"):
            ped = _meta(p).get("pedagogy") or {}
            if isinstance(ped, dict) and not _as_list(ped.get(field_name)):
                out.append(Finding(rule_id, "advice", _rel(p), message,
                                   "教学封装缺项——补写后再进正文"))
        return out
    return _check


# ── META：双清单一致性（ADR-0004）──────────────────────────────────────────
def _cmd_check_quality_gates() -> list[str] | None:
    """AST 解析 cppbible.py 的 quality 元组 → ['tools/x.py --flag', ...]。"""
    if not CPPBIBLE.is_file():
        return None
    tree = ast.parse(CPPBIBLE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        test = getattr(node, "test", None)
        if not (isinstance(node, ast.If) and isinstance(test, ast.Compare)
                and test.comparators
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "quality"):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assign) and any(
                    getattr(t, "id", "") == "gates" for t in sub.targets):
                out: list[str] = []
                for elt in getattr(sub.value, "elts", []):
                    if isinstance(elt, ast.Tuple) and len(elt.elts) == 2:
                        args = elt.elts[1]
                        parts = [a.value for a in getattr(args, "elts", [])
                                 if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                        if parts:
                            out.append(" ".join(parts))
                return out
    return None


def check_manifest_consistency() -> list[Finding]:
    exec_list = _cmd_check_quality_gates()
    if exec_list is None:
        return [Finding("META-MANIFEST", "warn", "tools/cppbible.py",
                        "未能解析 quality 元组（AST 结构变了？）", "检查 cmd_check 实现")]
    declared: list[str] = []
    text = PYPROJECT.read_text(encoding="utf-8")
    m = re.search(r"quality_gates\s*=\s*\[(.*?)\]", text, re.S)
    if m:
        declared = re.findall(r'"([^"]+)"', m.group(1))
    out: list[Finding] = []
    for cmd in exec_list:
        if cmd not in declared:
            out.append(Finding("META-MANIFEST", "warn", "pyproject.toml",
                               f"执行器有但清单缺：{cmd}",
                               "补进 pyproject:quality_gates（收敛双清单，ADR-0004）"))
    for cmd in declared:
        if cmd not in exec_list:
            out.append(Finding("META-MANIFEST", "warn", "tools/cppbible.py",
                               f"清单有但执行器缺：{cmd}",
                               "补进 cmd_check 元组或从清单删除"))
    return out


# ── 注册中心（规则全集）────────────────────────────────────────────────────
def _register_all() -> None:
    fact = [
        ("ATOM-FM-REQUIRED", "原子卡必填字段完整", "atom", check_atom_frontmatter),
        ("ATOM-ID-FORMAT", "原子 ID 格式/域/目录一致", "atom", check_atom_id_format),
        ("ATOM-VERIFIED-BOUND", "verified ⟹ 证据+一手+superiority", "atom",
         check_verified_bound),
        ("ATOM-NO-UNVERIFIED", "新原子禁未验证状态", "atom", check_no_unverified_status),
        ("ATOM-REL-TARGET", "关系目标存在", "atom", check_relations_target_exists),
        ("ATOM-REL-DAG", "学习路径 DAG 无环", "atom", check_relations_dag),
        ("ATOM-SUPERIORITY-WORDS", "superiority 禁词表", "atom",
         check_superiority_banned_words),
        ("EV-FM-REQUIRED", "证据卡必填字段完整", "evidence", check_evidence_frontmatter),
        ("EV-FALSIFICATION", "证伪对照存在（非恒真测试）", "evidence",
         check_evidence_falsification),
        ("EV-MATRIX", "版本矩阵字段完整", "evidence", check_evidence_matrix),
        ("ATOM-GRAY-ZONE", "UB 域原子标注灰色地带类别", "atom", check_atom_gray_zone),
        ("EV-SERVES-EXIST", "证据服务的原子存在", "evidence", check_evidence_serves_exist),
        ("DOC-ZERO-PLACEHOLDER", "新体系零占位符", "repo", check_zero_placeholder),
        ("META-MANIFEST", "双清单一致（ADR-0004）", "repo", check_manifest_consistency),
        ("S1-AUTHOR-SELF-VERIFY", "verified 须人工签收（Agent 无权定 golden）", "atom",
         check_s1_human_signoff),
        ("S2-EVIDENCE-VERDICT", "verified 只绑 verdict=confirm 的证据", "atom",
         check_s2_evidence_verdict),
        ("S3-EXPECTED-HARDCODED", "期望硬编码进夹具=伪证据", "evidence",
         check_s3_hardcoded_expected),
    ]
    sev = {"ATOM-REL-TARGET": "warn", "EV-SERVES-EXIST": "warn",
           "META-MANIFEST": "warn"}
    for rid, title, scope, fn in fact:
        register(Rule(rid, title, "fact", "programmatic", sev.get(rid, "block"), scope,
                      check=fn))

    # 教学/文学门禁（advice：只建议不改文；basis = 学习科学依据）
    register(Rule("PED-MOTIVATION", "动机先行：先说清为什么需要", "pedagogy",
                  "programmatic", "advice", "atom",
                  check=_pedagogy_gap("motivation", "PED-MOTIVATION", "缺 motivation"),
                  basis="Merrill 首要教学原理：以问题/需求激活先备经验"))
    register(Rule("PED-MISCONCEPTION", "学习者常见误解清单", "pedagogy",
                  "programmatic", "advice", "atom",
                  check=_pedagogy_gap("misconception", "PED-MISCONCEPTION",
                                      "缺 misconception 清单"),
                  basis="认知冲突/反驳性文本（refutation text）：先显化误解再纠正"))
    register(Rule("PED-SOCRATIC", "苏格拉底提问链", "pedagogy",
                  "programmatic", "advice", "atom",
                  check=_pedagogy_gap("socratic", "PED-SOCRATIC", "缺 socratic 提问链"),
                  basis="自我解释效应：追问迫使学习者生成推理"))
    register(Rule("PED-PREDICT-FIRST", "先预测后揭示（生成性学习）", "pedagogy",
                  "programmatic", "advice", "atom",
                  check=_pedagogy_gap("predict_first", "PED-PREDICT-FIRST",
                                      "缺 predict_first"),
                  basis="生成性学习/预测试效应：先产出再对照，记忆保持显著提升"))

    # 非程序化象限：登记在册、进人工队列（DRQ-5：本轮不接 LLM）
    register(Rule("LLM-SUPERIORITY-QUALITY", "superiority 是否真有洞见", "fact",
                  "llm", "advice", "atom",
                  basis="", fix_hint="人工/未来模型评审：红队通道"))
    register(Rule("HYBRID-TEACHING-DEPTH", "教学深度初筛 + 人工裁定", "pedagogy",
                  "hybrid", "advice", "atom", basis="费曼 rubric 人工判定（机器只做初筛）"))
    register(Rule("HUMAN-GOLDEN-REVIEW", "Golden 样板人审", "meta", "human", "advice",
                  "repo", basis="G4 门：认可权唯人（规程 0.1）"))


_register_all()


# ── 执行与报告 ────────────────────────────────────────────────────────────
def run(include_advice: bool = False) -> list[Finding]:
    out: list[Finding] = []
    for r in RULES:
        if not r.automated:
            continue
        if r.severity == "advice" and not include_advice:
            continue
        out.extend(r.check() if r.check else [])
    return out


def report(findings: Sequence[Finding], total_rules: int) -> str:
    by_sev: dict[str, int] = {}
    for f in findings:
        by_sev[f.severity] = by_sev.get(f.severity, 0) + 1
    lines = [f"[gate] 规则 {total_rules} 条 · 命中 {len(findings)} "
             f"(block={by_sev.get('block', 0)} warn={by_sev.get('warn', 0)} "
             f"advice={by_sev.get('advice', 0)})"]
    for f in sorted(findings, key=lambda x: (x.severity != "block", x.rule_id, x.target)):
        lines.append(f"  [{f.severity.upper():6}] {f.rule_id}  {f.target}")
        lines.append(f"           {f.message}")
        if f.fix_hint:
            lines.append(f"           ↳ {f.fix_hint}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="门禁引擎 M4（统一 Rule 接口 + 工单）")
    ap.add_argument("--list", action="store_true", help="列出规则全集")
    ap.add_argument("--run", action="store_true", help="执行并打印工单")
    ap.add_argument("--advice", action="store_true", help="附带教学/文学建议（只建议不改文）")
    ap.add_argument("--json", dest="json_path", help="工单落盘（JSON）")
    ap.add_argument("--check", action="store_true", help="任一 block 违规即 exit 1")
    ap.add_argument("--manifest-check", action="store_true", help="仅校验双清单一致性")
    ap.add_argument("--gates", action="store_true", help="导出 cmd_check 元组")
    a = ap.parse_args(argv)

    if a.gates:
        auto = [r for r in RULES if r.automated and r.quadrant == "programmatic"]
        print("# 按 ADR-0004：规则引擎作为**单个 gate** 注入 cmd_check（规则粒度在引擎内聚合）")
        print('            ("Gate Engine", [PYTHON_EXE, "tools/gate_engine.py", "--check"]),')
        print(f"# 当前覆盖 programmatic 规则 {len(auto)} 条："
              + ", ".join(r.id for r in auto))
        return 0
    if a.list:
        print(f"{'ID':30} {'KIND':10} {'QUADRANT':13} {'SEVERITY':9} AUTO TITLE")
        for r in RULES:
            print(f"{r.id:30} {r.kind:10} {r.quadrant:13} {r.severity:9} "
                  f"{'Y' if r.automated else '-':4} {r.title}")
        return 0
    if a.manifest_check:
        findings = check_manifest_consistency()
        print(report(findings, 1))
        return 1 if findings else 0

    findings = run(include_advice=a.advice or not a.check)
    # 门禁语义：--check 只按 block 计红；报告始终打印 warn/advice
    print(report(findings, len(RULES)))
    if a.json_path:
        Path(a.json_path).write_text(json.dumps(
            {"findings": [f.__dict__ for f in findings],
             "rules": len(RULES)}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[gate] 工单 → {a.json_path}")
    if a.check:
        return 1 if any(f.severity == "block" for f in findings) else 0
    return 0


PYTHON_EXE = sys.executable    # 与 cppbible 侧 PYTHON_EXE 语义一致（--gates 输出用）

if __name__ == "__main__":
    raise SystemExit(main())
