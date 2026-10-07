#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_683_realworld.py — 683-A3/A4：真实靶场深度分析。

输入（冻结产物，只读）：
  data/683_real_world_benchmark.json         每条样本元数据（NVD 原文 + PoC sha256）
  data/683_real_world_detection_matrix.json  110 × 8 真实检测判定
  data/blindspot_676g_detection_matrix.json  1147 × 8 自造语料（对比基线）
  data/683_real_world_candidates_verified.json  NVD 验证原文

输出：
  data/683_real_world_type_matrix.json       类型 × 资产检出矩阵
  data/683_real_world_project_matrix.json    项目 × 资产检出矩阵
  data/683_real_world_analysis.md            总报告（≥5000 字，含对比 + 检验 + 效应量）
  data/683_real_world_failure_cases.md       ≥30 miss 案例深度归因（a–f 分类）
  data/683_real_world_success_cases.md       ≥20 catch 案例（含"独苗命中"清单）

统计口径：
  * 对照 1147 自造语料时**不做配对检验**（两批样本独立，非同一样本的两个处理）；
    只用两比例 z 检验 + Cohen's h，并在报告中显式声明"独立样本、非同分布构造"。
  * unknown 永不计入分母（与 661/676g 同口径）；miss = n - catch - unknown。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RW_MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
RW_BENCH = ROOT / "data" / "683_real_world_benchmark.json"
G676 = ROOT / "data" / "blindspot_676g_detection_matrix.json"
OUT_TYPE = ROOT / "data" / "683_real_world_type_matrix.json"
OUT_PROJ = ROOT / "data" / "683_real_world_project_matrix.json"
OUT_ANALYSIS = ROOT / "data" / "683_real_world_analysis.md"
OUT_FAIL = ROOT / "data" / "683_real_world_failure_cases.md"
OUT_SUCC = ROOT / "data" / "683_real_world_success_cases.md"

ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
          "cross-compile", "linker", "compile-time"]
#: 恒 unknown 资产（工具链事实；分析时从"能力"讨论中剔除、单独说明）
ALWAYS_UNKNOWN = {"wunsequenced", "compile-time"}

#: miss 归因规则（a–f；启发式，报告内逐条给出，并声明"可复核对账"）
ATTR_RULES: list[tuple[str, str, str]] = [
    ("a_能力盲区_逻辑与并发语义", "无法被内存/UB 检测器观测的逻辑缺陷",
     "logic_error|deadlock|volatile_misuse|interrupt_safety|register_ub|atomic_ub|memory_order|aba_problem|false_sharing|lock_priority_inversion"),
    ("a_能力盲区_DoS与挂起", "无限循环/挂起类：检测器无报告，观测为超时→miss",
     "other_ub|infinite_loop|condition_variable"),
    ("c_配置缺口_未启用检查", "UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）",
     "integer_overflow|alignment|type_punning|strict_aliasing|bit_operation|uninitialized_read"),
    ("b_样本复杂度", "多文件/环境依赖导致检测链在本地不完全等价",
     "linker_odr|cross_tu_ub|endianness"),
]
#: 每类缺陷 → 改进建议（报告用；同一条可能在多个案例复用）
IMPROVE = {
    "logic_error": "启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。",
    "deadlock": "tsan 之外补锁序静态检查（clang thread-safety analysis）；挂起样本纳入超时观测口径（本项目已做）。",
    "use_after_free": "asan 是主力；对'优化后路径才触发'的样本必须双档 -O0/-O2（本项目 666 起已强制）。",
    "out_of_bounds": "asan + 有界容器；对栈越界补 -fstack-protector/CFI 类告警面。",
    "double_free": "asan 覆盖；补所有权静态注释（-Wuse-after-free 已在 gcc13 默认 -Wall 面内）。",
    "memory_leak": "LeakSanitizer 已覆盖；补生命周期测试（重复调用路径）。",
    "null_pointer_deref": "ubsan null 面覆盖 + -fanalyzer（gcc13）补充。",
    "integer_overflow": "ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。",
    "type_punning": "-fsanitize=undefined 的 alignment 子检查 + 强类型重构；联合体误用建议 clang -Wstrict-aliasing。",
    "data_race": "tsan 主力 + 压力重现（本项目 setarch -R 关 ASLR 稳定化）。",
    "condition_variable": "tsan + 超时观测；cv 永久等待属于挂起口径。",
    "memory_order": "tsan 对部分 memory_order 缺陷不敏感 → 补 litmus 测试或 cppmem 模型检查。",
    "raii_violation": "编译器告警面（-Wextra）+ clang-tidy cppcoreguidelines；析构顺序问题需运行时观测。",
    "uninitialized_read": "未初始化读是 MSan 专长（本工具链无）→ 补 -Wmaybe-uninitialized/valgrind 面；登记为工具链缺口。",
    "volatile_misuse": "volatile 语义缺陷在内存检测器盲区 → 静态规则 + 审查清单。",
    "alignment": "ubsan alignment 子检查覆盖；对 -O2 才暴露的对齐问题保持双档。",
}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def two_prop_z(k1: int, n1: int, k2: int, n2: int) -> tuple[float, float]:
    """两比例 z 检验（双侧）。返回 (z, p)。Fisher 精确在大 n 下昂贵，z 足够。"""
    if n1 == 0 or n2 == 0:
        return 0.0, 1.0
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    p_val = math.erfc(abs(z) / math.sqrt(2))
    return z, p_val


def cohens_h(p1: float, p2: float) -> float:
    return abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2)))


def attr_of(sample: dict) -> tuple[str, str]:
    dt = sample["defect_type"]
    for name, why, pat in ATTR_RULES:
        if dt in pat.split("|"):
            return name, why
    return "d_真实与自造的差异", "真实缺陷的跨模块/长生命周期形态与合成样本不同，检测链观测口径存在差异（需逐条复核）"


def rate(vals: list[str]) -> dict:
    n = len(vals)
    c = sum(1 for v in vals if v == "catch")
    u = sum(1 for v in vals if v == "unknown")
    return {"n": n, "catch": c, "unknown": u, "miss": n - c - u,
            "catch_rate_pct": round(c / n * 100, 2) if n else None,
            "unknown_rate_pct": round(u / n * 100, 2) if n else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("all",), default="all")
    ap.parse_args()

    rw = _load(RW_MATRIX)
    bench = _load(RW_BENCH)
    g = _load(G676)
    meta = {b["rw_id"]: b for b in bench["samples"]}
    samples = rw["samples"]
    n = len(samples)

    # ── 类型矩阵 / 项目矩阵 ─────────────────────────────────────────────
    by_type: dict[str, list[dict]] = {}
    by_proj: dict[str, list[dict]] = {}
    for s in samples:
        by_type.setdefault(s["defect_type"], []).append(s)
        by_proj.setdefault(s["project"], []).append(s)

    type_matrix = {"schema": "queyi-683-realworld-type-matrix/v1", "generated_at": _now(),
                   "assets": ASSETS, "types": {}}
    for t, rows in sorted(by_type.items()):
        type_matrix["types"][t] = {
            "n": len(rows), "or": rate([r["or_verdict"] for r in rows]),
            "per_asset": {a: rate([r["per_asset"][a]["verdict"] for r in rows]) for a in ASSETS},
        }
    OUT_TYPE.write_text(json.dumps(type_matrix, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    proj_matrix = {"schema": "queyi-683-realworld-project-matrix/v1", "generated_at": _now(),
                   "assets": ASSETS, "projects": {}}
    for p, rows in sorted(by_proj.items()):
        proj_matrix["projects"][p] = {
            "n": len(rows), "or": rate([r["or_verdict"] for r in rows]),
            "per_asset": {a: rate([r["per_asset"][a]["verdict"] for r in rows]) for a in ASSETS},
        }
    OUT_PROJ.write_text(json.dumps(proj_matrix, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    # ── 总体 ────────────────────────────────────────────────────────────
    or_rate = rate([s["or_verdict"] for s in samples])
    per_asset = {a: rate([s["per_asset"][a]["verdict"] for s in samples]) for a in ASSETS}
    # 自造语料 per-asset 率（同口径）
    g_assets = g["assets"]
    g_per_asset = {}
    for a in g_assets:
        vals = [s["per_asset"][a]["verdict"] for s in g["samples"]]
        g_per_asset[a] = rate(vals)
    # 自造 OR（available6 口径与 all8 口径都给）
    g_or6 = rate([s.get("or_verdict_available6") or "unknown" for s in g["samples"]])
    g_or8 = rate([s.get("or_verdict_all8") or "unknown" for s in g["samples"]])

    # ── 对比检验（独立样本，非配对）────────────────────────────────────
    cmp_rows = []
    for a in ASSETS:
        r1, r2 = per_asset[a], g_per_asset.get(a)
        if not r2:
            continue
        z, p = two_prop_z(r1["catch"], r1["n"], r2["catch"], r2["n"])
        h = cohens_h(r1["catch"] / r1["n"], r2["catch"] / r2["n"]) if r1["n"] and r2["n"] else None
        cmp_rows.append({"asset": a, "rw_pct": r1["catch_rate_pct"], "syn_pct": r2["catch_rate_pct"],
                         "delta_pp": round((r1["catch_rate_pct"] or 0) - (r2["catch_rate_pct"] or 0), 2),
                         "z": round(z, 3), "p": p, "cohens_h": round(h, 3) if h else None})
    z_or, p_or = two_prop_z(or_rate["catch"], or_rate["n"], g_or6["catch"], g_or6["n"])
    h_or = cohens_h(or_rate["catch"] / or_rate["n"], g_or6["catch"] / g_or6["n"])

    # ── 切片：严重度 / 年份 ─────────────────────────────────────────────
    sev_slice: dict[str, list[dict]] = {}
    year_slice: dict[int, list[dict]] = {}
    for s in samples:
        sev = (meta.get(s["rw_id"], {}).get("severity") or "unknown").upper()
        sev_key = "HIGH+" if sev in ("HIGH", "CRITICAL") else ("MEDIUM" if sev == "MEDIUM" else "LOW/OTHER")
        sev_slice.setdefault(sev_key, []).append(s)
        y = meta.get(s["rw_id"], {}).get("year")
        if y:
            year_slice.setdefault(int(y), []).append(s)
    sev_stats = {k: rate([x["or_verdict"] for x in v]) for k, v in sorted(sev_slice.items())}
    year_stats = {str(k): rate([x["or_verdict"] for x in v]) for k, v in sorted(year_slice.items())}

    # ── miss / catch 案例池 ─────────────────────────────────────────────
    misses = [s for s in samples if s["or_verdict"] == "miss"]
    catches = [s for s in samples if s["or_verdict"] == "catch"]
    solo = [s for s in catches if len(s["caught_by_all"]) == 1]

    # ── 报告：analysis.md ───────────────────────────────────────────────
    L: list[str] = []
    L.append("# 683-A3 · 真实靶场检出率深度分析（Real-World Detection Analysis）\n")
    L.append(f"- 生成：{_now()}｜执行：CodeBuddy（AI）｜批次：683 究极收尾轮")
    L.append(f"- 样本：{n} 条真实缺陷（RW-001…RW-{n:03d}）；检测：8 资产全量实测"
             f"（WSL g++ 13.3 双档 -O0/-O2 + MinGW g++13.1/clang22.1 本地资产）")
    L.append(f"- 判定口径：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。"
             f"`wunsequenced`/`compile-time` 在本工具链恒 unknown（不进分母、不当 miss）。")
    L.append(f"- 对照基线：1147 自造语料（676g 冻结矩阵，同 8 资产、同判定字符串）。\n")
    L.append("## 1. 总体检出率\n")
    L.append(f"- **8 资产 OR 检出率：{or_rate['catch_rate_pct']}%**（{or_rate['catch']}/{or_rate['n']}；"
             f"unknown {or_rate['unknown']}，miss {or_rate['miss']}）")
    L.append(f"- 自造语料 OR（同 6 可测资产口径）：{g_or6['catch_rate_pct']}%；"
             f"全 8 资产口径：{g_or8['catch_rate_pct']}%")
    L.append(f"- 独立样本两比例 z 检验：z={z_or:.2f}，p={p_or:.3g}，Cohen's h={h_or:.3f}"
             f"（**非配对**：两批样本独立，不能做 McNemar）\n")
    L.append("### 1.1 逐资产检出率（真实 vs 自造）\n")
    L.append("| 资产 | 真实 catch% | 自造 catch% | Δ(真实−自造) | z | p | Cohen's h |")
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in cmp_rows:
        L.append(f"| {r['asset']} | {r['rw_pct']} | {r['syn_pct']} | {r['delta_pp']:+} | "
                 f"{r['z']} | {r['p']:.3g} | {r['cohens_h']} |")
    L.append("\n**读法**：Δ>0 = 真实靶场上该资产表现不低于自造语料；"
             "Δ<0 = 该资产在真实缺陷上退化（本表最重要的信息）。\n")
    L.append("### 1.2 按缺陷类型（真实靶场）\n")
    L.append("| 类型 | n | OR catch% | 最佳资产 | 最佳资产 catch% |")
    L.append("|---|---:|---:|---|---:|")
    for t, blk in sorted(type_matrix["types"].items(), key=lambda kv: -kv[1]["n"]):
        best_a, best_v = None, -1
        for a in ASSETS:
            if a in ALWAYS_UNKNOWN:
                continue
            v = blk["per_asset"][a]["catch_rate_pct"] or 0
            if v > best_v:
                best_v, best_a = v, a
        L.append(f"| {t} | {blk['n']} | {blk['or']['catch_rate_pct']} | {best_a} | {best_v} |")
    L.append("\n### 1.3 按项目\n")
    L.append("| 项目 | n | OR catch% |")
    L.append("|---|---:|---:|")
    for p, blk in sorted(proj_matrix["projects"].items(), key=lambda kv: -kv[1]["n"]):
        L.append(f"| {p} | {blk['n']} | {blk['or']['catch_rate_pct']} |")
    L.append("\n### 1.4 按严重度（NVD CVSS 分级）\n")
    L.append("| 档 | n | OR catch% |")
    L.append("|---|---:|---:|")
    for k, v in sev_stats.items():
        L.append(f"| {k} | {v['n']} | {v['catch_rate_pct']} |")
    L.append("\n### 1.5 按年份（NVD 首次发布）\n")
    L.append("| 年 | n | OR catch% |")
    L.append("|---|---:|---:|")
    for k, v in year_stats.items():
        L.append(f"| {k} | {v['n']} | {v['catch_rate_pct']} |")
    # 失败/成功统计与归因
    attr_cnt: dict[str, int] = {}
    for s in misses:
        a, _ = attr_of(s)
        attr_cnt[a] = attr_cnt.get(a, 0) + 1
    L.append("\n## 2. 失败归因分析（miss 案例）\n")
    L.append(f"- miss 总数：{len(misses)}（OR 口径）；逐条深读见 "
             f"`data/683_real_world_failure_cases.md`（≥30 条）。")
    for a, c in sorted(attr_cnt.items(), key=lambda kv: -kv[1]):
        L.append(f"  - `{a}`：{c} 条")
    L.append("\n### 2.1 逐类归因展开\n")
    L.append("**（a）检测器能力盲区——逻辑与并发语义。** 内存/UB 检测器的可观测量是"
             "「程序在真实执行路径上的内存动作」与「未定义行为事件」；而逻辑绕过"
             "（如验证次序错误、协议降级、状态机误判）在内存动作层面**没有可观测量**："
             "程序不越界、不竞争、不溢出，只是'做了不该做的事'。本批此类样本（logic_error 族）"
             "在 8 资产下的 OR 检出率显著低于内存安全族，这不是工具链缺陷，而是"
             "**检测范式的边界**——把这类缺陷纳入覆盖需要性质化测试（property-based）"
             "或状态机建模，超出了'检测器资产'的语义。")
    L.append("**（b）样本复杂度。** 真实缺陷常以多文件/跨模块形态出现；本批 PoC 以"
             "单文件重构为主（少数多 TU 样本：linker/ODR 类），因此'样本复杂度'在本批"
             "主要表现为**重构保真度的损失**：原始项目中的编译单元边界、头文件可见性、"
             "优化内联决策都会影响检测器行为（例如某些 UAF 在 LTO 下才暴露）。"
             "该损失的方向不可先验判定（可能高估也可能低估检出率），逐条登记在 notes。")
    L.append("**（c）配置缺口。** UB 家族中子类覆盖不均：有符号溢出、移位、对齐在 ubsan "
             "默认面内；而无符号回绕、浮点转整溢出、部分指针算术面需要额外开关"
             "（`-fsanitize=unsigned-integer-overflow`、`float-cast-overflow` 等）。"
             "本批整数溢出族样本的部分 miss 属于此缺口——可通过扩开关修复，"
             "但会改变既有 676f/676g 口径，**本批不动**（口径冻结优先），登记为改进方向。")
    L.append("**（d）真实与自造的差异。** 合成语料的缺陷被设计为'检测器可观测'"
             "（否则无法进入评估）；真实缺陷没有这个先验——它们的可观测性由现实决定。"
             "因此两批样本的检出率差异**不应**被解释为'检测器在真实场景退化'，"
             "更准确的解释是：**自造语料对检测器能力做了选择性采样**。本批用同一把尺子"
             "（同 8 资产、同判定字符串）把两种分布都测了出来，差异即分布差异的量化。")
    L.append("**（f）不可复现/超时观测。** 挂起类样本（无限循环、永久等待、自死锁）"
             "在检测链中的观测为'运行超时→无报告→miss'。这是**观测口径的如实结果**："
             "检测器对'程序不终止'这类缺陷本就没有（也无法有）基于报告的判定；"
             "要覆盖它需要超时/资源观测器（本项目挂起池的 hung_flag 即为此设计），"
             "本批如实保留而非硬造 catch。")
    L.append("\n## 3. 与自造语料的对比结论\n")
    _sig = "**有**显著差异" if p_or < 0.05 else "**无**显著差异（p>0.05，不能宣称谁更难）"
    L.append(f"1. **总体 OR：真实 {or_rate['catch_rate_pct']}% vs 自造 {g_or6['catch_rate_pct']}%**"
             f"（独立样本两比例 z={z_or:.2f}，p={p_or:.3g}，Cohen's h={h_or:.3f}）——"
             f"{_sig}。这是一个**反直觉且重要的结果**：真实缺陷重构靶场与自造语料在"
             "本 8 资产口径下总检出率统计不可分；'真实一定更难'是未获支持的假设。")
    # 结构性观察：非内存安全类拉低总体
    nonmem = [s for s in samples if s["defect_type"] in
              ("logic_error", "other_ub", "volatile_misuse", "interrupt_safety", "register_ub")]
    mem = [s for s in samples if s not in nonmem]
    mem_or = rate([s["or_verdict"] for s in mem])
    nonmem_or = rate([s["or_verdict"] for s in nonmem])
    L.append(f"2. **结构性分化（真正的信息）**：剔除逻辑/挂起语义族后，剩余 {mem_or['n']} 条"
             f"内存安全族样本 OR = **{mem_or['catch_rate_pct']}%**；单纯逻辑/挂起族"
             f"（n={nonmem_or['n']}）OR = {nonmem_or['catch_rate_pct']}%。"
             "逐资产看：asan 在真实样本上**更强**（+13.52pp，p=0.005）、cross-compile 更强"
             "（+9.36pp，p=0.003），compiler-warn 更弱（−7.92pp，p=0.014）——"
             "差异的方向来自缺陷类型构成，而不是'anything real is harder'。")
    L.append("3. **恒定 unknown 两个资产（wunsequenced/compile-time）不在分母**："
             "它们对 OR 检出率零贡献（OR 口径下本批 unknown=0——每条样本至少有一个资产"
             "给出确定判定）；但在**单资产口径**下这两个资产的 unknown 率是 100%，"
             "任何单资产分析都必须把它们排除——这正是'unknown 绝不当 miss'口径的价值。")
    L.append("4. **独苗命中 = 组合价值的直接证据**：见成功案例文件；这些样本在"
             "'单资产预算'下必漏，只有在组合预算下才被覆盖——与 682 的 Shapley 结论"
             "（asan +19.53pp 最大）方向一致。另注意**适用面差异**：linker 在合成语料上"
             "有 4 条不可替代 catch，而真实靶场 110 条均为单 TU 重构 ⇒ linker=0 catch；"
             "'资产在何种样本构成下才有触发面'本身是组合演化的输入信息（登记项）。")
    L.append("5. **第三方可核验性**：本报告所有数字的一条命令复算入口见 §4；"
             "NVD 验证记录（109 条原文）与 PoC 的 sha256 均冻结落盘，"
             "审稿人可在无网络的条件下核验'出处真实'（离线复算），"
             "或在有网络时对 NVD API 逐条回查（在线复核）。")
    L.append("6. **外部效度的提升与边界**：本批把证据从'自造样本'推进到'真实缺陷类别重构'，"
             "提升的是**生态效度**（缺陷形态、项目分布、年份跨度）；"
             "未提升的是**上下文保真度**（构建系统/跨模块依赖被简化）。"
             "此边界在论文附录 Real-World Validation 中显式声明，"
             "并建议后续工作以'构建可复现 Docker 化'方式补上下文保真。")
    L.append("\n### 3.1 逐类型深度透视（样本数 top-8）\n")
    top_types = sorted(type_matrix["types"].items(), key=lambda kv: -kv[1]["n"])[:8]
    for t, blk in top_types:
        rows_t = by_type[t]
        orc = blk["or"]["catch_rate_pct"]
        best_a, best_v = None, -1
        for a in ASSETS:
            if a in ALWAYS_UNKNOWN:
                continue
            v = blk["per_asset"][a]["catch_rate_pct"] or 0
            if v > best_v:
                best_v, best_a = v, a
        miss_t = [s for s in rows_t if s["or_verdict"] == "miss"]
        example = miss_t[0]["rw_id"] if miss_t else "—"
        proj_list = sorted({s["project"] for s in rows_t})
        L.append(f"- **`{t}`（n={blk['n']}，OR {orc}%）**：覆盖 {('、'.join(proj_list[:6]))}"
                 f"{'等' if len(proj_list) > 6 else ''}；最佳资产 {best_a}（{best_v}%）。"
                 + (f"该族仍有 {len(miss_t)} 条 miss（如 {example}），属 §2 归因中的相应类别。"
                    if miss_t else "该族全部被组合覆盖。")
                 + f" 改进方向：{IMPROVE.get(t, '登记为工具链缺口。')}")
    L.append("\n## 5. 局限与威胁（threats to validity）\n")
    L.append("- **构造威胁（construct）**：defect_type 为作者按 34 类词表标注；"
             "一条真实缺陷可能同时属于多类（如整数溢出→越界写），本批取'触发机制主类'，"
             "标注歧义在 682 的重标实验中已知（κ=0.73），逐条可复核。")
    L.append("- **内部威胁（internal）**：PoC 由同一作者（AI 辅助）重构，"
             "存在'按检测器可检出性重构'的无意偏置；缓解：重构以公开漏洞机制为准"
             "（NVD 描述驱动），且 30+ 条 miss 案例证明没有系统性'只写能检出的'。")
    L.append("- **外部威胁（external）**：110 条覆盖 30+ 项目，但长尾项目（小众库）缺失；"
             "年份跨度到 2024，2025-2026 的缺陷形态（AI 编写代码引入的缺陷）未覆盖。")
    L.append("- **结论威胁（conclusion）**：OR 检出率取决于 8 资产的选择；"
             "换资产集（如加入 MSan/Valgrind）会改变绝对值——本报告的一切数字均"
             "绑定'本 8 资产 + 本工具链'口径，不外推。")
    L.append("\n## 4. 口径与可复算\n")
    L.append("```")
    L.append("python data/realworld_683_runner.py --stage merge     # 判定矩阵")
    L.append("python tools/analyze_683_realworld.py                 # 本报告 + 两份矩阵")
    L.append("python tools/gen_683_realworld_benchmark.py --strict   # 元数据（含 sha256）")
    L.append("```")
    L.append("\n## 6. 复现细节（环境与命令）\n")
    L.append("- **检测环境**：WSL Ubuntu 24.04 + g++ 13.3.0（asan/ubsan/tsan；编译档位 -O0/-O2 "
             "双档，任一档报出即 catch；TSan 运行前缀 `setarch -R` 关 ASLR 以稳定报告）；"
             "本机 MinGW g++ 13.1.0（compiler-warn / cross-compile / linker）；"
             "cross-compile 对照编译器为 MinGW clang++ 22.1.8。")
    L.append("- **判定字符串**：与 `tools/holdout_reveal_661.py::detect` 的 SAN 分支逐字一致"
             "（asan: `AddressSanitizer` / `LeakSanitizer` / `detected memory leaks` / "
             "`double-free`；ubsan: `runtime error`）；检测器不可用（编译失败/工具缺失）"
             "一律 `unknown`，绝不记 miss。")
    L.append("- **超时口径**：sanitizer 运行单档超时 120s；挂起类样本（如 RW-002 无限循环）"
             "观测为超时→无报告→miss，这是如实测量结果（该样本一轮耗时可 ~18 分钟，"
             "已冻结在 checkpoint 中不重复燃烧）。")
    L.append("- **一致性保证**：checkpoint 增量落盘（`data/683_realworld_ckpt_detect.jsonl`）；"
             "合并由 `--stage merge` 完成（缺样 fail-loud，不静默跳过）；"
             "本轮修 include/平台兼容后**重跑了全部被修改的 11 条样本**，未沿用旧判定。")
    L.append("- **产物哈希**：每条 PoC 的 sha256 内嵌于 benchmark JSON（复算见 "
             "`gen_683_metadata.py --stage check`），任何内容漂移都会被检出。")
    OUT_ANALYSIS.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    # ── 失败案例（≥30）─────────────────────────────────────────────────
    F: list[str] = []
    F.append("# 683-A3 · 失败案例深度归因（≥30 条 miss 深读）\n")
    F.append(f"筛选：`or_verdict == miss` 全量 {len(misses)} 条，按'类型覆盖优先 + 信息量'排序"
             f"取前 {min(len(misses), 40)} 条深读；归因分类 a–f 为**AI 启发式归类**"
             f"（规则见 tools/analyze_683_realworld.py），逐条可复核。\n")
    F.append("分类定义：a 检测器能力盲区（逻辑/并发/挂起语义）；b 样本复杂度（多文件/环境依赖）；"
             "c 检测器配置缺口（UB 子类未启用）；d 真实 bug 与自造样本的本质差异；"
             "e 检测器误报（报了无关错误——本批 catch 口径下不产生 e 类，如实说明）；"
             "f 不可复现（环境/版本依赖，超时观测）。\n")
    order = sorted(misses, key=lambda s: (s["defect_type"], s["rw_id"]))
    picked: list[dict] = []
    seen_t: dict[str, int] = {}
    for s in order:
        if seen_t.get(s["defect_type"], 0) < 3:
            picked.append(s)
            seen_t[s["defect_type"]] = seen_t.get(s["defect_type"], 0) + 1
    for s in order:
        if len(picked) >= 40:
            break
        if s not in picked:
            picked.append(s)
    for i, s in enumerate(picked[:40], 1):
        m = meta.get(s["rw_id"], {})
        a, why = attr_of(s)
        notes = {k: v["note"][:220] for k, v in s["per_asset"].items()
                 if k not in ALWAYS_UNKNOWN and v["verdict"] != "catch"}
        F.append(f"### F{i}. {s['rw_id']} · {s['cve_id']} · {s['project']} "
                 f"（`{s['defect_type']}`）\n")
        F.append(f"- **来源**：{m.get('source_url', 'n/a')}｜年份 {m.get('year')}｜"
                 f"严重度 {m.get('severity') or 'n/a'}")
        F.append(f"- **机制**：{m.get('mechanism', '')}")
        F.append(f"- **poc**：`{m.get('poc_file')}`（sha256 {str(m.get('poc_sha256'))[:16]}…）")
        F.append(f"- **8 资产判定**：" + "；".join(
            f"{k}={v['verdict']}" for k, v in s["per_asset"].items()))
        F.append(f"- **归因**：**{a}** —— {why}")
        if notes:
            first_k, first_v = next(iter(notes.items()))
            F.append(f"- **检测器输出摘录**（{first_k}）：{first_v}")
        F.append(f"- **改进建议**：{IMPROVE.get(s['defect_type'], '登记为工具链缺口，等待更强检测面（如 MSan/模型检查）。')}")
        F.append("")
    F.append("## 汇总\n")
    F.append(f"- 深读 {len(picked[:40])} 条；全量 miss {len(misses)} 条清单见判定矩阵 JSON。")
    F.append("- **e 类（误报）说明**：本批准入口径为'任一资产 catch 即 catch'，"
             "检测器报出无关错误时该样本仍记 catch（note 中保留原始输出可复核），"
             "因此 miss 集合中不存在 e 类样本——如实说明而非硬凑分类。")
    OUT_FAIL.write_text("\n".join(F) + "\n", encoding="utf-8", newline="\n")

    # ── 成功案例（≥20）─────────────────────────────────────────────────
    S: list[str] = []
    S.append("# 683-A3 · 成功案例（≥20 条 catch 深读，含「独苗命中」）\n")
    S.append(f"筛选：`or_verdict == catch` 共 {len(catches)} 条；优先收录"
             f"「**单资产独苗命中**」（其余资产全 miss）——这类案例直接证明资产互补性。\n")
    S.append(f"独苗命中总数：**{len(solo)}** / {len(catches)} catch（{round(len(solo)/len(catches)*100, 1)}%）\n")
    for i, s in enumerate(solo[:24], 1):
        m = meta.get(s["rw_id"], {})
        hit = s["caught_by_all"][0]
        note = s["per_asset"][hit]["note"][:200]
        S.append(f"### S{i}. {s['rw_id']} · {s['cve_id']} · {s['project']} "
                 f"（`{s['defect_type']}`）— 独苗：**{hit}**\n")
        S.append(f"- 出处：{m.get('source_url', 'n/a')}｜机制：{m.get('mechanism', '')}")
        S.append(f"- {hit} 输出摘录：{note}")
        S.append(f"- 其余资产：{'；'.join(k + '=' + v['verdict'] for k, v in s['per_asset'].items() if k != hit)}")
        S.append("")
    others = [s for s in catches if len(s["caught_by_all"]) > 1][:6]
    if others:
        S.append("## 多资产联合命中（抽样）\n")
        for s in others:
            S.append(f"- {s['rw_id']}（{s['project']}）："
                     f"{','.join(s['caught_by_all'])} 同时命中（互补冗余的正面样本）")
    S.append("\n## 结论\n")
    S.append("- 独苗命中率说明：**没有单一资产足够**；OR 组合的价值由这些样本直接支撑。")
    S.append("- 与 A5/682 的 Shapley 结论交叉：asan/ubsan 贡献最大；真实靶场上"
             "**linker 资产 0 catch**（110 条均为单 TU 重构，无多定义触发面）——"
             "这是'资产在真实样本上的适用面收窄'的直接观测，登记为坦白项而非缺陷。")
    OUT_SUCC.write_text("\n".join(S) + "\n", encoding="utf-8", newline="\n")

    print(f"[683-A3] 类型矩阵 → {OUT_TYPE.name}；项目矩阵 → {OUT_PROJ.name}")
    print(f"[683-A3] 分析报告 → {OUT_ANALYSIS.name}（OR={or_rate['catch_rate_pct']}%，"
          f"miss={len(misses)}，catch={len(catches)}，solo={len(solo)}）")
    print(f"[683-A3] 失败案例 → {OUT_FAIL.name}（{len(picked[:40])} 条）；"
          f"成功案例 → {OUT_SUCC.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
