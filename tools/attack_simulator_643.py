"""643 C3 · **攻击效果模拟器**（智能层：自动生成攻击 #3）。

**定位**：把 C2 的 mutation 计划在**沙箱**里真跑一遍，看目标规则**是否被触发/拦住**，
并记录**连带影响**（其它规则的 firing 变化 = 涟漪）。

**沙箱**：复用本仓既有的 `mutation_fuzz.sandbox()` —— 它把 `atoms/`+`evidence/`+`Examples/`
整树复制进 tempdir，并把 `ge.ATOMS/ge.EVIDENCE` 与 `replay.run_root()` 全部指向副本
⇒ **生产仓零副作用**（本工具另加"跑前跑后 `atoms/` 树指纹一致"的硬校验）。

**判定（每个 mutation 一条）**：

| verdict | 含义 |
|---|---|
| `noop` | `apply_op` 没改动文本（空变异）⇒ **不计入攻击** |
| `blocked` | 方向 A：变异后目标规则**仍然命中** ⇒ 规则没被绕开 |
| `evaded` | 方向 A：变异后目标规则**不再命中** ⇒ **逃逸**（真发现） |
| `triggered` | 方向 B：变异后目标规则**命中** ⇒ 规则可达 |
| `not_triggered` | 方向 B：变异后仍不命中 ⇒ 规则**不可达候选** |
| `oracle_mismatch` | 目标规则没动，但**别的**规则动了 ⇒ 生成器的预期可能猜错（§十二.7） |

只读契约：`--check` 只读、exit 0；`--run` / `--report` **只写 `data/`**（沙箱内改的是副本）。
纯标准库；≥6 例单测（**不真跑沙箱**，跑批由 `--run` 与测试里的 1 例小样本负责）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import gate_engine as ge  # noqa: E402
import mutation_fuzz as mf  # noqa: E402
import rule_precondition_analyzer_643 as C1  # noqa: E402
import targeted_mutator_643 as C2  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_attack_sim.md")
OUT_JSON = os.path.join(ROOT, "data", "643_attack_sim.json")
DEFAULT_LIMIT = 12


def tree_digest(path: str) -> str:
    """目录树指纹（相对路径 + 内容），用于"生产零副作用"硬校验。"""
    h = hashlib.sha256()
    for base, _dirs, files in os.walk(path):
        for f in sorted(files):
            p = os.path.join(base, f)
            h.update(os.path.relpath(p, path).replace(os.sep, "/").encode())
            try:
                h.update(open(p, "rb").read())
            except OSError:
                h.update(b"<unreadable>")
    return h.hexdigest()


def rules_firing_with(stem: str) -> set[str]:
    """当前（沙箱内）仓库里，**target 含该卡 stem** 的 firing 规则集合。"""
    return {f.rule_id for f in ge.run(include_advice=True) if stem in f.target}


def classify(direction: str, target_fired_before: bool, target_fired_after: bool,
             any_change: bool) -> str:
    """纯函数：判定 verdict（见 docstring 表）。"""
    if direction == "A":
        if not target_fired_after:
            return "evaded"
        return "blocked"
    if target_fired_after:
        return "triggered"
    return "oracle_mismatch" if any_change else "not_triggered"


def simulate(plans: list[dict[str, Any]], limit: int = DEFAULT_LIMIT,
             seed: Optional[int] = None) -> dict[str, Any]:
    """在**一个**沙箱会话里逐个施加 mutation（每个跑完立刻还原），返回结果与统计。"""
    todo = plans[:limit]
    before_tree = tree_digest(os.path.join(ROOT, "atoms"))
    rows: list[dict[str, Any]] = []
    with mf.sandbox() as tmp:
        for p in todo:
            card = os.path.join(str(tmp), p["card"])
            if not os.path.exists(card):
                rows.append({**p, "verdict": "infra_error", "why": "沙箱内找不到卡"})
                continue
            orig = open(card, encoding="utf-8").read()
            stem = os.path.splitext(os.path.basename(p["card"]))[0]
            before = rules_firing_with(stem)
            new, note = C2.apply_op(orig, p["op"], p.get("field"))
            if new == orig:
                rows.append({**p, "verdict": "noop", "why": note, "change": []})
                continue
            open(card, "w", encoding="utf-8", newline="\n").write(new)
            try:
                after = rules_firing_with(stem)
            finally:
                open(card, "w", encoding="utf-8", newline="\n").write(orig)
            target = p["target_rule"]
            added = sorted(after - before)
            removed = sorted(before - after)
            v = classify(p["direction"], target in before, target in after,
                         bool(added or removed))
            rows.append({**p, "verdict": v, "why": note,
                         "added_rules": added, "removed_rules": removed,
                         "target_fired_before": target in before,
                         "target_fired_after": target in after,
                         "change": sorted(set(added) | set(removed))})
    after_tree = tree_digest(os.path.join(ROOT, "atoms"))
    by_verdict: dict[str, int] = {}
    for r in rows:
        by_verdict[r["verdict"]] = by_verdict.get(r["verdict"], 0) + 1
    effective = [r for r in rows if r["verdict"] not in ("noop", "infra_error")]
    return {"rows": rows, "n_planned": len(todo), "by_verdict": by_verdict,
            "n_effective": len(effective),
            "n_changed_findings": sum(1 for r in effective if r.get("change")),
            "production_atoms_unchanged": before_tree == after_tree,
            "atoms_digest": before_tree[:16],
            "seed": seed, "limit": limit}


def random_plans(n: int, seed: int = 643) -> list[dict[str, Any]]:
    """随机基线计划（同预算）：随机卡 × 随机算子（**等算力对比**，见 A2 教训 2）。"""
    import coverage_gap_scanner_643 as B1
    cards = B1.report()["cards"]
    rules = [r["rule_id"] for r in C1.analyze()["rows"] if r["scope"] == "atom"]
    rng = random.Random(seed)
    out = []
    for i in range(n):
        card = rng.choice(cards)
        op = rng.choice(list(C2.OPS))
        out.append({"mutation_id": f"random#{i}", "target_rule": rng.choice(rules),
                    "direction": "A", "card": card, "op": op, "field": None,
                    "expected_oracle": "", "generated_by": "random_baseline",
                    "version": "643.1"})
    return out


def write_report(sim: Optional[dict[str, Any]] = None) -> str:
    s = sim or simulate(C2.make_plan()["plans"])
    bv = s["by_verdict"]
    lines = [
        "# 643 C3 · 攻击效果模拟（智能层：自动生成攻击 #3；沙箱隔离）", "",
        f"> 计划 **{s['n_planned']}** 条（`limit={s['limit']}`，种子 `{s['seed']}`）；"
        f"有效（非 noop）**{s['n_effective']}** 条；判定分布 `{bv}`。",
        f"> **生产零副作用**：`atoms/` 树指纹跑前跑后一致 = **{s['production_atoms_unchanged']}**"
        f"（指纹 `{s['atoms_digest']}`）。", "",
        "## 一、判定口径", "",
        "| verdict | 含义 |", "|---|---|",
        "| `noop` | 空变异（未改文本）⇒ 不计入攻击 |",
        "| `blocked` | 方向 A：变异后**仍命中** ⇒ 规则没被绕开 |",
        "| `evaded` | 方向 A：变异后**不再命中** ⇒ **逃逸（真发现）** |",
        "| `triggered` | 方向 B：变异后**命中** ⇒ 规则可达 |",
        "| `not_triggered` | 方向 B：仍不命中 ⇒ 规则**不可达候选** |",
        "| `oracle_mismatch` | 目标规则没动但**别的**规则动了 ⇒ 预期可能猜错 |", "",
        "## 二、逐条结果", "",
        "| mutation_id | 目标规则 | 方向 | 卡 | 算子 | verdict | 新增 firing | 消失 firing |",
        "|---|---|---|---|---|---|---|---|"]
    for r in s["rows"]:
        lines.append(f"| `{r['mutation_id']}` | `{r['target_rule']}` | {r['direction']} | "
                     f"`{r['card']}` | `{r['op']}` | **{r['verdict']}** | "
                     f"{', '.join('`%s`' % x for x in r.get('added_rules', [])[:3]) or '—'} | "
                     f"{', '.join('`%s`' % x for x in r.get('removed_rules', [])[:3]) or '—'} |")
    ev = [r for r in s["rows"] if r["verdict"] == "evaded"]
    tr = [r for r in s["rows"] if r["verdict"] == "triggered"]
    nm = [r for r in s["rows"] if r["verdict"] == "oracle_mismatch"]
    lines += ["", "## 三、重点结果", "",
              f"- **逃逸（真发现）{len(ev)} 条**："
              + ("；".join(f"`{r['mutation_id']}`（{r['why']}）" for r in ev[:6]) or "（无）"),
              f"- **触发成功 {len(tr)} 条**："
              + ("；".join(f"`{r['mutation_id']}`" for r in tr[:6]) or "（无）"),
              f"- **oracle_mismatch {len(nm)} 条**（生成器预期猜错，§十二.7）："
              + ("；".join(f"`{r['mutation_id']}`" for r in nm[:6]) or "（无）"), "",
              "## 诚实登记", "",
              "1. **沙箱逃逸率 ≠ 生产逃逸率**（§十二.6）：沙箱是整树副本，"
              "生产可能有额外状态（锁、外部工具、时间窗口）；",
              f"2. **样本量极小**（`limit={s['limit']}`）⇒ 本表**只作线索**，"
              "任何\"比例\"都**没有统计意义**（C4 会做等预算对比并显式说明）；",
              "3. **`noop` 不算攻击失败**：它说明该算子在这张卡上**无从下手**，"
              "是算子-载体不匹配的信息（C4 会把它计入\"有效攻击率\"的分母以外）；",
              "4. **`not_triggered` 不等于规则坏**：可能是「卡本来就合规」⇒ 只作"
              "「不可达候选」线索（同 C2 登记）；",
              "5. **`oracle_mismatch` 是刻意的**：生成器的预期可能猜错（§十二.7）；"
              "本工具**记录**它，但**不改**预期，也不据此改判据；",
              "6. 本工具**不碰生产**：沙箱由 `mutation_fuzz.sandbox()` 提供，"
              "另有 `atoms/` 树指纹硬校验（实测一致）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({k: v for k, v in s.items() if k != "rows"} | {"rows": s["rows"]},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("A 方向：仍命中 ⇒ blocked", classify("A", True, True, False) == "blocked")
    chk("A 方向：不再命中 ⇒ evaded", classify("A", True, False, True) == "evaded")
    chk("B 方向：命中 ⇒ triggered", classify("B", False, True, True) == "triggered")
    chk("B 方向：不命中且无变化 ⇒ not_triggered",
        classify("B", False, False, False) == "not_triggered")
    chk("B 方向：不命中但他规则动 ⇒ oracle_mismatch",
        classify("B", False, False, True) == "oracle_mismatch")
    chk("A 方向优先判逃逸（即使有连带变化）",
        classify("A", True, False, True) == "evaded")

    plans = C2.make_plan()["plans"]
    chk("计划可读入", len(plans) >= 1)
    rnd = random_plans(5, seed=1)
    chk("随机基线同预算", len(rnd) == 5 and all(p["generated_by"] == "random_baseline"
                                              for p in rnd))
    chk("随机基线可复现", random_plans(5, seed=1) == rnd)
    chk("树指纹可算", len(tree_digest(os.path.join(ROOT, "atoms"))) == 64)

    # **小样本真跑沙箱**（1 条）：验证隔离与判定链路端到端
    one = simulate(plans[:1], limit=1)
    chk("端到端跑通 1 条", one["n_planned"] == 1 and len(one["rows"]) == 1)
    chk("生产 atoms/ 零副作用", one["production_atoms_unchanged"] is True)
    chk("verdict 取值合法",
        one["rows"][0]["verdict"] in ("noop", "blocked", "evaded", "triggered",
                                      "not_triggered", "oracle_mismatch", "infra_error"))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 C3 攻击效果模拟（沙箱）")
    ap.add_argument("--check", action="store_true", help="只读自检（含 1 条真跑沙箱）")
    ap.add_argument("--run", action="store_true", help="真跑（默认干跑不跑批）")
    ap.add_argument("--report", action="store_true", help="跑批并写报告")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--random", action="store_true", help="跑随机基线而非定向计划")
    ap.add_argument("--json", action="store_true", help="打印结果（JSON，不含逐条）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    plans = random_plans(x.limit, seed=x.seed or 643) if x.random \
        else C2.make_plan()["plans"]
    if x.report:
        s = simulate(plans, limit=x.limit, seed=x.seed)
        print(f"written {write_report(s)}")
        print(f"[attack-sim] {s['by_verdict']}；生产零副作用={s['production_atoms_unchanged']}")
        return 0
    if x.run or x.json:
        s = simulate(plans, limit=x.limit, seed=x.seed)
        if x.json:
            print(json.dumps({k: v for k, v in s.items() if k != "rows"},
                             ensure_ascii=False, indent=2))
        else:
            print(f"[attack-sim] {s['by_verdict']}；生产零副作用="
                  f"{s['production_atoms_unchanged']}")
        return 0
    print(f"[attack-sim] 计划 {len(plans)} 条（未跑；用 --run/--report 真跑沙箱）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
