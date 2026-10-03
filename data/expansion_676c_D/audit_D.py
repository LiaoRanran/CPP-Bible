#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# 676c-D 质量审计：
#   A) 结构校验（200 个 json 字段齐全、行号指向标记行、expected==actual、planted/severity 合法）
#   B) 与 expA/expB/expC 查重（源码归一化后比对）
#   C) 汇总 miss 样本按“缺陷描述”分组，供人工复查缺陷真实性
import os
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MARK = "<<PLANTED-DEFECT>>"
REQUIRED_TOP = ["sample_id", "defect_type", "defect_location", "severity",
                "planted", "expected_verdict", "expected_detectors",
                "trigger_condition", "notes"]

def norm_code(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    lines = [ln.split("//")[0].rstrip() for ln in t.splitlines()]
    lines = [ln for ln in lines if ln.strip()]
    return "\n".join(lines)

def main():
    issues = []
    samples = []
    for i in range(1, 201):
        sid = f"D{i:03d}"
        cp = os.path.join(HERE, f"sample_{sid}.cpp")
        jp = os.path.join(HERE, f"sample_{sid}.json")
        if not (os.path.isfile(cp) and os.path.isfile(jp)):
            issues.append(f"{sid}: 文件缺失")
            continue
        obj = json.load(open(jp, encoding="utf-8"))
        # 字段齐全
        for k in REQUIRED_TOP:
            if k not in obj or obj[k] in (None, "", [], {}):
                issues.append(f"{sid}: 字段缺失/为空 -> {k}")
        # sample_id 一致
        if obj.get("sample_id") != sid:
            issues.append(f"{sid}: sample_id 不一致({obj.get('sample_id')})")
        # planted
        if obj.get("planted") is not True:
            issues.append(f"{sid}: planted 非 true")
        # severity 合法
        if obj.get("severity") not in ("low", "medium", "high"):
            issues.append(f"{sid}: severity 非法({obj.get('severity')})")
        # 行号指向标记行
        dl = obj.get("defect_location", {}).get("line")
        lines = open(cp, encoding="utf-8").read().splitlines()
        if not isinstance(dl, int) or dl < 1 or dl > len(lines):
            issues.append(f"{sid}: 缺陷行号越界({dl})")
        elif MARK not in lines[dl - 1]:
            issues.append(f"{sid}: 第{dl}行不含缺陷标记")
        # expected == actual
        v = obj.get("verification", {})
        if v.get("actual_verdict") not in ("catch", "miss"):
            issues.append(f"{sid}: actual_verdict 非 catch/miss({v.get('actual_verdict')})")
        if v.get("pooled") is not True:
            issues.append(f"{sid}: pooled 非 true")
        if obj.get("expected_verdict") != v.get("actual_verdict"):
            issues.append(f"{sid}: expected({obj.get('expected_verdict')}) != actual({v.get('actual_verdict')})")
        # 描述非空
        if not obj.get("defect_location", {}).get("description"):
            issues.append(f"{sid}: description 为空")
        samples.append((sid, obj, cp))

    # ---- B) 与 expA/B/C 查重 ----
    others = set()
    for b in ("expA", "expB", "expC"):
        d = os.path.join(ROOT, "data", "holdout_expansion", b)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".cpp"):
                others.add(hashlib.md5(norm_code(os.path.join(d, fn)).encode("utf-8")).hexdigest())
    dup = []
    for sid, obj, cp in samples:
        h = hashlib.md5(norm_code(cp).encode("utf-8")).hexdigest()
        if h in others:
            dup.append(sid)

    # ---- C) miss 分组 ----
    groups = {}
    for sid, obj, cp in samples:
        if obj.get("expected_verdict") == "miss":
            desc = obj["defect_location"]["description"]
            groups.setdefault(desc, []).append(sid)

    print("=== 结构问题 ===")
    print("\n".join(issues) if issues else "无")
    print(f"\n=== 与 expA/B/C 重复的样本: {dup if dup else '无'} ===")
    print(f"\n=== miss 样本按缺陷描述分组（{sum(len(v) for v in groups.values())} 个）===")
    for desc, sids in sorted(groups.items()):
        print(f"  [{len(sids):>2}] {desc}  e.g. {sids[0]}")
    # 抽一个代表样本源码，便于人工复查
    rep_dir = os.path.join(HERE, "audit_representatives")
    os.makedirs(rep_dir, exist_ok=True)
    for desc, sids in groups.items():
        sid = sids[0]
        src = open(os.path.join(HERE, f"sample_{sid}.cpp"), encoding="utf-8").read()
        with open(os.path.join(rep_dir, f"rep_{sid}.cpp"), "w", encoding="utf-8") as f:
            f.write(src)
    print(f"\n代表样本源码已写入 {rep_dir}")

if __name__ == "__main__":
    main()
