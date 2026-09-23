"""629 C2 · V2 Authority 账本接入透明日志（纯标准库，只读账本 + 追加日志）

把 626 建立的 DecisionEvent v2 账本（452 条）逐条**上哈希链**，并把它**锚定**到 628 的
VSA 透明日志里。目的：让「权威决定」与「验证凭证」共享同一套可验证的溯源结构。

**设计（合并 vs 并行的显式选择，见报告 §三）**：
- **并行细粒度链**：`data/authority/authority_event_chain_629.jsonl`，每条 = 一个事件
  （`event_id` + 事件 JSON 的 sha256 + 前跳 hash），复用 628 的 `_entry_hash` 口径
  （只读 import `transparency_log_628`，不改它）⇒ 链格式与 628 兼容、可被同一套逻辑复验。
- **一行锚定**：把整条并行链的**根 hash**（末条 entry_hash）+ 账本 sha256 写成一个
  anchor 文件 `data/authority/authority_event_chain_629_anchor.json`，再通过 628 的
  `append_vsa()` 追加**一条**条目到**生产 VSA 日志**（幂等）。
- 为什么不把 452 条直接写进 628 的日志：628 日志的语义是「VSA 凭证日志」，
  且 `append_vsa` 要求每条都有**落盘文件**（会凭空产生 452 个派生文件）；
  并行链 + 一行锚定既满足「逐条上链」，又不破坏 628 的语义与一致性检查。

**不修改原 V2 ledger**（只读）。**幂等**：按 `event_id` 去重，重复运行零新增。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
CHAIN = os.path.join(ROOT, "data", "authority", "authority_event_chain_629.jsonl")
ANCHOR = os.path.join(ROOT, "data", "authority", "authority_event_chain_629_anchor.json")
ANCHOR_CRED = os.path.join(ROOT, "data", "authority",
                           "authority_chain_anchor_credential_629.json")
OUT_MD = os.path.join(ROOT, "data", "authority_log_integration_629.md")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha256_bytes(fh.read())


def canonical(event: dict[str, Any]) -> bytes:
    """事件规范化字节（sort_keys + UTF-8 + 无空格）⇒ 同一事件恒同 hash。"""
    return json.dumps(event, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def ledger_events() -> list[dict[str, Any]]:
    """只读读取 626 V2 账本。"""
    if not os.path.exists(LEDGER):
        return []
    out = []
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
    return out


def _read_chain() -> list[dict[str, Any]]:
    if not os.path.exists(CHAIN):
        return []
    with open(CHAIN, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def build_chain() -> dict[str, Any]:
    """逐条上链（幂等：已入链的 event_id 跳过）。追加模式写文件。"""
    import transparency_log_628 as T

    events = ledger_events()
    chain = _read_chain()
    seen = {str(e.get("event_id")) for e in chain}
    prev = chain[-1]["entry_hash"] if chain else "GENESIS"
    added = 0
    os.makedirs(os.path.dirname(CHAIN), exist_ok=True)
    with open(CHAIN, "a", encoding="utf-8", newline="\n") as fh:
        for ev in events:
            eid = str(ev.get("event_id", ""))
            if not eid or eid in seen:
                continue
            entry = {
                "log_index": len(chain),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "event_id": eid,
                "event_seq": ev.get("seq"),
                "event_hash": sha256_bytes(canonical(ev)),
                "result": ev.get("result"),
                "review_method": ev.get("review_method"),
                "prev_log_hash": prev,
            }
            entry["entry_hash"] = T._entry_hash(entry)
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
            prev, added = entry["entry_hash"], added + 1
            chain.append(entry)
            seen.add(eid)
    return {"added": added, "total": len(chain),
            "root_hash": chain[-1]["entry_hash"] if chain else "GENESIS"}


def verify_chain() -> dict[str, Any]:
    """复用 628 的 verify_log（按环境变量指向并行链文件），链格式口径一致。"""
    import transparency_log_628 as T

    old = os.environ.get(T.LOG_ENV)
    os.environ[T.LOG_ENV] = CHAIN
    try:
        v = T.verify_log()
    finally:
        if old is None:
            os.environ.pop(T.LOG_ENV, None)
        else:
            os.environ[T.LOG_ENV] = old
    chain = _read_chain()
    dup = len(chain) - len({str(e.get("event_id")) for e in chain})
    return {**v, "duplicates": dup,
            "root_hash": chain[-1]["entry_hash"] if chain else "GENESIS"}


def anchor_credential(anchor: dict[str, Any]) -> dict[str, Any]:
    """构造一条**合规的 628 形态 VSA 凭证**，把 authority 链根纳入其字段。

    为什么需要：628 B3/B4 的一致性契约是「日志尾部的 `vsa_file` 必须是一张**可通过
    `vsa_attestation_628 --verify-path` 验证的凭证**」。629 C2 首版只追加了一个裸 anchor
    JSON（无 `attestation`），导致 628 B4 的 `--check` 报 `logged_vsa_valid=False`
    （门禁首跑实测到该回归）。修复方式：再追加一条**真凭证**（标准 input_hashes/results +
    额外 `authority_chain` 字段 + **重算 HMAC**），把链根带进凭证本体。
    原 anchor 条目按 append-only 原则**保留不删**。
    """
    import vsa_attestation_628 as V

    cred = V.build_credential()
    cred["authority_chain"] = {"events": anchor["events"],
                               "root_hash": anchor["root_hash"],
                               "ledger_sha256": anchor["ledger_sha256"]}
    with open(V.SECRET, "rb") as fh:          # 只读密钥；缺失则抛错（不新建）
        key = fh.read()
    cred["attestation"] = V.compute_attestation(cred, key)
    return cred


def anchor_payload() -> dict[str, Any]:
    """anchor 的可复现内容（**不含 volatile 时间戳** ⇒ 反复运行字节一致 ⇒ append 幂等）。

    `generated_at` 取**链条目自己的最后一个时间戳**（已在盘上、稳定），而不是 `now()`——
    这是 629 C2 首版踩过的坑：写入 `now()` 会让每次 `--build` 都改文件内容，
    使 `append_vsa` 的按-hash 幂等失效，产生重复日志条目并让 628 B3 的
    「日志引用文件哈希一致」检查漂移。
    """
    v = verify_chain()
    chain = _read_chain()
    return {"batch": "629", "kind": "authority_event_chain_anchor",
            "ledger": os.path.relpath(LEDGER, ROOT).replace(os.sep, "/"),
            "ledger_sha256": sha256_file(LEDGER),
            "events": v["entries"], "chain_valid": bool(v["chain_valid"]),
            "root_hash": v["root_hash"],
            "generated_at": (chain[-1]["timestamp"] if chain else "GENESIS")}


def write_anchor() -> dict[str, Any]:
    """写 anchor 文件 + 合规凭证，并（幂等）追加到 628 生产日志。"""
    import transparency_log_628 as T
    import vsa_attestation_628 as V

    anchor = anchor_payload()
    with open(ANCHOR, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(anchor, fh, ensure_ascii=False, indent=2)
    # 凭证含 volatile 的 verified_at ⇒ **只写一次**（已存在则复用，保证幂等）
    if not os.path.exists(ANCHOR_CRED):
        cred = anchor_credential(anchor)
        with open(ANCHOR_CRED, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(cred, fh, ensure_ascii=False, indent=2)
    return {"anchor": anchor,
            "anchor_append": T.append_vsa(ANCHOR),
            "credential_verify": V.verify_credential(ANCHOR_CRED),
            "credential_append": T.append_vsa(ANCHOR_CRED),
            "log_state": T.status()}


def measure() -> dict[str, Any]:
    import transparency_log_628 as T

    events, chain, v = ledger_events(), _read_chain(), verify_chain()
    unlogged = [str(e.get("event_id")) for e in events
                if str(e.get("event_id")) not in {str(c.get("event_id")) for c in chain}]
    anchor = json.load(open(ANCHOR, encoding="utf-8")) if os.path.exists(ANCHOR) else None
    inc = T.check_inclusion(ANCHOR) if os.path.exists(ANCHOR) else {"included": False,
                                                                    "log_index": None}
    return {"ledger_events": len(events), "chain_entries": len(chain),
            "chain_valid": bool(v["chain_valid"]), "chain_broken": v["broken_at"],
            "duplicates": v["duplicates"], "unlogged_events": unlogged[:5],
            "unlogged_count": len(unlogged), "root_hash": v["root_hash"],
            "anchor": anchor, "anchor_in_vsa_log": bool(inc["included"]),
            "anchor_log_index": inc["log_index"], "vsa_log": T.status()}


def write_report() -> str:
    m = measure()
    lines = [
        "# 629 C2 · V2 Authority 账本接入透明日志", "",
        "> 工具：`tools/authority_log_integration_629.py`（只读账本 + 追加日志；"
        "只读 import `transparency_log_628` 复用其 `_entry_hash` / `verify_log` 口径）", "",
        "## 一、结果", "",
        "| 指标 | 值 |", "|---|---|",
        f"| V2 账本事件（626，只读） | {m['ledger_events']} 条 |",
        f"| 并行链条目 | {m['chain_entries']} 条 |",
        f"| 链完整性（复用 628 `verify_log`） | {m['chain_valid']}（broken={m['chain_broken']}） |",
        f"| 重复条目（幂等检查） | {m['duplicates']} |",
        f"| 未入链事件 | {m['unlogged_count']} 条 |",
        f"| 链根 hash | `{m['root_hash'][:24]}…` |",
        f"| 锚定条目已在 628 生产日志 | {m['anchor_in_vsa_log']}"
        f"（log_index={m['anchor_log_index']}） |", "",
        "## 二、结构", "",
        "```",
        "decision_event_v2_ledger.jsonl（452 条，**只读不改**）",
        "        │  逐条 canonical JSON → sha256",
        "        ▼",
        "authority_event_chain_629.jsonl（并行链，entry: log_index/event_id/event_hash/",
        "                                  prev_log_hash/entry_hash）",
        "        │  末条 entry_hash = 链根",
        "        ▼",
        "authority_event_chain_629_anchor.json（{events, root_hash, ledger_sha256}）",
        "        │  append_vsa（幂等）",
        "        ▼",
        "data/transparency_log.jsonl（628 生产日志，**+1 条锚定**）",
        "```", "",
        "## 三、为什么「并行链 + 一行锚定」而不是「452 条直接进 628 日志」", "",
        "1. **语义**：628 日志的定位是「VSA 凭证日志」；把 452 条事件混进去会让"
        "`logged_files_status()` / `unlogged_credentials()` 的语义漂移。",
        "2. **落盘要求**：`append_vsa()` 要求每条都有**真实文件**计算 sha256；"
        "逐条入册会凭空产生 452 个派生 JSON 文件入库（噪音），而这些文件并不构成"
        "「可独立验证的凭证」。",
        "3. **可验证性不打折**：并行链复用 628 的 `_entry_hash` 与 `verify_log`，"
        "**同一套代码可复验**；锚定条目让 452 条事件的最终根 hash 进入生产日志，"
        "从而获得与 VSA 凭证同等的溯源地位（跨锚定）。",
        "4. **任务书原文允许二选一**（「与 628 原透明日志的关系（合并还是并行）」），"
        "本工具选了并行 + 锚定，并把理由登记在此。", "",
        "## 四、局限", "",
        "- 链是**本地线性哈希链**（同 628），无外部见证者 ⇒ 只能证明「本文件内部未被改」，"
        "不能证明「没被整段替换」；",
        "- 事件 hash 锚定的是**账本文件内容**，不校验事件签名（DecisionEvent 无签名机制）；",
        "- 452 条事件的「人审合法性」不在本工具范围（`review_method` 只作为字段带过）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = measure()
    chk("账本可读（626 V2，452 条）", m["ledger_events"] >= 452, f"({m['ledger_events']})")
    chk("并行链已建立且条目 = 账本事件数",
        m["chain_entries"] == m["ledger_events"], f"({m['chain_entries']})")
    chk("链完整性通过", m["chain_valid"] and not m["chain_broken"])
    chk("零重复条目（幂等）", m["duplicates"] == 0)
    chk("零未入链事件", m["unlogged_count"] == 0, f"({m['unlogged_events']})")
    chk("anchor 文件存在且字段齐全",
        bool(m["anchor"]) and all(k in (m["anchor"] or {}) for k in
                                  ("events", "root_hash", "ledger_sha256")))
    chk("anchor 内容确定性（反复生成字节一致 ⇒ append 幂等）",
        anchor_payload() == anchor_payload()
        and json.dumps(anchor_payload(), ensure_ascii=False, indent=2)
        == open(ANCHOR, encoding="utf-8").read(), "anchor 必须与 anchor_payload() 一致")
    chk("628 日志引用文件哈希一致（无漂移）",
        bool(m["vsa_log"]["files"]["ok"]) and not m["vsa_log"]["files"]["drifted"],
        f"({m['vsa_log']['files']['drifted']})")
    chk("anchor 已锚定进 628 生产日志", m["anchor_in_vsa_log"],
        f"(index={m['anchor_log_index']})")
    chk("账本文件未被修改（只读）",
        sha256_file(LEDGER) == (m["anchor"] or {}).get("ledger_sha256"))
    chk("628 生产日志自身一致性未受影响",
        bool(m["vsa_log"]["chain_valid"]) and bool(m["vsa_log"]["files"]["ok"]))
    chk("报告存在", os.path.exists(OUT_MD)
        and "并行链" in open(OUT_MD, encoding="utf-8").read())
    print(f"C2 authority log integration check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 C2 V2 账本接入透明日志")
    ap.add_argument("--check", action="store_true", help="只读自检（不建链）")
    ap.add_argument("--build", action="store_true", help="建链 + 锚定（幂等）")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.build:
        print(json.dumps({"chain": build_chain(), "anchor": write_anchor()},
                         ensure_ascii=False, default=str))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps(measure(), ensure_ascii=False, default=str, indent=2))
        return 0
    m = measure()
    print(f"ledger={m['ledger_events']} chain={m['chain_entries']} "
          f"valid={m['chain_valid']} anchor_in_log={m['anchor_in_vsa_log']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
