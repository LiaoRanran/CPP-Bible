#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_metrics.py — 指标单一事实源的「落地校验器」

`metrics_snapshot.py` 负责**产出**事实（build/metrics.json），本工具负责
**保证各文档引用的是同一份事实**。

为什么需要它
============
建好事实源不等于文档会用它。2026-08-31 实测：README 里两处数字已与事实源
漂移（cpp 块写 7530 / 实为 7523；自包含章数写 112 / 实为 114），STATE.json
的 `last_commit` 停在 `4c5cb32`、落后 HEAD 24 个提交。根因是「文档手写、
无人校验」——本工具把这件事变成门禁。

设计取舍
========
- **散文文档只校验、不改写**。README / NEXT_LLM 的数字嵌在叙述里，程序
  改写极易破坏语义与语气；漂移时指名文件与行号报错，由人确认后改。
- **机器自有的 JSON 字段才 `--sync` 自动回写**（STATE.json 的
  `last_commit` / `last_updated` / `total_chapters`）——这些字段本身已在
  `fact_source` 里声明由事实源派生，回写它们不算「改写内容」。
- **事实取自实时扫描，而非 build/metrics.json 快照**。`build/` 未进 git，
  CI 全新 checkout 时该文件不存在；且快照可能陈旧（其 `commit` 字段落后
  于 HEAD）。实时扫描才是权威，快照只作缓存与人读。

用法
====
    python tools/gen_metrics.py             # 打印字段取值 + 校验结果
    python tools/gen_metrics.py --check     # 任一漂移即 exit 1（CI 用）
    python tools/gen_metrics.py --sync      # 回写 STATE.json 的派生字段
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA = ROOT / "metrics.schema.json"
COMPILE_REPORT = ROOT / "tools" / "compile_report.json"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from metrics_snapshot import build as scan_build  # noqa: E402


def _get(obj: Any, dotted: str) -> Any:
    """按 dotted path 取值，缺失返回 None。"""
    cur = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _git(*args: str) -> str:
    """仓库内执行 git；失败返回空串，绝不抛异常（门禁可用性优先）。"""
    try:
        r = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=15)
    except (OSError, subprocess.SubprocessError):
        return ""
    return (r.stdout or "").strip()


def resolve_fields(schema: dict, live: dict, report: dict) -> dict[str, Any]:
    """按 schema 解析全部字段。派生字段（ratio_pct）在第二趟，故不依赖声明顺序。"""
    raw: dict[str, Any] = {}
    derived: dict[str, tuple[str, dict]] = {}

    for name, spec in schema["fields"].items():
        src = spec["from"]
        if src == "ratio_pct":
            derived[name] = (name, spec)
            continue
        if src == "git":
            raw[name] = _git(*spec["cmd"].split())
        elif src == "date":
            raw[name] = dt.datetime.now().strftime(spec.get("fmt", "%Y-%m-%d"))
        elif src == "scan":
            raw[name] = _get(live, spec["path"])
        elif src == "compile_report":
            raw[name] = _get(report, spec["path"])
        else:
            raise ValueError(f"[{SCHEMA.name}] 未知字段来源 {src!r}（字段 {name}）")

    for name, (_, spec) in derived.items():
        num = raw.get(spec["num"])
        den = raw.get(spec["den"])
        raw[name] = round(num / den * 100) if isinstance(num, int) and den else None
    return raw


def _line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def run_checks(schema: dict, values: dict[str, Any]) -> list[str]:
    """校验各文档写死数字是否与事实源一致，返回问题描述列表（空 = 全通过）。"""
    problems: list[str] = []
    cache: dict[str, str] = {}

    for chk in schema["checks"]:
        rel = chk["file"]
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"{rel}: 文件不存在，无法校验")
            continue
        if rel not in cache:
            cache[rel] = path.read_text(encoding="utf-8", errors="replace")

        text = cache[rel]
        m = re.search(chk["regex"], text)
        if not m:
            problems.append(f"{rel}: 未匹配到 {chk['regex']!r}——文档结构变了，"
                            f"请更新 metrics.schema.json 的 checks")
            continue

        for i, field in enumerate(chk["expect"], start=1):
            expect = values.get(field)
            if expect is None:
                problems.append(f"{rel}:{_line_of(text, m.start())}: 字段 {field} 无取值，无法校验")
                continue
            got = m.group(i)
            if got != str(expect):
                problems.append(f"{rel}:{_line_of(text, m.start())}: 写死 {got}，"
                                f"事实源 {field}={expect}")
    return problems


def _write_json(path: Path, data: Any) -> None:
    """回写 JSON，保留原文件的行尾（CRLF/LF）与「末尾是否有换行」。

    STATE.json 是 CRLF 且无末尾换行；若统一按 LF + 末尾换行写回，会产出
    整文件伪 diff，把真正的一行变更淹没在 669 行噪声里。本项目
    core.autocrlf=false，行尾必须 bytes 级对齐。
    """
    raw = path.read_bytes()
    eol = "\r\n" if b"\r\n" in raw else "\n"
    trailing = raw.endswith(b"\n")
    with open(path, "w", encoding="utf-8", newline=eol) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        if trailing:
            f.write("\n")


def run_sync(schema: dict, values: dict[str, Any]) -> list[str]:
    """把 schema.sync 声明的机器自有字段回写到目标 JSON。返回变更描述。"""
    by_file: dict[str, list[dict]] = {}
    for item in schema["sync"]:
        by_file.setdefault(item["file"], []).append(item)

    changed: list[str] = []
    for rel, items in by_file.items():
        path = ROOT / rel
        if not path.is_file():
            changed.append(f"{rel}: 文件不存在，跳过")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        file_changes: list[str] = []
        for item in items:
            new = values.get(item["field"])
            old = _get(data, item["json_path"])
            if old == new:
                continue
            cur: Any = data
            parts = item["json_path"].split(".")
            for p in parts[:-1]:
                cur = cur[p]
            cur[parts[-1]] = new
            file_changes.append(f"{rel}: {item['json_path']} {old!r} -> {new!r}")
        if file_changes:
            _write_json(path, data)
            changed.extend(file_changes)
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description="指标单一事实源落地校验器")
    ap.add_argument("--check", action="store_true",
                    help="任一文档数字与事实源不一致即退出 1（CI 用）")
    ap.add_argument("--sync", action="store_true",
                    help="把 metrics.schema.json 的 sync 字段回写到目标 JSON")
    ap.add_argument("--quiet", action="store_true", help="只打印结论行")
    args = ap.parse_args()

    if not SCHEMA.is_file():
        print(f"[gen-metrics] ✗ 缺少 {SCHEMA}")
        return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    live = scan_build()
    report = json.loads(COMPILE_REPORT.read_text(encoding="utf-8")) \
        if COMPILE_REPORT.is_file() else {}

    values = resolve_fields(schema, live, report)

    if not args.quiet:
        print(f"[gen-metrics] 事实源：实时扫描 Book/ + {COMPILE_REPORT.name} + git")
        for name in schema["fields"]:
            print(f"  {name:<24} {values.get(name)}")

    problems = run_checks(schema, values)

    if args.sync:
        for line in run_sync(schema, values):
            print(f"  sync  {line}")

    if problems:
        print(f"\n[gen-metrics] ✗ {len(problems)} 处数字与事实源不一致：")
        for p in problems:
            print(f"  - {p}")
        print("\n  散文文档需人工改（数字嵌在叙述里，程序改写会破坏语义）；")
        print("  改完再跑本命令确认。若属文档结构变化，请更新 metrics.schema.json。")
        return 1

    print("\n[gen-metrics] ✅ 全部文档数字与事实源一致")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
