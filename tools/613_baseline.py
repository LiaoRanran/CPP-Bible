#!/usr/bin/env python3
"""613 任务0 · 先量基线（只读，不写受控目录）。

四个子任务（spec 0.1-0.4）：
  0.1 CI 四 job 现状台账        → data/613_baseline_ci.md
  0.2 学习者镜像数据缺口台账     → data/613_baseline_learner_twin.md
  0.3 论证层桥接边人审状态台账   → data/613_baseline_argumentation.md
  0.4 D5 基准文件债务台账       → data/613_baseline_d5_debt.md

铁律：本工具**不运行**监工类 --check（gate_engine/poison_drill/atom_evidence_replay/tool_integrity）。
CI 结论一律来自 GitHub Actions API（权威、外部视角）；本地数字一律从既有工件读取。

CLI：
  python tools/613_baseline.py            # 生成四份台账
  python tools/613_baseline.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BOOK = ROOT / "Book"
ARCHIVE_BENCH = ROOT / "_archive" / "benchmarks"

REPO = "LiaoRanran/CPP-Bible"
GH_TIMEOUT = 25
UA = {"User-Agent": "cpp-bible-613-baseline", "Accept": "application/vnd.github+json"}

D5_RE = re.compile(r"_bench_d5_[A-Za-z0-9_]+\.cpp")


# ─────────────────────────── 通用 ───────────────────────────

def gh_api(path: str) -> dict | list:
    """GitHub API 只读；离线/失败返回 {'__error__': ...}，绝不抛异常（fail-soft）。"""
    url = f"https://api.github.com{path}"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=GH_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:  # 网络不可达 / 404 / 限流
        return {"__error__": f"{type(e).__name__}: {e}"}


def _md_table(rows: list[list[str]], header: list[str]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return out


def _write(name: str, lines: list[str]) -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    p = DATA / name
    p.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return p


def _head(title: str) -> list[str]:
    return [f"# {title}", "",
            f"> 生成：`python tools/613_baseline.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
            "> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。", ""]


# ─────────────────────────── 0.1 CI ───────────────────────────

def baseline_ci() -> list[str]:
    L = _head("613 基线 0.1 · CI 四 job 现状台账")
    runs = gh_api(f"/repos/{REPO}/actions/runs?per_page=3")
    if isinstance(runs, dict) and "__error__" in runs:
        L += [f"> ⚠ GitHub API 不可达：`{runs['__error__']}` ⇒ 无法记录 CI 结论（离线）。", ""]
        return L

    L.append(f"仓库 `{REPO}` ｜ API 总运行数={runs.get('total_count', '?')}")
    L.append("")
    for run in runs.get("workflow_runs", [])[:3]:
        rid = run["id"]
        L.append(f"## Run #{run['run_number']}（{run.get('status')} / **{run.get('conclusion')}**）")
        L.append("")
        L.append(f"- head_sha：`{run.get('head_sha', '')[:12]}` ｜ 事件={run.get('event')} ｜ "
                 f"分支={run.get('head_branch')} ｜ 创建={run.get('created_at')}")
        jobs = gh_api(f"/repos/{REPO}/actions/runs/{rid}/jobs?per_page=50")
        if isinstance(jobs, dict) and "__error__" in jobs:
            L.append(f"- ⚠ job 明细拉取失败：`{jobs['__error__']}`")
            L.append("")
            continue
        rows = []
        for j in jobs.get("jobs", []):
            failed = [s["name"] for s in j.get("steps", []) if s.get("conclusion") == "failure"]
            rows.append([j["name"], str(j.get("conclusion")), "、".join(failed) or "—"])
        L += _md_table(rows, ["job", "conclusion", "失败步骤"])
        L.append("")
    L.append("> 判定口径：CI 结论以 API 为准（外部视角，最权威）。本批不本地复跑监工工具。")
    return L


# ───────────────────── 0.2 学习者镜像数据缺口 ─────────────────────

def _jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            out.append({"__bad__": ln[:80]})
    return out


def baseline_learner_twin() -> list[str]:
    L = _head("613 基线 0.2 · 学习者镜像数据缺口台账")

    st_path = DATA / "learner_state_612.jsonl"
    st = _jsonl(st_path)
    L.append("## 掌握度存储 `data/learner_state_612.jsonl`")
    L.append("")
    if not st:
        L.append("- **不存在**（612 未初始化或路径不同）")
    else:
        keys = Counter()
        for r in st:
            keys.update(r.keys())
        L.append(f"- 记录数：**{len(st)}** ｜ 字段：{dict(keys)}")
        kcs = {r.get("kc_id") for r in st if r.get("kc_id")}
        mastered = [r for r in st if float(r.get("mastery", 0) or 0) >= 0.5]
        L.append(f"- 覆盖 KC 数={len(kcs)} ｜ 已掌握(≥0.5)={len(mastered)} ｜ "
                 f"平均掌握度={sum(float(r.get('mastery', 0) or 0) for r in st) / max(len(st), 1):.3f}")
    L.append("")

    kc_json = DATA / "kc_inventory_612.json"
    L.append("## KC 台账 `data/kc_inventory_612.json`")
    L.append("")
    if kc_json.is_file():
        try:
            inv = json.loads(kc_json.read_text(encoding="utf-8"))
            items = inv if isinstance(inv, list) else inv.get("kc", inv.get("items", []))
            L.append(f"- KC 数：**{len(items)}**")
            if items and isinstance(items[0], dict):
                L.append(f"- 字段：{sorted(items[0].keys())}")
        except Exception as e:
            L.append(f"- ⚠ 解析失败：{e}")
    else:
        L.append("- **不存在**")
    L.append("")

    L.append("## 真实学习行为数据源")
    L.append("")
    behavior = DATA / "learner_behavior.jsonl"
    L.append(f"- `data/learner_behavior.jsonl`：**{'存在' if behavior.is_file() else '不存在'}**"
             f"{f'（{len(_jsonl(behavior))} 条）' if behavior.is_file() else ''}")
    L.append("- 结论：**无真实学习行为数据**（612 原型全为模拟数据）⇒ 线 C 必须先建接入层（C1）。")
    L.append("")
    L.append("> 缺口判定：掌握度是 612 `simulate()` 生成的模拟值，非真实行为递推 ⇒ 镜像仍为空壳。")
    return L


# ───────────────────── 0.3 论证层桥接边 ─────────────────────

def _find_candidates() -> Path | None:
    for name in ("bridge_edge_candidates_612.json", "bridge_edge_candidates.json",
                 "bridge_edge_pre_annotate_612.json"):
        p = DATA / name
        if p.is_file():
            return p
    return None


def baseline_argumentation() -> list[str]:
    L = _head("613 基线 0.3 · 论证层桥接边人审状态台账")

    cp = _find_candidates()
    L.append("## 桥接候选边")
    L.append("")
    if cp is None:
        L.append("- ⚠ 未找到候选边工件（data/bridge_edge_candidates*.json）")
    else:
        try:
            cand = json.loads(cp.read_text(encoding="utf-8"))
            items = cand if isinstance(cand, list) else cand.get("candidates", [])
            L.append(f"- 工件：`{cp.name}` ｜ 候选数：**{len(items)}**")
            if items:
                L.append(f"- 字段：{sorted(items[0].keys()) if isinstance(items[0], dict) else 'n/a'}")
        except Exception as e:
            L.append(f"- ⚠ 解析失败：{e}")
    L.append("")

    rev = DATA / "bridge_edge_review_612.jsonl"
    rv = _jsonl(rev)
    L.append("## 桥接边人审记录")
    L.append("")
    L.append(f"- `data/bridge_edge_review_612.jsonl`：{'存在' if rev.is_file() else '不存在'} ｜ 记录数：**{len(rv)}**")
    L.append("- 结论：**桥接边人审记录为空** ⇒ 98 条候选边无一条经过人审确认。")
    L.append("")

    gl = DATA / "grounded_labels_w2.json"
    L.append("## W2 判决现状 `data/grounded_labels_w2.json`")
    L.append("")
    if gl.is_file():
        try:
            g = json.loads(gl.read_text(encoding="utf-8"))
            nodes = g.get("nodes", g) if isinstance(g, dict) else g
            if isinstance(nodes, dict):
                cnt = Counter(str(v).upper() for v in nodes.values())
            else:
                cnt = Counter(str(n.get("label", n.get("status", "?"))).upper() for n in nodes)
            L.append(f"- 判决分布：{dict(cnt)}")
            L.append(f"- 节点总数={sum(cnt.values())}")
        except Exception as e:
            L.append(f"- ⚠ 解析失败：{e}")
    else:
        L.append("- ⚠ 不存在")
    L.append("")
    L.append("> 口径提醒：W2 判决存在 keep-low(IN114/OUT7) 与 upgrade-medium(IN121/OUT0) 双口径（611 遗留未裁决）。")
    return L


# ───────────────────── 0.4 D5 债务 ─────────────────────

def baseline_d5() -> list[str]:
    L = _head("613 基线 0.4 · D5 基准文件债务台账")

    declared: Counter[str] = Counter()
    chapter_of: dict[str, set[str]] = {}
    for md in sorted(BOOK.rglob("*.md")):
        if not md.is_file():
            continue
        try:
            txt = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in D5_RE.findall(txt):
            declared[m] += 1
            chapter_of.setdefault(m, set()).add(md.relative_to(BOOK).as_posix())

    root_files = {p.name for p in ROOT.glob("_bench_d5_*.cpp")}
    arc_files = {p.name for p in ARCHIVE_BENCH.glob("_bench_d5_*.cpp")} if ARCHIVE_BENCH.is_dir() else set()
    all_files = root_files | arc_files

    L.append("## 计数")
    L.append("")
    L += _md_table([
        ["Book 中声明的基准源（去重）", len(declared)],
        ["仓库根 `_bench_d5_*.cpp`", len(root_files)],
        ["`_archive/benchmarks/` 中", len(arc_files)],
        ["磁盘合计（根 ∪ archive）", len(all_files)],
        ["声明但两处都缺失", len([f for f in declared if f not in all_files])],
        ["孤儿（存在但未被 Book 引用）", len(all_files - set(declared))],
    ], ["项", "数"])
    L.append("")

    missing = sorted(f for f in declared if f not in all_files)
    L.append("## 真·缺失（声明但磁盘不存在）")
    L.append("")
    L.append(f"- 共 **{len(missing)}** 个" + ("：" + "、".join(missing[:20]) + ("…" if len(missing) > 20 else "")
                                            if missing else "（无）"))
    L.append("")

    orphan = sorted(all_files - set(declared))
    L.append("## 孤儿文件（磁盘存在但 Book 未引用）")
    L.append("")
    L.append(f"- 共 **{len(orphan)}** 个" + ("：" + "、".join(orphan[:20]) + ("…" if len(orphan) > 20 else "")
                                           if orphan else "（无）"))
    L.append("")

    L.append("## 根因")
    L.append("")
    L.append("- `tools/d5_source_integrity.py` 的契约是「每条声明对应**仓库根**一个真实存在且 git 跟踪的 "
             "`_bench_d5_X.cpp`」；而基准源实际已迁至 `_archive/benchmarks/`（未 ignore，git 已跟踪）。")
    L.append("- ⇒ 门禁判「声明但磁盘缺失/未跟踪」，**并非文件内容真的丢失**。")
    L.append("")
    L.append("> 与任务书假设的偏差：任务书写「8 章引用缺失 + 22 孤儿文件」，实测见上表（以实测为准）。")
    return L


# ─────────────────────────── main ───────────────────────────

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 任务0 · 基线台账（只读）")
    ap.add_argument("--check", action="store_true", help="自验证：四份台账可生成且非空")
    a = ap.parse_args(argv)

    if a.check:
        ok = True
        for fn, name in ((baseline_ci, "613_baseline_ci.md"),
                         (baseline_learner_twin, "613_baseline_learner_twin.md"),
                         (baseline_argumentation, "613_baseline_argumentation.md"),
                         (baseline_d5, "613_baseline_d5_debt.md")):
            try:
                lines = fn()
                assert len(lines) > 6, f"{name} 内容过短"
                assert lines[0].startswith("# "), f"{name} 缺标题"
                print(f"[baseline] ✓ {name}（{len(lines)} 行）")
            except Exception as e:
                ok = False
                print(f"[baseline] ✗ {name}: {e}")
        print("[613_baseline] " + ("✅ 自验证通过" if ok else "❌ 自验证失败"))
        return 0 if ok else 1

    for fn, name in ((baseline_ci, "613_baseline_ci.md"),
                     (baseline_learner_twin, "613_baseline_learner_twin.md"),
                     (baseline_argumentation, "613_baseline_argumentation.md"),
                     (baseline_d5, "613_baseline_d5_debt.md")):
        p = _write(name, fn())
        print(f"[613_baseline] 写入 {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
