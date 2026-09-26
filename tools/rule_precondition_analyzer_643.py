"""643 C1 · **规则 precondition 分析器**（智能层：自动生成攻击 #1）。

**定位**：对 67 条规则，自动分析"**它需要什么才能触发**"，产出
**每规则的 precondition 描述 + 盲点列表** —— 这是 C2 定向变异的输入。

**⚠️ 根本限制（必须先说清）**：本仓的规则触达条件是**内嵌闭包**（`Rule.check` 是函数对象，
`gate_engine.py` 里没有声明式 `precondition` 字段）⇒ 本工具只能做**静态近似**：
- **AST 解析** `gate_engine.py`，把规则 id 与它的 `check` 函数名对上（两种注册形态都支持：
  4 元组 `(id, title, scope, fn)` 与 `register(Rule(id, ...))`）；
- 再 AST 解析该函数的函数体，收集**信号**：引用的**字段名**、`re` 调用、数值常量、
  跨卡扫描（循环/rglob）、跨卡引用；
- 用信号**推断** precondition 与盲点（判据见 `BLIND_RULES`）。

**盲点判据（启发式，逐条标来源）**：

| 盲点 | 判据 | 为什么可能是盲点 |
|---|---|---|
| `field_missing_silent` | 规则引用了字段 F，但**没有**"F 缺失即报"的分支 | F 缺失时规则**静默跳过**（正是 616 的 179 条 N/A 的一类成因） |
| `regex_fragile` | 函数体里有 `re.compile/match/search/fullmatch` | 正则被**格式微扰**绕过 |
| `numeric_threshold` | 函数体里有数值常量比较 | 值篡改**刚好压线**可绕过 |
| `cross_card_dependency` | 函数体里有对其它卡/目录的遍历 | 单卡损伤**不触发**（需配对卡才报） |
| `path_scope_only` | `scope == "repo"` | 与单卡变异**不同量纲**，C2 生成时要降权 |

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_rule_precondition.md` + `.json`。
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

import gate_engine as ge  # noqa: E402

GE_SRC = os.path.join(HERE, "gate_engine.py")
OUT_MD = os.path.join(ROOT, "data", "643_rule_precondition.md")
OUT_JSON = os.path.join(ROOT, "data", "643_rule_precondition.json")

#: 卡片/证据的已知字段名（用于从字符串字面量里识别"这规则在动哪些字段"）
KNOWN_FIELDS = ("id", "title", "domain", "type", "status", "claim", "claim_boundary",
                "relations", "evidence", "sources", "first_hand", "superiority", "depth",
                "pedagogy", "status_history", "dal", "serves", "artifact",
                "artifact_sha256", "assert", "falsification", "negative_controls",
                "env_dependent", "key", "value", "run_match", "expected_key", "tau",
                "observations", "n_observations", "card_id", "target", "kind")
NUMERIC_HINT = ("tau", "threshold", "limit", "min", "max", "60", "0.3", "0.5")


def rule_check_map(src: str) -> dict[str, str]:
    """从 `gate_engine.py` 源码里抽出 `rule_id -> check 函数名`（两种注册形态）。"""
    tree = ast.parse(src)
    out: dict[str, str] = {}
    for node in ast.walk(tree):
        # 形态 A：register(Rule("ID", ..., check=fn))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "Rule" and node.args:
            rid = _str_const(node.args[0])
            chk = next((kw.value for kw in node.keywords if kw.arg == "check"), None)
            if rid and isinstance(chk, ast.Name):
                out[rid] = chk.id
        # 形态 B：4 元组 ("ID", "title", "scope", fn)
        if isinstance(node, ast.Tuple) and len(node.elts) == 4:
            rid = _str_const(node.elts[0])
            fn = node.elts[3]
            if rid and isinstance(node.elts[1], ast.Constant) and isinstance(fn, ast.Name):
                out.setdefault(rid, fn.id)
    return out


def _str_const(n: ast.AST) -> Optional[str]:
    if isinstance(n, ast.Constant) and isinstance(n.value, str):
        return n.value
    return None


def function_index(src: str) -> dict[str, ast.AST]:
    tree = ast.parse(src)
    out: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[node.name] = node
    return out


def signals(fn: Optional[ast.AST]) -> dict[str, Any]:
    """AST 扫描一个 check 函数体，收集 precondition 信号（纯函数，可测）。"""
    sig: dict[str, Any] = {"fields": [], "regex_calls": 0, "numeric_consts": [],
                           "loops": 0, "iterdir_calls": 0, "lines": 0}
    if fn is None:
        return sig
    sig["lines"] = int(getattr(fn, "end_lineno", 0) or 0) - int(getattr(fn, "lineno", 0) or 0)
    fields: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for f in KNOWN_FIELDS:
                if f == node.value or f in node.value.split():
                    fields.add(f)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in ("match", "search", "fullmatch", "compile"):
                sig["regex_calls"] += 1
            if node.func.attr in ("iterdir", "rglob", "glob", "walk"):
                sig["iterdir_calls"] += 1
        if isinstance(node, (ast.For, ast.While)):
            sig["loops"] += 1
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool):
            if node.value not in (0, 1):
                sig["numeric_consts"].append(node.value)
    sig["fields"] = sorted(fields)
    sig["numeric_consts"] = sorted({round(float(x), 4) for x in sig["numeric_consts"]})[:8]
    return sig


def blind_spots(sig: dict[str, Any], scope: str) -> list[dict[str, str]]:
    """由信号推出盲点（纯函数）。**每条都标 why，便于人核。**"""
    out: list[dict[str, str]] = []
    if sig["fields"]:
        out.append({"kind": "field_missing_silent",
                    "why": f"规则引用字段 {', '.join(sig['fields'][:4])}"
                           f"{' …' if len(sig['fields']) > 4 else ''}；"
                           "若这些字段缺失而规则没有「缺失即报」分支 ⇒ 静默跳过"})
    if sig["regex_calls"]:
        out.append({"kind": "regex_fragile",
                    "why": f"函数体有 {sig['regex_calls']} 处正则调用 ⇒ 格式微扰可能绕过"})
    if sig["numeric_consts"]:
        out.append({"kind": "numeric_threshold",
                    "why": f"数值常量 {sig['numeric_consts']} ⇒ 值篡改可能刚好压线"})
    if sig["loops"] or sig["iterdir_calls"]:
        out.append({"kind": "cross_card_dependency",
                    "why": f"循环 {sig['loops']} 处 / 目录遍历 {sig['iterdir_calls']} 处"
                           " ⇒ 单卡损伤可能不触发"})
    if scope == "repo":
        out.append({"kind": "path_scope_only",
                    "why": "scope=repo ⇒ 与单卡变异不同量纲，C2 生成时应降权"})
    return out


def analyze() -> dict[str, Any]:
    src = open(GE_SRC, encoding="utf-8", errors="replace").read()
    cmap = rule_check_map(src)
    fmap = function_index(src)
    rows = []
    for r in ge.RULES:
        fn_name = cmap.get(r.id)
        sig = signals(fmap.get(fn_name) if fn_name else None)
        rows.append({"rule_id": r.id, "title": r.title, "severity": r.severity,
                     "scope": r.scope, "kind": r.kind, "quadrant": r.quadrant,
                     "check_fn": fn_name, "signals": sig,
                     "blind_spots": blind_spots(sig, r.scope),
                     "precondition": {
                         "scope": r.scope,
                         "fields": sig["fields"],
                         "needs_cross_card": bool(sig["loops"] or sig["iterdir_calls"]),
                         "has_regex": sig["regex_calls"] > 0,
                         "has_numeric_threshold": bool(sig["numeric_consts"]),
                     }})
    mapped = sum(1 for x in rows if x["check_fn"])
    blind_by_kind: dict[str, int] = {}
    for x in rows:
        for b in x["blind_spots"]:
            blind_by_kind[b["kind"]] = blind_by_kind.get(b["kind"], 0) + 1
    return {"rows": rows, "n_rules": len(rows), "n_mapped": mapped,
            "n_unmapped": len(rows) - mapped, "blind_by_kind": blind_by_kind,
            "no_blind_spot": [x["rule_id"] for x in rows if not x["blind_spots"]],
            "fields_histogram": _histo(rows)}


def _histo(rows: list[dict[str, Any]]) -> dict[str, int]:
    h: dict[str, int] = {}
    for r in rows:
        for f in r["signals"]["fields"]:
            h[f] = h.get(f, 0) + 1
    return dict(sorted(h.items(), key=lambda kv: (-kv[1], kv[0])))


def write_report() -> str:
    a = analyze()
    lines = [
        "# 643 C1 · 规则 precondition 分析（智能层：自动生成攻击 #1）", "",
        f"> 规模：**{a['n_rules']} 条规则**；成功映射到 `check` 函数 **{a['n_mapped']}** 条，"
        f"未映射 **{a['n_unmapped']}** 条。",
        "> **限制**：规则条件是**内嵌闭包**（无声明式 precondition）⇒ 本分析是**静态近似**，"
        "不是语义解析。", "",
        "## 一、盲点分布", "",
        "| 盲点类别 | 规则数 | 含义 |", "|---|---|---|"]
    meaning = {"field_missing_silent": "引用字段但可能没有「缺失即报」分支 ⇒ 静默跳过",
               "regex_fragile": "正则可被格式微扰绕过",
               "numeric_threshold": "数值阈值可被压线值绕过",
               "cross_card_dependency": "依赖跨卡/目录遍历 ⇒ 单卡损伤不触发",
               "path_scope_only": "scope=repo ⇒ 与单卡变异不同量纲"}
    for k, n in sorted(a["blind_by_kind"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| `{k}` | **{n}** | {meaning.get(k, '')} |")
    lines += ["", f"**零盲点规则**（{len(a['no_blind_spot'])} 条）："
              f"{', '.join('`%s`' % x for x in a['no_blind_spot']) or '（无）'}", "",
              "## 二、字段引用直方图（被最多规则引用的字段 = 攻击面最集中的字段）", "",
              "| 字段 | 引用它的规则数 |", "|---|---|"]
    for f, n in list(a["fields_histogram"].items())[:20]:
        lines.append(f"| `{f}` | {n} |")
    lines += ["", "## 三、逐规则 precondition + 盲点", "",
              "| 规则 | 级别 | scope | check 函数 | 引用字段 | 跨卡 | 正则 | 数值阈值 | 盲点数 |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in a["rows"]:
        p = r["precondition"]
        lines.append(f"| `{r['rule_id']}` | {r['severity']} | {r['scope']} | "
                     f"`{r['check_fn'] or '—'}` | {', '.join(p['fields'][:4]) or '—'} | "
                     f"{'✅' if p['needs_cross_card'] else '—'} | "
                     f"{'✅' if p['has_regex'] else '—'} | "
                     f"{'✅' if p['has_numeric_threshold'] else '—'} | "
                     f"{len(r['blind_spots'])} |")
    lines += ["", "## 四、盲点明细（逐条 why）", "",
              "| 规则 | 盲点 | 理由 |", "|---|---|---|"]
    for r in a["rows"]:
        for b in r["blind_spots"]:
            lines.append(f"| `{r['rule_id']}` | `{b['kind']}` | {b['why']} |")
    lines += ["", "## 诚实登记", "",
              "1. **静态近似 ≠ 真实 precondition**：规则条件是闭包，本工具只能看"
              "**字符串字面量/调用形态/数值常量**；`fields` 的识别依赖内置字段名表，"
              "**可能漏**（自定义字段名不在表内）也可能**误收**（注释/消息文本里的词）；",
              "2. **盲点是「可能性」不是「已证缺陷」**：`field_missing_silent` 只说明"
              "「引用字段」这一事实，**没有**证明该规则缺「缺失即报」分支"
              "（要证明需逐规则读代码）⇒ 全部盲点必须人核后才可作为 C2 的目标；",
              "3. **未映射的规则**（`n_unmapped>0`）说明注册形态超出本工具的两种模式，"
              "它们**没有** precondition 分析结果 ⇒ C2 应跳过；",
              "4. 本工具**只读** `gate_engine.py`：不改规则、不重钉台账、不生成任何攻击。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    src = ('register(Rule("R-A", "t", "fact", "programmatic", "block", "atom", '
           'check=check_a))\n'
           'rows = [("R-B", "t2", "atom", check_b)]\n'
           'def check_a():\n'
           '    if card.get("status") and re.match("x", s):\n'
           '        return []\n'
           '    for c in _cards(ATOMS, "*.md"):\n'
           '        if len(c) > 60:\n'
           '            return []\n'
           'def check_b():\n'
           '    return []\n')
    cm = rule_check_map(src)
    chk("形态 A（Rule(...)）解析", cm.get("R-A") == "check_a", str(cm))
    chk("形态 B（4 元组）解析", cm.get("R-B") == "check_b", str(cm))

    fmap = function_index(src)
    sg = signals(fmap["check_a"])
    chk("识别字段引用（status）", "status" in sg["fields"], str(sg["fields"]))
    chk("识别正则调用", sg["regex_calls"] >= 1, str(sg["regex_calls"]))
    chk("识别数值阈值（60）", 60.0 in sg["numeric_consts"], str(sg["numeric_consts"]))
    chk("识别跨卡遍历（循环/iterdir）", sg["loops"] >= 1)
    chk("空函数无信号", signals(None)["fields"] == [] and signals(None)["regex_calls"] == 0)

    bs = blind_spots(sg, "atom")
    kinds = {b["kind"] for b in bs}
    chk("盲点判据齐备（字段/正则/数值/跨卡）",
        {"field_missing_silent", "regex_fragile", "numeric_threshold",
         "cross_card_dependency"} <= kinds, str(kinds))
    chk("repo scope 追加 path_scope_only",
        any(b["kind"] == "path_scope_only" for b in blind_spots(sg, "repo")))
    chk("atom scope 不追加 path_scope_only",
        not any(b["kind"] == "path_scope_only" for b in bs))

    a = analyze()
    chk("67 规则在册", a["n_rules"] == 67, str(a["n_rules"]))
    chk("映射率过半", a["n_mapped"] >= 34, f"{a['n_mapped']}/{a['n_rules']}")
    chk("盲点统计自洽",
        sum(a["blind_by_kind"].values()) == sum(len(x["blind_spots"]) for x in a["rows"]))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 C1 规则 precondition 分析")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印分析（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = analyze()
    if x.json:
        print(json.dumps({"n_rules": a["n_rules"], "n_mapped": a["n_mapped"],
                          "blind_by_kind": a["blind_by_kind"],
                          "fields_histogram": a["fields_histogram"]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[precondition] {a['n_rules']} 规则（映射 {a['n_mapped']}）⇒ 盲点 "
          f"{a['blind_by_kind']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
