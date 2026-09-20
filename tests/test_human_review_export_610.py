"""610 A3 · 人审数据导出回归锁（JSON/CSV/Markdown/单 MIS + --check）。

锁五件事（任务书 5 例 + 2 例自加）：
  1. export_json：**388** 条，且每条被候选边补全出 source/target/direction/kind（无 UNKNOWN）；
  2. export_csv：表头逐字等于规定列顺序 + **388** 数据行；
  3. export_markdown_summary：含 **42** 个 MIS 的表格行；
  4. export_by_mis(MIS-LANG-001)：**6** 条（3 条 mis_to_prop + 3 条 prop_to_mis）；
  5. --check：三类导出件齐全且与源一致 ⇒ exit 0；
  +. 改一个导出件 ⇒ --check 必须报错；
  +. `verdict`/`confidence` 口径：modify ⇒ confidence 非空；approve ⇒ confidence 为空（不冒充改档）。
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import human_review_export as ex


def test_export_json(tmp_path: Path):
    p = ex.export_json(ex.load_annotations(), tmp_path / "hr.json")
    rows = json.loads(p.read_text(encoding="utf-8"))
    assert len(rows) == 388
    assert all(r["source"] != "UNKNOWN" for r in rows), "有记录未被候选边补全"
    assert all({"edge_id", "source", "target", "direction", "kind", "verdict",
                "reviewer", "reviewed_at", "reason"} <= set(r) for r in rows)
    assert {r["direction"] for r in rows} == {"mis_to_prop", "prop_to_mis"}


def test_export_csv(tmp_path: Path):
    p = ex.export_csv(ex.load_annotations(), tmp_path / "hr.csv")
    text = p.read_text(encoding="utf-8")
    lines = [x for x in text.splitlines() if x.strip()]
    assert lines[0].rstrip("\r") == ",".join(ex.CSV_COLUMNS)
    assert len(lines) - 1 == 388, f"CSV 数据行应为 388，实得 {len(lines) - 1}"
    with p.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 388
    assert sum(1 for r in rows if r["verdict"] == "modify") == 34
    # 口径检查：modify 必须有 confidence；approve 不得冒充改档
    mods = [r for r in rows if r["verdict"] == "modify"]
    apps = [r for r in rows if r["verdict"] == "approve"]
    assert all(r["confidence"] for r in mods) and all(not r["confidence"] for r in apps)
    assert all(int(r["reason_len"]) >= 47 for r in rows)


def test_export_markdown(tmp_path: Path):
    p = ex.export_markdown_summary(ex.load_annotations(), tmp_path / "s.md")
    text = p.read_text(encoding="utf-8")
    assert "MIS **42** 个" in text and "记录 **388** 条" in text
    rows = [ln for ln in text.splitlines() if ln.startswith("| `MIS-")]
    assert len(rows) == 42, f"表格应有 42 行 MIS，实得 {len(rows)}"
    assert "| `MIS-MEM-031` | 24 | 24 | 0 | 0 |" in text


def test_export_by_mis(tmp_path: Path):
    p = ex.export_by_mis(ex.load_annotations(), "MIS-LANG-001", tmp_path / "lang.json")
    doc = json.loads(p.read_text(encoding="utf-8"))
    assert doc["mis_id"] == "MIS-LANG-001" and doc["count"] == 6
    assert all(r["verdict"] == "modify" for r in doc["records"])
    assert sum(r["direction"] == "mis_to_prop" for r in doc["records"]) == 3
    assert sum(r["direction"] == "prop_to_mis" for r in doc["records"]) == 3


def test_check_consistency(tmp_path: Path):
    anns = ex.load_annotations()
    ex.export_all(tmp_path, annotations=anns)
    assert ex.check(tmp_path, annotations=anns) == []
    assert ex.main(["--dir", str(tmp_path), "--check"]) == 0


def test_check_catches_tampered_export(tmp_path: Path):
    anns = ex.load_annotations()
    ex.export_all(tmp_path, annotations=anns)
    (tmp_path / "human_review.json").write_text("[]\n", encoding="utf-8")
    assert ex.main(["--dir", str(tmp_path), "--check"]) == 2


def test_enrich_is_pure_and_deterministic(tmp_path: Path):
    anns = ex.load_annotations()
    assert ex.enrich(anns) == ex.enrich(anns)
    assert len(ex.enrich(anns)) == 388
