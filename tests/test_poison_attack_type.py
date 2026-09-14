"""424 攻击面分类回归锁：A1-A11 全映射、A4/A8/A10 盲区补齐、新毒样例直验、台账防过期。"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge
import poison_drill as pd


def _fake_results() -> list[tuple[str, bool, str]]:
    """从 ATTACK_TYPES 静态映射构造样例结果（避免跑全量真编译钻探）。"""
    return [(name, True, "") for name, _t in pd.ATTACK_TYPES]


def test_all_poison_have_attack_type():
    """每条攻击载荷（阴性除外）都映射到 A1-A10 之一，无 A? 漏标。"""
    stats = pd.attack_type_stats(_fake_results())
    assert "A?" not in stats, "存在未分类的毒样例"
    assert set(stats) <= set(pd.ALL_ATTACK_TYPES)


def test_a4_coverage():
    """A4 时序穿链 ≥2（P33/P34 编译后覆写 + P38 陈旧留痕）。"""
    assert pd.attack_type_stats(_fake_results()).get("A4", 0) >= 2


def test_a8_coverage():
    """A8 间接注入 ≥2（P21 注释伪造出处 + P39 注释伪造符号）。"""
    assert pd.attack_type_stats(_fake_results()).get("A8", 0) >= 2


def test_a10_coverage():
    """A10 供应链 ≥2（P40 工具冒充 + P41 非编译器产出）。"""
    assert pd.attack_type_stats(_fake_results()).get("A10", 0) >= 2


def test_no_uncovered_attack_surface():
    """A1-A10 无零覆盖类——攻击者无从「无样本预警」的面打进来。"""
    stats = pd.attack_type_stats(_fake_results())
    unc = [a for a in pd.ALL_ATTACK_TYPES if stats.get(a, 0) == 0]
    assert unc == [], f"零覆盖攻击面：{unc}"


def test_negative_controls_excluded():
    """阴性对照不参与攻击面统计（它们验证「不误伤」）。"""
    stats = pd.attack_type_stats(
        [("P14 ", True, ""), ("P14-阴 声明完整放行", True, ""),
         ("阴性对照（干净）", True, "")])
    assert stats == {"A1": 1}, "阴性对照不得计入载荷统计"


def test_p40_impersonated_producer_blocked():
    """P40 直验：producer 声明 clang++、command 实际 g++ → block。"""
    from poison_drill import sandbox, _write
    with sandbox():
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A10IMPO.md", {
            "id": "EV-MEM-A10IMPO", "serves": "[]", "hypothesis": "h", "kind": "asm",
            "command": "g++ -std=c++17 -S fx.cpp -o fx.asm",
            "artifact_producer": "clang++ -std=c++17 -S fx.cpp -o fx.asm",
            "artifact": "fx.asm", "verdict": "confirm", "falsification": "f",
        })
        who = {f.rule_id for f in ge.check_evidence_artifact_producer()}
        assert "EV-ARTIFACT-PRODUCER" in who, "工具冒充（声明≠实现）必须 block"


def test_p41_non_compiler_producer_blocked():
    """P41 直验：非编译器 argv[0]（生成脚本）产出工件 → block。"""
    from poison_drill import sandbox, _write
    with sandbox():
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A10GEN.md", {
            "id": "EV-MEM-A10GEN", "serves": "[]", "hypothesis": "h", "kind": "asm",
            "command": "python gen_asm.py -o fx.asm",
            "artifact_producer": "python gen_asm.py -o fx.asm", "artifact": "fx.asm",
            "verdict": "confirm", "falsification": "f",
        })
        who = {f.rule_id for f in ge.check_evidence_artifact_producer()}
        assert "EV-ARTIFACT-PRODUCER" in who, "非编译器产出工件必须 block"


def test_p39_comment_injection_detected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P39 直验：断言文本只在夹具注释里 → 检出（出处空间剥注释）。"""
    fx = tmp_path / "_fx_a8.cpp"
    fx.write_text("// 出处伪造注释：_Z10fake_symv\nint main(){return 0;}\n",
                  encoding="utf-8")
    (tmp_path / "_fx_a8.asm").write_text("\tret\n", encoding="utf-8")
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    import poison_drill
    with poison_drill.sandbox():
        poison_drill._write(ge.EVIDENCE / "mem" / "EV-MEM-A8T.md", {
            "id": "EV-MEM-A8T", "serves": "[]", "hypothesis": "h", "kind": "asm",
            "fixture": fx.as_posix(), "artifact": (tmp_path / "_fx_a8.asm").as_posix(),
            "command": "g++ -S fx.cpp -o fx.asm",
            "artifact_assert": "\n  - {kind: contains, text: _Z10fake_symv}",
        })
        hits = ge.check_evidence_assert_symbol_mapped()
        assert any("_Z10fake_symv" in f.message for f in hits), \
            "注释伪造出处必须被检出（出处空间剥注释）"


# ── 424 台账 `tools/poison_surface_map.json` 回归锁（472 收尾）──────────────
# 背景：修前 `--by-type` 用**静态前缀表**计数（46 条），与实测 results（49 条）各说各话，
# 且 A11 已入表而文案/产物仍写 A1-A10。现口径单点化为「实测 results → 台账 → --by-type」。


def _static_prefix_counts() -> dict[str, int]:
    """静态前缀登记数（每前缀 1 条）——仅作「有无覆盖」与下界的对照，不作载荷数。"""
    by: dict[str, int] = {}
    for _pfx, t in pd.ATTACK_TYPES:
        by[t] = by.get(t, 0) + 1
    return by


def test_surface_map_schema_and_labels():
    """入库台账结构合法：类别集合 == A1-A11、每类带 label、覆盖率自洽。"""
    m = pd.load_surface_map()
    assert m is not None, ("tools/poison_surface_map.json 缺失或损坏——"
                           "跑 `python tools/poison_drill.py --write-surface-map`")
    assert m["schema"] == 1
    assert set(m["attack_types"]) == set(pd.ALL_ATTACK_TYPES)
    for a, info in m["attack_types"].items():
        assert info.get("label"), f"{a} 缺可读标签"
        assert info.get("count", -1) >= 0, f"{a} 计数非法"
    cov = m["coverage"]
    assert cov["total"] == len(pd.ALL_ATTACK_TYPES)
    assert cov["covered"] + len(cov["uncovered"]) == cov["total"]
    assert cov["uncovered"] == [], f"入库台账存在零覆盖攻击面：{cov['uncovered']}"


def test_surface_map_not_stale():
    """台账不得过期：每类「有无覆盖」须与静态登记表一致，且计数不低于静态下界。"""
    m = pd.load_surface_map()
    assert m is not None
    static = _static_prefix_counts()
    for a in pd.ALL_ATTACK_TYPES:
        got = m["attack_types"][a]["count"]
        assert (got > 0) == (static.get(a, 0) > 0), (
            f"{a} 台账计数 {got} 与静态登记 {static.get(a, 0)} 覆盖性不一致——"
            "增删毒样例后须重跑 --write-surface-map（否则 --by-type 会撒谎）")
        assert got >= static.get(a, 0), (
            f"{a} 台账计数 {got} 低于静态登记 {static.get(a, 0)}（同前缀多载荷只多不少）")


def test_surface_map_payload_types_valid():
    """逐条载荷类型必须落在 A1-A11（阴性对照 type=None），且全部为已拦截状态。"""
    m = pd.load_surface_map()
    assert m is not None
    assert m["payloads"], "台账无载荷明细"
    for p in m["payloads"]:
        assert p["type"] in pd.ALL_ATTACK_TYPES, f"未登记类型：{p}"
        assert p["pass"], f"台账里存在未拦截载荷（先修制衡）：{p}"
    for p in m["negative_controls"]:
        assert p["type"] is None, "阴性对照不得计入攻击面"
    assert sum(x["count"] for x in m["attack_types"].values()) == len(m["payloads"])


def test_build_surface_map_matches_measured_stats():
    """口径单点化：台账计数 == attack_type_stats 实测计数（不是静态前缀表）。"""
    fake = [("P1 x", True, ""), ("P16 a", True, ""), ("P16 b", True, ""),
            ("P14-阴 y", True, ""), ("阴性对照（z）", True, "")]
    m = pd.build_surface_map(3, 5, fake, (1, 2, []))
    assert m["attack_types"]["A1"]["count"] == 1, "P1 应计 1 条"
    assert m["attack_types"]["A2"]["count"] == 2, "P16 同前缀两条各计一条（静态表只有 1）"
    assert len(m["negative_controls"]) == 2 and len(m["payloads"]) == 3
    cov = m["coverage"]
    assert cov["covered"] == len(pd.ALL_ATTACK_TYPES) - len(cov["uncovered"])


def test_surface_map_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """写→读 往返一致；缺失/损坏 → None（fail-loud 的上游，不得静默放行）。"""
    target = tmp_path / "map.json"
    monkeypatch.setattr(pd, "SURFACE_MAP", target)
    m = pd.build_surface_map(1, 1, [("P1 x", True, "")], (0, 1, []))
    pd.write_surface_map(m)
    assert pd.load_surface_map() == m
    target.write_text("{ 坏 json", encoding="utf-8")
    assert pd.load_surface_map() is None, "损坏台账必须返回 None 而非空 dict"
    monkeypatch.setattr(pd, "SURFACE_MAP", tmp_path / "nope.json")
    assert pd.load_surface_map() is None


def test_unknown_attack_type_visible():
    """未登记前缀 → `A?` 可见（不静默丢弃），unknown_attack_types 能报出。"""
    stats = pd.attack_type_stats([("P999 新攻击面", True, "")])
    assert stats == {"A?": 1}
    assert pd.unknown_attack_types(stats) == ["A?"]


def test_surface_map_has_unregistered_visibility():
    """台账生成路径同样保留 `A?`（新增攻击面必须显形，不能算进已覆盖类）。"""
    m = pd.build_surface_map(1, 1, [("P999 新攻击面", True, "")], (0, 1, []))
    unknown = pd.unknown_attack_types(
        {p["type"]: 1 for p in m["payloads"]})
    assert unknown == ["A?"], "未登记载荷未在台账中显形"
