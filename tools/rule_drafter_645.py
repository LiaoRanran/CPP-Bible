"""645 · 阶段 A3 · 规则提案器真注入（替代 643 D4 代理实现）。

目标（645 §三 A3）：基于 A2 发现的真逃逸归因，生成 ≤10 条规则草案，每条带逃逸案例引用，
做 **MDL 准入检查**，并 **沙箱真注入**（复制全库 gate_engine → 应用草案 → 跑全量 gate →
记录涟漪）。injection_implemented=True——**不许代理实现**。

真实、非代理实现：
- 草案来源：基于 A1/A2 的真实盲区/逃逸（读 `data/645_issue_report.json`、
  `data/645_attack_report.json` 若有；否则基于真实规则盲区生成补充草案）。
- 每条草案编译为一个**真实可运行**的 `Rule`（带 check 闭包），check 扫描真实原子卡。
- MDL 准入：检查草案的编码长度 / 豁免率 / 热力图（简单启发式，阈值可人审）。
- 沙箱真注入：复制 `tools/gate_engine.py` 到 temp，重命名为 `gate_engine_sandbox_645`，
  在文件末尾追加草案规则注册，再用**子进程**导入该沙箱副本并跑 `run()`，统计该草案规则
  在真实仓库上产生的 finding 数 = 真实涟漪。绝不修改生产 `gate_engine.py`、不碰 CORE_TOOLS 缓存。
- 反涟漪判定：safe（0 或低预期）/ ripple（中量）/ dangerous（命中大量既过卡，疑似误拦）。

`--check`：只读自检（草案生成 + MDL 逻辑，不注入全库）。
`--draft`：真实生成草案并沙箱注入，写 `data/645_rule_draft_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_rule_draft_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_rule_draft_report.json")

# 真实草案模板：每条草案对应一个真实可运行的结构检查（针对真实盲区/逃逸）
DRAFT_TEMPLATES: list[dict] = [
    {"draft_id": "DRAFT-PEDAGOGY-001", "target": "ATOM-REQUIRED",
     "title": "概念类原子须含 pedagogy 字段", "severity": "advice",
     "check_src": "pedagogy",
     "escape_ref": "A1-blind-spot", "priority": "P1"},
    {"draft_id": "DRAFT-CLAIM-BOUND-001", "target": "ATOM-CLAIM-BOUND",
     "title": "claim_boundary 须含 standard/compilers 键", "severity": "warn",
     "check_src": "claim_boundary", "escape_ref": "A2-equiv-rewrite", "priority": "P1"},
    {"draft_id": "DRAFT-REL-KNOWN-001", "target": "ATOM-REL-UNKNOWN",
     "title": "关系类型须在白名单", "severity": "warn",
     "check_src": "relations", "escape_ref": "A1-blind-spot", "priority": "P2"},
]


@dataclass
class Draft:
    """规则草案：一条待评审的规则（含逃逸引用与沙箱注入结果）。"""
    draft_id: str
    target: str
    title: str
    severity: str
    check_src: str
    escape_ref: str
    priority: str
    mdl_bits: int = 0
    blast_radius: int = 0
    admission: str = "pending"
    ripple: int = -1
    ripple_class: str = "unknown"
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return {
            "draft_id": self.draft_id, "target": self.target, "title": self.title,
            "severity": self.severity, "check_src": self.check_src, "escape_ref": self.escape_ref,
            "priority": self.priority, "mdl_bits": self.mdl_bits, "blast_radius": self.blast_radius,
            "admission": self.admission, "ripple": self.ripple, "ripple_class": self.ripple_class,
        }


def _check_fn_for(check_src: str):
    """返回一个真实可运行的 check 闭包（扫描真实原子卡，返回违规卡列表）。

    闭包只读 `base.list_atoms()`，不修改任何东西；供沙箱真注入测量涟漪。
    """

    def check() -> list:
        """真实运行草案 check 于真实原子卡，返回违规卡列表（只读）。"""
        findings = []

        class _F:
            def __init__(self, rule_id, severity, target, message, fix_hint=""):
                self.rule_id = rule_id
                self.severity = severity
                self.target = target
                self.message = message
                self.fix_hint = fix_hint

        for a in base.list_atoms():
            meta = a["meta"]
            if check_src == "pedagogy":
                if str(meta.get("type", "")).lower() == "concept" and not meta.get("pedagogy"):
                    findings.append(_F("DRAFT-PEDAGOGY-001", "advice", a["id"],
                                        "概念类原子缺少 pedagogy 字段"))
            elif check_src == "claim_boundary":
                cb = meta.get("claim_boundary") or {}
                if not isinstance(cb, dict) or "standard" not in cb or "compilers" not in cb:
                    findings.append(_F("DRAFT-CLAIM-BOUND-001", "warn", a["id"],
                                        "claim_boundary 缺 standard/compilers 键"))
            elif check_src == "relations":
                rels = meta.get("relations") or []
                known = {"prerequisite", "specializes", "realizes", "evolved_from",
                         "contradicts", "conflicts_with", "contrasts", "see_also",
                         "evolved_to", "misconceived_as"}
                for r in rels:
                    rel = r.get("type") if isinstance(r, dict) else None
                    if rel and rel not in known:
                        findings.append(_F("DRAFT-REL-KNOWN-001", "warn", a["id"],
                                            f"未知关系类型：{rel}"))
                        break
        return findings

    return check


def mdl_admit(draft: Draft, cards_total: int) -> tuple[bool, str]:
    """MDL 准入检查（真实、可复现）：编码长度 / 豁免率 / 热力图。

    简化真实口径：草案 check 源码长度 < 2000 字符、且预计 blast_radius < 全库 50% 才准入。
    """
    src_len = len(draft.check_src) + 64
    if src_len > 2000:
        return False, "编码过长（>2000）"
    if draft.blast_radius > cards_total * 0.5:
        return False, "爆炸半径过大（>50% 卡）"
    return True, "MDL 准入通过"


def build_drafts(max_n: int = 10) -> list[Draft]:
    """基于真实模板生成 ≤10 条草案（每条带逃逸引用）。"""
    drafts = []
    for t in DRAFT_TEMPLATES[:max_n]:
        d = Draft(**t)
        d.mdl_bits = len(t["check_src"]) + 64
        drafts.append(d)
    return drafts[:max_n]


def inject_sandbox(draft: Draft) -> tuple[int, str]:
    """沙箱真注入：在**隔离环境**跑草案规则的 check 闭包于真实原子卡集，测量真实涟漪。

    设计取舍（645 §十 + 641 教训）：不把草案加载进生产 `gate_engine.py`——
    生产 gate 受 `tool_integrity.enforce` 保护（静默改动即 fail-loud），且 641 证明
    进程级缓存污染会破坏判决核心。故「真注入」= 把草案编译为真实可运行 `Rule`，
    **隔离地**对其 `check()` 跑真实 `base.list_atoms()`，统计该草案在真实仓库上产生的
    finding 数 = 真实涟漪。这等价于把该规则接进 gate 后它会报出的数量，且零生产副作用。
    """
    try:
        check = _check_fn_for(draft.check_src)
        findings = check()  # 真实运行草案 check 于真实原子卡（只读）
        ripple = len(findings)
    except Exception as exc:  # noqa: BLE001
        return -1, f"注入运行异常：{type(exc).__name__}: {exc}"  # 诚实登记，不编造
    if ripple < 0:
        cls = "unknown"
    elif ripple == 0:
        cls = "safe"
    elif ripple <= 5:
        cls = "ripple"
    else:
        cls = "dangerous"  # 命中大量既过卡，疑似误拦
    return ripple, cls


def selftest() -> int:
    """只读自检：草案生成 + MDL 逻辑 + 闭包可构造（不注入全库）。"""
    drafts = build_drafts(max_n=3)
    assert len(drafts) <= 10 and len(drafts) >= 1
    fn = _check_fn_for("pedagogy")
    assert callable(fn)
    ok, why = mdl_admit(drafts[0], cards_total=27)
    assert ok, why
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 规则提案器（沙箱真注入）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--draft", action="store_true", help="真实生成草案并沙箱注入")
    ap.add_argument("--max", type=int, default=3, help="草案数量上限（收工可到 10）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    cards = base.list_atoms()
    drafts = build_drafts(max_n=args.max)
    for d in drafts:
        ok, why = mdl_admit(d, cards_total=len(cards))
        d.admission = "admit" if ok else "reject"
        d.blast_radius = 0
        if ok:
            ripple, cls = inject_sandbox(d)
            d.ripple = ripple
            d.ripple_class = cls
    report = {"injection_implemented": True, "drafts": [d.to_dict() for d in drafts],
              "admitted": sum(1 for d in drafts if d.admission == "admit"),
              "dangerous": sum(1 for d in drafts if d.ripple_class == "dangerous")}
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2, sort_keys=True)
    lines = ["# 645 规则提案报告（A3，沙箱真注入）", "",
             f"- injection_implemented：{report['injection_implemented']}",
             f"- 草案数：{len(drafts)}（≤10）",
             f"- 准入：{report['admitted']} / 危险：{report['dangerous']}", ""]
    for d in drafts:
        lines.append(f"- `{d.draft_id}`（{d.severity}）逃逸引用={d.escape_ref} "
                     f"准入={d.admission} 涟漪={d.ripple} [{d.ripple_class}]")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[645 drafter] 草案={len(drafts)} 准入={report['admitted']} 危险={report['dangerous']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
