#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prepush_check.py — 本地 / pre-push 快速卫生门禁（复用 CI 的「快」校验）。

CI 里「快」校验（quality / consistency / metrics / compile_gate / audit / expected）
约 20–30s；「慢」校验（全量 compile）约 40–60min。本工具在 push 前本地跑全部
「快」校验 + 仓库卫生，任一不过即 exit 1，避免把注定红的提交推上去。

卫生规则（与 CI pre-push 卫生一致）：仓库根出现**未提交**（未跟踪 `??` 或被
.gitignore 吞掉但仍残留 `!!`）的 *.cpp / *.exe / *.o 即阻断——这些是编译产物，
不该进库。`_probe*`/`_tu_*` 等刻意开发草稿（.gitignore 已明确忽略）豁免；已跟踪的
改动由各自门禁管，不在此拦截。

工作树清洁规则（369 P1-3，与 CI Worktree Cleanliness 步同款）：受控目录
`Examples/atoms/` `atoms/` `evidence/` `tools/golden_state.json` 出现**任何**未提交
改动（含 ` M` 与 `??`）即阻断——replay 重编译可能改写 `Examples/atoms/*.asm`，被改写
而无人察觉会形成慢性漂移（下次 replay 以改写后工件为基准）。先提交或还原再 push。

用法
====
  python tools/prepush_check.py              # 快校验 + 卫生（默认）
  python tools/prepush_check.py --compile    # 额外增量编译变更章并 triage（抓编译回归）
  python tools/prepush_check.py --no-hygiene # 只跑校验，跳过卫生
  python tools/prepush_check.py --install-hook  # 安装为 .git/hooks/pre-push

注：`--compile` 用 compile_all.py --changed（仅变更章；无变更则回退全量，慎用于大改）。
推送时绕过本门禁用 `git push --no-verify`。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# 默认快校验（与 CI 的「快」校验对齐）。argv 相对仓库根。
CORE = [
    ("quality",       ["tools/cppbible.py", "check", "--stage", "quality"]),
    ("consistency",   ["tools/consistency_check.py"]),
    ("metrics",       ["tools/gen_metrics.py", "--check"]),
    ("compile_gate",  ["tools/compile_gate.py"]),
    ("exempt_audit",  ["tools/exempt_audit.py", "--check"]),
    ("expected(changed)", ["tools/run_expected.py", "--changed", "--check"]),
    # 星级格/结构：示例头 span 5 格制回潮即拦（与 CI 的 Star / H2 Audit 步骤对齐）
    ("star_h2",       ["tools/star_h2_audit.py", "check", "--star"]),
]

# --compile 额外项：增量编译变更章 + 对照基线 triage（抓「我的回归」）。
COMPILE_EXTRA = [
    ("compile(changed)", ["tools/compile_all.py", "--changed", "--main-only"]),
    ("triage(changed)",  ["tools/compile_triage.py", "--check"]),
]

ARTIFACT_RE = re.compile(r"^[^/\\]+\.(cpp|exe|o)$", re.IGNORECASE)
# 刻意开发草稿（.gitignore 已明确忽略），不应阻断 push
DEV_OK_RE = re.compile(r"^(_probe|_tu)[^/\\]*\.(cpp|exe|o)$", re.IGNORECASE)


def _run(name: str, argv: list[str]) -> tuple[bool, str]:
    """运行一个子工具，返回 (通过?, 摘要行)。"""
    exe = [sys.executable, str(ROOT / argv[0]), *argv[1:]]
    try:
        r = subprocess.run(exe, cwd=str(ROOT), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=600)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"运行失败: {e}"
    ok = r.returncode == 0
    lines = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]
    summary = lines[-1] if lines else f"exit={r.returncode}"
    return ok, summary


def _hygiene() -> tuple[bool, str]:
    """仓库根未提交（未跟踪 `??` 或被 ignore 但仍残留 `!!`）的编译产物阻断。

    用 `git status --porcelain --ignored` 才能看到被 .gitignore 吞掉的根级产物
    （如 `/*.cpp` 忽略的漏回根目录 .cpp）——这些正是 pre-push 卫生要拦的。
    已跟踪改动（如 ` M`）由各自门禁管，不在此拦截；`_probe*`/`_tu_*` 等刻意
    开发草稿（.gitignore 已明确忽略）豁免。
    """
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--ignored"],
                           cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=15)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"git 失败: {e}"
    bad = []
    for line in r.stdout.splitlines():
        if len(line) < 4 or line[:2] not in ("??", "!!"):
            continue
        path = line[3:].strip()
        if not ARTIFACT_RE.match(path):  # 仅仓库根级 *.cpp/*.exe/*.o
            continue
        if DEV_OK_RE.match(path):
            continue
        bad.append(path)
    if bad:
        return False, "未提交根级编译产物: " + ", ".join(bad)
    return True, "无未提交根级编译产物"


# 为何用 Examples/atoms/ 而非整个 Examples/（369 实测对任务书字面的收窄）：
# Examples/ 根下是 Book 章节示例（实测 437 个 .cpp 有历史行尾漂移：工作树 CRLF vs 索引 LF，
# 非本批产物；Windows git 因 stat 缓存不可见、WSL git 可见）——全目录检查会让 WSL 本地
# 预检恒红；而 replay 等工具只写 Examples/atoms/，收窄不损失判别力。
CORE_DIRTY_PATHS = ("Examples/atoms/", "atoms/", "evidence/", "tools/golden_state.json")


def _worktree_core_clean() -> tuple[bool, str]:
    """受控目录（Examples/ atoms/ evidence/ golden_state）不得有未提交改动。

    为什么（369 P1-3）：replay 会重编译夹具并可能改写 `Examples/*.asm`（默认自动
    restore，但失败时静默）；被改写而无人察觉时，下一次 replay 会以"被改写后的工件"
    为基准，形成慢性漂移。CI 侧同款检查见 ci.yml 的 Worktree Cleanliness 步（replay 后）。
    """
    try:
        r = subprocess.run(["git", "status", "--porcelain", "--", *CORE_DIRTY_PATHS],
                           cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"git 失败: {e}"
    dirty = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    if dirty:
        sample = "; ".join(d[:48] for d in dirty[:4])
        more = f" …共 {len(dirty)} 项" if len(dirty) > 4 else ""
        return False, f"受控目录有未提交改动：{sample}{more}（先提交或还原）"
    return True, "受控目录干净（Examples/ atoms/ evidence/ golden_state.json）"


def _install_hook() -> int:
    hook_dir = ROOT / ".git" / "hooks"
    hook = hook_dir / "pre-push"
    hook_dir.mkdir(parents=True, exist_ok=True)
    script = (
        "#!/bin/sh\n"
        "# 本地 pre-push 门禁（R6）：复用 CI 快校验 + 仓库卫生\n"
        "while read -r _line; do :; done   # 排空 stdin，避免 git 报错\n"
        'cd "$(git rev-parse --show-toplevel)" || exit 0\n'
        'PY=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || true)\n'
        'if [ -z "$PY" ]; then\n'
        '  echo "[prepush] 未找到 python，跳过本地门禁（推送仍进行）"\n'
        "  exit 0\n"
        "fi\n"
        '"$PY" tools/prepush_check.py\n'
    )
    hook.write_text(script, encoding="utf-8", newline="\n")
    try:
        hook.chmod(0o755)
    except OSError:
        pass
    print(f"[prepush] 已安装钩子：{hook}")
    print("          push 前会自动跑快校验 + 卫生；绕过用 `git push --no-verify`")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="本地/pre-push 快速卫生门禁")
    ap.add_argument("--compile", action="store_true",
                    help="额外增量编译变更章并 triage（抓编译回归；无变更回退全量）")
    ap.add_argument("--no-hygiene", action="store_true", help="跳过仓库卫生检查")
    ap.add_argument("--install-hook", action="store_true",
                    help="安装为 .git/hooks/pre-push")
    args = ap.parse_args()

    if args.install_hook:
        return _install_hook()

    selected = list(CORE)
    if args.compile:
        selected += COMPILE_EXTRA

    print("=== pre-push 快速门禁（复用 CI 快校验）===")
    if args.compile:
        print("  （含 --compile：增量编译变更章 + triage）")
    fails = 0
    for name, argv in selected:
        tool = ROOT / argv[0]
        if not tool.is_file():
            print(f"  [✗] {name}: 工具缺失 {argv[0]}")
            fails += 1
            continue
        ok, summary = _run(name, argv)
        mark = "✅" if ok else "✗"
        print(f"  [{mark}] {name}: {summary}")
        if not ok:
            fails += 1

    if not args.no_hygiene:
        ok, summary = _hygiene()
        print(f"  [{'✅' if ok else '✗'}] hygiene: {summary}")
        if not ok:
            fails += 1
        ok_wt, summary_wt = _worktree_core_clean()
        print(f"  [{'✅' if ok_wt else '✗'}] worktree: {summary_wt}")
        if not ok_wt:
            fails += 1

    print()
    if fails:
        print(f"[prepush] FAIL: {fails} 项未过，勿 push"
              f"（先修，或 `git push --no-verify` 强制）")
        return 1
    print("[prepush] ✅ 全部快校验通过，可 push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
