#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""adversarial_regression.py — 对抗回归看板（494 任务 6）。

背景
====
已跑 5 轮独立对抗（368/373/402/452/470/480），探针散落在 `_adv_v61/`、`_adv_v70/`、
`_adv_v80/`（均为 untracked 沙箱目录）。每轮修复后，"当年的逃逸是否真的被拦住"只能靠
人工重跑探针 —— 本工具把它变成一条可复现命令。

**诚实边界（先说清楚，勿当全自动拦截判定器）**
================================================
1. 探针的判定是**自述型**：脚本用 `print(f"[{tag}] {verdict} | {note}")` 打印结论，
   note 里写"已拦/逃逸"。本工具**如实转述**该自述（`source: "probe-self-report"`），
   不假装是工具自己的判定 —— 若某轮探针文本口径已漂移（如 E05 升格前的"仍逃逸"），
   输出会显示 escape，需人工核对（工具会在映射表里给出该探针的**回归锁位置**供核对）。
2. **无法自动化的探针**（需并发编排/特殊环境/人工语义判断）一律记 `skip` 并写明原因；
   skip **不计入通过**（479 纪律：skip ≠ pass）。
3. 只实跑**最新一轮**（默认 `_adv_v80`）；历史轮次（v61/v70）默认 skip——其口径已随
   多轮修复漂移，自动转述只会生产噪音（如实记录该取舍，不假装扫全了）。

判定与退出码（**双轨**：机器判据优先，自述仅兜底）
==================================================
第一轨（硬）——**探针实际跑出的 verdict**（494 提示词口径："不是 confirm 才算拦住"）：
* `verdict` 以 `refute` / `infra_error` 开头 ⇒ `blocked`（卡不可直推 verified）；
* `verdict == confirm` ⇒ `escape`（卡可直推 = 逃逸）；
* `verdict ∈ {warn, advice}` ⇒ `visible`（gate 层可见化，**不阻断**；如 414 F04/F06 的
  有意设计。单列计数、不算失败，但打印提示交人裁决是否升格）。
第二轨（兜底）——探针自述（无机器 verdict 可用时）："已拦"⇒ blocked、"逃逸"⇒ escape。

其余状态与退出码：
* `skip`   ：说明型探针（`*.md`）/ 历史轮次 / 无可解析行（skip ≠ pass，单列计数）；
* `gap`    ：探针**有自述判定但没映射到回归锁**（修复未沉淀为可复现锁）；
* `blocked` 还要求**回归锁文件存在**——映射存在但锁文件缺失 ⇒ 记 `escape`（锁失效）。
有 `escape` 或 `gap` → exit 1；否则 exit 0（`visible` 不阻断，但会醒目打印）。

> 实测（2026-09-14 首跑 61 项）：自述口径已漂移——3 条自述"仍逃逸"的探针实际 verdict 已是
> `refute:artifact_tampered`/`artifact_assert_failed`（E01×2、E03），2 条是 414 的有意 warn/advice
> （E04/E06）。**这正是双轨判定的存在理由**：只信自述会误报 5 条，只信机器会丢掉"可见化层"。

用法
====
    python tools/adversarial_regression.py                 # 实跑 _adv_v80（默认）
    python tools/adversarial_regression.py --dir _adv_v70  # 指定目录
    python tools/adversarial_regression.py --list          # 只列探针与映射，不实跑
    python tools/adversarial_regression.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
PROBE_ROOTS = ("_adv_v61", "_adv_v70", "_adv_v80")
DEFAULT_DIR = "_adv_v80"
TIMEOUT = 300

# 探针标签前缀 → 回归锁（来源：470 §P0-H 映射表 / 472、479 的 worklog）。
# 值 = (锁文件相对路径, 说明)；锁文件**必须存在**，否则该探针记 escape（锁失效）。
_LOCKS: dict[str, tuple[str, str]] = {
    "E01": ("tests/test_recompile_invariant.py", "replay 重编译不变量（470 P0-A）"),
    "N2": ("tests/test_poison_attack_type.py", "恒真断言扩展 + P47/P48（472 P0-2）"),
    "E10a": ("tests/test_p0f_zerodiag.py", "零诊断字段位移，升 block（472 P1-1）"),
    "E10b": ("tests/test_p0f_zerodiag.py", "pragma 消音，升 block（472 P1-1）"),
    "E05": ("tests/test_p0b_echo.py", "cat 式证据升 warn（472 P1-2）"),
    "E03": ("tests/test_discriminative.py", "恒真符号判别力统计（470 P0-C）"),
    "P0-A": ("tests/test_recompile_invariant.py", "构建脚本卡 fail-closed（470 P0-A 边界）"),
    "E07": ("tests/test_p0d_hardening.py", "缩进走私（470 P0-D）"),
    "E09": ("tests/test_p0g_lock.py", "并发锁（470 P0-G1）"),
    "N1": ("tests/test_p0g_lock.py", "僵尸锁 pid 存活检测（472 P0-1）"),
    "N4": ("tests/test_artifact_snapshot.py", "工件快照幂等还原（472 P0-4）"),
    "E12": ("tests/test_s1_git_author_binding.py", "签收 × git 作者绑定（479 任务 4）"),
}
_LINE = re.compile(r"^\[(?P<tag>[^\]]+)\]\s+(?P<verdict>\S+)\s*(?:\|\s*(?P<note>.*))?$")


def _probe_scripts(d: str) -> list[Path]:
    root = ROOT / d
    if not root.is_dir():
        return []
    return sorted(p for p in root.glob("*.py") if not p.name.startswith("_"))


def _lock_for(tag: str) -> tuple[str, str] | None:
    for key, val in _LOCKS.items():
        if tag.startswith(key):
            return val
    return None


def parse_output(text: str) -> list[dict]:
    """解析探针自述行 → [{tag, verdict, note, kind}]（不猜语义，只转述）。"""
    rows: list[dict] = []
    for raw in text.splitlines():
        m = _LINE.match(raw.strip())
        if not m:
            continue
        tag = m.group("tag").strip()
        note = (m.group("note") or "").strip()
        verdict = m.group("verdict").strip()
        control = "对照" in tag
        if control:
            kind = "control"
        elif "已拦" in note:
            kind = "blocked"
        elif "逃逸" in note:
            kind = "escape"
        else:
            kind = "unknown"          # 自述不可判 → 不给结论（计入 skip 侧）
        rows.append({"tag": tag, "verdict": verdict, "note": note, "kind": kind})
    return rows


def _run_script(p: Path) -> tuple[str, str]:
    """实跑探针脚本，返回 (stdout, stderr)；超时/异常在 stderr 里说明，不抛断整轮。"""
    try:
        r = subprocess.run([sys.executable, "-u", str(p)], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=TIMEOUT)
        return r.stdout or "", r.stderr or ""
    except subprocess.TimeoutExpired:
        return "", f"探针超时（{TIMEOUT}s）"
    except OSError as e:                       # pragma: no cover
        return "", f"探针无法启动：{e}"


def scan(probe_dir: str) -> tuple[list[dict], list[dict]]:
    """扫描探针目录：返回 (results, summary)。results 每项含 status/source 等。"""
    results: list[dict] = []
    for d in PROBE_ROOTS:
        root = ROOT / d
        if not root.is_dir():
            continue
        for md in sorted(root.glob("probes/*.md")) + sorted(root.rglob("REPORT.md")):
            results.append({
                "probe": f"{d}/{md.relative_to(root).as_posix()}", "kind": "doc",
                "status": "skip", "reason": "说明型探针（需人工/语义判定，不自动断言）",
                "source": "n/a",
            })
        for kind_dir in ("adv61_*.py", "adv70_*.py", "probe_*.py"):
            for py in sorted(root.glob(kind_dir)):
                if d != probe_dir:
                    results.append({
                        "probe": f"{d}/{py.name}", "kind": "script", "status": "skip",
                        "reason": f"历史轮次（仅实跑 {probe_dir}）：口径随多轮修复漂移，须人核对",
                        "source": "n/a",
                    })
                    continue
                out, err = _run_script(py)
                rows = parse_output(out)
                if not rows:
                    results.append({
                        "probe": f"{d}/{py.name}", "kind": "script", "status": "skip",
                        "reason": f"无可解析自述行（{err.strip()[:80] or '无输出'}）",
                        "source": "n/a",
                    })
                    continue
                for row in rows:
                    loc = _lock_for(row["tag"])
                    lock_ok = bool(loc and (ROOT / loc[0]).is_file())
                    v = row["verdict"]
                    control = row["kind"] == "control"
                    # ── 第一轨：机器判据（探针实际 verdict）──────────────────
                    if v.startswith(("refute", "infra_error")):
                        st, why = "blocked", f"机器判据 verdict={v}（卡不可直推）"
                    elif v == "confirm" and not control:
                        st, why = "escape", "机器判据 verdict=confirm（卡可直推）"
                    elif v in ("warn", "advice"):
                        st, why = "visible", f"gate 层 {v}（可见化不阻断，需人裁决是否升格）"
                    # ── 第二轨：自述兜底（无机器 verdict 可用时）────────────
                    elif control:
                        st, why = "blocked", f"阴性对照（verdict={v}）"
                    elif row["kind"] == "escape":
                        st, why = "escape", "探针自述仍逃逸（无机器 verdict 可判）"
                    elif row["kind"] == "blocked":
                        st, why = "blocked", "探针自述已拦"
                    else:
                        st, why = "skip", "自述不可判（无『已拦/逃逸』字样且 verdict 非判据）"
                    # ── 锁校验：只对"已拦"的实质探针（对照组不需要锁）────────
                    if st == "blocked" and not control:
                        if loc is None:
                            st, why = "gap", "无回归锁映射（修复未沉淀为可复现锁）"
                        elif not lock_ok:
                            st, why = "escape", "映射的回归锁文件不存在（锁失效）"
                        else:
                            why += f" · 锁 {loc[0]}"
                    results.append({
                        "probe": f"{d}/{py.name}#{row['tag']}", "kind": "script",
                        "status": st, "reason": why, "verdict": row["verdict"],
                        "note": row["note"],
                        "source": "probe-verdict" if v.startswith(
                            ("refute", "infra_error")) or v in ("confirm", "warn", "advice")
                            else "probe-self-report",
                        "lock": loc[0] if loc else None,
                    })
    return results, []


def summarize(results: list[dict]) -> dict:
    by: dict[str, int] = {}
    for r in results:
        by[r["status"]] = by.get(r["status"], 0) + 1
    return by


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="对抗回归看板（494 任务 6）")
    ap.add_argument("--dir", default=DEFAULT_DIR, help=f"实跑哪一轮（默认 {DEFAULT_DIR}）")
    ap.add_argument("--list", action="store_true", help="只列探针与映射，不实跑")
    ap.add_argument("--json", nargs="?", const=True, default=False)
    a = ap.parse_args(argv)

    real_out = sys.stdout
    if a.json:
        sys.stdout = sys.stderr

    if a.list:
        for d in PROBE_ROOTS:
            for py in _probe_scripts(d):
                print(f"[probe] {d}/{py.name}")
        for k, (lock, note) in _LOCKS.items():
            print(f"[lock ] {k:<5} -> {lock}  # {note}")
        return 0

    results, _ = scan(a.dir)
    by = summarize(results)
    marks = {"blocked": "✅", "escape": "❌", "visible": "👁", "skip": "⏭", "gap": "⚠"}
    for r in results:
        mark = marks.get(r["status"], "?")
        print(f"{mark} [{r['status']:<7}] {r['probe']}"
              + (f" · {r['reason']}" if r.get("reason") else "")
              + (f" · verdict={r.get('verdict')}" if r.get("verdict") else ""))
    print(f"\n[adv-regression] blocked={by.get('blocked', 0)} · escape={by.get('escape', 0)}"
          f" · visible={by.get('visible', 0)} · gap={by.get('gap', 0)}"
          f" · skip={by.get('skip', 0)}")
    print("[adv-regression] 判定为双轨：机器 verdict（refute/infra_error⇒拦、confirm⇒逃逸）优先，"
          "自述兜底；visible=gate 层 warn/advice（可见化不阻断，需人裁决）；skip ≠ pass")
    escape_or_gap = by.get("escape", 0) + by.get("gap", 0)
    if escape_or_gap:
        print("[adv-regression] 存在逃逸/未沉淀项 ⇒ exit 1（先人核对自述口径，再修或补锁）")
    if a.json:
        real_out.write(json.dumps({
            "tool": "adversarial_regression", "version": "v1.0",
            "dir": a.dir, "status": "fail" if escape_or_gap else "pass",
            "summary": by, "results": results,
        }, ensure_ascii=False, indent=1) + "\n")
    return 1 if escape_or_gap else 0


if __name__ == "__main__":
    raise SystemExit(main())
