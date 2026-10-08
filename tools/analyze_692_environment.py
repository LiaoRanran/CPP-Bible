#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""analyze_692_environment.py — 692-A：环境感知协议实验（只读冻结矩阵，不跑 detect）。

为什么有这篇
============
两轮外部评审把「WSL 依赖」从复现细节抬升为**科学发现**：

    省略环境信息的测量协议，会让**不完整测量冒充有效测量**。

689 已经把三组件指标（catch_rate / unknown_rate / conditional_recall）算出来，
但仍停在「单一 profile 内报三组件」。692 要补的是**协议层的形式化 + 配对实验**：

1. **EnvironmentProfile 形式化**（15 字段）与
   ``measurement_context_id = H(sample_hash, asset@version, env_profile, configuration, protocol)``
   —— 把「一条测量记录」的完整语境压成一个可对账的 id；
2. **E1 ↔ E2 配对（within-sample）**：同一 566 条 evaluation 样本上，
   E1 = WSL/Ubuntu + g++13.3（原测量环境，6 个可捕获资产），
   E2 = native Windows + MinGW（环境门控可用集 = compiler-warn/cross-compile/linker），
   两种记账各报三组件；
3. **静默退化演示**：对 6 资产的全部 63 个非空子集做「能力撤退」扫描，量化
   **guard 绿而测量已失效**的窗口 —— aggregate 几乎不变、但负例已不可信。

核心记号（本脚本全篇一致）
==========================
* ``P`` = 声明 profile；``S(P) ⊆ P`` = 环境实际支持的资产（capability closure）。
* **环境门控缺口** ``G = P \\ S(P)``。本项目的两个缺口性质必须分开：

  - **静态未实现**（``wunsequenced`` / ``compile-time``）：项目本来就没有实现，
    冻结矩阵里**逐资产**记 100% unknown ⇒ 两个 profile 一样，**不改结论**；
  - **环境门控**（``asan`` / ``ubsan`` / ``tsan``）：实现了，但需要 Linux 运行时
    ⇒ E1 有、E2 没有。它在 unaware 记账下被静默写成 ``miss``。

* 两种记账（同一份底层测量的两种**报告协议**）：

  - **unaware（静默退化）**：``G`` 直接当 ``miss`` ⇒ 报出的 catch_rate 假装是
    「这个工具在此环境下检出率就是它」；
  - **aware（感知协议）**：``G ≠ ∅`` ⇒ 未被支持的资产没被测过的样本，其负例记
    ``unknown``（absence of evidence），conditional_recall 在分母为 0 时**定义为不可计算**。

* **type-relevant 可信性**（探索性，能力图**从 derivation split 估、在 evaluation 上评**，
  避免用同一批数据既定义能力又评分）：族 ``g`` 的负例，若某个缺失资产在 derivation 上
  对 ``g`` 有非零捕获能力，则该负例标记为「不可信（unsound）」；否则记为「可信」。

只读上游
========
``data/a5_676f_detection_matrix.json``（1137 条，含 derivation/evaluation 两 split）、
``data/683_real_world_detection_matrix.json``（真实 110 条锚点）、
``data/688_reproducibility_quantification.json``（口径对照）。**不调用 detect()**。

确定性：无随机数；输出 ``data/692_environment_paired_experiment.json``。

用法
====
    python tools/analyze_692_environment.py
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from dataclasses import asdict, dataclass
from itertools import combinations
from math import comb, sqrt
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
A5_MATRIX = ROOT / "data" / "a5_676f_detection_matrix.json"
RW_MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
RW_QUANT = ROOT / "data" / "688_reproducibility_quantification.json"
OUT_JSON = ROOT / "data" / "692_environment_paired_experiment.json"

PROTOCOL_VERSION = "queyi-measurement-protocol/692"

#: 8 资产池（冻结矩阵口径）
ALL_ASSETS: tuple[str, ...] = (
    "asan", "ubsan", "tsan", "compiler-warn", "wunsequenced", "cross-compile", "linker", "compile-time",
)
#: 静态未实现资产：项目无实现 ⇒ 两个 profile 都记 asset-level unknown=100%（已知限制，不改结论）
STATIC_UNIMPLEMENTED: tuple[str, ...] = ("wunsequenced", "compile-time")
#: 环境门控资产 6 元集：E1 全支持；能力撤退扫描就在这 6 元集上做
ENV_GATED_ASSETS: tuple[str, ...] = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
#: native Windows（MinGW）实际支持的资产：688/689 口径
NATIVE_SUPPORTED: tuple[str, ...] = ("compiler-warn", "cross-compile", "linker")
#: 真实 110 条上 688 记录的锚点（交叉校验用；不一致即 blast）
ANCHOR_RW_FULL_CATCH = 65
ANCHOR_RW_NATIVE_CATCH = 26

#: 预声明窗口阈值（先于扫描写死，见 data/692_environment_report.md §4）
WINDOW_RETENTION_PCT = 95.0


# --------------------------------------------------------------------------------------
# 1. EnvironmentProfile 形式化
# --------------------------------------------------------------------------------------
@dataclass(frozen=True)
class EnvironmentProfile:
    """一次测量的**环境语境**（15 字段）。字段即协议的一部分：缺一即为不完整测量。"""

    profile_id: str
    os: str
    kernel: str
    architecture: str
    compiler: str
    compiler_version: str
    stdlib: str
    libc: str
    sanitizer_runtime: str
    linker: str
    optimization: tuple[str, ...]
    compile_flags: str
    runtime_flags: str
    timeout_s: int
    resource_limits: str
    container_image: str | None
    #: 该 profile 下**环境支持**的资产（capability closure 的右半）
    supported_assets: tuple[str, ...]
    #: 指纹来源（可复核命令），不是装饰
    provenance: str


E1_WSL_GCC = EnvironmentProfile(
    profile_id="wsl-gcc-13.3",
    os="Ubuntu 24.04.4 LTS (WSL2)",
    kernel="6.18.33.2-microsoft-standard-WSL2",
    architecture="x86_64",
    compiler="g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1)",
    compiler_version="13.3.0",
    stdlib="libstdc++ (GCC 13.3)",
    libc="glibc 2.39-0ubuntu8.9",
    sanitizer_runtime="libasan.so/libubsan.so/libtsan.so (GCC 13, /usr/lib/gcc/x86_64-linux-gnu/13/)",
    linker="GNU ld (GNU Binutils for Ubuntu) 2.42",
    optimization=("-O0", "-O2"),
    compile_flags="-std=c++17 -g -fsanitize=<asset> -fno-omit-frame-pointer",
    runtime_flags="ASAN_OPTIONS / UBSAN_OPTIONS / TSAN_OPTIONS（688 记录档位）",
    timeout_s=60,
    resource_limits="未设硬限（进程内超时 60s）",
    container_image=None,
    supported_assets=ENV_GATED_ASSETS,
    provenance="wsl -d Ubuntu -- bash -c 'uname -r; g++ --version; ldd --version; ld --version'",
)

E2_WIN_MINGW = EnvironmentProfile(
    profile_id="windows-native-mingw",
    os="Windows 11 (10.0.26200)",
    kernel="NT 10.0.26200",
    architecture="x86_64 (AMD64)",
    compiler="g++ (MinGW-Builds x86_64-posix-seh-rev1) + clang 22.1.8 (MSYS2 mingw64)",
    compiler_version="13.1.0 / 22.1.8",
    stdlib="libstdc++ (MinGW 13.1.0)",
    libc="msvcrt（target x86_64-w64-mingw32）",
    sanitizer_runtime="无（MinGW 不带 ASan 动态运行时；clang 缺 libclang_rt.asan_dynamic，689 已实测登记）",
    linker="GNU ld (MinGW binutils)",
    optimization=("-O0", "-O2"),
    compile_flags="-std=c++17 -Wall（本地可捕获资产口径）",
    runtime_flags="不适用（无 sanitizer 运行时）",
    timeout_s=60,
    resource_limits="未设硬限（进程内超时 60s）",
    container_image=None,
    supported_assets=NATIVE_SUPPORTED,
    provenance="python platform + g++ -v + clang -print-target-triple（本机实测）",
)

PROFILES: tuple[EnvironmentProfile, ...] = (E1_WSL_GCC, E2_WIN_MINGW)


def profile_payload(profile: EnvironmentProfile) -> dict[str, Any]:
    """用于哈希的规范化载荷：去掉 profile_id/supported_assets/provenance 之外的元数据仍保留。"""
    d = asdict(profile)
    d["optimization"] = list(d["optimization"])
    d["supported_assets"] = list(d["supported_assets"])
    return d


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def measurement_context_id(
    sample_hash: str,
    asset_id: str,
    asset_version: str,
    profile: EnvironmentProfile,
    configuration: dict[str, Any],
) -> str:
    """``mc1_`` + sha256(canonical(sample_hash, asset@version, profile, configuration, protocol))[:32]。

    语义：**同 id ⇒ 同一条测量记录**。任一字段变化（换环境、换档位、换协议版本、
    换样本字节）⇒ id 变化 ⇒ 旧结论对新语境**不继承**。
    """
    payload = {
        "sample_hash": sample_hash,
        "asset": f"{asset_id}@{asset_version}",
        "environment_profile": profile_payload(profile),
        "configuration": configuration,
        "protocol_version": PROTOCOL_VERSION,
    }
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()
    return "mc1_" + digest[:32]


# --------------------------------------------------------------------------------------
# 2. 冻结矩阵读取（只读）
# --------------------------------------------------------------------------------------
def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell)


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path} 顶层不是 JSON 对象")
    return data


def _load_a5() -> dict[str, Any]:
    return _load_json(A5_MATRIX)


def _load_rw() -> dict[str, Any]:
    return _load_json(RW_MATRIX)


def triple(verdicts: list[str]) -> dict[str, Any]:
    catch = verdicts.count("catch")
    miss = verdicts.count("miss")
    unknown = verdicts.count("unknown")
    total = len(verdicts)
    denom = catch + miss
    return {
        "catch": catch,
        "miss": miss,
        "unknown": unknown,
        "total": total,
        "catch_rate_pct": _pct(catch, total),
        "unknown_rate_pct": _pct(unknown, total),
        "conditional_recall_pct": _pct(catch, denom),
    }


def _pct(k: int, n: int) -> float | None:
    return round(k / n * 100.0, 4) if n else None


def or_verdict(per_asset: dict[str, Any], assets: tuple[str, ...], *, aware: bool) -> str:
    """OR 口径（冻结矩阵逐字口径）+ 一条 692 追加的协议规则。

    标准 OR（与 ``a5_676f_detection_matrix.json``/689 逐字一致）：任一 catch ⇒ catch；
    在**给定资产集内部**全部 unknown ⇒ unknown；其余 miss。

    ``aware=True`` 追加的那条规则：若该 profile **声明了但环境不支持**的环境门控资产
    （``ENV_GATED_ASSETS \\ assets`` 非空），则未被支持的资产没测过的样本，其负例记
    ``unknown``（absence of evidence）而不是 ``miss``（evidence of absence）。

    注意：``wunsequenced``/``compile-time`` 是**静态未实现**资产（项目无实现，两 profile
    同等缺），按 689/676f 口径保留在资产级 unknown，不触发本条规则 —— 否则连 E1 都会
    被判为「不可信」，那是把两类不同的缺口混为一谈。
    """
    vs = [_verdict(per_asset.get(a, "unknown")) for a in assets]
    if "catch" in vs:
        return "catch"
    if aware and any(a not in assets for a in ENV_GATED_ASSETS):
        return "unknown"
    if all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def _paired_stats(e1: list[str], e2: list[str]) -> dict[str, Any]:
    """配对 McNemar（精确二项）：b = E1 catch 且 E2 非 catch；c = E2 catch 且 E1 非 catch。"""
    b = sum(1 for x, y in zip(e1, e2) if x == "catch" and y != "catch")
    c = sum(1 for x, y in zip(e1, e2) if y == "catch" and x != "catch")
    n = len(e1)
    disc = b + c
    if disc == 0:
        p = 1.0
    else:
        k = min(b, c)
        tail = sum(comb(disc, i) for i in range(0, k + 1)) / (2 ** disc)
        p = min(1.0, 2.0 * tail)
    # 配对比例差的 Wald 区间（Δcatch_rate）
    delta = (e1.count("catch") - e2.count("catch")) / n if n else 0.0
    if n:
        var = (disc - (b - c) ** 2 / n) / (n * n)
        se = sqrt(var) if var > 0 else 0.0
    else:
        se = 0.0
    return {
        "b_e1_catch_only": b,
        "c_e2_catch_only": c,
        "discordant": disc,
        "mcnemar_exact_p": p,
        "log10_p": (round(_log10(p), 2) if p > 0 else None),
        "delta_catch_rate_pp": round(delta * 100.0, 4),
        "delta_ci95_pp_wald": [round((delta - 1.96 * se) * 100.0, 4), round((delta + 1.96 * se) * 100.0, 4)],
        "ci_note": "配对比例差 Wald（正态近似）区间；p 为精确二项 McNemar",
    }


def _log10(x: float) -> float:
    from math import log10

    return log10(x) if x > 0 else float("-inf")


# --------------------------------------------------------------------------------------
# 3. 配对实验（E1 vs E2），两个样本框架
# --------------------------------------------------------------------------------------
def paired_experiment(samples: list[dict[str, Any]], frame: str) -> dict[str, Any]:
    e1: list[str] = []
    e2_unaware: list[str] = []
    e2_aware: list[str] = []
    for s in samples:
        pa = s["per_asset"]
        e1.append(or_verdict(pa, ENV_GATED_ASSETS, aware=False))
        e2_unaware.append(or_verdict(pa, NATIVE_SUPPORTED, aware=False))
        e2_aware.append(or_verdict(pa, NATIVE_SUPPORTED, aware=True))

    t1 = triple(e1)
    t2u = triple(e2_unaware)
    t2a = triple(e2_aware)

    lost = [s for s, x, y in zip(samples, e1, e2_unaware) if x == "catch" and y != "catch"]
    gained = [s for s, x, y in zip(samples, e1, e2_unaware) if y == "catch" and x != "catch"]
    # E2 报出的「负例」里，有多少其实是 E1 抓到的真阳性（静默把检出写成未检出）
    e2_neg = [s for s, y in zip(samples, e2_unaware) if y != "catch"]
    poisoned = [s for s in e2_neg if or_verdict(s["per_asset"], ENV_GATED_ASSETS, aware=False) == "catch"]

    def _group_count(rows: list[dict[str, Any]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in rows:
            g = str(r.get("defect_group", "unknown"))
            out[g] = out.get(g, 0) + 1
        return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))

    def _asset_sole(rows: list[dict[str, Any]]) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in rows:
            cs = [a for a in ENV_GATED_ASSETS if _verdict(r["per_asset"].get(a, "unknown")) == "catch"]
            if len(cs) == 1:
                out[cs[0]] = out.get(cs[0], 0) + 1
        return dict(sorted(out.items(), key=lambda kv: (-kv[1], kv[0])))

    return {
        "frame": frame,
        "n": len(samples),
        "E1_wsl_full": t1,
        "E2_native_unaware": t2u,
        "E2_native_aware": t2a,
        "delta": {
            "delta_catch_rate_pp_unaware": round((t1["catch_rate_pct"] or 0.0) - (t2u["catch_rate_pct"] or 0.0), 4),
            "delta_unknown_rate_pp_unaware": round((t1["unknown_rate_pct"] or 0.0) - (t2u["unknown_rate_pct"] or 0.0), 4),
            "delta_conditional_recall_pp_unaware": round(
                (t1["conditional_recall_pct"] or 0.0) - (t2u["conditional_recall_pct"] or 0.0), 4
            ),
            "delta_unknown_rate_pp_aware": round((t1["unknown_rate_pct"] or 0.0) - (t2a["unknown_rate_pct"] or 0.0), 4),
            "delta_conditional_recall_aware": "undefined（aware 口径下 E2 无可信负例 ⇒ 分母 0）",
        },
        "mcnemar": _paired_stats(e1, e2_unaware),
        "silent_false_miss": {
            "lost_e1_catches": len(lost),
            "lost_e1_catches_pct_of_e1_catch": _pct(len(lost), t1["catch"]),
            "lost_e1_catches_by_asset_sole": _asset_sole(lost),
            "lost_e1_catches_by_group": _group_count(lost),
            "gained_e2_catches": len(gained),
            "e2_reported_negatives": len(e2_neg),
            "e2_reported_negatives_that_e1_catches": len(poisoned),
            "poisoned_share_of_e2_negatives_pct": _pct(len(poisoned), len(e2_neg)),
        },
        "per_asset_E1": {
            a: triple([_verdict(s["per_asset"].get(a, "unknown")) for s in samples]) for a in ALL_ASSETS
        },
        "per_asset_E2_supported": {
            a: triple([_verdict(s["per_asset"].get(a, "unknown")) for s in samples]) for a in NATIVE_SUPPORTED
        },
        "per_asset_E2_missing": {
            a: {
                "declared": True,
                "supported": False,
                "measured": False,
                "verdict": "unknown",
                "unknown_rate_pct": 100.0,
                "note": "环境门控缺口：该资产在 E2 未运行 ⇒ 逐样本无测量记录（不是 miss）",
            }
            for a in ENV_GATED_ASSETS
            if a not in NATIVE_SUPPORTED
        },
    }


# --------------------------------------------------------------------------------------
# 4. 静默退化扫描（能力撤退）：63 个非空资产子集
# --------------------------------------------------------------------------------------
def capability_map(derivation: list[dict[str, Any]]) -> dict[str, set[str]]:
    """族 → 在其上有非零捕获能力的资产集（**从 derivation split 估**，在 evaluation 上评）。"""
    out: dict[str, set[str]] = {}
    for s in derivation:
        g = str(s.get("defect_group", "unknown"))
        out.setdefault(g, set())
        for a in ALL_ASSETS:
            if _verdict(s["per_asset"].get(a, "unknown")) == "catch":
                out[g].add(a)
    return out


def degradation_sweep(evaluation: list[dict[str, Any]], cap: dict[str, set[str]], full_rate: float) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    n = len(evaluation)
    for k in range(1, len(ENV_GATED_ASSETS) + 1):
        for subset in combinations(ENV_GATED_ASSETS, k):
            avail = set(subset)
            catch = 0
            sound_neg = 0
            unsound_neg = 0
            for s in evaluation:
                if any(_verdict(s["per_asset"].get(a, "unknown")) == "catch" for a in avail):
                    catch += 1
                    continue
                g = str(s.get("defect_group", "unknown"))
                missing_capable = (cap.get(g, set()) - avail) & set(ENV_GATED_ASSETS)
                if missing_capable:
                    unsound_neg += 1
                else:
                    sound_neg += 1
            rate = _pct(catch, n) or 0.0
            denom = sound_neg + unsound_neg
            rows.append({
                "available_assets": list(subset),
                "n_missing": len(ENV_GATED_ASSETS) - k,
                "missing_assets": [a for a in ENV_GATED_ASSETS if a not in avail],
                "unaware_catch_rate_pct": rate,
                "retention_of_full_pct": round(rate / full_rate * 100.0, 4) if full_rate else None,
                "aware_miss": 0,
                "aware_unknown": unsound_neg,
                "sound_negatives": sound_neg,
                "unsound_negatives": unsound_neg,
                "type_relevant_soundness_pct": _pct(sound_neg, denom),
                "aware_conditional_recall_pct": _pct(catch, catch + sound_neg),
            })
    # 预声明窗口：aggregate 几乎不变（retention ≥ 95%）但负例已不可信
    def _window(thr: float) -> list[dict[str, Any]]:
        return [r for r in rows if (r["retention_of_full_pct"] or 0.0) >= thr and r["unsound_negatives"] > 0]

    window = _window(WINDOW_RETENTION_PCT)
    with_unsound = [r for r in rows if r["unsound_negatives"] > 0]
    widest = max(with_unsound, key=lambda r: r["retention_of_full_pct"] or 0.0) if with_unsound else None
    full6_ok = [r for r in rows if r["n_missing"] == 0]
    return {
        "grid": "ENV_GATED_ASSETS 的全部 63 个非空子集（能力撤退阶梯）",
        "window_rule": f"retention_of_full_pct ≥ {WINDOW_RETENTION_PCT} 且 unsound_negatives > 0",
        "n_configs": len(rows),
        "n_window_configs": len(window),
        "window_by_threshold": {f"{t}_pct": len(_window(float(t))) for t in (100, 99, 95, 90, 80, 50)},
        "n_configs_with_unsound_negatives": len(with_unsound),
        "widest_window_config": widest,
        "single_drop_rows": [r for r in rows if r["n_missing"] == 1],
        "single_remaining_rows": [r for r in rows if r["n_missing"] == len(ENV_GATED_ASSETS) - 1],
        "full_capability_rows": full6_ok,
        "rows": rows,
        "capability_map_from_derivation": {g: sorted(v) for g, v in sorted(cap.items())},
    }


def silent_number_demo(evaluation: list[dict[str, Any]]) -> dict[str, Any]:
    """一个具体的最小退化：撤掉 ``compiler-warn``（静态资产，单资产贡献最小的一档）。

    目的：给读者一个「aggregate 几乎看不出、负例可信性已经掉」的最小可复述例子。
    """
    n = len(evaluation)
    keep = tuple(a for a in ENV_GATED_ASSETS if a != "compiler-warn")
    catch_keep = 0
    only_cw = 0
    for s in evaluation:
        if any(_verdict(s["per_asset"].get(a, "unknown")) == "catch" for a in keep):
            catch_keep += 1
        elif _verdict(s["per_asset"].get("compiler-warn", "unknown")) == "catch":
            only_cw += 1
    full = sum(
        1 for s in evaluation if any(_verdict(s["per_asset"].get(a, "unknown")) == "catch" for a in ENV_GATED_ASSETS)
    )
    return {
        "dropped_asset": "compiler-warn",
        "n": n,
        "unaware_catch_full_pct": _pct(full, n),
        "unaware_catch_dropped_pct": _pct(catch_keep, n),
        "delta_pp": round((_pct(full, n) or 0.0) - (_pct(catch_keep, n) or 0.0), 4),
        "samples_lost": only_cw,
        "aware_unknown_pct": _pct(n - catch_keep, n),
        "aware_conditional_recall": "undefined（无可信负例）",
    }


# --------------------------------------------------------------------------------------
# 5. measurement_context_id 样例
# --------------------------------------------------------------------------------------
def context_id_examples(samples: list[dict[str, Any]]) -> dict[str, Any]:
    sample = samples[0]
    sample_hash = hashlib.sha256(canonical_json(sample.get("sample_id", "unknown")).encode()).hexdigest()
    cfg = {
        "optimization": "-O2",
        "checks": "default",
        "timeout_s": 60,
        "flags": "-std=c++17 -g -fsanitize=address",
    }
    out: dict[str, Any] = {
        "algorithm": "mc1_ = sha256(canonical_json{sample_hash, asset@version, environment_profile, configuration, protocol_version})[:32]",
        "sample_used": sample.get("sample_id"),
        "sample_hash": sample_hash,
        "ids": {
            p.profile_id: measurement_context_id(sample_hash, "asan", "gcc-13", p, cfg) for p in PROFILES
        },
    }
    # 同 profile、同资产、只换优化档 ⇒ id 必须变
    cfg2 = dict(cfg)
    cfg2["optimization"] = "-O0"
    out["ids"]["wsl-gcc-13.3__O0"] = measurement_context_id(sample_hash, "asan", "gcc-13", E1_WSL_GCC, cfg2)
    out["ids"]["wsl-gcc-13.3__asan"] = out["ids"]["wsl-gcc-13.3"]
    out["invariants"] = {
        "same_context_same_id": out["ids"]["wsl-gcc-13.3__asan"] == out["ids"]["wsl-gcc-13.3"],
        "environment_change_changes_id": out["ids"]["wsl-gcc-13.3"] != out["ids"]["windows-native-mingw"],
        "configuration_change_changes_id": out["ids"]["wsl-gcc-13.3"] != out["ids"]["wsl-gcc-13.3__O0"],
    }
    return out


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------
def main() -> int:
    a5 = _load_a5()
    rw = _load_rw()
    quant = json.loads(RW_QUANT.read_text(encoding="utf-8"))

    samples = a5["samples"]
    evaluation = [s for s in samples if s.get("split") == "evaluation"]
    derivation = [s for s in samples if s.get("split") == "derivation"]

    frames: dict[str, Any] = {
        "A5_evaluation_566": paired_experiment(evaluation, "A5 holdout evaluation split (566)"),
        "A5_all_1137": paired_experiment(samples, "A5 full pool (1137)"),
        "A5_derivation_571": paired_experiment(derivation, "A5 derivation split (571)"),
    }
    rw_samples = list(rw["samples"])
    frames["real_world_110"] = paired_experiment(rw_samples, "real-world benchmark (110)")

    # 交叉校验：真实 110 上必须复现 688 的 65 / 26
    anchor = frames["real_world_110"]
    got_full = anchor["E1_wsl_full"]["catch"]
    got_native = anchor["E2_native_unaware"]["catch"]
    anchor_ok = got_full == ANCHOR_RW_FULL_CATCH and got_native == ANCHOR_RW_NATIVE_CATCH

    cap = capability_map(derivation)
    full_rate = frames["A5_evaluation_566"]["E1_wsl_full"]["catch_rate_pct"] or 0.0
    sweep = degradation_sweep(evaluation, cap, full_rate)
    demo = silent_number_demo(evaluation)

    out: dict[str, Any] = {
        "schema": "queyi-692/environment-paired-experiment/v1",
        "generated_by": "tools/analyze_692_environment.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "protocol_version": PROTOCOL_VERSION,
        "inputs": {
            "a5_matrix": "data/a5_676f_detection_matrix.json",
            "real_world_matrix": "data/683_real_world_detection_matrix.json",
            "anchor_688": "data/688_reproducibility_quantification.json",
            "detect_calls": 0,
        },
        "environment_profiles": {p.profile_id: profile_payload(p) for p in PROFILES},
        "asset_partition": {
            "all_assets": list(ALL_ASSETS),
            "env_gated_assets": list(ENV_GATED_ASSETS),
            "static_unimplemented": list(STATIC_UNIMPLEMENTED),
            "E1_supported": list(E1_WSL_GCC.supported_assets),
            "E2_supported": list(E2_WIN_MINGW.supported_assets),
            "E2_environment_gap": [a for a in ENV_GATED_ASSETS if a not in NATIVE_SUPPORTED],
        },
        "measurement_context_id": context_id_examples(samples),
        "frames": frames,
        "anchor_check_vs_688": {
            "expected_full_or_catch": ANCHOR_RW_FULL_CATCH,
            "recomputed_full_or_catch": got_full,
            "expected_native_or_catch": ANCHOR_RW_NATIVE_CATCH,
            "recomputed_native_or_catch": got_native,
            "quant_file_full_rate_pct": quant.get("full_rate"),
            "quant_file_native_rate_pct": quant.get("cross_platform_rate"),
            "pass": anchor_ok,
        },
        "silent_degradation": {
            "sweep": sweep,
            "minimal_demo": demo,
        },
        "reading_rules": [
            "E2 的 catch 是**实测**（3 个本地资产在 Windows 上真跑过）；E2 的「负例不可信」是**协议层判定**，不是对未运行资产的行为推断。",
            "aware 记账下 conditional_recall 分母为 0 ⇒ 按定义不可计算；任何把它写成 0% 或 100% 的做法都是口径错误。",
            "type-relevant 可信性用的是 derivation split 估计的能力图，属探索性指标，不作主结论。",
            "frames 之间的绝对率不可互相比较（不同样本框架）；只做同一 frame 内的 E1/E2 配对比较。",
        ],
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    fr = frames["A5_evaluation_566"]
    print("== 692-A 环境配对实验（A5 evaluation 566）==")
    print("E1 full   :", {k: fr["E1_wsl_full"][k] for k in ("catch", "miss", "unknown", "catch_rate_pct", "conditional_recall_pct")})
    print("E2 unaware:", {k: fr["E2_native_unaware"][k] for k in ("catch", "miss", "unknown", "catch_rate_pct")})
    print("E2 aware  :", {k: fr["E2_native_aware"][k] for k in ("catch", "miss", "unknown", "unknown_rate_pct")})
    print("delta     :", fr["delta"])
    print("silent    :", {k: fr["silent_false_miss"][k] for k in (
        "lost_e1_catches", "lost_e1_catches_pct_of_e1_catch", "e2_reported_negatives",
        "e2_reported_negatives_that_e1_catches", "poisoned_share_of_e2_negatives_pct")})
    print("mcnemar   :", fr["mcnemar"])
    print("anchor    :", out["anchor_check_vs_688"]["pass"], got_full, got_native)
    print("sweep     :", sweep["n_configs"], "configs |", sweep["n_window_configs"], "in window")
    print("minimal   :", demo)
    print("wrote", OUT_JSON)
    return 0 if anchor_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
