#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc_lint.py — 文档质量门禁（478 §三 / 479 任务 2）。

解决的问题（478 §3.1 实录）：100+ 份文档反复出现「文档说 21 条规则、实际 50 条」
这类系统性失真 —— 新 Agent 按过时文档写代码必然出错，架构调研的结论建立在错误数字上。
本工具把这类失真变成**机器可检**，为「文档即代码」提供最小可用的门禁。

扫描面与三类检查（扫描面：`docs/kernel/*.md`）
----------------------------------------------
① **规则名**：token 形态像规则 ID（`EV-…`/`ATOM-…`/`S1-…`/`META-…`）者必须在
   `gate_engine.RULES` 中存在；不在则查豁免台账 `tools/doc_lint_exemptions.yaml`
   （历史/已删/规划中的规则），仍未登记 ⇒ 失真。
   误报抑制：含 3 位数字段的 token（`ATOM-MEM-MOVE-001`/`EV-MEM-001` 是 ID 不是规则名）、
   含占位符（`XXX`/`NNN`）或通配（`EV-*`）者跳过。
② **数字**：`N 条规则` / `N 个毒样例` / `N 张卡` / `N 颗原子` / `N 个工具` 与**实测**比对。
   历史快照（行内含「约/历史/当时/快照/旧/曾」或 `~`）跳过 —— 历史报告的数字是其时真值，
   不该被当成失真（这一条是本工具能否长期存活的关键：否则历史文档永远在报错）。
③ **工具名**：`xxx.py` 必须在 `tools/` 下存在（支持 `tools/xxx.py` 与裸 `xxx.py`）。

退出码（479 验收）：无失真 → 0；有失真 → 1。
当前存量失真较多（478 §3.1 已知），提供 `--observe` 供 CI **渐进接入**（只报告、恒 exit 0），
待失真清理到可接受面后再去掉该开关走默认严格模式。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_engine as ge  # noqa: E402  单一真相源：规则注册表

DOCS = ROOT / "docs" / "kernel"
TOOLS = ROOT / "tools"
EXEMPTIONS = TOOLS / "doc_lint_exemptions.yaml"

# ── ① 规则名 ──────────────────────────────────────────────────────────────
# 形态：AAAA-BBBB(-CCCC)*；**不含纯 3 位数字段**（那是原子/证据/误解 ID 的形态）。
_RULE_TOKEN = re.compile(
    r"(?<![\w-])((?:EV|ATOM|META|S[1-6])-[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)*)(?![\w-])")
_PLACEHOLDER = ("XXX", "NNN", "YYY", "ZZZ")


def _looks_like_rule(token: str) -> bool:
    """排除「像 ID 不像规则」的 token：含 3 位纯数字段 / 占位符 / 通配。

    右侧负向断言（`_RULE_TOKEN` 里的 `(?!` + 反斜杠 w 减号 `)`）是关键：否则
    `EV-MEM-001` 会被**截断**成 `EV-MEM`（`-001` 段以数字开头，不匹配 `[A-Z]…`）
    ⇒ 报出一堆不存在的"规则"（实测首跑 79 处里大半是它，修后剩 19 处真失真）。
    """
    if "*" in token or any(p in token for p in _PLACEHOLDER):
        return False
    return not any(seg.isdigit() and len(seg) == 3 for seg in token.split("-"))


# ── ② 数字 ────────────────────────────────────────────────────────────────
# (正则, 实测键, 描述)。每条正则的捕获组 1 = 数字。
_COUNT_PATTERNS: tuple[tuple[re.Pattern[str], str, str], ...] = (
    (re.compile(r"(\d+)\s*条规则"), "rules", "条规则"),
    (re.compile(r"(\d+)\s*个毒样例"), "poison", "个毒样例"),
    (re.compile(r"(\d+)\s*张卡"), "evidence", "张卡"),
    (re.compile(r"(\d+)\s*颗原子"), "atoms", "颗原子"),
    (re.compile(r"(\d+)\s*个工具"), "tools", "个工具"),
)
_HISTORICAL = ("约", "历史", "当时", "快照", "旧", "曾", "~", "≈")


def _is_historical(line: str) -> bool:
    return any(w in line for w in _HISTORICAL)


# ── ③ 工具名 ──────────────────────────────────────────────────────────────
_TOOL_REF = re.compile(r"\b([a-z][a-z0-9_]{2,})\.py\b")
# 明确不是本仓工具的模块名（标准库/第三方/外部脚本）
_TOOL_WHITELIST = frozenset({"setup", "conftest", "__init__"})


def collect_actuals() -> dict[str, int]:
    """实测数字（单一采集点：任何检查都不许自算，避免工具自己引入失真）。"""
    surface = TOOLS / "poison_surface_map.json"
    poison = 0
    if surface.is_file():
        try:
            data = json.loads(surface.read_text(encoding="utf-8"))
            poison = len(data.get("payloads", [])) + len(data.get("negative_controls", []))
        except (OSError, ValueError):
            poison = 0
    return {
        "rules": len(ge.RULES),
        "evidence": len(list(ge.EVIDENCE.rglob("EV-*.md"))),   # 卡在域子目录下（mem/conc/…）
        "atoms": len(list(ge.ATOMS.rglob("ATOM-*.md"))),
        "tools": len(list(TOOLS.glob("*.py"))),
        "poison": poison,
    }


def load_exemptions() -> dict[str, str]:
    """台账 `tools/doc_lint_exemptions.yaml` → {token: "日期 · 原因"}（零依赖解析）。

    只允许单行 flow 映射：`- {id: X, reason: "...", date: YYYY-MM-DD}`（同 poison 台账风格）。
    缺失 ⇒ 空 dict（fail-closed：未登记即算失真，不因台账丢失而静默放行）。
    """
    if not EXEMPTIONS.is_file():
        return {}
    pat = re.compile(
        r'^\s*-\s*\{\s*id:\s*([A-Za-z0-9_.-]+)\s*,\s*reason:\s*"?(.*?)"?\s*,\s*'
        r'date:\s*(\d{4}-\d{2}-\d{2})\s*\}\s*$')
    out: dict[str, str] = {}
    for line in EXEMPTIONS.read_text(encoding="utf-8", errors="replace").split("\n"):
        m = pat.match(line)
        if m:
            out[m.group(1)] = f"{m.group(3)} · {m.group(2).strip()}"
    return out


def scan_doc(path: Path, actuals: dict[str, int],
             rule_ids: set[str], tool_names: set[str], test_names: set[str],
             exempt: dict[str, str]) -> list[dict]:
    """逐行扫描单个文档，返回问题列表（每项含 path/line/kind/message）。"""
    issues: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").split("\n")
    except OSError:
        return issues
    for i, line in enumerate(lines, 1):
        # 行内豁免（`doc-lint:ignore`，Markdown 里写成 <!-- doc-lint:ignore -->）：
        # 用于**逐字引用历史文档**的合法场景（如引用 409 原表的旧规则名）。
        # 与台账 `doc_lint_exemptions.yaml` 的分工：台账=全局豁免某个 token；
        # 行内=只放过这一行（避免全局豁免掩盖别处的真失真）。
        if "doc-lint:ignore" in line or "doc_lint:ignore" in line:
            continue
        for token in set(_RULE_TOKEN.findall(line)):
            if not _looks_like_rule(token):
                continue
            if token in rule_ids or token in exempt:
                continue
            issues.append({
                "file": path.name, "line": i, "kind": "rule",
                "message": f"引用了不存在的规则 {token}（须在 gate_engine.RULES 中，"
                           f"或在 tools/doc_lint_exemptions.yaml 登记）"})
        if not _is_historical(line):
            for pat, key, label in _COUNT_PATTERNS:
                for m in pat.finditer(line):
                    got, want = int(m.group(1)), actuals.get(key, -1)
                    if want >= 0 and got != want:
                        issues.append({
                            "file": path.name, "line": i, "kind": "count",
                            "message": f"说 {got} {label}，实际 {want}"
                                       f"（历史快照请在行内标『约/当时/快照』）"})
        for name in set(_TOOL_REF.findall(line)):
            # `tests/test_xxx.py` 也是合法引用（文档常指测试文件）→ 一并接受
            if (name in tool_names or name in test_names
                    or name in _TOOL_WHITELIST or name in exempt):
                continue
            issues.append({
                "file": path.name, "line": i, "kind": "tool",
                "message": f"引用了不存在的工具 {name}.py（tools/ 下无此文件）"})
    return issues


def scan(docs_dir: Path | None = None) -> tuple[list[dict], dict[str, int]]:
    actuals = collect_actuals()
    rule_ids = {r.id for r in ge.RULES}
    tool_names = {p.stem for p in TOOLS.glob("*.py")}
    tool_names.add(Path(__file__).stem)          # 本工具自身尚未被引用时也可自指
    test_names = {p.stem for p in (ROOT / "tests").glob("*.py")}
    exempt = load_exemptions()
    base = docs_dir or DOCS
    issues: list[dict] = []
    for p in sorted(base.glob("*.md")):
        issues.extend(scan_doc(p, actuals, rule_ids, tool_names, test_names, exempt))
    return issues, actuals


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="文档质量门禁（规则名/数字/工具名引用）")
    ap.add_argument("--observe", action="store_true",
                    help="观察模式：只报告，恒 exit 0（CI 渐进接入用；存量失真尚多）")
    ap.add_argument("--json", nargs="?", const=True, default=False,
                    help="结构化 JSON 输出到 stdout")
    ap.add_argument("--dir", default=None, help="扫描目录（默认 docs/kernel）")
    a = ap.parse_args(argv)

    real_out = sys.stdout
    if a.json:
        sys.stdout = sys.stderr
    issues, actuals = scan(Path(a.dir) if a.dir else None)

    by_kind: dict[str, int] = {}
    for it in issues:
        by_kind[it["kind"]] = by_kind.get(it["kind"], 0) + 1
    for it in issues:
        print(f"[WARN] {it['file']}:{it['line']}: {it['message']}")
    print(f"\n[doc_lint] 失真 {len(issues)} 处"
          f"（规则名 {by_kind.get('rule', 0)} · 数字 {by_kind.get('count', 0)} · "
          f"工具名 {by_kind.get('tool', 0)}）")
    print(f"[doc_lint] 实测基线：规则 {actuals['rules']} · 毒样例 {actuals['poison']} · "
          f"证据卡 {actuals['evidence']} · 原子 {actuals['atoms']} · 工具 {actuals['tools']}")
    if a.observe:
        print("[doc_lint] 观察模式（--observe）：不阻断（存量失真按 479 验收只记录不修）")
    if a.json:
        real_out.write(json.dumps({
            "tool": "doc_lint", "version": "v1.0",
            "status": "pass" if not issues else "fail",
            "summary": {"issues": len(issues), "by_kind": by_kind},
            "actuals": actuals, "findings": issues,
        }, ensure_ascii=False, indent=1) + "\n")
    if a.observe:
        return 0
    return 0 if not issues else 1

if "--check" in sys.argv:
    print("OK: doc_lint --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
