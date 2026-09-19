"""565 Part 4a/4b · metrics 采集"确实落盘"回归锁 + 三曲线机制字段契约。

4a 的病不是代码 bug，而是**没有任何自动化跑它**：`metrics_collector.py` 一直是手动工具，
`data/metrics.jsonl` 因此从 2026-09-14 21:30 起停写三天（560 发现、565 复核）。
所以这里锁两件事：
  * **落盘契约**：`append()` 必须真的追加一行可解析 JSON（不是覆盖、不是静默失败）；
  * **新鲜度闸**：真库最后一行的时间戳若超过 `MAX_STALE_DAYS` ⇒ 红（让"断流"显形，
    而不是像这三天一样无人知晓）——红了的修法就一句：`metrics_collector.py --no-heavy`。

4b 的三曲线字段（**只有 1 个时点**）：
  * `mutation_escape_rate`：逃逸率带**双侧** C-P95 区间，且必须与 Part 1 原语逐值一致；
  * `overturned_by_stronger_verifier`：事件字段，当前**真值就是 0**（不是缺数据）；
  * `escape_survival_batches`：0 = 「真值 = 非真逃逸」、None = 「缺数据」，两者不许混读。
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import metrics_collector as mc
import pytest
import stat_bounds as sb

REPO = mc.ROOT
MAX_STALE_DAYS = 14          # 超过这个天数没采集 ⇒ 判"断流"并红（本轮实测曾断 3 天无人知）


# ── 4a 落盘契约与新鲜度 ───────────────────────────────────────────────────────
def test_append_writes_parseable_line(tmp_path: Path):
    """`append()`：追加一行可解析 JSON，且**不覆盖**已有内容、以换行结尾。"""
    p = tmp_path / "m.jsonl"
    p.write_text('{"old": 1}\n', encoding="utf-8")
    mc.append({"timestamp": "2026-09-17T00:00:00", "metrics": {}, "notes": {}}, p)
    mc.append({"timestamp": "2026-09-17T00:01:00", "metrics": {}, "notes": {}}, p)
    lines = p.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3, "append 必须是追加（旧行保留）"
    assert json.loads(lines[0])["old"] == 1
    assert json.loads(lines[-1])["timestamp"].endswith("00:01:00")
    assert p.read_text(encoding="utf-8").endswith("\n"), "每行必须以换行结尾（jsonl 契约）"


def test_real_metrics_file_is_fresh():
    """真库最后一行必须**新鲜**（否则说明采集断流了——本轮实测断过 3 天）。"""
    f = REPO / "data" / "metrics.jsonl"
    assert f.is_file(), "data/metrics.jsonl 不存在：先跑 metrics_collector.py --no-heavy"
    last = [ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()][-1]
    snap = json.loads(last)
    ts = dt.datetime.fromisoformat(snap["timestamp"])
    age = (dt.datetime.now() - ts).total_seconds() / 86400
    assert age <= MAX_STALE_DAYS, (
        f"metrics 已断流 {age:.1f} 天（最后 {snap['timestamp']}）⇒ "
        "跑一次 `.venv\\Scripts\\python.exe tools/metrics_collector.py --no-heavy`")


# ── 4b 三曲线契约 ─────────────────────────────────────────────────────────────
def test_curves_declare_single_timepoint():
    """只有 1 个时点 ⇒ 必须显式声明"单调收敛不可声称"（不许拿单点画趋势）。"""
    c = mc.collect_curves()
    assert c["timepoints"] == 1
    assert "不可声称" in c["monotone_convergence"], c


def test_curves_escape_rate_matches_stat_bounds():
    """逃逸率块必须与 Part 1 原语逐值一致（双侧区间；分母是**可判** 1406）。"""
    c = mc.collect_curves()["mutation_escape_rate"]
    # 586 任务2：M6 的 8 条 matrix 块式→flow 等价变体从 escaped 剔除、单列 equivalent_invalid，
    # 全量 escaped 由 9 降为 1（仅余 M1 真实逃逸）；M6 新增 matrix 删键值层变异使可判分母升到 1155。
    # 587 任务1/2：M6 再增 matrix **非法值替换**变异 220 个，值校验（warn 起步）落地后全部转为 warn_only。
    # 591（v7 冻结）：589 T2 注释净化 un-mask 27 条真实 fixture 路径变异 ⇒ M2 可判 141→168，
    # 可判分母 1379 → **1406**（escaped 仍 1 = M1 那条 TCE）。数字按重跑实测，不照抄旧账。
    assert c["judged"] == 1406 and c["n_a"] == 179
    assert c["numerator"] == 1 and c["denominator"] == 1406      # 591：v7 的 1/1406（诚实口径）
    lo, hi = sb.cp_interval(1, 1406)
    assert abs(c["point"] - 1 / 1406) < 1e-6
    assert abs(c["cp_low"] - lo) < 1e-6 and abs(c["cp_high"] - hi) < 1e-6
    # 与单侧口径**不同**（防拿单侧当区间用来"更漂亮"）
    assert sb.cp_upper_one_sided(1, 1406) != pytest.approx(hi, abs=1e-9)


def test_curves_placeholders_are_honest():
    """事件字段 0 是**真值**；生存时间是 **None**（缺数据）——不许把两者混为一谈。"""
    c = mc.collect_curves()
    assert c["overturned_by_stronger_verifier"] == 0
    # 573 任务 A：overturned 不再是"恒 0 占位"，而是**事件流的真读数**（仍保持诚实口径：
    # 系统绝不自动产生推翻，写入只接人/异族的显式动作）。
    assert "绝不自动产生推翻" in c["overturned_note"]
    # 573：survival 有第一批真数据了（M3 的 52 条，571→572 = 1 批）。
    # 592 任务1.4【非回归】：M2 由 None 改为 0 批 —— M2 的 207 条已被 571 证伪为尺子 bug 的**假逃逸**，
    #   "非真逃逸"是**真值 0**（不是缺数据）；`others` 仍必须 None（缺数据不许填 0）。
    s = c["escape_survival_batches"]
    assert isinstance(s, dict) and s["M3"]["batches"] == 1
    assert s["M2"]["batches"] == 0 and "假逃逸" in s["M2"]["note"]
    assert s["others"] is None, "其余缺数据必须是 None，不是 0"
    assert "None" in c["escape_survival_note"]


def test_collect_snapshot_carries_curves(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """真快照（`collect(with_heavy=False)`，跳过 poison/replay）必须带 curves 块。"""
    snap = mc.collect(with_heavy=False)
    assert "curves" in snap and snap["curves"]["timepoints"] == 1
    assert set(snap) >= {"timestamp", "metrics", "notes", "curves", "alerts"}
    # 落盘走 append：写进 tmp，不动真库
    p = tmp_path / "m.jsonl"
    mc.append(snap, p)
    again = json.loads(p.read_text(encoding="utf-8").splitlines()[-1])
    assert again["curves"]["mutation_escape_rate"]["denominator"] == 1406   # 591：v7 口径
