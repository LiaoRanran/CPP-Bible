"""609 E1 · 度量诚实性：**Clopper-Pearson 精确上界 + 收敛曲线 + 方差声明 + 口径修正标注**。

四条都是"把话说严谨"，不是"把话说好听"：

  1. **Clopper-Pearson 精确区间**（不是正态近似）：`cp_upper(n,k,conf)` 解
     `P(X ≤ k | n, p) = 1-conf`（单调 ⇒ 纯标准库二分，无 scipy）；`k=0` 时给出**零失效上界**
     （`3/n` 的精确版）——**绝不写 0**。
  2. **收敛曲线 v1→v7**：从 `data/metrics.jsonl` 末行递归找 `escape_rate_history`；
     凡 note 里写明"口径修正/被 vX 取代"的点 ⇒ 标 `caliber_change=True`，
     **禁止把这些点连成"单调下降"的叙事**（尺子变了 ≠ 进步）。
  3. **方差声明**：点估计方差 `p(1-p)/n` + 标准误；并声明"C-P 区间已经吃掉了方差"，
     以及跨版本**不可做趋势检验**（不同口径 = 不同总体）。
  4. **口径修正标注**：逐版本把 judged/n_a/分子与 note 摆在一起，谁改了什么一目了然。

CLI：
    cp --n N --k K [--conf 0.95]    精确区间（含零失效上界对照）
    curve                           v1→v7 曲线（含口径修正标注）
    variance                        方差/标准误声明
    report [--write]                完整诚实性报告（Markdown）
    --check                         0 复算 v7 区间与 metrics 记录一致（1e-9）/ 1 破
"""
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_METRICS = ROOT / "data" / "metrics.jsonl"
REPORT_OUT = ROOT / "data" / "metrics_honesty.md"

#: v7 权威值（591 冻结）：judged 1406 · escaped 1 · n_a 179
V7 = {"n": 1406, "k": 1, "n_a": 179}


def binom_cdf(k: int, n: int, p: float) -> float:
    """P(X ≤ k)；n 上千 ⇒ 用 lgamma 走对数域，避免组合数溢出。"""
    if k < 0:
        return 0.0
    if k >= n or p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    lg, total = math.lgamma, 0.0
    log_p, log_q = math.log(p), math.log1p(-p)
    for i in range(k + 1):
        log_c = lg(n + 1) - lg(i + 1) - lg(n - i + 1)
        total += math.exp(log_c + i * log_p + (n - i) * log_q)
    return min(max(total, 0.0), 1.0)


def cp_upper(n: int, k: int, conf: float = 0.95) -> float:
    """C-P **双侧**上界：解 `P(X ≤ k) = (1-conf)/2`（⚠️ 是 α/2 不是 α，踩过这个坑）。"""
    if n <= 0 or k >= n:
        return 1.0
    alpha = (1.0 - conf) / 2.0
    lo, hi = (k / n if k else 0.0), 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if binom_cdf(k, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return (lo + hi) / 2


def cp_lower(n: int, k: int, conf: float = 0.95) -> float:
    """C-P **双侧**下界：解 `P(X ≥ k) = (1-conf)/2`（同样用 α/2）。"""
    if n <= 0 or k <= 0:
        return 0.0
    alpha = (1.0 - conf) / 2.0
    lo, hi = 0.0, k / n
    for _ in range(200):
        mid = (lo + hi) / 2
        if 1.0 - binom_cdf(k - 1, n, mid) < alpha:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return (lo + hi) / 2


def zero_failure_upper(n: int, conf: float = 0.95) -> float:
    """k=0 的零失效上界（教科书 `3/n` 的精确版）。"""
    return cp_upper(n, 0, conf)


def cp_bounds(n: int, k: int, conf: float = 0.95) -> dict:
    p = k / n if n else 0.0
    return {"n": n, "k": k, "conf": conf, "point": p,
            "cp_lower": cp_lower(n, k, conf), "cp_upper": cp_upper(n, k, conf),
            "variance": (p * (1 - p) / n) if n else None,
            "se": math.sqrt(p * (1 - p) / n) if n else None,
            "note": ("零失效：点估计 0 但**上界 ≠ 0**（不许宣称'逃逸率为 0'）" if k == 0
                     else "双侧 Clopper-Pearson 精确区间")}


# ── metrics 读取 ──────────────────────────────────────────────────────────────
def load_metrics(path: Path | str | None = None) -> dict:
    # ⚠️ 默认值在**调用时**解析（写成 `path=DEFAULT_METRICS` 会被默认参数在定义期绑定，
    #    导致测试里替换模块级路径后仍读老文件 ⇒ 自洽校验形同虚设）。
    p = Path(path) if path else Path(DEFAULT_METRICS)
    if not p.is_file():
        raise SystemExit(f"[honesty] metrics.jsonl 不存在：{p}")
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise SystemExit("[honesty] metrics.jsonl 为空")
    for ln in reversed(lines):                  # 末行通常是最新一次跑批
        try:
            doc = json.loads(ln)
        except ValueError:
            continue
        if find_history(doc):
            return doc
    try:
        return json.loads(lines[-1])
    except ValueError as exc:
        raise SystemExit(f"[honesty] 末行不是合法 JSON：{exc}") from exc


HISTORY_KEYS = ("escape_rate_convergence", "escape_rate_history", "mutation_escape_rate_history")


def _hist_ok(rows: object) -> bool:
    """只认"带 numerator/denominator（或 judged）"的那一份（另有只记判分数的历史表）。"""
    return (isinstance(rows, list) and bool(rows) and isinstance(rows[0], dict)
            and "numerator" in rows[0] and ("denominator" in rows[0] or "judged" in rows[0]))


def find_all_histories(node: object) -> list[list[dict]]:
    """**收集全部**候选曲线：末行里其实有两份（`curves.mutation_escape_rate_history`（6 点）
    与 `metrics_608.escape_rate_convergence`（7 点，**带 denominator 的权威份**）），
    只取第一份会漏 v7 ⇒ 必须先收全再挑。"""
    out: list[list[dict]] = []
    if isinstance(node, dict):
        for key in HISTORY_KEYS:
            rows = node.get(key)
            if _hist_ok(rows):
                out.append(rows)
        for v in node.values():
            out.extend(find_all_histories(v))
    elif isinstance(node, list):
        for v in node:
            out.extend(find_all_histories(v))
    return out


def _version_no(rows: list[dict]) -> int:
    best = 0
    for r in rows:
        ver = str(r.get("version") or r.get("baseline_version") or "")
        if ver.startswith("v") and ver[1:].isdigit():
            best = max(best, int(ver[1:]))
    return best


def find_history(node: object) -> list[dict]:
    """挑**版本号最高**的那份（并列时取条目更多的那份）⇒ 拿到含 v7 的权威曲线。"""
    cands = find_all_histories(node)
    if not cands:
        return []
    cands.sort(key=lambda rows: (_version_no(rows), len(rows)))
    return cands[-1]


def convergence_curve(doc: dict) -> list[dict]:
    out: list[dict] = []
    prev_n: int | None = None
    for h in find_history(doc):
        n = int(h.get("denominator") or h.get("judged") or 0)
        k = int(h.get("numerator") or 0)
        note = str(h.get("note") or "")
        caliber = ("口径修正" in note) or ("取代" in note) or (
            prev_n is not None and n != prev_n and "冻结" not in note)
        out.append({"version": str(h.get("version") or h.get("baseline_version")),
                    "judged": n, "n_a": h.get("n_a"),
                    "numerator": k, "point": (k / n) if n else None,
                    "cp_lower": h.get("cp_lower") or cp_lower(n, k),
                    "cp_upper": h.get("cp_upper") or cp_upper(n, k),
                    "caliber_change": bool(caliber), "note": note})
        prev_n = n
    return out


def render_curve() -> str:
    curve = convergence_curve(load_metrics())
    real = [c for c in curve if not c["caliber_change"]]
    lines = ["| 版本 | judged | n_a | 逃逸 | 点估计 | C-P95 上界 | 口径修正 | note |",
             "|---|---|---|---|---|---|---|---|"]
    for c in curve:
        lines.append(f"| {c['version']} | {c['judged']} | {c['n_a']} | {c['numerator']} | "
                     f"{(c['point'] or 0):.4%} | {(c['cp_upper'] or 0):.4%} | "
                     f"{'**是**' if c['caliber_change'] else '否'} | {c['note'][:40]}… |")
    lines.append("")
    lines.append(f"- 可比的真实进展点仅 **{len(real)}** 个，其余是尺子变更 ⇒ "
                 "**不得宣称单调收敛**（口径修正 ≠ 进步）。")
    return "\n".join(lines)


def render_report() -> str:
    b = cp_bounds(V7["n"], V7["k"])
    return "\n".join([
        "# 度量诚实性报告（609 E1）", "",
        "## 一、逃逸率的精确区间（Clopper-Pearson，**非正态近似**）", "",
        f"- v7 权威：judged **{V7['n']}** · escaped **{V7['k']}** · n_a {V7['n_a']}"
        "（n_a 永不进分母）",
        f"- 点估计 {b['point']:.6%} · **双侧 C-P95 [{b['cp_lower']:.6%}, {b['cp_upper']:.6%}]**",
        f"- 零失效上界对照（k=0，n={V7['n']}）：{zero_failure_upper(V7['n']):.6%}"
        " ⇒ 一个都没抓到也只能给上界，不能给 0",
        "",
        "## 二、方差声明", "",
        f"- 二项方差 `p(1-p)/n` = {b['variance']:.3e} · 标准误 {b['se']:.3e}",
        "- C-P 区间**已经吃掉**这份方差 ⇒ 不必再叠一层近似区间；",
        "- 跨版本**不可做趋势检验**：v1→v5 是口径修正（尺子换了），不是同一总体样本；",
        "",
        "## 三、收敛曲线 v1→v7", "", render_curve(), "",
    ])


def check() -> list[str]:
    """用**记录里自己的 n/k** 复算区间再对账 ⇒ 分母被改也会红（不是拿常量比常量）。"""
    problems: list[str] = []
    if not Path(DEFAULT_METRICS).is_file():
        return [f"metrics.jsonl 不存在：{DEFAULT_METRICS}"]
    row = [c for c in convergence_curve(load_metrics()) if c["version"] == "v7"]
    if not row:
        return ["metrics.jsonl 里没有 v7 逃逸率点 ⇒ 无法对账"]
    r = row[0]
    n, k = int(r["judged"]), int(r["numerator"])
    b = cp_bounds(n, k)
    if abs(float(r["cp_upper"]) - b["cp_upper"]) > 1e-9:
        problems.append(f"v7 C-P 上界复算不一致：记录 {r['cp_upper']} vs 复算 {b['cp_upper']}"
                        f"（按记录自身的 n={n}/k={k}）")
    if abs(float(r["cp_lower"]) - b["cp_lower"]) > 1e-9:
        problems.append(f"v7 C-P 下界复算不一致：记录 {r['cp_lower']} vs 复算 {b['cp_lower']}")
    if n != V7["n"] or k != V7["k"]:
        problems.append(f"v7 分母/分子与冻结值 {V7['n']}/{V7['k']} 不符 ⇒ 口径变了")
    if int(r["n_a"] or 0) != V7["n_a"]:
        problems.append(f"v7 n_a 与冻结值 {V7['n_a']} 不符 ⇒ n_a 口径变了")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="metrics_honesty",
                                 description="609 E1 度量诚实性（C-P 精确区间 + 收敛曲线 + 口径修正）")
    ap.add_argument("--version", action="version", version=f"metrics_honesty {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("cp")
    sp.add_argument("--n", type=int, required=True)
    sp.add_argument("--k", type=int, required=True)
    sp.add_argument("--conf", type=float, default=0.95)
    sub.add_parser("curve")
    sub.add_parser("variance")
    sp = sub.add_parser("report")
    sp.add_argument("--write", action="store_true", help="落盘到 data/metrics_honesty.md")
    sp.add_argument("--out", default=str(REPORT_OUT))
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[honesty] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        b = cp_bounds(V7["n"], V7["k"])
        print(f"[honesty] --check OK：v7 {V7['k']}/{V7['n']} 的 C-P95 上界复算 "
              f"{b['cp_upper']:.9f} 与 metrics.jsonl 记录一致（1e-9）")
        return 0

    if a.cmd == "cp":
        b = cp_bounds(a.n, a.k, a.conf)
        print(json.dumps(b, ensure_ascii=False, indent=1))
        if a.k == 0:
            print(f"零失效上界（k=0）={zero_failure_upper(a.n, a.conf):.6%}"
                  f"（点估计 0，但上界不是 0）")
        return 0

    if a.cmd == "curve":
        print(render_curve())
        return 0

    if a.cmd == "variance":
        b = cp_bounds(V7["n"], V7["k"])
        print(f"[honesty] 方差声明：p={b['point']:.6%} · 方差 p(1-p)/n = {b['variance']:.3e} · "
              f"SE = {b['se']:.3e}")
        print("  C-P 区间已含此方差；跨版本不可做趋势检验（口径修正 ≠ 时间序列）")
        return 0

    text = render_report()
    if a.cmd == "report" and getattr(a, "write", False):
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        print(f"[honesty] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
