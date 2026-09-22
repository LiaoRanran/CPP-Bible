"""623 E1 · 高复杂度带攻击面分析

**问题**（622 E2 Horizon 曲线）：高复杂度带（complexity 60-80+/80-100）只触发 **warn 级**规则
（M9 cross_reference 指向不存在目标 → 仅 `EV-SERVES-EXIST`(warn)，0% 被拦）。即高复杂度带
"无 block 级结构规则兜底"，攻击面在该带是**薄弱点**。

**本工具**：基于 622 E2 结论 + 623 A2/R3 实跑数据，量化高复杂度带攻击面：
- 哪些规则被高复杂度 mutation（H1-H4）触发、其 severity 分布；
- 高复杂度带"只 warn 不 block"的薄弱点清单；
- 给出 attack-surface 评分与加固建议（指向 E2 的 block 级规则）。

铁律：只读 gate 规则 + A2/R3 结果，不改任何受控文件。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any, cast

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_CACHE = os.path.join(ROOT, "data", "_gate_rules.json")
A2 = os.path.join(ROOT, "data", "high_complexity_sandbox_run_623.json")
R3 = os.path.join(ROOT, "data", "adversarial_loop_round3_sandbox_run_623.json")

# 622 E2 实测：高复杂度带只触发下列 warn 级规则（0% block 被拦）
HIGH_COMPLEXITY_WARN_ONLY = ["EV-SERVES-EXIST", "ATOM-REL-TARGET", "ATOM-REL-UNKNOWN"]


def load_rules() -> list[dict]:
    if os.path.exists(RULES_CACHE):
        return cast("list[dict[str, Any]]", json.load(open(RULES_CACHE, encoding="utf-8")))
    out = subprocess.check_output([sys.executable, "tools/gate_engine.py", "--list"],
                                  cwd=ROOT, text=True)
    import re
    rules = []
    for ln in out.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9-]+)\s+\S+\s+\S+\s+(block|warn|advice)\b", ln.strip())
        if m:
            rules.append({"rule": m.group(1), "severity": m.group(2)})
    return rules


def touched_rules() -> set[str]:
    s = set()
    for path in (A2, R3):
        res = json.load(open(path, encoding="utf-8"))
        for r in res["rows"]:
            s.update(r.get("new_block_rules", []))
            s.update(r.get("new_nonblock_rules", []))
    return s


def analyze() -> dict:
    rules = load_rules()
    touched = touched_rules()
    sev = {r["rule"]: r["severity"] for r in rules}

    # 高复杂度带薄弱点：本批高复杂度 mutation 触发的 warn 规则，且无对应 block 规则
    hc_warn_touched = [r for r in touched if sev.get(r) == "warn"]
    # 622 E2 指出的"只 warn 不 block"规则，本批是否被命中
    reproduced = [r for r in HIGH_COMPLEXITY_WARN_ONLY if r in touched]

    block_rules = [r["rule"] for r in rules if r["severity"] == "block"]
    block_touched = [r for r in block_rules if r in touched]

    # 攻击面评分：高复杂度带若只有 warn 兜底→弱；block 覆盖→强
    # 评分 = 高复杂度相关 block 规则触达数 / 高复杂度相关规则总数
    hc_related = set(HIGH_COMPLEXITY_WARN_ONLY) | set(block_touched)
    score = round(100.0 * len(block_touched) / max(1, len(hc_related)), 1)

    return {
        "total_rules": len(rules),
        "block_rules": len(block_rules),
        "warn_rules": sum(1 for r in rules if r["severity"] == "warn"),
        "touched_total": len(touched),
        "block_touched": sorted(block_touched),
        "hc_warn_touched": sorted(hc_warn_touched),
        "reproduced_622_e2": sorted(reproduced),
        "high_complexity_band_gap": "warn-only, no block structural rule",
        "attack_surface_score": score,
    }


def main():
    r = analyze()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return r


if __name__ == "__main__":
    main()
