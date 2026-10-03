#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""generate_E.py — 676c-E 扩样并发高级缺陷：候选样本生成器（Task A）。

按任务卡配额生成 E001..E200：
    memory_order 40 / atomic_ub 35 / deadlock 35 / aba_problem 30 /
    lock_priority_inversion 30 / condition_variable 30

每个样本写出一对文件：
    data/expansion_676c_E/sample_EXXX.cpp   —— 可编译的最小复现（含 main）
    data/expansion_676c_E/sample_EXXX.json  —— 权威标注

标注字段严格按任务卡「每个样本的 .json 字段（全部必填）」：
    sample_id / defect_type / defect_location{line,function,description} /
    severity / planted / expected_verdict / expected_detectors /
    trigger_condition / thread_count / timeout_seconds / notes

defect_location.line 由 DEFECT 标记行自动定位（源码里写 /*DEFECT: ...*/，
生成器把该行号回填进 JSON），避免手写行号漂移。
"""
from __future__ import annotations

import importlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from _dsl import SAMPLES, S  # noqa: F401  (S 供各 defs_* 模块使用)


def _defect_line(full_text: str) -> int:
    """在**落盘后的完整文本**里定位第一个 /*DEFECT 行号（1-based）；
    没有标记则回退到 1。直接扫最终文本，避免手写行号与文件头偏移漂移。"""
    for i, ln in enumerate(full_text.splitlines(), 1):
        if "/*DEFECT" in ln:
            return i
    return 1


#: 函数定义行的形态：`[static] [类型] name(args) [const] {`
_FUNC_DEF = re.compile(
    r"^(?:static\s+|inline\s+|extern\s+)*"
    r"(?:[A-Za-z_][\w:<>,\s*&]*?[\s*&])?"          # 返回类型（可含模板/指针/引用）
    r"([A-Za-z_]\w*)\s*\([^;]*\)\s*(?:const\s*)?(?:\{\s*)?$")


def _defect_function(full_text: str, line: int) -> str:
    """从 DEFECT 行向上找最近的外层函数定义名。

    为什么要自动推导而不是手写：手写的 function 名一旦与源码里的实际函数名
    漂移（如写了 shift_ptr、代码里叫 shifter），标注就变成假信息 —— 而这类
    错误在 200 个样本里出现了近百个。标注必须从**落盘后的文本**里读出来。
    """
    lines = full_text.splitlines()
    for i in range(min(line, len(lines)) - 1, -1, -1):
        s = lines[i].strip()
        if not s or s.startswith("//"):
            continue
        m = _FUNC_DEF.match(s)
        if m and m.group(1) not in ("if", "for", "while", "switch", "return",
                                    "catch", "sizeof"):
            return m.group(1)
        if s.endswith("{") or s.endswith("}"):
            continue
    return "main"


def _thread_count(full_text: str) -> int:
    """数出真正创建了多少个 std::thread 对象。

    不能直接数 `std::thread` 出现次数：`std::thread a(f), b(g);` 只出现一次
    `std::thread` 却创建了 2 个线程。按语句切分后数顶层逗号分隔的声明器。
    """
    n = 0
    for stmt in re.findall(r"std::thread\s+[^;]*;", full_text):
        depth, cur, parts = 0, "", []
        for ch in stmt[:-1]:
            if ch in "(<":
                depth += 1
            elif ch in ")>":
                depth -= 1
            if ch == "," and depth == 0:
                parts.append(cur)
                cur = ""
            else:
                cur += ch
        parts.append(cur)
        n += sum(1 for p in parts if "(" in p)
    return n


def _header(s: dict) -> str:
    return (
        f"// sample_{s['sid']}\n"
        f"// defect_type: {s['dtype']}\n"
        f"// severity: {s['sev']}\n"
        f"// planted: true\n"
        f"// expected_verdict: {s['verdict']}\n"
        f"// expected_detectors: {','.join(s['dets'])}\n"
        f"// thread_count: {s['nthreads']}\n"
        f"// timeout_seconds: {s['timeout']}\n"
        f"// (authoritative annotation in sample_{s['sid']}.json)\n\n"
    )


def _ensure_chrono(code: str) -> str:
    """用了 sleep_for 的样本显式补 <chrono>：不依赖 <thread> 的传递包含
    （MinGW 与 WSL libstdc++ 的传递包含不同，显式包含才是可移植写法）。"""
    if "sleep_for" not in code or "#include <chrono>" in code:
        return code
    return code.replace("#include <thread>", "#include <thread>\n#include <chrono>", 1)


PARTS = [
    "defs_E01_memory_order_a", "defs_E02_memory_order_b",
    "defs_E03_atomic_ub_a", "defs_E04_atomic_ub_b",
    "defs_E05_deadlock_a", "defs_E06_deadlock_b",
    "defs_E07_aba_a", "defs_E08_aba_b",
    "defs_E09_lockpri_a", "defs_E10_lockpri_b",
    "defs_E11_condvar_a", "defs_E12_condvar_b",
]


def main() -> int:
    for m in PARTS:
        importlib.import_module(m)
    SAMPLES.sort(key=lambda s: s["sid"])
    ids = [s["sid"] for s in SAMPLES]
    assert len(set(ids)) == len(ids), f"sample_id 重复: {len(ids)-len(set(ids))} 个"
    assert ids == [f"E{i:03d}" for i in range(1, 201)], (
        f"id 序列不连续/不完整: n={len(ids)} 首={ids[0]} 尾={ids[-1]}")

    for s in SAMPLES:
        s["code"] = _ensure_chrono(s["code"])
        base = os.path.join(HERE, f"sample_{s['sid']}")
        full = _header(s) + s["code"]
        with open(base + ".cpp", "w", encoding="utf-8", newline="\n") as f:
            f.write(full)
        dline = _defect_line(full)
        meta = {
            "sample_id": f"sample_{s['sid']}",
            "defect_type": s["dtype"],
            "defect_location": {
                "line": dline,
                # function / thread_count 一律从落盘文本推导，不采信手写值
                "function": _defect_function(full, dline),
                "description": s["desc"],
            },
            "severity": s["sev"],
            "planted": True,
            "expected_verdict": s["verdict"],
            "expected_detectors": s["dets"],
            "trigger_condition": s["trig"],
            "thread_count": _thread_count(full),
            "timeout_seconds": s["timeout"],
            "notes": s["notes"],
        }
        with open(base + ".json", "w", encoding="utf-8", newline="\n") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
            f.write("\n")

    import collections
    by_type = collections.Counter(s["dtype"] for s in SAMPLES)
    by_verdict = collections.Counter(s["verdict"] for s in SAMPLES)
    print(f"生成 {len(SAMPLES)} 个候选样本 -> {HERE}")
    print("类型分布:", dict(by_type))
    print("预期判定:", dict(by_verdict),
          f"盲区(miss)占比={by_verdict['miss']/len(SAMPLES):.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
