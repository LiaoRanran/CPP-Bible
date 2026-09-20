#!/usr/bin/env python3
"""612 线 B · B3：活性锚补全 what-if 分析（OBSERVATION-LIVENESS warn 消除）。

问题：607 审计出 50 条 observation 命题全缺**命题级**活性锚（`liveness`），每次 `gate_engine.py
--check` 都触发 `OBSERVATION-LIVENESS`（warn 观察期）共 **50** 条。本工具做**假设推演**：
若把 B1 候选 / B2 人审确认的活性锚补全上去，warn 能消到几条？

口径（**只读** gate，不修改任何东西）：
  * 完全复用 `gate_engine` 的 `OBSERVATION-LIVENESS` 两条 warn 分支与全部判定单点
    （`_prop_liveness_ok` / `_has_fixture_specific_assert_symbol` / `_falsification_quantified`
    / `_has_non_env_run_key` / `_has_artifact_assertion`）。本工具只"盖一层假设的 liveness"
    再跑同样的判定，不另写判据 —— 这样投影口径与门禁**逐字一致**。
  * 关键事实：一条**合法**的 `fixture_symbol` 锚（非通用符号 + 真实出现在引用卡的
    `artifact_assert` 目标里）同时也会让引用卡通过 `_has_fixture_specific_assert_symbol`
    ⇒ 分支①（命题级锚缺失）与分支②（卡级活性对照缺失）**同时**消除。故投影只取决于：
    "这条 observation 命题的引用卡里，是否存在一个可充当合法锚的非通用工件符号"。

三种情景：
  * `baseline`：当前真实门禁命中（调用 `gate_engine.check_observation_liveness()`）。
  * `full_anchor`：假设给**每条**可锚的 proposition 补上合法锚（取引用卡里第一个合法工件符号）；
    不可锚的（引用卡无合法非通用符号）保持原状 —— 它们只能靠"改标 inference / external_basis"
    解决（属人审决策，不在自动补全范围）。
  * `with_review`：叠加 B2 人审确认日志（`data/liveness_review_612.jsonl`）里已确认的锚；
    当前日志为空 ⇒ 与 baseline 一致，但工具支持随人审推进而更新投影。

用法：
  python tools/liveness_completion_whatif.py --write     # 写报告（data/liveness_completion_whatif_612.md）
  python tools/liveness_completion_whatif.py --check     # 自验证（exit 0=通过）
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW_LOG = ROOT / "data" / "liveness_review_612.jsonl"
REPORT_PATH = ROOT / "data" / "liveness_completion_whatif_612.md"

KNOWN_BASELINE_WARN = 50  # 607 审计 + 门禁实测：OBSERVATION-LIVENESS 当前 50 warn


def _gate():
    import gate_engine as g  # noqa: E402  （延迟导入，保持模块可被测试孤立 import）
    return g


# ── 数据装载（复用 gate 的 atom/evidence 解析）─────────────────────────────────
def load_observations() -> list[dict]:
    """→ [{card, prop_id, prop, cards(引用卡 meta 列表), refs}]，只含 observation 命题。"""
    g = _gate()
    idx = g._ev_index()
    out: list[dict] = []
    for p in g._cards(g.ATOMS, "ATOM-*.md"):
        meta = g._meta(p)
        for prop in g._claim_props(meta):
            if str(prop.get("claim_type") or "").strip() != "observation":
                continue
            refs = [str(r).strip() for r in (prop.get("evidence") or []) if str(r).strip()]
            cards = [idx[r] for r in refs if r in idx]
            out.append({"card": p.stem, "prop_id": str(prop.get("id") or "?"),
                        "prop": prop, "refs": refs, "cards": cards})
    return out


def valid_anchor_symbols(cards: list[dict]) -> list[str]:
    """引用卡里**所有**可作合法锚的符号（= 非通用 + 非纯散文 + 出现在某卡 artifact_assert 目标）。

    与 `_prop_liveness_ok` 的接受条件完全一致（非通用、非 CJK 散文、在 artifact_assert 目标里）。
    """
    g = _gate()
    syms: set[str] = set()
    for c in cards:
        for r in (c.get("artifact_assert") or []):
            if not isinstance(r, dict):
                continue
            for t in g._assert_targets(r)[1]:
                t = str(t).strip()
                if not t:
                    continue
                if g._is_universal_symbol(t):
                    continue
                if g._CJK_RE.search(t) and not g._IDENT_RE.search(t):
                    continue
                syms.add(t)
    return sorted(syms)


# ── 单条命题的两分支判定（与 gate 同构，支持盖一层假设的 liveness）─────────────
def simulate_one(prop: dict, cards: list[dict], anchor: str | None) -> str:
    """返回判定结果：`ok` / `branch1`(缺命题级锚) / `branch2`(卡级活性对照缺失) / `deferred`(交 NEEDS-ARTIFACT)。"""
    g = _gate()
    if cards and not any(g._has_artifact_assertion(c) for c in cards):
        return "deferred"                       # 交由 OBSERVATION-NEEDS-ARTIFACT（block）处置
    p = dict(prop)
    if anchor is not None:
        p["liveness"] = {"kind": "fixture_symbol", "symbol": anchor}
    ok, _why = g._prop_liveness_ok(p, cards)
    if not ok:
        return "branch1"
    if any(g._falsification_quantified(c.get("falsification"))
           or g._has_fixture_specific_assert_symbol(c)
           or g._has_non_env_run_key(c) for c in cards):
        return "ok"
    return "branch2"


def baseline_findings() -> list[dict]:
    g = _gate()
    fs = g.check_observation_liveness()
    return [{"card": f.target, "prop_id": _pid_from(f.message), "message": f.message}
            for f in fs if f.rule_id == "OBSERVATION-LIVENESS" and f.severity == "warn"]


def _pid_from(msg: str) -> str:
    # "命题 <id>（observation）…"
    import re  # noqa: E402
    m = re.search(r"命题\s+([^\s（(]+)", msg)
    return m.group(1) if m else "?"


def load_review_anchors() -> dict[str, str]:
    """B2 日志 → {proposition_id(卡::prop-N): confirmed_symbol}。"""
    out: dict[str, str] = {}
    if not REVIEW_LOG.is_file():
        return out
    for line in REVIEW_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        # 仅采纳「确认锚」类决策（confirm + 带了 symbol）；其余忽略
        if r.get("decision") == "confirm" and r.get("symbol"):
            out[r["proposition_id"]] = r["symbol"]
    return out


# ── 三情景投影 ──────────────────────────────────────────────────────────────
def project() -> dict:
    obs = load_observations()
    baseline = baseline_findings()
    baseline_pids = {b["prop_id"] for b in baseline}
    review = load_review_anchors()

    full_rows: list[dict] = []
    anchorable = must_reclassify = deferred = 0
    for o in obs:
        pid = f"{o['card']}::{o['prop_id']}"
        # baseline 分支（无假设锚）
        base = simulate_one(o["prop"], o["cards"], None)
        # full_anchor：给可锚的命题补合法锚
        anchors = valid_anchor_symbols(o["cards"])
        chosen = anchors[0] if anchors else None
        full = simulate_one(o["prop"], o["cards"], chosen)
        # with_review：叠加人审确认的锚
        rev_sym = review.get(pid)
        rev = simulate_one(o["prop"], o["cards"], rev_sym) if rev_sym else base

        if base == "deferred":
            deferred += 1
        cls = "可锚(补 fixture_symbol)" if anchors else "须改标(inference/external_basis)"
        if anchors:
            anchorable += 1
        else:
            must_reclassify += 1
        full_rows.append({"card": o["card"], "prop_id": o["prop_id"], "refs": o["refs"],
                          "base": base, "full": full, "review": rev,
                          "anchors": anchors, "chosen": chosen, "class": cls,
                          "in_baseline": o["prop_id"] in baseline_pids})

    n = len(obs)
    full_warn = sum(1 for r in full_rows if r["full"] != "ok")
    review_warn = sum(1 for r in full_rows if r["review"] != "ok")
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_obs": n,
        "baseline_warn": len(baseline),
        "baseline_pids": sorted(baseline_pids),
        "anchorable": anchorable,
        "must_reclassify": must_reclassify,
        "deferred": deferred,
        "full_anchor_warn_after": full_warn,
        "full_anchor_warn_eliminated": n - full_warn,
        "review_warn_after": review_warn,
        "review_anchors_applied": len(review),
        "rows": full_rows,
        "note": ("只读推演：复用 gate_engine 的 OBSERVATION-LIVENESS 两分支与全部判定单点，"
                 "仅叠加假设的 liveness 再跑同一判定；不修改 gate / 不写命题卡。"
                 "full_anchor 投影 = 假设给每条『可锚』命题补合法 fixture_symbol 锚；"
                 "『须改标』命题引用卡无合法非通用工件符号，只能靠人审改标 inference/external_basis 消除 warn。"),
    }


# ── 报告 ──────────────────────────────────────────────────────────────────
def _short(s: str, n: int = 50) -> str:
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[:n] + "…"


def render(d: dict) -> str:
    out: list[str] = []
    out.append("# 活性锚补全 what-if 分析（612 线 B · B3 · 只读）")
    out.append("")
    out.append(f"> 生成时间：{d['generated_at']} ｜ 命令：`python tools/liveness_completion_whatif.py --write`")
    out.append(">")
    out.append("> **只读推演**：完全复用 `gate_engine` 的 `OBSERVATION-LIVENESS` 两分支与判定单点，"
               "仅叠加假设的 `liveness` 再跑同一判定；不修改 gate / 不写命题卡。")
    out.append("")
    out.append("## 1 · 三情景投影")
    out.append("")
    out.append("| 情景 | OBSERVATION-LIVENESS warn | 说明 |")
    out.append("|---|---|---|")
    out.append(f"| `baseline`（当前真实门禁） | **{d['baseline_warn']}** | 50 条 observation 全缺命题级锚 |")
    out.append(f"| `full_anchor`（假设补全合法锚） | **{d['full_anchor_warn_after']}** "
               f"（消 {d['full_anchor_warn_eliminated']}） | 可锚的全补；不可锚的保持原状 |")
    out.append(f"| `with_review`（叠加 B2 人审锚） | **{d['review_warn_after']}** "
               f"（已应用 {d['review_anchors_applied']} 条） | 随人审推进而更新 |")
    out.append("")
    out.append("## 2 · 可达成的 warn 消除上限")
    out.append("")
    out.append(f"- observation 命题总数：**{d['total_obs']}**")
    out.append(f"- **可锚**（引用卡有合法非通用工件符号，自动补 `fixture_symbol` 即可消除 warn）："
               f"**{d['anchorable']}**")
    out.append(f"- **须改标**（引用卡无合法非通用符号，只能靠人审改标 `inference` / `external_basis`）："
               f"**{d['must_reclassify']}**")
    out.append(f"- 交由 `OBSERVATION-NEEDS-ARTIFACT`（block）处置、不在本 warn 口径内：**{d['deferred']}**")
    out.append("")
    out.append("> 结论：自动补全**最多**能消除 "
               f"**{d['anchorable']} / {d['total_obs']}** 条 warn；剩余 "
               f"**{d['must_reclassify']}** 条必须靠人审改标（非自动工具可解）。"
               "合法的 fixture_symbol 锚会**同时**满足命题级锚（分支①）与卡级活性对照"
               "（`_has_fixture_specific_assert_symbol`，分支②），故补锚即两分支同消。")
    out.append("")
    out.append(f"## 3 · 逐命题明细（{d['total_obs']} 条）")
    out.append("")
    out.append("| 卡 | 命题 | 引用卡 | baseline | full_anchor | 可锚符号(首) | 分类 |")
    out.append("|---|---|---|---|---|---|---|")
    for r in d["rows"]:
        refs = ", ".join(r["refs"]) or "—"
        chosen = r["chosen"] or "—"
        out.append(f"| `{r['card']}` | `{r['prop_id']}` | {refs} | {r['base']} | {r['full']} "
                   f"| `{chosen}` | {r['class']} |")
    out.append("")
    out.append("## 4 · 口径与边界（诚实）")
    out.append("")
    out.append("- **不重复实现判据**：`_prop_liveness_ok` / `_has_fixture_specific_assert_symbol` / "
               "`_falsification_quantified` / `_has_non_env_run_key` / `_has_artifact_assertion` 全部直接 import "
               "自 `gate_engine`，投影口径与门禁逐字一致。")
    out.append("- **假设 ≠ 提交**：本工具只做推演，不写命题卡、不改 gate；真正补全活性锚是 B2 人审的权力。")
    out.append("- **改标属人审**：`须改标` 类命题的引用卡里没有可由单一工件读数证伪的非通用符号，"
               "自动工具无法凭空造锚 —— 必须由人决定改标 `inference`（补 external_basis）或 `external_basis`。")
    out.append("- **`deferred`**：该命题引用卡均无工件断言，归 `OBSERVATION-NEEDS-ARTIFACT`（block）辖，"
               "不计入本 warn 口径。")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 线 B · B3 活性锚补全 what-if（只读）")
    ap.add_argument("--write", action="store_true", help="写 data/liveness_completion_whatif_612.md")
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    d = project()

    problems: list[str] = []
    if d["baseline_warn"] != KNOWN_BASELINE_WARN:
        problems.append(f"baseline warn 应为 {KNOWN_BASELINE_WARN}（实测 {d['baseline_warn']}）")
    if d["anchorable"] + d["must_reclassify"] + d["deferred"] != d["total_obs"]:
        problems.append("可锚+须改标+deferred 之和应等于 observation 总数")
    # 模型自洽：full_anchor 投影后，残留 warn 应恰为『须改标』（可锚的全消、deferred 不计 warn）
    if d["full_anchor_warn_after"] != d["must_reclassify"]:
        problems.append(f"full_anchor 残留 warn 应={d['must_reclassify']}（实测 {d['full_anchor_warn_after']}）")
    # 模型自洽：baseline 全为 branch1（无 liveness）⇒ baseline warn == total_obs - deferred
    expect_base = d["total_obs"] - d["deferred"]
    if d["baseline_warn"] != expect_base:
        problems.append(f"baseline warn 应={expect_base}（实测 {d['baseline_warn']}）")
    if problems:
        print("[B3] ❌ 自检失败：", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1

    if a.check:
        print(f"[B3] ✅ 自验证通过：baseline warn={d['baseline_warn']} / "
              f"可锚={d['anchorable']} / 须改标={d['must_reclassify']} / deferred={d['deferred']}；"
              f"full_anchor 后 warn={d['full_anchor_warn_after']}（消 {d['full_anchor_warn_eliminated']}）")
        return 0

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render(d), encoding="utf-8")
    print(f"[B3] 已写 {REPORT_PATH.relative_to(ROOT).as_posix()}："
          f"baseline warn={d['baseline_warn']} / 可锚={d['anchorable']} / 须改标={d['must_reclassify']}；"
          f"full_anchor 后 warn={d['full_anchor_warn_after']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
