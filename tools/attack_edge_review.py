#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attack_edge_review.py — 候选攻击边的**人审确认接口**（596 任务4；最小版本）。

为什么：候选攻击边是**机器推导**的（误区库 `related_atoms` → 命题），机器只保证"这两个对象被
书面关联过"，不保证"这条误解**确实**攻击这条命题"。W2 的判决完全建立在这张攻击图上，所以每一条
边都必须能被人**逐条接受/拒绝/改权**，并且这套动作要**可追溯、不可抵赖**（只追加 + git 作者绑定）。

硬不变量（与 573 推翻通道同款）：
  * **系统绝不自动 approve/reject** —— 本模块只提供写入接口，实际动作只能由人执行；
  * **fail-closed**：缺 `--reason` / `edge_id` 不存在 / git 不可用 / 审查人不是该边的
    误解卡（`misconceptions/MIS-*.md`）最后一次 git 提交作者 ⇒ **拒绝写入且不落行**；
  * **只追加**：`data/human_attack_edge_annotations.jsonl` 永不覆盖、永不删除 —— 同一条边审查两次
    就是两条历史（可追溯"改主意"），生效值取**最后一条**。

对人审结果的用法（W2 求解器 `--include-human-reviewed`，默认开启）：
  * `approve` ⇒ 可信度**升一级**（low→medium / medium→high / high→high）；
  * `reject`  ⇒ 该边**从求解输入中排除**（注意：只排除这一条；对称边要另审）；
  * `modify`  ⇒ 直接采用人审指定的可信度。

用法：
    python tools/attack_edge_review.py list [--status pending|approved|rejected|modified]
    python tools/attack_edge_review.py show <edge_id>
    python tools/attack_edge_review.py approve <edge_id> --reason "..."
    python tools/attack_edge_review.py reject  <edge_id> --reason "..."
    python tools/attack_edge_review.py modify  <edge_id> --confidence high|medium|low --reason "..."
    python tools/attack_edge_review.py stats
    python tools/attack_edge_review.py --check      # 标注文件 + 候选边一致性校验（失败 exit 2）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import gate_engine as ge  # noqa: E402

VERSION = "1.0"
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_ANN = ROOT / "data" / "human_attack_edge_annotations.jsonl"
DEFAULT_MIS_DIR = aeg.DEFAULT_MIS_DIR
ACTIONS = ("approve", "reject", "modify")
REQUIRED = ("edge_id", "action", "reason", "reviewer", "timestamp")
PROMOTE = {"low": "medium", "medium": "high", "high": "high"}
STATUSES = ("pending", "approved", "rejected", "modified")


# ── 读盘面 ─────────────────────────────────────────────────────────────────────
def load_edges(path: Path | str = DEFAULT_EDGES) -> list[dict]:
    return aeg.load_edges(path)


def load_annotations(path: Path | str = DEFAULT_ANN) -> list[dict]:
    """读人审标注（只追加事件流）。文件缺失 ⇒ `[]`（"没审过"与"审了 0 条"由文件是否存在区分）。"""
    p = Path(path)
    if not p.is_file():
        return []
    out: list[dict] = []
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        s = ln.strip()
        if not s:
            continue
        try:
            out.append(json.loads(s))
        except ValueError as exc:
            raise ValueError(f"{p} 第 {i} 行不是合法 JSON：{exc}") from exc
    return out


def git_user_name() -> str | None:
    """当前审查人 = `git config user.name`（拿不到 ⇒ None ⇒ fail-closed 拒写）。"""
    try:
        p = subprocess.run(["git", "config", "user.name"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    name = (p.stdout or "").strip()
    return name or None


def resolve_mis_card(edge: dict, mis_dir: Path | str = DEFAULT_MIS_DIR) -> Path | None:
    """一条边涉及的误解卡：source 或 target 里那个 MIS id（找不到 ⇒ None ⇒ 拒写）。"""
    for cand in (str(edge.get("source", "")), str(edge.get("target", ""))):
        if cand in aeg.read_mis(mis_dir):
            for f in sorted(Path(mis_dir).rglob(f"{cand}.md")):
                return f
    return None


# ── 写入（fail-closed，只追加）──────────────────────────────────────────────────
def append_annotation(edge_id: str, action: str, reason: str, *,
                      new_confidence: str | None = None,
                      reviewer: str | None = None,
                      path: Path | str = DEFAULT_ANN,
                      edges_path: Path | str = DEFAULT_EDGES,
                      mis_dir: Path | str = DEFAULT_MIS_DIR) -> dict:
    """追加一条人审记录；任何校验不过 ⇒ `ValueError`，**一行都不写**。

    校验顺序（与 573 同风格，便于错误文案对齐）：
      缺理由 → 动作非法 → edge_id 不存在 → 审查人取不到/冒名 → git 不可用 → 与卡作者不符。
    """
    if not str(reason or "").strip():
        raise ValueError("缺 --reason：理由必填（拒绝 rubber-stamp）⇒ 拒绝写入")
    if action not in ACTIONS:
        raise ValueError(f"action 须为 {ACTIONS} 之一，实得 {action!r}")
    if action == "modify" and new_confidence not in aeg.CONFIDENCE_WEIGHT:
        raise ValueError(f"modify 须给 --confidence ∈ {tuple(aeg.CONFIDENCE_WEIGHT)}"
                         f"，实得 {new_confidence!r}")
    by_id = {str(e["id"]): e for e in load_edges(edges_path)}
    edge = by_id.get(str(edge_id))
    if edge is None:
        raise ValueError(f"edge_id 不存在：{edge_id!r}（候选边共 {len(by_id)} 条）⇒ 拒绝写入")
    cfg = git_user_name()
    if cfg is None:
        raise ValueError("git 不可用（取不到 user.name）⇒ 无法核验审查人，拒绝写入（fail-closed）")
    who = str(reviewer or cfg).strip()
    if who != cfg:
        raise ValueError(f"审查人名 {who!r} 与当前 git 作者 {cfg!r} 不符 ⇒ 不许冒名，拒绝写入")
    mis_card = resolve_mis_card(edge, mis_dir)
    if mis_card is None:
        raise ValueError(f"边 {edge_id!r} 的误解卡解析不到 ⇒ 无法核验签署，拒绝写入（fail-closed）")
    author = ge._git_author_for(mis_card)
    if author is None:
        raise ValueError(f"git 不可用 ⇒ 无法核验审查人 {who!r} 对该误解卡的签署，拒绝写入")
    if not ge._author_matches(who, author):
        raise ValueError(f"审查人 {who!r} 不是该误解卡（{mis_card.name}）最后一次 git 提交的作者"
                         f"（{author[0]}）⇒ 无签名，拒绝写入")
    rec = {"edge_id": str(edge_id), "action": action, "reason": str(reason).strip(),
           "reviewer": who, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if action == "modify":
        rec["new_confidence"] = str(new_confidence)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


# ── 生效规则（W2 求解器消费）───────────────────────────────────────────────────
def latest_by_edge(annotations: list[dict]) -> dict[str, dict]:
    """同一条边多次审查 ⇒ 取**最后一条**（历史仍留在文件里，可追溯）。"""
    last: dict[str, dict] = {}
    for a in annotations:
        last[str(a.get("edge_id"))] = a
    return last


def status_of(edge_id: str, last: dict[str, dict]) -> str:
    a = last.get(edge_id)
    if a is None:
        return "pending"
    return {"approve": "approved", "reject": "rejected", "modify": "modified"}[a["action"]]


def effective_edges(edges: list[dict], annotations: list[dict]) -> list[dict]:
    """按人审结果生成**生效边**：reject 剔除；approve 升一级；modify 用指定档。"""
    last = latest_by_edge(annotations)
    out: list[dict] = []
    for e in edges:
        a = last.get(str(e["id"]))
        if a is None:
            out.append(e)
            continue
        if a["action"] == "reject":
            continue
        ne = dict(e)
        ne["confidence"] = (PROMOTE[str(e.get("confidence"))] if a["action"] == "approve"
                            else str(a.get("new_confidence")))
        ne["human_reviewed"] = a["action"]
        out.append(ne)
    return out


def stats(edges: list[dict], annotations: list[dict]) -> dict:
    last = latest_by_edge(annotations)
    counts = dict.fromkeys(STATUSES, 0)
    for e in edges:
        counts[status_of(str(e["id"]), last)] += 1
    done = len(edges) - counts["pending"]
    return {"total": len(edges), **counts, "annotations": len(annotations),
            "annotated_edges": done,
            "approve_rate": round(counts["approved"] / done, 3) if done else None,
            "reject_rate": round(counts["rejected"] / done, 3) if done else None,
            "pending_rate": round(counts["pending"] / len(edges), 3) if edges else None}


def check(edges: list[dict], annotations: list[dict]) -> list[str]:
    problems: list[str] = []
    ids = {str(e["id"]) for e in edges}
    for i, a in enumerate(annotations, 1):
        miss = [k for k in REQUIRED if not str(a.get(k) or "").strip()]
        if miss:
            problems.append(f"第 {i} 条缺字段 {miss}")
            continue
        if a["action"] not in ACTIONS:
            problems.append(f"第 {i} 条 action 非法：{a['action']}")
        if a["edge_id"] not in ids:
            problems.append(f"第 {i} 条 edge_id 不在候选边里：{a['edge_id']}")
        if a["action"] == "modify" and a.get("new_confidence") not in aeg.CONFIDENCE_WEIGHT:
            problems.append(f"第 {i} 条 modify 缺/错 new_confidence：{a.get('new_confidence')!r}")
        if set(a) - set(REQUIRED) - {"new_confidence"}:
            problems.append(f"第 {i} 条含未知字段 {sorted(set(a) - set(REQUIRED) - {'new_confidence'})}")
    return problems


# ── 群组级人审 + automation bias + 反馈闭环（604 任务1-3）────────────────────
DEFAULT_AUDIT = ROOT / "data" / "human_review_audit.json"


def mis_groups(edges: list[dict], mis_dir: Path | str = DEFAULT_MIS_DIR) -> list[dict]:
    """42 个 MIS 群组：歧义度 = 关联卡数 × 每卡命题数总体标准差。"""
    import statistics as _stat
    mis = aeg.read_mis(mis_dir)
    ap = aeg.atom_props()
    groups: list[dict] = []
    for mid, m in sorted(mis.items()):
        if not m["related_atoms"]:
            continue
        cards = m["related_atoms"]
        ppc = [len(ap.get(c, [])) for c in cards]
        std = _stat.pstdev(ppc) if len(ppc) > 1 else 0.0
        mis_edges = [e for e in edges if mid in (e.get("source", ""), e.get("target", ""))]
        groups.append({
            "mis_id": mid, "n_cards": len(cards), "cards": cards,
            "n_props": sum(ppc), "std": round(std, 2),
            "ambiguity": round(len(cards) * std, 2),
            "n_edges": len(mis_edges), "edge_ids": [e["id"] for e in mis_edges],
            "refutations": len(m["refutations"]),
        })
    groups.sort(key=lambda g: g["ambiguity"], reverse=True)
    return groups


def approve_group(mis_id: str, prop_ids: list[str], reason: str, *,
                   reviewer: str | None = None,
                   annotations_path: Path | str = DEFAULT_ANN,
                   edges_path: Path | str = DEFAULT_EDGES,
                   mis_dir: Path | str = DEFAULT_MIS_DIR) -> list[dict]:
    """群组级 approve：选了命题后自动 approve 对应 MIS→命题边 + 对称边。"""
    by_id = {str(e["id"]): e for e in load_edges(edges_path)}
    target_ids = set()
    for e in by_id.values():
        if mis_id not in (e.get("source", ""), e.get("target", "")):
            continue
        other = e["target"] if e["source"] == mis_id else e["source"]
        if other in prop_ids:
            target_ids.add(str(e["id"]))
    recs: list[dict] = []
    for eid in sorted(target_ids):
        recs.append(append_annotation(eid, "approve", reason, reviewer=reviewer,
                                       path=annotations_path, edges_path=edges_path, mis_dir=mis_dir))
    return recs


def load_audit(path: Path | str = DEFAULT_AUDIT) -> dict:
    p = Path(path)
    if not p.is_file():
        return {"total_reviews": 0, "approve_count": 0, "reject_count": 0,
                "skip_count": 0, "suspicious_count": 0, "trap_correct": 0,
                "trap_total": 0, "avg_review_seconds": 0.0, "alerts": [],
                "review_seconds": [], "reason_lengths": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save_audit(audit: dict, path: Path | str = DEFAULT_AUDIT) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(audit, ensure_ascii=False, indent=1), encoding="utf-8")


def record_review(audit: dict, action: str, reason: str, review_seconds: float,
                   *, is_trap: bool = False, trap_correct: bool | None = None) -> list[str]:
    """记录一次人审并做 automation bias 检测。返回告警列表。"""
    audit["total_reviews"] += 1
    audit["review_seconds"].append(round(review_seconds, 1))
    audit["reason_lengths"].append(len(str(reason or "").strip()))
    if action == "approve":
        audit["approve_count"] += 1
    elif action == "reject":
        audit["reject_count"] += 1
    elif action == "skip":
        audit["skip_count"] += 1
    alerts: list[str] = []
    if len(str(reason or "").strip()) < 10 or review_seconds < 5:
        audit["suspicious_count"] += 1
        alerts.append(f"suspicious: reason={len(str(reason or '').strip())}ch/{review_seconds:.1f}s")
    if audit["total_reviews"] >= 10 and audit["approve_count"] / audit["total_reviews"] > 0.9:
        alerts.append("agree_rate>90%: rubber-stamp pattern detected")
    if is_trap:
        audit["trap_total"] += 1
        if trap_correct:
            audit["trap_correct"] += 1
        else:
            alerts.append("TRAP QUESTION ANSWERED WRONG")
    audit["avg_review_seconds"] = round(sum(audit["review_seconds"]) / len(audit["review_seconds"]), 1)
    audit["alerts"].extend(alerts)
    audit["alerts"] = audit["alerts"][-50:]
    return alerts


def progress_summary(edges: list[dict], annotations: list[dict], groups: list[dict]) -> dict:
    last = latest_by_edge(annotations)
    done_edges = sum(1 for e in edges if status_of(str(e["id"]), last) != "pending")
    done_groups = sum(1 for g in groups
                       if not any(status_of(str(eid), last) == "pending" for eid in g["edge_ids"]))
    return {
        "total_groups": len(groups), "done_groups": done_groups,
        "pending_groups": len(groups) - done_groups,
        "total_edges": len(edges), "done_edges": done_edges,
        "pending_edges": len(edges) - done_edges,
        "est_remaining_minutes": round((len(groups) - done_groups) * 35 / 60, 1),
        "completion_pct": round(done_groups / len(groups) * 100, 1) if groups else 0,
    }


def feedback_summary(annotations: list[dict]) -> dict:
    rejects = [a for a in annotations if a["action"] == "reject"]
    return {
        "total_annotations": len(annotations),
        "reject_count": len(rejects),
        "reject_reasons": [r["reason"][:80] for r in rejects[:10]],
        "suggestions": [
            "reject-heavy MIS: check if related_atoms is too broad",
            "skip with 'ambiguous': needs more proposition-level anchors",
            "approve reason patterns: optimize next round candidate priority",
        ],
    }


# ── CLI ────────────────────────────────────────────────────────────────────────
def _short(s: str, n: int = 60) -> str:
    return s if len(s) <= n else s[:n] + "…"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="候选攻击边人审接口（只追加 + fail-closed）")
    ap.add_argument("--check", action="store_true", help="标注文件格式校验（失败 exit 2）")
    ap.add_argument("--edges", default=str(DEFAULT_EDGES))
    ap.add_argument("--annotations", default=str(DEFAULT_ANN))
    ap.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    sub = ap.add_subparsers(dest="cmd")
    for name in ("list", "stats"):
        sp = sub.add_parser(name)
        sp.add_argument("--edges", default=str(DEFAULT_EDGES))
        sp.add_argument("--annotations", default=str(DEFAULT_ANN))
        sp.add_argument("--json", action="store_true")
        if name == "list":
            sp.add_argument("--status", choices=STATUSES)
    sh = sub.add_parser("show")
    sh.add_argument("edge_id")
    sh.add_argument("--edges", default=str(DEFAULT_EDGES))
    sh.add_argument("--annotations", default=str(DEFAULT_ANN))
    sh.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    for name in ("approve", "reject", "modify"):
        sp = sub.add_parser(name)
        sp.add_argument("edge_id")
        sp.add_argument("--reason", default="")
        sp.add_argument("--reviewer", default=None)
        sp.add_argument("--edges", default=str(DEFAULT_EDGES))
        sp.add_argument("--annotations", default=str(DEFAULT_ANN))
        sp.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
        if name == "modify":
            sp.add_argument("--confidence", required=True,
                            choices=sorted(aeg.CONFIDENCE_WEIGHT))
    # 604 新命令
    q_sp = sub.add_parser("queue", help="MIS 群组级队列（按歧义度降序）")
    q_sp.add_argument("--sort", choices=["ambiguity", "confidence", "impact"], default="ambiguity")
    q_sp.add_argument("--json", action="store_true")
    q_sp.add_argument("--edges", default=str(DEFAULT_EDGES))
    q_sp.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    rg = sub.add_parser("review-group", help="群组级审核（选命题→自动 approve 对应边）")
    rg.add_argument("mis_id")
    rg.add_argument("--props", default="", help="逗号分隔的命题 id（卡id::prop-N）")
    rg.add_argument("--reason", default="")
    rg.add_argument("--reviewer", default=None)
    rg.add_argument("--edges", default=str(DEFAULT_EDGES))
    rg.add_argument("--annotations", default=str(DEFAULT_ANN))
    rg.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    pg = sub.add_parser("progress", help="人审进度汇总")
    pg.add_argument("--json", action="store_true")
    pg.add_argument("--edges", default=str(DEFAULT_EDGES))
    pg.add_argument("--annotations", default=str(DEFAULT_ANN))
    pg.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    fb = sub.add_parser("feedback", help="人审结果反馈（生成器改进建议）")
    fb.add_argument("--json", action="store_true")
    fb.add_argument("--annotations", default=str(DEFAULT_ANN))
    a = ap.parse_args(argv)

    if a.check:
        try:
            anns = load_annotations(a.annotations)
        except ValueError as exc:
            print(f"[review] ❌ {exc}", file=sys.stderr)
            return 2
        problems = check(load_edges(a.edges), anns)
        if problems:
            print(f"[review] ❌ 标注校验失败（{len(problems)} 项）：", file=sys.stderr)
            for p in problems[:20]:
                print(f"  - {p}", file=sys.stderr)
            return 2
        print(f"[review] ✓ 标注文件合法：{len(anns)} 条记录")
        return 0

    edges = load_edges(a.edges)
    anns = load_annotations(a.annotations)
    last = latest_by_edge(anns)

    if a.cmd == "stats":
        st = stats(edges, anns)
        if a.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
            return 0
        print(f"[review] 候选边 {st['total']} · 待审 {st['pending']} · 已确认 {st['approved']} · "
              f"已拒绝 {st['rejected']} · 已改权 {st['modified']}")
        print(f"[review] 已审 {st['annotated_edges']} 条（历史记录 {st['annotations']} 条）· "
              f"通过率 {st['approve_rate']} · 拒绝率 {st['reject_rate']}")
        print("[review] 注：**系统绝不自动 approve/reject**；生效规则见 effective_edges()")
        return 0

    if a.cmd == "queue":
        groups = mis_groups(edges, a.mis_dir)
        if a.sort == "confidence":
            groups.sort(key=lambda g: g["n_edges"], reverse=True)
        elif a.sort == "impact":
            groups.sort(key=lambda g: g["n_props"], reverse=True)
        if a.json:
            print(json.dumps({"count": len(groups), "groups": groups}, ensure_ascii=False, indent=1))
            return 0
        print(f"[queue] {len(groups)} 个 MIS 群组（按{a.sort}降序）· 候选边 {sum(g['n_edges'] for g in groups)}")
        for i, g in enumerate(groups, 1):
            pending = sum(1 for eid in g["edge_ids"] if status_of(str(eid), last) == "pending")
            print(f"{i:2d}. {g['mis_id']:20s} amb={g['ambiguity']:5.2f} cards={g['n_cards']} "
                  f"props={g['n_props']} edges={g['n_edges']}(pending={pending})")
        return 0

    if a.cmd == "review-group":
        t0 = time.time()
        prop_ids = [p.strip() for p in (a.props or "").split(",") if p.strip()]
        if not prop_ids:
            # 显示该群组的命题列表供选择
            groups = {g["mis_id"]: g for g in mis_groups(edges, a.mis_dir)}
            g = groups.get(a.mis_id)
            if g is None:
                print(f"[review-group] MIS 不存在：{a.mis_id}", file=sys.stderr)
                return 1
            ap_dict = aeg.atom_props()
            print(f"[review-group] {a.mis_id}（关联 {g['n_cards']} 卡 / {g['n_props']} 命题 / {g['n_edges']} 边）")
            for cid in g["cards"]:
                for pid in ap_dict.get(cid, []):
                    pending = any(status_of(str(eid), last) == "pending"
                                  for eid in g["edge_ids"] if pid in eid)
                    print(f"  {pid}  {'[pending]' if pending else '[done]'}")
            print("用法：review-group MIS-XXX --props '卡id::prop-1,卡id::prop-2' --reason '...'")
            return 0
        if not str(a.reason or "").strip():
            print("[review-group] 缺 --reason（理由必填，拒绝 rubber-stamp）", file=sys.stderr)
            return 2
        try:
            recs = approve_group(a.mis_id, prop_ids, a.reason, reviewer=a.reviewer,
                                  annotations_path=a.annotations, edges_path=a.edges, mis_dir=a.mis_dir)
        except ValueError as exc:
            print(f"[review-group] 拒绝写入：{exc}", file=sys.stderr)
            return 2
        elapsed = time.time() - t0
        # automation bias 检测
        audit = load_audit()
        alerts = record_review(audit, "approve", a.reason, elapsed)
        save_audit(audit)
        print(f"[review-group] 已 approve {len(recs)} 条边（{a.mis_id} → {len(prop_ids)} 命题）"
              f" by {recs[0]['reviewer'] if recs else '?'} @ {elapsed:.1f}s")
        for al in alerts:
            print(f"  ⚠ {al}")
        return 0

    if a.cmd == "progress":
        groups = mis_groups(edges, a.mis_dir)
        prog = progress_summary(edges, anns, groups)
        if a.json:
            print(json.dumps(prog, ensure_ascii=False, indent=1))
            return 0
        bar_len = 30
        filled = int(bar_len * prog["completion_pct"] / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"[progress] {bar} {prog['completion_pct']}%")
        print(f"  群组：{prog['done_groups']}/{prog['total_groups']}（待审 {prog['pending_groups']}）")
        print(f"  边：  {prog['done_edges']}/{prog['total_edges']}（待审 {prog['pending_edges']}）")
        print(f"  预计剩余：{prog['est_remaining_minutes']} 分钟（按 595 实证 35s/组）")
        audit = load_audit()
        if audit["alerts"]:
            print(f"  automation bias 告警：{len(audit['alerts'])} 条（最近：{audit['alerts'][-1]}）")
        return 0

    if a.cmd == "feedback":
        fb = feedback_summary(anns)
        if a.json:
            print(json.dumps(fb, ensure_ascii=False, indent=1))
            return 0
        print(f"[feedback] 标注 {fb['total_annotations']} 条 · reject {fb['reject_count']} 条")
        if fb["reject_reasons"]:
            print("  reject 原因（前10）：")
            for r in fb["reject_reasons"]:
                print(f"    - {r}")
        print("  改进建议：")
        for s in fb["suggestions"]:
            print(f"    - {s}")
        return 0

    if a.cmd in ("approve", "reject", "modify"):
        try:
            rec = append_annotation(a.edge_id, a.cmd, a.reason,
                                    new_confidence=getattr(a, "confidence", None),
                                    reviewer=a.reviewer, path=a.annotations,
                                    edges_path=a.edges, mis_dir=a.mis_dir)
        except ValueError as exc:
            print(f"[review] ❌ 拒绝写入：{exc}", file=sys.stderr)
            return 2
        extra = f"（新可信度 {rec.get('new_confidence')}）" if rec.get("new_confidence") else ""
        print(f"[review] 已追加：{rec['edge_id']} {rec['action']}{extra} by {rec['reviewer']} "
              f"@ {rec['timestamp']}")
        return 0

    if a.cmd == "show":
        edge = next((e for e in edges if str(e["id"]) == a.edge_id), None)
        if edge is None:
            print(f"[review] ❌ 找不到边：{a.edge_id}", file=sys.stderr)
            return 1
        mis_card = resolve_mis_card(edge, a.mis_dir)
        print(json.dumps({**edge, "human_status": status_of(str(edge["id"]), last),
                          "human_history": [x for x in anns if x.get("edge_id") == edge["id"]],
                          "mis_card": str(mis_card) if mis_card else None},
                         ensure_ascii=False, indent=1))
        return 0

    # list
    rows = [(e, status_of(str(e["id"]), last)) for e in edges]
    if getattr(a, "status", None):
        rows = [r for r in rows if r[1] == a.status]
    if a.json:
        print(json.dumps({"count": len(rows),
                          "rows": [{**e, "human_status": s} for e, s in rows]},
                         ensure_ascii=False, indent=1))
        return 0
    print(f"[review] {len(rows)} 条（待审 = 无任何标注；生效规则：reject 剔除 / approve 升一级 / "
          f"modify 指定档）")
    for e, s in rows:
        print(f"- {e['id']}  [{e['kind']} · {e['confidence']} · {s}]  {_short(e['evidence'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
