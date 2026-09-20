"""609 E1 · 度量诚实性回归锁（C-P 精确区间 + 曲线口径修正 + 方差声明）。

锁四件事（任务书 4 例 + 4 例自加）：
  1. `cp_upper(1406, 1)` 复算 == metrics.jsonl 记录的 v7 上界（1e-9）；
  2. `k=0` 的零失效上界 ≈ 3/n（精确版），且**绝不是 0**；
  3. 曲线里凡 note 含"口径修正"的点必须 `caliber_change=True`；v7（"冻结"）必须为 False；
  4. 方差声明：方差/标准误可复算，且报告里明写"C-P 已吃掉方差 / 不可做趋势检验"；
  +. 区间单调性：n 固定时 k 越大上界越大（自洽性）；
  +. `--check` exit 0；把 metrics 复制一份改分母 ⇒ `check(path)` 必须红；
  +. 报告含 v1→v7 全部版本行。
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import metrics_honesty as mh

N, K = mh.V7["n"], mh.V7["k"]


def test_v7_upper_bound_matches_recorded_value():
    b = mh.cp_bounds(N, K)
    recorded = float([c for c in mh.convergence_curve(mh.load_metrics())
                      if c["version"] == "v7"][0]["cp_upper"])
    assert abs(b["cp_upper"] - recorded) < 1e-9, f"复算 {b['cp_upper']} vs 记录 {recorded}"
    assert 0.0039 < b["cp_upper"] < 0.0040          # 0.3956%（任务0 实测）
    assert mh.check() == []


def test_zero_failure_upper_is_not_zero_and_close_to_three_over_n():
    up = mh.zero_failure_upper(N)
    assert up > 0.0, "零失效上界不许是 0（那是在宣称'逃逸率 0'）"
    assert abs(up - 3.0 / N) < 0.0012, f"k=0 上界 {up:.6f} 与 3/n={3 / N:.6f} 偏差过大"
    assert mh.cp_bounds(N, 0)["point"] == 0.0


def test_curve_marks_caliber_changes():
    curve = mh.convergence_curve(mh.load_metrics())
    assert [c["version"] for c in curve] == [f"v{i}" for i in range(1, len(curve) + 1)]
    for c in curve:
        if "口径修正" in c["note"] or "取代" in c["note"]:
            assert c["caliber_change"] is True, f"{c['version']} 口径修正未标注"
    v7 = [c for c in curve if c["version"] == "v7"][0]
    assert v7["caliber_change"] is False, "v7 是当前权威（'冻结'）⇒ 不该标成口径修正"
    assert v7["judged"] == 1406 and v7["numerator"] == 1


def test_variance_declaration_is_recomputable():
    b = mh.cp_bounds(N, K)
    p = K / N
    assert math.isclose(b["variance"], p * (1 - p) / N, rel_tol=1e-12)
    assert math.isclose(b["se"], math.sqrt(p * (1 - p) / N), rel_tol=1e-12)
    text = mh.render_report()
    for key in ("方差声明", "已经吃掉", "不可做趋势检验", "零失效上界", "口径修正"):
        assert key in text, f"报告缺 {key}"


def test_bounds_are_monotone_in_k():
    ups = [mh.cp_upper(N, k) for k in range(0, 6)]
    assert ups == sorted(ups), "上界应随 k 单调不减"
    assert 0 < mh.cp_lower(N, 5) <= mh.cp_upper(N, 5) <= 1


def test_check_red_when_denominator_changes(tmp_path: Path):
    """把 metrics 复制一份、改掉 v7 分母 ⇒ check 必须红（不许拿旧口径糊新数据）。"""
    src = Path(mh.DEFAULT_METRICS).read_text(encoding="utf-8").splitlines()
    docs = [json.loads(ln) for ln in src if ln.strip()]
    # 从后往前找**含 v7 的那一行**（前面若干行只有 6 点历史表 ⇒ 挑错行就白改）
    idx = next(i for i in range(len(docs) - 1, -1, -1)
               if any(str(h.get("version") or h.get("baseline_version")) == "v7"
                      for h in mh.find_history(docs[i])))
    hist = mh.find_history(docs[idx])
    assert str(hist[-1]["version"]) == "v7"
    hist[-1]["denominator"] = 999                    # 篡改分母（分子/记录区间都不动）
    copy = tmp_path / "metrics.jsonl"
    copy.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in docs) + "\n",
                    encoding="utf-8")
    saved = mh.DEFAULT_METRICS
    mh.DEFAULT_METRICS = copy
    try:
        problems = mh.check()
        assert problems, "分母被改还报 OK ⇒ 自洽校验形同虚设"
        assert any("口径变了" in p or "不一致" in p for p in problems), problems
    finally:
        mh.DEFAULT_METRICS = saved


def test_cli_report_and_write(tmp_path: Path, capsys):
    assert mh.main(["cp", "--n", "1406", "--k", "1"]) == 0
    out = capsys.readouterr().out
    assert "cp_upper" in out
    assert mh.main(["--check"]) == 0
    out_file = tmp_path / "rep.md"
    assert mh.main(["report", "--write", "--out", str(out_file)]) == 0
    text = out_file.read_text(encoding="utf-8")
    assert text == mh.render_report(), "落盘报告必须与 stdout 报告逐字一致"
    assert "度量诚实性报告" in text
    assert mh.main(["variance"]) == 0 and "方差声明" in capsys.readouterr().out
