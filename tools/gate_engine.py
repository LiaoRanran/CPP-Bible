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
import subprocess
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
CONFLICT_REL = {"contradicts", "conflicts_with"}   # 415 D1：冲突型关系（与 DAG_REL 并列，不参与 DAG 排序）
# 470 P0-D / 452 E11（H14）：冲突关系同义词——旧版只归一 CONFLICT_REL 两种拼写，
# contradiction/conflicts/cancels/opposes 会静默丢弃（两颗真矛盾原子可共存）。
CONFLICT_SYNONYMS = {"contradiction": "contradicts", "conflicts": "conflicts_with",
                     "cancels": "contradicts", "opposes": "contradicts",
                     "refutes": "contradicts", "denies": "contradicts"}  # 472 P1-4（N3）
# 已知关系类型白名单：`ATOM-REL-UNKNOWN` 对表外类型 warn（472 P1-4）。
# `evolved_to`/`misconceived_as` 由该规则**实测发现**后补入（存量合法语义，非冲突类，
# 不参与 DAG 排序与冲突检测——仅作引用/演化链语义）。新增类型须由人裁决后再入表。
REL_TYPES_KNOWN = (DAG_REL | CONFLICT_REL | set(CONFLICT_SYNONYMS)
                   | {"contrasts", "see_also", "evolved_to", "misconceived_as"})
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

# ── 署名实名制（373-P0-B9，2026-09-12 独立对抗渗透实测逃逸）────────────────────
# 逃逸：三处签署判定都只做 `startswith("human:")` —— 前缀命中即放行，于是
#   `by: human:`（空名）、`by: human:   `（纯空格）、`verified_by: human:attacker`
#   全部通过。等于任意一方（含 Writer 自己）可一步伪造「人已复核」，而人级是
#   放权体系里**唯一**的真人授权来源 ⇒ 放权根基被架空（最高危，故列 P0）。
# 修法：三处统一走 principal_ok() —— 前缀命中 + **实名非空** + 人级署名**在册**。
HUMAN_PRINCIPALS = ("liaoranran",)   # 在册人级署名（存量 51 处 human:liaoranran 同源）


def principal_name(by: str, need: Sequence[str]) -> str | None:
    """从 `前缀:实名` 署名取实名；前缀不命中 → None（区分「前缀错」与「名空」）。"""
    s = (by or "").strip()
    for pre in need:
        if s.startswith(pre):
            return s[len(pre):].strip()
    return None


def principal_ok(by: str, need: Sequence[str]) -> tuple[bool, str]:
    """署名合法性**单点判定**（373-P0-B9）。返回 (是否合法, 不合格原因)。

    `need` 为空元组 = draft 级：不限定前缀，但**必须留下非空署名**。
    人级（`human:`）额外要求实名在 `HUMAN_PRINCIPALS` 名册内——非空只是必要条件，
    `human:随便谁` 同样能把人级签出去。
    """
    if not need:
        return (bool((by or "").strip()), "缺署名留痕（draft 也要 by）")
    name = principal_name(by, need)
    if name is None:
        return False, f"前缀应为 {'/'.join(need)}"
    if not name:
        return False, f"前缀后缺实名（空名/纯空格不算签署，须 {'/'.join(need)}<实名>）"
    if need[0] == "human:" and name.lower() not in HUMAN_PRINCIPALS:
        return False, f"署名 {name!r} 不在人级名册（须 {'/'.join(HUMAN_PRINCIPALS)}）"
    return True, ""


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


def check_evidence_id_unique() -> list[Finding]:
    """证据身份唯一（373-N2）：文件 stem 必须等于 frontmatter.id，且 id 全库唯一。

    与 `ATOM-ID-UNIQUE` 同构、同理为 block：下游按 id 建 dict（S2 只绑 verdict=confirm
    的证据、原子 evidence[] 引用、去重），id 重复时**后者静默覆盖前者**——373 独立渗透
    N2 的载荷正是"同 id 的双卡"：一张 confirm、一张 refute，门禁按 id 取到前者即放行。

    实测（2026-09-13，56 张卡）：**0 命中** ⇒ 直接 block，无迁移期。
    """
    out: list[Finding] = []
    owner: dict[str, Path] = {}
    for p in _cards(EVIDENCE, "EV-*.md"):
        eid = str(_meta(p).get("id") or "").strip()
        if not eid:
            continue        # 缺 id 由 EV-FM-REQUIRED 承担
        if p.stem != eid:
            out.append(Finding("EV-ID-UNIQUE", "block", _rel(p),
                               f"文件名 stem（{p.stem}）≠ frontmatter.id（{eid}）",
                               "改名文件与 id 对齐——ID 是身份，两者必须同源"))
        if eid in owner:
            out.append(Finding("EV-ID-UNIQUE", "block", _rel(p),
                               f"ID 与 {_rel(owner[eid])} 重复（{eid}）"
                               "（同 id 双卡会让按 id 取 verdict 的下游静默覆盖）",
                               "改 id 或合并——禁止同 id 双卡"))
        else:
            owner[eid] = p
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
            p_ok, p_why = principal_ok(by, need)
            if not p_ok:
                bad.append(f"{lv} 的 by {p_why}（当前：{by or '空'}）")
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
        else:
            drb = str(meta.get("dal_reviewed_by") or "")
            d_ok, d_why = principal_ok(drb, ("human:",))
            if not d_ok:
                out.append(Finding("ATOM-DAL-MATCH", "block", _rel(p),
                                   f"DAL {dal} 豁免人审但无有效 dal_reviewed_by（{d_why}）"
                                   f"（当前：{drb or '空'}）",
                                   "豁免人审是放权决定：须人签**实名**（同批可一次签分级表）"))
    return out


def _relations_norm(meta: dict[str, Any]) -> list[dict[str, Any]]:
    """`relations` 双写法归一（373-N1）：mapping-form → dict-form。

    历史写法 `- prerequisite: ATOM-X` 解析后是 `{'prerequisite': 'ATOM-X'}`——**没有**
    `type`/`target` 键 ⇒ 三条下游规则（REL-TARGET / REL-DAG / PREREQ-READABLE）各自
    `rel.get("target")` 拿到空串 ⇒ **静默跳过**（既不计边也不查环，还不报错）。
    373 独立渗透 N1 实测：CONC 两颗原子正是此写法，其 prerequisite 关系完全在视野外。

    归一**只改解析、不改判据** ⇒ 误伤面只可能来自"此前被静默跳过的卡"（真命中）。
    实测（2026-09-13，27 颗原子）：2 颗用 mapping-form，归一后目标存在、无环 ⇒ **0 命中**。
    """
    out: list[dict[str, Any]] = []
    for rel in _as_list(meta.get("relations")):
        if not isinstance(rel, dict):
            continue
        if rel.get("type") or rel.get("target"):
            out.append(rel)
            continue
        for k, v in rel.items():
            key = str(k)
            if key in CONFLICT_SYNONYMS:            # H14/E11：同义词归一到冲突型
                key = CONFLICT_SYNONYMS[key]
            if key in DAG_REL or key in CONFLICT_REL:
                out.append({"type": key, "target": str(v)})
    return out


def check_relations_target_exists() -> list[Finding]:
    ids = {str(_meta(p).get("id") or p.stem) for p in _cards(ATOMS, "ATOM-*.md")}
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        # 414 P1-8（F07）：纯标量 relations（如 `relations: [PERF-001]`）不经 DAG 校验，
        # 被 _relations_norm 静默丢弃 ⇒ 这里显式 warn，让其进入视野（不 block，存量可能合法）。
        for rel in _as_list(meta.get("relations")):
            if isinstance(rel, str):
                out.append(Finding("ATOM-REL-TARGET", "warn", _rel(p),
                                   f"纯标量 relations 不经 DAG 校验，建议改为 {{type, target}} 结构：{rel!r}",
                                   "改为 dict 形式关系声明（如 - {type: prerequisite, target: X}）"))
        for rel in _relations_norm(meta):
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
        for rel in _relations_norm(_meta(p)):          # 373-N1：归一后再取边
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


def check_relations_unknown_type() -> list[Finding]:
    """472 P1-4（N3 根治）：未知关系类型 → warn（结束"同义词枚举"范式）。

    同义词表永远列不全（`refutes`/`denies` 之后还有下一个）——根治办法是让**表外
    类型可见**：任何不在 `REL_TYPES_KNOWN` 白名单内的 relations 类型都会被 warn，
    使"静默丢弃"变成"显式债务"。新增类型须先加入白名单并明确其语义（由人裁决）。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        unknown: list[str] = []
        # ⚠️ 不能走 `_relations_norm`：它只保留 DAG_REL∪CONFLICT_REL∪同义词的键，
        # **未知类型会被静默丢弃**——正是本规则要发现的对象。这里直接扫原始 relations。
        for rel in _as_list(_meta(p).get("relations")):
            if not isinstance(rel, dict):
                continue
            t = ""
            if rel.get("type") or rel.get("target"):
                t = str(rel.get("type") or "")
            else:
                for k in rel:
                    if str(k) in ("type", "target"):
                        continue
                    t = CONFLICT_SYNONYMS.get(str(k), str(k))   # 同义词先归一
                    break
            if t and t not in REL_TYPES_KNOWN:
                unknown.append(t)
        if unknown:
            out.append(Finding("ATOM-REL-UNKNOWN", "warn", _rel(p),
                               f"relations 含未知类型 {sorted(set(unknown))}"
                               "（不在已知白名单 ⇒ 不参与任何关系判定，等同静默丢弃）",
                               "改用已知类型（prerequisite/specializes/realizes/"
                               "evolved_from/contradicts/conflicts_with/contrasts/see_also），"
                               "或先登记新类型语义再入白名单"))
    return out


def check_atom_rel_conflict() -> list[Finding]:
    """415 D1：relations 矛盾检测（零 LLM，纯图遍历）。

    支持型关系（DAG_REL）与冲突型关系（CONFLICT_REL）互相校验：
      * A 支持/依赖 B，而 B 声明 contradictions A → 直接矛盾（block）
      * A 同时支持 B 又声明 contradictions B → 自身关系矛盾（block）
      * A 在自身 conflicts 中 → 自相矛盾（block）
    严守 L1 机械边界：只认关系**类型对立**，绝不读 claim 文本（语义层归红队/L2）。
    """
    support: dict[str, dict[str, str]] = {}
    conflict: dict[str, dict[str, str]] = {}
    owner: dict[str, Path] = {}
    for p in _cards(ATOMS, "ATOM-*.md"):
        aid = str(_meta(p).get("id") or p.stem)
        owner[aid] = p
        support[aid] = {}
        conflict[aid] = {}
        for rel in _relations_norm(_meta(p)):
            if not isinstance(rel, dict):
                continue
            t = str(rel.get("type") or "")
            g = str(rel.get("target") or "")
            if not g:
                continue
            if t in DAG_REL:
                support[aid][g] = t
            elif t in CONFLICT_REL:
                conflict[aid][g] = t
    out: list[Finding] = []
    for a, supports in support.items():
        for b, st in supports.items():                 # a 支持/依赖 b
            if a in conflict.get(b, {}):                # b 反过来声明与 a 矛盾
                out.append(Finding(
                    "ATOM-REL-CONFLICT", "block", _rel(owner.get(a, ROOT / "atoms")),
                    f"{a} {st} {b}，但 {b} 声明 contradicts {a}（关系自相矛盾）",
                    "拆分原子或修正其中一条 relations"))
            if b in conflict.get(a, {}):                # a 自己既支持 b 又声明与 b 矛盾
                out.append(Finding(
                    "ATOM-REL-CONFLICT", "block", _rel(owner.get(a, ROOT / "atoms")),
                    f"{a} 同时 {st} 且 contradicts {b}（自身关系矛盾）",
                    "删除其中一条 relations"))
    for a, confs in conflict.items():                  # 自相矛盾（A 声明 contradicts 自身）
        if a in confs:
            out.append(Finding(
                "ATOM-REL-CONFLICT", "block", _rel(owner.get(a, ROOT / "atoms")),
                f"{a} 自相矛盾（contradicts 自身）", "移除自引用"))
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
        rels = _relations_norm(meta)                   # 373-N1：归一后再算前置
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
    # 373-N3（2026-09-13）：留痕锚**不得自证**，且须撑得起"多编译器矩阵"的声明。
    #   · 删掉 `g++ … -o` / `clang++ … -o` 两个**命令锚**：任何 g++ 命令都能命中它，
    #     等于"写了编译命令就算留痕"——373 独立渗透 N3 实测：锚自满足，规则恒绿。
    #   · 改为要求**两处可核对留痕**（双平台 .out / 双 CI run / 各一处 / ::notice:: + 其一）；
    #     单一留痕只能证明"跑过一次"，撑不起多平台声明。
    #   · `标准条文 / M2 永久边界` 保留为**等效留痕**（无编译器可用时的声明形态）。
    _out_re = _re.compile(r"(?:Examples|build)/[^\s\])]+\.out")
    _run_re = _re.compile(r"run\s*#(\d+)")
    _run_no_re = _re.compile(r"\d{10,}")     # CI run 号裸写形态（如 `run 34595609458`）
    _notice_re = _re.compile(r"::notice::")
    _law_re = _re.compile(r"标准条文|M2.*永久边界")
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
            body = _raw_without_actual(raw)
            outs = set(_out_re.findall(body))
            runs = set(_run_re.findall(body)) | set(_run_no_re.findall(body))
            has_notice = bool(_notice_re.search(body))
            has_law = bool(_law_re.search(body))
            backed = (len(outs) + len(runs) >= 2          # 双平台 .out / 双 run / 各一处
                      or (has_notice and (outs or runs))
                      or has_law)                          # 无编译器可用时的声明形态
            if not backed:
                n = len(outs) + len(runs)
                out.append(Finding("EV-MATRIX-UNBACKED", "warn", _rel(p),
                                   f"matrix 声明 {len(comps)} 个编译器，但可核对留痕只有 {n} 处"
                                   f"（{', '.join(comps)}）——单一留痕撑不起多平台声明",
                                   "补两处可核对留痕：双平台 .out（各一份）/ 两个 CI run 号 / "
                                   "::notice:: + 其一；无编译器可用时写明标准条文代替声明"))
    return out


# F04（414 P1-6）：键提取升级为 Unicode——中文/全角键（`ｎｐｒｏｃ=`、`硬件并发数=`）
# 曾因 `^[A-Za-z_]` 起手排除而漏网（.out 键声明完整性对非 ASCII 同样适用）。
_OUT_KEY_RE = re.compile(r"^[\w\u4e00-\u9fff\uff00-\uffef][\w\u4e00-\u9fff\uff00-\uffef\-.]*\s*=")


def check_evidence_out_undeclared_key() -> list[Finding]:
    """373-B3 窄化（`EV-OUT-UNDECLARED-KEY`）：`.out` 里的 `key=value` 行，其 key **必须**
    在 `actual.run_match_keys` 中声明。

    为何：未声明的读数行是**门禁视野外**的自由区——S3 硬编码检查、恒真观测检查都不扫它，
    `expected` 也约束不到它 ⇒ 写什么都通过。373 独立渗透的编造载荷（`fabricated_leak=64`）
    正是这一形态：往 `.out` 里加一行，卡散文再引用它，全库零告警。

    **只抓结构化读数行**（`^\\w[\\w-]*=`）：散文行、注释行（`#`/`//`）不判——
    判"散文里的数字是不是观测"需要实验语义，机器不硬判（由红队/人审承担）。

    实测口径（2026-09-13，56 张卡）：命中 6 张，且**全部**是"卡内全无提及"的未声明键
    ⇒ 与编造键**结构上不可区分**，故本规则只做 **warn**（强制声明完整性，不阻断）；
    升级 block 需先把存量卡的 `run_match_keys` 补齐（改证据卡，本批铁律禁止）。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        actual = _meta(p).get("actual") or {}
        if not isinstance(actual, dict) or not actual.get("run_match_file"):
            continue
        f = ROOT / str(actual["run_match_file"])
        if not f.is_file():
            continue
        keys = {str(k).strip() for k in (actual.get("run_match_keys") or [])}
        miss: list[str] = []
        for ln in f.read_text(encoding="utf-8", errors="replace").split("\n"):
            s = ln.strip()
            if not s or s.startswith(("#", "//")):
                continue
            if _OUT_KEY_RE.match(s):
                k = s.split("=", 1)[0].strip()
                if k not in keys:
                    miss.append(k)
        if miss:
            out.append(Finding("EV-OUT-UNDECLARED-KEY", "warn", _rel(p),
                               f".out 含未声明读数键 {sorted(set(miss))}"
                               "（不在 run_match_keys 中 ⇒ 门禁视野外、不受 expected 约束）",
                               "把该键补进 run_match_keys 并声明期望值，或从 .out 移除"))
    return out


# ── F09/F06（414 P1-5/P1-7）─────────────────────────────────────────────────
_FM_KEY_RE = re.compile(r"^([A-Za-z][\w-]*)\s*:")


def check_frontmatter_duplicate_key() -> list[Finding]:
    """414 P1-5（F09）：frontmatter 重复键。零依赖解析器 after-wins **静默覆盖**——
    两个 `verdict:`（第一份 refute、第二份 confirm）时 gate 只见后者，S2 被遮蔽。

    不改解析器（改 loader 影响全库解析路径），做**文本级**检查：frontmatter 内
    顶层键出现 >1 次 → block（覆盖原子卡与证据卡，两类都要防遮蔽）。
    """
    out: list[Finding] = []
    for base, pat in ((ATOMS, "ATOM-*.md"), (EVIDENCE, "EV-*.md")):
        for p in _cards(base, pat):
            raw = p.read_text(encoding="utf-8", errors="replace")
            if not raw.startswith("---"):
                continue
            fm = raw.split("\n---", 1)[0]
            seen: dict[str, int] = {}
            for ln in fm.split("\n"):
                m = _FM_KEY_RE.match(ln)
                if m:
                    seen[m.group(1)] = seen.get(m.group(1), 0) + 1
            dups = sorted(k for k, n in seen.items() if n > 1)
            if dups:
                out.append(Finding(
                    "EV-FM-DUP-KEY", "block", _rel(p),
                    f"frontmatter 重复键 {dups}（解析器 after-wins 静默覆盖——"
                    "双 verdict 可让 refute 被 confirm 遮蔽、绕过 S2）",
                    "每个顶层键只写一次；要修改直接覆盖旧行"))
    return out


# ── 470 P0-D（452 E07/H8/H18）：frontmatter 解析硬化（safe_load 外层校验）────
_INDENT_KEY_RE = re.compile(r"^(\s+)([A-Za-z_][\w-]*)\s*:")
_SCALAR_KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s+\S")


def _frontmatter_raw(p: Path) -> str:
    raw = p.read_text(encoding="utf-8", errors="replace")
    if not raw.startswith("---"):
        return ""
    end = raw.find("\n---", 3)
    return raw[3:end] if end > 0 else ""


def _line_is_scalar_key(ln: str) -> bool:
    """该行是否为「键: 标量值」（非空值、非纯注释、非 block scalar 起始）。"""
    if not _SCALAR_KEY_RE.match(ln):
        return False
    val = ln.split(":", 1)[1].strip()
    if not val or val.startswith("#"):          # 空值 / 纯注释 = 块起始（合法）
        return False
    return not val.startswith(("|", ">"))       # block scalar 起始（|、>-、|+ …）


def _indent_smuggle_lines(fm: str) -> list[str]:
    """缩进走私检测（452 E07）：标量值行之后出现更深缩进的 `key:` 行。

    合法 YAML 中缩进的 `key:` 只能来自块起始（上一键无值/纯注释）、列表项（`- `）
    或 block scalar（`|`/`>`）内部。若上一行是「键: 标量值」再出现缩进键行
    ⇒ 结构项会被提升为顶层键（走私）。
    """
    hits: list[str] = []
    prev_scalar = False
    for ln in fm.split("\n"):
        if _INDENT_KEY_RE.match(ln):
            if prev_scalar:
                hits.append(ln.strip()[:60])
            prev_scalar = False
            continue
        prev_scalar = _line_is_scalar_key(ln)
    return hits


def check_frontmatter_hardening() -> list[Finding]:
    """470 P0-D：frontmatter 解析硬化——safe_load 外层校验，不换解析权威。

    兼容性实测（2026-09-13）：83 份中 79 份与 safe_load 有差异（尾换行、列表项
    str/dict 类型），3 份 safe_load 直接报错 ⇒ 按 470 风险控制**不硬切**，改为
    外层校验四信号：
      ① indent-smuggle（block）标量值后出现缩进键行（E07）；
      ② dup-key（block）唯一键加载器检出重复键（flow/嵌套均覆盖，E08/H8）；
      ③ invalid（warn）safe_load 语法错误（存量 3 份交人裁决）；
      ④ parse-diverge（block）safe 成功但关键字段与自定义解析不一致。
    无 pyyaml 环境跳过（保持零依赖可用）。
    """
    try:
        import yaml
    except ImportError:                                   # pragma: no cover
        return []
    from yaml.constructor import ConstructorError

    class _UniqueKeyLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            mapping = super().construct_mapping(node, deep=deep)
            seen: set = set()
            for key_node, _v in node.value:
                k = self.construct_object(key_node, deep=deep)
                if k in seen:
                    raise ConstructorError(None, None, f"duplicate key: {k}",
                                           key_node.start_mark)
                seen.add(k)
            return mapping

    out: list[Finding] = []
    for base, pat in ((ATOMS, "ATOM-*.md"), (EVIDENCE, "EV-*.md")):
        for p in _cards(base, pat):
            fm = _frontmatter_raw(p)
            if not fm:
                continue
            for ln in _indent_smuggle_lines(fm):
                out.append(Finding("EV-FM-YAML-HARDENING", "block", _rel(p),
                                   f"[indent-smuggle] 标量值后出现缩进键行：{ln!r}"
                                   "（缩进项会被提升为顶层键——结构走私）",
                                   "键值对不得跟随在标量值之后（检查缩进）"))
            try:
                safe = yaml.load(fm, Loader=_UniqueKeyLoader) or {}
            except ConstructorError as e:
                out.append(Finding("EV-FM-YAML-HARDENING", "block", _rel(p),
                                   f"[dup-key] 重复键：{str(e)[:100]}",
                                   "删除重复键（after-wins 会静默遮蔽）"))
                continue
            except yaml.YAMLError as e:
                out.append(Finding("EV-FM-YAML-HARDENING", "warn", _rel(p),
                                   f"[invalid] YAML 语法非法：{str(e).splitlines()[0][:88]}",
                                   "修正 frontmatter 语法（safe_load 须可解析）"))
                continue
            if not isinstance(safe, dict):
                continue
            meta = _meta(p)
            for k in ("id", "verdict", "status", "artifact_sha256"):
                a, b = meta.get(k), safe.get(k)
                if a is None or b is None:
                    continue
                if str(a).strip() != str(b).strip():
                    out.append(Finding("EV-FM-YAML-HARDENING", "block", _rel(p),
                                       f"[parse-diverge] {k} 两解析器不一致："
                                       f"自定义={str(a)[:36]!r} safe={str(b)[:36]!r}",
                                       "存在同构变换（缩进/重复键/锚点）——修正 frontmatter"))
    return out


# ── 470 P0-B（452 E05）：cat 式证据扫描（EXPERIMENTAL，只记录不参与门禁）────
_READ_OPEN_RE = re.compile(
    r'(?:std::)?ifstream\s+(\w+)\s*\(\s*"([^"]+)"'
    r'|fopen\s*\(\s*"([^"]+)"'
    r'|read_to_string\s*\(\s*"([^"]+)"')
_GETLINE_RE = re.compile(r"getline\s*\(\s*(\w+)\s*,\s*(\w+)")
_ECHO_OUT_RE = re.compile(r"\b(?:printf|fprintf|puts|fputs|cout)\b")


def check_fixture_no_echo_data(cards: list[Path] | None = None) -> list[tuple[str, str, int, str]]:
    """470 P0-B（452 E05）：cat 式证据——夹具读**仓库内**数据文件原样打印（零计算）。

    渐进发布（470 铁律 12）：**experimental** —— 只返回命中清单（调用方决定
    打印/写日志），**不注册进 RULES**、不产生 Finding、不参与门禁。观察一批次
    命中情况后再决定升 warn（升格前需列命中卡交人裁决）。

    判据（方案 A，保守正则）：读语句（ifstream/fopen/read_to_string）打开**仓库内
    存在的相对路径文件**；≤8 行窗口内 getline 中转或直接输出该文件/行变量
    （printf/cout 等）。读入后经算术/函数计算再输出（阴性样例）不命中。

    返回 [(卡名, 源文件, 行号, 证据行)]。
    """
    hits: list[tuple[str, str, int, str]] = []
    for p in (cards or _cards(EVIDENCE, "EV-*.md")):
        meta = _meta(p)
        srcs: list[str] = []
        fx = str(meta.get("fixture") or "")
        if fx and fx.endswith((".cpp", ".cc", ".cxx", ".c")):
            srcs.append(fx)
        for m in re.finditer(r"[^\s\"']+\.(?:cpp|cxx|cc|c)\b", str(meta.get("command") or "")):
            if m.group(0) not in srcs:
                srcs.append(m.group(0))
        for rel in srcs:
            f = ROOT / rel
            if not f.is_file():
                continue
            lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
            for i, ln in enumerate(lines):
                m = _READ_OPEN_RE.search(ln)
                if not m:
                    continue
                path = next((g for g in m.groups()[1::2] if g), "")  # 路径组
                if not path or ":" in path or path.startswith(("/", "\\")):
                    continue                       # 只关心仓库内相对路径
                if not (ROOT / path).exists():
                    continue
                fvars = {g for g in m.groups() if g and g != path}
                window = lines[i:i + 9]
                lvars: set[str] = set()
                for wl in window:
                    gm = _GETLINE_RE.search(wl)
                    if gm and gm.group(1) in fvars:
                        lvars.add(gm.group(2))
                for wl in window:
                    if _ECHO_OUT_RE.search(wl) and any(
                            re.search(rf"\b{re.escape(v)}\b", wl)
                            for v in (fvars | lvars)):
                        hits.append((p.name, rel, i + 1, wl.strip()[:90]))
                        break
    return hits


# ── 470 P0-E（452 E06）：环境依赖读数键（不可复现断言面）────────────────────
_ENV_KEY_EXACT = frozenset({
    "nproc", "date", "time", "user", "username", "host", "hostname", "whoami",
    "uname", "pid", "tmpdir", "temp_dir", "cpu_count", "hw_concurrency",
})
_ENV_KEY_PREFIX = ("nproc", "hardware_concurrency", "__DATE__", "__TIME__",
                   "__TIMESTAMP__", "sysconf", "getenv", "processor_")


def _is_env_key(k: str) -> bool:
    kl = k.strip().lower()
    return kl in _ENV_KEY_EXACT or any(kl.startswith(p) for p in _ENV_KEY_PREFIX)


def check_env_dependent_key() -> list[Finding]:
    """470 P0-E（452 E06）：环境量读数键——机器/时钟相关读数不可复现。

    分级（按存量实测面定级，见 worklog P0-E 摘要）：
      * 环境量键被**声明进 `run_match_keys`** → **block**：比对目标依赖机器/时钟
        ⇒ CI 异核、次日重跑必红（E06 载荷 `keys: [nproc, date, user]` 即此形态；
        存量 0 命中——实测无卡把环境量声明为断言）。
      * 环境量键**仅出现在 .out、未声明** → **advice**：记录性输出带环境量是隐患
        但未被断言（存量 2 张：EV-CONC-003/004 的 `nproc=32`），不进债桶不阻断。
    只认精确词与强前缀：`timestamp`/`elapsed`/`random` 等弱词不匹配（bench 卡正常
    记录时间戳会误伤，见实测）。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        actual = meta.get("actual") or {}
        if not isinstance(actual, dict):
            continue
        keys = {str(k).strip() for k in (actual.get("run_match_keys") or [])}
        bad = sorted(k for k in keys if _is_env_key(k))
        if bad:
            out.append(Finding("EV-ENV-DEPENDENT-KEY", "block", _rel(p),
                               f"run_match_keys 含环境量键 {bad}"
                               "（机器/时钟相关读数不可复现——CI 异核/次日必红）",
                               "把环境量从比对目标移除；需要跨环境复现的结论改用"
                               "与机器无关的读数"))
            continue
        rf = str(actual.get("run_match_file") or "")
        f = ROOT / rf if rf else None
        if not f or not f.is_file():
            continue
        undecl = []
        for ln in f.read_text(encoding="utf-8", errors="replace").split("\n"):
            s = ln.strip()
            if not s or s.startswith(("#", "//")) or "=" not in s:
                continue
            k = s.split("=", 1)[0].strip()
            if _is_env_key(k):
                undecl.append(k)
        if undecl:
            out.append(Finding("EV-ENV-DEPENDENT-KEY", "advice", _rel(p),
                               f".out 含环境量读数键 {sorted(set(undecl))}（未声明为断言）"
                               "——留痕即隐患，换机器后该行失去可比性",
                               "从 .out 移除环境量行，或明确它只作参考不作断言"))
    return out


def check_fixture_no_echo_findings() -> list[Finding]:
    """472 P1-2（452 E05）：cat 式证据由 experimental 升为 **warn**（默认参与门禁）。

    升格依据：experimental 零输出 ⇒ 卡照样 confirm 直推 verified（v5 复测实证）。
    存量实测 56 卡 **0 命中**（阴性对照：读入后计算再输出不命中），故升 warn 零误伤。
    """
    out: list[Finding] = []
    for card, fpath, lno, snip in check_fixture_no_echo_data():
        out.append(Finding(
            "EV-FIXTURE-NO-ECHO-DATA", "warn", card,
            f"疑似 cat 式证据：{fpath}:{lno} {snip}"
            "（夹具读仓库内数据文件原样打印 ⇒ 只证「输出==文件」，不证任何机制）",
            "让夹具真正计算；确需读基线数据时把计算过程显式留在夹具内"))
    return out


def check_evidence_out_stale_mtime() -> list[Finding]:
    """414 P1-7（F06）：`.out` 必须比夹具新。`.out` 可手写伪造（replay 只比对内容），
    真跑出来的 `.out` 一定晚于夹具最后修改。启发式（可被 touch 绕过），拦低级伪造。

    宽容差 5s：git 全新 checkout 会把全部文件 mtime 拉齐到检出时刻，若不设宽容差
    会对存量制造大量伪命中；只拦「.out 明显早于夹具」的真陈旧痕。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        actual = meta.get("actual") or {}
        rf = str(actual.get("run_match_file") or "") if isinstance(actual, dict) else ""
        fx = str(meta.get("fixture") or "")
        if not rf or not fx:
            continue
        f_out, f_fx = ROOT / rf, ROOT / fx
        if not (f_out.is_file() and f_fx.is_file()):
            continue
        if f_out.stat().st_mtime < f_fx.stat().st_mtime - 5:
            # advice 而非 warn：414 自认启发式（可 touch 绕过），且存量夹具存在
            # 「.out 生成后又碰过 .cpp」（replay 仍 confirm ⇒ 非语义陈旧）的良性情痕，
            # warn 会造新增债——只建议重跑，不进债桶。
            out.append(Finding("EV-OUT-STALE-MTIME", "advice", _rel(p),
                               f".out（{rf}）比夹具（{fx}）旧——疑似不是当前源码的"
                               "真实产出（手写/陈旧留痕）",
                               "重跑 command 重新生成 .out，或修正 run_match_file"))
    return out


# 373-B2 窄化（2026-09-13）：**无判别力的通用符号**——几乎出现在任何工件里，
# 拿它当断言等于没有断言（373 独立渗透 B2-R1 的载荷正是 `contains "main"`）。
UNIVERSAL_SYMBOLS = frozenset({
    "main", "call", "ret", "retq", "nop", "endbr64", "pushq", "popq", "movq", "movl",
    "lea", "jmp", "je", "jne", "cmp", "test", "add", "sub", "xor", "leave",
})
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
_CJK_RE = re.compile(r"[一-鿿]")


def _assert_targets(rule: dict) -> tuple[bool, list[str]]:
    """一条 `artifact_assert` 的目标文本 → (是否 any-of 形态, 文本列表)。

    与 `atom_evidence_replay.check_artifact_assert` 同构（同一套 kind 语义）：
    `contains_any`/`call_count` 是**任一候选命中即成立**，故只要有一个可映射即算有出处。
    """
    kind = str(rule.get("kind") or "")
    if kind in ("contains", "absent"):
        return False, [str(rule.get("text") or "")]
    if kind in ("contains_any", "absent_any"):
        return True, [str(t) for t in (rule.get("texts") or [])]
    if kind == "call_count":
        syms = [str(s) for s in (rule.get("symbols") or [])]
        return True, syms or ([str(rule["symbol"])] if rule.get("symbol") else [])
    if kind in ("contains_in", "absent_in"):
        return False, [str(rule.get("symbol") or "")]
    return False, []


def _strip_comments(text: str, is_asm: bool) -> str:
    """删注释，使"出处空间"不含伪造锚点（373 绕过测试 2c：夹具注释里写一句符号名即可给
    任意符号发通行证——`absent "_Znwm"` 配 `/* _Znwm */` 就能让断言恒真）。

    - C/C++/asm 通用：删 `/* ... */` 块注释；
    - 行注释：源文件 `//`，汇编 `;`（asm 注释符）。`.out` 等非源码文本不剥 `;`，避免误删内容。
    """
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    out: list[str] = []
    for ln in text.split("\n"):
        ln = ln.split(";", 1)[0] if is_asm else ln.split("//", 1)[0]
        out.append(ln)
    return "\n".join(out)


def _assert_haystack(meta: dict) -> str:
    """断言的可映射空间 = 夹具源码 ∪ 全部工件文本（`artifact` + `artifacts[]`），已剥注释。

    剥注释的原因：出处空间若含注释行，"在夹具里出现过符号名"就成了免费通行证——任何符号
    只要在注释里提一句就能被判定"有出处"。373 绕过测试 2c 正是此手法的实例。
    """
    parts: list[str] = []

    def _add(rel: object) -> None:
        f = ROOT / str(rel or "")
        if not f.is_file() and not f.is_dir():
            return
        is_asm = f.suffix.lower() in (".asm", ".s", ".S")
        if f.is_file():
            parts.append(_strip_comments(f.read_text(encoding="utf-8", errors="replace"), is_asm))
        elif f.is_dir():
            for x in sorted(f.rglob("*")):
                if x.is_file():
                    parts.append(_strip_comments(
                        x.read_text(encoding="utf-8", errors="replace"),
                        x.suffix.lower() in (".asm", ".s", ".S")))
    _add(meta.get("fixture") or "")
    _add(meta.get("artifact") or "")
    for e in (meta.get("artifacts") or []):
        _add(e if isinstance(e, str) else (e.get("path") or e.get("file") or ""))
    return "\n".join(parts)


def check_evidence_assert_symbol_mapped() -> list[Finding]:
    """373-B2 窄化（`EV-ASSERT-SYMBOL-MAPPED`）：断言文本必须**可定位到真实出处**。

    为何：B2 的两类逃逸都出在"断言对象"上——
      - **通用符号**（`main`/`call`/`ret`）：任何工件里都有 ⇒ 断言**恒真**，零判别力；
      - **拼错/平台专属符号**：任何工件里都没有 ⇒ 断言永不成立或被绕过，读者却以为有校验。

    判据：断言文本须命中 ∈ {夹具源码 ∪ 本卡全部工件文本 ∪ 卡内显式 `symbol_map`}。
    **不做模糊匹配**（`spin_plain` → `_Z10spin_plainv` 的映射不可靠，裁决 §2.2 明令禁止）：
    需要跨形态对应时由卡内**显式声明** `symbol_map: {spin_plain: _Z10spin_plainv}`。

    分级（实测 56 卡后的取舍）：
      - 通用符号不可映射 → **block**（零判别力载荷，一律拦）；
      - 其它符号不可映射 → **warn**（可能是平台拼写差异，非必然伪造）；
      - 纯散文断言（含中文且无 ASCII 标识符）→ **跳过**，由红队/人审承担（裁决 §2.2）。

    实测（2026-09-13，56 卡）：命中 1 张（EV-MEM-017 断言 `_Znwm`，而 MinGW 工件里
    operator new 实为 `_Znwy`——size_t 在 LLP64 下是 unsigned long long）。这是**真缺陷**：
    该卡在 Windows 侧走 sha 比对、断言从未被评估，故双平台 confirm 掩盖了它。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        rules = meta.get("artifact_assert")
        rules = [r for r in rules if isinstance(r, dict)] if isinstance(rules, list) else []
        if not rules:
            continue
        hay = _assert_haystack(meta)
        sm = meta.get("symbol_map") or {}
        sm_space = set(sm) | {str(v) for v in sm.values()} if isinstance(sm, dict) else set()
        bad_universal: list[str] = []
        bad_other: list[str] = []
        for r in rules:
            any_of, texts = _assert_targets(r)
            texts = [t for t in texts if t]
            if not texts or all(_CJK_RE.search(t) and not _IDENT_RE.search(t) for t in texts):
                continue                                   # 散文断言：交人审
            # 通用符号（main/call/ret…）**无论在哪都视为无出处**——任何工件里都有它，
            # 拿它当断言等于没有断言（零判别力）。即便它出现在夹具/工件/ symbol_map 里，
            # 也不算"可映射"，强制走 block（373 绕过测试 2a/2b 的载荷正是 `contains "main"`）。
            mapped = [t for t in texts
                      if t not in UNIVERSAL_SYMBOLS and (t in hay or t in sm_space)]
            if any_of and mapped:
                continue
            if not any_of and len(mapped) == len(texts):
                continue
            # 通用符号**始终视为无出处**（无论是否出现在工件里）：它要么进 miss（被 block），
            # 要么因 any_of 另有真实出处而被 mapped 兜住（放行）。普通符号则只在"既不在工件、
            # 也不在 symbol_map"时才算无出处。
            miss = [t for t in texts
                    if t in UNIVERSAL_SYMBOLS or (t not in hay and t not in sm_space)]
            for t in miss:
                (bad_universal if t in UNIVERSAL_SYMBOLS else bad_other).append(t)
        # F03（414 P1-4）：contains_in/absent_in 的 `text` 才是被检索的字面文本，
        # 旧版 `_assert_targets` 只回传 `symbol`（范围选择器）⇒ text 完全不受约束。
        # 414 原案「通用助记符一律 block」实测误伤存量 4 处：contains_in/absent_in 是
        # **符号区间**语义——`absent_in f "je"`（证循环消除）是强断言、`contains_in "je"`
        # 是存量活性对照，区间内助记符并非恒有，与攻击载荷（contains "mov"）结构上
        # 不可区分（373 教训：不可区分 ⇒ 不硬拦）。收窄为：
        #   * 空 text / 纯中文 text → block（asm 工件区间内恒无，结构性无判别力，存量 0 命中）；
        #   * contains_in + 通用助记符 → advice（近乎恒真的弱断言，质量债不阻断）。
        for r in rules:
            kind = str(r.get("kind") or "")
            if kind not in ("contains_in", "absent_in"):
                continue
            t = str(r.get("text") or "")
            if not t or (_CJK_RE.search(t) and not _IDENT_RE.search(t)):
                out.append(Finding("EV-ASSERT-SYMBOL-MAPPED", "block", _rel(p),
                                   f"contains_in/absent_in 的 text={t!r} 无判别力"
                                   "（空/纯中文——asm 工件中恒无，断言形同虚设）",
                                   "text 改为本卡工件中可定位的有判别力字面文本"))
            elif kind == "contains_in" and t in UNIVERSAL_SYMBOLS:
                out.append(Finding("EV-ASSERT-SYMBOL-MAPPED", "advice", _rel(p),
                                   f"contains_in 的 text={t!r} 是通用助记符"
                                   "（符号区间内近乎恒有 ⇒ 弱断言，判别力存疑）",
                                   "改锚有判别力的字面文本（特定立即数/寻址形态）"))
        if bad_universal:
            out.append(Finding("EV-ASSERT-SYMBOL-MAPPED", "block", _rel(p),
                               f"断言锚定无判别力的通用符号 {sorted(set(bad_universal))}"
                               "（不在夹具源码、无 symbol_map ⇒ 恒真断言）",
                               "改锚有判别力的符号（调用点/本机 mangled 名），"
                               "并用 symbol_map 显式声明夹具名 → 工件符号名"))
        elif bad_other:
            out.append(Finding("EV-ASSERT-SYMBOL-MAPPED", "warn", _rel(p),
                               f"断言文本在夹具/工件中均无出处：{sorted(set(bad_other))}"
                               "（疑似拼错或平台专属拼写，读者会以为有校验）",
                               "核对工件实测拼写；跨形态对应请显式声明 symbol_map"))
    return out


# ── F01（414 P0-2）：MSVC 卡免检链 ──────────────────────────────────────────
_MSVC_PROGS = frozenset({"cl", "cl.exe", "clang-cl", "clang-cl.exe"})


def _command_uses_msvc(cmd: str) -> bool:
    """卡命令是否调用 MSVC（`cl`/`cl.exe`/`clang-cl`）。与 replay 同名判定同构：
    逐 token 取文件名部分比对（大小写不敏感），覆盖 `cl /c`、`C:/.../cl.exe` 等写法。"""
    for line in str(cmd).replace("&&", "\n").split("\n"):
        for tok in line.split():
            name = tok.strip("\"'").replace("\\", "/").rsplit("/", 1)[-1].lower()
            if name in _MSVC_PROGS:
                return True
    return False


def check_evidence_msvc_no_verify() -> list[Finding]:
    """414 P0-2（F01）：含 MSVC(cl) 的卡 replay 只能给 `infra_error:msvc_unavailable`
    （MSVC 为永久边界，重编译校验不尝试 cl）——即**从未被复算**。卡面却标
    `verdict: confirm` ⇒ 不可验证的卡被当成已验证；gate S2 只认卡面 confirm，
    `--accept` 一次即永久挂账（免检链闭合）。

    判据：command 含 cl/cl.exe/clang-cl 且 verdict == confirm → block。
    允许 verdict: refute/unverified/infra_error（不宣称已复算即可）。
    实测（2026-09-13，56 卡）：存量 0 张含 cl ⇒ 0 误伤，直接 block。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        if not _command_uses_msvc(str(meta.get("command") or "")):
            continue
        if str(meta.get("verdict") or "") == "confirm":
            out.append(Finding(
                "EV-MSCV-NO-VERIFY", "block", _rel(p),
                "含 MSVC(cl) 的卡无法被 replay 复算（infra_error:msvc_unavailable），"
                "禁止标 verdict:confirm",
                "verdict 改为 unverified/infra_error；MSVC 卡不得充当 verified 原子的证据"))
    return out


_ARTIFACT_PRODUCER_EXEMPT = ROOT / "tools" / "artifact_producer_exempt.txt"
# 编译器白名单：只有编译器能"凭空产出"一个可复算的工件。
_COMPILER_PROGS = frozenset({
    "g++", "gcc", "clang++", "clang", "c++", "cc", "cl", "clang-cl",
    "x86_64-w64-mingw32-g++", "x86_64-w64-mingw32-gcc",
})


def _producer_exempt_ids() -> set[str]:
    """迁移期豁免名单（行解析，零依赖）。**名单本身就是迁移积压清单**（可审计）。"""
    if not _ARTIFACT_PRODUCER_EXEMPT.is_file():
        return set()
    return {ln.strip() for ln in _ARTIFACT_PRODUCER_EXEMPT.read_text(
        encoding="utf-8").split("\n") if ln.strip() and not ln.startswith("#")}


# ── F02（414 P0-3）：编译后覆写——时序约束（426 框架第一应用）─────────────────
_POST_WRITE_VERBS = re.compile(
    r"(?<![\w-])(?:cp|copy|mv|move|Copy-Item|Move-Item|Set-Content|Add-Content|"
    r"Out-File|tee|dd|shutil\.copy|shutil\.move|shutil\.copyfile)\b", re.I)
_POST_OPEN_WRITE = re.compile(r"open\s*\([^)]*['\"]w[b+]?", re.I)
_POST_READ_PROGS = re.compile(
    r"^\s*[\"']?(?:type|cat|head|tail|grep|findstr|more|less|wc|rg|Get-Content)\b", re.I)


def _post_compile_writes(cmd: str, prod: str, art: str) -> tuple[list[str], list[str]]:
    """F02：producer（编译行）之后的命令段里，artifact 路径是否被「写」。

    返回 (block 段, warn 段)。判据是**语义**（写动词/重定向/写模式 open）而非工具
    黑名单——cp/mv/python/powershell 列不全；编译前覆写会被编译覆盖故不拦（只看
    producer 段之后的段）；路径命中但语义不明（如 type 读）不拦，保守 warn。
    """
    blocks: list[str] = []
    warns: list[str] = []
    art = art.strip()
    if not art:
        return [], []
    base = art.replace("\\", "/").rsplit("/", 1)[-1]
    segs = [s.strip() for s in re.split(r"&&|;|\n", cmd)]
    idx = next((i for i, s in enumerate(segs) if prod in s), -1)
    if idx < 0:
        return [], []          # producer 不在 command 中——上游已有专项 block
    for seg in segs[idx + 1:]:
        if not seg:
            continue
        hit = art if art in seg else (base if base and base in seg else "")
        if not hit:
            continue
        if _POST_WRITE_VERBS.search(seg) or _POST_OPEN_WRITE.search(seg) or re.search(
                r">\s*['\"]?" + re.escape(hit), seg):
            blocks.append(seg)
        elif not _POST_READ_PROGS.match(seg):
            warns.append(seg)  # 语义不明：可能是读，保守 warn
    return blocks, warns


def check_evidence_artifact_producer() -> list[Finding]:
    """373-N4 窄化（`EV-ARTIFACT-PRODUCER`）：工件由谁产出，必须由卡**显式声明**。

    为何：N4 的借工件逃逸是——卡**不自己编译**，而是 `cp other.asm mine.asm`（或用脚本复制）
    一份别人的工件，于是 `artifact_sha256` 与真实编译产物逐字一致、replay 全绿，而这
    张卡**从未跑过自己的实验**。旧判据（命令行文本里出现过 artifact 路径即可）对
    `cp` / `python` 一律放行。

    373 绕过测试 3d 更深一层的漏洞：即便要求"声明编译器"，**只查声明文本**仍可被绕过——
    写 `artifact_producer: g++ -S x.cpp -o a.asm` 但实际 `command: cp other.asm a.asm`，
    两张都全绿（sha 一致）。故新增**声明-实现一致性**硬约束：producer 段须逐字出现在
    command 且 `-o` 目标 == artifact（见下方实现）。

    判据：卡须声明 `artifact_producer: <command 片段>`，该片段的 `argv[0]` 必须 ∈
    编译器白名单。**不做推断**——蓝图原文的"自动判定哪一段产出 artifact"实测误伤 11/56
    （同一命令多段 `-o`），已否决；显式化优于推断。

    迁移期（裁决 §2.3）：存量 56 张卡按 id 列在 `tools/artifact_producer_exempt.txt`，
    缺字段**不阻断**，名单即迁移积压（补一张删一行）；**名单外的卡（= 新卡）缺字段即 block**。
    这一步不能省：若"缺字段"一律豁免，攻击者只要**不写这个字段**就能绕过本规则——
    故豁免必须**按 id 枚举**且**可见**（不是"永久宽限"）。
    """
    exempt = _producer_exempt_ids()
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        eid = str(meta.get("id") or p.stem)
        prod = str(meta.get("artifact_producer") or "").strip()
        if not prod:
            if eid not in exempt:
                out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                                   "缺 artifact_producer：未声明工件由哪段命令产出"
                                   "（借/复制他人工件也能让 sha 全绿）",
                                   "补 `artifact_producer: <产出该工件的编译命令片段>`"))
            continue                      # 名单内 = 迁移期豁免（名单本身即可审计的积压）
        # 只取 argv[0] 的**程序名**：容忍带引号的完整路径（`"C:/.../g++.exe"`）与 `.exe` 后缀
        argv = prod.split()
        prog = argv[0].strip("\"'").replace("\\", "/").rsplit("/", 1)[-1] if argv else ""
        prog = prog.removesuffix(".exe")
        if prog.lower() not in _COMPILER_PROGS:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                               f"artifact_producer 的 argv[0]={prog or '空'} 不是编译器"
                               "（复制/脚本产出 ≠ 亲自编译）",
                               f"须为编译器：{'/'.join(sorted(_COMPILER_PROGS))}"))
            continue
        # 声明—实现一致性（373 绕过测试 3d：本批最核心漏洞）。仅查声明文本时，攻击者写一份
        # 漂亮声明、实际 `command: cp other.asm mine.asm` 即可全绿（replay 重算 sha 也一致，
        # 因为 cp 的就是真工件）。两条硬约束：
        #  ① `artifact_producer` 段必须**逐字出现在 command** 中（声明不是装饰）；
        #  ② 其 `-o` 目标必须 == `artifact` 路径（编译产物确为该工件）。
        cmd = str(meta.get("command") or "")
        art = str(meta.get("artifact") or "").strip()
        if prod not in cmd:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                               "artifact_producer 段未逐字出现在 command 中"
                               "（声明-实现脱钩：实际命令可能不是该编译命令）",
                               "把 artifact_producer 指向的编译命令原样写入 command，"
                               "或令 command 含该段"))
            continue
        m = re.search(r"(?<![\w-])-o\s+(\S+)", prod)
        if not m:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                               "artifact_producer 缺少 -o <artifact>（无法证明产物即该工件）",
                               "令 artifact_producer 含 `-o <artifact 路径>`"))
        elif m.group(1).strip('"\'') != art:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                               f"artifact_producer 的 -o 目标 {m.group(1)!r} 不等于 artifact {art!r}"
                               "（编译产物并非该 artifact）",
                               "令 artifact_producer 的 -o 目标 == artifact 路径"))
        # F02 时序约束（414 P0-3）：编译行之后任何对 artifact 的写操作都使 sha 比对
        # 失效——工件可能已被换成他卡产物。不用工具黑名单（列不全），用「artifact 路径
        # 出现在写位置」的语义判据；语义不明只 warn（保守）。
        for seg in _post_compile_writes(cmd, prod, art)[0]:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "block", _rel(p),
                               f"编译行之后存在对 artifact 的写操作：{seg[:88]!r}"
                               "（编译后覆写 ⇒ sha 比对的可信前提被破坏）",
                               "command 中编译行之后不得再触碰 artifact 路径"))
        for seg in _post_compile_writes(cmd, prod, art)[1]:
            out.append(Finding("EV-ARTIFACT-PRODUCER", "warn", _rel(p),
                               f"编译行之后 artifact 被再次引用、语义不明：{seg[:88]!r}"
                               "（若为读取请改用显式读程序；无法排除覆写）",
                               "移除编译行之后对 artifact 的引用，或改用明确的读操作"))
    return out


_ZERO_DIAG_RE = re.compile(
    r"零诊断|无诊断|无警告|无警示|no\s+warning|zero\s+diagnostic|warning-free", re.I)


_DIAG_SUPPRESS_RE = re.compile(
    r"#pragma\s+(?:GCC|clang)\s+diagnostic\s+ignored"
    r"|#pragma\s+warning\s*\(\s*disable"
    r"|-fno-diagnostics-show-option")


def check_evidence_zero_diag_werror() -> list[Finding]:
    """P11 零诊断类判据须 `-Werror`（371 W3）+ 470 P0-F 扩面（452 E10）。

    为何：replay 的 `compile_rc` **只看退出码**，而**警告不影响 rc** ⇒ "无警告/零诊断"
    这类判据在不加 `-Werror` 时**不可机器判定**。470 P0-F 补两个存活变种：
      * **字段位移**（H16a）：措辞挪到 `expected`/`hypothesis`，旧版只扫
        `falsification` ⇒ 漏检。扫描面扩到全部叙事字段。
      * **pragma 消音**（H16b）：夹具 `#pragma GCC diagnostic ignored` 让 -Werror
        失效——判据从"编译器没说话"退化为"作者让编译器闭嘴"。
    实测（2026-09-13，56 卡）：扩面后字段面仅 EV-LANG-001 命中（已带 -Werror，不报）；
    -Werror 卡 + 消音 pragma 0 条 ⇒ 扩面零新增命中。

    **级别（472 P1-1）**：warn → **block**。warn 级只是"可见化"，卡照样 confirm 直推
    verified（v5 E10a/b 实证）；而"零诊断但无 -Werror"的判据**不可机器判定**，属不可复算
    判据，放行即等于门禁假阳性。存量 0 命中 ⇒ 零误伤；回退方式见 `_register_all` 注册表注释。
    """
    out: list[Finding] = []
    for p in _cards(EVIDENCE, "EV-*.md"):
        meta = _meta(p)
        fields = " ".join(str(meta.get(k) or "") for k in
                          ("falsification", "expected", "hypothesis", "claim_boundary"))
        hits = sorted(set(_ZERO_DIAG_RE.findall(fields)))
        has_werror = "-Werror" in str(meta.get("command") or "")
        if hits and not has_werror:
            out.append(Finding("EV-ZERO-DIAG-WERROR", "block", _rel(p),
                               f"零诊断措辞 {hits}（falsification/expected/hypothesis/"
                               f"claim_boundary 任一），但 command 无 -Werror"
                               f"——警告不影响 rc，该判据不可机器判定",
                               "command 补 -Werror；或把判据改写为可观测读数（rc/输出）"))
        if has_werror:
            fx = ROOT / str(meta.get("fixture") or "")
            if fx.is_file():
                m = _DIAG_SUPPRESS_RE.search(
                    fx.read_text(encoding="utf-8", errors="replace"))
                if m:
                    out.append(Finding("EV-ZERO-DIAG-WERROR", "block", _rel(p),
                                       f"夹具含消音 pragma（{m.group(0)!r}）而卡声明 -Werror"
                                       "——判据从『编译器没说话』退化为『作者让编译器闭嘴』",
                                       "移除消音 pragma；若消音是受控变量须显式声明"))
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
        p_ok, p_why = principal_ok(by, need)
        if not p_ok:
            out.append(Finding("S1-AUTHOR-SELF-VERIFY", "block", _rel(p),
                               f"status={st} 但 verified_by {p_why}（当前：{by or '空'}）",
                               "人级由人复核后写 human:<实名>（须在册）；机器 machine:*；红队 redteam:*"))
    return out


# ── 479 任务 4 / 472 待裁决项 1：E12 签收 × git 作者绑定（观察期 warn）──────────
_GIT_AUTHOR_CACHE: dict[str, tuple[str, str] | None] = {}


def _git_author_for(path: Path) -> tuple[str, str] | None:
    """该文件最后一次 git 提交的 (作者名, 邮箱)；git 不可用/无记录 → None。

    *只读观察*：CI 浅克隆、无 git、路径未入库等情形一律 None ⇒ 调用方跳过，**不报警**
    （gate 不应因环境差异改变结论）。单文件一次调用、结果缓存（27 个原子约 1.5s）。
    """
    key = str(path)
    if key in _GIT_AUTHOR_CACHE:
        return _GIT_AUTHOR_CACHE[key]
    out: tuple[str, str] | None = None
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%an%x1f%ae", "--", str(path)],
            cwd=str(ROOT), capture_output=True, text=True, errors="replace", timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            name, _, mail = r.stdout.strip().partition("\x1f")
            out = (name.strip(), mail.strip())
    except (OSError, subprocess.SubprocessError):
        out = None
    _GIT_AUTHOR_CACHE[key] = out
    return out


def _author_matches(principal: str, author: tuple[str, str]) -> bool:
    """宽松匹配：签收名 vs git 作者名/邮箱（大小写与分隔符不敏感，包含即通过）。

    宽松的理由：本规则是观察期的「是否同一人」提示，不是身份认证；精确匹配会被
    `LiaoRanran` / `liaoranran` / `liaoranran@…` 这类形式差异淹掉，逼出假警。
    """
    def _norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower())

    p = _norm(principal)
    if not p:
        return True                    # 空名由 S1-AUTHOR-SELF-VERIFY / principal_ok 管
    return p in _norm(author[0]) or p in _norm(author[1])


def check_git_author_binding() -> list[Finding]:
    """S1-GIT-AUTHOR-BINDING（479 任务 4）：人级签收须与 git 作者一致 → warn。

    问题（v5 报告 E12，472 待裁决项 1）：`human:liaoranran` 自签**零 block 零 warn**——
    签收机制只验「名字在册」，不验「签字者与产出者是否同一人」，任何人抄上在册名即生效。

    本规则做**可机器核实的下限**：人级签收（`status_history[*].by: human:*` 或
    `verified_by: human:*`）必须与该文件最后一次 git 提交的作者匹配 ⇒ 否则 warn。

    为什么停在 warn（不 block），三条硬理由：
      ① 「甲写卡、乙复核」在协作下是合法流程，git 作者不足以证伪签收；
      ② 存量文件的最后 git 作者会被改写/迁移/合并改变，block 会砸历史（非本代罪）；
      ③ 479 明确定档为**观察期**。
    升 block 的前置：观察期实测零误伤 + 「签收必须本人」写进 G6 规范。
    """
    out: list[Finding] = []
    for p in _cards(ATOMS, "ATOM-*.md"):
        meta = _meta(p)
        principals: list[str] = []
        for h in _as_list(meta.get("status_history")):
            if isinstance(h, dict):
                by = str(h.get("by") or "").strip()
                if by.lower().startswith("human:"):
                    principals.append(by.split(":", 1)[1].strip())
        vb = str(meta.get("verified_by") or "").strip()
        if vb.lower().startswith("human:"):
            principals.append(vb.split(":", 1)[1].strip())
        principals = sorted({x for x in principals if x})
        if not principals:
            continue
        author = _git_author_for(p)
        if author is None:
            continue                       # git 不可用 → 跳过（不报警，见 docstring）
        mismatch = [x for x in principals if not _author_matches(x, author)]
        if mismatch:
            out.append(Finding(
                "S1-GIT-AUTHOR-BINDING", "warn", _rel(p),
                f"人级签收 {mismatch} 与该文件 git 作者 {author[0]} <{author[1]}> 不匹配"
                f"（观察期：只提示不阻断）",
                "确认签收人与产出者同一人；若为代签，在卡内留痕代签人与理由"))
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
        ("ATOM-REL-CONFLICT", "relations 矛盾检测：A 支持/依赖 B 且 B 声明 contradicts A（415 D1）",
         "atom", check_atom_rel_conflict),
        ("ATOM-SUPERIORITY-WORDS", "superiority 禁词表", "atom",
         check_superiority_banned_words),
        ("EV-FM-REQUIRED", "证据卡必填字段完整", "evidence", check_evidence_frontmatter),
        ("EV-ID-UNIQUE", "证据身份唯一（stem==id 且 id 全库唯一，N2）", "evidence",
         check_evidence_id_unique),
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
        ("S1-GIT-AUTHOR-BINDING", "人级签收须与 git 作者一致（479 任务 4，观察期 warn）",
         "atom", check_git_author_binding),
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
        ("EV-OUT-UNDECLARED-KEY", ".out 读数键须在 run_match_keys 声明（B3 窄化）",
         "evidence", check_evidence_out_undeclared_key),
        ("EV-ASSERT-SYMBOL-MAPPED", "断言文本须可定位（夹具/工件/symbol_map，B2 窄化）",
         "evidence", check_evidence_assert_symbol_mapped),
        ("EV-ARTIFACT-PRODUCER", "工件产出命令须显式声明、为编译器、且与 command 逐字一致（N4 窄化+373绕过3d）",
         "evidence", check_evidence_artifact_producer),
        ("EV-MSCV-NO-VERIFY", "含 MSVC(cl) 的卡禁止标 confirm（414 F01 免检链）", "evidence",
         check_evidence_msvc_no_verify),
        ("EV-FM-DUP-KEY", "frontmatter 重复键（after-wins 遮蔽，414 F09）", "repo",
         check_frontmatter_duplicate_key),
        ("EV-FM-YAML-HARDENING", "frontmatter 解析硬化（470 P0-D：走私/重复键/语法/一致性）",
         "repo", check_frontmatter_hardening),
        ("EV-ENV-DEPENDENT-KEY", "环境量读数键（470 P0-E：声明为断言=block/仅留痕=advice）",
         "evidence", check_env_dependent_key),
        ("ATOM-REL-UNKNOWN", "未知 relations 类型（472 P1-4：结束同义词枚举，表外即债务）",
         "atom", check_relations_unknown_type),
        ("EV-FIXTURE-NO-ECHO-DATA", "cat 式证据（472 P1-2：experimental→warn，读文件原样打印）",
         "evidence", check_fixture_no_echo_findings),
        ("EV-OUT-STALE-MTIME", ".out 须比夹具新（414 F06 陈旧留痕）", "evidence",
         check_evidence_out_stale_mtime),
    ]
    sev = {"ATOM-REL-TARGET": "warn", "EV-SERVES-EXIST": "warn",
           "META-MANIFEST": "warn",
           # 414 F06：规则级 warn（保证常跑），Finding 级 advice（启发式可 touch 绕过、
           #   存量有良性情痕 ⇒ 不进债桶）——混合级别同 EV-ASSERT 先例
           "EV-OUT-STALE-MTIME": "warn",
           # S6 P4–P7（2026-09-11 第四批）：判别力类问题，warn 级——不阻断但在门禁可见
           "EV-SELF-SATISFIED-ASSERT": "warn", "EV-FALSIFICATION-QUANT": "warn",
           "EV-TRIVIAL-OBSERVATION": "warn", "EV-MATRIX-UNBACKED": "warn",
           # 2026-09-12（W3）：零诊断类判据缺 -Werror —— 判据可判定性问题。
           # 472 P1-1 由 warn **升 block**，依据（v5 复测 + 实测）：
           #   ① warn 级只"可见化"，卡照样 confirm 直推 verified（E10a/b 两变种实证）；
           #   ② "零诊断"措辞缺 -Werror ⇒ 判据**不可机器判定**（compile_rc 不看警告），
           #      与 P11 毒样例语义一致 —— 不可复算的判据不该放行；
           #   ③ 存量 56 卡实测 **0 命中**（全库仅 EV-LANG-001 提及且已带 -Werror）⇒ 升格零误伤。
           # 回退：本行与两处 Finding 的 "block" 改回 "warn" 即可（无任何存量卡依赖）。
           "EV-ZERO-DIAG-WERROR": "block",
           # 2026-09-13（373-B3 窄化）：未声明读数键与"编造键"结构上不可区分 ⇒ 只 warn
           "EV-OUT-UNDECLARED-KEY": "warn",
           # 472 P1-4：未知关系类型是债务可见化，不阻断存量（新类型入白名单由人裁决）
           "ATOM-REL-UNKNOWN": "warn",
           # 472 P1-2：cat 式证据（存量实测 0 命中，升 warn 不误伤）
           "EV-FIXTURE-NO-ECHO-DATA": "warn",
           # 479 任务 4：E12 签收 × git 作者绑定——观察期只 warn（协作代签/历史迁移都会命中，
           # 升 block 的前置是「观察期零误伤 + 签收必须本人写进 G6 规范」）
           "S1-GIT-AUTHOR-BINDING": "warn",
           # （EV-ASSERT-SYMBOL-MAPPED 规则级登记为 block：通用符号载荷一律拦；
           #   单条 Finding 对"疑似拼写差异"降为 warn，故混合级别是刻意的）
           }
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
    ap.add_argument("--json", nargs="?", const=True, default=False,
                    help="结构化 JSON 输出到 stdout（亦可附路径落盘，兼容旧用法）")
    ap.add_argument("--check", action="store_true", help="任一 block 违规即 exit 1")
    ap.add_argument("--manifest-check", action="store_true", help="仅校验双清单一致性")
    ap.add_argument("--gates", action="store_true", help="导出 cmd_check 元组")
    ap.add_argument("--exp-scan", action="store_true",
                    help="experimental 扫描（P0-B cat 式证据，只记录不参与门禁）")
    a = ap.parse_args(argv)

    if a.exp_scan:
        hits = check_fixture_no_echo_data()
        print(f"[exp] EV-FIXTURE-NO-ECHO-DATA（P0-B experimental，不影响门禁）："
              f"{len(hits)} 处命中")
        for card, fpath, lno, snip in hits:
            print(f"[exp]   {card}:{fpath}:{lno}  {snip}")
        log = ROOT / "build" / "exp_fixture_echo.log"
        log.parent.mkdir(exist_ok=True)
        log.write_text("\n".join(f"{c}:{f}:{l}  {s}" for c, f, l, s in hits) + "\n",
                       encoding="utf-8")
        print(f"[exp] 命中已写入 {log.relative_to(ROOT).as_posix()}")
        return 0

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
    block = sum(1 for f in findings if f.severity == "block")
    warn = sum(1 for f in findings if f.severity == "warn")
    advice = sum(1 for f in findings if f.severity == "advice")
    real_out = sys.stdout
    if a.json:
        sys.stdout = sys.stderr          # 普通报告走 stderr，stdout 只留 JSON
    print(report(findings, len(RULES)))
    if a.json:
        import datetime as _dt
        payload = {
            "tool": "gate_engine", "version": "v6.1",
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "status": "fail" if block else "pass",
            "summary": {"rules": len(RULES), "block": block,
                        "warn": warn, "advice": advice},
            "findings": [{"rule": f.rule_id, "severity": f.severity,
                          "file": f.target, "message": f.message}
                         for f in findings],
            "infra_errors": [],
        }
        if isinstance(a.json, str):       # 兼容旧用法：落盘路径
            Path(a.json).write_text(
                json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[gate] 工单 → {a.json}", file=real_out)
        else:                             # 新用法：stdout 只输出 JSON
            real_out.write(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    if a.check:
        return 1 if block else 0
    return 0


PYTHON_EXE = sys.executable    # 与 cppbible 侧 PYTHON_EXE 语义一致（--gates 输出用）

if __name__ == "__main__":
    raise SystemExit(main())
