# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""670c B2 回归锁：复现编排器（tools/reproduce_all_670c.py）。

锁六件事 —— 每一条都对应一种真实出现过的"静默假绿"：

  ① 编排器**在**（文件存在 + 可 import + 步骤数够）——复现 kit 的主体不能悄悄消失；
  ② CLI 契约（--list / --mode / --skip-slow / --only / --keep-outputs）不被改名或改语义；
  ③ check 表**结构合法**（id 唯一 / 每步有 cmd 与 checks / artifact 路径在 data|web 下 /
     kind 与 mode 都在枚举内）——错了要**在跑之前**就红，而不是跑完看一堆 MISS；
  ④ 报告构造是**纯函数**：给假数据必得同一结构，且 summary 与 overall 自洽；
  ⑤ **不匹配判定真的会判不匹配** —— 这是本工具唯一能让"数字对不上"显形的地方，
     若它恒真，整条流水线就是装饰品；
  ⑥ check 表里的数字必须等于仓库里**已落盘**的事实源 —— 防止有人改预期值让流水线变绿。

为什么用假数据跑流程：本模块属 fast 组，真跑全流程（WSL 编译 + 变异 + pytest）会超时，
且会与并行批次抢同一批产物。真流程的验证落在 data/reproduction_report_670c.json。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import reproduce_all_670c as R  # noqa: E402


# ── ① 编排器在 ───────────────────────────────────────────────────────────────
def test_orchestrator_exists_and_exposes_contract():
    assert (ROOT / "tools" / "reproduce_all_670c.py").is_file()
    assert callable(R.main) and callable(R.evaluate) and callable(R.build_report)
    assert len(R.STEPS) >= 7, f"步骤太少（{len(R.STEPS)}）⇒ 复现流程被裁剪了"
    for must in ("S1_gate_658", "S3_holdout_reveal", "S4_external_corpus",
                 "S5_mutation_core", "S7_counterfactual", "S8_fast_tests"):
        assert must in R.STEP_IDS, f"缺关键步骤 {must}"


# ── ② CLI 契约 ───────────────────────────────────────────────────────────────
def test_cli_contract_defaults_and_flags():
    d = R.parse_args([])
    assert d.mode == "verify" and d.skip_slow is False and d.list is False, "默认必须是只读 verify"
    a = R.parse_args(["--list"])
    assert a.list is True
    b = R.parse_args(["--mode", "run", "--skip-slow",
                      "--only", "S3_holdout_reveal,S7_counterfactual"])
    assert b.mode == "run" and b.skip_slow is True
    assert R.parse_only(b.only) == ["S3_holdout_reveal", "S7_counterfactual"]
    assert R.parse_only("") == [] and R.parse_only(None) == []
    c = R.parse_args(["--keep-outputs", "--no-write", "--timeout-scale", "2.5"])
    assert c.keep_outputs and c.no_write and c.timeout_scale == 2.5


def test_cli_rejects_unknown_mode():
    with pytest.raises(SystemExit):
        R.parse_args(["--mode", "explode"])


# ── ③ check 表结构合法 ───────────────────────────────────────────────────────
def test_expect_table_is_valid():
    assert R.validate_expect_table(R.STEPS) == [], R.validate_expect_table(R.STEPS)
    ids = [s["id"] for s in R.STEPS]
    assert len(ids) == len(set(ids)), "step id 必须唯一"
    for s in R.STEPS:
        assert s["checks"], f"{s['id']} 没有预期 ⇒ 它永远无法被判红"
        assert s["timeout"] > 0 and s["cmd"], s["id"]


def test_expect_table_validator_actually_rejects():
    """阴性对照：坏表必须被拦下（否则 validate 恒真 = 没有校验）。"""
    bad = [{"id": "X", "name": "n", "why": "w", "slow": False, "cmd": [], "writes": ["/abs/p"],
            "timeout": 1,
            "checks": [{"mode": "nope", "kind": "nope", "desc": "d"},
                       {"mode": "run", "kind": "artifact", "desc": "无路径无值"}]}]
    errs = R.validate_expect_table(bad)
    assert any("cmd 为空" in e for e in errs), errs
    assert any("未知 kind" in e for e in errs), errs
    assert any("未知 mode" in e for e in errs), errs
    assert any("仓库相对路径" in e for e in errs), errs
    assert any("artifact check 缺 jsonpath" in e for e in errs), errs


# ── ④ 报告结构（纯函数，假数据）──────────────────────────────────────────────
def _fake_step(sid: str, matched: bool, skipped: bool = False) -> dict:
    return {"id": sid, "name": sid, "matched": matched, "skipped": skipped,
            "checks": [{"ok": matched, "desc": "d"}]}


def test_build_report_structure_with_fake_data():
    steps = [_fake_step("A", True), _fake_step("B", False)]
    rep = R.build_report(steps, {"python": "3.13.13"},
                         {"mode": "run", "skip_slow": False, "only": [], "keep_outputs": False})
    assert rep["schema"] == R.SCHEMA and rep["generated_by"].endswith("reproduce_all_670c.py")
    assert rep["summary"] == {"total": 2, "ran": 2, "skipped": 0, "matched": 1, "failed": 1}
    assert rep["overall"] == "FAIL", "有步骤红时 overall 必须是 FAIL"
    assert isinstance(rep["steps"], list) and len(rep["steps"]) == 2
    assert "env" in rep and "honest_note" in rep and "artifacts" in rep
    assert json.loads(json.dumps(rep, ensure_ascii=False))["overall"] == "FAIL"  # 可序列化


def test_overall_never_confuses_skipped_with_passed():
    """★ 核心诚实锁：跳过 ≠ 通过。全跳过只能是 PARTIAL。"""
    all_skipped = R.build_report([_fake_step("A", False, True), _fake_step("B", False, True)],
                                 {}, {"mode": "verify"})
    assert all_skipped["summary"]["skipped"] == 2 and all_skipped["summary"]["matched"] == 0
    assert all_skipped["overall"] == "PARTIAL", all_skipped["overall"]
    partial = R.build_report([_fake_step("A", True), _fake_step("B", False, True)],
                             {}, {"mode": "run", "skip_slow": True})
    assert partial["overall"] == "PARTIAL" and partial["skip_slow"] is True
    green = R.build_report([_fake_step("A", True)], {}, {"mode": "run"})
    assert green["overall"] == "PASS"


# ── ⑤ 不匹配判定真的会判不匹配 ───────────────────────────────────────────────
def _mismatch_step() -> dict:
    return {"id": "T", "name": "t", "why": "w", "slow": False, "cmd": ["x"], "writes": [],
            "timeout": 1,
            "checks": [
                {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
                {"mode": "run", "kind": "stdout_re", "value": r"检出率=87\.5%", "desc": "stdout 87.5"},
                {"mode": "run", "kind": "stdout_json", "jsonpath": "killed", "value": 110,
                 "desc": "stdout JSON killed=110"},
                {"mode": "both", "kind": "artifact", "path": "data/x.json",
                 "jsonpath": "a.b", "value": 7, "desc": "产物 a.b=7"},
            ]}


def test_evaluate_matches_and_flags_each_mismatch(tmp_path: Path):
    step = _mismatch_step()
    (tmp_path / "data").mkdir()
    art = tmp_path / "data" / "x.json"
    art.write_text(json.dumps({"a": {"b": 7}}), encoding="utf-8")
    good = {"exit": 0, "stdout": '检出率=87.5%\n{"killed": 110}', "root": tmp_path, "mode": "run"}
    res = R.evaluate(step, good)
    assert res["matched"] is True and res["failed"] == 0 and res["judged"] == 4, res

    # 四种坏法各自独立地被抓到（少抓一种 = 一类漂移能静默过去）
    for name, ctx in (
        ("退出码", {**good, "exit": 1}),
        ("stdout 文本", {**good, "stdout": '{"killed": 110}'}),
        ("stdout JSON 数字", {**good, "stdout": '检出率=87.5%\n{"killed": 109}'}),
        ("stdout 无 JSON", {**good, "stdout": "检出率=87.5%\n(broken)"}),
    ):
        bad = R.evaluate(step, ctx)
        assert bad["matched"] is False, f"{name} 漂移未被抓到 ⇒ 判定逻辑失效"

    # 产物改一个数字 ⇒ 必须红（这是"数据漂了"的唯一显形路径）
    art.write_text(json.dumps({"a": {"b": 8}}), encoding="utf-8")
    assert R.evaluate(step, good)["matched"] is False
    art.unlink()
    missing = R.evaluate(step, good)
    assert missing["matched"] is False and "缺文件" in json.dumps(missing, ensure_ascii=False)

    # verify 模式：stdout 类 check 被跳过，artifact 仍判 ⇒ 不是"全跳过就算过"
    art.write_text(json.dumps({"a": {"b": 7}}), encoding="utf-8")
    ver = R.evaluate(step, {"exit": None, "stdout": "", "root": tmp_path, "mode": "verify"})
    assert ver["judged"] == 1 and ver["matched"] is True
    assert sum(1 for c in ver["checks"] if c.get("skipped")) == 3
    # 一个都判不了的步骤必须被标成 unverifiable（不能算通过）
    nov = {"id": "U", "name": "u", "why": "w", "slow": False, "cmd": ["x"], "writes": [],
           "timeout": 1, "checks": [{"mode": "run", "kind": "exit", "value": 0, "desc": "d"}]}
    assert R.evaluate(nov, {"exit": None, "stdout": "", "root": tmp_path,
                            "mode": "verify"})["unverifiable"] is True


def test_json_extraction_and_value_comparison():
    objs = R.extract_json_objects('进度行…\n{"a": 1}\n噪声 {"b": "x"}\n')
    assert objs == [{"a": 1}, {"b": "x"}], objs
    assert R.extract_json_objects("没有 JSON") == []
    assert R.values_equal(87.5, 87.5) and R.values_equal(14, 14)
    assert not R.values_equal(87.5, 87.6) and not R.values_equal(14, 15)
    assert not R.values_equal(True, 1), "bool 不许冒充 1（planted=true 与计数是两回事）"
    assert not R.values_equal(0, False)
    assert R.json_get({"a": {"b": [3]}}, "a.b.0") == 3
    # 路径写错 / 字段改名 / 类型不符必须**一律**抛 KeyError（调用方只捕一种即可收敛成 MISS）
    for bad_path in ("a.nope", "a.b.9", "a.b.x"):
        with pytest.raises(KeyError):
            R.json_get({"a": {"b": [3]}}, bad_path)
    with pytest.raises(KeyError):
        R.json_get({"a": 1}, "a.nope")


# ── --only 选择语义 ──────────────────────────────────────────────────────────
def test_only_selection_keeps_definition_order_and_rejects_unknown():
    sel = R.select_steps(R.STEPS, ["S7_counterfactual", "S1_gate_658"])
    assert [s["id"] for s in sel] == ["S1_gate_658", "S7_counterfactual"], "必须保持定义顺序"
    assert len(R.select_steps(R.STEPS, [])) == len(R.STEPS)
    with pytest.raises(ValueError):
        R.select_steps(R.STEPS, ["S99_nope"])


# ── ⑥ 预期值 == 已落盘事实源 ─────────────────────────────────────────────────
def test_shipped_artifacts_match_expected_table():
    """★ 改预期值让流水线变绿会被这一条抓到（669 的审计正是被同类问题打中的）。"""
    checked = 0
    for s in R.STEPS:
        for c in s["checks"]:
            if c["kind"] != "artifact" or c["mode"] == "run":
                continue
            p = ROOT / c["path"]
            assert p.is_file(), f"{c['path']} 缺失 —— 复现 kit 的事实源不见了"
            doc = json.loads(p.read_bytes().decode("utf-8"))
            obs = R.json_get(doc, c["jsonpath"])
            assert R.values_equal(obs, c["value"]), (c["path"], c["jsonpath"], obs, c["value"])
            checked += 1
    assert checked >= 12, f"artifact 断言只有 {checked} 条 ⇒ 射程可能失效"
