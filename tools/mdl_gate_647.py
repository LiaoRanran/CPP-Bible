"""647 B5 · MDL 规则准入**真上岗**（636 试运行 → 642 出结论 → **647 不过不给上线**）。

三档语义（§四 B5）：

| 模式 | `publish_new_rule()` 的行为 |
|---|---|
| **enforce**（默认） | 只有 `ADMIT` ⇒ `published=True`；`REJECT_*` / `PENDING_HUMAN` ⇒ **`published=False`**（拒绝上线） |
| **shadow**（回滚） | 一律 `published=True` + 附"建议"（642 的"只出结论"行为） |

**铁律保持不变**：① **不修改现有 67 条规则**；② **被拒规则不删除**（结论全部留在报告 /
`data/647_published_rules.json`）；③ 本模块**不写 `gate_engine.py`** —— "上线"在这里的语义是
"**准予进入规则库的候选通道**"，真正入库仍由人裁决。

**一键回滚**：`QUEYI_PROTECTOR_MODE=shadow` ⇒ 退回"只出建议"。

**诚实登记**：① 编码长度/豁免率判据是**启发式**，**可能误杀好规则**；② 本批**没有真实新规则提案**
（候选是**合成**的），因此"拒绝上线"实际拦下的是**合成候选**，不是真实提案；
③ `ADMIT` 也只到"准予进候选通道"，不等于"已上线生效"。

CLI：`--check` / `--report` / `--json` / `--publish`（把准入结论落 `data/647_published_rules.json`）。
纯标准库。
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

import mdl_gate_642 as base  # noqa: E402  （准入判据/热力图/在册规则单一真源，不复制）
import protector_mode_647 as pmode  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "647_mdl_enforce.md")
OUT_JSON = os.path.join(ROOT, "data", "647_mdl_enforce.json")
PUBLISHED = os.path.join(ROOT, "data", "647_published_rules.json")

PASS_DECISION = "ADMIT"


def publish_new_rule(rule_id: str, title: str = "",
                     declared_exempt_rate: Optional[float] = None,
                     hm: Optional[dict[str, dict[str, bool]]] = None,
                     existing: Optional[list[str]] = None,
                     enforce: Optional[bool] = None) -> dict[str, Any]:
    """**准入门**：enforce 下只有 `ADMIT` 能过；其余一律 `published=False`（附理由）。"""
    en = pmode.is_enforce() if enforce is None else enforce
    verdict = base.admit_new_rule(rule_id, title, hm=hm, existing=existing,
                                 declared_exempt_rate=declared_exempt_rate)
    admitted = verdict["decision"] == PASS_DECISION
    published = admitted or not en
    return {**verdict, "admitted": admitted, "mode": "enforce" if en else "shadow",
            "published": published,
            "gate_note": ("enforce：不过 MDL ⇒ **不予上线**" if en
                          else "shadow：只出建议，一律放行（642 行为）")}


def run_gate(candidates: Optional[list[dict[str, Any]]] = None,
             enforce: Optional[bool] = None) -> dict[str, Any]:
    """对候选逐条过门（默认候选 = 642 的**合成**清单）。"""
    cands = base.demo_candidates() if candidates is None else candidates
    hm = dict(base.shadow.heatmap())
    hm.update(base.SYNTH_HEATMAP)     # 只让合成候选走到 ADMIT/编码长度分支（已标注"合成"）
    ex = base.existing_rule_ids()
    rows = [publish_new_rule(c["rule_id"], c.get("title", ""), c.get("declared_exempt_rate"),
                             hm=hm, existing=ex, enforce=enforce) for c in cands]
    by_decision = _count(r["decision"] for r in rows)
    return {"mode": rows[0]["mode"] if rows else pmode.mode(),
            "rows": rows, "n": len(rows), "by_decision": by_decision,
            "n_published": sum(1 for r in rows if r["published"]),
            "n_blocked": sum(1 for r in rows if not r["published"]),
            "candidates_are_synthetic": True}


def _count(it) -> dict[str, int]:
    d: dict[str, int] = {}
    for x in it:
        d[x] = d.get(x, 0) + 1
    return d


def write_published(g: Optional[dict[str, Any]] = None) -> str:
    """把准入结论落盘（**被拒规则也保留**，不删除任何信息）。"""
    g = g or run_gate()
    payload = {"version": "647.1", "existing_67_rules_untouched": True,
               "note": "只记候选准入结论；被拒候选**保留**（不删、不改现有 67 条）；"
                       "published=True 仅表示『准予进入候选通道』，不等于已生效",
               "mode": g["mode"], "candidates": g["rows"]}
    with open(PUBLISHED, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return PUBLISHED


def synthetic_check() -> list[dict[str, Any]]:
    """合成三档：ADMIT 放行 / 两类 REJECT 拦住 / PENDING_HUMAN 也拦住（缺数据≠通过）。"""
    cases = [("CAND-SHORT-001", "短标题", 0.10, True),
             ("CAND-LONG-001", "冗长标题" * 60, 0.10, False),
             ("CAND-NODATA-001", "无数据", None, False),
             ("CAND-HIGH-EXEMPT-001", "高豁免率", 0.85, False),
             ("ATOM-REL-TARGET-HC", "已在册", 0.0, False)]
    hm = dict(base.shadow.heatmap())
    hm.update(base.SYNTH_HEATMAP)          # 合成热力图条目（已标注"合成"）
    ex = base.existing_rule_ids()
    out = []
    for rid, title, er, expect in cases:
        r = publish_new_rule(rid, title, er, hm=hm, existing=ex, enforce=True)
        out.append({"rule_id": rid, "decision": r["decision"], "expect_published": expect,
                    "published": r["published"], "ok": r["published"] == expect})
    return out


def rollback_plan() -> list[dict[str, str]]:
    return [
        {"risk": "编码长度/豁免率是**启发式** ⇒ 可能误杀好规则",
         "trigger": "被拒候选事后证明能拦到真实攻击",
         "rollback": "`QUEYI_PROTECTOR_MODE=shadow` 一键退回只出建议；"
                     "候选结论全留档（含 savings/cost/理由），人可改判"},
        {"risk": "**缺数据被判 PENDING_HUMAN** ⇒ 也可能挡住真正的新方向",
         "trigger": "新方向规则长期无热力图样本",
         "rollback": "先补攻击样本让热力图可算，再重提；人可显式豁免（本批不自动化）"},
        {"risk": "本批候选是**合成**的 ⇒ 真实提案未被真正拦过",
         "trigger": "有人把「已拒绝上线」当成对待真实提案的既有结论",
         "rollback": "真实提案到来时重跑 `--report`（判据是确定性的，结论可复算）"},
    ]


def write_report(g: Optional[dict[str, Any]] = None) -> str:
    g = g or run_gate()
    syn = synthetic_check()
    lines = [
        "# 647 B5 · MDL 规则准入**真上岗**（不过 MDL 不予上线）", "",
        f"- 当前模式：**{g['mode']}**"
        f"（enforce = 不过不给上线；shadow = 一律放行 + 附建议）",
        f"- 判据（沿用 642）：编码长度 `savings > cost` · 热力图覆盖 · 豁免率 < "
        f"{base.EXEMPT_RATE_THRESHOLD} · 已在册 ⇒ 拒绝更新", "",
        "## 一、准入实跑（候选为**合成**，非真实提案）", "",
        f"- 候选：**{g['n']}**；结论分布 `{g['by_decision']}`",
        f"- **准予进候选通道**：**{g['n_published']}**；**被拒**：**{g['n_blocked']}**", "",
        "| 候选规则 | 结论 | 是否放行 | 理由 |", "|---|---|---|---|"]
    for r in g["rows"]:
        lines.append(f"| `{r['rule_id']}` | **{r['decision']}** | "
                     f"{'✅' if r['published'] else '⛔ 拒绝'} | {r['detail']} |")
    lines += ["", "### 1.1 合成三档验证（enforce 下）", "",
              "| 候选 | 结论 | 期望放行 | 实际 | 通过 |", "|---|---|---|---|---|"]
    for s in syn:
        lines.append(f"| `{s['rule_id']}` | {s['decision']} | {s['expect_published']} | "
                     f"{s['published']} | {'✅' if s['ok'] else '❌'} |")
    lines += ["", "## 二、enforce vs shadow", "",
              "| 模式 | 不过 MDL 时的行为 |", "|---|---|",
              "| **enforce** | `published=False` ⇒ **不予上线**（附拒绝理由） |",
              "| shadow（回滚） | `published=True` + 附建议（**642 行为**） |", "",
              "- 落盘（`--publish`）：`data/647_published_rules.json`（**被拒候选也保留**）", "",
              "## 三、误判风险评估 + 回滚方案", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in rollback_plan():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **候选是合成的**：本批**没有真实新规则提案** ⇒ 「被拒上线」实际拦的是合成候选；",
              "2. **判据是启发式**（642 已登记）⇒ 可能误杀；被拒候选**全部保留**可改判；",
              "3. **现有 67 条规则零改动**（本模块只读 gate_engine）；",
              "4. `published=True` 只表示**准予进候选通道**，**不等于已上线生效**（真正入库由人裁决）；",
              "5. **不写 `gate_engine.py`**：本模块没有任何修改规则库的代码路径。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in g.items() if k != "rows"} | {"synthetic": syn},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    hm = dict(base.shadow.heatmap())
    hm.update(base.SYNTH_HEATMAP)
    ex = base.existing_rule_ids()
    chk("在册规则 67 条", len(ex) == 67, str(len(ex)))

    a = publish_new_rule("CAND-SHORT-001", "短标题", 0.1, hm=hm, existing=ex, enforce=True)
    chk("enforce：ADMIT ⇒ 放行", a["decision"] == "ADMIT" and a["published"] is True)
    b = publish_new_rule("CAND-LONG-001", "冗长" * 400, 0.1, hm=hm, existing=ex, enforce=True)
    chk("enforce：REJECT_编码长度 ⇒ **不放过**",
        b["published"] is False and b["decision"].startswith("REJECT"))
    c = publish_new_rule("CAND-NODATA-001", "T", None, hm=hm, existing=ex, enforce=True)
    chk("enforce：PENDING_HUMAN ⇒ **不放过**", c["published"] is False)
    e = publish_new_rule("ATOM-REL-TARGET-HC", "已在册", 0.0, hm=hm, existing=ex, enforce=True)
    chk("enforce：已在册 ⇒ 不放行（不改现有规则）", e["published"] is False)
    chk("enforce：被拒理由可见", bool(b["detail"]) and bool(c["detail"]))

    s1 = publish_new_rule("CAND-LONG-001", "冗长" * 400, 0.1, hm=hm, existing=ex, enforce=False)
    chk("shadow：同一条 ⇒ 放行 + 建议", s1["published"] is True and s1["decision"].startswith("REJECT"))

    syn = synthetic_check()
    chk("合成三档全对", all(s["ok"] for s in syn), str([s["rule_id"] for s in syn if not s["ok"]]))
    g = run_gate()
    chk("准入结论分布可复现", g["by_decision"] == run_gate()["by_decision"])
    chk("被拒候选保留在 rows 里", all("detail" in r for r in g["rows"]))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"B5 mdl-enforce selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 B5 MDL 准入真上岗")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--publish", action="store_true", help="落盘准入结论（含被拒候选）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    g = run_gate()
    if a.publish:
        print(f"written {write_published(g)}")
        return 0
    if a.report:
        print(f"written {write_report(g)}")
        return 0
    if a.json:
        print(json.dumps({k: v for k, v in g.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 mdl] mode={g['mode']} 候选={g['n']} 放行={g['n_published']} "
          f"被拒={g['n_blocked']} by_decision={g['by_decision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
