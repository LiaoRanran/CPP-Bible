# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""657 B 段回归锁：边界三元组回填（只加不改 + 四态真正跑起来）。

- 单元级：确定性哈希 / 只加不改 / 换行风格保留 / 幂等 / 无覆盖不编造；
- 集成级：真实 atoms 上「23 张 verified 卡带边界 ⇒ 四态 = pass」这条**行为**锁死
  （本批之前是 23 张全 unknown —— 锁必须能红，否则等于没锁）。
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import boundary_backfill_657 as bf  # noqa: E402

TARGET_ST = ("verified", "red-team-verified")


def _atoms_fp() -> str:
    h = hashlib.sha256()
    for p in bf.cards():
        h.update(str(Path(p).relative_to(ROOT)).encode())
        h.update(hashlib.sha256(Path(p).read_bytes()).digest())
    return h.hexdigest()


def _text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_plan_scans_all_47_cards() -> None:
    # 668 P2-3：标题里的 "47" 是当时的口径；断言改成**从 counts_659 现算**
    # （651/659 的既定规则：语料基数只认唯一权威源，不认写死的数字）。
    import counts_659 as counts

    rows = bf.plan()
    assert len(rows) == counts.ATOMS_TOTAL
    assert {r["action"] for r in rows} <= {"write", "skip"}
    for r in rows:
        assert r["card"].startswith("atoms/")
        assert "triplet" in r and "reason" in r


def test_plan_is_idempotent_after_apply() -> None:
    """B 段已落地 ⇒ 再跑应当无事可做（否则说明写入没成功）。"""
    writes = [r for r in bf.plan() if r["action"] == "write"]
    assert writes == [], [r["card"] for r in writes]


def test_verified_cards_carry_triplet_on_disk() -> None:
    n = 0
    for r in bf.plan():
        if r["status"] not in TARGET_ST:
            continue
        got = bf.existing_triplet(_text(r["card"]))
        assert bf.triplet_ok(got), f"{r['card']} 缺边界三元组 ⇒ 四态必降级 unknown"
        n += 1
    assert n == 26, f"应有 23 verified + 3 red-team-verified，实测 {n}"


def test_on_disk_triplet_equals_independent_recompute() -> None:
    """卡里的三元组必须能由 mutation 基线**独立重算**出来（不是手填）。"""
    for r in bf.plan():
        if r["status"] not in TARGET_ST:
            continue
        hit = bf.newest_baseline_for(r["card"])
        assert hit is not None, r["card"]
        assert bf.triplet_for(hit[1], hit[0]) == bf.existing_triplet(_text(r["card"])), r["card"]


def test_draft_cards_do_not_get_boundary() -> None:
    """draft 卡判决未定 ⇒ 不写边界（避免"未验证的卡被判成 pass"）。"""
    for r in bf.plan():
        if r["status"] == "draft":
            assert not bf.triplet_ok(bf.existing_triplet(_text(r["card"]))), r["card"]


def test_skipped_cards_never_carry_fabricated_hash() -> None:
    for r in bf.plan():
        if r["action"] == "skip" and not r["already"]:
            assert r["triplet"] == {}, r["card"]


def test_triplet_is_deterministic() -> None:
    hit = bf.newest_baseline_for("atoms/conc/ATOM-CONC-RACE-001.md")
    assert hit is not None
    assert bf.triplet_for(hit[1], hit[0]) == bf.triplet_for(hit[1], hit[0])


def test_empty_mutation_set_is_fail_closed() -> None:
    assert not bf.triplet_ok(bf.triplet_for([], "full_baseline_v7.json"))


def test_patch_only_adds_three_lines(tmp_path: Path) -> None:
    rel = "atoms/conc/ATOM-CONC-RACE-001.md"
    hit = bf.newest_baseline_for(rel)
    assert hit is not None
    tri = bf.triplet_for(hit[1], hit[0])
    stripped = "\n".join(ln for ln in (ROOT / rel).read_text(encoding="utf-8").split("\n")
                         if not ln.startswith(bf.FIELDS))
    dst = tmp_path / "c.md"
    dst.write_text(stripped, encoding="utf-8")
    new = bf.patched_text(dst.read_text(encoding="utf-8"), tri)
    assert "\n".join(ln for ln in new.splitlines()
                     if not ln.startswith(bf.FIELDS)) == "\n".join(stripped.splitlines())
    assert len([ln for ln in new.splitlines() if ln.startswith(bf.FIELDS)]) == 3


def test_patch_preserves_newline_style() -> None:
    """回填不得改变原卡换行风格（D1 CRLF 债务的前置约束）。"""
    seen = set()
    for r in bf.plan():
        if r["status"] not in TARGET_ST:
            continue
        raw = (ROOT / r["card"]).read_bytes()
        stripped = b"\n".join(ln for ln in raw.split(b"\n")
                              if not ln.startswith(tuple(f.encode() for f in bf.FIELDS)))
        got = bf.patched_text(stripped.decode("utf-8"), r["triplet"]).encode("utf-8")
        assert (b"\r\n" in got) == (b"\r\n" in raw), r["card"]
        seen.add("crlf" if b"\r\n" in raw else "lf")
    # 实测：本批回填对象全是 LF（CRLF 侧是 draft 卡，不在回填范围）
    assert seen == {"lf"}, f"实测风格 {seen}（若仓库换行收口，请更新此断言）"


def test_patch_handles_crlf_input() -> None:
    """机制层锁：CRLF 合成样本必须仍产 CRLF（回填对象当前全是 LF，机制单独锁）。"""
    tri = {"mutation_set_hash": "a" * 64, "mutation_count": "3",
           "generator_version": "full_baseline_v7.json"}
    crlf = "---\r\nstatus: verified\r\n---\r\n\r\nbody\r\n"
    got = bf.patched_text(crlf, tri)
    assert "\r\n" in got
    assert got.replace("\r\n", "") .count("\n") == 0


def test_check_is_read_only() -> None:
    before = _atoms_fp()
    assert bf.selftest() == 0
    assert _atoms_fp() == before


def test_cross_check_with_639_overlay() -> None:
    cc = bf.cross_check_639(bf.plan())
    assert cc["available"] is True
    assert cc["same"] == 23 and cc["diff"] == []


def test_four_state_actually_runs_after_backfill() -> None:
    """**行为锁**：补完边界后，23 张 verified 卡必须真的从 unknown 翻成 pass。"""
    import four_state_verdict_638 as fs

    a = fs.audit()
    assert len(a["cards"]) == 23
    assert a["cards_with_boundary"] == 23
    assert a["card_dist"] == {"pass": 23}, a["card_dist"]


def test_readme_card_not_touched() -> None:
    """atoms/README.md 不是卡，不应被扫进回填范围。"""
    assert all(not r["card"].endswith("README.md") for r in bf.plan())
    assert "mutation_set_hash" not in _text("atoms/README.md")
