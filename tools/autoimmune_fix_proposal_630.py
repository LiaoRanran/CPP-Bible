"""630 A2 · 自身免疫率口径修复**方案生成**（纯标准库，只读，**不执行修复**）

基于 A1 的 132 条诊断，产出两个方案的**可审清单**：

**方案甲（补字段）**——为老卡补齐命题级字段：
- `liveness`（OBSERVATION-LIVENESS）：能从本命题**引用卡的 `artifact_assert`** 里定位到
  **夹具特有非通用符号**时，机器可**自动推断**（标 `auto`，沿用 gate 自己的
  `_assert_targets` / `_is_universal_symbol` 口径，不另写一套判定）；
  定位不到 ⇒ 标 `human`（该命题可能根本不该是 observation，见规则原文：改标 inference）。
- `object`（ATOM-CLAIM-CONCEPT-NORMALIZED）：语义判断，机器**不自动改**；但给出
  **规范概念集内的最相似候选项**（difflib）供人一键确认（标 `human`，附 `suggest`）。
- `signed_by`（INFERENCE-NOT-MACHINE-VERIFIED）：**永远 human**（§零.3 不代签；
  且填错会从 warn 升成 **block**——见 A3 悲观情景）。

**方案乙（调规则）**——按「老卡豁免 / 规则降级 / 规则改判据」三种改法给出 blast radius。

两方案的 blast radius、可逆性、风险、审计性对比 + **推荐**。
**本工具不修改任何卡、不改任何规则、不写 atoms/**。
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_fix_proposal_630.md")
OUT_JSON = os.path.join(ROOT, "data", "autoimmune_fix_proposal_630.json")

PLAN_B_RULES = {
    "OBSERVATION-LIVENESS": {
        "how": "给老卡加豁免分支：`created_at` 早于规则引入批次（530/575）的卡只 `advice` 不 `warn`",
        "blast": "改 `gate_engine.py`（CORE_TOOLS）⇒ 必须同 commit 跑 tool_integrity --update；"
                 "覆盖全库 27 张原子卡 + 未来所有卡（豁免条件一旦按卡龄写死，会长期生效）",
        "risk": "高——命题级放权闸在存量上失效；且 gate 规则数/命中数变化会牵动 191/67 等冻结数字",
    },
    "ATOM-CLAIM-CONCEPT-NORMALIZED": {
        "how": "放宽判据：object 只要**短于 N 字**即视为概念短语（不查规范集）",
        "blast": "改 CORE_TOOLS；全库所有 claim 命题；会同时放行真正不合规的 object",
        "risk": "中高——等于把「能否与图谱连通」的检查降级为长度检查",
    },
    "INFERENCE-NOT-MACHINE-VERIFIED": {
        "how": "把卡级签署兜底从 warn 降为 advice（进一步放宽）",
        "blast": "改 CORE_TOOLS；全库所有 inference 命题",
        "risk": "高——这是 526 的「核心放权闸」，降级会让「机器不能替 inference 背书」这条铁线失效",
    },
}


def _ge():
    import gate_engine as ge

    return ge


def suggest_liveness_symbol(prop: dict[str, Any], ev_idx: dict[str, dict]) -> Optional[str]:
    """从本命题引用卡的工件断言里找一个**夹具特有非通用符号**（口径复用 gate）。"""
    ge = _ge()
    refs = [str(r).strip() for r in ge._as_list(prop.get("evidence")) if str(r).strip()]
    for r in refs:
        meta = ev_idx.get(r)
        if not meta:
            continue
        rules = meta.get("artifact_assert")
        rules = [x for x in rules if isinstance(x, dict)] if isinstance(rules, list) else []
        for rule in rules:
            for t in ge._assert_targets(rule)[1]:
                t = str(t).strip()
                if not t:
                    continue
                if ge._is_universal_symbol(t):
                    continue
                if getattr(ge, "_CJK_RE", None) and ge._CJK_RE.search(t) \
                        and getattr(ge, "_IDENT_RE", None) and not ge._IDENT_RE.search(t):
                    continue      # 散文断言：无判别力
                return t
    return None


def suggest_object(object_value: str, norm: set[str]) -> Optional[str]:
    """规范概念集内最相似候选（仅供人确认，机器不自动改）。"""
    m = difflib.get_close_matches(str(object_value), sorted(norm), n=1, cutoff=0.3)
    return m[0] if m else None


def plan_a() -> dict[str, Any]:
    import autoimmune_diagnose_630 as D

    ge = _ge()
    ev_idx = ge._ev_index()
    norm = D._norm_set()
    items = []
    for r in D.diagnose()["rows"]:
        prop = D.prop_of(r["path"], r["prop_id"]) if os.path.exists(r["path"]) else {}
        item = {"card_id": r["card_id"], "card_rel": r["card_rel"],
                "prop_id": r["prop_id"], "rule": r["rule"], "field": r["field"],
                "diag_type": r["type"], "current": r["current"]}
        if r["field"] == "liveness":
            sym = suggest_liveness_symbol(prop, ev_idx)
            if sym:
                item.update({"mode": "auto", "value": {"kind": "fixture_symbol",
                                                       "symbol": sym},
                             "basis": f"符号 {sym!r} 取自本命题引用卡的 artifact_assert"
                                      "（非通用符号，gate 同口径判定）"})
            else:
                item.update({"mode": "human", "value": None,
                             "basis": "引用卡里找不到夹具特有符号 ⇒ 该命题可能不该是 "
                                      "observation（规则原文建议改标 inference 并补外部依据）"})
        elif r["field"] == "object":
            sug = suggest_object(str(r.get("current") or ""), norm)
            item.update({"mode": "human", "value": None, "suggest": sug,
                         "basis": "object 是语义判断，机器不改；给出规范集内最相似候选供人确认，"
                                  "若无合适候选则应改 claim_type 或补概念条目"})
        else:
            item.update({"mode": "human", "value": "human:<在册实名>",
                         "basis": "§零.3：机器永不代签人审；且填不规范会从 warn 升 block"})
        items.append(item)
    auto = [i for i in items if i["mode"] == "auto"]
    human = [i for i in items if i["mode"] == "human"]
    return {"items": items, "total": len(items), "auto": len(auto),
            "human": len(human),
            "cards": sorted({i["card_id"] for i in items}),
            "cards_all_auto": sorted({i["card_id"] for i in items
                                      if all(j["mode"] == "auto" for j in items
                                             if j["card_id"] == i["card_id"])}),
            "needs_human_approval": len(human) > 5}


def plan_b() -> dict[str, Any]:
    items = [{"rule": k, **v} for k, v in PLAN_B_RULES.items()]
    return {"items": items, "rules": len(items),
            "coredir": "gate_engine.py 属 CORE_TOOLS ⇒ 按 §零.7 必须同 commit 跑 "
                       "tool_integrity.py --update"}


def compare() -> dict[str, Any]:
    a, b = plan_a(), plan_b()
    return {
        "A": {"scope": f"{a['total']} 条字段（{len(a['cards'])} 张卡）",
              "files_touched": f"{len(a['cards'])} 张原子卡（受控目录！）",
              "reversible": "可逆（每张卡改动可单独回滚；建议改动前备份 + 逐卡 commit）",
              "audit": "好（逐卡 diff 可审；可进 ReviewItemLedger 留痕）",
              "debt": "偿付（债消失，不是掩盖）",
              "risk": f"中——{a['human']} 条需人填"
                      f"{'（>5 ⇒ §十.3 需人审批量处理）' if a['needs_human_approval'] else ''}；"
                      "改受控目录需遵守 §零.6 并逐条人审",
              "gate_numbers": "不变（不动规则 ⇒ 191/67 等冻结数字不动）"},
        "B": {"scope": f"{b['rules']} 条规则",
              "files_touched": "`tools/gate_engine.py`（CORE_TOOLS，单个文件）",
              "reversible": "可逆但需重钉尺子（tool_integrity --update）",
              "audit": "中（规则 diff 可审，但「为何老卡豁免」的语义落在代码里）",
              "debt": "固化（债不再报，但字段仍缺）",
              "risk": b["items"][0]["risk"] + "；且会改变 gate 冻结数字（191/67）⇒ 需重新建立基线",
              "gate_numbers": "**变化**（命中数下降 ⇒ §一 baseline 与多批冻结断言要跟着改）"},
    }


def write_report() -> str:
    a, b, cmp_ = plan_a(), plan_b(), compare()
    lines = [
        "# 630 A2 · 自身免疫率口径修复方案（两案对比，**不执行**）", "",
        "> 工具：`tools/autoimmune_fix_proposal_630.py`（只读；不修改任何卡、不改规则）",
        f"> 输入：A1 诊断的 **{a['total']} 条**口径级 warn（{len(a['cards'])} 张卡）", "",
        "## 一、方案甲：补字段", "",
        f"- 可自动推断（`auto`）：**{a['auto']} 条**；需人填（`human`）：**{a['human']} 条**",
        f"- **填完即可完全干净的卡**（该卡所有条目都 auto）：**{len(a['cards_all_auto'])} 张**",
        f"- 需人审批量处理：**{'是' if a['needs_human_approval'] else '否'}**"
        f"（任务书 §十.3 的门槛是 5 条，实测 {a['human']} 条）", "",
        "| # | 卡 | 命题 | 字段 | 模式 | 建议值 | 依据 |", "|---|---|---|---|---|---|---|",
        *[f"| {i} | `{it['card_id']}` | `{it['prop_id']}` | `{it['field']}` | "
          f"**{it['mode']}** | {json.dumps(it['value'], ensure_ascii=False) if it['value'] else '—'}"
          f"{'（建议 ' + str(it.get('suggest')) + '）' if it.get('suggest') else ''} | "
          f"{it['basis'][:60]} |" for i, it in enumerate(a["items"], 1)], "",
        "## 二、方案乙：调规则", "",
        "| 规则 | 改法 | blast radius | 风险 |", "|---|---|---|---|",
        *[f"| `{it['rule']}` | {it['how']} | {it['blast']} | {it['risk']} |"
          for it in b["items"]], "",
        "- **CORE_TOOLS 铁律提醒**：方案乙必然修改 `tools/gate_engine.py` ⇒ 按 §零.7"
        "必须同 commit 跑 `tool_integrity.py --update` 重钉尺子。", "",
        "## 三、两案对比", "",
        "| 维度 | 方案甲（补字段） | 方案乙（调规则） |", "|---|---|---|",
        *[f"| {k} | {cmp_['A'][k]} | {cmp_['B'][k]} |" for k in cmp_["A"]], "",
        "## 四、推荐：**方案甲**（附前置条件）", "",
        "理由（三条，按权重）：", "",
        "1. **不动 gate 冻结数字**：乙会改变命中数 191/67，牵动 §一 baseline 与"
        "**多批已冻结的断言**（627/629 的测试都用这些数字）⇒ 成本外溢到测试债；",
        "2. **乙的收益是假的**：老卡字段仍缺，只是不再报；「命题级放权」在存量上失效，"
        "而放权闸正是 526 的核心防线；",
        "3. **甲可审计、可回滚、可分批**：逐卡 diff + 逐卡 commit，进 ReviewItemLedger 留痕。", "",
        "**前置条件（必须人做）**：", "",
        f"- {a['human']} 条需人填（>5 ⇒ 触发 §十.3「需人审批量处理」）；其中 `signed_by` "
        "**只能由在册人签**（机器代签 = 违反 §零.3，且签错会从 warn 升 block）；",
        "- 修改受控目录 `atoms/` 需遵守人工授权流程（本批**不执行**）；",
        "- 若人选择乙，必须同时处理「gate 数字变化 ⇒ 多批测试断言同步更新」的连带债。", "",
        "## 五、诚实登记", "",
        "- `suggest`（object 的相似候选）是**机械相似度**（difflib，cutoff 0.3），"
        "**不是语义判断**，仅供人参考；",
        "- 本工具**没有**执行任何修复：atoms/ 零改动（自检断言 `git diff --quiet -- atoms`）；",
        "- 方案乙的 blast radius 是**基于源码结构**的静态判断，未实际改动规则做验证。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"plan_a": a, "plan_b": b, "compare": cmp_}, fh,
                  ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import autoimmune_diagnose_630 as D

    a, b, cmp_ = plan_a(), plan_b(), compare()
    diag = D.diagnose()
    chk("方案甲覆盖全部诊断条目", a["total"] == diag["warns"], f"({a['total']})")
    chk("每条都有 auto/human 标记",
        all(i["mode"] in ("auto", "human") for i in a["items"]))
    chk("signed_by 一律 human", all(i["mode"] == "human" for i in a["items"]
                                 if i["field"] == "signed_by"))
    chk("auto 条目都带具体建议值",
        all(i["value"] for i in a["items"] if i["mode"] == "auto"))
    chk("需人审批量处理已标记（>5 条）",
        a["needs_human_approval"] == (a["human"] > 5), f"({a['human']})")
    chk("方案乙覆盖三条规则且标注 CORE_TOOLS 风险", b["rules"] == 3
        and "CORE_TOOLS" in b["coredir"])
    chk("对比表六维齐全",
        set(cmp_["A"]) == set(cmp_["B"]) and len(cmp_["A"]) >= 6)
    chk("只读：atoms 零改动", D.git_atoms_clean())
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"A2 autoimmune fix proposal check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 A2 修复方案生成（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写方案报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    a = plan_a()
    if args.json:
        print(json.dumps({"plan_a": a, "plan_b": plan_b(), "compare": compare()},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"plan_a total={a['total']} auto={a['auto']} human={a['human']} "
          f"cards_all_auto={len(a['cards_all_auto'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
