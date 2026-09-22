"""621 D2 · 人审质量评估（30 条逐条建议 vs 388 条批量授权）

四个对比维度：

| 维度 | 度量 | 期望（假设） | 实测（见报告） |
|---|---|---|---|
| **理由长度** | 字符数 均值/中位/极值 | 逐条 > 批量 | 见报告 §一 |
| **理由多样性** | 去重理由数 / 总数 | 逐条 > 批量（批量模板化） | 见报告 §二 |
| **决策一致性** | 逐条建议 vs 批量决策 | 应有分歧 | 见报告 §三 |
| **mirror 方向** | 边 ID 是否带方向 | 逐条应区分方向 | 见报告 §四 |

**诚实立场**：本工具**不美化逐条**。若实测显示逐条建议**同样是模板化的**，
如实写出来 —— 那说明"逐条"目前只是**形式上的逐条**。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DECISION_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
PROPOSALS = os.path.join(ROOT, "data", "authority", "pending_review_621.jsonl")
DEFAULT_REPORT = os.path.join(ROOT, "data", "human_review_quality_compare_621.md")

EDGE_RE = re.compile(r"^ae-(?P<src>[A-Z0-9\-]+)->(?P<dst>[A-Z0-9\-]+)::(?P<prop>prop-\d+)$")
ACTION_TO_POWER = {"approve": "ACCEPT", "modify": "OVERRIDE", "reject": "REJECT"}

# 语义族映射：消除「MODIFY vs OVERRIDE」这类纯词汇差异
POWER_FAMILY = {"ACCEPT": "accept", "MODIFY": "override", "OVERRIDE": "override",
                "REJECT": "reject", "ABSTAIN": "abstain"}


def load_batch(path: str = DECISION_LOG) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


def load_proposals(path: str = PROPOSALS) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


def _stats(values: list[int]) -> dict:
    if not values:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None}
    return {"n": len(values), "mean": round(statistics.mean(values), 2),
            "median": statistics.median(values), "min": min(values), "max": max(values)}


def reason_stats(rows: list[dict], key: str) -> dict:
    lens = [len(str(r.get(key) or "")) for r in rows if str(r.get(key) or "").strip()]
    uniq = len({str(r.get(key) or "").strip() for r in rows})
    total = len([r for r in rows if str(r.get(key) or "").strip()])
    return {
        "length": _stats(lens),
        "unique_reasons": uniq,
        "total_reasons": total,
        "diversity": round(uniq / total, 4) if total else None,
    }


def edge_direction(edge_id: str) -> dict | None:
    m = EDGE_RE.match(str(edge_id or ""))
    return m.groupdict() if m else None


def decision_consistency(batch: list[dict], proposals: list[dict]) -> dict:
    """把批量决策的 power 与逐条建议的 suggested_decision 逐边比对。

    **两套口径**（都很重要，如实并列）：
    - `literal`：字面比较。`modify` 建议（MODIFY）与批量日志的 `OVERRIDE`
      **字面不同** ⇒ 会被计为"不一致"，但这是**词汇映射差异**，不是真分歧。
    - `normalized`：按**语义族**比较（MODIFY ≡ OVERRIDE，都是"改写"）⇒ 消除词汇噪音。
    """
    by_edge: dict[str, str] = {}
    for e in batch:
        tid = str((e.get("target") or {}).get("id") or "")
        if tid:
            by_edge[tid] = e.get("power")

    lit_same = lit_diff = unknown = 0
    norm_same = norm_diff = 0
    detail = []
    for p in proposals:
        tid = str((p.get("target") or {}).get("id") or "")
        sug = p.get("suggested_decision")
        actual = by_edge.get(tid)
        if actual is None:
            unknown += 1
            detail.append({"edge": tid, "batch_power": None, "suggested": sug,
                           "verdict": "batch 无记录"})
            continue
        if actual == sug:
            lit_same += 1
        else:
            lit_diff += 1
            detail.append({"edge": tid, "batch_power": actual, "suggested": sug,
                           "verdict": "字面不一致",
                           "note": "词汇映射差异" if POWER_FAMILY.get(actual) == POWER_FAMILY.get(sug)
                                   else "语义分歧"})
        if POWER_FAMILY.get(actual) == POWER_FAMILY.get(sug):
            norm_same += 1
        else:
            norm_diff += 1
    n = len(proposals)
    return {
        "same": lit_same, "diff": lit_diff, "unknown": unknown, "detail": detail,
        "consistency_rate": round(lit_same / n, 4) if n else None,
        "norm_same": norm_same, "norm_diff": norm_diff,
        "norm_rate": round(norm_same / n, 4) if n else None,
        "semantic_disagreements": [d for d in detail
                                   if d.get("verdict") == "字面不一致"
                                   and d.get("note") == "语义分歧"],
    }


def mirror_handling(proposals: list[dict]) -> dict:
    """检查逐条条目是否保留方向（边 ID 形如 ae-SRC->DST::prop）。"""
    with_dir = 0
    reversed_pairs = 0
    seen: dict[tuple, str] = {}
    for p in proposals:
        tid = str((p.get("target") or {}).get("id") or "")
        d = edge_direction(tid)
        if not d:
            continue
        with_dir += 1
        rev = (d["dst"], d["src"], d["prop"])
        if rev in seen:
            reversed_pairs += 1
        seen[(d["src"], d["dst"], d["prop"])] = tid
    return {"with_direction": with_dir, "total": len(proposals),
            "reversed_pairs_found": reversed_pairs}


def analyze(batch_path: str = DECISION_LOG, proposal_path: str = PROPOSALS) -> dict:
    batch = load_batch(batch_path)
    props = load_proposals(proposal_path)
    return {
        "batch": {"count": len(batch), **reason_stats(batch, "reason")},
        "item": {"count": len(props), **reason_stats(props, "suggested_reason")},
        "consistency": decision_consistency(batch, props),
        "mirror": mirror_handling(props),
    }


def render_report(res: dict) -> str:
    o = ["# 621 D2 · 人审质量评估（30 条逐条建议 vs 388 条批量授权）\n"]
    b, i = res["batch"], res["item"]
    o.append("## 一、理由长度对比\n")
    o.append("| 组 | 条数 | 均值 | 中位 | 最小 | 最大 |")
    o.append(f"| 批量授权 | {b['count']} | {b['length']['mean']} | {b['length']['median']} | "
             f"{b['length']['min']} | {b['length']['max']} |")
    o.append(f"| 逐条建议 | {i['count']} | {i['length']['mean']} | {i['length']['median']} | "
             f"{i['length']['min']} | {i['length']['max']} |")
    o.append("")
    o.append("## 二、理由多样性对比\n")
    o.append("| 组 | 去重理由数 | 总理由数 | 多样性（去重/总） |")
    o.append(f"| 批量授权 | {b['unique_reasons']} | {b['total_reasons']} | {b['diversity']} |")
    o.append(f"| 逐条建议 | {i['unique_reasons']} | {i['total_reasons']} | {i['diversity']} |")
    o.append("")
    c = res["consistency"]
    o.append("## 三、决策一致性对比\n")
    o.append("| 口径 | 一致 | 不一致 | 一致率 |")
    o.append(f"| 字面比较 | {c['same']} | {c['diff']} | {c['consistency_rate']} |")
    o.append(f"| **语义族比较**（MODIFY≡OVERRIDE） | **{c['norm_same']}** | "
             f"**{c['norm_diff']}** | **{c['norm_rate']}** |")
    o.append(f"\n- 批量日志中无记录：{c['unknown']}")
    o.append(f"- **真正的语义分歧条目：{len(c['semantic_disagreements'])}**")
    if c["semantic_disagreements"]:
        for d in c["semantic_disagreements"]:
            o.append(f"  - `{d['edge']}`：批量={d['batch_power']} vs 建议={d['suggested']}")
    o.append("")
    o.append("## 四、mirror 方向处理\n")
    o.append(f"- 保留方向（边 ID 形如 `ae-SRC->DST::prop`）的条目：**{res['mirror']['with_direction']}"
             f" / {res['mirror']['total']}**")
    o.append(f"- 检测到的反向对：**{res['mirror']['reversed_pairs_found']}**")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    strs = [{"reason": "a" * 10}, {"reason": "a" * 10}, {"reason": "b" * 20}]
    st = reason_stats(strs, "reason")
    chk("长度统计正确", st["length"]["n"] == 3 and st["length"]["max"] == 20)
    chk("多样性 = 去重/总", st["unique_reasons"] == 2 and st["diversity"] == round(2 / 3, 4))
    chk("空输入长度统计安全", reason_stats([], "reason")["length"]["n"] == 0)

    batch = [{"target": {"id": "ae-A->B::prop-1"}, "power": "OVERRIDE"},
             {"target": {"id": "ae-C->D::prop-1"}, "power": "ACCEPT"}]
    props = [{"target": {"id": "ae-A->B::prop-1"}, "suggested_decision": "MODIFY"},
             {"target": {"id": "ae-C->D::prop-1"}, "suggested_decision": "ACCEPT"},
             {"target": {"id": "ae-X->Y::prop-1"}, "suggested_decision": "ACCEPT"}]
    # MODIFY(建议) vs OVERRIDE(批量) —— 语义同族但字面不同，应计入"不一致"（如实）
    cc = decision_consistency(batch, props)
    chk("一致性统计覆盖 3 条", cc["same"] + cc["diff"] + cc["unknown"] == 3)
    chk("batch 无记录计入 unknown", cc["unknown"] == 1)

    mh = mirror_handling([{"target": {"id": "ae-A->B::prop-1"}},
                          {"target": {"id": "ae-B->A::prop-1"}},
                          {"target": {"id": "bad-id"}}])
    chk("方向解析 2 条", mh["with_direction"] == 2)
    chk("反向对被识别", mh["reversed_pairs_found"] == 1)
    chk("edge 正则拒绝非法 id", edge_direction("bad-id") is None)
    chk("报告可渲染", "人审质量评估" in render_report(
        {"batch": {"count": 0, **st}, "item": {"count": 0, **st},
         "consistency": cc, "mirror": mh}))
    print(f"D2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 D2 人审质量评估")
    ap.add_argument("--batch-log", default=DECISION_LOG)
    ap.add_argument("--proposals", default=PROPOSALS)
    ap.add_argument("--out", default=DEFAULT_REPORT)
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = analyze(args.batch_log, args.proposals)
    md = render_report(res)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(f"wrote {args.out}")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
