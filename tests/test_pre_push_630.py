"""630 B1 · push 前检查 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import pre_push_630 as P


@pytest.fixture(scope="module")
def c():
    return P.check()


def test_controlled_dirs_clean(c):
    assert c["controlled_clean"], "§零.6：受控目录必须零污染"


def test_ci_syntax_ok(c):
    assert c["ci"]["ok"], c["ci"]
    assert c["ci"]["mode"] == "pyyaml", "本仓有 PyYAML，应走真解析"
    assert c["ci"]["jobs"] >= 5, f"jobs={c['ci']['jobs']}"


def test_deliverables_all_committed(c):
    assert c["deliverables"]["required"] >= 20
    assert c["deliverables"]["ok"], f"缺失：{c['deliverables']['missing']}"


def test_status_classifier():
    exp = P.classify_status(["?? _arch_v22/x.md", "?? _adv_v80/probes/a.cpp"])
    assert len(exp["expected"]) == 2 and not exp["other"]
    oth = P.classify_status([" M data/x.md", "?? tools/new.py"])
    assert len(oth["other"]) == 2 and not oth["expected"]


def test_check_components_all_green(c):
    """631 A2：原用例断言**聚合** `all_ok`，而 all_ok 要求"工作区干净"——
    这在**套件内**永远不成立（本批/后续批次总有待提交的新文件）⇒ 跨批脆弱。
    改为断言**各分量**（语义不变、不再随时点失效）：
    受控干净 + ci.yml 合法 + 交付物齐 + 630 代码无未提交 + 无阻断性意外改动。

    聚合 `all_ok` 的语义（push 闸门）仍由 `pre_push_630.py --check` 与 B1 报告守住：
    它只在**真正 push 前**由人/流程调用，不在套件内断言。
    """
    assert c["controlled_clean"], "§零.6：受控目录必须零污染"
    assert c["ci"]["ok"] and c["ci"]["mode"] == "pyyaml"
    assert c["deliverables"]["ok"], f"缺失：{c['deliverables']['missing']}"
    # 630 代码的未提交项（本批/后续批次编辑中必然存在）必须被**归类为阻断项**——
    # 不断言"为空"（那是 push 时点的性质，不是套件内性质）
    for x in c["uncommitted_630"]:
        assert P.batch_path(x).startswith(("tools/", "tests/")), \
            f"630 代码未提交项归类错误：{x}"
    # 阻断项里不得出现任何**生产逻辑文件**（tools/ 下的 630 工具除外：它们由上面覆盖）
    assert not [x for x in c["status_other_blocking"]
                if P.batch_path(x).startswith("atoms/")
                or P.batch_path(x).startswith("evidence/")], \
        "受控目录出现阻断项"
    assert isinstance(c["ahead"], int) and c["ahead"] >= 0


def test_regen_artifacts_are_excluded_from_blocking():
    """测试再生产物必须被识别为非阻断（否则本测试在套件内必然自我判红）。"""
    assert P.is_regen("data/629_baseline.md")
    assert P.is_regen("data/vsa/attestation_x.json")
    assert P.is_regen("_adv_v80/probes/p57.cpp")
    assert not P.is_regen("tools/some_new_tool.py")
    assert not P.is_regen("data/some_new_report.md")


def test_report_json_and_selftest(c):
    p = P.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("检查项", "预期残留", "push 命令", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    assert "git push --no-verify" in md
    assert json.load(open(P.OUT_JSON, encoding="utf-8"))["controlled_clean"] is True
    assert P.selftest() == 0
