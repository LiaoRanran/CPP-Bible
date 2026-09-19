"""596 任务1 · 候选攻击边生成器回归锁。

锁四件事：
  * 正例：沙箱误区库 + 原子卡 ⇒ 每条 `mis_to_prop` **必须配一条对称边** `prop_to_mis`
    （594 实证：没有对称边 W2 必然退化）；
  * 反例：无关联 / 指向不存在的卡 / 重复关联 / 无 claim_structured，都不许把边造出来；
  * 幂等：同输入两次生成**逐字节一致**（`generated_at` 默认 null 就是为此）；
  * 真实语料：42 个 MIS 带 `related_atoms` ⇒ 194 条 `mis_to_prop`（594 数字**独立复算一致**）。
"""
from __future__ import annotations

from pathlib import Path

import attack_edge_generator as aeg

ATOM = """---
id: ATOM-SYN-001
claim_structured:
  - id: prop-1
    claim_type: observation
    statement: 合成命题一
  - id: prop-2
    claim_type: inference
    statement: 合成命题二
---
body
"""


def _mis(mid: str, **fields) -> str:
    lines = [f"id: {mid}", f"name: {mid} 合成误解", "refutations:", "  - 这是错的（合成反例）"]
    for k, v in fields.items():
        lines.append(f"{k}: {v}")
    return "---\n" + "\n".join(lines) + "\n---\nbody\n"


def _sandbox(tmp_path: Path, mis_files: dict[str, str], atom: str = ATOM):
    mis_dir = tmp_path / "misconceptions"
    atoms_dir = tmp_path / "atoms"
    mis_dir.mkdir(parents=True, exist_ok=True)
    atoms_dir.mkdir(parents=True, exist_ok=True)
    for name, text in mis_files.items():
        (mis_dir / f"{name}.md").write_text(text, encoding="utf-8")
    (atoms_dir / "ATOM-SYN-001.md").write_text(atom, encoding="utf-8")
    return mis_dir, atoms_dir


# ── 正例 ───────────────────────────────────────────────────────────────────────
def test_generate_makes_paired_edges_with_full_fields(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {"MIS-SYN-001": _mis("MIS-SYN-001",
                                                                 related_atoms="[ATOM-SYN-001]")})
    edges, warn = aeg.generate_edges(mis_dir, atoms_dir)
    assert warn == []
    # 2 命题 × (mis_to_prop + prop_to_mis)
    assert len(edges) == 4
    fwd = [e for e in edges if e["direction"] == "mis_to_prop"]
    rev = [e for e in edges if e["direction"] == "prop_to_mis"]
    assert len(fwd) == len(rev) == 2, "每条 mis_to_prop 必须配一条对称边（W2 的必要条件）"
    assert {e["kind"] for e in fwd} == {"related_atom"}
    assert {e["kind"] for e in rev} == {"misconception_refutation"}
    for e in edges:
        assert set(e) == {"id", "source", "target", "kind", "evidence", "confidence",
                          "direction", "generated_at", "generator_version"}
        assert e["id"] == f"ae-{e['source']}->{e['target']}"
        assert e["confidence"] == "low" and e["generated_at"] is None
        assert len(e["evidence"]) <= aeg.EVIDENCE_MAX
        assert e["generator_version"] == aeg.VERSION
    assert {e["target"] for e in fwd} == {"ATOM-SYN-001::prop-1", "ATOM-SYN-001::prop-2"}
    assert {e["target"] for e in rev} == {"MIS-SYN-001"}
    assert {e["source"] for e in rev} == {"ATOM-SYN-001::prop-1", "ATOM-SYN-001::prop-2"}


def test_confidence_grading_high_medium_low(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-H": _mis("MIS-SYN-H", related_atoms="[ATOM-SYN-001]", verified_by="human:X"),
        "MIS-SYN-M": _mis("MIS-SYN-M", related_atoms="[ATOM-SYN-001]", machine_verified="true"),
        "MIS-SYN-L": _mis("MIS-SYN-L", related_atoms="[ATOM-SYN-001]"),
    })
    edges, _ = aeg.generate_edges(mis_dir, atoms_dir)
    got = {e["source"]: e["confidence"] for e in edges if e["direction"] == "mis_to_prop"}
    assert got == {"MIS-SYN-H": "high", "MIS-SYN-M": "medium", "MIS-SYN-L": "low"}
    assert aeg.CONFIDENCE_WEIGHT == {"high": 3, "medium": 2, "low": 1}


# ── 反例 ───────────────────────────────────────────────────────────────────────
def test_no_related_atoms_makes_no_edges(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {"MIS-SYN-002": _mis("MIS-SYN-002")})
    edges, warn = aeg.generate_edges(mis_dir, atoms_dir)
    assert edges == [] and warn == [], "无关联的误解不得凭空造边"


def test_dangling_atom_ref_warns_and_skips_without_crash(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-003": _mis("MIS-SYN-003",
                            related_atoms="[ATOM-NOT-EXIST, ATOM-SYN-001]")})
    edges, warn = aeg.generate_edges(mis_dir, atoms_dir)
    assert len(warn) == 1 and "ATOM-NOT-EXIST" in warn[0]
    assert len(edges) == 4, "合法的那张卡仍要正常产边（跳过 ≠ 整条丢弃）"


def test_duplicate_related_atoms_dedup(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-004": _mis("MIS-SYN-004",
                            related_atoms="[ATOM-SYN-001, ATOM-SYN-001]")})
    edges, warn = aeg.generate_edges(mis_dir, atoms_dir)
    assert len(edges) == 4 and warn == []
    assert len({e["id"] for e in edges}) == 4, "同 (source,target,kind) 只能留一条"


def test_card_without_claim_structured_makes_no_edges(tmp_path: Path):
    no_claim = "---\nid: ATOM-SYN-001\nstatus: draft\n---\nbody\n"
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-005": _mis("MIS-SYN-005", related_atoms="[ATOM-SYN-001]")}, atom=no_claim)
    edges, warn = aeg.generate_edges(mis_dir, atoms_dir)
    assert edges == [] and warn == []


# ── 幂等 / 校验 ────────────────────────────────────────────────────────────────
def test_generate_is_bytewise_idempotent(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-001": _mis("MIS-SYN-001", related_atoms="[ATOM-SYN-001]")})
    e1, _ = aeg.generate_edges(mis_dir, atoms_dir)
    e2, _ = aeg.generate_edges(mis_dir, atoms_dir)
    p1 = aeg.write_edges(e1, tmp_path / "a.jsonl")
    p2 = aeg.write_edges(e2, tmp_path / "b.jsonl")
    assert p1.read_bytes() == p2.read_bytes(), "同输入两次生成必须逐字节一致"


def test_check_passes_then_catches_tampering(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-001": _mis("MIS-SYN-001", related_atoms="[ATOM-SYN-001]")})
    edges, _ = aeg.generate_edges(mis_dir, atoms_dir)
    assert aeg.check(edges, mis_dir=mis_dir, atoms_dir=atoms_dir) == []
    # 可证伪：删一条 ⇒ 复算不一致
    bad = edges[:-1]
    assert any("不一致" in p for p in aeg.check(bad, mis_dir=mis_dir, atoms_dir=atoms_dir))
    # 可证伪：字段缺失 / target 不存在 / id 重复
    broken = [dict(e) for e in edges]
    broken[0].pop("evidence")
    assert any("缺字段" in p for p in aeg.check(broken, mis_dir=mis_dir, atoms_dir=atoms_dir))
    gone = [dict(e) for e in edges]
    gone[0]["target"] = "ATOM-SYN-999::prop-9"
    assert any("不存在" in p for p in aeg.check(gone, mis_dir=mis_dir, atoms_dir=atoms_dir))
    dup = [dict(e) for e in edges] + [dict(edges[0])]
    assert any("重复 id" in p for p in aeg.check(dup, mis_dir=mis_dir, atoms_dir=atoms_dir))


def test_cli_generate_stats_check_exit_codes(tmp_path: Path):
    mis_dir, atoms_dir = _sandbox(tmp_path, {
        "MIS-SYN-001": _mis("MIS-SYN-001", related_atoms="[ATOM-SYN-001]")})
    out = tmp_path / "cand.jsonl"
    assert aeg.main(["generate", "--mis-dir", str(mis_dir), "--atoms-dir", str(atoms_dir),
                     "--out", str(out)]) == 0
    assert aeg.main(["stats", "--out", str(out), "--json"]) == 0
    assert aeg.main(["--check", "--out", str(out), "--mis-dir", str(mis_dir),
                     "--atoms-dir", str(atoms_dir)]) == 0
    out.write_text("", encoding="utf-8")
    assert aeg.main(["--check", "--out", str(out), "--mis-dir", str(mis_dir),
                     "--atoms-dir", str(atoms_dir)]) == 2


# ── 真实语料（594 数字独立复算）────────────────────────────────────────────────
def test_real_corpus_reproduces_594_numbers():
    """594 说：42 个 MIS 带 `related_atoms`、194 条候选边。**独立复算**必须一致。"""
    mis = aeg.read_mis()
    with_rel = [k for k, v in mis.items() if v["related_atoms"]]
    edges, warn = aeg.generate_edges()
    fwd = [e for e in edges if e["direction"] == "mis_to_prop"]
    assert len(mis) == 79 and len(with_rel) == 42, f"带 related_atoms 的 MIS 数漂移：{len(with_rel)}"
    assert len(fwd) == 194, f"MIS→命题边数漂移：{len(fwd)}"
    assert len(edges) == 388, "对称边必须 1:1 配齐（194 + 194）"
    assert warn == [], f"真实语料不该有悬空引用：{warn[:3]}"
