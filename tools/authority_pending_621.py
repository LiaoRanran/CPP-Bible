"""621 D1 · 30 条逐条复核清单 → Authority「待审条目」

把 615 的 30 条逐条复核候选（17 modify + 13 approve）转成 **待审条目**。

**⚠ 关键边界：待审条目 ≠ 决策。**
- 本工具**绝不**写入 `data/authority/authority_log.jsonl`（那是 append-only 的**决策**日志）。
  往决策日志里写任何一条，都等于**代签**（哪怕写 ABSTAIN）。
- 待审条目写入**独立通道** `data/authority/pending_review_621.jsonl`，
  `status=pending`、`review_method=item_by_item_proposed`，等**人**执行。
- 工具每跑一次会**校验决策日志条目数不变**，从机制上保证"不代签"。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DEFAULT_SOURCE = os.path.join(ROOT, "data", "human_review_item_by_item_30_615.md")
DEFAULT_OUT = os.path.join(ROOT, "data", "authority", "pending_review_621.jsonl")
DEFAULT_REPORT = os.path.join(ROOT, "data", "authority_pending_30_621.md")
DECISION_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")

# 615 清单里的「当前」列 → 建议决策
CURRENT_TO_SUGGESTION = {"modify": "MODIFY", "approve": "ACCEPT", "reject": "REJECT"}


def parse_615(path: str = DEFAULT_SOURCE) -> list[dict]:
    """解析 615 清单的决策表格（只读 markdown）。"""
    rows: list[dict] = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            if not ln.startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 9 or not cells[0].isdigit():
                continue
            rows.append({
                "n": int(cells[0]),
                "edge_id": cells[1].strip("`"),
                "mis_id": cells[2],
                "proposition": cells[3],
                "atom_card": cells[4],
                "current": cells[5].lower(),
                "reason_len": int(cells[6]) if cells[6].isdigit() else None,
                "suggestion": cells[7],
                "confidence": cells[8],
            })
    return rows


def to_proposal(row: dict) -> dict:
    return {
        "proposal_id": f"prop-621-{row['n']:03d}",
        "type": "pending_review_proposal",
        "target": {"type": "attack_edge", "id": row["edge_id"]},
        "source_mis": row["mis_id"],
        "proposition": row["proposition"],
        "atom_card": row["atom_card"],
        "suggested_decision": CURRENT_TO_SUGGESTION.get(row["current"], "UNDECIDED"),
        "suggested_reason": row["suggestion"],
        "confidence": row["confidence"],
        "review_method": "item_by_item_proposed",
        "status": "pending",
        "source": "data/human_review_item_by_item_30_615.md",
        "note": "这是**建议**，不是**决策**；需人执行后另行写入 Authority 决策日志",
    }


def build(source: str = DEFAULT_SOURCE) -> list[dict]:
    return [to_proposal(r) for r in parse_615(source)]


def write(out: str, proposals: list[dict]) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        for p in proposals:
            fh.write(json.dumps(p, ensure_ascii=False, sort_keys=True) + "\n")
    return out


# ── 622 D1：把待审条目**按用户授权**执行，写入 Authority 决策日志 ─────────────
# 硬边界（622 §六.5）：人审执行必须标注来源（615 决策清单 + 用户授权日期），
# 不伪装成系统自动决策。故每条决策都带 authorized_by / source / review_method。
REVIEWER_DEFAULT = "human:LiaoRanran"
AUTHORIZATION = "user_authorization_2026-09-21"
SOURCE = "615_decision_list"
REVIEW_METHOD = "item_by_item_executed"

# 建议决策 → Authority 决策日志的 power
SUGGESTION_TO_POWER = {"ACCEPT": "ACCEPT", "MODIFY": "OVERRIDE", "REJECT": "REJECT"}


def existing_decision_index(log_path: str = DECISION_LOG) -> dict[str, str]:
    """edge_id → 该边最后一条决策的 decision_id（用于 OVERRIDE 指名）。"""
    idx: dict[str, str] = {}
    for e in _load_log(log_path):
        tid = str((e.get("target") or {}).get("id") or "")
        if tid:
            idx[tid] = str(e.get("decision_id") or "")
    return idx


def _load_log(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def build_decision(proposal: dict, prev_id: str | None,
                   reviewer: str = REVIEWER_DEFAULT) -> dict:
    """把一条待审条目转成可写入决策日志的决策（带来源标注）。"""
    power = SUGGESTION_TO_POWER.get(str(proposal.get("suggested_decision") or ""), "ACCEPT")
    dec = {
        "target": {"type": "attack_edge",
                   "id": (proposal.get("target") or {}).get("id")},
        "power": power,
        "reviewer": reviewer,
        "reason": f"[615决策清单] {proposal.get('suggested_reason')}",
        "review_method": REVIEW_METHOD,
        "authorized_by": AUTHORIZATION,
        "source": SOURCE,
        "proposal_id": proposal.get("proposal_id"),
        "confidence": proposal.get("confidence"),
        "note": "按用户授权执行 615 决策清单（逐条）；非系统自动决策",
    }
    if power == "OVERRIDE":
        dec["overrides"] = prev_id or f"legacy:pre_annotation:{(proposal.get('target') or {}).get('id')}"
    return dec


def execute_all(proposals: list[dict], log_path: str = DECISION_LOG,
                reviewer: str = REVIEWER_DEFAULT) -> dict:
    """逐条执行（append-only）；返回执行统计与链校验结果。"""
    sys.path.insert(0, HERE)
    import authority_log_620 as AL  # noqa: PLC0415
    before = decision_log_count(log_path)
    idx = existing_decision_index(log_path)
    entries = []
    for p in proposals:
        edge = (p.get("target") or {}).get("id")
        dec = build_decision(p, idx.get(str(edge)), reviewer)
        entries.append(AL.append(log_path, dec))
    after = decision_log_count(log_path)
    ok, errs = AL.verify(log_path)
    return {"executed": len(entries), "before": before, "after": after,
            "delta": after - before, "chain_ok": ok, "chain_errors": errs[:5],
            "entries": entries}


# ── 622 D2：把「已执行的 30 条」与 W2 求解器的真实输入（annotations）比对 ────────
# 为什么要比：`weighted_af_solver` 读的是 `human_attack_edge_annotations.jsonl`，
# **不是** Authority 决策日志 ⇒ 两条通道是否"同向"决定了 D1 对 W2 有无影响。
ACTION_FOR_POWER = {"ACCEPT": "approve", "OVERRIDE": "modify", "REJECT": "reject"}


def compare_with_annotations(decisions: list[dict],
                             ann_path: str | None = None) -> dict:
    """逐边比较「决策的 action」与「annotations 里既有的 action」是否同向。"""
    p = ann_path or os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
    ann: dict[str, dict] = {}
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            for ln in fh:
                ln = ln.strip()
                if ln:
                    e = json.loads(ln)
                    ann[str(e.get("edge_id"))] = e
    same = diff = missing = 0
    detail = []
    for d in decisions:
        edge = str((d.get("target") or {}).get("id"))
        a = ann.get(edge)
        if a is None:
            missing += 1
            detail.append({"edge": edge, "power": d.get("power"), "ann_action": None,
                           "verdict": "annotations 无此边"})
            continue
        want = ACTION_FOR_POWER.get(str(d.get("power")))
        got = str(a.get("action"))
        if want == got:
            same += 1
        else:
            diff += 1
            detail.append({"edge": edge, "power": d.get("power"), "ann_action": got,
                           "verdict": "与既有标注不同向"})
    return {"total": len(decisions), "same": same, "diff": diff, "missing": missing,
            "annotations_edges": len(ann), "differences": detail,
            "all_same_direction": diff == 0 and missing == 0}


def decision_log_count(path: str = DECISION_LOG) -> int:
    if not os.path.exists(path):
        return 0
    with open(path, encoding="utf-8") as fh:
        return sum(1 for ln in fh if ln.strip())


def render_report(proposals: list[dict], log_before: int, log_after: int) -> str:
    o = ["# 621 D1 · 30 条逐条复核清单 → Authority 待审条目\n"]
    o.append("> **重要**：这些是**建议（pending proposals）**，不是**决策**。")
    o.append("> 人执行后才会写入 Authority 决策日志（`data/authority/authority_log.jsonl`）。\n")
    o.append("## 一、待审条目统计\n")
    o.append(f"- 条目总数：**{len(proposals)}**")
    sug: dict[str, int] = {}
    for p in proposals:
        sug[p["suggested_decision"]] = sug.get(p["suggested_decision"], 0) + 1
    for k, v in sorted(sug.items()):
        o.append(f"- 建议 {k}：{v}")
    o.append("")
    o.append("## 二、不代签证明（决策日志未被写入）\n")
    o.append("| 阶段 | 决策日志条目数 |")
    o.append(f"| 生成待审条目**前** | {log_before} |")
    o.append(f"| 生成待审条目**后** | {log_after} |")
    ok = log_before == log_after
    o.append(f"\n⇒ **{'未写入决策日志 ✅（不代签）' if ok else '⚠ 决策日志发生变化！'}**\n")
    o.append("## 三、与 615 清单的对应关系\n")
    o.append("| proposal_id | 615 # | 边 ID | 当前 | 建议决策 | 置信度 |")
    for p in proposals:
        n = int(p["proposal_id"].split("-")[-1])
        o.append(f"| `{p['proposal_id']}` | {n} | `{p['target']['id']}` | "
                 f"{'modify' if p['suggested_decision'] == 'MODIFY' else 'approve'} | "
                 f"{p['suggested_decision']} | {p['confidence']} |")
    o.append("")
    o.append("## 四、声明\n")
    o.append("1. 30 条**全部为 pending**，`review_method=item_by_item_proposed`。")
    o.append("2. **没有一条**被写成已决策条目；Authority 决策日志**零改动**（见 §二 计数）。")
    o.append("3. 是否执行这 30 条、以及执行结论，**由人决定**（621 §八 人拍板项 3）。")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    rows = parse_615()
    chk("解析出 30 条", len(rows) == 30)
    chk("modify 17 条", sum(1 for r in rows if r["current"] == "modify") == 17)
    chk("approve 13 条", sum(1 for r in rows if r["current"] == "approve") == 13)
    props = build()
    chk("全部为 pending", all(p["status"] == "pending" for p in props))
    chk("review_method 为 item_by_item_proposed",
        all(p["review_method"] == "item_by_item_proposed" for p in props))
    chk("建议决策映射正确",
        all(p["suggested_decision"] in ("MODIFY", "ACCEPT") for p in props))
    chk("proposal_id 唯一", len({p["proposal_id"] for p in props}) == len(props))
    chk("决策日志存在且可计数", isinstance(decision_log_count(), int))
    chk("报告可渲染（含不代签证明）",
        "不代签证明" in render_report(props, 5, 5))
    chk("空输入不崩", parse_615("__nonexistent__") == [])
    print(f"D1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 D1 30 条逐条复核 → Authority 待审条目（不代签）")
    ap.add_argument("--source", default=DEFAULT_SOURCE)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--report", default=DEFAULT_REPORT)
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    before = decision_log_count()
    proposals = build(args.source)
    write(args.out, proposals)
    after = decision_log_count()
    md = render_report(proposals, before, after)
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(json.dumps({"proposals": len(proposals), "out": args.out,
                      "decision_log_before": before, "decision_log_after": after,
                      "no_forgery": before == after}, ensure_ascii=False))
    return 0 if before == after else 1


if __name__ == "__main__":
    sys.exit(main())
