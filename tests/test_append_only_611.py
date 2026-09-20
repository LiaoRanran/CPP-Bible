"""611 A1 · `verify_append_only` 字节前缀快路径回归锁（610 交人项 ④）。

**问题**：旧实现是 `splitlines(keepends=True)` 的**行级**逐字节比对 ⇒
末行**没有换行**的文件（实测 `data/supply_chain/merkle_roots.json` 末行无 `\\n`）在末尾追加内容时，
"旧末行 + 新内容"会被算作**同一行** ⇒ 必然判"第 N 行被改写"（**假红**）。

锁五件事：
  1. 末行无换行的文件可以正常追加（旧实现判红的那个场景）；
  2. 有换行的文件仍走行级检查（通过 + 能定位"第几行被改写"）；
  3. 空文件追加；
  4. 反例仍被拦住：截断 / 改历史行 / **末行无换行但被改写**（快慢路径都不许放行）；
  5. 快慢路径**通过集合一致**（穷举小样本证明"不等于放水"）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import supply_chain_verify as scv  # noqa: E402


def _legacy(old: str, new: str) -> bool:
    """610 之前的行级实现（照抄旧逻辑）——用来证明快路径**确实**修掉了假红。"""
    old_lines, new_lines = old.splitlines(keepends=True), new.splitlines(keepends=True)
    if len(new_lines) < len(old_lines):
        return False
    return all(new_lines[i] == o for i, o in enumerate(old_lines))


def test_no_trailing_newline_append_is_accepted():
    """① 末行无换行：追加必须通过（旧实现在此假红 —— 这条测试就是它的回归锁）。"""
    old = '{"book": "aaa"}'
    new = old + '\n{"examples": "bbb"}'
    ok, why = scv.verify_append_only(old, new)
    assert ok is True, f"末行无换行的追加被误杀：{why}"
    assert "字节前缀" in why and "末行无换行" in why
    # 直接拼接（不加换行）也是纯追加
    ok2, _ = scv.verify_append_only('{"a": 1}', '{"a": 1}{"b": 2}')
    assert ok2 is True
    # 反证：旧实现会在这两个场景判红（= 假红），所以快路径不是"多余优化"
    assert _legacy(old, new) is False, "旧实现本应假红（若这条断言失败，说明我对旧逻辑的理解有误）"
    assert _legacy('{"a": 1}', '{"a": 1}{"b": 2}') is False


def test_with_trailing_newline_still_line_level():
    """② 有换行 ⇒ 常规行级追加通过，报文说明新增行数（不是字节数）。"""
    old = "a\nb\n"
    ok, why = scv.verify_append_only(old, old + "c\n")
    assert ok is True and "字节前缀" in why
    assert _legacy(old, old + "c\n") is True          # 旧实现也能过（这条不是修复项）
    # 非前缀（改历史行）⇒ 走慢路径并**指出第几行**
    ok2, why2 = scv.verify_append_only(old, "a\nB\nc\n")
    assert ok2 is False and "第 2 行被改写" in why2


def test_empty_file_append():
    """③ 空文件（或空 old）⇒ 任何内容都算纯追加（`startswith("")` 恒真）。"""
    for new in ("", "x", '{"a": 1}', "a\nb\n"):
        ok, _ = scv.verify_append_only("", new)
        assert ok is True, f"空文件追加被误杀：{new!r}"


def test_negative_cases_still_blocked():
    """④ 反例：截断 / 改历史行 / 末行无换行但被改写 —— 一个都不许放行。"""
    for old, new in (('{"a": 1}', ''),                       # 截断
                     ("a\nb\n", "a\nB\nc\n"),                # 改历史行
                     ("a\nb\n", "a\n"),                      # 截断更多
                     ('{"a": 1}', '{"a": 2}\n{"b": 2}'),     # 末行无换行但被改写
                     ("x\ny", "x\nz\ny")):                   # 中间插入（非追加）
        ok, why = scv.verify_append_only(old, new)
        assert ok is False, f"反例被放行：{old!r} → {new!r}（{why}）"


def test_fast_and_slow_path_agree_on_small_space():
    """⑤ 一致性：穷举小样本，快路径与旧行级实现的差异**只允许**是"快路径多放过纯字节追加"。"""
    alphabet = ("a", "b", "\n")
    texts = [""]
    for c1 in alphabet:
        texts.append(c1)
        for c2 in alphabet:
            texts.append(c1 + c2)
    diff = []
    for old in texts:
        for new in texts:
            fast = scv.verify_append_only(old, new)[0]
            slow = _legacy(old, new)
            if fast != slow:
                diff.append((old, new, fast, slow))
    # 唯一的合法差异方向：fast=True & slow=False（末行无换行的假红被修掉）
    assert diff, "若差异集为空 ⇒ 快路径没起作用（末行无换行的假红应当被修）"
    assert all(f is True and s is False for _, _, f, s in diff), \
        f"快路径放过了旧实现拦得住的东西（= 放水）：{[d for d in diff if d[2] is not True][:5]}"
    # 反方向（fast=False & slow=True）必须为空：字节前缀成立 ⇒ 行级前缀必然成立
    assert not [d for d in diff if d[2] is False], f"快路径误杀：{diff[:5]}"


def test_check_reports_no_problem():
    """`--check` 自检（含新增 4 正例 + 3 反例）必须零问题。"""
    assert scv.check() == []


def test_real_merkle_roots_file_is_now_appendable():
    """真实盘：`data/supply_chain/merkle_roots.json` 末行无换行 ⇒ 追加必须通过。"""
    p = ROOT / "data" / "supply_chain" / "merkle_roots.json"
    if not p.is_file():
        pytest.skip("merkle 台账不存在")
    old = p.read_text(encoding="utf-8")
    assert not old.endswith("\n"), "（前提变了：该文件现在以换行结尾 ⇒ 本用例的靶子已不存在）"
    ok, why = scv.verify_append_only(old, old + '\n{"note": "611 A1 append test"}\n')
    assert ok is True, why
    assert "末行无换行" in why
    assert _legacy(old, old + '\n{"note": "611 A1 append test"}\n') is False
