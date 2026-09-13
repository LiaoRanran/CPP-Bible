#!/usr/bin/env python3
"""一键仓库状态：git 状态分类 + ahead 数 + 未跟踪资产盘点 + 门禁快览。

用法：
    python scripts/repo_status.py
    python scripts/repo_status.py --json

只读，不修改任何文件。给人/Agent 开工前的"我在哪"快照。
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> str:
    p = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return (p.stdout or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    info: dict = {}

    # 分支与 ahead/behind
    info["branch"] = git("rev-parse", "--abbrev-ref", "HEAD")
    info["ahead"] = int(git("rev-list", "--count", "origin/master..HEAD") or 0)
    info["behind"] = int(git("rev-list", "--count", "HEAD..origin/master") or 0)
    info["last_commit"] = git("log", "-1", "--oneline")

    # porcelain 状态分类
    porcelain = git("status", "--porcelain")
    modified, untracked, deleted, renamed = [], [], [], []
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:].strip().strip('"')
        if code.startswith("R"):
            renamed.append(path)
        elif code == "??":
            untracked.append(path)
        elif code.startswith("D"):
            deleted.append(path)
        elif code.startswith("M") or code[1] == "M":
            modified.append(path)

    info["modified"] = modified
    info["untracked"] = untracked
    info["deleted"] = deleted
    info["renamed"] = renamed

    # 未跟踪按顶层目录分类
    untracked_dirs = Counter()
    for p in untracked:
        top = p.split("/")[0].split("\\")[0]
        untracked_dirs[top] += 1
    info["untracked_by_dir"] = dict(untracked_dirs)

    # 关键计数
    for name, pattern in [
        ("atoms", "atoms/**/*.md"),
        ("evidence", "evidence/**/*.md"),
        ("misconceptions", "misconceptions/**/*.md"),
        ("arch_docs", "References/architecture_架构演进/*.md"),
        ("tools", "tools/*.py"),
        ("tests", "tests/*.py"),
    ]:
        info[f"count_{name}"] = len(list(ROOT.glob(pattern)))

    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0

    print(f"{'='*60}")
    print(f"  仓库状态快照")
    print(f"{'='*60}")
    print(f"  分支     : {info['branch']}  (ahead {info['ahead']} / behind {info['behind']})")
    print(f"  最新提交 : {info['last_commit']}")
    print(f"{'─'*60}")
    print(f"  已修改   : {len(modified)}")
    for p in modified[:10]:
        print(f"    M {p}")
    if len(modified) > 10:
        print(f"    ... 还有 {len(modified)-10} 个")
    print(f"  已删除   : {len(deleted)}  {deleted[:5] if deleted else ''}")
    print(f"  已重命名 : {len(renamed)}")
    print(f"  未跟踪   : {len(untracked)}")
    for d, c in untracked_dirs.most_common():
        print(f"    {d}/ : {c} 个")
    print(f"{'─'*60}")
    print(f"  资产计数 :")
    print(f"    原子 {info['count_atoms']}  证据 {info['count_evidence']}  误解 {info['count_misconceptions']}")
    print(f"    架构文档 {info['count_arch_docs']}  工具 {info['count_tools']}  测试 {info['count_tests']}")
    print(f"{'='*60}")
    if info["ahead"] > 0:
        print(f"  ⚠️  {info['ahead']} 条提交未推送（需用户在可连通网络 git push）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
