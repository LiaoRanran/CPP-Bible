#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pck_export_652.py — T7 知识 manifest 导出（652 D，PCK → C2PA/in-toto 兼容）。

为什么（652 D-T7）：PCK 证书是自研格式，外部审查者要学新词。T7 把每张 PCK 证书导出成
**两个业界标准形态**（映射见 `docs/pck_c2pa_mapping.md`）：
- **in-toto link**：`materials`（= evidence 引用+哈希）、`products`、`command`、`byproducts`；
- **C2PA 形态**：`claim.assertions[]`，其中 evidence 哈希落为 **硬绑定** `c2pa.hash.data`。

**只读**：不改 PCK 证书。导出物是**派生视图**（可重新生成，非信任根）。

用法
====
    python tools/pck_export_652.py --check
    python tools/pck_export_652.py --export      # → data/652_t7_pck_export.json/md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "pck_export_652", "entry": "export_all",
                "description": "T7 PCK 证书导出为 in-toto link + C2PA 断言（硬绑定,只读派生）"}

PCK_DIR = ROOT / "data" / "pck" / "certificates"
OUT_JSON = ROOT / "data" / "652_t7_pck_export.json"
OUT_MD = ROOT / "data" / "652_t7_pck_export.md"


def _sha256_file(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def to_intoto_link(cert: dict) -> dict:
    """PCK → in-toto link（materials=证据引用哈希；byproducts=否定测试/人审）。"""
    claim = cert.get("claim", {}) or {}
    ev = cert.get("evidence", []) or []
    materials = {}
    for e in ev:
        ref = e.get("ref")
        if ref:
            materials[ref] = (e.get("hash") or "").replace("sha256:", "")
    return {
        "_type": "link",
        "name": claim.get("id"),
        "materials": materials,
        "products": {},
        "command": "pck:export_652",
        "byproducts": {
            "negative_tests": cert.get("negative_tests", []),
            "verifiers": cert.get("verifiers", []),
            "human_authority": cert.get("human_authority", {}),
            "uncertainty": cert.get("uncertainty", {}),
            "provenance": cert.get("provenance", {}),
        },
    }


def to_c2pa(cert: dict) -> dict:
    """PCK → C2PA 形态断言集；evidence 哈希落为硬绑定 c2pa.hash.data。"""
    claim = cert.get("claim", {}) or {}
    assertions: list[dict] = [
        {"label": "c2pa.claim", "data": {"id": claim.get("id"), "statement": claim.get("statement"),
                                         "domain": claim.get("domain"), "type": claim.get("type")}},
    ]
    for e in cert.get("evidence", []) or []:
        h = (e.get("hash") or "").replace("sha256:", "")
        if h:
            assertions.append({"label": "c2pa.hash.data",
                               "data": {"url": e.get("ref"), "hash": h, "alg": "sha256"}})
    if cert.get("expiry"):
        assertions.append({"label": "c2pa.expiration", "data": {"expiry": cert["expiry"]}})
    return {"claim_generator": "pck-export-652", "schema_version": cert.get("schema_version"),
            "assertions": assertions}


def _load_cert(p: Path) -> dict | None:
    try:
        import yaml

        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else None
    except Exception:  # noqa: BLE001
        return None


def export_all() -> dict:
    certs = sorted(PCK_DIR.glob("*.yaml")) + sorted(PCK_DIR.glob("*.yml"))
    rows: list[dict] = []
    failed = 0
    for p in certs:
        cert = _load_cert(p)
        if cert is None:
            failed += 1
            rows.append({"certificate": p.name, "error": "parse_failed"})
            continue
        link = to_intoto_link(cert)
        c2pa = to_c2pa(cert)
        # 硬绑定一致性：C2PA hash.data 与 in-toto materials 必须逐条对应
        hard = [(a["data"]["url"], a["data"]["hash"]) for a in c2pa["assertions"]
                if a["label"] == "c2pa.hash.data"]
        consistent = all(link["materials"].get(u) == h for u, h in hard)
        rows.append({"certificate": p.name, "claim_id": link["name"],
                     "materials": len(link["materials"]), "hard_bindings": len(hard),
                     "binding_consistent": consistent,
                     "intoto": link, "c2pa": c2pa,
                     "cert_sha256_16": (_sha256_file(p) or "")[:16]})
    return {"certificates": len(certs), "exported": len(certs) - failed, "failed": failed, "rows": rows}


def _write(rep: dict) -> None:
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 T7 · PCK → C2PA/in-toto 导出（只读派生视图）\n",
             f"- 证书 {rep['certificates']}｜导出 {rep['exported']}｜失败 {rep['failed']}\n",
             "| 证书 | claim.id | materials | 硬绑定 | 绑定一致 |", "|---|---|---|---|---|"]
    for r in rep["rows"]:
        lines.append(f"| {r['certificate']} | {r.get('claim_id')} | {r.get('materials')} | "
                     f"{r.get('hard_bindings')} | {r.get('binding_consistent')} |")
    lines.append("\n> evidence 哈希 = C2PA 硬绑定 `c2pa.hash.data`；导出物可重生成，非信任根。")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    cert = {"schema_version": "619-pck-v1",
            "claim": {"id": "ATOM-X", "statement": "s", "domain": "d", "type": "observation"},
            "evidence": [{"type": "replay", "ref": "evidence/a.md", "hash": "sha256:abc"}],
            "verifiers": [{"name": "gate_engine", "result": "pass"}],
            "human_authority": {"status": "pending", "review_method": "batch_authorization"}}
    link = to_intoto_link(cert)
    chk("in-toto materials 取自证据", link["materials"] == {"evidence/a.md": "abc"})
    c2pa = to_c2pa(cert)
    hard = [a for a in c2pa["assertions"] if a["label"] == "c2pa.hash.data"]
    chk("C2PA 硬绑定 1 条", len(hard) == 1 and hard[0]["data"]["hash"] == "abc")
    chk("硬绑定与 materials 一致", link["materials"]["evidence/a.md"] == hard[0]["data"]["hash"])
    rep = export_all()
    chk("导出可跑（≥0 证书）", rep["certificates"] >= 0)
    print(f"pck_export_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="652 T7 PCK → C2PA/in-toto 导出")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--export", action="store_true")
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    rep = export_all()
    _write(rep)
    print(f"证书 {rep['certificates']}｜导出 {rep['exported']}｜→ {OUT_MD.name}")
    raise SystemExit(0)
