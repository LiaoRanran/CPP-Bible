#!/usr/bin/env python3
"""prune_exempt.py — A2 豁免消化工具

依据一份**全量 main-only** 编译报告，将 tools/compile_exempt.json 精确收敛为
「当前仍失败的 main 块」集合：

  - 报告中仍失败的 (file, block)          -> 保留豁免 (active)
  - 豁免清单里、报告未失败的 (file, block) -> 移除 (stale/redundant)
  - 报告失败、但不在豁免清单的 (file,block) -> 回归 (regression)，脚本报错退出，需人工修复

用法:
  python3 tools/prune_exempt.py --report tools/compile_report.json [--write]

默认 dry-run；加 --write 才真正回写 compile_exempt.json。
回写前对 compile_exempt.json 做 .bak 备份。
"""
import json, sys, shutil, argparse, datetime, os

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="tools/compile_report.json")
    ap.add_argument("--exempt", default="tools/compile_exempt.json")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    rep = load(a.report)
    if rep.get("partial"):
        print(f"[FATAL] 报告是部分扫描 (partial=True, total_chapters={rep.get('total_chapters')})，"
              "不能据此裁剪。请用全量 main-only 报告。")
        sys.exit(2)
    if not rep.get("main_only"):
        print("[WARN] 报告非 main-only 模式，与 CI 门禁不一致。")

    exj = load(a.exempt)
    ex = exj["exempt"]

    failing = set()
    for c in rep["failures"]:
        f = c["file"]
        for fr in c["failures"]:
            failing.add((f, fr["block"]))

    exk = [(e["file"], e["block"]) for e in ex]
    exset = set(exk)
    active = [k for k in exk if k in failing]
    stale  = [k for k in exk if k not in failing]
    regression = sorted(failing - exset)

    print(f"报告失败块 (main-only, 全量): {len(failing)}")
    print(f"豁免清单条目            : {len(ex)}")
    print(f"  ACTIVE 保留           : {len(active)}")
    print(f"  STALE  移除           : {len(stale)}")
    print(f"新增回归 (失败且未豁免) : {len(regression)}")
    for k in regression:
        print("   REGRESSION", k[0], "blk", k[1])

    if regression:
        print("\n[FAIL] 存在未豁免的失败块（回归），必须先修复，未回写。")
        sys.exit(1)

    # keep only active entries, preserve original field order/metadata
    new_ex = [e for e in ex if (e["file"], e["block"]) in failing]

    if a.write:
        shutil.copy(a.exempt, a.exempt + ".bak")
        exj["exempt"] = new_ex
        exj["pruned_from"] = os.path.basename(a.report)
        exj["pruned_at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        exj["exempt_count"] = len(new_ex)
        with open(a.exempt, "w", encoding="utf-8") as f:
            json.dump(exj, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"\n[WROTE] {a.exempt}  {len(ex)} -> {len(new_ex)} 条 (备份 {a.exempt}.bak)")
    else:
        print(f"\n[DRY-RUN] 未回写。将裁剪 {len(ex)} -> {len(new_ex)} 条。加 --write 执行。")

if __name__ == "__main__":
    main()
