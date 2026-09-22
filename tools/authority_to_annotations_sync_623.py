"""623 D1 · Authority 日志 → annotations 同步工具（打通 622 D1 断掉的通道）

**背景**：622 D1 把人审决策写进 `data/authority/authority_log.jsonl`，但 W2 solver 读的是
`data/human_attack_edge_annotations.jsonl`。两处各自为政 ⇒ 通道断：Authority 新增的 30 条决策
（622 D1 item-by-item）从未进入 annotations，导致 622 D2 重算 W2 "变化 0" 并非真无变化，而是通道断。

**本工具**：把 authority_log 的决策 reconcile 进 annotations 的"同步视图"
`data/human_attack_edge_annotations.synced.jsonl`（不覆盖受治理的原始文件，避免污染基线；
是否写回真实 annotations 由人审决定，符合铁律"不自动 push"）。

铁律：只读 authority_log + 受治理 annotations，只产出 synced 视图与汇总，不改原始卡/CORE_TOOLS。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
SYNCED = os.path.join(ROOT, "data", "human_attack_edge_annotations.synced.jsonl")

POWER_MAP = {"ACCEPT": "approve", "REJECT": "reject", "MODIFY": "modify",
             "ESCALATE": "escalate", "DEFER": "defer"}


def _ts(rec):
    return str(rec.get("decided_at") or rec.get("seq") or "")


def load_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def sync(authority, annotations):
    """把 authority 决策合并进 annotations（按 edge_id），返回 (synced_list, stats)。"""
    by_edge = {}
    for a in annotations:
        by_edge[a.get("edge_id")] = a
    added = updated = unchanged = 0
    for dec in authority:
        tgt = dec.get("target") or {}
        edge_id = tgt.get("id") or dec.get("decision_id")
        if not edge_id:
            continue
        action = POWER_MAP.get(str(dec.get("power", "")).upper(), "approve")
        new_rec = {
            "edge_id": edge_id,
            "action": action,
            "reason": dec.get("reason", ""),
            "reviewer": (dec.get("reviewer") or "").replace("human:", ""),
            "timestamp": dec.get("decided_at", ""),
            "source": "authority_log:" + str(dec.get("decision_id", "")),
        }
        if edge_id not in by_edge:
            by_edge[edge_id] = new_rec
            added += 1
        else:
            old = by_edge[edge_id]
            # 以 authority 决策的更新时间/序号判定新颖性
            if _ts(dec) >= (old.get("timestamp") or ""):
                if (old.get("action") != action) or (old.get("source", "").startswith("authority")):
                    by_edge[edge_id] = new_rec
                    updated += 1
                else:
                    unchanged += 1
            else:
                unchanged += 1
    return list(by_edge.values()), {"added": added, "updated": updated, "unchanged": unchanged}


def check() -> int:
    """只读自检（不写盘）：输入存在 / JSONL 合法 / 字段映射 / sync 可计算。"""
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("authority 日志存在", os.path.exists(AUTH))
    chk("annotations 文件存在", os.path.exists(ANN))
    try:
        authority = load_jsonl(AUTH)
        chk("authority JSONL 可解析", True)
    except (OSError, ValueError) as exc:
        authority = []
        chk(f"authority JSONL 可解析（{exc}）", False)
    try:
        annotations = load_jsonl(ANN)
        chk("annotations JSONL 可解析", True)
    except (OSError, ValueError) as exc:
        annotations = []
        chk(f"annotations JSONL 可解析（{exc}）", False)
    unmapped = {str(d.get("power", "")).upper() for d in authority} - set(POWER_MAP)
    print(f"  [info] 未在映射表的 power 值：{sorted(unmapped) or '无'}")
    _, stats = sync(authority, annotations)
    chk("sync() 可计算且返回统计字典", isinstance(stats, dict) and "added" in stats)
    print(f"D1 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="623 D1 Authority→annotations 同步")
    ap.add_argument("--authority", default=AUTH)
    ap.add_argument("--annotations", default=ANN)
    ap.add_argument("--out", default=SYNCED)
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return check()

    authority = load_jsonl(args.authority)
    annotations = load_jsonl(args.annotations)
    synced, stats = sync(authority, annotations)
    with open(args.out, "w", encoding="utf-8") as fh:
        for r in synced:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"authority 决策：{len(authority)} 条")
    print(f"原 annotations：{len(annotations)} 条")
    print(f"同步后视图：{len(synced)} 条  (新增 {stats['added']} / 更新 {stats['updated']} / 未变 {stats['unchanged']})")
    print(f"→ 写入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
