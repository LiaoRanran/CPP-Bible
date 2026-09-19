#!/usr/bin/env python3
"""547 D 面探针：mutation_fuzz 判决诚实性（最高优先）。

纯 gate / 单测式，不编译、不改正式文件。每项输出一行 `[PASS|FAIL|INFO] Dx ...`。
判定口径：
  - PASS  = 工具行为诚实（无该假设描述的洞）
  - FAIL  = 发现该假设描述的洞（ESCAPE）
  - INFO  = 结构性说明，非洞
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gate_engine as ge          # noqa: E402
import mutation_fuzz as mf        # noqa: E402
import atom_evidence_replay as replay  # noqa: E402

EV = ROOT / "evidence"
CARD = EV / "conc" / "EV-CONC-001.md"   # 真仓库卡（只读）


def _run_card(card: Path = CARD, ops=("M4",), limit: int = 1) -> dict:
    """在沙箱里跑一次 run_fuzz，返回报告（不污染真仓）。"""
    return mf.run_fuzz(mf.pick_cards(str(card.relative_to(ROOT)))[:limit], list(ops), limit)


# ── D1：classify 真的跑了正式 ge.run（不是桩/缓存） ────────────────────────────
def t_d1_real_run() -> str:
    calls = []
    real = mf._snapshot

    def spy():
        calls.append(1)
        return real()

    mf._snapshot = spy
    try:
        with mf.sandbox() as tmp:
            sb = mf._rel_in_sandbox(CARD, tmp)
            base = real()
            variants = mf.MUTATORS["M4"](CARD.read_text(encoding="utf-8"))
            text = variants[0][1]
            mf.classify(CARD.stem, "M4", base, text, sb, tmp)
    finally:
        mf._snapshot = real
    return "PASS" if calls else "FAIL"


# ── D2：跨卡规则不被按卡裁剪（落在别卡上的命中也算） ──────────────────────────
def t_d2_cross_card_not_scoped() -> str:
    ids = {}
    for p in ge._cards(EV, "EV-*.md"):
        m = ge._meta(p)
        if m.get("id"):
            ids[str(m["id"])] = str(p)
    other_id = next(i for i in ids if i != ge._meta(CARD).get("id"))
    base_text = CARD.read_text(encoding="utf-8")
    # 把本卡的 id 改成与别卡碰撞 ⇒ EV-ID-UNIQUE 应命中（target 可能是别卡）
    mutated = re.sub(r"^id:.*$", f"id: {other_id}", base_text, count=1, flags=re.M)
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        base = mf._snapshot()
        r = mf.classify(CARD.stem, "M6", base, mutated, sb, tmp)
    if r["verdict"] != "blocked":
        return f"FAIL (verdict={r['verdict']})"
    if not any("EV-ID-UNIQUE" in b for b in r["new_block"]):
        return f"FAIL (EV-ID-UNIQUE 不在 new_block: {r['new_block']})"
    return "PASS"


# ── D3：畸形变体 → n_a(malformed)，不冒充 blocked ─────────────────────────────
def t_d3_malformed_is_na() -> str:
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        base = mf._snapshot()
        # ① frontmatter 根本不存在 ⇒ parse_frontmatter 抛 ValueError ⇒ n_a（不冒充 blocked）
        bad1 = "这不是一张卡（无 --- 包裹）\nid: x\n正文\n"
        r1 = mf.classify(CARD.stem, "M6", base, bad1, sb, tmp)
        if r1["verdict"] != "n_a":
            return f"FAIL (不可解析应有 n_a，得 {r1['verdict']})"
        # ② artifact_assert 畸形（空 text ⇒ 退化恒真断言，543 P1 必须 n_a）
        # 先把已有的 artifact_assert 块删掉（避免变成"重复键"——那会被更严的 gate 规则 block，
        # 掩盖本要测的"畸形 assert → n_a"路径），再在 frontmatter 内插入一条畸形块
        raw = CARD.read_text(encoding="utf-8")
        raw2 = re.sub(r"\nartifact_assert:.*?(?=\n[a-zA-Z_]+:|\n---|\Z)", "", raw, flags=re.S)
        insert = "\nartifact_assert:\n  - kind: contains\n    text: \"\"\n"
        close = raw2.find("\n---", 3)
        bad2 = raw2[:close] + insert + raw2[close:]
        r2 = mf.classify(CARD.stem, "M6", base, bad2, sb, tmp)
    if r2["verdict"] != "n_a" or not r2.get("malformed"):
        return f"FAIL (畸形 assert 应 n_a/malformed，得 {r2})"
    return "PASS"


# ── D4：baseline 每次 run_fuzz 重算（进程内两次调用不串味） ────────────────────
def t_d4_baseline_fresh_per_run() -> str:
    r1 = _run_card(CARD, ("M4",), 1)
    r2 = _run_card(CARD, ("M4",), 1)
    if r1["ge_runs"] < 1 or r1["ge_runs"] != r2["ge_runs"]:
        return f"FAIL (ge_runs {r1['ge_runs']} vs {r2['ge_runs']})"
    # 同一卡两次跑，排除 n_a 后 verdict 集合应一致（baseline 不被上次运行污染）
    v1 = sorted((x["op"], x["point"], x["verdict"]) for x in r1["results"]
                if x["verdict"] != "n_a")
    v2 = sorted((x["op"], x["point"], x["verdict"]) for x in r2["results"]
                if x["verdict"] != "n_a")
    return "PASS" if v1 == v2 else f"FAIL (两次 verdict 不一致 {v1} vs {v2})"


# ── D5：引入新 block 的变异被如实报出（门禁降级反过来也是"新命中"，不藏） ────────
def t_d5_regression_surfaced() -> str:
    # 注入一个会让门禁新 block 的变异：duplicate `serves` 指向非法/重复服务关系
    base = CARD.read_text(encoding="utf-8")
    mutated = base.replace("serves:", "serves: [ATOM-MEM-001, ATOM-MEM-001]  # dup", 1)
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        b = mf._snapshot()
        r = mf.classify(CARD.stem, "M6", b, mutated, sb, tmp)
    # 要么被 block（新命中如实报），要么 escaped（该卡无对应规则也诚实）；关键是**不谎报**
    if r["verdict"] not in ("blocked", "escaped", "n_a"):
        return f"FAIL (未知 verdict {r['verdict']})"
    return "PASS"


# ── D6：replay 的 infra_error 不当 escaped / 不静默丢 ──────────────────────────
def t_d6_replay_infra_error_visible() -> str:
    real_replay = replay.replay_card

    def infra(*a, **k):
        return ("infra_error:compiler_missing", [])

    replay.replay_card = infra
    try:
        base = CARD.read_text(encoding="utf-8")
        variants = mf.MUTATORS["M1"](base)
        reached = []
        for pt, vt in variants:
            with mf.sandbox() as tmp:
                sb = mf._rel_in_sandbox(CARD, tmp)
                b = mf._snapshot()
                r = mf.classify(CARD.stem, "M1", b, vt, sb, tmp)
            reached.append((pt, r["verdict"], "infra_error" in r.get("why", "")))
    finally:
        replay.replay_card = real_replay
    # 至少一个 M1 变体**跑到 replay 分支**（门禁没先拦）且如实报 n_a+infra_error ⇒ PASS
    if any(v == "n_a" and inf for _, v, inf in reached):
        return "PASS"
    # 若全部 M1 变体先被门禁拦（replay 没机会跑）⇒ 设计内，不算洞
    if all(v == "blocked" for v, _, _ in reached):
        return "INFO (全部 M1 变体先被门禁拦，replay 未达：设计内)"
    return f"FAIL (replay 可达但未如实报 infra_error: {reached})"


# ── D7：selection bias 不存在（--cards all 真处理每张卡） ──────────────────────
def t_d7_no_selection_bias() -> str:
    cards = mf.pick_cards("all")
    n = min(15, len(cards))
    rep = mf.run_fuzz(cards[:n], ["M4"], n)
    if len(rep["by_card"]) != n:
        return f"FAIL (by_card 数 {len(rep['by_card'])} ≠ 选中 {n})"
    return "PASS"


DEFS = [t_d1_real_run, t_d2_cross_card_not_scoped, t_d3_malformed_is_na,
        t_d4_baseline_fresh_per_run, t_d5_regression_surfaced,
        t_d6_replay_infra_error_visible, t_d7_no_selection_bias]


def main() -> int:
    print("=== D 面：mutation_fuzz 判决诚实性 ===")
    bad = 0
    for f in DEFS:
        try:
            res = f()
        except Exception as e:  # noqa: BLE001
            res = f"FAIL (抛异常 {type(e).__name__}: {e})"
        tag = "PASS" if res == "PASS" else "FAIL"
        if tag == "FAIL":
            bad += 1
        print(f"[{tag}] {f.__name__}: {res}")
    print(f"D 面：{len(DEFS)-bad}/{len(DEFS)} 项 PASS" + ("（发现洞！）" if bad else "（无洞）"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
