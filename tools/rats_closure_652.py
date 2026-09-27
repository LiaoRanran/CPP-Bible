#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rats_closure_652.py — T3 闭包 RATS 化（652 D，**三类信任根**）。

为什么（652 D-T3）：IETF **RATS** 架构把信任拆成三类可独立核对的证据：
1. **Reference Values（参考值）**——"预期是什么"：Merkle 根、校验和基准；
2. **Endorsements（背书）**——"谁担保"：OTS 时间戳凭据、VSA 凭证；
3. **Verifier Code（验证器码）**——"用什么验"：CORE_TOOLS + 判决尺子。

本工具把现有信任根（`tool_integrity` 的闭包）**映射成这三库**并出清单，便于外部审查者
按 RATS 术语逐库核对。**只读**：不改信任根、不重钉。

用法
====
    python tools/rats_closure_652.py --check
    python tools/rats_closure_652.py --export      # → data/652_t3_rats_closure.json/md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "trust_asset", "name": "rats_closure_652", "entry": "export_closure",
                "description": "T3 闭包 RATS 化：reference values / endorsements / verifier code 三库"}

OUT_JSON = ROOT / "data" / "652_t3_rats_closure.json"
OUT_MD = ROOT / "data" / "652_t3_rats_closure.md"
CHECKSUMS = ROOT / "tools" / ".tool_checksums"

# 背书类（endorsements）：时间戳/凭证/他验凭据
ENDORSEMENT_GLOBS = ("data/supply_chain/*.ots", "data/authority/*_credential_*.json",
                     "data/authority/*_anchor*.json", "data/ots_anchor_613.md")


@dataclass
class Entry:
    store: str      # reference_values | endorsements | verifier_code
    path: str
    exists: bool
    sha256_16: str | None


def _sha16(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16] if p.is_file() else None


def _checksum_sections() -> dict[str, list[str]]:
    """解析 .tool_checksums 的分节（core/test_config/supply_chain/ruler）。"""
    out: dict[str, list[str]] = {}
    if not CHECKSUMS.is_file():
        return out
    cur = "unknown"
    for ln in CHECKSUMS.read_text(encoding="utf-8", errors="replace").splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#") and s.endswith("test_config"):
            cur = "test_config"
            continue
        if s.startswith("#"):
            m = re.search(r"(core|supply_chain|ruler|merkle)", s)
            if m:
                cur = m.group(1)
            continue
        if s.startswith("#"):
            continue
        path = s.split()[0] if s.split() else ""
        if path:
            out.setdefault(cur, []).append(path)
    return out


def export_closure() -> dict:
    stores: dict[str, list[Entry]] = {"reference_values": [], "endorsements": [], "verifier_code": []}

    # ① Reference Values：Merkle 根 + 校验和台账本身
    for rel in ("data/supply_chain/merkle_roots.json", "tools/.tool_checksums"):
        p = ROOT / rel
        stores["reference_values"].append(Entry("reference_values", rel, p.is_file(), _sha16(p)))

    # ② Verifier Code：CORE_TOOLS + 判决尺子（从 tool_integrity 常量取，取不到则从 checksums 节取）
    core: list[str] = []
    ruler: list[str] = []
    try:
        import tool_integrity as ti  # noqa: PLC0415

        core = [str(x) for x in getattr(ti, "CORE_TOOLS", ())]
        supply = [str(x) for x in getattr(ti, "SUPPLY_CHAIN_FILES", ())]
    except Exception:  # noqa: BLE001
        supply = []
    secs = _checksum_sections()
    if not core:
        core = secs.get("core", [])
    ruler = [x for x in secs.get("ruler", [])]
    for rel in core:
        p = ROOT / "tools" / Path(rel).name if not rel.startswith("tools") else ROOT / rel
        r = str(p.relative_to(ROOT)).replace("\\", "/")
        stores["verifier_code"].append(Entry("verifier_code", r, p.is_file(), _sha16(p)))
    for rel in ruler[:30]:
        p = ROOT / rel if rel.startswith(("tools", "tests")) else ROOT / "tools" / rel
        r = str(p.relative_to(ROOT)).replace("\\", "/")
        stores["verifier_code"].append(Entry("verifier_code", r, p.is_file(), _sha16(p)))
    # supply_chain 数据文件也是"参考值"（豁免台账/Merkle/in-toto layout）
    for rel in supply:
        p = ROOT / rel if not rel.startswith("tools") else ROOT / rel
        r = str(p.relative_to(ROOT)).replace("\\", "/")
        stores["reference_values"].append(Entry("reference_values", r, p.is_file(), _sha16(p)))

    # ③ Endorsements
    seen: set[str] = set()
    for g in ENDORSEMENT_GLOBS:
        for p in sorted(ROOT.glob(g)):
            r = str(p.relative_to(ROOT)).replace("\\", "/")
            if r in seen:
                continue
            seen.add(r)
            stores["endorsements"].append(Entry("endorsements", r, p.is_file(), _sha16(p)))

    return {
        "counts": {k: len(v) for k, v in stores.items()},
        "stores": {k: [asdict(e) for e in v] for k, v in stores.items()},
        "note": "RATS 三库映射：reference_values=预期值(merkle/checksums/豁免台账)；"
                "endorsements=时间戳与凭证；verifier_code=核心工具+尺子。只读，不改信任根。",
    }


def _write(rep: dict) -> None:
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 T3 · 闭包 RATS 化（三库）\n",
             f"- reference_values **{rep['counts']['reference_values']}**｜"
             f"endorsements **{rep['counts']['endorsements']}**｜"
             f"verifier_code **{rep['counts']['verifier_code']}**\n",
             f"> {rep['note']}\n"]
    for store, rows in rep["stores"].items():
        lines += [f"## {store}（{len(rows)}）", "", "| 路径 | 存在 | sha256(16) |", "|---|---|---|"]
        for r in rows:
            lines.append(f"| {r['path']} | {r['exists']} | {r['sha256_16']} |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rep = export_closure()
    chk("三库齐全", set(rep["stores"]) == {"reference_values", "endorsements", "verifier_code"})
    chk("reference_values 非空", rep["counts"]["reference_values"] > 0)
    chk("verifier_code 非空", rep["counts"]["verifier_code"] > 0)
    chk("merkle 根在 reference_values",
        any("merkle_roots" in r["path"] for r in rep["stores"]["reference_values"]))
    chk("core 工具存在", all(r["exists"] for r in rep["stores"]["verifier_code"][:2]))
    print(f"rats_closure_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="652 T3 闭包 RATS 化")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--export", action="store_true")
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    rep = export_closure()
    _write(rep)
    print(f"三库：{rep['counts']}｜→ {OUT_MD.name}")
    raise SystemExit(0)
