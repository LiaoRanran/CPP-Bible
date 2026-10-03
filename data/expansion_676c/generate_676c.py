#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""generate_676c.py — 676c 扩样-A 候选样本生成器（数据标注 Agent 自用）。

产物：data/expansion_676c/sample_NNN.cpp + sample_NNN.json
缺陷类别（扩样-A）：UB / 内存安全 / 未初始化 / 空指针 / 越界
缺陷类型受控词表：undefined_behavior / memory_safety / uninitialized_read /
                  null_pointer_deref / out_of_bounds

设计约束（红线）：
- 每个样本是独立 .cpp，不修改任何已有文件。
- 缺陷行内嵌 `<<PLANTED-DEFECT>>` 哨兵注释，用于精确计算 defect_location 行号。
- planted 全部为 true（LLM 生成即人为植入，如实标注，不伪称自然缺陷）。
- 多样性：每类 >=8，且含变体（上下文/触发条件不同）；uninitialized_read 作为
  检测器盲区（无本地可用检测器可抓），天然构成"边界案例"（~20%）。

检测器主资产映射（Task C 用 detect() 真实跑）：
  memory_safety / out_of_bounds / null_pointer_deref -> asan (WSL)
  undefined_behavior                            -> ubsan (WSL)
  uninitialized_read                            -> compiler-warn (本机)
"""
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)  # data/ -> repo root
OUT = HERE
os.makedirs(OUT, exist_ok=True)

SENT = "<<PLANTED-DEFECT>>"


def prog(includes, body_lines):
    inc = "\n".join(f"#include {h}" for h in includes)
    lines = [
        "// 676c 扩样-A: planted C++ defect candidate (generated sample)",
        "// SPDX-License-Identifier: Apache-2.0",
        inc,
        "int main() {",
    ] + body_lines + ["  return 0;", "}"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 模板构建器：每个返回 (code, defect_type, kind, expected, severity, notes, func)
# ---------------------------------------------------------------------------

def m_uaf(op, idx, use_struct, sev):
    if use_struct:
        body = [
            "  struct Rec { int a; double b; };",
            "  Rec* r = new Rec{1, 2.0};",
            "  delete r;",
            f"  r->a = 7; // {SENT} use-after-free: write through freed struct pointer",
            "  (void)r;",
        ]
        notes = "释放后通过悬空结构指针写内存（UAF）。asan 在运行时捕获。"
    else:
        body = [
            f"  int* p = new int[8];",
            f"  p[{idx}] = 42;",
            "  delete[] p;",
        ]
        if op == "read":
            body += [
                f"  int v = p[{idx}]; // {SENT} use-after-free: read freed heap slot",
                "  (void)v;",
            ]
        else:
            body += [
                f"  p[{idx}] = 99; // {SENT} use-after-free: write freed heap slot",
            ]
        notes = f"释放后访问已 delete 的堆数组第 {idx} 槽（UAF，{op}）。asan 捕获。"
    return prog(["<cstdio>"], body), "memory_safety", "asan", "catch", sev, notes, "main"


def m_double(flavor, sev):
    if flavor == "plain":
        body = [
            "  int* p = new int[4];",
            "  delete[] p;",
            "  delete[] p; // " + SENT + " double-free: same pointer released twice",
        ]
        notes = "同一指针被 delete[] 两次（double-free）。asan 捕获。"
    elif flavor == "branch":
        body = [
            "  int* p = new int[4];",
            "  bool again = true;",
            "  delete[] p;",
            "  if (again) {",
            "    delete[] p; // " + SENT + " double-free inside branch",
            "  }",
        ]
        notes = "条件分支内对同一指针二次释放（double-free）。asan 捕获。"
    else:  # loop
        body = [
            "  int* p = new int[4];",
            "  for (int k = 0; k < 2; ++k) {",
            "    if (k == 0) delete[] p;",
            "    if (k == 1) delete[] p; // " + SENT + " double-free at loop iteration 1",
            "  }",
        ]
        notes = "循环中对同一指针重复释放（double-free）。asan 捕获。"
    return prog(["<cstdio>"], body), "memory_safety", "asan", "catch", sev, notes, "main"


def m_heap_ovf(write_past, size, sev):
    op = "write" if write_past else "read"
    idx = size + 2
    body = [
        f"  int* a = new int[{size}];",
        f"  a[{idx}] = 1; // {SENT} heap buffer overflow: write {idx} past size {size}" if write_past
        else f"  int v = a[{idx}]; // {SENT} heap buffer overflow: read {idx} past size {size}",
        "  (void)v;" if not write_past else "",
        "  delete[] a;",
    ]
    body = [b for b in body if b != ""]
    notes = f"堆数组 size={size}，越界访问下标 {idx}（heap OOB {op}）。asan 捕获。"
    return prog(["<cstdio>"], body), "memory_safety", "asan", "catch", sev, notes, "main"


def m_stack_ovf(write_past, size, sev):
    op = "write" if write_past else "read"
    idx = size + 3
    body = [
        f"  int b[{size}] = {{0}};",
        f"  b[{idx}] = 1; // {SENT} stack buffer overflow: write {idx} past size {size}" if write_past
        else f"  int v = b[{idx}]; // {SENT} stack buffer overflow: read {idx} past size {size}",
        "  (void)v;" if not write_past else "",
    ]
    body = [b for b in body if b != ""]
    notes = f"栈数组 size={size}，越界访问下标 {idx}（stack OOB {op}）。asan 捕获。"
    return prog(["<cstdio>"], body), "memory_safety", "asan", "catch", sev, notes, "main"


def o_heap(kind, size, sev):
    if kind == "read":
        idx = size + 1
        body = [
            f"  int* a = new int[{size}];",
            f"  int v = a[{idx}]; // {SENT} out-of-bounds: read heap index {idx} (size {size})",
            "  (void)v;",
            "  delete[] a;",
        ]
        notes = f"堆数组越界读，下标 {idx} >= size {size}。asan 捕获。"
    elif kind == "write":
        idx = size + 1
        body = [
            f"  int* a = new int[{size}];",
            f"  a[{idx}] = 7; // {SENT} out-of-bounds: write heap index {idx} (size {size})",
            "  delete[] a;",
        ]
        notes = f"堆数组越界写，下标 {idx} >= size {size}。asan 捕获。"
    else:  # memcpy
        n = size + 5
        body = [
            f"  char dst[{size}];",
            f"  char src[{n}] = \"{'a' * (n - 1)}\";",
            f"  __builtin_memcpy(dst, src, {n}); // {SENT} out-of-bounds: memcpy {n} bytes into {size}-byte dst",
        ]
        notes = f"memcpy 写入 {n} 字节到仅 {size} 字节目标（堆/栈溢出）。asan 捕获。"
    return prog(["<cstdio>", "<cstring>"], body), "out_of_bounds", "asan", "catch", sev, notes, "main"


def o_stack(kind, size, sev):
    if kind == "read":
        idx = size + 2
        body = [
            f"  int b[{size}] = {{0}};",
            f"  int v = b[{idx}]; // {SENT} out-of-bounds: read stack index {idx} (size {size})",
            "  (void)v;",
        ]
        notes = f"栈数组越界读，下标 {idx} >= size {size}。asan 捕获。"
    else:  # write via loop off-by-one
        body = [
            f"  int b[{size}] = {{0}};",
            f"  for (int i = 0; i <= {size}; ++i) {{ b[i] = i; }} // {SENT} out-of-bounds: loop writes index {size} (size {size})",
        ]
        notes = f"循环 off-by-one，写入下标 {size}（越界）。asan 捕获。"
    return prog(["<cstdio>"], body), "out_of_bounds", "asan", "catch", sev, notes, "main"


def n_direct(sev):
    body = [
        "  int* p = nullptr;",
        f"  *p = 5; // {SENT} null pointer dereference: write through nullptr",
    ]
    notes = "解引用空指针写入（null pointer dereference）。asan 捕获 SEGV。"
    return prog(["<cstdio>"], body), "null_pointer_deref", "asan", "catch", sev, notes, "main"


def n_funcnull(sev):
    body = [
        "  auto get = []() -> int* { return nullptr; };",
        "  int* p = get();",
        f"  *p = 3; // {SENT} null pointer dereference: deref returned nullptr",
    ]
    notes = "函数返回 nullptr 后解引用写入。asan 捕获。"
    return prog(["<cstdio>"], body), "null_pointer_deref", "asan", "catch", sev, notes, "main"


def n_struct(sev):
    body = [
        "  struct S { int x; int y; };",
        "  S* s = nullptr;",
        f"  s->x = 1; // {SENT} null pointer dereference: member access through null",
    ]
    notes = "通过空结构指针访问成员。asan 捕获。"
    return prog(["<cstdio>"], body), "null_pointer_deref", "asan", "catch", sev, notes, "main"


def n_doubleptr(sev):
    body = [
        "  int** pp = nullptr;",
        f"  (*pp)[0] = 1; // {SENT} null pointer dereference: double deref of null",
    ]
    notes = "二级空指针双重解引用写入。asan 捕获。"
    return prog(["<cstdio>"], body), "null_pointer_deref", "asan", "catch", sev, notes, "main"


def u_arith(varname, sev):
    body = [
        f"  int {varname};",
        f"  int r = {varname} + 7; // {SENT} uninitialized read: arithmetic on uninit var",
        "  (void)r;",
    ]
    notes = (f"变量 {varname} 未初始化即参与运算（uninitialized read）。"
             "无本地检测器可抓（需 MSan），属边界案例。")
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def u_cmp(varname, sev):
    body = [
        f"  int {varname};",
        f"  if ({varname} > 100) {{ (void)1; }} // {SENT} uninitialized read: compare uninit var",
    ]
    notes = (f"未初始化变量 {varname} 直接参与比较（uninitialized read）。"
             "compiler-warn 在 -O0 -fsyntax-only 下通常不报，属边界案例。")
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def u_pass(varname, sev):
    body = [
        "  auto use = [](int v) { (void)v; };",
        f"  int {varname};",
        f"  use({varname}); // {SENT} uninitialized read: pass uninit var to function",
    ]
    notes = (f"未初始化变量 {varname} 作为参数传入函数（uninitialized read）。"
             "无本地检测器可抓，属边界案例。")
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def u_struct(sev):
    body = [
        "  struct P { int a; int b; };",
        "  P p;",
        f"  int r = p.a + p.b; // {SENT} uninitialized read: read uninit struct fields",
        "  (void)r;",
    ]
    notes = "读取未初始化的结构字段（uninitialized read）。无本地检测器可抓，边界案例。"
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def u_bool(sev):
    body = [
        "  bool flag;",
        f"  if (flag) {{ (void)0; }} // {SENT} uninitialized read: branch on uninit bool",
    ]
    notes = "未初始化 bool 控制分支（uninitialized read）。无本地检测器可抓，边界案例。"
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def u_arr(sev):
    body = [
        "  int arr[4];",
        f"  int r = arr[2]; // {SENT} uninitialized read: read uninit array element",
        "  (void)r;",
    ]
    notes = "读取未初始化数组元素（uninitialized read）。无本地检测器可抓，边界案例。"
    return prog(["<cstdio>"], body), "uninitialized_read", "compiler-warn", "miss", sev, notes, "main"


def b_shift(kind, val, sev):
    if kind == "large":
        body = [
            f"  int r = 1 << {val}; // {SENT} undefined behavior: shift exponent {val} too large for 32-bit int",
            "  (void)r;",
        ]
        notes = f"左移指数 {val} 超出 int 位宽（ub：shift exponent too large）。ubsan 捕获。"
    elif kind == "neg":
        body = [
            f"  int r = 1 << ({val}); // {SENT} undefined behavior: negative shift exponent {val}",
            "  (void)r;",
        ]
        notes = f"负左移指数 {val}（ub：negative shift）。ubsan 捕获。"
    else:  # width
        body = [
            "  int x = 1;",
            f"  int r = x << 32; // {SENT} undefined behavior: shift by 32 equals width of int",
            "  (void)r;",
        ]
        notes = "左移量等于 int 位宽 32（ub：shift by width）。ubsan 捕获。"
    return prog(["<cstdio>"], body), "undefined_behavior", "ubsan", "catch", sev, notes, "main"


def b_divzero(sev):
    body = [
        "  int a = 10;",
        f"  int r = a / 0; // {SENT} undefined behavior: integer division by zero",
        "  (void)r;",
    ]
    notes = "整数除以零（ub：division by zero）。ubsan 捕获。"
    return prog(["<cstdio>"], body), "undefined_behavior", "ubsan", "catch", sev, notes, "main"


def b_intmin(sev):
    body = [
        "#include <climits>",
        "  int m = INT_MIN;",
        f"  int r = -m; // {SENT} undefined behavior: negation of INT_MIN not representable",
        "  (void)r;",
    ]
    # prog() injects includes at top; we already added <climits> as a body line, remove duplicate
    notes = "对 INT_MIN 取负（ub：negation overflow）。ubsan 捕获。"
    code = prog(["<cstdio>", "<climits>"], [
        "  int m = INT_MIN;",
        "  int r = -m; // " + SENT + " undefined behavior: negation of INT_MIN not representable",
        "  (void)r;",
    ])
    return code, "undefined_behavior", "ubsan", "catch", sev, notes, "main"


def b_boolinv(sev):
    body = [
        "  bool b = true;",
        "  unsigned char* p = reinterpret_cast<unsigned char*>(&b);",
        "  *p = 2;  // corrupt bool storage",
        f"  bool c = b; // {SENT} undefined behavior: load of invalid bool value (2)",
        "  (void)c;",
    ]
    notes = "内存中 bool 被写成非法值 2 后加载（ub：invalid bool load）。ubsan 捕获。"
    return prog(["<cstdio>"], body), "undefined_behavior", "ubsan", "catch", sev, notes, "main"


# ---------------------------------------------------------------------------
# 组装 100 个样本的计划
# ---------------------------------------------------------------------------
plan = []
# memory_safety (24)
plan += [("m_uaf", dict(op="read", idx=i, use_struct=False, sev="high")) for i in (0, 3, 5, 7)]
plan += [("m_uaf", dict(op="write", idx=i, use_struct=False, sev="high")) for i in (1, 2, 4, 6)]
plan += [("m_uaf", dict(op="read", idx=2, use_struct=True, sev="high"))]
plan += [("m_uaf", dict(op="write", idx=1, use_struct=True, sev="high"))]
plan += [("m_double", dict(flavor=f, sev="high")) for f in ("plain", "branch", "loop") * 2]
plan += [("m_heap_ovf", dict(write_past=True, size=s, sev="high")) for s in (4, 8, 16, 32)]
plan += [("m_heap_ovf", dict(write_past=False, size=s, sev="medium")) for s in (4, 8)]
plan += [("m_stack_ovf", dict(write_past=True, size=s, sev="high")) for s in (4,)]
plan += [("m_stack_ovf", dict(write_past=False, size=s, sev="medium")) for s in (4,)]

# out_of_bounds (20)
plan += [("o_heap", dict(kind="read", size=s, sev="medium")) for s in (4, 8, 16, 32, 64)]
plan += [("o_heap", dict(kind="write", size=s, sev="high")) for s in (4, 8, 16, 32, 64)]
plan += [("o_heap", dict(kind="memcpy", size=s, sev="high")) for s in (4, 8)]
plan += [("o_stack", dict(kind="read", size=s, sev="medium")) for s in (4, 8, 16, 32)]
plan += [("o_stack", dict(kind="write", size=s, sev="high")) for s in (4, 8, 16, 32)]

# null_pointer_deref (15)
plan += [("n_direct", dict(sev="high"))] * 4
plan += [("n_funcnull", dict(sev="high"))] * 4
plan += [("n_struct", dict(sev="high"))] * 4
plan += [("n_doubleptr", dict(sev="high"))] * 3

# uninitialized_read (20)
plan += [("u_arith", dict(varname=n, sev="medium")) for n in ("x", "y", "z", "k")]
plan += [("u_cmp", dict(varname=n, sev="low")) for n in ("a", "b", "c", "d")]
plan += [("u_pass", dict(varname=n, sev="medium")) for n in ("v", "w", "q", "t")]
plan += [("u_struct", dict(sev="medium"))]
plan += [("u_bool", dict(sev="low"))]
plan += [("u_arr", dict(sev="low"))]
plan += [("u_arith", dict(varname="m", sev="medium"))]
plan += [("u_cmp", dict(varname="e", sev="low"))]
plan += [("u_pass", dict(varname="s", sev="medium"))]
plan += [("u_struct", dict(sev="medium"))]
plan += [("u_bool", dict(sev="low"))]

# undefined_behavior (21)
plan += [("b_shift", dict(kind="large", val=v, sev="high")) for v in (33, 40, 45, 60)]
plan += [("b_shift", dict(kind="neg", val=v, sev="high")) for v in (-1, -3, -5)]
plan += [("b_shift", dict(kind="width", val=0, sev="high"))]
plan += [("b_divzero", dict(sev="high"))] * 3
plan += [("b_intmin", dict(sev="high"))] * 3
plan += [("b_boolinv", dict(sev="high"))] * 3
plan += [("b_shift", dict(kind="large", val=v, sev="high")) for v in (50, 55)]
plan += [("b_divzero", dict(sev="high"))] * 2

assert len(plan) == 100, f"plan size {len(plan)} != 100"


def build_one(spec):
    name, kw = spec
    fn = globals()[name]
    return fn(**kw)


def emit(idx, code, defect_type, kind, expected, severity, notes, func):
    n3 = f"{idx:03d}"
    cpp_path = os.path.join(OUT, f"sample_{n3}.cpp")
    with open(cpp_path, "w", encoding="utf-8") as f:
        f.write(code + "\n")
    lines = code.splitlines()
    dline = None
    for i, ln in enumerate(lines, 1):
        if SENT in ln:
            dline = i
            break
    assert dline is not None, f"sample_{n3}: missing defect sentinel"
    meta = {
        "id": f"sample_{n3}",
        "category": "A",
        "defect_type": defect_type,
        "defect_location": {
            "line": dline,
            "function": func,
            "note": lines[dline - 1].strip(),
        },
        "severity": severity,
        "planted": True,
        "expected_verdict": expected,
        "expected_detectors": [kind],
        "notes": notes,
        "generator": "676c-expA-generate",
    }
    json_path = os.path.join(OUT, f"sample_{n3}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return n3, meta


def main():
    manifest = {}
    for i, spec in enumerate(plan, 1):
        code, dt, kind, exp, sev, notes, func = build_one(spec)
        n3, meta = emit(i, code, dt, kind, exp, sev, notes, func)
        manifest[n3] = meta
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    # 统计
    from collections import Counter
    c = Counter(m["defect_type"] for m in manifest.values())
    print(f"generated {len(manifest)} samples")
    for k, v in sorted(c.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
