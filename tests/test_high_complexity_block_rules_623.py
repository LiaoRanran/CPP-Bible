"""623 E2 · 高复杂度带 block 级规则 单元测试（≥3 例，规则定义文件校验）"""
from __future__ import annotations

import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YAML = os.path.join(ROOT, "data", "gate_rules_high_complexity_block_623.yaml")
RULES_CACHE = os.path.join(ROOT, "data", "_gate_rules.json")


def _load_yaml():
    # 用标准库 yaml（若不可用则简易解析）—项目 venv 含 pyyaml
    import yaml
    with open(YAML, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _load_existing_rule_ids():
    return {r["rule"] for r in json.load(open(RULES_CACHE, encoding="utf-8"))}


def test_rule_count_3_to_5():
    doc = _load_yaml()
    assert 3 <= len(doc["rules"]) <= 5, f"应 3-5 条，实际 {len(doc['rules'])}"


def test_all_block_severity():
    doc = _load_yaml()
    for r in doc["rules"]:
        assert r["severity"] == "block", f"{r['id']} 必须是 block 级"


def test_promotes_reference_real_rules():
    doc = _load_yaml()
    existing = _load_existing_rule_ids()
    for r in doc["rules"]:
        assert r["promotes"] in existing, f"{r['id']} 提升的 {r['promotes']} 必须是既有规则"


def test_required_fields_present():
    doc = _load_yaml()
    for r in doc["rules"]:
        for f in ("id", "title", "severity", "scope", "promotes", "bind", "rationale"):
            assert f in r and r[f], f"{r.get('id','?')} 缺字段 {f}"
