"""619 B4 · PCK 证书渲染器 v1（machine → human 可读）

把 B2 验证过的 PCK 证书（yaml/json）渲染成便携、带诚实徽标的 markdown。
只读：不改证书、不改受控目录（619 §六）。

铁律：新工具必有 `--check`（只读自验证，exit 0）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pck_certificate_verifier_619 as B2  # noqa: E402


def load_cert(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)


def render(cert: dict) -> str:
    v = B2.validate_cert(cert)
    badge = "✅ PASS" if v["ok"] else "❌ FAIL"
    c = cert.get("claim", {})
    ev = cert.get("evidence", []) or []
    nt = cert.get("negative_tests") or []
    vs = cert.get("verifiers", []) or []
    ha = cert.get("human_authority", {})
    u = cert.get("uncertainty", {})
    p = cert.get("provenance", {})

    out: list[str] = []
    out.append(f"# PCK 证书 · {c.get('id', '?')}\n")
    out.append(f"> 验证徽标：**{badge}**（B2 v{B2.SCHEMA_VERSION}）"
               f"{'  ⚠ 结构有错' if not v['ok'] else ''}\n")

    out.append("## 主张（claim）")
    out.append(f"- **id**：`{c.get('id')}`")
    out.append(f"- **命题**：{c.get('statement')}")
    out.append(f"- **domain**：{c.get('domain')} · **type**：{c.get('type')}")
    out.append("")

    out.append("## 证据（evidence）")
    if ev:
        out.append("| type | ref | hash |")
        for e in ev:
            out.append(f"| {e.get('type')} | {e.get('ref')} | {e.get('hash') or '—'} |")
    else:
        out.append("- （无）")
    out.append("")

    out.append(f"## 负向测试（negative_tests · {len(nt)} 条，来自 v7 baseline）")
    if nt:
        out.append("| mutation_id | result |")
        for t in nt:
            out.append(f"| `{t.get('mutation_id')}` | {t.get('result')} |")
    else:
        out.append("- （无）")
    out.append("")

    out.append("## 验证器（verifiers）")
    for vv in vs:
        out.append(f"- `{vv.get('name')}` → **{vv.get('result')}**")
    if len(vs) == 1:
        out.append("> ⚠ 仅 1 个验证器：`verifier_disagreement` 不适用（A1 雷2 口径）。")
    out.append("")

    out.append("## 人审判定（human_authority）")
    out.append(f"- **status**：{ha.get('status')}")
    out.append(f"- **review_method**：{ha.get('review_method')}")
    if ha.get('review_method') == 'batch_authorization':
        out.append("> ⚠ 批量授权，非逐条独立审阅（615 诚实审计结论）。")
    out.append("")

    out.append("## 不确定性（uncertainty）")
    out.append(f"- **cs_upper_bound**：{u.get('cs_upper_bound')}（estimand `{u.get('estimand')}`）")
    out.append("")

    out.append("## 溯源（provenance）")
    out.append(f"- **commit**：`{p.get('commit')}`")
    out.append(f"- **first_authorized_at**：{p.get('first_authorized_at')}")
    out.append("")

    if v["errors"]:
        out.append("## 结构错误（B2）")
        for e in v["errors"]:
            out.append(f"- ❌ {e}")
        out.append("")
    if v["notes"]:
        out.append("## 诚实注释（B2）")
        for n in v["notes"]:
            out.append(f"- ℹ️ {n}")
        out.append("")
    return "\n".join(out)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def _sample_cert() -> dict:
    return {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": "ATOM-CONC-FENCE-001", "statement": "fence≠atomic",
                  "domain": "conc", "type": "observation"},
        "evidence": [{"type": "replay", "ref": "evidence/conc/EV-CONC-001.md"}],
        "negative_tests": [{"mutation_id": "atoms/ATOM-CONC-FENCE-001.md|M5|claim_type 自标", "result": "blocked"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "approved", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "7602058d", "first_authorized_at": "2026-09-12"},
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    cert = _sample_cert()
    md = render(cert)
    chk("渲染含标题", "# PCK 证书" in md)
    chk("渲染含 PASS 徽标", "✅ PASS" in md)
    chk("渲染含诚实注释（单验证器）", "verifier_disagreement" in md)
    chk("渲染含批量授权注释", "batch_authorization" in md)
    chk("渲染含负向测试表", "negative_tests" in md)
    # 含错证书应渲染 FAIL 徽标
    bad = dict(cert)
    bad["schema_version"] = "old"
    bad["evidence"] = []
    md_bad = render(bad)
    chk("含错证书渲染 FAIL 徽标", "❌ FAIL" in md_bad)
    chk("含错证书列出结构错误", "结构错误" in md_bad)
    print(f"B4 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 B4 PCK 证书渲染器（machine→human）")
    ap.add_argument("--cert", help="待渲染证书（yaml/json）")
    ap.add_argument("--out", help="输出 markdown 路径")
    ap.add_argument("--demo", action="store_true",
                    help="渲染内置样本到 data/pck_renderer_demo_619.md")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.demo:
        out = args.out or os.path.join(ROOT, "data", "pck_renderer_demo_619.md")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(render(_sample_cert()) + "\n")
        print(f"wrote {out}")
        return 0
    if args.cert:
        md = render(load_cert(args.cert))
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(md + "\n")
            print(f"wrote {args.out}")
        else:
            print(md)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
