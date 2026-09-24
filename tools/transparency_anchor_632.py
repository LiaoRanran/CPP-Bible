"""632 B1 · 透明日志外部锚定（纯标准库，默认只读安全的 --check）。

把 `data/transparency_log.jsonl` 整份算 SHA256，写锚到 `data/vsa/anchor_<YYYYMMDD>.json`
（含 log_sha256 + 锚定时间 + 外部可验证位置指引）。外部锚定（公开 gist / 链上 txid）
需网络与人工，故默认写「LOCAL_ONLY」锚并提供发布指引；`--external <url/txid>` 可填入。

铁律：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
LOG_PATH = REPO_ROOT / "data" / "transparency_log.jsonl"
VSA_DIR = REPO_ROOT / "data" / "vsa"


def compute_log_hash(log_path: Path) -> str:
    """整份日志字节的 SHA256（规范化：直接对原始字节哈希）。"""
    return hashlib.sha256(Path(log_path).read_bytes()).hexdigest()


def entry_count(log_path: Path) -> int:
    n = 0
    with open(log_path, "rb") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def latest_anchor(vsa_dir: Path = VSA_DIR) -> Path | None:
    anchors = sorted(Path(vsa_dir).glob("anchor_*.json"))
    return anchors[-1] if anchors else None


def write_anchor(log_path: Path = LOG_PATH, vsa_dir: Path = VSA_DIR,
                 external: dict | None = None) -> Path:
    h = compute_log_hash(log_path)
    cnt = entry_count(log_path)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    out = Path(vsa_dir) / f"anchor_{stamp}.json"
    rec = {
        "tool": "transparency_anchor_632.py",
        "log_path": (str(log_path.relative_to(REPO_ROOT))
                     if Path(log_path).is_absolute() else str(log_path)),
        "log_sha256": h,
        "entry_count": cnt,
        "anchored_at": datetime.now(timezone.utc).isoformat(),
        "external": external or {
            "status": "LOCAL_ONLY",
            "note": "外部锚定（公开 gist / 链上 txid）待人工执行；本文件提供可验证哈希。",
            "suggested": ("将 log_sha256 发布到公开可验证位置（GitHub gist / OpenTimestamps / "
                         "以太坊 tx calldata），把返回的 URL/txid 填入 external.location。"),
        },
        "verify": "python tools/transparency_anchor_632.py --check",
    }
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def verify_anchor(log_path: Path = LOG_PATH, vsa_dir: Path = VSA_DIR) -> bool:
    a = latest_anchor(vsa_dir)
    if not a:
        return False
    rec = json.loads(Path(a).read_text(encoding="utf-8"))
    return rec.get("log_sha256") == compute_log_hash(log_path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 B1 透明日志外部锚定")
    ap.add_argument("--check", action="store_true", help="只读验证锚与日志一致，exit 0")
    ap.add_argument("--external", default=None, help="外部可验证位置 URL/txid（可选）")
    ap.add_argument("--log", default=str(LOG_PATH))
    ap.add_argument("--vsa-dir", default=str(VSA_DIR))
    args = ap.parse_args(argv)
    log, vsa = Path(args.log), Path(args.vsa_dir)
    if args.check:
        ok = verify_anchor(log, vsa)
        print("632 B1 --check:", "OK 锚与日志一致" if ok else "FAIL 锚与日志不一致（日志已变或被篡改）")
        return 0 if ok else 1
    out = write_anchor(log, vsa,
                       {"status": "PROVIDED", "location": args.external} if args.external else None)
    print("已写锚:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
