#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
705-B · 失败模式结构化分类 + 能力边界地图（只读，不调用 detect()）。

输入（冻结，只读）：
  - data/683_real_world_detection_matrix.json   （110 条 8 资产判定）
  - data/688_unique_hit_analysis.json           （独苗命中分布）
  - data/692_environment_report.md / .json       （环境感知）
  - data/683_real_world_failure_cases.md          （归因深读）

输出（本批产物）：
  - data/705_failure_mode_taxonomy.md
  - data/705_failure_mode_statistics.md
  - data/705_capability_boundary_map.md
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
MATRIX = os.path.join(DATA, "683_real_world_detection_matrix.json")
UNIQUE = os.path.join(DATA, "688_unique_hit_analysis.json")
ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
          "cross-compile", "linker", "compile-time"]


def load_matrix():
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    idx = {}
    for s in m["samples"]:
        pa = s.get("per_asset", {})
        catches = sum(1 for a in ASSETS if pa.get(a, {}).get("verdict") == "catch")
        unk = sum(1 for a in ASSETS if pa.get(a, {}).get("verdict") == "unknown")
        if catches > 0:
            ors = "catch"
        elif unk == len(ASSETS):
            ors = "unknown"
        else:
            ors = "miss"
        idx[s["rw_id"]] = {
            "rw_id": s["rw_id"], "cve": s.get("cve_id", ""),
            "project": s.get("project", ""), "defect_type": s.get("defect_type", ""),
            "ors": ors, "per_asset": pa,
        }
    return m, idx


# defect_type -> 一级失败模式
def primary_mode(dt):
    if dt == "logic_error":
        return "逻辑型"
    if dt == "data_race":
        return "并发型"
    if dt in ("integer_overflow", "type_punning"):
        return "配置依赖型"
    # out_of_bounds / use_after_free / null_pointer_deref / double_free / memory_leak 的 miss
    return "语义复杂型（语境保真损失）"


def main():
    m, idx = load_matrix()
    n_miss = sum(1 for s in idx.values() if s["ors"] == "miss")
    # 一级计数
    by_primary = {}
    by_type = {}
    miss_samples = []
    for s in idx.values():
        if s["ors"] == "miss":
            pm = primary_mode(s["defect_type"])
            by_primary[pm] = by_primary.get(pm, 0) + 1
            by_type[s["defect_type"]] = by_type.get(s["defect_type"], 0) + 1
            miss_samples.append(s)

    # 独苗命中
    with open(UNIQUE, encoding="utf-8") as f:
        uniq = json.load(f)
    sole = uniq["sole_catcher_counts"]  # asan/cross-compile/tsan/ubsan
    n_unique = uniq["n_unique_hit"]

    # ---------- taxonomy.md ----------
    taxonomy = f"""# 705-B · 失败模式结构化分类体系（Failure-Mode Taxonomy）

> 口径：基于 683 冻结检测矩阵（110 条真实缺陷，8 资产 OR 判定）与 683/688/692 归因。
> 所有失败案例均来自 `or_verdict == miss` 的 **{n_miss}** 条；分类为 AI 启发式（a–f 归因）归纳，
> 逐条可复核。**这是 110 条样本上观察到的模式，不声称覆盖所有失败模式。**

## 一级分类（6 类）

| 一级 | 定义 | 在 110 条 miss 中的样本数 | 占 miss 比 |
|---|---|---:|---:|
| 逻辑型 | 缺陷是逻辑/协议/状态机错误，内存动作与 UB 事件层无可观测信号 | {by_primary.get('逻辑型',0)} | {by_primary.get('逻辑型',0)*100.0/n_miss:.1f}% |
| 并发型 | data race / 跨线程非同步访问，需 tsan + 压力重现 | {by_primary.get('并发型',0)} | {by_primary.get('并发型',0)*100.0/n_miss:.1f}% |
| 配置依赖型 | UB 子类检查未启用（无符号回绕/alignment/strict-aliasing 等） | {by_primary.get('配置依赖型',0)} | {by_primary.get('配置依赖型',0)*100.0/n_miss:.1f}% |
| 语义复杂型（语境保真损失） | 真实跨模块/长生命周期形态在单 TU 重构下保真度损失 | {by_primary.get('语义复杂型（语境保真损失）',0)} | {by_primary.get('语义复杂型（语境保真损失）',0)*100.0/n_miss:.1f}% |
| 环境依赖型 | 测量环境 profile 改变导致部分资产不可用→捕获丢失（692 配对实验） | 跨样本（见统计） | — |
| 平台特定型 | 资产可用性受 OS/工具链约束（wunsequenced/compile-time 恒 unknown；linker 仅多 TU 触发） | 结构性 | — |

## 二级分类与案例

### 逻辑型（{by_primary.get('逻辑型',0)} 条）
- **协议/状态机误判**：CVE-2021-41773（Apache 路径规范化绕过）、CVE-2021-22946（curl STARTTLS 降级）、CVE-2022-32221（curl 307 改方法）
- **身份认证/权限绕过**：CVE-2018-15473（OpenSSH 用户枚举时序 oracle）、CVE-2019-13272（Linux ptrace suid）、CVE-2022-26691（CUPS 前缀匹配）
- **解析/资源语义**：CVE-2016-3714（ImageMagick ImageTragick 命令注入）、CVE-2016-1897（FFmpeg 任意文件读）、CVE-2022-1941（protobuf 递归深度绕过）
- **非终止/挂起**：CVE-2022-0778（OpenSSL BN_mod_sqrt 无限循环→超时 miss）

### 并发型（{by_primary.get('并发型',0)} 条）
- **跨线程 data race**：CVE-2016-8655（Linux AF_PACKET setsockopt race，tsan 在单 TU 重构下亦未触发）

### 配置依赖型（{by_primary.get('配置依赖型',0)} 条）
- **整数溢出子类未启用**：CVE-2018-13785（libpng height*rowbytes）、CVE-2021-33909（Linux seq_file size_t 下溢）、CVE-2021-3490（Linux eBPF ALU32）、CVE-2012-2677（Boost pool 乘积溢出）
- **type punning / alignment 未启用**：CVE-2023-0286（OpenSSL X.400 联合体）、CVE-2021-30551（Chromium/V8 Map 混淆）、CVE-2020-16040（Chromium/V8 整数回绕假设）

### 语义复杂型（语境保真损失）（{by_primary.get('语义复杂型（语境保真损失）',0)} 条）
- **真实跨模块 OOB 重构损失**：CVE-2023-4911（glibc Looney Tunables）、CVE-2021-23017（nginx resolver CNAME 越界）、CVE-2022-0185（Linux legacy_parse_param）

### 环境依赖型（692 配对实验，跨样本）
- 同 OS 换编译器几乎无感（689：一致率 93.5%、Δ≤2pp）；换 **deployment profile** 是灾难性的：
  A5 566 帧 catch 60.07% → 24.74%（−35.34pp），真实靶场 110 catch 59.09% → 23.64%（−35.45pp）。
- 丢失的捕获里 200/340（A5）与 39/65（真实靶场）是同一工具在声明 profile 下**能抓到的真阳性**——
  静默退化的指纹是 `Δunknown = 0.00pp`（"没测"被写成"测了没中"）。

### 平台特定型（结构性）
- `wunsequenced`/`compile-time` 在 8 资产池中**恒 unknown**（本机 MinGW 不认 -Wunsequenced / 无本地检测器），对 OR 零贡献。
- `linker` 在真实靶场 110 条（均为单 TU 重构）上 **0 catch**——其触发面（ODR/多定义）缺失，属"资产适用面收窄"的坦白项。

## 诚实边界
- 一/二级分类为启发式归纳；环境依赖型与平台特定型是**跨样本/结构性**失败模式，不以单条案例计数。
- 不声称"找到所有失败模式"——仅声明"在 110 条样本中观察到上述 N 种模式"。
"""
    with open(os.path.join(DATA, "705_failure_mode_taxonomy.md"), "w", encoding="utf-8") as f:
        f.write(taxonomy)

    # ---------- statistics.md ----------
    hardest = max(by_primary, key=by_primary.get)
    stats = f"""# 705-B · 失败模式统计

## 1. 各一级模式样本数（110 条真实缺陷中的 miss，共 {n_miss} 条）

| 一级模式 | 样本数 | 占 miss 比 | 备注 |
|---|---:|---:|---|
"""
    for pm, c in sorted(by_primary.items(), key=lambda x: -x[1]):
        stats += f"| {pm} | {c} | {c*100.0/n_miss:.1f}% | — |\n"
    stats += f"""
## 2. 按缺陷类型的 miss 分布

| defect_type | miss 数 | 该类型在 110 中 n | 该类型 OR 检出率 |
|---|---:|---:|---:|
"""
    # 该类型 n 与 OR 来自 683 报告 §1.2
    type_n = {"out_of_bounds": 38, "logic_error": 31, "integer_overflow": 14,
              "use_after_free": 10, "null_pointer_deref": 6, "data_race": 4,
              "type_punning": 4, "double_free": 2, "memory_leak": 1}
    type_or = {"out_of_bounds": "84.21%", "logic_error": "3.23%", "integer_overflow": "71.43%",
               "use_after_free": "100.0%", "null_pointer_deref": "100.0%", "data_race": "75.0%",
               "type_punning": "0.0%", "double_free": "100.0%", "memory_leak": "100.0%"}
    for dt, c in sorted(by_type.items(), key=lambda x: -x[1]):
        stats += f"| {dt} | {c} | {type_n.get(dt,'?')} | {type_or.get(dt,'?')} |\n"

    stats += f"""
## 3. 哪种模式最常见
- **逻辑型** 以 {by_primary.get('逻辑型',0)} 条居首（占 miss 的 {by_primary.get('逻辑型',0)*100.0/n_miss:.1f}%），是真实缺陷漏检的主因。
  这与合成语料（676g）形成对照：合成语料缺陷被设计为"检测器可观测"，故逻辑类占比极低；
  真实缺陷不受此先验约束，逻辑/协议错误占比高 → 这是**分布差异**，不是"检测器在真实场景退化"。

## 4. 哪种模式最难检测
- **按 OR 检出率**：type_punning 0.0%、logic_error 3.23%（683 §1.2）——这两类在 8 资产口径下几乎不可检。
- **按结构**：环境依赖型最"致命"——它不是单条缺陷难检，而是**整组测量在换 profile 后失效**
  （692：−35pp 且 60% 捕获丢失，且 `conditional_recall` 在 aware 口径下不可计算）。

## 5. 互补性对照（独苗命中）
- 110 条 catch 中 **{n_unique}** 条为独苗命中（占 catch 41.5%），单资产预算下必漏：
  asan {sole.get('asan',0)} / cross-compile {sole.get('cross-compile',0)} / tsan {sole.get('tsan',0)} / ubsan {sole.get('ubsan',0)}。
- 结论：没有单一资产足够；OR 组合的价值由这些样本直接支撑（与 682 Shapley 一致）。
"""
    with open(os.path.join(DATA, "705_failure_mode_statistics.md"), "w", encoding="utf-8") as f:
        f.write(stats)

    # ---------- capability_boundary_map.md ----------
    pas = m["per_asset_summary"]
    cap = f"""# 705-B · 检测器能力边界地图（Capability Boundary Map）

> 8 资产在 110 条真实缺陷上的逐资产表现（683 冻结矩阵）。`wunsequenced`/`compile-time` 结构性恒 unknown，
> 不进 OR 分母、不当 miss。

## 逐资产能力边界

| 资产 | catch | miss | unknown | catch% | 能抓什么 | 抓不到什么 |
|---|---:|---:|---:|---:|---|---|
| asan | {pas['asan']['catch']} | {pas['asan']['miss']} | {pas['asan']['unknown']} | {pas['asan']['catch_rate_pct']:.2f}% | 堆/栈溢出、UAF、double-free、leak（内存动作） | 逻辑/协议语义、UB 非内存类、并发 race |
| ubsan | {pas['ubsan']['catch']} | {pas['ubsan']['miss']} | {pas['ubsan']['unknown']} | {pas['ubsan']['catch_rate_pct']:.2f}% | 有符号整数溢出等 runtime error | 无符号回绕（默认关）、内存越界、逻辑 |
| tsan | {pas['tsan']['catch']} | {pas['tsan']['miss']} | {pas['tsan']['unknown']} | {pas['tsan']['catch_rate_pct']:.2f}% | data race / 并发语义 | 单 TU 重构难复现的真实跨模块 race、逻辑 |
| compiler-warn | {pas['compiler-warn']['catch']} | {pas['compiler-warn']['miss']} | {pas['compiler-warn']['unknown']} | {pas['compiler-warn']['catch_rate_pct']:.2f}% | 警告级诊断（极少） | 绝大多数内存/UB/逻辑 |
| cross-compile | {pas['cross-compile']['catch']} | {pas['cross-compile']['miss']} | {pas['cross-compile']['unknown']} | {pas['cross-compile']['catch_rate_pct']:.2f}% | g++/clang++ 输出不一致暴露的 UB/ODR | 单编译器内一致的行为 |
| linker | {pas['linker']['catch']} | {pas['linker']['miss']} | {pas['linker']['unknown']} | {pas['linker']['catch_rate_pct']:.2f}% | 多 TU ODR/多定义（真实靶场 0 触发面） | 单 TU 重构样本（全 110 条） |
| wunsequenced | {pas['wunsequenced']['catch']} | {pas['wunsequenced']['miss']} | {pas['wunsequenced']['unknown']} | {pas['wunsequenced']['catch_rate_pct']:.2f}% | （本机不可用） | 全部 |
| compile-time | {pas['compile-time']['catch']} | {pas['compile-time']['miss']} | {pas['compile-time']['unknown']} | {pas['compile-time']['catch_rate_pct']:.2f}% | （无本地检测器） | 全部 |

## 资产互补性（独苗命中案例）
- **asan 独苗**（典型）：CVE-2014-0160（Heartbleed）、CVE-2021-3711（OpenSSL SM2）、CVE-2023-6246（glibc vsyslog）
- **tsan 独苗**（并发）：CVE-2024-6387（regreSSHion）、CVE-2016-5195（Dirty COW）、CVE-2022-31747（Firefox WebRTC）
- **ubsan 独苗**（UB）：CVE-2022-35737（SQLite printf 溢出）、CVE-2021-46143（expat DTD 组溢出）
- **cross-compile 独苗**（编译器分歧）：CVE-2022-4450（OpenSSL double-free）、CVE-2022-23308（libxml2 UAF）、CVE-2021-30663（WebKit 整数溢出）

## 能力边界的三条结论
1. **语义不可观测区**：逻辑/协议/状态机错误（logic_error 族 OR 3.23%）超出 8 资产观测范围——需性质化测试/状态机建模。
2. **配置缺口区**：UB 子类（无符号回绕/alignment/strict-aliasing）默认未启用 → 可通过补开关修复，但会改变口径（本批冻结）。
3. **环境/平台门控区**：换 deployment profile 丢 35pp（692）；wunsequenced/compile-time/linker 受平台约束——资产可用性本身是测量 tuple 的坐标。

## 诚实边界
- 上述"能抓/抓不到"绑定"本 8 资产 + 本工具链（WSL g++13.3 + MinGW g++13.1/clang22.1）"口径，不外推。
- 加入 MSan/Valgrind 等会改变绝对值（683 §5 已声明）。
"""
    with open(os.path.join(DATA, "705_capability_boundary_map.md"), "w", encoding="utf-8") as f:
        f.write(cap)

    print(f"[done] miss={n_miss} 一级={by_primary}")


if __name__ == "__main__":
    main()
