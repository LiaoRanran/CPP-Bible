"""629 C3 · 独立验证者静态证明 单测（6 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import independence_static_check as I


def test_ast_import_analysis(tmp_path):
    f = tmp_path / "probe.py"
    f.write_text("import json\nimport gate_engine\n"
                 "from transparency_log_628 import status\n", encoding="utf-8")
    loc, other = I.imports_of(str(f))
    assert loc == ["gate_engine", "transparency_log_628"]
    assert "json" in other and "gate_engine" not in other


def test_both_verifiers_are_zero_import():
    for t in I.measure()["targets"]:
        assert t["local_imports"] == [], f"{t['module']} 有本地 import"
        assert not t["imports_gate_engine"] and not t["imports_any_local"]


def test_path_literals_found_and_classified():
    targets = {t["module"]: t for t in I.measure()["targets"]}
    iv = targets["tools/independent_verifier_628.py"]
    paths = {i["path"]: i["kind"] for i in iv["paths"]}
    assert "decision_event_v2_ledger.jsonl" in " ".join(paths)
    assert any(v == "敏感信任文件" for v in paths.values())
    assert I.classify("data/authority/decision_event_v2_ledger.jsonl") == "敏感信任文件"
    assert I.classify("atoms/mem/ATOM-X.md") == "原始数据"
    assert I.classify("data/authority_projection_626.json") == "系统输出（对比基准）"


def test_sensitive_read_is_registered_not_hidden():
    """两个验证端都读 authority 账本（各自都要重算哈希链）⇒ 必须**如实登记**而非隐藏。"""
    ms = {t["module"]: t for t in I.measure()["targets"]}
    for mod, t in ms.items():
        assert t["reads_sensitive"], f"{mod} 应读取账本（被验证对象）"
        assert any("decision_event_v2_ledger" in p for p in t["sensitive_paths"])
    kinds = {i["kind"] for t in ms.values() for i in t["paths"]}
    assert "敏感信任文件" in kinds and "原始数据" in kinds
    md = open(I.OUT_MD, encoding="utf-8").read()
    assert "被验证对象" in md and "不是**信任依赖**" in md, "性质判定必须写进报告"


def test_independence_levels_are_honest():
    lv = I.independence_level()
    assert set(lv) == {"L1_独立主体", "L2_独立实现", "L3_独立执行环境", "L4_独立信任根"}
    assert lv["L2_独立实现"]["achieved"] is True
    for k in ("L1_独立主体", "L3_独立执行环境", "L4_独立信任根"):
        assert lv[k]["achieved"] is False and lv[k]["why"], f"{k} 需给出未达成原因"


def test_report_and_selftest():
    p = I.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("硬断言", "数据读取清单", "口径不符", "独立性分级", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert I.selftest() == 0
