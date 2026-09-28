#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""dco_check_657.py — 657 D2：DCO（Developer Certificate of Origin）签名检查。

判据（与 `DCO.md` / `.github/PULL_REQUEST_TEMPLATE.md` 的承诺一致）
================================================================
对提交区间内**每一个**提交：
1. 提交正文（含 trailer）必须含 `Signed-off-by: 姓名 <邮箱>`；
2. 该署名必须**恰好出现一次**（重复署名通常意味着合并/改写痕迹）；
3. 署名里的邮箱必须等于**作者（author）邮箱** —— 这是 `git commit -s` 的语义；
   代签（用别人的邮箱签名）在这里必然失败（本仓红线：**不代签**）。

豁免（逐条给理由，且**只对明确标注过的**生效）
==========================================
- **合并提交**（`parent 数 > 1`）：合并提交本身不引入内容，强制签名会让 rebase 流程瘫痪；
- 正文含 `[skip-dco]` 的提交：给**历史批量导入**留一条显式、可审计的口子
  （本仓 610 之前的提交未补签，属 655 交人项 2；本批**不代签**）。

区间口径
========
- 有 `DCO_BASE` / `GITHUB_BASE_REF` ⇒ `base..HEAD`；否则回退 `HEAD~1..HEAD`（push 单提交）。
- 显式 `--range A..B` 可复算任意区间（离线复核、CI 之外的本地预检都用它）。
- `--all` 扫全史（**会红**：历史未补签，这是**如实**的结果，不是缺陷）。

`--check` 只读自检（不依赖 git 状态）；`--report` 写 `data/657_dco_report.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

OUT_JSON = os.path.join(ROOT, "data", "657_dco_report.json")
SOB_RE = re.compile(r"^Signed-off-by:\s*(.+?)\s*<([^>]+)>\s*$", re.MULTILINE | re.IGNORECASE)
SKIP_TOKEN = "[skip-dco]"


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", check=False)
    return r.stdout if r.returncode == 0 else ""


def commits(rng: str) -> list[str]:
    out = git("rev-list", rng)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def inspect(sha: str) -> dict:
    body = git("log", "-1", "--format=%B", sha)
    mail = git("log", "-1", "--format=%aE", sha).strip()
    parents = [p for p in git("log", "-1", "--format=%P", sha).split() if p]
    subject = git("log", "-1", "--format=%s", sha).strip()
    rec: dict = {"sha": sha[:10], "subject": subject[:90], "author_mail": mail,
                 "merge": len(parents) > 1, "signed_off": [], "ok": True, "why": []}
    if rec["merge"]:
        rec["why"].append("合并提交 ⇒ 豁免")
        return rec
    if SKIP_TOKEN in body:
        rec["why"].append(f"正文含 {SKIP_TOKEN} ⇒ 显式豁免")
        return rec
    matches = SOB_RE.findall(body)
    rec["signed_off"] = [f"{n} <{m}>" for n, m in matches]
    if not matches:
        rec["ok"] = False
        rec["why"].append("缺 Signed-off-by（`git commit -s`）")
    elif len(matches) > 1:
        rec["ok"] = False
        rec["why"].append(f"Signed-off-by 出现 {len(matches)} 次（期望 1 次）")
    elif matches[0][1].strip().lower() != mail.strip().lower():
        rec["ok"] = False
        rec["why"].append(f"署名邮箱 {matches[0][1]} ≠ 作者邮箱 {mail}（不得代签）")
    else:
        rec["why"].append("签名合规")
    return rec


def default_range() -> str:
    base = os.environ.get("DCO_BASE") or ""
    if not base and os.environ.get("GITHUB_BASE_REF"):
        base = f"origin/{os.environ['GITHUB_BASE_REF']}"
    if base:
        return f"{base}..HEAD"
    return "HEAD~1..HEAD"


def run(rng: str) -> dict:
    shas = commits(rng)
    rows = [inspect(s) for s in shas]
    bad = [r for r in rows if not r["ok"]]
    return {"range": rng, "total": len(rows), "failed": len(bad),
            "rows": rows, "bad": bad}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="657 D2 DCO 签名检查")
    ap.add_argument("--range", default=None, help="ex 或 A..B（默认按 CI 环境推断）")
    ap.add_argument("--all", action="store_true", help="扫全史（会红：历史未补签）")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rng = "HEAD" if a.all else (a.range or default_range())
    rep = run(rng)
    if a.report:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(rep, fh, ensure_ascii=False, indent=2)
    if a.json:
        print(json.dumps({k: v for k, v in rep.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
    for r in rep["bad"]:
        print(f"::error::DCO 不合规 {r['sha']} {r['subject']} ⇒ {'; '.join(r['why'])}")
    print(f"[dco657] 区间 {rep['range']}：{rep['total']} 个提交，"
          f"不合规 {rep['failed']}")
    return 1 if rep["failed"] else 0


def selftest() -> int:
    """只读自检：**用合成样本**验判据（不依赖当前仓库的提交状态）。"""
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    good = "feat: x\n\nSigned-off-by: A <a@x.com>\n"
    bad_missing = "feat: x\n"
    bad_msgs = "feat: x\n\nSigned-off-by: A <a@x.com>\nSigned-off-by: A <a@x.com>\n"
    bad_wrong = "feat: x\n\nSigned-off-by: B <b@x.com>\n"
    skip = f"feat: x {SKIP_TOKEN}\n"
    chk("合规样本：签名恰好 1 次且邮箱一致",
        len(SOB_RE.findall(good)) == 1 and SOB_RE.findall(good)[0][1] == "a@x.com")
    chk("缺签名被判不合规", SOB_RE.findall(bad_missing) == [])
    chk("重复签名可被识别（>1 次）", len(SOB_RE.findall(bad_msgs)) == 2)
    chk("代签可被识别（邮箱不一致）",
        SOB_RE.findall(bad_wrong)[0][1] != "a@x.com")
    chk("skip 标记生效", SKIP_TOKEN in skip)
    # 真实仓库跑一遍默认区间（只读；不因结果影响自检）
    rng = default_range()
    rep = run(rng)
    print(f"  [info] 真实区间 {rng}：{rep['total']} 个提交，不合规 {rep['failed']}")
    chk("输出路径落在 data/ 下",
        OUT_JSON.replace("\\", "/").endswith("data/657_dco_report.json"))
    print(f"dco_check_657 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
