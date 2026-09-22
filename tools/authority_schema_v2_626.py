"""626 A3 · Authority Schema v2（review_method 五级 + decision_origin 四级）

**根治 P0-A**：把「人类判断」和「人类授权执行」彻底拆成两个概念。

- `review_method`（**方法**——人是怎么审的）：
  - `BATCH_AUTH`          批量授权（一个人用模板在几分钟内批量通过）
  - `MIRROR_DERIVED`      镜像边派生（由对称关系自动派生，未独立审查）
  - `ITEM_OPEN`           逐条开放式审查（**看得到** AI 推荐）
  - `ITEM_BLIND`          逐条盲审（**看不到** AI 推荐）
  - `ITEM_SECOND_REVIEW`  二次复核（对已有决定再审查一次）

- `decision_origin`（**来源**——这个决定实际来自谁）：
  - `human_observed`              人真实观察后判断
  - `user_authorized_execution`   用户授权执行（机器/流程代落，人未逐条判断）
  - `machine_projection`          机器投影（由 Authority 派生视图推出）
  - `mirror_projection`           镜像投影（由对称关系推出）

**独立人类确认强度**：只有 `review_method ∈ {ITEM_BLIND, ITEM_SECOND_REVIEW}`
**且** `decision_origin == human_observed` 才计入。
⇒ 622 的 30 条（ITEM_OPEN + user_authorized_execution）**不计入**，当前强度 = **0**。

纯标准库；`--check` 验证 schema 完整性。
"""
from __future__ import annotations

import argparse
import sys

# ── review_method 五级 ──
REVIEW_METHODS: tuple[str, ...] = (
    "BATCH_AUTH",
    "MIRROR_DERIVED",
    "ITEM_OPEN",
    "ITEM_BLIND",
    "ITEM_SECOND_REVIEW",
)

# ── decision_origin 四级 ──
DECISION_ORIGINS: tuple[str, ...] = (
    "human_observed",
    "user_authorized_execution",
    "machine_projection",
    "mirror_projection",
)

# ── 计入「独立人类确认强度」的 review_method ──
INDEPENDENT_METHODS: frozenset[str] = frozenset({"ITEM_BLIND", "ITEM_SECOND_REVIEW"})
INDEPENDENT_ORIGIN = "human_observed"

# 旧 schema → v2 的兼容映射
LEGACY_METHOD_MAP: dict[str, str] = {
    "batch_authorization": "BATCH_AUTH",
    "item_by_item_executed": "ITEM_OPEN",
    "mirror": "MIRROR_DERIVED",
    "mirror_edge": "MIRROR_DERIVED",
}

LEGACY_POWER_MAP: dict[str, str] = {
    # 旧 authority_log 的 power → v2 的 operation
    "ACCEPT": "CREATE",
    "OVERRIDE": "REPLACE",
    "REVOKE": "REVOKE",
}

OPERATIONS: tuple[str, ...] = ("CREATE", "REPLACE", "REVOKE")
RESULTS: tuple[str, ...] = ("APPROVE", "REJECT", "MODIFY", "ABSTAIN")


def is_valid_review_method(v: str) -> bool:
    return v in REVIEW_METHODS


def is_valid_decision_origin(v: str) -> bool:
    return v in DECISION_ORIGINS


def is_independent_human_review(review_method: str, decision_origin: str) -> bool:
    """是否计入「独立人类确认强度」。"""
    return review_method in INDEPENDENT_METHODS and decision_origin == INDEPENDENT_ORIGIN


def normalize_legacy_method(v: str | None) -> str:
    """旧 review_method → v2；未知一律保守映射为 BATCH_AUTH。"""
    if not v:
        return "BATCH_AUTH"
    return LEGACY_METHOD_MAP.get(str(v), "BATCH_AUTH" if str(v) not in REVIEW_METHODS else str(v))


def normalize_legacy_power(v: str | None) -> str:
    """旧 power → v2 operation。"""
    return LEGACY_POWER_MAP.get(str(v or "").upper(), "CREATE")


def validate_event(review_method: str, decision_origin: str,
                   operation: str, result: str) -> list[str]:
    """校验一个 event 的枚举合法性，返回错误列表（空 = 合法）。"""
    errs: list[str] = []
    if not is_valid_review_method(review_method):
        errs.append(f"review_method 非法：{review_method!r} ∉ {REVIEW_METHODS}")
    if not is_valid_decision_origin(decision_origin):
        errs.append(f"decision_origin 非法：{decision_origin!r} ∉ {DECISION_ORIGINS}")
    if operation not in OPERATIONS:
        errs.append(f"operation 非法：{operation!r} ∉ {OPERATIONS}")
    if result not in RESULTS:
        errs.append(f"result 非法：{result!r} ∉ {RESULTS}")
    return errs


def describe() -> dict:
    return {
        "review_methods": list(REVIEW_METHODS),
        "decision_origins": list(DECISION_ORIGINS),
        "independent_methods": sorted(INDEPENDENT_METHODS),
        "independent_origin": INDEPENDENT_ORIGIN,
        "operations": list(OPERATIONS),
        "results": list(RESULTS),
        "legacy_method_map": LEGACY_METHOD_MAP,
        "legacy_power_map": LEGACY_POWER_MAP,
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("review_method 五级", len(REVIEW_METHODS) == 5)
    chk("decision_origin 四级", len(DECISION_ORIGINS) == 4)
    chk("旧 batch_authorization → BATCH_AUTH",
        normalize_legacy_method("batch_authorization") == "BATCH_AUTH")
    chk("旧 item_by_item_executed → ITEM_OPEN",
        normalize_legacy_method("item_by_item_executed") == "ITEM_OPEN")
    chk("旧 power OVERRIDE → REPLACE", normalize_legacy_power("OVERRIDE") == "REPLACE")
    chk("旧 power ACCEPT → CREATE", normalize_legacy_power("ACCEPT") == "CREATE")
    # 关键：622 的 30 条（ITEM_OPEN + user_authorized_execution）**不**算独立人审
    chk("ITEM_OPEN+user_authorized_execution 不计独立",
        not is_independent_human_review("ITEM_OPEN", "user_authorized_execution"))
    chk("BATCH_AUTH+human_observed 不计独立",
        not is_independent_human_review("BATCH_AUTH", "human_observed"))
    chk("ITEM_BLIND+human_observed 计独立",
        is_independent_human_review("ITEM_BLIND", "human_observed"))
    chk("ITEM_SECOND_REVIEW+human_observed 计独立",
        is_independent_human_review("ITEM_SECOND_REVIEW", "human_observed"))
    chk("非法枚举可被校验", bool(validate_event("BOGUS", "human_observed", "CREATE", "APPROVE")))
    chk("合法组合无错误",
        validate_event("ITEM_BLIND", "human_observed", "CREATE", "APPROVE") == [])
    print(f"A3 schema check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="626 A3 Authority Schema v2")
    ap.add_argument("--check", action="store_true", help="schema 完整性自检")
    ap.add_argument("--describe", action="store_true", help="打印 schema 定义")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.describe:
        import json
        print(json.dumps(describe(), ensure_ascii=False, indent=2))
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
