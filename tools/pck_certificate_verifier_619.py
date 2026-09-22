"""619 B2 · PCK 证书验证器 v1（结构诚实性校验）

只读校验 `data/pck_certificate_schema_619.md` 定义的证书结构。**不代替真实门禁**判 pass/fail
（619 §六），只验证「字段齐备 + 类型合法 + 诚实缺口显式登记」。

铁律：新工具必有 `--check`（只读自验证，exit 0）。

依赖：优先 `import yaml`（.venv 已装 PyYAML）；缺失时退回 `json`（仅能解析 JSON 形态证书）。
"""
from __future__ import annotations

import argparse
import json
import sys

SCHEMA_VERSION = "619-pck-v1"
CLAIM_TYPES = ("inference", "observation")
EVIDENCE_TYPES = ("replay", "artifact", "url", "standard")
VERIFY_RESULTS = ("pass", "fail", "n_a")
AUTH_STATUS = ("pending", "approved", "rejected")
ESTIMANDS = ("L1", "L2", "L3")


def load_cert(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


def validate_cert(cert: object) -> dict:
    """返回 {'ok': bool, 'errors': [...], 'notes': [...]}。

    errors = 结构硬错误（必填缺失/类型非法）⇒ ok=False
    notes  = 诚实注释（单验证器 / batch_authorization），不报错，只登记
    """
    errors: list[str] = []
    notes: list[str] = []

    if not isinstance(cert, dict):
        return {"ok": False, "errors": ["certificate 顶层必须是 mapping"], "notes": []}

    if cert.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version 必须是 {SCHEMA_VERSION}，实际 {cert.get('schema_version')!r}")

    claim = cert.get("claim")
    if not isinstance(claim, dict):
        errors.append("claim 缺失或非 mapping")
    else:
        for f in ("id", "statement", "domain", "type"):
            if not str(claim.get(f, "")).strip():
                errors.append(f"claim.{f} 缺失或空")
        if claim.get("type") not in CLAIM_TYPES:
            errors.append(f"claim.type 必须是 {CLAIM_TYPES}，实际 {claim.get('type')!r}")

    evidence = cert.get("evidence")
    if not isinstance(evidence, list) or len(evidence) == 0:
        errors.append("evidence 必须是非空数组")
    else:
        for i, e in enumerate(evidence):
            if not isinstance(e, dict) or not str(e.get("ref", "")).strip():
                errors.append(f"evidence[{i}] 缺失 ref")
            elif e.get("type") not in EVIDENCE_TYPES:
                errors.append(f"evidence[{i}].type 必须是 {EVIDENCE_TYPES}")

    if "negative_tests" in cert:
        nt = cert["negative_tests"]
        if not isinstance(nt, list):
            errors.append("negative_tests 必须是数组")
        else:
            for i, t in enumerate(nt):
                if not isinstance(t, dict) or not str(t.get("mutation_id", "")).strip():
                    errors.append(f"negative_tests[{i}] 缺失 mutation_id")
                elif t.get("result") not in ("blocked", "escaped", "n_a"):
                    errors.append(f"negative_tests[{i}].result 非法")

    verifiers = cert.get("verifiers")
    if not isinstance(verifiers, list) or len(verifiers) == 0:
        errors.append("verifiers 必须是非空数组")
    else:
        for i, v in enumerate(verifiers):
            if not isinstance(v, dict) or not str(v.get("name", "")).strip():
                errors.append(f"verifiers[{i}] 缺失 name")
            elif v.get("result") not in VERIFY_RESULTS:
                errors.append(f"verifiers[{i}].result 必须是 {VERIFY_RESULTS}")
        if len(verifiers) == 1:
            notes.append("单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）")

    ha = cert.get("human_authority")
    if not isinstance(ha, dict):
        errors.append("human_authority 缺失")
    else:
        if ha.get("status") not in AUTH_STATUS:
            errors.append(f"human_authority.status 必须是 {AUTH_STATUS}")
        rm = str(ha.get("review_method", "")).strip()
        if not rm:
            errors.append("human_authority.review_method 缺失")
        elif rm == "batch_authorization":
            notes.append("review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）")

    u = cert.get("uncertainty")
    if not isinstance(u, dict):
        errors.append("uncertainty 缺失")
    else:
        cs = u.get("cs_upper_bound")
        if not isinstance(cs, (int, float)) or float(cs) <= 0:
            errors.append("uncertainty.cs_upper_bound 必须是 >0 数值")
        if u.get("estimand") not in ESTIMANDS:
            errors.append(f"uncertainty.estimand 必须是 {ESTIMANDS}")

    p = cert.get("provenance")
    if not isinstance(p, dict):
        errors.append("provenance 缺失")
    else:
        if not str(p.get("commit", "")).strip():
            errors.append("provenance.commit 缺失或空")
        if not str(p.get("first_authorized_at", "")).strip():
            errors.append("provenance.first_authorized_at 缺失或空")

    return {"ok": len(errors) == 0, "errors": errors, "notes": notes}


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def _valid_cert() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "claim": {"id": "ATOM-CONC-FENCE-001", "statement": "fence 安全", "domain": "conc", "type": "inference"},
        "evidence": [{"type": "replay", "ref": "evidence/conc/EV-CONC-001.md"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "approved", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "e050b00", "first_authorized_at": "2026-09-20"},
    }


def _invalid_cert() -> dict:
    c = _valid_cert()
    c["schema_version"] = "old"
    c["evidence"] = []
    c["claim"]["type"] = "bogus"
    c["uncertainty"]["cs_upper_bound"] = -1
    del c["provenance"]["commit"]
    return c


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    good = validate_cert(_valid_cert())
    chk("合法证书 ok=True", good["ok"] and not good["errors"])
    chk("合法证书标注单验证器", any("单验证器" in n for n in good["notes"]))
    chk("合法证书标注 batch_authorization", any("batch_authorization" in n for n in good["notes"]))

    bad = validate_cert(_invalid_cert())
    chk("非法证书 ok=False", not bad["ok"])
    chk("非法证书捕获 schema_version 错误", any("schema_version" in e for e in bad["errors"]))
    chk("非法证书捕获 evidence 空", any("evidence" in e for e in bad["errors"]))
    chk("非法证书捕获 claim.type 非法", any("claim.type" in e for e in bad["errors"]))
    chk("非法证书捕获 cs_upper_bound<=0", any("cs_upper_bound" in e for e in bad["errors"]))
    chk("非法证书捕获 provenance.commit 缺失", any("provenance.commit" in e for e in bad["errors"]))
    chk("顶层非 mapping 被拒", not validate_cert([1, 2])["ok"])
    print(f"B2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 B2 PCK 证书验证器（结构诚实性）")
    ap.add_argument("--cert", help="待验证证书路径（yaml 或 json）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.cert:
        result = validate_cert(load_cert(args.cert))
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0 if result["ok"] else 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
