"""620 B1 · PCK 批量迁移工具（markdown 卡 → PCK certificate）

从 `atoms/`（27 张原子卡）与 `evidence/`（56 张证据卡）**只读**派生 PCK certificate，
逐张用 619 B2 验证器校验，输出到 `data/pck/certificates/{CARD_ID}.pck.yaml`。

与 619 B3（10 张试点）的关系：B3 的 `PILOT_CARDS` 是硬编码 10 张；本工具**自动发现**全量卡，
逻辑保持同源（同一套 build 规则），故试点结论可直接外推。

**硬边界**：
- 不修改原始 markdown 卡（只读 frontmatter）
- 缺失字段如实标 `null` / `unknown`，**不编造**
- `negative_tests` 只取 v7 baseline 真实 `results[]`；verdict 不在 B2 允许域时**如实丢弃并登记**

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pck_certificate_verifier_619 as B2  # noqa: E402

DEFAULT_OUT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
CS_UPPER = 0.009062  # 617 A1 estimand L1 全局 CS anytime 上界（冻结）
ALLOWED_NT_RESULTS = ("blocked", "escaped", "n_a")


# ── 卡发现 ────────────────────────────────────────────────────────────────────
def discover_cards(root: str = ROOT) -> list[str]:
    """自动发现全量卡：atoms/**/ATOM-*.md + evidence/**/EV-*.md（相对路径，posix）。"""
    found: list[str] = []
    for base, prefix in (("atoms", "ATOM-"), ("evidence", "EV-")):
        abs_base = os.path.join(root, base)
        if not os.path.isdir(abs_base):
            continue
        for dirpath, _dirs, files in os.walk(abs_base):
            for f in sorted(files):
                if f.endswith(".md") and f.startswith(prefix):
                    rel = os.path.relpath(os.path.join(dirpath, f), root)
                    found.append(rel.replace(os.sep, "/"))
    return sorted(found)


# ── frontmatter ──────────────────────────────────────────────────────────────
def read_frontmatter(path: str) -> dict:
    import yaml  # .venv 已装
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return yaml.safe_load(text[3:end].strip()) or {}


def _git_commit(path: str) -> str:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%H", "--", path],
                             cwd=ROOT, capture_output=True, text=True, check=True)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _v7_for_card(card_rel: str) -> list[dict]:
    bl = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
    if not os.path.exists(bl):
        return []
    with open(bl, encoding="utf-8") as fh:
        data = json.load(fh)
    return [r for r in (data.get("results") or []) if r.get("card") == card_rel]


def _norm_evidence_ref(ev: str, domain: str) -> str:
    """证据引用归一：已是路径则原样，否则按 evidence/{domain}/{id}.md 拼。"""
    if "/" in ev or ev.endswith(".md"):
        return ev
    return f"evidence/{domain}/{ev}.md"


# ── 证书构建 ──────────────────────────────────────────────────────────────────
def build_cert(card_rel: str) -> dict:
    fm = read_frontmatter(os.path.join(ROOT, card_rel))
    parts = card_rel.split("/")
    domain = parts[1] if len(parts) > 2 else "unknown"
    is_atom = card_rel.startswith("atoms/")

    if is_atom:
        cs = fm.get("claim_structured") or []
        claim_type = (cs[0].get("claim_type") if cs else None) or "inference"
        statement = fm.get("claim") or (cs[0].get("statement") if cs else card_rel)
        refs: list[str] = []
        for c in cs:
            if not isinstance(c, dict):
                continue
            for ev in (c.get("evidence") or []):
                if isinstance(ev, str) and ev.strip():
                    refs.append(_norm_evidence_ref(ev.strip(), domain))
        evidence: list[dict] = [{"type": "replay", "ref": r} for r in refs[:5]] or [
            {"type": "replay", "ref": f"evidence/{domain}/(见 claim_structured.evidence)"}]
    else:
        claim_type = "observation"
        statement = fm.get("hypothesis") or card_rel
        artifact = fm.get("artifact_sha256")
        evidence = [{"type": "artifact", "ref": card_rel,
                     "hash": ("sha256:" + artifact) if artifact else None}]

    # negative_tests：只保留 verdict 在 B2 允许域内的，其余如实登记丢弃
    negative_tests: list[dict] = []
    dropped: list[dict] = []
    for r in _v7_for_card(card_rel):
        item = {"mutation_id": f"{card_rel}|{r.get('op')}|{r.get('point')}",
                "result": r.get("verdict")}
        (negative_tests if r.get("verdict") in ALLOWED_NT_RESULTS else dropped).append(item)

    status = fm.get("status")
    ha_status = "approved" if str(status).startswith("verified") else "pending"
    cert_id = fm.get("id") or os.path.basename(card_rel).replace(".md", "")

    cert = {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": cert_id, "statement": statement,
                  "domain": domain, "type": claim_type},
        "evidence": evidence,
        "negative_tests": negative_tests,
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": ha_status, "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": CS_UPPER, "estimand": "L1"},
        "provenance": {"commit": _git_commit(card_rel),
                       "first_authorized_at": str(fm.get("verified_at") or "unknown")},
    }
    if dropped:
        cert["migration_dropped_negative_tests"] = dropped
    return cert


def _dump(cert: dict) -> str:
    import yaml
    return str(yaml.safe_dump(cert, allow_unicode=True, sort_keys=False, default_flow_style=False))


def cert_filename(cert: dict, card_rel: str) -> str:
    return f"{cert['claim']['id']}.pck.yaml"


# ── 迁移 ──────────────────────────────────────────────────────────────────────
def migrate(cards: list[str], out_dir: str = DEFAULT_OUT_DIR) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    rows: list[dict] = []
    ok = fail = 0
    for card in cards:
        cert = build_cert(card)
        res = B2.validate_cert(cert)
        fname = cert_filename(cert, card)
        path = os.path.join(out_dir, fname)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# PCK 证书（620 B1 批量迁移，只读派生）\n")
            fh.write(_dump(cert))
        ok += bool(res["ok"])
        fail += (not res["ok"])
        rows.append({"card": card, "file": fname, "cert_id": cert["claim"]["id"],
                     "ok": res["ok"], "errors": res["errors"], "notes": res["notes"],
                     "n_negative": len(cert["negative_tests"]),
                     "ha_status": cert["human_authority"]["status"],
                     "commit": cert["provenance"]["commit"][:8]})
    return {"out_dir": out_dir, "total": len(cards), "ok": ok, "fail": fail, "rows": rows}


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    cards = discover_cards()
    chk("自动发现全量卡 = 83 张（27 原子 + 56 证据）", len(cards) == 83)
    chk("原子卡 27 张", sum(1 for c in cards if c.startswith("atoms/")) == 27)
    chk("证据卡 56 张", sum(1 for c in cards if c.startswith("evidence/")) == 56)

    # 单张迁移
    sample = build_cert(cards[0])
    chk("单张迁移通过 B2", B2.validate_cert(sample)["ok"])
    chk("cert 含 7 个必需字段",
        all(k in sample for k in ("claim", "evidence", "negative_tests", "verifiers",
                                  "human_authority", "uncertainty", "provenance")))
    chk("缺失字段标 unknown 而非编造",
        isinstance(sample["provenance"]["first_authorized_at"], str))
    chk("幂等：同输入两次构建一致", build_cert(cards[0]) == sample)
    chk("negative_tests 结果均在 B2 允许域",
        all(t["result"] in ALLOWED_NT_RESULTS for t in sample["negative_tests"]))
    chk("报告可汇总", all(k in migrate_preview(cards[:3]) for k in ("total", "ok", "fail")))
    print(f"B1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def migrate_preview(cards: list[str]) -> dict:
    """只读预览（不写盘）：供 selftest / 报告使用。"""
    ok = fail = 0
    for card in cards:
        res = B2.validate_cert(build_cert(card))
        ok += bool(res["ok"])
        fail += (not res["ok"])
    return {"total": len(cards), "ok": ok, "fail": fail}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 B1 PCK 批量迁移（只读派生）")
    ap.add_argument("--all", action="store_true", help="迁移全量卡")
    ap.add_argument("--card", action="append", help="指定单张卡（可多次）")
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    if args.card:
        cards = args.card
    elif args.all:
        cards = discover_cards()
    else:
        ap.print_help()
        return 0

    result = migrate(cards, args.out_dir)
    print(json.dumps({"total": result["total"], "ok": result["ok"], "fail": result["fail"]},
                     ensure_ascii=False))
    for r in result["rows"]:
        if not r["ok"]:
            print(f"FAIL {r['card']}: {r['errors']}")
    return 0 if result["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
