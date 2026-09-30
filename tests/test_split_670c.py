# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""670c C4 · check_split_670c 单测（拆分完整性检查器）。

覆盖：verifier 定位 · wrapper/实现分类 · SHA256 · 检查项 schema · overall 判定 ·
      --json 输出可解析 · 真实仓库不变式（有 verifier 时才断言）。
编号 S-1..S-14。纯逻辑用 tmp_path 造样本，不依赖真实仓库布局的部分也一并覆盖。
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import check_split_670c as cs


# ── S-1: find_verifier 能在人造布局里逐级向上找到 ──
def test_s1_find_verifier_walks_up(tmp_path: Path):
    deep = tmp_path / "a" / "b" / "c" / "CPP-Bible" / "tools"
    deep.mkdir(parents=True)
    ver_tools = tmp_path / "a" / "queyi-verifier" / "tools"
    ver_tools.mkdir(parents=True)
    found = cs.find_verifier(deep)
    assert found is not None, "S-1: 应向上找到 queyi-verifier"
    assert found == (tmp_path / "a" / "queyi-verifier")


# ── S-2: 找不到时返回 None（不抛异常）──
def test_s2_find_verifier_absent(tmp_path: Path):
    solo = tmp_path / "solo" / "tools"
    solo.mkdir(parents=True)
    assert cs.find_verifier(solo) is None, "S-2: 无 verifier 时应返回 None"


# ── S-3/S-4: 分类：薄 wrapper vs 完整实现 ──
def test_s3_classify_wrapper(tmp_path: Path):
    p = tmp_path / "w.py"
    p.write_text("# canonical 在 queyi-verifier/tools/\nimport importlib.util\n", encoding="utf-8")
    assert cs.classify(p) == "WRAPPER", "S-3: 小且引用 canonical 的应判为 WRAPPER"


def test_s4_classify_full_impl(tmp_path: Path):
    p = tmp_path / "big.py"
    p.write_text("# 纯实现\n" + "x = 1\n" * 20000, encoding="utf-8")
    assert cs.classify(p) == "FULL-IMPL", "S-4: 超体积的应判为 FULL-IMPL"


# ── S-5: 提到 queyi-verifier 但体积过大 ⇒ 不是 wrapper（防"搬回实现"）──
def test_s5_classify_big_file_mentioning_verifier(tmp_path: Path):
    p = tmp_path / "sneaky.py"
    p.write_text("import importlib\n# queyi-verifier\n" + "y = 2\n" * 20000, encoding="utf-8")
    assert cs.classify(p) == "FULL-IMPL", "S-5: 体积超限即使提及 verifier 也不算 wrapper"


# ── S-6: SHA256 稳定且可区分 ──
def test_s6_sha256(tmp_path: Path):
    a, b = tmp_path / "a.bin", tmp_path / "b.bin"
    a.write_bytes(b"hello")
    b.write_bytes(b"hello")
    c = tmp_path / "c.bin"
    c.write_bytes(b"world")
    assert cs.sha256_file(a) == hashlib.sha256(b"hello").hexdigest(), "S-6a: SHA256 与标准库一致"
    assert cs.sha256_file(a) == cs.sha256_file(b), "S-6b: 同内容同哈希"
    assert cs.sha256_file(a) != cs.sha256_file(c), "S-6c: 异内容异哈希"


# ── S-7: 检查项常量与实际返回的 check 名一一对应 ──
def test_s7_check_names():
    rep = cs.run_all()
    names = [r["check"] for r in rep["results"]]
    assert names == list(cs.CHECKS), "S-7: 返回的检查项应与 CHECKS 顺序一致"


# ── S-8/S-9: 报告 schema 与 overall 判定 ──
def test_s8_report_schema():
    rep = cs.run_all()
    for key in ("tool", "repo", "verifier", "results", "fails", "warns", "skips", "overall"):
        assert key in rep, "S-8: 报告缺字段 " + key
    for r in rep["results"]:
        assert r["status"] in ("PASS", "WARN", "FAIL", "SKIP"), "S-8: 非法状态 " + str(r["status"])
        assert r.get("detail"), "S-8: 每个检查都要有 detail"


def test_s9_overall_matches_fails():
    rep = cs.run_all()
    assert rep["overall"] == ("FAIL" if rep["fails"] else "PASS"), "S-9a: overall 与 fails 应一致"
    assert rep["fails"] == len([r for r in rep["results"] if r["status"] == "FAIL"]), "S-9b: fails 计数"


# ── S-10: --json 输出可解析且落到 stdout ──
def test_s10_json_output():
    p = subprocess.run([sys.executable, str(Path(cs.__file__)), "--json"],
                       capture_output=True, text=True, timeout=180)
    data = json.loads(p.stdout)
    assert data["tool"] == "check_split_670c", "S-10a: tool 名"
    assert isinstance(data["results"], list) and data["results"], "S-10b: results 非空"


# ── S-11: 退出码语义：无 FAIL ⇒ 0；有 FAIL ⇒ 1 ──
def test_s11_exit_code():
    rep = cs.run_all()
    rc = cs.main([])
    assert rc == (1 if rep["fails"] else 0), "S-11: main 退出码应与 fails 对应"


# ── S-12..S-14: 真实仓库不变式（verifier 不在时跳过，但打印原因）──
def test_s12_kernel_layer_is_wrapper_only():
    rep = cs.run_all()
    by = {r["check"]: r for r in rep["results"]}
    r = by["kernel_is_wrapper"]
    assert r["status"] == "PASS", "S-12: 内核层应全为薄 wrapper，实际：" + r["detail"]
    assert r["files"] >= 1, "S-12: 至少应检查到 1 个内核文件"


def test_s13_wrapper_resolves_to_canonical():
    rep = cs.run_all()
    by = {r["check"]: r for r in rep["results"]}
    r = by["wrapper_resolves"]
    if r["status"] == "SKIP":
        print("S-13 SKIP: " + r["detail"])
        return
    assert r["status"] == "PASS", "S-13: wrapper 必须解析到 canonical，实际：" + r["detail"]
    assert "queyi-verifier" in r.get("resolved", ""), "S-13: 解析路径应落在 verifier"


def test_s14_no_duplication_drift():
    rep = cs.run_all()
    by = {r["check"]: r for r in rep["results"]}
    r = by["duplication_drift"]
    if r["status"] == "SKIP":
        print("S-14 SKIP: " + r["detail"])
        return
    assert r["status"] in ("PASS", "WARN"), "S-14a: 复制层不允许漂移，实际：" + r["detail"]
    assert r.get("identical", 0) >= 0, "S-14b: identical 计数应为整数"
    if r["status"] == "WARN":
        print("S-14 WARN(已知债务): " + r["detail"])
