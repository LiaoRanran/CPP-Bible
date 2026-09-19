"""589 任务 2 · M2 注释净化回归锁（_is_within_yaml_comment + 正反例）。

只测 `mut_m2` 的**纯函数**产出（不跑门禁）⇒ 快测。
"""
from __future__ import annotations

import json

import mutation_fuzz as mf

ROOT = mf.ROOT

# 588 实测的 9 张"注释伪变异"卡（field 块内注释行里有示意路径）
NINE = [
    "evidence/conc/EV-CONC-001.md", "evidence/conc/EV-CONC-002.md",
    "evidence/mem/EV-MEM-038.md", "evidence/mem/EV-MEM-040.md",
    "evidence/mem/EV-MEM-041.md", "evidence/mem/EV-MEM-042.md",
    "evidence/mem/EV-MEM-043.md", "evidence/mem/EV-MEM-044.md",
    "evidence/mem/EV-MEM-045.md",
]


def _changed_line(text: str, vtext: str):
    a = text.split("\n")
    b = vtext.split("\n")
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i + 1, y
    return -1, None


# ── _is_within_yaml_comment 单元测试 ──────────────────────────────────────────
def test_comment_whole_line():
    t = "a: 1\n# 见 Examples/atoms/x.cpp\nb: 2"
    i = t.index("Examples")
    assert mf._is_within_yaml_comment(t, i) is True


def test_comment_inline():
    t = "run_match_file: x.out   # 见 Examples/x.cpp\n"
    i = t.index("Examples/x.cpp")
    assert mf._is_within_yaml_comment(t, i) is True


def test_real_value_not_comment():
    t = "run_match_file: Examples/x.out\n"
    i = t.index("Examples")
    assert mf._is_within_yaml_comment(t, i) is False


def test_hash_glued_to_nonspace_is_not_comment():
    # `a#b`：`#` 前非空白 ⇒ YAML 不算注释起点（保守判非注释）
    t = "key: foo#bar/baz\n"
    i = t.index("bar/baz")
    assert mf._is_within_yaml_comment(t, i) is False


def test_before_any_hash_is_not_comment():
    t = "run_match_file: Examples/x.out   # 注\n"
    i = t.index("Examples")
    assert mf._is_within_yaml_comment(t, i) is False


# ── 反例：9 张卡的注释伪变异不再产生（改动行不再是注释行）──────────────────────
def test_m2_no_comment_mutation_on_the_nine():
    for rel in NINE:
        text = (ROOT / rel).read_text(encoding="utf-8")
        vs = mf.mut_m2(text)
        assert vs and vs[0][1] is not None, f"{rel} 变异器返回空/单例"
        for _p, vt in vs:
            ln, content = _changed_line(text, vt)
            assert content is not None, f"{rel} 未定位改动行"
            assert not content.strip().startswith("#"), f"{rel} L{ln} 仍在改注释行：{content!r}"


# ── 正例：v6 的 M2 blocked 变体一条不少（真实变异未被误伤）────────────────────
def test_m2_v6_blocked_points_preserved():
    v6 = json.loads((ROOT / "data/mutation/full_baseline_v6.json").read_text(encoding="utf-8"))
    by_card: dict[str, set[str]] = {}
    for r in v6["results"]:
        if r["op"] == "M2" and r["verdict"] == "blocked":
            by_card.setdefault(r["card"], set()).add(r["point"])
    assert sum(len(s) for s in by_card.values()) == 141, "v6 M2 blocked 基线应为 141"
    for rel, pts in by_card.items():
        got = {p for p, _ in mf.mut_m2((ROOT / rel).read_text(encoding="utf-8"))}
        assert pts <= got, f"{rel} 丢了 blocked 变体：{sorted(pts - got)}"


# ── 正例（合成卡）：只变真实路径，不碰注释路径 ────────────────────────────────
def test_m2_synthetic_only_real_path():
    card = ("---\nid: X\nmatrix:\n  compiler: [GCC 13.1.0]\n"
            "  # 示意命令：Examples/atoms/comment_only.cpp\n"
            "actual:\n  run_match_file: Examples/atoms/real_target.out\n---\nbody\n")
    vs = mf.mut_m2(card)
    assert vs and vs[0][1] is not None, "合成长卡未找到真实路径"
    assert len(vs) == 3, f"应产 3 条真实路径变形，实得 {len(vs)}"
    for _p, vt in vs:
        _ln, content = _changed_line(card, vt)
        assert content is not None
        assert "comment_only" not in content, f"变异落在注释路径：{content!r}"
        assert "real_target" in content or "REAL_TARGET" in content, f"未变异真实路径：{content!r}"
