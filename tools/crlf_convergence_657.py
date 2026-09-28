#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""crlf_convergence_657.py — 657 D1：行尾（CRLF/LF）漂移的**度量**与**按策略收敛**。

先读规则再动手（`.gitattributes` 里已经写死了一条**监工裁决**）
==============================================================
`.gitattributes` 2026-09-13 原文记录：

> 裁决：不做一次性 renormalize。理由：①437 个文件的假 M 会淹没真实改动，等于给下一次
> 真实回归提供藏身处；②历史上它曾让工作树清洁检查恒红，使门禁沦为"狼来了"。
> 策略 = **碰到即转**（逐步迁移）：谁修改某个 .cpp，谁顺手把它转成 LF 一并提交。

所以本工具**不**擅自把全仓 renormalize（那是被明确裁决过的事，且要牵动 Merkle 根与
`artifact_sha256` 这类**字节即身份**的证据），而是：

1. **度量**：用 `git ls-files --eol` 给出真实分布（索引侧 / 工作树侧交叉表），
   并把「索引 LF + 工作树 CRLF」这一**真漂移**与 `.bat/.cmd/.ps1`（规则要求 CRLF）
   和 `-text`（.asm/.out 等，**字节即身份、永不转换**）区分开；
2. **按策略收敛**：`--migrate <paths...>` 把**本批碰到的文件**转成 LF（碰到的即转），
   转换前逐文件断言"只变行尾、字节内容不变（去掉 CR 后逐字节相同）"；
3. **如实登记**：`--report` 把"全量 renormalize 未做（前置裁决未撤销）"与剩余漂移
   数量一起写进 `data/657_crlf_convergence.md`，不含糊其辞。

红线自查（`--check`）：`.gitattributes` 必须仍然 ①`* text=auto eol=lf`、
②把 `.bat/.cmd/.ps1` 钉 CRLF、③把 `*.asm/*.out/*.o/*.obj/*.exe` 标 `-text`。
任一被改动 ⇒ 直接 FAIL（这三条是"字节即身份"的地基，不能悄悄被撼动）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

OUT_MD = os.path.join(ROOT, "data", "657_crlf_convergence.md")
OUT_JSON = os.path.join(ROOT, "data", "657_crlf_convergence.json")

#: 规则要求 CRLF 的文件（`.gitattributes` 明写）
CRLF_BY_RULE = (".bat", ".cmd", ".ps1")
#: `-text`（字节即身份）的文件（`.gitattributes` 明写）
BINARY_BY_RULE = (".asm", ".out", ".o", ".obj", ".exe")


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", check=False)
    return r.stdout


def census() -> dict[str, Any]:
    """索引侧/工作树侧 EOL 交叉表 + 真漂移清单。"""
    raw = git("ls-files", "--eol")
    table: Counter[tuple[str, str]] = Counter()
    drift: list[str] = []
    rule_crlf: list[str] = []
    binary: list[str] = []
    mixed: list[str] = []
    for line in raw.splitlines():
        # 格式：`i/lf  w/crlf  attr/text=auto eol=lf<TAB>path`
        # 注意 attr 段**含空格** ⇒ 不能按空白切整行（首版按 split(None,3) 取路径，
        # 结果把 "eol=lf\tpath" 当路径 ⇒ 漂移恒为 0，是**假绿**，已被本注释钉住）。
        head, _, path = line.partition("\t")
        toks = head.split()
        if len(toks) < 2 or not path:
            continue
        i, w = toks[0], toks[1]
        table[(i, w)] += 1
        if w in ("w/crlf", "w/mixed") and i == "i/lf":
            drift.append(path)
        if w == "w/crlf" and i == "i/crlf":
            rule_crlf.append(path)
        if i == "i/-text" or w == "w/-text":
            binary.append(path)
        if "mixed" in i or "mixed" in w:
            mixed.append(path)
    return {"table": {f"index={k[0]}|wt={k[1]}": v for k, v in sorted(table.items())},
            "n_tracked": sum(table.values()),
            "drift_lf_index_crlf_wt": sorted(drift),
            "n_drift": len(drift),
            "crlf_both_rule_based": sorted(rule_crlf),
            "binary_identity": sorted(binary),
            "mixed_eol": sorted(mixed)}


def at_to_lf(paths: list[str]) -> dict[str, Any]:
    """把给定文件的工作树内容转成 LF。**只变行尾**（剥离 CR 后逐字节必须相同）。"""
    changed, skipped, failed = [], [], []
    for rel in paths:
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            failed.append(f"{rel}: 文件不存在")
            continue
        if rel.endswith(BINARY_BY_RULE):
            skipped.append(f"{rel}: `-text`（字节即身份）⇒ 拒绝转换")
            continue
        if rel.endswith(CRLF_BY_RULE):
            skipped.append(f"{rel}: 规则要求 CRLF ⇒ 拒绝转换")
            continue
        raw = open(p, "rb").read()
        if b"\r\n" not in raw:
            skipped.append(f"{rel}: 已是 LF")
            continue
        new = raw.replace(b"\r\n", b"\n")
        if new.replace(b"\n", b"") != raw.replace(b"\r\n", b""):
            failed.append(f"{rel}: 去掉 CR 后字节不一致（含裸 CR？）⇒ 拒绝写入")
            continue
        open(p, "wb").write(new)
        changed.append(rel)
    return {"changed": changed, "skipped": skipped, "failed": failed}


def check_rules() -> list[str]:
    """`.gitattributes` 三条地基是否还在（缺任一即 FAIL）。"""
    text = open(os.path.join(ROOT, ".gitattributes"), encoding="utf-8").read()
    errs = []
    if "* text=auto eol=lf" not in text:
        errs.append("缺 `* text=auto eol=lf`（手写文本统一 LF 的总开关）")
    for ext in CRLF_BY_RULE:
        if f"*{ext}" not in text or "eol=crlf" not in text:
            errs.append(f"缺 `*{ext} text eol=crlf`（Windows 脚本依赖 CRLF）")
            break
    for ext in BINARY_BY_RULE:
        if f"*{ext}" not in text or "-text" not in text:
            errs.append(f"缺 `*{ext} -text`（字节即身份，禁止行尾转换）")
            break
    return errs


def report(c: dict[str, Any]) -> str:
    L = ["# 657 D1 · 行尾（CRLF/LF）漂移度量与收敛", "",
         "> 工具：`tools/crlf_convergence_657.py`；度量命令 = `git ls-files --eol`。", "",
         "## 一、真实分布（索引侧 × 工作树侧）", "",
         f"- 跟踪文件总数：**{c['n_tracked']}**；", "",
         "| 组合 | 文件数 |", "|---|---:|"]
    for k, v in c["table"].items():
        L.append(f"| `{k}` | {v} |")
    L += ["",
          "## 二、真漂移（索引 LF + 工作树 CRLF）", "",
          f"- 数量：**{c['n_drift']}** 个；",
          f"- 抽样（前 10）：{', '.join('`' + p + '`' for p in c['drift_lf_index_crlf_wt'][:10])}",
          "",
          "> 读法：这一栏才是「漂移」。`index=crlf|wt=crlf`（"
          f"**{len(c['crlf_both_rule_based'])}** 个）是 `.bat/.cmd/.ps1`，规则**要求** CRLF；"
          f"`index=-text` 一类（**{len(c['binary_identity'])}** 个）是 `.asm/.out` 等"
          "**字节即身份**的证据工件，**永不做行尾转换**。", "",
          "## 三、本批按「碰到即转」收敛的文件", "",
          "见 `data/657_crlf_convergence.json` 的 `migrated` 字段（只列本批改动的文件，"
          "转换前后**剥离 CR 后逐字节相同**）。", "",
          "## 四、为什么**不**做一次性全量 renormalize（如实登记）", "",
          "`.gitattributes` 里 2026-09-13 的**监工裁决**原文是「暂不 renormalize」，"
          "理由两条：",
          "",
          "1. 数百个文件的**假 M** 会淹没真实改动，给下一次真实回归提供藏身处；",
          "2. 历史上它曾让「工作树清洁检查」恒红，使门禁沦为「狼来了」。",
          "",
          "该裁决**未被本批任务书撤销**，因此本工具只执行裁决写明的 **「碰到即转」** 策略，"
          "并把全量 renormalize（含 Merkle 根/`artifact_sha256` 的连带重建与 OTS 重锚）"
          "登记为**交人项**。这不是「没做」，是「不该由苦力单方面做」。", ""]
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="657 D1 行尾漂移度量 / 碰到即转")
    ap.add_argument("--check", action="store_true", help="只读自检（含 .gitattributes 地基）")
    ap.add_argument("--migrate", nargs="*", default=None, help="要转成 LF 的文件（相对路径）")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        errs = check_rules()
        c = census()
        print(f"  [{'ok' if not errs else 'FAIL'}] .gitattributes 三条地基"
              + (f" · {errs}" if errs else "（LF 总开关 / 脚本 CRLF / 证据 -text）"))
        print(f"  [ok] 跟踪文件 {c['n_tracked']}；真漂移（索引LF+工作树CRLF）{c['n_drift']}")
        print(f"  [ok] 规则要求 CRLF 的脚本 {len(c['crlf_both_rule_based'])}；"
              f"字节即身份 -text {len(c['binary_identity'])}")
        print(f"crlf_convergence_657 selftest: {'PASS' if not errs else 'FAIL'}")
        return 0 if not errs else 1
    c = census()
    migrated: dict[str, Any] = {}
    if a.migrate:
        migrated = at_to_lf(a.migrate)
        c["migrated"] = migrated
        print(f"[crlf657] 转换 {len(migrated['changed'])} 个；跳过 {len(migrated['skipped'])}；"
              f"拒绝 {len(migrated['failed'])}")
        for x in migrated["failed"]:
            print(f"  !! {x}")
    if a.report:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({k: (v if not isinstance(v, list) or len(v) < 500 else v[:500])
                       for k, v in c.items()}, fh, ensure_ascii=False, indent=2)
        open(OUT_MD, "w", encoding="utf-8", newline="\n").write(report(c) + "\n")
        print(f"[crlf657] 已写 {os.path.relpath(OUT_MD, ROOT)}")
    if a.json:
        print(json.dumps({k: v for k, v in c.items() if not isinstance(v, list)},
                         ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
