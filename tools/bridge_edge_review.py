"""612 A2 · 桥接边人审执行工具（**只追加不修改** · 不直接改攻击边数据）。

人审对 611 C2 的 98 条桥接候选做决策，把决策**只追加**到 `data/bridge_edge_review_612.jsonl`
（append-only 决策日志）。本工具**不直接修改** `data/attack_edges_609.json` 或任何攻击边数据——
实际加边/置信度变更由 `weighted_af_solver.py` 在 what-if 重算时读取本日志后应用（见 A3）。

记录格式：`{id, action, confidence, reason, reviewer, timestamp}`
  * action ∈ {approve, reject, modify}
  * reviewer 固定 `human`（不自动批准任何候选）

CLI：
  list [--status pending|approved|rejected]   列出候选及当前决策状态
  approve <id> [--confidence medium|high]     批准（升置信度）⇒ 追加一条 approve
  reject  <id> --reason "<原因>"              拒绝 ⇒ 追加一条 reject
  batch   --from-file <file>                  批量执行（每行 `approve ID [conf]` / `reject ID reason`），失败记录后继续
  stats                                       审批进度
  --check                                     验证日志与候选数据一致（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
CAND_IN = ROOT / "data" / "bridge_edge_candidates_611.jsonl"
REVIEW_LOG = ROOT / "data" / "bridge_edge_review_612.jsonl"
_ACTIONS = ("approve", "reject", "modify")


def load_candidate_ids() -> list[str]:
    return [json.loads(line)["edge_id"]
            for line in CAND_IN.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_reviews(path: Path | None = None) -> list[dict]:
    p = Path(path) if path else REVIEW_LOG
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def append_record(rec: dict, path: Path | None = None) -> None:
    """追加一条决策记录（**只以 append 模式打开**）。"""
    p = Path(path) if path else REVIEW_LOG
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def modify_record(*_a, **_k):  # noqa: ANN002, ANN003
    """显式禁止修改已有记录（append-only 纪律的守卫）。"""
    raise PermissionError("append-only：决策日志不可修改，只能追加新记录")


def _record(cid: str, action: str, confidence: str | None = None,
            reason: str = "", reviewer: str = "human") -> dict:
    return {"id": cid, "action": action, "confidence": confidence,
            "reason": reason, "reviewer": reviewer,
            "timestamp": datetime.now().isoformat(timespec="seconds")}


def _status_map(reviews: list[dict]) -> dict[str, str]:
    """id → 最新决策（后写覆盖先写，仅用于展示/统计，不改日志）。"""
    m: dict[str, str] = {}
    for r in reviews:
        if r.get("action") in ("approve", "modify"):
            m[r["id"]] = "approved"
        elif r.get("action") == "reject":
            m[r["id"]] = "rejected"
    return m


def do_approve(cid: str, confidence: str = "medium", reason: str = "") -> dict:
    ids = load_candidate_ids()
    if cid not in ids:
        raise SystemExit(f"[A2] ❌ 候选不存在：{cid}")
    if confidence not in ("medium", "high"):
        raise SystemExit(f"[A2] ❌ confidence 只能是 medium/high：{confidence}")
    rec = _record(cid, "approve", confidence, reason)
    append_record(rec)
    return rec


def do_reject(cid: str, reason: str) -> dict:
    ids = load_candidate_ids()
    if cid not in ids:
        raise SystemExit(f"[A2] ❌ 候选不存在：{cid}")
    if not reason.strip():
        raise SystemExit("[A2] ❌ reject 必须给出 --reason")
    rec = _record(cid, "reject", None, reason)
    append_record(rec)
    return rec


def do_batch(path: Path) -> list[str]:
    """批量执行；单条失败记录错误后**继续**后续。返回错误列表。"""
    errors: list[str] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        try:
            op = parts[0]
            if op == "approve":
                do_approve(parts[1], parts[2] if len(parts) > 2 else "medium")
            elif op == "reject":
                do_reject(parts[1], " ".join(parts[2:]))
            else:
                errors.append(f"line {i}: 未知操作 {op!r}")
        except (IndexError, SystemExit) as exc:
            errors.append(f"line {i}: {exc}")
    return errors


def stats() -> dict:
    ids = load_candidate_ids()
    reviews = load_reviews()
    st = _status_map(reviews)
    approved = sum(1 for v in st.values() if v == "approved")
    rejected = sum(1 for v in st.values() if v == "rejected")
    return {"total_candidates": len(ids), "records": len(reviews),
            "approved": approved, "rejected": rejected,
            "pending": len(ids) - approved - rejected,
            "reviewers": sorted({r.get("reviewer", "") for r in reviews})}


def check() -> list[str]:
    problems: list[str] = []
    ids = set(load_candidate_ids())
    for r in load_reviews():
        if r.get("id") not in ids:
            problems.append(f"决策记录引用了不存在的候选：{r.get('id')}")
        if r.get("action") not in _ACTIONS:
            problems.append(f"非法 action：{r.get('action')}")
        if r.get("action") == "approve" and r.get("confidence") not in ("medium", "high"):
            problems.append(f"approve 记录 confidence 非法：{r.get('confidence')}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bridge_edge_review", description="612 A2 桥接人审执行（append-only）")
    ap.add_argument("--version", action="version", version=f"bridge_edge_review {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p_list = sub.add_parser("list")
    p_list.add_argument("--status", choices=["pending", "approved", "rejected"], default=None)
    p_app = sub.add_parser("approve")
    p_app.add_argument("candidate_id")
    p_app.add_argument("--confidence", default="medium")
    p_rej = sub.add_parser("reject")
    p_rej.add_argument("candidate_id")
    p_rej.add_argument("--reason", required=True)
    p_batch = sub.add_parser("batch")
    p_batch.add_argument("--from-file", required=True)
    sub.add_parser("stats")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[A2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[A2] ✓ 决策日志与候选数据一致（{stats()['records']} 条记录）")
        return 0
    if a.cmd == "list":
        st = _status_map(load_reviews())
        for cid in load_candidate_ids():
            s = st.get(cid, "pending")
            if a.status and s != a.status:
                continue
            print(f"{s:9s} {cid}")
        return 0
    if a.cmd == "approve":
        rec = do_approve(a.candidate_id, a.confidence)
        print(f"[A2] ✓ approve {rec['id']} ⇒ {rec['confidence']}")
        return 0
    if a.cmd == "reject":
        rec = do_reject(a.candidate_id, a.reason)
        print(f"[A2] ✓ reject {rec['id']}")
        return 0
    if a.cmd == "batch":
        errors = do_batch(Path(a.from_file))
        for e in errors:
            print(f"[A2] ⚠ {e}", file=sys.stderr)
        print(f"[A2] batch 完成，错误 {len(errors)} 条")
        return 0 if not errors else 1
    if a.cmd == "stats":
        print(json.dumps(stats(), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
