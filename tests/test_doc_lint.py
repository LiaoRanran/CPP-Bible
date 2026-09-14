"""doc_lint 回归锁（479 任务 2）：规则名/数字/工具名三类检查 + 误报抑制 + 退出码。"""
from __future__ import annotations

from pathlib import Path

import doc_lint as dl


def _actuals() -> dict[str, int]:
    """固定实测基线（测试用，避免绑定仓库当前数字）。"""
    return {"rules": 50, "evidence": 56, "atoms": 27, "tools": 92, "poison": 61}


def _scan(tmp: Path, text: str, *, rules: set[str] | None = None,
          tools: set[str] | None = None, exempt: dict[str, str] | None = None) -> list[dict]:
    p = tmp / "doc.md"
    p.write_text(text, encoding="utf-8")
    return dl.scan_doc(p, _actuals(), rules or {"ATOM-REL-CONFLICT"},
                       tools or {"doc_lint"}, {"test_doc_lint"}, exempt or {})


# ── 正例：干净的文档不得报警 ───────────────────────────────────────────────
def test_clean_doc_no_issue(tmp_path: Path):
    issues = _scan(tmp_path,
                   "# 规范\n规则 `ATOM-REL-CONFLICT` 生效；当前 50 条规则、27 颗原子、"
                   "56 张卡、61 个毒样例，工具 doc_lint.py 可用。\n")
    assert issues == [], f"干净文档被误报：{issues}"


# ── ① 规则名 ───────────────────────────────────────────────────────────────
def test_unknown_rule_reported(tmp_path: Path):
    issues = _scan(tmp_path, "该规则 EV-DOES-NOT-EXIST 负责拦截。\n")
    assert len(issues) == 1 and issues[0]["kind"] == "rule"
    assert "EV-DOES-NOT-EXIST" in issues[0]["message"]


def test_id_not_mistaken_as_rule(tmp_path: Path):
    """回归锁：`EV-MEM-001`/`ATOM-MEM-MOVE-001` 是 ID 不是规则名，不得被截断误报。"""
    issues = _scan(tmp_path, "证据卡 EV-MEM-001 服务原子 ATOM-MEM-MOVE-001，"
                             "误解 MIS-LANG-001 已登记。\n")
    assert issues == [], f"ID 被误判为规则名：{issues}"


def test_placeholder_and_wildcard_skipped(tmp_path: Path):
    issues = _scan(tmp_path, "模板里写 `EV-XXX` 或 `ATOM-*` 表示通配。\n")
    assert issues == [], f"占位符/通配被误报：{issues}"


def test_inline_ignore_marker(tmp_path: Path):
    """行内豁免（`doc-lint:ignore`）：只放过该行——逐字引用历史文档的合法场景。"""
    text = ("历史引用：`EV-OLD-NAME` 已被取代 <!-- doc-lint:ignore -->\n"
            "真失真：`EV-OLD-NAME` 仍在用。\n")
    issues = _scan(tmp_path, text)
    assert len(issues) == 1 and issues[0]["line"] == 2, f"行内豁免未生效：{issues}"


def test_exemption_applied(tmp_path: Path):
    """豁免台账登记后不再报（规划中/已删规则的合法出场口）。"""
    text = "规划规则 EV-PLANNED-ONLY 尚未实现。\n"
    assert len(_scan(tmp_path, text)) == 1
    issues = _scan(tmp_path, text, exempt={"EV-PLANNED-ONLY": "2026-09-14 · 规划中"})
    assert issues == [], f"豁免未生效：{issues}"


# ── ② 数字 ────────────────────────────────────────────────────────────────
def test_count_mismatch_reported(tmp_path: Path):
    issues = _scan(tmp_path, "门禁共 21 条规则。\n")
    assert len(issues) == 1 and issues[0]["kind"] == "count"
    assert "21" in issues[0]["message"] and "50" in issues[0]["message"]


def test_historical_snapshot_skipped(tmp_path: Path):
    """历史快照（行内标「当时/快照/约」）不报——否则历史报告永远在报错。"""
    issues = _scan(tmp_path, "当时 21 条规则；约 40 个毒样例；快照：26 张卡。\n")
    assert issues == [], f"历史快照被误报：{issues}"


def test_count_other_kinds(tmp_path: Path):
    issues = _scan(tmp_path, "本轮产出 3 颗原子、4 张卡、5 个工具、6 个毒样例。\n")
    kinds = [i["kind"] for i in issues]
    assert kinds.count("count") == 4, f"四类计数都应报：{issues}"


# ── ③ 工具名 ──────────────────────────────────────────────────────────────
def test_missing_tool_reported(tmp_path: Path):
    issues = _scan(tmp_path, "跑 python tools/no_such_tool.py 即可。\n")
    assert len(issues) == 1 and issues[0]["kind"] == "tool"
    assert "no_such_tool" in issues[0]["message"]


def test_test_file_reference_accepted(tmp_path: Path):
    """`tests/test_xxx.py` 形态是合法引用（文档常指测试文件）。"""
    issues = _scan(tmp_path, "回归锁见 tests/test_doc_lint.py。\n")
    assert issues == [], f"测试文件引用被误报：{issues}"


# ── 退出码 ────────────────────────────────────────────────────────────────
def test_exit_codes_follow_findings(monkeypatch, tmp_path: Path):
    """验收：无失真 → 0；有失真 → 1；--observe → 恒 0（CI 渐进接入）。"""
    clean = tmp_path / "clean"
    clean.mkdir()
    (clean / "a.md").write_text("当前 50 条规则、27 颗原子、56 张卡、61 个毒样例。\n",
                                encoding="utf-8")
    assert dl.main(["--dir", str(clean)]) == 0
    (clean / "a.md").write_text("门禁共 21 条规则。\n", encoding="utf-8")
    assert dl.main(["--dir", str(clean)]) == 1
    assert dl.main(["--dir", str(clean), "--observe"]) == 0
