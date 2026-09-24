"""632 E1 · 探针 #3：向量 **L4.4 规则优先级冲突**（P1，此前无探针）

向量定义（`data/attack_surface_taxonomy.md` L4.4）：两条规则对同一事实给出相反
结论（谁优先未定义）。

**探针性质（诚实说明）**：当前仓库无 L4.4 专用运行时检测器，故本探针是
**结构性覆盖探针**——静态解析 `tools/gate_engine.py` 中所有 `register(Rule(...))`
注册项，提取每条规则的 `id/severity/scope`，构造「同 scope 且同为 block/warn 级」
的潜在冲突规则对，并判断引擎是否定义了**显式的优先级/冲突解决策略**
（源码中出现 `priority`/`precedence`/`tie-break`/`conflict` 解决 或 具名优先级表）。

- `conflict_pairs`：潜在冲突对数量
- `global_policy_present`：引擎是否定义了显式冲突解决策略
- `pairs_resolved`：在策略存在时，冲突对视为「有解决依据」

机制存在 = 既存在潜在冲突对、又定义了显式解决策略。否则登记为覆盖缺口。

**只读**：只解析源码文本，零改写（`--check` 不写报告）。
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

GATE = os.path.join(ROOT, "tools", "gate_engine.py")
OUT_MD = os.path.join(ROOT, "data", "coverage_probe_l4_4_632.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_probe_l4_4_632.json")

_ID_RE = re.compile(r"id\s*=\s*[\"']([^\"']+)[\"']")
_SEV_RE = re.compile(r"severity\s*=\s*[\"']([^\"']+)[\"']")
_SCOPE_RE = re.compile(r"scope\s*=\s*[\"']([^\"']+)[\"']")
_POLICY_RE = re.compile(r"(?i)priority|precedence|tie[\s_-]?break|conflict[\s_-]?resol|ORDER\s*=")


def parse_rules(src: str) -> list[dict[str, str]]:
    chunks = src.split("register(Rule(")
    rules: list[dict[str, str]] = []
    for c in chunks[1:]:
        rid = _ID_RE.search(c)
        sev = _SEV_RE.search(c)
        scope = _SCOPE_RE.search(c)
        if not rid:
            continue
        rules.append({
            "id": rid.group(1),
            "severity": sev.group(1) if sev else "",
            "scope": scope.group(1) if scope else "",
        })
    return rules


def potential_conflicts(rules: list[dict[str, str]]) -> list[tuple[str, str]]:
    blockish = [r for r in rules if r["severity"] in ("block", "warn")]
    pairs = []
    for a, b in itertools.combinations(blockish, 2):
        if a["scope"] and a["scope"] == b["scope"]:
            pairs.append((a["id"], b["id"]))
    return pairs


def parse_rules_live() -> list[dict[str, str]]:
    """从权威来源 `gate_engine.RULES` 读取规则元数据（含 id/severity/scope）。"""
    import importlib
    mod = importlib.import_module("gate_engine")
    return [{"id": r.id, "severity": r.severity, "scope": r.scope}
            for r in getattr(mod, "RULES", [])]


def measure() -> dict[str, Any]:
    out: dict[str, Any] = {
        "vector": "L4.4", "name": "规则优先级冲突",
        "gate_exists": os.path.exists(GATE), "rules": [],
    }
    if not out["gate_exists"]:
        out["error"] = "gate_engine.py 不存在"
        return out
    # 优先用权威 RULES；导入失败则退回静态解析
    try:
        rules = parse_rules_live()
    except Exception:
        rules = parse_rules(open(GATE, encoding="utf-8", errors="replace").read())
    pairs = potential_conflicts(rules)
    policy = bool(_POLICY_RE.search(open(GATE, encoding="utf-8", errors="replace").read()))
    out["rules_parsed"] = len(rules)
    out["conflict_pairs"] = len(pairs)
    out["conflict_examples"] = pairs[:10]
    out["global_policy_present"] = policy
    out["pairs_resolved"] = len(pairs) if policy else 0
    out["mechanism_present"] = (len(pairs) > 0) and policy
    return out


def write_report() -> str:
    m = measure()
    lines = ["# 632 E1 · 探针 #3：L4.4 规则优先级冲突", "",
             f"- 解析 `tools/gate_engine.py` 中 `register(Rule(...))` 注册项：**{m.get('rules_parsed', 0)}** 条",
             f"- 同 scope 且同为 block/warn 级的潜在冲突对：**{m.get('conflict_pairs', 0)}** 对",
             f"- 引擎是否定义显式冲突解决策略：**{'是' if m.get('global_policy_present') else '否'}**",
             f"- 冲突对中有解决依据：**{m.get('pairs_resolved', 0)}** 对", "",
             "## 机制评估", "",
             f"- **机制总体：{'存在（定义了显式优先级/冲突解决策略）' if m.get('mechanism_present') else '存在缺口（潜在冲突对无显式优先级定义）'}**", "",
             "## 诚实登记", "",
             "1. 本探针是**结构性覆盖探针**：静态解析规则注册项，不动态复现「两规则相反结论」攻击"
             "（当前无 L4.4 专用运行时检测器，无法动态复现）；",
             "2. 「潜在冲突对」按「同 scope + 同为 block/warn 级」启发式构造，"
             "并未真正验证两条规则对**同一事实**给出相反结论（那需要语义分析）；",
             "3. `global_policy_present` 仅检测源码是否出现 priority/precedence/tie-break 等词，"
             "不保证该策略**正确覆盖**所有冲突对；",
             "4. 真实冲突解决是否完备，建议后续补「构造相反结论双规则卡 → 跑 gate 看判决」的动态探针。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 1) 合成源码：两条同 scope 同 severity 规则 + 一个优先级表
    src = (
        'register(Rule(id="EV-A", severity="block", scope="evidence"))\n'
        'register(Rule(id="EV-B", severity="block", scope="evidence"))\n'
        'register(Rule(id="AT-C", severity="warn", scope="atom"))\n'
        'PRIORITY = {"EV-A": 1, "EV-B": 2}\n'
    )
    rules = parse_rules(src)
    pairs = potential_conflicts(rules)
    chk("解析到 3 条规则", len(rules) == 3, f"({len(rules)})")
    chk("构造出 1 个冲突对", len(pairs) == 1, f"({pairs})")
    chk("优先级策略被识别", bool(_POLICY_RE.search(src)))

    # 2) 真实仓库口径
    m = measure()
    chk("measure 返回 vector=L4.4", m.get("vector") == "L4.4")
    chk("measure 含 conflict_pairs", "conflict_pairs" in m)
    chk("报告路径在 data 下（--check 不写）",
        OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="632 E1 探针 L4.4 规则优先级冲突")
    ap.add_argument("--check", action="store_true", help="只读自检（不写报告）")
    ap.add_argument("--report", action="store_true", help="写探针报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"conflict_pairs={m.get('conflict_pairs')} "
          f"policy={m.get('global_policy_present')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
