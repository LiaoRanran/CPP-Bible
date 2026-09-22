"""626 A2 · 控制字符检测器与清洗器（纯标准库）

外部大模型发现：`data/` 下多个报告（尤其 PCK 报告）含 `0x08` / `0x0B` 等控制字符，
导致 `verifier` 等文本出现字符损坏，也不利于跨平台发布。

模式：
- `--check`：只检测，列出含控制字符的文件（exit 1 = 发现）
- `--fix`：清洗（删除 0x00-0x1F 中除 \\n(0x0A) \\r(0x0D) 之外的字符），**写回原文件**
- `--scan-dir`：指定目录（默认 `data/`）

安全：只处理文本后缀；清洗前保留 `.bak`？——**不保留**（保持仓库整洁），但 `--check` 先跑可预览。
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TEXT_EXT = (".md", ".json", ".jsonl", ".yaml", ".yml", ".txt", ".html")
CTRL = set(range(0x00, 0x20)) - {0x0A, 0x0D}


def scan(target: str) -> list[tuple[str, list[str]]]:
    """扫描目录，返回 [(相对路径, [控制字符 hex 列表])]。"""
    out: list[tuple[str, list[str]]] = []
    for dirpath, _dn, fns in os.walk(target):
        for fn in sorted(fns):
            if not fn.endswith(TEXT_EXT):
                continue
            p = os.path.join(dirpath, fn)
            try:
                with open(p, "rb") as fh:
                    data = fh.read()
            except OSError:
                continue
            hits = sorted({c for c in data if c in CTRL})
            if hits:
                out.append((os.path.relpath(p, ROOT), [hex(h) for h in hits]))
    return sorted(out)


def clean_file(path: str) -> int:
    """清洗单个文件，返回删除的字符数；未变更则 0。"""
    with open(path, "rb") as fh:
        data = fh.read()
    new = bytes(b for b in data if b not in CTRL)
    if new == data:
        return 0
    with open(path, "wb") as fh:
        fh.write(new)
    return len(data) - len(new)


def selftest() -> int:
    import tempfile
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "bad.md")
        good = os.path.join(td, "good.md")
        with open(bad, "wb") as w1:
            w1.write(b"verifier\x08x\x0b\nend\n")
        with open(good, "w", encoding="utf-8") as w2:
            w2.write("clean\ntext\n")
        found = scan(td)
        chk("检出 1 个含控制字符文件", len(found) == 1, str(found))
        chk("检出的字符含 0x8/0xb",
            any("0x8" in h or "0xb" in h for _p, h in found))
        n = clean_file(bad)
        chk("清洗删除了 2 个字符", n == 2, f"(删除 {n})")
        chk("清洗后无残留", scan(td) == [])
        with open(bad, "rb") as r1:
            chk("换行保留", b"\n" in r1.read())
        chk("干净文件不被改动", clean_file(good) == 0)
    print(f"A2 cleaner selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 A2 控制字符检测/清洗")
    ap.add_argument("--check", action="store_true", help="只检测（默认）；或自检")
    ap.add_argument("--fix", action="store_true", help="清洗写回")
    ap.add_argument("--scan-dir", default=None, help="扫描目录（默认 data/）")
    ap.add_argument("--selftest", action="store_true", help="运行内置自检")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    target = args.scan_dir or os.path.join(ROOT, "data")
    found = scan(target)
    for p, h in found:
        print(f"  {p}: {h}")
    print(f"scan {target}: {len(found)} file(s) with control chars")
    if args.fix:
        total = 0
        for p, _h in found:
            total += clean_file(os.path.join(ROOT, p))
        print(f"fixed: removed {total} control chars from {len(found)} file(s)")
        left = scan(target)
        print(f"rescan: {len(left)} file(s) remaining")
        return 0 if not left else 1
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
