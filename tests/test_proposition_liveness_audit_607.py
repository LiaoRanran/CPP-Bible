"""607 任务 3 · `proposition_liveness_audit.py` 回归锁（只读审计）。

锁的是审计口径与**只读边界**：
  * observation / inference 分别计数，inference 不进任何异常分类（gate 只要求 observation 有锚）；
  * 无 `liveness` 的 observation ⇒ `missing`（gate 必报 warn）；
  * `kind: fixture_symbol` 但 `symbol` 空 ⇒ `missing_symbol`；未知 `kind` ⇒ `unknown_kind`；
  * `kind: external_basis` 的 observation ⇒ `needs_review`（单列）；
  * 已有合规锚的 observation **不被**标记；
  * `--json` 输出合法 JSON、`--check` 写报告且 exit 0；
  * 审计**不动任何命题卡**（跑前跑后文件指纹一致）。

全部在 `tmp_path` 假库上跑（`--atoms-root` 注入），不碰真实 `atoms/`。
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import proposition_liveness_audit as lv

OBS_MISSING = """  - id: prop-1
    subject: s
    predicate: p
    object: o
    claim_type: observation
    statement: 缺锚的观测句。
    evidence: [EV-T-001]
"""

OBS_OK = """  - id: prop-1
    claim_type: observation
    statement: 有夹具锚的观测句。
    evidence: [EV-T-002]
    liveness:
      kind: fixture_symbol
      symbol: FIX_LOCK_001
"""

OBS_EXTERNAL = """  - id: prop-1
    claim_type: observation
    statement: 靠外部标准背书的观测句。
    liveness:
      kind: external_basis
      symbol: ISO/IEC 14882:2023
"""

OBS_EMPTY_SYMBOL = """  - id: prop-1
    claim_type: observation
    statement: 锚的种类对但符号空。
    liveness:
      kind: fixture_symbol
      symbol: ""
"""

OBS_UNKNOWN_KIND = """  - id: prop-1
    claim_type: observation
    statement: 锚的种类不认识。
    liveness:
      kind: oracle
      symbol: FIX_ORACLE
"""

INFERENCE = """  - id: prop-2
    claim_type: inference
    statement: 推断句。
    external_basis: "ISO/IEC 14882:2023 [atomics.order]"
"""


def _card(root: Path, sub: str, card_id: str, props: str) -> Path:
    p = root / sub / f"{card_id}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"---\nid: {card_id}\ntitle: 测试卡\nclaim_structured:\n{props}---\n\n正文。\n",
                 encoding="utf-8")
    return p


def _fake_atoms(tmp_path: Path) -> Path:
    """6 卡 / 7 命题：observation 5（missing / ok / needs_review / missing_symbol / unknown_kind）
    + inference 2（其中 1 张卡只有 inference ⇒ 不该进清单）。"""
    root = tmp_path / "atoms"
    _card(root, "a", "ATOM-T-A-001", OBS_MISSING + INFERENCE)
    _card(root, "b", "ATOM-T-B-001", OBS_OK)
    _card(root, "c", "ATOM-T-C-001", OBS_EXTERNAL)
    _card(root, "d", "ATOM-T-D-001", OBS_EMPTY_SYMBOL)
    _card(root, "e", "ATOM-T-E-001", OBS_UNKNOWN_KIND)
    _card(root, "f", "ATOM-T-F-001", INFERENCE)
    return root


def _ids(entries: list[dict]) -> set[str]:
    return {e["id"] for e in entries}


def _all_missing(res: dict) -> list[dict]:
    return [e for c in res["cards"] for e in c["missing"]]


def _all_review(res: dict) -> list[dict]:
    return [e for c in res["cards"] for e in c["needs_review"]]


# ── 计数口径 ────────────────────────────────────────────────────────────────
def test_counts_observation_and_inference(tmp_path: Path):
    res = lv.audit(_fake_atoms(tmp_path))
    assert res["propositions"] == {"total": 7, "observation": 5, "inference": 2, "other": 0}
    assert res["liveness"]["with"] == 4 and res["liveness"]["without"] == 3
    assert res["liveness"]["by_kind"] == {"fixture_symbol": 2, "external_basis": 1, "oracle": 1}
    st = res["observation_status"]
    assert (st["ok"], st["missing"], st["missing_symbol"], st["unknown_kind"], st["needs_review"]) \
        == (1, 1, 1, 1, 1), st


# ── 缺锚 / 锚不合格都被列出，且按卡分组 ─────────────────────────────────────
def test_missing_liveness_marked(tmp_path: Path):
    res = lv.audit(_fake_atoms(tmp_path))
    by_card = {c["card"]: c["missing"] for c in res["cards"]}
    assert _ids(by_card["ATOM-T-A-001"]) == {"prop-1"}, by_card       # 完全没 liveness
    assert by_card["ATOM-T-A-001"][0]["status"] == "missing"
    assert by_card["ATOM-T-D-001"][0]["status"] == "missing_symbol"    # kind 对、symbol 空
    assert by_card["ATOM-T-E-001"][0]["status"] == "unknown_kind"      # kind 不认
    assert by_card["ATOM-T-E-001"][0]["kind"] == "oracle"
    assert len(_all_missing(res)) == 3 and res["missing_cards"] == 3
    assert res["review_cards"] == 1, "needs_review 的卡不与缺锚卡混计"
    # inference 不进任何异常清单
    assert "ATOM-T-F-001" not in by_card


# ── 已有合规锚的命题不被标记 ────────────────────────────────────────────────
def test_existing_liveness_not_marked(tmp_path: Path):
    res = lv.audit(_fake_atoms(tmp_path))
    assert "ATOM-T-B-001" not in {c["card"] for c in res["cards"]}, res["cards"]
    assert res["observation_status"]["ok"] == 1


# ── external_basis 的 observation ⇒ needs_review（且不混进 missing）──────────
def test_external_basis_needs_review(tmp_path: Path):
    res = lv.audit(_fake_atoms(tmp_path))
    review = _all_review(res)
    assert len(review) == 1 and review[0]["kind"] == "external_basis", review
    card = next(c for c in res["cards"] if c["card"] == "ATOM-T-C-001")
    assert _ids(card["needs_review"]) == {"prop-1"} and card["missing"] == []


# ── CLI：--json 合法、--check 写报告并 exit 0，且全程只读 ────────────────────
def test_cli_json_and_check_are_readonly(tmp_path: Path, capsys):
    root = _fake_atoms(tmp_path)
    snap = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*.md"))}

    assert lv.main(["--json", "--atoms-root", str(root)]) == 0
    res = json.loads(capsys.readouterr().out)
    assert res["propositions"]["observation"] == 5
    assert res["observation_status"]["needs_review"] == 1

    report = tmp_path / "out" / "liveness.md"
    assert lv.main(["--check", "--atoms-root", str(root), "--report", str(report)]) == 0
    text = report.read_text(encoding="utf-8")
    assert "命题活性锚审计" in text and "ATOM-T-A-001" in text
    assert "needs_review" in text and "external_basis" in text

    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*.md"))}
    assert after == snap, "审计不得改动任何命题卡"


def test_missing_atoms_root_returns_2(tmp_path: Path):
    assert lv.main(["--check", "--atoms-root", str(tmp_path / "nope"),
                    "--report", str(tmp_path / "r.md")]) == 2
