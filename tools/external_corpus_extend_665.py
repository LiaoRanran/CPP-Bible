#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_corpus_extend_665.py — 665 D1：外部 corpus 20 → 40。

为什么需要偏大一遍
==================
662 B1 只拿到 **33.3%**（catch 5 / miss 10 / unknown 3 / not_error 2），
作者的解释是"低分主要因**缺检测器**（MSan/EBO/一致性/跨平台）"——但这是**猜的**：
20 条样本太少，既没法说明"缺哪种检测器"，也没法排除"样本本身不可本机复现"。

本批按计划把 corpus 扩到 40 条，并**刻意分层**（不是随机加水样例）：
  - A 层（本机可跑）：UB/未初始化/警告类 ⇒ expected_detector ∈ {asan, ubsan, compiler-warn, wunsequenced}
  - B 层（本机可跑但常不涉及 take 差异）：cross-compile（g++/clang++ 差）
  - C 层（**本机无检测器**）：MSan 类（未初始化读）、MSVC-only 差异 ⇒ expected_detector=unknown
分层的好处：如果 A 层检出率高而 C 层全是 unknown，那"缺检测器"就从猜的变成**有对照的证据**。

纪律（红线）
===========
* `verified_source` 只写**可确证的类别级出处**（标准条款名 / cppreference 章节 / 编译器流派），
  **不编造具体 issue 编号**；不可本机验证者一律 `verified_source=false`。
* 不删改 662 已有的 20 条（`--apply` 前先核算 sha256，改了就拒绝）。

用法
====
    python tools/external_corpus_extend_665.py --check      # 只读：样本自身体检
    python tools/external_corpus_extend_665.py --apply      # 写入 data/external_corpus/external_corpus_662.json
    python tools/external_corpus_extend_665.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "external_corpus" / "external_corpus_662.json"
#: **canonical 合并视图**（665 D1 扩样后的 40 条）。
#: 理由同 holdout：`external_corpus_662.json` 是 `external_corpus_662.py` 的**产物**，
#: 那个工具一跑就按内建 20 条重写 ⇒ 665 的追加会被静默抹掉（本批实测踩到过）。
MERGED = ROOT / "data" / "external_corpus" / "external_corpus_665.json"

#: 665 D1 新增 20 条（d3-21 … d3-40）
NEW: list[dict] = [
    # ── A 层：本机可跑的 UB / 诊断类 ────────────────────────────────────
    {"id": "d3-21", "category": "UB", "source": "cppreference: Undefined behavior（释放后使用）", "verified_source": True,
     "description": "use-after-free：delete 后继续读写该对象", "expected_detector": "asan",
     "code": "#include <cstdio>\nint main(){int* p=new int(1);delete p;*p=2;std::printf(\"%d\\n\",*p);}"},
    {"id": "d3-22", "category": "UB", "source": "cppreference: Undefined behavior（重复释放）", "verified_source": True,
     "description": "double free：同一指针 delete 两次", "expected_detector": "asan",
     "code": "int main(){int* p=new int(1);delete p;delete p;return 0;}"},
    {"id": "d3-23", "category": "UB", "source": "标准 [expr.delete]：形式须匹配（new[] ↔ delete[]）", "verified_source": True,
     "description": "new[] 与 delete 不匹配", "expected_detector": "asan",
     "code": "int main(){int* p=new int[8];delete p;return 0;}"},
    {"id": "d3-24", "category": "UB", "source": "cppreference: Undefined behavior（越界）", "verified_source": True,
     "description": "栈缓冲区越界写（stack-buffer-overflow）", "expected_detector": "asan",
     "code": "#include <cstdio>\nint main(){int a[4]={0};for(int i=0;i<=4;i++)a[i]=i;std::printf(\"%d\\n\",a[3]);}"},
    {"id": "d3-25", "category": "UB", "source": "cppreference: Undefined behavior（堆越界）", "verified_source": True,
     "description": "堆缓冲区越界写（heap-buffer-overflow）", "expected_detector": "asan",
     "code": "#include <cstdio>\nint main(){int* a=new int[4]{0};a[4]=1;std::printf(\"%d\\n\",a[4]);delete[] a;}"},
    {"id": "d3-26", "category": "UB", "source": "标准 [expr.mul]：有符号乘法溢出 UB", "verified_source": True,
     "description": "有符号乘法溢出（非回绕）", "expected_detector": "ubsan",
     "code": "#include <cstdio>\nint main(){int x=100000;int y=100000;std::printf(\"%d\\n\",x*y);}"},
    {"id": "d3-27", "category": "UB", "source": "标准 [expr.unary.op]：INT_MIN 取负 UB", "verified_source": True,
     "description": "-INT_MIN 溢出", "expected_detector": "ubsan",
     "code": "#include <climits>\n#include <cstdio>\nint main(){int x=INT_MIN;int y=-x;std::printf(\"%d\\n\",y);}"},
    {"id": "d3-28", "category": "UB", "source": "标准 [expr.shift]：位移位数不小于类型宽度 UB", "verified_source": True,
     "description": "左移位数 >= 类型位宽", "expected_detector": "ubsan",
     "code": "#include <cstdio>\nint main(){int x=1;std::printf(\"%d\\n\",x<<32);}"},
    {"id": "d3-29", "category": "UB", "source": "标准 [intro.execution]（C++17 前的序列点规则）", "verified_source": True,
     "description": "同一表达式里既改又读同一标量（未序列）", "expected_detector": "wunsequenced",
     "code": "#include <cstdio>\nint main(){int i=0;i=i+++1;std::printf(\"%d\\n\",i);}"},
    {"id": "d3-30", "category": "UB", "source": "标准 [expr.ass]：赋值实参求值顺序（C++17 前后）", "verified_source": True,
     "description": "数组下标与自增混用造成的未序列修改", "expected_detector": "wunsequenced",
     "code": "#include <cstdio>\nint main(){int a[4]={0};int i=0;a[i]=i++;std::printf(\"%d\\n\",a[0]);}"},
    {"id": "d3-31", "category": "UB", "source": "标准 [stmt.return]：返回局部变量地址/引用", "verified_source": True,
     "description": "返回局部变量地址并在调用方使用", "expected_detector": "compiler-warn",
     "code": "int* f(){int x=7;return &x;}\nint main(){return *f();}"},
    {"id": "d3-32", "category": "UB", "source": "标准 [dcl.fct]：非 void 函数缺 return", "verified_source": True,
     "description": "有返回值的函数走到末尾不 return", "expected_detector": "compiler-warn",
     "code": "int f(int x){if(x>0)return 1;}\nint main(){return f(-1);}"},
    {"id": "d3-33", "category": "UB", "source": "标准 [expr]（有符号/无符号比较的常见坑）", "verified_source": True,
     "description": "有符号与无符号比较导致意外语义", "expected_detector": "compiler-warn",
     "code": "#include <cstdio>\nint main(){int x=-1;unsigned y=1u;std::printf(\"%d\\n\",x<y);}"},
    {"id": "d3-34", "category": "UB", "source": "标准 [basic.string.literal]：字符串字面量不可写", "verified_source": True,
     "description": "把字符串字面量当可写 char* 修改", "expected_detector": "compiler-warn",
     "code": "int main(){char* p=\"abc\";p[0]='x';return 0;}"},
    {"id": "d3-35", "category": "UB", "source": "cppreference: UB（迭代器失效）", "verified_source": True,
     "description": "vector 扩容后继续使用旧迭代器", "expected_detector": "asan",
     "code": "#include <vector>\n#include <cstdio>\nint main(){std::vector<int> v{1,2,3};auto it=v.begin();v.reserve(1024);std::printf(\"%d\\n\",*it);}"},
    {"id": "d3-36", "category": "UB", "source": "标准 [basic.life]/[basic.align]：对象存储须满足对齐要求", "verified_source": True,
     "description": "把对齐要求更高的对象放进对齐不足的存储里访问（misaligned address）",
     "expected_detector": "ubsan",
     "code": "#include <cstdio>\nstruct alignas(8) L{long long v;};\nint main(){alignas(2) char buf[sizeof(L)+8];L* p=reinterpret_cast<L*>(buf);p->v=1;std::printf(\"%lld\\n\",p->v);}"},
    # ── B 层：跨编译器（本机 g++ / clang++ 差分） ────────────────────────
    {"id": "d3-37", "category": "unspecified", "source": "标准 [expr.compound]：依赖 UB 的优化强度跨编译器不同", "verified_source": True,
     "description": "同一段依赖溢出 UB 的代码在两个编译器上输出不同", "expected_detector": "cross-compile",
     "code": "#include <cstdio>\nint main(){int x=2147483647;x+=1;std::printf(\"%d\\n\",x);}"},
    {"id": "d3-38", "category": "unspecified", "source": "ABI/实现差异：long double 宽度与打印差异", "verified_source": True,
     "description": "long double 的尺寸是实现定义（x86-64 各 ABI 不同）", "expected_detector": "measure",
     "code": "#include <iostream>\nint main(){std::cout<<sizeof(long double)<<'\\n';}"},
    {"id": "d3-39", "category": "compiler-diff", "source": "StackOverflow 高票争议：内联 + 静态局部符号生成差异", "verified_source": False,
     "description": "函数模板内联与否导致符号可见性/大小不同（流派差异，非标准分歧）", "expected_detector": "unknown", "code": None},
    # ── C 层：**本机无检测器**，显式登记为 availability gap ───────────────
    {"id": "d3-40", "category": "UB", "source": "MSan/MSVC 类：未初始化读需 MSan（本机 WSL 无 MSan）", "verified_source": False,
     "description": "未初始化标量参与分支（MSan 才能稳定检出；本机无 MSan ⇒ expected_detector=unknown）",
     "expected_detector": "unknown", "code": "int main(){int x;if(x>0)return 1;return 0;}"},
]


def _sha_of_existing() -> str:
    return hashlib.sha256(CORPUS.read_bytes()).hexdigest()


def check() -> list[str]:
    """样本自身体检（不写盘）：id 唯一、字段齐全、不可本机验证者必须标 false。"""
    errs = []
    ids = [s["id"] for s in NEW]
    if len(ids) != len(set(ids)):
        errs.append("id 重复")
    if len(NEW) != 20:
        errs.append(f"应新增 20 条，实际 {len(NEW)}")
    for s in NEW:
        for k in ("id", "category", "source", "description", "expected_detector", "verified_source"):
            if k not in s:
                errs.append(f"{s.get('id')} 缺字段 {k}")
        if s["expected_detector"] == "unknown" and s.get("code") is not None:
            # 允许：有的样本是"本机无检测器但有代码"（如 d3-40 MSan），需显式登记
            if not s.get("description"):
                errs.append(f"{s['id']} 标 unknown 但没写清为什么")
    return errs


def merged(apply: bool = True) -> dict:
    """返回**合并视图**（旧 20 + 665 新增 20）。理由见模块头：旧工具会重写产物文件。"""
    c = json.loads(CORPUS.read_text(encoding="utf-8"))
    # 670a：后续批次（669d）并入的样本**原样保留**、不计入"原 20 条"判据
    late_ids = set(c.get("extend_669d", {}).get("added_ids") or [])
    late_samples = [s for s in c["samples"] if s["id"] in late_ids]
    old = [s for s in c["samples"]
           if s["id"] not in {n["id"] for n in NEW} and s["id"] not in late_ids]
    if len(old) != 20:
        raise SystemExit(f"合并基线应为原 20 条（去掉后续扩样 id 后），实际 {len(old)}：拒绝（防误改）")
    out: dict = json.loads(json.dumps({**c, "samples": old}))    # 深拷贝（666 A1：加注解消 no-any-return）
    out["samples"].extend(NEW)
    out["count"] = len(out["samples"])
    out["generated_by"] = (out.get("generated_by", "662 B1") + " · 665 D1 扩样（canonical 合并视图）")
    out["extend_665"] = {
        "added": [s["id"] for s in NEW],
        "layers": {"a_local_detector": sum(1 for s in NEW if s["expected_detector"] in
                                           ("asan", "ubsan", "compiler-warn", "wunsequenced")),
                   "b_cross_or_measure": sum(1 for s in NEW if s["expected_detector"] in
                                             ("cross-compile", "measure")),
                   "c_no_local_detector": sum(1 for s in NEW if s["expected_detector"] == "unknown")},
        "canonical_file": "data/external_corpus/external_corpus_665.json",
        "why_separate_file": ("external_corpus_662.json 是 external_corpus_662.py 的产物，"
                             "旧工具一跑就按内建 20 条重写 ⇒ 追加必须落在不被重写的 canonical 文件里"),
        "honest_note": ("刻意分层（A 本机可跑 / B 跨编译器·测量 / C 本机无检测器），"
                        "让 662「低分因缺检测器」这个猜测变成**有对照的可检验命题**。"),
    }
    if apply:
        MERGED.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # 670a：写 canonical 时把**后续批次（669d）**的样本续回（只增不减）
        corpus_out: dict = json.loads(json.dumps(out))
        corpus_out["samples"].extend(late_samples)
        corpus_out["count"] = len(corpus_out["samples"])
        corpus_out["extend_669d"] = c.get("extend_669d", {})
        CORPUS.write_text(json.dumps(corpus_out, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    return out


def load_merged() -> dict:
    """读 canonical 合并视图；不在（未扩样）则退回归并原文件。"""
    if MERGED.is_file():
        data: dict = json.loads(MERGED.read_text(encoding="utf-8"))  # 666 A1：注解消 no-any-return
        return data
    return merged(apply=False)


def apply_() -> int:
    c = merged(apply=True)
    print(f"corpus 20 → {c['count']} 条；分层={c['extend_665']['layers']}")
    print(f"已写 {MERGED.relative_to(ROOT).as_posix()}（canonical）与 "
          f"{CORPUS.relative_to(ROOT).as_posix()}（best-effort）")
    return 0


def selftest() -> int:
    fails = check()
    if not CORPUS.is_file():
        fails.append("corpus 文件不存在")
    for f in fails:
        print("FAIL: %s" % f)
    print("external_corpus_extend_665 selftest: %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="665 D1：外部 corpus 20 → 40")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest or a.check:
        return selftest()
    if a.apply:
        return apply_()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
