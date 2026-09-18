"""583 任务 2（N1）回归锁：`tools/prop_asof.py` 只读四轴快照。

任务书 §任务 2 的五条验收，逐条落成用例：
  ① 同输入两次跑 stdout **逐字相同**；② 源码**不含写操作**（静态断言）；
  ③ 命题行数 == `prop_graph.stats()["propositions"]`；④ git/命题库不可用 ⇒ **fail-loud**（不返回空表）；
  ⑤ `overturned_events.jsonl` 缺失 ⇒ 按 0 事件且**不报错**（设计上的"无数据"）。
另加：字段名硬约束（`asserted_at_approx_from_card_commit`，**不许**叫 `asserted_at`）。
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import prop_asof as pa  # noqa: E402


def test_583_asof_two_runs_are_byte_identical(capsys):
    """① 两次跑 stdout 逐字相同（确定性）。"""
    assert pa.main(["--json", "--limit", "5"]) == 0
    first = capsys.readouterr().out
    assert pa.main(["--json", "--limit", "5"]) == 0
    second = capsys.readouterr().out
    assert first == second
    assert first.strip().startswith("{")


def test_583_asof_source_is_read_only():
    """② 静态断言：源码无写操作；唯一的 subprocess 调用是**只读 git log**。

    注意：先剥掉模块 docstring 与行注释再扫——否则**文档里描述禁令的词**（本文开头就写着
    "无 `open(...,'w')`/`write_text`"）会把断言自己打红（第一次就是这么红的）。
    """
    raw = pathlib.Path(pa.__file__).read_text(encoding="utf-8")
    body = raw.split('"""', 2)[-1] if raw.startswith(('#!/usr/bin/env python3\n"""',
                                                     '"""')) else raw
    code = "\n".join(ln for ln in body.splitlines() if not ln.lstrip().startswith("#"))
    for bad in ("write_text(", "open(", "mkdir(", "unlink(", "rename(", "shutil."):
        assert bad not in code, f"只读工具里不许出现 {bad!r}"
    assert code.count("subprocess.run(") == 1, "只允许一处 subprocess（git 时间轴）"
    assert '["git", "log"' in code, "该处必须是只读 git log"
    assert "mode=ro" in code, "sqlite 必须以只读模式打开"


def test_583_asof_prop_count_matches_prop_graph(capsys):
    """③ 命题行数 == `prop_graph.stats()['propositions']`（与库自报口径一致）。"""
    import prop_graph as pg
    stats = pg.stats() if not hasattr(pg.stats, "__wrapped__") else pg.stats()
    assert pa.main(["--json"]) == 0
    import json
    payload = json.loads(capsys.readouterr().out)
    n = stats["propositions"] if isinstance(stats, dict) else stats
    assert payload["counts"]["propositions"] == int(n), (payload["counts"], n)


def test_583_asof_field_name_is_constrained(capsys):
    """字段名硬约束：近似时间必须叫 `asserted_at_approx_from_card_commit`（B 级证据不许伪装真值）。"""
    import json
    assert pa.main(["--json", "--limit", "3"]) == 0
    payload = json.loads(capsys.readouterr().out)
    row = payload["rows"][0]
    assert "asserted_at_approx_from_card_commit" in row
    assert "asserted_at" not in row, "不许给出一个叫 asserted_at 的『权威』时间"
    assert "B 级证据" in payload["evidence_grade"]


def test_583_asof_missing_db_fails_loud(tmp_path, monkeypatch):
    """④a 命题库缺失 ⇒ fail-loud（exit 2），**不返回空表**。"""
    monkeypatch.setattr(pa, "DEFAULT_DB", tmp_path / "nope.db")
    with pytest.raises(SystemExit) as ei:
        pa.build_rows(limit=1)
    assert ei.value.code == 2


def test_583_asof_git_unavailable_fails_loud(monkeypatch):
    """④b git 不可用 ⇒ fail-loud（exit 2），绝不把"没有时间轴"降级成空表。"""
    def _boom(*_a, **_k):
        raise OSError("git 不存在")
    monkeypatch.setattr(pa.subprocess, "run", _boom)
    with pytest.raises(SystemExit) as ei:
        pa.build_rows(limit=1)
    assert ei.value.code == 2


def test_583_asof_missing_overturned_is_zero_not_error(tmp_path, monkeypatch):
    """⑤ 推翻事件文件缺失 ⇒ 0 条事件、不报错（"无数据"是设计常态，不是缺陷）。"""
    monkeypatch.setattr(pa, "OVERTURNED", tmp_path / "not-there.jsonl")
    assert pa._load_overturned() == []
    payload = pa.build_rows(limit=3)
    assert payload["counts"]["overturned_events"] == 0
    assert all(r["overturned"] == 0 for r in payload["rows"])


def test_583_asof_reports_library_wide_missing_oracle():
    """口径对齐任务书：**全库**缺 oracle 的卡清单 + 卡数（实测 83 张卡、今天全缺）如实报出。"""
    payload = pa.build_rows(limit=1)
    c, lists = payload["counts"], payload["lists"]
    assert c["library_cards"] >= 80, c                       # 27 原子 + 56 证据（实测 83）
    assert c["library_missing_oracle_cards"] == len(lists["library_missing_oracle_cards"])
    assert c["library_missing_oracle_cards"] >= 1, c          # 今天应为"全缺"，如实
    assert lists["library_missing_oracle_cards"], "清单是交付物：机器只列缺，不代填"
