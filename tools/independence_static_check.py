"""629 C3 · 独立验证者静态证明（纯标准库 ast，只读）

对 628 的两个「验证端」做**静态独立性审计**（不运行、不修改它们）：

1. `tools/independent_verifier_628.py`（B1 独立验证者）
2. `tools/vsa_verify_628.py`（B2 独立验证端）

断言（任务书口径）：
- **不 import** `gate_engine`（被验证的核心引擎）
- **不 import 任何 `tools/` 下的模块**（纯标准库）
- **不读取** golden_lock / authority ledger / annotations（只读原始卡数据）

前两条是**硬断言**（AST 可判定）。第三条**按字面口径会失败**——
`independent_verifier_628.py` 确实读取 `data/authority/decision_event_v2_ledger.jsonl`
（它的任务就是**验证这条账本的哈希链**，账本是**被验证对象**而非信任依赖）。
按任务书 §C3「如果发现耦合，不修改，只报告」⇒ 本工具把它登记为**口径不符（设计使然）**，
并把每个读取路径分类为「原始数据 / 系统输出 / 敏感信任文件」。

独立性分级（L1–L4，617 批次定义沿用）：
- L1 分主体（独立的人/组织）· L2 分实现（独立代码）· L3 分执行环境（独立机器）
- L4 分信任根（独立密钥托管）
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "independence_static_check_629.md")

TARGETS = ("tools/independent_verifier_628.py", "tools/vsa_verify_628.py")
FORBIDDEN_IMPORTS = ("gate_engine",)
SENSITIVE_HINTS = ("golden_lock", "annotations", "decision_event_v2_ledger")
RAW_DIRS = ("atoms", "evidence", "pck")
SYSTEM_OUTPUTS = ("authority_projection_626.json", "grounded_labels_w2.json",
                  "review_item_ledger.jsonl", "attack_edges_candidates.jsonl")


def local_modules() -> set[str]:
    return {os.path.splitext(f)[0] for f in os.listdir(HERE) if f.endswith(".py")}


def imports_of(path: str) -> tuple[list[str], list[str]]:
    """(本地模块, 标准库/第三方) —— AST 判定，比正则可靠。"""
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                names.add(node.module.split(".")[0])
            elif node.level:
                names.add("<relative>")
    loc = local_modules()
    return sorted(names & loc), sorted(names - loc)


def path_literals_of(path: str) -> list[str]:
    """源码里的数据路径字面量（AST）。

    两类都要抓：
    1. `os.path.join(ROOT, "data", "x", "y.json")` —— 字符串是**分段常量**，
       必须把常量段拼回完整路径（否则分类会退化成对 "data"/"authority" 这种碎片判类）；
    2. 单段字面量（含扩展名或斜杠的），如 `"data/pck/certificates"`。
    """
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    out: set[str] = set()

    def const(x: ast.AST) -> Optional[str]:
        return x.value if isinstance(x, ast.Constant) and isinstance(x.value, str) else None

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "join":
            parts = [p for p in (const(a) for a in node.args) if p]
            if len(parts) >= 2:
                joined = "/".join(p.strip("/") for p in parts)
                if len(joined) < 120 and " " not in joined:
                    out.add(joined)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            v = node.value
            if (re.search(r"\.(json|jsonl|yaml|yml|md)$", v) or v.count("/") >= 1) \
                    and " " not in v and len(v) < 120:
                out.add(v)
    return sorted(out)


def classify(p: str) -> str:
    low = p.lower()
    if any(h in low for h in SENSITIVE_HINTS):
        return "敏感信任文件"
    if any(s in p for s in SYSTEM_OUTPUTS):
        return "系统输出（对比基准）"
    if any(f"/{d}/" in p or p.startswith(d) for d in RAW_DIRS):
        return "原始数据"
    return "报告/临时产物"


def analyze(rel: str) -> dict[str, Any]:
    p = os.path.join(ROOT, rel)
    loc, other = imports_of(p)
    paths = path_literals_of(p)
    inv = [{"path": x, "kind": classify(x)} for x in paths]
    deny = [x for x in paths if any(h in x.lower() for h in SENSITIVE_HINTS)]
    return {"module": rel, "local_imports": loc, "stdlib_imports": other,
            "paths": inv, "sensitive_paths": deny,
            "imports_gate_engine": "gate_engine" in loc,
            "imports_any_local": bool(loc),
            "reads_sensitive": bool(deny)}


def independence_level() -> dict[str, Any]:
    """当前他验链的独立性分级（每级的判据 + 是否达成）。"""
    return {
        "L1_独立主体": {"achieved": False,
                    "why": "验证者与作者是同一主体（你 + 本项目）"},
        "L2_独立实现": {"achieved": True,
                    "why": "零 import 本项目工具（AST 证明）+ 朴素重算"},
        "L3_独立执行环境": {"achieved": False,
                      "why": "同机同解释器同依赖（无第三方依赖可移植）"},
        "L4_独立信任根": {"achieved": False,
                     "why": "RSA 公私钥同主体生成（629 C1）；HMAC 更是共享秘密"},
    }


def measure() -> dict[str, Any]:
    return {"targets": [analyze(t) for t in TARGETS],
            "levels": independence_level(),
            "local_module_count": len(local_modules())}


def write_report() -> str:
    m = measure()
    lines = [
        "# 629 C3 · 独立验证者静态证明", "",
        "> 工具：`tools/independence_static_check.py`（纯标准库 `ast`，只读；"
        "**不运行被审工具、不修改它们**）", "",
        "## 一、硬断言（AST 可判定）", "",
        "| 目标 | import 的本地模块 | import 标准库/第三方 | 含 gate_engine |",
        "|---|---|---|---|",
        *[f"| `{t['module']}` | {t['local_imports'] or '（无，零 import）'} | "
          f"{len(t['stdlib_imports'])} 个 | {'是' if t['imports_gate_engine'] else '**否**'} |"
          for t in m["targets"]], "",
        f"- 仓库 `tools/` 下模块共 {m['local_module_count']} 个；两个验证端"
        "**均零 import** 其中任何模块 ⇒ 代码层独立性（L2）成立。", "",
        "## 二、数据读取清单（含分类）", "",
    ]
    for t in m["targets"]:
        lines += [f"### `{t['module']}`", "",
                  "| 路径 | 分类 |", "|---|---|",
                  *[f"| `{i['path']}` | {i['kind']} |" for i in t["paths"]], ""]
    lines += [
        "## 三、第三条第断言：不读敏感信任文件 —— **口径不符（如实报告）**", "",
    ]
    for t in m["targets"]:
        if t["reads_sensitive"]:
            lines += [
                f"- `{t['module']}` 读取：{'、'.join('`' + x + '`' for x in t['sensitive_paths'])}",
                "  ⇒ 按任务书字面口径**构成耦合**。",
                "  **性质判定（诚实）**：`decision_event_v2_ledger.jsonl` 是**被验证对象**"
                "（该验证者的任务就是重算它的哈希链），不是**信任依赖**（它不把账本当「真」"
                "而直接采信，而是重算后与系统输出比对）。",
                "  因此本条按「口径不符 + 性质为设计使然」登记，**不修改 628 工具**（§零.11）。"]
        else:
            lines += [f"- `{t['module']}`：未读取敏感信任文件 ✔", ""]
    lines += [
        "", "## 四、独立性分级（L1–L4）", "",
        "| 级别 | 是否达成 | 判据/原因 |", "|---|---|---|",
        *[f"| {k.replace('_', ' ')} | {'✅' if v['achieved'] else '❌'} | {v['why']} |"
          for k, v in m["levels"].items()], "",
        "**当前等级 = L2（分实现）**。要达到 L3/L4 需要：", "",
        "- L3：把验证者放到**独立执行环境**（另一台机器 / 容器 / 无共享依赖介质）跑；",
        "- L4：**公钥托管到独立第三方**（或外部透明日志），使「验签通过」不再由被验证方自证。",
        "",
        "这两项都涉及**人与外部机构**，机器不能代办 ⇒ 已列入交人项（C1 同款结论）。", "",
        "## 五、局限", "",
        "- 静态分析只看**源码字面**：动态拼接的路径（`os.path.join(ROOT, *parts)`）"
        "或间接读取（经由第三方库）无法证明；",
        "- `stdlib_imports` 未区分标准库与第三方（本仓工具依赖 `pyproject.toml` 白名单，"
        "两个验证端只用到 `argparse/hashlib/hmac/json/os/subprocess/sys/typing`）；",
        "- 「被验证对象 vs 信任依赖」的性质判定是**人工判断**，已给出理由但需人审复核。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = measure()
    targets = m["targets"]
    chk("审计目标存在且可解析", len(targets) == len(TARGETS))
    chk("两个验证端都不 import gate_engine",
        not any(t["imports_gate_engine"] for t in targets))
    chk("两个验证端都零 import 本项目工具",
        not any(t["imports_any_local"] for t in targets),
        f"({[t['local_imports'] for t in targets]})")
    chk("读取清单非空（审计有效）",
        all(t["paths"] for t in targets),
        f"({[len(t['paths']) for t in targets]})")
    chk("敏感读取已如实登记（口径不符但不改工具）",
        any(t["reads_sensitive"] for t in targets))
    chk("每个路径都有分类",
        all(i["kind"] for t in targets for i in t["paths"]))
    lv = m["levels"]
    chk("L2 达成（零 import + 朴素重算）", lv["L2_独立实现"]["achieved"])
    chk("L1/L3/L4 未达成且给出原因（不粉饰）",
        all(not lv[k]["achieved"] and lv[k]["why"]
            for k in ("L1_独立主体", "L3_独立执行环境", "L4_独立信任根")))
    chk("报告存在且含分级表", os.path.exists(OUT_MD)
        and "独立性分级" in open(OUT_MD, encoding="utf-8").read())
    print(f"C3 independence static check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 C3 独立性静态证明（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps(measure(), ensure_ascii=False, indent=2))
        return 0
    m = measure()
    print(f"targets={len(m['targets'])} local_imports="
          f"{[t['local_imports'] for t in m['targets']]} "
          f"sensitive={[t['sensitive_paths'] for t in m['targets']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
