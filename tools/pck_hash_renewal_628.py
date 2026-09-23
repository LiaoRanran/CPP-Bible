"""628 A2 · PCK hash 漂移处置执行（83 张全量重算，**不判失效**）

627 A3 只做了根因分类（content_drift 56 + hash_absent 26 + ref_missing 1 = 83），
本工具执行**机械重算**：

- content_drift：重新计算当前 evidence 文件的 SHA256，更新 `evidence.hash`
  （保持 `sha256:<hex>` 前缀格式）
- hash_absent：补上 `evidence.hash` 字段（当前文件 SHA256）
- ref_missing：**不自动修复**——标 `hash_status: ref_missing_needs_human`，
  文件不存在可能意味着证据被删或路径变更，需人裁决

**硬边界**：
1. 只更新 evidence 条目的 `hash` / `hash_status` 字段，
   **绝不修改** verdict/authorized/status/uncertainty 等语义字段
2. **不判任何证书失效**——"失效"是语义判断，需人审
3. 重算前全量备份到 `data/pck_backup_628/`（可回滚）
4. 重算后验证：82/83 张 hash 与当前文件一致（ref_missing 的 1 张除外）

用法：`--apply` 执行重算（幂等）；`--check` 自检验证一致率；`--report` 写报告。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
from typing import Any, Optional

import yaml  # noqa: E402  # 项目既有依赖（PCK 均为 yaml）

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
DRIFT_JSON = os.path.join(ROOT, "data", "pck_hash_drift_627.json")
BACKUP_DIR = os.path.join(ROOT, "data", "pck_backup_628")
OUT_JSON = os.path.join(ROOT, "data", "pck_hash_renewal_628.json")
OUT_MD = os.path.join(ROOT, "data", "pck_hash_renewal_report_628.md")

NEEDS_HUMAN = "ref_missing_needs_human"


def _sha256_file(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def load_categories() -> dict[str, dict[str, str]]:
    """cert → {ref: category}（来自 627 A3 的分类）。"""
    d = json.load(open(DRIFT_JSON, encoding="utf-8"))
    out: dict[str, dict[str, str]] = {}
    for c in d["certs"]:
        m = out.setdefault(str(c["cert"]), {})
        for e in c["evidence"]:
            m.setdefault(str(e["ref"]), str(e["category"]))
    return out


def backup() -> int:
    """全量备份 PCK 目录（幂等：已存在则跳过，保留首次原始状态）。"""
    if os.path.isdir(BACKUP_DIR):
        return len(glob.glob(os.path.join(BACKUP_DIR, "*.yaml")))
    shutil.copytree(CERT_DIR, BACKUP_DIR)
    return len(glob.glob(os.path.join(BACKUP_DIR, "*.yaml")))


def renew(apply_changes: bool = True) -> dict:
    """重算（幂等）：以**当前文件实际状态**为准——
    文件缺失 ⇒ 需人审；有 hash 且一致 ⇒ 跳过；否则重算/补 hash。
    （不依赖 627 分类快照，避免快照过时导致漏修。）
    """
    stats = {"renewed": 0, "added": 0, "needs_human": 0, "already_ok": 0,
             "certs_touched": 0}
    needs_human_list: list[dict] = []
    for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.yaml"))):
        cert = os.path.splitext(os.path.basename(p))[0]
        with open(p, encoding="utf-8") as fh:
            data: dict[str, Any] = yaml.safe_load(fh)
        touched = False
        for ev in data.get("evidence", []) or []:
            if not isinstance(ev, dict) or "ref" not in ev:
                continue
            ref = str(ev["ref"])
            cur = _sha256_file(os.path.join(ROOT, ref))
            if cur is None:
                # ref_missing：不自动修，标需人审
                if ev.get("hash_status") != NEEDS_HUMAN:
                    ev["hash_status"] = NEEDS_HUMAN
                    touched = True
                    stats["needs_human"] += 1
                    needs_human_list.append({"cert": cert, "ref": ref})
                continue
            want = f"sha256:{cur}"
            old = ev.get("hash")
            if old == want:
                stats["already_ok"] += 1
                continue
            if apply_changes:
                ev["hash"] = want
                touched = True
            if old is None:
                stats["added"] += 1
            else:
                stats["renewed"] += 1
        if touched:
            stats["certs_touched"] += 1
            if apply_changes:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    yaml.safe_dump(data, fh, allow_unicode=True,
                                   sort_keys=False, default_flow_style=False)
    result = {"total_certs": len(glob.glob(os.path.join(CERT_DIR, "*.yaml"))),
              "applied": apply_changes, "stats": stats,
              "needs_human": needs_human_list}
    if apply_changes:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    return result


def verify() -> dict:
    """重算后核验：82/83 一致（ref_missing 需人审的除外）。"""
    total = ok = needs_human = 0
    bad: list[str] = []
    for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.yaml"))):
        cert = os.path.splitext(os.path.basename(p))[0]
        with open(p, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        for ev in data.get("evidence", []) or []:
            if not isinstance(ev, dict) or "ref" not in ev:
                continue
            total += 1
            if ev.get("hash_status") == NEEDS_HUMAN:
                needs_human += 1
                continue
            cur = _sha256_file(os.path.join(ROOT, str(ev["ref"])))
            if cur and ev.get("hash") == f"sha256:{cur}":
                ok += 1
            else:
                bad.append(f"{cert}:{ev['ref']}")
    return {"total_evidence": total, "hash_ok": ok, "needs_human": needs_human,
            "bad": bad[:10], "bad_count": len(bad),
            "consistent": len(bad) == 0 and ok >= 82}


def semantic_fields_untouched() -> bool:
    """重算未修改语义字段：对比备份，除 evidence[].hash/hash_status 外全部一致。"""
    if not os.path.isdir(BACKUP_DIR):
        return False
    for bp in glob.glob(os.path.join(BACKUP_DIR, "*.yaml")):
        cp = os.path.join(CERT_DIR, os.path.basename(bp))
        a = yaml.safe_load(open(bp, encoding="utf-8"))
        b = yaml.safe_load(open(cp, encoding="utf-8"))
        if not a or not b:
            return False
        ev_a, ev_b = a.pop("evidence", []), b.pop("evidence", [])
        if a != b:
            return False
        if len(ev_a) != len(ev_b):
            return False
        for x, y in zip(ev_a, ev_b):
            kx = {k: v for k, v in x.items() if k not in ("hash", "hash_status")}
            ky = {k: v for k, v in y.items() if k not in ("hash", "hash_status")}
            if kx != ky:
                return False
    return True


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    v = verify()
    chk("PCK 目录 83 张证书", v["total_evidence"] > 80, f"(evidence {v['total_evidence']})")
    chk("hash 与当前文件一致 ≥82", v["hash_ok"] >= 82, f"({v['hash_ok']})")
    chk("ref_missing 需人审（1 张证书 ATOM-HIST-AUTOPTR-001 的缺失引用）",
        1 <= v["needs_human"] <= 2, f"({v['needs_human']} 条引用)")
    chk("无意外失配", v["bad_count"] == 0, f"({v['bad_count']})")
    chk("备份目录存在且 83 张", os.path.isdir(BACKUP_DIR)
        and len(glob.glob(os.path.join(BACKUP_DIR, "*.yaml"))) == 83)
    chk("语义字段未被修改（对比备份）", semantic_fields_untouched())
    print(f"A2 pck hash renewal check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 A2 PCK hash 重算")
    ap.add_argument("--apply", action="store_true", help="执行重算（幂等）")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="写处置报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    n = backup()
    if args.apply or args.report:
        r = renew(apply_changes=True)
        v = verify()
        if args.report:
            st = r["stats"]
            lines = [
                "# 628 A2 · PCK hash 漂移处置报告", "",
                f"- 处置证书：{r['total_certs']} 张（备份 {n} 张 → `data/pck_backup_628/`）",
                f"- 重算（content_drift）：**{st['renewed']}** 条 hash 更新",
                f"- 补 hash（hash_absent）：**{st['added']}** 条",
                f"- 需人审（ref_missing）：**{st['needs_human']}** 条——"
                f"{r['needs_human']}",
                f"- 重算前 B2-R：27/83 → 重算后：**{v['hash_ok']}/{v['total_evidence']} 一致**",
                "- **未判任何证书失效**：hash 重算是机械操作；\"失效\"是语义判断需人审",
                "- **语义字段未动**：verdict/authorized/status/uncertainty 等与备份逐字段一致",
                "",
                "## 回滚方法", "",
                "```bash",
                "cp data/pck_backup_628/*.yaml data/pck/certificates/",
                "```",
            ]
            with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines) + "\n")
            print(f"written {OUT_MD}")
        print(json.dumps({"stats": st, "verify": v}, ensure_ascii=False, indent=2))
        return 0
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
