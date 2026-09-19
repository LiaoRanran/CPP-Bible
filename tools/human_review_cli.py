"""609 A1 · 人审 CLI（append-only + fail-closed），操作 596 人审通道。

这是一支**给人用的笔**，不是自动判决器：

  * 只**追加**一行 JSONL 到 `data/human_attack_edge_annotations.jsonl`
    （596 入库为空的 append-only 通道）；不修改已有行、不删除已有行；
  * **fail-closed**：edge_id 不在 388 条候选边里 ⇒ 拒写；reason < 20 字符 ⇒ 拒写；
    reviewer 必须 = 字面量 `human`（机器不得冒名）；modify 必须有合法 confidence；
  * **不自动执行任何人审**（本 exe 只被人调用），**不自动重算 W2**
    （重算要人显式跑 `weighted_af_solver.py solve --include-human-reviewed`，见 A3）。

annotations 记录 schema（每行一个 JSON 对象）：

    edge_id     str  必填  必须存在于 attack_edge_generator 产出的 388 条候选边
    kind        str  必填  approve | reject | modify
    reviewer    str  必填  固定 "human"（不接受其他值）
    timestamp   str  必填  ISO 8601，形如 2026-09-19T12:00:00+08:00
    reason      str  必填  ≥ 20 字符（防 rubber-stamp）
    confidence  str  可选  high|medium|low，kind=modify 时必填

⚠️ 与 596 `attack_edge_review.py` 的口径差：596 用字段名 `action`，609 任务书用 `kind`。
本工具**写** `kind`、**读**时兼容两者（`action` 会被归一化成 `kind`），两条通路互不打断。

CLI：
    approve <edge_id> --reason <t>        0 ok / 1 edge 不存在 / 2 reason 过短
    reject  <edge_id> --reason <t>        0 ok / 1 / 2
    modify  <edge_id> --confidence <lvl> --reason <t>
                                          0 ok / 1 / 2 / 3 confidence 非法
    list    [--pending|--approved|--rejected|--modified] [--limit N]
    --check                               0 全合法 / 1 有非法行（打印行号+原因）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import attack_edge_review as aer  # noqa: E402

VERSION = "1.0"
DEFAULT_ANN = aer.DEFAULT_ANN
DEFAULT_EDGES = aeg.DEFAULT_OUT

KINDS = ("approve", "reject", "modify")
CONFIDENCES = tuple(sorted(aeg.CONFIDENCE_WEIGHT))     # low / medium / high
REVIEWER = "human"
MIN_REASON = 20
REQUIRED = ("edge_id", "kind", "reviewer", "timestamp", "reason")
OPTIONAL = ("confidence",)
TZ = timezone(timedelta(hours=8))

STATUS_OF_KIND = {"approve": "approved", "reject": "rejected", "modify": "modified"}


# ── 读取 ──────────────────────────────────────────────────────────────────────
def load_annotations(path: Path | str = DEFAULT_ANN) -> list[dict]:
    """读人审通道；缺件 ⇒ `[]`。每行必须可 JSON 解析，否则 `ValueError`（fail-loud）。"""
    p = Path(path)
    if not p.is_file():
        return []
    out: list[dict] = []
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        s = ln.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except ValueError as exc:
            raise ValueError(f"{p} 第 {i} 行不是合法 JSON：{exc}") from exc
        if not isinstance(obj, dict):
            raise ValueError(f"{p} 第 {i} 行不是 JSON 对象")
        out.append(obj)
    return out


def kind_of(rec: dict) -> str:
    """609 的 `kind` 为主；兼容 596 的 `action` 字段（读侧归一化）。"""
    return str(rec.get("kind") or rec.get("action") or "").strip()


def load_edge_ids(path: Path | str = DEFAULT_EDGES) -> set[str]:
    return {str(e["id"]) for e in aeg.load_edges(path)}


def latest_by_edge(annotations: list[dict]) -> dict[str, dict]:
    """同一条边多次审查 ⇒ 取**最后一条**（历史仍在文件里可追溯）。"""
    last: dict[str, dict] = {}
    for a in annotations:
        last[str(a.get("edge_id"))] = a
    return last


def status_of(edge_id: str, last: dict[str, dict]) -> str:
    a = last.get(edge_id)
    if a is None:
        return "pending"
    return STATUS_OF_KIND.get(kind_of(a), "pending")


# ── 校验 ──────────────────────────────────────────────────────────────────────
def validate_record(rec: dict, edge_ids: set[str]) -> list[str]:
    """返回问题列表（空 = 合法）。逐字段校验，一次报全部问题（便于人一次修完）。"""
    problems: list[str] = []
    for k in REQUIRED:
        if not str(rec.get(k) or "").strip():
            problems.append(f"缺字符段 {k}")
    unknown = set(rec) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        problems.append(f"含未知字段 {sorted(unknown)}")
    k = kind_of(rec)
    if k and k not in KINDS:
        problems.append(f"kind 非法：{k!r}（须 ∈ {KINDS}）")
    rv = str(rec.get("reviewer") or "")
    if rv and rv != REVIEWER:
        problems.append(f"reviewer 必须 = {REVIEWER!r}（防机器冒名），实得 {rv!r}")
    ts = str(rec.get("timestamp") or "")
    if ts:
        if not parse_timestamp(ts):
            problems.append(f"timestamp 不是合法 ISO 8601：{ts!r}")
    r = str(rec.get("reason") or "")
    if r and len(r) < MIN_REASON:
        problems.append(f"reason 长度 {len(r)} < {MIN_REASON}（防 rubber-stamp）")
    eid = str(rec.get("edge_id") or "")
    if eid and edge_ids and eid not in edge_ids:
        problems.append(f"edge_id 不在候选边（共 {len(edge_ids)} 条）里：{eid!r}")
    conf = rec.get("confidence")
    if conf is not None:
        if conf not in CONFIDENCES:
            problems.append(f"confidence 非法：{conf!r}（须 ∈ {CONFIDENCES}）")
    elif k == "modify":
        problems.append("kind=modify 缺 confidence")
    return problems


def parse_timestamp(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts))
    except ValueError:
        return None


def check(path: Path | str = DEFAULT_ANN, *,
          edges_path: Path | str = DEFAULT_EDGES) -> list[str]:
    """全通道合法性体检；返回带行号的问题列表（空 = 全绿）。"""
    problems: list[str] = []
    edge_ids = load_edge_ids(edges_path)
    try:
        anns = load_annotations(path)
    except ValueError as exc:
        return [str(exc)]
    for i, rec in enumerate(anns, 1):
        for p in validate_record(rec, edge_ids):
            problems.append(f"第 {i} 行：{p}")
    return problems


# ── 写入（只追加 + fail-closed）────────────────────────────────────────────────
def _now_iso() -> str:
    return datetime.now(TZ).replace(microsecond=0).isoformat()


def build_record(edge_id: str, kind: str, reason: str, *,
                 confidence: str | None = None) -> dict:
    rec = {"edge_id": str(edge_id), "kind": str(kind), "reviewer": REVIEWER,
           "timestamp": _now_iso(), "reason": str(reason).strip()}
    if confidence is not None:
        rec["confidence"] = str(confidence)
    return rec


def append_annotation(edge_id: str, kind: str, reason: str, *,
                      confidence: str | None = None,
                      path: Path | str = DEFAULT_ANN,
                      edges_path: Path | str = DEFAULT_EDGES) -> dict:
    """追加一条人审记录。任何校验不过 ⇒ `ValueError`，**一行都不写**。"""
    if str(reason or "").strip() == "":
        raise ValueError("缺 --reason：理由必填 ⇒ 拒绝写入")
    if len(str(reason).strip()) < MIN_REASON:
        raise ValueError(f"--reason 长度 {len(str(reason).strip())} < {MIN_REASON}"
                         f" ⇒ 拒绝写入（防 rubber-stamp，须说明判断依据）")
    if kind not in KINDS:
        raise ValueError(f"kind 须 ∈ {KINDS}，实得 {kind!r}")
    if kind == "modify" and confidence not in CONFIDENCES:
        raise ValueError(f"modify 须给 --confidence ∈ {CONFIDENCES}，实得 {confidence!r}")
    edge_ids = load_edge_ids(edges_path)
    if str(edge_id) not in edge_ids:
        raise ValueError(f"edge_id 不存在：{edge_id!r}（候选边共 {len(edge_ids)} 条）⇒ 拒绝写入")
    rec = build_record(edge_id, kind, reason, confidence=confidence)
    problems = validate_record(rec, edge_ids)
    if problems:
        raise ValueError("记录自检不过 ⇒ 拒绝写入：" + "；".join(problems))
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


# ── 输出 ──────────────────────────────────────────────────────────────────────
def _short(s: str, n: int = 40) -> str:
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def render_table(annotations: list[dict], limit: int | None = None) -> str:
    rows = list(annotations)
    if limit is not None:
        rows = rows[:limit]
    head = f"{'edge_id':<44} {'kind':<8} {'reviewer':<9} {'timestamp':<26} reason"
    lines = [head, "-" * len(head)]
    for a in rows:
        lines.append(f"{_short(str(a.get('edge_id', '')), 44):<44} "
                     f"{kind_of(a) or '?':<8} "
                     f"{str(a.get('reviewer', '?')):<9} "
                     f"{str(a.get('timestamp', '?')):<26} "
                     f"{_short(str(a.get('reason', '')))}")
    lines.append(f"（共 {len(rows)} 行 / 通道 {len(annotations)} 行）")
    return "\n".join(lines)


def list_rows(annotations: list[dict], *, status_filter: str | None = None,
              edges_path: Path | str = DEFAULT_EDGES) -> list[dict]:
    """按状态筛选：pending/approved/rejected/modified（无筛选 = 全部已审行）。"""
    last = latest_by_edge(annotations)
    if status_filter is None:
        return list(annotations)
    if status_filter == "pending":
        edge_ids = load_edge_ids(edges_path)
        done = set(last)
        return [{"edge_id": e, "kind": "pending", "reviewer": "-",
                 "timestamp": "-", "reason": "（未人审）"}
                for e in sorted(edge_ids - done)]
    return [a for a in annotations if status_of(str(a.get("edge_id")), last) == status_filter]


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="human_review_cli",
        description="609 A1 人审 CLI：approve/reject/modify/list/--check（append-only + fail-closed）")
    p.add_argument("--version", action="version", version=f"human_review_cli {VERSION}")
    p.add_argument("--annotations", default=str(DEFAULT_ANN), help="人审通道 JSONL 路径")
    p.add_argument("--edges", default=str(DEFAULT_EDGES), help="候选边 JSONL 路径")
    p.add_argument("--check", action="store_true", help="体检人审通道合法性（0 全合法 / 1 有非法行）")
    sub = p.add_subparsers(dest="cmd")

    for name in ("approve", "reject"):
        sp = sub.add_parser(name, help=f"{name} 一条候选边")
        sp.add_argument("edge_id")
        sp.add_argument("--reason", required=True)

    sp = sub.add_parser("modify", help="modify 一条候选边的可信度")
    sp.add_argument("edge_id")
    sp.add_argument("--confidence", required=True)
    sp.add_argument("--reason", required=True)

    sp = sub.add_parser("list", help="列出人审结果")
    sp.add_argument("--pending", dest="status", action="store_const", const="pending")
    sp.add_argument("--approved", dest="status", action="store_const", const="approved")
    sp.add_argument("--rejected", dest="status", action="store_const", const="rejected")
    sp.add_argument("--modified", dest="status", action="store_const", const="modified")
    sp.add_argument("--limit", type=int, default=None)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.check:
        problems = check(args.annotations, edges_path=args.edges)
        if problems:
            print(f"[human_review_cli] --check FAIL：人审通道 {args.annotations} "
                  f"共 {len(problems)} 处非法", file=sys.stderr)
            for msg in problems[:200]:
                print("  - " + msg, file=sys.stderr)
            return 1
        print(f"[human_review_cli] --check OK：人审通道 {args.annotations} "
              f"共 {len(load_annotations(args.annotations))} 行全部合法")
        return 0

    if args.cmd is None:
        build_parser().print_help()
        return 2

    if args.cmd == "list":
        rows = list_rows(load_annotations(args.annotations), status_filter=args.status,
                         edges_path=args.edges)
        print(render_table(rows, args.limit))
        return 0

    kind = args.cmd
    conf = getattr(args, "confidence", None)
    try:
        rec = append_annotation(args.edge_id, kind, args.reason, confidence=conf,
                                path=args.annotations, edges_path=args.edges)
    except ValueError as exc:
        print(f"[human_review_cli] 拒写：{exc}", file=sys.stderr)
        msg = str(exc)
        if "edge_id 不存在" in msg:
            return 1
        if "--reason 长度" in msg or "缺 --reason" in msg:
            return 2
        if "--confidence" in msg or "confidence" in msg:
            return 3
        return 1
    if kind == "modify":
        print(f"MODIFIED: {rec['edge_id']} -> {rec['confidence']}")
    else:
        print(f"{kind.upper()}D: {rec['edge_id']}"
              if kind != "reject" else f"REJECTED: {rec['edge_id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
