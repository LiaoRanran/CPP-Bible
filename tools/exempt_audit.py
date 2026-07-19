#!/usr/bin/env python3
"""编译豁免有效性审计门禁 (exempt audit).

《现代 C++ 终极圣经》的 cpp 块由 `compile_all.py --main-only`
(`g++ -std=c++23 -O0 -fsyntax-only`, 仅编含 `int main` 的块) 验证,
设计性豁免 (多文件/模块/MSVC/POSIX/外部库/故意错误·UB/跨块增量等)
记录在 `tools/compile_exempt.json`, 由 `compile_gate.py` 放行。

`compile_gate` 只比对「当前失败块 vs 豁免清单」, **从不反查豁免是否还成立**.
本工具闭合这个死角: 用与基线完全相同的命令, 逐块重编 65 条豁免,
比对「基线(全部 FAIL) → 当前」是否发生翻转:

  * 仍 FAIL (与预期一致)            -> OK        (豁免仍有效; 若 INTENTIONAL_UB 仍 FAIL 附 INFO 提示标签可能不准)
  * INTENTIONAL_ERROR 变 PASS       -> DRIFT     (正文"会报错"已成谎言, 内容漂移, 阻断)
  * 其余 reason 变 PASS             -> STALE     (豁免失效, 可清理, 门禁可重启用, 默认 WARN)
  * 目标块不存在/越界              -> MISSING   (章节编辑致 block 号漂移, 豁免指向错块, 阻断)
  * POSIX 在 Linux 仍 FAIL 等       -> UNEXPECTED_FAIL (平台异常, WARN)

平台感知: POSIX 块在 Linux 预期 PASS (有 <sys/mman.h>), 在 Windows 预期 FAIL
(MinGW 无 POSIX 头). 基线审计于 mingw/Windows (gcc-15.3.0), 故 POSIX 在基线 FAIL;
在 Linux CI 上 PASS 属正常, 不误报. INTENTIONAL_UB 两平台均预期 PASS (UB 是运行时).

设计: 零外部依赖纯 Python; `--check` 非零退出 (仅 DRIFT / MISSING 必失败,
STALE / UB_FAIL 默认 WARN, `--strict-stale` 升级 STALE 为失败); JSON 报告.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, "..", "Book"))
DEFAULT_EXEMPT = os.path.join(HERE, "compile_exempt.json")
DEFAULT_REPORT = os.path.join(HERE, "exempt_audit_report.json")
FLAGS = "-std=c++23 -O0 -fsyntax-only"

# 默认所有豁免块预期 FAIL (compile_gate 仅放行失败块).
# 唯一例外: POSIX 在 Linux 有 <sys/mman.h> 等头, 预期 PASS (平台差异, 非腐坏).


def detect_platform() -> str:
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform.startswith("win"):
        return "windows"
    return sys.platform


def gcc_version(gcc: str) -> str:
    try:
        out = subprocess.run([gcc, "--version"], capture_output=True,
                              text=True, timeout=10)
        m = re.search(r"(\d+\.\d+\.\d+)", out.stdout)
        return m.group(1) if m else out.stdout.splitlines()[0][:40]
    except Exception:
        return "unknown"


def find_files(root: str) -> dict[str, str]:
    """basename -> absolute path (recursive)."""
    out = {}
    for r, _d, files in os.walk(root):
        if "_legacy" in r:
            continue
        for f in files:
            if f.endswith(".md"):
                out.setdefault(f, os.path.join(r, f))
    return out


def extract_cpp_blocks(text: str) -> list[str]:
    """Replicate compile_all.extract_blocks: ```cpp ... ``` (closing ```)."""
    blocks, cur, in_block = [], [], False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("```cpp"):
            in_block, cur = True, []
        elif s == "```" and in_block:
            in_block = False
            blocks.append("\n".join(cur))
        elif in_block:
            cur.append(line)
    return blocks


def compile_block(gcc: str, block: str) -> tuple[bool, str]:
    """Return (passed, error_snippet)."""
    if not block.strip():
        return True, "(empty block)"
    with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w",
                                     delete=False, encoding="utf-8") as f:
        f.write(block)
        fpath = f.name
    try:
        res = subprocess.run([gcc] + FLAGS.split() + [fpath],
                             capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            msg = ""
            for e in res.stderr.strip().split("\n"):
                if "error:" in e:
                    msg = e.split("error:")[-1].strip()[:160]
                    break
            if not msg:
                msg = (res.stderr.strip().split("\n")[0] or "unknown")[:160]
            return False, msg
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT(>15s)"
    finally:
        try:
            os.unlink(fpath)
        except OSError:
            pass


def expected_fail(reason: str, platform: str) -> bool:
    """compile_gate 假设豁免块均 FAIL (仅放行失败块).

    POSIX 块在 Linux 有 <sys/mman.h> 等 POSIX 头, 预期 PASS — 这是平台差异,
    不是腐坏, 故在 Linux 上不视其 PASS 为翻转. 其余 reason 两平台均预期 FAIL.
    """
    if reason == "POSIX" and platform == "linux":
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="编译豁免有效性审计")
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--exempt", default=DEFAULT_EXEMPT)
    ap.add_argument("--gcc", default=None,
                    help="g++ 路径 (默认: mingw1530 若存在, 否则 PATH g++)")
    ap.add_argument("--json", default=DEFAULT_REPORT)
    ap.add_argument("--check", action="store_true",
                    help="非零退出 (DRIFT/MISSING 必失败; --strict-stale 升级 STALE)")
    ap.add_argument("--strict-stale", action="store_true")
    args = ap.parse_args()

    gcc = args.gcc
    if not gcc:
        mingw = r"C:/Qt/Tools/mingw1530_64/bin/g++.EXE"
        gcc = mingw if os.path.exists(mingw) else (shutil_which())
    gcc = os.path.normpath(gcc)
    platform = detect_platform()

    exempt_data = json.load(open(args.exempt, encoding="utf-8"))
    entries = exempt_data.get("exempt", [])
    files = find_files(args.root)

    results = []
    for e in entries:
        f, blk, reason = e["file"], e["block"], e["reason"]
        rec = {"file": f, "block": blk, "reason": reason,
               "note": e.get("note", ""), "status": None,
               "passed": None, "error": "", "has_main": None}
        path = files.get(f)
        if not path:
            rec["status"] = "MISSING_FILE"
            results.append(rec)
            continue
        blocks = extract_cpp_blocks(open(path, encoding="utf-8").read())
        if blk < 1 or blk > len(blocks):
            rec["status"] = "MISSING_BLOCK"
            rec["error"] = f"章节仅 {len(blocks)} 个 cpp 块, 豁免指向 #{blk}"
            results.append(rec)
            continue
        block = blocks[blk - 1]
        rec["has_main"] = ("int main" in block)
        passed, err = compile_block(gcc, block)
        rec["passed"] = passed
        rec["error"] = err
        exp_fail = expected_fail(reason, platform)
        flipped = (passed != (not exp_fail))  # 实际与预期相反 => 翻转
        if not flipped:
            rec["status"] = "OK"
            # INTENTIONAL_UB 但实为编译期硬错 (ill-formed), 非运行时 UB:
            # 标签可能不准确 (在书声明的 C++23 下应为 INTENTIONAL_ERROR).
            if reason == "INTENTIONAL_UB" and not passed:
                rec["info"] = ("INTENTIONAL_UB 块实际为编译期硬错误(ill-formed), "
                               "非运行时 UB; 标签可能不准确, 建议复核正文")
        else:
            # 发生翻转
            if reason == "INTENTIONAL_ERROR" and passed:
                rec["status"] = "DRIFT"
            elif passed:
                rec["status"] = "STALE"
            else:
                rec["status"] = "UNEXPECTED_FAIL"
        results.append(rec)

    # 汇总
    by_status: dict[str, int] = {}
    for r in results:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1

    report = {
        "gcc": gcc,
        "gcc_version": gcc_version(gcc),
        "platform": platform,
        "flags": FLAGS,
        "baseline": exempt_data.get("audited_against", "?"),
        "total": len(results),
        "by_status": by_status,
        "results": results,
    }
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # 输出
    print("=" * 70)
    print(f"编译豁免审计  gcc={report['gcc_version']}  platform={platform}  "
          f"flags='{FLAGS}'")
    print(f"  豁免总数 : {len(results)}")
    for st in ["OK", "STALE", "DRIFT", "MISSING_FILE", "MISSING_BLOCK",
               "UNEXPECTED_FAIL"]:
        if by_status.get(st):
            print(f"  {st:14}: {by_status[st]}")
    print("-" * 70)
    for r in results:
        if r["status"] in ("OK",):
            if r.get("info"):
                print(f"  [INFO        ] {r['reason']:14} {r['file']}#blk"
                      f"{r['block']} :: {r['info'][:80]}")
            continue
        tag = r["status"]
        extra = f" :: {r['error'][:90]}" if r["error"] else ""
        print(f"  [{tag:13}] {r['reason']:14} {r['file']}#blk{r['block']}{extra}")
    print("=" * 70)

    fail = by_status.get("DRIFT", 0) + by_status.get("MISSING_FILE", 0) \
        + by_status.get("MISSING_BLOCK", 0)
    stale = by_status.get("STALE", 0)
    if fail:
        print(f"[audit] FAIL: {fail} 个阻断性问题 (DRIFT/MISSING).")
        return 1
    if stale and args.strict_stale:
        print(f"[audit] FAIL: {stale} 个 STALE 豁免 (--strict-stale).")
        return 1
    if stale or by_status.get("UB_FAIL") or by_status.get("UNEXPECTED_FAIL"):
        print(f"[audit] WARN: 存在 STALE/UB_FAIL/UNEXPECTED_FAIL, 建议复核 "
              f"(非阻断).")
        return 0
    print("[audit] PASS: 全部豁免仍有效, 无内容漂移.")
    return 0


def shutil_which() -> str:
    import shutil
    return shutil.which("g++") or "g++"


if __name__ == "__main__":
    sys.exit(main())
