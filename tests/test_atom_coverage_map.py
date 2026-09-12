"""锁定 atom_coverage_map 的三次真实事故（2026-09-10 G1 监工验收）。

1. 文档域表手抄漂移：合计行「纯注释 148」vs 实算 139，而 `--check` 只查覆盖率所以放行
   → 新增 `--check-doc`（doc_diff）逐格勾稽。
2. `--fix-doc` 行尾污染：CRLF 文件走 `decode().split("\\n")` + `"\\r\\n".join()` 会产出
   `\\r\\r\\n`（实测 126 处双回车、diff 全文件 130 行）→ 必须 bytes 层按真实 eol 切分。
3. `--fix-doc` 抹掉排版：域行只加粗 UNVERIFIED 一列（强调最薄弱项）、合计行整行加粗，
   无条件重写整行会去掉加粗 → 逐格保留原标记，只替换数字值。
"""
from __future__ import annotations

from pathlib import Path

import atom_coverage_map as acm

HEADER = (
    "| 域 | 章数 | cpp 块 | 含 main | 纯注释块 | VERIFIED | UNVERIFIED |\r\n"
    "|---|---|---|---|---|---|---|\r\n"
)
MEM_ROW = "| MEM | 1 | 1108 | 720 | 12 | 29 | 55 |\r\n"      # 域章数与 _rows() 一致（每域 1 条章记录）
STL_ROW = "| STL | 1 | 828 | 742 | 8 | 3 | **89** |\r\n"       # UNVERIFIED 列有意加粗
TOTAL_OK = "| **合计** | **2** | **1936** | **1462** | **20** | **32** | **144** |\r\n"
TOTAL_BAD = "| **合计** | **2** | **1936** | **1462** | **20** | **32** | **148** |\r\n"


def _rows() -> list[dict]:
    return [
        {"domain": "MEM", "cpp_blocks": 1108, "with_main": 720,
         "pure_comment": 12, "verified": 29, "unverified": 55},
        {"domain": "STL", "cpp_blocks": 828, "with_main": 742,
         "pure_comment": 8, "verified": 3, "unverified": 89},
    ]


def _doc(tmp_path: Path, total: str) -> Path:
    p = tmp_path / "G1_knowledge_map.md"
    p.write_bytes(("# map\r\n\r\n" + HEADER + MEM_ROW + STL_ROW + total).encode("utf-8"))
    return p


def test_doc_diff_catches_hand_copied_total(tmp_path):
    """手抄合计与实算不一致必须被抓住（事故 1 的回归锁）。"""
    rows = _rows()
    diffs = acm.doc_diff(_doc(tmp_path, TOTAL_BAD), acm._agg(rows), rows, [])
    assert any("合计.unverified" in d and "148" in d for d in diffs), diffs


def test_doc_diff_accepts_bold_and_matching_total(tmp_path):
    """文档与实算一致时零差异；数字加粗（`**89**`）不得被误判。"""
    rows = _rows()
    assert acm.doc_diff(_doc(tmp_path, TOTAL_OK), acm._agg(rows), rows, []) == []


def test_fix_doc_is_byte_safe_keeps_bold_and_edits_one_line(tmp_path):
    """事故 2+3 的回归锁：只改需改的行、保 CRLF、无双回车、域行加粗不被抹。"""
    rows = _rows()
    doc = _doc(tmp_path, TOTAL_BAD)
    before = doc.read_bytes()
    n = acm.fix_doc(doc, acm._agg(rows), rows, [])
    raw = doc.read_bytes()

    assert n == 1, "只应改动合计行"
    assert b"\r\r\n" not in raw, "禁止双回车（行尾污染）"
    assert raw.count(b"\r\n") == before.count(b"\r\n"), "行数/行尾必须保持不变"
    assert b"| STL | 1 | 828 | 742 | 8 | 3 | **89** |" in raw, "域行加粗必须保留"
    total_line = "| **合计** | **2** | **1936** | **1462** | **20** | **32** | **144** |"
    assert total_line.encode("utf-8") in raw, "合计行须回填实算值且保留整行加粗"


def test_density_is_not_rounded_during_aggregation():
    """事故 2 的显示侧：89/828 = 10.7488%，显示 10.7%；聚合期 round(...,4) 会变 10.8%。"""
    agg = acm._agg(_rows())
    assert f"{agg['STL']['unverified_density']:.1%}" == "10.7%"
