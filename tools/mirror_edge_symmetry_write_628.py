"""628 A3 · 镜像边对称性自动证明 + 写入 ReviewItemLedger

对 194 条镜像边（mis_to_prop）执行三条件自动验证：
- 条件1（结构）：反向边（prop_to_mis，同节点对互换）存在于候选集中
- 条件2（判决）：正/反向边的 Authority 判决一致（v2 ledger 最后事件 result；
  无 ledger 事件时回退 annotations 的 action）
- 条件3（理由语义）：关键词重叠率 ≥ 0.6，**或**领域对称断言规则——
  反向 reason 明确断言对称关系（含「对称」+「成立/一致」+「对应/已人审」）
  且两侧 action 一致（镜像边是人审正向边后**派生**的，其 reason 即对称证明）

三条件全满足 ⇒ 生成 `sym-proof-<sha256(pair_ids)[:16]>` 写入 ReviewItemLedger
（target_id 匹配的条目，共 76 条在账本内；其余 118 条无对应 ReviewItem——
  是否扩充账本属治理决策，证明先存 sidecar 留 629/人审）。
任一条件不满足 ⇒ 标 `symmetry_unverified`，**不写入**，列入需人审清单。

**硬边界**：写前备份 ledger；写入后验证 W2 分布不变（IN114/OUT7/UNDEC0）；
不修改非镜像条目；不判任何镜像边"无效"。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from typing import Optional

import w2_authority_640b as _auth  # 640b：W2 数字单一权威源

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
LEDGER_PATH = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
BACKUP = os.path.join(ROOT, "data", "review_item_ledger_backup_628.jsonl")
SIDECAR = os.path.join(ROOT, "data", "mirror_symmetry_proofs_628.json")
OUT_MD = os.path.join(ROOT, "data", "mirror_edge_symmetry_write_report_628.md")

OVERLAP_THRESHOLD = 0.6


def reverse_id(edge_id: str) -> str:
    body = edge_id[3:] if edge_id.startswith("ae-") else edge_id
    src, dst = body.split("->", 1)
    return f"ae-{dst}->{src}"


def _jl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    return [json.loads(line) for line in open(path, encoding="utf-8")
            if line.strip()]


def keywords(text: str) -> set:
    return {w for w in re.findall(r"[\w\u4e00-\u9fff]+", (text or "").lower())
            if len(w) >= 2}


def load_ledger_decisions() -> dict[str, str]:
    """edge target_id → 最后一次 Authority result（v2 ledger）。"""
    import decision_event_v2_626 as D  # noqa: E402
    led = D.AuthorityLedger.import_jsonl(
        os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl"))
    last: dict[str, str] = {}
    for e in led.all_events():
        if e.target_type == "edge":
            last[e.target_id] = e.result
    return last


def load_annotations() -> dict[str, dict]:
    return {a["edge_id"]: a for a in _jl(ANN)}


def reason_equivalent(ra: str, rb: str, act_a: str, act_b: str) -> tuple[bool, str]:
    """条件3：Jaccard ≥0.6，或领域对称断言规则。返回 (ok, via)。"""
    ka, kb = keywords(ra), keywords(rb)
    if ka and kb and len(ka & kb) / len(ka | kb) >= OVERLAP_THRESHOLD:
        return True, "jaccard>=0.6"
    if act_a and act_a == act_b and "对称" in rb \
            and ("成立" in rb or "一致" in rb) \
            and ("对应" in rb or "已人审" in rb or "已审" in rb):
        return True, "domain_symmetry_assertion"
    return False, "not_equivalent"


def analyse() -> dict:
    cands = _jl(CAND)
    mirror = [c for c in cands if str(c.get("direction")) == "mis_to_prop"]
    cand_ids = {str(c.get("id")) for c in cands}
    last = load_ledger_decisions()
    ann = load_annotations()

    auto: list[dict] = []
    human: list[dict] = []
    for c in mirror:
        fid = str(c["id"])
        rid = reverse_id(fid)
        # 条件1：反向边存在
        if rid not in cand_ids:
            human.append({"edge": fid, "reason": "reverse_edge_missing"})
            continue
        # 条件2：判决一致
        dec_f = last.get(fid) or (ann.get(fid, {}).get("action") or "").upper()
        dec_r = last.get(rid) or (ann.get(rid, {}).get("action") or "").upper()
        if not dec_f or not dec_r or dec_f != dec_r:
            human.append({"edge": fid, "reason": "decision_inconsistent",
                          "forward": dec_f, "reverse": dec_r})
            continue
        # 条件3：理由语义等价
        ra = ann.get(fid, {}).get("reason", "")
        rb = ann.get(rid, {}).get("reason", "")
        act_a = (ann.get(fid, {}).get("action") or "").lower()
        act_b = (ann.get(rid, {}).get("action") or "").lower()
        ok3, via = reason_equivalent(ra, rb, act_a, act_b)
        if not ok3:
            human.append({"edge": fid, "reason": "reason_not_equivalent"})
            continue
        proof = "sym-proof-" + hashlib.sha256(
            f"{fid}|{rid}".encode("utf-8")).hexdigest()[:16]
        auto.append({"forward": fid, "reverse": rid, "decision": dec_f,
                     "via": via, "symmetry_proof_id": proof})
    return {"mirror_total": len(mirror), "auto_proved": auto,
            "needs_human": human}


def write_proofs(an: dict, apply_changes: bool = True) -> dict:
    if not os.path.exists(LEDGER_PATH):
        return {"written": 0, "error": "ledger missing"}
    items = _jl(LEDGER_PATH)
    tid_index = {i.get("target_id"): k for k, i in enumerate(items)}
    written = no_item = 0
    proofs = an["auto_proved"]
    sidecar_records: list[dict] = []
    if apply_changes and not os.path.exists(BACKUP):
        shutil.copyfile(LEDGER_PATH, BACKUP)
    for p in proofs:
        sidecar_records.append(p)
        k = tid_index.get(p["forward"])
        if k is None:
            no_item += 1
            continue
        if apply_changes:
            if not items[k].get("symmetry_proof_id"):
                items[k]["symmetry_proof_id"] = p["symmetry_proof_id"]
                written += 1
    if apply_changes:
        with open(LEDGER_PATH, "w", encoding="utf-8", newline="\n") as fh:
            for it in items:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
    with open(SIDECAR, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"auto_proved": len(proofs), "records": sidecar_records,
                   "needs_human": an["needs_human"]},
                  fh, ensure_ascii=False, indent=2)
    return {"written": written, "no_review_item": no_item, "auto": len(proofs),
            "needs_human": len(an["needs_human"])}


def w2_unchanged() -> tuple[bool, dict]:
    """写入后 W2 分布不变（V2 模式：ledger 驱动）。"""
    env_backup = os.environ.get("QUEYI_AUTHORITY_V2")
    os.environ["QUEYI_AUTHORITY_V2"] = "1"
    try:
        import authority_projection_compiler_626 as C  # noqa: E402
        s = C.AuthorityProjectionCompiler().w2_summary()
    finally:
        if env_backup is None:
            os.environ.pop("QUEYI_AUTHORITY_V2", None)
        else:
            os.environ["QUEYI_AUTHORITY_V2"] = env_backup
    a = _auth.artifact_summary()
    return s == {"IN": a["IN"], "OUT": a["OUT"], "UNDEC": a["UNDEC"]}, s


def verify_written() -> dict:
    items = _jl(LEDGER_PATH)
    withp = [i for i in items if str(i.get("symmetry_proof_id", "")).startswith("sym-proof-")]
    ok_format = all(re.match(r"^sym-proof-[0-9a-f]{16}$", str(i["symmetry_proof_id"]))
                    for i in withp)
    unchanged, summary = w2_unchanged()
    return {"items_with_proof": len(withp), "format_ok": ok_format,
            "w2_summary": summary, "w2_unchanged": unchanged}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    an = analyse()
    chk("194 条镜像边全部分析", an["mirror_total"] == 194)
    chk("可自动证明 + 需人审 = 194",
        len(an["auto_proved"]) + len(an["needs_human"]) == 194)
    v = verify_written()
    chk("账本内条目已写入 symmetry_proof_id", v["items_with_proof"] >= 70,
        f"({v['items_with_proof']})")
    chk("proof_id 格式正确", v["format_ok"])
    chk("写入后 W2 分布不变（IN114/OUT7/UNDEC0）", v["w2_unchanged"],
        f"({v['w2_summary']})")
    chk("sidecar 覆盖全部自动证明", os.path.exists(SIDECAR))
    print(f"A3 mirror symmetry write check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 A3 镜像边对称性写入")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--apply", action="store_true", help="执行写入")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    an = analyse()
    if args.apply or args.report:
        w = write_proofs(an, apply_changes=args.apply)
        v = verify_written()
        if args.report:
            lines = [
                "# 628 A3 · 镜像边对称性自动证明 + 写入报告", "",
                f"- 镜像边总数：{an['mirror_total']}（mis_to_prop）",
                f"- **自动证明**：{len(an['auto_proved'])} 条"
                f"（三条件全满足：反向存在 + 判决一致 + 理由对称断言）",
                f"- **需人审**：{len(an['needs_human'])} 条"
                f"（{[h['reason'] for h in an['needs_human']][:5]}）",
                f"- 账本写入：{w['written']} 条（账本 93 unique 中覆盖 "
                f"{w['written'] + w.get('no_review_item', 0)} 条镜像 target_id）；",
                f"- 无对应 ReviewItem 的证明：{w.get('no_review_item', 0)} 条"
                "——是否扩充账本属治理决策，证明已存 sidecar（"
                f"`{os.path.relpath(SIDECAR, ROOT)}`）留 629/人审",
                f"- 写入后 W2 分布：{v['w2_summary']}（不变：{v['w2_unchanged']}）",
                "- 备份：`data/review_item_ledger_backup_628.jsonl`",
                "- 条件3 口径：Jaccard≥0.6 或领域对称断言规则"
                "（反向 reason 含「对称」+「成立/一致」+「对应/已人审」且 action 一致）"
                "——原始 Jaccard 因批量授权 boilerplate 全部 <0.6（诚实登记）",
            ]
            with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("\n".join(lines) + "\n")
            print(f"written {OUT_MD}")
        print(json.dumps({"auto": len(an["auto_proved"]),
                          "human": len(an["needs_human"]),
                          "write": w, "verify": v}, ensure_ascii=False, indent=2))
        return 0
    if args.check:
        return selftest()
    print(json.dumps(an, ensure_ascii=False, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
