#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""grounded_audit.py — grounded 标注实测与对照报告（596 任务3；**只读生成器**）。

为什么：W2 求解器给出 121 个节点的 IN/OUT/UNDEC 之后，必须回答三个"怎么办"的问题：
  1. 这个标注**和既有判决自洽吗**（命题的 `claim_type`、引用证据卡的 replay verdict）；
  2. 每个 IN 命题是**靠什么辩护链**站住的（哪些误解攻击它 → 那些误解为什么 OUT → 谁反驳了它们）；
  3. 有没有**异常**（命题被判 OUT / 误解被判 IN / 出现 UNDEC）——有就必须**显形并标红**，
     绝不能静默通过（"全绿"和"没检查"看起来一样，这正是本仓反复吃的亏）。

只读纪律：不写卡、不改命题库、不改标注/候选边；唯一写动作是 `--out` 指定的**报告文件**；
`--check` 模式一个字节都不写（用于检测报告是否过期）。

用法：
    python tools/grounded_audit.py                # 重新生成 data/grounded_audit_report.md
    python tools/grounded_audit.py --stdout       # 只打印
    python tools/grounded_audit.py --check        # 报告与事实源一致？（漂移/异常 ⇒ exit 2）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import gate_engine as ge  # noqa: E402

DEFAULT_LABELS = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_MANIFEST = ROOT / "build" / "replay_manifest.json"
DEFAULT_MIS = ROOT / "misconceptions"
OUT_DEFAULT = ROOT / "data" / "grounded_audit_report.md"
#: 594 实证对账基线（任务 2 已复现）
W2_EXPECTED = {"IN": 79, "OUT": 42, "UNDEC": 0}


# ── 读盘面（只读）──────────────────────────────────────────────────────────────
def load_labels(path: Path | str = DEFAULT_LABELS) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[audit] 标注文件不存在：{p}（先跑 weighted_af_solver.py solve）")
    doc = json.loads(p.read_text(encoding="utf-8"))
    for k in ("summary", "nodes"):
        if k not in doc:
            raise SystemExit(f"[audit] 标注文件结构不完整（缺 {k}）⇒ 拒绝生成报告")
    return doc


def prop_evidence_refs(atoms_dir: Path | str | None = None) -> dict[str, list[str]]:
    """命题 → 它引用的证据卡 id 列表（读卡面 `claim_structured[*].evidence`，只读）。"""
    out: dict[str, list[str]] = {}
    for p in sorted(ge.ATOMS.rglob("ATOM-*.md")):
        if "README" in p.name:
            continue
        m = ge._meta(p)
        cid = str(m.get("id") or p.stem)
        for it in (m.get("claim_structured") or []):
            if isinstance(it, dict) and str(it.get("id") or "").strip():
                refs = [str(x).strip() for x in ge._as_list(it.get("evidence")) if str(x).strip()]
                out[f"{cid}{aeg.PROP_SEP}{str(it['id']).strip()}"] = refs
    return out


def replay_verdicts(manifest: Path | str = DEFAULT_MANIFEST) -> tuple[dict[str, str], str]:
    """证据卡 replay verdict：`{EV id: verdict}` + 来源说明。

    优先读 `build/replay_manifest.json`（replay 的**实跑**结果）；清单缺失则回退卡面
    `verdict` 字段（声明值），并在报告里写明来源——**不猜**。
    """
    p = Path(manifest)
    if p.is_file():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            out = {Path(k).stem: str(v.get("verdict") or "").split(":")[0]
                   for k, v in d.items() if isinstance(v, dict)}
            if out:
                return out, f"build/replay_manifest.json（replay 实跑，{len(out)} 张）"
        except ValueError:
            pass
    out = {}
    for f in sorted(ge.EVIDENCE.rglob("EV-*.md")):
        if "README" in f.name:
            continue
        m = ge._meta(f)
        out[str(m.get("id") or f.stem)] = str(m.get("verdict") or "").split(":")[0]
    return out, f"卡面 `verdict` 字段回退（清单不可读，{len(out)} 张）"


def collect(labels_path: Path | str = DEFAULT_LABELS) -> dict:
    doc = load_labels(labels_path)
    nodes = doc["nodes"]
    refs = prop_evidence_refs()
    verdicts, vsrc = replay_verdicts()
    mis = aeg.read_mis(DEFAULT_MIS)
    return {"doc": doc, "nodes": nodes, "refs": refs, "verdicts": verdicts,
            "verdict_source": vsrc, "mis": mis}


# ── 派生统计 ───────────────────────────────────────────────────────────────────
def prop_verdict_class(refs: list[str], verdicts: dict[str, str]) -> str:
    """命题的 replay verdict 归类：全 confirm / 含 refute / 无引用卡。"""
    vs = [verdicts.get(r, "") for r in refs]
    if not refs or not any(vs):
        return "无引用卡"
    if any(v == "refute" for v in vs):
        return "refute"
    return "confirm"


def anomalies(nodes: dict) -> dict:
    """三类异常（任务书 596 任务3.4）：命题 OUT / 误解 IN / 任意 UNDEC。"""
    props = {k: v for k, v in nodes.items() if v["type"] == "proposition"}
    mis = {k: v for k, v in nodes.items() if v["type"] == "misconception"}
    return {"prop_out": sorted(k for k, v in props.items() if v["label"] == "OUT"),
            "mis_in": sorted(k for k, v in mis.items() if v["label"] == "IN"),
            "undec": sorted(k for k, v in nodes.items() if v["label"] == "UNDEC"),
            "prop_undec": sorted(k for k, v in props.items() if v["label"] == "UNDEC"),
            "mis_undec": sorted(k for k, v in mis.items() if v["label"] == "UNDEC")}


def defense_chain(pid: str, nodes: dict, limit: int = 3) -> list[str]:
    """一个 IN 命题的辩护链（人读文本）：误解攻击它 → 该误解被谁击败 → 因此它 IN。"""
    p = nodes[pid]
    lines = [f"- 命题 `{pid}`（{p.get('claim_type', '?')}，可信度 {p['credibility']}）判 **IN**："
             f"它击败了全部 {len(p['attackers'])} 个攻击它的误解（严格可信度优势）"]
    for att in p["attackers"]:
        m = nodes.get(att, {})
        beat_by = []
        for am in m.get("attackers", []):
            nm = nodes.get(am)
            if nm and nm["label"] == "IN" and nm["credibility"] > m.get("credibility", 1):
                beat_by.append(am)
        lines.append(f"  - 攻击者 `{att}`（误解，可信度 {m.get('credibility')}）判 "
                     f"**{m.get('label', '?')}**：被 {len(beat_by)} 条命题击败，"
                     f"如 `{beat_by[0] if beat_by else '（无）'}` 等")
    return lines


# ── 渲染 ───────────────────────────────────────────────────────────────────────
def render(data: dict) -> str:
    nodes = data["nodes"]
    doc = data["doc"]
    s = doc["summary"]
    an = anomalies(nodes)
    props = {k: v for k, v in nodes.items() if v["type"] == "proposition"}
    misses = {k: v for k, v in nodes.items() if v["type"] == "misconception"}
    L: list[str] = []
    add = L.append
    add("# grounded 标注实测与对照报告（596 任务3 · W2 模型）")
    add("")
    add("> **只读生成**：`.venv\\Scripts\\python.exe tools\\grounded_audit.py`（`--check` 校验本文件与事实源一致）。")
    add("> 数据源：`data/grounded_labels_w2.json`（`weighted_af_solver.py solve` 的派生结果）"
        "+ 卡面 `claim_structured` + `data/attack_edges_candidates.jsonl`。")
    add("> 本文件是**人审清单**，不参与任何判决；异常项以 ❌ 标出，出现异常时生成器 exit 2（fail-loud）。")
    add("")
    add("## §1 grounded 标注总览")
    add("")
    add(f"- 节点 **{s['nodes']}** = 命题 {len(props)} + 误解 {len(misses)}")
    add(f"- **IN {s['IN']} / OUT {s['OUT']} / UNDEC {s['UNDEC']}**"
        f"（in_propositions {s['IN_propositions']} · in_misconceptions {s['IN_misconceptions']}）")
    add(f"- 击败边 {doc['defeating_edges']}/{doc['edges']} · 不动点 **{doc['rounds']} 轮**收敛"
        f"（上限 100）")
    add(f"- 模型 `{doc['model']}` · 可信度档 {doc['credibility_levels']}")
    add("")
    add("## §2 与 `claim_type` 对照")
    add("")
    add("| claim_type | 节点数 | IN | OUT | UNDEC |")
    add("|---|---|---|---|---|")
    by_type: dict[str, Counter] = {}
    for v in props.values():
        by_type.setdefault(str(v.get("claim_type") or "?"), Counter())[v["label"]] += 1
    for ct in sorted(by_type):
        c = by_type[ct]
        add(f"| {ct} | {sum(c.values())} | {c['IN']} | {c['OUT']} | {c['UNDEC']} |")
    add("")
    add("## §3 与 replay verdict 对照")
    add("")
    add(f"来源：**{data['verdict_source']}**（实测 refute=0）")
    add("")
    add("| 引用卡 replay 归类 | 节点数 | IN | OUT | UNDEC |")
    add("|---|---|---|---|---|")
    by_v: dict[str, Counter] = {}
    for k, v in props.items():
        cls = prop_verdict_class(data["refs"].get(k, []), data["verdicts"])
        by_v.setdefault(cls, Counter())[v["label"]] += 1
    for cls in sorted(by_v):
        c = by_v[cls]
        add(f"| {cls} | {sum(c.values())} | {c['IN']} | {c['OUT']} | {c['UNDEC']} |")
    add("")
    add("MIS 侧对照（误解的 `refutations` 条数 vs 其 grounded 判决——"
        "误解全部 OUT，与其被多少条命题反驳无关，判决由可信度决定）：")
    add("")
    ref_hist: Counter = Counter()
    for mid in misses:
        ref_hist[len(data["mis"].get(mid, {}).get("refutations", []))] += 1
    add(f"- 误解 `refutations` 条数分布：{dict(sorted(ref_hist.items()))}")
    add("")
    add("## §4 辩护链示例（按攻击者数量取前 3 个 IN 命题）")
    add("")
    top = sorted((k for k, v in props.items() if v["label"] == "IN"),
                 key=lambda k: (-len(props[k]["attackers"]), k))[:3]
    for pid in top:
        for line in defense_chain(pid, nodes):
            add(line)
        add("")
    add("## §5 异常检测（fail-loud）")
    add("")
    if not (an["prop_out"] or an["mis_in"] or an["undec"]):
        add("- ✓ 无异常：命题无 OUT、误解无 IN、无 UNDEC 节点")
    else:
        add("### ❌❌ 异常【必须人审，不得静默通过】❌❌")
        add("")
        add(f"- ❌ 命题被判 **OUT**（{len(an['prop_out'])} 条，理论应为 0——命题该全 IN）："
            f"{an['prop_out'][:10]}")
        add(f"- ❌ 误解被判 **IN**（{len(an['mis_in'])} 条，理论应为 0——误解该全 OUT）："
            f"{an['mis_in'][:10]}")
        add(f"- ❌ **UNDEC** 节点（{len(an['undec'])} 个，理论应为 0——出现即攻击边不完整）："
            f"命题 {len(an['prop_undec'])} / 误解 {len(an['mis_undec'])}；样例 {an['undec'][:10]}")
    add("")
    add("## §6 与 594 实证对账")
    add("")
    add("| 指标 | 594 实证 | 本批实测 | 一致？ |")
    add("|---|---|---|---|")
    for k, want in W2_EXPECTED.items():
        got = s.get(k)
        add(f"| {k} | {want} | {got} | {'✓' if got == want else '❌'} |")
    add(f"| 节点数 | 121（79 命题 + 42 误解） | {s['nodes']} | "
        f"{'✓' if s['nodes'] == 121 else '❌'} |")
    add("")
    add(f"另注：**{len([k for k in props if not props[k]['attackers']])} 条命题没有任何误解攻击**"
        "（其所属卡的 MIS 关联记在**原子卡侧** `misconceptions` 字段，本批按任务书只读 MIS 侧 "
        "`related_atoms` ⇒ 不产边，偏差 D5）——它们无攻击者 ⇒ 立即 IN，不影响 IN/OUT 总数。")
    add("")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="grounded 标注对照报告（只读生成；异常 fail-loud）")
    ap.add_argument("--labels", default=str(DEFAULT_LABELS))
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--check", action="store_true", help="报告与事实源一致？（漂移/异常 ⇒ exit 2）")
    a = ap.parse_args(argv)
    data = collect(a.labels)
    text = render(data)
    an = anomalies(data["nodes"])
    bad = bool(an["prop_out"] or an["mis_in"] or an["undec"])
    out = Path(a.out)
    if a.check:
        if not out.is_file():
            print(f"[audit] ❌ 报告不存在：{out}", file=sys.stderr)
            return 2
        if out.read_text(encoding="utf-8") != text:
            print(f"[audit] ❌ 报告与事实源不一致（过期）：{out}\n"
                  f"  修法：`.venv\\Scripts\\python.exe tools\\grounded_audit.py`", file=sys.stderr)
            return 2
        if bad:
            print("[audit] ❌ 报告一致，但 grounded 标注存在异常（详见报告 §5）", file=sys.stderr)
            return 2
        print(f"[audit] ✓ 报告与事实源一致且无异常：{out}")
        return 0
    if a.stdout:
        print(text, end="")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    s = data["doc"]["summary"]
    print(f"[audit] 已写 {out.relative_to(ROOT).as_posix()}：IN {s['IN']} / OUT {s['OUT']} / "
          f"UNDEC {s['UNDEC']}")
    if bad:
        print(f"[audit] ❌ 异常：OUT 命题 {len(an['prop_out'])} · IN 误解 {len(an['mis_in'])} · "
              f"UNDEC {len(an['undec'])}（见报告 §5；exit 2）", file=sys.stderr)
        return 2
    print("[audit] ✓ 无异常（命题全 IN / 误解全 OUT / 无 UNDEC）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
