"""620 C3 · Authority 日志 ↔ PCK certificate 集成

读取 Authority 日志（620 C2）+ 全量 PCK certificate（620 B2），
对每张证书从日志查找对应决策，更新其 `human_authority` 字段。

**匹配规则（如实、可审计）**：
- Authority 日志的 `target.id` 现为 attack_edge 形态
  （如 `ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3`），其中**内嵌**原子卡 id；
- 因此用**子串匹配**：`cert_id in entry.target.id`；
- 证据卡（EV-*）在历史人审通道中**没有**对应决策 ⇒ 保持 `pending`，**不伪造**。

**硬边界**：
- 只更新 `data/pck/certificates/` 下的证书（非受控目录）
- **不代签任何决策**：无决策的证书保持 `pending`，绝不因"同步"而变成 approved
- 幂等：同一日志重复同步结果一致

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import authority_log_620 as AL  # noqa: E402
import pck_certificate_verifier_619 as B2  # noqa: E402
import yaml  # noqa: E402

DEFAULT_CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
DEFAULT_LOG = AL.DEFAULT_LOG
DEFAULT_REPORT = os.path.join(ROOT, "data", "pck_authority_sync_report_620.md")

POWER_TO_STATUS = {"ACCEPT": "approved", "REJECT": "rejected",
                   "OVERRIDE": "approved", "ABSTAIN": "pending"}


def load_certs(cert_dir: str = DEFAULT_CERT_DIR) -> list[tuple[str, dict]]:
    out = []
    for path in sorted(glob.glob(os.path.join(cert_dir, "*.pck.yaml"))):
        with open(path, encoding="utf-8") as fh:
            cert = yaml.safe_load(fh.read())
        out.append((path, cert))
    return out


def match_decisions(cert_id: str, entries: list[dict]) -> list[dict]:
    """子串匹配：cert_id 出现在 decision 的 target.id 中。"""
    return [e for e in entries if cert_id and cert_id in str((e.get("target") or {}).get("id", ""))]


def sync(cert_dir: str = DEFAULT_CERT_DIR, log_path: str = DEFAULT_LOG,
         write: bool = True) -> dict:
    entries = AL.load_entries(log_path)
    certs = load_certs(cert_dir)

    synced = 0
    unmatched = 0
    status_after: dict[str, int] = {}
    rows: list[dict] = []

    for path, cert in certs:
        cert_id = str((cert.get("claim") or {}).get("id", ""))
        hits = match_decisions(cert_id, entries)
        ha = cert.setdefault("human_authority", {})

        if hits:
            # 取**最后一条**（时间序）决策为当前生效
            last = hits[-1]
            new_status = POWER_TO_STATUS.get(str(last.get("power") or ""), "pending")
            ha["status"] = new_status
            ha["review_method"] = last.get("review_method") or "batch_authorization"
            ha["authority_ref"] = last.get("decision_id")
            ha["authority_power"] = last.get("power")
            ha["authority_decided_at"] = last.get("decided_at")
            ha["authority_source"] = "import:data/human_attack_edge_annotations.jsonl"
            synced += 1
        else:
            # 无决策 ⇒ 保持 pending，**不代签**
            ha.setdefault("status", "pending")
            ha["authority_ref"] = None
            ha["authority_note"] = "无匹配的 Authority 决策（不代签，保持 pending）"
            unmatched += 1

        status_after[ha["status"]] = status_after.get(ha["status"], 0) + 1
        rows.append({"cert_id": cert_id, "matched": len(hits),
                     "status": ha["status"], "file": os.path.basename(path),
                     "power": ha.get("authority_power")})

        if write:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("# PCK 证书（620 B1 迁移 + C3 Authority 同步，只读派生）\n")
                fh.write(yaml.safe_dump(cert, allow_unicode=True,
                                        sort_keys=False, default_flow_style=False))

    # 同步后重新验证（确保同步没有把证书改坏）
    ok = 0
    for _p, cert in load_certs(cert_dir) if write else certs:
        if B2.validate_cert(cert)["ok"]:
            ok += 1

    return {
        "total": len(certs), "synced": synced, "unmatched": unmatched,
        "status_after": dict(sorted(status_after.items())),
        "validation_ok_after": ok,
        "log_entries": len(entries),
        "rows": rows,
    }


def render_report(res: dict) -> str:
    o = ["# 620 C3 · Authority 与 PCK 集成同步报告\n"]
    o.append(f"> Authority 日志条目：**{res['log_entries']}** · 证书总数：**{res['total']}**\n")
    o.append("## 一、同步统计\n")
    o.append("| 指标 | 值 |")
    o.append(f"| 证书总数 | {res['total']} |")
    o.append(f"| 匹配到 Authority 决策 | **{res['synced']}** |")
    o.append(f"| 无匹配（保持 pending，不代签） | **{res['unmatched']}** |")
    o.append(f"| 同步后 B2 验证通过 | {res['validation_ok_after']} / {res['total']} |")
    o.append("")
    o.append("## 二、同步后状态分布\n")
    o.append("| status | 张数 |")
    for k, v in res["status_after"].items():
        o.append(f"| {k} | {v} |")
    o.append("")
    o.append("## 三、匹配明细（前 30 条）\n")
    o.append("| cert_id | 匹配决策数 | 生效 status | power |")
    for r in res["rows"][:30]:
        o.append(f"| {r['cert_id']} | {r['matched']} | {r['status']} | {r['power'] or '—'} |")
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

    sample: dict = {
        "schema_version": B2.SCHEMA_VERSION,
        "claim": {"id": "ATOM-MEM-PERF-003", "statement": "s", "domain": "mem",
                  "type": "inference"},
        "evidence": [{"type": "replay", "ref": "evidence/mem/EV-MEM-001.md"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "pending", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "abc", "first_authorized_at": "unknown"},
    }
    entries = [{"decision_id": "dec-000001", "seq": 1,
                "target": {"type": "attack_edge",
                           "id": "ae-MIS-MEM-032->ATOM-MEM-PERF-003::prop-3"},
                "power": "ACCEPT", "reviewer": "human:LiaoRanran", "reason": "r",
                "review_method": "batch_authorization", "decided_at": "2026-09-19",
                "prev_hash": AL.GENESIS, "self_hash": "x"}]

    chk("子串匹配命中内嵌卡 id", len(match_decisions("ATOM-MEM-PERF-003", entries)) == 1)
    chk("不相关卡 id 不误匹配", match_decisions("EV-CONC-001", entries) == [])
    chk("ACCEPT 映射为 approved", POWER_TO_STATUS["ACCEPT"] == "approved")
    chk("ABSTAIN 映射为 pending（弃权≠接受）", POWER_TO_STATUS["ABSTAIN"] == "pending")

    with tempfile.TemporaryDirectory() as td:
        cdir = os.path.join(td, "certs")
        os.makedirs(cdir)
        p = os.path.join(cdir, "ATOM-MEM-PERF-003.pck.yaml")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(sample, allow_unicode=True))
        lpath = os.path.join(td, "log.jsonl")
        with open(lpath, "w", encoding="utf-8") as fh:
            for e in entries:
                fh.write(AL._canonical(e) + "\n")

        res = sync(cdir, lpath, write=True)
        chk("同步命中 1 张", res["synced"] == 1)
        with open(p, encoding="utf-8") as fh:
            after = yaml.safe_load(fh.read())
        chk("证书 human_authority 被更新为 approved",
            after["human_authority"]["status"] == "approved")
        chk("证书记录 authority_ref", after["human_authority"]["authority_ref"] == "dec-000001")
        chk("同步后仍通过 B2 验证", B2.validate_cert(after)["ok"])

        # 无匹配的证书保持 pending
        p2 = os.path.join(cdir, "EV-CONC-001.pck.yaml")
        s2 = dict(sample)
        s2["claim"] = {**sample["claim"], "id": "EV-CONC-001"}
        with open(p2, "w", encoding="utf-8") as fh:
            fh.write(yaml.safe_dump(s2, allow_unicode=True))
        res2 = sync(cdir, lpath, write=True)
        chk("无匹配证书保持 pending（不代签）",
            res2["status_after"].get("pending") == 1)
        chk("幂等：重复同步结果一致", sync(cdir, lpath, write=True)["status_after"]
            == res2["status_after"])

    chk("报告可渲染", "同步统计" in render_report(res))
    print(f"C3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 C3 Authority ↔ PCK 集成")
    ap.add_argument("--cert-dir", default=DEFAULT_CERT_DIR)
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--out", default=DEFAULT_REPORT)
    ap.add_argument("--dry-run", action="store_true", help="只统计不写证书")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = sync(args.cert_dir, args.log, write=not args.dry_run)
    md = render_report(res)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(md + "\n")
    print(f"wrote {args.out}  synced={res['synced']} unmatched={res['unmatched']} "
          f"valid={res['validation_ok_after']}/{res['total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
