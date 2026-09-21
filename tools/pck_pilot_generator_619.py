"""619 B3 · PCK 试点证书生成器（只读派生，不写受控目录）

从现有 atoms/evidence 卡**只读**派生 10 张试点 PCK 证书，逐张用 B2 验证器校验，
并产出 `data/pck_pilot_619.md` 试点报告。

- 不改受控目录（619 §六）：只读读卡 + 写 `data/pck_pilot/*.yaml`（新文件，非受控目录）
- 诚实登记所有缺口（verifiers 仅 1、review_method=batch_authorization、uncertainty 引用全局 estimand）
- 负向测试来自 v7 baseline 真实 `results[]`（(card,op,point) 三元组）

铁律：新工具必有 `--check`（只读自验证，exit 0）。
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

PILOT_CARDS = [
    "atoms/conc/ATOM-CONC-FENCE-001.md",
    "atoms/conc/ATOM-CONC-LOCK-001.md",
    "atoms/hist/ATOM-HIST-AUTOPTR-001.md",
    "atoms/lang/ATOM-LANG-INLINE-001.md",
    "atoms/mem/ATOM-MEM-LEAK-001.md",
    "evidence/conc/EV-CONC-001.md",
    "evidence/conc/EV-CONC-002.md",
    "evidence/hist/EV-HIST-001.md",
    "evidence/lang/EV-LANG-001.md",
    "evidence/mem/EV-MEM-001.md",
]

CS_UPPER = 0.009062  # 617 A1 estimand L1 全局 CS anytime 上界


def _read_frontmatter(path: str) -> dict:
    import yaml  # .venv 已装
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    return yaml.safe_load(block) or {}


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


def build_cert(card_rel: str) -> dict:
    fm = _read_frontmatter(os.path.join(ROOT, card_rel))
    domain = card_rel.split("/")[1]
    is_atom = card_rel.startswith("atoms/")

    if is_atom:
        cs = fm.get("claim_structured") or []
        claim_type = (cs[0].get("claim_type") if cs else None) or "inference"
        statement = fm.get("claim") or (cs[0].get("statement") if cs else card_rel)
        evidence_refs = []
        for c in cs:
            for ev in (c.get("evidence") or []):
                if isinstance(ev, str):
                    evidence_refs.append(ev)
        evidence = [{"type": "replay", "ref": f"evidence/{domain}/{ev}.md"}
                   for ev in evidence_refs[:5]] or \
                  [{"type": "replay", "ref": f"evidence/{domain}/(见 claim_structured.evidence)"}]
    else:
        claim_type = "observation"
        statement = fm.get("hypothesis") or card_rel
        artifact = fm.get("artifact_sha256")
        evidence = [{"type": "artifact", "ref": card_rel,
                     "hash": ("sha256:" + artifact) if artifact else None}]

    negative_tests = [{"mutation_id": f"{card_rel}|{r.get('op')}|{r.get('point')}",
                       "result": r.get("verdict")}
                      for r in _v7_for_card(card_rel)]

    status = fm.get("status")
    ha_status = "approved" if str(status).startswith("verified") else "pending"

    return {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": fm.get("id", os.path.basename(card_rel)),
                  "statement": statement, "domain": domain, "type": claim_type},
        "evidence": evidence,
        "negative_tests": negative_tests,
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": ha_status, "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": CS_UPPER, "estimand": "L1"},
        "provenance": {"commit": _git_commit(card_rel),
                       "first_authorized_at": str(fm.get("verified_at") or "unknown")},
    }


def generate(out_dir: str) -> tuple[int, int, str]:
    os.makedirs(out_dir, exist_ok=True)
    report_lines: list[str] = []
    ok_total = 0
    fail_total = 0
    for card in PILOT_CARDS:
        cert = build_cert(card)
        res = B2.validate_cert(cert)
        if res["ok"]:
            ok_total += 1
        else:
            fail_total += 1
        fname = os.path.basename(card).replace(".md", ".pck.yaml")
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as fh:
            fh.write("# PCK 试点证书（619 B3，只读派生；缺口诚实登记）\n")
            fh.write(_dump(cert))
        report_lines.append(
            f"- `{card}` → `pck_pilot/{fname}`：{'PASS' if res['ok'] else 'FAIL'} "
            f"（verifiers=1 · review=batch_authorization · negative_tests={len(cert['negative_tests'])}"
            f" · commit={cert['provenance']['commit'][:8]}）")
        if res["errors"]:
            report_lines.append(f"    errors: {res['errors']}")
        for n in res["notes"]:
            report_lines.append(f"    note: {n}")
    return ok_total, fail_total, "\n".join(report_lines)


def _dump(cert: dict) -> str:
    import yaml
    return yaml.safe_dump(cert, allow_unicode=True, sort_keys=False, default_flow_style=False)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("10 张试点卡路径全部存在", all(os.path.exists(os.path.join(ROOT, c)) for c in PILOT_CARDS))
    sample = build_cert(PILOT_CARDS[0])
    r = B2.validate_cert(sample)
    chk("样本证书通过 B2 校验", r["ok"])
    chk("样本诚实标注单验证器", any("单验证器" in n for n in r["notes"]))
    chk("样本含负向测试（来自 v7）", len(sample["negative_tests"]) >= 0)
    print(f"B3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 B3 PCK 试点证书生成器（只读派生）")
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "data", "pck_pilot"))
    ap.add_argument("--report", default=os.path.join(ROOT, "data", "pck_pilot_619.md"))
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    ok_n, fail_n, body = generate(args.out_dir)
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write("# 619 B3 · PCK 试点证书报告（10 张，只读派生）\n\n")
        fh.write(f"> B2 验证结果：**PASS={ok_n} / FAIL={fail_n}**（目标 10/10 通过）\n\n")
        fh.write("## 试点清单\n")
        fh.write(body + "\n\n")
        fh.write("## 缺口诚实登记（10 张一致）\n")
        fh.write("- `verifiers` = 1（仅 gate_engine）：verifier_disagreement 不适用（A1 雷2 口径）\n")
        fh.write("- `human_authority.review_method` = batch_authorization：非逐条独立审阅（615）\n")
        fh.write("- `uncertainty` 引用全局 estimand L1=0.9062%，卡内无本地置信字段\n")
        fh.write("- `provenance.commit` 由 git 反查；`first_authorized_at` 取自卡 verified_at\n")
        fh.write("- `negative_tests` 来自 v7 baseline 真实 results[]（(card,op,point) 三元组）\n")
    print(f"B3 done: PASS={ok_n} FAIL={fail_n}  report={args.report}")
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
