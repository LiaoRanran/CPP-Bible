"""642 A4 · 校准追踪器**上岗**（新判决自动累积规则错误率；初值为全库代理，非精确）。

**与 636 的关系**：636（`calibration_tracker_636`）只出**清单**（67/67「无数据」），本模块
把它落成**可累积的追踪器**：新判决发生时自动记账，规则被推翻就累计错误。

上岗三件事（§三 A4）：

1. **记录**：`record(rule_ids, result)` —— 每条命中规则的 `total_count + 1`（append-only 日志）；
2. **推翻**：`overturn(rule_ids)` —— 该规则 `error_count + 1`（并回标日志条目），
   未被推翻时只涨 `total_count`（短期窗口内**全部算未推翻**，这是口径而非事实）；
3. **初值**：从 452 条历史判决**重建全库代理**（改判率 / 人审改判率 / 逃逸率），
   作为 67 条规则的 `known_error_rate` **起点值**并显式标注 `proxy`。

**ECE 三级降级格式**：L1 重校准（ECE > 0.10）/ L2 禁言（> 0.20）/ L3 降级（> 0.30），
沿用 636 口径（本批只提供格式，**不启用**降级动作）。

**诚实登记**（§十.2）：历史数据**无规则归属字段**（638 已实证：ledger 26 字段无 rule_id，
`target_type` 452/452 全为 `edge`）⇒ 规则级错误率**没有真实样本**，
初值是**全库代理**，**不是精确值**；"未被推翻"在短窗口内只是**尚未观察到**，不是"证明没错"。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_calibration_rollout.md`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import calibration_tracker_636 as shadow  # noqa: E402  （67 规则清单单一真源，不复制）

OUT_MD = os.path.join(ROOT, "data", "642_calibration_rollout.md")
LEDGER = shadow.LEDGER
HUMAN_ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")

#: 逃逸率代理是 **616 v7 契约值**（可判分母 1406），**无单一数据文件可复算** ⇒ 只作冻结上下文。
ESCAPE_CONTRACT = (1, 1406)
#: ECE 三级降级阈值（636 口径）
ECE_L1, ECE_L2, ECE_L3 = 0.10, 0.20, 0.30
UNATTRIBUTED = "__unattributed__"


def _read_jsonl(path: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    try:
        for ln in open(path, encoding="utf-8"):
            if ln.strip():
                try:
                    out.append(json.loads(ln))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return out


def history_proxies() -> dict[str, Any]:
    """从历史数据**重建**三个全库代理（每个都标注可复算性与来源）。"""
    rows = _read_jsonl(LEDGER)
    total = len(rows)
    modify = sum(1 for r in rows if str(r.get("result", "")).upper() == "MODIFY")
    ledger_rate = round(modify / total, 4) if total else None

    ann = _read_jsonl(HUMAN_ANN)
    n_ann = len(ann)
    n_mod = sum(1 for r in ann if str(r.get("action", "")).lower() == "modify")
    human_rate = round(n_mod / n_ann, 4) if n_ann else None

    hits, denom = ESCAPE_CONTRACT
    return {
        "ledger_modify_rate": {"value": ledger_rate, "numerator": modify,
                               "denominator": total, "recomputable": True,
                               "source": "data/authority/decision_event_v2_ledger.jsonl"},
        "human_modify_rate": {"value": human_rate, "numerator": n_mod,
                              "denominator": n_ann, "recomputable": True,
                              "source": "data/human_attack_edge_annotations.jsonl"},
        "escape_rate": {"value": round(hits / denom, 4), "numerator": hits,
                        "denominator": denom, "recomputable": False,
                        "source": "616 v7 契约（可判分母 1406，本工具不复算）"},
    }


@dataclasses.dataclass
class RuleStats:
    """单条规则的累积统计。**有自身样本才用实测率**，否则回退全库代理。"""
    rule_id: str
    total_count: int = 0
    error_count: int = 0
    proxy_rate: Optional[float] = None
    proxy_source: str = ""

    @property
    def known_error_rate(self) -> Optional[float]:
        if self.total_count > 0:
            return round(self.error_count / self.total_count, 4)
        return self.proxy_rate

    @property
    def is_proxy(self) -> bool:
        """True = 该值**不是**实测（无自身样本，用的是全库代理）。"""
        return self.total_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {"rule_id": self.rule_id, "total_count": self.total_count,
                "error_count": self.error_count,
                "known_error_rate": self.known_error_rate,
                "is_proxy": self.is_proxy, "proxy_source": self.proxy_source}


class CalibrationTracker:
    """规则错误率累积器。**append-only 日志**：`record()` 只追加，从不改写历史条目。"""

    def __init__(self, rule_ids: list[str], proxy_rate: Optional[float] = None,
                 proxy_source: str = "") -> None:
        self.stats: dict[str, RuleStats] = {
            r: RuleStats(rule_id=r, proxy_rate=proxy_rate, proxy_source=proxy_source)
            for r in rule_ids}
        self.log: list[dict[str, Any]] = []

    # ── 记账 ────────────────────────────────────────────────────────────────
    def record(self, rule_ids: list[str], result: str = "",
               decision_id: str = "") -> dict[str, Any]:
        """一条新判决：命中规则各 `total_count + 1`。**未归属**的判决记入 `UNATTRIBUTED`。"""
        hits = [r for r in rule_ids if r] or [UNATTRIBUTED]
        for r in hits:
            st = self.stats.setdefault(r, RuleStats(rule_id=r))
            st.total_count += 1
        entry = {"seq": len(self.log) + 1, "decision_id": decision_id, "result": result,
                 "rule_ids": hits, "overturned": False}
        self.log.append(entry)
        return entry

    def overturn(self, rule_ids: list[str], decision_id: str = "") -> dict[str, Any]:
        """判决被推翻/修改：命中规则各 `error_count + 1`，并把相关日志条目标记 overturned。"""
        hits = [r for r in rule_ids if r] or [UNATTRIBUTED]
        for r in hits:
            st = self.stats.setdefault(r, RuleStats(rule_id=r))
            st.error_count += 1
        marked = 0
        for e in self.log:
            if decision_id and e["decision_id"] == decision_id:
                e["overturned"] = True
                marked += 1
        return {"rule_ids": hits, "error_counted": len(hits), "log_marked": marked}

    # ── 输出 ────────────────────────────────────────────────────────────────
    def snapshot(self) -> dict[str, Any]:
        rows = [s.to_dict() for s in self.stats.values()]
        real = [r for r in rows if not r["is_proxy"]]
        return {"n_rules": len(rows), "n_with_samples": len(real),
                "n_proxy": len(rows) - len(real), "rows": rows,
                "n_log_entries": len(self.log)}

    @staticmethod
    def ece_format() -> dict[str, Any]:
        return {
            "per_verifier": "ECE = Σ_b (n_b/N) × |acc(b) − conf(b)|（b 为置信分桶）",
            "domains": ["简单", "中等", "复杂"],
            "degradation": {
                f"L1 重校准(ECE>{ECE_L1:.2f})": "重校准置信映射",
                f"L2 禁言(ECE>{ECE_L2:.2f})": "该验证器不单独判 block",
                f"L3 降级(ECE>{ECE_L3:.2f})": "降级为 advice",
            },
            "enabled": False,
            "note": "本批只提供格式，**不启用任何降级动作**（不改判决）。",
        }


def build_tracker() -> CalibrationTracker:
    """上线态追踪器：67 规则 + 全库代理初值（改判率）。"""
    prox = history_proxies()
    rate = prox["ledger_modify_rate"]["value"]
    t = CalibrationTracker(shadow_rules(), proxy_rate=rate,
                           proxy_source="全库代理：ledger 改判率（MODIFY/总数）")
    return t


def shadow_rules() -> list[str]:
    """67 规则 id（636 单一真源；gate_engine 不可用时回退空表）。"""
    return [r["id"] for r in shadow.rules()]


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "代理初值被当成实测值使用（最危险）",
         "trigger": "有人引用 `known_error_rate` 而忽略 `is_proxy=True`",
         "rollback": "每个值都带 `is_proxy` 字段 + 报告显式标注；"
                     "对接方必须判 `is_proxy` 再决定是否采信"},
        {"risk": "「未被推翻」被当成「没错」（短窗口必然全未推翻）",
         "trigger": "用 `known_error_rate=0` 推断规则无错",
         "rollback": "只统计 `total_count`，**不把 0 当作证据**；"
                     "报告登记「未推翻 ≠ 证明无误」"},
        {"risk": "「命中规则」缺失（ledger 无 rule_id）⇒ 归入 `__unattributed__`",
         "trigger": "未归属桶计数远超已归属桶",
         "rollback": "不改判定；把未归属量作为**数据缺口指标**上报（信号而非噪声）"},
    ]


def write_report() -> str:
    prox = history_proxies()
    snap = build_tracker().snapshot()        # 上线**初值态**（未记任何新判决）
    t = build_tracker()
    # 演示：3 条新判决，其中 1 条被推翻
    rules = shadow_rules()
    e1 = t.record(rules[:2], "APPROVE", "NEW-001")
    t.record(rules[:2], "APPROVE", "NEW-002")
    t.overturn(rules[:2], "NEW-001")
    ece = t.ece_format()
    lines = [
        "# 642 A4 · 校准追踪器上岗（规则错误率自动累积；初值为**全库代理**）", "",
        "## 一、全库代理重建（可复算性已标注）", "",
        "| 代理 | 值 | 分子/分母 | 可复算 | 来源 |", "|---|---|---|---|---|"]
    for k, v in prox.items():
        lines.append(f"| {k} | **{v['value']}** | {v['numerator']}/{v['denominator']} | "
                     f"{'✅' if v['recomputable'] else '⛔ 冻结契约'} | {v['source']} |")
    lines += ["", "## 二、67 规则 known_error_rate 初值（**全部为代理**）", "",
              f"- 规则总数：**{snap['n_rules']}**；有自身样本：**{snap['n_with_samples']}**；"
              f"用代理：**{snap['n_proxy']}**",
              f"- 代理值 = {prox['ledger_modify_rate']['value']}"
              f"（ledger 改判率 {prox['ledger_modify_rate']['numerator']}/"
              f"{prox['ledger_modify_rate']['denominator']}）", "",
              "| 规则 | total | error | known_error_rate | 是代理 | 代理来源 |",
              "|---|---|---|---|---|---|"]
    for r in snap["rows"]:
        lines.append(f"| `{r['rule_id']}` | {r['total_count']} | {r['error_count']} | "
                     f"{r['known_error_rate']} | {'⚠️ 是' if r['is_proxy'] else '否'} | "
                     f"{r['proxy_source']} |")
    lines += ["", "## 三、新判决累积演示（3 条，其中 1 条被推翻）", "",
              "| seq | decision_id | 结果 | 命中规则 | 已推翻 |", "|---|---|---|---|---|"]
    for e in t.log:
        lines.append(f"| {e['seq']} | {e['decision_id']} | {e['result']} | "
                     f"`{'`,`'.join(e['rule_ids'])}` | {'✅' if e['overturned'] else '—'} |")
    hit = t.stats[rules[0]]
    lines += ["", f"- `{rules[0]}`：total={hit.total_count}，error={hit.error_count}，"
                  f"`known_error_rate={hit.known_error_rate}`（**自身样本 2 条**，已不再是代理）;",
              f"- 首次命中记录：`{json.dumps(e1, ensure_ascii=False)}`", "",
              "## 四、ECE 三级降级格式（**只提供格式，不启用**）", "",
              f"- 每验证器：`{ece['per_verifier']}`",
              f"- 分域：{ece['domains']}",
              f"- 启用：**{ece['enabled']}**（本批不改判决）", "",
              "| 级别 | 阈值 | 动作 |", "|---|---|---|"]
    for k, v in ece["degradation"].items():
        lines.append(f"| {k} | — | {v} |")
    lines += ["", "## 五、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **初值不是精确值**（§十.2）：历史无规则归属字段（638 实证）⇒ 67/67 用的是"
              "**全库代理**，逐条 `is_proxy=True`；",
              "2. **逃逸率代理不可复算**（分母 1406 是 616 v7 契约，无单一数据文件）⇒ 标为冻结上下文；",
              "3. **「未推翻」≠「没错」**：短窗口内必然全部未推翻，只涨 `total_count`，"
              "不得把 `known_error_rate=0` 当作证据；",
              "4. 日志 **append-only**：`record()` 只追加，`overturn()` 只回标 `overturned` 字段"
              "（不改数值、不删条目）；",
              "5. **不改任何判决**、不启用任何降级动作；"
              "本模块只记账，是否按错误率调整规则由人裁决。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    t = CalibrationTracker(["R1", "R2"], proxy_rate=0.1881, proxy_source="proxy")
    chk("初始为代理（无自身样本）", t.stats["R1"].is_proxy is True
        and t.stats["R1"].known_error_rate == 0.1881)

    t.record(["R1"], "APPROVE", "D1")
    chk("未推翻 ⇒ 只涨 total", t.stats["R1"].total_count == 1
        and t.stats["R1"].error_count == 0)
    t.overturn(["R1"], "D1")
    chk("推翻 ⇒ error+1", t.stats["R1"].error_count == 1)
    chk("有样本后用实测率", t.stats["R1"].is_proxy is False
        and t.stats["R1"].known_error_rate == 1.0)
    chk("推翻回标日志", t.log[0]["overturned"] is True)

    t.record([], "APPROVE", "D2")
    chk("无规则归属 ⇒ 记入未归属桶", UNATTRIBUTED in t.stats)

    # error_rate 算术：2 错 / 4 总 = 0.5
    t2 = CalibrationTracker(["R3"])
    for i in range(4):
        t2.record(["R3"], "APPROVE", f"X{i}")
    t2.overturn(["R3"], "X0")
    t2.overturn(["R3"], "X1")
    chk("error_rate = error/total", t2.stats["R3"].known_error_rate == 0.5)

    ece = CalibrationTracker.ece_format()
    chk("ECE 三级降级", len(ece["degradation"]) == 3)
    chk("ECE 阈值递增", ECE_L1 < ECE_L2 < ECE_L3)
    chk("ECE 不启用", ece["enabled"] is False)

    prox = history_proxies()
    chk("ledger 改判率可复算", prox["ledger_modify_rate"]["recomputable"] is True
        and prox["ledger_modify_rate"]["numerator"] == 85
        and prox["ledger_modify_rate"]["denominator"] == 452)
    chk("人审改判率可复算", prox["human_modify_rate"]["value"] == 0.0876)
    chk("逃逸率为冻结契约", prox["escape_rate"]["recomputable"] is False)
    chk("67 规则", len(shadow_rules()) == 67, str(len(shadow_rules())))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A4 校准追踪器上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写上岗报告")
    ap.add_argument("--json", action="store_true", help="打印代理重建（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    prox = history_proxies()
    if a.json:
        print(json.dumps(prox, ensure_ascii=False, indent=2))
        return 0
    snap = build_tracker().snapshot()
    print(f"[calibration] 规则 {snap['n_rules']}；有样本 {snap['n_with_samples']}；"
          f"用代理 {snap['n_proxy']}；代理值="
          f"{prox['ledger_modify_rate']['value']}（改判率，非精确）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
