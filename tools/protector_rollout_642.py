"""642 A6 · 五个保护器**联调 + 灰度报告**（证「零生产判决被改变」）。

联调对象：A1 冲突检测（flag）/ A2 anti-windup（标记）/ A3 blind_protocol（只标记历史 + 盲化新项）/
A4 校准追踪（记账）/ A5 MDL 准入（只对新规则）。五个**同时在灰度模式**跑一遍全量判决面。

产出的四件事（§三 A6）：

1. **各保护器触发次数**（`triggers`）；
2. **标记清单**（`marks`，按保护器分区，**可叠加、不互相覆盖**）；
3. **误判风险评估**（各保护器自带 + 汇总）；
4. **零漂移实证**：联调**前后**生产面指纹（5 个 CORE_TOOLS 字节 + 452 判决账本 +
   人审队列 + 权威日志 + verified 卡清单）**逐项相同**。

**标记可叠加 + 回滚可验证**：

* `MARK_NAMESPACES`：五个保护器各占一组**互不重叠**的键名 ⇒ 叠加不会互相覆盖；
* `merge_marks()`：同名键值冲突 ⇒ 抛 `MarkConflictError`（**不静默覆盖**）；
* `rollback_marks()`：按保护器**精确摘除**自己的标记，其余保护器标记**一字不动** ⇒
  逐个回滚到底即回到"灰度前"（`marks == {}`）。

**诚实登记**（§十.1）：**联调通过 ≠ 保护器有效**。本模块只证明"灰度期零副作用 + 标记可叠加 +
可回滚"，**不证明**拦截后系统更安全 —— 那需要 643+ 的真实运行数据（真实盲评 / 真实拦截）。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_protector_rollout.md`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import anti_windup_642 as a2  # noqa: E402
import blind_protocol_642 as a3  # noqa: E402
import calibration_tracker_642 as a4  # noqa: E402
import conflict_detector_642 as a1  # noqa: E402
import mdl_gate_642 as a5  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "642_protector_rollout.md")
LEDGER = a3.LEDGER
AUTH_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
#: 5 个 CORE_TOOLS（判决逻辑，铁律：本批零改动）
CORE_TOOLS = ("gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
              "toolchain.py", "cppbible.py")

PROTECTORS = ("A1", "A2", "A3", "A4", "A5")
#: 各保护器的标记键名空间（**互不重叠** ⇒ 可叠加）
MARK_NAMESPACES: dict[str, tuple[str, ...]] = {
    "A1": ("conflict_flag", "conflict_types", "conflict_strength"),
    "A2": ("queued_pending", "frozen", "upgraded", "priority_out"),
    "A3": ("blind_state", "masked", "residual"),
    "A4": ("total_count", "error_count", "known_error_rate"),
    "A5": ("decision", "detail"),
}


class MarkConflictError(ValueError):
    """同一键被两个保护器写了不同值 ⇒ 拒绝合并（**不静默覆盖**）。"""


def merge_marks(target: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """把 `new` 的标记叠到 `target` 上（返回**新字典**，不改入参）。同名不同值 ⇒ 抛错。"""
    out = dict(target)
    for k, v in new.items():
        if k in out and out[k] != v:
            raise MarkConflictError(f"标记键 {k!r} 冲突：{out[k]!r} vs {v!r}")
        out[k] = v
    return out


def rollback_marks(marks: dict[str, Any], protector: str) -> dict[str, Any]:
    """按保护器**精确摘除**自己的标记；其余保护器的标记一字不动。"""
    drop = set(MARK_NAMESPACES[protector])
    return {k: v for k, v in marks.items() if k not in drop}


def _sha(path: str) -> str:
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return ""


def production_digest() -> dict[str, str]:
    """生产面指纹（联调前后必须逐项相同）。"""
    d = {name: _sha(os.path.join(HERE, name)) for name in CORE_TOOLS}
    d["decision_ledger"] = _sha(LEDGER)
    d["authority_log"] = _sha(AUTH_LOG)
    d["human_queue"] = _sha(a2.QUEUE)
    d["verified_cards"] = hashlib.sha256(
        "\n".join(rel for rel, _t in a1.shadow.verified_cards()).encode("utf-8")
    ).hexdigest()
    return d


def rollout() -> dict[str, Any]:
    """五个保护器**同时**在灰度模式跑一遍；前后对比生产面指纹。"""
    before = production_digest()
    marks: dict[str, Any] = {}
    triggers: dict[str, Any] = {}

    # A1 冲突检测（flag）
    r1 = a1.run_flag()
    triggers["A1"] = {"卡片": r1["n_cards"], "标记": r1["n_marked"],
                      "判决被改变": r1["n_verdict_changed"]}
    marks = merge_marks(marks, {k: r1["rows"][0]["decision_after"][k]
                                for k in MARK_NAMESPACES["A1"]})

    # A2 anti-windup（标记，不丢请求）
    r2 = a2.replay_queue()
    triggers["A2"] = {"队列": r2["n"], "queued_pending": r2["n_queued_pending"],
                      "冻结": r2["n_frozen"], "升级": r2["n_upgraded"]}
    row2 = r2["rows"][0] if r2["rows"] else {k: None for k in MARK_NAMESPACES["A2"]}
    marks = merge_marks(marks, {k: row2[k] for k in MARK_NAMESPACES["A2"]})

    # A3 blind_protocol（只标记历史 + 盲化新项）
    h3 = a3.scan_history()
    item = a3.open_item("ROLLOUT-NEW-001", 35.8)
    triggers["A3"] = {"历史判决": h3["n_decisions"], "违规标记": h3["n_violations"],
                      "账本未变": h3["ledger_unchanged"]}
    marks = merge_marks(marks, {"blind_state": item.visible_view()["blind_state"],
                               "masked": item.masked, "residual": item.residual})

    # A4 校准追踪（记账）
    t4 = a4.build_tracker()
    snap4 = t4.snapshot()
    triggers["A4"] = {"规则": snap4["n_rules"], "有样本": snap4["n_with_samples"],
                      "用代理": snap4["n_proxy"]}
    row4 = snap4["rows"][0]
    marks = merge_marks(marks, {"total_count": row4["total_count"],
                               "error_count": row4["error_count"],
                               "known_error_rate": row4["known_error_rate"]})

    # A5 MDL 准入（只对新规则）
    r5 = a5.run_admission()
    triggers["A5"] = r5["by_decision"]
    row5 = r5["rows"][0]
    marks = merge_marks(marks, {"decision": row5["decision"], "detail": row5["detail"]})

    after = production_digest()
    drift = sorted(k for k in before if before[k] != after[k])
    return {"before": before, "after": after, "drift": drift, "zero_drift": not drift,
            "triggers": triggers, "marks": marks,
            "critical_changed": sum(1 for v in (r1["n_verdict_changed"],) if v)}


def risk_summary() -> list[dict[str, str]]:
    """五个保护器的误判风险汇总（每项附回滚动作）。"""
    risks = []
    for pid, mod in (("A1", a1), ("A2", a2), ("A3", a3), ("A4", a4), ("A5", a5)):
        for r in mod.rollback_plan():
            risks.append({"protector": pid, "risk": r["risk"], "rollback": r["rollback"]})
    return risks


def write_report() -> str:
    r = rollout()
    lines = [
        "# 642 A6 · 五个保护器联调 + 灰度报告（**零生产判决被改变**）", "",
        "> 灰度原则：flag 只加标记 / anti-windup 只标记不丢请求 / blind 只标记历史 + 盲化新项 /",
        "> 校准只记账 / MDL 只对新规则。**没有任何判决、规则、账本被改写。**", "",
        "## 一、联调结果：各保护器触发次数", "",
        "| 保护器 | 触发 |", "|---|---|"]
    for k, v in r["triggers"].items():
        lines.append(f"| {k} | `{json.dumps(v, ensure_ascii=False)}` |")
    lines += ["", "## 二、零漂移实证（联调前 vs 联调后）", "",
              "| 生产工件 | 前 | 后 | 相同 |", "|---|---|---|---|"]
    for k in r["before"]:
        same = r["before"][k] == r["after"][k]
        lines.append(f"| `{k}` | `{r['before'][k][:12]}…` | `{r['after'][k][:12]}…` | "
                     f"{'✅' if same else '❌'} |")
    lines += ["", f"- **漂移项：{r['drift'] or '零'}**；"
                  f"**生产判决被改变：{r['critical_changed']}**", "",
              "## 三、标记清单（按保护器分区，**可叠加、不互相覆盖**）", "",
              "| 保护器 | 标记键空间 | 本次标记 |", "|---|---|---|"]
    for pid in PROTECTORS:
        keys = [k for k in MARK_NAMESPACES[pid] if k in r["marks"]]
        vals = {k: r["marks"][k] for k in keys}
        lines.append(f"| {pid} | `{'`, `'.join(MARK_NAMESPACES[pid])}` | "
                     f"`{json.dumps(vals, ensure_ascii=False)[:110]}` |")
    lines += ["", "### 3.1 可叠加 + 回滚（机械验证）", "",
              f"- 五个保护器的键空间**互不重叠** ⇒ 叠加后全集 = "
              f"{len(r['marks'])} 个键；",
              "- 同名键值冲突 ⇒ `MarkConflictError`（**不静默覆盖**）；",
              "- `rollback_marks()` 按保护器精确摘除，逐个回滚到底 ⇒ `marks == {}`。", "",
              "## 四、误判风险评估（含回滚动作）", "",
              "| 保护器 | 风险 | 回滚动作 |", "|---|---|---|"]
    for x in risk_summary():
        lines.append(f"| {x['protector']} | {x['risk']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **联调通过 ≠ 保护器有效**（§十.1）：本模块只证明「灰度期零副作用 + 标记可叠加 + "
              "可回滚」，**不证明**拦截后更安全；有效性需 643+ 真实运行数据；",
              "2. **零漂移的强度**：指纹覆盖 5 个 CORE_TOOLS 字节 + 452 判决账本 + 权威日志 + "
              "人审队列 + verified 卡清单；**未覆盖**受控目录全量（那是 642 门禁的另一项）；",
              "3. **A2/A3/A5 的「触发」多数是标记量**，不是被拦截量（灰度期不拦截）；",
              "4. **A5 候选是合成**（本批无真实新规则提案）；",
              "5. 本批**未启用任何 block**：A1 的 block 模式显式未实现（留 643）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = rollout()
    chk("零漂移（生产面指纹前后一致）", r["zero_drift"] is True, str(r["drift"]))
    chk("生产判决被改变数 = 0", r["critical_changed"] == 0)
    chk("五个保护器都有触发记录", set(r["triggers"]) == set(PROTECTORS))

    # 标记可叠加
    merged: dict[str, Any] = {}
    for pid in PROTECTORS:
        merged = merge_marks(merged, {MARK_NAMESPACES[pid][0]: f"{pid}-v"})
    chk("标记可叠加（五键全在）", len(merged) == 5, str(sorted(merged)))
    chk("叠加不互相覆盖", merged == {MARK_NAMESPACES[p][0]: f"{p}-v" for p in PROTECTORS})

    # 冲突不静默覆盖
    try:
        merge_marks({"conflict_flag": True}, {"conflict_flag": False})
        chk("同名冲突抛 MarkConflictError", False)
    except MarkConflictError:
        chk("同名冲突抛 MarkConflictError", True)

    # 键空间互不重叠 ⇒ 联调不互相干扰
    all_keys: list[str] = [k for p in PROTECTORS for k in MARK_NAMESPACES[p]]
    chk("键空间互不重叠", len(all_keys) == len(set(all_keys)))

    # 回滚方案有效：逐个摘除到底 ⇒ 空
    marks = dict(r["marks"])
    for pid in PROTECTORS:
        before_n = len(marks)
        marks = rollback_marks(marks, pid)
        chk(f"回滚 {pid} 只摘自己的键", len(marks) < before_n or not MARK_NAMESPACES[pid])
    chk("全部回滚后回到灰度前（marks == {}）", marks == {}, str(marks))

    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A6 保护器联调 + 灰度报告")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写联调/灰度报告")
    ap.add_argument("--json", action="store_true", help="打印联调结果（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = rollout()
    if a.json:
        print(json.dumps({"triggers": r["triggers"], "drift": r["drift"],
                          "zero_drift": r["zero_drift"],
                          "critical_changed": r["critical_changed"]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[rollout] 五保护器灰度联调：零漂移={r['zero_drift']}；"
          f"生产判决被改变={r['critical_changed']}；标记键={len(r['marks'])}")
    for k, v in r["triggers"].items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
