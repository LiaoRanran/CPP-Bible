"""608 C2 · metrics 新增 5 类指标回归锁（只读 / monkeypatch，无真编译）。

覆盖：
  * 人审进度（初始 0 已审 / 388 待审）
  * 论证层状态（IN79 / OUT42 / UNDEC0 / 388 边 / 42 MIS 组）
  * 编译可复现指标读取（monkeypatch I2，验证 reproducible / drift / symtab 三字段）
  * 逃逸率历史（v1→v7 ≥ 5 时点）
  * Clopper-Pearson 双侧 95% 区间：对 1/1406 验证 ≈ [0.0018%, 0.3956%]
  * 尺子变更史标注（v1→v5 标"口径修正"）
  * 只读验证（采集不改动任何数据文件）

本模块无真编译、无仓库写盘 ⇒ **不进 SERIAL_EXTRA**，随 fast 门禁跑。
"""
from __future__ import annotations

from pathlib import Path

import metrics_collector as mc
import replay_invariants as ri

ROOT = Path(__file__).resolve().parent.parent


def test_human_review_initial():
    out = mc.collect_608_new_metrics({}, with_heavy=False)["human_review"]
    assert out["total"] == 388, out
    assert out["pending"] == 388
    assert out["approved"] == 0 and out["rejected"] == 0 and out["modified"] == 0


def test_grounded_status():
    out = mc.collect_608_new_metrics({}, with_heavy=False)["grounded"]
    assert out["in"] == 79 and out["out"] == 42 and out["undec"] == 0
    assert out["candidate_edges_total"] == 388
    assert out["candidate_edges_by_mis"] == 42


def test_build_reproducibility_reads(monkeypatch):
    fake = {"passed": True, "cards": [
        {"card": "EV-X1", "match": True, "cross": "一致", "detail": ""},
        {"card": "EV-X2", "match": True, "cross": "未启用", "detail": "symtab=no"},
    ]}
    monkeypatch.setattr(ri, "check_build_reproducibility", lambda **k: fake)
    out = mc.collect_608_new_metrics({}, with_heavy=True)["build_reproducibility"]
    assert out["reproducible"] is True
    assert out["time_macro_drift"] == 0
    # detail 含 "symtab=no" ⇒ 符号表不一致
    assert out["symtab_consistent"] is False
    assert out["n_cards"] == 2


def test_escape_rate_history():
    conv = mc.collect_608_new_metrics({}, with_heavy=False)["escape_rate_convergence"]
    assert len(conv) >= 5
    versions = {c["version"] for c in conv}
    assert {"v1", "v7"} <= versions


def test_clopper_pearson_1_1406():
    conv = {c["version"]: c
            for c in mc.collect_608_new_metrics({}, with_heavy=False)["escape_rate_convergence"]}
    v7 = conv["v7"]
    assert v7["numerator"] == 1 and v7["denominator"] == 1406
    # 双侧 C-P95 对 1/1406 ≈ [0.0018%, 0.3956%]（点估计 0.0711%）
    assert abs(v7["cp_lower"] - 1.8006813682120512e-05) < 1e-9
    assert abs(v7["cp_upper"] - 0.003956325504751501) < 1e-9
    assert 0 < v7["cp_lower"] < v7["point"] < v7["cp_upper"]


def test_ruler_change_annotation():
    out = mc.collect_608_new_metrics({}, with_heavy=False)
    assert "口径修正" in out["escape_rate_note"]
    # v1→v5 每版都标"口径修正"（非同一量时间序列）
    conv = {c["version"]: c for c in out["escape_rate_convergence"]}
    for v in ("v1", "v2", "v3", "v4", "v5"):
        assert "口径修正" in conv[v]["note"], v


def test_readonly_does_not_modify_files():
    ann = ROOT / "data" / "human_attack_edge_annotations.jsonl"
    before_exists = ann.exists()
    w2 = ROOT / "data" / "grounded_labels_w2.json"
    w2_mtime = w2.stat().st_mtime
    mc.collect_608_new_metrics({}, with_heavy=False)
    # 不应创建/删除标注文件（采集只读，人审权力）
    assert ann.exists() == before_exists
    # 不应改写 W2 判决文件
    assert abs(w2.stat().st_mtime - w2_mtime) < 1e-6
