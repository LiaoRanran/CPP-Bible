"""609 E4 · M6 算子优化 **方案**（**只给方案 + 测算，绝不落地**）。

609 铁律第 10 条：改 `mutation_fuzz.py` = 改判决口径 ⇒ **需监工单独授权**。
本工具被严格限制在：
  ① 读 v7 基线，把 M6 现状**算清楚**（数字见下，全部来自基线，不猜）；
  ② 把 M6 的变异分成 **4 类有效变异**（留下）与 **4 类等价变异**（建议剔除）；
  ③ 估算剔除后的新分母（见下方口径声明）；
  ④ 明确写下"本方案**未落地**"、落地需要谁授权、会动到哪些已冻结数字。

v7 实测输入（`data/mutation/full_baseline_v7.json::by_operator.M6`）：
    M6: judged **716** · blocked 716 · escaped 0 · n_a 0 · equivalent_invalid **8**
    M6 严格拦截率 379/716 = 0.52933（C-P95 [0.492014, 0.566403]）—— 明显低于其他算子，
    这是"被琐碎/等价变异稀释"的**最直接的实测征兆**。

> ⚠️ **口径纠正（承接任务0）**：任务书写"M6 可判分母 332 ⇒ ~323"，但 v7 基线实测 M6 可判是
> **716**（n_a=0，且全批 8 条等价变异**全部**来自 M6 —— `equivalent=equivalent_invalid=8`）。
> 本工具一律用**实测值**，不用任务书的占位数字。

分母口径声明（**诚实的关键**）：716 ⇒ 708 是"从 M6 可判样本里剔除已实测到的 8 条等价类"的
**算术结果**，不是实测值；4 类等价变异还可能覆盖更多未识别样本（**上限未知**，
不跑重冻结就算不出来）。真正落地要重跑 mutation 重冻结 —— 本批**不做**
（改算子=改口径，需授权；做了也不是改小数，是重算基线）。

CLI：
    plan       0 ok（打印 4+4 分类 + 分母测算）
    report     0 ok（写 Markdown 方案）
    --check    0 基线可读且 M6 数字自洽 / 1 破
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_BASELINE = ROOT / "data" / "mutation" / "full_baseline_v7.json"
REPORT_OUT = ROOT / "data" / "mutation_m6_plan.md"

#: 4 类**有效变异**（留下：语义真的变了 ⇒ 检测力有抓手）
EFFECTIVE_CLASSES = (
    ("E1", "删内存序/原子性/volatile 修饰", "改变可见性与顺序语义 ⇒ 编译或运行时可观察"),
    ("E2", "改函数返回值（nullptr / -1 / false）", "改变控制流与返回值 ⇒ 断言可捕"),
    ("E3", "重排初始化/释放顺序", "改变先后次序 ⇒ UB/泄漏可捕"),
    ("E4", "同类型变量替换 / 删除空指针检查", "改变数据流 ⇒ 静态分析与用例可捕"),
)

#: 4 类**等价变异**（建议剔除：换了等于没换 ⇒ 只会稀释分母、拉低拦截率）
EQUIVALENT_CLASSES = (
    ("Q1", "只改注释/文档串", "不产生任何可执行语义差异 ⇒ 编译产物一致"),
    ("Q2", "空白字符/换行/分号位置调整", "语法等价 ⇒ 编译产物一致"),
    ("Q3", "给已初始化变量追加同值再赋值", "数据流不变 ⇒ 编译产物可优化成同一份"),
    ("Q4", "把 if(x) return x; 拆成等价早返回", "控制流等价 ⇒ 编译器归一化后一致"),
)

#: 已在 v7 里被识别并排除的 M6 等价变异数（**实测值**：全批 equivalent=8 全部来自 M6，
#: 见 `by_operator.M6.equivalent_invalid`）。用它当"下界"：剔除至少这么多；
#: 4 类划分还会覆盖多少**未知**，不重冻结就算不出来 ⇒ 报告里明写下界 + 未知上限。
EST_EQUIVALENT_IN_M6 = 8


def load_baseline(path: Path | str = DEFAULT_BASELINE) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[m6] 基线不存在：{p}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"[m6] 基线不是合法 JSON：{exc}") from exc


def m6_stats(doc: dict) -> dict:
    m6 = doc.get("by_operator", {}).get("M6", {})
    judged = int(m6.get("blocked", 0)) + int(m6.get("escaped", 0))
    return {"judged": judged, "blocked": int(m6.get("blocked", 0)),
            "escaped": int(m6.get("escaped", 0)), "n_a": int(m6.get("n_a", 0)),
            "equivalent_invalid": int(m6.get("equivalent_invalid", 0)),
            "variants": doc.get("variants"), "blocked_all": doc.get("blocked"),
            "escaped_all": doc.get("escaped"), "equivalent_all": doc.get("equivalent"),
            "strict_blocked": doc.get("strict_blocked")}


def plan(s: dict) -> dict:
    judged = s["judged"]
    new_judged = max(judged - EST_EQUIVALENT_IN_M6, 0)
    return {"m6": s, "keep_classes": [{"id": i, "name": n, "why": w}
                                      for i, n, w in EFFECTIVE_CLASSES],
            "drop_classes": [{"id": i, "name": n, "why": w}
                             for i, n, w in EQUIVALENT_CLASSES],
            "judged_before": judged, "judged_after_est": new_judged,
            "delta": judged - new_judged,
            "est_note": f"剔除 {EST_EQUIVALENT_IN_M6} 条等价类样本（占 M6 可判 "
                        f"{s['judged']} 条的 {EST_EQUIVALENT_IN_M6 / max(judged, 1):.1%}）"
                        f" ⇒ M6 可判分母 {judged} ⇒ {new_judged}",
            "landed": False,
            "authority": "**未落地**：改 mutation_fuzz.M6 属于改判决口径，"
                         "需监工单独授权后由下一批重跑 mutation 重冻结（本批不跑、不改）"}


def render_report(doc: dict) -> str:
    s = m6_stats(doc)
    p = plan(s)
    lines = [
        "# M6 算子优化方案（609 E4 · **只做方案，未落地**）",
        "",
        "## 一、M6 现状（数字全部来自 v7 基线）",
        "",
        f"- M6 可判 **{s['judged']}** · blocked {s['blocked']} · escaped {s['escaped']}"
        f" · n_a {s['n_a']} · equivalent_invalid {s['equivalent_invalid']}",
        f"- 全批对照：variants {s['variants']} · blocked {s['blocked_all']}"
        f" · escaped {s['escaped_all']} · equivalent {s['equivalent_all']}"
        f" · strict_blocked {s['strict_blocked']}",
        "",
        "## 二、4 类有效变异（**保留**）",
        "",
    ]
    for i, n, w in EFFECTIVE_CLASSES:
        lines.append(f"- **{i}** {n} —— {w}")
    lines += ["", "## 三、4 类等价变异（**建议剔除**）", ""]
    for i, n, w in EQUIVALENT_CLASSES:
        lines.append(f"- **{i}** {n} —— {w}")
    lines += [
        "",
        "## 四、分母测算（**测算，不是实测**）",
        "",
        f"- {p['est_note']}",
        "- 口径：所谓 `716 ⇒ 708` 就是上面这条算术；真实值只能靠重冻结实测出来，",
        "  本批既不跑全量 mutation 也不改 `mutation_fuzz.py`。",
        "",
        "## 五、落地授权（**本批不做**）",
        "",
        f"- {p['authority']}",
        "- 落地会动到：严格拦截率分母、`strict_blocked`、等价类计数、"
        "`data/mutation/full_baseline_v*.json` 的版本号 ⇒ 属于监工/下一批的事。",
        "",
    ]
    return "\n".join(lines) + "\n"


def check(path: Path | str = DEFAULT_BASELINE) -> list[str]:
    problems: list[str] = []
    if not Path(path).is_file():
        return [f"基线不存在：{path}"]
    try:
        doc = load_baseline(path)
    except SystemExit as exc:
        return [str(exc)]
    s = m6_stats(doc)
    if s["judged"] != 716:
        problems.append(f"M6 可判不是 716（= {s['judged']}）⇒ 方案前提变了，须重算")
    if s["escaped"] != 0:
        problems.append(f"M6 escaped 不是 0（= {s['escaped']}）⇒ 逃逸口径变了")
    if s["n_a"] != 0:
        problems.append(f"M6 n_a 不是 0（= {s['n_a']}）⇒ 分母口径变了")
    if s["equivalent_invalid"] != 8:
        problems.append(f"M6 equivalent_invalid 不是 8（= {s['equivalent_invalid']}）"
                        f" ⇒ 等价类基线变了")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="mutation_m6_optimizer",
                                 description="609 E4 M6 算子优化方案（只做方案，不落地）")
    ap.add_argument("--version", action="version", version=f"mutation_m6_optimizer {VERSION}")
    ap.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true", help="落盘 Markdown 方案")
    ap.add_argument("--out", default=str(REPORT_OUT))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.baseline)
        if problems:
            print(f"[m6] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[m6] --check OK：v7 基线里 M6 可判 716 / escaped 0 / n_a 0 / "
              "equivalent_invalid 8 ⇒ 方案前提自洽")
        return 0

    doc = load_baseline(a.baseline)
    p = plan(m6_stats(doc))
    if a.write:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_report(doc), encoding="utf-8", newline="\n")
        print(f"[m6] 已写 {out.relative_to(ROOT).as_posix()}（方案，未落地）")
        return 0
    if a.json:
        print(json.dumps(p, ensure_ascii=False, indent=1))
        return 0
    print(f"[m6] M6 可判 {p['judged_before']} ⇒ 剔除等价类后约 {p['judged_after_est']}"
          f"（delta {p['delta']}，**测算非实测**）")
    for c in p["drop_classes"]:
        print(f"  剔除 {c['id']}：{c['name']}")
    for c in p["keep_classes"]:
        print(f"  保留 {c['id']}：{c['name']}")
    print(f"[m6] {p['authority']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
