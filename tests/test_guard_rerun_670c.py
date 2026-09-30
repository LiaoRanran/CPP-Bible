# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_guard_rerun_670c.py — 670c D2 守卫的回归测试（>=8 断言）。

纪律：每条判定都要有**正例 + 反例**。尤其 STALE（改了代码没重跑产物）这一条——
若改了源码仍报绿，等于本门禁根本没进射程（667 两次翻车「产物是旧代码结论」的形态）。
所有用例在 tmp_path 里构造最小仓库，绝不触碰真实仓库。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import guard_rerun_670c as Guard  # noqa: E402

# ─────────────────────────────────────────────────────────────────────────────
# helper：最小仓库（5 个核心工具的源码 + 全部声明产物）
# ─────────────────────────────────────────────────────────────────────────────

def mk_root(tmp: Path) -> Path:
    for name, spec in Guard.CORE_TOOLS.items():
        src = tmp / spec["src"]
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(f"def {name}_fn():\n    return 1\n", encoding="utf-8")
        for rel in spec["products"]:
            p = tmp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('{"v": 1}\n', encoding="utf-8")
    return tmp


def bp_of(tmp: Path) -> Path:
    return tmp / Guard.DEFAULT_BASELINE


def arm(tmp: Path) -> Path:
    """--update 标定基线（用例公共前置）。"""
    assert Guard.main(["--root", str(tmp), "--baseline", str(bp_of(tmp)), "--update"]) == 0
    return bp_of(tmp)


def verdict(res: dict, tool: str) -> dict:
    return next(v for v in res["verdicts"] if v["tool"] == tool)


# ─────────────────────────────────────────────────────────────────────────────
# ① 哈希稳定性（裸 sha256 + AST 语义哈希）
# ─────────────────────────────────────────────────────────────────────────────

def test_hashes_stable_and_semantic(tmp_path):
    p = tmp_path / "m.py"
    p.write_text("def f():\n    return 1\n", encoding="utf-8")
    assert Guard.sha256_file(p) == Guard.sha256_file(p), "裸 sha256 不稳定"
    assert Guard.semantic_hash(p) == Guard.semantic_hash(p), "语义哈希不稳定"
    raw1, ast1 = Guard.sha256_file(p), Guard.semantic_hash(p)
    p.write_text("# 只加一行注释\ndef f():\n    return 1\n", encoding="utf-8")
    assert Guard.sha256_file(p) != raw1, "注释变更应改变裸哈希"
    assert Guard.semantic_hash(p) == ast1, "注释变更不该改变语义哈希（否则门禁沦为狼来了）"
    p.write_text("def f():\n    return 2\n", encoding="utf-8")
    assert Guard.semantic_hash(p) != ast1, "语义变更必须改变语义哈希"


def test_missing_file_hashes_are_none(tmp_path):
    ghost = tmp_path / "nope.py"
    assert Guard.sha256_file(ghost) is None, "缺失文件必须返回 None 而不是抛异常"
    assert Guard.semantic_hash(ghost) is None


# ─────────────────────────────────────────────────────────────────────────────
# ② 四种组合：源码×产物
# ─────────────────────────────────────────────────────────────────────────────

def test_source_changed_product_unchanged_is_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / Guard.CORE_TOOLS["gate_engine"]["src"]).write_text(
        "def gate_engine_fn():\n    return 2\n", encoding="utf-8")
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "gate_engine")
    assert v["status"] == Guard.STALE and v["severity"] == Guard.BLOCK, "改了代码没重跑产物却未标红"
    assert v["src_changed"] is True and v["products_changed"] == []
    assert res["overall"] == "RED"
    assert Guard.main(["--root", str(root), "--baseline", str(bp_of(root))]) == 1, \
        "发现 STALE 时退出码必须非 0"


def test_source_and_product_changed_passes(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    spec = Guard.CORE_TOOLS["cppbible"]
    (root / spec["src"]).write_text("def cppbible_fn():\n    return 3\n", encoding="utf-8")
    (root / spec["products"][0]).write_text('{"v": 2}\n', encoding="utf-8")
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "cppbible")
    assert v["status"] == Guard.RERUN and v["severity"] == Guard.PASS, "改了也重跑了却判红 ⇒ 误报"
    assert v["products_changed"] == [spec["products"][0]]
    assert res["overall"] == "PASS"


def test_product_changed_without_source_change_is_not_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    spec = Guard.CORE_TOOLS["poison_drill"]
    (root / spec["products"][0]).write_text('{"v": 9}\n', encoding="utf-8")
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "poison_drill")
    assert v["status"] == Guard.RERUN_ONLY and v["severity"] == Guard.PASS
    assert res["overall"] == "PASS", "源码没动、产物刷新过，不该判红"


# ─────────────────────────────────────────────────────────────────────────────
# ③ 基线生命周期
# ─────────────────────────────────────────────────────────────────────────────

def test_first_run_without_baseline_is_unarmed(tmp_path):
    root = mk_root(tmp_path)
    res = Guard.evaluate(root, bp_of(root))
    assert res["overall"] == "UNARMED" and res["armed"] is False, "无基线必须显式标为未进射程"
    assert res["baseline_found"] is False and res["verdicts"] == []
    assert Guard.main(["--root", str(root), "--baseline", str(bp_of(root))]) == 2, \
        "无基线必须返回 2（未进射程 ≠ 通过）"


def test_update_writes_baseline(tmp_path):
    root = mk_root(tmp_path)
    assert not bp_of(root).is_file()
    assert Guard.main(["--root", str(root), "--baseline", str(bp_of(root)), "--update"]) == 0
    base = json.loads(bp_of(root).read_text(encoding="utf-8"))
    assert base["schema"] == Guard.SCHEMA
    assert sorted(base["tools"]) == sorted(Guard.CORE_TOOLS)
    one = base["tools"]["gate_engine"]
    assert one["src_sha256"] and one["src_ast_sha256"], "基线必须同时记裸哈希与语义哈希"
    assert res_overall_ok(root), "标定后应立刻对账通过"


def res_overall_ok(root: Path) -> bool:
    """标定后立刻复算：应当 PASS（否则基线写歪了）。"""
    return bool(Guard.evaluate(root, bp_of(root))["overall"] == "PASS")


# ─────────────────────────────────────────────────────────────────────────────
# ④ 缺失文件容错 + 射程自检
# ─────────────────────────────────────────────────────────────────────────────

def test_missing_source_is_tolerated_as_warn(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / Guard.CORE_TOOLS["poison_drill"]["src"]).unlink()
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "poison_drill")
    assert v["status"] == Guard.SRC_MISSING and v["severity"] == Guard.WARN
    assert res["overall"] == "PASS", "源码缺失属「无法判定」，不该直接判红"


def test_missing_product_is_warn_not_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    spec = Guard.CORE_TOOLS["atom_evidence_replay"]
    (root / spec["products"][0]).unlink()
    (root / spec["src"]).write_text("def atom_evidence_replay_fn():\n    return 4\n",
                                    encoding="utf-8")
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "atom_evidence_replay")
    assert v["status"] == Guard.PRODUCT_MISSING and v["severity"] == Guard.WARN, \
        "产物缺失应降级为「无法判定」而非判红"


def test_toolchain_has_no_product_so_no_range(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    spec = Guard.CORE_TOOLS["toolchain"]
    assert spec["products"] == [], "toolchain 是纯只读库，不该假装有产物"
    (root / spec["src"]).write_text("def toolchain_fn():\n    return 5\n", encoding="utf-8")
    res = Guard.evaluate(root, bp_of(root))
    v = verdict(res, "toolchain")
    assert v["status"] == Guard.NO_PRODUCT and v["severity"] == Guard.WARN


def test_registered_core_tools_are_real(tmp_path):
    """射程自检：注册表里的 5 个源码必须在本仓真实存在，且出现在信任根清单里。"""
    assert len(Guard.CORE_TOOLS) == 5
    for name, spec in Guard.CORE_TOOLS.items():
        assert (ROOT / spec["src"]).is_file(), f"{name} 的源码路径不存在：{spec['src']}"
    checksums = (ROOT / "tools" / ".tool_checksums").read_text(encoding="utf-8")
    for spec in Guard.CORE_TOOLS.values():
        assert Path(spec["src"]).name in checksums, f"{spec['src']} 不在 tools/.tool_checksums"


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 机读输出 schema
# ─────────────────────────────────────────────────────────────────────────────

def test_json_output_schema(tmp_path, capsys):
    root = mk_root(tmp_path)
    arm(root)
    capsys.readouterr()          # 丢掉 arm() 的人读输出，只留 --json 的机读输出
    assert Guard.main(["--root", str(root), "--baseline", str(bp_of(root)), "--json"]) == 0
    out = capsys.readouterr().out
    d = json.loads(out)
    for k in ("schema", "tool", "overall", "counts", "verdicts", "baseline_found"):
        assert k in d, f"json 缺字段 {k}"
    assert d["counts"]["tools"] == len(Guard.CORE_TOOLS) == 5
    assert d["schema"] == Guard.SCHEMA
    assert all("status" in v and "severity" in v for v in d["verdicts"])
