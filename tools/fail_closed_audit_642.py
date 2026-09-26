"""642 B3 · fail-closed 全量审计（**只审计，不修复**）。

对照 641 D 线的「信任根缺失 ⇒ FAIL」口径，扫描全仓 **fail-open** 反模式：
**缺失 ⇒ warning**、**异常 ⇒ 通过**、**默认值 ⇒ 通过**、**校验失败 ⇒ 仅记录**。

三部分：

1. **已知点复核（可复现实测）**：GPT 审核指出的两处 ——
   `tool_integrity.verify_supply_chain()` 缺文件只警告不失败（**实测 exit=0**）、
   `DecisionEvent.from_dict({})` 用默认值补全（**实测空 dict ⇒ result=APPROVE、
   decision_origin=human_observed**，即最"信任假设"的默认）；
2. **全量模式扫描**（AST，高精度低噪声四条）：
   - FO-1 `except` 处理器直接 `return True/0/[]/{}`（**异常 ⇒ 通过**）；
   - FO-2 `if not os.path.exists(...)` ⇒ 直接 `return True/0`（**缺失 ⇒ 通过**）；
   - FO-3 关键字段用 `.get(key, 非 None 默认)`（**默认值 ⇒ 通过**）；
   - FO-4 校验结果里 `... if changed else 0` 形态（**warning 不影响退出码**）；
3. **清单 + 严重度 + 修复建议**（严重度按"能否让坏东西通过"分级，不按出现次数）。

**铁律**：本模块**不修改任何被审计代码**（修复留 643 或本批末尾若人授权）。
**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/642_fail_open_audit.md` + `.json`。
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

import decision_event_v2_626 as de  # noqa: E402  （只读，做已知点实测）
import tool_integrity as ti  # noqa: E402  （只读，做已知点实测）

OUT_MD = os.path.join(ROOT, "data", "642_fail_open_audit.md")
OUT_JSON = os.path.join(ROOT, "data", "642_fail_open_audit.json")

#: 关键字段（缺省值补全即可能让坏东西通过）
CRITICAL_KEYS = ("result", "status", "verdict", "state", "decision", "severity",
                 "self_hash", "prev_hash", "digest", "sha256", "target_id", "evidence",
                 "review_method", "decision_origin")

#: 视为"成功/通过"的返回值字面量
SUCCESS_LITERALS = (True, 0, "ok", "OK", "PASS", "pass")

SEVERITY_ORDER = {"高": 0, "中": 1, "低": 2}


# ── 第一部分：已知点实测（可复现）───────────────────────────────────────────
def known_point_supply_chain() -> dict[str, Any]:
    """FO-A：`tool_integrity.verify_supply_chain()` 对**缺失文件**只警告、退出码 0（实测）。"""
    ch, wn, code = ti.verify_supply_chain(names=("data/__nope_xyz__.json",))
    return {"id": "FO-A", "file": "tools/tool_integrity.py",
            "symbol": "verify_supply_chain",
            "evidence": {"changed": ch, "warnings": wn, "exit_code": code},
            "fail_open": bool(wn) and code == 0,
            "severity": "中",
            "impact": "信任根数据文件（毒样例豁免台账 / 覆盖率台账 / 治理 manifest / Merkle 根 / "
                      "in-toto layout）缺失时**不失败**；在完整检出里等于放弃判别力",
            "why_not_high": "设计理由是'仓库副本/部分检出下无判别力'，属**有理由的取舍**，"
                            "但缺少'完整仓库下必须钉住'的分支 ⇒ 仍是 fail-open",
            "fix_suggestion": "增加 `--require-supply-chain`（或按 `.tool_checksums` 是否已含 "
                              "supply_chain 节判定）：**节存在但文件缺失 ⇒ exit 1**；"
                              "仅当节整体缺失（旧格式基准）才降级为 warning"}


def known_point_decision_event() -> dict[str, Any]:
    """FO-B：`DecisionEvent.from_dict({})` 静默用默认值补全（实测 ⇒ APPROVE + human_observed）。"""
    e = de.DecisionEvent.from_dict({})
    errs = e.validate()
    _ = de.DecisionEvent.from_dict({"bogus_key": 1})
    return {"id": "FO-B", "file": "tools/decision_event_v2_626.py",
            "symbol": "DecisionEvent.from_dict",
            "evidence": {"empty_dict_accepted": True, "result": e.result,
                         "review_method": e.review_method,
                         "decision_origin": e.decision_origin,
                         "validate_errors": errs,
                         "unknown_keys_silently_dropped": "bogus_key" not in
                                                          de.DecisionEvent.__dataclass_fields__},
            "fail_open": str(e.result) == "APPROVE",
            "severity": "高",
            "impact": "空/残 JSON 被补成 **result=APPROVE + review_method=BATCH_AUTH + "
                      "decision_origin=human_observed** —— 恰好是最'信任假设'的组合；"
                      "`validate()` 能抓 `target_id` 必填，但**不抓 result 使用了默认值**；"
                      "另外**未知键被静默丢弃**（拼错字段名等于没写）",
            "why_not_high": "",
            "fix_suggestion": "① `from_dict` 增加 `strict=True`：**缺失必填字段 ⇒ 抛错**"
                              "（而不是补默认）；② 记录哪些字段来自默认值（`_defaulted` 集）并在 "
                              "`validate()` 里报错；③ 未知键 ⇒ 抛错（fail-loud）"}


def known_points() -> list[dict[str, Any]]:
    out = []
    for fn in (known_point_supply_chain, known_point_decision_event):
        try:
            out.append(fn())
        except Exception as exc:  # noqa: BLE001
            out.append({"id": fn.__name__, "fail_open": None, "severity": "低",
                        "evidence": {"error": f"{type(exc).__name__}: {exc}"},
                        "impact": "实测失败（未能取证）"})
    return out


# ── 第二部分：全量 AST 模式扫描 ─────────────────────────────────────────────
def _files() -> list[str]:
    return sorted(os.path.join(HERE, f) for f in os.listdir(HERE) if f.endswith(".py"))


def _is_success_const(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value in SUCCESS_LITERALS


def _empties(node: ast.AST) -> bool:
    return ((isinstance(node, ast.List) and not node.elts)
            or (isinstance(node, ast.Dict) and not node.keys)
            or (isinstance(node, ast.Constant) and node.value == ""))


def _scan_file(path: str) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except (OSError, SyntaxError):
        return []
    hits: list[dict[str, Any]] = []
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")

    # FO-1：except 处理器直接返回"成功"常量
    for node in ast.walk(tree):
        if not isinstance(node, ast.Try):
            continue
        for h in node.handlers:
            body = [n for n in h.body if not isinstance(n, ast.Expr)
                    or not isinstance(n.value, ast.Constant)]     # 忽略纯 docstring
            if len(body) == 1 and isinstance(body[0], ast.Return) and body[0].value is not None:
                v = body[0].value
                if _is_success_const(v) or _empties(v):
                    hits.append({"rule": "FO-1", "file": rel, "line": h.lineno,
                                 "code": ast.unparse(body[0])[:80],
                                 "meaning": "异常 ⇒ 返回成功/空集（fail-open）"})

    # FO-2：`if not os.path.exists(...)` ⇒ 直接返回成功
    for node in ast.walk(tree):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.UnaryOp):
            continue
        if not isinstance(node.test.op, ast.Not):
            continue
        txt = ast.unparse(node.test.operand)
        if "exists(" not in txt:
            continue
        if len(node.body) == 1 and isinstance(node.body[0], ast.Return) \
                and node.body[0].value is not None and _is_success_const(node.body[0].value):
            hits.append({"rule": "FO-2", "file": rel, "line": node.lineno,
                         "code": f"if {txt}: {ast.unparse(node.body[0])}"[:80],
                         "meaning": "文件缺失 ⇒ 返回成功（fail-open）"})

    # FO-3：关键字段 `.get(key, 非 None 默认)`
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "get" or len(node.args) < 2:
            continue
        k = node.args[0]
        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
            continue
        if k.value not in CRITICAL_KEYS:
            continue
        default = node.args[1]
        if isinstance(default, ast.Constant) and default.value is None:
            continue
        hits.append({"rule": "FO-3", "file": rel, "line": node.lineno,
                     "code": ast.unparse(node)[:80],
                     "meaning": f"关键字段 {k.value!r} 缺省即补默认（可能让坏东西通过）"})

    # FO-4：`... if changed else 0` 形态（warning 不影响退出码）
    src = open(path, encoding="utf-8", errors="replace").read()
    for i, line in enumerate(src.splitlines(), 1):
        if "if changed else" in line and "1" in line:
            hits.append({"rule": "FO-4", "file": rel, "line": i,
                         "code": line.strip()[:80],
                         "meaning": "仅内容变更算失败；缺失/未钉只警告（fail-open）"})
    return hits


def scan_all() -> dict[str, Any]:
    hits: list[dict[str, Any]] = []
    scanned = 0
    for p in _files():
        scanned += 1
        hits += _scan_file(p)
    by_rule: dict[str, int] = {}
    for h in hits:
        by_rule[h["rule"]] = by_rule.get(h["rule"], 0) + 1
    return {"scanned_files": scanned, "n_hits": len(hits), "by_rule": by_rule, "hits": hits}


RULE_META = {
    "FO-1": {"severity": "高", "name": "异常 ⇒ 通过",
             "fix": "区分'可容忍异常'与'无法判定'：后者必须抛错或返回 UNKNOWN（四态），不得返回成功"},
    "FO-2": {"severity": "中", "name": "缺失 ⇒ 通过",
             "fix": "缺失应映射为 UNKNOWN/FAIL；若确为可选产物，需在文档与常量里显式声明白名单"},
    "FO-3": {"severity": "中", "name": "关键字段默认值 ⇒ 通过",
             "fix": "关键字段缺失应抛错；确需默认时必须显式标注来源（`_defaulted`）并在校验时报错"},
    "FO-4": {"severity": "中", "name": "警告不影响退出码",
             "fix": "为'警告'提供严格模式开关（如 --strict-supply-chain）：严格模式下警告即失败"},
}


def severity_table() -> dict[str, int]:
    t = {"高": 0, "中": 0, "低": 0}
    for kp in known_points():
        t[str(kp.get("severity", "低"))] += 1
    return t


# ── 报告 ───────────────────────────────────────────────────────────────────
def write_report() -> str:
    kps = known_points()
    sc = scan_all()
    lines = [
        "# 642 B3 · fail-closed 全量审计（**只审计，不修复**）", "",
        "> 对照口径：641 D 线「信任根缺失 ⇒ FAIL」。本模块扫描**缺失 ⇒ warning / 异常 ⇒ 通过 /"
        " 默认值 ⇒ 通过 / 校验失败 ⇒ 仅记录** 四类 fail-open。",
        "> **本文件不修改任何被审计代码**（修复留 643 或经人授权）。", "",
        "## 一、已知点复核（**可复现实测**）", "",
        "| # | 位置 | 实测证据 | fail-open | 严重度 |", "|---|---|---|---|---|"]
    for kp in kps:
        ev = kp.get("evidence", {})
        evs = json.dumps(ev, ensure_ascii=False)
        lines.append(f"| {kp['id']} | `{kp.get('file', '?')}::{kp.get('symbol', '?')}` | "
                     f"`{evs[:150]}` | {'⚠️ 是' if kp.get('fail_open') else '—'} | "
                     f"**{kp.get('severity', '?')}** |")
    lines += ["", "### 1.1 逐条影响与修复建议", "",
              "| # | 影响 | 为什么这个严重度 | 修复建议 |", "|---|---|---|---|"]
    for kp in kps:
        lines.append(f"| {kp['id']} | {kp.get('impact', '')} | "
                     f"{kp.get('why_not_high') or '—'} | {kp.get('fix_suggestion', '')} |")
    lines += ["", "## 二、全量 AST 模式扫描", "",
              f"- 扫描文件：**{sc['scanned_files']}** 个 `tools/*.py`",
              f"- 命中：**{sc['n_hits']}** 条；按规则分布 `{sc['by_rule']}`", "",
              "| 规则 | 名称 | 严重度 | 修复建议 |", "|---|---|---|---|"]
    for rid, meta in RULE_META.items():
        lines.append(f"| {rid} | {meta['name']} | {meta['severity']} | {meta['fix']} |")
    lines += ["", "### 2.1 命中清单（逐条，按文件聚合便于复核）", "",
              "> **注意**：上表严重度是**规则类**的严重度，不等于每个命中的实例严重度 ——"
              " 命中在 CLI 容错里可能无害，落在判决/信任路径上才是真缺陷（需逐条人核）。", "",
              "| 规则 | 文件:行 | 代码 | 含义 |", "|---|---|---|---|"]
    for h in sorted(sc["hits"], key=lambda x: (x["file"], x["line"])):
        lines.append(f"| {h['rule']} | `{h['file']}:{h['line']}` | `{h['code']}` | "
                     f"{h['meaning']} |")
    if not sc["hits"]:
        lines.append("| — | — | — | 零命中 |")
    t = severity_table()
    lines += ["", "## 三、严重度汇总（含已知点）", "",
              f"- 高：**{t['高']}**；中：**{t['中']}**；低：**{t['低']}**", "",
              "## 四、修复优先级建议（**不执行**）", "",
              "1. **高**：FO-B（`DecisionEvent.from_dict` 默认值 ⇒ APPROVE + human_observed）——"
              "它直接决定'信任账本里的一条事件是否可信'；",
              "2. **中**：FO-A（supply_chain 缺失不失败）——加严格模式开关即可，改动面小；",
              "3. **中**：FO-3 命中项逐条复核（多数是「读外部数据时的容错」，"
              "需区分「可容忍」与「不可判定」）；",
              "4. **低**：FO-1/FO-2 的命中多为工具自身容错，需按'该工具是否参与判决'分级。", "",
              "## 诚实登记", "",
              "1. **只审计不修复**（§七.5）：本批**未改动** `tool_integrity.py` / "
              "`decision_event_v2_626.py` 等任何被审计代码；",
              "2. **扫描是启发式**：AST 四条规则**高精度低召回** —— 漏判一定存在"
              "（如'异常被 pass 后靠后续默认值通过'这类跨语句模式未覆盖）；",
              "3. **命中 ≠ 缺陷**：需要按'该代码是否参与判决/信任'逐条人核，本报告给出的是**线索清单**，"
              "不是判决；",
              "4. 实测两处**均为可复现**（不是纸面推断）：FO-A 实测 `exit_code=0`，"
              "FO-B 实测空 dict ⇒ `result='APPROVE'`；",
              "5. **fail-open 的严重度不按出现次数**，按'能否让坏东西通过'分级。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"known_points": kps, "scan": sc, "severity": t,
                   "rule_meta": RULE_META}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    a = known_point_supply_chain()
    chk("FO-A 实测 fail-open（缺文件 exit=0）",
        a["fail_open"] is True and a["evidence"]["exit_code"] == 0)
    b = known_point_decision_event()
    chk("FO-B 实测 fail-open（空 dict ⇒ APPROVE）",
        b["fail_open"] is True and b["evidence"]["result"] == "APPROVE")
    chk("FO-B 默认 origin 是 human_observed",
        b["evidence"]["decision_origin"] == "human_observed")
    chk("FO-B 未知键被静默丢弃", b["evidence"]["unknown_keys_silently_dropped"] is True)

    sc = scan_all()
    chk("扫描覆盖 > 400 文件", sc["scanned_files"] > 400, str(sc["scanned_files"]))
    chk("四条规则都有定义", set(RULE_META) == {"FO-1", "FO-2", "FO-3", "FO-4"})
    chk("命中清单可复现（同一次扫描两次一致）",
        scan_all()["n_hits"] == sc["n_hits"])
    chk("FO-4 命中 tool_integrity", any(h["rule"] == "FO-4" and "tool_integrity" in h["file"]
                                        for h in sc["hits"]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    chk("JSON 路径在 data 下", OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 B3 fail-closed 全量审计")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写审计报告 + JSON")
    ap.add_argument("--json", action="store_true", help="打印审计（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    sc = scan_all()
    kps = known_points()
    if a.json:
        print(json.dumps({"known_points": kps, "scan": {k: v for k, v in sc.items()
                                                       if k != "hits"}},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[fail-closed] 已知点 {len(kps)} 处（fail-open "
          f"{sum(1 for k in kps if k.get('fail_open'))}）；扫描 {sc['scanned_files']} 文件 ⇒ "
          f"命中 {sc['n_hits']} 条 {sc['by_rule']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
