#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""check_split_670c.py — 670c C4：拆分完整性检查（CPP-Bible ↔ queyi-verifier）。

为什么要这个检查
================
660 B6 / 666 把「协议内核」迁到了 queyi-verifier，CPP-Bible 侧只留薄 wrapper。
但拆分**不是一层**，670c 实测发现两种形态并存：

  · 内核层（queyi_core_*.py ×7 + queyi_data_models_645.py）
      CPP-Bible = 约 2.7KB 的薄 wrapper，运行期用 importlib 找
      queyi-verifier/tools/<同名文件>，再把 sys.modules[__name__] 换成 canonical。
      ⇒ 单一实现、两处入口。这是**拆分完成的**部分。

  · 判决/变异层（gate_engine.py / verifier_closure_*.py / mutation_*.py）
      两侧都是**完整实现**、且逐字节相同（例如 gate_engine.py 两侧都是 217834 B）。
      ⇒ 这是**复制**而非拆分；647 方案 §六 把"是否合并"明确留交人裁决，
         所以本工具把它记作 WARN（已知债务），而不是 FAIL。

本工具检查的就是这两条真实不变式，外加最要命的一条：
  **复制层不允许漂移** —— 两侧同名字节不同 ⇒ FAIL（说明有人在一边改了核心却没同步）。

诚实边界
========
* 不修改任何文件，只读。
* 找不到 queyi-verifier（例如 CI 只 checkout 了主仓）⇒ 相关检查记 SKIP，
  退出码 0，并明确打印"未检查"，绝不假装通过。
* 不把"复制层存在"判成失败：那是人的决策，不是机器的。

用法
====
    python tools/check_split_670c.py            # 人读
    python tools/check_split_670c.py --json     # 机读
    python tools/check_split_670c.py --verbose  # 打印每个文件
退出码：0 = 无 FAIL（WARN/SKIP 也算通过）；1 = 有 FAIL。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

# 应当是「薄 wrapper」的层（拆分已完成）
KERNEL_PATTERNS = ("queyi_core_*.py", "queyi_data_models_*.py")
# 两侧都是完整实现、且当前逐字节相同的层（已知债务，647 §六）
DUP_PATTERNS = ("gate_engine.py", "verifier_closure_*.py", "mutation_*.py")

WRAPPER_SIZE_MAX = 12000  # 薄 wrapper 的体积上限（实测约 2.7KB）
CANONICAL_MARK = "queyi-verifier"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def find_verifier(start: Path | None = None, max_up: int = 8) -> Path | None:
    """从 start 逐级向上找 <dir>/queyi-verifier/tools，返回 verifier 根目录。"""
    d = (start or ROOT).resolve()
    for _ in range(max_up):
        cand = d / "queyi-verifier"
        if (cand / "tools").is_dir():
            return cand
        parent = d.parent
        if parent == d:
            break
        d = parent
    return None


def classify(path: Path) -> str:
    """判断 CPP-Bible 侧某文件是薄 wrapper 还是完整实现。"""
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "UNREADABLE"
    if (CANONICAL_MARK in txt) and ("importlib" in txt) and (path.stat().st_size < WRAPPER_SIZE_MAX):
        return "WRAPPER"
    return "FULL-IMPL"


def _collect(root: Path, patterns) -> list[Path]:
    out: list[Path] = []
    for pat in patterns:
        out.extend(sorted((root / "tools").glob(pat)))
    return out


def check_kernel_wrappers(verbose: bool = False) -> dict:
    """内核层在 CPP-Bible 侧必须全是薄 wrapper。"""
    files = _collect(ROOT, KERNEL_PATTERNS)
    if not files:
        return {"check": "kernel_is_wrapper", "status": "FAIL",
                "detail": "CPP-Bible/tools 下找不到任何内核文件（queyi_core_*/queyi_data_models_*）"}
    bad = []
    for f in files:
        kind = classify(f)
        if verbose:
            print("    %-42s %s (%dB)" % (f.name, kind, f.stat().st_size))
        if kind != "WRAPPER":
            bad.append(f.name)
    if bad:
        return {"check": "kernel_is_wrapper", "status": "FAIL",
                "detail": "以下内核文件不是薄 wrapper（疑似把实现搬回了主仓）：" + ", ".join(bad),
                "files": len(files), "bad": bad}
    return {"check": "kernel_is_wrapper", "status": "PASS",
            "detail": "%d 个内核文件全部是薄 wrapper" % len(files), "files": len(files)}


def check_canonical_present(ver: Path | None, verbose: bool = False) -> dict:
    """每个 wrapper 在 verifier 侧都要有 canonical（且比 wrapper 大）。"""
    if ver is None:
        return {"check": "canonical_present", "status": "SKIP", "detail": "未找到 queyi-verifier"}
    missing, ok = [], 0
    for f in _collect(ROOT, KERNEL_PATTERNS):
        canon = ver / "tools" / f.name
        if not canon.is_file():
            missing.append(f.name)
        elif canon.stat().st_size <= f.stat().st_size:
            missing.append(f.name + "(canonical 不大于 wrapper)")
        else:
            ok += 1
    if missing:
        return {"check": "canonical_present", "status": "FAIL",
                "detail": "wrapper 找不到对应 canonical：" + ", ".join(missing)}
    return {"check": "canonical_present", "status": "PASS",
            "detail": "%d 个 wrapper 都有更大的 canonical" % ok, "resolved": ok}


def check_wrapper_resolves(ver: Path | None) -> dict:
    """真跑一次：import wrapper 后 __file__ 必须落在 queyi-verifier。"""
    if ver is None:
        return {"check": "wrapper_resolves", "status": "SKIP", "detail": "未找到 queyi-verifier"}
    kernels = _collect(ROOT, KERNEL_PATTERNS)
    if not kernels:
        return {"check": "wrapper_resolves", "status": "SKIP", "detail": "无内核文件可测"}
    name = kernels[0].stem
    code = ("import sys; sys.path.insert(0, r'%s'); import %s as m; print(m.__file__)"
            % (str(TOOLS), name))
    try:
        p = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return {"check": "wrapper_resolves", "status": "FAIL",
                "detail": "无法运行子进程解析 wrapper：%s" % e}
    out = (p.stdout or "").strip().splitlines()
    resolved = out[-1] if out else ""
    if p.returncode != 0:
        return {"check": "wrapper_resolves", "status": "FAIL",
                "detail": "import %s 失败（rc=%d）：%s" % (name, p.returncode, (p.stderr or "").strip()[-300:])}
    if CANONICAL_MARK not in resolved:
        return {"check": "wrapper_resolves", "status": "FAIL",
                "detail": "import %s 解析到 %s，未指向 queyi-verifier" % (name, resolved)}
    return {"check": "wrapper_resolves", "status": "PASS",
            "detail": "import %s -> %s" % (name, resolved), "resolved": resolved}


def check_verifier_self_sufficient(ver: Path | None, verbose: bool = False) -> dict:
    """verifier 侧必须自带：内核 / 数据模型 / 门禁引擎 / 变异工具。"""
    if ver is None:
        return {"check": "verifier_self_sufficient", "status": "SKIP", "detail": "未找到 queyi-verifier"}
    need = {
        "kernel": list((ver / "tools").glob("queyi_core_*.py")),
        "data_models": list((ver / "tools").glob("*data_models*.py")),
        "gate_engine": list((ver / "tools").glob("gate_engine*.py")),
        "mutation": list((ver / "tools").glob("mutation_*.py")),
    }
    counts = {k: len(v) for k, v in need.items()}
    empty = [k for k, v in counts.items() if v == 0]
    if verbose:
        for k, v in counts.items():
            print("    verifier %-12s %d 个" % (k, v))
    if empty:
        return {"check": "verifier_self_sufficient", "status": "FAIL",
                "detail": "verifier 缺少：" + ", ".join(empty), "counts": counts}
    has_conftest = (ver / "conftest.py").is_file()
    return {"check": "verifier_self_sufficient", "status": "PASS",
            "detail": "内核 %d / 数据模型 %d / 门禁引擎 %d / 变异 %d；自有 conftest=%s"
                      % (counts["kernel"], counts["data_models"], counts["gate_engine"],
                         counts["mutation"], has_conftest),
            "counts": counts, "own_conftest": has_conftest}


def check_duplication_drift(ver: Path | None, verbose: bool = False) -> dict:
    """复制层：两侧同名字节必须一致（漂移 = FAIL）；存在本身 = WARN（已知债务）。"""
    if ver is None:
        return {"check": "duplication_drift", "status": "SKIP", "detail": "未找到 queyi-verifier"}
    dup, drifted, only_main = [], [], []
    for f in _collect(ROOT, DUP_PATTERNS):
        canon = ver / "tools" / f.name
        if not canon.is_file():
            only_main.append(f.name)
            continue
        a, b = sha256_file(f), sha256_file(canon)
        if verbose:
            print("    %-42s %s" % (f.name, "same" if a == b else "DRIFT"))
        if a == b:
            dup.append(f.name)
        else:
            drifted.append(f.name)
    if drifted:
        return {"check": "duplication_drift", "status": "FAIL",
                "detail": "两侧复制体已漂移（改了核心没同步）：" + ", ".join(drifted),
                "drifted": drifted, "identical": len(dup)}
    return {"check": "duplication_drift", "status": "WARN" if dup else "PASS",
            "detail": ("%d 个文件两侧均为完整实现且逐字节相同（已知债务：拆分只做了内核层，"
                       "647 方案 §六 留交人裁决）；未检测到漂移" % len(dup)) if dup else "无复制层文件",
            "identical": len(dup), "only_in_main": only_main}


CHECKS = ("kernel_is_wrapper", "canonical_present", "wrapper_resolves",
          "verifier_self_sufficient", "duplication_drift")


def run_all(verbose: bool = False) -> dict:
    ver = find_verifier()
    results = [
        check_kernel_wrappers(verbose),
        check_canonical_present(ver, verbose),
        check_wrapper_resolves(ver),
        check_verifier_self_sufficient(ver, verbose),
        check_duplication_drift(ver, verbose),
    ]
    fails = [r for r in results if r["status"] == "FAIL"]
    return {
        "tool": "check_split_670c",
        "repo": str(ROOT),
        "verifier": str(ver) if ver else None,
        "results": results,
        "fails": len(fails),
        "warns": len([r for r in results if r["status"] == "WARN"]),
        "skips": len([r for r in results if r["status"] == "SKIP"]),
        "overall": "FAIL" if fails else "PASS",
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="670c C4 拆分完整性检查（只读）")
    ap.add_argument("--json", action="store_true", help="输出机读 JSON")
    ap.add_argument("--verbose", action="store_true", help="打印每个文件")
    args = ap.parse_args(argv)

    rep = run_all(args.verbose)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print("[check_split_670c] CPP-Bible = %s" % rep["repo"])
        print("[check_split_670c] verifier  = %s" % (rep["verifier"] or "未找到（相关检查 SKIP）"))
        for r in rep["results"]:
            print("  %-6s %-26s %s" % (r["status"], r["check"], r["detail"]))
        print("[check_split_670c] overall=%s  FAIL=%d WARN=%d SKIP=%d"
              % (rep["overall"], rep["fails"], rep["warns"], rep["skips"]))
    return 1 if rep["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
