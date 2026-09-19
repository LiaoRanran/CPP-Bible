"""608 A3 · human_review_queue.py 回归锁 + 首次队列报告。

锁十件事：
  * 聚合：388 边 → 42 MIS 组，每组边数正确、加总 = 388
  * 排序：歧义度降序（本仓 credibility 全均匀 ⇒ 歧义度恒 0，退化为按边数降序保底）
  * --stats：初始 0 已审 / 388 待审
  * --check：聚合与 attack_edge_review 权威数据一致（exit 0）
  * --feedback：0 已审时输出「无反馈数据」
  * 只读：跑完工具后人审通道文件不被创建/改动（596 入库为空）、候选边文件 mtime 不变
  * 反例：--show 不存在的 MIS ⇒ 非 0 退出
"""
from __future__ import annotations

import contextlib
import io
import os
import time

import human_review_queue as hrq


def _capture(argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = hrq.main(argv)
    return rc, buf.getvalue()


def test_aggregate_388_edges_to_42_groups():
    groups = hrq.build_groups()
    assert len(groups) == 42, f"期望 42 个 MIS 组，实得 {len(groups)}"
    total = sum(g["edge_count"] for g in groups)
    assert total == 388, f"边数加总应 = 388，实得 {total}"
    # 每组的边数 = 该 MIS 在候选边里出现的次数
    import attack_edge_generator as aeg
    edges = aeg.load_edges()
    by_mis = {}
    for e in edges:
        mid = e["source"] if e["direction"] == "mis_to_prop" else e["target"]
        by_mis[mid] = by_mis.get(mid, 0) + 1
    for g in groups:
        assert g["edge_count"] == by_mis[g["mis_id"]], \
            f"{g['mis_id']} 边数 {g['edge_count']} ≠ 实算 {by_mis[g['mis_id']]}"


def test_ambiguity_sort_order():
    groups = hrq.build_groups()
    # 本仓 79 命题 credibility 全 = 2、42 MIS 全 = 1（596 实测）⇒ 歧义度恒 0，
    # 排序退化为按 (-edge_count, mis_id)。断言：首组边数 = 最大边数，且整体非增。
    counts = [g["edge_count"] for g in groups]
    assert counts[0] == max(counts)
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))


def test_stats_initial_zero_reviewed():
    rc, out = _capture(["--stats"])
    assert rc == 0
    assert "已审（生效）：0" in out, out
    assert "待审：388" in out, out
    assert "approve=0" in out and "reject=0" in out and "modify=0" in out


def test_check_consistency_passes():
    rc, out = _capture(["--check"])
    assert rc == 0, out
    assert "一致性校验通过" in out, out


def test_feedback_empty_output():
    rc, out = _capture(["--feedback"])
    assert rc == 0
    assert "无反馈数据" in out, out


def test_readonly_never_creates_annotation_and_keeps_edges_mtime():
    ann_path = hrq.aer.DEFAULT_ANN
    edges_path = hrq.aeg.DEFAULT_OUT
    before = os.path.getmtime(edges_path)
    # 人审通道文件由 596 入库为空（必须存在）；工具只读，绝不得创建/改动它（人审权力）。
    ann_existed = os.path.exists(ann_path)
    ann_mtime = os.path.getmtime(ann_path) if ann_existed else None
    _capture(["--check"])
    _capture(["--list"])
    _capture(["--stats"])
    _capture(["--feedback"])
    time.sleep(0.01)
    after = os.path.getmtime(edges_path)
    assert before == after, "候选边文件 mtime 被改动 ⇒ 工具非只读"
    if ann_existed:
        assert os.path.exists(ann_path), "只读工具删除了人审通道文件"
        assert os.path.getmtime(ann_path) == ann_mtime, \
            "只读工具改动了人审通道文件 mtime ⇒ 违反只读硬纪律"
        assert hrq.aer.load_annotations() == [], \
            "只读工具向人审通道写入了内容（人审权力）"
    else:
        assert not os.path.exists(ann_path), \
            "工具不应创建人审结果文件（人审权力；违反只读硬纪律）"


def test_show_missing_mis_exits_nonzero():
    rc, _ = _capture(["--show", "MIS-DOES-NOT-EXIST"])
    assert rc != 0, "不存在的 MIS 应非 0 退出（报错）"
