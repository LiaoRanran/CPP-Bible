#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_asm_evidence.py — 汇编证据「符号真实性」守卫

《现代 C++ 终极圣经》的汇编/符号证据节承诺其 asm 块来自真实 GCC 编译产物
（Examples/*.asm）。本工具机器校验：
  书内 asm 块引用的 mangled 符号集合 是否 ⊆ 真实 Examples/*.asm 的符号集合。

- 书内符号全部能在真实产物中找到  → ACCURATE（书为节选/缩写，符合预期）
- 书内有真实产物里没有的符号      → DRIFT（书捏造/笔误，HIGH，必须修）
- 书内块无 mangled 符号           → EMPTY（纯注释节选，LOW，仅记录）
- 引用文件在磁盘缺失              → MISSING_FILE（证据丢失，仅计数告警）
- 未引用具体文件                  → UNANCHORED（无法机校，仅计数）

校验是「符号级」的：Itanium mangled 名在不同 GCC 次版本间稳定，
故本工具对证据库的 GCC 版本不敏感。证据库 Examples/*.asm 目前为
13.1.0 与 15.3.0 混合（以 13.1.0 为主，少量 15.3.0），版本一致性由
独立审计负责，不在本工具范围。

只读取 Book/ 与 Examples/，只写 build/。不修改源文件。
退出码：存在 DRIFT → 1（CI 应阻断）；否则 → 0。

CI 用法：python3 tools/verify_asm_evidence.py --root Book --examples Examples
"""
import re, json, pathlib, sys, argparse

# Itanium mangled name: _Z 开头，后接编码字符；放宽以覆盖 _ZN/_ZSt/_ZTV 等
MANGLE = re.compile(r"_Z[0-9A-Za-z_]{3,}")
# 标准库符号（libstdc++ 等）不会出现在用户 .asm 中，属预期，不判 DRIFT
LIB_RE = re.compile(r"_Z(?:St|NS|NSt)")
ASM_BLOCK = re.compile(r"```asm\n(.*?)```", re.S)
REF_RE = re.compile(r"Examples/([A-Za-z0-9_]+\.asm)")


def syms(text: str):
    return {s for s in MANGLE.findall(text) if not LIB_RE.match(s)}


def find_ref(block: str, before: str):
    m = REF_RE.search(block)
    if m:
        return m.group(1)
    # 仅当块前 200 字符内有「节选自 Examples/X.asm」时才关联，
    # 避免与邻近其它块误关联（如 c++filt 通用示意块）
    m = REF_RE.search(before[-200:])
    if m:
        return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser(description="汇编证据符号真实性守卫")
    ap.add_argument("--root", default="Book", help="Book 根目录（含 *.md）")
    ap.add_argument("--examples", default="Examples", help="真实 .asm 工件目录")
    ap.add_argument("--out", default="build/asm_evidence_report.json",
                    help="JSON 报告输出路径")
    args = ap.parse_args()

    ROOT = pathlib.Path(args.root)
    EX = pathlib.Path(args.examples)
    OUT = pathlib.Path(args.out)

    # Windows 控制台（GBK）无法编码 emoji/中文，重导向为 utf-8 容错，避免本地验证崩溃
    # （CI 为 UTF-8 本就无碍；errors='replace' 保证任何环境都能跑完并 exit 0/1）
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    records = []
    summary = {"accurate": 0, "drift": 0, "empty": 0, "unanchored": 0,
               "missing_file": 0, "chapters": 0, "blocks": 0}
    for f in sorted(ROOT.rglob("*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        # 逐块定位，并取块前 500 字符用于找引用
        for m in ASM_BLOCK.finditer(t):
            block = m.group(1)
            before = t[max(0, m.start() - 500):m.start()]
            ref = find_ref(block, before)
            book_syms = syms(block)
            rec = {"chapter": str(f), "ref": ref, "book_syms": sorted(book_syms)}
            if ref is None:
                rec["status"] = "UNANCHORED"
                summary["unanchored"] += 1
            else:
                real = (EX / ref)
                if not real.exists():
                    rec["status"] = "MISSING_FILE"
                    summary["missing_file"] += 1
                else:
                    real_syms = syms(real.read_text(encoding="utf-8", errors="ignore"))
                    rec["real_syms"] = sorted(real_syms)
                    # 书内符号若「等于或作为某真实符号的前缀」→ 合法缩写（节选）
                    real_list = list(real_syms)
                    extra = set()
                    for b in book_syms:
                        if not any(b == r or r.startswith(b) for r in real_list):
                            extra.add(b)
                    if extra:
                        rec["status"] = "DRIFT"
                        rec["extra_in_book"] = sorted(extra)
                        summary["drift"] += 1
                    elif not book_syms:
                        rec["status"] = "EMPTY"
                        summary["empty"] += 1
                    else:
                        rec["status"] = "ACCURATE"
                        summary["accurate"] += 1
            records.append(rec)
            summary["blocks"] += 1
        summary["chapters"] = len({r["chapter"] for r in records})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "records": records},
                              ensure_ascii=False, indent=2), encoding="utf-8")

    s = summary
    print(f"扫描章数: {s['chapters']}   asm 块: {s['blocks']}")
    print(f"  ✅ ACCURATE (书⊆真实): {s['accurate']}")
    print(f"  ⚠️  DRIFT (书有捏造符号): {s['drift']}")
    print(f"  🟡 EMPTY (书块无符号):  {s['empty']}")
    print(f"  🔴 MISSING_FILE (引用文件缺失): {s['missing_file']}")
    print(f"  ⚪ UNANCHORED (未引用文件): {s['unanchored']}")
    print(f"\n明细 → {OUT}")
    # 列出所有 DRIFT
    drifts = [r for r in records if r["status"] == "DRIFT"]
    if drifts:
        print("\n=== DRIFT 详情（必须修复）===")
        for r in drifts:
            ch = r["chapter"].split("/")[-1]
            print(f"  {ch}  引用 {r['ref']}")
            print(f"    书内多余符号: {r['extra_in_book']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
