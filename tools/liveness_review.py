"""612 B2 · 活性锚人审确认工具（**只追加不修改** · 不直接改卡面）。

人审对 B1 的 50 条活性锚候选做确认，把决策**只追加**到 `data/liveness_review_612.jsonl`。
本工具**不直接修改**任何命题文件或卡面——实际填 `liveness` 字段由人审或后续批执行（苦力不碰受控目录）。

记录格式：`{proposition_id, action, symbol, reason, reviewer, timestamp}`
  * action ∈ {approve, reject, mark-inference}
  * reviewer 固定 `human`（不自动批准任何候选）

CLI：
  list [--class A|B|C] [--status pending|approved|rejected|inference]   列出候选及状态
  approve <proposition_id> --symbol <符号>      批准（选定符号）
  reject  <proposition_id> --reason "<原因>"    拒绝
  mark-inference <proposition_id> --reason "<原因>"   标记应改标 inference（C 类）
  batch   --from-file <file>                    批量执行，失败记录后继续
  stats / --check
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
CAND_IN = ROOT / "data" / "liveness_candidates_612.jsonl"
REVIEW_LOG = ROOT / "data" / "liveness_review_612.jsonl"
_ACTIONS = ("approve", "reject", "mark-inference")
_STATUS = {"approve": "approved", "reject": "rejected", "mark-inference": "inference"}


@lru_cache(maxsize=1)
def load_props() -> dict[str, dict]:
    """→ {proposition_id: {class, candidates:[{symbol,confidence}], card}}（**全部 50 条**，含无候选的 C 类）。

    C 类命题在 B1 的 jsonl 里**没有候选行**，故先用审计真源枚举全部缺锚命题（键=卡级复合键
    `卡::prop-N`），再用 B1 的候选 jsonl 覆盖 class/候选。
    """
    import proposition_liveness_audit as pla  # noqa: E402
    out: dict[str, dict] = {}
    for c in pla.audit()["cards"]:
        for e in c["missing"]:
            pid = f"{c['card']}::{e['id']}"
            out[pid] = {"class": "C", "card": c["card"], "candidates": []}
    if CAND_IN.is_file():
        for line in CAND_IN.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            p = out.setdefault(r["proposition_id"],
                               {"class": r.get("class", "C"), "card": r.get("card", ""),
                                "candidates": []})
            p["class"] = r.get("class", "C")
            p["candidates"].append({"symbol": r["symbol"], "confidence": r["confidence"]})
    return out


def load_reviews(path: Path | None = None) -> list[dict]:
    p = Path(path) if path else REVIEW_LOG
    if not p.is_file():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_record(rec: dict, path: Path | None = None) -> None:
    p = Path(path) if path else REVIEW_LOG
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def modify_record(*_a, **_k):  # noqa: ANN002, ANN003
    raise PermissionError("append-only：确认日志不可修改，只能追加新记录")


def _record(pid: str, action: str, symbol: str | None = None,
            reason: str = "", reviewer: str = "human") -> dict:
    return {"proposition_id": pid, "action": action, "symbol": symbol,
            "reason": reason, "reviewer": reviewer,
            "timestamp": datetime.now().isoformat(timespec="seconds")}


def _status_map(reviews: list[dict]) -> dict[str, str]:
    m: dict[str, str] = {}
    for r in reviews:
        m[r["proposition_id"]] = _STATUS.get(r.get("action"), "pending")
    return m


def do_approve(pid: str, symbol: str) -> dict:
    props = load_props()
    if pid not in props:
        raise SystemExit(f"[B2] ❌ 命题无活性锚候选：{pid}")
    if not symbol.strip():
        raise SystemExit("[B2] ❌ approve 必须给出 --symbol")
    append_record(_record(pid, "approve", symbol))
    return _record(pid, "approve", symbol)


def do_reject(pid: str, reason: str) -> dict:
    props = load_props()
    if pid not in props:
        raise SystemExit(f"[B2] ❌ 命题无活性锚候选：{pid}")
    if not reason.strip():
        raise SystemExit("[B2] ❌ reject 必须给出 --reason")
    append_record(_record(pid, "reject", None, reason))
    return _record(pid, "reject", None, reason)


def do_mark_inference(pid: str, reason: str) -> dict:
    props = load_props()
    if pid not in props:
        raise SystemExit(f"[B2] ❌ 命题无活性锚候选：{pid}")
    if not reason.strip():
        raise SystemExit("[B2] ❌ mark-inference 必须给出 --reason")
    append_record(_record(pid, "mark-inference", None, reason))
    return _record(pid, "mark-inference", None, reason)


def do_batch(path: Path) -> list[str]:
    errors: list[str] = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=2)
        try:
            op = parts[0]
            if op == "approve":
                do_approve(parts[1], parts[2])
            elif op in ("reject", "mark-inference"):
                (do_reject if op == "reject" else do_mark_inference)(parts[1], parts[2])
            else:
                errors.append(f"line {i}: 未知操作 {op!r}")
        except (IndexError, SystemExit) as exc:
            errors.append(f"line {i}: {exc}")
    return errors


def stats() -> dict:
    props = load_props()
    st = _status_map(load_reviews())
    counts = {"approved": 0, "rejected": 0, "inference": 0, "pending": 0}
    for pid in props:
        counts[st.get(pid, "pending")] = counts.get(st.get(pid, "pending"), 0) + 1
    return {"total_props": len(props), "records": len(load_reviews()),
            "by_status": counts, "reviewers": sorted({r.get("reviewer", "")
                                                       for r in load_reviews()})}


def check() -> list[str]:
    problems: list[str] = []
    props = set(load_props())
    for r in load_reviews():
        if r.get("proposition_id") not in props:
            problems.append(f"确认记录引用了无候选的命题：{r.get('proposition_id')}")
        if r.get("action") not in _ACTIONS:
            problems.append(f"非法 action：{r.get('action')}")
        if r.get("action") == "approve" and not str(r.get("symbol") or "").strip():
            problems.append(f"approve 记录缺 symbol：{r.get('proposition_id')}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="liveness_review", description="612 B2 活性锚人审确认（append-only）")
    ap.add_argument("--version", action="version", version=f"liveness_review {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p_list = sub.add_parser("list")
    p_list.add_argument("--class", dest="cls", choices=["A", "B", "C"], default=None)
    p_list.add_argument("--status", choices=["pending", "approved", "rejected", "inference"], default=None)
    p_app = sub.add_parser("approve")
    p_app.add_argument("proposition_id")
    p_app.add_argument("--symbol", required=True)
    p_rej = sub.add_parser("reject")
    p_rej.add_argument("proposition_id")
    p_rej.add_argument("--reason", required=True)
    p_mi = sub.add_parser("mark-inference")
    p_mi.add_argument("proposition_id")
    p_mi.add_argument("--reason", required=True)
    p_b = sub.add_parser("batch")
    p_b.add_argument("--from-file", required=True)
    sub.add_parser("stats")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[B2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[B2] ✓ 确认日志与候选数据一致（{stats()['records']} 条记录）")
        return 0
    if a.cmd == "list":
        props = load_props()
        st = _status_map(load_reviews())
        n = 0
        for pid, p in props.items():
            s = st.get(pid, "pending")
            if a.cls and p["class"] != a.cls:
                continue
            if a.status and s != a.status:
                continue
            syms = ", ".join(c["symbol"] for c in p["candidates"][:3]) or "—"
            print(f"{s:10s} {p['class']}  {pid}  [{syms}]")
            n += 1
        print(f"[B2] 共 {n} 条")
        return 0
    if a.cmd == "approve":
        print(f"[B2] ✓ approve {a.proposition_id} ⇒ {a.symbol}")
        do_approve(a.proposition_id, a.symbol)
        return 0
    if a.cmd == "reject":
        do_reject(a.proposition_id, a.reason)
        print(f"[B2] ✓ reject {a.proposition_id}")
        return 0
    if a.cmd == "mark-inference":
        do_mark_inference(a.proposition_id, a.reason)
        print(f"[B2] ✓ mark-inference {a.proposition_id}")
        return 0
    if a.cmd == "batch":
        errors = do_batch(Path(a.from_file))
        for e in errors:
            print(f"[B2] ⚠ {e}", file=sys.stderr)
        print(f"[B2] batch 完成，错误 {len(errors)} 条")
        return 0 if not errors else 1
    if a.cmd == "stats":
        print(json.dumps(stats(), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
