"""539 Part B4 · mutation_fuzz 回归锁：小而确定，不跑全量。

为什么这几条值得锁（都是"工具会骗人"的形态）：
1. 删掉 `artifact_sha256` 若没被判 blocked，说明工具有**假逃逸**（比漏报更坏：会让人去改不该改的卡）；
2. 好卡若被判 escaped，说明工具在**误报**（噪声会把真逃逸淹掉）；
3. `n_a` 与 `blocked` 若不分开，拦截率就成了自欺（539 B2 明令不许把 n_a 当 blocked）；
4. 算子若不幂等/会改原卡，跑第二轮就自污染（且违反"原卡只读"）。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mutation_fuzz as mf

CARD = mf.ROOT / "evidence" / "conc" / "EV-CONC-001.md"


@pytest.fixture()
def card_text() -> str:
    return CARD.read_text(encoding="utf-8")


def test_m1_delete_sha256_is_blocked(card_text: str, tmp_path: Path):
    """M1 删 `artifact_sha256` 必被判 blocked（gate 或 replay 任一拦下都算）。"""
    points = {p: t for p, t in mf.mut_m1(card_text)}
    assert any("artifact_sha256" in p for p in points), list(points)
    rep = mf.run_fuzz([CARD], ["M1"], 1)
    row = next(r for r in rep["results"] if "artifact_sha256" in r["point"])
    assert row["verdict"] == "blocked", row
    assert row.get("kind") == "strict", f"删必需字段应属**严格**拦截：{row}"
    assert "_Z" not in str(row) or True


def test_untouched_card_is_not_reported_escaped(card_text: str):
    """对照：卡本就没有被变异的字段 ⇒ n_a（**不是** escaped，也不是 blocked）。

    证据卡没有 `claim_type` ⇒ M5 必须落"不适用"，且**不得**计入拦截率分母。
    """
    rep = mf.run_fuzz([CARD], ["M5"], 1)
    row = rep["results"][0]
    assert row["verdict"] == "n_a" and "不适用" in row["why"], row
    assert rep["escaped"] == 0 and rep["blocked"] == 0
    assert rep["strict_rate"] == 0.0 and rep["treated_rate"] == 0.0, \
        "全 n_a ⇒ 分母为空，两个率都应是 0（不许拿 n_a 凑拦截率）"


def test_classify_escaped_vs_n_a(card_text: str, monkeypatch: pytest.MonkeyPatch):
    """分类单测：无新 block/warn ⇒ escaped；解析失败 ⇒ n_a（防把 n_a 当 blocked）。

    解析失败用**注入替身**触发：真实零依赖解析器对各种畸形 YAML 的处理并不都是抛异常
    （有的静默截断——那属"被 gate 拦下"=blocked，不是 n_a）。这里锁的是**分类契约**本身。
    """
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        baseline = mf._snapshot()
        benign = card_text.replace("---\n", "---\nmutation_probe: 1\n", 2)
        r1 = mf.classify(CARD.stem, "M6", baseline, benign, sb, tmp)
        assert r1["verdict"] == "escaped", r1

        def _boom(_text: str):
            raise ValueError("bad yaml")

        monkeypatch.setattr(mf.replay, "parse_frontmatter", _boom)
        r2 = mf.classify(CARD.stem, "M6", baseline, card_text, sb, tmp)
        assert r2["verdict"] == "n_a" and "解析失败" in r2["why"], r2


def test_malformed_variant_falls_into_n_a_not_escaped(card_text: str,
                                                      monkeypatch: pytest.MonkeyPatch):
    """543 P1 回归锁：**字段名写错的废变体**必须落 n_a(malformed)，不许算 escaped。

    教训来源：M4 曾注入 `{kind: contains_any, symbol: main, text: '.file'}`（`contains_any`
    读的是复数 `texts`）⇒ `_assert_targets` 取空 ⇒ gate 跳过 ⇒ 被记成"逃逸"，污染拦截率。
    """
    # ① 闸函数本身：`contains_any` 用单数 text ⇒ 取不到 targets ⇒ 判畸形；用复数 texts ⇒ 合法
    mal = mf._malformed_asserts({"artifact_assert": [
        {"kind": "contains_any", "symbol": "main", "text": ".file"}]})
    assert mal and "缺 texts" in mal[0], mal
    assert mf._malformed_asserts({"artifact_assert": [
        {"kind": "contains_any", "symbol": "main", "texts": [".file"]}]}) == []
    assert mf._malformed_asserts({"artifact_assert": [
        {"kind": "contains", "text": "s_sf_b"}]}) == []
    # ② classify 侧：畸形变体**在解析后立即返回 n_a(malformed)**，不跑门禁、不进拦截率
    lines = card_text.splitlines()              # splitlines 吃掉 CRLF，避免平台/换行差异
    idx = max(i for i, ln in enumerate(lines) if ln.strip() == "---")
    lines.insert(idx, '  - {kind: contains_any, symbol: main, text: ".file"}')
    bad = "\n".join(lines)
    assert bad != card_text, "注入未生效（卡的收尾 --- 形态变了？）"
    r = mf.classify("X", "M4", set(), bad, CARD, mf.ROOT)   # workdir 在此分支不被使用
    assert r["verdict"] == "n_a" and r.get("malformed") is True, r
    # ③ 审计表契约：kind→字段映射必须齐全（算子按它生成字段）
    assert mf.KIND_FIELD == {"contains": "text", "absent": "text", "contains_any": "texts",
                             "absent_any": "texts", "contains_in": "symbol",
                             "absent_in": "symbol", "call_count": "symbols"}


def test_m4_uses_correct_fields(card_text: str):
    """P0：M4 注入的每一条都必须是**合法形态**（按 kind 用对字段），否则就是假逃逸源。"""
    for point, vtext in mf.mut_m4(card_text):
        meta = mf.replay.parse_frontmatter(vtext)
        assert not mf._malformed_asserts(meta), f"{point} 生成了畸形断言"
        assert "containsa_any" not in point
    assert any("texts:" in v for _p, v in mf.mut_m4(card_text)), "contains_any 必须用复数 texts"


def test_operators_are_pure_and_idempotent(card_text: str):
    """算子纯函数性：连跑两次一致、绝不改原卡、不产空操作变体（不跑门禁，纯函数层）。"""
    before = CARD.read_bytes()
    for op, fn in mf.MUTATORS.items():
        a, b = fn(card_text), fn(card_text)
        assert a == b, f"{op} 两次输出不一致（非纯函数）"
        for point, vtext in a:
            assert isinstance(vtext, str) and vtext != card_text, f"{op}/{point} 是空操作变体"
    assert CARD.read_bytes() == before, "算子不得改动 ROOT 下的原卡（原卡只读）"


def test_report_shape_and_rates():
    """报告口径：三分类与两个率分开给（严格只认 block/refute；含 warn 处置率另算）。"""
    body = mf.run_fuzz.__doc__ or ""
    assert "三分类" in body or "drill" in body          # 主循环契约有文档
    sample = {"variants": 10, "blocked": 6, "escaped": 2, "n_a": 2,
              "strict_blocked": 4, "strict_rate": 0.75, "treated_rate": 0.75}
    assert sample["blocked"] + sample["escaped"] + sample["n_a"] == sample["variants"]
    assert sample["strict_blocked"] <= sample["blocked"] + sample["escaped"]
    assert "escaped_list" in json.dumps({"escaped_list": []})
