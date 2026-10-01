# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_guard_rerun_671a.py — 671a A 的回归测试（>=30 例）。

纪律（与 670c D2 同款）：每条判定都要有**正例 + 反例**。三条最关键的不可漏：
  1. 改了检测器**没重跑**产物 ⇒ STALE + block + exit 1（这是 667 两次翻车的形态）；
  2. 只改注释 / 只改局部变量名 ⇒ **不许**判红（否则门禁变成狼来了）；
  3. 三方数字（产物↔论文↔前端）任一不一致 ⇒ block。
所有用例都在 tmp_path 里构造最小仓库，绝不触碰真实仓库。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import guard_rerun_671a as G  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# helper：最小仓库
# ─────────────────────────────────────────────────────────────────────────────

DET_SRC = "def detect_a(x):\n    total = x + 1\n    return total\n"
DEP_SRC = "def judge(x):\n    val = x * 2\n    return val\n"


def wj(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")


def wt(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def mk_root(tmp: Path, *, rate_k: int = 14, rate_n: int = 16, strict: bool = True,
            advisory: bool = False) -> Path:
    """最小仓库：2 个检测器（det_a 带 dep_a；det_b 无产物）+ 产物 + 三方数字配置。"""
    wt(tmp / "tools" / "det_a.py", DET_SRC)
    wt(tmp / "tools" / "dep_a.py", DEP_SRC)
    wt(tmp / "tools" / "det_b.py", "def b():\n    return 1\n")
    wj(tmp / "data" / "prod_a.json", {"catch": rate_k, "miss": rate_n - rate_k,
                                      "detect_rate_pct": round(rate_k / rate_n * 100, 1)})
    wj(tmp / "data" / "prod_b.json", {"killed": 1, "survived": 0})
    dets = [
        {"id": "det_a", "src": "tools/det_a.py", "deps": ["tools/dep_a.py"],
         "products": ["data/prod_a.json"] if strict else [{"path": "data/prod_a.json",
                                                            "strict": False}],
         "why": "测试用检测器 A"},
        ({"id": "det_b", "src": "tools/det_b.py", "deps": [], "products": [],
          "why": "无产物的检测器（射程自检）"} if not advisory else
         {"id": "det_b", "src": "tools/det_b.py", "deps": [], "products": [{"path": "data/prod_b.json",
                                                                            "strict": False}],
          "why": "advisory 产物"}),
    ]
    wj(tmp / "data" / "guard_detector_files_671a.json",
       {"schema": "t", "detectors": dets})
    wj(tmp / "data" / "guard_artifacts_671a.json", {
        "schema": "t", "tolerance_pp": 0.5,
        "metrics": [{
            "key": "rate_a", "label": "测试率", "kind": "rate", "unit": "%",
            "artifact": {"path": "data/prod_a.json", "k": "catch", "n_sum": ["catch", "miss"],
                         "stored": "detect_rate_pct"},
            "paper": {"path": "research/paper.md", "k": rate_k, "n": rate_n},
            "web": [{"path": "web/data/metrics.json", "pointer": "metrics.rate_a"}],
        }],
    })
    wt(tmp / "research" / "paper.md",
       f"检出率 {round(rate_k / rate_n * 100, 1)}%（{rate_k}/{rate_n}，95% CI）。\n")
    wj(tmp / "web" / "data" / "metrics.json",
       {"metrics": {"rate_a": round(rate_k / rate_n * 100, 1)}})
    return tmp


def set_rate_consistent(root: Path, k: int, n: int) -> None:
    """把产物率改掉时，**同时**改配置/论文/前端 —— 否则三方不一致才是对的（红）。

    真实工作流同理：产物口径一变，配置里的论文 k/n 与论文/前端都要跟上，
    本门禁不接受"产物改了、论文还写旧数"。
    """
    pct = round(k / n * 100, 1)
    wj(root / "data" / "prod_a.json", {"catch": k, "miss": n - k, "detect_rate_pct": pct})
    cfg = json.loads((root / "data" / "guard_artifacts_671a.json").read_text(encoding="utf-8"))
    cfg["metrics"][0]["paper"] = {"path": "research/paper.md", "k": k, "n": n}
    wj(root / "data" / "guard_artifacts_671a.json", cfg)
    wt(root / "research" / "paper.md", f"检出率 {pct}%（{k}/{n}）。\n")
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"rate_a": pct}})


def bp(tmp: Path) -> Path:
    return tmp / G.DEFAULT_BASELINE


def arm(tmp: Path) -> Path:
    assert G.main(["--root", str(tmp), "--init"]) == 0
    return bp(tmp)


def ev(tmp: Path, **kw):
    return G.evaluate(tmp, bp(tmp), include_core=False, **kw)


def v_of(res: dict, did: str) -> dict:
    return next(v for v in res["verdicts"] if v["detector"] == did)


def m_of(res: dict, key: str = "rate_a") -> dict:
    return next(m for m in res["three_way"]["metrics"] if m["key"] == key)


# ─────────────────────────────────────────────────────────────────────────────
# ① 三种指纹：注释/重命名不触发，语义变更必触发
# ─────────────────────────────────────────────────────────────────────────────

def test_three_hashes_stable(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    assert G.sha256_file(p) == G.sha256_file(p)
    assert G.ast_hash(p) == G.ast_hash(p)
    assert G.judgment_hash(p) == G.judgment_hash(p)


def test_comment_only_change_does_not_move_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    raw0, j0 = G.sha256_file(p), G.judgment_hash(p)
    wt(p, "# 新增一行注释\n" + DET_SRC)
    assert G.sha256_file(p) != raw0, "裸哈希应当变（诊断层）"
    assert G.judgment_hash(p) == j0, "注释变更不许改判据指纹（否则狼来了）"


def test_whitespace_only_change_does_not_move_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    j0 = G.judgment_hash(p)
    wt(p, DET_SRC.replace("\n", "\n\n"))
    assert G.judgment_hash(p) == j0


def test_local_rename_does_not_move_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    ast0, j0 = G.ast_hash(p), G.judgment_hash(p)
    wt(p, "def detect_a(x):\n    acc = x + 1\n    return acc\n")
    assert G.ast_hash(p) != ast0, "AST 层应当看到名字变化"
    assert G.judgment_hash(p) == j0, "纯局部重命名不该要求重跑"


def test_logic_change_moves_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    j0 = G.judgment_hash(p)
    wt(p, DET_SRC.replace("x + 1", "x + 2"))
    assert G.judgment_hash(p) != j0, "改逻辑必须改判据指纹"


def test_function_name_change_moves_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, DET_SRC)
    j0 = G.judgment_hash(p)
    wt(p, DET_SRC.replace("detect_a", "detect_aa"))
    assert G.judgment_hash(p) != j0, "模块级函数名不参与归一 ⇒ 改了必须重跑"


def test_module_constant_change_moves_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, "OPT = ('-O0', '-O2')\ndef f(x):\n    y = x\n    return y\n")
    j0 = G.judgment_hash(p)
    wt(p, "OPT = ('-O1',)\ndef f(x):\n    y = x\n    return y\n")
    assert G.judgment_hash(p) != j0, "模块常量改了（口径变了）必须重跑"


def test_string_literal_change_moves_judgment(tmp_path):
    p = tmp_path / "m.py"
    wt(p, 'KEY = "verdict"\ndef f(x):\n    return x\n')
    j0 = G.judgment_hash(p)
    wt(p, 'KEY = "verdicts"\ndef f(x):\n    return x\n')
    assert G.judgment_hash(p) != j0


def test_syntax_error_and_missing_file_are_none(tmp_path):
    p = tmp_path / "bad.py"
    wt(p, "def f(:\n")
    assert G.judgment_hash(p) is None and G.ast_hash(p) is None
    ghost = tmp_path / "nope.py"
    assert G.sha256_file(ghost) is None and G.ast_hash(ghost) is None
    assert G.judgment_hash(ghost) is None


def test_fingerprint_aggregates_components(tmp_path):
    a = tmp_path / "a.py"
    wt(a, DET_SRC)
    fp1, comps = G.fingerprint([a])
    assert fp1 and len(comps) == 1
    wt(a, DET_SRC.replace("x + 1", "x + 3"))
    fp2, _ = G.fingerprint([a])
    assert fp1 != fp2
    assert G.fingerprint([a, tmp_path / "ghost.py"])[0] is None, "缺组件 ⇒ 组合指纹不可用"


def test_dep_change_moves_combined_fingerprint(tmp_path):
    """deps 必须进射程：661 的 detect 被 3_665 复用，只盯 src 会漏掉换判据。"""
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "tools" / "dep_a.py", DEP_SRC.replace("x * 2", "x * 3"))
    res = ev(root)
    assert res["overall"] == "RED"
    assert v_of(res, "det_a")["status"] == G.STALE


# ─────────────────────────────────────────────────────────────────────────────
# ② 检测器 × 产物 状态机
# ─────────────────────────────────────────────────────────────────────────────

def test_init_then_immediate_pass(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    res = ev(root)
    assert res["overall"] == "PASS" and res["armed"] is True
    assert G.main(["--root", str(root)]) == 0


def test_detector_changed_without_rerun_is_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "tools" / "det_a.py", DET_SRC.replace("x + 1", "x + 9"))
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["status"] == G.STALE and v["severity"] == G.BLOCK, "改了检测器没重跑却报绿 ⇒ 门禁没射程"
    assert v["judgment_changed"] is True and v["products_changed"] == []
    assert res["overall"] == "RED"
    assert G.main(["--root", str(root)]) == 1, "STALE 必须 exit 1"


def test_detector_changed_and_product_rerun_passes(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "tools" / "det_a.py", DET_SRC.replace("x + 1", "x + 9"))
    set_rate_consistent(root, 15, 16)
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["status"] == G.RERUN and v["severity"] == G.PASS
    assert v["products_changed"] == ["data/prod_a.json"]
    assert res["overall"] == "PASS"


def test_comment_only_edit_is_not_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "tools" / "det_a.py", "# 只加注释\n" + DET_SRC)
    res = ev(root)
    assert v_of(res, "det_a")["status"] == G.OK
    assert res["overall"] == "PASS", "只改注释不该判红"


def test_local_rename_only_is_not_red(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "tools" / "det_a.py", "def detect_a(x):\n    acc = x + 1\n    return acc\n")
    res = ev(root)
    assert v_of(res, "det_a")["status"] == G.OK
    assert res["overall"] == "PASS", "纯局部重命名不该判红"


def test_product_changed_alone_is_rerun_only(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    set_rate_consistent(root, 13, 16)          # 判据没动，只是产物刷新
    res = ev(root)
    assert v_of(res, "det_a")["status"] == G.RERUN_ONLY
    assert res["overall"] == "PASS", "判据没动、产物刷新过 ⇒ 不该红"


def test_product_changed_without_paper_update_is_red(tmp_path):
    """产物换了口径而论文/前端没跟上 ⇒ 三方不一致，必须红（不许悄悄落后）。"""
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "data" / "prod_a.json", {"catch": 13, "miss": 3, "detect_rate_pct": 81.2})
    res = ev(root)
    assert res["overall"] == "RED"
    assert m_of(res)["severity"] == G.BLOCK


def test_missing_product_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / "data" / "prod_a.json").unlink()
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["status"] == G.PRODUCT_MISSING and v["severity"] == G.BLOCK
    assert res["overall"] == "RED", "产物缺失无从对账 ⇒ fail-closed"


def test_missing_source_is_warn_only(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / "tools" / "det_a.py").unlink()
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["status"] == G.SRC_MISSING and v["severity"] == G.WARN
    assert res["overall"] == "PASS", "源码缺失属无法判定，不假装覆盖也不判红"


def test_no_product_is_warn(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    res = ev(root)
    v = v_of(res, "det_b")
    assert v["status"] == G.NO_PRODUCT and v["severity"] == G.WARN


def test_advisory_product_only_warns(tmp_path):
    root = mk_root(tmp_path, strict=False, advisory=True)
    arm(root)
    wt(root / "tools" / "det_a.py", DET_SRC.replace("x + 1", "x + 7"))
    wt(root / "tools" / "det_b.py", "def b():\n    return 2\n")
    res = ev(root)
    assert v_of(res, "det_a")["status"] == G.ADVISORY_STALE
    assert v_of(res, "det_a")["severity"] == G.WARN
    assert res["overall"] == "PASS", "advisory 产物只提醒（慢操作不能天天跑）"


def test_new_detector_without_baseline_entry_warns(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    cfg = json.loads((root / "data" / "guard_detector_files_671a.json").read_text(encoding="utf-8"))
    cfg["detectors"].append({"id": "det_c", "src": "tools/det_a.py", "deps": [],
                             "products": ["data/prod_b.json"], "why": "新注册"})
    wj(root / "data" / "guard_detector_files_671a.json", cfg)
    res = ev(root)
    v = v_of(res, "det_c")
    assert v["status"] == G.NO_BASELINE_ENTRY and v["severity"] == G.WARN
    assert res["overall"] == "PASS"


def test_no_baseline_is_unarmed_exit_2(tmp_path):
    root = mk_root(tmp_path)
    res = ev(root)
    assert res["overall"] == "UNARMED" and res["armed"] is False
    assert all(v["status"] == G.NO_BASELINE_ENTRY for v in res["verdicts"])
    assert G.main(["--root", str(root)]) == 2, "未进射程 ≠ 通过"


def test_init_writes_baseline_with_snapshot(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    base = json.loads(bp(root).read_text(encoding="utf-8"))
    assert base["schema"] == G.SCHEMA
    assert sorted(base["detectors"]) == ["det_a", "det_b"]
    one = base["detectors"]["det_a"]
    assert one["judgment_sha256"] and one["src_sha256"] and one["src_ast_sha256"]
    assert "data/prod_a.json" in one["products"]
    assert "fresh" in one["products"]["data/prod_a.json"]
    assert "rate_a" in base["three_way"], "基线要记三方数字现值"


def test_judgment_fingerprint_includes_deps_in_baseline(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    base = json.loads(bp(root).read_text(encoding="utf-8"))
    assert base["detectors"]["det_a"]["deps"] == ["tools/dep_a.py"]
    assert len(base["detectors"]["det_a"]["component_judgment_sha256"]) == 2


# ─────────────────────────────────────────────────────────────────────────────
# ③ 产物新鲜度（mtime 轴）
# ─────────────────────────────────────────────────────────────────────────────

def test_fresh_product_is_ok(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    res = ev(root)
    f = v_of(res, "det_a")["freshness"]
    assert "data/prod_a.json" in f["fresh"] and f["stale"] == []


def test_product_made_older_than_detector_is_freshness_stale(tmp_path):
    root = mk_root(tmp_path)
    # 先让产物比检测器新，标定基线（基线记 fresh=true）
    det = root / "tools" / "det_a.py"
    prod = root / "data" / "prod_a.json"
    now = time.time()
    os.utime(det, (now - 500, now - 500))
    os.utime(prod, (now, now))
    arm(root)
    # 再把检测器改新（语义不变 ⇒ 判据指纹不变，只有 mtime 轴能看见）
    os.utime(det, (now + 500, now + 500))
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["judgment_changed"] is False, "本用例专门测 mtime 轴（判据没变）"
    assert v["status"] == G.FRESHNESS_STALE and v["severity"] == G.BLOCK
    assert res["overall"] == "RED"


def test_legacy_unfresh_is_registered_not_red(tmp_path):
    """基线时即不新鲜（如 checkout 顺序）⇒ 存量缺口，只登记，不判红。"""
    root = mk_root(tmp_path)
    det = root / "tools" / "det_a.py"
    prod = root / "data" / "prod_a.json"
    now = time.time()
    os.utime(det, (now, now))
    os.utime(prod, (now - 500, now - 500))
    arm(root)
    res = ev(root)
    v = v_of(res, "det_a")
    assert v["status"] == G.OK and v["severity"] == G.PASS
    assert v["freshness"]["legacy"] == ["data/prod_a.json"]
    assert any("存量缺口" in n for n in v["notes"])
    assert res["overall"] == "PASS"


def test_legacy_pair_tightens_after_rerun(tmp_path):
    """存量缺口在产物重跑后应转为严格判定（不会永久豁免）。"""
    root = mk_root(tmp_path)
    det = root / "tools" / "det_a.py"
    prod = root / "data" / "prod_a.json"
    now = time.time()
    os.utime(det, (now, now))
    os.utime(prod, (now - 500, now - 500))
    arm(root)
    os.utime(prod, (now + 500, now + 500))          # 重跑产物
    wj(prod, {"catch": 14, "miss": 2, "detect_rate_pct": 87.5})
    os.utime(prod, (now + 500, now + 500))
    res = ev(root)
    assert v_of(res, "det_a")["freshness"]["stale"] == []
    assert v_of(res, "det_a")["freshness"]["legacy"] == []


# ─────────────────────────────────────────────────────────────────────────────
# ④ 三方数字一致性
# ─────────────────────────────────────────────────────────────────────────────

def test_three_way_consistent(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    res = ev(root)
    m = m_of(res)
    assert m["status"] == G.CONSISTENT and m["severity"] == G.PASS
    assert m["artifact"]["k"] == 14 and m["artifact"]["n"] == 16


def test_paper_mismatch_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wt(root / "research" / "paper.md", "检出率 80.0%（14/16）。\n")
    res = ev(root)
    m = m_of(res)
    assert m["status"] == G.MISMATCH and m["severity"] == G.BLOCK
    assert res["overall"] == "RED"


def test_web_mismatch_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"rate_a": 80.0}})
    res = ev(root)
    assert m_of(res)["status"] == G.MISMATCH


def test_web_pointer_missing_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"other": 1}})
    m = m_of(ev(root))
    assert m["severity"] == G.BLOCK and "指针取不到" in m["message"]


def test_web_file_missing_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / "web" / "data" / "metrics.json").unlink()
    assert m_of(ev(root))["severity"] == G.BLOCK


def test_artifact_missing_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / "data" / "prod_a.json").unlink()
    m = m_of(ev(root))
    assert m["status"] == G.SOURCE_MISSING and m["severity"] == G.BLOCK


def test_paper_missing_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    (root / "research" / "paper.md").unlink()
    assert m_of(ev(root))["severity"] == G.BLOCK


def test_config_kn_stale_against_artifact_is_block(tmp_path):
    """配置里写的论文 k/n 与产物现算不符 ⇒ 红（防配置腐烂）。"""
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "data" / "prod_a.json", {"catch": 7, "miss": 1, "detect_rate_pct": 87.5})
    m = m_of(ev(root))
    assert m["severity"] == G.BLOCK and "配置声明" in m["message"]


def test_stored_rate_inconsistent_is_block(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "data" / "prod_a.json", {"catch": 14, "miss": 2, "detect_rate_pct": 50.0})
    m = m_of(ev(root))
    assert m["severity"] == G.BLOCK and "不自洽" in m["message"]


def test_tolerance_boundary_exactly_half_pp_passes(tmp_path):
    root = mk_root(tmp_path, rate_k=87, rate_n=200)      # 43.5%
    arm(root)
    wt(root / "research" / "paper.md", "检出率 44.0%（87/200）。\n")   # +0.5pp
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"rate_a": 43.0}})   # -0.5pp
    res = ev(root, tol=0.5)
    assert m_of(res)["status"] == G.CONSISTENT, "正好 0.5pp 在容差内"


def test_tolerance_outside_is_block(tmp_path):
    root = mk_root(tmp_path, rate_k=87, rate_n=200)
    arm(root)
    wt(root / "research" / "paper.md", "检出率 44.1%（87/200）。\n")   # +0.6pp
    assert m_of(ev(root, tol=0.5))["severity"] == G.BLOCK


def test_fail_loud_on_zero_denominator(tmp_path):
    root = mk_root(tmp_path)
    arm(root)
    wj(root / "data" / "prod_a.json", {"catch": 0, "miss": 0, "detect_rate_pct": 0.0})
    m = m_of(ev(root))
    assert m["status"] == G.SOURCE_MISSING and "拒绝给率" in m["message"]


def test_count_kind_requires_exact_equality(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "data" / "rules.json", [{"r": i} for i in range(67)])
    cfg = json.loads((root / "data" / "guard_artifacts_671a.json").read_text(encoding="utf-8"))
    cfg["metrics"].append({
        "key": "rules_total", "label": "规则数", "kind": "count", "unit": "条",
        "artifact": {"path": "data/rules.json", "len": True},
        "paper": {"path": "research/paper.md", "pattern": "(\\d+)\\*\\*\\s*条规则"},
        "web": [{"path": "web/data/metrics.json", "pointer": "rules"}],
    })
    wj(root / "data" / "guard_artifacts_671a.json", cfg)
    wt(root / "research" / "paper.md", "系统现有 **67** 条规则。\n")
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"rate_a": 87.5}, "rules": 68})
    arm(root)
    m = m_of(ev(root), "rules_total")
    assert m["severity"] == G.BLOCK, "计数类差 1 也要红（不套用率的容差）"
    wj(root / "web" / "data" / "metrics.json", {"metrics": {"rate_a": 87.5}, "rules": 67})
    assert m_of(ev(root), "rules_total")["status"] == G.CONSISTENT


def test_newer_artifact_difference_is_pending_not_red(tmp_path):
    root = mk_root(tmp_path)
    cfg = json.loads((root / "data" / "guard_artifacts_671a.json").read_text(encoding="utf-8"))
    cfg["metrics"][0]["newer_artifact"] = {"path": "data/prod_new.json", "k": "catch",
                                           "n_sum": ["catch", "miss"], "owner": "671b"}
    wj(root / "data" / "guard_artifacts_671a.json", cfg)
    wj(root / "data" / "prod_new.json", {"catch": 17, "miss": 4})
    arm(root)
    res = ev(root)
    m = m_of(res)
    assert m["status"] == G.PENDING_NEWER and m["severity"] == G.WARN
    assert m["pending_newer"]["owner"] == "671b"
    assert res["overall"] == "PASS", "更新的那一轮只提示（论文更新归 671b），不判红"


def test_newer_artifact_equal_is_consistent(tmp_path):
    root = mk_root(tmp_path)
    cfg = json.loads((root / "data" / "guard_artifacts_671a.json").read_text(encoding="utf-8"))
    cfg["metrics"][0]["newer_artifact"] = {"path": "data/prod_new.json", "k": "catch",
                                           "n_sum": ["catch", "miss"]}
    wj(root / "data" / "guard_artifacts_671a.json", cfg)
    wj(root / "data" / "prod_new.json", {"catch": 14, "miss": 2})
    arm(root)
    assert m_of(ev(root))["status"] == G.CONSISTENT


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 配置缺失 / 自检 / 机读输出
# ─────────────────────────────────────────────────────────────────────────────

def test_missing_detector_config_is_exit_2(tmp_path):
    root = mk_root(tmp_path)
    (root / "data" / "guard_detector_files_671a.json").unlink()
    res = ev(root)
    assert res["configured"] is False and res["overall"] == "UNCONFIGURED"
    assert res["config"]["detectors_found"] is False
    assert G.main(["--root", str(root)]) == 2, "配置缺失必须显式报错（exit 2）"


def test_missing_artifacts_config_is_exit_2(tmp_path):
    root = mk_root(tmp_path)
    (root / "data" / "guard_artifacts_671a.json").unlink()
    assert G.main(["--root", str(root)]) == 2


def test_malformed_detector_entry_raises(tmp_path):
    root = mk_root(tmp_path)
    wj(root / "data" / "guard_detector_files_671a.json",
       {"detectors": [{"id": "x"}]})            # 缺 src
    try:
        G.load_detectors(root, G.DEFAULT_DETECTORS)
        raised = False
    except SystemExit:
        raised = True
    assert raised, "缺 src 的条目必须显式拒绝，而不是静默跳过"


def test_normalize_product_forms():
    assert G.normalize_product("a.json") == {"path": "a.json", "strict": True}
    assert G.normalize_product({"path": "a.json", "strict": False}) == {"path": "a.json",
                                                                        "strict": False}


def test_verify_config_flags_missing_source(tmp_path):
    root = mk_root(tmp_path)
    (root / "tools" / "det_a.py").unlink()
    reg, _ = G.load_detectors(root, G.DEFAULT_DETECTORS)
    ver = G.verify_config(root, reg)
    assert ver["ok"] is False
    assert any(p["kind"] == "src-missing" for p in ver["problems"])


def test_verify_config_flags_unreferenced_product(tmp_path):
    root = mk_root(tmp_path)
    reg, _ = G.load_detectors(root, G.DEFAULT_DETECTORS)
    reg["detectors"]["det_a"]["products"] = [{"path": "data/not_mentioned.json", "strict": True}]
    ver = G.verify_config(root, reg)
    assert any(p["kind"] == "product-not-referenced" for p in ver["problems"])


def test_json_output_schema(tmp_path, capsys):
    root = mk_root(tmp_path)
    arm(root)
    capsys.readouterr()
    assert G.main(["--root", str(root), "--json", "--no-core"]) == 0
    d = json.loads(capsys.readouterr().out)
    for k in ("schema", "tool", "overall", "armed", "configured", "detector_counts",
              "verdicts", "three_way", "config", "notes"):
        assert k in d, f"机读输出缺字段 {k}"
    assert d["schema"] == G.SCHEMA
    assert d["detector_counts"]["detectors"] == 2
    assert all("status" in v and "severity" in v for v in d["verdicts"])


def test_real_repo_config_is_consistent():
    """射程自检：真实配置里的检测器与产物必须真实存在（防"配了不存在的路径"）。"""
    reg, _ = G.load_detectors(ROOT, G.DEFAULT_DETECTORS)
    assert reg is not None and len(reg["detectors"]) >= 8
    ver = G.verify_config(ROOT, reg)
    assert ver["ok"] is True, f"真实配置自检失败：{ver['problems']}"
    assert all((ROOT / v["src"]).is_file() for v in reg["detectors"].values())
    assert all((ROOT / p["path"]).is_file() for v in reg["detectors"].values()
               for p in v["products"]), "声明的产物必须都存在"


def test_real_repo_three_way_config_covers_headline_rates():
    acfg = json.loads((ROOT / G.DEFAULT_ARTIFACTS).read_text(encoding="utf-8"))
    keys = {m["key"] for m in acfg["metrics"]}
    assert {"holdout_rate_pct", "corpus_rate_pct", "mutation_core_pct"} <= keys
    assert all(m.get("web") for m in acfg["metrics"]), "每个指标都要有前端指针（三方）"


def test_real_repo_guard_passes():
    """本仓现状态：guard_rerun_671a 必须 PASS（红路径由上面 tmp_path 用例覆盖）。"""
    res = G.evaluate(ROOT, ROOT / G.DEFAULT_BASELINE, include_core=False)
    assert res["overall"] == "PASS", f"真实仓库应当 PASS，实际：{res['message']}"
    assert res["three_way"]["blocked"] == 0


def test_selftest_passes(capsys):
    assert G.selftest() == 0
    out = capsys.readouterr().out
    assert "selftest: PASS" in out
