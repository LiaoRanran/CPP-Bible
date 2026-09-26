"""643 E1 · **新规则 known_error_rate 初始化与追踪**（抗 Goodhart #1）。

**定位**：D 阶段产出的草案**一旦人审批准上线**，必须从 **"无数据"** 起步（A3-G1）——
**不是 0、也不是全库代理**。本工具提供该新规则的**独立台账**与 `record/overturn`。

**为什么必须在 642 之外单开一份**（关键区分）：
- 642 的 `CalibrationTracker` 对**已有 67 条**规则用 **全库代理** 做初值（因为历史无归属字段）；
- 新规则**没有历史包袱** ⇒ 用代理就是在**借用别人的错误率**，属自欺（A3 教训 2/3）；
- ⇒ 新规则一律 **`known_error_rate = None`（"无数据"）**，直到它有**自己的**判决样本。

**台账形态（append-only）**：`data/643_new_rule_errors.json`
`{"schema", "append_only": true, "rules": {rule_id: {total, error, first_seen, log[]}},
  "initialized_from": "D2 草案 + D4 非危险"}`

只读契约：`--check` 只读、exit 0；`--init` 写台账（新规则初始化）；`--report` 写报告。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import rule_draft_anti_ripple_643 as D4  # noqa: E402
import rule_draft_mdl_check_643 as D3  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_new_rule_errors.md")
LEDGER = os.path.join(ROOT, "data", "643_new_rule_errors.json")
NO_DATA = "无数据"
#: 当前台账路径（**参数化**：单测可重定向，不靠 global 可变全局）
_P: dict[str, str] = {"path": ""}


def init_rules() -> list[str]:
    """待初始化规则 = D2 草案中**非冗余且非危险**者（D3 未 REJECT 且 D4 未判危险）。"""
    d3 = D3.check()
    d4 = {r["proposed_rule_id"]: r for r in D4.assess()["rows"]}
    out = []
    for r in d3["rows"]:
        if r["redundant"]:
            continue
        if d4.get(r["proposed_rule_id"], {}).get("ripple_grade") == "危险":
            continue
        out.append(r["proposed_rule_id"])
    return sorted(out)


def error_rate(total: int, error: int) -> Optional[float]:
    """`None` = 无数据（**不是 0**）。"""
    if total <= 0:
        return None
    return round(error / total, 4)


def load_ledger() -> dict[str, Any]:
    path = _P["path"] or LEDGER
    if not os.path.exists(path):
        return {"schema": "new_rule_errors/1", "append_only": True, "rules": {},
                "initialized_from": "D2 草案 + D4 非危险"}
    try:
        data: dict[str, Any] = json.loads(open(path, encoding="utf-8").read())
        return data
    except (OSError, json.JSONDecodeError):
        return {"schema": "new_rule_errors/1", "append_only": True, "rules": {},
                "initialized_from": "（台账损坏，已重建）"}


def _save(led: dict[str, Any]) -> None:
    led["updated"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(_P["path"] or LEDGER, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(led, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def init_ledger() -> dict[str, Any]:
    """把待初始化规则写进台账（**已存在的不覆盖**，保留其历史样本）。"""
    led = load_ledger()
    added = []
    for rid in init_rules():
        if rid not in led["rules"]:
            led["rules"][rid] = {"total": 0, "error": 0,
                                 "first_seen": datetime.datetime.now().isoformat(
                                     timespec="seconds"),
                                 "known_error_rate": None, "log": []}
            added.append(rid)
    _save(led)
    return {"added": added, "n_rules": len(led["rules"]),
            "no_data_rules": sorted(r for r, v in led["rules"].items()
                                    if error_rate(v["total"], v["error"]) is None)}


def record(rule_ids: list[str], decision_id: str = "", result: str = "") -> dict[str, Any]:
    """记一次该规则的判决（total+1）。**只写 643 自己的台账。**"""
    led = load_ledger()
    marked = []
    for rid in rule_ids:
        st = led["rules"].setdefault(rid, {"total": 0, "error": 0,
                                           "first_seen": datetime.datetime.now()
                                           .isoformat(timespec="seconds"),
                                           "known_error_rate": None, "log": []})
        st["total"] += 1
        st["log"].append({"ts": datetime.datetime.now().isoformat(timespec="seconds"),
                          "decision_id": decision_id, "result": result, "overturned": False})
        st["known_error_rate"] = error_rate(st["total"], st["error"])
        marked.append(rid)
    _save(led)
    return {"recorded": marked}


def overturn(rule_ids: list[str], decision_id: str = "") -> dict[str, Any]:
    """判决被推翻 ⇒ `error+1` 并回标日志（**append-only：不删条目**）。"""
    led = load_ledger()
    marked = 0
    for rid in rule_ids:
        st = led["rules"].get(rid)
        if st is None:
            continue
        st["error"] += 1
        for e in reversed(st["log"]):
            if not e["overturned"] and (not decision_id or e["decision_id"] == decision_id):
                e["overturned"] = True
                marked += 1
                break
        st["known_error_rate"] = error_rate(st["total"], st["error"])
    _save(led)
    return {"overturned_rules": rule_ids, "log_marked": marked}


def snapshot() -> dict[str, Any]:
    led = load_ledger()
    rows = [{"rule_id": rid, "total": v["total"], "error": v["error"],
             "known_error_rate": error_rate(v["total"], v["error"]),
             "is_no_data": error_rate(v["total"], v["error"]) is None,
             "n_log": len(v["log"])} for rid, v in sorted(led["rules"].items())]
    return {"rows": rows, "n_rules": len(rows),
            "n_no_data": sum(1 for r in rows if r["is_no_data"]),
            "n_with_samples": sum(1 for r in rows if not r["is_no_data"]),
            "append_only": led.get("append_only", True),
            "initialized_from": led.get("initialized_from", "")}


def write_report() -> str:
    s = snapshot()
    lines = [
        "# 643 E1 · 新规则 known_error_rate 追踪（抗 Goodhart #1）", "",
        f"> 台账：`data/643_new_rule_errors.json`（append-only **{s['append_only']}**，"
        f"来源 {s['initialized_from']}）；规则数 **{s['n_rules']}**，"
        f"其中 **无数据 {s['n_no_data']}** / 有自身样本 {s['n_with_samples']}。", "",
        "## 一、为什么新规则必须「从无数据起步」", "",
        "- 642 的 `CalibrationTracker` 对**已有 67 条**用**全库代理**（历史无归属字段，"
        "是无奈的近似）；",
        "- 新规则**没有历史包袱** ⇒ 若也给代理值，就是**借用别人的错误率**（A3 教训 2："
        "代理指标必须成对且不可混用）⇒ 本工具一律 `known_error_rate = None`（**不是 0**）；",
        "- `None` 与 `0` 的区别是本质的：`0` 会被当成「从未出错」（**假精确**），"
        "`None` 表示「还没有样本」。", "",
        "## 二、逐条台账", "",
        "| 规则 | 判决样本 total | 推翻 error | known_error_rate | 无数据？ | 日志条数 |",
        "|---|---|---|---|---|---|"]
    for r in s["rows"]:
        ker = NO_DATA if r["is_no_data"] else r["known_error_rate"]
        lines.append(f"| `{r['rule_id']}` | {r['total']} | {r['error']} | {ker} | "
                     f"{'✅' if r['is_no_data'] else '—'} | {r['n_log']} |")
    if not s["rows"]:
        lines.append("| — | — | — | — | — | — |")
    lines += ["", "## 诚实登记", "",
              "1. **「无数据」是结论不是缺陷**：新规则上线前**必然**无样本；"
              "本工具的价值是**让这一点显式**，而不是用代理值把它盖住；",
              "2. **台账独立于 642**：不写 `data/642_*`，避免跨批污染"
              "（642 的台账属 642 批产物）；",
              "3. **`record/overturn` 只在人审判决真实发生后才该被调用**："
              "本批**没有**真实上线任何草案 ⇒ 台账里**全是 0 样本**（这正是实情）；",
              "4. **回标不删条目**（append-only 铁律）；",
              "5. 本工具**不改任何规则**：初始化只写 643 侧车台账。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest(tmp: Optional[str] = None) -> int:
    ok = True
    saved = _P["path"]
    _P["path"] = tmp or ""

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("无样本 ⇒ rate 为 None（不是 0）", error_rate(0, 0) is None)
    chk("有样本 ⇒ 正常算率", error_rate(4, 1) == 0.25)
    chk("全错 ⇒ 1.0", error_rate(2, 2) == 1.0)

    if tmp:
        init = init_ledger()
        chk("初始化后全部为无数据", init["n_rules"] > 0
            and len(init["no_data_rules"]) == init["n_rules"], str(init["n_rules"]))
        r1 = [init["added"][0]] if init["added"] else []
        if r1:
            record(r1, decision_id="d1")
            s1 = {x["rule_id"]: x for x in snapshot()["rows"]}[r1[0]]
            chk("record 后 total=1 且 rate=0（有样本）",
                s1["total"] == 1 and s1["known_error_rate"] == 0.0)
            overturn(r1, decision_id="d1")
            s2 = {x["rule_id"]: x for x in snapshot()["rows"]}[r1[0]]
            chk("overturn 后 error=1 且 rate=1.0",
                s2["error"] == 1 and s2["known_error_rate"] == 1.0)
            led = load_ledger()
            chk("回标不删条目（日志仍在且标 overturned）",
                len(led["rules"][r1[0]]["log"]) == 1
                and led["rules"][r1[0]]["log"][0]["overturned"] is True)
            chk("重复 init 不覆盖已有样本",
                init_ledger()["n_rules"] == init["n_rules"]
                and load_ledger()["rules"][r1[0]]["total"] == 1)
    _P["path"] = saved
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 E1 新规则误差追踪")
    ap.add_argument("--check", action="store_true", help="只读自检（含临时台账演练）")
    ap.add_argument("--init", action="store_true", help="初始化台账（D2 草案）")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印台账（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            return selftest(os.path.join(td, "led.json"))
    if x.init:
        print(f"init {init_ledger()}")
        return 0
    if x.report:
        print(f"written {write_report()}")
        return 0
    s = snapshot()
    if x.json:
        print(json.dumps(s, ensure_ascii=False, indent=2))
        return 0
    print(f"[new-rule-errors] {s['n_rules']} 规则 ⇒ 无数据 {s['n_no_data']} / "
          f"有样本 {s['n_with_samples']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
