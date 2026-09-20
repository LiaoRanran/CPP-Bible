"""611 A2 · 人审 schema 补 `review_seconds`（610 交人项 ⑤）。

锁六件事：
  1. schema：`review_seconds` 是**可选**字段（缺它不得拒写一条人审 —— 人审权力优先于度量完备）；
  2. 写侧：`--review-seconds` 落盘为数字 + `review_seconds_source`；`append_annotation` 直调同效；
  3. 会话计时：`--began-at` ⇒ `seconds_since()` 按"现在 - 起点"算，来源标 `session`；
  4. **fail-closed**：负数 / NaN / 字符串 / bool / 超上限 ⇒ 拒写（一行都不写）；
  5. **存量不回填**：真实 388 条仍无该字段，统计 `measured=false`、avg/median/max/min 全 `None`
     （**不伪造 0**）；
  6. 统计正确性：混入测得值后 avg/median/max/min/来源分布逐项可复算。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import human_review_cli as hrc  # noqa: E402
import human_review_report as hrr  # noqa: E402

#: 用真实候选边里的第一条（**别硬编码**：边集变了测试会假红，2026-09-20 实遇）
EDGE = sorted(hrc.load_edge_ids())[0]
REASON = "611 A2 测试：显式给出实测耗时（秒），用于锁 schema 与统计口径"


def _ann(tmp: Path, rows: list[dict]) -> Path:
    p = tmp / "ann.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return p


def test_schema_field_is_optional(tmp_path: Path):
    ann = tmp_path / "ann.jsonl"
    # ① 不给 review_seconds 也能写（可选）
    rec = hrc.append_annotation(EDGE, "approve", REASON, path=ann)
    assert "review_seconds" not in rec, "未测耗时不该凭空生成字段（不猜）"
    assert rec["kind"] == "approve"
    # ② 显式给 ⇒ 落盘数字 + 来源
    rec2 = hrc.append_annotation(EDGE, "approve", REASON, review_seconds=12.5, path=ann)
    assert rec2["review_seconds"] == 12.5 and rec2["review_seconds_source"] == "explicit"
    rows = [json.loads(ln) for ln in ann.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(rows) == 2 and rows[1]["review_seconds"] == 12.5
    assert hrc.check(ann, edges_path=hrc.DEFAULT_EDGES) == []
    # ③ 0 秒是**真实值**（与"未测"必须区分开）
    rec3 = hrc.append_annotation(EDGE, "approve", REASON, review_seconds=0, path=ann)
    assert rec3["review_seconds"] == 0
    assert hrc.validate_record(rec3, hrc.load_edge_ids()) == []


def test_validation_fail_closed(tmp_path: Path):
    ids = hrc.load_edge_ids()
    base = {"edge_id": EDGE, "kind": "approve", "reviewer": hrc.REVIEWER,
            "timestamp": "2026-09-20T10:00:00+08:00", "reason": REASON}
    for bad, hint in ((-1, "不得为负"), (float("nan"), "有限数"), ("12", "必须是数字"),
                      (True, "必须是数字"), (hrc.MAX_REVIEW_SECONDS + 1, "上限")):
        rec = {**base, "review_seconds": bad}
        probs = hrc.validate_record(rec, ids)
        assert any(hint in p for p in probs), f"{bad!r} 未被拦住：{probs}"
    # 写侧同样 fail-closed（不合法 ⇒ 一行都不写）
    ann = tmp_path / "ann.jsonl"
    for bad in (-1.0, hrc.MAX_REVIEW_SECONDS + 1):
        with pytest.raises(ValueError):
            hrc.append_annotation(EDGE, "approve", REASON, review_seconds=bad, path=ann)
    assert not ann.exists()
    # 非法来源
    assert hrc.validate_record({**base, "review_seconds": 5,
                                "review_seconds_source": "guessed"}, ids)


def test_session_timing_seconds_since():
    # 起点 → 现在：固定两端算（不依赖真实时钟）
    assert hrc.seconds_since("2026-09-20T10:00:00+08:00",
                             now="2026-09-20T10:00:30+08:00") == 30.0
    assert hrc.seconds_since("2026-09-20T10:00:00+08:00",
                             now="2026-09-20T10:00:00.5+08:00") == 0.5
    assert hrc.seconds_since(None) is None
    assert hrc.seconds_since("不是时间") is None                    # 算不出 ⇒ None（不猜）
    assert hrc.seconds_since("2026-09-20T10:00:30+08:00",
                             now="2026-09-20T10:00:00+08:00") is None   # 负耗时 ⇒ None


def test_cli_began_at_records_session_source(tmp_path: Path, capsys):
    ann = tmp_path / "ann.jsonl"
    # ⚠️ argparse 坑：`--annotations` 是**父 parser** 的选项，必须写在子命令**之前**
    # ⚠️ 起点必须是"真的刚刚"：写死一个过去时刻会算出上万秒 ⇒ 被 MAX_REVIEW_SECONDS 拦下（fail-closed）
    began = (hrc.datetime.now(hrc.TZ) - hrc.timedelta(seconds=30)).replace(microsecond=0).isoformat()
    rc = hrc.main(["--annotations", str(ann), "approve", EDGE, "--reason", REASON,
                   "--began-at", began])
    assert rc == 0, capsys.readouterr().err
    rows = [json.loads(ln) for ln in ann.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert rows[-1]["review_seconds_source"] == "session"
    assert isinstance(rows[-1]["review_seconds"], float)
    assert 29.0 <= rows[-1]["review_seconds"] <= 60.0, rows[-1]
    # --review-seconds 优先于 --began-at（显式实测值更可信）
    rc2 = hrc.main(["--annotations", str(ann), "approve", EDGE, "--reason", REASON,
                    "--began-at", began,
                    "--review-seconds", "7.5"])
    assert rc2 == 0
    rows = [json.loads(ln) for ln in ann.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert rows[-1]["review_seconds"] == 7.5 and rows[-1]["review_seconds_source"] == "explicit"


def test_legacy_388_not_backfilled_and_stats_honest():
    """存量不回填：真实通道 0 条测得 ⇒ measured=false 且统计全 None（绝不伪造 0）。"""
    anns = hrr.load_annotations(hrc.DEFAULT_ANN)
    assert anns, "真实人审通道应非空（388 条）"
    assert all("review_seconds" not in a for a in anns), "存量记录被回填了（不许）"
    st = hrr.summarize_review_seconds(anns)
    assert st["total"] == len(anns) and st["measured_count"] == 0
    assert st["null_count"] == len(anns) and st["measured"] is False
    for k in ("avg", "median", "max", "min", "sum"):
        assert st[k] is None, f"未测量却给出 {k}={st[k]}（伪造数字）"
    assert "不可回溯" in st["note"] and st["by_source"] == {}


def test_stats_math_on_measured_rows():
    """统计正确性：给定测得的秒数，avg/median/max/min/来源分布可独立复算。"""
    rows = [{"edge_id": EDGE, "kind": "approve", "reason": REASON, "review_seconds": v,
             "review_seconds_source": s}
            for v, s in ((10.0, "explicit"), (20.0, "session"), (30.0, "session"),
                         (None, "unlabeled"))]
    st = hrr.summarize_review_seconds([r for r in rows if r["review_seconds"] is not None]
                                      + [{"edge_id": EDGE, "kind": "approve", "reason": REASON}])
    assert st["measured_count"] == 3 and st["null_count"] == 1 and st["measured"] is True
    assert st["avg"] == 20.0 and st["median"] == 20.0 and st["max"] == 30.0 and st["min"] == 10.0
    assert st["sum"] == 60.0
    assert st["by_source"] == {"explicit": 1, "session": 2}
    assert st["measured_ratio"] == 0.75


def test_report_has_section_9_and_keeps_section_8():
    anns = hrr.load_annotations(hrc.DEFAULT_ANN)
    text = hrr.generate_report(anns)
    assert "## 8. 后续建议" in text, "610 的 §8 断言锚点被破坏"
    assert "## 9. 耗时统计（review_seconds · 611 A2）" in text
    assert "measured=false" in text and "—" in text
    assert "不伪造 0" in text
    # 报告与事实源一致（--check 的判据）
    assert hrr.check(None, None, None) == []
