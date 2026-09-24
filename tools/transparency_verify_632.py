"""632 B2 · 透明日志完整性校验（纯标准库，默认只读 --check）。

校验 `data/transparency_log.jsonl`：
1. 哈希链自洽：log_index 连续 0..n-1；第 i 条 `prev_log_hash` == 第 i-1 条 `entry_hash`；
   首条 `prev_log_hash == "GENESIS"`；`entry_hash` 为 64 位十六进制。
2. 锚一致：复用 B1 的 `verify_anchor`（锚中 log_sha256 == 当前日志 SHA256）。

注：逐条 `entry_hash` 的完整重算需日志写入器的规范化序列化公式（不在本工具内），
故 B2 以「链环衔接 + 索引连续 + 锚一致」作为完整性判据（与 E2 公钥第三方可验互补）。

铁律：纯标准库、必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
LOG_PATH = REPO_ROOT / "data" / "transparency_log.jsonl"
VSA_DIR = REPO_ROOT / "data" / "vsa"

# 复用 B1 的锚校验（同仓 tools/ 已在 sys.path）
sys.path.insert(0, str(HERE))
from transparency_anchor_632 import verify_anchor  # noqa: E402


def load_entries(log_path: Path) -> list[dict]:
    out = []
    for line in Path(log_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _is_hash(h: str) -> bool:
    return isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)


def verify_chain(entries: list[dict]) -> list[str]:
    """返回错误列表（空 = 自洽）。"""
    errs: list[str] = []
    for i, e in enumerate(entries):
        if e.get("log_index") != i:
            errs.append(f"[{i}] log_index 应为 {i}，实际 {e.get('log_index')}")
        h = e.get("entry_hash", "")
        if not _is_hash(h):
            errs.append(f"[{i}] entry_hash 非 64 位十六进制：{h!r}")
        prev = e.get("prev_log_hash", "")
        if i == 0:
            if prev != "GENESIS":
                errs.append(f"[0] 首条 prev_log_hash 应为 GENESIS，实际 {prev!r}")
        else:
            if prev != entries[i - 1].get("entry_hash"):
                errs.append(f"[{i}] prev_log_hash 不等于上一条 entry_hash")
    return errs


def verify(log_path: Path = LOG_PATH, vsa_dir: Path = VSA_DIR) -> tuple[list[str], bool]:
    """返回 (链错误列表, 锚是否一致)。"""
    entries = load_entries(log_path)
    errs = verify_chain(entries)
    anchor_ok = verify_anchor(log_path, vsa_dir)
    return errs, anchor_ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 B2 透明日志完整性校验")
    ap.add_argument("--check", action="store_true", help="只读校验，exit 0=通过")
    ap.add_argument("--log", default=str(LOG_PATH))
    ap.add_argument("--vsa-dir", default=str(VSA_DIR))
    args = ap.parse_args(argv)
    log, vsa = Path(args.log), Path(args.vsa_dir)
    errs, anchor_ok = verify(log, vsa)
    if args.check:
        n = len(load_entries(log))
        if not errs and anchor_ok:
            print(f"632 B2 --check OK：{n} 条链自洽，锚一致")
            return 0
        for e in errs:
            print("链错误:", e)
        if not anchor_ok:
            print("锚不一致：锚中哈希与当前日志不符")
        return 1
    # 非 --check 也给出可读报告（不写盘）
    n = len(load_entries(log))
    print(f"条目数: {n}")
    print(f"链自洽: {'OK' if not errs else 'FAIL'}")
    for e in errs:
        print("  -", e)
    print(f"锚一致: {'OK' if anchor_ok else 'FAIL'}")
    return 0 if (not errs and anchor_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
