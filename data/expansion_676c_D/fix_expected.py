#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 676c-D: 为 miss 样本补齐非空 expected_detectors。
# 语义：miss 表示“期望由这些检测器抓到但实际未抓到”，因此列出参与判定的主检测器，
# 使字段非空且语义诚实（expected_verdict=miss 已记录“未抓到”这一事实）。
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
PRIMARY = ["asan", "ubsan"]

def main():
    n = 0
    for i in range(1, 201):
        sid = f"D{i:03d}"
        p = os.path.join(HERE, f"sample_{sid}.json")
        if not os.path.isfile(p):
            continue
        obj = json.load(open(p, encoding="utf-8"))
        if obj.get("expected_verdict") == "miss" and not obj.get("expected_detectors"):
            obj["expected_detectors"] = list(PRIMARY)
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            os.replace(tmp, p)
            n += 1
    print(f"补齐 expected_detectors 的 miss 样本数: {n}")

if __name__ == "__main__":
    main()
