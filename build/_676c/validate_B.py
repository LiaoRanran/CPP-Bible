#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676c 扩样-B 验证 harness（Task B 编译门 + Task C 检测器复现）。

严格不修改 tools/holdout_reveal_661.py：只做运行时 monkeypatch：
  - os.environ 注入 WSL_UTF8=1 / WSLENV=WSL_UTF8/u（修 WSL UTF-16LE 横幅导致
    subprocess text 解码失败 → sanitizer 报告整段丢失的系统性假 miss 坑）
  - 把 holdout_reveal_661.ATOMS 改成本批次样本目录，使 detect(kind, [fname]) 命中本批样本。

Task B：WSL g++ -std=c++17 -O0 -g -fsanitize=address,undefined (+ -pthread 对 data_race)
        编译+链接每个 sample_B*.cpp，记录 rc / 编译告警。rc!=0 => 编译失败，淘汰。
Task C：对通过编译的样本，按其 expected_detectors 调 detect()，与 expected_verdict 比对：
        - expected=catch => 必须 catch；否则不一致（淘汰/复标）
        - expected=miss  => 不可为 catch；miss 或 unknown 均视为"未抓到"（一致），
                            unknown 单独标记（检测器不可用而非运行期无报告）
合格（入池）：编译通过 且 与期望判定一致。

用法：
  python build/_676c/validate_B.py            # 全量 100
  python build/_676c/validate_B.py --limit 8  # 冒烟，只跑前 N 个（按 sample_id 排序）
产物：data/expansion_676c_B/validation.json
"""
import os
import sys
import json
import glob
import importlib.util
import argparse

REPO = "C:/CodeLearnling/note/note/C++/CPP-Bible"
SAMPLE_DIR = os.path.join(REPO, "data", "expansion_676c_B")
TOOLS = os.path.join(REPO, "tools")
OUT = os.path.join(SAMPLE_DIR, "validation.json")

# ---- 修 WSL UTF-16LE 横幅坑（必须在 import 检测器并调用 _wsl 之前设好 env）----
os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"

# ---- 载入检测器（不修改文件，仅运行时引用）----
spec = importlib.util.spec_from_file_location(
    "holdout_reveal_661", os.path.join(TOOLS, "holdout_reveal_661.py"))
det = importlib.util.module_from_spec(spec)
spec.loader.exec_module(det)
# monkeypatch：让 detect() 在样本目录里找 sample_B*.cpp
det.ATOMS = SAMPLE_DIR


def task_b_compile(json_path):
    """编译门：WSL g++ 全量编译+链接。返回 (rc, warnings_str)。"""
    ann = json.load(open(json_path, encoding="utf-8"))
    dt = ann["defect_type"]
    fname = ann["sample_id"] + ".cpp"
    src = os.path.join(SAMPLE_DIR, fname)
    wsrc = det._to_wsl(src)
    pthread = " -pthread" if dt == "data_race" else ""
    exe = det._to_wsl(f"/tmp/676c_{ann['sample_id']}.exe")
    cmd = (f"g++ -std=c++17 -O0 -g -fsanitize=address,undefined{pthread} "
           f"-o {exe} {wsrc}")
    rc, out = det._wsl(cmd, timeout=120)
    warns = [ln for ln in out.splitlines() if "warning:" in ln]
    return rc, "\n".join(warns)


def task_c_detect(ann):
    """对样本按 expected_detectors 跑 detect()，返回 {detector:(verdict,note)}。"""
    results = {}
    for d in ann["expected_detectors"]:
        v, note = det.detect(d, [ann["sample_id"] + ".cpp"])
        results[d] = (v, note)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0,
                    help="只跑前 N 个样本（按 sample_id 排序），0=全量")
    a = ap.parse_args()

    jsons = sorted(glob.glob(os.path.join(SAMPLE_DIR, "sample_B*.json")))
    if a.limit:
        jsons = jsons[:a.limit]

    records = []
    for jp in jsons:
        ann = json.load(open(jp, encoding="utf-8"))
        sid = ann["sample_id"]
        rc, warns = task_b_compile(jp)
        rec = {
            "sample_id": sid,
            "defect_type": ann["defect_type"],
            "expected_verdict": ann["expected_verdict"],
            "expected_detectors": ann["expected_detectors"],
            "compile_rc": rc,
            "compile_ok": rc == 0,
            "compile_warnings": warns,
            "detections": {},
            "consistent": None,
            "unknown_flag": False,
            "pool": False,
        }
        if rc != 0:
            rec["consistent"] = False
            rec["elim_reason"] = "Task B 编译失败"
            records.append(rec)
            print(f"  {sid}  COMPILE_FAIL rc={rc} {ann['defect_type']}")
            continue

        dets = task_c_detect(ann)
        rec["detections"] = {k: {"verdict": v, "note": n} for k, (v, n) in dets.items()}
        # 判定一致性
        ev = ann["expected_verdict"]
        any_unknown = any(v == "unknown" for (v, _) in dets.values())
        any_catch = any(v == "catch" for (v, _) in dets.values())
        if ev == "catch":
            rec["consistent"] = any_catch  # 期望 catch => 任一检测器 catch 即一致
        else:  # miss
            rec["consistent"] = not any_catch  # 期望 miss => 不可为 catch
        rec["unknown_flag"] = any_unknown
        rec["pool"] = rec["consistent"]
        if not rec["consistent"]:
            rec["elim_reason"] = "Task C 判定与期望不一致"
        status = "POOL" if rec["pool"] else ("ELIM" if not rec["consistent"] else "OK?")
        print(f"  {sid}  {status:<4} {ann['defect_type']:<15} "
              f"exp={ev:<5} dets={ {k:v for k,(v,_) in dets.items()} }")
        records.append(rec)

    json.dump(records, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    n = len(records)
    compiled = sum(1 for r in records if r["compile_ok"])
    pooled = sum(1 for r in records if r["pool"])
    nconsist = sum(1 for r in records if r["consistent"] is False)
    unknown = sum(1 for r in records if r["unknown_flag"])
    print("\n=== 汇总 ===")
    print(f"样本总数: {n}")
    print(f"编译通过: {compiled}")
    print(f"入池(编译通过且判定一致): {pooled}")
    print(f"淘汰(编译失败或判定不一致): {n - pooled}")
    print(f"  其中编译失败: {n - compiled}")
    print(f"  其中判定不一致: {nconsist - (n - compiled)}")
    print(f"unknown 标记(检测器不可用): {unknown}")
    # 按类型分
    by_type = {}
    for r in records:
        by_type.setdefault(r["defect_type"], {"pool": 0, "total": 0})
        by_type[r["defect_type"]]["total"] += 1
        if r["pool"]:
            by_type[r["defect_type"]]["pool"] += 1
    print("按类型(入池/总数):")
    for t, c in sorted(by_type.items()):
        print(f"  {t:<15} {c['pool']}/{c['total']}")
    print(f"已写 {OUT}")


if __name__ == "__main__":
    main()
