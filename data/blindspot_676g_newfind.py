#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""blindspot_676g_newfind.py — 676g 任务 E：新发现盲区的验证与分类。

输入  data/blindspot_676g_detection_matrix.json
输出  data/blindspot_676g_new_findings.json

方法（诚实边界）
================
1. 候选清单来自各批次报告的明确记载（报告+行号），不把批次没提过的东西编造成"批次新发现"。
2. 每条声明都在本批全量判定矩阵上复核（样本级 + 类型级数字）。
3. 根因分类用本批做的**对照实验**校准（如：WSL g++ 13.3 接受 -fsanitize=pointer-overflow、
   拒绝伪名 ⇒ "clang 专属"是机制误判，正确分类是"配置缺口"）。
4. 已被 673u 等先前批次记载的问题（如 wunsequenced 恒 unknown）标为 known_before，不算新发现。
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MATRIX = HERE / "blindspot_676g_detection_matrix.json"
OUT = HERE / "blindspot_676g_new_findings.json"

AVAILABLE = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]


def load_matrix():
    doc = json.loads(MATRIX.read_text(encoding="utf-8"))
    by_uid = {s["uid"]: s for s in doc["samples"]}
    return doc, by_uid


def sample_verdicts(by_uid, uid):
    s = by_uid[uid]
    return {a: s["per_asset"].get(a, {}).get("verdict") for a in AVAILABLE}


def type_stat(doc, dtype):
    rows = [s for s in doc["samples"] if s["defect_type"] == dtype]
    n = len(rows)
    if n == 0:
        return None
    catch = sum(1 for s in rows if s["or_verdict_all8"] == "catch")
    miss = sum(1 for s in rows if s["or_verdict_all8"] == "miss")
    unk = sum(1 for s in rows if s["or_verdict_all8"] == "unknown")
    per_asset = {a: sum(1 for s in rows
                        if s["per_asset"].get(a, {}).get("verdict") == "catch")
                 for a in AVAILABLE}
    return {"n": n, "catch": catch, "miss": miss, "unknown": unk,
            "blindspot_ratio": round((miss + unk) / n, 4),
            "asset_catch": per_asset}


def main() -> int:
    doc, by_uid = load_matrix()
    findings = []

    def add(fid, title, source, kind, classification, verify, experiment=None,
           correction=None, known_before=False):
        f = {"id": fid, "title": title, "source_claim": source,
             "category": kind, "classification": classification,
             "verification": verify, "known_before": known_before}
        if experiment:
            f["control_experiment"] = experiment
        if correction:
            f["correction_to_batch_report"] = correction
        findings.append(f)

    # ── 1) EDEADLK / std::system_error abort：崩溃但零报告 ──────────────
    v103 = sample_verdicts(by_uid, "expE:sample_E103")
    v110 = sample_verdicts(by_uid, "expE:sample_E110")
    st = type_stat(doc, "deadlock")
    add(
        "NF-1", "进程级 abort（std::system_error/EDEADLK）对所有 6 个可用资产隐形",
        "data/676c_扩样E报告.md §4「一条额外发现的盲区（新类别，卡片未列）」："
        "E103/E110 由 libstdc++ 抛 std::system_error(\"Resource deadlock avoided\") 并 abort(rc=6)，"
        "既不挂起也不产生任何 sanitizer 报告——程序当场崩掉而检测流水线标签为「干净」",
        "tool/流水线行为", "检测器设计缺失",
        {"samples": {"expE:sample_E103": v103, "expE:sample_E110": v110},
         "interpretation": "若两样本全部可用资产=miss 且无任何报告文本 ⇒ 声明在矩阵上成立",
         "deadlock_type_stats": st},
        known_before=False)

    # ── 2) ASan 对 printf("%.*s") 的漏报 ────────────────────────────────
    v81 = sample_verdicts(by_uid, "expD:D081")
    v93 = sample_verdicts(by_uid, "expD:D093")
    st_str = type_stat(doc, "string_ub")
    add(
        "NF-2", "ASan 不校验 printf(\"%.*s\", len, ptr) 形态的悬垂读",
        "data/676c_扩样D报告.md §4 第 2 条：悬垂 string_view 用 printf(\"%.*s\",...) 输出，"
        "ASan 只拦截 printf(\"%s\", p) 形态的指针校验，libc 内部读不被编译期插桩 ⇒ 漏报",
        "tool/插桩边界", "工具链限制（库函数插桩的参数形态覆盖不足）",
        {"samples": {"expD:D081": v81, "expD:D093": v93},
         "string_ub_type_stats": st_str},
        known_before=False)

    # ── 3) float-cast-overflow 默认不启用（配置缺口，显式启用即报）──────
    v98 = sample_verdicts(by_uid, "expG:sample_G098")
    st_int = type_stat(doc, "integer_overflow")
    add(
        "NF-3", "-fsanitize=undefined 默认组不含 float-cast-overflow ⇒ G098 型 float→uint64 越界转换零报告",
        "data/676c_扩样G报告.md §附录：G098（jsoncpp#1545 float→uint64 越界转换）："
        "默认 -fsanitize=undefined 不启用 float-cast-overflow → 无报告",
        "config/口径", "配置问题（检查存在、detect 固定口径未启用）",
        {"samples": {"expG:sample_G098": v98}, "integer_overflow_type_stats": st_int},
        {"setup": "WSL g++ 13.3，double d=3e19; (unsigned long long)d（G098 同型 UB 转换）",
         "result": ("默认口径 -fsanitize=undefined：输出 0，无任何报告（miss）；"
                    "显式 -fsanitize=float-cast-overflow：runtime error: 3e+19 is outside "
                    "the range of representable values of type 'long long unsigned int'（catch）"),
         "conclusion": "检查在本工具链存在且有效，仅因 detect 固定 -fsanitize=undefined 口径未启用 ⇒ 配置缺口"},
        known_before=False)

    # ── 4) pointer-overflow「clang 专属」机制纠错（配置缺口而非平台限制）──
    v13 = sample_verdicts(by_uid, "expG:sample_G013")
    st_po = type_stat(doc, "pointer_overflow")
    add(
        "NF-4", "pointer-overflow 检查并非 clang 专属：WSL g++ 13.3 接受该 flag，只是不在 undefined 默认组",
        "data/676c_扩样G报告.md §附录：G013（CVE-2016-2177 指针算术回绕）：GCC 的 -fsanitize=undefined "
        "不含 pointer-overflow 检查（clang 专属资产）→ 检测器无报告",
        "config/口径（批次报告误标为平台限制）", "配置问题（**修正**：非 clang 专属）",
        {"samples": {"expG:sample_G013": v13}, "pointer_overflow_type_stats": st_po},
        {"setup": "WSL g++ 13.3 上分别编译 -fsanitize=pointer-overflow、"
                  "-fsanitize=bogus-test-flag（对照）、-fsanitize=undefined",
         "result": ("pointer-overflow 编译通过（rc=0）；bogus-test-flag 被拒绝："
                    "g++: error: unrecognized argument to '-fsanitize=' option；"
                    "undefined 组编译通过但不含该检查"),
         "conclusion": ("GCC 13.3 实现了 pointer-overflow 检查（接受 flag、拒绝未知名），"
                        "只是不在 -fsanitize=undefined 默认组 ⇒ 与 NF-3 同类：**配置缺口**。"
                        "批次报告的「clang 专属资产（平台限制）」分类不成立，本批予以纠正。"
                        "G013 在 detect 固定口径下仍为 miss（矩阵验证），但根因归类必须改。")},
        known_before=False)

    # ── 5) TSan 只检测竞争：memory_order / ABA / 优先级反转全盲 ──────────
    mo = type_stat(doc, "memory_order")
    aba = type_stat(doc, "aba_problem")
    lpi = type_stat(doc, "lock_priority_inversion")
    add(
        "NF-5", "TSan 不建模内存序：memory_order / aba_problem / lock_priority_inversion 三类结构性盲区",
        "data/676c_扩样E报告.md §4：lock_priority_inversion 76.7%、aba_problem 66.7%、"
        "memory_order 55.0%（本批以全量矩阵复测）",
        "tool/设计哲学 + 平台", "检测器设计缺失 + 平台依赖（x86-TSO 下不显现）",
        {"type_stats": {"memory_order": mo, "aba_problem": aba,
                        "lock_priority_inversion": lpi},
         "interpretation": "类型级盲区比例 >50% 且 asan/ubsan 几乎无补充覆盖 ⇒ 结构性而非样本噪声",
         "note": "批次报告已指出，本批在全量矩阵上验证并量化（复核性发现，非首次发现）"},
        known_before=True)

    # ── 6) 端序缺陷：纯逻辑错误全盲 ─────────────────────────────────────
    endi = type_stat(doc, "endianness")
    add(
        "NF-6", "endianness（字节序误用）：无任何运行时陷阱，全部资产不可见",
        "data/676c_扩样F报告.md §5 第 1 条：端序是逻辑错误，sanitizer/compiler 均不报，35 候选全 miss",
        "defect/本质", "缺陷本质（逻辑/语义错误，无运行时表现）",
        {"type_stats": endi},
        known_before=True)

    # ── 7) 未初始化读：需要 MSan，本地资产池无此资产 ─────────────────────
    uninit = type_stat(doc, "uninitialized_read")
    add(
        "NF-7", "uninitialized_read：本地无 MSan 等价资产，20 个样本结构性全盲",
        "data/676c_扩样数据生成报告.md §结论第 4 条：uninitialized_read 需 MSan，本地无可用检测器，"
        "20 个样本标注 miss 且检测器一致返回 miss",
        "tool/资产池缺口", "工具链限制（本地未接线 MSan；MSan 需 libc++ 全量重编）",
        {"type_stats": uninit,
         "interpretation": "asan（分配 poisoning 不同机制）/ubsan/tsan 对未初始化读均无报告"},
        known_before=True)

    # ── 8) 已知问题复核：wunsequenced 恒 unknown（673u 已记载）────────────
    wu = {a: sum(1 for s in doc["samples"]
                 if s["per_asset"].get(a, {}).get("verdict") == "unknown")
          for a in ("wunsequenced", "compile-time")}
    add(
        "NF-8", "（复核已知）wunsequenced/compile-time 两资产在全部 1147 样本上恒 unknown",
        "673u 判据修正记载（tools/holdout_reveal_661.py 头注）+ 本规格常见坑第 4 条："
        "MinGW g++ 13.1 不认 -Wunsequenced ⇒ 恒 unknown，不计入盲区",
        "tool/工具链版本", "工具链限制（已知，列为对照基线，不算新发现）",
        {"asset_unknown_counts_over_n": {"n_total": len(doc["samples"]), **wu},
         "interpretation": "两资产 unknown 数应等于样本总数；统计口径中已按规格说明排除"},
        known_before=True)

    doc_out = {
        "schema": "queyi-blindspot-new-findings/676g",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": MATRIX.relative_to(ROOT).as_posix(),
        "method": "每条声明 = 批次报告原文 + 全量判定矩阵复核 + （需要时）本批对照实验；"
                  "known_before=true 的是批次已记载、本批全量验证的条目，不冒充新发现",
        "n_findings": len(findings),
        "n_new": sum(1 for f in findings if not f["known_before"]),
        "findings": findings,
    }
    OUT.write_text(json.dumps(doc_out, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"[676g] new_findings: {len(findings)} 条（新 {doc_out['n_new']} / 复核 "
          f"{doc_out['n_findings'] - doc_out['n_new']}）→ {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
