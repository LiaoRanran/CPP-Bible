"""621 C3 · ABSTAIN 状态与 PCK certificate 集成

把 C2 的六态分类结果写入 certificate 的 `uncertainty` 字段：

```yaml
uncertainty:
  cs_upper_bound: 0.009062
  estimand: L1
  abstain_state: UNDECIDED      # 新增
  abstain_reason: "…"           # 新增
  abstain_is_abstain: true      # 新增
```

**硬边界**：
- **不修改 `human_authority` 字段**（那是人审，621 不代签）
- 不修改原始卡
- 只写 `data/pck/certificates/`（非受控目录）
- 同步后必须仍通过 619 B2 验证（本工具会复查）

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pck_certificate_verifier_619 as B2  # noqa: E402

DEFAULT_CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
DEFAULT_CLASSIFICATION = os.path.join(ROOT, "data", "abstain_classification_621.jsonl")
DEFAULT_REPORT = os.path.join(ROOT, "data", "pck_abstain_sync_report_621.md")


def load_classification(path: str = DEFAULT_CLASSIFICATION) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln:
                continue
            r = json.loads(ln)
            out[r["card_id"]] = r
    return out


def load_certs(cert_dir: str = DEFAULT_CERT_DIR) -> list[tuple[str, dict]]:
    out = []
    for p in sorted(glob.glob(os.path.join(cert_dir, "*.pck.yaml"))):
        with open(p, encoding="utf-8") as fh:
            out.append((p, yaml.safe_load(fh.read())))
    return out


def sync(cert_dir: str = DEFAULT_CERT_DIR,
         classification_path: str = DEFAULT_CLASSIFICATION,
         write: bool = True) -> dict:
    cls = load_classification(classification_path)
    certs = load_certs(cert_dir)

    synced = 0
    unmatched = 0
    by_state: dict[str, int] = {}
    ha_before: dict[str, int] = {}
    ha_after: dict[str, int] = {}
    rows: list[dict] = []

    for path, cert in certs:
        cid = str((cert.get("claim") or {}).get("id", ""))
        ha_before[(cert.get("human_authority") or {}).get("status")] = \
            ha_before.get((cert.get("human_authority") or {}).get("status"), 0) + 1

        info = cls.get(cid)
        u = cert.setdefault("uncertainty", {})
        if info:
            u["abstain_state"] = info["state"]
            u["abstain_reason"] = info.get("reason")
            u["abstain_is_abstain"] = bool(info.get("is_abstain"))
            by_state[info["state"]] = by_state.get(info["state"], 0) + 1
            synced += 1
        else:
            u["abstain_state"] = "UNKNOWN"
            u["abstain_reason"] = "无对应 ABSTAIN 分类结果"
            u["abstain_is_abstain"] = True
            unmatched += 1

        # human_authority 一律不动（不代签）
        ha_after[(cert.get("human_authority") or {}).get("status")] = \
            ha_after.get((cert.get("human_authority") or {}).get("status"), 0) + 1

        rows.append({"cert_id": cid, "abstain_state": u["abstain_state"],
                     "abstain": u["abstain_is_abstain"],
                     "ha_status": (cert.get("human_authority") or {}).get("status")})

        if write:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("# PCK 证书（620 B1 迁移 + C3 Authority 同步 + 621 C3 ABSTAIN 同步）\n")
                fh.write(yaml.safe_dump(cert, allow_unicode=True,
                                        sort_keys=False, default_flow_style=False))

    valid = 0
    for _p, cert in load_certs(cert_dir) if write else certs:
        if B2.validate_cert(cert)["ok"]:
            valid += 1

    return {
        "total": len(certs), "synced": synced, "unmatched": unmatched,
        "by_state": dict(sorted(by_state.items())),
        "ha_before": dict(sorted(ha_before.items(), key=lambda kv: str(kv[0]))),
        "ha_after": dict(sorted(ha_after.items(), key=lambda kv: str(kv[0]))),
        "validation_ok_after": valid,
        "rows": rows,
    }


def render_report(res: dict) -> str:
    o = ["# 621 C3 · ABSTAIN 与 PCK 集成同步报告\n"]
    o.append(f"> 证书总数：**{res['total']}** · 同步成功 **{res['synced']}** · "
             f"无匹配 **{res['unmatched']}**\n")
    o.append("## 一、同步后的 abstain_state 分布\n")
    o.append("| abstain_state | 张数 |")
    for k, v in res["by_state"].items():
        o.append(f"| {k} | {v} |")
    if res["unmatched"]:
        o.append(f"| UNKNOWN（无分类） | {res['unmatched']} |")
    o.append("")
    o.append("## 二、human_authority 未被改动（不代签）\n")
    o.append("| 阶段 | 分布 |")
    o.append(f"| 同步前 | {res['ha_before']} |")
    o.append(f"| 同步后 | {res['ha_after']} |")
    o.append("")
    o.append(f"- 同步后 B2 验证通过：**{res['validation_ok_after']} / {res['total']}**\n")
    o.append("## 三、明细（前 20 条）\n")
    o.append("| cert_id | abstain_state | 弃权 | human_authority |")
    for r in res["rows"][:20]:
        o.append(f"| {r['cert_id']} | {r['abstain_state']} | "
                 f"{'是' if r['abstain'] else '否'} | {r['ha_status']} |")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    import tempfile

    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    base = {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": "ATOM-CONC-FENCE-001", "statement": "s", "domain": "conc",
                  "type": "inference"},
        "evidence": [{"type": "replay", "ref": "evidence/conc/EV-CONC-001.md"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "approved", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "abc", "first_authorized_at": "unknown"},
    }
    with tempfile.TemporaryDirectory() as td:
        cdir = os.path.join(td, "certs")
        os.makedirs(cdir)
        with open(os.path.join(cdir, "ATOM-CONC-FENCE-001.pck.yaml"), "w",
                  encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(base, allow_unicode=True))
        cpath = os.path.join(td, "cls.jsonl")
        with open(cpath, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"card_id": "ATOM-CONC-FENCE-001", "state": "UNDECIDED",
                                 "reason": "无 verdict", "is_abstain": True},
                                ensure_ascii=False) + "\n")

        res = sync(cdir, cpath, write=True)
        chk("同步命中 1 张", res["synced"] == 1 and res["unmatched"] == 0)
        with open(os.path.join(cdir, "ATOM-CONC-FENCE-001.pck.yaml"), encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        chk("uncertainty 写入 abstain_state",
            after["uncertainty"]["abstain_state"] == "UNDECIDED")
        chk("abstain_is_abstain 为真", after["uncertainty"]["abstain_is_abstain"] is True)
        chk("human_authority 未被改动（不代签）",
            after["human_authority"] == base["human_authority"])
        chk("同步后仍通过 B2", B2.validate_cert(after)["ok"])

        # 无分类 ⇒ UNKNOWN
        c2 = dict(base)
        c2["claim"] = dict(base["claim"], id="EV-CONC-999")
        with open(os.path.join(cdir, "EV-CONC-999.pck.yaml"), "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(c2, allow_unicode=True))
        res2 = sync(cdir, cpath, write=True)
        chk("无分类时标 UNKNOWN", res2["unmatched"] == 1)
        chk("幂等：重复同步一致",
            sync(cdir, cpath, write=True)["by_state"] == res2["by_state"])

    chk("报告可渲染", "ABSTAIN 与 PCK 集成" in render_report(res))
    print(f"C3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 C3 ABSTAIN 与 PCK 集成")
    ap.add_argument("--cert-dir", default=DEFAULT_CERT_DIR)
    ap.add_argument("--classification", default=DEFAULT_CLASSIFICATION)
    ap.add_argument("--out", default=DEFAULT_REPORT)
    ap.add_argument("--dry-run", action="store_true", help="只统计不写证书")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = sync(args.cert_dir, args.classification, write=not args.dry_run)
    md = render_report(res)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(f"wrote {args.out}  synced={res['synced']} unmatched={res['unmatched']} "
          f"valid={res['validation_ok_after']}/{res['total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
