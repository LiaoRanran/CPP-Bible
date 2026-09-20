#!/usr/bin/env python3
"""613 任务F1 · 逃逸率**诚实化**：同一份基线，把分母摊开算。

背景：本仓对外一直报「逃逸率契约 **1/1406**」。这个数字**依赖一组排除**——
`n_a`(179) / `equivalent`(8) / `out_of_scope`(69) 全都不进分母。
排除合理与否见仁见智，但**只报一个口径**会让读者误以为"真实逃逸率就是 0.07%"。

本工具把分母摊开，给出**同一份 v7 基线**下的多口径逃逸率，每个都给
**分子/分母 + 点估计 + 双侧 Wilson 95% CI**（565 口径纪律：比率必须带双侧区间）。

口径定义（按"最宽松 → 最保守"排列）：
  1. **官方契约**：escaped / 可判（blocked+escaped）            = 1 / 1406
  2. **+等价变异**：把 equivalent 也算未杀                       = (1+8) / 1414
  3. **+n_a**：把 n_a 也算未杀                                   = (1+179) / 1585
  4. **最保守上界**：escaped+n_a+equivalent 全算未杀             = (1+179+8) / 1593
  5. **strict 口径**：1 − strict_rate（严格块率下的未杀比例）

诚实要点（报告里明写）：
  * 唯一 escaped = **M1 / EV-CONC-001 / 删 negative_controls**，且是**冻结 TCE**
    ⇒ 它是"已知且被冻结的例外"，**不是新逃逸**；但它确实未被杀死，不能装作 0。
  * `equivalent_invalid = 8` 意味着**全部 8 个等价判定本身无效** ⇒
    把它们当"等价"而排除是**有争议**的，故口径 2/4 把它们算回未杀。
  * 官方口径与最保守上界差 **两个数量级**，引用时必须标清分母。

CLI：
  python tools/escape_rate_honest_613.py          # 生成 data/escape_rate_honest_613.md
  python tools/escape_rate_honest_613.py --check  # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "escape_rate_honest_613.md"
Z = 1.959963984540054  # 双侧 95%


def wilson(k: int, n: int, z: float = Z) -> tuple[float, float]:
    """双侧 Wilson 分数区间（小比例、小样本也比 Wald 稳）。"""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def latest_baseline() -> tuple[Path, dict]:
    files = sorted(glob.glob(str(ROOT / "data" / "mutation" / "full_baseline_v*.json")))
    if not files:
        raise SystemExit("[F1] 找不到 mutation 基线")
    p = Path(files[-1])
    return p, json.loads(p.read_text(encoding="utf-8"))


def rates(d: dict) -> list[dict]:
    blocked = int(d.get("blocked", 0))
    escaped = int(d.get("escaped", 0))
    n_a = int(d.get("n_a", 0))
    equiv = int(d.get("equivalent", 0))
    decidable = blocked + escaped
    # `results` 是**列表**（每条变体一条），不是计数 ⇒ 取 len（本批实踩）
    res = d.get("results", [])
    total = len(res) if isinstance(res, list) else int(res or 0)
    if not total:
        total = blocked + escaped + n_a + equiv
    strict_rate = float(d.get("strict_rate", 0.0))

    rows = [
        ("① 官方契约（可判分母）", escaped, decidable),
        ("② +等价变异（equivalent 算未杀）", escaped + equiv, decidable + equiv),
        ("③ +n_a（n_a 算未杀）", escaped + n_a, decidable + n_a),
        ("④ 最保守上界（n_a+equivalent 全算未杀）", escaped + n_a + equiv, total),
    ]
    out = []
    for name, k, n in rows:
        lo, hi = wilson(k, n)
        out.append({"name": name, "k": k, "n": n, "p": (k / n) if n else 0.0,
                    "lo": lo, "hi": hi})
    out.append({"name": "⑤ strict 口径（1 − strict_rate）", "k": None, "n": None,
                "p": 1 - strict_rate, "lo": None, "hi": None})
    return out


def render(p: Path, d: dict, rs: list[dict]) -> str:
    notes = d.get("notes", "")
    esc_list = d.get("escaped_list") or []
    L = ["# 613 · 逃逸率诚实化（F1）", "",
         f"> 生成：`python tools/escape_rate_honest_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 基线：`{p.relative_to(ROOT).as_posix()}`（frozen_at_commit `{d.get('frozen_at_commit')}`）",
         "> 纪律（565）：比率一律「分子/分母 + 点估计 + **双侧** Wilson 95% CI」。", "",
         "## 一、原始计数", "",
         "| 项 | 值 |", "|---|---|",
         f"| results（变体总数） | {len(d.get('results') or [])} |",
         f"| blocked | {d.get('blocked')} |",
         f"| escaped | **{d.get('escaped')}** |",
         f"| n_a（不适用） | {d.get('n_a')} |",
         f"| equivalent | {d.get('equivalent')} |",
         f"| equivalent_invalid | **{d.get('equivalent_invalid')}** |",
         f"| out_of_scope | {d.get('out_of_scope')} |",
         f"| strict_blocked / strict_rate | {d.get('strict_blocked')} / {d.get('strict_rate')} |",
         f"| treated_rate | {d.get('treated_rate')} |", "",
         "## 二、多口径逃逸率（分母摊开）", "",
         "| 口径 | 分子/分母 | 点估计 | 双侧 Wilson 95% CI |", "|---|---|---|---|"]
    for r in rs:
        if r["n"] is None:
            L.append(f"| {r['name']} | — | {r['p'] * 100:.2f}% | — |")
        else:
            L.append(f"| {r['name']} | **{r['k']}/{r['n']}** | {r['p'] * 100:.3f}% "
                     f"| [{r['lo'] * 100:.3f}%, {r['hi'] * 100:.3f}%] |")
    L += ["", "## 三、诚实披露（必读）", "",
          f"- 唯一 escaped 条目：{esc_list if esc_list else '（空）'}；"
          "基线 notes 记为**冻结 TCE** ⇒ 已知且冻结的例外，**不是新逃逸**，但它确实未被杀死。",
          f"- `equivalent_invalid = {d.get('equivalent_invalid')}` 与 `equivalent = {d.get('equivalent')}` "
          "**相等** ⇒ 全部等价判定本身无效；把它们当等价而排除**有争议**，故口径 ②④ 算回未杀。",
          "- 官方口径（①）与最保守上界（④）相差**两个数量级** ⇒ "
          "任何引用都必须标清分母，不得只报 1/1406。",
          f"- 基线 notes：{notes}", "",
          "> 本工具只读基线 JSON，**不跑 mutation、不改基线**（铁律：不跑全量 mutation）。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 F1 · 逃逸率诚实化")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    p, d = latest_baseline()
    rs = rates(d)

    if a.check:
        errs = []
        if int(d.get("escaped", -1)) != 1:
            errs.append(f"escaped 应为 1，实测 {d.get('escaped')}")
        if int(d.get("blocked", -1)) != 1405:
            errs.append(f"blocked 应为 1405，实测 {d.get('blocked')}")
        for r in rs:
            if r["n"] and not (0.0 <= r["lo"] <= r["p"] <= r["hi"] <= 1.0):
                errs.append(f"{r['name']} 区间不覆盖点估计")
        # Wilson 边界性质：k=0 ⇒ lo=0；k=n ⇒ hi=1
        lo, hi = wilson(0, 10)
        if lo != 0.0:
            errs.append("k=0 时下界应为 0")
        lo2, hi2 = wilson(10, 10)
        if abs(hi2 - 1.0) > 1e-9:
            errs.append("k=n 时上界应为 1")
        for e in errs:
            print(f"[F1] ✗ {e}")
        print("[F1] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(p, d, rs), encoding="utf-8", newline="\n")
    print(f"[F1] 写入 {OUT.relative_to(ROOT).as_posix()}（口径 {len(rs)} 个；"
          f"官方 {rs[0]['k']}/{rs[0]['n']} = {rs[0]['p'] * 100:.3f}%）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
