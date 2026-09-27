#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""embedded_adapter_652.py — M5 嵌入式 C 适配包（652 C，**裸金属约束层**）。

为什么（652 C-M5）：C++ 域的 Domain Pack 假设有完整运行时；嵌入式（裸金属）没有堆/异常/RTTI/
线程，且"**能编译 ≠ 对**"。M5 给出一层**嵌入式约束检查**（对源码扫禁用构造），把"嵌入式域"
的规则显式化。

诚实登记（652 要求）：
- LLM 生成嵌入式代码的 pass@1 ≈ **55.6%** ⇒ 约 44% 不可用，**必须**机器验证（编译+约束+真机），
  不得直接采用；
- 本适配包是**静态约束层**；**交叉编译 / 真机在环（HIL）本环境不可得** ⇒ 登记为 gap；
- 「能编译≠对」：编译通过只说明语法/类型；语义与外设行为需真机（本环境做不到）。

用法
====
    python tools/embedded_adapter_652.py --check
    python tools/embedded_adapter_652.py --scan            # 扫 648 C fixtures → data/652_m5_embedded.json/md
    python tools/embedded_adapter_652.py --scan-file PATH
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "embedded_adapter_652", "entry": "scan_file",
                "description": "M5 嵌入式 C 适配包（裸金属约束静态检查 + 诚实 55.6% LLM 限制）"}

OUT_JSON = ROOT / "data" / "652_m5_embedded.json"
OUT_MD = ROOT / "data" / "652_m5_embedded.md"
LLM_EMBEDDED_PASS_AT_1 = 0.556  # 诚实登记：LLM 嵌入式 pass@1
FIXTURE_GLOB = "Examples/atoms/_c_*.c"

# 裸金属禁用/受限构造（静态规则）
RULES: list[tuple[str, str, str]] = [
    ("no_heap", r"\b(malloc|calloc|realloc|free)\s*\(", "裸金属禁用动态堆分配（用静态/池）"),
    ("no_exceptions", r"\b(try|catch|throw)\b", "禁用 C++ 异常（无 unwinder）"),
    ("no_rtti", r"\b(dynamic_cast|typeid)\b", "禁用 RTTI（体积/行为不可预测）"),
    ("no_threads", r"<thread>|\bstd::thread\b|pthread_create", "无 OS 线程；用中断/DMA/状态机"),
    ("no_heavy_printf", r"\bprintf\s*\(", "printf 体积大且非可重入，建议裸金属禁用或改写"),
    ("no_new", r"\bnew\s+[A-Za-z_]", "裸金属禁用 new（无堆）"),
    ("isr_hint", r"__attribute__\s*\(\s*\(\s*interrupt", "ISR：注意浮点/长耗时不安全（需人核）"),
]


@dataclass
class Violation:
    rule: str
    line: int
    text: str
    message: str


def scan_text(text: str) -> list[Violation]:
    out: list[Violation] = []
    for i, ln in enumerate(text.splitlines(), 1):
        for name, pat, msg in RULES:
            if re.search(pat, ln):
                out.append(Violation(name, i, ln.strip()[:80], msg))
    return out


def scan_file(path: Path) -> dict:
    if not path.is_file():
        return {"file": str(path), "error": "not_found", "violations": []}
    vio = scan_text(path.read_text(encoding="utf-8", errors="replace"))
    return {"file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            "violations": [asdict(v) for v in vio], "count": len(vio)}


def scan_all() -> dict:
    files = sorted(ROOT.glob(FIXTURE_GLOB))
    rows = [scan_file(p) for p in files]
    total = sum(r.get("count", 0) for r in rows)
    return {"fixtures": len(rows), "total_violations": total,
            "llm_embedded_pass_at_1": LLM_EMBEDDED_PASS_AT_1,
            "honest_note": "能编译≠对；交叉编译/真机(HIL)本环境不可得（gap）；LLM 嵌入式 pass@1≈55.6% 必须机器验证。",
            "rows": rows}


def _write(rep: dict) -> None:
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 M5 · 嵌入式 C 适配包（裸金属约束静态检查）\n",
             f"- fixtures {rep['fixtures']}｜违规 {rep['total_violations']}"
             f"｜LLM 嵌入式 pass@1 诚实登记 = **{rep['llm_embedded_pass_at_1']}**\n",
             f"> {rep['honest_note']}\n",
             "| 文件 | 违规数 | 规则 |", "|---|---|---|"]
    for r in rep["rows"]:
        rs = ",".join(sorted({v["rule"] for v in r.get("violations", [])})) or "-"
        lines.append(f"| {r['file']} | {r.get('count', 0)} | {rs} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("检出 malloc", any(v.rule == "no_heap" for v in scan_text("p = malloc(4);")))
    chk("检出线程", any(v.rule == "no_threads" for v in scan_text("#include <thread>")))
    chk("干净代码 0 违规", not scan_text("int x = 1;\nreturn x;"))
    chk("行号正确", scan_text("a\nb = malloc(1);")[0].line == 2)
    chk("55.6% 已登记", LLM_EMBEDDED_PASS_AT_1 == 0.556)
    print(f"embedded_adapter_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="652 M5 嵌入式 C 适配包")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--scan-file", default=None)
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    if a.scan_file:
        r = scan_file(ROOT / a.scan_file)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        raise SystemExit(0)
    rep = scan_all()
    _write(rep)
    print(f"fixtures {rep['fixtures']}｜违规 {rep['total_violations']}｜→ {OUT_MD.name}")
    raise SystemExit(0)
