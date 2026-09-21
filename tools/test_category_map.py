#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 C4 · 测试分类映射表（机器可读，供 C2 计数脚本与 CI 读取）

- 复用 618 C2 test_classifier_618.scan 分类，输出 tests/test_category_map.json：
  { "<test_file>.py": {"categories": [...], "is_real_verification": bool} }
- 纯标准库；只读 tests/，不 import 受控工具。
- 可被 CI 读取以决定运行集与覆盖率口径（剔除 script_self_test）。
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import test_classifier_618 as tc  # noqa: E402

REAL_CATS = set(tc.REAL_CATS)
MAP_OUT = os.path.join(ROOT, "tests", "test_category_map.json")


def build(tests_dir=tc.TESTS):
    results = tc.scan(tests_dir)
    mapping = {}
    for name, cats in results.items():
        is_real = any(c in REAL_CATS for c in cats)
        mapping[name] = {
            "categories": cats if cats else ["其他"],
            "is_real_verification": is_real,
        }
    return mapping


def render(mapping):
    meta = {
        "generated_by": "tools/test_category_map.py (618 C4)",
        "source": "test_classifier_618.scan (文件名+import 成员关系分类)",
        "schema": {
            "<test_file>.py": {
                "categories": ["gate|poison|replay|mutation|evidence|independent_verification|statistics|tooling_integrity|snapshot|script_self_test|其他"],
                "is_real_verification": "bool（命中 8 个真实验证类别之一）",
            }
        },
        "counts": {
            "total": len(mapping),
            "real_verification": sum(1 for v in mapping.values() if v["is_real_verification"]),
        },
        "map": mapping,
    }
    return meta


def main():
    ap = argparse.ArgumentParser(description="618 C4 测试分类映射表 (JSON)")
    ap.add_argument("--tests", default=tc.TESTS)
    ap.add_argument("--out", default=MAP_OUT)
    args = ap.parse_args()
    meta = render(build(args.tests))
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote %s: total=%d real=%d" % (args.out, meta["counts"]["total"], meta["counts"]["real_verification"]))


if __name__ == "__main__":
    main()
