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


def selftest():
    """只读自验证（不写任何文件）。返回失败项列表，空列表 = 通过。"""
    fails = []
    mapping = build(tc.TESTS)
    if not mapping:
        fails.append("映射表为空")
    for name, v in mapping.items():
        if not v["categories"]:
            fails.append("%s categories 为空" % name)
        if not isinstance(v["is_real_verification"], bool):
            fails.append("%s is_real_verification 非 bool" % name)
        elif v["is_real_verification"] != any(c in REAL_CATS for c in v["categories"]):
            fails.append("%s is_real_verification 与 categories 不一致" % name)
    meta = render(mapping)
    if meta["counts"]["total"] != len(mapping):
        fails.append("counts.total 不一致")
    if meta["counts"]["real_verification"] != sum(
            1 for v in mapping.values() if v["is_real_verification"]):
        fails.append("counts.real_verification 不一致")
    try:
        if json.loads(json.dumps(meta, ensure_ascii=False))["counts"]["total"] != len(mapping):
            fails.append("JSON 往返不一致")
    except (TypeError, ValueError) as e:
        fails.append("JSON 序列化失败：%s" % e)
    return fails


def main():
    ap = argparse.ArgumentParser(description="618 C4 测试分类映射表 (JSON)")
    ap.add_argument("--tests", default=tc.TESTS)
    ap.add_argument("--out", default=MAP_OUT)
    ap.add_argument("--check", action="store_true", help="只读自验证（不写文件），exit 0=通过")
    args = ap.parse_args()
    if args.check:
        fails = selftest()
        for f in fails:
            print("FAIL: %s" % f)
        print("618 C4 --check: %s" % ("PASS" if not fails else "FAIL"))
        sys.exit(0 if not fails else 1)
    meta = render(build(args.tests))
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote %s: total=%d real=%d" % (args.out, meta["counts"]["total"], meta["counts"]["real_verification"]))


if __name__ == "__main__":
    main()
