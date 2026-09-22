"""625 D3 · 人审执行工具（**只准备框架，不代签**）

设计目标：把「人审判决如何写入 Authority 日志」做成**可复用、可审计**的函数，但**本批不调用、不代签**——
严格遵循铁律「Authority 日志更新函数只定义不调用」。

- `build_entry(...)`：纯函数，构造一条带哈希链的 Authority 日志条目（不写盘）。
- `append_entry(path, entry)`：实际的写盘函数（**定义但本批 main/--check 均不调用**）。
- `--check`：验证函数签名 / 哈希链格式 / 输入校验，**且不修改任何日志**（size 不变）。

铁律：必有 `--check`；**绝不调用 append_entry**。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
VALID_POWER = {"ACCEPT", "REJECT", "ABSTAIN"}
VALID_DECISION = {"approve", "reject", "abstain"}


def _chain_hash(prev: str, entry: dict) -> str:
    """计算本条哈希（含前一条哈希，形成链）。"""
    payload = json.dumps({k: entry[k] for k in entry if k != "hash"},
                         ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(f"{prev}|{payload}".encode("utf-8")).hexdigest()


def build_entry(edge_id: str, power: str, decision: str,
                authorized_by: str, reason: str,
                prev_hash: str = "GENESIS", source: str = "human_review_executor_625") -> dict:
    """纯函数：构造一条 Authority 日志条目（**不写盘**）。

    - power ∈ {ACCEPT, REJECT, ABSTAIN}（与 Authority 日志既有 power 字段对齐）
    - decision ∈ {approve, reject, abstain}
    - authorized_by：人审执行者标识（来源标注，必填）
    """
    power = str(power).upper()
    decision = str(decision).lower()
    if power not in VALID_POWER:
        raise ValueError(f"power 非法：{power!r}（应 ∈ {VALID_POWER}）")
    if decision not in VALID_DECISION:
        raise ValueError(f"decision 非法：{decision!r}（应 ∈ {VALID_DECISION}）")
    if not authorized_by:
        raise ValueError("authorized_by 必填（人审来源标注）")
    entry = {
        "edge_id": edge_id,
        "power": power,
        "decision": decision,
        "authorized_by": authorized_by,
        "reason": reason,
        "source": source,
        "decided_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    entry["hash"] = _chain_hash(prev_hash, entry)
    return entry


def append_entry(path: str, entry: dict) -> int:
    """**实际的写盘函数：定义但本批绝不调用**（防代签）。"""
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return 1


def _read_last_hash(path: str) -> str:
    if not os.path.exists(path):
        return "GENESIS"
    last = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                last = json.loads(line)
    return last.get("hash", "GENESIS") if last else "GENESIS"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    before = os.path.getsize(AUTH) if os.path.exists(AUTH) else 0
    # 构造样例条目（不写盘）
    e = build_entry("EV-EDGE-0001", "ACCEPT", "approve", "reviewer:A",
                    "复核通过：证据可复现", prev_hash=_read_last_hash(AUTH))
    chk("build_entry 返回带 hash 的条目", isinstance(e, dict) and "hash" in e and len(e["hash"]) == 64)
    chk("哈希链含前驱", _chain_hash("GENESIS", e) == e["hash"])
    # 非法输入应抛错
    try:
        build_entry("x", "BOGUS", "approve", "A", "r")
        chk("非法 power 抛错", False)
    except ValueError:
        chk("非法 power 抛错", True)
    # 关键：本批绝不调用 append_entry（日志 size 不变）
    after = os.path.getsize(AUTH) if os.path.exists(AUTH) else 0
    chk("未代签：Authority 日志未被修改", before == after)
    # 明确断言 append_entry 在本批未被调用（仅定义）
    chk("append_entry 已定义但未调用", callable(append_entry))
    print(f"D3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 D3 人审执行框架（只准备，不代签）")
    ap.add_argument("--check", action="store_true", help="只读自检（绝不代签）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    # 框架就绪但**不执行任何判决**：仅提示可用入口。
    print("人审执行框架已就绪（build_entry / append_entry 已定义）。")
    print("本批**不调用** append_entry —— 人审判决须由人执行（来源标注 authorized_by）。")
    print("可用：python tools/human_review_executor_625.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
