"""626 A1 · 关键统计数字重算与校验器（只读）

外部大模型审阅发现 4 个数值/统计错误（median 75→67.5、110→93 唯一、27→31 总豁免、README 大小口径）。
本工具**独立重算**所有关键数字，并校验文档是否已同步修正。

**只读**：不修改任何数据文件或报告；`--check` 返回 0 = 全部一致。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
EXEMPT = os.path.join(ROOT, "tools", "poison_exemptions.yaml")
L615 = os.path.join(ROOT, "data", "human_review_item_by_item_30_615.md")
L624 = os.path.join(ROOT, "data", "human_review_item_by_item_624.md")
HONESTY = os.path.join(ROOT, "data", "human_review_honesty_615.md")
EXPIRY = os.path.join(ROOT, "data", "exemption_expiry_615.md")

# 由外部大模型独立重算并经本工具复现的**正确值**
EXPECTED = {
    "annotations_n": 388,
    "authority_n": 418,
    "reason_min": 47,
    "reason_max": 80,
    "reason_mean": 69.20,
    "reason_median": 67.5,
    "unique_615": 30,
    "unique_624": 80,
    "overlap_615_624": 17,
    "union_615_624": 93,
    "exemptions_total": 31,
    "exemptions_legacy": 27,
    "exemptions_hc": 4,
}


def _jl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _edge_ids(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    return set(re.findall(r"ae-[A-Za-z0-9_:\->.]+", open(path, encoding="utf-8").read()))


def recompute() -> dict:
    ann = _jl(ANN)
    lens = [len(str(a.get("reason") or "")) for a in ann]
    a = _edge_ids(L615)
    b = _edge_ids(L624)
    ex_total = ex_legacy = ex_hc = 0
    if os.path.exists(EXEMPT):
        import yaml  # type: ignore[import-untyped]
        with open(EXEMPT, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        rows = raw.get("exemptions", raw) if isinstance(raw, dict) else raw
        ex_total = len(rows)
        ex_legacy = sum(1 for d in rows if str(d.get("redteam_seen")) == "legacy")
        ex_hc = ex_total - ex_legacy
    return {
        "annotations_n": len(ann),
        "authority_n": len(_jl(AUTH)),
        "reason_min": min(lens) if lens else 0,
        "reason_max": max(lens) if lens else 0,
        "reason_mean": round(statistics.mean(lens), 2) if lens else 0.0,
        "reason_median": statistics.median(lens) if lens else 0.0,
        "unique_615": len(a),
        "unique_624": len(b),
        "overlap_615_624": len(a & b),
        "union_615_624": len(a | b),
        "exemptions_total": ex_total,
        "exemptions_legacy": ex_legacy,
        "exemptions_hc": ex_hc,
    }


def check_docs() -> list[tuple[str, bool, str]]:
    """校验文档是否已同步修正（只读扫描关键字）。"""
    out: list[tuple[str, bool, str]] = []
    try:
        t = open(HONESTY, encoding="utf-8").read()
        out.append(("honesty_615 含 median=67.5", "67.5" in t, ""))
        out.append(("honesty_615 不再写 median=75", not re.search(r"47/80/75", t),
                    "仍存在 '47/80/75' 旧值"))
    except OSError as exc:
        out.append(("honesty_615 可读", False, str(exc)))
    try:
        t = open(L624, encoding="utf-8").read()
        out.append(("624 清单含唯一性说明(93)", "93" in t, ""))
        out.append(("624 清单含 overlap 说明(17)", "17" in t, ""))
    except OSError as exc:
        out.append(("624 清单可读", False, str(exc)))
    try:
        t = open(EXPIRY, encoding="utf-8").read()
        ok = ("31" in t) and ("27" in t)
        out.append(("豁免到期制区分 27 legacy + 31 total", ok, ""))
    except OSError as exc:
        out.append(("豁免到期制可读", False, str(exc)))
    return out


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    got = recompute()
    for k, want in EXPECTED.items():
        g = got[k]
        chk(f"重算 {k} = {want}", g == want, f"(实测 {g})")
    for name, cond, note in check_docs():
        chk(name, cond, note if not cond else "")
    print(f"A1 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 A1 统计重算校验器（只读）")
    ap.add_argument("--check", action="store_true", help="重算并校验与文档一致")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出重算结果")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    got = recompute()
    if args.json:
        print(json.dumps(got, ensure_ascii=False, indent=2))
    else:
        for k, v in got.items():
            print(f"{k:24s} = {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
