#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""handover_check.py — 接手自检：一条命令建立「可信的现状认知」

为什么需要它
============
本项目是多 Agent / 多批次接力的长周期工程。这种模式的失效方式是：
**每一批都直接信上一批写的接手文档**。2026-08-31 实测，接手文档里三处
关键声称与实际情况不符：

- `quality 16/16` → 默认控制台实为 15/16（结论依赖终端编码）
- `HEAD = 4f62438（待 push）` → 实际已前进一个提交且已推送
- `系统 python 3.10.11` → 实测 3.14.5

`NEXT_LLM.md` 给出了 4 步启动序列，但「跑完之后该怎么判断对不对」仍靠人。
本工具把它变成一条命令 + 机器判定，并把「文档声称 vs 事实源」纳入校验。

设计取舍
========
- **只编排、不重复实现**：门禁一律调用既有脚本（gen_metrics / ruff /
  cppbible），本工具不做第二套实现——否则又多出一个真相源。
- **纯只读**：不写任何文件，可随时安全运行。
- **简报自动跟随文档**：「剩余待办」从 TOOLCHAIN_UPGRADE_NEXT.md 抓取，
  不在这里硬编码，避免简报自己也变成会过期的副本。

用法
====
    python tools/handover_check.py            # 全量自检 + 接手简报
    python tools/handover_check.py --quick    # 秒级（跳过 quality 门禁与 mypy）
    python tools/handover_check.py --json     # 机器可读输出
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from gen_metrics import resolve_fields, run_checks  # noqa: E402
from metrics_snapshot import build as scan_build  # noqa: E402
from utf8_console import ensure_utf8  # noqa: E402

PY_EXE = sys.executable
TOOLCHAIN_DOC = ROOT / "TOOLCHAIN_UPGRADE_NEXT.md"


def _run(cmd: list[str], timeout: int = 300) -> tuple[int, str]:
    """执行命令并返回 (退出码, 合并输出)。失败不抛异常。"""
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"<执行失败: {exc}>"
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


def check_git() -> dict:
    """仓库同步状态：分支、HEAD、与上游的 ahead/behind、工作树脏文件。"""
    _, head = _run(["git", "rev-parse", "--short", "HEAD"])
    _, branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    _, upstream = _run(["git", "rev-parse", "--abbrev-ref",
                        "--symbolic-full-name", "@{u}"])
    _, dirty = _run(["git", "status", "--porcelain"])

    # 用两条单向计数而非 `--left-right --count A...B`：后者在本机（PowerShell
    # 捕获 + 制表符分隔）实测返回空串，会让 ahead/behind 静默变成未知。
    ahead = behind = None
    if upstream:
        _, ahead = _run(["git", "rev-list", "--count", f"{upstream}..HEAD"])
        _, behind = _run(["git", "rev-list", "--count", f"HEAD..{upstream}"])

    dirty_files = [line for line in dirty.splitlines() if line.strip()]
    return {
        "branch": branch,
        "head": head,
        "upstream": upstream or None,
        "ahead": ahead,
        "behind": behind,
        "dirty_files": dirty_files,
    }


def check_doc_claims() -> list[str]:
    """文档写死数字 vs 事实源（复用 metrics.schema.json 的声明）。"""
    schema_path = ROOT / "metrics.schema.json"
    if not schema_path.is_file():
        return [f"缺少 {schema_path.name}，无法校验文档数字"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    report_path = ROOT / "tools" / "compile_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) \
        if report_path.is_file() else {}
    values = resolve_fields(schema, scan_build(), report)
    return run_checks(schema, values)


def check_ruff() -> tuple[bool, str]:
    """ruff 硬门禁。优先用 PATH 里的 ruff，否则回退 uvx（与 CI 同版本）。"""
    if shutil.which("ruff"):
        cmd = ["ruff", "check", "tools/"]
    elif shutil.which("uvx"):
        cmd = ["uvx", "ruff==0.6.9", "check", "tools/"]
    else:
        return True, "跳过（ruff 与 uvx 均不可用）"
    code, out = _run(cmd, timeout=180)
    return code == 0, out.strip().splitlines()[-1] if out.strip() else ""


def check_quality() -> tuple[bool, str]:
    """本地质量门禁（cppbible.py check --stage quality）。"""
    code, out = _run([PY_EXE, "tools/cppbible.py", "check", "--stage", "quality"],
                     timeout=900)
    tail = [line for line in out.splitlines() if "Result:" in line]
    return code == 0, tail[-1].strip() if tail else f"exit={code}"


def remaining_todos() -> list[str]:
    """从 TOOLCHAIN_UPGRADE_NEXT.md 抓取「当前剩余」段落，避免在此硬编码。"""
    if not TOOLCHAIN_DOC.is_file():
        return []
    text = TOOLCHAIN_DOC.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\*\*当前剩余[^\n]*\*\*[：:]\s*(.+)", text)
    return [m.group(1).strip()] if m else []


def print_briefing(git: dict, facts: dict) -> None:
    print("\n接手简报")
    print("=" * 74)
    print(f"  HEAD        {git['head']}  ({git['branch']})")
    if git["upstream"]:
        print(f"  与上游      ahead={git['ahead']} behind={git['behind']}")
    else:
        print("  与上游      无上游分支（未跟踪远端）")
    print(f"  工作树      {'干净' if not git['dirty_files'] else str(len(git['dirty_files'])) + ' 个变更'}")
    for f in git["dirty_files"][:8]:
        print(f"              {f}")
    print("-" * 74)
    print(f"  章节 {facts.get('chapters')} ｜ cpp 块 {facts.get('cpp_blocks')} ｜ "
          f"D5 覆盖 {facts.get('d5_coverage')} ｜ ASM 可校锚定 {facts.get('asm_anchor_pct')}")
    print("-" * 74)
    print("  门禁        quality / compile 见上；ruff 与文档数字见上")
    print("  单行复跑    python tools/cppbible.py check --stage quality")
    for item in remaining_todos():
        print(f"  剩余待办    {item}")
    print("=" * 74)
    print("  陷阱：① 终端是 GBK，单独直跑部分 tools/*.py 可能因打印 ✅ 崩溃，")
    print("        经 cppbible.py 调用则已被 PYTHONIOENCODING 覆盖；")
    print("        ② 别照抄文档里的数字，先跑本命令核对。")


def main() -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="接手自检：一条命令建立可信的现状认知")
    ap.add_argument("--quick", action="store_true",
                    help="秒级自检：跳过 quality 门禁（约 2 分钟）")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()

    git = check_git()
    doc_problems = check_doc_claims()
    ruff_ok, ruff_msg = check_ruff()
    quality_ok, quality_msg = (True, "已跳过（--quick）")
    if not args.quick:
        quality_ok, quality_msg = check_quality()

    # 事实快照：供简报展示，避免接手者再去翻 metrics.json
    live = scan_build()
    facts = {
        "chapters": live["content"]["files"]["chapters"],
        "cpp_blocks": live["content"]["blocks"]["cpp"],
        "d5_coverage": live["content"]["d5_coverage"],
        "asm_anchor_pct": f"{live['asm']['anchor_rate']:.1%}",
    }

    ok = not doc_problems and ruff_ok and quality_ok and not git["dirty_files"]

    if args.json:
        print(json.dumps({
            "ok": ok,
            "git": git,
            "doc_claim_problems": doc_problems,
            "ruff": {"ok": ruff_ok, "msg": ruff_msg},
            "quality": {"ok": quality_ok, "msg": quality_msg},
            "facts": facts,
        }, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print("[handover] 接手自检")
    print("-" * 74)
    print(f"  {'git 同步':<14}{'✅' if not git['dirty_files'] else '⚠️'}  "
          f"HEAD={git['head']} ahead={git['ahead']} behind={git['behind']}")
    print(f"  {'文档数字':<14}{'✅' if not doc_problems else '❌'}  "
          f"{'与事实源一致' if not doc_problems else str(len(doc_problems)) + ' 处漂移'}")
    for p in doc_problems:
        print(f"                 - {p}")
    print(f"  {'ruff':<14}{'✅' if ruff_ok else '❌'}  {ruff_msg}")
    print(f"  {'quality':<14}{'✅' if quality_ok else '❌'}  {quality_msg}")

    print_briefing(git, facts)

    if not ok:
        print("\n[handover] ✗ 存在未通过项，接手前请先处理（或明确记录为已知遗留）")
        return 1
    print("\n[handover] ✅ 现状可信，可以开始干活")
    return 0


if __name__ == "__main__":
    sys.exit(main())
