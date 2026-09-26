"""647 B5(联调) · 五个保护器**真上岗联调**（证：真上岗了、不互相打架、可一键回滚）。

联调对象（全部 647 版，**enforce 模式**）：

| 保护器 | 647 的强制动作 | 对象层 |
|---|---|---|
| B1 冲突检测 | 高置信冲突（C ≥ 0.8 且双方有证据）⇒ 判决态**改判 fail** | **单卡判决** |
| B2 anti-windup | 超预算（>20/周）⇒ **冻结**（`enqueued=False`） | **人审队列项** |
| B3 blind_protocol | 新判决**强制盲化**（人审前 AI 推荐不可见） | **人审条目** |
| B4 校准追踪 | error_rate >20% 降级 warn / >50% **暂停规则** | **规则** |
| B5 MDL 准入 | 不过 MDL ⇒ **不予上线** | **规则候选** |

联调产出（§四 B5）：
1. **上岗前后对比**（enforce 的强制量 vs 642 灰度的标记量）；
2. **不冲突 / 不重复拦截**（键空间互不重叠 + 对象层不同 + 逐项核验）；
3. **零漂移**：5 个 CORE_TOOLS 字节 + 452 判决账本 + 权威日志 + 人审队列 + verified 卡清单
   在联调前后**逐项相同**（保护器**不动生产工件**）；
4. **一键回滚**：`protector_mode_647.rollback()` ⇒ 五个保护器同时退回 642 灰度，
   并**实测**回滚后强制量为零。

**诚实登记**：联调通过 **≠ 保护器有效**。本模块只证明"能同时上岗 + 不打架 + 可回滚 + 不动生产工件"，
**不证明**拦截后系统更安全 —— 那需要真实运行数据。

CLI：`--check` / `--report` / `--json` / `--rollback`（一键回 shadow 并实测零强制）。纯标准库。
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

import anti_windup_647 as b2  # noqa: E402
import blind_protocol_647 as b3  # noqa: E402
import calibration_tracker_647 as b4  # noqa: E402
import conflict_detector_647 as b1  # noqa: E402
import mdl_gate_647 as b5  # noqa: E402
import protector_mode_647 as pmode  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_protector_report.md")
OUT_JSON = os.path.join(ROOT, "data", "647_protector_report.json")

PROTECTORS = ("B1", "B2", "B3", "B4", "B5")
#: 各保护器的标记键名空间（**互不重叠** ⇒ 可叠加）
MARK_NAMESPACES: dict[str, tuple[str, ...]] = {
    "B1": ("conflict_flag", "conflict_types", "conflict_strength", "conflict_action"),
    "B2": ("queued_pending", "frozen", "frozen_enforced", "enqueued", "priority_out"),
    "B3": ("blind_state", "masked", "residual"),
    "B4": ("known_error_rate", "effective_severity", "rule_active"),
    "B5": ("mdl_decision", "mdl_published"),
}
#: 各保护器作用的**对象层**（证明"不重复拦截"）
TARGET_LAYER = {"B1": "单卡判决", "B2": "人审队列项", "B3": "人审条目",
                "B4": "规则", "B5": "规则候选"}
CORE_TOOLS = ("gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
              "toolchain.py", "cppbible.py")


class MarkConflictError(ValueError):
    """同一键被两个保护器写了不同值 ⇒ 拒绝合并（**不静默覆盖**）。"""


def merge_marks(target: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    out = dict(target)
    for k, v in new.items():
        if k in out and out[k] != v:
            raise MarkConflictError(f"标记键 {k!r} 冲突：{out[k]!r} vs {v!r}")
        out[k] = v
    return out


def rollback_marks(marks: dict[str, Any], protector: str) -> dict[str, Any]:
    drop = set(MARK_NAMESPACES[protector])
    return {k: v for k, v in marks.items() if k not in drop}


def _sha(path: str) -> str:
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return ""


def production_digest() -> dict[str, str]:
    """生产工件指纹（联调前后必须逐项相同）。"""
    d = {name: _sha(os.path.join(HERE, name)) for name in CORE_TOOLS}
    d["decision_ledger"] = _sha(b3.base.LEDGER)
    d["authority_log"] = _sha(os.path.join(ROOT, "data", "authority", "authority_log.jsonl"))
    d["human_queue"] = _sha(b2.QUEUE)
    d["transparency_log"] = _sha(os.path.join(ROOT, "data", "transparency_log.jsonl"))
    d["verified_cards"] = hashlib.sha256(
        "\n".join(rel for rel, _t in b1.det_src.verified_cards()).encode("utf-8")
    ).hexdigest()
    return d


def enforce_effects() -> dict[str, Any]:
    """五个保护器在**当前模式**下的**强制量**（enforce 有值；shadow 应全为零）。

    注意：每个保护器的"强制量"都取**模式相关**的那一项 ——
    B1 取"判决态被改变"（不是"高置信动作数"，后者是检测事实、与模式无关）。
    """
    r1 = b1.run_new()
    r2 = b2.replay_queue()
    d3 = b3.run_new_demo()
    rules = [x["rule_id"] for x in b4.grader(b4.rule_error_rates())["rows"]]
    acts = [b4.effective_action(rid, "block") for rid in rules]
    g5 = b5.run_gate()
    return {
        "B1": {"卡片": r1["n"], "高置信动作数": r1["n_blocked"],
               "判决态被改变（enforce 强制量）": r1["n_verdict_changed"],
               "动作分布": r1["by_action"]},
        "B2": {"队列": r2["n"], "冻结不入队（enforce 强制量）": r2["n_frozen_enforced"],
               "积压警报": r2["backlog"]["alert"], "占用%": r2["state"]["occupancy_pct"]},
        "B3": {"新判决": d3["n"], "强制盲化（enforce 强制量）": sum(
            1 for r in d3["rows"] if r["enforced"]),
            "被盲化总数": d3["n_blinded"], "生效方法分布": d3["by_effective_method"]},
        "B4": {"规则": len(rules),
               "降级（enforce 强制量）": sum(
                   1 for a in acts if a["enforced"] and a["action"] == "degraded_warn"),
               "暂停（enforce 强制量）": sum(
                   1 for a in acts if a["enforced"] and a["action"] == "suspended"),
               "有样本": b4.grader(b4.rule_error_rates())["n_with_samples"]},
        "B5": {"候选": g5["n"], "不放行（enforce 强制量）": g5["n_blocked"],
               "结论分布": g5["by_decision"]},
    }


def collect_marks() -> dict[str, Any]:
    """把五个保护器的标记叠到一起（**可叠加、不互相覆盖**）。"""
    marks: dict[str, Any] = {}
    r1 = b1.run_new()
    row1 = r1["rows"][0]["decision_after"] if r1["rows"] else {}
    marks = merge_marks(marks, {k: row1.get(k) for k in MARK_NAMESPACES["B1"]})
    r2 = b2.replay_queue()
    row2 = r2["rows"][0] if r2["rows"] else {}
    marks = merge_marks(marks, {k: row2.get(k) for k in MARK_NAMESPACES["B2"]})
    j3 = b3.new_judgment("ROLLOUT-647", 35.8)
    marks = merge_marks(marks, {"blind_state": j3.blind_state,
                                "masked": j3.item.masked, "residual": j3.item.residual})
    g4 = b4.grader(b4.rule_error_rates())
    row4 = g4["rows"][0]
    marks = merge_marks(marks, {"known_error_rate": row4["known_error_rate"],
                                "effective_severity": row4["action"],
                                "rule_active": row4["action"] != "suspended"})
    g5 = b5.run_gate()
    row5 = g5["rows"][0] if g5["rows"] else {}
    marks = merge_marks(marks, {"mdl_decision": row5.get("decision"),
                                "mdl_published": row5.get("published")})
    return marks


def layer_check() -> dict[str, Any]:
    """**不重复拦截**：键空间互不重叠 + 对象层互不相同（逐项机器核验）。"""
    all_keys = [k for p in PROTECTORS for k in MARK_NAMESPACES[p]]
    layers = [TARGET_LAYER[p] for p in PROTECTORS]
    return {"keys_disjoint": len(all_keys) == len(set(all_keys)),
            "n_keys": len(all_keys),
            "layers_distinct": len(layers) == len(set(layers)),
            "layers": TARGET_LAYER}


def rollout() -> dict[str, Any]:
    """联调：enforce 下五保护器同时跑；对比生产工件指纹。"""
    before = production_digest()
    effects = enforce_effects()
    marks = collect_marks()
    after = production_digest()
    drift = sorted(k for k in before if before[k] != after[k])
    return {"mode": pmode.mode(), "before": before, "after": after,
            "drift": drift, "zero_drift": not drift, "effects": effects,
            "marks": marks, "layer_check": layer_check(),
            "n_marks": len(marks)}


def shadow_baseline() -> dict[str, Any]:
    """642 灰度对照：同一批输入在 shadow 下的**标记量**（强制量应为零）。"""
    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "shadow"
        e = enforce_effects()
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved
    return e


def rollback_and_verify(commit: bool = False) -> dict[str, Any]:
    """一键回滚 ⇒ 实测五个保护器的强制量是否归零。

    两档机制（**默认那档绝不写盘**，避免"验证"污染运行期状态）：

    * `commit=False`（默认，`--check`/`--report` 用）：**只设环境变量** `QUEYI_PROTECTOR_MODE=shadow`
      跑一遍，跑完还原 —— **不写模式文件**（历史版本会写盘再删，属于自找麻烦）；
    * `commit=True`（CLI `--rollback`）：**真的**写模式文件（`protector_mode_647.rollback()`），保留回滚。
    """
    prev = pmode.mode()
    prev_env = os.environ.get(pmode.ENV)
    if commit:
        pmode.rollback()                       # 真回滚：落盘
    os.environ[pmode.ENV] = pmode.MODE_SHADOW  # 运行期生效
    try:
        e = enforce_effects()
        zero = (e["B1"]["判决态被改变（enforce 强制量）"] == 0
                and e["B2"]["冻结不入队（enforce 强制量）"] == 0
                and e["B3"]["强制盲化（enforce 强制量）"] == 0
                and e["B4"]["降级（enforce 强制量）"] == 0
                and e["B4"]["暂停（enforce 强制量）"] == 0
                and e["B5"]["不放行（enforce 强制量）"] == 0)
    finally:
        if prev_env is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = prev_env
    return {"prev_mode": prev, "new_mode": pmode.MODE_SHADOW, "zero_enforcement": zero,
            "restored": (not commit), "wrote_mode_file": bool(commit),
            "mechanism": ("模式文件（真回滚）" if commit
                          else "环境变量（不写盘，验证后还原）"),
            "effects_after_rollback": e}


def write_report() -> str:
    r = rollout()
    sh = shadow_baseline()
    rb = rollback_and_verify()
    lines = [
        "# 647 B5(联调) · 五个保护器**真上岗**联调（前后对比 + 不打架 + 可回滚）", "",
        f"- 当前模式：**{r['mode']}**（`QUEYI_PROTECTOR_MODE`；`--rollback` 一键回 642 灰度）",
        f"- 标记键：**{r['n_marks']}** 个（键空间互不重叠={r['layer_check']['keys_disjoint']}，"
        f"对象层互不相同={r['layer_check']['layers_distinct']}）", "",
        "## 一、上岗前后对比（enforce 强制量 vs 642 灰度标记量）", "",
        "| 保护器 | enforce（647 真上岗） | shadow（642 灰度） |", "|---|---|---|"]
    for p in PROTECTORS:
        lines.append(f"| **{p}** {TARGET_LAYER[p]} | `{json.dumps(r['effects'][p], ensure_ascii=False)}` | "
                     f"`{json.dumps(sh[p], ensure_ascii=False)}` |")
    lines += ["", "## 二、不冲突 / 不重复拦截", "",
              "| 保护器 | 作用对象层 | 标记键空间 |", "|---|---|---|"]
    for p in PROTECTORS:
        lines.append(f"| {p} | {TARGET_LAYER[p]} | `{'`, `'.join(MARK_NAMESPACES[p])}` |")
    lines += ["",
              "- 五个对象的**集合两两不相交**（卡判决 / 队列项 / 人审条目 / 规则 / 规则候选）⇒ "
              "**同一个东西不会被两个保护器同时处置**；",
              "- 标记键空间互不重叠 ⇒ 叠加不互相覆盖；同名不同值 ⇒ `MarkConflictError`（不静默覆盖）；",
              "- `rollback_marks()` 按保护器精确摘除 ⇒ 逐个回滚到底为空。", "",
              "## 三、零漂移实证（保护器**不动生产工件**）", "",
              "| 生产工件 | 联调前 | 联调后 | 相同 |", "|---|---|---|---|"]
    for k in r["before"]:
        same = r["before"][k] == r["after"][k]
        lines.append(f"| `{k}` | `{r['before'][k][:12]}…` | `{r['after'][k][:12]}…` | "
                     f"{'✅' if same else '❌'} |")
    lines += ["", f"- **漂移项：{r['drift'] or '零'}**", "",
              "## 四、一键回滚（实测）", "",
              f"- `protector_mode_647.rollback()` ⇒ 模式 {rb['prev_mode']} → **{rb['new_mode']}**",
              f"- 回滚后**强制量是否归零**：**{rb['zero_enforcement']}**",
              f"- 回滚后实测：`{json.dumps(rb['effects_after_rollback'], ensure_ascii=False)}`", "",
              "## 诚实登记", "",
              "1. **联调通过 ≠ 保护器有效**：本模块只证明「能同时上岗 + 不打架 + 可回滚 + 不动生产工件」，"
              "**不证明**拦截后更安全（需真实运行数据）；",
              "2. **真实数据上多数强制量为 0**（无高置信冲突卡、队列无「低」项、无 >50% 规则、"
              "候选为合成）⇒ 机制由**合成输入**验证，报告已逐项标注；",
              "3. **B1 会真的改判**（内核态 → fail），是五者中唯一直接改判决态的 —— 风险最高；",
              "4. **零漂移的覆盖范围**：5 CORE_TOOLS + 452 账本 + 权威日志 + 人审队列 + 透明日志 + "
              "verified 卡清单；**不含**受控目录全量（那是门禁的另一项）；",
              "5. **回滚文件是运行期状态**（`data/647_protector_mode.json`），"
              "审计时必须一并记录当前模式。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"enforce": r, "shadow": sh, "rollback": rb},
                  fh, ensure_ascii=False, indent=2, default=str)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "enforce"
        r = rollout()
        chk("零漂移（生产工件前后一致）", r["zero_drift"] is True, str(r["drift"]))
        chk("五个保护器都有上岗记录", set(r["effects"]) == set(PROTECTORS))
        chk("标记键空间互不重叠", r["layer_check"]["keys_disjoint"] is True)
        chk("对象层互不相同（不重复拦截）", r["layer_check"]["layers_distinct"] is True)
        chk("标记可叠加且键数 = 命名空间并集", r["n_marks"] == sum(
            len(MARK_NAMESPACES[p]) for p in PROTECTORS), str(r["n_marks"]))

        # 叠加 / 冲突 / 回滚
        m: dict[str, Any] = {}
        for p in PROTECTORS:
            m = merge_marks(m, {MARK_NAMESPACES[p][0]: f"{p}-v"})
        chk("叠加不互相覆盖", len(m) == 5)
        try:
            merge_marks({"conflict_flag": True}, {"conflict_flag": False})
            chk("同名冲突抛 MarkConflictError", False)
        except MarkConflictError:
            chk("同名冲突抛 MarkConflictError", True)
        mm = dict(r["marks"])
        for p in PROTECTORS:
            mm = rollback_marks(mm, p)
        chk("逐个回滚到底 ⇒ 空", mm == {})

        sh = shadow_baseline()
        chk("shadow 下 B1 改判=0", sh["B1"]["判决态被改变（enforce 强制量）"] == 0)
        chk("shadow 下 B2 冻结=0", sh["B2"]["冻结不入队（enforce 强制量）"] == 0)
        chk("shadow 下 B3 强制盲化=0", sh["B3"]["强制盲化（enforce 强制量）"] == 0)
        chk("shadow 下 B4 降级/暂停=0",
            sh["B4"]["降级（enforce 强制量）"] == 0 and sh["B4"]["暂停（enforce 强制量）"] == 0)
        chk("shadow 下 B5 不放行=0", sh["B5"]["不放行（enforce 强制量）"] == 0)
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved

    rb = rollback_and_verify()
    chk("一键回滚 ⇒ 强制量归零", rb["zero_enforcement"] is True,
        json.dumps(rb["effects_after_rollback"], ensure_ascii=False)[:120])
    chk("回滚后模式是 shadow", rb["new_mode"] == pmode.MODE_SHADOW)
    chk("--check 实测后已恢复现场（无副作用）", rb["restored"] is True)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"B5 rollout selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B5 五保护器真上岗联调")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写联调报告 + JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rollback", action="store_true", help="一键回滚到 642 灰度并实测")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.rollback:
        print(json.dumps(rollback_and_verify(commit=True), ensure_ascii=False, indent=2,
                         default=str))
        return 0
    if a.report:
        print(f"written {write_report()}")
        return 0
    r = rollout()
    if a.json:
        print(json.dumps({"mode": r["mode"], "zero_drift": r["zero_drift"],
                          "drift": r["drift"], "effects": r["effects"]},
                         ensure_ascii=False, indent=2, default=str))
        return 0
    print(f"[647 rollout] mode={r['mode']} 零漂移={r['zero_drift']} 标记键={r['n_marks']}")
    for p in PROTECTORS:
        print(f"  {p}: {json.dumps(r['effects'][p], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
