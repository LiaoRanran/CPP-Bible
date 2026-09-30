#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ci_check.py — 检出率断言必须带**区间**（Clopper–Pearson 95%，口径见 `research/ci_policy.md`）。

病（`_arch_v47/32` + 667 复盘 A2）：
  论文/文档里到处是裸的 `k/n` 与 `xx.x%`：`6/6 = 100%` 没有下界、`0/8 = 0%` 没有上界、
  `14/32 = 43.8%` 没有区间。裸点估计是审稿人**一击致命**的地方——
  "零样本断言零失效率"（"C 层检出率 0%"）在统计上是**覆盖率**问题：n=8 且 k=0 时，
  真实率高达 **36.9%** 都与观测相容（C-P 上界）。
  768 口径：所有 k/n 一律报 **Clopper–Pearson 精确区间**（`method="beta"`，
  实现单一来源 = `tools/stat_bounds.py::cp_interval`），论文表另加 Wilson 作敏感性列。

判据（本工具只做这一件事，机器可判）：
  一行里出现「**检出率类断言**」（k/n 且同行含比率关键词或百分号）⇒ 同一行（或紧邻下一行）
  必须出现 **CI 标记**（`95% CI` / `CI [` / `Clopper` / `[lo, hi]` 形态）。
  缺 ⇒ `G-CI-REQUIRED`（block，exit 1）。

**刻意的豁免机制（可见、不静默）**：
  * 代码围栏（```…```）内不判——那是命令/输出，不是断言；
  * 行尾写 `<!-- ci-check: ignore（理由） -->` 可豁免**该行**，理由必须写在注释里（可审计）；
  * `n == 0` 的分数（`0/0`）不判"缺 CI"（不可判），但必须在 `--report` 里显形。

用法：
    python tools/ci_check.py research/                 # 扫指定目录（默认 research/）
    python tools/ci_check.py research/paper_v0.5.md    # 扫单文件
    python tools/ci_check.py --report research/        # 只列出断言与 CI 状态，不判红
    python tools/ci_check.py --selftest                # 自检（含"缺 CI 必红"的射程自检）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

#: k/n 分数（避免日期 `2026/09/30` 与路径：两侧不能是数字/点/斜杠/减号）
FRAC_RE = re.compile(r"(?<![\d/.\-])(\d{1,5})\s*/\s*(\d{1,5})(?![\d/.\-])")
#: CI 标记（任一命中即算"带区间"）
CI_MARKERS = (
    re.compile(r"95\s*%\s*CI", re.IGNORECASE),
    re.compile(r"\bCI\s*\["),
    re.compile(r"Clopper", re.IGNORECASE),
    re.compile(r"\[\s*\d+(\.\d+)?\s*[%]?\s*[,–\-—~]\s*\d+(\.\d+)?\s*[%]?\s*\]"),
    re.compile(r"置信区间"),
)
#: 比率关键词（决定一行里的 k/n 是否算"检出率断言"）
RATE_WORDS = ("检出率", "命中率", "逃逸率", "误报率", "覆盖率", "检出力", "catch", "miss",
              "召回", "recall", "precision", "精度", "通过率", "失败率", "率")
#: 显式豁免注释（理由必须写在括号里）
IGNORE_RE = re.compile(r"ci-check:\s*ignore\s*[（(]([^）)]+)[）)]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


#: **豁免台账**（可见的迁移积压，不是静默白名单）：路径 → 理由。要纳入射程就删掉对应行。
#: 口径演进写在 `research/ci_policy.md` §冻结与豁免。
EXEMPT: dict[str, str] = {
    # 冻结历史稿：v0.1–v0.3 是各自时点口径的快照，追改等于改写历史记录。
    "research/paper_v0.1.md": "冻结历史稿（快照口径，不追改）",
    "research/paper_v0.2.md": "冻结历史稿（快照口径，不追改）",
    "research/paper_v0.3.md": "冻结历史稿（快照口径，不追改）",
    # 并行起草中的 v0.5 草稿：由 669 P4 终稿（research/paper_v0.5.md）承接并补 CI。
    "research/paper_draft_v0.5.md": "并行草稿，待并入 P4 终稿 paper_v0.5.md 时统一补 CI",
}


def exempt_reason(path_str: str) -> str | None:
    return EXEMPT.get(path_str)


def _rel(p: Path) -> str:
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:                          # 仓外文件（自检用的临时目录）
        return p.as_posix()


def _iter_lines(path: Path) -> list[tuple[int, str, bool]]:
    """返回 [(行号, 文本, 是否在代码围栏内)]。"""
    out: list[tuple[int, str, bool]] = []
    in_fence = False
    for i, ln in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            out.append((i, ln, True))
            continue
        out.append((i, ln, in_fence))
    return out


def _has_ci(text: str) -> bool:
    return any(rx.search(text) for rx in CI_MARKERS)


def _is_claim(line: str, frac: re.Match) -> bool:
    """该 k/n 是否算"检出率断言"：同行含比率关键词，或紧邻百分号。"""
    if any(w in line for w in RATE_WORDS):
        return True
    tail = line[frac.end():frac.end() + 3]
    head = line[max(0, frac.start() - 3):frac.start()]
    return "%" in tail or "%" in head


def scan(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    """扫描：返回 (findings, sightings)。findings = 缺 CI 的断言（红）；sightings = 全部断言。"""
    findings: list[dict] = []
    sightings: list[dict] = []
    for p in paths:
        if exempt_reason(_rel(p)):
            continue
        for no, ln, in_fence in _iter_lines(p):
            if in_fence or IGNORE_RE.search(ln):
                continue
            for m in FRAC_RE.finditer(ln):
                k, n = int(m.group(1)), int(m.group(2))
                if k > n:
                    continue
                # 编号语境（"威胁 7/8"、"T-1/5"）：那是威胁编号，不是比例断言。
                ctx = ln[max(0, m.start() - 8):m.start()]
                if any(w in ctx for w in ("威胁", "threat", "Threat", "T-")):
                    continue
                # 标识符/路径语境（"A5 / 08_metrics"）：两侧贴字母或下划线 ⇒ 不是比例断言。
                if (m.start() and (ln[m.start() - 1].isalpha() or ln[m.start() - 1] == "_")) \
                        or (m.end() < len(ln) and (ln[m.end()].isalnum() or ln[m.end()] == "_")):
                    continue
                if not _is_claim(ln, m):
                    continue
                ok = _has_ci(ln)
                rec = {"file": _rel(p), "line": no,
                       "k": k, "n": n, "has_ci": ok, "text": ln.strip()[:160]}
                sightings.append(rec)
                if not ok and n > 0:
                    findings.append(rec)
    return findings, sightings


def collect(paths: list[Path] | None = None) -> tuple[list[dict], list[dict]]:
    if paths:
        targets = [q for p in paths for q in ([p] if p.is_file() else sorted(p.rglob("*.md")))]
    else:
        targets = sorted((ROOT / "research").rglob("*.md"))
    return scan(targets)


def _fmt(f: dict) -> str:
    return f"  [G-CI-REQUIRED] {f['file']}:{f['line']}  {f['k']}/{f['n']} 缺 CI —— {f['text']}"


def selftest() -> int:
    """射程自检：**缺 CI 必红**。用内存里造的文本跑真判据（不写盘）。"""
    fails: list[str] = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)

        def _write(name: str, text: str) -> Path:
            f = d / name
            f.write_text(text, encoding="utf-8")
            return f

        f1 = _write("a.md", "- holdout 检出率 14/16 = 87.5%\n")
        f2 = _write("b.md", "- holdout 检出率 14/16 = 87.5%（95% CI 63.9–97.2）\n")
        f3 = _write("c.md", "- 外部 corpus 14/32 = 43.8%（Clopper–Pearson [26.4, 62.3]）\n")
        f4 = _write("d.md", "```\n14/16 = 87.5%  检出率\n```\n")
        f5 = _write("e.md", "- 检出率 14/16 <!-- ci-check: ignore（本节是历史记录） -->\n")
        f6 = _write("f.md", "- 日期 2026/09/30 的批次\n")
        f7 = _write("g.md", "- 0/0 不可判\n")
        chk("裸 14/16 ⇒ 红", [Path(x["file"]).name for x in scan([f1])[0]] == ["a.md"])
        chk("带 CI ⇒ 绿", scan([f2])[0] == [])
        chk("Clopper 形态 ⇒ 绿", scan([f3])[0] == [])
        chk("代码围栏内不判", scan([f4])[0] == [])
        chk("显式豁免注释 ⇒ 绿", scan([f5])[0] == [])
        chk("日期不误判", scan([f6])[0] == [])
        chk("0/0 不判缺 CI", scan([f7])[0] == [])
    for f in fails:
        print(f"FAIL: {f}")
    print(f"ci_check selftest: {'PASS' if not fails else 'FAIL'}")
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="k/n 检出率断言必须带 Clopper–Pearson 95% CI")
    ap.add_argument("paths", nargs="*", default=[], help="文件或目录（默认 research/）")
    ap.add_argument("--report", action="store_true", help="只列断言与 CI 状态，不判红")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    paths = [Path(p) if Path(p).is_absolute() else ROOT / p for p in a.paths] or None
    findings, sightings = collect(paths)
    for s in sightings:
        flag = "✅" if s["has_ci"] else "❌"
        print(f"  {flag} {s['file']}:{s['line']}  {s['k']}/{s['n']}  {s['text'][:110]}")
    if a.report:
        print(f"\n[ci_check] 断言 {len(sightings)} 条，其中缺 CI {len(findings)} 条（--report 不判红）")
        return 0
    for f in findings:
        print(_fmt(f))
    print(f"\n[ci_check] {'PASS' if not findings else 'FAIL'}："
          f"{len(sightings) - len(findings)}/{len(sightings)} 条断言带 CI")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
