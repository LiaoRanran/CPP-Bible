#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI 编排：T1 质量门禁统一入口 (T1-orchestrator)
============================================
一次性串联全部 T1 门禁，输出单一 CI 报告与退出码：

  T1-1  编译+链接+运行+Sanitizer 流水线   —— 硬门禁：编译/运行失败或超时即红
      * 开启 --chapter-context：用同章片段块作编译前缀，消解教学书增量式
        定义（log_if<>/Level/g_mtx 等）造成的前向引用误报。
      * MinGW GCC 15.3.0 不提供 std::print 运行时（__open_terminal /
        __write_to_terminal 缺失）→ 该类块被标记 skip(toolchain:std-print)，
        编译通过但跳过链接/运行，不计为失败（非书稿错误）。
  T1-2  悬空章节引用 linter               —— 软门禁：对已知债务设基线，增量回归即红
  T1-3  前置依赖拓扑校验                 —— 软门禁：同上
  gen   gen_indexes.py --check            —— 硬门禁：索引与磁盘一致

软门禁基线存于 tools/ci_baseline.json；`--update-baseline` 在债务有意变动后刷新。

用法:
  python tools/ci_gate.py                  # 增量 CI：仅跑 git diff 变更章节
  python tools/ci_gate.py --all-run        # 全量扫描（全书所有 ch*.md）
  python tools/ci_gate.py --update-baseline
  python tools/ci_gate.py --json ci_report.json
  python tools/ci_gate.py --no-baseline-gate   # 软门禁仅报告不判红
  python tools/ci_gate.py --no-chapter-context # 关闭 T1-1 前向引用消解
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / "Book"
BASELINE = HERE / "ci_baseline.json"
T1_1_JSON = HERE / "_t1_1_report.json"
T1_2_JSON = HERE / "_t1_2_report.json"
T1_3_JSON = HERE / "_t1_3_report.json"

# 优先用受管 Python 运行子脚本（仅用标准库，兼容性高）
MANAGED_PY = r"C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"
PY = MANAGED_PY if os.path.isfile(MANAGED_PY) else sys.executable


def run_tool(script, *args, json_out=None, timeout=3000):
    """在项目根下运行一个工具脚本，回传 CompletedProcess。"""
    cmd = [PY, str(script)] + list(args)
    if json_out:
        cmd += ["--json", str(json_out)]
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True,
                          text=True, timeout=timeout)


def load_baseline():
    if BASELINE.is_file():
        try:
            return json.loads(BASELINE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def save_baseline(data):
    BASELINE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path):
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def main():
    ap = argparse.ArgumentParser(description="T1 质量门禁统一 CI 入口")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--json", default=None, help="聚合 CI 报告输出路径")
    ap.add_argument("--update-baseline", action="store_true",
                    help="以当前结果刷新软门禁基线")
    ap.add_argument("--no-baseline-gate", action="store_true",
                    help="软门禁（T1-2/T1-3）仅报告，不因回归判红")
    ap.add_argument("--no-chapter-context", action="store_true",
                    help="关闭 T1-1 同章前向引用消解（默认开启）")
    ap.add_argument("--all-run", action="store_true",
                    help="强制 T1-1 全量扫描 (--all)，忽略 --changed 增量模式")
    args = ap.parse_args()

    baseline = load_baseline()
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "toolchain": {
            "python": PY,
            "gpp": "GCC 15.3.0 (MinGW) via compile_run_sanitize_pipeline.find_gpp()",
            "note": "T1-1 硬门禁；T1-2/T1-3 软门禁（已知债务设基线，增量即红）",
        },
        "gates": {},
        "ci_pass": True,
    }

    # ---------------------------------------------------------------- T1-1
    # 增量模式：`--changed` 仅扫描 git diff 变更的 ch*.md，
    # 大幅缩短本地开发 + CI 的 T1-1 用时（全量跑 --all 可加 --all-run）。
    # CI 环境（从 origin/master 拉取完整历史）下 git diff origin/master...HEAD
    # 可正常返回；本地或首次克隆无对比基线时自动回退至 --all。
    t11_flags = ["--book", args.book]
    if args.all_run:
        t11_flags.append("--all")
    else:
        t11_flags.append("--changed")
    if not args.no_chapter_context:
        t11_flags.append("--chapter-context")
    p1 = run_tool(HERE / "compile_run_sanitize_pipeline.py",
                  *t11_flags, json_out=T1_1_JSON)
    t11 = load_json(T1_1_JSON)
    st = t11.get("stats", {})
    t11_pass = (st.get("compile_fail", 0) == 0 and st.get("run_fail", 0) == 0)
    report["gates"]["T1-1_compile_run"] = {
        "rc": p1.returncode,
        "pass": t11_pass,
        "mode": "changed" if not args.all_run else "all",
        "stats": st,
        "failures": len(t11.get("failures", [])),
        "toolchain_skip": st.get("toolchain_skip", 0),
        "stderr_tail": (p1.stderr or "")[-1200:],
    }
    if not t11_pass:
        report["ci_pass"] = False

    # ---------------------------------------------------------------- T1-2
    p2 = run_tool(HERE / "dangling_ref_linter.py", "--book", args.book,
                  json_out=T1_2_JSON)
    t12 = load_json(T1_2_JSON)
    dangling = t12.get("dangling_count", 0)
    orphan = len(t12.get("orphan_links", []))
    t12_regress = False
    if baseline and "T1-2" in baseline and not args.no_baseline_gate:
        b = baseline["T1-2"]
        if dangling > b.get("dangling_count", 0) or orphan > len(b.get("orphan_links", [])):
            t12_regress = True
            report["ci_pass"] = False
    report["gates"]["T1-2_dangling_ref"] = {
        "rc": p2.returncode,
        "dangling_count": dangling,
        "orphan_links": orphan,
        "regression": t12_regress,
        "baseline": (baseline or {}).get("T1-2"),
        "soft_gate": True,
    }

    # ---------------------------------------------------------------- T1-3
    p3 = run_tool(HERE / "prereq_topo_check.py", "--book", args.book,
                  json_out=T1_3_JSON)
    t13 = load_json(T1_3_JSON)
    inverted = len(t13.get("inverted", []))
    dpre = len(t13.get("dangling_pre", []))
    t13_regress = False
    if baseline and "T1-3" in baseline and not args.no_baseline_gate:
        b = baseline["T1-3"]
        if inverted > b.get("inverted", 0) or dpre > b.get("dangling_pre", 0):
            t13_regress = True
            report["ci_pass"] = False
    report["gates"]["T1-3_prereq_topo"] = {
        "rc": p3.returncode,
        "inverted": inverted,
        "dangling_pre": dpre,
        "regression": t13_regress,
        "baseline": (baseline or {}).get("T1-3"),
        "soft_gate": True,
    }

    # ---------------------------------------------------------------- gen
    p4 = run_tool(ROOT / "tools" / "gen_indexes.py", "--check")
    gen_pass = p4.returncode == 0
    report["gates"]["gen_indexes_check"] = {
        "rc": p4.returncode, "pass": gen_pass,
        "stdout_tail": (p4.stdout or "")[-600:],
    }
    if not gen_pass:
        report["ci_pass"] = False

    # ---------------------------------------------------------------- baseline
    if args.update_baseline:
        newb = {
            "T1-2": {"dangling_count": dangling, "orphan_links": t12.get("orphan_links", [])},
            "T1-3": {"inverted": inverted, "dangling_pre": dpre},
        }
        save_baseline(newb)
        report["baseline_updated"] = newb

    # ---------------------------------------------------------------- 输出
    g = report["gates"]
    print("=" * 76)
    print("T1 CI 质量门禁汇总")
    print("=" * 76)
    print(f"  T1-1 编译+链接+运行 [{g['T1-1_compile_run'].get('mode','?')}] : {'PASS' if g['T1-1_compile_run']['pass'] else 'FAIL'}  "
          f"(编译失败 {st.get('compile_fail',0)}, 运行失败 {st.get('run_fail',0)}, "
          f"工具链缺口跳过 {st.get('toolchain_skip',0)})")
    t2 = g["T1-2_dangling_ref"]
    print(f"  T1-2 悬空章节引用     : {'PASS' if not t2['regression'] else 'FAIL(回归)'}  "
          f"(悬空 {t2['dangling_count']} / 孤儿链接 {t2['orphan_links']})")
    t3 = g["T1-3_prereq_topo"]
    print(f"  T1-3 前置拓扑         : {'PASS' if not t3['regression'] else 'FAIL(回归)'}  "
          f"(倒置 {t3['inverted']} / 悬空前置 {t3['dangling_pre']})")
    print(f"  gen  索引一致性       : {'PASS' if g['gen_indexes_check']['pass'] else 'FAIL'}")
    print("-" * 76)
    print(f"  CI 总判定            : {'PASS ✅' if report['ci_pass'] else 'FAIL ❌'}")
    print("=" * 76)

    if args.json:
        Path(args.json).write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[+] CI 报告写入: {args.json}")

    return 0 if report["ci_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
