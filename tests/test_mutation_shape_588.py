"""588 任务 0 · mutation_shape_audit 的回归测试（只读、幂等）。

不跑 replay / 不碰受控目录工件；只在内存里跑审计函数并比对。
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import mutation_shape_audit as audit
from mutation_fuzz import _mut_matrix_values

N = "\n"

# 588 任务 1.2 回归基线：含四键（compiler/std/opt/arch）的干净 matrix 卡，预期恰好 7 个变体。
_CLEAN_MATRIX_CARD = (
    "---" + N + "id: X" + N + "matrix:" + N
    + "  compiler: [GCC 13.1.0]" + N + "  std: [c++17]" + N
    + "  opt: [-O2]" + N + "  arch: [x86-64]" + N
    + "fixture: a.cpp" + N + "---" + N + "b"
)
_EXPECTED_CLEAN_POINTS = {
    "matrix 删键（移除 compiler: [GCC 13.1.0]）",
    "matrix 非法值（compiler: [GCC 13.1.0] → 首元素 totally-not-a-compiler xyz）",
    "matrix 删键（移除 std: [c++17]）",
    "matrix 非法值（std: [c++17] → 首元素 c++99）",
    "matrix 删键（移除 opt: [-O2]）",
    "matrix 非法值（opt: [-O2] → 首元素 -O9）",
    "matrix 非法值（arch: [x86-64] → 首元素 z80-nonexistent）",
}


def _tail_comment_card() -> str:
    return ("---" + N + "id: Y" + N + "matrix:                          # 尾注释：笛卡尔声明"
            + N + "  compiler: [GCC 13.1.0]" + N + "  std: [c++17]" + N
            + "  opt: [-O2]" + N + "  arch: [x86-64]" + N
            + "fixture: a.cpp" + N + "---" + N + "b")


def _inline_comment_card() -> str:
    return ("---" + N + "id: Z" + N + "matrix:" + N
            + "  compiler: [GCC 13.1.0]" + N + "  # 注释：含冒号也不怕"
            + N + "  std: [c++17]" + N + "  opt: [-O2]" + N + "  arch: [x86-64]"
            + N + "fixture: a.cpp" + N + "---" + N + "b")

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


# ── 588 任务 1.2 · M6 matrix 正则放宽回归锁 ──────────────────────────────────────
def test_m6_matrix_clean_path_unchanged():
    """修尾注释不得顺手改正常路径：干净四键 matrix 卡仍恰产 7 个变体（3 删键 + 4 非法值）。"""
    pts = {p for p, _ in _mut_matrix_values(_CLEAN_MATRIX_CARD)}
    assert pts == _EXPECTED_CLEAN_POINTS, f"干净卡变体集漂移：{pts ^ _EXPECTED_CLEAN_POINTS}"


def test_m6_matrix_tail_comment_now_mutates():
    """① 矩阵键行带尾注释的卡，修后应正常产出 compiler/std/opt 三个删键变体（不再 0 变体）。"""
    vs = _mut_matrix_values(_tail_comment_card())
    pts = {p for p, _ in vs}
    assert len(vs) == 7, f"尾注释卡变体数应为 7，实得 {len(vs)}"
    for key in ("compiler", "std", "opt"):
        assert any(f"matrix 删键（移除 {key}:" in p for p in pts), f"缺 {key} 删键变体"


def test_m6_matrix_inline_comment_not_key():
    """② 块内整行注释（含冒号）不得被当成 matrix 键、不得造伪变体；std/opt 变体仍在。"""
    vs = _mut_matrix_values(_inline_comment_card())
    pts = {p for p, _ in vs}
    assert len(vs) == 7, f"块内注释卡变体数应为 7，实得 {len(vs)}"
    # 注释文本绝不应出现在任何变体 point 里（未被当成键）
    assert all("comment" not in p for p in pts), "注释行被误当成键/变体"
    for key in ("compiler", "std", "opt"):
        assert any(f"matrix 删键（移除 {key}:" in p for p in pts), f"缺 {key} 删键变体"


def test_m6_matrix_crlf_eq_lf():
    """④ CRLF 版与 LF 版同内容卡的 matrix 变体集（归一 \\r）应逐字相等。"""
    lf = {(p, v.replace("\r\n", "\n").replace("\r", "\n"))
          for p, v in _mut_matrix_values(_CLEAN_MATRIX_CARD)}
    cr = {(p, v.replace("\r\n", "\n").replace("\r", "\n"))
          for p, v in _mut_matrix_values(_CLEAN_MATRIX_CARD.replace("\n", "\r\n"))}
    assert lf == cr, "matrix 变体在 CRLF 下与 LF 不一致"
