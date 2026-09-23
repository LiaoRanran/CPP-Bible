"""631 C1 · 污染二分定位 单测（6 例，用模拟污染验证二分逻辑）。"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pollution_bisect_631 as P


def _mk(items: list[str], polluter: str):
    return lambda sub: polluter in sub


def test_bisect_finds_unique_polluter():
    items = [f"tests/t{i}.py" for i in range(8)]
    r = P.bisect(items, _mk(items, "tests/t5.py"))
    assert r["found"] == ["tests/t5.py"] and r["inconclusive"] is False
    assert len(r["steps"]) >= 3, "必须留下每一步的检查记录"


def test_bisect_boundaries():
    items = [f"tests/t{i}.py" for i in range(8)]
    assert P.bisect(items, _mk(items, "tests/t0.py"))["found"] == ["tests/t0.py"]
    assert P.bisect(items, _mk(items, "tests/t7.py"))["found"] == ["tests/t7.py"]


def test_bisect_intermittent_is_inconclusive():
    items = [f"tests/t{i}.py" for i in range(8)]
    r = P.bisect(items, lambda sub: False)
    assert r["found"] == [] and r["inconclusive"] is True, "不复现时必须显式标注"


def test_bisect_edge_collections():
    assert P.bisect([], lambda s: False)["found"] == []
    assert P.bisect(["a"], lambda s: True)["found"] == ["a"]
    assert P.bisect(["a"], lambda s: False)["inconclusive"] is True


def test_pollution_marker_and_candidates():
    assert isinstance(P.is_polluted(), bool)
    cands = P.candidate_files()
    assert len(cands) >= 1
    assert all(c.startswith("tests" + os.sep) and c.endswith(".py") for c in cands)
    assert os.path.exists(os.path.join(P.ROOT, P.TARGET)), "污染目标卡必须存在"


def test_readonly_and_report():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=P.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    P.candidate_files()
    P.is_polluted()
    assert snap() == before, "只读：不得写盘"
    md = P.write_report()
    text = open(md, encoding="utf-8").read()
    for kw in ("静态候选", "二分过程", "真实执行记录", "未能复现", "诚实登记"):
        assert kw in text, f"报告缺：{kw}"
    # 未复现的事实必须写进报告（§十二.2）
    assert "**False**" in text and "已排除" in text
    assert P.selftest() == 0
