#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""counts_659.py — 语料基数唯一权威源（659 A/B3「去写死」）。

背景（657 D5 / 655 交人项 5）：650–652 把语料从 27 卡扩到 37 卡、并新增
`atoms/draft650/` 10 张草稿卡后，多批测试/工具自检里写死的计数断言（37 / 103 /
27 / 83）没有同步 ⇒ 大批「写死数字型」红斑。657 结论：**不是产品 bug**，
正确修法是「去写死」——让断言从事实源现算，而不是把数字改成新的写死值。

事实源（只读，零手写）：
  原子卡（实卡）= `atoms/**/ATOM-*.md` 且父目录不是 `draft650/`
  原子卡（草稿）= `atoms/draft650/ATOM-*.md`（650 批新增，仍计为卡）
  证据卡        = `evidence/**/EV-*.md`
  卡（实卡）= 原子实卡 + 证据卡      （历史口径 103）
  卡（全量）= 原子全量 + 证据卡      （当前口径 113）

口径依据：`data/655_baseline.md`「原子卡 47 = 37 实卡 + 10 draft650」、
`README.md` 卡数行、`tools/web_status_655.py::count_cards`。

用法：
    python tools/counts_659.py --json        # 打印现算 JSON
    python tools/counts_659.py --check       # 自检 + 打印（只读，exit 0=通过）
    python tools/counts_659.py --selftest    # 只做自检
    python tools/counts_659.py --md          # 生成 data/659_corpus_counts.md

测试/工具导入（tests 已把 tools/ 加入 sys.path）：
    import counts_659 as counts
    assert len(discover_atoms()) == counts.ATOMS_TOTAL
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DRAFT_DIR_NAME = "draft650"


def _atoms():
    real = draft = 0
    for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
        if p.parent.name == DRAFT_DIR_NAME:
            draft += 1
        else:
            real += 1
    return real, draft


def _evidence() -> int:
    d = ROOT / "evidence"
    if not d.is_dir():
        return 0
    return sum(1 for p in d.rglob("EV-*.md"))


def _propositions() -> int:
    """命题数（事实源 = **卡面** `claim_structured` 的条目总数）。

    口径（566/640）：一个 `claim_structured` 元素 = 一条命题；证据卡不带该字段（实测）。
    刻意**不读** `data/propositions.db`：那是派生库，派生坏了不该让"事实源"跟着坏；
    两者一致由 `tests/test_prop_graph.py` 的"派生 vs 事实源"断言来锁。

    666 A2 背景：659 曾想加这个常量但**回退**了——因为 `tests/test_prop_graph.py` 里
    `79` 一处指"命题总数"、一处指"已签数"，盲替 `PROPOSITIONS` 会把已签断言改错。
    本批按"逐断言建立事实源"重做：总数用本常量，**已签数**用 `st["by_signoff"]` 现算。
    """
    try:
        import yaml  # 运行时依赖（pyproject dependencies 已声明 pyyaml）
    except ImportError:                                    # 无 yaml ⇒ 不臆造数字
        return 0
    total = 0
    for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        try:
            meta = yaml.safe_load(text[3:end])
        except Exception:                                  # 卡面损坏由 gate 报，这里不重复
            continue
        if isinstance(meta, dict):
            cs = meta.get("claim_structured")
            if isinstance(cs, list):
                total += len(cs)
    return total


_ATOMS_REAL, _ATOMS_DRAFT = _atoms()
_EVIDENCE = _evidence()

#: 原子卡（不含 draft650）
ATOMS_REAL = _ATOMS_REAL
#: 原子卡（draft650）
ATOMS_DRAFT = _ATOMS_DRAFT
#: 原子卡（全量 = 实卡 + 草稿）——历史写死 37 的位置现应取此值
ATOMS_TOTAL = _ATOMS_REAL + _ATOMS_DRAFT
#: 证据卡
EVIDENCE_TOTAL = _EVIDENCE
#: 命题（卡面 `claim_structured` 条目总数）——666 A2 新增，见 `_propositions()` 的说明
PROPOSITIONS = _propositions()
#: 卡（实卡口径：原子实卡 + 证据卡）——历史写死 103 的位置现应取此值
CARDS_REAL = _ATOMS_REAL + _EVIDENCE
#: 卡（全量口径：原子全量 + 证据卡）——历史写死 83/103 的位置现应取此值
CARDS_TOTAL = ATOMS_TOTAL + _EVIDENCE


def snapshot() -> dict:
    return {
        "atoms_real": ATOMS_REAL,
        "atoms_draft": ATOMS_DRAFT,
        "atoms_total": ATOMS_TOTAL,
        "evidence_total": EVIDENCE_TOTAL,
        "cards_real": CARDS_REAL,
        "cards_total": CARDS_TOTAL,
    }


def selftest() -> list:
    """只读自检：结构与恒等式。返回失败项（空 = 通过）。"""
    fails = []
    s = snapshot()
    for k, v in s.items():
        if not isinstance(v, int) or v <= 0:
            fails.append("counts.%s 非正：%r" % (k, v))
    if s["atoms_total"] != s["atoms_real"] + s["atoms_draft"]:
        fails.append("atoms_total != atoms_real + atoms_draft")
    if s["cards_real"] != s["atoms_real"] + s["evidence_total"]:
        fails.append("cards_real != atoms_real + evidence_total")
    if s["cards_total"] != s["atoms_total"] + s["evidence_total"]:
        fails.append("cards_total != atoms_total + evidence_total")
    if s["cards_total"] < s["cards_real"]:
        fails.append("cards_total < cards_real（草稿卡数为负）")
    return fails


def render_md() -> str:
    s = snapshot()
    return (
        "# 659 · 语料基数（唯一权威源：`tools/counts_659.py` 现算）\n\n"
        "> 本文件由 `python tools/counts_659.py --md` 生成，**禁止手改**。\n"
        "> 口径依据：`data/655_baseline.md`（47 = 37 实卡 + 10 draft650）、`README.md`。\n\n"
        "| 量 | 值 | 事实源 |\n|---|---:|---|\n"
        f"| 原子卡·实卡 | {s['atoms_real']} | `atoms/*/ATOM-*.md`（不含 `draft650/`） |\n"
        f"| 原子卡·草稿 | {s['atoms_draft']} | `atoms/draft650/ATOM-*.md` |\n"
        f"| 原子卡·全量 | {s['atoms_total']} | 实卡 + 草稿 |\n"
        f"| 证据卡 | {s['evidence_total']} | `evidence/**/EV-*.md` |\n"
        f"| 卡·实卡口径 | {s['cards_real']} | 原子实卡 + 证据卡（历史写死 103 的口径） |\n"
        f"| 卡·全量口径 | {s['cards_total']} | 原子全量 + 证据卡（当前口径） |\n"
        "\n"
        "## 去写死规则（659 A/B3）\n\n"
        "1. 新写的断言**禁止**再裸写上述数字；一律 `import counts_659 as counts` 后\n"
        "   用 `counts.ATOMS_TOTAL` / `counts.CARDS_TOTAL` 等常量。\n"
        "2. 语义不同要选对常量：只遍历 5 个域目录（`conc/hist/lang/mem/ub`）的工具\n"
        "   应取 `ATOMS_REAL`（`tools/evidence_base_644.py::list_atoms` 即此口径）；\n"
        "   用 `atoms/**/ATOM-*.md` 通配符的工具应取 `ATOMS_TOTAL`。\n"
        "3. 语料真扩容后，本文件随 `--md` 自动更新；测试无需再改数字。\n"
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="659 语料基数唯一权威源")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--md", action="store_true", help="生成 data/659_corpus_counts.md")
    a = ap.parse_args(argv)
    if a.json:
        print(json.dumps(snapshot(), ensure_ascii=False, indent=2))
        return 0
    if a.md:
        out = ROOT / "data" / "659_corpus_counts.md"
        out.write_text(render_md(), encoding="utf-8", newline="\n")
        print("已生成 %s" % out.relative_to(ROOT).as_posix())
        return 0
    fails = selftest()
    for f in fails:
        print("FAIL: %s" % f)
    if a.selftest:
        print("counts_659 selftest: %s" % ("PASS" if not fails else "FAIL"))
        return 0 if not fails else 1
    print(json.dumps(snapshot(), ensure_ascii=False))
    print("counts_659 --check: %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
