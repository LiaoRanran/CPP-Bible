"""609 B2 · 全量 slow 性能剖析（cProfile，**不改任何被测代码**）。

从 `tests/conftest.py` 的 `SLOW_MODULES` 读出 slow 测试清单，逐个：

    python -m cProfile -o data/profiles/<file>.prof \
           -m pytest tests/<file> -n0 --tb=no -q -p no:cacheprovider

然后用 `pstats` 取 **tottime Top5**（真正在本进程里烧 CPU 的函数），连同墙钟、退出码、
通过的用例数写 `data/slow_performance_profile_full.md`，并给每条瓶颈一句的建议。

诚实口径：
  * **不改一行被测代码**（剖析 ≠ 优化，优化是 B3 的事）；
  * per-file 墙钟预算 `--cap N`（默认 45s）：超时则**标注 TIMEOUT/未完成**，
    `.prof` 可能残缺或被跳过 —— 绝不把没跑完的东西说成跑完了；
  * tottime 是**采样/计数**得来的；`-n0` 串行跑，避免 xdist 子进程抢 CPU 让数字失真；
  * `--check` 只做两件能复算的事：报表齐全性 + 每个 `.prof` 重解析出来的 Top1
    与报表里记的 Top1 一致（派生件可复核）。

CLI：
    profile [--cap 45] [--only FILE ...]   0 ok
    --check                                0 ok / 1 报表缺或与 .prof 不自洽
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import pstats
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"
PROFILE_DIR = ROOT / "data" / "profiles"
REPORT = ROOT / "data" / "slow_performance_profile_full.md"

VERSION = "1.0"

#: 已知瓶颈形态 → 建议（**只是标签匹配**，不是凭空结论）
PATTERNS: tuple[tuple[tuple[str, ...], str, str], ...] = (
    (("sqlite3", "_connect", "execute", "PRAGMA"),
     "库连接/PRAGMA 生命周期",
     "连接复用（609 B1 已在 task_queue 落地：同 path+thread 一把连接，WAL 只一次）"),
    (("subprocess", "Popen", "communicate", "run"),
     "子进程起停",
     "批处理化：把 N 次命令行调用合成 1 次；或加结果缓存（key=输入哈希）"),
    (("compile", "g++", "cc1plus", "toolchain"),
     "真实编译",
     "编译产物缓存（key=源文件哈希）⇒ 同源码不重复编译；热 ccache 前缀"),
    (("read_file", "read_text", "open", "md5", "sha256", "hexdigest"),
     "重复读盘/重复哈希",
     "数据缓存（key=路径+mtime）⇒ 同一份输入只读一次、只算一次哈希"),
    (("json", "loads", "dumps", "yaml", "safe_load"),
     "重复解析同一份规则/台账",
     "模块级规则缓存（key=文件 mtime+大小），脏则失效"),
    (("sleep", "time.sleep"), "显式等待",
     "缩小等待窗口或改事件通知（需确认语义不能被 races 依赖）"),
    (("rglob", "glob", "walk", "scandir"), "全树遍历",
     "把遍历结果按目录 mtime 缓存；或把清单固化进台账"),
)


def slow_modules(conftest: Path = TESTS / "conftest.py") -> list[str]:
    """从 conftest 里正则读出 `SLOW_MODULES`（**不 import conftest**：它有 fixture 副作用）。"""
    src = conftest.read_text(encoding="utf-8")
    m = re.search(r"SLOW_MODULES\s*=\s*frozenset\(\{(.*?)\}\)", src, re.DOTALL)
    if not m:
        return []
    body = m.group(1)
    out = re.findall(r'"([^"]+\.py)"', body)
    return [f for f in out if (TESTS / f).is_file()]


def _top(st: pstats.Stats, n: int = 5) -> list[dict]:
    rows = []
    for (fn, line, name), (cc, nc, tt, ct, _callers) in st.stats.items():
        rows.append({"file": fn, "line": line, "func": name, "calls": nc,
                     "tottime": tt, "cumtime": ct, "percall": tt / nc if nc else 0.0})
    rows.sort(key=lambda r: (-r["tottime"], -r["cumtime"]))
    total = sum(r["tottime"] for r in rows) or 1.0
    for r in rows:
        r["share"] = r["tottime"] / total
    return rows[:n]


def _count_results(out: str) -> dict[str, int]:
    """从 pytest 的进度行（`.....sF [100%]`）数结果。

    本仓 `-q` 下 pytest 的"N passed in Xs"汇总行被抑制（实测无该行），
    故改数**进度点**：`.`=passed `s`=skipped `F`=failed `E`=error `x`=xfail `X`=xpass。
    """
    marks = "".join(re.findall(r"^([.sFExX]+)\s*(?:\[\s*\d+%\])?", out, re.MULTILINE))
    return {"passed": marks.count("."), "skipped": marks.count("s"),
            "failed": marks.count("F"), "errors": marks.count("E"),
            "xfail": marks.count("x"), "xpass": marks.count("X")}


def _suggest(rows: list[dict]) -> str:
    """按 Top 的热点函数判瓶颈形态；**同类只报一次**，且只认 Top3（避免尾部的噪声入结论）。"""
    hits: dict[str, str] = {}
    for r in rows[:3]:
        key = f"{r['file']}::{r['func']}"
        for words, label, advice in PATTERNS:
            if any(w in key for w in words) and label not in hits:
                hits[label] = advice
    return "；".join(f"{k} ⇒ {v}" for k, v in list(hits.items())[:2]) \
        if hits else "（未匹配到已知形态 ⇒ 需人工读 caller 图）"


def profile_one(name: str, cap: float) -> dict:
    """跑一个测试文件的 cProfile；返回实测结果 dict（超时也如实记账）。"""
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    prof = PROFILE_DIR / f"{name}.prof"
    cmd = [sys.executable, "-m", "cProfile", "-o", str(prof), "-m", "pytest",
           str(TESTS / name), "-n0", "--tb=no", "-q", "-p", "no:cacheprovider"]
    t0 = time.time()
    timed_out = False
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=cap)
        out, rc = p.stdout or "", p.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        out = str(exc.stdout or "") if isinstance(exc.stdout, str) else ""
        rc = None
    dt = time.time() - t0
    row = {"file": name, "wallclock": round(dt, 2), "exit": rc,
           "results": _count_results(out), "timeout": timed_out,
           "prof": prof.name if prof.is_file() else None,
           "top": [], "suggestion": ""}
    if prof.is_file() and not timed_out:
        try:
            st = pstats.Stats(str(prof))
            row["top"] = _top(st)
            row["suggestion"] = _suggest(row["top"])
        except Exception as exc:                      # prof 残缺 ⇒ 如实记账
            row["suggestion"] = f"（prof 解析失败：{exc!r}）"
    return row


def _fmt_results(r: dict) -> str:
    res = r.get("results") or {}
    if not res:
        return "—"
    bits = [f"passed {res.get('passed', 0)}"]
    for k in ("failed", "errors", "skipped", "xfail", "xpass"):
        if res.get(k):
            bits.append(f"{k} {res[k]}")
    return " · ".join(bits)


def render_report(rows: list[dict], cap: float) -> str:
    ok = [r for r in rows if not r["timeout"]]
    to = [r for r in rows if r["timeout"]]
    agg: dict[str, float] = {}
    for r in rows:
        for t in r["top"]:
            agg[f"{Path(t['file']).name}::{t['func']}"] = (
                agg.get(f"{Path(t['file']).name}::{t['func']}", 0.0) + t["tottime"])
    top10 = sorted(agg.items(), key=lambda kv: -kv[1])[:10]

    lines = [
        "# 全量 slow 性能剖析（609 B2 · cProfile，不改被测代码）",
        "",
        f"- 解释器：`{sys.executable}`",
        f"- 清单来源：`tests/conftest.py::SLOW_MODULES`（共 {len(rows)} 个文件）",
        f"- per-file 墙钟预算：**{cap:.0f}s**（超时 ⇒ 标注未完成，不许拿残缺数据充数）",
        f"- 已完整剖析 **{len(ok)}** 个 · 超时未完成 **{len(to)}** 个",
        "",
        "## Top10 聚合瓶颈（按 tottime 求和）",
        "",
        "| # | 函数 | 累计 tottime(s) |",
        "|---|---|---|",
    ]
    for i, (name, tt) in enumerate(top10, 1):
        lines.append(f"| {i} | `{name}` | {tt:.3f} |")
    if not top10:
        lines.append("| — | （无可用样本） | — |")

    lines += ["", "## 逐文件剖析", ""]
    for r in rows:
        lines += [
            f"### {r['file']}",
            "",
            f"- 墙钟 **{r['wallclock']}s** · 退出码 {r['exit']} · {_fmt_results(r)}"
            + (" · ⚠️ **TIMEOUT（未完成剖析）**" if r["timeout"] else ""),
        ]
        if r["top"]:
            lines += ["", "| tottime(s) | 占比 | calls | 函数 |", "|---|---|---|---|"]
            for t in r["top"]:
                lines.append(f"| {t['tottime']:.3f} | {t['share'] * 100:.1f}% | {t['calls']} | "
                             f"`{Path(t['file']).name}:{t['line']}::{t['func']}` |")
            lines += ["", f"- 瓶颈判定：{r['suggestion']}"]
        else:
            lines += ["", "- 无可用 .prof（超时/解析失败）⇒ **不给瓶颈结论**（托底诚实）"]
        lines.append("")
    return "\n".join(lines) + "\n"


def profile(cap: float = 45.0, only: list[str] | None = None) -> list[dict]:
    names = only or slow_modules()
    rows = [profile_one(n, cap) for n in names]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_report(rows, cap), encoding="utf-8", newline="\n")
    # 原始结果留底 ⇒ 报表可以脱离重跑被复核/重渲染（`--check` 与人工核对都要用）
    (PROFILE_DIR / "_rows.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return rows


# ── 校验 ──────────────────────────────────────────────────────────────────────
def check() -> list[str]:
    problems: list[str] = []
    if not REPORT.is_file():
        return [f"报表缺失：{REPORT}（先跑 profile）"]
    md = REPORT.read_text(encoding="utf-8")
    for prof in sorted(PROFILE_DIR.glob("*.prof")):
        name = prof.name[:-5]
        if name not in md:
            problems.append(f"报表缺少 {name} 的章节")
            continue
        try:
            rows = _top(pstats.Stats(str(prof)), 1)
        except Exception as exc:
            problems.append(f"{prof} 无法解析：{exc!r}")
            continue
        if rows:
            key = f"{Path(rows[0]['file']).name}:{rows[0]['line']}::{rows[0]['func']}"
            if key not in md and rows[0]["func"] not in md:
                problems.append(f"{name}：报表里的 Top1 与 {prof} 重解析结果不一致（{key}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="slow_perf_profile",
                                 description="609 B2 全量 slow 性能剖析（cProfile，不改代码）")
    ap.add_argument("--version", action="version", version=f"slow_perf_profile {VERSION}")
    ap.add_argument("--check", action="store_true", help="校验报表与 .prof 自洽（exit 1 = 破）")
    ap.add_argument("--cap", type=float, default=45.0, help="单文件墙钟预算秒数（默认 45）")
    ap.add_argument("--only", nargs="*", default=None, help="只剖析这几个文件")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[slow_perf] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[slow_perf] --check OK：{REPORT.name} 与 {PROFILE_DIR.name}/ 自洽"
              f"（prof 文件 {len(list(PROFILE_DIR.glob('*.prof')))} 个）")
        return 0

    rows = profile(cap=a.cap, only=a.only)
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
    print(f"[slow_perf] 剖析完成 → {REPORT.relative_to(ROOT).as_posix()}"
          f"（完成 {sum(1 for r in rows if not r['timeout'])} / {len(rows)}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
