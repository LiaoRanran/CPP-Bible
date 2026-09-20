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
# mypy: ignore-errors
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
REVIEWER = "human"                     # 本工具写出的 reviewer 字面量
MIN_REASON = 20
REQUIRED = ("edge_id", "kind", "reviewer", "timestamp", "reason")
#: 611 A2：新增可选 `review_seconds`（耗时，秒）。
#: **存量 388 条不含该字段 ⇒ 一律 null/缺失，不回填**（`measured=false`，见 human_review_report）。
#: 为什么是可选而非必填：① 存量没有；② `review_seconds` 为 0（秒级）也可能是真值，
#: 用"缺字段"表示"未测量"最诚实；③ 不因缺它而拒绝一条人审（人审权力优先于度量完备）。
OPTIONAL = ("confidence", "review_seconds", "review_seconds_source")
#: 本工具承认的计时来源（写进记录，供质量报告区分"自报"与"会话计时"）
TIMING_SOURCES = ("explicit", "session")
#: 单条人审耗时上限（秒）：1 小时。超了大概率是单位写错（毫秒当秒）⇒ 不静默收下
MAX_REVIEW_SECONDS = 3600.0
#: 596 `attack_edge_review.py` 的历史写法（同人审通道上的**并存 schema**）：
#:   `action` 顶替 `kind`、`new_confidence` 顶替 `confidence`、reviewer 写真实 git 署名。
#: 609 读侧一律与之互认（"同一条通道两套笔迹"是既成事实，不是错误）。
LEGACY_ALIASES = ("action", "new_confidence")
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
def human_identities() -> set[str]:
    """被承认的"真人"署名集合 = 字面量 `human` ∪ 当前 git user.name。

    **`action` 版记录**（596 的 `attack_edge_review.py`）写的是**真实 git 署名**，
    它和 609 的字面量 `human` 是同一个通道上的两套笔迹 ⇒ 一并承认；
    这条口子**只认 git 能证明的人**，机器写不出 git 身份 ⇒ 防冒名的目的不打折。
    """
    out = {REVIEWER}
    who = aer.git_user_name()
    if who:
        out.add(who)
    return out


def validate_record(rec: dict, edge_ids: set[str]) -> list[str]:
    """返回问题列表（空 = 合法）。逐字段校验，一次报全部问题（便于人一次修完）。"""
    problems: list[str] = []
    if not kind_of(rec):
        problems.append("缺 kind（或 596 的 action）")
    for k in ("edge_id", "reviewer", "timestamp", "reason"):
        if not str(rec.get(k) or "").strip():
            problems.append(f"缺字符段 {k}")
    unknown = set(rec) - set(REQUIRED) - set(OPTIONAL) - set(LEGACY_ALIASES)
    if unknown:
        problems.append(f"含未知字段 {sorted(unknown)}")
    k = kind_of(rec)
    if k and k not in KINDS:
        problems.append(f"kind 非法：{k!r}（须 ∈ {KINDS}）")
    rv = str(rec.get("reviewer") or "")
    if rv and rv not in human_identities():
        problems.append(f"reviewer 不是可证明的真人身份（须 = {sorted(human_identities())}）：{rv!r}")
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
    conf = rec.get("confidence", rec.get("new_confidence"))   # 兼容 596 的 new_confidence
    if conf is not None:
        if conf not in CONFIDENCES:
            problems.append(f"confidence 非法：{conf!r}（须 ∈ {CONFIDENCES}）")
    elif k == "modify":
        problems.append("kind=modify 缺 confidence（或 596 的 new_confidence）")
    # 611 A2：review_seconds（可选）必须是非负有限数；给了就必须可信（不许负数/NaN/字符串）
    if "review_seconds" in rec:
        rs = rec.get("review_seconds")
        if isinstance(rs, bool) or not isinstance(rs, (int, float)):
            problems.append(f"review_seconds 必须是数字：{rs!r}")
        elif rs != rs or rs in (float("inf"), float("-inf")):
            problems.append(f"review_seconds 必须是有限数：{rs!r}")
        elif rs < 0:
            problems.append(f"review_seconds 不得为负：{rs!r}")
        elif rs > MAX_REVIEW_SECONDS:
            problems.append(f"review_seconds {rs} > 上限 {MAX_REVIEW_SECONDS}s"
                            f" ⇒ 疑似计时单位写错（毫秒当秒？）")
    if "review_seconds_source" in rec and rec.get("review_seconds_source") not in TIMING_SOURCES:
        problems.append(f"review_seconds_source 非法：{rec.get('review_seconds_source')!r}"
                        f"（须 ∈ {TIMING_SOURCES}）")
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


def seconds_since(began_at: str | None, *, now: str | None = None) -> float | None:
    """611 A2：`--began-at` 到现在的秒数（**用记录里的 timestamp 口径算**，不另起时钟）。

    `began_at` 非法/缺 ⇒ None（**不猜**：算不出就说算不出）。
    """
    if not began_at:
        return None
    t0 = parse_timestamp(str(began_at))
    t1 = parse_timestamp(str(now)) if now else datetime.now(TZ)
    if t0 is None or t1 is None:
        return None
    dt = (t1 - t0).total_seconds()
    return round(dt, 1) if dt >= 0 else None


def build_record(edge_id: str, kind: str, reason: str, *,
                 confidence: str | None = None,
                 review_seconds: float | None = None,
                 timing_source: str | None = None) -> dict:
    rec = {"edge_id": str(edge_id), "kind": str(kind), "reviewer": REVIEWER,
           "timestamp": _now_iso(), "reason": str(reason).strip()}
    if confidence is not None:
        rec["confidence"] = str(confidence)
    if review_seconds is not None:
        rec["review_seconds"] = float(review_seconds)
        rec["review_seconds_source"] = str(timing_source or "explicit")
    return rec


def append_annotation(edge_id: str, kind: str, reason: str, *,
                      confidence: str | None = None,
                      review_seconds: float | None = None,
                      timing_source: str | None = None,
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
    if review_seconds is not None and (review_seconds < 0 or review_seconds > MAX_REVIEW_SECONDS):
        raise ValueError(f"--review-seconds 须 ∈ [0, {MAX_REVIEW_SECONDS}]，实得 {review_seconds!r}")
    if timing_source is not None and timing_source not in TIMING_SOURCES:
        raise ValueError(f"--timing-source 须 ∈ {TIMING_SOURCES}，实得 {timing_source!r}")
    edge_ids = load_edge_ids(edges_path)
    if str(edge_id) not in edge_ids:
        raise ValueError(f"edge_id 不存在：{edge_id!r}（候选边共 {len(edge_ids)} 条）⇒ 拒绝写入")
    rec = build_record(edge_id, kind, reason, confidence=confidence,
                       review_seconds=review_seconds, timing_source=timing_source)
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

    def _add_timing(sp: argparse.ArgumentParser) -> None:
        """611 A2：两条计时路 —— 显式秒数（外部实测）或会话起点（本工具可证）。"""
        sp.add_argument("--review-seconds", type=float, default=None,
                        help="本条人审耗时（秒，外部实测值）；与 --began-at 二选一")
        sp.add_argument("--began-at", default=None,
                        help="开始复核的时刻（ISO 8601）⇒ 耗时 = 现在 - 该时刻（session 计法）")
        sp.add_argument("--timing-source", choices=TIMING_SOURCES, default=None,
                        help="计时来源标注（默认按用法自动：--began-at ⇒ session，否则 explicit）")

    for name in ("approve", "reject"):
        sp = sub.add_parser(name, help=f"{name} 一条候选边")
        sp.add_argument("edge_id")
        sp.add_argument("--reason", required=True)
        _add_timing(sp)

    sp = sub.add_parser("modify", help="modify 一条候选边的可信度")
    sp.add_argument("edge_id")
    sp.add_argument("--confidence", required=True)
    sp.add_argument("--reason", required=True)
    _add_timing(sp)

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
    # 611 A2：计时（显式优先；否则用 --began-at 算；都没有 ⇒ 不写 review_seconds，不猜）
    rs = getattr(args, "review_seconds", None)
    src = getattr(args, "timing_source", None)
    if rs is None:
        rs = seconds_since(getattr(args, "began_at", None))
        if rs is not None:
            src = src or "session"
    elif src is None:
        src = "explicit"
    try:
        rec = append_annotation(args.edge_id, kind, args.reason, confidence=conf,
                                review_seconds=rs, timing_source=src,
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
