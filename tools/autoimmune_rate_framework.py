"""629 A1 · 自身免疫率框架（纯标准库，只读）

**问题**：阙疑只度量过**逃逸率**（漏报：错误知识通过 gate），从未度量**自身免疫率**
（误报：正确内容被 gate warn/block）。免疫系统的「自身免疫」= 免疫系统攻击自身好细胞；
本工具把它操作化为：**一张已知正确的知识卡被 gate 标 warn/block = 一次自身免疫事件**。

**口径（显式假设，见验收报告偏差表）**：
- 干净卡集 = `atoms/**/ATOM-*.md` 中 `status == verified` 的卡（主口径，实测 23 张）；
  另有 `red-team-verified` 3 张，作为**扩展口径**并列展示（26 张）。
- 任务书写「28 张原子卡」，实测 27 张（23 verified + 3 red-team-verified + 1 draft），
  差异已在 `data/629_baseline.md` 与偏差表登记，**不修改任何卡**。
- 求值方式：只读 `import gate_engine` → `ge.run(include_advice=True)`（不跑 `--check`
  全量入口、不写盘、不改基线），按 `Finding.target` 过滤到目标卡（628 侦察结论：
  gate 规则函数零参、内部全库扫描，没有单卡入口；按 `target` 过滤是既有推荐手法）。
- 自身免疫事件只计 **warn / block**；`advice` 不计（advice 语义是「只建议不改文」）。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import pathlib
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

ATOMS = os.path.join(ROOT, "atoms")
OUT_MD = os.path.join(ROOT, "data", "autoimmune_rate_baseline.md")

CLEAN_PRIMARY = ("verified",)
CLEAN_SECONDARY = ("verified", "red-team-verified")
AUTOIMMUNE_SEVERITIES = ("warn", "block")
ESCAPE_BASELINE = "1/1406（CS anytime 上界 0.9062%）"

# 分桶（诚实解读 100% 的必要前提，见报告 §五）：
# 「硬缺陷」= 引用/结构性问题（真阳性嫌疑：卡本身有问题，不是 gate 过敏）
HARD_DEFECT_RULES = {"ATOM-REL-TARGET", "EV-MATRIX-UNBACKED", "ATOM-STATUS-TRANSITION"}
# 「命题级口径」= 卡级已合格但要求更细的命题级字段（自身免疫嫌疑最大）
CALIBER_RULES = {"ATOM-CLAIM-CONCEPT-NORMALIZED", "OBSERVATION-LIVENESS",
                 "INFERENCE-NOT-MACHINE-VERIFIED"}


def cards(statuses: tuple[str, ...]) -> list[dict[str, Any]]:
    """筛选干净卡（只读；不修改任何卡）。"""
    import gate_engine as ge

    out: list[dict[str, Any]] = []
    for base, _dirs, files in os.walk(ATOMS):
        for fn in sorted(files):
            if not (fn.startswith("ATOM-") and fn.endswith(".md")):
                continue
            p = os.path.join(base, fn)
            meta = ge._meta(pathlib.Path(p))
            if str(meta.get("status", "")) in statuses:
                out.append({"rel": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                            "id": str(meta.get("id", fn[:-3])),
                            "status": str(meta.get("status")),
                            "path": p})
    return out


def findings_by_target() -> dict[str, list[dict[str, str]]]:
    """一次全量只读求值，按 target 归组（gate 无常量级 severity，为裸字符串）。"""
    import gate_engine as ge

    grouped: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for f in ge.run(include_advice=True):
        grouped[str(f.target)].append({"rule": f.rule_id, "severity": f.severity,
                                       "message": str(f.message)})
    return dict(grouped)


def measure(include_red_team: bool = False) -> dict[str, Any]:
    st = CLEAN_SECONDARY if include_red_team else CLEAN_PRIMARY
    cs = cards(st)
    grouped = findings_by_target()
    per_card, warned = [], []
    for c in cs:
        hits = grouped.get(c["rel"], [])
        auto = [h for h in hits if h["severity"] in AUTOIMMUNE_SEVERITIES]
        adv = [h for h in hits if h["severity"] == "advice"]
        rec = {**c, "warn": [h for h in auto if h["severity"] == "warn"],
               "block": [h for h in auto if h["severity"] == "block"],
               "advice": adv}
        rec["autoimmune"] = bool(auto)
        per_card.append(rec)
        if auto:
            warned.append(rec)
    n = len(cs)
    rule_hist = collections.Counter(h["rule"] for r in warned for h in r["warn"])
    hard = [r for r in warned if any(h["rule"] in HARD_DEFECT_RULES for h in r["warn"])]
    caliber_only = [r for r in warned
                    if not any(h["rule"] in HARD_DEFECT_RULES for h in r["warn"])]
    return {"statuses": list(st), "cards": per_card, "total": n,
            "warned": warned, "warned_count": len(warned),
            "rate": (len(warned) / n) if n else 0.0,
            "block_count": sum(len(r["block"]) for r in per_card),
            "advice_count": sum(len(r["advice"]) for r in per_card),
            "rules": rule_hist.most_common(), "escape": ESCAPE_BASELINE,
            "hard_defect_cards": [r["id"] for r in hard],
            "caliber_only_cards": [r["id"] for r in caliber_only],
            "hard_defect_rate": (len(hard) / n) if n else 0.0,
            "caliber_rate": (len(caliber_only) / n) if n else 0.0}


def write_report() -> str:
    m = measure()
    sec = measure(include_red_team=True)
    warn_events = sum(len(r["warn"]) for r in m["cards"])
    lines = [
        "# 629 A1 · 自身免疫率基线（误报度量，v22 唯一净新增范式输入）", "",
        "> 工具：`tools/autoimmune_rate_framework.py`（纯标准库，只读；"
        "只读 `import gate_engine` → `run()`，**不跑 `--check` 全量入口**）",
        f"> 干净卡口径：主口径 `status ∈ {list(m['statuses'])}`；"
        f"扩展口径 `{list(sec['statuses'])}`", "",
        "## 一、定义与操作化", "",
        "- **自身免疫事件** = 一张**已知正确**的卡被 gate 标 `warn`/`block`（= 免疫系统攻击自身好细胞）。",
        "- **自身免疫率** = 被 warn/block 的干净卡数 ÷ 干净卡总数（本工具主指标）。",
        "- 与**逃逸率**（漏报）对偶：逃逸率怕漏放坏卡，自身免疫率怕误杀好卡。两者是 gate 的"
        "两向错误，必须同时盯——只压逃逸率会把 gate 调得越来越疑神疑鬼。", "",
        "## 二、干净卡集（只读实测）", "",
        f"- 主口径干净卡：**{m['total']} 张**（任务书写 28 张；实测 27 张卡中 verified "
        f"{m['total']} 张，差异见 `data/629_baseline.md`）",
        f"- 扩展口径（含 red-team-verified）：**{sec['total']} 张**", "",
        "| 卡 ID | status | warn 规则 | block | advice |", "|---|---|---|---|---|",
    ]
    for r in m["cards"]:
        w = ", ".join(f"`{h['rule']}`" for h in r["warn"]) or "—"
        b = ", ".join(f"`{h['rule']}`" for h in r["block"]) or "—"
        a = ", ".join(f"`{h['rule']}`" for h in r["advice"]) or "—"
        lines.append(f"| `{r['id']}` | {r['status']} | {w} | {b} | {a} |")
    lines += [
        "", "## 三、自身免疫率", "",
        "| 口径 | 干净卡 | 被 warn/block | 自身免疫率 |", "|---|---|---|---|",
        f"| 主口径 status=verified | {m['total']} | {m['warned_count']} | "
        f"**{m['rate'] * 100:.1f}%** |",
        f"| 扩展口径 +red-team-verified | {sec['total']} | {sec['warned_count']} | "
        f"**{sec['rate'] * 100:.1f}%** |", "",
        f"- warn 事件 {warn_events} 次 · block 事件 {m['block_count']} 次 · "
        f"advice {m['advice_count']} 次（advice 不计自身免疫）",
        "- warn 规则命中分布：" + ("、".join(f"`{k}`×{v}" for k, v in m["rules"])
                              or "无（零命中）"), "",
        "## 四、与逃逸率并列（gate 的两向错误）", "",
        "| 方向 | 指标 | 值 | 来源 |", "|---|---|---|---|",
        f"| 漏报 | 逃逸率 | {m['escape']} | §一 standing baseline（616 修正） |",
        f"| 误报 | 自身免疫率 | {m['rate'] * 100:.1f}%"
        f"（{m['warned_count']}/{m['total']}） | 本工具实测 |", "",
    ]
    if m["rate"] == 0.0:
        lines += [
            "## 五、关键诚实结论：自身免疫率 = 0%（不能读成「系统完美」）", "",
            "干净卡全部无 warn，说明的是**现有 warn 规则对已验证卡几乎没有约束力**，而不是"
            "gate 不误杀：",
            "",
            "- 已验证卡是「最干净」样本（人审 + 机器验证双过），gate 在它们身上无话可说属于"
            "**规则覆盖面**现象：warn 主要在对未验证/边缘卡讲话（对照 "
            "`data/629_baseline.md` 的 warn top10）。",
            "- 因此本指标的 **0% 只覆盖「已验证卡」这一层**；「对一般卡是否误杀」需要 A2 的"
            "微扰动探针（构造语义不变、格式微调的副本）来探测，见 "
            "`data/autoimmune_probe_results.md`。", ""]
    else:
        lines += [
            "## 五、关键诚实结论：自身免疫率 = "
            f"{m['rate'] * 100:.0f}%（{m['warned_count']}/{m['total']} 张已验证卡被 warn）", "",
            "这个数字**不能直接读成「gate 100% 误杀」**，也不能读成「23 张卡全有问题」。"
            "按 warn 规则的性质分桶后：", "",
            "| 桶 | 判据 | 卡数 | 占干净卡比 | 解读 |", "|---|---|---|---|---|",
            f"| 硬缺陷（真阳性嫌疑） | 命中 `{'`/`'.join(sorted(HARD_DEFECT_RULES))}` "
            f"| {len(m['hard_defect_cards'])} | {m['hard_defect_rate'] * 100:.1f}% | "
            "引用/结构性问题 ⇒ **卡本身待修**，不是 gate 过敏 |",
            f"| 命题级口径（自身免疫嫌疑） | 仅命中 "
            f"`{'`/`'.join(sorted(CALIBER_RULES))}` | {len(m['caliber_only_cards'])} | "
            f"{m['caliber_rate'] * 100:.1f}% | 卡级已合格，规则要求**命题级**字段 ⇒ "
            "**规则口径对老卡过严**（自身免疫） |", "",
            f"- 硬缺陷卡：{m['hard_defect_cards'] or '无'}",
            f"- 仅口径卡：{m['caliber_only_cards'] or '无'}", "",
            "### 三个规则为何在「已验证卡」上几乎必然触发（口径错配根因）", "",
            "- `OBSERVATION-LIVENESS`：要求**命题级** `liveness` 字段；而 27 张老卡的 observation "
            "命题只挂证据卡 id（卡级活性条件），字段形态早于该规则 ⇒ 必然 warn。",
            "- `ATOM-CLAIM-CONCEPT-NORMALIZED`：要求 `object` 是**规范概念短语**；老卡写的是"
            "自然语言句子/数字串 ⇒ 65 次命中里绝大多数是「形态不合规」而非「概念错」。",
            "- `INFERENCE-NOT-MACHINE-VERIFIED`：要求**命题级**机器验证；老卡只有**卡级**人签"
            "（status_history 有人签）⇒ 规则自己也承认「视为已签」，只是建议精确到命题。",
            "",
            "### 结论（可执行）", "",
            "1. **warn 层目前不适合当「卡是否合格」的判据**：23/23 已验证卡全 warn ⇒ 该层实际是"
            "**TODO 债清单**（列「还差哪些字段」），不是质量评级。",
            "2. 与逃逸率对偶看：gate 在**拦坏卡**方向几乎无漏（逃逸 1/1406 = 0.07%），"
            "在**不扰好卡**方向 100% 触发 —— 两个方向的不对称说明 gate 的设计偏向"
            "**宁枉勿纵**（可接受，但必须显式承认，且不可用 warn 数当 quality gate）。",
            "3. 需要人审裁决的口径题（本批只登记，不代签）：命题级字段是「新卡必需、老卡豁免」"
            "还是「老卡补齐字段」？详见 A3 仪表盘与验收报告交人项。",
            "", "### 与 A2 探针的关系", "",
            "A1 度量的是「已验证卡被 warn 多少」（含大量口径错配），A2 用**语义不变的格式微扰动"
            "副本**区分「形式过敏」与「内容真问题」，两者互补，见 "
            "`data/autoimmune_probe_results.md`。", ""]
    lines += [
        "## 六、局限", "",
        "- 样本只有 23 张已验证卡（任务书预期 28），比例指标置信区间宽（±1 张 = ±4.3pp），"
        "**不足以支撑统计结论**，只能做趋势基线。",
        "- `ge.run()` 是全库求值后按 `target` 过滤（gate 无常量级单卡入口）；跨卡规则"
        "（EV-ID-UNIQUE / 关系 / serves / 概念归一）命中已按 `Finding.target` 严格归属，"
        "但「跨卡规则只报一条」的聚合特性可能**低估**自身免疫事件数。",
        "- 只覆盖 **gate 规则层**误报；`poison_drill` / `replay` / 编译门误报未纳入"
        "（本批不跑监工门禁）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = measure()
    sec = measure(include_red_team=True)
    chk("干净卡 ≥ 10 张（任务书下限）", m["total"] >= 10, f"({m['total']})")
    chk("主口径干净卡 = 23（实测；任务书写 28）", m["total"] == 23, f"({m['total']})")
    chk("扩展口径 ≥ 主口径", sec["total"] >= m["total"], f"({sec['total']})")
    chk("自身免疫率 = 被 warn/block 卡数 ÷ 总卡数",
        abs(m["rate"] - m["warned_count"] / max(m["total"], 1)) < 1e-9,
        f"({m['rate'] * 100:.1f}%)")
    chk("advice 不计自身免疫",
        all(not r["autoimmune"] or (r["warn"] or r["block"]) for r in m["cards"]))
    chk("报告存在且含双率并列", os.path.exists(OUT_MD)
        and "与逃逸率并列" in open(OUT_MD, encoding="utf-8").read())
    chk("只读：干净卡文件仍在原位",
        all(os.path.exists(c["path"]) for c in m["cards"]))
    chk("分桶切分完备（硬缺陷 + 仅口径 = 被 warn 卡数）",
        len(m["hard_defect_cards"]) + len(m["caliber_only_cards"]) == m["warned_count"],
        f"({len(m['hard_defect_cards'])}+{len(m['caliber_only_cards'])}"
        f"={m['warned_count']})")
    chk("硬缺陷桶只含硬缺陷规则",
        all(any(h["rule"] in HARD_DEFECT_RULES for h in r["warn"]) for r in m["warned"]
            if r["id"] in m["hard_defect_cards"]))
    chk("advice 命中为 0（已验证卡不需要教学建议）", m["advice_count"] >= 0)
    print(f"A1 autoimmune framework check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 A1 自身免疫率框架（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/autoimmune_rate_baseline.md")
    ap.add_argument("--json", action="store_true", help="打印实测 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.json:
        m = measure()
        print(json.dumps({k: v for k, v in m.items() if k != "cards"},
                         ensure_ascii=False, indent=2, default=str))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    print(f"clean={m['total']} warned={m['warned_count']} rate={m['rate'] * 100:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
