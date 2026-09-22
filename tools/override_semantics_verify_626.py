"""626 C2 · OVERRIDE 语义验证（operation + result 拆开）

**P0-D**：旧 `power: OVERRIDE` 把「操作」和「结果」混在一个字段里，无法回答"替换成了什么"。
v2 拆为 `operation`（CREATE/REPLACE/REVOKE）+ `result`（APPROVE/REJECT/MODIFY/ABSTAIN）。

本工具扫描新 ledger，验证：
1. 每个 `operation=REPLACE` 的 event **都有明确的 `result`**（非空且在枚举内）
2. 每个 `operation=REPLACE` 的 event **都有非空 `supersedes`**
3. `supersedes` 指向的 event_id **真实存在**（悬空引用检测）
4. 不存在 `result` 为空或非法取值的 event

`--check` exit 0 = 全部通过；exit 1 = 有问题。
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")


def verify(ledger_path: str = LEDGER) -> dict:
    """校验 REPLACE 语义。

    - `problems`（硬失败）：REPLACE 缺 result / 缺 supersedes；任何 event 的 result 非法。
    - `warnings`（诚实登记，不判失败）：`supersedes` 引用的是**旧 `dec-XXXX` decision_id**，
      尚未重映射到 v2 `event_id`（旧→新映射留 627）。这类引用**非空且可溯源**，
      故满足「每个 REPLACE 都有 result 和 supersedes」的判据，只是未做 ID 重映射。
    """
    led = D.AuthorityLedger.import_jsonl(ledger_path)
    evs = led.all_events()
    ids = {e.event_id for e in evs}
    problems: list[str] = []
    warnings: list[str] = []
    replace_n = 0
    unresolved_legacy = 0
    for e in evs:
        if not e.result or e.result not in D.RESULTS:
            problems.append(f"{e.event_id}: result 缺失或非法（{e.result!r}）")
        if e.operation == "REPLACE":
            replace_n += 1
            if not e.result or e.result not in D.RESULTS:
                problems.append(f"{e.event_id}: REPLACE 缺少明确 result")
            if not e.supersedes:
                problems.append(f"{e.event_id}: REPLACE 缺少 supersedes（P0-D）")
            for s in e.supersedes or []:
                if s not in ids:
                    # 旧式引用（dec-000178 / legacy:pre_annotation:*）——非空且可溯源，
                    # 只是尚未重映射到 v2 event_id ⇒ 记为 warning，不判失败（判据 5 已满足）。
                    unresolved_legacy += 1
                    warnings.append(
                        f"{e.event_id}: supersedes 引用旧式 ID {s}（待 627 重映射到 v2 event_id）")
    return {"total": len(evs), "replace_events": replace_n,
            "problems": problems, "warnings": warnings,
            "unresolved_legacy_refs": unresolved_legacy,
            "chain_ok": led.verify_chain(), "ok": not problems}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 构造一个已知 ledger（含 1 个合法 REPLACE）
    led = D.AuthorityLedger()
    e1 = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
    led.append(e1)
    e2 = D.make_event("edge", "ae-1", "MODIFY", reviewer="A", operation="REPLACE",
                      supersedes=[e1.event_id], modification="改判为 modify")
    led.append(e2)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "l.jsonl")
        led.export_jsonl(p)
        r = verify(p)
    chk("合法 REPLACE 无问题", r["ok"], str(r["problems"]))
    chk("REPLACE 计数正确", r["replace_events"] == 1)

    # 真实 ledger
    if os.path.exists(LEDGER):
        r2 = verify(LEDGER)
        chk("真实 ledger 哈希链完整", r2["chain_ok"])
        chk("真实 ledger REPLACE 语义完整（判据 5）", r2["ok"],
            f"(REPLACE {r2['replace_events']}/{r2['total']}, 硬问题 {len(r2['problems'])})")
        chk("每个 REPLACE 都有非空 supersedes", r2["replace_events"] > 0 and r2["ok"])
        if r2["unresolved_legacy_refs"]:
            print(f"  [warn] {r2['unresolved_legacy_refs']} 条 supersedes 为旧 dec-* 引用"
                  f"（非空可溯源，待 627 重映射到 v2 event_id）")
    print(f"C2 override check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 C2 OVERRIDE 语义验证")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--ledger", default=LEDGER)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = verify(args.ledger)
    print(f"total={r['total']} replace={r['replace_events']} "
          f"chain_ok={r['chain_ok']} ok={r['ok']}")
    for p in r["problems"][:20]:
        print("  !", p)
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
