#!/usr/bin/env python3
"""
699-D · 数据加载接口 (reusable by batches 700+)

提供两个函数:
  load_original_project_defects() -> list[dict]   来自 data/699_original_project_defects.json
  load_llm_eval_data()           -> list[dict]   来自 data/699_llm_eval_unified_format.json

仅用标准库; 路径相对于本文件自动定位到仓库 data/ 目录。
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.normpath(os.path.join(_HERE, "..", "data"))

_DEFECTS_PATH = os.path.join(_DATA, "699_original_project_defects.json")
_LLM_PATH = os.path.join(_DATA, "699_llm_eval_unified_format.json")


def load_original_project_defects(path=_DEFECTS_PATH):
    """返回 699-A 收集的原始项目缺陷列表 (含 meta)。"""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d


def load_llm_eval_data(path=_LLM_PATH):
    """返回 699-B 统一的 LLM 评估样本列表 (含 meta)。"""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d


def get_original_project_defects_by_family(family=None, path=_DEFECTS_PATH):
    """按缺陷家族过滤 (memory-safety / concurrency / logic / ub)。"""
    d = load_original_project_defects(path)
    defs = d.get("defects", [])
    if family is None:
        return defs
    return [x for x in defs if x.get("defect_family") == family]


if __name__ == "__main__":
    a = load_original_project_defects()
    b = load_llm_eval_data()
    print("original_project_defects:", len(a.get("defects", [])), "items")
    print("llm_eval_data:", len(b.get("records", [])), "records")
    print("families:",
          {f: len(get_original_project_defects_by_family(f))
           for f in ("memory-safety", "concurrency", "logic", "ub")})
