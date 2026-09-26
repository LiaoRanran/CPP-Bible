"""643 D4 · **规则草案反涟漪测试**（智能层：自动提案规则 #4）。

**定位**：对 D3 未冗余的草案做**涟漪范围评估**（640c 方法论：改一处看会不会批量红），
输出 `安全 / 有涟漪 / 危险 / 数据不足`。

**⚠️ 本批的实现边界（必须先读）**：
真正的反涟漪需要把草案**注入沙箱里的 `gate_engine.py` 副本**再跑一遍全量 gate。
本批**没有**这么做，原因是**硬的**：
1. `gate_engine.py` 是 5 个 CORE_TOOLS 之一，**受完整性台账约束**（改副本也要保证
   `tool_integrity` 的信任根不被污染）；
2. 在**同进程**里"注入规则定义再回滚"需要改**已导入模块**的 `RULES` 列表，
   会与 `ge._META_CACHE` 等进程级缓存交互，**风险不可控**（641 的 selftest 投影名假失败
   就是进程级全局状态的教训）；
3. ⇒ 本批改用**代理**：用 C3 **实测**的"同卡/同字段变异的 firing 影响面"当作涟漪估计，
   并**逐条标 `proxy: true`**；无实测证据 ⇒ `数据不足`（**不猜**）。

**等级判据（机械）**：`ripple = |added ∪ removed|`
`0 → 安全` · `1–3 → 有涟漪` · `>3 → 危险` · 无证据 → `数据不足`

**644 的正确做法（本工具给出路径）**：把草案写成**独立的规则模块**（不进 `gate_engine.py`），
在沙箱里用 `importlib` 加载并注册到沙箱内的 `ge.RULES`，跑完 **必须**校验
`ge.RULES` 长度与 `_META_CACHE` 已复原 —— 这套"注入-回滚"要单独设计并单测。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_draft_anti_ripple.md` + `.json`。
纯标准库；≥6 例单测。
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

import rule_draft_mdl_check_643 as D3  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_draft_anti_ripple.md")
OUT_JSON = os.path.join(ROOT, "data", "643_draft_anti_ripple.json")
SIM_JSON = os.path.join(ROOT, "data", "643_attack_sim.json")
RIPPLE_SAFE, RIPPLE_MILD, RIPPLE_DANGER = 0, 3, 3


def grade(ripple: Optional[int]) -> str:
    """涟漪等级（纯函数）。`None` = 无证据 ⇒ 数据不足。"""
    if ripple is None:
        return "数据不足"
    if ripple <= RIPPLE_SAFE:
        return "安全"
    if ripple <= RIPPLE_MILD:
        return "有涟漪"
    return "危险"


def evidence_index() -> dict[str, dict[str, Any]]:
    """C3 实测证据索引：`card` → 最大涟漪（added ∪ removed）。"""
    if not os.path.exists(SIM_JSON):
        return {}
    try:
        sim = json.loads(open(SIM_JSON, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return {}
    idx: dict[str, dict[str, Any]] = {}
    for r in sim.get("rows", []):
        card = str(r.get("card", ""))
        if not card or r.get("verdict") in ("noop", "infra_error"):
            continue
        footprint = len(set(r.get("added_rules", [])) | set(r.get("removed_rules", [])))
        cur = idx.get(card)
        if cur is None or footprint > cur["ripple"]:
            idx[card] = {"ripple": footprint, "mutation_id": r.get("mutation_id"),
                         "op": r.get("op"), "verdict": r.get("verdict")}
    return idx


def assess() -> dict[str, Any]:
    chk = D3.check()
    idx = evidence_index()
    rows = []
    for r in chk["rows"]:
        if r["redundant"]:
            rows.append({**r, "ripple": None, "ripple_grade": "跳过",
                         "proxy": False, "evidence": "D3 已判 REJECT_冗余 ⇒ 不进入反涟漪"})
            continue
        card = r.get("overlap_against", "")
        # NEW 草案的资源：provenance 里带 card；MODIFY 草案没有单卡 ⇒ 用规则级证据（暂缺）
        ev = None
        for c, d in idx.items():
            if c and c in card:
                ev = d
                break
        if ev is None:
            rows.append({**r, "ripple": None, "ripple_grade": "数据不足",
                         "proxy": True, "evidence": "C3 无同卡实测证据 ⇒ 不猜"})
            continue
        rows.append({**r, "ripple": ev["ripple"], "ripple_grade": grade(ev["ripple"]),
                     "proxy": True,
                     "evidence": f"C3 实测（`{ev['mutation_id']}`，op={ev['op']}，"
                                 f"verdict={ev['verdict']}）"})
    by_grade: dict[str, int] = {}
    for r in rows:
        by_grade[r["ripple_grade"]] = by_grade.get(r["ripple_grade"], 0) + 1
    return {"rows": rows, "n": len(rows), "by_grade": by_grade,
            "n_with_evidence": sum(1 for r in rows if r["ripple"] is not None),
            "n_proxy": sum(1 for r in rows if r["proxy"]),
            "sim_available": bool(idx),
            "injection_implemented": False,
            "safe_to_上线": [r["proposed_rule_id"] for r in rows
                             if r["ripple_grade"] == "安全"],
            "dangerous": [r["proposed_rule_id"] for r in rows
                          if r["ripple_grade"] == "危险"]}


def write_report() -> str:
    a = assess()
    lines = [
        "# 643 D4 · 规则草案反涟漪（智能层：自动提案规则 #4；**代理实现**）", "",
        f"> 草案 **{a['n']}** 条；等级分布 `{a['by_grade']}`；有实测证据 "
        f"**{a['n_with_evidence']}** 条（代理标记 {a['n_proxy']} 条）。",
        f"> C3 证据可用：**{a['sim_available']}**；**草案注入沙箱未实现**"
        f"（`injection_implemented={a['injection_implemented']}`）。", "",
        "## 一、逐条等级", "",
        "| 草案 | 形态 | 涟漪范围 | 等级 | 代理？ | 证据 |", "|---|---|---|---|---|---|"]
    for r in a["rows"]:
        lines.append(f"| `{r['proposed_rule_id']}` | {r['kind']} | "
                     f"{'—' if r['ripple'] is None else r['ripple']} | "
                     f"**{r['ripple_grade']}** | {'✅' if r['proxy'] else '—'} | "
                     f"{r['evidence']} |")
    lines += ["", "## 二、⚠️ 本批**没有**做真反涟漪（边界说明）", "",
              "真反涟漪需要把草案**注入沙箱里的 `gate_engine.py` 副本**再跑全量 gate。"
              "本批**未做**，原因是硬的：",
              "1. `gate_engine.py` 是 5 个 **CORE_TOOLS** 之一（受完整性台账约束）；",
              "2. 同进程「注入规则定义再回滚」要改**已导入模块**的 `RULES` 列表，"
              "会与 `_META_CACHE` 等**进程级缓存**交互 ⇒ 风险不可控"
              "（641 的 selftest 投影名假失败就是进程级全局状态的教训）；",
              "3. ⇒ 改用**代理**：C3 实测的「同卡/同字段变异的 firing 影响面」，逐条标 `proxy: true`；"
              "**无实测证据一律 `数据不足`，不猜**。", "",
              "## 三、644 的正确做法（本工具给出的路径）", "",
              "1. 草案写成**独立规则模块**（不进 `gate_engine.py`）；",
              "2. 用 `importlib` 在**沙箱**里加载，注册进沙箱内的 `ge.RULES`；",
              "3. 跑完全量 gate 后**必须校验**：`len(ge.RULES)` 复原、`_META_CACHE` 复原、"
              "`atoms/` 树指纹不变；",
              "4. 这套「注入-回滚」要**单独设计 + 单测**（含「注入失败也必须复原」的异常路径）。", "",
              "## 诚实登记", "",
              "1. **代理 ≠ 反涟漪**：代理只说明「**同类变异**在实测中影响了 N 条规则」，"
              "**不等于**「草案上线后会波及 N 张卡」；",
              f"2. **`数据不足` 占多数**（{a['by_grade'].get('数据不足', 0)}/{a['n']}）："
              "这是**实情**（C3 只跑 20 条、且按卡匹配）⇒ 本批**给不出**草案级反涟漪结论；",
              "3. **`危险` 判定基于 `>3` 条规则受影响**（本批经验阈值）⇒ 边界已在单测固定；",
              "4. **不能据此批准任何草案上线**（§十二.3）：本工具的输出只作"
              "**644 真反涟漪的输入与优先级**；",
              "5. 本工具**只读**：不改规则、不改沙箱机制、不写侧车。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("等级：0 ⇒ 安全", grade(0) == "安全")
    chk("等级：3 ⇒ 有涟漪（阈值内）", grade(3) == "有涟漪")
    chk("等级：4 ⇒ 危险", grade(4) == "危险")
    chk("等级：None ⇒ 数据不足（不猜）", grade(None) == "数据不足")
    chk("阈值常量在册", (RIPPLE_SAFE, RIPPLE_MILD) == (0, 3))

    a = assess()
    chk("逐条覆盖全部草案", a["n"] == len(a["rows"]) and a["n"] > 0)
    chk("等级分布自洽", sum(a["by_grade"].values()) == a["n"])
    chk("草案注入**未实现**（如实登记）", a["injection_implemented"] is False)
    chk("危险项不会同时出现在 safe 清单",
        not (set(a["dangerous"]) & set(a["safe_to_上线"])))
    chk("所有代理结论都标 proxy",
        all(r["proxy"] for r in a["rows"] if r["ripple_grade"] != "跳过"))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 D4 草案反涟漪（代理）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = assess()
    if x.json:
        print(json.dumps({"by_grade": a["by_grade"], "n": a["n"],
                          "injection_implemented": a["injection_implemented"],
                          "dangerous": a["dangerous"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"[anti-ripple] {a['n']} 草案 ⇒ {a['by_grade']}；危险 {len(a['dangerous'])}；"
          f"注入未实现（代理）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
