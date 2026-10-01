# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D1：规则版本钉扎红绿路径（10 条）。"""
from __future__ import annotations

import json

import rules_manifest_671g as M


class _R:
    def __init__(self, id_, title="t", severity="block"):
        self.id, self.title, self.severity = id_, title, severity
        self.kind = "k"; self.basis = "b"; self.quadrant = "q"
        self.scope = "s"; self.automated = True; self.meta = {}; self.check = None


def test_real_manifest_present_and_matches():
    man = M.load_manifest(M.ROOT)
    assert man and man["count"] == 67 and man["rules_version"] == "1.0.0"
    assert M.verify(M.ROOT) == []


def test_manifest_deterministic(tmp_path, monkeypatch):
    import sys, types
    mod = types.ModuleType("fake_gate_engine")
    mod.RULES = [_R("R1"), _R("R2")]
    sys.modules["gate_engine"] = mod
    try:
        m1 = M.compute_manifest(tmp_path, version="1.0.0")
        m2 = M.compute_manifest(tmp_path, version="1.0.0")
    finally:
        sys.modules.pop("gate_engine", None)
    assert m1["rules_sha256"] == m2["rules_sha256"]
    assert m1["count"] == 2 and m1["severity"]["block"] == 2


def test_manifest_changes_when_rule_changes(tmp_path, monkeypatch):
    import sys, types
    m1mod = types.ModuleType("gate_engine"); m1mod.RULES = [_R("R1")]
    sys.modules["gate_engine"] = m1mod
    try:
        m1 = M.compute_manifest(tmp_path, version="1.0.0")
    finally:
        sys.modules.pop("gate_engine", None)
    m2mod = types.ModuleType("gate_engine"); m2mod.RULES = [_R("R1"), _R("R2")]
    sys.modules["gate_engine"] = m2mod
    try:
        m2 = M.compute_manifest(tmp_path, version="1.0.0")
    finally:
        sys.modules.pop("gate_engine", None)
    assert m1["rules_sha256"] != m2["rules_sha256"]
    assert m2["count"] == 2


def test_verify_catches_count_drift(tmp_path, monkeypatch):
    import sys, types
    mod = types.ModuleType("gate_engine"); mod.RULES = [_R("R1")]
    sys.modules["gate_engine"] = mod
    man = {"rules_version": "1.0.0", "rules_sha256": "x", "engine_file_sha256": "y",
           "count": 99, "severity": {}, "rule_ids": ["R1"]}
    try:
        probs = M.verify(tmp_path, man)
    finally:
        sys.modules.pop("gate_engine", None)
    assert any("count" in p for p in probs) and any("sha256" in p for p in probs)


def test_verify_bad_semver(tmp_path):
    man = {"rules_version": "v1", "rules_sha256": "x", "engine_file_sha256": "y",
           "count": 0, "severity": {}, "rule_ids": []}
    assert any("语义化" in p for p in M.verify(tmp_path, man))


def test_verify_missing_manifest(tmp_path):
    assert any("缺失" in p for p in M.verify(tmp_path))


def test_stamp_and_verify_verdict(tmp_path, monkeypatch):
    import sys, types
    mod = types.ModuleType("gate_engine"); mod.RULES = [_R("R1")]
    sys.modules["gate_engine"] = mod
    man = M.compute_manifest(tmp_path, version="1.0.0")
    try:
        vd = tmp_path / "data" / "671g" / "verdicts"
        vd.mkdir(parents=True)
        vp = vd / "v1.json"
        vp.write_text('{"verdict": "catch"}', encoding="utf-8")
        M.stamp_verdict(tmp_path, vp, man)
        assert M.verify_verdicts(tmp_path, vd, man) == []
    finally:
        sys.modules.pop("gate_engine", None)


def test_verify_verdict_stale_sha_blocks(tmp_path, monkeypatch):
    import sys, types
    mod = types.ModuleType("gate_engine"); mod.RULES = [_R("R1")]
    sys.modules["gate_engine"] = mod
    man = M.compute_manifest(tmp_path, version="1.0.0")
    try:
        vd = tmp_path / "data" / "671g" / "verdicts"
        vd.mkdir(parents=True)
        (vd / "v.json").write_text(json.dumps(
            {"verdict": "catch", "rules_version": "1.0.0", "rules_sha256": "stale"}),
            encoding="utf-8")
        f = M.verify_verdicts(tmp_path, vd, man)
    finally:
        sys.modules.pop("gate_engine", None)
    assert f and f[0]["rule"] == "G-RULES-PINNED"


def test_verify_verdict_wrong_version_blocks(tmp_path, monkeypatch):
    man = {"rules_version": "2.0.0", "rules_sha256": "x"}
    vd = tmp_path / "data" / "671g" / "verdicts"
    vd.mkdir(parents=True)
    (vd / "v.json").write_text(json.dumps(
        {"verdict": "catch", "rules_version": "1.0.0", "rules_sha256": "x"}),
        encoding="utf-8")
    f = M.verify_verdicts(tmp_path, vd, man)
    assert f and "rules_version" in f[0]["message"]


def test_gate_real_repo_green():
    import gate_rules_671g as G
    f = [x for x in G.run_all(G.ROOT) if x["rule"] == "G-RULES-PINNED"]
    assert [x for x in f if x["severity"] == "block"] == []
