"""424 攻击面分类回归锁：A1-A10 全映射、A4/A8/A10 盲区补齐、新毒样例直验。"""
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
