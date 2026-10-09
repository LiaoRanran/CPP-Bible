# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_tool_manifest_696.py — 696 批次：``tools/gen_tool_manifest_696.py`` 单元测试。

覆盖点（对应 696 交付物 6）：
* ``classify`` 对命名信号清晰的文件路由正确，且对同一输入**确定性**；
* 在临时目录上跑生成器：分类**非空**、总数 == ``tools/*.py`` 数量；
* **确定性**：同目录两次生成，除 ``generated_at`` 外逐字段一致；
* CLI 落盘路径：``main([...])`` 写出合法 JSON。

注意：真实 ``tools/*.py`` 数量会随其他批次增删而变，故**断言用运行时 glob 计数**，
不写死数字。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import gen_tool_manifest_696 as G  # noqa: E402

REPO_TOOLS = Path(__file__).resolve().parent.parent / "tools"


def _write(path: Path, text: str = "") -> None:
    path.write_text(text, encoding="utf-8")


# ── classify ────────────────────────────────────────────────────────────────
def test_classify_routes_by_name_signal() -> None:
    assert G.classify("verify_paper_numbers.py") == "verification"
    assert G.classify("consistency_check.py") == "verification"
    assert G.classify("gate_engine.py") == "verification"
    assert G.classify("queyi_common.py") == "utils"
    assert G.classify("path_config_625.py") == "utils"
    assert G.classify("human_review_dashboard.py") == "visualization"
    assert G.classify("web_data_653.py") == "visualization"
    assert G.classify("612_baseline.py") == "batch"
    assert G.classify("coverage_probe_batch_634.py") == "batch"
    assert G.classify("analyze_692_environment.py") == "analysis"
    assert G.classify("totally_unlabeled_thing.py") == "analysis"


def test_classify_is_deterministic_and_in_domain() -> None:
    name = "audit_676k_integrity.py"
    first = G.classify(name)
    assert first == G.classify(name)
    assert first in G.CATEGORY_ORDER


def test_scan_routes_synthetic_tools_dir(tmp_path: Path) -> None:
    for fn in ("verify_a.py", "check_b.py", "common_c.py", "plot_d.py",
               "700_e.py", "mystery_f.py"):
        _write(tmp_path / fn)
    cats = G.scan_tools(tmp_path)
    assert cats["verification"] == ["check_b.py", "verify_a.py"]
    assert cats["utils"] == ["common_c.py"]
    assert cats["visualization"] == ["plot_d.py"]
    assert cats["batch"] == ["700_e.py"]
    assert cats["analysis"] == ["mystery_f.py"]


# ── build_manifest 结构 / 确定性 ─────────────────────────────────────────────
def test_manifest_all_categories_non_empty() -> None:
    manifest = G.build_manifest(REPO_TOOLS, generated_at="FIXED")
    for key in G.CATEGORY_ORDER:
        assert manifest["categories"][key], f"分类 {key} 为空"
        assert manifest["counts"][key] == len(manifest["categories"][key])


def test_manifest_count_equals_tools_py_count() -> None:
    manifest = G.build_manifest(REPO_TOOLS, generated_at="FIXED")
    expected = len(list(REPO_TOOLS.glob("*.py")))
    assert manifest["count"] == expected


def test_manifest_is_deterministic_across_runs() -> None:
    a = G.build_manifest(REPO_TOOLS)
    b = G.build_manifest(REPO_TOOLS)
    for field in ("count", "counts", "categories", "generated_by"):
        assert a[field] == b[field], f"字段 {field} 两次生成不一致"


def test_manifest_fixed_timestamp_fully_equal() -> None:
    a = G.build_manifest(REPO_TOOLS, generated_at="FIXED")
    b = G.build_manifest(REPO_TOOLS, generated_at="FIXED")
    assert a == b


# ── CLI 落盘 ────────────────────────────────────────────────────────────────
def test_cli_writes_valid_json_to_out(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    _write(src / "verify_x.py")
    _write(src / "analyze_y.py")
    out = tmp_path / "manifest.json"

    rc = G.main(["--tools-dir", str(src), "--out", str(out)])
    assert rc == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["count"] == 2
    assert data["counts"]["verification"] == 1
    assert data["counts"]["analysis"] == 1
    assert data["generated_by"] == "tools/gen_tool_manifest_696.py"
