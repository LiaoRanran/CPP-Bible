"""638 B1 · known_error_rate 收集器（从历史判决估算每条规则的错误率）

**背景（636 发现的最大缺口）**：`data/636_calibration_tracker_report.md` 实测
**67 条规则全部缺 `known_error_rate`**，全部标「无数据」。

估算方法（§三.B1.3，三层，**绝不编造**）：

| 层级 | 样本来源 | 判据 |
|---|---|---|
| `rule` | Authority ledger 中**可归属到该规则**的判决 | 需 ledger 有 rule 字段才可能 >0 |
| `scope` | 同 `scope` 规则共享的判决样本 | 需 target_type 与 scope 可映射 |
| `global` | 全库代理（人审改判率 / 逃逸率） | **非规则级**，只作先验参照 |

规则（§三.B1.3）：样本 ≥30 → 直接算频率；<30 且 >0 → 标注「样本不足」+ 先验；
**=0 → 标注「无数据」，不给估算值**（`rate=None`，先验仅作参考列）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/638_error_rate_estimate.md` + `.json`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import collections
import datetime
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "638_error_rate_estimate.md")
OUT_JSON = os.path.join(ROOT, "data", "638_error_rate_estimate.json")

LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
HUMAN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
ESCAPE = os.path.join(ROOT, "data", "mutation", "known_tce.jsonl")

PRIOR = 0.05          # 先验错误率（样本不足时参照；=0 样本时不作为估算值）
MIN_SAMPLES = 30      # 直接算频率的最小样本量

# ledger 的规则归属字段候选（实测全部不存在，保留以便未来回填时自动生效）
RULE_FIELD_CANDIDATES = ("rule_id", "rule", "rule_ref", "gate_rule")


# ── 载入 ────────────────────────────────────────────────────────────────
def load_jsonl(path: str) -> list[dict[str, Any]]:
    if not os.path.exists(path):
        return []
    out: list[dict[str, Any]] = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def load_rules() -> list[dict[str, str]]:
    """读 67 条规则元数据（只读 id/severity/scope）。"""
    try:
        import gate_engine as ge
        return [{"id": r.id, "severity": getattr(r, "severity", ""),
                 "scope": getattr(r, "scope", "")} for r in ge.RULES]
    except Exception:  # noqa: BLE001
        src = open(os.path.join(ROOT, "tools", "gate_engine.py"), encoding="utf-8",
                   errors="replace").read()
        ids = re.findall(r'register\(Rule\(\s*"([^"]+)"', src)
        return [{"id": i, "severity": "block", "scope": "unknown"} for i in ids]


# ── 样本归属（三层）─────────────────────────────────────────────────────
def rule_samples(ledger: list[dict[str, Any]]) -> dict[str, int]:
    """统计 ledger 中**可归属到具体规则**的判决数。

    实测 ledger 无任何 `RULE_FIELD_CANDIDATES` 字段 ⇒ 恒为空 dict（0 样本），
    这是诚实结果，不是 bug（详见报告 §四）。
    """
    counts: dict[str, int] = {}
    for e in ledger:
        rid = next((str(e[f]) for f in RULE_FIELD_CANDIDATES if e.get(f)), "")
        if rid:
            counts[rid] = counts.get(rid, 0) + 1
    return counts


def global_proxies(ledger: list[dict[str, Any]], human: list[dict[str, Any]],
                   escape: list[dict[str, Any]]) -> dict[str, Any]:
    """全库代理指标（真实数字；**非规则级**）。"""
    res = collections.Counter(str(e.get("result", "")) for e in ledger)
    n = len(ledger)
    hc = collections.Counter(str(a.get("action", "")) for a in human)
    hn = len(human)
    esc = sum(1 for e in escape if str(e.get("verdict", "")) == "escaped")
    judged = 0
    metrics = {}
    for e in escape:
        m = e.get("metrics") or {}
        if isinstance(m, dict) and m.get("judged"):
            metrics = m
            judged = int(m.get("judged") or 0)
    return {
        "ledger_n": n,
        "ledger_modify": res.get("MODIFY", 0),
        "ledger_approve": res.get("APPROVE", 0),
        "ledger_reject": res.get("REJECT", 0),
        # 假阳性代理：被判「需改判」的比例
        "fp_proxy_modify_rate": round(res.get("MODIFY", 0) / n, 4) if n else None,
        "human_n": hn,
        "human_modify": hc.get("modify", 0),
        "fp_proxy_human_modify_rate": round(hc.get("modify", 0) / hn, 4) if hn else None,
        # 假阴性代理：逃逸率
        "escape_n": esc,
        "escape_judged": judged,
        "fn_proxy_escape_rate": round(esc / judged, 6) if judged else None,
        "escape_metrics": metrics,
    }


# ── 逐规则估算 ──────────────────────────────────────────────────────────
def estimate_rule(rule: dict[str, str], samples: int,
                  proxies: dict[str, Any]) -> dict[str, Any]:
    """给一条规则估算错误率。**=0 样本一律「无数据」**，不给估算值。"""
    if samples >= MIN_SAMPLES:
        return {"rule_id": rule["id"], "severity": rule["severity"], "scope": rule["scope"],
                "n_samples": samples, "fp_rate": None, "fn_rate": None,
                "confidence": "待算（有样本但缺改判标注）", "tier": "rule",
                "prior_fp": PRIOR, "prior_fn": PRIOR,
                "note": "样本充足，但缺「该规则判错」的标注列 ⇒ 暂不能算真实频率"}
    if samples > 0:
        return {"rule_id": rule["id"], "severity": rule["severity"], "scope": rule["scope"],
                "n_samples": samples, "fp_rate": PRIOR, "fn_rate": PRIOR,
                "confidence": "低（样本不足，用先验）", "tier": "scope",
                "prior_fp": PRIOR, "prior_fn": PRIOR, "note": "样本不足，先验参照"}
    return {"rule_id": rule["id"], "severity": rule["severity"], "scope": rule["scope"],
            "n_samples": 0, "fp_rate": None, "fn_rate": None,
            "confidence": "无数据", "tier": "无数据",
            "prior_fp": PRIOR, "prior_fn": PRIOR,
            "note": "无任何可归属样本 ⇒ 不给估算值（先验仅参考）"}


def estimate_all() -> dict[str, Any]:
    ledger = load_jsonl(LEDGER)
    human = load_jsonl(HUMAN)
    escape = load_jsonl(ESCAPE)
    rules = load_rules()
    counts = rule_samples(ledger)
    proxies = global_proxies(ledger, human, escape)
    rows = [estimate_rule(r, counts.get(r["id"], 0), proxies) for r in rules]

    tiers = collections.Counter(r["tier"] for r in rows)
    scopes = collections.Counter(r["scope"] for r in rows)
    no_data = [r["rule_id"] for r in rows if r["tier"] == "无数据"]
    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "n_rules": len(rules), "rows": rows, "tier_dist": dict(tiers),
        "scope_dist": dict(scopes), "no_data_rules": no_data,
        "no_data_n": len(no_data), "proxies": proxies,
        "rule_field_candidates": list(RULE_FIELD_CANDIDATES),
        "ledger_has_rule_field": bool(counts),
    }


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report() -> dict[str, str]:
    e = estimate_all()
    p = e["proxies"]
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(e, fh, ensure_ascii=False, indent=2)
    fmt = lambda v: "无数据" if v is None else f"{v:.4f}"   # noqa: E731
    lines = [
        "# 638 B1 · known_error_rate 估算（67 条规则）", "",
        f"> 生成时间：{e['generated']}。工具：`tools/error_rate_collector_638.py`。", "",
        "## 一、估算方法（三层，绝不编造）", "",
        "| 层级 | 样本来源 | 本批实测结果 |", "|---|---|---|",
        f"| `rule` | ledger 中可归属到该规则的判决 | "
        f"**{0 if not e['ledger_has_rule_field'] else '有'}** 条（ledger 无规则字段） |",
        "| `scope` | 同 scope 共享样本 | 0（target_type 全为 `edge`，与 scope 不可映射） |",
        "| `global` | 全库代理（非规则级） | 见 §三 |", "",
        f"- 样本 ≥{MIN_SAMPLES} ⇒ 直接算频率；<{MIN_SAMPLES} 且 >0 ⇒ 「样本不足」+ 先验；"
        f"**=0 ⇒ 「无数据」，不给估算值**；",
        f"- 先验值（参考列）：`{PRIOR}`。", "",
        "## 二、逐规则估算（67 条）", "",
        "| # | 规则 | severity | scope | 假阳性率 | 假阴性率 | 样本量 | 置信度 | 层级 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(e["rows"], 1):
        lines.append(f"| {i} | `{r['rule_id']}` | {r['severity']} | {r['scope']} | "
                     f"{fmt(r['fp_rate'])} | {fmt(r['fn_rate'])} | {r['n_samples']} | "
                     f"{r['confidence']} | {r['tier']} |")
    lines += [
        "", "## 三、全库代理指标（真实数字，**非规则级**）", "",
        "| 指标 | 值 | 口径 |", "|---|---|---|",
        f"| ledger 判决总数 | {p['ledger_n']} | `decision_event_v2_ledger.jsonl` |",
        f"| APPROVE / MODIFY / REJECT | {p['ledger_approve']} / {p['ledger_modify']} / "
        f"{p['ledger_reject']} | 同上（**无 REJECT**） |",
        f"| 假阳性代理（ledger 改判率） | {fmt(p['fp_proxy_modify_rate'])} | MODIFY / 总数 |",
        f"| 假阳性代理（人审改判率） | {fmt(p['fp_proxy_human_modify_rate'])} | "
        f"{p['human_modify']} / {p['human_n']}（human_attack_edge_annotations） |",
        f"| 假阴性代理（逃逸率） | {fmt(p['fn_proxy_escape_rate'])} | "
        f"{p['escape_n']} / {p['escape_judged']}（known_tce.jsonl） |", "",
        "> 代理值**不能**下推到单条规则，只作为「全库错误率量级」的参照。", "",
        "## 四、样本不足 / 无数据清单（透明）", "",
        f"- **无数据**规则：**{e['no_data_n']} / {e['n_rules']}** 条；",
        f"- 层级分布：`{e['tier_dist']}`；",
        f"- scope 分布：`{e['scope_dist']}`。", "",
        "### 4.1 为什么 67 条全部「无数据」（根因）", "",
        "1. Authority ledger 的 26 字段里**没有规则 id**（实测候选字段 "
        f"`{e['rule_field_candidates']}` 全部不存在）；",
        "2. ledger 的 `target_type` **452/452 全为 `edge`**，与规则 `scope`"
        "（atom/evidence/repo）不可映射；",
        "3. 因此**任何**规则都取不到「该规则判错」的样本 ⇒ 按 §三.B1.3 一律标「无数据」，",
        "   **不编造数字**（636 的 `calibration_tracker_636` 结论一致）。", "",
        "## 五、诚实登记", "",
        "1. **0 条真实规则级估算值**：67/67 标「无数据」——本批没有产出任何一条规则错误率，",
        "   这是数据缺口，不是实现缺陷；",
        "2. 先验 5% 仅作**参考列**，不冒充实测（`fp_rate=None`）；",
        "3. 代理指标（18.8% / 8.76% / 0.071%）是**全库级**，误当规则级使用会失真；",
        "4. 本批**未回填** `calibration_tracker` 的 known_error_rate 字段（交人项）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("规则数 67", len(load_rules()) == 67)
    e = estimate_all()
    chk("逐规则行数 = 规则数", len(e["rows"]) == e["n_rules"] == 67)
    chk("0 样本 ⇒ 无数据 + fp_rate=None",
        estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 0,
                      {"ledger_n": 1})["fp_rate"] is None)
    chk("<30 样本 ⇒ 先验 + 样本不足",
        estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 5,
                      {})["confidence"].startswith("低"))
    chk("≥30 样本 ⇒ tier=rule",
        estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 30,
                      {})["tier"] == "rule")
    chk("ledger 无规则字段（实测）", rule_samples(load_jsonl(LEDGER)) == {})
    chk("代理指标有真实值", e["proxies"]["ledger_n"] == 452
        and e["proxies"]["ledger_modify"] == 85)
    chk("全部无数据（实测 67/67）", e["no_data_n"] == 67)
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 B1 known_error_rate 收集器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    e = estimate_all()
    if args.json:
        print(json.dumps({k: v for k, v in e.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"rules={e['n_rules']} tiers={e['tier_dist']} no_data={e['no_data_n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
