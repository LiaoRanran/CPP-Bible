"""632 E1 · L2.3 探针单测（纯标准库，≥5 例）。

聚焦 `coverage_probe_l2_3_632`：陈旧证据留痕的结构性覆盖探针。
编号 E1-L2.3-1..E1-L2.3-6。
"""
from __future__ import annotations

import os

import tools.coverage_probe_l2_3_632 as m


def _write_card(path: str, body: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)


# E1-L2.3-1：frontmatter 解析
def test_parse_frontmatter_keys(tmp_path):
    p = tmp_path / "EV.md"
    p.write_text("---\nid: X\nartifact_sha256: abc\n---\nbody\n", encoding="utf-8")
    fm = m.parse_frontmatter(str(p))
    assert fm.get("id") == "X"
    assert fm.get("artifact_sha256") == "abc"


# E1-L2.3-2：产物 sha 漂移被识别
def test_artifact_drift_detected(tmp_path):
    ap = tmp_path / "x.asm"
    ap.write_bytes(b"hello")
    card = tmp_path / "EV-X.md"
    card.write_text(f"---\nid: EV-X\nartifact: {ap}\nartifact_sha256: deadbeef\n---\n",
                    encoding="utf-8")
    r = m.analyze_card(str(card))
    assert r["artifact_declared"] is True
    assert r["drift_detected"] is True


# E1-L2.3-3：留痕字段被识别
def test_staleness_field_recognized(tmp_path):
    card = tmp_path / "EV-Y.md"
    card.write_text("---\nid: EV-Y\nupstream_version: 3\n---\n",
                    encoding="utf-8")
    r = m.analyze_card(str(card))
    assert r["has_staleness_field"] is True
    assert r["artifact_declared"] is False


# E1-L2.3-4：无 artifact 声明时不误报漂移
def test_no_artifact_no_false_drift(tmp_path):
    card = tmp_path / "EV-Z.md"
    card.write_text("---\nid: EV-Z\nstatus: verified\n---\n",
                    encoding="utf-8")
    r = m.analyze_card(str(card))
    assert r["artifact_declared"] is False
    assert r["drift_detected"] is None


# E1-L2.3-5：measure 结构完整（只读扫描真实 evidence 目录）
def test_measure_structure():
    out = m.measure()
    assert out.get("vector") == "L2.3"
    assert "cards_scanned" in out
    assert "detection_capable" in out


# E1-L2.3-6：--check 自检通过（exit 0）
def test_selftest_passes():
    assert m.selftest() == 0
