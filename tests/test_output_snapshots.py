"""554 T2：syrupy 快照锁「结构化输出」漂移（gate / poison / kg / mutation）。

历史病：规则数/warn 数/卡数多次"文档与磁盘失真"（warn 32→54→59→136 缺显形）。
本文件直接 import 各工具的 **report/run 库函数** 取结构化结果（dict/tuple），做
`assert data == snapshot` —— 不比对 stdout 字符串，避免措辞噪声。

动态字段纪律（否则快照必抖）：**在构造待快照 dict 时就排除** timestamp /
绝对路径 / 耗时秒数 / 平台分隔符 / git commit 等；不锁 findings 全文，只锁计数与结构。
（本文件用"手工挑键"达到与 syrupy matcher 等同的效果，且更直观可审。）

范围口径（诚实说明）：
- `poison_drill.drill()` 会真跑编译器 + 写 `build/_poison_*` 与 `_adv_v80/probes/p57.cpp`
  （重副作用 + 慢 + 污染仓库），其"通过数"由既有 slow 用例 `test_poison_attack_type.py` 覆盖。
  本文件只锁 poison 的**纯读**结构：live `rule_coverage()` + 已提交台账 `poison_surface_map.json`
  的结构（drill 通过数 / coverage / rule_coverage）。**本文件不触发编译、不写仓库。**
- mutation 选用 M4（门禁严格拦截 ⇒ 跳过 replay）+ M5（不适用）⇒ 不跑 replay、不编译。
- gate 用 `run(include_advice=True)` 取计数，配 `CPPBIBLE_OBS=0` 关闭观测日志写入。

标 fast：纯读 + 纯 Python（不调编译器、不跑 replay、不跑 poison）。
"""
from __future__ import annotations

from pathlib import Path

import gate_engine as ge
import knowledge_graph as kg
import mutation_fuzz as mf
import poison_drill as pd
import pytest

CARD = mf.ROOT / "evidence" / "conc" / "EV-CONC-001.md"


# ── gate：规则总数 + block/warn/advice 计数 ────────────────────────────────
def test_gate_summary_counts(snapshot, monkeypatch: pytest.MonkeyPatch):
    """gate 汇总：注册规则数 + block/warn/advice（不锁 Finding 文本全文）。"""
    monkeypatch.setenv("CPPBIBLE_OBS", "0")     # 关观测日志写盘（否则 data/logs 被写）
    findings = ge.run(include_advice=True)
    data = {
        "rules": len(ge.RULES),
        "block": sum(1 for f in findings if f.severity == "block"),
        "warn": sum(1 for f in findings if f.severity == "warn"),
        "advice": sum(1 for f in findings if f.severity == "advice"),
    }
    assert data == snapshot


# ── poison：RULE-COVERAGE 分子分母（live）+ 攻击面台账结构（已提交）──────────
def test_poison_rule_coverage_live(snapshot):
    """RULE-COVERAGE：已覆盖规则数 / 注册规则数 / 未覆盖清单 + 攻击面 taxonomy（live 纯读）。"""
    covered, total, uncovered = pd.rule_coverage()
    data = {
        "covered": covered,
        "total": total,
        "uncovered": uncovered,            # rule_coverage() 已 sorted ⇒ 稳定
        "attack_taxonomy": list(pd.ALL_ATTACK_TYPES),
    }
    assert data == snapshot


def test_poison_surface_map_committed(snapshot):
    """攻击面台账结构：drill 通过数、coverage、rule_coverage、各攻击类型计数（已提交基线）。"""
    surf = pd.load_surface_map()
    assert surf is not None, "tools/poison_surface_map.json 缺失（fail-loud）"
    data = {
        "drill": surf["drill"],                        # {passed, total} ← 通过数
        "coverage": surf["coverage"],                  # {covered, total, uncovered} ← 攻击面覆盖
        "rule_coverage": surf["rule_coverage"],        # {covered, total, exempt}
        "attack_type_counts": {a: surf["attack_types"][a]["count"]
                               for a in sorted(surf["attack_types"])},
    }
    assert data == snapshot


# ── kg：节点/边/概念/命题边/连通分量计数（tmp 库，绝不写真实 db）──────────
def test_kg_stats_counts(snapshot, tmp_path: Path):
    """kg stats：节点/边/概念/命题边/最大连通分量等计数（tmp db + 真实卡，只读仓）。"""
    conn = kg.connect(tmp_path / "kg.db")
    kg.build(conn, verbose=False)
    st = kg.stats(conn)
    data = {
        "nodes": st["nodes"],
        "edges": st["edges"],
        "card_nodes": st["card_nodes"],
        "concepts": st["concepts"],
        "concept_edges": st["concept_edges"],
        "concepts_multi_atom": st["concepts_multi_atom"],
        "max_component": st["max_component"],
        # 类型计数按 COUNT DESC 返回，并列时顺序可能不稳 ⇒ 排序后快照
        "nodes_by_type": dict(sorted(st["nodes_by_type"].items())),
        "edges_by_type": dict(sorted(st["edges_by_type"].items())),
        "dangling": len(st["dangling"]),
    }
    assert data == snapshot


# ── mutation：变体总数 + 严格拦截率/含 warn 处置率的计算结构 ─────────────────
def test_mutation_summary_structure(snapshot, monkeypatch: pytest.MonkeyPatch):
    """mutation 汇总结构：三分类（blocked/escaped/n_a）+ 两个率（分母口径 n_a 不入账）。

    选 M4（门禁严格拦截 ⇒ 跳过 replay）+ M5（不适用）⇒ 不编译、不跑 replay。
    排除动态：elapsed_s / ge_runs / replay_runs / replay_skipped / results[*].reproduce。
    """
    monkeypatch.setenv("CPPBIBLE_OBS", "0")
    rep = mf.run_fuzz([CARD], ["M4", "M5"], 1)
    data = {
        "variants": rep["variants"],
        "blocked": rep["blocked"],
        "escaped": rep["escaped"],
        "n_a": rep["n_a"],
        "strict_blocked": rep["strict_blocked"],
        "strict_rate": rep["strict_rate"],
        "treated_rate": rep["treated_rate"],
        "by_operator": {op: rep["by_operator"][op] for op in sorted(rep["by_operator"])},
    }
    assert data == snapshot
