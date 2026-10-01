#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""rules_manifest_671g.py — 671g D1：判决规则版本钉扎（rules_version + rules_sha256）。

问题（671c #74）
==================
判决产物只说"67 条规则"，但不说是**哪一版的 67 条**：规则改了之后，旧判决能否用旧规则
复现无从核对。本工具把"规则集"钉成一份 manifest：

  * rules_version：语义化版本（MAJOR.MINOR.PATCH）；
  * rules_sha256：① 执行权威源 tools/gate_engine.py 的文件哈希；② 规则元组
    (id/title/severity/kind/basis/quadrant/scope/automated/meta) 按 id 排序后的规范化哈希
    （**不含 check 函数对象**）；
  * effective_date / supersedes / count / severity 分布 / rule_ids。

判决产物（verdict JSON）必须带 rules_version + rules_sha256 且与现行 manifest 一致
（门禁 G-RULES-PINNED）。旧判决在规则升级后应 supersedes 链上可追溯。

用法
====
    python tools/rules_manifest_671g.py --generate        # 生成/更新 manifest（--apply）
    python tools/rules_manifest_671g.py --check          # 校验 manifest 与现行规则一致
    python tools/rules_manifest_671g.py --stamp f.json   # 给一个判决产物钉扎（写入，--apply）
    python tools/rules_manifest_671g.py --verify-verdicts data/671g/verdicts  # 门禁用
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SCHEMA = "queyi-rules-manifest/671g"
MANIFEST_PATH = Path("data/rules_manifest_671g.json")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

#: 钉扎进规则哈希的字段（**排除 check 函数对象**——它不可序列化且实现细节易变）
RULE_FIELDS = ("id", "title", "severity", "kind", "basis", "quadrant",
               "scope", "automated", "meta")


def _canonical_rules(engine_module) -> list[dict[str, Any]]:
    out = []
    for r in engine_module.RULES:
        out.append({f: getattr(r, f, None) for f in RULE_FIELDS})
    out.sort(key=lambda d: str(d.get("id")))
    return out


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_manifest(root: Path = ROOT, *, version: str = "1.0.0",
                   supersedes: str | None = None) -> dict[str, Any]:
    """从现行 gate_engine.RULES 计算 manifest（纯读，不写）。"""
    sys.path.insert(0, str(root / "tools"))
    import gate_engine
    engine_p = root / "tools" / "gate_engine.py"
    engine_src = engine_p.read_text(encoding="utf-8") if engine_p.is_file() else ""
    rules = _canonical_rules(gate_engine)
    from collections import Counter
    sev = Counter(str(r.get("severity")) for r in rules)
    canon = json.dumps(rules, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "schema": SCHEMA,
        "rules_version": version,
        "rules_sha256": _sha256_text(canon),
        "engine_file_sha256": _sha256_text(engine_src),
        "effective_date": time.strftime("%Y-%m-%d"),
        "supersedes": supersedes,
        "count": len(rules),
        "severity": dict(sev),
        "rule_ids": [str(r["id"]) for r in rules],
        "canonical_fields": list(RULE_FIELDS),
        "generated_by": "tools/rules_manifest_671g.py",
    }


def load_manifest(root: Path = ROOT) -> dict[str, Any] | None:
    p = root / MANIFEST_PATH
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def verify(root: Path = ROOT, manifest: dict[str, Any] | None = None) -> list[str]:
    """返回问题清单；空 = manifest 与现行规则一致。"""
    man = manifest or load_manifest(root)
    if man is None:
        return [f"manifest 缺失：{MANIFEST_PATH.as_posix()}（跑 --generate）"]
    problems = []
    if not SEMVER_RE.match(str(man.get("rules_version", ""))):
        problems.append(f"rules_version 非语义化版本：{man.get('rules_version')!r}")
    cur = compute_manifest(root, version=str(man.get("rules_version", "1.0.0")),
                          supersedes=man.get("supersedes"))
    if man.get("count") != cur["count"]:
        problems.append(f"count 不一致：manifest={man.get('count')} 现行={cur['count']}")
    if man.get("rules_sha256") != cur["rules_sha256"]:
        problems.append("rules_sha256 与现行 gate_engine.RULES 不一致（规则变了，需 bump 版本并重钉扎）")
    if man.get("engine_file_sha256") != cur["engine_file_sha256"]:
        problems.append("engine_file_sha256 与 tools/gate_engine.py 不一致（执行权威源码已改）")
    if man.get("severity") != cur["severity"]:
        problems.append(f"severity 分布不一致：manifest={man.get('severity')} 现行={cur['severity']}")
    if man.get("rule_ids") != cur["rule_ids"]:
        problems.append("rule_ids 集合/顺序与现行规则不一致")
    return problems


def stamp_verdict(root: Path, verdict_path: Path,
                 manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """把 rules_version + rules_sha256 钉进一个判决产物（in-place，调用方负责授权）。"""
    man = manifest or load_manifest(root)
    if man is None:
        raise RuntimeError("manifest 缺失，先 --generate")
    d = json.loads(verdict_path.read_text(encoding="utf-8"))
    d["rules_version"] = man["rules_version"]
    d["rules_sha256"] = man["rules_sha256"]
    verdict_path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": str(verdict_path), "rules_version": d["rules_version"],
            "rules_sha256": d["rules_sha256"]}


def verify_verdicts(root: Path, verdict_dir: str | Path,
                  manifest: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """门禁：目录下每个判决 JSON 必须钉扎且与现行 manifest 一致。"""
    man = manifest or load_manifest(root)
    if man is None:
        return [{"rule": "G-RULES-PINNED", "severity": "block",
                 "target": str(verdict_dir), "message": "manifest 缺失，无法核验判决钉扎"}]
    out: list[dict[str, Any]] = []
    d = root / verdict_dir
    if not d.is_dir():
        return out                       # 目录不存在 ⇒ 未进射程（不判红）
    for p in sorted(d.glob("*.json")):
        try:
            v = json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            out.append({"rule": "G-RULES-PINNED", "severity": "block", "target": p.name,
                         "message": f"判决 JSON 解析失败：{e}"})
            continue
        rel = p.relative_to(root).as_posix()
        if v.get("rules_version") != man["rules_version"]:
            out.append({"rule": "G-RULES-PINNED", "severity": "block", "target": rel,
                         "message": f"rules_version={v.get('rules_version')!r} ≠ 现行 {man['rules_version']}"})
        if v.get("rules_sha256") != man["rules_sha256"]:
            out.append({"rule": "G-RULES-PINNED", "severity": "block", "target": rel,
                         "message": "rules_sha256 与现行规则集不一致（旧规则判决，需显式归档）"})
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D1：规则版本钉扎")
    ap.add_argument("--root", default=None)
    ap.add_argument("--version", default="1.0.0")
    ap.add_argument("--supersedes", default=None)
    ap.add_argument("--generate", action="store_true", help="生成/更新 manifest（写盘）")
    ap.add_argument("--check", action="store_true", help="校验 manifest 与现行规则一致")
    ap.add_argument("--stamp", default=None, help="给判决产物钉扎（写盘）")
    ap.add_argument("--verify-verdicts", default="data/671g/verdicts")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.generate:
        old = load_manifest(root)
        man = compute_manifest(root, version=a.version,
                              supersedes=a.supersedes or (old or {}).get("rules_version"))
        (root / MANIFEST_PATH).parent.mkdir(parents=True, exist_ok=True)
        (root / MANIFEST_PATH).write_text(
            json.dumps(man, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[rules-manifest] 已生成 {MANIFEST_PATH}：{man['rules_version']} "
              f"{man['count']} 条 sha={man['rules_sha256'][:12]}")
        return 0
    if a.stamp:
        print(json.dumps(stamp_verdict(root, Path(a.stamp)), ensure_ascii=False))
        return 0
    if a.check:
        probs = verify(root)
        print("[rules-manifest] " + ("PASS（与现行规则一致）" if not probs else "FAIL："))
        for p in probs:
            print(f"  - {p}")
        return 1 if probs else 0
    # 默认：打印 manifest + 校验判决目录
    man = load_manifest(root)
    if man:
        print(f"[rules-manifest] {man['rules_version']} count={man['count']} "
              f"sha={man['rules_sha256'][:12]}")
    f = verify_verdicts(root, a.verify_verdicts, man)
    print(f"[rules-manifest] verdicts={a.verify_verdicts} findings={len(f)}")
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if f else 0


if __name__ == "__main__":
    raise SystemExit(main())
