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

# ── G5 新增：全局误解库 + 认知适切维度 ──────────────────────────────────────
MISCONCEPTIONS = ROOT / "misconceptions"
AUDIENCES = {"beginner", "intermediate", "expert"}
COGNITIVE_LOADS = {"low", "medium", "high"}
# beginner 原子须给直觉入口：正文里应能找到类比/直觉类表述，而不是只有形式化定义
ANALOGY_RE = re.compile(r"(类比|直觉|打个比方|好比|就像|想象一下|可以理解为)")

# ── G6 四级状态 + 失效后果分级 DAL（2026-09-12，References/300 落地）──────────
# 状态链：draft → machine-verified → red-team-verified → human-verified
#   `verified` = 四级体系启用前的历史取值，语义等价 human-verified（兼容别名，存量沿用）
# 三条防"放权变降标"的铁律（缺一条则放权 = 静默降标）：
#   ① **判断单点化**：任何"是否已验证"必须走 is_verified()/level_of()，禁止散落
#      `status == "verified"` —— 新枚举会让写死比较**静默跳过**（不报错、不拦截）。
#   ② **人级须有非人级前驱**：人只能签"已被机器验过"的东西；链中必须含 machine 或
#      red-team 级，否则 draft 直签人级 = 未验证内容入库。
#   ③ **免人审本身必须人签**：DAL C/D/E 意味着豁免人审，这是放权决定而非写作决定，
#      须 `dal_reviewed_by: human:*`；否则 Writer 自填 `dal: C` 即可绕过人审（权力反转）。
ATOM_STATUSES = ("draft", "machine-verified", "red-team-verified", "human-verified",
                 "verified", "rejected")
HUMAN_STATUSES = ("human-verified", "verified")
VERIFIED_STATUSES = ("machine-verified", "red-team-verified") + HUMAN_STATUSES
STATUS_LEVEL = {"draft": 0, "machine-verified": 1, "red-team-verified": 2,
                "human-verified": 3, "verified": 3}
LEVEL_PRINCIPALS = {"draft": (), "machine-verified": ("machine:",),
                    "red-team-verified": ("redteam:",),
                    "human-verified": ("human:",), "verified": ("human:",)}
DAL_LEVELS = ("A", "B", "C", "D", "E")
DAL_HUMAN_REVIEW = ("A", "B")     # 必须人审签署；C/D/E 红队通过即可（须人签豁免）
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def level_of(meta: dict[str, Any]) -> int | None:
    """状态级别序数（draft=0 / machine=1 / red-team=2 / human=3）；枚举外 → None。"""
    return STATUS_LEVEL.get(str(meta.get("status") or "").strip().lower())


def is_verified(meta: dict[str, Any]) -> bool:
    """是否属「已验证」三级（机器 / 红队 / 人）——**唯一判断点**。

    散落的 `status == "verified"` 在新枚举下会静默跳过（不报错、不拦截），
    等于把 S1/S2/证据边界三条硬约束一起关掉。新增状态一律改这里。
    """
    return str(meta.get("status") or "").strip().lower() in VERIFIED_STATUSES


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


def check_atom_id_unique() -> list[Finding]:
    """原子身份唯一：文件 stem 必须等于 frontmatter.id，且 id 全库唯一。

    为什么是 block（369 任务3，P1-5）：下游多处按 id 建 dict（证据绑定 / 关系解析 /
    status 迁移 / 去重），id 重复时**后者静默覆盖前者**——复制一张卡不改 id 即产生
    "双份 verified"，而其余规则各自只看单卡，谁都不报。
    """
    out: list[Finding] = []
    owner: dict[str, Path] = {}
    for p in _cards(ATOMS, "ATOM-*.md"):
        aid = str(_meta(p).get("id") or "").strip()
        if not aid:
            continue        # 缺 id 由 ATOM-FM-REQUIRED / ATOM-ID-FORMAT 承担
        if p.stem != aid:
            out.append(Finding("ATOM-ID-UNIQUE", "block", _rel(p),
                               f"文件名 stem（{p.stem}）≠ frontmatter.id（{aid}）",
                               "改名文件与 id 对齐——ID 是身份，两者必须同源"))
        if aid in owner:
            out.append(Finding("ATOM-ID-UNIQUE", "block", _rel(p),
                               f"ID 与 {_rel(owner[aid])} 重复（{aid}）",
                               "改 id 或合并——id 重复会让 dict-by-id 的下游静默覆盖"))
        else:
            owner[aid] = p
    return out


def check_verified_bound() -> list[Finding]:
    """G1_layout 硬约束：status 属已验证三级 ⟹ evidence 非空 ∧ first_hand ∧ superiority。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        if not is_verified(meta):
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
                               f"status={meta.get('status')} 但 " + "；".join(gaps),
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


def check_status_value() -> list[Finding]:
    """status 必须是四级体系枚举内取值（枚举外 = 检查会静默漏过，故显式拦）。"""
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        st = str(meta.get("status") or "").strip()
        if st and st.lower() not in ATOM_STATUSES:
            out.append(Finding("ATOM-STATUS-VALUE", "block", _rel(p),
                               f"status 非法：{st}",
                               "取值 " + " / ".join(ATOM_STATUSES)))
    return out


def check_status_transition() -> list[Finding]:
    """状态跃迁可证：非 draft/rejected 的原子必须带合法 `status_history` 链。

    校验（全部机器可判）：
      * 链首 = draft；级别单调不减；链尾 = 当前 status；
      * `at` 为 ISO 日期、`by` 前缀与该级执行者匹配（machine:* / redteam:* / human:*）；
      * **人级必须链上含非人级前驱**（人只能签已被机器或红队验过的东西）。

    不强制逐级（draft→machine→red-team→human 每步 +1）：逐级对历史原子不可回溯，
    硬要求只会逼人**编造**红队记录——规则若要求机器无法核实的历史，就是在生产假记录。
    因此只拦风险实质：绕过全部非人级检查直接由人签字。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        st = str(meta.get("status") or "").strip().lower()
        if st not in STATUS_LEVEL:
            continue                                    # 枚举外 → ATOM-STATUS-VALUE 管
        hist = _as_list(meta.get("status_history"))
        if not hist:
            if STATUS_LEVEL[st] > 0:
                out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                                   f"status={st} 但无 status_history（晋升路径不可证）",
                                   "补 status_history: [{level, at, by}]，链尾=当前状态"))
            continue
        steps: list[tuple[int, str]] = []
        bad: list[str] = []
        for h in hist:
            if not isinstance(h, dict):
                bad.append("存在非结构化项（须 {level, at, by}）")
                continue
            lv = str(h.get("level") or "").strip().lower()
            if lv not in STATUS_LEVEL:
                bad.append(f"level 非法：{lv or '空'}")
                continue
            at, by = str(h.get("at") or "").strip(), str(h.get("by") or "").strip()
            # `at: legacy` 仅限 draft 级：起草时间未留记录是历史事实，逼填日期 = 逼造数据
            if at == "legacy" and lv != "draft":
                bad.append(f"{lv} 不得用 at: legacy（该级须有真实签署日期）")
            elif at != "legacy" and not DATE_RE.match(at):
                bad.append(f"{lv} 的 at 须为 ISO 日期或 draft 级 legacy：{at or '空'}")
            need = LEVEL_PRINCIPALS.get(lv, ())
            if need and not by.startswith(need):
                bad.append(f"{lv} 的 by 前缀应为 {'/'.join(need)}（当前：{by or '空'}）")
            elif not need and not by:
                bad.append(f"{lv} 缺 by")
            steps.append((STATUS_LEVEL[lv], lv))
        if bad:
            out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                               "status_history 不合法：" + "；".join(bad),
                               "按 docs/kernel/G6_status_levels.md §2 修链"))
            continue
        levels = [lv for lv, _ in steps]
        if levels[0] != 0:
            out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                               f"status_history 链首必须是 draft（当前：{steps[0][1]}）",
                               "链首补 {level: draft, at: …, by: writer:…}"))
        elif any(b < a for a, b in zip(levels, levels[1:])):
            out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                               f"status_history 级别回退未留痕：{[s[1] for s in steps]}",
                               "回退须在链尾追加低级别步骤（保留历史，不删记录）"))
        elif levels[-1] != STATUS_LEVEL[st]:
            out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                               f"status_history 链尾({steps[-1][1]}) ≠ status({st})",
                               "链尾须等于当前状态"))
        # 必须是 machine(1)/red-team(2) 级**具体存在**，不是"级别 ≥1"——否则
        # draft→human 这种 0→3 的直签会被 level>=1 误判成合规（0→3 里 3 也 ≥1）
        elif st in HUMAN_STATUSES and not any(lv in (1, 2) for lv in levels):
            out.append(Finding("ATOM-STATUS-TRANSITION", "block", _rel(p),
                               "人级签署但链上无 machine/red-team 级（未过机器验证即签）",
                               "先过门禁晋升 machine-verified / 红队晋升 red-team-verified"))
    return out


def check_dal_match() -> list[Finding]:
    """失效后果分级（DAL）与人审要求一致（G6，References/300 §3）。

    * 已入库原子必须有 `dal ∈ A–E`；
    * DAL A/B ⟹ `human_review: required` 且状态必须是人级；
    * DAL C/D/E ⟹ 豁免人审，但**豁免决定须人签** `dal_reviewed_by: human:*`
      （否则 Writer 自填 `dal: C` 即可绕过人审 = 放权变权力反转）。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        if not is_verified(meta):
            continue                                    # 草稿期不要求分级
        dal = str(meta.get("dal") or "").strip().upper()
        if dal not in DAL_LEVELS:
            out.append(Finding("ATOM-DAL-MATCH", "block", _rel(p),
                               f"已入库原子缺合法 dal（当前：{dal or '空'}）",
                               "标 A–E + human_review；C/D/E 须 human:* 签 dal_reviewed_by"))
            continue
        hr = str(meta.get("human_review") or "").strip().lower()
        st = str(meta.get("status") or "").strip().lower()
        if dal in DAL_HUMAN_REVIEW:
            if hr != "required":
                out.append(Finding("ATOM-DAL-MATCH", "block", _rel(p),
                                   f"DAL {dal} 须 human_review: required（当前：{hr or '空'}）",
                                   "A/B 级失效后果必须人审签署"))
            if st not in HUMAN_STATUSES:
                out.append(Finding("ATOM-DAL-MATCH", "block", _rel(p),
                                   f"DAL {dal} 须 human-verified（当前：{st}）",
                                   "先人审签署再入库，或人签下调 DAL"))
        elif not str(meta.get("dal_reviewed_by") or "").strip().startswith("human:"):
            out.append(Finding("ATOM-DAL-MATCH", "block", _rel(p),
                               f"DAL {dal} 豁免人审但无 dal_reviewed_by: human:*",
                               "豁免人审是放权决定：须人签（同批可一次签分级表）"))
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


def check_misconception_levels() -> list[Finding]:
    """教学封装：误解必须**分层标注** surface/deep，deep 类须 ≥2 个独立反例。

    依据（2026-09-10 调研核心结论）：surface 误解一次纠正即可；deep 是结构性误解，
    不给足 ≥2 个独立反例纠不过来。故 `misconception[]` 是结构化项而非字符串列表：
    `{level: surface|deep, text: ..., refutations: [EV-…]}（deep 必填 ≥2）`。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        ped = _meta(p).get("pedagogy") or {}
        if not isinstance(ped, dict):
            continue
        for item in _as_list(ped.get("misconception")):
            if not isinstance(item, dict):
                out.append(Finding("ATOM-MISCONCEPTION-LEVELS", "block", _rel(p),
                                   f"误解项不是结构化字段（缺 level/text）：{str(item)[:40]!r}",
                                   "写成 {level: surface|deep, text: ...}（见 G1_layout §3）"))
                continue
            lvl = str(item.get("level") or "")
            if lvl not in ("surface", "deep"):
                out.append(Finding("ATOM-MISCONCEPTION-LEVELS", "block", _rel(p),
                                   f"误解层非法或缺失：{lvl or '空'}（应 surface|deep）",
                                   "surface=一次纠正即可；deep=结构性误解"))
            elif lvl == "deep" and len(_as_list(item.get("refutations"))) < 2:
                out.append(Finding("ATOM-MISCONCEPTION-LEVELS", "block", _rel(p),
                                   f"deep 类误解反例不足（{len(_as_list(item.get('refutations')))}/2）",
                                   "补 refutations[]（≥2 个独立反例，指向证据卡 ID）"))
    return out


def _mis_ids() -> set[str]:
    return {str(_meta(p).get("id") or "") for p in _cards(MISCONCEPTIONS, "MIS-*.md")}


def check_mis_library() -> list[Finding]:
    """误解库自身合规：字段齐全 · level 合法 · **deep 类 refutations ≥2** · 有出处。

    为什么单列：误解库是 G5 大规模生产的前置资产——1300 个原子都要引用它，
    条目本身写歪（level 乱标、deep 只有 1 条反例）会污染全库。故库与原子**双向**校验。
    """
    out: list[Finding] = []
    for p in _cards(MISCONCEPTIONS, "MIS-*.md"):
        meta = _meta(p)
        if not str(meta.get("id") or ""):
            out.append(Finding("MIS-LIBRARY", "block", _rel(p), "缺 id",
                               "补 id: MIS-{域}-{序号}"))
        if not str(meta.get("name") or ""):
            out.append(Finding("MIS-LIBRARY", "block", _rel(p), "缺 name",
                               "name 必须是**错误说法本身**，不是正确结论或元描述"))
        lvl = str(meta.get("level") or "")
        if lvl not in ("surface", "deep"):
            out.append(Finding("MIS-LIBRARY", "block", _rel(p),
                               f"level 非法或缺失：{lvl or '空'}（应 surface|deep）",
                               "surface=一次纠正即可；deep=结构性误解"))
        elif lvl == "deep" and len(_as_list(meta.get("refutations"))) < 2:
            out.append(Finding("MIS-LIBRARY", "block", _rel(p),
                               f"deep 类反例不足（{len(_as_list(meta.get('refutations')))}/2）",
                               "补 ≥2 条**独立**反例，且从不同角度打（标准怎么说 / 实测后果）"))
        if not str(meta.get("source") or ""):
            out.append(Finding("MIS-LIBRARY", "warn", _rel(p), "缺 source（出处）",
                               "填 Book 章节或三样板，保证每条可回溯、不是凭空编的"))
    return out


def check_misconception_ref() -> list[Finding]:
    """原子引用的误解 ID 必须存在（G5：误解抽成全局库，原子只引用 ID）。

    为什么是 block：引用不存在的 ID 等于"引用了一个不存在的反例"——教学封装那一项
    实际是空的，却又通过了五重剖面检查。
    """
    known = _mis_ids()
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        ped = _meta(p).get("pedagogy") or {}
        if not isinstance(ped, dict):
            continue
        for mid in _as_list(ped.get("misconceptions")):
            if str(mid) not in known:
                out.append(Finding("ATOM-MISCONCEPTION-REF", "block", _rel(p),
                                   f"引用的误解 ID 不存在：{mid}",
                                   "先在 misconceptions/ 建该条，或改用已有 ID"))
    return out


def check_audience() -> list[Finding]:
    """认知适切：audience / cognitive_load 必须合法且声明；beginner 正文须有类比/直觉段。

    依据（G5 指令 §2.2）：原子此前默认读者是"懂 C++ 基础的进阶者"，没有显式声明，
    G5 涉及入门章节后会导致认知负荷错配。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        # 缺失 → **warn（记债）**；写了但值非法 → block。分级理由：G5 要迁移 1300 个原子，
        # 渐进标注是现实路径；**未标注**的后果只是"学习路径排序缺依据"，不损害断言可信度；
        # 而**标错**（如 audience: novice）会让路径排序拿到非法值，是硬错。
        aud = str(meta.get("audience") or "")
        if not aud:
            out.append(Finding("ATOM-AUDIENCE", "warn", _rel(p),
                               "缺 audience（认知适切维度未标注）",
                               f"取值 {sorted(AUDIENCES)}（见 G1_layout §3）"))
        elif aud not in AUDIENCES:
            out.append(Finding("ATOM-AUDIENCE", "block", _rel(p),
                               f"audience 非法：{aud}", f"取值 {sorted(AUDIENCES)}"))
        cl = str(meta.get("cognitive_load") or "")
        if not cl:
            out.append(Finding("ATOM-AUDIENCE", "warn", _rel(p),
                               "缺 cognitive_load（认知负荷预算未标注）",
                               f"取值 {sorted(COGNITIVE_LOADS)}"))
        elif cl not in COGNITIVE_LOADS:
            out.append(Finding("ATOM-AUDIENCE", "block", _rel(p),
                               f"cognitive_load 非法：{cl}",
                               f"取值 {sorted(COGNITIVE_LOADS)}"))
        if aud == "beginner" and not ANALOGY_RE.search(
                p.read_text(encoding="utf-8", errors="replace")):
            out.append(Finding("ATOM-AUDIENCE", "warn", _rel(p),
                               "beginner 原子正文缺类比/直觉段",
                               "入门读者需要直觉入口，不能只有形式化定义"))
    return out


def check_prereq_readable() -> list[Finding]:
    """`prerequisites_readable` 声明须与**实算**一致（relations 中 prerequisite 目标都已锻造）。

    为什么机器可查：学习路径装配时若按声明把原子排到前置之前，读者会遇到未定义术语。
    声明与实算不符 = 路径排序依据失真。
    """
    existing = {str(_meta(p).get("id") or "") for p in _cards(ATOMS, "ATOM-*.md")}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        declared = meta.get("prerequisites_readable")
        if declared is None:
            continue
        rels = [r for r in _as_list(meta.get("relations")) if isinstance(r, dict)]
        prereqs = [str(r.get("target")) for r in rels if str(r.get("type")) == "prerequisite"]
        actual = all(t in existing for t in prereqs) if prereqs else True
        want = declared if isinstance(declared, bool) else str(declared).lower() == "true"
        if want != actual:
            out.append(Finding("ATOM-PREREQ-READABLE", "warn", _rel(p),
                               f"prerequisites_readable={want} 与实算不符"
                               f"（实算 {actual}；前置 {prereqs or '无'}）",
                               "改声明，或先锻造缺失的前置原子"))
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


# ── S6 毒样例 P4–P7 对应的四条规则 ─────────────────────────────────────────
# 2026-09-11 第四批：把第三批红队抓到的**真实漏网**变成机器可判的结构性质疑。
# 统一取 warn 级：它们指向「断言/证伪/观测/矩阵」的**判别力**问题，而非形式缺失
# （形式缺失已由 EV-FM-REQUIRED / EV-FALSIFICATION 等 block 规则覆盖）。
_SELF_SATISFIED_PREFIXES = ("_Zn", "_Zd")      # Itanium ABI：operator new / operator delete 家族
_TRIVIAL_OBS_PATTERNS = (
    r"!= nullptr", r"not null=1", r"is null=0",
)


def _assert_candidates(raw: str) -> list[str]:
    """抓 `artifact_assert` 段里的候选字符串（不依赖 meta 的 YAML 解析形态）。"""
    if "artifact_assert:" not in raw:
        return []
    seg = raw.split("artifact_assert:", 1)[1]
    for stop in ("\nexpected", "\nactual", "\nverdict", "\n---"):
        seg = seg.split(stop, 1)[0]
    return re.findall(r'"([^"]+)"', seg)


def check_evidence_self_satisfied_assert() -> list[Finding]:
    """P4 自证断言：夹具自己定义了 operator new/delete ⇒ 工件里**必然**出现其符号（定义处），
    此时任何存在性断言（`contains`/`contains_any` 命中 `_Zn*`/`_Zd*`）都不再区分
    「定义存在」与「调用点存在」——零调用点也恒真。

    第三批实例：EV-MEM-032 初版 `contains_any ["_ZdaPv","_ZdaPvy"]`，而夹具自己重载了
    `operator delete[]`（工件里只有定义、没有 `call`）。修法是改用调用点计数，或在卡内
    写明调用点口径（`grep -c 'call _Znw'` 的实测条数）。
    """
    import re as _re
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        fixture = str(meta.get("fixture") or "")
        fx = ROOT / fixture if fixture else None
        if fx is None or not fx.is_file():
            continue
        code = "\n".join(ln for ln in fx.read_text(encoding="utf-8", errors="replace").split("\n")
                         if not ln.lstrip().startswith("//"))
        if not _re.search(r"operator\s+(new|delete)", code):
            continue                              # 夹具未自定义分配/释放 ⇒ 无自证风险
        raw = p.read_text(encoding="utf-8", errors="replace")
        if "调用点" in raw:
            continue                              # 卡内已注明调用点口径（含 grep 条数）⇒ 视为已处置
        hit = [t for t in _assert_candidates(raw)
               if t.startswith(_SELF_SATISFIED_PREFIXES)]
        if hit:
            out.append(Finding("EV-SELF-SATISFIED-ASSERT", "warn", _rel(p),
                               f"夹具自定义了 operator new/delete，而断言做存在性匹配：{hit[:3]}"
                               "（命中定义处即通过，不区分调用点）",
                               "改用 call_count 锚调用点，或在卡内写明调用点 N 处与统计口径"))
    return out


def check_evidence_falsification_quantified() -> list[Finding]:
    """P5 伪证伪：`falsification` 只有「若…则应…」的假设句、**无任何量化对照值** ⇒ 无法判真伪。

    与 EV-FALSIFICATION（block，管"缺失"）互补：本条管"有但不可判"。
    真对照必须给出两个取值（如 `destroyed` 3 vs 0），否则读者无法复核"结论错了会怎样"。
    """
    import re as _re
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        f = str(_meta(p).get("falsification") or "").strip()
        if f and not _re.search(r"\d", f):
            out.append(Finding("EV-FALSIFICATION-QUANT", "warn", _rel(p),
                               "falsification 无任何量化对照值（纯假设句，不可复核）",
                               "写入「让它失败」的实验的两个取值（如 3 vs 0）"))
    return out


def _raw_without_actual(raw: str) -> str:
    """剥掉「声明型字段」的取值段，供「留痕锚不得自证」检查（A3①）。

    剥离两类（都不是"留痕"，不能充当外部锚）：
      - `actual:` 段（含缩进续行）—— `run_match_file: …x.out` 命中 `.out 路径` 锚，
        使 P7 对所有 run_match_file 形态的卡**结构上恒命中**（声明即留痕）；
      - `artifact_sha256:` 行 —— 64 位十六进制若全为数字会命中「10+ 位数字」锚
        （该锚本意是 CI run 号/时间戳），同属自证。
        **2026-09-12 由 P12 毒样例首跑暴露**：只剥 actual 时毒卡仍靠 sha 的全零被放行。

    （顶层键与 `---` 保留；被剥字段的缩进续行丢弃。）
    """
    lines = raw.split("\n")
    out: list[str] = []
    skipping = False
    for ln in lines:
        if re.match(r"^(actual:|artifact_sha256:)", ln):
            skipping = True
            continue
        if skipping:
            if re.match(r"^\S", ln) or ln.startswith("---"):
                skipping = False
            else:
                continue
        out.append(ln)
    return "\n".join(out)


def check_evidence_trivial_observation() -> list[Finding]:
    """P6 恒真观测：`actual` 里出现「同型自比 / 存在性」观测——对 claim 的关键变量零响应。

    第三批实例：SHARED-002 初版 `use_count after join=1`（join 后任何实现都读到 1，
    对"计数原子/非原子"零判别力）。此类读数只能当烟测，不能承担证伪主证责任。

    **视野（2026-09-12，A3② 扩展）**：`actual.run_match_file` 形态的卡，真实观测量在
    留痕 `.out` 里——本规则现将其**一并纳入扫描范围**（此前只看 `actual:` 文本与夹具
    字面量，`.out` 在视野外）。

    **视野边界（诚实声明）**：`.out` 的 `key=value` **数值同值性**（如 8 个读数同为 42）
    **不在此判**——同值既可能是恒真伪证、也可能是**合法对照/不同档位同结论**（后者正是
    实验结论本身），判定它需要实验语义，机器不硬判；该层由**红队盲读 + 卡内显式声明**
    承担（实例：EV-LANG-001 的 8 个 42 已在卡内声明为活性对照）。
    """
    import re as _re
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        raw = p.read_text(encoding="utf-8", errors="replace")
        seg = raw.split("actual:", 1)[1].split("\nverdict", 1)[0] if "actual:" in raw else ""
        # A3②：run_match_file 形态 —— 把 .out 内容也纳入视野
        actual = _meta(p).get("actual") or {}
        if isinstance(actual, dict) and actual.get("run_match_file"):
            f = ROOT / str(actual["run_match_file"])
            if f.is_file():
                seg += "\n" + f.read_text(encoding="utf-8", errors="replace")
        hit = [pat for pat in _TRIVIAL_OBS_PATTERNS if _re.search(pat, seg)]
        if hit:
            out.append(Finding("EV-TRIVIAL-OBSERVATION", "warn", _rel(p),
                               f"actual/.out 含疑似恒真观测：{hit[:3]}（同型自比/存在性判断，"
                               "对关键变量无响应）",
                               "降级为烟测并在卡内声明，补一条对关键变量有响应的对照读数"))
    return out


def check_evidence_matrix_backed() -> list[Finding]:
    """P7 无留痕矩阵：matrix.compiler 声明多个编译器，但卡内无可核对的外部留痕锚。

    v2 收紧（2026-09-12）：旧版用松散关键词匹配，写一句"已留痕"即可自证通过。
    新版要求可核对锚：.out 路径 / CI run 号 / ::notice:: / 完整编译器命令行 / 标准条文声明。
    """
    import re as _re
    out: list[Finding] = []
    _trace_anchors = [
        _re.compile(r"Examples/[^\s\])]+\.out"),
        _re.compile(r"build/[^\s\])]+\.out"),
        _re.compile(r"run\s*#\d+"),
        _re.compile(r"\b\d{10,}\b"),
        _re.compile(r"::notice::"),
        _re.compile(r"g\+\+\s+[^\n]*-o\s+"),
        _re.compile(r"clang\+\+\s+[^\n]*-o\s+"),
        _re.compile(r"标准条文"),
        _re.compile(r"M2.*永久边界"),
    ]
    for p in _cards(EVIDENCE, "EV-*.md"):
        raw = p.read_text(encoding="utf-8", errors="replace")
        m = _re.search(r"compiler:\s*\[([^\]]*)\]", raw)
        if not m:
            continue
        comps = [c.strip().strip("'") for c in m.group(1).split(',') if c.strip()]
        if len(comps) > 1:
            # A3①（2026-09-12）：锚必须出现在 **actual 段之外**——actual 里的
            # `run_match_file: …x.out` 是"声明"不是"留痕"，否则本规则对 run_match_file
            # 形态的卡结构上恒命中（永久失效）。
            has_anchor = any(pat.search(_raw_without_actual(raw)) for pat in _trace_anchors)
            if not has_anchor:
                out.append(Finding("EV-MATRIX-UNBACKED", "warn", _rel(p),
                                   f"matrix 声明 {len(comps)} 个编译器，卡内无可核对的外部留痕锚"
                                   f"（{', '.join(comps)}）",
                                   "补可核对锚：.out 路径 / CI run 号 / ::notice:: / 完整编译器命令行 / 标准条文代替声明"))
    return out


_ZERO_DIAG_RE = re.compile(
    r"零诊断|无诊断|无警告|无警示|no\s+warning|zero\s+diagnostic|warning-free", re.I)


def check_evidence_zero_diag_werror() -> list[Finding]:
    """P11 零诊断类判据须 `-Werror`（371 报告 W3，红队发现）。

    为何：replay 的 `compile_rc` **只看退出码**，而**警告不影响 rc** ⇒ "无警告/零诊断"
    这类 `falsification` 在不加 `-Werror` 时**不可机器判定**（判据形同虚设：编译器发了
    警告也照样 confirm）。补 `-Werror` 后警告即 rc≠0，判据才真正落地。

    实测口径（2026-09-12 全库排查）：falsification 含此类措辞者仅 1 张（EV-LANG-001），
    且已带 `-Werror` —— 本规则为**防回归**（该体裁洞此前是隐性的：判据写得漂亮，
    机器却看不见）。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        hits = sorted(set(_ZERO_DIAG_RE.findall(str(meta.get("falsification") or ""))))
        if not hits:
            continue
        if "-Werror" not in str(meta.get("command") or ""):
            out.append(Finding("EV-ZERO-DIAG-WERROR", "warn", _rel(p),
                               f"falsification 含零诊断措辞 {hits}，但 command 无 -Werror"
                               f"——警告不影响 rc，该判据不可机器判定",
                               "command 补 -Werror；或把判据改写为可观测读数（rc/输出）"))
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
    """S1 三权分立：签署人须与状态级别匹配（人级唯人可签，Agent 不得自证）。

    G6 起级别化：machine-verified → `machine:*`（门禁自动晋升）、
    red-team-verified → `redteam:*`（红队晋升）、human-verified/verified → `human:*`。
    人级的"唯人可置"语义**不变**——变的只是它不再是唯一的已验证状态。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        st = str(meta.get("status") or "").strip().lower()
        if st not in VERIFIED_STATUSES:
            continue
        need = LEVEL_PRINCIPALS.get(st, ())
        by = str(meta.get("verified_by") or "")
        if not by.startswith(need):
            out.append(Finding("S1-AUTHOR-SELF-VERIFY", "block", _rel(p),
                               f"status={st} 但 verified_by 前缀应为 {'/'.join(need)}"
                               f"（当前：{by or '空'}）",
                               "人级由人复核后写 human:*；机器晋升 machine:*；红队 redteam:*"))
    return out


def check_s2_evidence_verdict() -> list[Finding]:
    """S2 声明-证据绑定：已验证原子引用的证据必须 verdict=confirm（作者自述无效）。"""
    verdicts = {str(_meta(p).get("id") or p.stem): str(_meta(p).get("verdict") or "")
                for p in _cards(EVIDENCE, "EV-*.md")}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        if not is_verified(_meta(p)):
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


def _s3_expected_segments(actual: dict) -> list[tuple[str, str]]:
    """产出"待检期望片段"及其来源标签——覆盖两种 actual 形态（369 任务8，P1-12）。

    ① literal 形态：`actual: {key: value}` → 取 value 的 `|` 分隔段；
    ② 文件形态：`actual: {run_match_file: path, run_match_keys: [...]}` → 读留痕 `.out`，
       按 `key=value` 取 **value 段**（含 `|` 分隔）——**不拿 key 名比对**（key 合法地
       出现在 printf 格式串 `"x=%d\\n"` 里，拿 key 比对会全库误报）；且只查本卡声明的
       keys（`.out` 里其余行不是本卡证据，不越界判卡）。
    """
    segs: list[tuple[str, str]] = []
    for k, v in actual.items():
        if k in ("run_match_file", "run_match_keys"):
            continue
        for t in (x.strip() for x in str(v).split("|")):
            if t:
                segs.append((t, f"actual.{k}"))
    mf = actual.get("run_match_file")
    if mf:
        of = ROOT / str(mf)
        if of.is_file():
            keys = {str(x) for x in _as_list(actual.get("run_match_keys"))}
            for ln in of.read_text(encoding="utf-8", errors="replace").split("\n"):
                if not ln.strip():
                    continue
                key, _, val = ln.partition("=")
                if keys and key.strip() not in keys:
                    continue
                for t in (x.strip() for x in val.split("|")):
                    if t:
                        segs.append((t, f"{Path(str(mf)).name}:{key.strip()}"))
    return segs


def check_s3_hardcoded_expected() -> list[Finding]:
    """S3 伪证据检测：期望输出**硬编码进夹具字符串字面量**（打印常量冒充观测）→ 作弊级阻断。

    两种实际形态都查（369 任务8，P1-12）：direct literal（`actual: {k: v}`）与
    `run_match_file + run_match_keys`（CONC 域 6 张卡）——后者此前完全免检，
    夹具里 `printf("total=100000\\n")` 再把输出抄进 `.out` 即可绕过。
    只查字符串字面量：`//@ 注释`与 printf 的 %d 格式串都不含"带实测数字"的片段，不误报。
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
        for seg, where in _s3_expected_segments(actual):
            if len(seg) >= 6 and any(seg in lit for lit in literals):
                out.append(Finding("S3-EXPECTED-HARDCODED", "block", _rel(p),
                                   f"期望片段被硬编码进夹具字面量：{seg[:40]!r}"
                                   f"（来源 {where}）",
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


def _misconception_gap() -> list[Finding]:
    """PED-MISCONCEPTION：误解清单**存在性**检查（兼容三种合法写法）。

    2026-09-12 实测（26 颗原子，369 任务2，P1-4）：
      * `pedagogy.misconception`（单数） → 3 颗（CONC 三颗）
      * `pedagogy.misconceptions`（复数）→ 22 颗
      * 顶层 `misconceptions`（无缩进）  → 4 颗（其 pedagogy 为折叠字符串，无子字段）
    规则语义是"清单必须存在"，不限定写在哪一层；三处皆空才报。

    已知盲区（**不在此处扩权**，列入 369 报告"待裁决"项）：pedagogy 为折叠字符串
    （`pedagogy: >-`）的 4 颗原子，PED-MOTIVATION/SOCRATIC/PREDICT-FIRST 三规则因
    `isinstance(ped, dict)` 为假而静默跳过——结构异常需另行裁决，本规则不代判。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        ped = meta.get("pedagogy") or {}
        found: list = []
        if isinstance(ped, dict):
            found += _as_list(ped.get("misconception"))
            found += _as_list(ped.get("misconceptions"))
        found += _as_list(meta.get("misconceptions"))
        if not found:
            out.append(Finding("PED-MISCONCEPTION", "advice", _rel(p),
                               "缺 misconception 清单（pedagogy 与顶层字段均为空）",
                               "至少一处非空：pedagogy.misconception / "
                               "pedagogy.misconceptions / 顶层 misconceptions"))
    return out


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
        ("ATOM-ID-UNIQUE", "原子身份唯一（stem==id 且 id 全库唯一）", "atom",
         check_atom_id_unique),
        ("ATOM-VERIFIED-BOUND", "verified ⟹ 证据+一手+superiority", "atom",
         check_verified_bound),
        ("ATOM-NO-UNVERIFIED", "新原子禁未验证状态", "atom", check_no_unverified_status),
        ("ATOM-STATUS-VALUE", "status 取值限于四级枚举", "atom", check_status_value),
        ("ATOM-STATUS-TRANSITION", "状态跃迁可证（status_history 链）", "atom",
         check_status_transition),
        ("ATOM-DAL-MATCH", "DAL 分级与人审要求一致", "atom", check_dal_match),
        ("ATOM-REL-TARGET", "关系目标存在", "atom", check_relations_target_exists),
        ("ATOM-REL-DAG", "学习路径 DAG 无环", "atom", check_relations_dag),
        ("ATOM-SUPERIORITY-WORDS", "superiority 禁词表", "atom",
         check_superiority_banned_words),
        ("EV-FM-REQUIRED", "证据卡必填字段完整", "evidence", check_evidence_frontmatter),
        ("EV-FALSIFICATION", "证伪对照存在（非恒真测试）", "evidence",
         check_evidence_falsification),
        ("EV-MATRIX", "版本矩阵字段完整", "evidence", check_evidence_matrix),
        ("ATOM-GRAY-ZONE", "UB 域原子标注灰色地带类别", "atom", check_atom_gray_zone),
        ("ATOM-MISCONCEPTION-LEVELS", "误解分层 surface/deep（deep 须 ≥2 反例）", "atom",
         check_misconception_levels),
        ("MIS-LIBRARY", "误解库自身合规（level 合法 / deep≥2 反例 / 有出处）", "atom",
         check_mis_library),
        ("ATOM-MISCONCEPTION-REF", "原子引用的误解 ID 必须存在", "atom",
         check_misconception_ref),
        ("ATOM-AUDIENCE", "认知适切：audience/cognitive_load 合法 + beginner 须有类比段",
         "atom", check_audience),
        ("ATOM-PREREQ-READABLE", "前置可读声明与实算一致", "atom", check_prereq_readable),
        ("EV-SERVES-EXIST", "证据服务的原子存在", "evidence", check_evidence_serves_exist),
        ("DOC-ZERO-PLACEHOLDER", "新体系零占位符", "repo", check_zero_placeholder),
        ("META-MANIFEST", "双清单一致（ADR-0004）", "repo", check_manifest_consistency),
        ("S1-AUTHOR-SELF-VERIFY", "verified 须人工签收（Agent 无权定 golden）", "atom",
         check_s1_human_signoff),
        ("S2-EVIDENCE-VERDICT", "verified 只绑 verdict=confirm 的证据", "atom",
         check_s2_evidence_verdict),
        ("S3-EXPECTED-HARDCODED", "期望硬编码进夹具=伪证据", "evidence",
         check_s3_hardcoded_expected),
        ("EV-SELF-SATISFIED-ASSERT", "断言不得被夹具自身定义满足（P4 自证断言）", "evidence",
         check_evidence_self_satisfied_assert),
        ("EV-FALSIFICATION-QUANT", "证伪对照须含量化取值（P5 伪证伪）", "evidence",
         check_evidence_falsification_quantified),
        ("EV-TRIVIAL-OBSERVATION", "actual 禁恒真观测承担主证（P6）", "evidence",
         check_evidence_trivial_observation),
        ("EV-MATRIX-UNBACKED", "多编译器矩阵须有留痕说明（P7）", "evidence",
         check_evidence_matrix_backed),
        ("EV-ZERO-DIAG-WERROR", "零诊断类判据须 -Werror（W3）", "evidence",
         check_evidence_zero_diag_werror),
    ]
    sev = {"ATOM-REL-TARGET": "warn", "EV-SERVES-EXIST": "warn",
           "META-MANIFEST": "warn",
           # S6 P4–P7（2026-09-11 第四批）：判别力类问题，warn 级——不阻断但在门禁可见
           "EV-SELF-SATISFIED-ASSERT": "warn", "EV-FALSIFICATION-QUANT": "warn",
           "EV-TRIVIAL-OBSERVATION": "warn", "EV-MATRIX-UNBACKED": "warn",
           # 2026-09-12（W3）：零诊断类判据缺 -Werror —— 判据可判定性问题，warn 级
           # （不阻断存量，但在门禁可见；漏登记会默认 block，与 Finding 实际级别不符）
           "EV-ZERO-DIAG-WERROR": "warn"}
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
                  check=_misconception_gap,
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
