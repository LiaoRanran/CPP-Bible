#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""annotate_693_b.py — 693-A1：AI 双标（Annotator B 独立第二标注）+ 一致性统计。

背景（为什么需要这一批）
========================
692 验收报告 H1 登记：**人类 IAA 仍为 0**。论文 §7 T1（标签有效性）目前只有一个
标注者（= 管道实测标签），无法区分"标签错"与"标注者主观漂移"。本批补的是**第二个
标注者的完整材料**：先用一个**独立的 AI 标注者（Annotator B）**跑通全流程，产出
分歧清单 → 人类裁决表 → 统计脚本，使真人标注回来后 0 成本可算 κ。

⚠ 诚实边界（必须随产物一起引用）
================================
1. **Annotator B 是 AI 模拟的第二标注者，不是人类。** 它只能证明"流程跑得通、
   分歧分布长什么样"，**不能替代人类 IAA**。人类 IAA 在本批之后**仍为 0**。
2. **Annotator A 不是人类标注**，而是 676g/681 冻结矩阵里的 ``expected_verdict``，
   语义是"在八资产×双优化档实测下任一资产是否报告"（**声明可检出性**）。
   因此 A 与 B 的分歧里，有一部分是"实测可检出 vs 静态判读认为不该检出"的
   **语义层分歧**，不完全等价于两个人对同一个概念的分歧。
3. **去标识化泄漏污染**：B 在执行静态阅读时，看到 13 条样本头部注释里残留的
   ``expected_verdict:`` 原文（689 材料包净化未覆盖）。这些条目的 B 标签已标记
   ``leak_exposed=true``，主 κ 之外另给**剔除泄漏后的敏感性 κ**。
4. B 执行前已知材料包总体分布（145 条中 catch 96 / miss 49），存在**锚定风险**；
   该先验只在"极端不确定"时影响判定，已在 ``b_confidence=low`` 条目中登记。

Annotator B 协议（与 A 刻意不同的判读视角）
==========================================
* 视角：**ISO C++ 语义 + 常规告警档（-Wall -Wextra）的静态判读**；
* 输入：仅去标识化源码 + 八资产定义（asan / ubsan / tsan / compiler-warn /
  wunsequenced / cross-compile / linker / compile-time）；
* 禁止：不得查询任何实测结果、不得参考其他标注者；
* 四态：
  - ``catch``      至少一个资产会明确产出诊断（sanitizer 报告 / 告警 / 链接错误 / 编译失败）；
  - ``miss``       八资产全部静默（逻辑错误、协议缺陷、标准不要求诊断的语义 UB）；
  - ``unknown``    判定依赖材料中**未给出**的上下文（第二 TU、链接顺序、-std 版本、
                   实际地址对齐、运行期参数）；
  - ``contradiction`` 材料自相矛盾（依赖缺失 / 无法编译 / 标注条件互斥）。

用法
====
    python tools/annotate_693_b.py                 # 产出 693_ai_double_label.json
    python tools/annotate_693_b.py --csv           # 同时产出 693_human_adjudication_package.csv

输出
====
* ``data/693_ai_double_label.json``          A/B 双标 + raw agreement / κ / 混淆矩阵 / 分歧清单
* ``data/693_human_adjudication_package.csv`` 人类裁决表（human_verdict 列**留空**）
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "data" / "annotation_package"
MAPPING = ROOT / "data" / "689_annotation_key_mapping.json"
OUT_JSON = ROOT / "data" / "693_ai_double_label.json"
OUT_CSV = ROOT / "data" / "693_human_adjudication_package.csv"

VERDICTS = ("catch", "miss", "unknown", "contradiction")

# ---------------------------------------------------------------------------
# 去标识化泄漏清单（B 在阅读时暴露到的条目）
# ---------------------------------------------------------------------------
# 689 材料包的注释净化没有覆盖 ``// expected_verdict: <value>`` 这一行，
# 导致下列样本在源码里明文保留了 A 的标签。B 无法"忘记"已看到的内容 ⇒ 标记剔除。
LEAK_EXPOSED = {
    "S021": "catch", "S022": "miss", "S033": "miss", "S034": "miss",
    "S035": "catch", "S039": "catch", "S051": "catch", "S055": "miss",
    "S058": "catch", "S074": "catch", "S111": "miss", "S120": "miss",
    "S133": "catch",
}

# ---------------------------------------------------------------------------
# Annotator B 标注：anon_id -> (verdict, confidence, reason)
# ---------------------------------------------------------------------------
# confidence: high = 判据唯一且无版本/平台依赖；medium = 依赖告警档或优化档；
#             low   = 依赖未给出的上下文，但不足以列为 unknown。
B_LABELS: dict[str, tuple[str, str, str]] = {
    # --- 并发 ---
    "S001": ("catch", "high", "relaxed 标志不构成 happens-before，TSan 报 d 的竞态"),
    "S022": ("miss", "high", "fetch_sub 下溢是逻辑错误，无 UB、无告警（泄漏暴露）"),
    "S033": ("miss", "high", "锁优先级反转是调度语义缺陷，八资产均无报告（泄漏暴露）"),
    "S034": ("miss", "high", "分配/释放 convoy 无 UB、无竞态（泄漏暴露）"),
    "S043": ("catch", "high", "两线程无同步 ++g，TSan 报 data race"),
    "S055": ("catch", "medium", "delete old 后另一线程仍读 b->tag/data ⇒ ASan UAF；"
                                "但实测可能未触发，需裁决（泄漏暴露）"),
    "S059": ("catch", "high", "bench_race 两线程无同步写 g_shared，TSan 命中"),
    "S074": ("catch", "high", "writer 在发布后仍写非原子字段 c->cached，TSan 命中（泄漏暴露）"),
    "S078": ("catch", "high", "两线程无同步 ++g，TSan 命中"),
    "S079": ("catch", "high", "同上，TSan 命中"),
    "S089": ("miss", "high", "atomic fetch_add 正确同步，无竞态"),
    "S094": ("catch", "high", "两线程无同步 ++g，TSan 命中"),
    "S104": ("catch", "high", "两线程并发 push_back 同一 vector，TSan 命中"),
    "S105": ("catch", "high", "返回局部变量地址并解引用，ASan stack-use-after-scope / -Wreturn-local-addr"),
    "S106": ("catch", "high", "同 S059，TSan 命中"),
    "S138": ("miss", "medium", "屏障语义夹具靠汇编/输出对比观测，八资产无报告；"
                               "spin 标志已先置位不会挂死"),
    # --- 未初始化 / 求值顺序 ---
    "S003": ("catch", "medium", "两个 i++ 之间无序列点 ⇒ GCC -Wsequence-point（-Wall）告警"),
    "S005": ("miss", "high", "实参求值顺序 unspecified 但非 UB，无告警"),
    "S007": ("catch", "medium", "读未初始化 x；-O2 下 -Wuninitialized 命中（-O0 可能不报）"),
    "S008": ("catch", "medium", "i = i++ + 1 无序列点修改并读取，GCC -Wsequence-point 命中"),
    "S020": ("catch", "medium", "i = i++ 无序列点，GCC -Wsequence-point 命中"),
    "S023": ("miss", "high", "两个函数实参求值顺序 unspecified，非 UB，无告警"),
    "S044": ("catch", "medium", "读未初始化 m；-Wuninitialized/-Wmaybe-uninitialized 可能命中"),
    "S071": ("catch", "medium", "a[i] = i++ 同一表达式读写 i 无序列点，-Wsequence-point 命中"),
    "S080": ("catch", "medium", "同 S007，读未初始化 x"),
    "S084": ("catch", "medium", "f(i++, i++) 两次无序列点修改，-Wsequence-point 命中"),
    "S111": ("catch", "medium", "a[i++] = i++ + i++ 多次无序列点修改，-Wsequence-point 命中"
                                "（与 A 分歧，泄漏暴露）"),
    "S112": ("miss", "high", "bump(i) 两次调用顺序 unspecified，非 UB，无告警"),
    "S116": ("catch", "medium", "i = i++ + ++i 无序列点修改，-Wsequence-point 命中"),
    # --- 整数 / 位运算 ---
    "S009": ("catch", "high", "100000*100000 有符号溢出，UBSan signed-integer-overflow 命中"),
    "S015": ("catch", "high", "n << -1 位移指数为负，UBSan shift 命中"),
    "S026": ("catch", "high", "1 << 40 超过 int 宽度，编译期 -Wshift-count-overflow 命中"),
    "S037": ("catch", "high", "INT_MAX + 1 有符号溢出，UBSan 命中"),
    "S049": ("catch", "medium", "int 与 sizeof 无符号比较，-Wsign-compare（-Wall for C++）命中"),
    "S051": ("catch", "high", "13! 溢出 int，UBSan signed-integer-overflow 命中（泄漏暴露）"),
    "S056": ("catch", "high", "INT_MAX + 1，UBSan 命中"),
    "S057": ("catch", "high", "INT_MAX + 1，UBSan 命中"),
    "S065": ("miss", "medium", "x << 31 在 C++20 起良定义；UBSan shift 只查指数范围，不报"),
    "S066": ("miss", "high", "无符号位域截断是良定义，无告警"),
    "S083": ("catch", "high", "INT_MAX + 1，UBSan 命中"),
    "S093": ("catch", "high", "v + 1（v=INT_MAX）溢出，UBSan 命中"),
    "S097": ("catch", "high", "x << 32 常量位移超宽度，-Wshift-count-overflow 命中"),
    "S100": ("catch", "high", "INT_MAX + 1，UBSan 命中"),
    "S102": ("miss", "high", "bswap 两次为恒等，良定义"),
    "S114": ("catch", "high", "-INT_MIN 有符号溢出，UBSan/编译期 -Woverflow 命中"),
    "S124": ("miss", "medium", "负数右移 C++20 起良定义；C++17 为实现定义，均无诊断"),
    "S141": ("catch", "medium", "int/unsigned 比较，-Wsign-compare 命中"),
    "S143": ("catch", "high", "x << 33 常量位移超宽度，-Wshift-count-overflow 命中"),
    # --- 内存安全 ---
    "S004": ("catch", "high", "new int(1) 未 delete，LSan 报泄漏"),
    "S006": ("catch", "high", "二次 delete，ASan double-free 命中"),
    "S012": ("catch", "high", "返回局部变量地址并写入，ASan stack-use-after-scope / -Wreturn-local-addr"),
    "S014": ("catch", "high", "arr[10] 越界写，ASan heap-buffer-overflow 命中"),
    "S017": ("catch", "high", "new int[100] 未释放，LSan 报泄漏"),
    "S018": ("catch", "high", "shared_ptr 成环，退出时 LSan 报泄漏"),
    "S024": ("catch", "high", "返回局部变量引用，-Wreturn-local-addr 命中"),
    "S025": ("catch", "high", "memcpy 5 字节进 4 字节缓冲，ASan heap-buffer-overflow 命中"),
    "S028": ("catch", "high", "空指针写，ASan 报 SEGV"),
    "S030": ("catch", "high", "二次 delete，ASan double-free 命中"),
    "S031": ("catch", "high", "a[5] 越界写（a[4]），ASan stack-buffer-overflow 命中"),
    "S032": ("catch", "high", "lambda 按引用捕获局部变量并逃逸，ASan stack-use-after-scope 命中"),
    "S038": ("catch", "high", "vector 析构后读 *p，ASan heap-use-after-free 命中"),
    "S040": ("catch", "high", "a[5] 越界写（a[4]），ASan stack-buffer-overflow 命中"),
    "S041": ("catch", "high", "返回局部变量地址并解引用，ASan/-Wreturn-local-addr 命中"),
    "S042": ("catch", "high", "a[6] 越界读（new int[4]），ASan heap-buffer-overflow 命中"),
    "S045": ("catch", "high", "push_back 后再用旧迭代器，ASan heap-use-after-free 命中"),
    "S058": ("catch", "high", "malloc 未 free，LSan 报泄漏（泄漏暴露）"),
    "S060": ("catch", "high", "遍历中 push_back 致 realloc，ASan heap-use-after-free 命中"),
    "S063": ("catch", "high", "delete 后解引用，ASan heap-use-after-free 命中"),
    "S064": ("catch", "high", "new[] 配 delete，ASan alloc-dealloc-mismatch 命中"),
    "S067": ("catch", "high", "a[5] 越界读（a[3]），ASan stack-buffer-overflow 命中"),
    "S068": ("catch", "high", "空指针写，ASan 报 SEGV"),
    "S069": ("miss", "high", "new[]/delete[] 配对正确，nothrow 失败返回 nullptr 为良定义"),
    "S070": ("catch", "high", "strcpy 10 字节进 4 字节缓冲，ASan/-Wstringop-overflow 命中"),
    "S073": ("catch", "high", "reserve 后使用旧迭代器，ASan heap-use-after-free 命中"),
    "S081": ("catch", "high", "new[] 配 delete，ASan alloc-dealloc-mismatch 命中"),
    "S082": ("catch", "high", "memcpy 9 字节进 4 字节缓冲，ASan/-Wstringop-overflow 命中"),
    "S087": ("catch", "high", "二次 free，ASan double-free 命中"),
    "S088": ("catch", "high", "循环 i<=4 写 a[4]，ASan stack-buffer-overflow 命中"),
    "S090": ("catch", "high", "string_view 在 append 后悬垂，ASan heap-use-after-free 命中"),
    "S091": ("catch", "high", "parent 强引用成环 + scrub_stack，LSan 报泄漏"),
    "S092": ("catch", "high", "空指针写，ASan 报 SEGV"),
    "S107": ("catch", "high", "resize 后使用旧指针，ASan heap-use-after-free 命中"),
    "S113": ("catch", "high", "delete 后写 *p，ASan heap-use-after-free 命中"),
    "S115": ("catch", "high", "a[4] 越界写（new int[4]），ASan heap-buffer-overflow 命中"),
    "S117": ("catch", "high", "lambda 按引用捕获局部 x 存入全局 function，ASan 命中"),
    "S118": ("catch", "high", "vptr 置空后虚调用，解引用空指针，ASan 报 SEGV"),
    "S119": ("catch", "high", "new int[64] 未释放，LSan 报泄漏"),
    "S121": ("catch", "high", "浅拷贝后 delete a 与栈上 b 双次 delete data，ASan double-free 命中"),
    "S123": ("catch", "high", "两节点 shared_ptr 成环 + scrub_stack，LSan 报泄漏"),
    "S125": ("catch", "high", "二次 delete，ASan double-free 命中"),
    "S128": ("catch", "high", "二次 delete[]，ASan double-free 命中"),
    "S130": ("catch", "high", "free 后写 *p，ASan heap-use-after-free 命中"),
    "S131": ("catch", "high", "new[] 配 delete，ASan alloc-dealloc-mismatch 命中"),
    "S135": ("catch", "high", "同 S018，shared_ptr 成环，LSan 报泄漏"),
    "S136": ("catch", "high", "p 被二次 new 覆盖，首块泄漏，LSan 命中（泄漏暴露）"),
    "S140": ("catch", "high", "二次 delete，ASan double-free 命中"),
    "S142": ("catch", "high", "a[5] 越界写（a[4]），ASan stack-buffer-overflow 命中"),
    "S144": ("catch", "high", "delete 后写 *p，ASan heap-use-after-free 命中"),
    "S145": ("catch", "high", "保存并解引用局部变量地址，ASan stack-use-after-scope 命中"),
    # --- 别名 / 对齐 / 字节序 ---
    "S002": ("catch", "medium", "C 风格强转后解引用 ⇒ GCC -Wstrict-aliasing（-Wall,level 3）告警"),
    "S027": ("miss", "medium", "reinterpret_cast 型别名在默认告警档下静默；"
                               "cross-compile 只比两编译器输出，同档位一致"),
    "S035": ("catch", "high", "alignas(1) 缓冲 +1 后按 double* 写，UBSan alignment 命中（泄漏暴露）"),
    "S036": ("catch", "high", "buffer+2 按 float* 读，UBSan alignment 命中"),
    "S050": ("catch", "high", "buffer+7 按 int64_t* 读，UBSan alignment 命中"),
    "S052": ("unknown", "low", "alignas(2) 缓冲实际地址可能偶然 8 字节对齐 ⇒ 对齐 UB 是否触发不确定；"
                               "-Wcast-align 不在 -Wall 内"),
    "S086": ("catch", "high", "buffer+3 按 short* 写，UBSan alignment 命中"),
    "S096": ("catch", "medium", "同 S002，C 风格强转解引用，-Wstrict-aliasing 告警"),
    "S099": ("miss", "medium", "严格别名夹具靠 -O0/-O2 输出差异观测，八资产无报告"),
    "S110": ("catch", "medium", "同 S002，-Wstrict-aliasing 告警"),
    "S127": ("catch", "high", "buffer+1 按 int* 写，UBSan alignment 命中"),
    "S137": ("miss", "medium", "同 S099，别名夹具无 sanitizer/告警输出"),
    # --- STL / 语言 / OOP ---
    "S011": ("catch", "high", "transform 写 4 容量 out 存 5 元素，ASan heap-buffer-overflow 命中"),
    "S013": ("miss", "high", "构造函数内虚调用是良定义（解析到 B::vf），无诊断"),
    "S019": ("miss", "high", "lower_bound 作用于未排序区间是 UB，但无 sanitizer/告警覆盖"),
    "S029": ("catch", "high", "if (x = 1) 赋值作真值，-Wparentheses 命中"),
    "S046": ("catch", "high", "控制流到达非 void 函数结尾，-Wreturn-type 命中"),
    "S048": ("catch", "high", "同上，-Wreturn-type 命中"),
    "S061": ("miss", "high", "double→int 窄化转换良定义"),
    "S062": ("catch", "high", "修改字符串字面量；C++11 起 char* 接收字面量即非良定义，编译期命中"),
    "S072": ("catch", "high", "格式串 1 个转换符给 2 个实参，-Wformat-extra-args 命中"),
    "S075": ("miss", "high", "两阶段名字查找结果为 f(double)，良定义、无诊断"),
    "S076": ("miss", "high", "析构为观测型（只计数），无真实二次释放、无泄漏"),
    "S085": ("catch", "high", "%d 传入 double，-Wformat 命中"),
    "S101": ("catch", "medium", "auto_ptr 在 C++11 起弃用（-Wdeprecated-declarations）、"
                                "C++17 起移除（编译失败）⇒ 至少一档命中"),
    "S108": ("miss", "high", "同 S061，窄化转换良定义"),
    "S109": ("catch", "high", "对 vector<bool> 代理取地址非良定义，编译期命中"),
    "S122": ("miss", "medium", "bitset 越界下标是 UB，但 libstdc++ 断言默认关闭，无报告"),
    "S126": ("catch", "medium", "改写 const 对象：rodata 写入触发 SIGSEGV/ASan SEGV"),
    "S129": ("miss", "medium", "deque 两端插入只失效迭代器、不释放元素内存 ⇒ 无 ASan 报告"),
    "S132": ("miss", "medium", "经非 volatile 左值访问 volatile 对象是 UB，但无资产可检出"),
    # --- 信号 / 中断 / 嵌入式 ---
    "S077": ("miss", "high", "信号处理函数改非原子全局是 UB，但无资产可检出"),
    "S098": ("miss", "high", "同上，无诊断"),
    "S139": ("miss", "medium", "处理函数内再 raise 同步信号属允许行为，无诊断"),
    # --- 真实世界重构（逻辑/协议缺陷） ---
    "S039": ("catch", "high", "固定读 5 字节但缓冲仅 3 字节，ASan heap-buffer-overflow 命中（泄漏暴露）"),
    "S120": ("miss", "high", "OpenSSH roaming 重传过量是逻辑/协议缺陷，八资产均无报告（泄漏暴露）"),
    "S133": ("catch", "high", "DNS 名拷贝差一字节越界写，ASan heap-buffer-overflow 命中（泄漏暴露）"),
    # --- 除零 / 运行期参数 ---
    "S047": ("catch", "high", "volatile 阻止折叠，运行期除零，UBSan division-by-zero 命中"),
    "S095": ("catch", "medium", "默认无参运行 ⇒ z = argc-1 = 0 ⇒ 运行期除零，UBSan 命中"),
    "S103": ("catch", "high", "同 S047，volatile 除零，UBSan 命中"),
    "S134": ("catch", "high", "同 S047，volatile 除零，UBSan 命中"),
    # --- 依赖未给出上下文 ---
    "S010": ("miss", "medium", "单线程下 lock 后经异常返回未 unlock，但进程即结束；无报告"),
    "S016": ("unknown", "high", "ODR 夹具需要第二个 TU 与链接顺序才能判定，材料包只给 TU A"),
    "S053": ("unknown", "high", "register 关键字是否触发 -Wdeprecated-register 取决于 -std"),
    "S054": ("unknown", "high", "inline 变量是 C++17 特性；C++11/14 下非良定义 ⇒ 判定依赖 -std"),
    "S021": ("catch", "high", "volatile 阻止折叠，(a+b)*2 溢出，UBSan 命中（泄漏暴露）"),
}

FAMILY_OF = {
    "memory": ("memory_safety", "use_after_free", "double_free", "memory_leak",
               "smart_pointer", "raii_violation", "move_semantics", "uninitialized_read"),
    "bounds": ("out_of_bounds", "null_pointer_deref"),
    "integer": ("integer_overflow", "bit_operation"),
    "alias_type": ("type_punning", "strict_aliasing", "alignment", "endianness"),
    "concurrency": ("data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable"),
    "stl": ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"),
    "language_oop": ("virtual_function", "lambda_capture", "logic_error", "cross_tu_ub", "other_ub"),
    "embedded_link": ("volatile_misuse", "register_ub", "interrupt_safety", "linker_odr"),
}


def _family(defect_type: str) -> str:
    """把 34 类规范缺陷类型折叠到 8 个家族。"""
    for fam, types in FAMILY_OF.items():
        if defect_type in types:
            return fam
    return "language_oop"


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def cohen_kappa(a: list[str], b: list[str]) -> float | None:
    """Cohen's κ（标准库实现）。pe→1 且未完全一致时无法定义，返回 None。"""
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    labels = set(ca) | set(cb)
    pe = sum((ca.get(k, 0) / n) * (cb.get(k, 0) / n) for k in labels)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else None
    return (po - pe) / (1.0 - pe)


def _read_source(rel: str) -> str:
    p = PKG / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", action="store_true", help="同时产出人类裁决 CSV")
    args = ap.parse_args()

    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    rows = {str(r["anon_id"]): r for r in mapping["rows"]}

    missing = sorted(set(rows) - set(B_LABELS))
    extra = sorted(set(B_LABELS) - set(rows))
    if missing or extra:
        raise SystemExit(f"[693-A1] 标注覆盖不一致：缺 {missing}；多 {extra}")

    per_sample: list[dict[str, Any]] = []
    for anon in sorted(rows):
        a_row = rows[anon]
        a_verdict = str(a_row["expected_verdict"])
        b_verdict, b_conf, b_reason = B_LABELS[anon]
        src = _read_source(str(a_row["file"]))
        per_sample.append({
            "anon_id": anon,
            "uid": a_row["uid"],
            "source_batch": a_row["source_batch"],
            "defect_type": a_row["defect_type"],
            "defect_family": _family(str(a_row["defect_type"])),
            "annotator_a": {"verdict": a_verdict, "provenance": "681 冻结矩阵 expected_verdict（实测）"},
            "annotator_b": {"verdict": b_verdict, "confidence": b_conf, "reason": b_reason},
            "agree": a_verdict == b_verdict,
            "leak_exposed": anon in LEAK_EXPOSED,
            "leaked_value": LEAK_EXPOSED.get(anon),
            "code_sha256": _sha256(src),
            "code_bytes": len(src.encode("utf-8")),
        })

    pairs = [(s["annotator_a"]["verdict"], s["annotator_b"]["verdict"]) for s in per_sample]
    a_list = [p[0] for p in pairs]
    b_list = [p[1] for p in pairs]
    n = len(pairs)
    raw = sum(1 for x, y in pairs if x == y) / n * 100.0
    kappa = cohen_kappa(a_list, b_list)

    clean = [(x, y) for (x, y), s in zip(pairs, per_sample) if not s["leak_exposed"]]
    kappa_clean = cohen_kappa([x for x, _ in clean], [y for _, y in clean])
    raw_clean = sum(1 for x, y in clean if x == y) / len(clean) * 100.0

    confusion: dict[str, dict[str, int]] = {
        av: {bv: sum(1 for x, y in pairs if x == av and y == bv) for bv in VERDICTS}
        for av in sorted({x for x, _ in pairs})
    }

    disagreements = [s for s in per_sample if not s["agree"]]

    def _rate(items: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
        """按 ``key`` 分桶统计分歧率；``key`` 支持 ``a.b`` 形式取嵌套字段。"""
        out: dict[str, dict[str, Any]] = {}
        buckets: dict[str, list[dict[str, Any]]] = {}
        for s in items:
            cur: Any = s
            for part in key.split("."):
                cur = cur[part]
            buckets.setdefault(str(cur), []).append(s)
        for k in sorted(buckets):
            grp = buckets[k]
            dis = sum(1 for s in grp if not s["agree"])
            out[k] = {"n": len(grp), "n_disagree": dis,
                      "disagree_pct": round(dis / len(grp) * 100.0, 1)}
        return out

    doc: dict[str, Any] = {
        "schema": "queyi-693-ai-double-label/v1",
        "generated_by": "tools/annotate_693_b.py",
        "generated_at": _now(),
        "honest_status": {
            "human_iaa": 0,
            "note": ("Annotator B 为 AI 模拟第二标注者；人类 IAA 在本批之后仍为 0。"
                     "本产物只用于跑通流程 + 产出分歧清单，不能充当人类一致性证据。"),
            "annotator_a_is_human": False,
            "annotator_a_semantics": "声明可检出性（八资产实测 OR），非人类审读真值",
            "known_biases": [
                "B 执行前已知材料包总体分布 catch 96 / miss 49（锚定风险）",
                f"{len(LEAK_EXPOSED)} 条样本源码残留 expected_verdict 注释 ⇒ B 标签被污染",
                "B 的 compiler-warn 判据按 -Wall -Wextra 推定，未实测",
            ],
        },
        "protocol": {
            "annotator_b_prompt": (
                "你是独立的第二标注者。只依据给定源码与八资产定义，按 ISO C++ 语义与常规告警档"
                "（-Wall -Wextra）判断：给定检测条件下是否会产出诊断报告。禁止查询任何实测结果或"
                "其他标注者结论。四态：catch / miss / unknown / contradiction。"
            ),
            "assets": ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
                       "cross-compile", "linker", "compile-time"],
        },
        "n_samples": n,
        "leak_exposed": sorted(LEAK_EXPOSED),
        "n_leak_exposed": len(LEAK_EXPOSED),
        "raw_agreement_pct": round(raw, 2),
        "cohen_kappa": round(kappa, 4) if kappa is not None else None,
        "sensitivity_excluding_leak": {
            "n": len(clean),
            "raw_agreement_pct": round(raw_clean, 2),
            "cohen_kappa": round(kappa_clean, 4) if kappa_clean is not None else None,
        },
        "distributions": {
            "annotator_a": dict(Counter(a_list)),
            "annotator_b": dict(Counter(b_list)),
        },
        "confusion_matrix_a_rows_b_cols": confusion,
        "n_disagreements": len(disagreements),
        "disagreement_by_defect_type": _rate(per_sample, "defect_type"),
        "disagreement_by_family": _rate(per_sample, "defect_family"),
        "disagreement_by_batch": _rate(per_sample, "source_batch"),
        "disagreement_by_b_confidence": _rate(per_sample, "annotator_b.confidence"),
        "disagreements": [
            {"anon_id": s["anon_id"], "defect_type": s["defect_type"],
             "annotator_a": s["annotator_a"]["verdict"],
             "annotator_b": s["annotator_b"]["verdict"],
             "b_confidence": s["annotator_b"]["confidence"],
             "b_reason": s["annotator_b"]["reason"],
             "leak_exposed": s["leak_exposed"]}
            for s in disagreements
        ],
        "per_sample": per_sample,
    }

    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"[693-A1] n={n} raw={raw:.1f}% kappa={kappa:.3f} "
          f"disagree={len(disagreements)} (剔除泄漏后 κ={kappa_clean:.3f})")

    if args.csv:
        _write_csv(per_sample)
        print(f"[693-A2] 裁决表 → {OUT_CSV}")


def _write_csv(per_sample: list[dict[str, Any]]) -> None:
    """人类裁决表（仅分歧条目；human_verdict 列必须留空）。"""
    dis = [s for s in per_sample if not s["agree"]]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["sample_id", "code_sha256", "defect_type_A", "annotator_A",
                    "annotator_B", "b_confidence", "b_reason",
                    "leak_suspected", "human_verdict", "human_note", "source_code"])
        for s in dis:
            src = _read_source(f"sources/{s['anon_id']}.cpp")
            w.writerow([
                s["anon_id"], s["code_sha256"], s["defect_type"],
                s["annotator_a"]["verdict"], s["annotator_b"]["verdict"],
                s["annotator_b"]["confidence"], s["annotator_b"]["reason"],
                "yes" if s["leak_exposed"] else "no",
                "",  # human_verdict —— 留给人类填，脚本绝不写
                "",  # human_note
                src,
            ])


if __name__ == "__main__":
    main()
