"""592 任务4 · 命题网络台账（`data/prop_network_inventory.md`）回归锁。

台账是 R4 grounded 层的**输入基线**，只有在"与事实源逐字节一致"时才有意义：
本文件因此把**重新生成的结果**与**已提交台账**逐字节比对 —— 卡/命题一变而台账没跟上 ⇒ 红。
"""
from __future__ import annotations

import prop_network_inventory as inv

LEDGER = inv.OUT_DEFAULT
SECTIONS = ("## 0. 汇总与完整性校验", "## 1. 命题列表", "## 2. 卡列表",
            "## 3. 边统计", "## 4. 闭包口径与对账")


def _text() -> str:
    return LEDGER.read_text(encoding="utf-8")


def test_ledger_exists_and_has_all_sections():
    assert LEDGER.is_file(), "台账缺失：跑 `tools/prop_network_inventory.py`"
    t = _text()
    for s in SECTIONS:
        assert s in t, f"台账缺小节：{s}"


def test_ledger_lists_79_props_and_27_cards():
    t = _text()
    prop_rows = [ln for ln in t.splitlines() if ln.startswith("| ") and "/prop-" in ln]
    assert len(prop_rows) == 79, f"命题行应 79 条，实得 {len(prop_rows)}"
    card_rows = [ln for ln in t.splitlines()
                 if ln.startswith("| `ATOM-") and "/prop-" not in ln]
    assert len(card_rows) == 27, f"卡行应 27 条，实得 {len(card_rows)}"


def test_integrity_checks_are_clean():
    """三条完整性校验：引用卡不存在 = 0、无命题原子卡 = 0、闭包异常（>50 或 =1）= 0。"""
    d = inv.collect()
    assert d["bad_refs"] == []
    assert d["no_prop_cards"] == []
    assert d["bad_closure"] == []
    assert len(d["rows"]) == 79
    assert d["stats"]["propositions"] == 79 and d["stats"]["cards"] == 27


def test_ledger_matches_fresh_render_byte_for_byte():
    """台账必须与**现读事实源重新渲染**的结果逐字节一致（既锁幂等，也锁"不过期"）。"""
    fresh = inv.render(inv.collect())
    assert fresh == _text(), (
        "台账与事实源漂移 ⇒ 重跑 `.venv\\Scripts\\python.exe tools/prop_network_inventory.py`")
