"""628 B3 · 透明日志（append-only Transparency Log）—— 他验三件套 #3

维护 append-only 日志 `data/transparency_log.jsonl`，每条：
```
{"log_index": N, "timestamp": ISO, "vsa_hash": <VSA凭证文件sha256>,
 "prev_log_hash": <上一条 entry_hash>, "entry_hash": <本条 sha256（不含 entry_hash 字段）>}
```
- `--append <vsa路径>`：把 VSA 凭证追加进日志（计算 prev_log_hash，**只追加不修改**）
- `--verify`：从第一条到最后一条重算每个 entry_hash / prev_log_hash，确认链完整
- `--inclusion <vsa路径>`：验证某 VSA 凭证在日志中（线性查找 + hash 验证）
- `--check`：验证当前日志完整性

**设计说明**（与 Rekor v2 对比）：本项目用**简单哈希链**而非 Merkle tree——
单用户阶段日志量小（几十条），线性链足够；Merkle 的优势在百万条级。日志存本地、
无外部见证者——真正的透明日志需外部可审计（推公开 Rekor 实例），留后续批次。
**不 import** 613/625 的 Merkle/OTS 工具（保持独立性），自实现哈希链。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LOG = os.path.join(ROOT, "data", "transparency_log.jsonl")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
OUT_MD = os.path.join(ROOT, "data", "transparency_log_report_628.md")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _read_log() -> list[dict]:
    if not os.path.exists(LOG):
        return []
    return [json.loads(l) for l in open(LOG, encoding="utf-8") if l.strip()]


def _entry_hash(entry: dict) -> str:
    payload = {k: v for k, v in entry.items() if k != "entry_hash"}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def append_vsa(vsa_path: str) -> dict:
    """追加 VSA 凭证到日志（append-only：只写文件末尾）。"""
    if not os.path.exists(vsa_path):
        return {"ok": False, "error": f"not found: {vsa_path}"}
    log = _read_log()
    prev_hash = log[-1]["entry_hash"] if log else "GENESIS"
    entry = {
        "log_index": len(log),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "vsa_hash": _sha256_file(vsa_path),
        "vsa_file": os.path.relpath(vsa_path, ROOT),
        "prev_log_hash": prev_hash,
    }
    entry["entry_hash"] = _entry_hash(entry)
    with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"ok": True, "log_index": entry["log_index"],
            "entry_hash": entry["entry_hash"], "vsa_hash": entry["vsa_hash"]}


def verify_log() -> dict:
    """重算整条链：entry_hash 与 prev_log_hash 逐条验证。"""
    log = _read_log()
    prev = "GENESIS"
    broken: list[int] = []
    for i, e in enumerate(log):
        if e.get("prev_log_hash") != prev or _entry_hash(e) != e.get("entry_hash"):
            broken.append(i)
        prev = str(e.get("entry_hash"))
    return {"entries": len(log), "chain_valid": not broken, "broken_at": broken,
            "first_ts": log[0].get("timestamp") if log else None,
            "last_ts": log[-1].get("timestamp") if log else None}


def check_inclusion(vsa_path: str) -> dict:
    """验证某 VSA 凭证在日志中（线性查找 + hash 比对）。"""
    vh = _sha256_file(vsa_path)
    log = _read_log()
    hits = [e for e in log if e.get("vsa_hash") == vh]
    return {"vsa_path": os.path.relpath(vsa_path, ROOT),
            "vsa_hash": vh, "included": bool(hits),
            "log_index": hits[-1]["log_index"] if hits else None}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    v = verify_log()
    chk("日志哈希链完整", v["chain_valid"], f"({v['entries']} 条, broken={v['broken_at']})")
    chk("至少 1 条日志条目", v["entries"] >= 1, f"({v['entries']})")
    # inclusion：取最近一张 VSA 凭证验证存在性
    creds = sorted(f for f in os.listdir(VSA_DIR)
                   if f.startswith("attestation_")) if os.path.isdir(VSA_DIR) else []
    if creds:
        inc = check_inclusion(os.path.join(VSA_DIR, creds[-1]))
        chk("最近 VSA 凭证可验证存在于日志", inc["included"],
            f"(index={inc['log_index']})")
    print(f"B3 transparency log check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B3 透明日志")
    ap.add_argument("--check", action="store_true", help="自检（验证完整性）")
    ap.add_argument("--append", metavar="VSA", help="追加 VSA 凭证")
    ap.add_argument("--inclusion", metavar="VSA", help="验证凭证在日志中")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    if args.append:
        print(json.dumps(append_vsa(args.append), ensure_ascii=False, indent=2))
        return 0
    if args.inclusion:
        print(json.dumps(check_inclusion(args.inclusion), ensure_ascii=False, indent=2))
        return 0
    if args.report:
        v = verify_log()
        lines = [
            "# 628 B3 · 透明日志报告（他验三件套 #3）", "",
            "- 日志：`data/transparency_log.jsonl`（append-only）",
            f"- 当前状态：**{v['entries']} 条**，链完整：{v['chain_valid']}",
            f"- 最早条目：{v['first_ts']} · 最新条目：{v['last_ts']}",
            "",
            "## 设计说明", "",
            "- 结构：线性哈希链——`entry_hash = sha256(除 entry_hash 外全字段)`，",
            "  `prev_log_hash` 指向上一条 entry_hash，首条 prev=GENESIS。",
            "- **append-only**：追加只写文件末尾；任何历史条目的修改/删除都会使"
            "其后所有 prev_log_hash/entry_hash 校验失败。",
            "- 与 Rekor v2 对比：本项目用简单哈希链而非 Merkle tree——单用户阶段"
            "日志量小（几十条），线性链足够；Merkle 优势在百万条级。",
            "- 不 import 613/625 的 Merkle/OTS 工具（保持独立性），自实现哈希链。",
            "",
            "## 局限性（诚实）", "",
            "- 日志存储在本地，**没有外部见证者**。真正的透明日志需要外部可审计",
            "（如推送到公开 Rekor 实例），留后续批次。",
        ]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
        return 0
    if args.check:
        return selftest()
    print(json.dumps(verify_log(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
