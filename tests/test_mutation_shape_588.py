"""588 任务 0 · mutation_shape_audit 的回归测试（只读、幂等）。

不跑 replay / 不碰受控目录工件；只在内存里跑审计函数并比对。
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import mutation_shape_audit as audit

REPO = Path(__file__).resolve().parent.parent
CARDS = sorted((REPO / "evidence").rglob("EV-*.md")) + sorted(
    (REPO / "atoms").rglob("ATOM-*.md"))
CARDS = [c for c in CARDS if "README" not in c.name]


def _cards_snapshot() -> str:
    h = hashlib.sha256()
    for c in CARDS:
        h.update(c.read_bytes())
    return h.hexdigest()


def _run_audit() -> str:
    card_texts = audit._all_card_texts()
    mat = audit.matrix_audit(card_texts)
    shapes = audit.shape_audit(card_texts)
    crlf = audit.crlf_audit()
    return audit.build_report(mat, shapes, crlf)


def test_audit_idempotent():
    """对固定卡集连跑两次，审计台账逐字相同（可复现）。"""
    a = _run_audit()
    b = _run_audit()
    assert a == b, "审计输出非幂等"


def test_audit_readonly():
    """审计纯只读：跑前后 evidence/atoms 全部卡内容哈希不变。"""
    before = _cards_snapshot()
    _run_audit()
    after = _cards_snapshot()
    assert before == after, "审计改动了受控目录卡文件"


def test_matrix_block_finder_counts_evmem004():
    """宽容探测应数到带键行尾注释的 EV-MEM-004（0a 漏网依据）。"""
    texts = audit._all_card_texts()
    by_id = {rel: t for rel, t in texts}
    assert "evidence/mem/EV-MEM-004.md" in by_id
    ki, block = audit.find_matrix_block(by_id["evidence/mem/EV-MEM-004.md"])
    assert ki >= 0 and block, "宽容探测漏掉了 EV-MEM-004 的 matrix 块"


def test_no_crlf_in_corpus_or_invariant():
    """0c：全库应无 CRLF 卡，且 LF/CRLF 同构对拍不变。"""
    crlf = audit.crlf_audit()
    assert crlf["crlf"] == 0 and crlf["mixed"] == 0, "全库出现 CRLF，需重评"
    assert crlf["diffs"] == [], f"LF/CRLF 同构对拍有差异：{crlf['diffs']}"
