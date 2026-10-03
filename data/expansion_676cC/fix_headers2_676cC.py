#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_headers2_676cC.py — 修正第一次重命名产生的多余点号。

第一次把 sample_NNN.h_a 错改成 sample_NNN._a.h（多了一个点）。
这里统一改为 sample_NNN_a.h / sample_NNN_b.h，并同步引用。
"""
import os, json

EXP = os.path.dirname(os.path.abspath(__file__))
BAD = [99,100,101,102,103,104,105,106,114,115,116,117,118,119,120]

def main():
    for n in BAD:
        prefix = f"sample_{n:03d}"
        # 错误名 -> 正确名
        wrong_a, right_a = f"{prefix}._a.h", f"{prefix}_a.h"
        wrong_b, right_b = f"{prefix}._b.h", f"{prefix}_b.h"
        for w, r in [(wrong_a, right_a), (wrong_b, right_b)]:
            wp = os.path.join(EXP, w); rp = os.path.join(EXP, r)
            if os.path.isfile(wp):
                os.rename(wp, rp); print(f"  rename {w} -> {r}")
        mp = {wrong_a: right_a, wrong_b: right_b}
        # 更新 .cpp 引用
        for fn in os.listdir(EXP):
            if fn.startswith(prefix) and fn.endswith(".cpp"):
                p = os.path.join(EXP, fn)
                s = open(p, encoding="utf-8").read()
                for w, r in mp.items():
                    s = s.replace('"%s"' % w, '"%s"' % r)
                open(p, "w", encoding="utf-8").write(s)
        # 更新 JSON（source_files + 任何引用）
        jp = os.path.join(EXP, prefix + ".json")
        raw = open(jp, encoding="utf-8").read()
        for w, r in mp.items():
            raw = raw.replace(w, r)
        json.dump(json.loads(raw), open(jp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        m = json.load(open(jp, encoding="utf-8"))
        print(f"{prefix}: source_files -> {m['source_files']}")

if __name__ == "__main__":
    main()
