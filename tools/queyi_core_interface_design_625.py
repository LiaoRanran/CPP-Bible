"""625 C2 · QueYi Core 核心接口抽象设计（**只设计不实现**，v0.1）

设计 5 个核心接口：Claim / Evidence / Attack / Verify / Authority，并给出与现有工具的映射关系。
接口版本 **v0.1（设计版）**；626 为实现版。

铁律：**不改任何现有工具的实现**（本工具只产出设计数据 + 文档）；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VERSION = "v0.1"

INTERFACES: dict[str, dict] = {
    "Claim": {
        "desc": "知识命题（原子卡的可验证主张）",
        "attrs": ["id", "statement", "domain", "difficulty", "prerequisites", "evidence_refs"],
        "methods": ["validate()", "get_evidence()", "get_prerequisites()"],
    },
    "Evidence": {
        "desc": "证据（可复算工件/观测）",
        "attrs": ["id", "type", "source", "content", "hash", "verifier_refs", "provenance"],
        "methods": ["validate()", "get_verifiers()", "get_provenance()", "verify_hash()"],
    },
    "Attack": {
        "desc": "攻击/mutation（对命题或证据的扰动）",
        "attrs": ["id", "type", "target", "strategy", "complexity", "expected_result"],
        "methods": ["apply()", "revert()", "get_result()", "get_complexity()"],
    },
    "Verify": {
        "desc": "验证器（规则/复算/毒样例）",
        "attrs": ["id", "type", "version", "rules", "config"],
        "methods": ["verify(claim)", "verify(evidence)", "verify(attack)", "get_rules()"],
    },
    "Authority": {
        "desc": "人审权威（第一原则：生成者不得兼任判断者）",
        "attrs": ["id", "type", "permissions", "audit_log"],
        "methods": ["authorize(claim)", "reject(claim)", "abstain(claim)", "get_audit_log()"],
    },
}

# 与现有工具的映射（现有实现 → QueYi Core 接口）
EXISTING_MAP = {
    "gate_engine": "Verify（规则层验证器）",
    "atom_evidence_replay": "Evidence（证据复算/复现）",
    "poison_drill": "Attack（毒样例攻击面 + 回归）",
    "tool_integrity": "Verify（信任根/尺子完整性）",
    "weighted_af_solver": "Claim（论证图判决：IN/OUT/UNRESOLVED）",
    "human_review_queue": "Authority（人审队列）",
    "authority_log_620": "Authority（决策审计日志）",
    "pck_certificate_verifier_619": "Evidence（PCK 证书验证）",
}

# 接口关系（有向）
RELATIONS = [
    ("Claim", "Evidence", "claim 引用 evidence_refs"),
    ("Attack", "Claim", "attack 扰动 claim"),
    ("Attack", "Evidence", "attack 扰动 evidence"),
    ("Verify", "Claim", "verify 判定 claim"),
    ("Verify", "Evidence", "verify 判定 evidence"),
    ("Verify", "Attack", "verify 判定 attack 是否被挡"),
    ("Authority", "Claim", "authorize/reject/abstain claim"),
]

# 626 实现计划（先做哪个）
IMPL_PLAN = [
    ("Evidence", "先实现（replay/PCK 已近接口）"),
    ("Verify", "其次（gate/integrity 已具备）"),
    ("Claim", "再次（论证图/原子卡已有数据）"),
    ("Attack", "随后（沙箱 apply API 已具备）"),
    ("Authority", "最后（涉及人审治理）"),
]


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("5 个接口", set(INTERFACES) == {"Claim", "Evidence", "Attack", "Verify", "Authority"})
    chk("每接口有 attrs+methods", all(v["attrs"] and v["methods"] for v in INTERFACES.values()))
    chk("版本 v0.1", VERSION == "v0.1")
    chk("映射非空", len(EXISTING_MAP) >= 6)
    chk("关系图非空", len(RELATIONS) >= 5)
    chk("实现计划含 5 接口", {x[0] for x in IMPL_PLAN} == set(INTERFACES))
    print(f"C2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def render() -> str:
    L = ["# 625 C2 · QueYi Core 核心接口抽象设计（v0.1 · 设计版）", "",
         f"> 接口版本 **{VERSION}**（设计版）；626 为实现版。**只设计不实现**。", "",
         "## 一、核心接口", ""]
    for name, spec in INTERFACES.items():
        L += [f"### {name} —— {spec['desc']}", "",
              "- 属性：" + " / ".join(f"`{a}`" for a in spec["attrs"]),
              "- 方法：" + " / ".join(f"`{m}`" for m in spec["methods"]), ""]
    L += ["## 二、接口关系图", "", "```"]
    for a, b, why in RELATIONS:
        L.append(f"{a} --> {b}   // {why}")
    L += ["```", "", "## 三、与现有工具的映射", "", "| 现有工具 | QueYi Core 接口 |", "|---|---|"]
    for k, v in EXISTING_MAP.items():
        L.append(f"| `{k}` | {v} |")
    L += ["", "## 四、626 实现计划", "", "| 顺序 | 接口 | 理由 |", "|---|---|---|"]
    for i, (name, why) in enumerate(IMPL_PLAN, 1):
        L.append(f"| {i} | {name} | {why} |")
    L += ["", "## 五、局限性声明", "",
          "1. v0.1 为**设计草案**，未落地为 Python `Protocol`/抽象基类。",
          "2. 映射为**语义映射**，现有实现未必严格满足接口契约（626 逐项对齐）。",
          "3. 未定义跨靶场（C++/数学/嵌入式）的差异化实现细节。", ""]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 C2 QueYi Core 接口设计")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        p = os.path.join(ROOT, "data", "queyi_core_interface_design_625.md")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render())
        print(f"written {p}")
        return 0
    print(json.dumps({"version": VERSION, "interfaces": list(INTERFACES),
                      "mapped": list(EXISTING_MAP)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
