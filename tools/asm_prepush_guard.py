#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asm_prepush_guard.py — Examples/*.asm 证据库完整性预推送守卫。

《现代 C++ 终极圣经》的汇编证据库（Examples/*.asm）是 MinGW GCC 15.3.0 生成
的，CI (Ubuntu gcc-15) 无法复现 MinGW 调用约定（seh_proc/def/__main vs
CFI/AT&T/SysV），故汇编证据的"真实性"只能在本地（Windows + MinGW）验证。

本工具是 pre-push 自检守卫：调用 asm_repro_spotcheck.py 对证据库做对抗式审计，
判定标准为「存储 asm 的用户函数符号集合 ⊆ 重编产物」——即书内展示的汇编片段
仍能在当前工具链下复现，不存在"伪证据"（编造的汇编）或"版本漂移"（旧版 GCC
产物已过时）。

退出码语义（pre-push 阻断条件）：
  0 = PASS（全量 MATCH 或仅有 NO_SOURCE/FORMAT_SKIP 的策展噪声）
  1 = DRIFT（存在汇编漂移 — 用户函数符号在重编后消失或改变）
  2 = COMPILE_FAIL（源码无法用当前 GCC 重编 — 源码演进或编译标志过时）

用法:
  python tools/asm_prepush_guard.py                    # 全量审计
  python tools/asm_prepush_guard.py --only 15.3.0      # 仅审 15.3.0 产物
  python tools/asm_prepush_guard.py --name-substr ch27  # 仅审含 ch27 的文件

集成建议（写进 .git/hooks/pre-push 或 AGENT.md 开发流程）:
  在推送任何涉及 Book/ 正文汇编围栏或 Examples/*.asm 的改动前，运行本守卫。
  CI（Ubuntu）已有 book_asm_freshness.py + verify_asm_evidence.py 做"围栏 vs
  工件"的符号一致性检查（跨平台），本工具补充"工件 vs 源码重编"的真实性检查
  （MinGW-only）。
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GPP_CANON = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"


def find_gpp():
    if os.path.isfile(GPP_CANON):
        return GPP_CANON
    for cand in ("g++",):
        from shutil import which
        p = which(cand)
        if p:
            return p
    return None


def main():
    ap = argparse.ArgumentParser(description="Examples/*.asm 预推送守卫")
    ap.add_argument("--gpp", default=None, help="MinGW g++.exe (默认自动探测)")
    ap.add_argument("--examples", default=str(ROOT / "Examples"))
    ap.add_argument("--only", default="all",
                    choices=["all", "15.3.0", "13.1.0", "unmarked"])
    ap.add_argument("--name-substr", default=None)
    ap.add_argument("--json", default=None, help="详细 JSON 报告输出路径")
    args = ap.parse_args()

    gpp = args.gpp or find_gpp()
    if not gpp:
        print("[FATAL] 找不到 g++。请用 --gpp 指定 MinGW g++.exe 路径。", file=sys.stderr)
        return 3

    if not Path(args.examples).is_dir():
        print(f"[FATAL] Examples 目录不存在: {args.examples}", file=sys.stderr)
        return 3

    report_json = args.json or str(HERE / "_prepush_asm_report.json")

    print(f"[*] ASM 预推送守卫")
    print(f"    工具链: {gpp}")
    print(f"    证据库: {args.examples}")
    print(f"    审计范围: {args.only}" + (f" (过滤: {args.name_substr})" if args.name_substr else ""))
    print()

    cmd = [
        sys.executable, str(HERE / "asm_repro_spotcheck.py"),
        "--gpp", gpp,
        "--examples", args.examples,
        "--out", report_json,
        "--only", args.only,
    ]
    if args.name_substr:
        cmd += ["--name-substr", args.name_substr]

    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    print(r.stdout)
    if r.stderr:
        print(r.stderr, file=sys.stderr)

    if r.returncode != 0:
        print(f"[ERROR] asm_repro_spotcheck 退出码 {r.returncode}", file=sys.stderr)
        return 3

    try:
        rep = json.load(open(report_json, encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] 无法读取报告 {report_json}: {e}", file=sys.stderr)
        return 3

    summary = rep.get("summary", {})
    n_match = summary.get("MATCH", 0)
    n_drift = summary.get("DRIFT", 0)
    n_cf = summary.get("COMPILE_FAIL", 0)
    n_ns = summary.get("NO_SOURCE", 0)
    n_fs = summary.get("FORMAT_SKIP", 0)
    total = sum(summary.values())

    print("=" * 60)
    print(f"ASM 证据库审计汇总: {total} 文件")
    print(f"  MATCH={n_match}  DRIFT={n_drift}  COMPILE_FAIL={n_cf}  "
          f"NO_SOURCE={n_ns}  FORMAT_SKIP={n_fs}")
    print("=" * 60)

    # 判定逻辑：区分基线内已知 DRIFT（WARN）与新增 DRIFT（FAIL）
    baseline_path = HERE / "asm_drift_baseline.json"
    known_drift = set()
    known_cf = set()
    if baseline_path.exists():
        try:
            bl = json.load(open(baseline_path, encoding="utf-8"))
            known_drift = {d["file"].replace(".asm", "")
                           for d in bl.get("known_drift", [])}
            known_cf = {d["file"].replace(".asm", "")
                        for d in bl.get("known_compile_fail", [])}
        except Exception:
            pass

    drift_items = [r for r in rep.get("results", []) if r["status"] == "DRIFT"]
    new_drifts = [d for d in drift_items if d["name"] not in known_drift]
    known_drifts_hit = [d for d in drift_items if d["name"] in known_drift]

    if new_drifts:
        print(f"\n[FAIL] 检测到 {len(new_drifts)} 个 *新增* 汇编漂移 (DRIFT)")
        print("  存储的 .asm 中用户函数符号在重编后消失或改变。")
        print("  可能原因: 源码演进后函数改名/删除，或 GCC 版本差异导致代码生成变化。")
        print("  修复: 用 asm_regen.py --apply 重新生成漂移文件，或手动核查。")
        for item in new_drifts[:10]:
            extra = f" (stored_lost={item.get('n_extra_stored',0)}, fresh_new={item.get('n_extra_fresh',0)})"
            print(f"    {item['name']}.asm  v{item.get('ver','?')}{extra}")
        if len(new_drifts) > 10:
            print(f"    ... 及其他 {len(new_drifts)-10} 个")
        if known_drifts_hit:
            print(f"\n  (另有 {len(known_drifts_hit)} 个基线已知 DRIFT，见 asm_drift_baseline.json)")
        return 1

    if known_drifts_hit:
        print(f"\n[WARN] {len(known_drifts_hit)} 个基线已知 DRIFT（非新增回归）:")
        for item in known_drifts_hit:
            print(f"    {item['name']}.asm")
        print("  详见 tools/asm_drift_baseline.json。")
        print("[PASS] 无新增漂移（基线已知 DRIFT 容忍）。")

    cf_items = [r for r in rep.get("results", []) if r["status"] == "COMPILE_FAIL"]
    new_cf = [c for c in cf_items if c["name"] not in known_cf]
    known_cf_hit = [c for c in cf_items if c["name"] in known_cf]

    if new_cf:
        print(f"\n[WARN] {len(new_cf)} 个 *新增* 源文件无法用当前 GCC 重编 (COMPILE_FAIL)")
        print("  源码可能已演进（函数签名变化）或编译标志过时。")
        print("  这些文件的 .asm 无法验证真实性，建议手动核查或更新源码。")
        for item in new_cf[:5]:
            print(f"    {item['name']}.asm: {item.get('detail','')[:60]}")
        return 2

    if known_cf_hit:
        print(f"\n[WARN] {len(known_cf_hit)} 个基线已知 COMPILE_FAIL"
              f"（C++20 模块等需特殊构建，非回归）:")
        for item in known_cf_hit:
            print(f"    {item['name']}.asm")
        print("  详见 tools/asm_drift_baseline.json#known_compile_fail。")

    if n_ns:
        print(f"\n[INFO] {n_ns} 个 NO_SOURCE（手写多档对比/示意汇编，"
              f"设计内策展噪声，不计入失败）。")

    print(f"\n[PASS] 全部 {n_match} 个可重编证据 MATCH，无新增漂移/编译失败。")
    if n_fs:
        print(f"  ({n_fs} 个 FORMAT_SKIP 为策展噪声)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
