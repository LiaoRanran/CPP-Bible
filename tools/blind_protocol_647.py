"""647 B3 · blind_protocol **真上岗**（636 影子 → 642 标记违规 + 盲化新开单 → **647 新判决强制盲化**）。

647 与 642 的差别（§四 B3）：
* 642：只有 `review_method=ITEM_BLIND` 的**新开单**才盲化；历史 258 条**只标记**；
* 647（enforce）：**所有新判决**在生成时**强制盲化** —— 不论请求的方法是什么，
  AI 推荐一律**人审完成后才可见**；人审期读 AI 推荐 ⇒ 抛 `BlindViolation`（**不是**返回 None）。

三条硬边界（沿用 642，**647 不动**）：
1. **历史 452 条不回溯、只标记**（append-only；本模块只读账本、字节不变）；
2. **不写权威账本**、**不代签**（揭盲结果只在内存/报告里，形态仍是 `staged`）；
3. **不接管任何人审前端**（本模块提供协议与可执行校验；真实盲性靠前端 + 流程纪律）。

**回滚**：`QUEYI_PROTECTOR_MODE=shadow` ⇒ 退回 642 行为（只有 ITEM_BLIND 才盲化）。

**诚实登记**：协议级盲化 **≠ 密码学盲化** —— 载荷仍在内存，`recommendation()` 的拒绝是
**流程级纪律**（能拦住"顺手读一下"，拦不住"绕过封装读属性"）。真实盲性靠前端（交人项）。

CLI：`--check` / `--report` / `--json`。纯标准库。
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

import blind_protocol_642 as base  # noqa: E402  （盲化算法/历史扫描单一真源，不复制）
import protector_mode_647 as pmode  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_blind_enforce.md")
OUT_JSON = os.path.join(ROOT, "data", "647_blind_enforce.json")

BLIND_METHOD = base.BLIND_METHOD      # ITEM_BLIND


class BlindViolation(RuntimeError):
    """647 B3：人审未完成就想拿 AI 推荐 ⇒ **拒绝**（不是返回 None、不是静默放行）。"""


@dataclasses.dataclass
class Judgment:
    """一条**新判决**（enforce 下强制盲化）。"""

    item_id: str
    review_method_requested: str
    review_method_effective: str
    item: base.BlindItem
    enforced: bool

    def visible_view(self) -> dict[str, Any]:
        """人审期可见视图。enforce 下**保证**不含 `ai_recommendation`。"""
        view = self.item.visible_view()
        if self.enforced and not self.item.revealed and "ai_recommendation" in view:
            raise BlindViolation(f"{self.item_id}：enforce 下**人审未完成**却泄露了 AI 推荐")
        return view

    def recommendation(self) -> float:
        """读 AI 推荐：**未揭盲 ⇒ 抛 `BlindViolation`**（enforce）；shadow 下按 642 行为放行。"""
        if self.enforced and not self.item.revealed:
            raise BlindViolation(
                f"{self.item_id}：人审未完成，AI 推荐不可见（647 B3 强制盲化）")
        return self.item.ai_recommendation

    def reveal(self, human_value: float) -> "Judgment":
        """人审提交后揭盲（校验可逆）+ 记录人审值。**不写账本**。"""
        return dataclasses.replace(self, item=base.reveal_after_human(self.item, human_value))

    def disagreement(self) -> Optional[dict[str, Any]]:
        return base.disagreement(self.item)

    @property
    def blind_state(self) -> str:
        return str(self.item.visible_view()["blind_state"])


def new_judgment(item_id: str, ai_recommendation: float,
                 review_method: str = "BATCH_AUTH") -> Judgment:
    """生成一条新判决。

    * **enforce**：不论请求什么方法，一律 `ITEM_BLIND` **强制盲化**；
    * **shadow**（回滚态）：按 642 行为 —— 只有 `ITEM_BLIND` 才盲化。
    """
    enforce = pmode.is_enforce()
    effective = BLIND_METHOD if enforce else review_method
    item = base.open_item(item_id, ai_recommendation, review_method=effective)
    return Judgment(item_id=item_id, review_method_requested=review_method,
                    review_method_effective=effective, item=item, enforced=enforce)


def disagreement_rate(judgments: list[Judgment]) -> Optional[float]:
    """分歧率（人 vs AI）；无已揭盲条 ⇒ **None**（不编造）。"""
    return base.disagreement_rate([j.item for j in judgments])


def history_marks() -> dict[str, Any]:
    """历史 452 条扫描（**只标记不修改**，账本字节不变由 642 保证）。"""
    h = base.scan_history()
    return {"n_decisions": h["n_decisions"], "n_violations": h["n_violations"],
            "ledger_unchanged": h["ledger_unchanged"], "ledger_digest": h["ledger_digest"],
            "policy": "不回溯、只标记（append-only）"}


def run_new_demo() -> dict[str, Any]:
    """新判决演示：3 条不同请求方法 ⇒ enforce 下**全部** ITEM_BLIND；1 条揭盲算分歧。"""
    demo = [new_judgment("NEW-001", 35.8, "BATCH_AUTH"),
            new_judgment("NEW-002", 12.5, "ITEM_OPEN"),
            new_judgment("NEW-003", 7.0, "ITEM_BLIND")]
    done = [demo[0].reveal(40.0), demo[1], demo[2]]
    return {"n": len(demo), "by_effective_method": _count(j.review_method_effective for j in demo),
            "n_blinded": sum(1 for j in demo if j.item.blinded),
            "rows": [{"item_id": j.item_id,
                      "requested": j.review_method_requested,
                      "effective": j.review_method_effective,
                      "blind_state": j.blind_state,
                      "visible_keys": sorted(j.visible_view()),
                      "enforced": j.enforced} for j in done],
            "disagreement_rate": disagreement_rate(done),
            "n_revealed": sum(1 for j in done if j.item.revealed)}


def _count(it) -> dict[str, int]:
    d: dict[str, int] = {}
    for x in it:
        d[x] = d.get(x, 0) + 1
    return d


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "强制盲化降低人审吞吐（审者失去 AI 提示）",
         "trigger": "人审队列 waiting 增加 / throughput 下降",
         "rollback": "`QUEYI_PROTECTOR_MODE=shadow` ⇒ 只有 ITEM_BLIND 才盲化（642 行为）"},
        {"risk": "协议级盲化**不是密码学盲化**（载荷在内存里，能绕过封装读属性）",
         "trigger": "有人直接访问 `Judgment.item.ai_recommendation`",
         "rollback": "真实盲性需前端 + 流程纪律（交人项）；本模块只保证「正常路径拿不到」"},
        {"risk": "强制盲化对**所有**新判决生效 ⇒ 连 BATCH_AUTH 批量流程也被改",
         "trigger": "批量授权流程被盲化阻塞",
         "rollback": "shadow 一键回滚；或仅对指定方法强制（需人裁决口径）"},
    ]


def write_report() -> str:
    d = run_new_demo()
    h = history_marks()
    saved = os.environ.get(pmode.ENV)
    try:
        os.environ[pmode.ENV] = "shadow"
        shadow_demo = [new_judgment("S-001", 1.0, "BATCH_AUTH"),
                       new_judgment("S-002", 2.0, "ITEM_BLIND")]
        shadow_row = {"by_effective": _count(j.review_method_effective for j in shadow_demo),
                      "n_blinded": sum(1 for j in shadow_demo if j.item.blinded)}
        os.environ[pmode.ENV] = "enforce"
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved
    lines = [
        "# 647 B3 · blind_protocol **真上岗**（新判决强制盲化；历史只标记不回溯）", "",
        f"- 当前模式：**{pmode.mode()}**"
        f"（enforce = **所有新判决强制 ITEM_BLIND**；shadow = 642 行为，仅 ITEM_BLIND 盲化）",
        f"- 强制方法：`{BLIND_METHOD}`；人审期读 AI 推荐 ⇒ **`BlindViolation`**（不返回 None）", "",
        "## 一、新判决实跑（3 条，请求了 3 种不同方法）", "",
        f"- 生效方法分布：`{d['by_effective_method']}`；被盲化：**{d['n_blinded']}/{d['n']}**",
        f"- 已揭盲 1 条 ⇒ 分歧率 **{d['disagreement_rate']}**（样本 1，**不可解读为盲评收益**）", "",
        "| 条目 | 请求方法 | 生效方法 | 盲态 | 可见字段 | enforce |", "|---|---|---|---|---|---|"]
    for r in d["rows"]:
        lines.append(f"| `{r['item_id']}` | {r['requested']} | **{r['effective']}** | "
                     f"{r['blind_state']} | `{', '.join(r['visible_keys'])}` | {r['enforced']} |")
    lines += ["", "### 1.1 enforce vs shadow 对照（同一调用）", "",
              "| 模式 | 生效方法分布 | 被盲化 |", "|---|---|---|",
              f"| **enforce** | `{d['by_effective_method']}` | {d['n_blinded']}/{d['n']} |",
              f"| shadow（回滚态） | `{shadow_row['by_effective']}` | "
              f"{shadow_row['n_blinded']}/2 |", "",
              "## 二、历史判决（**不回溯、只标记**）", "",
              f"- 判决总数：**{h['n_decisions']}**；AI 可见（违规）：**{h['n_violations']}** 条",
              f"- 账本字节前后一致：**{h['ledger_unchanged']}**（sha256 `{h['ledger_digest']}…`）",
              f"- 处置：{h['policy']}", "",
              "## 三、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **协议级盲化 ≠ 密码学盲化**：载荷仍在内存；`recommendation()` 的拒绝是**流程纪律**；",
              "2. **历史一字未改**（642 已实测 sha256 前后一致）；258 条违规**只标记**；",
              "3. **分歧率样本 1/1 ⇒ 不可解读**为盲评收益（无历史基线，不编造）；",
              "4. **强制盲化扩到了所有新判决**（含 BATCH_AUTH）——这是 647 与 642 的行为差别，也是风险点；",
              "5. 揭盲结果只 `staged`/内存，**不写权威账本、不代签**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"demo": d, "history": h, "shadow_control": shadow_row,
                   "mode": pmode.mode()}, fh, ensure_ascii=False, indent=2)
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
        j = new_judgment("T-1", 35.8, "BATCH_AUTH")
        chk("enforce：任意请求方法都强制 ITEM_BLIND",
            j.review_method_effective == BLIND_METHOD and j.item.blinded is True)
        chk("enforce：盲态视图不含 AI 推荐", "ai_recommendation" not in j.visible_view())
        chk("enforce：盲态含 masked/residual",
            {"masked", "residual"} <= set(j.visible_view()))
        try:
            j.recommendation()
            chk("enforce：未揭盲读 AI 推荐 ⇒ BlindViolation", False)
        except BlindViolation:
            chk("enforce：未揭盲读 AI 推荐 ⇒ BlindViolation", True)
        done = j.reveal(40.0)
        chk("揭盲后可读 AI 推荐", done.recommendation() == 35.8)
        chk("揭盲校验可逆（不可逆则抛 RuntimeError）", done.item.revealed is True)
        chk("分歧计算正确", (done.disagreement() or {}).get("disagree") is True)
        chk("无已揭盲条 ⇒ 分歧率 None",
            disagreement_rate([new_judgment("T-2", 1.0)]) is None)

        os.environ[pmode.ENV] = "shadow"
        s = new_judgment("T-3", 9.0, "BATCH_AUTH")
        chk("shadow：非 ITEM_BLIND 不盲化（642 行为）",
            s.item.blinded is False and s.visible_view().get("ai_recommendation") == 9.0)
        chk("shadow：读 AI 推荐不抛", s.recommendation() == 9.0)
        s2 = new_judgment("T-4", 3.0, "ITEM_BLIND")
        chk("shadow：ITEM_BLIND 仍盲化", s2.item.blinded is True)
        os.environ[pmode.ENV] = "enforce"
    finally:
        if saved is None:
            os.environ.pop(pmode.ENV, None)
        else:
            os.environ[pmode.ENV] = saved

    h = history_marks()
    chk("历史判决 452 条且未改账本",
        h["n_decisions"] == 452 and h["ledger_unchanged"] is True)
    chk("历史只标记不回溯", h["n_violations"] == 258, str(h["n_violations"]))
    d = run_new_demo()
    chk("enforce 下 3/3 全盲化", d["n_blinded"] == 3)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"B3 blind-enforce selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B3 blind_protocol 真上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    d = run_new_demo()
    h = history_marks()
    if a.json:
        print(json.dumps({"mode": pmode.mode(), "demo": d, "history": h},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 blind] mode={pmode.mode()} 生效方法分布={d['by_effective_method']} "
          f"盲化={d['n_blinded']}/{d['n']}；历史 {h['n_decisions']} 条违规 "
          f"{h['n_violations']} 只标记（账本未变={h['ledger_unchanged']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
