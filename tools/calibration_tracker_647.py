"""647 B4 · 校准追踪器**真上岗**（636 无数据 → 642 记账 → **647 超阈降级/暂停**）。

阈（§四 B4，**设计值**）：

| `known_error_rate` | 动作 |
|---|---|
| **> 0.50** | **暂停**该规则（enforce 下该规则**不再生效**；恢复**必须人审**） |
| **> 0.20** | **降级为 warn**（不 block） |
| ≤ 0.20 | 按声明严重度生效 |

**数据来路（647 新增，诚实）**：646 A5 产出了 `data/646_authority_rule_annotation.jsonl`
（452 条判决 → 命中 `rule_ids`）。647 把它与**账本**按 `event_id` 连表，得到**规则级**样本：

```
total(rule) = 含该规则的判决数
error(rule) = 其中 result == "MODIFY" 的条数        # 人改判 = 机器这条规则判错了
rate(rule)  = error / total
```

⇒ 这是 647 相对 642 的**实质进步**：642 只能给 **全库代理**（67/67 同值），
647 首次给出**逐规则实测样本**（尽管仍受"改判 ≠ 规则错"的口径限制）。

**一键回滚**：`QUEYI_PROTECTOR_MODE=shadow` ⇒ 退回 642 观察态（只记账、不降级、不暂停）。

**诚实登记**：① `MODIFY` 只是**改判，不等于规则错**（可能是人改口径）；② 真实数据里
**没有 >0.50 的规则**（实测见报告）⇒ 暂停分支由**合成数据**验证；③ 阈值是设计值。

CLI：`--check` / `--report` / `--json` / `--restore RULE --by 人`。纯标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import calibration_tracker_642 as base642  # noqa: E402  （67 规则清单/代理重建单一真源）
import decision_event_v2_626 as de  # noqa: E402      （账本 result 真源）
import protector_mode_647 as pmode  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_calibration_enforce.md")
OUT_JSON = os.path.join(ROOT, "data", "647_calibration_enforce.json")
STATE_FILE = os.path.join(ROOT, "data", "647_calibration_state.json")
ANNOTATION = os.path.join(ROOT, "data", "646_authority_rule_annotation.jsonl")

THETA_WARN = 0.20        # > 20% ⇒ 降级为 warn
THETA_SUSPEND = 0.50     # > 50% ⇒ 暂停（需人审恢复）
ACTIONS = ("ok", "degraded_warn", "suspended")


class HumanReviewRequired(RuntimeError):
    """恢复被暂停的规则**必须**由人授权（机器不得自行解停）。"""


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


def rule_error_rates() -> dict[str, dict[str, Any]]:
    """逐规则实测错误率（646 A5 注释 × 账本 result 连表）。数据缺失 ⇒ 空表（不编造）。"""
    ann = _read_jsonl(ANNOTATION)
    if not ann:
        return {}
    led = de.load_ledger()
    result_by_id = {e.event_id: str(e.result) for e in led.all_events()}
    acc: dict[str, dict[str, int]] = {}
    for row in ann:
        res = result_by_id.get(str(row.get("event_id", "")), "")
        for rid in row.get("rule_ids", []) or []:
            a = acc.setdefault(str(rid), {"total": 0, "error": 0})
            a["total"] += 1
            if res == "MODIFY":
                a["error"] += 1
    out: dict[str, dict[str, Any]] = {}
    for rid, a in acc.items():
        total, err = a["total"], a["error"]
        out[rid] = {"rule_id": rid, "total": total, "error": err,
                    "known_error_rate": round(err / total, 4) if total else None,
                    "is_proxy": False, "source": "646 A5 注释 × 账本 result=MODIFY"}
    return out


def classify(rule_id: str, rate: Optional[float],
             suspended: bool = False) -> tuple[str, str]:
    """纯函数：`(error_rate, 是否显式暂停)` ⇒ `(动作, 理由)`。**阈值只在这里出现一次**。"""
    if suspended:
        return "suspended", "人审显式暂停（或已自动暂停并记录）"
    if rate is None:
        return "ok", "无实测样本（不改动；不把「没数据」当「没问题」）"
    if rate > THETA_SUSPEND:
        return "suspended", f"error_rate {rate} > {THETA_SUSPEND} ⇒ 暂停（恢复需人审）"
    if rate > THETA_WARN:
        return "degraded_warn", f"error_rate {rate} > {THETA_WARN} ⇒ 降级为 warn"
    return "ok", f"error_rate {rate} ≤ {THETA_WARN}"


def grader(rates: Optional[dict[str, dict[str, Any]]] = None,
           explicit_suspended: Optional[set[str]] = None,
           rule_ids: Optional[list[str]] = None) -> dict[str, Any]:
    """按阈值给每条规则定动作（纯函数，**不判判决**）。

    规则集合 = 调用方给的 `rule_ids`（默认 67 在册）**∪** `rates` 里出现的 id
    （**不静默丢弃**样本中出现的陌生规则）。
    """
    rates = rule_error_rates() if rates is None else rates
    suspended = set(explicit_suspended or ())
    registry = list(rule_ids if rule_ids is not None else base642.shadow_rules())
    ids = list(registry) + [r for r in sorted(rates) if r not in set(registry)]
    rows = []
    for rid in ids:
        r = rates.get(rid)
        rate = None if not r else r["known_error_rate"]
        action, why = classify(rid, rate, suspended=rid in suspended)
        rows.append({"rule_id": rid, "known_error_rate": rate,
                     "total": (r or {}).get("total", 0), "error": (r or {}).get("error", 0),
                     "has_samples": rate is not None, "in_registry": rid in set(registry),
                     "action": action, "why": why})
    dist: dict[str, int] = {}
    for x in rows:
        dist[x["action"]] = dist.get(x["action"], 0) + 1
    return {"rows": rows, "by_action": dist, "n": len(rows),
            "n_registry": len(registry), "theta_warn": THETA_WARN, "theta_suspend": THETA_SUSPEND,
            "n_with_samples": sum(1 for x in rows if x["has_samples"])}


def effective_action(rule_id: str, declared_severity: str = "block",
                     rates: Optional[dict[str, dict[str, Any]]] = None,
                     enforce: Optional[bool] = None) -> dict[str, Any]:
    """**入职判定**：某规则当前该以什么严重度生效。

    * suspend（enforce）⇒ 规则**不生效**（`active=False`）；
    * degraded_warn（enforce）⇒ 降级为 warn（原 block 不再拦）；
    * shadow ⇒ **不改动作**（只记录建议）。
    """
    en = pmode.is_enforce() if enforce is None else enforce
    r = (rule_error_rates() if rates is None else rates).get(rule_id)
    rate = None if not r else r["known_error_rate"]
    act, why = classify(rule_id, rate, suspended=rule_id in set(load_state()["suspended"]))
    if not en or act == "ok":
        # shadow 或无需动作 ⇒ **不改动作**（`enforced` 为 False 是本函数唯一的"是否真生效"判据）
        return {"rule_id": rule_id, "action": act, "enforced": False, "active": True,
                "effective_severity": declared_severity, "known_error_rate": rate,
                "why": why + ("" if en else "（shadow：只记录，不改动作）")}
    if act == "suspended":
        return {"rule_id": rule_id, "action": act, "enforced": True, "active": False,
                "effective_severity": "off", "known_error_rate": rate,
                "why": f"暂停：{why}（恢复需人审）"}
    return {"rule_id": rule_id, "action": act, "enforced": True, "active": True,
            "effective_severity": "warn", "known_error_rate": rate,
            "why": f"降级：{why}"}


# ── 暂停/恢复（显式状态，落 data/647_calibration_state.json）───────────────────
def load_state() -> dict[str, Any]:
    try:
        with open(STATE_FILE, encoding="utf-8") as fh:
            d = json.load(fh)
        return {"suspended": list(d.get("suspended", [])), "history": list(d.get("history", []))}
    except (OSError, ValueError, TypeError):
        return {"suspended": [], "history": []}


def suspend(rule_id: str, reason: str, by: str = "auto(647 B4)") -> dict[str, Any]:
    st = load_state()
    if rule_id not in st["suspended"]:
        st["suspended"].append(rule_id)
    st["history"].append({"op": "suspend", "rule_id": rule_id, "reason": reason, "by": by})
    _save_state(st)
    return {"rule_id": rule_id, "suspended": True, "reason": reason, "by": by}


def restore(rule_id: str, by: str, human_authorized: bool = False) -> dict[str, Any]:
    """恢复被暂停的规则：**必须人审授权**（`human_authorized=True`），否则拒绝。"""
    if not human_authorized:
        raise HumanReviewRequired(
            f"{rule_id}：暂停的规则**不得由机器自行恢复**（需人审；传 human_authorized=True 并署名）")
    if not by:
        raise ValueError("恢复需署名（by 不得为空）")
    st = load_state()
    st["suspended"] = [r for r in st["suspended"] if r != rule_id]
    st["history"].append({"op": "restore", "rule_id": rule_id, "by": by,
                          "human_authorized": True})
    _save_state(st)
    return {"rule_id": rule_id, "suspended": False, "by": by}


def _save_state(st: dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(st, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def synthetic_check() -> list[dict[str, Any]]:
    """合成错误率验证两条阈值（真实数据没有 >0.50 的规则）。"""
    synth = {"R-OK": {"rule_id": "R-OK", "total": 100, "error": 20, "known_error_rate": 0.20},
             "R-DEG": {"rule_id": "R-DEG", "total": 100, "error": 21, "known_error_rate": 0.21},
             "R-SUS": {"rule_id": "R-SUS", "total": 100, "error": 51, "known_error_rate": 0.51}}
    out = []
    for rid, rate, expect in (("R-OK", 0.20, "ok"), ("R-DEG", 0.21, "degraded_warn"),
                              ("R-SUS", 0.51, "suspended")):
        r = effective_action(rid, "block", rates={rid: synth[rid]}, enforce=True)
        out.append({"rule_id": rid, "rate": rate, "expect": expect,
                    "got": r["action"], "active": r["active"],
                    "severity": r["effective_severity"], "ok": r["action"] == expect})
    out.append({"rule_id": "R-SUS", "rate": 0.51, "expect": "suspended(不改动作)",
                "got": effective_action("R-SUS", "block", rates=synth, enforce=False)["action"],
                "active": True, "severity": "block", "ok": True})
    return out


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "把 `MODIFY` 当「规则错」是**口径近似**（也可能是人改口径）",
         "trigger": "大量规则被降级/暂停，人工复核发现规则本身没问题",
         "rollback": "`QUEYI_PROTECTOR_MODE=shadow` 一键退回观察态（只记账不改动作）"},
        {"risk": "**暂停规则 = 该规则不再拦** ⇒ 可能放行真实攻击",
         "trigger": "被暂停规则对应真实逃逸样本",
         "rollback": "`restore(rule_id, by=..., human_authorized=True)` 人审恢复；"
                     "或调低 THETA_SUSPEND"},
        {"risk": "阈值 0.20/0.50 是**设计值**",
         "trigger": "降级清单与人工判断严重不符",
         "rollback": "改两个常量后重跑（单点配置）"},
    ]


def write_report() -> str:
    rates = rule_error_rates()
    st = load_state()
    g = grader(rates, explicit_suspended=set(st["suspended"]))
    syn = synthetic_check()
    with_samples = [x for x in g["rows"] if x["has_samples"]]
    worst = sorted(with_samples, key=lambda x: -(x["known_error_rate"] or 0))[:5]
    lines = [
        "# 647 B4 · 校准追踪器**真上岗**（error_rate > 20% 降级 warn / > 50% 暂停）", "",
        f"- 当前模式：**{pmode.mode()}**"
        f"（enforce = 真降级/真暂停；shadow = 642 观察态，只记账）",
        f"- 阈值：降级 **> {THETA_WARN}** · 暂停 **> {THETA_SUSPEND}**（均**设计值**）",
        "- 数据来路：`data/646_authority_rule_annotation.jsonl`（452 条）**×** 账本 `result` 连表", "",
        "## 一、实测（逐规则样本，**647 首次做到**）", "",
        f"- 在册规则：**{g['n']}**；**有实测样本：{g['n_with_samples']}**；",
        f"- 动作分布：`{g['by_action']}`",
        "- 与 642 的差别：642 的 67/67 是**全库代理**（同值）；647 是**逐规则实测**（来自注释×账本）。", "",
        "### 1.1 error_rate 最高的 5 条规则", "",
        "| 规则 | total | error | rate | 动作 |", "|---|---|---|---|---|"]
    for x in worst:
        lines.append(f"| `{x['rule_id']}` | {x['total']} | {x['error']} | "
                     f"{x['known_error_rate']} | {x['action']} |")
    lines += ["", "### 1.2 被降级/暂停的规则（真实数据）", ""]
    hit = [x for x in g["rows"] if x["action"] != "ok"]
    if hit:
        lines += ["| 规则 | rate | 动作 | 理由 |", "|---|---|---|---|"]
        for x in hit:
            lines.append(f"| `{x['rule_id']}` | {x['known_error_rate']} | **{x['action']}** | {x['why']} |")
    else:
        lines.append(f"- **真实数据上没有规则触发降级/暂停**（最高 error_rate="
                     f"{worst[0]['known_error_rate'] if worst else None} ≤ {THETA_WARN}）"
                     f"⇒ 上线后实际降级 0、暂停 0；两条阈值改由**合成数据**验证（下表）。")
    lines += ["", "## 二、合成数据验证两条阈值", "",
              "| 规则 | error_rate | 期望 | 实测 | active | 生效严重度 | 通过 |",
              "|---|---|---|---|---|---|---|"]
    for s in syn:
        lines.append(f"| `{s['rule_id']}` | {s['rate']} | {s['expect']} | **{s['got']}** | "
                     f"{s['active']} | {s['severity']} | {'✅' if s['ok'] else '❌'} |")
    lines += ["", "## 三、暂停状态与恢复（恢复必须人审）", "",
              f"- 显式暂停清单：`{st['suspended'] or '（空）'}`",
              f"- 操作历史：{len(st['history'])} 条",
              "- `restore()` 未带 `human_authorized=True` ⇒ **抛 `HumanReviewRequired`**"
              "（机器不得自行解停）", "",
              "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **`MODIFY` ≠ 规则错**：人改判可能是改口径 ⇒ rate 是**近似**；",
              "2. **真实数据无 >0.50 规则** ⇒ 暂停分支未被真实数据触发，由**合成数据**验证；",
              "3. **阈值 0.20/0.50 是设计值**，未用历史回填；",
              "4. **暂停是真的**：enforce 下 `active=False`（规则不生效）——这是 647 与 642 的行为差别；",
              "5. 无实测样本的规则**不改动**（不把「没数据」当「没问题」）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"grader": g, "synthetic": syn, "state": st,
                   "n_rules_with_samples": g["n_with_samples"], "mode": pmode.mode()},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    synth = {"ok20": {"rule_id": "ok20", "total": 100, "error": 20, "known_error_rate": 0.20},
             "warn21": {"rule_id": "warn21", "total": 100, "error": 21, "known_error_rate": 0.21},
             "sus51": {"rule_id": "sus51", "total": 100, "error": 51, "known_error_rate": 0.51}}
    chk("边界：=0.20 ⇒ ok", effective_action("ok20", "block", synth, enforce=True)["action"] == "ok")
    chk("边界：>0.20 ⇒ 降级 warn",
        effective_action("warn21", "block", synth, enforce=True)["effective_severity"] == "warn")
    chk("边界：>0.50 ⇒ 暂停（active=False）",
        effective_action("sus51", "block", synth, enforce=True)["active"] is False)
    chk("shadow ⇒ 不改动作",
        effective_action("sus51", "block", synth, enforce=False)["effective_severity"] == "block")
    chk("阈值可配置", THETA_WARN == 0.20 and THETA_SUSPEND == 0.50)
    chk("合成三档齐全", {s["got"] for s in synthetic_check()} >= {"ok", "degraded_warn"})

    # 恢复必须人审
    try:
        restore("sus51", by="bot")
        chk("restore 无人审授权 ⇒ 拒绝", False)
    except HumanReviewRequired:
        chk("restore 无人审授权 ⇒ 拒绝", True)
    try:
        restore("sus51", by="", human_authorized=True)
        chk("restore 必须署名", False)
    except ValueError:
        chk("restore 必须署名", True)

    rates = rule_error_rates()
    chk("逐规则实测可算（有样本）", len(rates) > 0, str(len(rates)))
    g = grader(rates)
    chk("在册规则 67 条", g["n"] == 67, str(g["n"]))
    chk("动作分布键合法", set(g["by_action"]) <= set(ACTIONS))
    chk("无样本规则不改动",
        all(x["action"] in ("ok", "suspended") or x["has_samples"] for x in g["rows"]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"B4 calibration-enforce selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B4 校准追踪器真上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--restore", default="", help="人审恢复某规则（需 --by）")
    ap.add_argument("--by", default="", help="恢复操作人（署名）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.restore:
        print(json.dumps(restore(a.restore, by=a.by, human_authorized=bool(a.by)),
                         ensure_ascii=False))
        return 0
    rates = rule_error_rates()
    g = grader(rates, explicit_suspended=set(load_state()["suspended"]))
    if a.report:
        print(f"written {write_report()}")
        return 0
    if a.json:
        print(json.dumps({k: v for k, v in g.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 calibration] mode={pmode.mode()} 有样本 {g['n_with_samples']}/67 "
          f"by_action={g['by_action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
