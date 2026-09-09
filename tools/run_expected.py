"""run_expected.py — 运行含 //@ 期望标记的 main 块并逐条断言 stdout。

L2 真机深耕会在会产生输出的语句行尾写 `//@ <期望>`。此前该标记纯装饰、无人校验；
本工具把它变成可执行断言：整块独立编译并运行，若 stdout 与期望不符即为失败。

契约（今后写 //@ 必须遵守，详见本文件 docstring）：
  1. `//@` 只放在会向 stdout 输出的一句之后；
  2. `//@` 之后到行尾的文本 = 期望值，运行结果（空白折叠后）必须是 stdout 的
     **连续子串**；多个期望按代码顺序各匹配一次；
  3. 期望内**不得夹带注记**（中文解释/括注请放代码行上方的 `//` 行，或删除）；
     旧块若含注记会先判 FAIL，需手工迁移后再纳入。
  4. `//@` 后为空 = UNVERIFIED（不构成断言，应删去或补全）。

判定：
  PASS          编译运行且所有期望按序命中
  FAIL          某期望未命中（给出实际 stdout 供对比）
  COMPILE_ERR   块编译失败（自包含块不应发生；报首行错误）
  RUN_ERR       运行超时 / 退出码非 0
  UNVERIFIED    含空 //@ 或该行不产出可验证输出
  NO_MARK       块无 main 或无 //@（不跑）

用法：
  python tools/run_expected.py --all                 # 全库
  python tools/run_expected.py --chapter ch42        # 单章
  python tools/run_expected.py --changed             # git 变更文件
  python tools/run_expected.py --all --json rep.json --check
                                                     # --check: 有 FAIL/COMPILE_ERR/RUN_ERR 即退出码 1
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compile_all import extract_blocks, resolve_gcc  # noqa: E402

BOOK: Path = Path(__file__).resolve().parent.parent / "Book"
SKIP_DIRS = {"_legacy_ModernCppBible"}
SKIP_FILES = {"SUMMARY.md", "GLOSSARY.md", "PREREQUISITES.md", "INDEX.md", "MANIFEST.md"}
GCC = resolve_gcc(None)
FLAGS = "-std=c++23 -O2"
TIMEOUT = 15
MARKER_RE = re.compile(r"//@\s*(.*)$")
MAIN_RE = re.compile(r"\bint\s+main\s*\(")

PASS = "PASS"
FAIL = "FAIL"
COMPILE_ERR = "COMPILE_ERR"
RUN_ERR = "RUN_ERR"
UNVERIFIED = "UNVERIFIED"
NO_MARK = "NO_MARK"


@dataclass
class Block:
    stem: str
    rel: str
    index: int
    body: str
    markers: list[str]
    status: str = NO_MARK
    detail: str = ""
    stdout: str = ""


def iter_md_files(book: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(book.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        out.append(p)
    return out


def normalize(s: str) -> str:
    return re.sub(r"[ \t]+", " ", s)


def split_block_bodies(path: Path) -> list[str]:
    """返回每个 ```cpp 块的正文文本（含围栏内所有行，不剥 include）。"""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    bodies: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        if lines[i].strip().startswith("```cpp"):
            j = i + 1
            buf: list[str] = []
            while j < n and lines[j].strip() != "```":
                buf.append(lines[j])
                j += 1
            bodies.append("\n".join(buf))
            i = j + 1
        else:
            i += 1
    # 与 extract_blocks 的 1-based 编号对齐（两者都按 ```cpp 顺序数）
    return bodies


def markers_of(body: str) -> list[str]:
    out: list[str] = []
    for ln in body.split("\n"):
        m = MARKER_RE.search(ln)
        if m:
            out.append(m.group(1).strip())
    return out


def make_blocks(path: Path) -> list[Block]:
    stems = path.stem
    bodies = split_block_bodies(path)
    if len(bodies) != len(extract_blocks(path.read_text(encoding="utf-8"))):
        raise SystemExit("block 数不一致（解析 bug）")
    blocks: list[Block] = []
    for i, body in enumerate(bodies, 1):
        mk = markers_of(body)
        has_main = bool(MAIN_RE.search(body))
        if not mk or not has_main:
            continue
        rel = path.relative_to(BOOK).as_posix()
        blocks.append(Block(stem=stems, rel=rel, index=i, body=body, markers=mk))
    return blocks


def run_one(blk: Block) -> Block:
    nonempty = [e for e in blk.markers if e]
    if len(nonempty) != len(blk.markers):
        blk.status = UNVERIFIED
        blk.detail = "含空 //@ 标记"
        return blk
    with tempfile.TemporaryDirectory(prefix="rexp_") as td:
        td_p = Path(td)
        src = td_p / "b.cpp"
        exe = td_p / "b.exe"
        src.write_text(blk.body + "\n", encoding="utf-8")
        try:
            c = subprocess.run(
                [GCC, *FLAGS.split(), str(src), "-o", str(exe)],
                capture_output=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            blk.status = RUN_ERR
            blk.detail = "编译超时"
            return blk
        if c.returncode != 0:
            blk.status = COMPILE_ERR
            first = (c.stderr or b"").decode("utf-8", "replace").strip().splitlines()
            blk.detail = (first[0][:160] if first else "unknown")
            return blk
        try:
            r = subprocess.run([str(exe)], capture_output=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            blk.status = RUN_ERR
            blk.detail = "运行超时(>15s)"
            return blk
        out = normalize(r.stdout.decode("utf-8", "replace"))
        blk.stdout = r.stdout.decode("utf-8", "replace")
        if r.returncode != 0:
            blk.status = RUN_ERR
            blk.detail = f"运行退出码 {r.returncode}"
            return blk
        pos = 0
        for e in blk.markers:
            ne = normalize(e)
            idx = out.find(ne, pos)
            if idx < 0:
                blk.status = FAIL
                blk.detail = f"期望未命中: {e!r}"
                return blk
            pos = idx + len(ne)
        blk.status = PASS
        return blk


def collect(paths: list[Path]) -> list[Block]:
    blocks: list[Block] = []
    for p in paths:
        blocks.extend(make_blocks(p))
    return blocks


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="运行含 //@ 期望标记的 main 块并断言 stdout")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--chapter", help="章前缀，如 ch42")
    g.add_argument("--changed", action="store_true")
    ap.add_argument("--json", dest="json_path", help="写 JSON 报告")
    ap.add_argument("--check", action="store_true", help="存在 FAIL/ERR 即退出码 1")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args(argv)

    if a.chapter:
        hits = [p for p in iter_md_files(BOOK) if p.stem.startswith(a.chapter)]
        if len(hits) != 1:
            raise SystemExit(f"expected 1 file, got {len(hits)}")
        paths = hits
    elif a.changed:
        base = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], capture_output=True, text=True)
        ref = base.stdout.strip() if base.returncode == 0 else "HEAD"
        out = subprocess.run(
            ["git", "diff", "--name-only", f"{ref}..HEAD", "--", "Book"],
            capture_output=True, text=True)
        changed = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
        paths = [BOOK / p for p in changed if p.endswith(".md") and (BOOK / p).exists()]
        if not paths:
            print("no changed Book files")
            return 0
    else:
        paths = iter_md_files(BOOK)

    blocks = collect(paths)
    if not blocks:
        print("no //@ main blocks selected")
        return 0
    with cf.ProcessPoolExecutor(max_workers=a.workers) as ex:
        results = list(ex.map(run_one, blocks))

    from collections import Counter
    cnt = Counter(b.status for b in results)
    print(f"blocks with //@ = {len(results)} | "
          f"PASS={cnt[PASS]} FAIL={cnt[FAIL]} COMPILE_ERR={cnt[COMPILE_ERR]} "
          f"RUN_ERR={cnt[RUN_ERR]} UNVERIFIED={cnt[UNVERIFIED]}")
    for b in results:
        if b.status != PASS:
            print(f"  [{b.status}] {b.rel} blk#{b.index}: {b.detail}")
            if b.status == FAIL:
                head = "\n".join(b.stdout.splitlines()[:3])
                print(f"      stdout(head): {head[:200]!r}")
    if a.json_path:
        Path(a.json_path).write_text(
            json.dumps([asdict(b) for b in results], ensure_ascii=False, indent=1),
            encoding="utf-8")
    bad = cnt[FAIL] + cnt[COMPILE_ERR] + cnt[RUN_ERR]
    if a.check and bad:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
