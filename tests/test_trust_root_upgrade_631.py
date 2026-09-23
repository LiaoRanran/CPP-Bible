"""631 E1 · 信任根升级评估 单测（6 例）。"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import trust_root_upgrade_631 as T


def test_three_paths_with_five_dimensions():
    assert len(T.PATHS) == 3
    for name, v in T.PATHS.items():
        assert set(v["scores"]) == set(T.DIMENSIONS), name
        assert set(v["why"]) == set(T.DIMENSIONS), name
        assert all(1 <= s <= 5 for s in v["scores"].values()), name


def test_only_c_raises_third_party_verifiability():
    tp = {k: v["scores"]["第三方可验证性"] for k, v in T.PATHS.items()}
    assert tp["C 外部 KMS / 透明日志"] >= 4
    assert tp["A 纯标准库继续"] <= 2 and tp["B 引入 cryptography"] <= 2, \
        "A/B 的公钥都仍可被同主体改写 ⇒ 不该给高分"


def test_scores_and_totals_consistent():
    s, t = T.scores(), T.totals()
    assert set(s) == set(t) == set(T.PATHS)
    for k in t:
        assert t[k] == sum(s[k].values())


def test_recommendation_is_c_and_explained():
    rec, why = T.recommend()
    assert rec.startswith("C"), "只有 C 真正外移信任根"
    assert "第三方可验证性" in why, "必须交代为何不选总分更高的路径"


def test_steps_are_actionable():
    assert len(T.STEPS_C) >= 4
    assert any("OTS" in s or "外部锚" in s for s in T.STEPS_C)


def test_readonly_and_report():
    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=T.ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    T.scores()
    md = T.write_report()
    assert snap() == before, "只读：不生成密钥、不联网"
    text = open(md, encoding="utf-8").read()
    for kw in ("五维对比", "逐项理由", "推荐与实施步骤", "诚实登记"):
        assert kw in text, f"报告缺：{kw}"
    assert json.load(open(T.OUT_JSON, encoding="utf-8"))["recommend"].startswith("C")
    assert T.selftest() == 0
