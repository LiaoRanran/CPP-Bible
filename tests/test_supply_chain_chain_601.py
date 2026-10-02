# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""601 任务2.2 · 溯源链「入库 layout + 整链验证」回归锁。

与 `test_supply_chain_601.py` 的分工：那边是 link/layout 的单元语义，这边锁**仓库级事实**：
  * 已入库的 `data/supply_chain/layout.json` 必须与 `STEPS` 定义逐字一致（防"改了代码没刷 layout"）；
  * layout 必须进 `tool_integrity` 的 `SUPPLY_CHAIN_FILES` 且 hash 已钉；
  * 真库 `layout verify` / `stats` / `chain verify` 全绿（链上 0 link 是**合法**状态）；
  * 端到端：沙箱里造 link（真实 layout + 假仓）⇒ 绿；事后篡改被覆盖文件 ⇒ **红**（585 攻击1 链路层）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import merkle_integrity as mi
import pytest
import supply_chain as sc
import tool_integrity as ti

#: 673u：xdist 并发守卫（与 622/647 同一惯例）。本文件的 `test_chain_verify_with_real_inspections`
#: 会跑 `tool_integrity --check` 的 `merkle_check` inspection（覆盖 atoms/evidence/Examples/Book），
#: 而 xdist 下别的 worker 可能正处在"隔离快照 → 测试 → 还原"的中段 ⇒ 读到瞬时污染 ⇒ flip-flop。
_XDIST_PARALLEL = os.environ.get("PYTEST_XDIST_WORKER") is not None


def _fake_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    fake = tmp_path / "repo"
    (fake / "atoms" / "mem").mkdir(parents=True)
    (fake / "atoms" / "mem" / "A.md").write_text("A\n", encoding="utf-8")
    (fake / "evidence").mkdir()
    (fake / "evidence" / "E.md").write_text("E\n", encoding="utf-8")
    (fake / "Examples").mkdir()
    (fake / "Examples" / "x.cpp").write_text("int main(){}\n", encoding="utf-8")
    monkeypatch.setattr(sc, "ROOT", fake)
    monkeypatch.setattr(mi, "ROOT", fake)
    return fake


# ── 入库事实 ───────────────────────────────────────────────────────────────────
def test_committed_layout_matches_steps_definition():
    committed = sc.load_layout()
    assert committed is not None, "layout.json 必须入库（`supply_chain.py layout init`）"
    assert committed == sc.create_layout(), "layout 与 STEPS 定义漂移 ⇒ 重跑 `layout init`"
    assert sc.verify_layout(committed) == []
    assert committed["generated_at"] is None, "入库的 layout 不打点（幂等）"
    assert [s["name"] for s in committed["steps"]] == [
        "card_authoring", "gate_check", "replay_verify", "poison_test", "mutation_test",
        "metrics_collect", "human_review"]


def test_layout_is_in_supply_chain_files_and_pinned():
    assert "data/supply_chain/layout.json" in ti.SUPPLY_CHAIN_FILES
    base = ti.load_supply_chain_baseline()
    assert base is not None, "缺 supply_chain 节（跑 `tool_integrity --update`）"
    assert base["data/supply_chain/layout.json"] == ti.sha256_of(sc.LAYOUT_PATH), \
        "layout 未钉或已被改（跑 `tool_integrity --update`）"
    assert base["data/supply_chain/merkle_roots.json"] == ti.sha256_of(mi.ROOTS_PATH), \
        "Merkle 台账未钉或已被改"


def test_real_repo_layout_stats_chain_green():
    assert sc.main(["layout", "verify"]) == 0
    assert sc.main(["layout", "show"]) == 0
    assert sc.main(["stats"]) == 0
    assert sc.main(["chain", "verify", "--no-inspections"]) == 0


# ── 端到端：沙箱造 link（真 layout + 假仓）──────────────────────────────────────
def test_end_to_end_chain_green_then_red_on_tamper(tmp_path: Path, monkeypatch):
    fake = _fake_repo(tmp_path, monkeypatch)
    links = tmp_path / "links"
    lay = sc.load_layout()
    # 造两条真实步骤的 link：card_authoring（人）→ gate_check（机器）
    sc.write_link(sc.create_link("card_authoring", functionary="human:LiaoRanran",
                                 command="人工编写卡面", now="2026-09-19T18:00:00", layout=lay),
                  links)
    sc.write_link(sc.create_link("gate_check", command="gate_engine.py --check",
                                 now="2026-09-19T18:01:00", layout=lay), links)
    problems, notes = sc.chain_verify(links_dir=links, layout=lay, run_inspections=False)
    assert problems == [], problems
    # 585 攻击1（链路层）：事后改一个被覆盖文件 ⇒ 既有 link 的 products/materials 对不上
    (fake / "atoms" / "mem" / "A.md").write_text("A 被篡改\n", encoding="utf-8")
    problems, _ = sc.chain_verify(links_dir=links, layout=lay, run_inspections=False)
    assert any("与记录不符" in p for p in problems), problems
    assert any("atoms" in p for p in problems), problems
    # 再改回原样 ⇒ 链重新变绿（证明红是"内容变了"，不是噪声）
    (fake / "atoms" / "mem" / "A.md").write_text("A\n", encoding="utf-8")
    problems2, _ = sc.chain_verify(links_dir=links, layout=lay, run_inspections=False)
    assert problems2 == [], problems2


def test_end_to_end_chain_red_on_link_record_tamper(tmp_path: Path, monkeypatch):
    _fake_repo(tmp_path, monkeypatch)
    links = tmp_path / "links"
    lay = sc.load_layout()
    sc.write_link(sc.create_link("card_authoring", functionary="human:X",
                                 now="2026-09-19T18:00:00", layout=lay), links)
    f = sorted(links.glob("card_authoring*.json"))[0]
    link = json.loads(f.read_text(encoding="utf-8"))
    link["products"][0]["hash"] = "0" * 64          # 改记录（不碰文件）
    f.write_text(json.dumps(link, ensure_ascii=False), encoding="utf-8")
    problems, _ = sc.chain_verify(links_dir=links, layout=lay, run_inspections=False)
    assert any("与记录不符" in p for p in problems), problems


# 673u：**摘除 632 A2 的 `residue_present()` 守卫**（该守卫恒真 —— `_arch_v19..v23/_adv_v80`
# 早已入库 ⇒ 任何检出都为 True ⇒ 本用例此前从未真跑过）。673u 定位到两个真实阻塞，**均已解除**：
#   ① 治理清单漂移 634 处 —— 673u 修（扫描面按 git 在册过滤 + 哈希按 `.gitattributes` 归一换行）；
#   ② 本用例 `integrity_check` inspection 里 `merkle_integrity --check` 在**干净检出**下
#      5 个目录根不匹配 —— 673t C（commit 1072c605）修（Merkle 根与 tool_integrity 摆脱检出环境）。
# 673u 在**干净检出（git worktree @ 673t HEAD）**下复验本用例**串行绿** ⇒ 旧守卫失去理由。
# 但实测它在 **xdist 并发下会 flip-flop**（本用例要跑覆盖 atoms/evidence/Examples/Book 的
# `merkle_check` inspection，而别的 worker 可能正处在隔离快照的中段）⇒ 按 622/647 的既有惯例
# 换成 `_XDIST_PARALLEL` 守卫：**串行真跑、并发跳过**（比原来那个恒真的守卫强，且不制造假红）。
# 未改动任何断言。
@pytest.mark.skipif(
    _XDIST_PARALLEL,
    reason="673u：串行（含干净检出复验）真跑且绿；xdist 并发下与 merkle_check inspection 对 "
           "atoms/evidence/Examples/Book 的读写争用致 flip-flop ⇒ 仅并发下跳过（622/647 同惯例）",
)
def test_chain_verify_with_real_inspections(tmp_path: Path):
    """inspection 真的跑起来（真 layout + **真仓**，检查命令是只读的）：绿；换成必失败 ⇒ 红。

    注意这里**不 monkeypatch `sc.ROOT`**：inspection 命令的路径（`tools/*.py`）与 cwd 都必须是真仓，
    否则子进程在假仓里找不到工具（601 实测：exit 2 "can't open file"）。
    link 只写到 tmp（对真仓**只读**）。
    """
    links = tmp_path / "links"
    lay = sc.load_layout()
    sc.write_link(sc.create_link("card_authoring", functionary="human:X",
                                 now="2026-09-19T18:00:00", layout=lay), links)
    problems, notes = sc.chain_verify(links_dir=links, layout=lay, run_inspections=True)
    assert problems == [], problems
    assert sum(1 for n in notes if "✓" in n) == 3, notes     # 三条 inspection 全跑且全绿
    lay2 = json.loads(json.dumps(lay))
    lay2["inspections"] = [{"name": "fake_fail", "after": "card_authoring",
                            "command": ["-c", "raise SystemExit(7)"]}]
    problems2, _ = sc.chain_verify(links_dir=links, layout=lay2, run_inspections=True)
    assert any("exit 7" in p for p in problems2), problems2


def test_links_are_append_only_and_traceable_to_commit(tmp_path: Path, monkeypatch):
    _fake_repo(tmp_path, monkeypatch)
    links = tmp_path / "links"
    lay = sc.load_layout()
    p1 = sc.write_link(sc.create_link("card_authoring", functionary="human:X",
                                      now="2026-09-19T18:00:00", layout=lay), links)
    p2 = sc.write_link(sc.create_link("card_authoring", functionary="human:X",
                                      now="2026-09-19T18:00:00", layout=lay), links)
    assert p1 != p2 and len(sc.load_links(links)) == 2, "同时间戳也不许覆盖历史"
    rec = sc.read_link(p1)
    assert "signature" in rec, "link 必须记 git commit（可追溯；非密码学签名）"
