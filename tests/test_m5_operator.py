"""574 任务 E 回归锁：M5 算子（claim 自标）的尺子修复。

旧 bug：`re.search(r"^(\\s*)claim_type:...")` 只取**全文第一个** claim_type，而原子卡的命题写在
`claim_structured:` 列表里、prop-1 多为 observation ⇒ 永远返回空 ⇒ 29 条 inference 命题一条都改不到
（v2 实测 M5 = 0/0/83 全 n_a —— 把"没问到"记成了"不适用"）。
"""
from __future__ import annotations

import mutation_fuzz as mf

CARD = """---
id: ATOM-TEST-M5
domain: mem
title: t
type: atom
status: draft
claim: c
claim_boundary: b
claim_type: inference          # 卡面**顶层**的 claim_type（不该被 M5 动）
claim_structured:
  - prop-id: prop-1
    claim_type: observation
    statement: s1
  - prop-id: prop-2
    claim_type: inference
    statement: s2
  - prop-id: prop-3
    claim_type: inference
    statement: s3
---
正文
"""

PURE_OBS = CARD.replace("claim_type: inference", "claim_type: observation")


def test_574_m5_one_variant_per_inference_proposition():
    """每个 inference 命题各出一个**独立变体**，描述带命题 id。"""
    vs = mf.MUTATORS["M5"](CARD)
    real = [(p, v) for p, v in vs if v is not None]
    assert len(real) == 2, [(p, v is not None) for p, v in vs]
    assert "[命题 prop-2]" in real[0][0] and "[命题 prop-3]" in real[1][0]
    # 每个变体只把**自己那条** inference 改成 observation（别的 inference 命题原样保留）
    for p, v in real:
        assert v.count("claim_type: inference") == CARD.count("claim_type: inference") - 1
        assert v.count("claim_type: observation") == CARD.count("claim_type: observation") + 1


def test_574_m5_only_changes_the_one_line():
    """只改**目标那一行**：其余逐字不动（定点干预，不是重写卡）。"""
    base = CARD.split("\n")
    for _p, v in mf.MUTATORS["M5"](CARD):
        if _p is None or True:
            pass
    for point, vtext in mf.MUTATORS["M5"](CARD):
        if vtext is None:
            continue
        new = vtext.split("\n")
        assert len(new) == len(base), "行数不许变"
        diff = [i for i, (a, b) in enumerate(zip(base, new)) if a != b]
        assert len(diff) == 1, diff
        assert "claim_type" in base[diff[0]]


def test_574_m5_leaves_top_level_claim_type_alone():
    """卡面**顶层**的 claim_type 不动（只改 claim_structured 块内）。"""
    for _p, v in mf.MUTATORS["M5"](CARD):
        if v is None:
            continue
        head = v.split("claim_structured:")[0]
        assert "claim_type: inference" in head, "顶层 claim_type 必须原样保留"


def test_574_m5_pure_observation_card_is_out_of_scope():
    """块内没有 inference ⇒ 明确 out_of_scope（None），**不许假装成可判**。"""
    vs = mf.MUTATORS["M5"](PURE_OBS)
    assert len(vs) == 1 and vs[0][1] is None, vs


def test_574_m5_is_pure_and_no_claim_block_returns_empty():
    """纯函数（同输入 ⇒ 同输出、不改入参）；没有 claim_structured 块 ⇒ 空。"""
    a = mf.MUTATORS["M5"](CARD)
    b = mf.MUTATORS["M5"](CARD)
    assert [p for p, _ in a] == [p for p, _ in b]
    assert [v for _, v in a] == [v for _, v in b]
    assert mf.MUTATORS["M5"]("---\nid: X\n---\n") == []
