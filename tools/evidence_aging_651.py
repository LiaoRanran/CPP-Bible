#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""evidence_aging_651.py — H7 证据时效（651 W1，**只读/旁路**）。

为什么（651 W1-H7）：证据会过期——标准改版、编译器升级、卡被新证据取代。没有时效治理，
陈旧的 L1/L2 证据会被当"当前有效"反复引用。本工具做三件事，**只标不判**：

1. **时效计算**：读卡 frontmatter 的 `verified_at`，算 `age_days` 与 `recheck_after`
   （= verified_at + RECHECK_DAYS，默认 180 天）；过期 ⇒ 进**陈旧标记队列**。
2. **frontmatter 计划（dry-run，不写盘）**：为每张卡生成"拟新增字段"计划
   （`verified_at` 已有则不重复、`superseded_by=None`、`recheck_after=计算值`）。
   **不真写卡**：卡片内容寻址（PCK hash），写卡会致 hash 漂移（626/628 实证）⇒ 只出计划交人。
3. **订阅清单**：WG14/WG21 issue log + 编译器状态页清单，落 `data/651_h7_subscriptions.md`。

用法
====
    python tools/evidence_aging_651.py --check                       # 纯合成自检（CI 可跑，不读真卡）
    python tools/evidence_aging_651.py --scan [--today 2026-09-27]   # 真扫 atoms/evidence，出队列+计划+订阅清单
    python tools/evidence_aging_651.py --json                        # 打印 JSON

诚实边界：**不判断卡对错**，只报"多久没复核"；`superseded_by` 由人填，本工具只留空位。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:  # Windows 控制台 UTF-8（仓库既有工具）
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "evidence_aging_651", "entry": "scan",
                "description": "H7 证据时效：陈旧标记队列 + frontmatter 计划（只读）"}

RECHECK_DAYS_DEFAULT = 180
OUT_JSON = ROOT / "data" / "651_h7_aging.json"
OUT_QUEUE = ROOT / "data" / "651_h7_stale_queue.md"
OUT_SUBS = ROOT / "data" / "651_h7_subscriptions.md"

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_VERIFIED_AT_RE = re.compile(r"^verified_at:\s*(\S+)", re.MULTILINE)
_ID_RE = re.compile(r"^id:\s*(\S+)", re.MULTILINE)


@dataclass
class AgingRow:
    card: str
    path: str
    verified_at: str | None
    age_days: int | None
    recheck_after: str | None
    stale: bool


def _frontmatter(text: str) -> str | None:
    m = _FM_RE.match(text)
    return m.group(1) if m else None


def compute_aging(card_id: str, path: str, verified_at: str | None, today: str,
                  recheck_days: int = RECHECK_DAYS_DEFAULT) -> AgingRow:
    """给定 verified_at，算 age_days / recheck_after / stale（纯函数，可测）。"""
    if not verified_at:
        return AgingRow(card_id, path, None, None, None, False)
    try:
        v = _dt.date.fromisoformat(verified_at[:10])
        t = _dt.date.fromisoformat(today[:10])
    except ValueError:
        return AgingRow(card_id, path, verified_at, None, None, False)
    recheck = v + _dt.timedelta(days=recheck_days)
    return AgingRow(card_id, path, verified_at, (t - v).days, recheck.isoformat(), t > recheck)


def plan_frontmatter(row: AgingRow) -> dict:
    """拟新增字段计划（**不写盘**）；已存在 verified_at 则不重复计划。"""
    plan: dict = {"card": row.card, "add": {}, "note": "dry-run：不写卡（内容寻址，改了致 PCK hash 漂移）"}
    if row.verified_at is None:
        plan["add"]["verified_at"] = "<需人填>"
    plan["add"]["superseded_by"] = None
    plan["add"]["recheck_after"] = row.recheck_after
    return plan


def scan(today: str | None = None, recheck_days: int = RECHECK_DAYS_DEFAULT) -> dict:
    today = today or _dt.date.today().isoformat()
    rows: list[AgingRow] = []
    for sub in ("atoms", "evidence"):
        base = ROOT / sub
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if p.name.upper().startswith("README"):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            fm = _frontmatter(text)
            if fm is None:
                continue
            vm = _VERIFIED_AT_RE.search(fm)
            im = _ID_RE.search(fm)
            card_id = im.group(1) if im else p.stem
            rows.append(compute_aging(card_id, str(p.relative_to(ROOT)),
                                      vm.group(1).strip().strip('"') if vm else None,
                                      today, recheck_days))
    stale = [r for r in rows if r.stale]
    no_verified = [r for r in rows if r.verified_at is None]
    return {
        "today": today,
        "recheck_days": recheck_days,
        "total": len(rows),
        "with_verified_at": len(rows) - len(no_verified),
        "stale": len(stale),
        "no_verified_at": len(no_verified),
        "rows": [asdict(r) for r in rows],
        "plan": [plan_frontmatter(r) for r in rows if r.verified_at is not None],
    }


def _write_outputs(rep: dict) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# 651 H7 · 陈旧标记队列（只标不判）\n\n- today: {rep['today']}　recheck_days: {rep['recheck_days']}",
             f"- 卡总数 {rep['total']}｜有 verified_at {rep['with_verified_at']}｜无 verified_at {rep['no_verified_at']}｜**过期 {rep['stale']}**\n",
             "| 卡 | verified_at | age_days | recheck_after |", "|---|---|---|---|"]
    for r in rep["rows"]:
        if r["stale"]:
            lines.append(f"| {r['card']} | {r['verified_at']} | {r['age_days']} | {r['recheck_after']} |")
    if rep["stale"] == 0:
        lines.append("| （无） | | | |")
    lines.append("\n> 无 verified_at 的卡需人补；本队列**只标记**，不判卡对错。")
    OUT_QUEUE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    OUT_SUBS.write_text(SUBSCRIBE_DOC, encoding="utf-8")


SUBSCRIBE_DOC = """# 651 H7 · 外部变更订阅清单（证据时效）

> 证据会因**外部世界变化**而过期。以下清单供人工定期核对（本工具不抓网，只列清单）。

## 一、标准 issue log（条款可能改）
| 来源 | 地址 | 频率 |
|---|---|---|
| WG21（C++）邮件/issue | https://wg21.link/ / https://github.com/cplusplus/papers | 季度 |
| WG14（C）文档 | https://www.open-std.org/jtc1/sc22/wg14/www/docs/ | 季度 |
| cppreference 变更 | https://en.cppreference.com/w/ | 季度 |

## 二、编译器状态页（实测结论可能失效）
| 来源 | 地址 | 关注 |
|---|---|---|
| GCC release notes | https://gcc.gnu.org/gcc-15/changes.html | 语义/优化变更 |
| Clang release notes | https://releases.llvm.org/ | 语义/优化变更 |
| MSVC 更新 | https://learn.microsoft.com/en-us/cpp/ | 语义变更 |

## 三、触发口径
当上游发布新版本/新条款 ⇒ 相关卡 `recheck_after` 提前，重跑 L1 实测（648 探针模板）。
"""


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 过期：verified 2026-01-01，today 2026-09-27，180 天 ⇒ 过期
    r1 = compute_aging("A", "a.md", "2026-01-01", "2026-09-27", 180)
    chk("过期判定=True", r1.stale is True, f"age={r1.age_days}")
    chk("age_days 正确", r1.age_days == 269)
    chk("recheck_after=verified+180", r1.recheck_after == "2026-06-30")
    # 未过期：verified 2026-09-01 ⇒ 26 天 < 180
    r2 = compute_aging("B", "b.md", "2026-09-01", "2026-09-27", 180)
    chk("未过期判定=False", r2.stale is False)
    # 无 verified_at ⇒ 不判 stale，但进 no_verified
    r3 = compute_aging("C", "c.md", None, "2026-09-27", 180)
    chk("无 verified_at ⇒ stale False", r3.stale is False and r3.verified_at is None)
    # 计划含三字段
    plan = plan_frontmatter(r1)
    chk("计划含 superseded_by", "superseded_by" in plan["add"])
    chk("计划含 recheck_after", plan["add"]["recheck_after"] == "2026-06-30")
    # 坏日期不崩
    r4 = compute_aging("D", "d.md", "not-a-date", "2026-09-27", 180)
    chk("坏日期不崩", r4.age_days is None and r4.stale is False)
    print(f"evidence_aging_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 H7 证据时效（只读）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--today", default=None)
    ap.add_argument("--recheck-days", type=int, default=RECHECK_DAYS_DEFAULT)
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.scan:
        rep = scan(a.today, a.recheck_days)
        _write_outputs(rep)
        print(f"扫描卡 {rep['total']}｜有过期 {rep['stale']}｜无 verified_at {rep['no_verified_at']}"
              f"\n→ {OUT_QUEUE.name} / {OUT_JSON.name} / {OUT_SUBS.name}")
        return 0
    rep = scan(a.today, a.recheck_days)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json
          else f"total={rep['total']} stale={rep['stale']} no_verified_at={rep['no_verified_at']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
