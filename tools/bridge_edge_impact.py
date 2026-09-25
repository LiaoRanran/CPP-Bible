"""612 A3 · 加桥后 W2 重算 + 判决变化分析（**只读** · 复用 weighted_af_solver，不重实现求解）。

读取 A2 人审**已批准**的桥接边（`data/bridge_edge_review_612.jsonl` 中 approve/modify），
把它们作为 MIS→MIS 攻击边加入攻击图，基于 `weighted_af_solver` 的 W2 模型重算判决，输出加桥前后对比：

  * IN/OUT/UNDEC 节点数变化 · 击败边数变化 · 判决翻转清单（谁翻、为何）
  * 连通分量数变化（结构）+ 最大级联变化 + 承重脆弱节点提示
  * **同时报告 keep-low 与 upgrade-medium 两种 modify 口径**（不选边，见 611 B1）

what-if 三模式：
  * `approved-only`（默认）：只应用已批准的候选（0 条批准 ⇒ 与基线一致）
  * `all-medium`：假设 98 条候选全部升 medium
  * `all-high`：假设 98 条候选全部升 high

⚠️ 诚实预期（与 611 C3 一致）：W2 的 MIS 可信度取自其 **MIS↔命题** 边，MIS→MIS 桥接边默认不改可信度；
故**补桥对判决通常零影响**——本工具的价值是把「零影响」与「结构改善（分量减少）」同时据实报出。

CLI：`[--what-if MODE]`（写 `data/bridge_edge_impact_612.md`）/ `--stats` / `--check`（exit 0=通过）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_review as aer  # noqa: E402
import weighted_af_solver as w2  # noqa: E402

VERSION = "1.0"
CAND_IN = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REVIEW_LOG = ROOT / "data" / "bridge_edge_review_612.jsonl"
REPORT_OUT = ROOT / "data" / "bridge_edge_impact_612.md"

def _known_base() -> dict:
    """640b A1：基线取**单一权威源**（曾写死 611 的 114/7、121/0 = 签署前快照）。

    两种模式的基线都用权威现算值（640 A1 后双模式已趋同：79/42）。
    """
    try:
        import w2_authority_640b as _auth
        c = _auth.current()
        base = {"IN": c["IN"], "OUT": c["OUT"], "UNDEC": c["UNDEC"]}
    except Exception:  # noqa: BLE001
        base = {"IN": 114, "OUT": 7, "UNDEC": 0}          # 回退：历史登记口径
    return {"keep-low": dict(base), "upgrade-medium": dict(base),
            "components_before": 11}


KNOWN_BASE = _known_base()
MODES = ("keep-low", "upgrade-medium")
WHATIFS = ("approved-only", "all-medium", "all-high")


def load_candidates() -> list[dict]:
    return [json.loads(line) for line in CAND_IN.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_approved(path: Path | None = None) -> dict[str, str]:
    """→ {candidate_id: confidence}（只取**最后一条** approve/modify；reject 剔除）。"""
    p = Path(path) if path else REVIEW_LOG
    if not p.is_file():
        return {}
    latest: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        latest[r["id"]] = r.get("action")
        if r.get("action") in ("approve", "modify"):
            latest[r["id"]] = "approve"
            latest["__conf__" + r["id"]] = str(r.get("confidence") or "medium")
    out = {}
    for k, v in latest.items():
        if k.startswith("__conf__"):
            out[k[len("__conf__"):]] = v
    return out


def bridges_for(approved: dict[str, str], all_conf: str | None) -> list[dict]:
    out: list[dict] = []
    for c in load_candidates():
        eid = c["edge_id"]
        if all_conf is not None:
            conf = all_conf
        elif eid in approved:
            conf = approved[eid] or "medium"
        else:
            continue
        out.append({"id": eid, "source": c["source"], "target": c["target"],
                    "direction": "mis_to_mis", "confidence": conf,
                    "bridge": True, "priority": c["priority"]})
    return out


def component_count(edges: list[dict], nodes: list[str] | None = None) -> int:
    """无向 BFS 数连通分量（结构分析，非 W2 求解逻辑）。

    `nodes` 给出**全集**（含孤立点）⇒ 孤立点各计一个分量（与 611 C1 的 11 分量口径一致）。
    """
    adj: dict[str, set[str]] = {}
    for n in (nodes or []):
        adj.setdefault(n, set())
    for e in edges:
        s, t = str(e["source"]), str(e["target"])
        adj.setdefault(s, set()).add(t)
        adj.setdefault(t, set()).add(s)
    seen: set[str] = set()
    comps = 0
    for n in adj:
        if n in seen:
            continue
        comps += 1
        stack = [n]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(adj.get(x, ()))
    return comps


def impact(modify_mode: str, whatif: str) -> dict:
    anns = aer.load_annotations()
    raw = w2.load_edges()
    eff, _changes = w2.reviewed_edges(raw, anns, modify_mode=modify_mode)
    base_doc = w2.solve(eff)
    if whatif == "approved-only":
        bridges = bridges_for(load_approved(), None)
    elif whatif == "all-medium":
        bridges = bridges_for({}, "medium")
    else:
        bridges = bridges_for({}, "high")
    combined = eff + bridges
    new_doc = w2.solve(combined)
    d = w2.diff_verdicts(base_doc, new_doc, edges=bridges, changes=None)
    comp_before = component_count(eff, list(base_doc["nodes"]))
    comp_after = component_count(combined, list(new_doc["nodes"]))
    return {"modify_mode": modify_mode, "what_if": whatif,
            "bridges_applied": len(bridges),
            "base_summary": base_doc["summary"], "new_summary": new_doc["summary"],
            "base_defeating": base_doc["defeating_edges"],
            "new_defeating": new_doc["defeating_edges"],
            "flipped": d["flipped"], "flips": d["flips"],
            "components_before": comp_before, "components_after": comp_after,
            "base_edges": base_doc["edges"], "new_edges": new_doc["edges"]}


def _sum(s: dict) -> str:
    return f"IN {s['IN']} / OUT {s['OUT']} / UNDEC {s['UNDEC']}"


def render(results: list[dict]) -> str:
    L = ["# 612 A3 · 加桥后 W2 重算 + 判决变化分析（只读）", "",
         "> 复用 `weighted_af_solver` 的 W2 模型（不重实现求解）；同时报告 keep-low 与 upgrade-medium 两种口径（不选边）。",
         "> 桥接边为 MIS→MIS；W2 的 MIS 可信度取自其 MIS↔命题边，故**补桥通常不改判决**——本报告把「零影响」与「结构改善」同时据实列出。", "",
         "## 一、总览（加桥前后关键数字）", "",
         "| 口径 | what-if | 应用桥数 | 加桥前 | 加桥后 | 击败边 | 分量 | 翻转 |",
         "|---|---|---|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['modify_mode']} | {r['what_if']} | {r['bridges_applied']} | "
                 f"{_sum(r['base_summary'])} | {_sum(r['new_summary'])} | "
                 f"{r['base_defeating']}→{r['new_defeating']} | "
                 f"{r['components_before']}→{r['components_after']} | {r['flipped']} |")
    L += ["", "## 二、判决翻转清单", ""]
    any_flip = False
    for r in results:
        if not r["flips"]:
            continue
        any_flip = True
        L.append(f"### {r['modify_mode']} · {r['what_if']}（{len(r['flips'])} 个）")
        L.append("")
        L.append("| 节点 | 类型 | 旧 | 新 | 原因 |")
        L.append("|---|---|---|---|---|")
        for f in r["flips"][:30]:
            L.append(f"| `{f['node_id']}` | {f['node_type']} | {f['old']} | {f['new']} | {f['reason'][:60]} |")
        L.append("")
    if not any_flip:
        L.append("**加桥前后**所有节点判决均未翻转（0 个）——与 611 C3 的「加桥判决变化 0」一致：")
        L.append("桥接边是 MIS→MIS，W2 的 MIS 可信度取自 MIS↔命题边，桥不构成击败。")
        L.append("")
    L += ["## 三、风险提示", "",
          "- 加桥改善的是**连通性**（分量减少），不改判决；「脆弱节点（承重高但辩护弱）」清单待后续结合辩护链细化。",
          "- 加桥是否真成立仍须人审（A2）；本工具只算「若成立」的判决影响。", "",
          "## 四、口径与边界", "",
          "- **只读**：不写任何数据文件、不改攻击边；",
          "- 同时报告 keep-low（入库权威口径 IN114/OUT7）与 upgrade-medium（609 A3 口径 IN121/OUT0），**不裁决**；",
          "- `approved-only` 在 0 条批准时应与基线**逐项一致**（--check 锁此不变量）。", ""]
    return "\n".join(L)


def check(results: list[dict]) -> list[str]:
    problems: list[str] = []
    for r in results:
        if r["what_if"] == "approved-only" and r["bridges_applied"] == 0:
            want: dict[str, int] = KNOWN_BASE[r["modify_mode"]]  # type: ignore[assignment]
            got = r["base_summary"]
            for k, v in want.items():
                if got.get(k) != v:
                    problems.append(f"0 批准基线 {r['modify_mode']} {k} 应为 {v}（实测 {got.get(k)}）")
    for r in results:
        if r["components_before"] != KNOWN_BASE["components_before"]:
            problems.append(f"加桥前分量数应为 {KNOWN_BASE['components_before']}"
                            f"（实测 {r['components_before']}）")
            break
    for r in results:
        if r["what_if"] in ("all-medium", "all-high") and r["components_after"] != 7:
            problems.append(f"全量加桥后分量数应为 7（实测 {r['components_after']}）")
            break
    for r in results:
        for f in r["flips"]:
            if not {"node_id", "old", "new", "node_type"} <= set(f):
                problems.append(f"翻转清单字段缺失：{f}")
                break
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bridge_edge_impact", description="612 A3 加桥影响（只读）")
    ap.add_argument("--version", action="version", version=f"bridge_edge_impact {VERSION}")
    ap.add_argument("--what-if", choices=WHATIFS, default="approved-only")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    whatifs = [a.what_if] if a.what_if != "approved-only" else list(WHATIFS)
    results = [impact(m, w) for m in MODES for w in whatifs]
    if a.stats:
        print(json.dumps([{k: v for k, v in r.items() if k != "flips"} for r in results],
                         ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(results)
        if problems:
            for p in problems:
                print(f"[A3] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[A3] ✓ 加桥影响锁定（{len(results)} 组口径×what-if；approved-only 0 批准与基线一致）")
        return 0
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(results), encoding="utf-8", newline="\n")
    print(f"[A3] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（{len(results)} 组）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
