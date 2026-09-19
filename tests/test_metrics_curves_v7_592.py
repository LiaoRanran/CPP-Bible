"""592 任务1 · metrics curves 度量诚实化回归锁（v1 → v7）。

病：报告层看的 `curves.mutation_escape_rate` 曾是 v1 的 0.2374（23.7%），而真实基线是
v7 的 1/1406 ≈ 0.071% —— 差 340 倍。本文件锁死"曲线只能读**当前权威基线**"这件事，
并给每条断言配一个**会变红的方向**（旧值/旧源出现即红），防止"改了数字但没改口径"。

口径三件套（565 Part 1）：分子/分母 + 点估计 + **双侧** C-P95，一律走 `stat_bounds`。
"""
from __future__ import annotations

import json

import metrics_collector as mc
import pytest
import stat_bounds as sb

V7 = "data/mutation/full_baseline_v7.json"
V1_POINT = 0.237448                      # v1（571 修尺子前，含 M2 假逃逸）——只配作历史时点


def test_escape_rate_point_is_v7_over_1406():
    """任务1.2：当前逃逸率 = v7 的 escaped/(blocked+escaped) = **1/1406**。

    ⚠️ 精度口径（实测修正任务书）：曲线的 `point` 是**6 位小数展示值**（报告口径，既有测试锁死），
    1e-9 级断言只能在新增的全精度 `point_raw` 上做 —— 6 位小数下 1/1406 只剩 2 位有效数字，
    拿它做 1e-9 断言在任何实现下都会红（不是实现问题，是口径问题）。
    """
    r = mc.collect_curves()["mutation_escape_rate"]
    assert r["source"].endswith(V7), f"当前口径必须读 v7，实得 {r['source']}"
    assert (r["numerator"], r["denominator"]) == (1, 1406)
    assert r["judged"] == 1406 and r["n_a"] == 179
    assert abs(r["point_raw"] - 1 / 1406) < 1e-9, r          # 全精度：1e-9 容差
    assert r["point"] == round(1 / 1406, 6)                  # 展示值：与全精度一致的取整
    # 反向：绝不能再是 v1 的 0.237448（这正是本任务要修的"度量不诚实"）
    assert abs(r["point_raw"] - V1_POINT) > 0.1, "曲线又退回 v1 旧值了"


def test_escape_rate_cp_interval_matches_stat_bounds_independent_recompute():
    """双侧 C-P95 必须与 `stat_bounds.cp_interval` **独立复算**逐值一致（且不是单侧）。"""
    r = mc.collect_curves()["mutation_escape_rate"]
    lo, hi = sb.cp_interval(1, 1406, 0.95)
    assert r["cp_low_raw"] == lo and r["cp_high_raw"] == hi, (r, (lo, hi))   # 全精度逐值
    assert (r["cp_low"], r["cp_high"]) == (round(lo, 6), round(hi, 6))      # 展示值
    assert r["conf"] == 0.95
    # 单侧上界必须**不同**（防拿单侧当区间、"看起来更好"）
    assert sb.cp_upper_one_sided(1, 1406, 0.95) != pytest.approx(hi, abs=1e-12)


def test_escape_rate_declares_baseline_version_and_frozen_commit():
    """任务1.2：曲线块须自报 `baseline_version`/`frozen_at_commit`，且与基线文件自身一致。"""
    r = mc.collect_curves()["mutation_escape_rate"]
    assert r["baseline_version"] == "v7"
    d = json.loads((mc.ROOT / V7).read_text(encoding="utf-8"))
    assert r["frozen_at_commit"] == d["frozen_at_commit"] == "d36d5c8"
    # 反向：v6（被 v7 取代）绝不能出现在当前口径位
    assert "v6" not in r["source"]


def test_monotone_convergence_is_not_claimable():
    """任务1.5：单时点 + 尺子变更史 ⇒ 必须显式写"不可声称"。"""
    c = mc.collect_curves()
    assert c["timepoints"] == 1
    assert "不可声称" in c["monotone_convergence"]
    assert "v1→v7" in c["monotone_convergence"] or "v1" in c["monotone_convergence"]


def test_new_row_does_not_carry_v1_rate(tmp_path):
    """任务1 验收：**新采集的一行**里，当前逃逸率块不含 v1 旧值 0.2374。

    （v1 值仍合法地留在 `mutation_escape_rate_history` 里且带"仅历史"标签——
      所以只在**当前口径块**上断言，不整行搜字符串。）
    """
    snap = mc.collect(with_heavy=False)
    rate_blob = json.dumps(snap["curves"]["mutation_escape_rate"], ensure_ascii=False)
    assert "0.237" not in rate_blob, f"当前口径块里出现 v1 旧值：{rate_blob}"
    # 落盘走 append（写 tmp，不碰真库）——"新行"指这一行
    p = tmp_path / "m.jsonl"
    mc.append(snap, p)
    row = json.loads(p.read_text(encoding="utf-8").splitlines()[-1])
    assert row["curves"]["mutation_escape_rate"]["baseline_version"] == "v7"
    assert row["curves"]["mutation_escape_rate"]["denominator"] == 1406
    # 可证伪对照：v1 值确实存在于**历史**里（因此上面那条不是空断言）
    hist = row["curves"]["mutation_escape_rate_history"]
    v1 = [h for h in hist if h["source"].endswith("full_baseline_v1.json")]
    assert v1 and v1[0]["point"] == V1_POINT, "历史里应保留 v1 时点（否则本测试失去对照）"


def test_overturned_channel_flag_distinguishes_no_channel_from_no_event():
    """任务1.3：`overturned_channel_initialized` 必须与通道文件是否真的存在一致。

    文件缺失时计数 0 的意思是"**没有通道**"，不是"没有推翻"；592 任务2 建空文件后转 True。
    """
    c = mc.collect_curves()
    assert isinstance(c["overturned_channel_initialized"], bool)
    assert c["overturned_channel_initialized"] == mc.OVERTURNED_FILE.is_file()
    assert c["overturned_by_stronger_verifier"] == len(mc.read_overturned_events())


def test_survival_entries_cover_m3_m5_m2_m6_and_none_else():
    """任务1.4：survival 逐算子条目 —— 0 = 真值（非真逃逸）、None = 缺数据，不许混。"""
    s = mc.collect_curves()["escape_survival_batches"]
    assert s["M3"]["batches"] == 1 and s["M3"]["escapes"] == 52
    assert (s["M3"]["produced_in"], s["M3"]["closed_in"]) == ("571", "572")
    assert s["M5"]["batches"] == 1 and s["M5"]["escapes"] == 29
    assert s["M5"]["produced_in"] == "574"
    assert s["M2"]["batches"] == 0 and "假逃逸" in s["M2"]["note"]
    assert s["M6"]["batches"] == 0 and "等价" in s["M6"]["note"]
    assert s["others"] is None, "其余算子缺数据必须是 None，不许填 0"
    assert "None" in mc.collect_curves()["escape_survival_note"]
