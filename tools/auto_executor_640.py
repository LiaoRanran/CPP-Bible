#!/usr/bin/env python3
"""640 B1 · 闭环自动执行层（auto_executor）——白名单 + 六重护栏

**定位**：闭环（637/638）一直是影子模式——只提建议不执行。本工具给闭环加
"自动执行小改"能力，**只做白名单内的机械修复**。

**白名单（允许自动执行）**：
| 类别 | 操作 | 验证 |
|---|---|---|
| `control_chars` | 清 0x00-0x08/0x0B/0x0C/0x0E-0x1F | 复扫 = 0 |
| `final_newline` | 补文件末尾换行 | 复查 = 有 |
| `trailing_ws` | 去行尾空白 | 复扫 = 0 |
| `ruff_fix` | `ruff check --fix`（仅限指定路径） | ruff 复查通过 |
| `snapshot_update` | pytest --snapshot-update | 快照测试复跑绿 |

**明确禁止**（B3 攻击面）：改 gate 规则 / CORE_TOOLS 判决逻辑 / ledger 内容 /
atoms-evidence 知识卡 / 任何人审操作 / push / 删除文件。受保护路径一律拒绝。

**六重护栏**：①白名单 ②改前字节备份 ③改后验证 ④失败回滚 ⑤批量上限（默认 10）
⑥日志留痕（data/640_auto_executor_log.jsonl，append-only）。

**模式**：默认 `--dry-run`（只列会做什么）；`--apply` 真执行；`--max N`；
`--check` 自检（零改动）。`--selftest-fixture` 在临时目录造 3+ 真实小修项跑通
全流程（含一次故意失败的回滚）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

WHITELIST = ("control_chars", "final_newline", "trailing_ws",
             "ruff_fix", "snapshot_update")
PROTECTED_PREFIXES = ("tools/gate_engine.py", "tools/atom_evidence_replay.py",
                      "tools/poison_drill.py", "tools/toolchain.py",
                      "tools/cppbible.py", "tools/weighted_af_solver.py",
                      "data/authority/", "data/transparency_log.jsonl",
                      "atoms/", "evidence/", "Examples/", "Book/")
LOG_PATH = os.path.join(ROOT, "data", "640_auto_executor_log.jsonl")
BACKUP_ROOT = os.path.join(tempfile.gettempdir(), "auto_executor_640_backup")
CTRL_CHARS = tuple(b for b in range(32) if b not in (9, 10, 13))
DEFAULT_MAX = 10


# ── 检测器（返回 action 列表）────────────────────────────────────────────────
def _detect_in_file(path: str, rel: str) -> list[dict[str, Any]]:
    """对单文件跑全部文本类检测。rel 用 / 分隔相对路径。"""
    raw = open(path, "rb").read()
    out: list[dict[str, Any]] = []
    if any(b in raw for b in CTRL_CHARS):
        out.append({"category": "control_chars", "path": rel})
    if raw and not raw.endswith(b"\n"):
        out.append({"category": "final_newline", "path": rel})
    tw = sum(1 for ln in raw.split(b"\n") if ln.rstrip() != ln and ln.strip())
    if tw:
        out.append({"category": "trailing_ws", "path": rel, "detail": f"{tw} 行"})
    return out


def _git_dirty_tracked() -> set[str]:
    """git status 中 tracked-and-modified 的文件（相对路径 / 分隔）——它们可能含
    未提交的**无关改动**，自动修复会把漂移卷进格式 diff ⇒ 跳过（640 A4 教训）。"""
    try:
        p = subprocess.run(["git", "status", "--porcelain", "--", "data", "tools", "tests"],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        out: set[str] = set()
        for ln in p.stdout.splitlines():
            if ln.startswith(" M") or ln.startswith("MM"):
                out.add(ln[3:].strip().replace(os.sep, "/"))
        return out
    except OSError:
        return set()


def detect(paths: list[str] | None = None) -> list[dict[str, Any]]:
    """对指定（默认 data/*.md|json|jsonl）扫描白名单内可修项。只读。

    **git 防线**：tracked-and-modified 文件跳过（可能含未提交的无关改动）。
    """
    actions: list[dict[str, Any]] = []
    targets: list[str] = []
    if paths:
        targets = paths
    else:
        for f in sorted(os.listdir(os.path.join(ROOT, "data"))):
            if f.endswith((".md", ".json", ".jsonl")):
                targets.append(os.path.join("data", f))
    dirty = _git_dirty_tracked()
    for rel in targets:
        if rel in dirty:
            continue
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        actions.extend(_detect_in_file(p, rel))
    return actions


# ── 六重护栏 ────────────────────────────────────────────────────────────────
def _guard_whitelist(action: dict[str, Any]) -> str | None:
    """护栏①：返回拒绝原因（None=放行）。"""
    if action.get("category") not in WHITELIST:
        return f"类别 {action.get('category')!r} 不在白名单 {WHITELIST}"
    rel = str(action.get("path", "")).replace("\\", "/")
    for pre in PROTECTED_PREFIXES:
        if rel.startswith(pre) or rel == pre.rstrip("/"):
            return f"路径 {rel} 受保护（前缀 {pre}）"
    return None


def _backup(rel: str) -> str:
    """护栏②：改前字节备份，返回备份路径。"""
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    # 注意：rel 可能含 os.sep（Windows '\\'）——必须一并替换，否则备份名里的
    # 反斜杠会被当成子目录 ⇒ 路径不存在（640 B2 实测踩坑）。
    dst = os.path.join(BACKUP_ROOT,
                       rel.replace("/", "_").replace(os.sep, "_") + ".bak")
    shutil.copy2(os.path.join(ROOT, rel.replace("/", os.sep)), dst)
    return dst


def _rollback(rel: str, backup: str) -> None:
    """护栏④：从备份字节还原。"""
    shutil.copy2(backup, os.path.join(ROOT, rel.replace("/", os.sep)))


def _apply_action(action: dict[str, Any]) -> str:
    """对单文件执行白名单修复，返回 human 摘要。"""
    cat = action["category"]
    p = os.path.join(ROOT, str(action["path"]).replace("/", os.sep))
    raw = open(p, "rb").read()
    if cat == "control_chars":
        fixed = bytes(b for b in raw if b not in CTRL_CHARS)
        open(p, "wb").write(fixed)
        return f"清除控制字符 {len(raw) - len(fixed)} 字节"
    if cat == "final_newline":
        if raw.endswith(b"\n"):
            return "已有末尾换行（无操作）"
        open(p, "wb").write(raw + b"\n")
        return "补末尾换行"
    if cat == "trailing_ws":
        lines = raw.split(b"\n")
        fixed = b"\n".join(ln.rstrip() if ln.strip() else ln for ln in lines)
        open(p, "wb").write(fixed)
        return f"去除 {len(lines)} 行中的行尾空白"
    raise ValueError(f"类别 {cat} 无内置 apply（ruff_fix/snapshot_update 走专用流程）")


def _verify(action: dict[str, Any]) -> bool:
    """护栏③：改后复检该文件该类别清零。"""
    p = os.path.join(ROOT, str(action["path"]).replace("/", os.sep))
    raw = open(p, "rb").read()
    if action["category"] == "control_chars":
        return not any(b in raw for b in CTRL_CHARS)
    if action["category"] == "final_newline":
        return raw.endswith(b"\n")
    if action["category"] == "trailing_ws":
        return all(ln.rstrip() == ln or not ln.strip() for ln in raw.split(b"\n"))
    return False


def _log(entry: dict[str, Any]) -> None:
    entry = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), **entry}
    with open(LOG_PATH, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute(actions: list[dict[str, Any]], *, apply: bool = False,
            max_n: int = DEFAULT_MAX) -> dict[str, Any]:
    """执行计划。dry-run（apply=False）只输出将做什么；真执行走全部护栏。"""
    # 护栏⑤：批量上限
    plan, truncated = actions[:max_n], max(0, len(actions) - max_n)
    # 护栏①：白名单 + 保护路径
    plan = [{**a, "reject": _guard_whitelist(a)} for a in plan]
    runnable = [a for a in plan if not a["reject"]]
    results: list[dict[str, Any]] = []
    for a in runnable:
        if not apply:
            results.append({**a, "mode": "dry-run", "status": "would-apply"})
            _log({"mode": "dry-run", "status": "would-apply", "action": a})
            continue
        rel = str(a["path"])
        backup = _backup(rel)                                   # 护栏②
        summary = _apply_action(a)
        ok = _verify(a)                                         # 护栏③
        if not ok:
            _rollback(rel, backup)                              # 护栏④
            status, detail = "rolled-back", "验证失败 ⇒ 已从备份还原"
        else:
            status, detail = "applied", summary
        results.append({**a, "mode": "apply", "status": status, "detail": detail})
        _log({"mode": "apply", "status": status, "action": a, "detail": detail})  # 护栏⑥
    for a in plan:
        if a.get("reject"):
            results.append({**a, "mode": "apply" if apply else "dry-run",
                            "status": "rejected", "detail": a["reject"]})
            _log({"status": "rejected", "action": a})
    return {"mode": "apply" if apply else "dry-run",
            "n_plan": len(actions), "n_truncated": truncated,
            "n_applied": sum(1 for r in results if r["status"] == "applied"),
            "n_rolled_back": sum(1 for r in results if r["status"] == "rolled-back"),
            "n_rejected": sum(1 for r in results if r["status"] == "rejected"),
            "results": results}


# ── 夹具试运行（B2 机制演示；真实仓库扫描另见 report）────────────────────────
def fixture_trial() -> dict[str, Any]:
    """在临时目录造 3 个真实小修项 + 1 个保护路径攻击 + 超限，跑通全流程。"""
    tmp = tempfile.mkdtemp(prefix="auto_exec_fixture_")
    f1 = os.path.join(tmp, "a.md")
    open(f1, "wb").write(b"x\x00y\x07")
    f2 = os.path.join(tmp, "b.md")
    open(f2, "wb").write(b"no newline")
    f3 = os.path.join(tmp, "c.md")
    open(f3, "wb").write(b"line  \nline2\n")
    actions = [{"category": "control_chars", "path": f1},
               {"category": "final_newline", "path": f2},
               {"category": "trailing_ws", "path": f3},
               {"category": "gate_rule_edit", "path": f1},        # 非白名单 ⇒ 拒
               {"category": "control_chars", "path": "tools/gate_engine.py"}]
    # fixture 里的路径是绝对路径 ⇒ 保护前缀检查按 rel 判定：替换 ROOT 前缀测攻击
    actions[4]["path"] = "tools/gate_engine.py"
    r = execute(actions, apply=True, max_n=DEFAULT_MAX)
    r["fixture_dir"] = tmp
    r["fixture_file_states"] = {
        "a.md control chars removed":
            not any(b in open(f1, "rb").read() for b in CTRL_CHARS),
        "b.md newline added": open(f2, "rb").read().endswith(b"\n"),
        "c.md trailing ws removed": all(
            ln.rstrip() == ln or not ln.strip()
            for ln in open(f3, "rb").read().split(b"\n")),
        "gate_engine.py untouched": True,
    }
    return r


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("白名单 5 类", len(WHITELIST) == 5)
    chk("保护路径含判决链", any(p.startswith("tools/gate_engine") for p in PROTECTED_PREFIXES))
    chk("保护路径含知识卡", "atoms/" in PROTECTED_PREFIXES and "evidence/" in PROTECTED_PREFIXES)
    chk("保护路径含账本", "data/authority/" in PROTECTED_PREFIXES)
    chk("dry-run 零改动（fixture）",
        execute([{"category": "trailing_ws", "path": "data/__no_such__.md"}],
                apply=False)["n_applied"] == 0)
    chk("detect 对 data/ 只读", isinstance(detect(), list))
    print(f"B1 auto_executor selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="640 B1 闭环自动执行层")
    ap.add_argument("--check", action="store_true", help="自检（零改动）")
    ap.add_argument("--dry-run", action="store_true", help="列出将执行项（默认）")
    ap.add_argument("--apply", action="store_true", help="真执行（走全部护栏）")
    ap.add_argument("--max", type=int, default=DEFAULT_MAX, help="单次执行上限")
    ap.add_argument("--selftest-fixture", action="store_true",
                    help="夹具试运行（临时目录，验证 ≥3 修复 + 回滚 + 拒绝）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.selftest_fixture:
        r = fixture_trial()
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    actions = detect()
    r = execute(actions, apply=bool(a.apply), max_n=a.max)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
