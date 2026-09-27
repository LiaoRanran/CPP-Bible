#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_assembler_652.py — H5 探针积木化（652 B，**离线造块 + 在线零 LLM 组装 + 差分矩阵**）。

为什么（652 B-H5）：每张新卡都要人写探针，成本高。H5 的思路：**特性积木**（小 C 片段）离线造好，
在线只做**零成本组合**（拼成单个翻译单元 → 编译 → 跑 → 记录），并自动产出 **L1 差分矩阵**
（gcc/clang × O0/O2 × sanitizer），矩阵本身就是可复核的证据。

诚实边界（652 要求"不假装"）：
- 「LLM 离线造积木」在本环境**无 LLM** ⇒ 积木来自**预置库**（人工/离线产物），工具做**组合与矩阵**；
  真正的 LLM 造块留交人/后续（登记于 652_gaps）。
- sanitizer 可用性**实测**：MinGW gcc 常不支持 `-fsanitize=undefined` ⇒ 工具如实记
  `sanitizer_unsupported`，**不伪造**"sanitizer 通过"。

用法
====
    python tools/probe_assembler_652.py --check
    python tools/probe_assembler_652.py --build          # 生成 data/652_h5_probe.c + 差分矩阵
    python tools/probe_assembler_652.py --matrix-public  # 看矩阵（json）
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "probe_assembler_652", "entry": "build",
                "description": "H5 探针积木：离线块 + 在线零 LLM 组装 + 编译/sanitizer 差分矩阵"}

C_OUT = ROOT / "data" / "652_h5_probe.c"
M_JSON = ROOT / "data" / "652_h5_matrix.json"
M_MD = ROOT / "data" / "652_h5_matrix.md"
BUILD = ROOT / "build" / "c652"

# ── 积木库（离线造好；每块打印 "块名.键=值"）──────────────────────────────────
BLOCKS: dict[str, str] = {
    "shift": r"""
static void blk_shift(void) {
    unsigned u = 1u; int neg = -1; int r;
    r = (int)(u << 31);                 /* 有符号解释实现定义 */
    printf("shift.u31=%d\n", r);
    printf("shift.neg_shift=%d\n", (neg << 1) == -2 ? 1 : 0);  /* 左移负数是 UB */
}
""",
    "bitfield": r"""
struct bf_t { unsigned a:3; unsigned b:5; signed c:2; };
static void blk_bitfield(void) {
    struct bf_t v; v.a=5; v.b=21; v.c=-1;
    printf("bitfield.size=%d\n", (int)sizeof(struct bf_t));
    printf("bitfield.a=%d\n", (int)v.a);
    printf("bitfield.c=%d\n", (int)v.c);
}
""",
    "alignof_": r"""
struct al_t { char c; double d; };
static void blk_alignof_(void) {
    printf("alignof_.size=%d\n", (int)sizeof(struct al_t));
    printf("alignof_.ptr=%d\n", (int)sizeof(void*));
}
""",
    "volatile_": r"""
static void blk_volatile_(void) {
    volatile int sink = 0; int i;
    for (i = 0; i < 3; i++) { sink = i; }
    printf("volatile_.sink=%d\n", (int)sink);
}
""",
    "intpromo": r"""
static void blk_intpromo(void) {
    char a = 100, b = 100;
    printf("intpromo.char_sum=%d\n", (int)(a + b));
    printf("intpromo.cmp=%d\n", (-1 < 1u) ? 1 : 0);
}
""",
    "macro": r"""
#define SQ(x) ((x)*(x))
#define MAX_BAD(a, b) ((a) > (b) ? (a) : (b))
static void blk_macro(void) {
    int i = 1;
    printf("macro.sq_good=%d\n", SQ(i + 3));
    printf("macro.max_bad=%d\n", MAX_BAD(i++, 1));  /* 双求值副作用 */
    printf("macro.i_after=%d\n", i);
}
""",
}


def assemble(blocks: list[str] | None = None) -> str:
    """把选中积木拼成**单个翻译单元**（在线零 LLM 成本：纯文本拼接）。"""
    names = blocks if blocks is not None else list(BLOCKS)
    parts = ["#include <stdio.h>", "#include <limits.h>"]
    for n in names:
        if n not in BLOCKS:
            raise KeyError(f"未知积木 {n}")
        parts.append(BLOCKS[n])
    parts.append("int main(void){")
    for n in names:
        parts.append(f"    blk_{n}();")
    parts.append("    return 0;")
    parts.append("}")
    return "\n".join(parts) + "\n"


def _parse_kv(stdout: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for ln in stdout.splitlines():
        if "=" in ln:
            k, _, v = ln.strip().partition("=")
            try:
                out[k] = int(v)
            except ValueError:
                continue
    return out


def run_case(src: Path, cc: str, std: str, opt: str, sanitizer: str | None) -> dict:
    BUILD.mkdir(parents=True, exist_ok=True)
    exe = BUILD / f"h5_{cc}_{std}_{opt}{'_san' if sanitizer else ''}.exe"
    cmd = [cc, f"-std={std}", opt, "-Wall", "-Wextra"]
    if sanitizer:
        cmd.append(f"-fsanitize={sanitizer}")
    cmd += [str(src), "-o", str(exe)]
    res: dict = {"cc": cc, "std": std, "opt": opt, "sanitizer": sanitizer or "none"}
    try:
        cp = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=120, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        res.update(compile_rc=-1, status="compiler_unavailable", err=str(e)[:120])
        return res
    res["compile_rc"] = cp.returncode
    if cp.returncode != 0:
        low = (cp.stderr or "").lower()
        if sanitizer and ("cannot find -l" in low or "undefined reference to `__ubsan" in low):
            res["status"] = "sanitizer_runtime_missing"   # 库没装（不是代码错）
        elif sanitizer and ("unrecognized" in low or "not supported" in low):
            res["status"] = "sanitizer_unsupported"       # 编译器不认这个 flag
        else:
            res["status"] = "compile_error"
        res["err"] = (cp.stderr or "")[-200:]
        return res
    try:
        rp = subprocess.run([str(exe)], cwd=str(ROOT), capture_output=True, text=True, timeout=60, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        res.update(run_rc=-1, status="run_failed", err=str(e)[:120])
        return res
    res["run_rc"] = rp.returncode
    res["kv"] = _parse_kv(rp.stdout)
    # sanitizer 命中通常以非 0 退出并在 stderr 报 runtime error
    tripped = bool(rp.returncode != 0 or "runtime error" in (rp.stderr or "").lower())
    res["sanitizer_tripped"] = tripped if sanitizer else None
    res["status"] = "sanitizer_tripped" if (sanitizer and tripped) else "ok"
    return res


def build() -> dict:
    src = assemble()
    C_OUT.parent.mkdir(parents=True, exist_ok=True)
    C_OUT.write_text(src, encoding="utf-8")
    matrix = []
    for cc in ("gcc", "clang"):
        for opt in ("-O0", "-O2"):
            for san in (None, "undefined"):
                matrix.append(run_case(C_OUT, cc, "c11", opt, san))
    ok = sum(1 for r in matrix if r["status"] == "ok")
    rep = {"source": str(C_OUT.relative_to(ROOT)), "blocks": list(BLOCKS), "cases": len(matrix),
           "ok": ok, "matrix": matrix}
    M_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 H5 · 探针积木差分矩阵（L1 证据）\n",
             f"- 积木 {len(BLOCKS)} 个｜用例 {len(matrix)}｜ok {ok}\n",
             "| cc | std | opt | sanitizer | compile_rc | run_rc | sanitizer_tripped | status | 来源 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in matrix:
        lines.append(f"| {r['cc']} | {r['std']} | {r['opt']} | {r['sanitizer']} | {r.get('compile_rc')} | "
                     f"{r.get('run_rc', '')} | {r.get('sanitizer_tripped', '')} | {r['status']} | 真机 |")
    M_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rep


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    src = assemble()
    chk("组装含 main", "int main(void){" in src)
    chk("组装含全部积木函数", all(f"blk_{n}()" in src for n in BLOCKS))
    try:
        assemble(["nope"])
        chk("未知积木抛错", False)
    except KeyError:
        chk("未知积木抛错", True)
    chk("kv 解析", _parse_kv("a.b=3\nc= -2\n")== {"a.b": 3, "c": -2})
    chk("kv 忽略噪声", _parse_kv("# x\nshift.u31=1\n") == {"shift.u31": 1})
    print(f"probe_assembler_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="652 H5 探针积木化（离线块 + 在线组装 + 差分矩阵）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--matrix-public", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rep = build()
    if a.matrix_public:
        print(json.dumps(rep["matrix"], ensure_ascii=False, indent=2))
        return 0
    print(f"积木 {len(rep['blocks'])}｜用例 {rep['cases']}｜ok {rep['ok']}｜→ {M_MD.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
