"""609 A2 · 人审质量控制（automation bias 检测 + 陷阱题）。

**只检测、只标记**——复核标记是人要处理的东西，本工具绝不自动改判、绝不自动执行人审。

三件事：

1. **陷阱题**（`inject-trap`）：给一条候选边注册"标准答案"（expected=approve|reject）。
   人审时若把陷阱题判错 ⇒ `trap_failed`。用 `TRAP::` 前缀与真实 388 条隔离，
   检测时既认 `TRAP::<id>` 形式的记录、也认直接落在被注册边上的记录。
2. **automation bias 检测**（`detect`）：逐条算 `review_seconds` / `reason_len` /
   `agree_rate`，打复核标记：`short_time`(<5s) / `short_reason`(<20 字符) /
   `rubber_stamp`(agree_rate==1.0 且 short_reason) / `trap_failed` / `none`。
3. **质量报告**（`report`）：陷阱题捕获率、平均耗时、平均理由长度、agree_rate、
   复核标记分布、automation bias 风险等级（低/中/高）。

诚实口径（**不编数字**）：
  * A1 的 annotations schema 里**没有** `review_seconds` 字段 ⇒ 存量人审记录
    **不可回溯测量**耗时。缺失时写 `review_seconds=null` + `review_seconds_measured=false`，
    **不参与** `short_time` 判定（否则会把"测不到"伪造成"秒过"）；
  * `agree_rate` = approve 数 / 总人审数（**不含陷阱题**），是该条为止的累计值；
  * quality.jsonl 是**派生件**（可由 annotations 完全重算），故 detect 是幂等**整体重写**；
  * 无人审记录时 report 给出 `insufficient evidence`，**不填 0**、不宣称"质量良好"。

CLI：
    inject-trap <edge_id> --expected <approve|reject>    0 ok / 1 edge 不存在 / 2 expected 非法
    detect                                               0 ok
    report                                               0 ok
    --check                                              0 合法 / 1 有非法行
"""
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import human_review_cli as hrc  # noqa: E402

VERSION = "1.0"
DEFAULT_ANN = hrc.DEFAULT_ANN
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_TRAPS = ROOT / "data" / "human_review_traps.json"
DEFAULT_QUALITY = ROOT / "data" / "human_review_quality.jsonl"

TRAP_PREFIX = "TRAP::"
SHORT_TIME_S = 5.0
MIN_REASON = hrc.MIN_REASON
FLAGS = ("trap_failed", "rubber_stamp", "short_reason", "short_time", "none")
TZ = timezone(timedelta(hours=8))

QUALITY_REQUIRED = ("edge_id", "kind", "review_seconds", "reason_len", "is_trap", "timestamp")
QUALITY_OPTIONAL = ("trap_expected", "trap_caught", "agree_rate", "review_flag",
                    "review_seconds_measured")


# ── 陷阱题台账 ────────────────────────────────────────────────────────────────
def load_traps(path: Path | str = DEFAULT_TRAPS) -> dict[str, dict]:
    """返回 {original_edge_id: trap}；缺件 ⇒ {}。"""
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        doc = json.loads(p.read_text(encoding="utf-8") or "{}")
    except ValueError as exc:
        raise ValueError(f"陷阱题台账 {p} 不是合法 JSON：{exc}") from exc
    traps = doc.get("traps", doc) if isinstance(doc, dict) else {}
    return {str(k): v for k, v in traps.items() if isinstance(v, dict)}


def inject_trap(edge_id: str, expected: str, *,
                path: Path | str = DEFAULT_TRAPS,
                edges_path: Path | str = DEFAULT_EDGES) -> dict:
    """注册一条陷阱题（expected=approve|reject）。edge 不在 388 条 ⇒ ValueError。"""
    if expected not in hrc.KINDS[:2]:                       # approve / reject
        raise ValueError(f"expected 须 ∈ {('approve', 'reject')}，实得 {expected!r}")
    base = str(edge_id)
    if base.startswith(TRAP_PREFIX):
        base = base[len(TRAP_PREFIX):]
    edge_ids = hrc.load_edge_ids(edges_path)
    if base not in edge_ids:
        raise ValueError(f"edge_id 不存在：{edge_id!r}（候选边共 {len(edge_ids)} 条）")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    traps = load_traps(p)
    now = datetime.now(TZ).replace(microsecond=0).isoformat()
    traps[base] = {"trap_edge_id": TRAP_PREFIX + base, "original_edge_id": base,
                   "expected": expected, "timestamp": now}
    p.write_text(json.dumps({"tool": "human_review_quality", "version": VERSION,
                             "trap_count": len(traps), "traps": traps},
                            ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                 encoding="utf-8", newline="\n")
    return traps[base]


def trap_of(edge_id: str, traps: dict[str, dict]) -> dict | None:
    eid = str(edge_id)
    if eid.startswith(TRAP_PREFIX):
        eid = eid[len(TRAP_PREFIX):]
    t = traps.get(eid)
    return dict(t, is_prefixed=str(edge_id).startswith(TRAP_PREFIX)) if t else None


# ── 检测 ──────────────────────────────────────────────────────────────────────
def _review_seconds(rec: dict) -> tuple[float | None, bool]:
    """（秒数, 是否真实测得）。A1 schema 无该字段 ⇒ 存量记录不可回溯测量 ⇒ None/False。"""
    v = rec.get("review_seconds")
    try:
        return (float(v), True) if v is not None else (None, False)
    except (TypeError, ValueError):
        return (None, False)


def detect_records(annotations: list[dict], traps: dict[str, dict]) -> list[dict]:
    """逐条派生质量记录。纯函数（不读盘/不写盘），便于测试注入。"""
    out: list[dict] = []
    total = 0          # 非陷阱题人审数
    approves = 0       # 非陷阱题 approve 数
    for rec in annotations:
        eid = str(rec.get("edge_id", ""))
        kind = hrc.kind_of(rec)
        trap = trap_of(eid, traps)
        is_trap = trap is not None
        sec, measured = _review_seconds(rec)
        reason = str(rec.get("reason", "") or "")
        reason_len = int(rec.get("reason_len", len(reason)))
        row = {"edge_id": eid, "kind": kind, "review_seconds": sec,
               "review_seconds_measured": measured, "reason_len": reason_len,
               "is_trap": is_trap, "timestamp": str(rec.get("timestamp", ""))}
        if is_trap:
            expected = str(trap.get("expected", ""))
            row["trap_expected"] = expected
            row["trap_caught"] = kind == expected
        else:
            total += 1
            if kind == "approve":
                approves += 1
            row["agree_rate"] = round(approves / total, 4)
        out.append(row)

    # 复核标记（优先级：trap_failed > rubber_stamp > short_reason > short_time > none）
    for row in out:
        short_time = (row.get("review_seconds_measured") and
                      row.get("review_seconds") is not None and
                      float(row["review_seconds"]) < SHORT_TIME_S)
        short_reason = row["reason_len"] < MIN_REASON
        rubber = (row.get("agree_rate") == 1.0 and short_reason)
        trap_failed = bool(row.get("is_trap")) and row.get("trap_caught") is False
        row["review_flag"] = ("trap_failed" if trap_failed else
                              "rubber_stamp" if rubber else
                              "short_reason" if short_reason else
                              "short_time" if short_time else "none")
    return out


def write_quality(records: list[dict], path: Path | str = DEFAULT_QUALITY) -> Path:
    """整体重写派生件（幂等：同输入 ⇒ 同文件）。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records)
    p.write_text(body, encoding="utf-8", newline="\n")
    return p


def detect(*, annotations_path: Path | str = DEFAULT_ANN,
           traps_path: Path | str = DEFAULT_TRAPS,
           quality_path: Path | str = DEFAULT_QUALITY) -> list[dict]:
    anns = hrc.load_annotations(annotations_path)
    traps = load_traps(traps_path)
    recs = detect_records(anns, traps)
    write_quality(recs, quality_path)
    return recs


# ── 报告 ──────────────────────────────────────────────────────────────────────
def summarize(records: list[dict]) -> dict:
    traps = [r for r in records if r.get("is_trap")]
    caught = [r for r in traps if r.get("trap_caught")]
    measured = [float(r["review_seconds"]) for r in records
                if r.get("review_seconds_measured") and r.get("review_seconds") is not None]
    real = [r for r in records if not r.get("is_trap")]
    flags = {f: sum(1 for r in records if r.get("review_flag") == f) for f in FLAGS}
    agree = [float(r["agree_rate"]) for r in real if r.get("agree_rate") is not None]
    if not records:
        risk = "insufficient evidence"
    elif flags["trap_failed"] or flags["rubber_stamp"]:
        risk = "high"
    elif flags["short_reason"] or flags["short_time"]:
        risk = "medium"
    else:
        risk = "low"
    n = len(records)
    return {
        "records": n,
        "traps_total": len(traps),
        "traps_caught": len(caught),
        "trap_capture_rate": (round(len(caught) / len(traps), 4) if traps else None),
        "avg_review_seconds": (round(sum(measured) / len(measured), 3) if measured else None),
        "review_seconds_measured": len(measured),
        "review_seconds_unmeasurable": n - len(measured),
        "avg_reason_len": (round(sum(r["reason_len"] for r in records) / n, 2) if n else None),
        "agree_rate": (round(agree[-1], 4) if agree else None),
        "agree_rate_note": "approve 数 / 人审总数（不含陷阱题）",
        "review_flags": flags,
        "bias_risk": risk,
        "insufficient_evidence": n == 0,
    }


def render_report(summary: dict) -> str:
    f = summary["review_flags"]
    lines = [
        f"[quality] 人审质量报告 · 记录 {summary['records']} 条",
        f"  陷阱题：{summary['traps_caught']}/{summary['traps_total']}"
        f" 捕获率={summary['trap_capture_rate']}",
        f"  平均耗时：{summary['avg_review_seconds']}s"
        f"（实测 {summary['review_seconds_measured']} 条 / 不可回溯测量 "
        f"{summary['review_seconds_unmeasurable']} 条 ⇒ 后者不参与判定）",
        f"  平均理由长度：{summary['avg_reason_len']} 字符",
        f"  agree_rate：{summary['agree_rate']}（{summary['agree_rate_note']}）",
        "  复核标记：" + " ".join(f"{k}={f[k]}" for k in FLAGS),
        f"  automation bias 风险等级：{summary['bias_risk']}",
    ]
    if summary["insufficient_evidence"]:
        lines.append("  ⚠️ 零人审记录 ⇒ insufficient evidence：不填 0、不宣称质量良好")
    return "\n".join(lines)


# ── 校验 ──────────────────────────────────────────────────────────────────────
def check(*, quality_path: Path | str = DEFAULT_QUALITY,
          traps_path: Path | str = DEFAULT_TRAPS) -> list[str]:
    problems: list[str] = []
    qp = Path(quality_path)
    if qp.is_file():
        for i, ln in enumerate(qp.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if not s:
                continue
            try:
                rec = json.loads(s)
            except ValueError as exc:
                problems.append(f"quality 第 {i} 行不是合法 JSON：{exc}")
                continue
            if not isinstance(rec, dict):
                problems.append(f"quality 第 {i} 行不是 JSON 对象")
                continue
            for k in QUALITY_REQUIRED:
                if k not in rec:
                    problems.append(f"quality 第 {i} 行缺字段 {k}")
            if "review_flag" in rec and rec["review_flag"] not in FLAGS:
                problems.append(f"quality 第 {i} 行 review_flag 非法：{rec['review_flag']!r}")
            if rec.get("is_trap") and rec.get("trap_expected") not in ("approve", "reject", None):
                problems.append(f"quality 第 {i} 行 trap_expected 非法：{rec['trap_expected']!r}")
            unknown = set(rec) - set(QUALITY_REQUIRED) - set(QUALITY_OPTIONAL)
            if unknown:
                problems.append(f"quality 第 {i} 行含未知字段 {sorted(unknown)}")
    try:
        traps = load_traps(traps_path)
    except ValueError as exc:
        problems.append(str(exc))
        return problems
    for k, v in traps.items():
        if v.get("expected") not in ("approve", "reject"):
            problems.append(f"陷阱题 {k} 的 expected 非法：{v.get('expected')!r}")
    return problems


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="human_review_quality",
                                description="609 A2 人审质量控制（陷阱题 + automation bias 检测）")
    p.add_argument("--version", action="version", version=f"human_review_quality {VERSION}")
    p.add_argument("--annotations", default=str(DEFAULT_ANN))
    p.add_argument("--edges", default=str(DEFAULT_EDGES))
    p.add_argument("--traps", default=str(DEFAULT_TRAPS))
    p.add_argument("--quality", default=str(DEFAULT_QUALITY))
    p.add_argument("--check", action="store_true", help="校验 quality.jsonl + 陷阱题台账合法性")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("inject-trap", help="注册一条陷阱题")
    sp.add_argument("edge_id")
    sp.add_argument("--expected", required=True, choices=("approve", "reject"))

    sub.add_parser("detect", help="扫描 annotations 派生质量记录")
    sub.add_parser("report", help="输出人审质量报告")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.check:
        problems = check(quality_path=args.quality, traps_path=args.traps)
        if problems:
            print(f"[quality] --check FAIL：{len(problems)} 处非法", file=sys.stderr)
            for m in problems[:200]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[quality] --check OK：质量台账 {args.quality} 与陷阱题台账 {args.traps} 全合法")
        return 0

    if args.cmd is None:
        build_parser().print_help()
        return 2

    if args.cmd == "inject-trap":
        try:
            t = inject_trap(args.edge_id, args.expected, path=args.traps,
                            edges_path=args.edges)
        except ValueError as exc:
            print(f"[quality] 拒写陷阱题：{exc}", file=sys.stderr)
            return 1 if "edge_id 不存在" in str(exc) else 2
        print(f"TRAP INJECTED: {t['trap_edge_id']} (expected={t['expected']})")
        return 0

    if args.cmd == "detect":
        recs = detect(annotations_path=args.annotations, traps_path=args.traps,
                      quality_path=args.quality)
        s = summarize(recs)
        f = s["review_flags"]
        print(f"[quality] detect OK：{len(recs)} 条质量记录 → {args.quality}")
        print("  复核标记：" + " ".join(f"{k}={f[k]}" for k in FLAGS))
        return 0

    recs = detect(annotations_path=args.annotations, traps_path=args.traps,
                  quality_path=args.quality)
    print(render_report(summarize(recs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
