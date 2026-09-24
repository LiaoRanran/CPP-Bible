"""632 E1 · 探针 #2：向量 **L4.2 阈值边界歧义**（P1，此前无探针）

向量定义（`data/attack_surface_taxonomy.md` L4.2）：规则用 `>` 还是 `>=`、
四舍五入方向未定义 ⇒ 边界样本判决不稳定。

**探针性质（诚实说明）**：当前仓库无 L4.2 专用运行时检测器，故本探针是
**结构性覆盖探针**——静态解析 `tools/gate_engine.py` 中所有 `check_*` 规则函数，
找出含数值阈值比较的规则，并判断其边界算子（`>`/`>=`/`<`/`<=`）是否**显式说明**
（函数 docstring / 邻近注释提及边界、阈值或算子方向）。

- 阈值规则数 `threshold_rules`
- 其中边界被显式说明的 `documented`
- 其中未说明的 `undocumented`（即潜在"边界歧义"漏洞面）

机制存在 = 阈值规则普遍显式说明边界方向。否则登记为覆盖缺口。

**只读**：只解析源码文本，零改写（`--check` 不写报告）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

GATE = os.path.join(ROOT, "tools", "gate_engine.py")
OUT_MD = os.path.join(ROOT, "data", "coverage_probe_l4_2_632.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_probe_l4_2_632.json")

_CMP_RE = re.compile(r"(>=|<=|==|!=|>|<)\s*(\d+)|(\d+)\s*(>=|<=|==|!=|>|<)")
_OP_RE = re.compile(r"(>=|<=|==|!=|>|<)")
_DOC_HINT_RE = re.compile(r"(边界|阈值|threshold|boundary|direction|方向|四舍五入|向上取整|向下取整|inclusive|exclusive)", re.IGNORECASE)


def _split_functions(src: str) -> list[str]:
    """按 `def check_` 切分函数体（到下一个 `def check_` 或文末为止）。"""
    starts = [m.start() for m in re.finditer(r"def\s+check_\w+\s*\(", src)]
    funcs: list[str] = []
    for i, s in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(src)
        colon = src.find(":", s)
        if colon == -1 or colon > end:
            continue
        funcs.append(src[colon + 1:end])
    return funcs


def analyze_threshold(body: str) -> dict[str, Any]:
    ops = set(_OP_RE.findall(body))
    has_cmp = bool(_CMP_RE.search(body))
    # docstring / 注释里是否说明边界（在整个函数体内检索）
    documented = bool(_DOC_HINT_RE.search(body))
    return {"has_threshold": has_cmp, "operators": sorted(ops),
            "boundary_documented": documented}


def measure() -> dict[str, Any]:
    out: dict[str, Any] = {
        "vector": "L4.2", "name": "阈值边界歧义",
        "gate_exists": os.path.exists(GATE), "rules": [],
    }
    if not out["gate_exists"]:
        out["error"] = "gate_engine.py 不存在"
        return out
    src = open(GATE, encoding="utf-8", errors="replace").read()
    bodies = _split_functions(src)
    thr = 0
    documented = 0
    undoc: list[str] = []
    for b in bodies:
        a = analyze_threshold(b)
        if a["has_threshold"]:
            thr += 1
            if a["boundary_documented"]:
                documented += 1
            else:
                undoc.append(a["operators"])
    out["threshold_rules"] = thr
    out["documented_boundaries"] = documented
    out["undocumented_boundaries"] = thr - documented
    out["undocumented_examples"] = undoc[:10]
    out["mechanism_present"] = (thr > 0) and (documented == thr)
    return out


def write_report() -> str:
    m = measure()
    lines = ["# 632 E1 · 探针 #2：L4.2 阈值边界歧义", "",
             "- 解析 `tools/gate_engine.py` 中的 `check_*` 规则函数",
             f"- 含数值阈值比较的规则：**{m.get('threshold_rules', 0)}** 条",
             f"- 边界算子被显式说明：**{m.get('documented_boundaries', 0)}** 条",
             f"- 边界**未**说明（潜在歧义面）：**{m.get('undocumented_boundaries', 0)}** 条", "",
             "## 机制评估", "",
             f"- **机制总体：{'存在（阈值规则均显式说明边界）' if m.get('mechanism_present') else '存在缺口（部分阈值规则边界未说明）'}**", "",
             "## 诚实登记", "",
             "1. 本探针是**结构性覆盖探针**：静态解析规则源码，不动态复现边界攻击"
             "（当前无 L4.2 专用运行时检测器，无法动态复现）；",
             "2. 「边界被显式说明」按 docstring/注释是否出现 边界/阈值/方向/inclusive 等词判定，"
             "是**启发式**口径，可能漏判默默写明在代码逻辑里、但注释未点明的边界；",
             "3. 即便边界算子被说明，探针**不验证**「n-1/n/n+1 三样本判决单调」这一更严格的稳定性"
             "（需运行 gate 三样本比对，属动态口径，本批未做）；",
             "4. 真实判决稳定性需结合具体规则取值，建议后续补「边界差分」动态探针。"]
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

    # 1) 合成源码：含一个未说明边界的阈值规则 + 一个已说明的
    src = (
        "def check_a(self):\n    return n > 2\n"
        "def check_b(self):\n    # 边界：>= 3 视为达标（inclusive）\n    return n >= 3\n"
    )
    bodies = _split_functions(src)
    a = analyze_threshold(bodies[0])
    b = analyze_threshold(bodies[1])
    chk("切分得到 2 个函数", len(bodies) == 2, f"({len(bodies)})")
    chk("未说明边界被识别为未说明", a["has_threshold"] and not a["boundary_documented"])
    chk("已说明边界被识别为已说明", b["has_threshold"] and b["boundary_documented"])

    # 2) 真实仓库口径
    m = measure()
    chk("measure 返回 vector=L4.2", m.get("vector") == "L4.2")
    chk("measure 含 threshold_rules", "threshold_rules" in m)
    chk("报告路径在 data 下（--check 不写）",
        OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="632 E1 探针 L4.2 阈值边界歧义")
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
    print(f"threshold_rules={m.get('threshold_rules')} "
          f"documented={m.get('documented_boundaries')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
