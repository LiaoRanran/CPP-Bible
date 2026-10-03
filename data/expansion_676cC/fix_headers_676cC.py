#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_headers_676cC.py — 修复 15 个 cross_tu 样本的非法头文件扩展名。

问题：生成器把跨 TU 头文件命名为 sample_NNN.h_a / sample_NNN.h_b。
g++ 不识别 .h_a / .h_b 扩展名，会把它当作链接器输入 -> 'file format not recognized'。
修复：重命名为 g++ 可识别的 sample_NNN_a.h / sample_NNN_b.h，并同步
#include 指令与 JSON source_files。头文件被 .cpp 通过 #include 引用，
改扩展名不影响缺陷语义（inline/weak ODR 仍链接通过 -> 盲区）。
"""
import os, re, json

EXP = os.path.dirname(os.path.abspath(__file__))

BAD = [99,100,101,102,103,104,105,106,114,115,116,117,118,119,120]

def remap(name):
    if name.endswith(".h_a"):
        return name[:-3] + "_a.h"      # sample_NNN.h_a -> sample_NNN_a.h
    if name.endswith(".h_b"):
        return name[:-3] + "_b.h"
    return name

def main():
    for n in BAD:
        prefix = f"sample_{n:03d}"
        jp = os.path.join(EXP, prefix + ".json")
        meta = json.load(open(jp, encoding="utf-8"))
        sf = meta.get("source_files", [])
        # 建立旧->新映射（仅本样本内）
        mapping = {}
        for f in list(sf):
            nf = remap(f)
            if nf != f:
                mapping[f] = nf
        if not mapping:
            print(f"{prefix}: 无需修复"); continue
        # 1) 重命名磁盘文件
        for old, new in mapping.items():
            op = os.path.join(EXP, old); np_ = os.path.join(EXP, new)
            if os.path.isfile(op):
                os.rename(op, np_)
                print(f"  rename {old} -> {new}")
            else:
                print(f"  !! 文件缺失 {old}")
        # 2) 更新本样本所有 .cpp 文件中的 #include 引用
        for fn in os.listdir(EXP):
            if fn.startswith(prefix) and fn.endswith(".cpp"):
                p = os.path.join(EXP, fn)
                s = open(p, encoding="utf-8").read()
                for old, new in mapping.items():
                    s = s.replace('"%s"' % old, '"%s"' % new)
                open(p, "w", encoding="utf-8").write(s)
        # 3) 更新 JSON source_files（及其他可能引用旧名的字段）
        new_sf = [mapping.get(f, f) for f in sf]
        meta["source_files"] = new_sf
        raw = json.dumps(meta, ensure_ascii=False)
        for old, new in mapping.items():
            raw = raw.replace(old, new)
        json.dump(json.loads(raw), open(jp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"{prefix}: source_files -> {new_sf}")

if __name__ == "__main__":
    main()
