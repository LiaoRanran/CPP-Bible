"""643 B1 · **规则覆盖盲区扫描器**（智能层：自动发现问题 #1）。

**定位**：系统自己扫描"**67 条规则 × 卡片**的覆盖矩阵"，输出**盲区清单 + 热力图 + 优先级**，
不靠人喂问题，也**不做任何修复**。

**矩阵口径（机械可复算）**：`矩阵[rule][card] = 1 ⟺ 该规则在该卡上产生了 Finding`
（数据源 = `gate_engine.run(include_advice=True)` 的现算结果，**不是**历史快照）。

**四类盲区**（对应 inbox B1 的四个问题）：

| 判据 | 含义 | 优先级 |
|---|---|---|
| 卡**零规则命中** | 这张卡没有任何规则报过 ⇒ 检查盲区 | **P0** |
| `block` 级规则**零命中** | 重规则空转 ⇒ 要么规则死、要么卡全合规（需人判） | **P0** |
| 规则只命中 **1** 张卡 | 过拟合候选（规则写死到某张卡） | P1 |
| 卡被 **>10** 条规则命中 | 冗余候选（同一张卡被反复报，噪声放大） | P2 |

**诚实边界**：
- 卡口径 = `atoms/**/ATOM-*.md` = **27 张**；而 638 census 的"28 张"是 `atoms/**/*.md`
  （多一个 `atoms/README.md`）⇒ **口径差异已登记**，本工具以"可被规则检查的 ATOM 卡"为准。
- 矩阵只反映**当前仓库状态**：干净仓库里"少命中"是正常的，**不等于**规则没用
  （规则的判别力要靠 622/623 的变异跑批体现）⇒ 本清单是**线索**，需人复核（§十二.1）。
- `warn/advice` 规则同样计入矩阵（否则会误判为"零命中"）。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_coverage_gap.md` + `.json`。
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

import gate_engine as ge  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_coverage_gap.md")
OUT_JSON = os.path.join(ROOT, "data", "643_coverage_gap.json")
OVER_HIT = 10          # 卡被 >10 条规则命中 ⇒ 冗余候选
SINGLE_HIT = 1         # 规则只命中 1 张卡 ⇒ 过拟合候选


def cards() -> list[str]:
    """卡片全集（ROOT 相对路径，`/` 分隔）。"""
    out = []
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        rel = os.path.relpath(str(p), str(ge.ROOT)).replace(os.sep, "/")
        out.append(rel)
    return sorted(out)


def rules() -> list[dict[str, str]]:
    return [{"id": r.id, "title": r.title, "severity": r.severity,
             "scope": r.scope, "kind": r.kind} for r in ge.RULES]


def live_findings() -> list[dict[str, str]]:
    """现算 67 条规则的判决结果（**只读**：`ge.run` 不改任何文件）。"""
    return [{"rule_id": f.rule_id, "target": f.target.replace(os.sep, "/"),
             "severity": f.severity} for f in ge.run(include_advice=True)]


def build_matrix(finds: list[dict[str, str]], card_list: list[str],
                 rule_list: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    """`matrix[rule_id][card] = 命中次数`（只统计 target 落在 card_list 上的）。"""
    cs = set(card_list)
    m: dict[str, dict[str, int]] = {r["id"]: {} for r in rule_list}
    for f in finds:
        if f["rule_id"] in m and f["target"] in cs:
            m[f["rule_id"]][f["target"]] = m[f["rule_id"]].get(f["target"], 0) + 1
    return m


def analyze(m: dict[str, dict[str, int]],
            rule_list: list[dict[str, str]],
            card_list: list[str]) -> dict[str, Any]:
    """四类盲区 + 优先级（纯函数，可用合成矩阵测试）。"""
    sev = {r["id"]: r["severity"] for r in rule_list}
    card_hits: dict[str, int] = {c: 0 for c in card_list}
    for rid, row in m.items():
        for c in row:
            card_hits[c] = card_hits.get(c, 0) + 1

    cards_no_hit = sorted(c for c, n in card_hits.items() if n == 0)
    never = sorted(rid for rid, row in m.items() if not row)
    block_never = sorted(rid for rid in never if sev.get(rid) == "block")
    single = sorted(rid for rid, row in m.items() if len(row) == SINGLE_HIT)
    over = sorted(c for c, n in card_hits.items() if n > OVER_HIT)

    priorities = []
    for c in cards_no_hit:
        priorities.append({"level": "P0", "kind": "card_no_rule_hit", "target": c,
                           "why": "该卡没有任何规则命中 ⇒ 检查盲区（可能是卡太干净，也可能是规则漏）"})
    for rid in block_never:
        priorities.append({"level": "P0", "kind": "block_rule_zero_hit", "target": rid,
                           "why": "block 级规则零命中 ⇒ 规则空转或卡全合规，需人判"})
    for rid in single:
        priorities.append({"level": "P1", "kind": "rule_single_card", "target": rid,
                           "why": "只命中 1 张卡 ⇒ 过拟合候选（规则可能写死到该卡）"})
    for c in over:
        priorities.append({"level": "P2", "kind": "card_over_hit", "target": c,
                           "why": f"被 >{OVER_HIT} 条规则命中 ⇒ 冗余候选（噪声放大）"})
    return {
        "n_rules": len(rule_list), "n_cards": len(card_list),
        "cards_no_rule_hit": cards_no_hit,
        "rules_never_hit": never,
        "block_rules_zero_hit": block_never,
        "rules_single_card": single,
        "cards_over_10_rules": over,
        "card_hit_counts": card_hits,
        "rule_hit_counts": {rid: len(row) for rid, row in m.items()},
        "priorities": priorities,
        "by_level": {lv: sum(1 for p in priorities if p["level"] == lv)
                     for lv in ("P0", "P1", "P2")},
        "total_cells_hit": sum(len(row) for row in m.values()),
    }


def heatmap_text(m: dict[str, dict[str, int]], card_list: list[str]) -> str:
    """紧凑热力图：每条规则一行，卡片按列（`x`=命中 / `.`=未命中）。"""
    head = "| 规则 | " + " ".join(f"c{i:02d}" for i in range(len(card_list))) + " | 命中卡数 |"
    lines = [head, "|---|" + "---|" * (len(card_list) + 1)]
    for rid in sorted(m):
        cells = " ".join("x" if m[rid].get(c) else "." for c in card_list)
        lines.append(f"| `{rid}` | {cells} | {len(m[rid])} |")
    lines.append("")
    lines.append("列号 → 卡片：")
    for i, c in enumerate(card_list):
        lines.append(f"- `c{i:02d}` = `{c}`")
    return "\n".join(lines)


def report() -> dict[str, Any]:
    cl, rl = cards(), rules()
    fs = live_findings()
    m = build_matrix(fs, cl, rl)
    a = analyze(m, rl, cl)
    return {"matrix": m, "analysis": a, "cards": cl, "rules": rl,
            "n_findings": len(fs),
            "atom_targets": sorted({f["target"] for f in fs if f["target"].startswith("atoms/")})}


def write_report() -> str:
    r = report()
    a = r["analysis"]
    lines = [
        "# 643 B1 · 规则覆盖盲区扫描（智能层 #1：自动发现问题）", "",
        "> 矩阵口径：`矩阵[rule][card] = 1 ⟺ 该规则在该卡上产生 Finding`；",
        f"> 数据源 = `gate_engine.run(include_advice=True)` **现算**（{r['n_findings']} 条 Finding）。",
        f"> 规模：**{a['n_rules']} 条规则 × {a['n_cards']} 张 ATOM 卡**，命中单元 **{a['total_cells_hit']}** 个。", "",
        "## 一、盲区清单（四类）", "",
        "| 类别 | 条数 | 清单 |", "|---|---|---|",
        f"| **P0** 卡零规则命中 | {len(a['cards_no_rule_hit'])} | "
        f"{', '.join('`%s`' % x for x in a['cards_no_rule_hit']) or '（无）'} |",
        f"| **P0** block 规则零命中 | {len(a['block_rules_zero_hit'])} | "
        f"{', '.join('`%s`' % x for x in a['block_rules_zero_hit'][:20]) or '（无）'}"
        f"{' …' if len(a['block_rules_zero_hit']) > 20 else ''} |",
        f"| **P1** 规则只命中 1 张卡 | {len(a['rules_single_card'])} | "
        f"{', '.join('`%s`' % x for x in a['rules_single_card']) or '（无）'} |",
        f"| **P2** 卡被 >{OVER_HIT} 条规则命中 | {len(a['cards_over_10_rules'])} | "
        f"{', '.join('`%s`' % x for x in a['cards_over_10_rules']) or '（无）'} |", "",
        f"**优先级分布**：P0 {a['by_level']['P0']} / P1 {a['by_level']['P1']} / "
        f"P2 {a['by_level']['P2']}。", "",
        "### 1.1 全部零命中规则（{0} 条）".format(len(a["rules_never_hit"])), "",
        ", ".join("`%s`" % x for x in a["rules_never_hit"]) or "（无）", "",
        "## 二、热力图（规则 × 卡）", "",
        heatmap_text(r["matrix"], r["cards"]), "",
        "## 三、逐卡命中数", "",
        "| 卡 | 命中规则数 |", "|---|---|"]
    for c, n in sorted(a["card_hit_counts"].items(), key=lambda kv: (kv[1], kv[0])):
        lines.append(f"| `{c}` | {n} |")
    lines += ["", "## 四、优先级条目（逐条）", "",
              "| 级别 | 类别 | 对象 | 理由 |", "|---|---|---|---|"]
    for p in a["priorities"]:
        lines.append(f"| **{p['level']}** | `{p['kind']}` | `{p['target']}` | {p['why']} |")
    if not a["priorities"]:
        lines.append("| — | — | — | 零条目 |")
    lines += ["", "## 诚实登记", "",
              "1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：这是**启发式扫描**，"
              "清单是**线索**不是判决，需人复核；",
              f"2. **卡口径差异**：本工具用 `atoms/**/ATOM-*.md` = **{a['n_cards']} 张**；"
              "638 census 的\"28 张\"是 `atoms/**/*.md`（多 `atoms/README.md`）⇒ 口径不同已登记；",
              "3. **矩阵只反映当前仓库状态**：干净仓里\"零命中\"是正常的 —— 规则的判别力要看 "
              "622/623 的变异跑批（B2/B4 覆盖那一面），不能据此判规则无用；",
              "4. **`block` 零命中不必然是缺陷**：可能是卡全合规（好事），"
              "也可能是规则条件写死了（坏事）—— 工具**不给结论**，只列为 P0 线索；",
              "5. `advice`/`warn` 规则计入矩阵；若排除它们，\"零命中\"会虚增 —— 口径已固定为含全部 67 条。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"analysis": a, "n_findings": r["n_findings"], "cards": r["cards"],
                   "matrix": r["matrix"]}, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 合成矩阵（构造说明，便于复核）：
    #   R1 = block 且零命中；R2 = 只命中 card_b（单卡 ⇒ 过拟合候选）；
    #   R3 = 命中 card_b+card_d；R4..R15 = 各命中 card_b+card_d；
    #   card_a 零命中（盲区）；card_b/card_d 各被 >10 条命中（冗余候选）。
    rl = [{"id": f"R{i}", "title": "", "severity": "block" if i == 1 else "warn",
           "scope": "atom", "kind": "fact"} for i in range(1, 16)]
    cl = ["card_a", "card_b", "card_d"]
    m: dict[str, dict[str, int]] = {r["id"]: {} for r in rl}
    m["R2"]["card_b"] = 1
    m["R3"]["card_b"] = 1
    m["R3"]["card_d"] = 1
    for i in range(4, 16):
        m[f"R{i}"] = {"card_b": 1, "card_d": 1}
    a = analyze(m, rl, cl)
    chk("已知盲区必检出（card_a）", a["cards_no_rule_hit"] == ["card_a"],
        str(a["cards_no_rule_hit"]))
    chk("block 规则零命中必检出（R1）", a["block_rules_zero_hit"] == ["R1"],
        str(a["block_rules_zero_hit"]))
    chk("单卡命中规则必检出（R2）", a["rules_single_card"] == ["R2"],
        str(a["rules_single_card"]))
    chk("超阈值卡必检出（card_b/card_d）",
        a["cards_over_10_rules"] == ["card_b", "card_d"],
        str(a["cards_over_10_rules"]))
    chk("矩阵维度正确（规则数 × 卡数）",
        a["n_rules"] == 15 and a["n_cards"] == 3, f"{a['n_rules']}x{a['n_cards']}")
    full = analyze({r["id"]: {c: 1 for c in cl} for r in rl}, rl, cl)
    chk("全覆盖不报错（无零命中卡、无零命中规则）",
        full["cards_no_rule_hit"] == [] and full["rules_never_hit"] == [],
        f"{full['cards_no_rule_hit']} / {full['rules_never_hit']}")
    chk("优先级分级正确（P0=2 / P1=1 / P2=2）",
        a["by_level"]["P0"] == 2 and a["by_level"]["P1"] == 1
        and a["by_level"]["P2"] == 2, str(a["by_level"]))

    # 真实仓库：维度与只读性
    real = report()
    chk("真实矩阵 67 × 27", real["analysis"]["n_rules"] == 67
        and real["analysis"]["n_cards"] == 27,
        f"{real['analysis']['n_rules']}x{real['analysis']['n_cards']}")
    chk("findings 非空", real["n_findings"] > 0, str(real["n_findings"]))
    chk("热力图含全部规则", heatmap_text(real["matrix"], real["cards"]).count("| `") >= 67)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 B1 覆盖盲区扫描")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印分析（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    an = report()["analysis"]
    if a.json:
        print(json.dumps({k: an[k] for k in ("n_rules", "n_cards", "by_level",
                                             "cards_no_rule_hit", "block_rules_zero_hit")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[coverage-gap] {an['n_rules']} 规则 × {an['n_cards']} 卡 ⇒ P0 {an['by_level']['P0']} / "
          f"P1 {an['by_level']['P1']} / P2 {an['by_level']['P2']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
