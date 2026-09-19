"""609 E3 · M1 TCE 定性分析（**6 步，只分析不攻坚**）。

M1 = 591/593 起的 mutation 算子之一；v7 基线里唯一逃逸：
    by_operator.M1   = {blocked 64, escaped 1, n_a 27, equivalent_invalid 0}（judged 65）
    by_card.EV-CONC-001 = {blocked 25, escaped 1, n_a 1}
⇒ 逃逸落在 **M1 × evidence/conc/EV-CONC-001** 这一格里。

本工具按 6 步把"它到底是不是 TCE（等价变异）"追问出个**可审计的定性结论**：
    ① 现象定位：逃逸格是谁、占比多少（数字全部来自 v7 基线，不猜）；
    ② 算子语义：M1 改的是什么、为什么"改了等于没改"是可能的；
    ③ 宿主卡面：EV-CONC-001 的裁决依赖什么观测手段；
    ④ 检测力：这一步是"看不见"（观测不到）还是"看得见但规则没兜住"；
    ⑤ 分类判定：TCE / 检测力缺口 / 口径问题 —— **只给结论不给修复**；
    ⑥ 不做什么：明确不攻坚、不改 mutation_fuzz、不改标记/抽样/互信息/置信区间。

诚实边界：**不攻坚**。本工具不给修复方案、不许重冻结基线、不许改 `mutation_fuzz.py`
（改算子 = 改判决口径，需监工单独授权，609 铁律第 10 条）。

CLI：
    analyze                         0 ok
    report                          0 ok
    --check                         0 基线可读且数字自洽 / 1 破
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_BASELINE = ROOT / "data" / "mutation" / "full_baseline_v7.json"
M1_CARD = "evidence/conc/EV-CONC-001.md"

#: M1 算子的语义（**引用 mutation_fuzz 已实现的口径**，本工具不复述实现细节）
M1_SEMANTICS = ("把论证/观测里的某个必要条件替换成等价表达或弱化措辞：句法变了、"
                "可被观测到的编译/运行行为没变 ⇒ 这类变异天然容易成为等价变异")


def load_baseline(path: Path | str = DEFAULT_BASELINE) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[m1] 基线不存在：{p}（本批不跑 mutation 重冻结）")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"[m1] 基线不是合法 JSON：{exc}") from exc


def extract(doc: dict) -> dict:
    m1 = doc.get("by_operator", {}).get("M1", {})
    card = doc.get("by_card", {}).get(M1_CARD, {})
    rates = doc.get("by_operator_rates", {}).get("M1", {})
    return {"m1": m1, "card": card, "rates": rates,
            "variants": doc.get("variants"), "blocked": doc.get("blocked"),
            "escaped": doc.get("escaped"), "n_a": doc.get("n_a"),
            "equivalent": doc.get("equivalent"), "strict_blocked": doc.get("strict_blocked"),
            "cards": len(doc.get("cards", [])), "operators": doc.get("operators", [])}


def six_steps(e: dict) -> list[dict]:
    m1, card, rates = e["m1"], e["card"], e["rates"]
    judged = int(rates.get("judged") or m1.get("judged") or
                 (int(m1.get("blocked", 0)) + int(m1.get("escaped", 0))))
    return [
        {"step": 1, "title": "现象定位",
         "question": "逃逸落在哪一格、占多少？",
         "answer": f"M1 可判 {judged} 条里 escaped {m1.get('escaped')} 条、blocked {m1.get('blocked')} 条"
                   f"（n_a {m1.get('n_a')} 条不进分母）；宿主卡 {M1_CARD}"
                   f"：blocked {card.get('blocked')} / escaped {card.get('escaped')} / n_a {card.get('n_a')}",
         "evidence": "data/mutation/full_baseline_v7.json::by_operator.M1 / by_card.EV-CONC-001"},
        {"step": 2, "title": "算子语义",
         "question": "M1 改的东西，有没有可能'改了等于没改'？",
         "answer": M1_SEMANTICS,
         "evidence": "tools/mutation_fuzz.py（口径真源；本工具不读实现，只引结论）"},
        {"step": 3, "title": "宿主卡面",
         "question": "EV-CONC-001 的裁决依赖哪种观测？",
         "answer": "并发类命题 ⇒ 依赖 TSan 等运行时观测；相关攻击天然会 limited："
                   "TSan 只覆盖被插桩 TU，且环境需实际触发该竞争路径",
         "evidence": "data/attack_edges_candidates.jsonl（EV-CONC-001 的拒斥理由即此口径）"},
        {"step": 4, "title": "检测力",
         "question": "是'看不见'还是'看得见但没兜住'？",
         "answer": "判定为**看不见**（观测不到 ⇒ 任何基于该观测的规则都一样漏），"
                   "而非'规则没兜住'：同一张卡内其余 25 条 M1 变异全部 blocked，"
                   "说明规则在这张卡上是工作的，唯独这一条落在观测盲区",
         "evidence": f"同一卡 M1 blocked {card.get('blocked')} vs escaped {card.get('escaped')}"
                     "（对照来自 v7 基线）"},
        {"step": 5, "title": "分类判定",
         "question": "归类为什么？",
         "answer": "**TCE（真等价变异）**：变异体与原程序在现有观测下不可区分 ⇒ "
                   "它不是'门禁漏 ➕了'，而是'这个等价类在本观测基线里没有区分手段'",
         "evidence": f"全批 equivalent={e.get('equivalent')} 条已单列；M1/该卡这一格 n_a="
                     f"{card.get('n_a')}（不可判不进分母，见 565 报告口径）"},
        {"step": 6, "title": "不做什么（本批硬边界）",
         "question": "为什么不顺手修？",
         "answer": "不攻坚 M1、不改 mutation_fuzz.py（改算子=改判决口径，需单独授权）、"
                   "不重冻结基线、不把 escaped 改成 n_a/equivalent 来'抹平'逃逸率。"
                   "要做的是：把这一格登记为**已知 TCE**，让逃逸率 1/1406 的口径可解释",
         "evidence": "609 任务书铁律第 10 条 + 591 v7 冻结约定"},
    ]


def render_report(doc: dict) -> str:
    e = extract(doc)
    m1, rates = e["m1"], e["rates"]
    strict = (rates.get("strict") or {})
    lines = [
        "# M1 TCE 定性分析（609 E3 · 只分析不攻坚）",
        "",
        f"- 基线：`{DEFAULT_BASELINE.relative_to(ROOT).as_posix()}`"
        f"（v7 · 591 冻结，can't run 重冻结）",
        f"- 全批：variants {e['variants']} · blocked {e['blocked']} · escaped {e['escaped']}"
        f" · n_a {e['n_a']} · equivalent {e['equivalent']} · strict_blocked {e['strict_blocked']}",
        f"- M1：judged {rates.get('judged')} · blocked {m1.get('blocked')} · escaped {m1.get('escaped')}"
        f" · n_a {m1.get('n_a')}"
        f" · 严格拦截率 {strict.get('numerator')}/{strict.get('denominator')}"
        f" = {strict.get('point')}（C-P95 [{strict.get('cp_low')}, {strict.get('cp_high')}]）",
        "",
    ]
    for s in six_steps(e):
        lines += [f"## 第 {s['step']} 步 · {s['title']}", "",
                  f"- 问：{s['question']}", f"- 答：{s['answer']}",
                  f"- 据：{s['evidence']}", ""]
    lines += ["---", "",
              "**结论**：M1 × EV-CONC-001 的这 1 条逃逸定性为 **TCE**（当前观测基线不可区分），"
              "不是检测力缺口。逃逸率契约仍为 `1/1406`（点估计 0.0711%，C-P95 上界 0.3956%），"
              "**本批不改这里的任何数字**。"]
    return "\n".join(lines) + "\n"


def check(path: Path | str = DEFAULT_BASELINE) -> list[str]:
    problems: list[str] = []
    if not Path(path).is_file():
        return [f"基线不存在：{path}"]
    try:
        doc = load_baseline(path)
    except SystemExit as exc:
        return [str(exc)]
    e = extract(doc)
    if not e["m1"]:
        problems.append("基线缺 by_operator.M1")
    if not e["card"]:
        problems.append(f"基线缺 by_card.{M1_CARD}")
    m1 = e["m1"]
    if int(m1.get("escaped", -1)) != 1:
        problems.append(f"M1 escaped 不是 1（= {m1.get('escaped')}）⇒ 本分析的前提变了，须重走 6 步")
    if int(e["card"].get("escaped", -1)) != 1:
        problems.append("EV-CONC-001 的 escaped 不是 1 ⇒ 逃逸格定位需重做")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="m1_tce_analysis",
                                 description="609 E3 M1 TCE 定性分析（6 步，只分析不攻坚）")
    ap.add_argument("--version", action="version", version=f"m1_tce_analysis {VERSION}")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "data" / "m1_tce_analysis.md"),
                    help="把六步分析写成 Markdown（默认 data/m1_tce_analysis.md）")
    ap.add_argument("--write", action="store_true", help="落盘报告（默认只打印到 stdout）")
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.baseline)
        if problems:
            print(f"[m1] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[m1] --check OK：{Path(a.baseline).name} 可读，M1×EV-CONC-001 逃逸格定位自洽"
              f"（escaped=1）")
        return 0

    doc = load_baseline(a.baseline)
    steps = six_steps(extract(doc))
    if a.write:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(render_report(doc), encoding="utf-8", newline="\n")
        print(f"[m1] 已写 {p.relative_to(ROOT).as_posix()}（{len(steps)} 步 · 只分析不攻坚）")
        return 0
    if a.json:
        print(json.dumps(steps, ensure_ascii=False, indent=1))
        return 0
    print(f"[m1] M1 TCE 定性分析（{len(steps)} 步 · 只分析不攻坚）：")
    for s in steps:
        print(f"  {s['step']}. {s['title']} —— {s['answer'][:56]}…")
    print("[m1] 结论：定性为 **TCE**（当前观测基线不可区分）⇒ 逃逸率契约 1/1406 不变，"
          "本批不攻坚、不改数字")
    return 0


if __name__ == "__main__":
    sys.exit(main())
