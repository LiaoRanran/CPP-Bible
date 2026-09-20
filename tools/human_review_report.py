"""610 A2 · 人审质量报告（基于 388 条授权人审，**只读**、纯标准库）。

人审全量完成后，质量分析散在产品经理文档里 ⇒ 工具化：按 verdict / MIS / 主题 / 方向四个维度
统计，并做**质量异常检测**（歧义集中度、rubber-stamp 风险、耗时缺失、理由过短）。

口径声明（**不编数字**）：
  * verdict 取注解记录的 `action`（596 口径；609 的 `kind` 亦兼容）；
  * MIS 归属**按边的方向**判定（`mis_to_prop` ⇒ source 是 MIS；`prop_to_mis` ⇒ target 是 MIS），
    不用正则猜 —— 实测这样恰好得到 42 个 MIS（与 W2 图一致）；
  * `review_seconds`：存量人审**没有**该字段 ⇒ 一律计入"耗时缺失"异常，
    **不伪造 0**、不据此判 short_time；
  * 主题 = MIS id 的第二段（MEM/UB/HIST/CONC/LANG）；未知前缀归 `OTHER`。

CLI：
    generate          生成 data/human_review_quality_report.md（并打印关键数字）
    stats             统计信息（JSON）
    anomalies         质量异常列表（JSON）
    --check           报告数字与 annotations 逐字段对账（不一致 ⇒ exit 2）
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
import human_review_cli as hrc  # noqa: E402

VERSION = "1.0"
DEFAULT_ANN = hrc.DEFAULT_ANN
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_REPORT = ROOT / "data" / "human_review_quality_report.md"

TOPICS = ("MEM", "UB", "HIST", "CONC", "LANG")
SHORT_REASON = 20          # 与 609 A1 的 MIN_REASON 同口径
MODIFY_RATIO_THRESHOLD = 0.5


def load_annotations(path: Path | str | None = None) -> list[dict]:
    """加载人审记录（走 609 A1 的读侧：JSON 合法性 fail-loud、`action`/`kind` 双兼容）。"""
    return hrc.load_annotations(path if path else DEFAULT_ANN)


def edge_index(edges_path: Path | str | None = None) -> dict[str, dict]:
    """edge_id ⇒ 边（含 source/target/direction），用于**按方向**判 MIS 归属。"""
    out: dict[str, dict] = {}
    for e in aeg.load_edges(edges_path if edges_path else DEFAULT_EDGES):
        out[str(e["id"])] = e
    return out


def mis_of(edge: dict) -> str:
    """按方向取 MIS：`mis_to_prop` 取 source，`prop_to_mis` 取 target。"""
    return str(edge["source"]) if edge.get("direction") == "mis_to_prop" else str(edge["target"])


def topic_of(mis_id: str) -> str:
    parts = str(mis_id).split("-")
    return parts[1] if len(parts) > 1 and parts[1] in TOPICS else "OTHER"


# ── 四个维度的统计 ────────────────────────────────────────────────────────────
def summarize_by_verdict(annotations: list[dict]) -> dict:
    total = len(annotations)
    cnt = Counter(hrc.kind_of(a) for a in annotations)
    return {k: {"count": cnt.get(k, 0),
                "ratio": round(cnt.get(k, 0) / total, 4) if total else None}
            for k in ("approve", "modify", "reject")}


def _mis_counter(annotations: list[dict], edges_path: Path | str | None = None
                 ) -> dict[str, Counter]:
    idx = edge_index(edges_path)
    by_mis: dict[str, Counter] = {}
    for a in annotations:
        e = idx.get(str(a.get("edge_id")))
        if e is None:                      # 边不在候选集 ⇒ 归 unknown（显形，不静默丢）
            by_mis.setdefault("UNKNOWN-EDGE", Counter())[hrc.kind_of(a)] += 1
            continue
        by_mis.setdefault(mis_of(e), Counter())[hrc.kind_of(a)] += 1
    return by_mis


def summarize_by_mis(annotations: list[dict], edges_path: Path | str | None = None,
                     top: int | None = None) -> list[dict]:
    """按 MIS 分组；按 **modify 比例降序**（并列再按总条数降序）。"""
    rows = []
    for mid, c in _mis_counter(annotations, edges_path).items():
        total = sum(c.values())
        rows.append({"mis_id": mid, "total": total,
                     "approve": c.get("approve", 0), "modify": c.get("modify", 0),
                     "reject": c.get("reject", 0),
                     "modify_ratio": round(c.get("modify", 0) / total, 4) if total else None})
    rows.sort(key=lambda r: (-(r["modify_ratio"] or 0), -r["total"], r["mis_id"]))
    return rows[:top] if top else rows


def summarize_review_seconds(annotations: list[dict]) -> dict:
    """611 A2：`review_seconds` 耗时统计（平均/中位数/最大/最小/来源分布）。

    **诚实口径**：只有**显式测到**的记录才算进统计（`measured_count`）；缺字段或 `null` 的一律
    记为 `null_count`，**不按 0 计入**（0 秒是个真实值，不能当"没测"用；反之"没测"也绝不能当 0）。
    存量 388 条**全部未测量** ⇒ `measured=false`，此时 avg/median/max/min 一律 `None`（不编数）。
    """
    vals = [a["review_seconds"] for a in annotations
            if isinstance(a.get("review_seconds"), (int, float))
            and not isinstance(a.get("review_seconds"), bool)]
    total = len(annotations)
    out = {"total": total, "measured_count": len(vals), "null_count": total - len(vals),
           "measured": bool(vals),
           "measured_ratio": round(len(vals) / total, 4) if total else None,
           "avg": round(sum(vals) / len(vals), 1) if vals else None,
           "median": round(sorted(vals)[len(vals) // 2], 1) if vals else None,
           "max": max(vals) if vals else None, "min": min(vals) if vals else None,
           "sum": round(sum(vals), 1) if vals else None,
           "by_source": dict(sorted(Counter(str(a.get("review_seconds_source") or "unlabeled")
                                           for a in annotations
                                           if isinstance(a.get("review_seconds"), (int, float))
                                           and not isinstance(a.get("review_seconds"), bool)
                                           ).items())),
           "note": ("存量人审未测耗时 ⇒ 统计不可回溯（measured=false，不伪造 0）"
                    if not vals else
                    f"仅 {len(vals)}/{total} 条测得耗时；未测的 {total - len(vals)} 条不进统计")}
    return out


def summarize_by_topic(annotations: list[dict], edges_path: Path | str | None = None) -> dict:
    by_mis = _mis_counter(annotations, edges_path)
    out: dict[str, dict] = {}
    for mid, c in by_mis.items():
        t = topic_of(mid) if mid != "UNKNOWN-EDGE" else "OTHER"
        row = out.setdefault(t, {"total": 0, "approve": 0, "modify": 0, "reject": 0,
                                 "mis_count": 0})
        row["total"] += sum(c.values())
        row["approve"] += c.get("approve", 0)
        row["modify"] += c.get("modify", 0)
        row["reject"] += c.get("reject", 0)
        row["mis_count"] += 1
    total = sum(r["total"] for r in out.values()) or 1
    for row in out.values():
        row["ratio"] = round(row["total"] / total, 4)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["total"]))


def summarize_by_direction(annotations: list[dict],
                           edges_path: Path | str | None = None) -> dict:
    idx = edge_index(edges_path)
    cnt: Counter = Counter()
    for a in annotations:
        e = idx.get(str(a.get("edge_id")))
        cnt[str(e.get("direction")) if e else "unknown"] += 1
    return dict(sorted(cnt.items()))


# ── 质量异常 ──────────────────────────────────────────────────────────────────
def detect_quality_anomalies(annotations: list[dict],
                             edges_path: Path | str | None = None) -> list[dict]:
    """四类异常（全部来自实测字段，**不含推测**）。"""
    out: list[dict] = []
    rows = summarize_by_mis(annotations, edges_path)
    idx = edge_index(edges_path)
    reasons_by_mis: dict[str, list[str]] = {}
    for a in annotations:
        e = idx.get(str(a.get("edge_id")))
        key = mis_of(e) if e is not None else "UNKNOWN-EDGE"
        reasons_by_mis.setdefault(key, []).append(str(a.get("reason", "")))
    for r in rows:
        if r["total"] and r["modify_ratio"] == 1.0:
            out.append({"type": "modify_ratio_1.0", "mis_id": r["mis_id"],
                        "detail": f"{r['total']} 条全部被判 modify ⇒ 歧义度最高，建议人工复核"})
        if r["total"] and r["approve"] == r["total"]:
            lens = [len(x) for x in reasons_by_mis.get(r["mis_id"], [])]
            shortest = min(lens) if lens else 0
            if shortest < SHORT_REASON:
                out.append({"type": "rubber_stamp_risk", "mis_id": r["mis_id"],
                            "detail": f"全部 approve 且最短理由 {shortest} 字符 < {SHORT_REASON}"})
    missing = [a for a in annotations if a.get("review_seconds") is None]
    if missing:
        out.append({"type": "review_seconds_missing", "mis_id": "*",
                    "detail": f"{len(missing)}/{len(annotations)} 条无 review_seconds "
                              "⇒ 耗时不可回溯测量（不伪造 0，short_time 判定对其不可用）"})
    short = [a for a in annotations if len(str(a.get("reason", ""))) < SHORT_REASON]
    if short:
        out.append({"type": "reason_too_short", "mis_id": "*",
                    "detail": f"{len(short)} 条 reason < {SHORT_REASON} 字符（防 rubber-stamp 阈值）"})
    return out


# ── 报告 ──────────────────────────────────────────────────────────────────────
def _sample_accuracy_note(annotations: list[dict]) -> str:
    """抽样准确率**只从 annotations 的理由原文里提取**（不外部声明）。"""
    for a in annotations:
        r = str(a.get("reason", ""))
        if "抽样验证准确率" in r:
            seg = r.split("抽样验证准确率", 1)[1].split("，")[0]
            return f"理由原文记载：抽样验证准确率{seg}"
    return "理由原文未记载抽样准确率 ⇒ 本报告不声明该数字"


def generate_report(annotations: list[dict], edges_path: Path | str | None = None) -> str:
    v = summarize_by_verdict(annotations)
    by_mis = summarize_by_mis(annotations, edges_path)
    topics = summarize_by_topic(annotations, edges_path)
    dirs = summarize_by_direction(annotations, edges_path)
    an = detect_quality_anomalies(annotations, edges_path)
    zeros = [r for r in by_mis if r["modify_ratio"] == 1.0]
    lines = [
        "# 人审质量报告（610 A2 · 只读生成）", "",
        "> 数据源：`data/human_attack_edge_annotations.jsonl`（用户两次授权的真实人审）；",
        "> 本报告由 `tools/human_review_report.py` 生成，**不含任何外部输入的数字**。", "",
        "## 1. 总览", "",
        f"- 记录 **{len(annotations)}** 条：approve {v['approve']['count']}"
        f"（{v['approve']['ratio']:.1%}）· modify {v['modify']['count']}"
        f"（{v['modify']['ratio']:.1%}）· reject {v['reject']['count']}",
        f"- MIS 组 **{len(by_mis)}** 个 · 主题 {len(topics)} 类",
        f"- {_sample_accuracy_note(annotations)}", "",
        "## 2. 按 verdict 分布", "",
        "| verdict | 条数 | 占比 |", "|---|---:|---:|",
    ]
    for k in ("approve", "modify", "reject"):
        ratio = v[k]["ratio"]
        shown = "—" if ratio is None else f"{ratio:.1%}"
        lines.append(f"| {k} | {v[k]['count']} | {shown} |")
    lines += ["", "## 3. 按 MIS 分组（modify 比例 Top 10）", "",
              "| MIS | 总条数 | approve | modify | modify 比例 |", "|---|---:|---:|---:|---:|"]
    for r in by_mis[:10]:
        lines.append(f"| `{r['mis_id']}` | {r['total']} | {r['approve']} | {r['modify']} | "
                     f"{r['modify_ratio']:.2f} |")
    lines += ["", "## 4. 按主题分布", "", "| 主题 | MIS 数 | 条数 | 占比 | approve | modify |",
              "|---|---:|---:|---:|---:|---:|"]
    for t, row in topics.items():
        lines.append(f"| {t} | {row['mis_count']} | {row['total']} | {row['ratio']:.1%} | "
                     f"{row['approve']} | {row['modify']} |")
    lines += ["", "## 5. 按方向分布", "", "| direction | 条数 |", "|---|---:|"]
    for d, n in dirs.items():
        lines.append(f"| {d} | {n} |")
    lines += ["", "## 6. 质量异常检测", ""]
    if an:
        lines += ["| 类型 | MIS | 说明 |", "|---|---|---|"]
        lines += [f"| {a['type']} | `{a['mis_id']}` | {a['detail']} |" for a in an]
    else:
        lines.append("- 未检出（注意：**未检出 ≠ 无风险**，只是本工具的四类判据都没命中）")
    lines += ["", f"## 7. modify 比例 = 1.0 的 MIS（{len(zeros)} 个）", ""]
    lines += [f"- `{r['mis_id']}`（{r['total']} 条全 modify）" for r in zeros] or ["- 无"]
    lines += ["", "## 8. 后续建议", "",
              "- 上表 `modify_ratio_1.0` 的 MIS 是**歧义度最高**的一组：建议优先安排第二轮人审"
              "（把'证据较充分但偏保守'的档位判断沉淀成判据）；",
              "- 耗时类质量指标（automation bias / 单位时间产出）：人审 CLI 的 schema **已扩**"
              "（611 A2 新增 `review_seconds`），新记录起即可测；存量 388 条**不可回溯**"
              "（如实标 measured=false，**不伪造 0**）；",
              "- 本报告只呈现事实与异常清单，**不自动执行任何人审**、不修改任何注解。", ""]
    # 611 A2：耗时统计单列一节（放在 §8 之后 ⇒ 610 的"## 8. 后续建议"断言不受影响）
    rs = summarize_review_seconds(annotations)
    lines += ["## 9. 耗时统计（review_seconds · 611 A2）", "", "| 指标 | 值 |", "|---|---:|",
              f"| 记录总数 | {rs['total']} |",
              f"| **测得** | {rs['measured_count']} |",
              f"| 未测得（null/缺字段） | {rs['null_count']} |",
              f"| measured | {'true' if rs['measured'] else '**false**'} |"]
    for k, label in (("avg", "平均（s）"), ("median", "中位数（s）"), ("max", "最大（s）"),
                     ("min", "最小（s）"), ("sum", "合计（s）")):
        v = rs[k]
        lines.append(f"| {label} | {'—' if v is None else v} |")
    lines += [f"| 计时来源 | {rs['by_source'] if rs['by_source'] else '—'} |", "",
              f"- {rs['note']}", "",
              "- **口径**：只统计**显式测得**的记录；未测的既不按 0 计入、也不参与均值"
              "（0 秒是真实值，缺测是另一种状态，两者不可混同）。", ""]
    return "\n".join(lines)


def write_report(report: str, path: Path | str | None = None) -> Path:
    p = Path(path) if path else DEFAULT_REPORT
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(report, encoding="utf-8", newline="\n")
    return p


def check(report_path: Path | str | None = None,
          ann_path: Path | str | None = None,
          edges_path: Path | str | None = None) -> list[str]:
    """报告 vs annotations 逐字段对账（不一致 ⇒ 返回问题列表 ⇒ CLI exit 2）。"""
    problems: list[str] = []
    p = Path(report_path) if report_path else DEFAULT_REPORT
    if not p.is_file():
        return [f"报告不存在：{p}（先跑 generate）"]
    text = p.read_text(encoding="utf-8")
    anns = load_annotations(ann_path)
    v = summarize_by_verdict(anns)
    by_mis = summarize_by_mis(anns, edges_path)
    expect = [f"- 记录 **{len(anns)}** 条",
              f"approve {v['approve']['count']}", f"modify {v['modify']['count']}",
              f"reject {v['reject']['count']}",
              f"MIS 组 **{len(by_mis)}** 个"]
    fresh = generate_report(anns, edges_path)
    if text != fresh:
        problems.append("报告与事实源重新渲染不一致（过期）⇒ 跑 generate 重生成")
    for e in expect:
        if e not in text:
            problems.append(f"报告缺事实：{e!r}")
    if text != fresh:
        return problems
    if len(by_mis) == 0:
        problems.append("MIS 组数为 0 ⇒ 边索引未生效")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_report",
                                 description="610 A2 人审质量报告（只读 · 纯标准库）")
    ap.add_argument("--version", action="version", version=f"human_review_report {VERSION}")
    ap.add_argument("--annotations", default=None)
    ap.add_argument("--edges", default=None)
    ap.add_argument("--report", default=None)
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("generate", "stats", "anomalies"):
        sub.add_parser(name)
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.report, a.annotations, a.edges)
        if problems:
            print(f"[hrreport] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 2
        print(f"[hrreport] --check OK：报告 {Path(a.report or DEFAULT_REPORT).name} "
              f"与 annotations 逐字段一致")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    anns = load_annotations(a.annotations)
    if a.cmd == "stats":
        print(json.dumps({"by_verdict": summarize_by_verdict(anns),
                          "by_direction": summarize_by_direction(anns, a.edges),
                          "by_topic": summarize_by_topic(anns, a.edges),
                          "mis_count": len(summarize_by_mis(anns, a.edges)),
                          "top_modify_mis": summarize_by_mis(anns, a.edges)[:5],
                          "review_seconds": summarize_review_seconds(anns)},   # 611 A2
                         ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "anomalies":
        print(json.dumps(detect_quality_anomalies(anns, a.edges),
                         ensure_ascii=False, indent=1))
        return 0
    p = write_report(generate_report(anns, a.edges), a.report)
    v = summarize_by_verdict(anns)
    print(f"[hrreport] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}："
          f"{len(anns)} 条 · approve {v['approve']['count']} / modify {v['modify']['count']} / "
          f"reject {v['reject']['count']} · MIS 组 {len(summarize_by_mis(anns, a.edges))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
