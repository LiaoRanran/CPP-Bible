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

# 测试隔离：可用环境变量把日志指向临时文件（默认生产日志），保证单测不污染生产状态
LOG_ENV = "CPPBIBLE_TRANSPARENCY_LOG"


def _log_path() -> str:
    return os.environ.get(LOG_ENV) or LOG


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def _read_log() -> list[dict]:
    p = _log_path()
    if not os.path.exists(p):
        return []
    return [json.loads(line) for line in open(p, encoding="utf-8")
            if line.strip()]


def _entry_hash(entry: dict) -> str:
    payload = {k: v for k, v in entry.items() if k != "entry_hash"}
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def append_vsa(vsa_path: str) -> dict:
    """追加 VSA 凭证到日志（append-only：只写文件末尾）。

    **幂等**：同一凭证（相同 sha256）已入册时不重复追加（返回 `already_present`）。
    """
    if not os.path.exists(vsa_path):
        return {"ok": False, "error": f"not found: {vsa_path}"}
    log = _read_log()
    vh = _sha256_file(vsa_path)
    for e in log:
        if e.get("vsa_hash") == vh:
            return {"ok": True, "already_present": True, "log_index": e["log_index"],
                    "entry_hash": e["entry_hash"], "vsa_hash": vh}
    prev_hash = log[-1]["entry_hash"] if log else "GENESIS"
    entry = {
        "log_index": len(log),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "vsa_hash": _sha256_file(vsa_path),
        "vsa_file": os.path.relpath(vsa_path, ROOT),
        "prev_log_hash": prev_hash,
    }
    entry["entry_hash"] = _entry_hash(entry)
    with open(_log_path(), "a", encoding="utf-8", newline="\n") as fh:
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


def logged_files_status() -> dict:
    """每条日志引用的凭证文件是否存在、sha256 是否与登记值一致（漂移检测）。"""
    log = _read_log()
    missing, drifted = [], []
    for e in log:
        p = os.path.join(ROOT, str(e.get("vsa_file", "")))
        if not os.path.exists(p):
            missing.append(e.get("log_index"))
        elif _sha256_file(p) != e.get("vsa_hash"):
            drifted.append(e.get("log_index"))
    return {"entries": len(log), "missing": missing, "drifted": drifted,
            "ok": not missing and not drifted}


def unlogged_credentials() -> list[str]:
    """生产凭证目录里**未入册**的凭证（正常状态应为空）。"""
    if not os.path.isdir(VSA_DIR):
        return []
    logged = {e.get("vsa_file") for e in _read_log()}
    out = []
    for f in sorted(os.listdir(VSA_DIR)):
        if f.startswith("attestation_") and f.endswith(".json"):
            rel = os.path.relpath(os.path.join(VSA_DIR, f), ROOT)
            if rel not in logged:
                out.append(rel)
    return out


def status() -> dict:
    """日志状态汇总（供 B4 编排器与他验报告读取）。"""
    v = verify_log()
    log = _read_log()
    tail = log[-1]["vsa_file"] if log else None
    inc = check_inclusion(os.path.join(ROOT, tail)) if tail else {"included": False,
                                                                 "log_index": None}
    return {**v, "files": logged_files_status(), "unlogged": unlogged_credentials(),
            "tail_vsa_file": tail, "tail_included": bool(inc["included"]),
            "tail_log_index": inc["log_index"]}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    st = status()
    chk("日志哈希链完整", st["chain_valid"],
        f"({st['entries']} 条, broken={st['broken_at']})")
    chk("至少 1 条日志条目", st["entries"] >= 1, f"({st['entries']})")
    chk("日志引用的凭证文件都在且哈希一致", st["files"]["ok"],
        f"(missing={st['files']['missing']}, drifted={st['files']['drifted']})")
    chk("凭证全部入册（无未登记凭证）", not st["unlogged"], f"({st['unlogged']})")
    chk("日志尾部凭证可验证存在于日志", st["tail_included"],
        f"(index={st['tail_log_index']})")
    # 幂等：重复追加同一凭证不新增条目
    if st["tail_vsa_file"]:
        n_before = len(_read_log())
        r = append_vsa(os.path.join(ROOT, st["tail_vsa_file"]))
        chk("重复追加幂等（不新增日志条目）",
            bool(r.get("already_present")) and len(_read_log()) == n_before)
        chk("追加后链仍完整", verify_log()["chain_valid"])
    print(f"B3 transparency log check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B3 透明日志")
    ap.add_argument("--check", action="store_true", help="自检（验证完整性）")
    ap.add_argument("--append", metavar="VSA", help="追加 VSA 凭证")
    ap.add_argument("--inclusion", metavar="VSA", help="验证凭证在日志中")
    ap.add_argument("--status", action="store_true", help="输出日志状态 JSON")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    if args.status:
        print(json.dumps(status(), ensure_ascii=False, indent=2))
        return 0
    if args.append:
        print(json.dumps(append_vsa(args.append), ensure_ascii=False, indent=2))
        return 0
    if args.inclusion:
        print(json.dumps(check_inclusion(args.inclusion), ensure_ascii=False, indent=2))
        return 0
    if args.report:
        v = status()
        lines = [
            "# 628 B3 · 透明日志报告（他验三件套 #3）", "",
            "- 日志：`data/transparency_log.jsonl`（append-only）",
            f"- 当前状态：**{v['entries']} 条**，链完整：{v['chain_valid']}",
            f"- 最早条目：{v['first_ts']} · 最新条目：{v['last_ts']}",
            f"- 日志引用凭证文件完整性：{v['files']['ok']}"
            f"（missing={v['files']['missing']} / drifted={v['files']['drifted']}）",
            f"- 未入册凭证：{v['unlogged'] or '无'}",
            f"- 尾部凭证存在性：{v['tail_included']}（index={v['tail_log_index']}）",
            "- 追加幂等：同一凭证（相同 sha256）重复追加为 no-op（不新增条目）",
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
