#!/usr/bin/env python3
"""原子知识地图：域归属统计 + 覆盖率门禁（G1.1 的可复算产物）。

把 147 章按知识域（domain）归类并统计真实指标，供「最薄弱优先」排序使用：

    python tools/atom_coverage_map.py                 # 打印域统计与逐章映射
    python tools/atom_coverage_map.py --check         # 覆盖率门禁：存在未映射章即 exit 1
    python tools/atom_coverage_map.py --json out.json # 落机器可读结果

判定口径（与 docs/kernel/G1_knowledge_map.md 一致）：
  * 域 ≠ part 目录：域是知识视图，part 是出版视图；3 处重归类见文档第 2 节。
  * 覆盖率 = 已映射章数 / 全部章数，要求 100%（未映射即 exit 1）。

不修改任何文件，只读。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from comment_blocks import iter_md_files, parse, is_pure_comment  # noqa: E402

ROOT = HERE.parent


def _book() -> Path:
    return ROOT / "Book"


# 域映射：章前缀 -> 域。特例（与 part 目录不一致者）在文档第 2 节写了理由。
DOMAIN_OF_PREFIX: dict[str, str] = {
    "ch01": "HIST", "ch02": "HIST", "ch03": "HIST", "ch04": "HIST", "ch05": "HIST",
    "ch06": "HIST", "ch07": "HIST", "ch08": "HIST", "ch09": "HIST", "ch10": "HIST",
    "ch11": "TOOL", "ch12": "TOOL", "ch13": "TOOL", "ch14": "TOOL", "ch15": "TOOL",
    "ch16": "TOOL", "ch17": "TOOL", "ch18": "TOOL",
    "ch19": "LANG", "ch20": "LANG", "ch21": "LANG", "ch22": "LANG", "ch23": "LANG",
    "ch24": "LANG", "ch25": "LANG", "ch26": "LANG", "ch27": "LANG",
    "ch29": "LANG", "ch31": "LANG", "ch32": "LANG",
    "ch28": "UB", "ch30": "UB", "ch42": "UB",
    "ch35": "MEM", "ch36": "MEM", "ch37": "MEM", "ch38": "MEM", "ch39": "MEM",
    "ch40": "MEM", "ch41": "MEM", "ch43": "MEM", "ch44": "MEM",
    "ch45": "MEM", "ch46": "MEM", "ch47": "MEM", "ch48": "MEM", "ch49": "MEM",
    "ch50": "MEM", "ch51": "MEM", "ch52": "MEM",
    "ch115": "MEM", "ch116": "MEM", "ch117": "MEM",
    "ch60": "TMPL", "ch61": "TMPL", "ch62": "TMPL", "ch63": "TMPL", "ch64": "TMPL",
    "ch65": "TMPL", "ch66": "TMPL", "ch67": "TMPL", "ch68": "TMPL", "ch69": "TMPL",
    "ch70": "TMPL", "ch71": "TMPL", "ch72": "TMPL",
    "ch76": "STL", "ch77": "STL", "ch78": "STL", "ch79": "STL", "ch80": "STL",
    "ch81": "STL", "ch82": "STL", "ch83": "STL", "ch84": "STL", "ch85": "STL",
    "ch86": "STL", "ch87": "STL", "ch88": "STL", "ch89": "STL", "ch90": "STL",
    "ch91": "STL", "ch92": "STL",
    "ch93": "CONC", "ch94": "CONC",
    "ch107": "CONC", "ch108": "CONC", "ch109": "CONC", "ch110": "CONC",
    "ch111": "CONC", "ch112": "CONC", "ch113": "CONC",
    "ch95": "ALGO", "ch96": "ALGO", "ch97": "ALGO", "ch98": "ALGO", "ch99": "ALGO",
    "ch100": "ALGO", "ch101": "ALGO",
    "ch118": "MOD", "ch119": "MOD", "ch120": "MOD", "ch121": "MOD", "ch122": "MOD",
    "ch123": "MOD",
    "ch124": "ABI", "ch125": "ABI", "ch126": "ABI", "ch127": "ABI", "ch128": "ABI",
    "ch129": "ABI", "ch130": "ABI", "ch131": "ABI", "ch132": "ABI", "ch133": "ABI",
    "ch134": "ABI",
    "ch135": "PAT", "ch136": "PAT", "ch137": "PAT", "ch138": "PAT", "ch139": "PAT",
    "ch140": "PAT", "ch141": "PAT", "ch142": "PAT", "ch143": "PAT",
    "ch144": "ENG", "ch145": "ENG", "ch146": "ENG", "ch147": "ENG", "ch148": "ENG",
    "ch149": "ENG", "ch150": "ENG", "ch151": "ENG",
    "ch152": "PERF", "ch153": "PERF", "ch154": "PERF", "ch155": "PERF",
    "ch156": "PERF", "ch157": "PERF", "ch158": "PERF",
    "ch159": "CASE", "ch160": "CASE", "ch161": "CASE", "ch162": "CASE",
    "ch163": "CASE", "ch164": "CASE",
    "ch165": "READ",
}


def scan() -> tuple[list[dict], list[str]]:
    """返回 (每章记录, 未映射章列表)。"""
    rows: list[dict] = []
    unmapped: list[str] = []
    for p in iter_md_files(_book()):
        rel = p.relative_to(_book()).as_posix()
        key = p.stem.split("_")[0]
        dom = DOMAIN_OF_PREFIX.get(key)
        if dom is None:
            unmapped.append(rel)
            continue
        text = p.read_bytes().decode("utf-8")
        blocks = parse(p)
        rows.append({
            "chapter": rel,
            "domain": dom,
            "cpp_blocks": len(blocks),
            "with_main": sum(1 for b in blocks if "int main" in "\n".join(b.body)),
            "pure_comment": sum(1 for b in blocks if is_pure_comment(b.body)),
            "verified": len(re.findall(r"\[VERIFIED\]", text)),
            "unverified": len(re.findall(r"\[UNVERIFIED\]", text)),
        })
    return rows, unmapped


def _agg(rows: Sequence[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        s = out.setdefault(r["domain"], {"chapters": 0, "cpp_blocks": 0, "with_main": 0,
                                         "pure_comment": 0, "verified": 0, "unverified": 0})
        for k in ("chapters", "cpp_blocks", "with_main", "pure_comment",
                  "verified", "unverified"):
            s[k] += (1 if k == "chapters" else r[k])
    for s in out.values():
        s["unverified_density"] = round(s["unverified"] / max(1, s["cpp_blocks"]), 4)
    return out


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="原子知识地图：域统计与覆盖率门禁")
    ap.add_argument("--check", action="store_true", help="存在未映射章即 exit 1")
    ap.add_argument("--json", dest="json_path")
    a = ap.parse_args(argv)

    rows, unmapped = scan()
    agg = _agg(rows)
    total = len(rows) + len(unmapped)
    covered = len(rows)
    rate = covered / max(1, total)

    print(f"[coverage-map] 覆盖率 {covered}/{total} = {rate:.1%}；未映射 {len(unmapped)}")
    if unmapped:
        for u in unmapped[:20]:
            print(f"  UNMAPPED {u}")
    print()
    print("| 域 | 章数 | cpp块 | 含main | 纯注释 | VERIFIED | UNVERIFIED | 缺口密度 |")
    print("|---|---|---|---|---|---|---|---|")
    for dom in sorted(agg, key=lambda d: -agg[d]["cpp_blocks"]):
        s = agg[dom]
        print(f"| {dom} | {s['chapters']} | {s['cpp_blocks']} | {s['with_main']} | "
              f"{s['pure_comment']} | {s['verified']} | {s['unverified']} | "
              f"{s['unverified_density']:.1%} |")

    if a.json_path:
        Path(a.json_path).write_text(json.dumps(
            {"coverage": rate, "unmapped": unmapped, "domains": agg, "chapters": rows},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n[coverage-map] JSON → {a.json_path}")

    if a.check and (unmapped or rate < 1.0):
        print("[coverage-map] ✗ 覆盖率未达 100%")
        return 1
    if a.check:
        print("[coverage-map] ✅ 覆盖率 100%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
