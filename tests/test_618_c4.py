#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 C4 · test_category_map 单测（≥3 例）"""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import test_category_map as m  # noqa: E402


def test_build_has_entry():
    with tempfile.TemporaryDirectory() as d:
        p1 = os.path.join(d, "test_g.py")
        open(p1, "w").write("import gate_engine\n")
        p2 = os.path.join(d, "test_u.py")
        open(p2, "w").write("q=1\n")
        mapping = m.build(d)
        assert "test_g.py" in mapping and "test_u.py" in mapping
        assert "gate" in mapping["test_g.py"]["categories"]
        assert mapping["test_g.py"]["is_real_verification"] is True
        assert mapping["test_u.py"]["is_real_verification"] is False
        assert mapping["test_u.py"]["categories"] == ["其他"]


def test_render_schema_and_counts():
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "test_g.py"), "w").write("import gate_engine\n")
        open(os.path.join(d, "test_s.py"), "w").write("import snapshot_manifest\n")
        meta = m.render(m.build(d))
        assert meta["counts"]["total"] == 2
        # test_s 为 snapshot（脚本自测）→ 非真实验证
        assert meta["counts"]["real_verification"] == 1
        assert "map" in meta and "schema" in meta


def test_json_roundtrip(tmp_path=None):
    import tempfile
    ctx = tempfile.TemporaryDirectory() if tmp_path is None else None
    base = ctx.name if ctx is not None else str(tmp_path)
    try:
        out = os.path.join(base, "cat.json")
        with tempfile.TemporaryDirectory() as d:
            open(os.path.join(d, "test_g.py"), "w").write("import gate_engine\n")
            meta = m.render(m.build(d))
        with open(out, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)
        with open(out, encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["counts"]["total"] == 1
        assert loaded["map"]["test_g.py"]["is_real_verification"] is True
    finally:
        if ctx is not None:
            ctx.cleanup()


def test_membership_consistency_with_c2():
    # C4 映射与 C2 分类成员关系一致
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "test_p.py"), "w").write("import poison_drill\n")
        open(os.path.join(d, "test_r.py"), "w").write("import atom_evidence_replay\n")
        mapping = m.build(d)
        assert "poison" in mapping["test_p.py"]["categories"]
        assert "replay" in mapping["test_r.py"]["categories"]


if __name__ == "__main__":
    test_build_has_entry()
    test_render_schema_and_counts()
    test_json_roundtrip(None)
    test_membership_consistency_with_c2()
    print("ALL C4 TESTS PASSED")
