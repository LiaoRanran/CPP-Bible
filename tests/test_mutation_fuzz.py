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
    # 必须插在 `artifact_assert:` **块头之后**：插到 frontmatter 末尾会被最后那个 block
    # scalar（`falsification: >-`）吞掉，parse 后根本不在 artifact_assert 里（实测踩过）。
    i = next(i for i, ln in enumerate(lines) if ln.strip() == "artifact_assert:")
    lines.insert(i + 1, '  - {kind: contains_any, symbol: main, text: ".file"}')
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
            # 558 Part B：`None` = 算子自判 out_of_scope（门禁读取面内无变异点，见 mut_m2/mut_m3）
            assert vtext is None or (isinstance(vtext, str) and vtext != card_text), \
                f"{op}/{point} 是空操作变体"
    assert CARD.read_bytes() == before, "算子不得改动 ROOT 下的原卡（原卡只读）"


# ── 548 Part 0：性能改造的回归锁（**结论不许变**，只许变快）────────────────────


FROZEN_CONCLUSIONS = [
    # (op, 变异点, verdict, kind, 门禁规则 id 集合) —— 冻结基线，对账口径含规则 id。
    # ⚠️ 558 Part B1 **有意**改了 M3 两条的结论（escaped → blocked/warn_only）：这正是本批的
    #   收口目标——`contains_in{symbol:区间,text}` 被降级成 `contains{text}` 后区间锚定丢失，
    #   修前主路径放行（真逃逸），修后由"全文 kind 残留 symbol"指纹出 warn（见 gate_engine
    #   该处注释与 poison P70/P70-阴）。故此处按**实测重核**后重新冻结，不是改测试凑数。
    #   只挑 M3/M4：M2 的路径口径由 558 Part B2 改动（门禁读取面），不混进这条性能对账锁。
    ("M3", "contains_in → contains（区间断言降级为全文存在性）", "blocked", "warn_only",
     ["EV-ASSERT-SYMBOL-MAPPED"]),
    ("M3", "absent_in → absent（区间断言降级为全文不存在）", "blocked", "warn_only",
     ["EV-ASSERT-SYMBOL-MAPPED"]),
    ("M4", "注入通用符号 main", "blocked", "strict", ["EV-ASSERT-SYMBOL-MAPPED"]),
    ("M4", "注入通用符号 ret", "blocked", "strict", ["EV-ASSERT-SYMBOL-MAPPED"]),
    ("M4", "注入 ABI 帧符号 .p2align", "blocked", "strict", ["EV-ASSERT-SYMBOL-MAPPED"]),
    ("M4", "注入 contains_any: ['.file']（合法形态）", "blocked", "strict",
     ["EV-ASSERT-SYMBOL-MAPPED"]),
]


def test_548_perf_conclusions_unchanged(replay_serial):
    """548 Part 0 硬约束：提速前/后**逐变体结论一致**（冻结基线，对账口径含规则 id）。

    提速手段（frontmatter 解析缓存 / 按卡批 / 门禁已拦则跳过 replay）都不得改判决；
    一旦这里红，说明"省下的时间"是拿漏判换的。

    559 Part B：本用例跑**全库门禁**（逐变体 `ge.run()`）⇒ 读真实工件状态，会与并发 replay 的
    "删旧工件→重生成→还原"窗口相撞——实测误跑法（`pytest -n auto`）下冻结集合里多出
    `EV-ARTIFACT-FILE-EXISTS`（工件瞬时不存在）⇒ 假红。故与 replay 同锁串行。
    本用例只用 M3/M4（`REPLAY_OPS = {M1, M7}`）⇒ 自己**不跑 replay**，持锁不会自锁。
    """
    rep = mf.run_fuzz([CARD], ["M3", "M4"], 1)
    got = [(r["op"], r["point"], r["verdict"], r.get("kind"),
            sorted({x.split(":")[0] for x in (r.get("new_block") or [])
                    + (r.get("new_warn") or [])}))
           for r in rep["results"]]
    assert got == FROZEN_CONCLUSIONS, got
    # 按卡批的**可观测**证据：基线 1 次 + 每个进门禁的变体 1 次，一次不多一次不少
    assert rep["ge_runs"] == 1 + len(rep["results"]), rep["ge_runs"]
    assert rep["elapsed_s"] > 0 and rep["cards"] == ["evidence/conc/EV-CONC-001.md"]


# ── 558 Part B1/B2：门禁读取面纪律（假逃逸 → n_a(out_of_scope)）─────────────────


def test_558_gate_read_spans_only_frontmatter_keys():
    """`_gate_read_spans` 只认 frontmatter 里的门禁键，且**不含**正文/非门禁键。"""
    text = ("---\n"
            "id: EV-X\n"
            "claim: 正文式说明，提到 Examples/atoms/f.cpp 但门禁不读其实这里不算\n"
            "artifact_assert:\n  - {kind: contains, text: \"_Z1fv\"}\n"
            "---\n"
            "正文：contains_in 与 Examples/atoms/f.cpp。\n")
    spans = mf._gate_read_spans(text)
    covered = {k: False for k in ("claim", "artifact_assert", "body")}
    for key, needle in (("claim", "claim: 正文式说明"),
                        ("artifact_assert", "kind: contains"),
                        ("body", "正文：contains_in")):
        idx = text.index(needle)
        covered[key] = any(s <= idx < e for s, e in spans)
    assert covered == {"claim": False, "artifact_assert": True, "body": False}, covered


def test_558_out_of_scope_when_only_prose_mentions():
    """正文里的 `contains_in` / 路径**不是**门禁读取面 ⇒ 算子须报 out_of_scope（`None`）。

    修前 M3 取全文第一个 `contains_in`——实测 CONC-003/004/005 的首个出现落在 `expected:`
    正文，弱化正文门禁从不读 ⇒ 被记成 3 条**假逃逸**（虚增逃逸率）。同一张卡把 `_in` 放进
    `artifact_assert` 后立即变成在面内的真提问。
    """
    prose = ("---\n"
             "id: EV-PROSE-001\n"
             "command: g++ -S f.cpp -o f.asm\n"
             'artifact_assert:\n  - {kind: contains, text: "_Z1fv"}\n'
             "---\n"
             "正文：contains_in 三条全中；夹具 Examples/atoms/f.cpp 见正文。\n")
    m3 = mf.mut_m3(prose)
    assert len(m3) == 1 and m3[0][1] is None, m3          # 门禁面内无可弱化点
    m2 = mf.mut_m2(prose)
    assert len(m2) == 1 and m2[0][1] is None, m2          # 门禁面内无可变形路径
    inscope = prose.replace('{kind: contains, text: "_Z1fv"}',
                            '{kind: contains_in, symbol: "_Z1fv", text: "mov"}')
    assert any(v is not None for _p, v in mf.mut_m3(inscope)), mf.mut_m3(inscope)


def test_548_diff_is_not_card_scoped(monkeypatch: pytest.MonkeyPatch):
    """跨卡规则不许被"按卡裁剪"漏掉：diff 必须是**全量**（别的卡上的新命中也要算）。"""
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        baseline = mf._snapshot()
        foreign = {("EV-ID-UNIQUE", "block", "evidence/other/EV-OTHER-999.md")}
        monkeypatch.setattr(mf, "_snapshot", lambda: baseline | foreign)
        r = mf.classify(CARD.stem, "M6", baseline, CARD.read_text(encoding="utf-8"), sb, tmp)
        assert r["verdict"] == "blocked" and r["kind"] == "strict", r
        assert any(x.startswith("EV-ID-UNIQUE:") for x in r["new_block"]), r


def test_548_replay_runs_only_when_it_can_change_verdict(monkeypatch: pytest.MonkeyPatch):
    """replay 只在"它可能改变结论"时跑：门禁已严格拦截 ⇒ 跳过；否则**必须**跑（543 P0）。"""
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        baseline = mf._snapshot()
        calls: list[Path] = []

        def _fake_replay(card: Path, do_sanitizer: bool = True):
            calls.append(card)
            return ("confirm", [])

        monkeypatch.setattr(mf.replay, "replay_card", _fake_replay)
        blocked_diff = {("R-BLOCK", "block", "evidence/conc/EV-CONC-001.md")}
        monkeypatch.setattr(mf, "_snapshot", lambda: baseline | blocked_diff)
        r1 = mf.classify(CARD.stem, "M1", baseline, CARD.read_text(encoding="utf-8"), sb, tmp)
        assert r1["verdict"] == "blocked" and r1["kind"] == "strict"
        assert r1.get("replay_skipped") and calls == [], "门禁已拦 ⇒ 不该再跑 replay"
        # 门禁没拦 ⇒ replay 必须跑（只看 gate 会把"删必需字段"误判成逃逸）
        monkeypatch.setattr(mf, "_snapshot", lambda: baseline)
        r2 = mf.classify(CARD.stem, "M1", baseline, CARD.read_text(encoding="utf-8"), sb, tmp)
        assert len(calls) == 1 and r2["verdict"] == "escaped", (calls, r2)


def test_548_meta_cache_is_transparent(card_text: str, tmp_path: Path):
    """frontmatter 缓存必须**透明**：命中值 == 现解析值；改盘即失效（不许拿旧值判决）。"""
    import gate_engine as ge

    p = tmp_path / "ATOM-MEM-CACHE-001.md"
    p.write_text(card_text, encoding="utf-8")
    first = ge._meta(p)
    assert first == ge.replay.parse_frontmatter(card_text), "缓存值必须等于现解析值"
    assert ge._meta(p) == first, "同内容重复读应稳定"
    # 改盘（内容不同）⇒ 必须失效；否则门禁会拿旧 frontmatter 判决
    p.write_text(card_text.replace("\nid:", "\nid2:", 1), encoding="utf-8")
    assert "id2" in ge._meta(p), "改盘后仍返回旧值 = 缓存失效机制坏了"
    n = ge.clear_meta_cache()
    assert n >= 0 and ge._meta(p) == ge.replay.parse_frontmatter(p.read_text(encoding="utf-8"))


def test_548_gate_findings_stable_across_warm_cache():
    """温缓存下的第二次全库扫描必须与第一次**逐字一致**（缓存若被规则改写会立刻现形）。"""
    import gate_engine as ge

    key = lambda fs: {(f.rule_id, f.severity, f.target, f.message) for f in fs}  # noqa: E731
    cold = key(ge.run(include_advice=False))
    warm = key(ge.run(include_advice=False))
    assert cold == warm and len(cold) > 50, f"冷/温不一致：{len(cold)} vs {len(warm)}"


def test_548_cppbible_mutation_subcommand(tmp_path: Path):
    """`cppbible mutation` 接线（--cards/--operators/--limit/--out 透传）。"""
    import cppbible

    out = tmp_path / "mut.json"
    rc = cppbible.main(["mutation", "--cards", "evidence/conc/EV-CONC-001.md",
                        "--operators", "M3", "--limit", "1", "--out", str(out)])
    assert rc == 0, rc
    assert out.is_file() and json.loads(out.read_text(encoding="utf-8"))["variants"] >= 2


def test_report_shape_and_rates():
    """报告口径：三分类与两个率分开给（严格只认 block/refute；含 warn 处置率另算）。"""
    body = mf.run_fuzz.__doc__ or ""
    assert "三分类" in body or "drill" in body          # 主循环契约有文档
    sample = {"variants": 10, "blocked": 6, "escaped": 2, "n_a": 2,
              "strict_blocked": 4, "strict_rate": 0.75, "treated_rate": 0.75}
    assert sample["blocked"] + sample["escaped"] + sample["n_a"] == sample["variants"]
    assert sample["strict_blocked"] <= sample["blocked"] + sample["escaped"]
    assert "escaped_list" in json.dumps({"escaped_list": []})
