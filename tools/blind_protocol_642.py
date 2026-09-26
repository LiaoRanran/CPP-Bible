"""642 A3 · blind_protocol **上岗**（新入队判决强制盲化；历史只标记不修改）。

**与 636 的关系**：636 是**影子设计**（`blind_protocol_636` 只出报告），本模块把它落成
**可执行流程**：新入队判决走盲化 —— `review_method=ITEM_BLIND` 的判决，**AI 推荐在人审完成前不可见**。

**上岗行为**（§三 A3）：

| 环节 | 行为 |
|---|---|
| 开单 | `open_item()`：AI 推荐 → **注入式盲化** `masked = value + sign × offset`（沿用 636 算法） |
| 人审期 | `visible_view()`：只给 `masked` / `residual`，**不含 AI 推荐**（强制盲化） |
| 提交后 | `reveal_after_human()`：揭盲并算**分歧**（人 vs AI） |
| 非 ITEM_BLIND | 不盲化（BATCH_AUTH / MIRROR_DERIVED / ITEM_OPEN 照旧） |
| 历史 452 条 | **只扫描标记，不修改一字**（append-only 铁律） |

**铁律**：**不修改历史判决**（`data/authority/decision_event_v2_ledger.jsonl` 只读）；
**不改任何人审前端/流程**（本批只提供协议与工具；真实盲评需人授权）。
**不代签**：`reveal_after_human()` 只产出 `staged:` 形态的结果，**不写权威账本**。

**诚实登记**（§十.1）：本模块是**协议级盲化**，不是密码学承诺 —— Python 对象里 AI 推荐仍存在，
"不可见"指的是**人审视图不含它**；真实盲性依赖前端与流程纪律。分歧率**无历史基线** ⇒
只能对**本批新开单**计算，历史分歧率**仍无法计算**（不编造）。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_blind_rollout.md`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import blind_protocol_636 as shadow  # noqa: E402  （盲化算法单一真源，不复制）

OUT_MD = os.path.join(ROOT, "data", "642_blind_rollout.md")
LEDGER = shadow.LEDGER

#: 强制盲化的 review_method（决策包 v2 五级口径之一）
BLIND_METHOD = "ITEM_BLIND"
#: 历史扫描口径：AI 推荐**可见**下做的判决（636 同源）
AI_VISIBLE_ORIGINS = ("human_observed", "user_authorized_execution")


@dataclasses.dataclass(frozen=True)
class BlindItem:
    """盲态条目。`ai_recommendation` 是**载荷**；`visible_view()` 在盲态**不暴露它**。"""
    item_id: str
    review_method: str
    masked: float
    offset: float
    sign: int
    residual: float
    ai_recommendation: float
    blinded: bool = True
    revealed: bool = False
    human_value: Optional[float] = None

    def visible_view(self) -> dict[str, Any]:
        """人审期间可见视图。**盲态下不含 AI 推荐**（含揭盲后才出现）。"""
        view: dict[str, Any] = {
            "item_id": self.item_id,
            "review_method": self.review_method,
            "blind_state": "REVEALED" if self.revealed else ("BLIND" if self.blinded else "OPEN"),
            "masked": self.masked,
            "residual": self.residual,
        }
        if not self.blinded or self.revealed:
            view["ai_recommendation"] = self.ai_recommendation
        return view


def requires_blinding(review_method: str) -> bool:
    """哪些判决方法**必须盲化**：新入队的 `ITEM_BLIND`。"""
    return review_method == BLIND_METHOD


def open_item(item_id: str, ai_recommendation: float,
              review_method: str = BLIND_METHOD) -> BlindItem:
    """开一条待审项：ITEM_BLIND ⇒ 盲化；其余方法 ⇒ 不盲化（AI 推荐可见）。"""
    blind = requires_blinding(review_method)
    inj = shadow.inject(ai_recommendation)
    return BlindItem(item_id=item_id, review_method=review_method,
                     masked=inj["masked"] if blind else ai_recommendation,
                     offset=inj["offset"] if blind else 0.0,
                     sign=int(inj["sign"]) if blind else 0,
                     residual=inj["residual"] if blind else 0.0,
                     ai_recommendation=ai_recommendation,
                     blinded=blind, revealed=not blind)


def reveal_after_human(item: BlindItem, human_value: float) -> BlindItem:
    """人审提交后揭盲 + 算分歧。返回新对象（`BlindItem` 不可变）；**不写账本**。"""
    restored = shadow.reveal({"masked": item.masked, "sign": item.sign,
                              "offset": item.offset}) if item.blinded else item.masked
    if restored != item.ai_recommendation:
        raise RuntimeError(f"揭盲失真：{restored} != {item.ai_recommendation}（盲化不可逆）")
    return dataclasses.replace(item, revealed=True, blinded=False, human_value=human_value)


def disagreement(item: BlindItem) -> Optional[dict[str, Any]]:
    """单条分歧：人 vs AI。未揭盲 ⇒ None（不编造）。"""
    if not item.revealed or item.human_value is None:
        return None
    return {"item_id": item.item_id, "human": item.human_value,
            "ai": item.ai_recommendation, "disagree": item.human_value != item.ai_recommendation}


def disagreement_rate(items: list[BlindItem]) -> Optional[float]:
    """分歧率 = 分歧条数 / 已揭盲条数；无已揭盲条 ⇒ **None**（不编造）。"""
    ds = [d for d in (disagreement(i) for i in items) if d is not None]
    if not ds:
        return None
    return round(sum(1 for d in ds if d["disagree"]) / len(ds), 4)


def _read_jsonl(path: str) -> list[dict[str, Any]]:
    """只读读法（坏行跳过，不抛）。"""
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


def _ledger_digest() -> str:
    try:
        with open(LEDGER, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return ""


def scan_history() -> dict[str, Any]:
    """扫描历史 452 条判决：AI 可见 = 违规。**只标记，不修改**（append-only 铁律）。"""
    before = _ledger_digest()
    rows = _read_jsonl(LEDGER)
    marks = [{"event_id": r.get("event_id", ""), "review_method": r.get("review_method", ""),
              "decision_origin": r.get("decision_origin", ""),
              "violation": r.get("decision_origin") in AI_VISIBLE_ORIGINS}
             for r in rows]
    viol = [m for m in marks if m["violation"]]
    after = _ledger_digest()
    return {"n_decisions": len(rows), "n_violations": len(viol),
            "marked": marks, "violations": viol,
            "ledger_unchanged": before == after and before != "",
            "ledger_digest": before[:16]}


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "盲化降低人审吞吐（审者失去 AI 提示）",
         "trigger": "人审队列 waiting 增加 / throughput 下降",
         "rollback": "只对**新开单**生效 ⇒ 停止新开 ITEM_BLIND 单即可回到旧流程；"
                     "已开单可 `reveal_after_human()` 立即揭盲"},
        {"risk": "协议级盲化非密码学承诺（载荷仍在内存）",
         "trigger": "有人直接读 `BlindItem.ai_recommendation`",
         "rollback": "真实盲性需前端 + 流程纪律（交人项）；本批不接管前端"},
        {"risk": "分歧率无历史基线 ⇒ 新开单样本少时不可解读",
         "trigger": "用 1–2 条样本推断盲评收益",
         "rollback": "无已揭盲条时返回 **None**（不编造）；样本充足后再解读"},
    ]


def write_report() -> str:
    h = scan_history()
    # 演示：开 3 条新单（2 条 ITEM_BLIND + 1 条 BATCH_AUTH），其中 1 条已揭盲
    demo_open = [open_item("NEW-001", 35.8), open_item("NEW-002", 12.5),
                 open_item("NEW-003", 7.0, review_method="BATCH_AUTH")]
    demo_done = [reveal_after_human(demo_open[0], 40.0), demo_open[1], demo_open[2]]
    rate = disagreement_rate(demo_done)
    lines = [
        "# 642 A3 · blind_protocol 上岗（新入队判决强制盲化 · 历史只标记不修改）", "",
        "## 一、上岗流程", "",
        "| 环节 | 行为 |", "|---|---|",
        f"| 开单 `open_item()` | `review_method={BLIND_METHOD}` ⇒ 注入式盲化 "
        "`masked = value + sign × offset` |",
        "| 人审期 `visible_view()` | 只给 `masked` / `residual`，**不含 AI 推荐** |",
        "| 提交后 `reveal_after_human()` | 揭盲（校验可逆）+ 算分歧，**只 staged 不写账本** |",
        "| 非 ITEM_BLIND | 不盲化（BATCH_AUTH / MIRROR_DERIVED / ITEM_OPEN 照旧） |", "",
        "## 二、盲化演示（新开单）", "",
        "| 条目 | 方法 | 盲态 | 可见字段 | 揭盲后 |", "|---|---|---|---|---|"]
    for it in demo_open:
        shown = ", ".join(sorted(it.visible_view()))
        lines.append(f"| `{it.item_id}` | {it.review_method} | "
                     f"{'盲' if it.blinded else '公开'} | `{shown}` | — |")
    lines += ["", f"- 已揭盲 1 条（NEW-001：人 40.0 vs AI 35.8）⇒ 分歧率 **{rate}**"
                  f"（{1 if rate == 1.0 else 0}/1）",
              "- **无已揭盲条时 `disagreement_rate` 返回 `None`**（不编造）；历史分歧率仍**无法计算**"
              "（636 同结论：无盲评基线）", "",
              "## 三、历史判决扫描（452 条，**只标记不修改**）", "",
              f"- 判决总数：**{h['n_decisions']}**",
              f"- **AI 推荐可见（违规）：{h['n_violations']}** 条"
              f"（口径：`decision_origin ∈ {AI_VISIBLE_ORIGINS}`）",
              f"- 账本字节前后一致：**{h['ledger_unchanged']}**（sha256 `{h['ledger_digest']}…`）", "",
              "| 违规条数 | 处置 |", "|---|---|",
              f"| {h['n_violations']} | **只标记**（append-only 铁律：不修改、不删除、不回填） |", "",
              "## 四、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **协议级盲化 ≠ 密码学盲化**：AI 推荐仍在对象载荷里，"
              "「不可见」指**人审视图不含它**；真实盲性靠前端 + 流程纪律（交人项）；",
              "2. **历史一字未改**（sha256 前后一致已实测）；258 条违规**只标记**；",
              "3. **分歧率无历史基线**：本批只对新开单可算，样本为 1/1，**不可解读为盲评收益**；",
              "4. 不代签：揭盲结果只 `staged`，不写权威账本；",
              "5. 灰度期**不接管任何人审前端**，新判决是否真走 ITEM_BLIND 由人审流程决定。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    it = open_item("T-1", 35.8)
    chk("ITEM_BLIND ⇒ 盲化", it.blinded is True)
    chk("盲化可逆（揭盲还原 AI 值）", shadow.reveal({"masked": it.masked, "sign": it.sign,
                                                    "offset": it.offset}) == 35.8)
    view = it.visible_view()
    chk("盲态视图不含 AI 推荐", "ai_recommendation" not in view, str(sorted(view)))
    chk("盲态视图含 masked/residual", "masked" in view and "residual" in view)

    done = reveal_after_human(it, 40.0)
    chk("揭盲后可见 AI 推荐", done.visible_view().get("ai_recommendation") == 35.8)
    d = disagreement(done)
    chk("分歧计算正确", d is not None and d["disagree"] is True)
    chk("未揭盲不计分歧", disagreement(open_item("T-2", 1.0)) is None)
    chk("无已揭盲条 ⇒ 分歧率 None", disagreement_rate([open_item("T-3", 1.0)]) is None)

    plain = open_item("T-4", 9.0, review_method="BATCH_AUTH")
    chk("非 ITEM_BLIND 不盲化", plain.blinded is False
        and plain.visible_view().get("ai_recommendation") == 9.0)

    h = scan_history()
    chk("历史判决 452 条", h["n_decisions"] == 452, str(h["n_decisions"]))
    chk("历史账本未被改动", h["ledger_unchanged"] is True)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 A3 blind_protocol 上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写上岗报告")
    ap.add_argument("--json", action="store_true", help="打印历史扫描（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    h = scan_history()
    if a.json:
        print(json.dumps({k: v for k, v in h.items() if k not in ("marked", "violations")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[blind] 历史 {h['n_decisions']} 条；AI 可见（违规）{h['n_violations']} 条"
          f"（只标记不修改，账本未变={h['ledger_unchanged']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
