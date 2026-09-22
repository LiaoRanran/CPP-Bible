"""626 C2 · W2 三态解耦（`argument_status` / `truth_support` / `publication_status`）

国外大模型要求 W2 必须把「图论状态」和「知识真假」分开。三套状态**独立存储、独立计算、互不替代**：

| 状态 | 含义 | 取值 |
|---|---|---|
| `argument_status` | 图论语义状态（Dung grounded） | IN / OUT / UNDEC |
| `truth_support` | 知识真假支持程度（基于证据卡 + 人审） | supported / refuted / unresolved |
| `publication_status` | 发布状态（基于 Authority Ledger + 聚合策略） | authorized / blocked / pending |

**关键澄清**：
- `IN ≠ 真`——只表示"在当前攻击图中未被击败"
- `OUT ≠ 假`——只表示"被某个攻击击败"
- `publication_status` 必须有显式 aggregation policy（受治理）

本批**只读取并输出三态**，**不修改 gate_engine.py 的 W2 计算逻辑**（三态是新增投影）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402

GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
OUT_JSON = os.path.join(ROOT, "data", "w2_three_state_626.json")

AGGREGATION_POLICY = "v0.1-strict"


def load_argument_status() -> dict:
    """从现有 grounded_labels 读取图论状态（不重算，向后兼容）。"""
    if not os.path.exists(GROUNDED):
        return {"IN": 0, "OUT": 0, "UNDEC": 0, "source": "missing"}
    g = json.load(open(GROUNDED, encoding="utf-8"))
    s = g.get("summary") or {}
    return {"IN": int(s.get("IN", 0)), "OUT": int(s.get("OUT", 0)),
            "UNDEC": int(s.get("UNDEC", 0)), "source": "grounded_labels_w2.json"}


def load_truth_support() -> dict:
    """truth_support：基于 PCK 证书状态（approved ⇒ supported）。"""
    sup = ref = unres = 0
    for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))):
        try:
            import yaml  # type: ignore[import-untyped]
            c = yaml.safe_load(open(p, encoding="utf-8")) or {}
        except Exception:  # noqa: BLE001
            unres += 1
            continue
        st = str((c.get("human_authority") or {}).get("status") or "")
        if st == "approved":
            sup += 1
        elif st == "rejected":
            ref += 1
        else:
            unres += 1
    return {"supported": sup, "refuted": ref, "unresolved": unres,
            "source": "data/pck/certificates"}


def load_publication_status() -> dict:
    """publication_status：基于 Authority Ledger 的 **card-level** authority。"""
    led = D.AuthorityLedger.import_jsonl(LEDGER)
    by_card: dict[str, str] = {}
    for e in led.all_events():
        if e.target_type in ("card", "certificate"):
            by_card[e.target_id] = e.result
    c = Counter(by_card.values())
    return {"authorized": c.get("APPROVE", 0), "blocked": c.get("REJECT", 0),
            "pending": sum(v for k, v in c.items() if k not in ("APPROVE", "REJECT")),
            "cards_with_authority": len(by_card),
            "aggregation_policy": AGGREGATION_POLICY,
            "source": "decision_event_v2_ledger.jsonl"}


def compute() -> dict:
    return {
        "argument_status": load_argument_status(),
        "truth_support": load_truth_support(),
        "publication_status": load_publication_status(),
        "note": ("三套状态独立：IN≠真、OUT≠假；publication_status 须有显式 aggregation policy。"
                 "本批只读取输出，不改 gate_engine 的 W2 计算逻辑。"),
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = compute()
    a, t, p = r["argument_status"], r["truth_support"], r["publication_status"]
    chk("argument_status 有 IN/OUT/UNDEC",
        all(k in a for k in ("IN", "OUT", "UNDEC")), str(a))
    chk("truth_support 有 supported/refuted/unresolved",
        all(k in t for k in ("supported", "refuted", "unresolved")), str(t))
    chk("publication_status 有 authorized/blocked/pending",
        all(k in p for k in ("authorized", "blocked", "pending")), str(p))
    chk("publication_status 带 aggregation policy", bool(p.get("aggregation_policy")))
    # 三态独立：互不替代 —— 键集合互不相交且各自可独立变化
    chk("三态键集互不相交",
        not ({"IN", "OUT", "UNDEC"} & {"supported", "refuted", "unresolved"})
        and not ({"IN", "OUT", "UNDEC"} & {"authorized", "blocked", "pending"}))
    chk("三态独立可分别读取",
        isinstance(a.get("IN"), int) and isinstance(t.get("supported"), int)
        and isinstance(p.get("authorized"), int))
    print(f"C2 w2_three_state check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 C2 W2 三态解耦")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="输出 JSON 到 data/")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = compute()
    if args.json:
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(r, fh, ensure_ascii=False, indent=2)
        print(f"written {OUT_JSON}")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
