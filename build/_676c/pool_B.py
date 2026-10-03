#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676c 扩样-B · Task E：把验证通过的样本入池到 data/holdout_expansion/expB/。

读取 build/_676c 产生的 data/expansion_676c_B/validation.json：
  - 仅入池 rec["pool"] == True 的样本（编译通过 且 判定与期望一致）
  - 拷贝 sample_B*.cpp + .json 到 data/holdout_expansion/expB/
  - 生成 expB/INDEX.json（池清单 + 统计）
不修改任何既有数据；文件名沿用 sample_B 前缀，与 expA 的 sample_ 不冲突。
"""
import os
import sys
import json
import shutil

REPO = "C:/CodeLearnling/note/note/C++/CPP-Bible"
SRC_DIR = os.path.join(REPO, "data", "expansion_676c_B")
VAL = os.path.join(SRC_DIR, "validation.json")
POOL_DIR = os.path.join(REPO, "data", "holdout_expansion", "expB")


def main():
    if not os.path.isfile(VAL):
        print("ERROR: 未找到 validation.json，请先跑 validate_B.py")
        return 2
    recs = json.load(open(VAL, encoding="utf-8"))
    os.makedirs(POOL_DIR, exist_ok=True)

    pooled = [r for r in recs if r.get("pool")]
    index = []
    for r in pooled:
        sid = r["sample_id"]
        # 拷贝 cpp + json
        for ext in (".cpp", ".json"):
            src = os.path.join(SRC_DIR, sid + ext)
            dst = os.path.join(POOL_DIR, sid + ext)
            shutil.copy2(src, dst)
        # 读取权威标注
        ann = json.load(open(os.path.join(SRC_DIR, sid + ".json"), encoding="utf-8"))
        det_v = {k: v["verdict"] for k, v in r["detections"].items()}
        index.append({
            "sample_id": sid,
            "defect_type": ann["defect_type"],
            "defect_location": ann["defect_location"],
            "severity": ann["severity"],
            "planted": ann["planted"],
            "expected_verdict": ann["expected_verdict"],
            "expected_detectors": ann["expected_detectors"],
            "pooled_verdict": det_v,
            "notes": ann["notes"],
        })

    # 统计
    by_type = {}
    for it in index:
        by_type.setdefault(it["defect_type"], 0)
        by_type[it["defect_type"]] += 1
    stats = {
        "total_generated": len(recs),
        "compiled": sum(1 for r in recs if r["compile_ok"]),
        "pooled": len(index),
        "eliminated": len(recs) - len(index),
        "by_type": by_type,
        "severity": {
            "low": sum(1 for it in index if it["severity"] == "low"),
            "medium": sum(1 for it in index if it["severity"] == "medium"),
            "high": sum(1 for it in index if it["severity"] == "high"),
        },
        "planted_true": sum(1 for it in index if it["planted"] is True),
    }
    manifest = {
        "schema": "queyi-expansion-pool/v1",
        "batch": "676c-扩样-B",
        "pool_dir": "data/holdout_expansion/expB",
        "count": len(index),
        "stats": stats,
        "samples": index,
    }
    with open(os.path.join(POOL_DIR, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"入池: {len(index)} / {len(recs)}")
    print("按类型:", by_type)
    print(f"已写 {os.path.join(POOL_DIR, 'INDEX.json')}")
    # 列出被淘汰的（供报告引用）
    elim = [r for r in recs if not r.get("pool")]
    if elim:
        print("淘汰样本:")
        for r in elim:
            print(f"  {r['sample_id']} {r.get('elim_reason','?')} "
                  f"(compile_ok={r['compile_ok']}, consistent={r['consistent']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
