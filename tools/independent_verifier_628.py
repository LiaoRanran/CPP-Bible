"""628 B1 · 独立验证者（IndependentVerifier）—— **零 import 本项目工具**

他验三件套的第一件。核心原则（硬边界 9）：
- **绝对不 import** `tools/` 下任何本项目模块（gate_engine / weighted_af_solver /
  decision_event_v2_626 / authority_projection_compiler 等）
- 只使用 Python 标准库（json / hashlib / os / sys / argparse / re / tempfile）
- 直接读取原始数据文件，**自己重算**关键数字，与系统输出对比

独立重算项：
1. W2 论证图 IN/OUT/UNDEC——**朴素实现**：
   节点=grounded_labels_w2.json（credibility 在卡面）；
   生效攻击=ledger 中 target_type=edge 且 result∈{APPROVE,MODIFY}（去重）；
   击败=(A,B) 当 cred(A) > cred(B)（严格大于）；在击败关系上求 grounded 语义。
   算法是最直接的遍历迭代，不含任何优化——若系统求解器有隐性 bug，这里会发现。
2. PCK authorized/pending/blocked——自解析 PCK yaml（**行级子集解析器**，
   只依赖固定 schema 的缩进规则，不用 pyyaml）
3. DecisionEvent 哈希链——自行重算每条
   `self_hash = sha256(f"{prev_hash}|{payload}")`，
   payload = 事件 dict 去 self_hash/event_id 后 sort_keys JSON
4. 唯一审查账本 unique 数（按 target_id 去重）

对比基准（来自系统产物/报告，非系统工具）：`data/grounded_labels_w2.json` 的
label、`data/authority_projection_626.json`、627/628 报告登记数字
（IN114/OUT7/UNDEC0、PCK authorized 27、unique 93）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
REVIEW = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
PROJECTION = os.path.join(ROOT, "data", "authority_projection_626.json")
OUT_JSON = os.path.join(ROOT, "data", "independent_verifier_628.json")
OUT_MD = os.path.join(ROOT, "data", "independent_verifier_report_628.md")

GENESIS = "GENESIS"
ACTIVE_RESULTS = ("APPROVE", "MODIFY")

# 期望数字（登记于 626/627/628 报告的"系统口径"）
EXPECT = {"w2": {"IN": 114, "OUT": 7, "UNDEC": 0},
          "pck_authorized": 27, "unique_review_items": 93, "ledger_events": 452}


def _jl(path: str) -> list[dict]:
    out: list[dict] = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
    return out


# ── 1. 朴素 W2 求解器（零依赖重实现） ──────────────────────────────

def parse_edge(target_id: str) -> tuple[Optional[str], Optional[str]]:
    body = target_id[3:] if target_id.startswith("ae-") else target_id
    if "->" not in body:
        return None, None
    src, dst = body.split("->", 1)
    return src, dst


def naive_active_edges(ledger_path: str = LEDGER) -> list[tuple[str, str]]:
    seen: set = set()
    out: list[tuple[str, str]] = []
    for e in _jl(ledger_path):
        if e.get("target_type") != "edge" or e.get("result") not in ACTIVE_RESULTS:
            continue
        s, d = parse_edge(str(e.get("target_id", "")))
        if not s or not d or (s, d) in seen:
            continue
        seen.add((s, d))
        out.append((s, d))
    return out


def naive_grounded(nodes: dict[str, int],
                   defeats: set[tuple[str, str]]) -> dict[str, str]:
    """最直接的 grounded 语义：IN=未被任何 IN 攻击者击败且（有攻击者则全 OUT）/
    OUT=被某 IN 攻击者击败/UNDEC=其余。迭代到不动点。"""
    labels = {n: "UNDEC" for n in nodes}
    attackers: dict[str, list] = {n: [] for n in nodes}
    for a, b in defeats:
        attackers.setdefault(b, []).append(a)
    changed = True
    while changed:
        changed = False
        for n in sorted(nodes):
            if labels[n] != "UNDEC":
                continue
            atk = attackers.get(n, [])
            if any(labels.get(a) == "IN" for a in atk):
                labels[n] = "OUT"
                changed = True
            elif atk and all(labels.get(a) == "OUT" for a in atk):
                labels[n] = "IN"
                changed = True
            elif not atk:
                labels[n] = "IN"
                changed = True
    return labels


def verify_w2(grounded_path: str = GROUNDED,
              ledger_path: str = LEDGER) -> dict:
    g = json.load(open(grounded_path, encoding="utf-8"))
    nodes_meta = g["nodes"]
    cred = {k: int(v.get("credibility", 0)) for k, v in nodes_meta.items()}
    edges = naive_active_edges(ledger_path)
    defeats = {(a, b) for a, b in edges
               if a in cred and b in cred and cred[a] > cred[b]}
    labels = naive_grounded(cred, defeats)
    summary = {"IN": 0, "OUT": 0, "UNDEC": 0}
    for v in labels.values():
        summary[v] += 1
    # 与"系统冻结输出"（grounded_labels 的 label 字段）对比
    frozen = {k: str(v.get("label")) for k, v in nodes_meta.items()}
    diff = [k for k in frozen if labels.get(k) != frozen[k]]
    return {"nodes": len(cred), "active_edges": len(edges),
            "defeats": len(defeats), "summary": summary,
            "labels": labels, "frozen_labels_match": not diff, "diff": diff[:5]}


# ── 2. PCK 计数（行级子集解析器） ─────────────────────────────────

def parse_pck_minimal(path: str) -> dict:
    """最小 YAML 子集解析：只认本 schema 用到的两级缩进键。

    支持：`key:`（块开始）、`  key: value`（二级标量）、`- ` 列表项内的
    `  key: value`（evidence 的 ref/hash）。字符串值去引号。
    """
    claim_id = ""
    ha_status = ""
    in_human_authority = False
    in_claim = False
    evidence_refs: list[str] = []
    cur_is_evidence = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            top = re.match(r"^([A-Za-z_][\w]*):", line)
            if top:
                key = top.group(1)
                in_human_authority = key == "human_authority"
                in_claim = key == "claim"
                cur_is_evidence = key == "evidence"
                continue
            m = re.match(r"^\s{2,}-?\s*([A-Za-z_][\w]*):\s*(.*)$", line)
            if m:
                k, v = m.group(1), m.group(2).strip().strip("'\"")
                if in_claim and k == "id":
                    claim_id = v
                elif in_human_authority and k == "status":
                    ha_status = v
                elif cur_is_evidence and k == "ref" and v:
                    evidence_refs.append(v)
    return {"id": claim_id, "human_authority_status": ha_status,
            "evidence_refs": evidence_refs}


def verify_pck(cert_dir: str = CERT_DIR) -> dict:
    statuses: dict[str, int] = {}
    per_cert: dict[str, str] = {}
    n_evidence = 0
    for name in sorted(os.listdir(cert_dir)):
        if not name.endswith(".yaml"):
            continue
        p = parse_pck_minimal(os.path.join(cert_dir, name))
        st = p["human_authority_status"] or "missing"
        statuses[st] = statuses.get(st, 0) + 1
        per_cert[p["id"] or name] = st
        n_evidence += len(p["evidence_refs"])
    return {"total": sum(statuses.values()), "by_status": statuses,
            "authorized": statuses.get("approved", 0),
            "pending": statuses.get("pending", 0),
            "blocked": statuses.get("blocked", 0),
            "evidence_refs": n_evidence, "per_cert": per_cert}


# ── 3. ledger 哈希链（自行重算） ──────────────────────────────────

def verify_ledger_chain(ledger_path: str = LEDGER) -> dict:
    events = _jl(ledger_path)
    prev = GENESIS
    broken: list[str] = []
    for e in events:
        payload = json.dumps({k: v for k, v in e.items()
                              if k not in ("self_hash", "event_id")},
                             ensure_ascii=False, sort_keys=True, default=str)
        expect = hashlib.sha256(f"{prev}|{payload}".encode("utf-8")).hexdigest()
        if e.get("self_hash") != expect or e.get("prev_hash") != prev:
            broken.append(str(e.get("event_id")))
        prev = str(e.get("self_hash"))
    return {"events": len(events), "chain_valid": not broken,
            "broken_at": broken[:5], "first_prev": events[0].get("prev_hash") if events else None}


def verify_unique_review(review_path: str = REVIEW) -> dict:
    items = _jl(review_path)
    tids = [str(i.get("target_id")) for i in items]
    return {"records": len(items), "unique": len(set(tids))}


# ── 4. 汇总对比 + 篡改检测 ────────────────────────────────────────

def run_all(grounded_path: str = GROUNDED, ledger_path: str = LEDGER,
            cert_dir: str = CERT_DIR, review_path: str = REVIEW) -> dict:
    w2 = verify_w2(grounded_path, ledger_path)
    pck = verify_pck(cert_dir)
    chain = verify_ledger_chain(ledger_path)
    uniq = verify_unique_review(review_path)
    checks = {
        "w2_summary_match": w2["summary"] == EXPECT["w2"],
        "w2_frozen_labels_match": w2["frozen_labels_match"],
        "pck_authorized_match": pck["authorized"] == EXPECT["pck_authorized"],
        "ledger_chain_valid": chain["chain_valid"],
        "ledger_events_match": chain["events"] == EXPECT["ledger_events"],
        "unique_match": uniq["unique"] == EXPECT["unique_review_items"],
    }
    return {"w2": {k: v for k, v in w2.items() if k != "labels"},
            "pck": {k: v for k, v in pck.items() if k != "per_cert"},
            "ledger_chain": chain, "unique": uniq,
            "checks": checks, "all_match": all(checks.values())}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run_all()
    chk("独立重算 W2 = IN114/OUT7/UNDEC0", r["checks"]["w2_summary_match"],
        f"({r['w2']['summary']})")
    chk("与系统冻结输出逐节点一致", r["checks"]["w2_frozen_labels_match"])
    chk("独立重算 PCK authorized = 27", r["checks"]["pck_authorized_match"],
        f"({r['pck']['by_status']})")
    chk("ledger 哈希链独立验证通过（452 条）", r["checks"]["ledger_chain_valid"]
        and r["checks"]["ledger_events_match"], f"({r['ledger_chain']['events']})")
    chk("唯一账本 unique = 93", r["checks"]["unique_match"],
        f"({r['unique']['records']} records)")
    chk("全部一致", r["all_match"])
    # 零 import 静态自证：源码不得 import 任何 tools/ 模块
    src = open(__file__, encoding="utf-8").read()
    bad = re.findall(r"^\s*(?:import|from)\s+(?!json|hashlib|os|sys|argparse|re|tempfile|typing|__future__)(\w+)",
                     src, re.MULTILINE)
    chk("零 import 本项目工具（静态自证）", not bad, f"({bad})")
    print(f"B1 independent verifier check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 B1 独立验证者")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    r = run_all()
    if args.report:
        lines = [
            "# 628 B1 · 独立验证者报告（他验三件套 #1）", "",
            "## 对比表（独立重算 vs 系统口径）", "",
            "| 项目 | 独立重算 | 系统口径 | 一致 |",
            "|---|---|---|---|",
            f"| W2 分布 | {r['w2']['summary']} | IN114/OUT7/UNDEC0 | "
            f"{r['checks']['w2_summary_match']} |",
            f"| W2 逐节点 | vs grounded_labels 冻结输出 | 121 节点 | "
            f"{r['checks']['w2_frozen_labels_match']} |",
            f"| PCK authorized | {r['pck']['authorized']}（{r['pck']['by_status']}） | 27 | "
            f"{r['checks']['pck_authorized_match']} |",
            f"| ledger 哈希链 | {'valid' if r['ledger_chain']['chain_valid'] else 'BROKEN'}"
            f"（{r['ledger_chain']['events']} 条） | 452 条 valid | "
            f"{r['checks']['ledger_chain_valid']} |",
            f"| unique 审查项 | {r['unique']['unique']}（{r['unique']['records']} records） | 93 | "
            f"{r['checks']['unique_match']} |",
            "",
            "## 实现说明", "",
            "- **零 import**：只 import 标准库（json/hashlib/os/sys/argparse/re/typing）。",
            "- W2 朴素重实现：节点 credibility 取自卡面；生效攻击=ledger APPROVE∪MODIFY 去重；",
            "  击败=cred(A)>cred(B) 严格大于；其上求 grounded 不动点。无任何优化或捷径。",
            "- PCK 用**行级最小 YAML 子集解析器**（固定 schema），不用 pyyaml。",
            "- 哈希链公式独立重写：sha256(f\"{prev_hash}|{payload}\")，",
            "  payload=事件 dict 去 self_hash/event_id 后 sort_keys JSON。",
            "",
            "## 他验意义", "",
            "- 这是系统第一次有**不依赖本项目代码的验证**：若 626 求解器/账本工具有隐性 bug，",
            "  独立重算与之不符即暴露。当前全部一致 ⇒ 两个独立实现交叉确认同一结论。",
            "- 局限：验证者仍由本项目作者编写（写代码的人相同），真正的第三方独立需",
            "  外部验证者 + 非对称签名（VSA/B2-B4 是其原型）。",
            "",
            f"- **总判定**：{'全部一致 ✅' if r['all_match'] else '存在不一致 ❌'}",
        ]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
    if args.check:
        return selftest()
    print(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False, indent=2)[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
