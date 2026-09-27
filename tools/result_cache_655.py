#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""result_cache_655.py — pytest 结果缓存（**哈希校验**，655 C 杠杆 2）。

目标
====
同一份输入不该跑第二遍：CI 重跑、批内反复验证、门禁多阶段复用，都属"输入没变"。
本工具按 **输入内容哈希** 记录"这一组测试 + 这一组依赖文件 ⇒ 这个结果"，
命中时可直接跳过重跑（由调用方决定跳过还是仍然跑）。

为什么不是 `--lf/--cacheprovider`
=================================
pytest 自带的 cache 以**用例名**为键、以 **mtime/上次结果**为依据，既不校验依赖文件内容，
也不区分"配置/解释器变了"。本工具把**内容哈希**做成命中的唯一依据：

1. 键 = `sha256(canonical_json({nodeids, inputs{path:sha256}, env{python,pytest,config}))`；
2. 条目内**逐文件**保存 sha256，`--lookup/--verify` 时**重算比对**，任何漂移 ⇒ miss；
3. 条目自带 `entry_sha256`（排除自身字段后的规范化哈希）⇒ 手改缓存会被 `--verify` 抓到。

用法
====
    python tools/result_cache_655.py --key --tests tests/test_655_tools.py
    python tools/result_cache_655.py --lookup <key>
    python tools/result_cache_655.py --record --junit data/655_junit_fast.xml
    python tools/result_cache_655.py --verify          # 逐条重算输入哈希（陈旧/篡改体检）
    python tools/result_cache_655.py --prune --keep-days 30
    python tools/result_cache_655.py --check           # 自检（tmp 目录，不碰生产缓存）

诚实边界
========
- **不改变 pytest 行为**（不是插件）：是否跳过重跑由调用方决定，本工具只回答"输入是否一模一样"；
- 只缓存**结果摘要**（通过/失败/跳过计数与墙钟），不缓存 stdout/日志；
- 缓存**不是信任根的一部分**（不在 `.tool_checksums` 内）；它可能被删、被清，命中与否**不得**影响判决。
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

CACHE = ROOT / "data" / "655_result_cache.json"
SCHEMA = "cppbible-result-cache/1.0"

#: 环境指纹：解释器/测试器/配置变了 ⇒ 缓存必须作废
ENV_FILES = ("pyproject.toml", "tests/conftest.py", "conftest.py")


def _sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def env_fingerprint() -> dict[str, str]:
    env = {"python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"}
    try:
        import pytest

        env["pytest"] = pytest.__version__
    except Exception:  # noqa: BLE001
        env["pytest"] = "unknown"
    for rel in ENV_FILES:
        p = ROOT / rel
        env[f"file:{rel}"] = _sha256_file(p) if p.is_file() else "absent"
    return env


def collect_inputs(tests: list[str]) -> dict[str, str]:
    """测试文件本身 + 它们**提到**的 tools/ 模块（粗粒度依赖面，宁可多哈希）。"""
    files: set[str] = set()
    for t in tests:
        tp = ROOT / t
        if tp.is_file():
            files.add(t)
    for t in tests:
        tp = ROOT / t
        if not tp.is_file():
            continue
        text = tp.read_text(encoding="utf-8", errors="replace")
        for cand in sorted((ROOT / "tools").glob("*.py")):
            mod = cand.stem
            if f"import {mod}" in text or f"{mod}.py" in text or f'"{mod}"' in text:
                files.add(cand.relative_to(ROOT).as_posix())
    return {rel: _sha256_file(ROOT / rel) for rel in sorted(files) if (ROOT / rel).is_file()}


def make_key(tests: list[str], inputs: dict[str, str] | None = None) -> str:
    payload = {"tests": sorted(tests), "inputs": inputs if inputs is not None else collect_inputs(tests),
               "env": env_fingerprint()}
    return hashlib.sha256(canonical(payload).encode()).hexdigest()


def _entry_hash(entry: dict[str, Any]) -> str:
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return hashlib.sha256(canonical(body).encode()).hexdigest()


def load(path: Path = CACHE) -> dict[str, Any]:
    if not path.is_file():
        return {"schema": SCHEMA, "entries": {}}
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"schema": SCHEMA, "entries": {}}
    if not isinstance(raw, dict):
        return {"schema": SCHEMA, "entries": {}}
    data: dict[str, Any] = raw
    if not isinstance(data.get("entries"), dict):
        data["entries"] = {}
    return data


def save(data: dict[str, Any], path: Path = CACHE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["schema"] = SCHEMA
    data["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
                    encoding="utf-8", newline="\n")


def parse_junit(path: Path) -> dict[str, Any]:
    root = ET.parse(str(path)).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    summary: dict[str, Any] = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0,
                               "duration_s": 0.0, "failed_nodeids": []}
    for s in suites:
        summary["tests"] += int(s.get("tests", 0))
        summary["failures"] += int(s.get("failures", 0))
        summary["errors"] += int(s.get("errors", 0))
        summary["skipped"] += int(s.get("skipped", 0))
        summary["duration_s"] += float(s.get("time", 0.0) or 0.0)
        for tc in s.iter("testcase"):
            if tc.find("failure") is not None or tc.find("error") is not None:
                summary["failed_nodeids"].append(f"{tc.get('classname', '')}::{tc.get('name', '')}")
    summary["duration_s"] = round(summary["duration_s"], 3)
    return summary


def record(key: str, summary: dict[str, Any], inputs: dict[str, str], path: Path = CACHE) -> str:
    data = load(path)
    entry: dict[str, Any] = {"created_at": dt.datetime.now().isoformat(timespec="seconds"),
                             "inputs": inputs, "summary": summary}
    entry["entry_sha256"] = _entry_hash(entry)
    data["entries"][key] = entry
    save(data, path)
    return str(entry["entry_sha256"])


def lookup(key: str, path: Path = CACHE) -> dict[str, Any]:
    """命中判定：条目存在 + **逐文件重算哈希一致** + 条目自哈希一致。"""
    data = load(path)
    entry = data["entries"].get(key)
    if not entry:
        return {"hit": False, "reason": "无此键（首次或输入已变）"}
    if entry.get("entry_sha256") != _entry_hash(entry):
        return {"hit": False, "reason": "条目自哈希不符 ⇒ 缓存被外部改动，拒绝采信"}
    drift: list[str] = []
    for rel, want in (entry.get("inputs") or {}).items():
        p = ROOT / rel
        got = _sha256_file(p) if p.is_file() else "absent"
        if got != want:
            drift.append(rel)
    if drift:
        return {"hit": False, "reason": f"依赖文件漂移 {len(drift)} 个", "drift": drift[:10]}
    return {"hit": True, "summary": entry.get("summary", {}), "created_at": entry.get("created_at")}


def verify(path: Path = CACHE) -> dict[str, Any]:
    data = load(path)
    bad_hash, drift = [], []
    for key, entry in data["entries"].items():
        if entry.get("entry_sha256") != _entry_hash(entry):
            bad_hash.append(key)
            continue
        for rel, want in (entry.get("inputs") or {}).items():
            p = ROOT / rel
            got = _sha256_file(p) if p.is_file() else "absent"
            if got != want:
                drift.append({"key": key, "file": rel})
    return {"entries": len(data["entries"]), "tampered": bad_hash,
            "stale_files": drift[:20], "stale_count": len(drift)}


def prune(keep_days: int, path: Path = CACHE) -> int:
    data = load(path)
    cutoff = dt.datetime.now() - dt.timedelta(days=keep_days)
    keep = {}
    for key, entry in data["entries"].items():
        try:
            ts = dt.datetime.fromisoformat(str(entry.get("created_at", "")))
        except ValueError:
            continue
        if ts >= cutoff:
            keep[key] = entry
    removed = len(data["entries"]) - len(keep)
    data["entries"] = keep
    save(data, path)
    return removed


def selftest() -> int:  # 需要 tmp 目录 ⇒ 由 tests/test_655_tools.py 覆盖真实路径
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    tmp = ROOT / ".pytest_tmp" / "cache655_selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    f = tmp / "dep.py"
    f.write_text("X = 1\n", encoding="utf-8")
    t = tmp / "test_dep.py"
    t.write_text("def test_x():\n    assert 1\n", encoding="utf-8")
    rel = f.relative_to(ROOT).as_posix()
    inputs = {rel: _sha256_file(f)}
    cpath = tmp / "cache.json"
    k = hashlib.sha256(canonical({"t": ["only-for-selftest"], "i": inputs}).encode()).hexdigest()
    record(k, {"tests": 1, "failures": 0}, inputs, cpath)
    chk("记录后可命中", lookup(k, cpath)["hit"] is True)
    f.write_text("X = 2\n", encoding="utf-8")
    miss = lookup(k, cpath)
    chk("依赖漂移 ⇒ miss", miss["hit"] is False and "漂移" in miss["reason"])
    inputs2 = {rel: _sha256_file(f)}
    record(k, {"tests": 1}, inputs2, cpath)
    chk("重录后可命中", lookup(k, cpath)["hit"] is True)
    d = load(cpath)
    d["entries"][k]["summary"]["tests"] = 999
    save(d, cpath)
    chk("篡改条目 ⇒ 拒绝采信", lookup(k, cpath)["hit"] is False)
    chk("verify 能报篡改", len(verify(cpath)["tampered"]) == 1)
    chk("prune 不误删新条目", prune(30, cpath) == 0)
    print(f"result_cache_655 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="pytest 结果缓存（哈希校验，655 C 杠杆 2）")
    ap.add_argument("--key", action="store_true", help="打印输入键")
    ap.add_argument("--tests", nargs="*", default=[], help="参与输入的测试文件")
    ap.add_argument("--lookup", metavar="KEY")
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--junit", help="--record 时读 junit XML")
    ap.add_argument("--key-hex", help="--record 时显式给键（否则用 --tests 现算）")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--prune", action="store_true")
    ap.add_argument("--keep-days", type=int, default=30)
    ap.add_argument("--clear", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        return selftest()
    if a.clear:
        save({"schema": SCHEMA, "entries": {}})
        print("[cache655] 已清空")
        return 0
    if a.verify:
        rep = verify()
        print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else
              f"[cache655] 条目 {rep['entries']}｜被篡改 {len(rep['tampered'])}｜依赖漂移 "
              f"{rep['stale_count']}")
        return 0 if not rep["tampered"] else 1
    if a.prune:
        print(f"[cache655] 清理 {prune(a.keep_days)} 条（keep_days={a.keep_days}）")
        return 0
    if a.lookup:
        rep = lookup(a.lookup)
        print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else
              (f"[cache655] HIT（{rep.get('created_at')}）：{rep.get('summary')}"
               if rep["hit"] else f"[cache655] MISS：{rep['reason']}"))
        return 0 if rep["hit"] else 1
    if a.record:
        if not a.junit:
            print("[cache655] --record 需要 --junit", file=sys.stderr)
            return 2
        inputs = collect_inputs(a.tests)
        key = a.key_hex or make_key(a.tests, inputs)
        summary = parse_junit(Path(a.junit))
        h = record(key, summary, inputs)
        print(f"[cache655] 已记录 key={key[:16]}… entry_sha256={h[:16]}… 摘要={summary}")
        return 0
    key = make_key(a.tests)
    print(json.dumps({"key": key, "tests": sorted(a.tests),
                      "inputs": len(collect_inputs(a.tests))}, ensure_ascii=False, indent=2)
          if a.json else f"[cache655] key={key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
