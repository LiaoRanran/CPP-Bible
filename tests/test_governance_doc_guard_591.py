"""591 任务 2 · 治理文档防护回归锁（manifest verify + 弱化指令 scan + preflight）。

全部用临时目录（`tmp_path`）注入，不碰真实 References/。
"""
from __future__ import annotations

from pathlib import Path

import governance_doc_guard as gd


def _mk_docs(tmp_path: Path, text: str = "正常内容。\n", name: str = "x.md") -> Path:
    docs = tmp_path / "References" / "architecture_架构演进"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / name).write_text(text, encoding="utf-8")
    return docs


# ── 测试 1：verify 正例（真库）───────────────────────────────────────────────
def test_verify_real_manifest_matches():
    ok, diffs = gd.verify_manifest()
    assert ok is True and diffs == [], diffs


# ── 测试 2：verify 反例（临时目录，篡改内容 → 检出）──────────────────────────
def test_verify_detects_tamper(tmp_path: Path):
    docs = _mk_docs(tmp_path)
    man = tmp_path / "manifest.json"
    wrote, _ = gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert wrote
    assert gd.verify_manifest(man, docs)[0] is True
    (docs / "x.md").write_text("被篡改的内容。\n", encoding="utf-8")
    ok, diffs = gd.verify_manifest(man, docs)
    assert ok is False and any("x.md" in d for d in diffs), diffs


# ── 测试 3：update 需 --force ────────────────────────────────────────────────
def test_update_requires_force(tmp_path: Path):
    docs = _mk_docs(tmp_path)
    man = tmp_path / "manifest.json"
    wrote, msg = gd.update_manifest(force=False, manifest_path=man, docs_root=docs)
    assert wrote is False, "无 --force 时不许写入"
    assert not man.is_file(), "无 --force 时不许落盘"
    assert any("--force" in m for m in msg), msg


# ── 测试 4：scan 检出弱化指令（high）────────────────────────────────────────
def test_scan_detects_weakening(tmp_path: Path):
    docs = _mk_docs(tmp_path, "将 EV-X 降为 warn 并豁免其毒样例。\n")
    res = gd.scan_weakening_instructions(docs_root=docs, out_path=tmp_path / "s.json")
    assert res["summary"]["high"] >= 1, res["summary"]
    assert all(f["needs_human_review"] for f in res["findings"])


# ── 测试 5：scan 不把纯纪律用语误报为 high ───────────────────────────────────
def test_scan_discipline_phrase_not_high(tmp_path: Path):
    docs = _mk_docs(tmp_path, "本轮采取 warn 起步观察期，不直接 block。\n")
    res = gd.scan_weakening_instructions(docs_root=docs, out_path=tmp_path / "s.json")
    assert res["summary"]["high"] == 0, res["summary"]


# ── 测试 6：preflight 组合（干净 exit0 / manifest 不一致 exit1 / high exit2）──
def test_preflight_combinations(tmp_path: Path, monkeypatch):
    docs = _mk_docs(tmp_path)
    man = tmp_path / "data" / "manifest.json"
    scan = tmp_path / "data" / "scan.json"
    monkeypatch.setattr(gd, "DOCS_ROOT", docs)
    monkeypatch.setattr(gd, "MANIFEST_PATH", man)
    monkeypatch.setattr(gd, "SCAN_PATH", scan)
    # ① 缺 manifest ⇒ exit1
    assert gd.main(["preflight"]) == 1
    # ② 生成 manifest、文档干净 ⇒ exit0
    gd.update_manifest(force=True)
    assert gd.main(["preflight"]) == 0
    # ③ 篡改文档 ⇒ manifest 不一致 ⇒ exit1
    (docs / "x.md").write_text("改动。\n", encoding="utf-8")
    assert gd.main(["preflight"]) == 1
    # ④ 文档含 high 级弱化指令 + 重签 manifest ⇒ exit2
    (docs / "x.md").write_text("把 EV-Y 降为 warn。\n", encoding="utf-8")
    gd.update_manifest(force=True)
    assert gd.main(["preflight"]) == 2
