"""629 D2 · 第八轮攻击 单测（6 例）。

**不跑沙箱**（跑一轮 ≈70s 且临时改动受控目录）；只校验契约构造 + 已保存结果的内部一致性
+ 受控目录洁净（只读）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_round8_629 as R


def test_mutation_contract_for_sandbox():
    ms = R.build_mutations()
    assert len(ms) == 20
    for i, m in enumerate(ms, 1):
        assert m["mutation_id"] == f"MUT-629-R8-{i:02d}"
        c = json.loads(m["content"])
        assert c["target_card"] and c["op"], "沙箱契约：content 必须含 target_card/op"
        assert "target_rule" in c and "point" in c


def test_saved_run_has_20_rows():
    d = R.load_saved()
    assert d, "--run 必须先跑过（本批已实跑）"
    assert d["mutations"] == 20 and len(d["rows"]) == 20
    assert all(r.get("verdict") for r in d["rows"])
    assert all(r.get("target_rule") is not None for r in d["rows"])


def test_distribution_reconciles_with_rows():
    d = R.load_saved()
    dist: dict = {}
    for r in d["rows"]:
        dist[r["verdict"]] = dist.get(r["verdict"], 0) + 1
    assert dist == d["distribution"]
    assert sum(dist.values()) == 20


def test_zero_escape_and_repo_clean():
    d = R.load_saved()
    assert d["escaped"] == [], "第八轮目标：零逃逸"
    assert not R.repo_dirty_controlled(), f"受控目录必须零污染：{R.repo_dirty_controlled()}"
    assert not os.path.exists(os.path.join(R.ROOT, "data", ".622_apply.lock"))


def test_touched_rules_recorded_honestly():
    d = R.load_saved()
    assert isinstance(d["touched_this_round"], list)
    assert d["touched_count"] == len(d["touched_this_round"])
    assert d["touched_baseline"] == 36 and d["rules_total"] == 67
    md = open(R.OUT_MD, encoding="utf-8").read()
    assert "未达成" in md, "目标未达必须显式声明（不粉饰）"
    assert "翻译失真" in md, "种子翻译失真必须登记"


def test_report_and_selftest():
    p = R.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("判决分布", "触达规则", "零污染", "诚实登记", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert R.selftest() == 0
