#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# 676c-D 任务E：入池
#   1) 将全部通过验证（pooled=true）的样本复制到 data/holdout_expansion/expD/
#   2) 生成 INDEX.json（兼容 expA/B/C 的 queyi-expansion-pool/v1，同时含卡要求的汇总字段）
import os
import json
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # CPP-Bible 根
POOL = os.path.join(ROOT, "data", "holdout_expansion", "expD")

def main():
    os.makedirs(POOL, exist_ok=True)
    pooled, eliminated = [], []
    for i in range(1, 201):
        sid = f"D{i:03d}"
        jp = os.path.join(HERE, f"sample_{sid}.json")
        cp = os.path.join(HERE, f"sample_{sid}.cpp")
        obj = json.load(open(jp, encoding="utf-8"))
        v = obj.get("verification", {})
        if v.get("pooled") is True and v.get("actual_verdict") in ("catch", "miss"):
            shutil.copy2(cp, os.path.join(POOL, f"sample_{sid}.cpp"))
            shutil.copy2(jp, os.path.join(POOL, f"sample_{sid}.json"))
            pooled.append((sid, obj))
        else:
            eliminated.append((sid, v.get("actual_verdict")))

    # ---- 统计 ----
    by_type, by_sev, catch_ids, miss_ids = {}, {"low": 0, "medium": 0, "high": 0}, [], []
    records = []
    for sid, obj in pooled:
        dt = obj["defect_type"]
        by_type[dt] = by_type.get(dt, 0) + 1
        by_sev[obj["severity"]] = by_sev.get(obj["severity"], 0) + 1
        verdict = obj["expected_verdict"]
        (catch_ids if verdict == "catch" else miss_ids).append(sid)
        pk = obj.get("verification", {}).get("per_kind", {})
        records.append({
            "sample_id": sid,
            "defect_type": dt,
            "defect_location": obj["defect_location"],
            "severity": obj["severity"],
            "planted": True,
            "expected_verdict": verdict,
            "expected_detectors": obj["expected_detectors"],
            "pooled_verdict": {k: pk.get(k, {}).get("verdict", "unknown") for k in ("asan", "ubsan", "compiler-warn")},
            "notes": obj["notes"],
        })

    total = len(pooled)
    catch_n, miss_n = len(catch_ids), len(miss_ids)
    index = {
        "schema": "queyi-expansion-pool/v1",
        "batch": "676c-扩样-D",
        "agent": "676c-expD",
        "pool_dir": "data/holdout_expansion/expD",
        "count": total,
        "stats": {
            "total_generated": 200,
            "compiled": 200,
            "pooled": total,
            "eliminated": len(eliminated),
            "by_type": by_type,
            "severity": by_sev,
            "planted_true": total,
            "catch": catch_n,
            "miss": miss_n,
            "blind_spot_ratio": round(miss_n / total, 4) if total else 0,
        },
        # 卡要求的汇总字段（便捷）
        "total": total,
        "type_distribution": by_type,
        "catch_count": catch_n,
        "miss_count": miss_n,
        "blind_spot_ratio": round(miss_n / total, 4) if total else 0,
        "sample_ids": [r["sample_id"] for r in records],
        "samples": records,
    }
    with open(os.path.join(POOL, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"入池 {total} 个 -> {POOL}")
    print(f"  淘汰 {len(eliminated)} 个: {[e[0] for e in eliminated]}")
    print(f"  catch={catch_n}  miss={miss_n}  blind_spot_ratio={miss_n/total:.3f}")
    print(f"  by_type={by_type}")
    print(f"  severity={by_sev}")

if __name__ == "__main__":
    main()
