#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prop_network_inventory.py — 命题网络台账（592 任务4；**只读生成器**）。

为什么：R4 grounded 论证层要在"命题 + 卡 + 证据"的网络上算可接受集，动手前先把**事实基线**
落成一份人审台账：79 条命题各自引用了哪些卡、闭包多大、有没有签名/活性锚；27 张卡各有几条命题、
谁签的、oracle 字段填了没；边到底有多少条；以及三条完整性校验是否干净。

只读纪律：本工具**不写卡、不写库**（只读 `data/propositions.db` + 卡面 frontmatter），
唯一写动作是 `--out` 指定的**台账文件**；`--check` 模式一个字节都不写。

用法：
    python tools/prop_network_inventory.py                 # 重新生成 data/prop_network_inventory.md
    python tools/prop_network_inventory.py --stdout        # 只打印，不落盘
    python tools/prop_network_inventory.py --check         # 校验已提交台账与事实源一致（漂移 ⇒ exit 2）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_engine as ge  # noqa: E402
import metrics_collector as mc  # noqa: E402
import prop_closure as pc  # noqa: E402
import prop_graph as pg  # noqa: E402

OUT_DEFAULT = ROOT / "data" / "prop_network_inventory.md"
#: 闭包大小异常阈值（任务书 592 任务4）：>50 或 =1 的命题要在台账里单列。
CLOSURE_MAX_OK = 50
CLOSURE_MIN_OK = 1


def _evidence_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for p in sorted(ge.EVIDENCE.rglob("EV-*.md")):
        if "README" in p.name:
            continue
        m = ge._meta(p)
        idx[str(m.get("id") or p.stem)] = m
    return idx


def _liveness_map(ev_idx: dict[str, dict]) -> dict[str, dict]:
    """命题级活性锚状态：直接调 gate 的判定单点 `_prop_liveness_ok`（不另写一套口径）。"""
    out: dict[str, dict] = {}
    for p in sorted(ge.ATOMS.rglob("ATOM-*.md")):
        if "README" in p.name:
            continue
        m = ge._meta(p)
        cid = str(m.get("id") or p.stem)
        for prop in (m.get("claim_structured") or []):
            if not isinstance(prop, dict):
                continue
            refs = [str(x).strip() for x in ge._as_list(prop.get("evidence")) if str(x).strip()]
            cards = [ev_idx[r] for r in refs if r in ev_idx]
            ok, why = ge._prop_liveness_ok(prop, cards)
            out[f"{cid}/{prop.get('id') or '?'}"] = {
                "claim_type": str(prop.get("claim_type") or ""),
                "has_field": bool(prop.get("liveness")), "ok": bool(ok), "why": str(why)}
    return out


def _card_meta() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for pat, root in (("ATOM-*.md", ge.ATOMS), ("EV-*.md", ge.EVIDENCE)):
        for p in sorted(root.rglob(pat)):
            if "README" in p.name:
                continue
            m = ge._meta(p)
            out[str(m.get("id") or p.stem)] = {
                "meta": m, "path": p.relative_to(ROOT).as_posix()}
    return out


def _liveness_cell(claim_type: str, live: dict | None) -> str:
    if claim_type != "observation":
        return "n/a（inference）"
    if live is None:
        return "未评（不在卡面 claim_structured 里）"
    if live["ok"]:
        return "有锚"
    return "缺锚（无 liveness 字段）" if not live["has_field"] else "缺锚（字段不合判据）"


def collect() -> dict:
    """汇总一次性读盘结果（纯读）。"""
    rows = pg.extract()                       # 命题行（排序确定，便于逐字节复现）
    ev_idx = _evidence_index()
    live = _liveness_map(ev_idx)
    cards_meta = _card_meta()
    sizes = pc.stats()["closure_sizes"]
    edges = pc.load_edges()
    conn_edges = {"prop_to_card": 0, "prop_to_evidence": 0, "card_to_prop": 0}
    props_set = {r["prop_key"] for r in rows}
    for prop in rows:
        conn_edges["prop_to_card"] += 1                      # 命题 → 本卡（每命题恰 1 条）
        conn_edges["card_to_prop"] += 1                      # 卡 → 命题（每命题恰 1 条）
        for e in [x for x in str(prop["evidence"]).split(",") if x.strip()]:
            conn_edges["prop_to_evidence"] += 1
    # 完整性校验
    bad_refs, bad_closure = [], []
    for r in rows:
        refs = [x.strip() for x in str(r["evidence"]).split(",") if x.strip()]
        missing = [x for x in refs if x not in cards_meta]
        if missing:
            bad_refs.append({"prop_key": r["prop_key"], "missing": missing})
        sz = sizes.get(r["prop_key"])
        if sz is None or sz > CLOSURE_MAX_OK or sz == CLOSURE_MIN_OK:
            bad_closure.append({"prop_key": r["prop_key"], "size": sz})
    no_prop_cards = [cid for cid, v in cards_meta.items()
                     if v["path"].startswith("atoms/") and not v["meta"].get("claim_structured")]
    oracle = mc.oracle_report([{"id": cid, "verified_by_oracle": v["meta"].get("verified_by_oracle")}
                               for cid, v in sorted(cards_meta.items())])
    oracle_by_card = {e["card"]: e for e in oracle["entries"]}
    return {"rows": rows, "live": live, "cards": cards_meta, "sizes": sizes, "edges": edges,
            "edge_kinds": conn_edges, "bad_refs": bad_refs, "bad_closure": bad_closure,
            "no_prop_cards": no_prop_cards, "oracle": oracle, "oracle_by_card": oracle_by_card,
            "stats": pc.stats(), "props_set": props_set}


def render(data: dict) -> str:
    rows, live = data["rows"], data["live"]
    st = data["stats"]
    L: list[str] = []
    add = L.append
    add("# 命题网络台账（592 任务4 · R4 grounded 层输入基线）")
    add("")
    add("> **只读生成**：`.venv\\Scripts\\python.exe tools/prop_network_inventory.py`"
        "（`--check` 校验本文件与事实源一致）。")
    add("> 数据源：`data/propositions.db`（`prop_graph.py build` 的派生视图）+ 卡面 `claim_structured`"
        " + `tools/prop_closure.py` 的闭包。")
    add("> 本文件是**人审清单**，不参与任何判决；数字与事实源不一致即视为台账过期。")
    add("")
    add("## 0. 汇总与完整性校验")
    add("")
    add(f"- 命题 **{st['propositions']}** · 命题所属卡 **{st['cards']}** · 卡节点 {st['card_nodes']}"
        f"（含证据卡 {st['evidence_cards']}）· 边 **{st['edges']}** · 连通分量 {st['components']}")
    add(f"- 闭包大小（全体节点口径，含命题+卡两类 id）：avg {st['avg_closure_size']}"
        f" / max {st['max_closure_size']} / min {st['min_closure_size']} · 分布 {st['size_histogram']}")
    add(f"- 可达命题数：avg {st['avg_closure_props']} / max {st['max_closure_props']}")
    add(f"- 活性锚：observation 命题 {sum(1 for r in rows if r['claim_type'] == 'observation')} 条，"
        f"其中有锚 {sum(1 for r in rows if live.get(r['prop_key'], {}).get('ok'))} 条")
    add("")
    add("| 完整性校验 | 期望 | 实测 | 结论 |")
    add("|---|---|---|---|")
    add(f"| 引用卡不存在的命题 | 0 | {len(data['bad_refs'])} | "
        f"{'✓' if not data['bad_refs'] else '✗ 需人审'} |")
    add(f"| 无命题的原子卡 | 0 | {len(data['no_prop_cards'])} | "
        f"{'✓' if not data['no_prop_cards'] else '✗ 需人审'} |")
    add(f"| 闭包大小异常（>{CLOSURE_MAX_OK} 或 ={CLOSURE_MIN_OK}） | 0 | {len(data['bad_closure'])} | "
        f"{'✓' if not data['bad_closure'] else '✗ 需人审'} |")
    add("")
    if data["bad_refs"]:
        add("**引用卡不存在的命题（需人审）**：")
        for b in data["bad_refs"]:
            add(f"- `{b['prop_key']}` → 缺 {b['missing']}")
        add("")
    if data["no_prop_cards"]:
        add("**无命题的原子卡（需人审）**：" + "、".join(f"`{c}`" for c in data["no_prop_cards"]))
        add("")
    if data["bad_closure"]:
        add("**闭包大小异常（需人审）**：")
        for b in data["bad_closure"]:
            add(f"- `{b['prop_key']}` → {b['size']}")
        add("")
    add("## 1. 命题列表（逐条）")
    add("")
    add("| # | 命题 | 类型 | 引用卡 | 闭包大小 | 签署 | 活性锚 |")
    add("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        sign = r["signed_by"] or f"（{r['signoff_state']}）"
        add(f"| {i} | `{r['prop_key']}` | {r['claim_type']} | {r['evidence'] or '—'} | "
            f"{data['sizes'].get(r['prop_key'])} | {sign} | "
            f"{_liveness_cell(r['claim_type'], live.get(r['prop_key']))} |")
    add("")
    add("## 2. 卡列表（27 张原子卡）")
    add("")
    add("| 卡 | 命题数 | verified_by（卡级人签） | oracle 状态 | 本卡命题闭包大小 |")
    add("|---|---|---|---|---|")
    by_card: dict[str, list[str]] = {}
    for r in rows:
        by_card.setdefault(r["card"], []).append(r["prop_key"])
    for cid in sorted(by_card):
        meta = data["cards"][cid]["meta"]
        vo = data["oracle_by_card"].get(cid) or {}
        if meta.get("verified_by_oracle"):
            ocell = f"已填（{'stale' if vo.get('stale') else 'fresh'}）"
        else:
            ocell = "未填（正常状态）"
        sizes = [data["sizes"][k] for k in by_card[cid]]
        add(f"| `{cid}` | {len(by_card[cid])} | {meta.get('verified_by') or '—'} | {ocell} | "
            f"{min(sizes)}–{max(sizes)} |")
    add("")
    add("## 3. 边统计")
    add("")
    add("| 边类型 | 条数 | 说明 |")
    add("|---|---|---|")
    ek = data["edge_kinds"]
    add(f"| 命题 → 本卡 | {ek['prop_to_card']} | 每条命题引用自己所属的原子卡 |")
    add(f"| 命题 → 证据卡 | {ek['prop_to_evidence']} | `claim_structured[*].evidence` 逐条 |")
    add(f"| 卡 → 命题 | {ek['card_to_prop']} | 卡声明自己的命题（反向边） |")
    add(f"| **合计（去重后）** | **{len(set(data['edges']))}** | "
        f"三类合计 {ek['prop_to_card'] + ek['prop_to_evidence'] + ek['card_to_prop']}（含重复对） |")
    add(f"| 卡节点 | {st['card_nodes']} | 命题所属卡 {st['cards']} + 证据卡 {st['evidence_cards']} |")
    add("")
    add("## 4. 闭包口径与对账")
    add("")
    add("- 闭包定义：从命题出发，沿 `card→prop` / `prop→card` / `prop→evidence` 有向边可达的**全部节点**"
        "（含命题与卡两类 id）。")
    add("- 双实现对账：`tools/prop_closure.py cross-check`（Python BFS vs SQL `WITH RECURSIVE`）"
        "必须逐集合相等；不一致时该命令 **exit 2**。")
    add("- oracle 统计（报告层只读，不改判决）："
        f"未填字段 {data['oracle']['missing_field']} 张 · stale {len(data['oracle']['stale'])} 张 · "
        f"放权开关 {json.dumps(data['oracle']['delegation_switches'], ensure_ascii=False)}")
    add("")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="命题网络台账（只读生成；R4 grounded 层输入基线）")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--stdout", action="store_true", help="只打印，不落盘")
    ap.add_argument("--check", action="store_true",
                    help="校验已提交台账与事实源一致（漂移 ⇒ exit 2，不写任何文件）")
    a = ap.parse_args(argv)
    text = render(collect())
    out = Path(a.out)
    if a.check:
        if not out.is_file():
            print(f"[inventory] ❌ 台账不存在：{out}", file=sys.stderr)
            return 2
        if out.read_text(encoding="utf-8") != text:
            print(f"[inventory] ❌ 台账与事实源不一致（过期）：{out}\n"
                  f"  修法：`.venv\\Scripts\\python.exe tools/prop_network_inventory.py`", file=sys.stderr)
            return 2
        print(f"[inventory] ✓ 台账与事实源一致：{out}（{len(text.splitlines())} 行）")
        return 0
    if a.stdout:
        print(text, end="")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    d = collect()
    print(f"[inventory] 已写 {out.relative_to(ROOT).as_posix()}："
          f"命题 {len(d['rows'])} · 卡 {len({r['card'] for r in d['rows']})} · "
          f"边 {len(set(d['edges']))} · 异常 引用卡 {len(d['bad_refs'])} / 无命题卡 {len(d['no_prop_cards'])}"
          f" / 闭包 {len(d['bad_closure'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
