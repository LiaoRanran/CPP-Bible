#!/usr/bin/env python3
"""614 线C C3：信任根状态统一检查（诚实标注）。

检查六项信任根证据，逐项给出**诚实状态**（绝不把占位/替代证据说成"已锚定"）：
  1. Merkle 根      `data/supply_chain/merkle_roots.json`（E3 信任根）
  2. OTS 时间戳     `data/supply_chain/merkle_roots.json.ots`（pending=占位零 / confirmed=有比特币 attestation）
  3. in-toto link   `data/supply_chain/link_613_verify.json`（standard=非对称签名 / hmac=非标准替代）
  4. tool_integrity `tools/.tool_checksums`
  5. golden lock    `tools/golden_state.json`
  6. governance     `data/governance_docs_manifest.json`

总判定：
  * `fully_anchored`    = OTS confirmed **且** in-toto standard
  * `partially_anchored`= 证据齐备但有 pending / HMAC 替代
  * `untrusted`         = 核心文件缺失

CLI：
  python tools/trust_root_status_check.py [--out data/trust_root_status_614.md] [--json]
  python tools/trust_root_status_check.py --check      # 自验证（exit 0=通过）

铁律：只读检查，绝不修改任何信任根文件；不臆造"已锚定/已签名"。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import opentimestamps_anchor as ots  # noqa: E402

MERKLE = ROOT / "data" / "supply_chain" / "merkle_roots.json"
OTS_FILE = ROOT / "data" / "supply_chain" / "merkle_roots.json.ots"
LINK = ROOT / "data" / "supply_chain" / "link_613_verify.json"
CHECKSUMS = ROOT / "tools" / ".tool_checksums"
GOLDEN = ROOT / "tools" / "golden_state.json"
GOV_MANIFEST = ROOT / "data" / "governance_docs_manifest.json"
OUT = ROOT / "data" / "trust_root_status_614.md"

#: in-toto 标准（非对称）签名 scheme；含 hmac / not-in-toto 一律视为非标准
STANDARD_SCHEMES = ("ed25519", "rsa", "ecdsa")


def scheme_standard(scheme: str | None) -> bool:
    if not scheme:
        return False
    s = scheme.lower()
    if "hmac" in s or "not-in-toto" in s:
        return False
    return any(s.startswith(k) for k in STANDARD_SCHEMES)


def ots_pending(parsed: dict) -> bool:
    """attestation 段是否仍是占位零（未上链）。"""
    return bool(parsed.get("attestation_pending", True))


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def collect() -> dict:
    sec: dict[str, dict] = {}

    # 1) Merkle 根
    if MERKLE.is_file():
        sec["merkle_root"] = {"exists": True, "path": MERKLE.relative_to(ROOT).as_posix(),
                              "sha256": sha256_file(MERKLE)}
    else:
        sec["merkle_root"] = {"exists": False, "path": MERKLE.relative_to(ROOT).as_posix()}

    # 2) OTS
    if OTS_FILE.is_file():
        try:
            parsed = ots.parse_ots(OTS_FILE.read_bytes())
            sec["ots"] = {"exists": True, "path": OTS_FILE.relative_to(ROOT).as_posix(),
                          "bytes": OTS_FILE.stat().st_size, "pending": ots_pending(parsed),
                          "kind": parsed.get("attestation_kind"),
                          "digest": parsed.get("file_digest")}
        except ValueError as exc:
            sec["ots"] = {"exists": True, "path": OTS_FILE.relative_to(ROOT).as_posix(),
                          "pending": True, "error": str(exc)}
    else:
        sec["ots"] = {"exists": False, "path": OTS_FILE.relative_to(ROOT).as_posix()}

    # 3) in-toto link
    if LINK.is_file():
        try:
            d = cast("dict[str, Any]", json.loads(LINK.read_text(encoding="utf-8")))
            scheme = (d.get("signature") or {}).get("scheme")
            sec["in_toto_link"] = {"exists": True, "path": LINK.relative_to(ROOT).as_posix(),
                                   "scheme": scheme, "standard": scheme_standard(scheme)}
        except (ValueError, TypeError) as exc:
            sec["in_toto_link"] = {"exists": True, "path": LINK.relative_to(ROOT).as_posix(),
                                   "scheme": None, "standard": False, "error": str(exc)}
    else:
        sec["in_toto_link"] = {"exists": False, "path": LINK.relative_to(ROOT).as_posix()}

    # 4) tool_integrity / 5) golden / 6) governance（存在性）
    sec["tool_integrity"] = {"exists": CHECKSUMS.is_file(),
                             "path": CHECKSUMS.relative_to(ROOT).as_posix()}
    sec["golden_lock"] = {"exists": GOLDEN.is_file(),
                          "path": GOLDEN.relative_to(ROOT).as_posix()}
    sec["governance"] = {"exists": GOV_MANIFEST.is_file(),
                         "path": GOV_MANIFEST.relative_to(ROOT).as_posix()}
    return sec


def overall(sec: dict) -> str:
    core_ok = all(sec[k]["exists"] for k in ("merkle_root", "tool_integrity", "golden_lock", "governance"))
    if not core_ok:
        return "untrusted"
    ots_ok = sec["ots"].get("exists") and not sec["ots"].get("pending", True)
    link_ok = sec["in_toto_link"].get("exists") and bool(sec["in_toto_link"].get("standard"))
    return "fully_anchored" if (ots_ok and link_ok) else "partially_anchored"


def render(sec: dict, verdict: str) -> str:
    def yn(b: bool) -> str:
        return "✅" if b else "❌"

    ots_s = sec["ots"]
    ots_label = ("❌ 缺失" if not ots_s.get("exists") else
                 ("⚠ pending（占位零，未上链）" if ots_s.get("pending", True) else "✅ confirmed（有比特币 attestation）"))
    link_s = sec["in_toto_link"]
    link_label = ("❌ 缺失" if not link_s.get("exists") else
                  ("✅ standard（非对称签名）" if link_s.get("standard") else
                   f"⚠ 非标准替代（scheme={link_s.get('scheme')}）"))
    verdict_label = {"fully_anchored": "✅ fully_anchored（完全锚定）",
                     "partially_anchored": "⚠ partially_anchored（部分锚定：存在 pending/HMAC 替代）",
                     "untrusted": "❌ untrusted（核心文件缺失）"}[verdict]
    L = ["# 614 · 信任根状态（诚实标注）", "",
         f"> 生成：`python tools/trust_root_status_check.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 只读检查；**绝不**把占位/替代证据说成已锚定。", "",
         "## 一、逐项状态", "",
         "| # | 证据 | 存在 | 诚实状态 |", "|---|---|---|---|",
         f"| 1 | Merkle 根 | {yn(sec['merkle_root']['exists'])} | "
         f"`{sec['merkle_root'].get('sha256', '-')}` |",
         f"| 2 | OTS 时间戳 | {yn(ots_s.get('exists', False))} | {ots_label} |",
         f"| 3 | in-toto link | {yn(link_s.get('exists', False))} | {link_label} |",
         f"| 4 | tool_integrity | {yn(sec['tool_integrity']['exists'])} | `tools/.tool_checksums` |",
         f"| 5 | golden lock | {yn(sec['golden_lock']['exists'])} | `tools/golden_state.json` |",
         f"| 6 | governance | {yn(sec['governance']['exists'])} | `data/governance_docs_manifest.json` |",
         "", "## 二、总判定", "", f"- {verdict_label}", "",
         "## 三、能力边界（诚实）", "",
         f"- OTS：{ots_label} ⇒ "
         + ("可证「.ots 绑定此摘要」，**不能**证「某时刻已存在」。"
            if ots_s.get("pending", True) else "已含比特币 attestation（仍需人/监工核验来源）。"),
         f"- in-toto：{link_label} ⇒ "
         + ("完整性 + 持有证明；**无**公钥可验/非否认。"
            if not link_s.get("standard") else "非对称可验（公钥）。"),
         "", "> 真上链 / 真签名仍为**交人项**（见 `data/ots_real_chain_evaluation_614.md`、"
         "`data/in_toto_real_signing_evaluation_614.md`）。"]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    # OTS pending 分类
    if not ots_pending({"attestation_pending": True}):
        problems.append("占位 attestation 应判 pending")
    if ots_pending({"attestation_pending": False}):
        problems.append("非占位 attestation 不应判 pending")
    # scheme 分类
    if scheme_standard("hmac-sha256-not-in-toto-standard"):
        problems.append("HMAC scheme 不应判 standard")
    if not scheme_standard("ed25519"):
        problems.append("ed25519 应判 standard")
    # 总判定
    fake_sec = {"merkle_root": {"exists": True}, "tool_integrity": {"exists": True},
                "golden_lock": {"exists": True}, "governance": {"exists": True},
                "ots": {"exists": True, "pending": True},
                "in_toto_link": {"exists": True, "standard": False}}
    if overall(fake_sec) != "partially_anchored":
        problems.append("pending+HMAC 应判 partially_anchored")
    fake_sec["ots"]["pending"] = False
    fake_sec["in_toto_link"]["standard"] = True
    if overall(fake_sec) != "fully_anchored":
        problems.append("confirmed+standard 应判 fully_anchored")
    fake_sec["merkle_root"]["exists"] = False
    if overall(fake_sec) != "untrusted":
        problems.append("核心缺失应判 untrusted")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 C3 信任根状态统一检查")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print("[trust] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print("[trust] ✅ 自验证通过：OTS pending 分类 / scheme standard 分类 / 总判定 均一致")
        return 0

    sec = collect()
    verdict = overall(sec)
    if a.json:
        print(json.dumps({"sections": sec, "verdict": verdict}, ensure_ascii=False, indent=1))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(sec, verdict), encoding="utf-8", newline="\n")
    print(f"[trust] 已生成：{out} ｜ 总判定：{verdict}"
          f"（OTS pending={sec['ots'].get('pending')} / in-toto standard={sec['in_toto_link'].get('standard')}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
