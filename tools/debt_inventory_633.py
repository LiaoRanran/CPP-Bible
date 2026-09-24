"""633 任务0 · 全量债务盘点（静态扫描，不跑 pytest）

本批最重要的任务：**先全量盘点，再一波端一大批**。7 个维度静态扫描，产出
`data/633_debt_inventory.md`（含化债前快照 + 分类分级 + 本批可清清单 + 交人清单）。
后续 A2/B1/B2/C1/C2/D1/D2/E1 的清理动作都以本盘点结果为输入。

**不做的事**：不跑 pytest（留给 A2）、不代签、不自动改卡、不预设债务清单。
**只读契约**：`--check` 只扫描不写盘；`--report`/默认 才写 `data/633_debt_inventory.md`。

7 维度：CI/测试债、工具债、数据债、安全债、文档债、git 债、协议债。
纯标准库；`--check` 只读 exit 0；≥5 例单测（tests/test_debt_inventory_633.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "633_debt_inventory.md")
OUT_JSON = os.path.join(ROOT, "data", "633_debt_inventory.json")

# §零.12 工作区残留（禁提交）
RESIDUAL_PREFIXES = ("_arch_v19", "_arch_v20", "_arch_v21", "_arch_v22", "_arch_v23",
                     "_adv_v80", "data/pck_backup_628", "data/queyi_core_", "tools/queyi_core_")
# §零.8 两条 CRLF 假脏文件（不碰）
CRLF_FALSE_DIRTY = ("data/mutation/full_baseline_v4.json", "evidence/conc/EV-CONC-001.md")

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".mypy_cache", ".ruff_cache",
             ".pytest_tmp", ".pytest_cache"}
BATCH_RE = re.compile(r"\b6[12]\d\b")
TODO_RE = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
IMPORT_RE = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", re.MULTILINE)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
STALE_RE = re.compile(r"截至\s*(6[0-2]\d)")
SECRET_RE = re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key)\b\s*[:=]\s*[\"']([^\"']{6,})[\"']")

_IDS: dict[str, int] = {}


def _nid(code: str) -> str:
    _IDS[code] = _IDS.get(code, 0) + 1
    return f"{code}-{_IDS[code]:03d}"


def _reset_ids() -> None:
    _IDS.clear()


def item(category: str, code: str, severity: str, desc: str, loc: str,
         root_cause: str, action: str, effort: str) -> dict[str, Any]:
    return {"id": _nid(code), "category": category, "severity": severity,
            "desc": desc, "loc": loc, "root_cause": root_cause,
            "action": action, "effort": effort}


def _walk(base: str, exts: tuple[str, ...], limit: Optional[int] = None) -> list[str]:
    out: list[str] = []
    for r, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(exts):
                out.append(os.path.join(r, f))
                if limit and len(out) >= limit:
                    return out
    return out


def rel(p: str) -> str:
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def _read(p: str) -> str:
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def _run(args: list[str]) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=120).stdout
    except Exception:  # noqa: BLE001
        return ""


# ───────────────────────── 1. CI/测试债（静态，不跑 pytest） ─────────────────────────
def _missing_local_imports(path: str) -> list[str]:
    src = _read(path)
    missing = []
    for m in IMPORT_RE.finditer(src):
        mod = m.group(1) or m.group(2) or ""
        top = mod.split(".")[0]
        if top not in ("tools", "tests"):
            continue
        parts = mod.split(".")
        cand = os.path.join(ROOT, *parts) + ".py"
        cand_pkg = os.path.join(ROOT, *parts, "__init__.py")
        if not os.path.exists(cand) and not os.path.exists(cand_pkg):
            missing.append(mod)
    return sorted(set(missing))


def scan_ci_tests() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    tests = _walk(os.path.join(ROOT, "tests"), (".py",))
    hardcoded = 0
    skipif = 0
    slow = 0
    broken = 0
    for t in tests:
        src = _read(t)
        for i, line in enumerate(src.splitlines(), 1):
            if "assert" in line and BATCH_RE.search(line) and re.search(r"==|>=|<=|=", line):
                if hardcoded < 40:
                    items.append(item("CI/测试债", "CI", "P1",
                                      f"硬编码批次号断言：{line.strip()[:70]}",
                                      f"{rel(t)}:{i}", "断言绑定当时最新批次",
                                      "改相对断言或从 status.json/baseline 动态读", "S"))
                hardcoded += 1
        if "@pytest.mark.skipif" in src:
            skipif += 1
            items.append(item("CI/测试债", "CI", "P3", "含 skipif（环境依赖，可能 CI 不成立）",
                              rel(t), "依赖本地文件/编译器/网络",
                              "登记；E1 统一到 conftest.py skipif", "M"))
        if "@pytest.mark.slow" in src:
            slow += 1
            items.append(item("CI/测试债", "CI", "P3", "含 slow 标记测试",
                              rel(t), "运行耗时长", "登记；E1 评估优化", "M"))
        miss = _missing_local_imports(t)
        if miss:
            broken += len(miss)
            items.append(item("CI/测试债", "CI", "P0",
                              f"import 了不存在的本地模块：{', '.join(miss)}",
                              rel(t), "模块被删除/重命名/路径变更",
                              "定位根因：路径→修 import；真缺失→登记", "S"))
    return items


# ───────────────────────── 2. 工具债 ─────────────────────────
def _referenced_stems() -> set[str]:
    stems: set[str] = set()
    for base, exts in ((os.path.join(ROOT, "tools"), (".py",)),
                       (os.path.join(ROOT, "tests"), (".py",)),
                       (os.path.join(ROOT, "."), (".yml", ".cfg", ".toml"))):
        for p in _walk(base, exts):
            src = _read(p)
            for m in IMPORT_RE.finditer(src):
                mod = m.group(1) or m.group(2) or ""
                if mod.split(".")[0] in ("tools", "tests"):
                    stems.add(mod.split(".")[-1])
            for m in re.finditer(r"tools/([\w]+)\.py", src):
                stems.add(m.group(1))
    return stems


def _is_cli(src: str) -> bool:
    """是否为可执行 CLI（含主入口），库模块不算工具债候选。"""
    return ("__main__" in src) or ("argparse" in src and "ArgumentParser" in src)


def scan_tools() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    tools = _walk(os.path.join(ROOT, "tools"), (".py",))
    refd = _referenced_stems()
    todo = 0
    big = 0
    for t in tools:
        name = os.path.basename(t)[:-3]
        src = _read(t)
        nlines = src.count("\n") + 1
        if _is_cli(src) and "--check" not in src:
            used = name in refd
            items.append(item("工具债", "TOOL", "P1" if used else "P2",
                              f"CLI 无 --check（{'被引用，仍在使用' if used else '未见引用'}）",
                              rel(t), "旧工具未补只读自检",
                              "加 --check（只读，见 B2）" if used else "登记（可能已废弃，不删除）",
                              "S"))
        for i, line in enumerate(src.splitlines(), 1):
            if TODO_RE.search(line):
                todo += 1
                if todo <= 40:
                    items.append(item("工具债", "TOOL", "P2",
                                      f"标记：{line.strip()[:70]}", f"{rel(t)}:{i}",
                                      "历史遗留未决项", "逐条评估：能修则修，否则登记", "M"))
        if nlines > 500:
            big += 1
            items.append(item("工具债", "TOOL", "P3",
                              f"超过 500 行的巨型文件（{nlines} 行）", rel(t),
                              "职责未拆分", "登记；不拆分（风险高）", "L"))
        if not re.search(r"_6\d\d(?:\.py)?$", name):
            items.append(item("工具债", "TOOL", "P3", "命名不符合 *_6XX.py 批次规范",
                              rel(t), "命名约定不统一", "登记；不重命名（引用成本高）", "L"))
        miss = _missing_local_imports(t)
        if miss:
            items.append(item("工具债", "TOOL", "P0",
                              f"import 了不存在的本地模块：{', '.join(miss)}", rel(t),
                              "模块被删除/重命名/路径变更", "定位根因修复或登记", "S"))
    return items


# ───────────────────────── 3. 数据债 ─────────────────────────
def scan_data() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    # 大文件 >1MB（未跟踪）
    tracked = set(_run(["git", "ls-files"]).splitlines())
    for r, dirs, files in os.walk(os.path.join(ROOT, "data")):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = os.path.join(r, f)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            if sz > 1024 * 1024 and rel(p) not in tracked:
                items.append(item("数据债", "DATA", "P2",
                                  f"未跟踪的大文件（{sz // 1024}KB）", rel(p),
                                  "运行时产物未清理", "登记；按 §零.17 移至 data/_archive_633/", "S"))
    # JSON/MD 引用不存在的文件（抽样：只查 data/*.json 中的路径串）
    for j in _walk(os.path.join(ROOT, "data"), (".json",), limit=200):
        src = _read(j)
        for m in re.finditer(r"[\"']((?:tools|data|evidence|tests|atoms)/[\w./-]+\.\w+)[\"']", src):
            ref = m.group(1)
            if not os.path.exists(os.path.join(ROOT, ref)):
                items.append(item("数据债", "DATA", "P2", f"JSON 引用不存在的文件：{ref}",
                                  rel(j), "引用漂移", "登记；交 C2/D 线核对", "M"))
                break
    return items


# ───────────────────────── 4. 安全债 ─────────────────────────
def scan_security() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    keyfiles = []
    for r, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith((".key", ".pem", ".priv")):
                keyfiles.append(os.path.join(r, f))
    for k in keyfiles:
        rp = rel(k)
        ci = subprocess.run(["git", "check-ignore", "-q", rp], cwd=ROOT, capture_output=True)
        is_ign = ci.returncode == 0
        tracked = rp in set(_run(["git", "ls-files"]).splitlines())
        sev = "P0" if tracked else ("P1" if not is_ign else "P1")
        items.append(item("安全债", "SEC", sev,
                          f"密钥文件（{'已忽略' if is_ign else '未忽略'}，{'已入库' if tracked else '未入库'}）",
                          rp, "明文密钥落盘", "备份 + 评估影响（C1）；确认 ignore 覆盖", "S"))
    # 硬编码 secret 关键词
    hits = 0
    for p in _walk(os.path.join(ROOT, "tools"), (".py",)) + _walk(os.path.join(ROOT, "data"), (".py", ".md"), limit=300):
        for i, line in enumerate(_read(p).splitlines(), 1):
            if SECRET_RE.search(line):
                hits += 1
                if hits <= 20:
                    items.append(item("安全债", "SEC", "P2",
                                      "疑似硬编码机密赋值（值已脱敏）",
                                      f"{rel(p)}:{i}", "可能与密钥/令牌相关",
                                      "人工核对；确认是真实机密则轮换", "M"))
    return items


# ───────────────────────── 5. 文档债 ─────────────────────────
def scan_docs() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    docs = _walk(os.path.join(ROOT, "data"), (".md",)) + _walk(os.path.join(ROOT, "References"), (".md",))
    dead = 0
    stale = 0
    for d in docs:
        src = _read(d)
        base_dir = os.path.dirname(d)
        for m in MD_LINK_RE.finditer(src):
            tgt = m.group(1).strip().split("#")[0]
            if not tgt or tgt.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            cands = [os.path.join(base_dir, tgt), os.path.join(ROOT, tgt)]
            if not any(os.path.exists(c) for c in cands):
                dead += 1
                if dead <= 40:
                    items.append(item("文档债", "DOC", "P1", f"死链接 → {tgt}",
                                      rel(d), "目标文件被删除/重命名",
                                      "更新为新路径或标注『已迁移』（D2）", "S"))
        for m in STALE_RE.finditer(src):
            b = int(m.group(1))
            if b < 633:
                stale += 1
                if stale <= 40:
                    items.append(item("文档债", "DOC", "P1", f"过期标注：截至 {b}",
                                      rel(d), "文档标注的历史批次已过",
                                      "文首加『⚠️ 已过时』标注（不删原文，D2）", "S"))
                break
    return items


# ───────────────────────── 6. git 债 ─────────────────────────
def _git_status_lines() -> list[str]:
    return [ln for ln in _run(["git", "status", "--short"]).splitlines() if ln.strip()]


def scan_git() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    lines = _git_status_lines()
    residual = 0
    for ln in lines:
        path = ln[3:].strip().strip('"')
        if any(path.startswith(pre) for pre in RESIDUAL_PREFIXES):
            residual += 1
    if residual:
        items.append(item("git债", "GIT", "P2",
                          f"工作区残留 {residual} 项（§零.12 禁提交）", "git status",
                          "前批次调研/临时产物未清理",
                          "登记；F1 收工时确认不提交；D 线评估是否归档", "M"))
    other = len(lines) - residual
    if other:
        items.append(item("git债", "GIT", "P1",
                          f"其余工作区改动 {other} 项（需逐项判定假脏/真脏）", "git status",
                          "前批次运行时产物 / 真脏未提交",
                          "B1 逐项 git diff 判定：假脏还原，不确定登记", "M"))
    stash = _run(["git", "stash", "list"]).strip()
    if stash:
        items.append(item("git债", "GIT", "P2", "存在 git stash", "git stash list",
                          "历史临时保存未清理", "登记", "S"))
    return items


# ───────────────────────── 7. 协议债 ─────────────────────────
def scan_protocol() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    sp = os.path.join(ROOT, "_auto", "status.json")
    if os.path.exists(sp):
        try:
            st = json.loads(_read(sp))
        except json.JSONDecodeError:
            st = {}
        head = _run(["git", "rev-parse", "--short", "HEAD"]).strip()
        if st.get("last_commit") and st["last_commit"] != head:
            items.append(item("协议债", "PROTO", "P1",
                              f"_auto/status.json last_commit={st.get('last_commit')} 与实际 HEAD={head} 不一致",
                              "_auto/status.json", "批次收工时未更新 status",
                              "F1 更新 status（last_completed_batch=633, next=634）", "S"))
        if str(st.get("last_completed_batch")) not in ("632", "633"):
            items.append(item("协议债", "PROTO", "P1",
                              f"last_completed_batch={st.get('last_completed_batch')} 落后于实际（632 已完成）",
                              "_auto/status.json", "状态文件滞后", "F1 更新", "S"))
    # outbox 最新 vs inbox 下一批
    inbox = sorted(os.path.basename(x) for x in _walk(os.path.join(ROOT, "_auto", "inbox"), (".md",)))
    outbox = sorted(os.path.basename(x) for x in _walk(os.path.join(ROOT, "_auto", "outbox"), (".md",)))
    if inbox and outbox:
        items.append(item("协议债", "PROTO", "P3",
                          f"inbox 最新 {inbox[-1]} / outbox 最新 {outbox[-1]}",
                          "_auto/{inbox,outbox}", "批次对齐检查", "F1 产出 outbox/633.md", "S"))
    # 625-632 验收报告中的交人项计数
    handlers = _walk(os.path.join(ROOT, "data"), (".md",))
    handoff = 0
    for h in handlers:
        if re.search(r"6[23]\d_acceptance_report\.md$", h) or re.search(r"632_acceptance_report\.md$", h):
            handoff += len(re.findall(r"交人|待裁决|需人", _read(h)))
    if handoff:
        items.append(item("协议债", "PROTO", "P2",
                          f"625-632 验收报告含交人/待裁决关键词约 {handoff} 处",
                          "data/*_acceptance_report.md", "历史交人项散落",
                          "D1/D 线汇总为统一清单（633_handoff.md）", "M"))
    return items


# ───────────────────────── 快照 / 汇总 / 报告 ─────────────────────────
def snapshot() -> dict[str, Any]:
    tools = _walk(os.path.join(ROOT, "tools"), (".py",))
    no_check = sum(1 for t in tools if _is_cli(_read(t)) and "--check" not in _read(t))
    todo = 0
    for t in tools:
        todo += len(TODO_RE.findall(_read(t)))
    keys = []
    for r, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        keys += [f for f in files if f.endswith((".key", ".pem", ".priv"))]
    dead = 0
    for d in _walk(os.path.join(ROOT, "data"), (".md",)):
        src = _read(d)
        bd = os.path.dirname(d)
        for m in MD_LINK_RE.finditer(src):
            tgt = m.group(1).strip().split("#")[0]
            if not tgt or tgt.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            if not any(os.path.exists(c) for c in (os.path.join(bd, tgt), os.path.join(ROOT, tgt))):
                dead += 1
    push = _run(["git", "rev-list", "--count", "origin/master..HEAD"]).strip() or "0"
    return {
        "dirty_files": len(_git_status_lines()),
        "tools_total": len(tools),
        "tools_no_check": no_check,
        "todo_count": todo,
        "key_files": len(keys),
        "dead_links": dead,
        "pending_push": int(push) if push.isdigit() else 0,
    }


def scan_all() -> dict[str, Any]:
    _reset_ids()
    sections = {
        "CI/测试债": scan_ci_tests(),
        "工具债": scan_tools(),
        "数据债": scan_data(),
        "安全债": scan_security(),
        "文档债": scan_docs(),
        "git债": scan_git(),
        "协议债": scan_protocol(),
    }
    all_items = [it for v in sections.values() for it in v]
    matrix: dict[str, dict[str, int]] = {}
    for it in all_items:
        matrix.setdefault(it["category"], {}).setdefault(it["severity"], 0)
        matrix[it["category"]][it["severity"]] += 1
    clearable = [it for it in all_items if it["severity"] in ("P0", "P1")]
    handoff = [it for it in all_items if it["severity"] in ("P2", "P3")]
    return {"snapshot": snapshot(), "sections": sections, "matrix": matrix,
            "total": len(all_items), "clearable": clearable, "handoff": handoff,
            "severity_counts": {s: sum(1 for it in all_items if it["severity"] == s)
                                for s in ("P0", "P1", "P2", "P3")}}


def write_report() -> str:
    data = scan_all()
    snap = data["snapshot"]
    lines = ["# 633 任务0 · 全量债务盘点（静态扫描）", "",
             "> 只做静态扫描，不跑 pytest（留给 A2）。本表是 633 后续所有清理任务的输入。", "",
             "## 一、化债前快照（量化指标）", "",
             "| 指标 | 值 |", "|---|---|",
             f"| 工作区脏文件数 | {snap['dirty_files']} |",
             f"| 工具总数 | {snap['tools_total']} |",
             f"| 无 --check 工具数 | {snap['tools_no_check']} |",
             f"| TODO/FIXME 总数 | {snap['todo_count']} |",
             f"| 密钥文件数 | {snap['key_files']} |",
             f"| 死链接数 | {snap['dead_links']} |",
             f"| 待 push commit 数 | {snap['pending_push']} |", "",
             "## 二、汇总矩阵（类别 × 严重度）", "",
             "| 类别 | P0 | P1 | P2 | P3 | 小计 |", "|---|---|---|---|---|---|"]
    for cat, sev in data["matrix"].items():
        row = [sev.get(k, 0) for k in ("P0", "P1", "P2", "P3")]
        lines.append(f"| {cat} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {sum(row)} |")
    sc = data["severity_counts"]
    lines.append(f"| **合计** | {sc['P0']} | {sc['P1']} | {sc['P2']} | {sc['P3']} | {data['total']} |")
    lines += ["", "## 三、各维度债务明细", ""]
    for cat, its in data["sections"].items():
        lines.append(f"### {cat}（{len(its)} 项）")
        lines.append("")
        lines.append("| ID | 严重度 | 描述 | 位置 | 根因 | 处置建议 | 工作量 |")
        lines.append("|---|---|---|---|---|---|---|")
        for it in its[:60]:
            lines.append(f"| {it['id']} | {it['severity']} | {it['desc'][:60]} | "
                         f"`{it['loc']}` | {it['root_cause']} | {it['action']} | {it['effort']} |")
        if len(its) > 60:
            lines.append(f"| … | | 另有 {len(its) - 60} 项（见 JSON） | | | | |")
        lines.append("")
    lines += ["## 四、本批可清理清单（P0+P1）", "",
              f"共 **{len(data['clearable'])}** 项。", "",
              "| ID | 类别 | 严重度 | 描述 |", "|---|---|---|---|"]
    for it in data["clearable"][:80]:
        lines.append(f"| {it['id']} | {it['category']} | {it['severity']} | {it['desc'][:70]} |")
    lines += ["", "## 五、交人清单（P2+P3）", "",
              f"共 **{len(data['handoff'])}** 项。", "",
              "| ID | 类别 | 严重度 | 描述 |", "|---|---|---|---|"]
    for it in data["handoff"][:80]:
        lines.append(f"| {it['id']} | {it['category']} | {it['severity']} | {it['desc'][:70]} |")
    lines += ["", "## 六、诚实登记", "",
              "1. 本盘点为**静态启发式**：批次号断言/死链接/交人项均为正则+关键词口径，非人工精读，"
              "存在漏判/误判（每条明细已给定位，可复核）；",
              "2. **未跑 pytest**：CI 实测失败项由 A2 采集，本表 CI/测试债为静态估计；",
              "3. 数据债的 JSON 引用检查为**抽样**（限 200 个文件、每题只报首处）；"
              "PCK hash 漂移未在此深查（交由 C2/D 线与既有 628 A2 方法）；",
              "4. 命名不合规工具**不重命名**（318 处引用成本≫收益，624 已评估）；"
              "巨型文件**不拆分**；这两类只登记；",
              "5. §零.12 残留（_arch_v2x / queyi_core 等）**登记不提交**，处置交人。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    _reset_ids()
    a = item("CI/测试债", "CI", "P1", "x", "y", "z", "w", "S")
    b = item("CI/测试债", "CI", "P2", "x", "y", "z", "w", "S")
    chk("ID 自增唯一", a["id"] == "CI-001" and b["id"] == "CI-002", f"({a['id']},{b['id']})")
    chk("严重度字段合法", a["severity"] in ("P0", "P1", "P2", "P3"))
    _reset_ids()
    snap = snapshot()
    chk("快照含全部指标",
        set(snap) >= {"dirty_files", "tools_total", "tools_no_check", "todo_count",
                      "key_files", "dead_links", "pending_push"})
    chk("工具总数为正", snap["tools_total"] > 0)
    secs = scan_all()
    chk("7 维度齐全", set(secs["sections"]) == {"CI/测试债", "工具债", "数据债", "安全债",
                                              "文档债", "git债", "协议债"})
    chk("分级不越界", all(it["severity"] in ("P0", "P1", "P2", "P3")
                        for v in secs["sections"].values() for it in v))
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="633 任务0 全量债务盘点（静态）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘）")
    ap.add_argument("--report", action="store_true", help="写 data/633_debt_inventory.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    data = scan_all()
    if args.json:
        print(json.dumps({"snapshot": data["snapshot"], "severity_counts": data["severity_counts"],
                          "total": data["total"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"total={data['total']} severity={data['severity_counts']} snapshot={data['snapshot']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
