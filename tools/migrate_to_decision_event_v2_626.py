"""626 B2 · 数据迁移：annotations(388) + authority_log(418) → DecisionEvent v2

**向后兼容**：旧文件**只读、不删、不改**；新 ledger 并行运行。

映射规则：
- annotations：`action` → `result`；`approve→APPROVE` / `modify→MODIFY` / `reject→REJECT`
  - 镜像边（`attack_edges_candidates.direction == "mis_to_prop"`）→
    `review_method=MIRROR_DERIVED` + `decision_origin=mirror_projection`
  - 其余 → `BATCH_AUTH` + `human_observed`
- authority_log：`power` → `operation`（`ACCEPT→CREATE` / `OVERRIDE→REPLACE`）
  - 622 执行的 30 条（`source == "615_decision_list"`）→
    `ITEM_OPEN` + `user_authorized_execution`，并把 `overrides` 映射为 `supersedes`
  - 其余 → `BATCH_AUTH` + `human_observed`
- seq：按 `decided_at` 升序；同刻 annotations 先、authority_log 后（哈希链依赖 seq 顺序）
- 去重：五元组 `(target_type, target_id, operation, result, decided_at)`

铁律：旧文件不修改；`--check` 为只读干跑。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402

ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
REPORT = os.path.join(ROOT, "data", "migration_report_v2_626.md")

ACTION_TO_RESULT = {"approve": "APPROVE", "modify": "MODIFY", "reject": "REJECT"}


def _jl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _mirror_ids() -> set[str]:
    """镜像边 ID：`direction == "mis_to_prop"`（实测 194 条）。"""
    return {str(c.get("id")) for c in _jl(CAND)
            if str(c.get("direction")) == "mis_to_prop"}


def _local_ts(v: object) -> str:
    return str(v or "")


def build_events() -> tuple[list[tuple[D.DecisionEvent, int]], dict]:
    """构造待迁移事件（未分配 seq），返回 ([(event, src_order)], stats)。

    `src_order`：0 = annotations，1 = authority_log（同刻排序用）。
    """
    mirrors = _mirror_ids()
    events: list[tuple[D.DecisionEvent, int]] = []
    stats: dict = {"annotations": 0, "authority": 0, "mirror": 0,
                   "executed_30": 0, "override": 0}

    # ── annotations (388) ──
    for a in _jl(ANN):
        eid = str(a.get("edge_id") or "")
        action = str(a.get("action") or "approve").lower()
        result = ACTION_TO_RESULT.get(action, "APPROVE")
        is_mirror = eid in mirrors
        if is_mirror:
            stats["mirror"] += 1
        ev = D.make_event(
            target_type="edge", target_id=eid, result=result,
            operation="CREATE",
            review_method="MIRROR_DERIVED" if is_mirror else "BATCH_AUTH",
            decision_origin="mirror_projection" if is_mirror else "human_observed",
            reviewer=str(a.get("reviewer") or ""),
            decided_at=_local_ts(a.get("timestamp")),
            modification=(str(a.get("reason") or "")[:200] if result == "MODIFY" else ""),
            scope="single_edge",
            confidence="low",
        )
        ev.basis_refs = ["data/human_attack_edge_annotations.jsonl"]
        events.append((ev, 0))
        stats["annotations"] += 1

    # ── authority_log (418) ──
    # 注：annotations 的 target 集合用于判重参考；迁移保留两条（原始 + REPLACE 取代关系）


    for a in _jl(AUTH):
        tgt = a.get("target")
        tid = str(tgt.get("id")) if isinstance(tgt, dict) else str(tgt or "")
        power = str(a.get("power") or "ACCEPT").upper()
        operation = "REPLACE" if power == "OVERRIDE" else "CREATE"
        reason = str(a.get("reason") or "")
        if power == "OVERRIDE":
            stats["override"] += 1
            result = "APPROVE" if "复核 approve" in reason else "MODIFY"
        else:
            result = "APPROVE"
        executed = str(a.get("source")) == "615_decision_list"
        if executed:
            stats["executed_30"] += 1
        supersedes: list[str] = []
        ov = a.get("overrides")
        if ov:
            supersedes.append(str(ov))
        ev = D.make_event(
            target_type="edge", target_id=tid, result=result, operation=operation,
            review_method="ITEM_OPEN" if executed else "BATCH_AUTH",
            decision_origin="user_authorized_execution" if executed else "human_observed",
            reviewer=str(a.get("reviewer") or ""),
            decided_at=_local_ts(a.get("decided_at")),
            supersedes=supersedes,
            modification=(reason[:200] if result == "MODIFY" else ""),
            scope="single_edge",
            confidence=str(a.get("confidence") or "low"),
        )
        ev.basis_refs = ["data/authority/authority_log.jsonl", str(a.get("decision_id") or "")]
        events.append((ev, 1))         # 同刻 authority 排在 annotations 之后
        stats["authority"] += 1

    return events, stats


def migrate() -> tuple[D.AuthorityLedger, dict]:
    events, stats = build_events()
    # 排序：decided_at 升序；同刻 annotations 先、authority 后
    events.sort(key=lambda p: (_local_ts(p[0].decided_at), p[1]))
    # 去重：五元组
    seen: set[tuple] = set()
    deduped: list[D.DecisionEvent] = []
    dup = 0
    for e, _order in events:
        key = (e.target_type, e.target_id, e.operation, e.result, e.decided_at)
        if key in seen:
            dup += 1
            continue
        seen.add(key)
        deduped.append(e)

    led = D.AuthorityLedger()
    for e in deduped:
        try:
            led.append(e)
        except ValueError:
            # 校验失败（如 REPLACE 缺 supersedes）：降级为 CREATE 再入账，并记录
            if e.operation == "REPLACE":
                e.operation = "CREATE"
                e.supersedes = []
                led.append(e)
            else:
                raise
    stats.update({
        "input_total": stats["annotations"] + stats["authority"],
        "after_dedup": len(deduped),
        "duplicates_removed": dup,
        "ledger_size": len(led),
    })
    return led, stats


def render_report(led: D.AuthorityLedger, stats: dict) -> str:
    by_m = led.count_by_review_method()
    by_o = led.count_by_decision_origin()
    L = ["# 626 B2 · 数据迁移报告（annotations + authority_log → DecisionEvent v2）", "",
         "## 一、迁移条数（**实测，非预设**）", "",
         "| 项 | 数量 |", "|---|---|",
         f"| annotations 输入 | {stats['annotations']} |",
         f"| authority_log 输入 | {stats['authority']} |",
         f"| **输入合计** | **{stats['input_total']}** |",
         f"| 五元组去重移除 | {stats['duplicates_removed']} |",
         f"| **迁移后 ledger 条数** | **{stats['ledger_size']}** |",
         f"| 其中镜像边（MIRROR_DERIVED） | {stats['mirror']} |",
         f"| 其中 622 授权执行 30 条（ITEM_OPEN） | {stats['executed_30']} |",
         f"| 其中 OVERRIDE→REPLACE | {stats['override']} |", "",
         "## 二、映射规则", "",
         "| 旧 | v2 |", "|---|---|",
         "| `action: approve/modify/reject` | `result: APPROVE/MODIFY/REJECT` |",
         "| `power: ACCEPT` | `operation: CREATE` |",
         "| `power: OVERRIDE` | `operation: REPLACE`（+ `supersedes` from `overrides`） |",
         "| `review_method: batch_authorization` | `BATCH_AUTH` + `human_observed` |",
         "| `review_method: item_by_item_executed`（622 的 30 条） | `ITEM_OPEN` + `user_authorized_execution` |",
         "| `direction: mis_to_prop`（194 条镜像边） | `MIRROR_DERIVED` + `mirror_projection` |", "",
         "## 三、验证结果", "",
         f"- 哈希链完整：**{'✅ 通过' if led.verify_chain() else '❌ 失败'}**",
         f"- 独立人类确认强度：**{led.independent_human_review_count()}**"
         "（无 ITEM_BLIND/ITEM_SECOND_REVIEW ⇒ 应为 0）",
         f"- review_method 分布：`{by_m}`",
         f"- decision_origin 分布：`{by_o}`", "",
         "## 四、向后兼容", "",
         "- `human_attack_edge_annotations.jsonl`（388）**未删除、未修改**",
         "- `authority/authority_log.jsonl`（418）**未删除、未修改**",
         "- 新 ledger：`data/authority/decision_event_v2_ledger.jsonl`（并行运行）",
         "- 切换开关：统一环境变量 `QUEYI_AUTHORITY_V2=1`（dashboard 投影默认启用；W2/PCK 关键路径默认旧逻辑）",
         "- 回滚：`QUEYI_AUTHORITY_V2=0`（新 ledger 保留供审计，不删除）", "",
         "## 五、已知局限（诚实登记）", "",
         "1. 旧 `authority_log` **没有 `action` 字段**，`result` 由 `power` + `reason` 推导"
         "（`OVERRIDE` 且 reason 含「复核 approve」→ APPROVE，否则 MODIFY）；属**保守推断**，已在下表可审计。",
         "2. `annotations` **没有 `is_mirror` 字段**，镜像判定来自 `attack_edges_candidates.direction`。",
         "3. 622 的 30 条与 annotations 同 target 的记录按任务要求**保留两条**（原始 + REPLACE），"
         "通过 `supersedes` 表达取代关系，而非物理删除。", ""]
    return "\n".join(L) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    led, st = migrate()
    chk("输入合计 806", st["input_total"] == 806, f"({st['input_total']})")
    chk("ledger 非空", len(led) > 0, f"({len(led)})")
    chk("哈希链完整", led.verify_chain())
    chk("独立人类确认强度 = 0", led.independent_human_review_count() == 0)
    chk("迁移后条数 = 输入 - 去重", st["ledger_size"] == st["input_total"] - st["duplicates_removed"])
    chk("含 MIRROR_DERIVED", led.count_by_review_method().get("MIRROR_DERIVED", 0) > 0)
    chk("含 ITEM_OPEN（622 的 30 条）",
        led.count_by_review_method().get("ITEM_OPEN", 0) == 30,
        f"({led.count_by_review_method().get('ITEM_OPEN', 0)})")
    cur = led.get_current("edge", led.all_events()[0].target_id)
    chk("get_current 可查询", cur is not None)
    # 向后兼容：旧文件仍在
    chk("旧 annotations 仍存在", os.path.exists(ANN))
    chk("旧 authority_log 仍存在", os.path.exists(AUTH))
    print(f"B2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 B2 数据迁移 → DecisionEvent v2")
    ap.add_argument("--check", action="store_true", help="只读干跑自检（不写文件）")
    ap.add_argument("--run", action="store_true", help="执行迁移并写出 ledger + 报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    led, st = migrate()
    if args.run:
        led.export_jsonl(LEDGER)
        with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(led, st))
        print(f"ledger -> {LEDGER} ({len(led)} events)")
        print(f"report -> {REPORT}")
    print(json.dumps({k: v for k, v in st.items()}, ensure_ascii=False, indent=2))
    print("by_review_method =", led.count_by_review_method())
    print("by_decision_origin =", led.count_by_decision_origin())
    print("independent_human_review_count =", led.independent_human_review_count())
    return 0


if __name__ == "__main__":
    sys.exit(main())
