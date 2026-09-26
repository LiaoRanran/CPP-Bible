"""643 C4 · **攻击生成器质量评估**（智能层：自动生成攻击 #4）。

**定位**：回答"针对性生成（C2）比**随机撒网**强吗？"—— 用**等预算对比**（A2 教训 2：
LLM/定向方法常靠"每次迭代更贵"取胜，不做等算力对比就是自欺）。

**指标（全部可复算）**：
- **有效攻击率** = 非 `noop` 条数 / 计划条数（空变异算"算子-载体不匹配"，不计为攻击）；
- **产生影响率** = firing 集合有变化的条数 / 有效条数（能撼动门禁的占比）；
- **预期兑现率（oracle 命中率）** = (`blocked` + `triggered`) / 有效条数
  （**生成器的预期是否靠谱**：方向 A 的预期是"仍命中"⇒ 兑现=`blocked`；
  方向 B 的预期是"开始命中"⇒ 兑现=`triggered`。**`evaded` 算预期落空**，
  但它本身是"逃逸发现"这一独立指标的价值所在 —— 两个量**必须分开**，
  本批实测踩过：早先把 `evaded` 也计入"命中"，导致"方向 A 的随机基线"**构造性恒为 1.0**，
  对比彻底失真）；
- **逃逸发现率** = `evaded` / 方向 A 的有效条数；
- **不可达候选率** = `not_triggered` / 方向 B 的有效条数。

**对比方法**：同一 `limit`、同一沙箱机制，跑 **定向计划** 与 **随机基线**，
用 **Wilson 95% 区间** 报"有效攻击率"与"oracle 命中率"的差异；样本量不足则**明确说无统计意义**。

只读契约：`--check` 只读、exit 0；`--report` **只写 `data/`**（沙箱内改副本）。纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import attack_simulator_643 as C3  # noqa: E402
import targeted_mutator_643 as C2  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_attack_quality.md")
OUT_JSON = os.path.join(ROOT, "data", "643_attack_quality.json")
DEFAULT_LIMIT = 20
MIN_N_FOR_CLAIM = 30          # 低于此样本量不声称"有统计意义"


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson 得分区间（小样本比例比正态近似稳）。n=0 ⇒ (0,1)。"""
    if n <= 0:
        return 0.0, 1.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def metrics(sim: dict[str, Any]) -> dict[str, Any]:
    """从 C3 的结果算指标（纯函数，可用合成输入测试）。"""
    rows = sim["rows"]
    total = len(rows)
    noop = sum(1 for r in rows if r["verdict"] == "noop")
    infra = sum(1 for r in rows if r["verdict"] == "infra_error")
    eff = [r for r in rows if r["verdict"] not in ("noop", "infra_error")]
    n_eff = len(eff)
    changed = sum(1 for r in eff if r.get("change"))
    # 预期兑现 = 目标规则**按生成器预期**行动：
    #   方向 A 预期"仍命中" ⇒ blocked；方向 B 预期"开始命中" ⇒ triggered。
    # `evaded` **不算兑现**（它是"逃逸发现"，另立指标），否则方向 A 的随机基线恒为 1.0。
    hit = sum(1 for r in eff if r["verdict"] in ("blocked", "triggered"))
    dir_a = [r for r in eff if r.get("direction") == "A"]
    dir_b = [r for r in eff if r.get("direction") == "B"]
    evaded = sum(1 for r in eff if r["verdict"] == "evaded")
    not_trig = sum(1 for r in eff if r["verdict"] == "not_triggered")
    mismatch = sum(1 for r in eff if r["verdict"] == "oracle_mismatch")

    def rate(k: int, n: int) -> Optional[float]:
        return round(k / n, 4) if n else None

    return {"total": total, "noop": noop, "infra_error": infra, "effective": n_eff,
            "effective_rate": rate(n_eff, total),
            "impact_rate": rate(changed, n_eff),
            "oracle_hit_rate": rate(hit, n_eff),
            "escape_find_rate": rate(evaded, len(dir_a)),
            "unreachable_rate": rate(not_trig, len(dir_b)),
            "oracle_mismatch": mismatch,
            "n_dir_a": len(dir_a), "n_dir_b": len(dir_b),
            "by_verdict": sim["by_verdict"],
            "production_unchanged": sim.get("production_atoms_unchanged"),
            "ci_effective": wilson(n_eff, total) if total else (0.0, 1.0),
            "ci_oracle_hit": wilson(hit, n_eff)}


def compare(targeted: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    """定向 vs 随机基线的等预算对比（纯函数）。"""
    t, b = metrics(targeted), metrics(baseline)
    n = min(t["total"], b["total"])
    diff_oracle = ((t["oracle_hit_rate"] or 0) - (b["oracle_hit_rate"] or 0))
    diff_impact = ((t["impact_rate"] or 0) - (b["impact_rate"] or 0))
    # 区间是否重叠 ⇒ 差异是否"看得见"
    overlap_oracle = not (t["ci_oracle_hit"][0] > b["ci_oracle_hit"][1]
                          or b["ci_oracle_hit"][0] > t["ci_oracle_hit"][1])
    significant = (n >= MIN_N_FOR_CLAIM) and not overlap_oracle
    return {"targeted": t, "random_baseline": b, "n_per_arm": n,
            "diff_oracle_hit_rate": round(diff_oracle, 4),
            "diff_impact_rate": round(diff_impact, 4),
            "ci_overlap_oracle": overlap_oracle,
            "statistically_significant": significant,
            "verdict": ("样本量足够且区间不重叠 ⇒ 差异**可声称**" if significant else
                        f"样本量 {n} < {MIN_N_FOR_CLAIM} 或区间重叠 ⇒ "
                        "**不能声称差异有统计意义**（只作方向性观察）")}


def evaluate(limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
    t = C3.simulate(C2.make_plan()["plans"], limit=limit, seed=643)
    b = C3.simulate(C3.random_plans(limit, seed=643), limit=limit, seed=643)
    cmp_ = compare(t, b)
    return {**cmp_, "limit": limit,
            "improvements": suggestions(cmp_)}


def suggestions(c: dict[str, Any]) -> list[str]:
    """改进建议（由指标推出的可执行项）。"""
    out = []
    t = c["targeted"]
    if (t["effective_rate"] or 0) < 0.8:
        out.append(f"有效攻击率 {t['effective_rate']} 偏低 ⇒ 生成前先检查"
                   "「字段/值是否真的存在于该卡」（当前 apply_op 会返回空变异）")
    if (t["oracle_hit_rate"] or 0) < 0.5:
        out.append(f"oracle 命中率 {t['oracle_hit_rate']} 偏低 ⇒ "
                   "C1 的静态 precondition 与真实触发条件偏差大：应先用**实测**"
                   "（C3 结果）回调 C2 的目标选择，而不是只信静态信号")
    if t["oracle_mismatch"]:
        out.append(f"`oracle_mismatch` {t['oracle_mismatch']} 条 ⇒ 预期规则与真实责任规则"
                   "不一致：应按实测的 `added_rules/removed_rules` 重标 oracle（留 644）")
    if t["unreachable_rate"] is not None and t["unreachable_rate"] > 0.5:
        out.append(f"不可达候选率 {t['unreachable_rate']} 偏高 ⇒ 多数方向 B 的规则"
                   "在该卡上**无法被触发**：应改选「规则本来就该管」的卡，"
                   "或承认该规则不可达（接 B3 的退役候选）")
    if c["diff_impact_rate"] <= 0:
        out.append("定向 vs 随机的**产生影响率**没拉开差距 ⇒ 定向策略当前**没有证据优势**"
                   "（这正是 A2 教训 2 要防的：不要只看\"看起来更聪明\"）")
    if not c["statistically_significant"]:
        out.append(f"样本量 {c['n_per_arm']} 太小 ⇒ 任何\"更好\"都只是方向性观察，"
                   f"要下结论需 ≥{MIN_N_FOR_CLAIM} 条/组（且 644 可复用本评估器）")
    return out or ["指标未触发任何改进项（或样本太小看不出问题）"]


def write_report() -> str:
    e = evaluate()
    t, b = e["targeted"], e["random_baseline"]
    lines = [
        "# 643 C4 · 攻击生成器质量评估（智能层：自动生成攻击 #4；等预算对比）", "",
        f"> 两组各 `limit={e['limit']}` 条，同一沙箱机制、同一种子 ⇒ **等预算对比**"
        "（A2 教训 2）。", "",
        "## 一、指标对比（定向 vs 随机基线）", "",
        "| 指标 | 定向（C2 计划） | 随机基线 | 差 |", "|---|---|---|---|"]
    keys = (("有效攻击率", "effective_rate"), ("产生影响率", "impact_rate"),
            ("oracle 命中率", "oracle_hit_rate"), ("逃逸发现率", "escape_find_rate"),
            ("不可达候选率", "unreachable_rate"))
    for label, k in keys:
        tv, bv = t[k], b[k]
        d = "—" if tv is None or bv is None else f"{tv - bv:+.4f}"
        lines.append(f"| {label} | {tv if tv is not None else '—'} | "
                     f"{bv if bv is not None else '—'} | {d} |")
    lines += ["", "### 1.1 明细与区间", "",
              f"- 定向：`total={t['total']}`（noop {t['noop']}）、有效 {t['effective']}、"
              f"verdict `{t['by_verdict']}`；有效攻击率 95% Wilson 区间 "
              f"[{t['ci_effective'][0]:.3f}, {t['ci_effective'][1]:.3f}]；"
              f"oracle 命中率区间 [{t['ci_oracle_hit'][0]:.3f}, {t['ci_oracle_hit'][1]:.3f}]",
              f"- 随机：`total={b['total']}`（noop {b['noop']}）、有效 {b['effective']}、"
              f"verdict `{b['by_verdict']}`；有效攻击率区间 "
              f"[{b['ci_effective'][0]:.3f}, {b['ci_effective'][1]:.3f}]；"
              f"oracle 命中率区间 [{b['ci_oracle_hit'][0]:.3f}, {b['ci_oracle_hit'][1]:.3f}]",
              f"- **统计判定**：{e['verdict']}",
              f"- **生产零副作用**：定向 {t['production_unchanged']} / 随机 "
              f"{b['production_unchanged']}", "",
              "## 二、改进建议（由指标推出）", ""]
    for s in e["improvements"]:
        lines.append(f"- {s}")
    lines += ["", "## 三、方向分布", "",
              f"- 定向：方向 A（逃逸型）{t['n_dir_a']} 条 / 方向 B（触发型）{t['n_dir_b']} 条；",
              "- 随机基线**全部标 A**（随机基线不知道目标规则的真实责任关系）⇒ "
              "两组的「逃逸发现率」分母不同，**直接比该率不公平**，故只比"
              "「有效攻击率 / 产生影响率 / oracle 命中率」。", "",
              "## 诚实登记", "",
              "1. **沙箱逃逸率 ≠ 生产逃逸率**（§十二.6）；",
              f"2. **样本量 {e['n_per_arm']} < {MIN_N_FOR_CLAIM}** ⇒ "
              "**不声称**任何差异有统计意义（C4 的 Wilson 区间就是为了让这句话有据）；",
              "3. **随机基线是「同载体同算子」的随机**（不是完全随机输入）⇒ 它比「真随机输入」强，"
              "因此对定向方法**更不利**（更保守的对比）；",
              "4. **oracle 命中率低不等于生成器无用**：它主要说明 C1 的**静态** precondition"
              "预测差（实测 11/20 条 `oracle_mismatch`），这正是「静态近似」的代价（见 C1 登记）；",
              "5. 本工具**只读**：不生成新算子、不改 C2/C3、不碰生产（沙箱内改副本）；",
              "6. **本批实测修掉一个指标缺陷**：早先版本把 `evaded` 也算进"
              "「oracle 命中率」⇒ **方向 A 的随机基线构造性恒为 1.0**（方向 A 的非 noop "
              "结果只可能是 blocked 或 evaded，两者都被算成「命中」），"
              "使定向 vs 随机的对比**彻底失真**（当时读到 `diff_oracle=-0.9` 才发现）；"
              "已改为「预期兑现率 = (blocked+triggered)/有效」，并加**回归锁**单测"
              "（`test_evaded_is_not_oracle_hit`）；",
              "7. **另一处已修的真实缺陷**：C2 的 `value_tamper` 布尔分支正则**组号写错**"
              "（`m2.start(2)` 但只有 1 个组）⇒ IndexError；它**逃过了 C2 自己的单测**"
              "（当时只测了数值分支），是 C4 的随机基线跑批才暴露 ⇒ 已修并补布尔分支用例。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(e, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("Wilson 全成功", wilson(10, 10) [0] > 0.6 and wilson(10, 10)[1] == 1.0)
    chk("Wilson 全失败", wilson(0, 10)[0] == 0.0 and wilson(0, 10)[1] < 0.4)
    chk("Wilson n=0 ⇒ (0,1)", wilson(0, 0) == (0.0, 1.0))
    lo, hi = wilson(5, 10)
    chk("Wilson 区间包含点估计", lo < 0.5 < hi, f"{lo:.3f},{hi:.3f}")

    sim = {"rows": [
        {"verdict": "noop", "direction": "A", "change": []},
        {"verdict": "evaded", "direction": "A", "change": ["X"]},
        {"verdict": "blocked", "direction": "A", "change": []},
        {"verdict": "not_triggered", "direction": "B", "change": []},
        {"verdict": "triggered", "direction": "B", "change": ["Y"]},
        {"verdict": "oracle_mismatch", "direction": "B", "change": ["Z"]},
    ], "by_verdict": {}, "production_atoms_unchanged": True}
    m = metrics(sim)
    chk("有效攻击率 = 5/6（noop 排除）", m["effective_rate"] == round(5 / 6, 4),
        str(m["effective_rate"]))
    chk("产生影响率 = 3/5", m["impact_rate"] == 0.6, str(m["impact_rate"]))
    # 预期兑现率 = (blocked+triggered)/有效 = 2/5（evaded **不算**兑现，见指标定义）
    chk("预期兑现率 = 2/5", m["oracle_hit_rate"] == 0.4, str(m["oracle_hit_rate"]))
    # 合成里 noop 属方向 A 但**被排除**（无效）⇒ 方向 A 有效只有 evaded/blocked 两条
    chk("逃逸发现率 = 1/2（仅方向 A 的有效条）", m["escape_find_rate"] == 0.5,
        str(m["escape_find_rate"]))
    chk("不可达候选率 = 1/3（仅方向 B）", m["unreachable_rate"] == round(1 / 3, 4))
    chk("分母互不混用（A/B 分开且排除 noop）",
        m["n_dir_a"] == 2 and m["n_dir_b"] == 3, f"{m['n_dir_a']}/{m['n_dir_b']}")
    chk("空输入不除零", metrics({"rows": [], "by_verdict": {}})["effective_rate"] is None)

    c = compare({"rows": [{"verdict": "blocked", "direction": "A", "change": []}] * 5,
                 "by_verdict": {}, "production_atoms_unchanged": True},
                {"rows": [{"verdict": "evaded", "direction": "A", "change": []}] * 5,
                 "by_verdict": {}, "production_atoms_unchanged": True})
    chk("小样本不声称显著", c["statistically_significant"] is False, c["verdict"])
    chk("改进建议非空", len(suggestions(c)) >= 1)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 C4 攻击生成器质量评估")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="跑等预算对比并写报告")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--json", action="store_true", help="打印评估（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    if x.json:
        e = evaluate(x.limit)
        print(json.dumps({k: v for k, v in e.items()}, ensure_ascii=False, indent=2))
        return 0
    print("[attack-quality] 用 --report 跑等预算对比（会真跑两次沙箱）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
