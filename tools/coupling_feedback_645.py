"""645 · 阶段 C4 · 耦合反馈真实化（替代 643 C3 静态反馈）。

目标（645 §五 C4）：基于三层耦合结果，真实驱动反馈：哪类问题需补充头部层证据、哪类结论
待人审、头部层优先级调整（按漏洞密度）。非静态统计——从真实编排链出发，输出可行动反馈。

真实、非代理：输入来自 C2 编排链（真实 Issue→证据→验证）；反馈按真实验证结果分类。
`--check`：只读自检。`--feedback`：真实生成反馈，写 `data/645_feedback_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_feedback_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_feedback_report.json")


def generate_feedback(chains: list[dict]) -> dict:
    """从真实编排链生成反馈（纯函数，便于单测）。"""
    needs_evidence = []     # 缺头部层证据 → 头部层补
    needs_human = []        # 反例/充分性不足 → 人审
    verified_ok = []        # 已验证通过 → 可沉淀
    for c in chains:
        v = c["verification"]
        if v["verdict"] == "pass":
            verified_ok.append(c["issue"])
        elif v["verdict"] == "needs_human":
            needs_human.append(c["issue"])
        elif v["verdict"] in ("fail", "escape"):
            if c.get("evidence_count", 0) == 0:
                needs_evidence.append(c["issue"])
            else:
                needs_human.append(c["issue"])
    # 头部层优先级：按漏洞密度（needs_evidence+needs_human 占比）
    total = len(chains) or 1
    density = (len(needs_evidence) + len(needs_human)) / total
    return {
        "chains": len(chains),
        "verified_ok": verified_ok,
        "needs_evidence": needs_evidence,
        "needs_human": needs_human,
        "head_layer_priority": "high" if density > 0.5 else "medium",
        "vulnerability_density": round(density, 4),
    }


def selftest() -> int:
    """只读自检：反馈分类逻辑。"""
    chains = [
        {"issue": "I1", "verification": {"verdict": "pass"}},
        {"issue": "I2", "verification": {"verdict": "needs_human"}},
        {"issue": "I3", "verification": {"verdict": "fail", "evidence_count": 0}},
    ]
    fb = generate_feedback(chains)
    assert fb["verified_ok"] == ["I1"]
    assert "I2" in fb["needs_human"]
    assert "I3" in fb["needs_evidence"]
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 耦合反馈（真实驱动）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--feedback", action="store_true", help="真实生成反馈")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    # 复用 C2 真实编排链
    import three_layer_orchestrator_645 as c2
    res = c2.orchestrate()
    fb = generate_feedback(res["chains"])
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(fb, fh, ensure_ascii=False, indent=2, sort_keys=True)
    lines = ["# 645 耦合反馈报告（C4，真实驱动）", "",
             f"- 编排链数：{fb['chains']}",
             f"- 已验证通过：{len(fb['verified_ok'])}",
             f"- 需补头部层证据：{len(fb['needs_evidence'])}",
             f"- 需人审：{len(fb['needs_human'])}",
             f"- 头部层优先级：{fb['head_layer_priority']}（漏洞密度 {fb['vulnerability_density']}）", ""]
    lines.append("## 需补证据的问题")
    lines.extend(f"- {i}" for i in fb["needs_evidence"])
    lines.append("## 需人审的问题")
    lines.extend(f"- {i}" for i in fb["needs_human"])
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"[645 feedback] 补证据={len(fb['needs_evidence'])} 人审={len(fb['needs_human'])} "
          f"优先级={fb['head_layer_priority']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
