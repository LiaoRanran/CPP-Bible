"""642 B2 · 内核**最小性审计**（AST；只出报告，**不实际移代码**）。

审计对象：`tools/queyi_core_v10_641.py`（641 建成的协议内核 v1.0）。

审计五问（对应 v29 A4「最小可信计算基」）：

| # | 问题 | 判据 |
|---|---|---|
| 1 | 内核有领域依赖吗？ | 内核 import ∩ `FORBIDDEN_DOMAIN_MODULES` = ∅ |
| 2 | 内核有**非标准库**依赖吗？ | 内核 import ⊆ `sys.stdlib_module_names` ∪ {`__future__`} |
| 3 | 内核有**高攻击面**能力吗？（网络/子进程/动态执行） | 不含 `subprocess` / `socket` / `urllib` / `eval` / `exec` / `__import__` |
| 4 | 内核写盘面有多大？ | 写盘路径全部落在 `data/` 下的**声明常量**内 |
| 5 | 哪些符号属于「内核必须」，哪些**建议移出**？ | 逐符号分类 + 理由（`KERNEL_LAYERS` / `MOVE_OUT`） |

**铁律**：本模块**只读内核源码**，**不修改、不移动**任何代码（移代码留 643）。
结论里"建议移出"只是**建议**，不是已执行的动作。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_kernel_minimality_audit.md`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import queyi_core_v10_641 as core  # noqa: E402  （只读其常量做交叉核验）

OUT_MD = os.path.join(ROOT, "data", "642_kernel_minimality_audit.md")
KERNEL = os.path.join(HERE, "queyi_core_v10_641.py")
ADAPTERS = ("queyi_core_cpp_641.py", "queyi_core_toy_641.py")

#: 高攻击面能力（内核不该有）
DANGEROUS_NAMES = ("subprocess", "socket", "urllib", "http", "requests",
                   "eval", "exec", "compile", "__import__", "pickle", "ctypes")

#: 内核职责分层（641 设计文档 §层 表）
KERNEL_LAYERS: dict[str, str] = {
    "数据原语": "Artifact / ArtifactRef / Evidence / EvidenceResult / Decision",
    "运行协议": "VerificationRun / VerificationRunBuilder / _run_id / _run_integrity",
    "端口与插件契约": "VerifierPort / AttackerPort / AuthorityPort / EvidencePort / DomainPack",
    "投影层": "_PROJECTORS / register_projector / project / _p_summary / _p_manifest / _p_decisions",
    "通用规则引擎": "Rule / RuleOutcome / RuleEngine",
    "规范化与哈希": "canonical_json / digest_of / digest_bytes / canonicalize_content / _uri_norm",
    "不变量与自证": "module_imports / verify_no_domain_imports / kernel_self_digest",
    "报告与 CLI": "write_report / measure / selftest / main / _raises",
}

#: 建议移出清单（**只建议，不执行**）：符号 → (目标层, 理由)
MOVE_OUT: dict[str, tuple[str, str]] = {
    "write_report": ("CLI/报告层（内核外）",
                     "报告是**呈现**而非协议；内核只应产出投影，渲染交给 CLI 层"),
    "OUT_MD": ("CLI/报告层（内核外）", "同上：写盘路径常量属报告层"),
    "OUT_JSON": ("CLI/报告层（内核外）", "同上"),
    "RuleEngine": ("插件侧（待复核）",
                   "引擎本身通用（规则外置），但它只服务『判定』方向；若 643+ 出现规则模型"
                   "不同的第二/第三领域，应评估下沉为插件服务"),
}


def _src() -> str:
    return open(KERNEL, encoding="utf-8", errors="replace").read()


def _tree() -> ast.Module:
    return ast.parse(_src())


def imports_of(path: str) -> list[str]:
    """顶层与函数内全部 import 的**顶层模块名**（与 641 内核的口径一致，便于对照）。"""
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except (OSError, SyntaxError):
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module.split(".")[0])
    return sorted(set(names))


def symbols() -> dict[str, list[str]]:
    """顶层符号清单（class / function / constant）。"""
    tree = _tree()
    out: dict[str, list[str]] = {"classes": [], "functions": [], "constants": []}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            out["classes"].append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out["functions"].append(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out["constants"].append(t.id)
    return out


def code_stats() -> dict[str, int]:
    lines = _src().splitlines()
    blank = sum(1 for ln in lines if not ln.strip())
    comment = sum(1 for ln in lines if ln.strip().startswith("#"))
    doc = 0
    in_doc = False
    for ln in lines:
        s = ln.strip()
        if s.count('"""') == 1:
            in_doc = not in_doc
            doc += 1
            continue
        if in_doc or s.startswith('"""'):
            doc += 1
    return {"total": len(lines), "blank": blank, "comment": comment, "doc": doc,
            "code": len(lines) - blank - comment - doc}


def dangerous_uses() -> list[str]:
    """高攻击面符号的实际使用（import 或名字引用）。"""
    hits: set[str] = set(imports_of(KERNEL))
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Name) and node.id in DANGEROUS_NAMES:
            hits.add(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in DANGEROUS_NAMES:
            hits.add(node.attr)
    return sorted(h for h in hits if h in DANGEROUS_NAMES)


def write_paths() -> list[str]:
    """内核里 `open(..., "w")` 的目标表达式（只读源码文本，不求值）。"""
    out: list[str] = []
    for node in ast.walk(_tree()):
        if not isinstance(node, ast.Call):
            continue
        if not (isinstance(node.func, ast.Name) and node.func.id == "open"):
            continue
        mode = ""
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = str(kw.value.value)
        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
            mode = mode or str(node.args[1].value)
        if "w" in mode or "a" in mode:
            out.append(ast.unparse(node.args[0]) if node.args else "?")
    return sorted(set(out))


def audit() -> dict[str, Any]:
    imps = imports_of(KERNEL)
    stdlib = set(sys.stdlib_module_names)
    non_stdlib = sorted(m for m in imps if m not in stdlib and m != "__future__")
    domain = core.verify_no_domain_imports(KERNEL)
    sym = symbols()
    stats = code_stats()
    moved = [{"symbol": s, "target": t, "reason": r} for s, (t, r) in MOVE_OUT.items()]
    present = set(sym["classes"]) | set(sym["functions"]) | set(sym["constants"])
    keep = sorted(present - set(MOVE_OUT))
    return {
        "kernel": os.path.basename(KERNEL),
        "imports": imps, "domain_imports": domain, "non_stdlib_imports": non_stdlib,
        "forbidden_blacklist_size": len(core.FORBIDDEN_DOMAIN_MODULES),
        "dangerous": dangerous_uses(), "write_paths": write_paths(),
        "symbols": sym, "stats": stats,
        "n_symbols": len(present), "keep": keep, "move_out": moved,
        "layers": KERNEL_LAYERS,
        "adapters_import_kernel": {a: ("queyi_core_v10_641" in imports_of(os.path.join(HERE, a)))
                                   for a in ADAPTERS},
        "kernel_imports_adapters": sorted(set(imps) & set(ADAPTERS)),
    }


def write_report() -> str:
    a = audit()
    s = a["stats"]
    lines = [
        "# 642 B2 · 内核最小性审计（AST · 只出报告，**不实际移代码**）", "",
        f"> 审计对象：`tools/{a['kernel']}`（内核 v{core.SCHEMA_VERSION}）。"
        "本模块**只读源码**，未修改/移动任何代码。", "",
        "## 一、五问结论", "",
        "| # | 问题 | 结论 |", "|---|---|---|",
        f"| 1 | 领域依赖 | **{'零 ✅' if not a['domain_imports'] else a['domain_imports']}**"
        f"（黑名单 {a['forbidden_blacklist_size']} 个模块，AST 扫描） |",
        f"| 2 | 非标准库依赖 | **{'零 ✅' if not a['non_stdlib_imports'] else a['non_stdlib_imports']}** |",
        f"| 3 | 高攻击面能力 | **{'零 ✅' if not a['dangerous'] else a['dangerous']}**"
        "（无网络/子进程/动态执行/pickle/ctypes） |",
        f"| 4 | 写盘面 | `{a['write_paths']}`（全部在 `data/` 下的声明常量） |",
        f"| 5 | 建议移出 | **{len(a['move_out'])} 项**（见 §三） |", "",
        "## 二、内核功能清单（按 641 设计分层）", "",
        "| 层 | 内容 | 归属 |", "|---|---|---|"]
    for layer, content in a["layers"].items():
        own = "**内核必须**" if layer not in ("报告与 CLI",) else "**建议剥离到 CLI 层**"
        lines.append(f"| {layer} | {content} | {own} |")
    lines += ["", "### 2.1 统计", "",
              f"- 总行数 **{s['total']}**（代码 {s['code']} / 注释 {s['comment']} / "
              f"文档串 {s['doc']} / 空行 {s['blank']}）",
              f"- 顶层符号 **{a['n_symbols']}**（类 {len(a['symbols']['classes'])} / "
              f"函数 {len(a['symbols']['functions'])} / 常量 {len(a['symbols']['constants'])}）",
              f"- 内核 import：`{a['imports']}`", "",
              "### 2.2 依赖方向（双向核验）", "",
              "| 检查 | 结果 |", "|---|---|"]
    for k, v in a["adapters_import_kernel"].items():
        lines.append(f"| 适配器 `{k}` 是否 import 内核 | {'✅ 是' if v else '❌ 否'}（预期：是） |")
    lines.append(f"| 内核是否 import 适配器 | "
                 f"{'✅ 否' if not a['kernel_imports_adapters'] else '❌ 是：' + str(a['kernel_imports_adapters'])}"
                 "（预期：否） |")
    lines += ["", "## 三、建议移出清单（**只建议，不执行**；移代码留 643）", "",
              "| 符号 | 建议去向 | 理由 |", "|---|---|---|"]
    for m in a["move_out"]:
        lines.append(f"| `{m['symbol']}` | {m['target']} | {m['reason']} |")
    if not a["move_out"]:
        lines.append("| — | — | 无 |")
    lines += ["", "### 3.1 为什么「建议移出」只有这几项（诚实结论）", "",
              "内核里**没有**任何领域逻辑可移 —— 这不是「没查」，而是 AST 机械证明了：",
              "",
              f"1. 内核 import 集 `{a['imports']}` **全部是标准库**（无 gate_engine / poison_drill / "
              "authority_v2 等）；",
              "2. 领域知识只以**注入形式**出现（`RuleEngine.apply(evaluator=...)`、端口 ABC、"
              "投影注册表）；",
              f"3. 因此建议移出的 {len(a['move_out'])} 项都是**层次性**改进（报告层剥离、"
              "规则引擎归属复核），**不是**领域污染清理。", "",
              "## 四、诚实登记", "",
              "1. **只审计不修改**：本模块**未移动任何代码**（铁律 §七.5），"
              "「建议移出」仅为**建议**；",
              "2. 分类是**人工判据**（`KERNEL_LAYERS` / `MOVE_OUT` 常量），不是机器自动推断；"
              "换人会得出不同分层，但 §一 的四个机械判据（领域/非标准库/攻击面/写盘面）是客观的；",
              "3. `write_paths()` 用 `ast.unparse` 取**表达式文本**，不求值 ⇒ 若路径由变量间接拼接，"
              "仍可能漏判（本内核只有 2 个直接常量，风险低）；",
              "4. 本审计**不覆盖**「内核是否做对了事」（正确性），只覆盖"
              "「内核是否足够小 / 依赖是否干净」（最小性）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = audit()
    chk("内核存在", os.path.exists(KERNEL))
    chk("① 零领域 import", a["domain_imports"] == [], str(a["domain_imports"]))
    chk("② 零非标准库 import", a["non_stdlib_imports"] == [], str(a["non_stdlib_imports"]))
    chk("③ 零高攻击面能力", a["dangerous"] == [], str(a["dangerous"]))
    chk("④ 写盘面全在 data/", all(p in ("OUT_MD", "OUT_JSON") for p in a["write_paths"]),
        str(a["write_paths"]))
    chk("内核不 import 适配器", a["kernel_imports_adapters"] == [])
    chk("适配器确实 import 内核", all(a["adapters_import_kernel"].values()))
    chk("符号数 > 30", a["n_symbols"] > 30, str(a["n_symbols"]))
    chk("建议移出非空（报告层）", len(a["move_out"]) >= 3)
    chk("建议移出项都在内核里存在",
        all(m["symbol"] in (set(a["symbols"]["classes"]) | set(a["symbols"]["functions"])
                            | set(a["symbols"]["constants"])) for m in a["move_out"]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 B2 内核最小性审计")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写审计报告")
    ap.add_argument("--json", action="store_true", help="打印审计（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = audit()
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k != "layers"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[kernel-audit] {r['kernel']}：行 {r['stats']['total']}；符号 {r['n_symbols']}；"
          f"领域 import {len(r['domain_imports'])}；非标准库 import {len(r['non_stdlib_imports'])}；"
          f"高攻击面 {len(r['dangerous'])}；建议移出 {len(r['move_out'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
