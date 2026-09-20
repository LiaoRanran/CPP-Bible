#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""metrics_collector.py — 质量度量 L1（508 任务6）。

为什么（497/508）：仓库里已有 `gen_metrics.py`（**文档数字 vs 事实源**的一致性门禁）、
`cost_tracker.py`（单原子成本）、`golden_lock.py`（质量指标基线）——但它们各自回答一个问题，
**没有一份"某个时刻全仓健康度的横截面快照"**。于是"这周比上周好在哪"只能靠人回忆。
L1 把 5 类指标采成一行 JSON 追加到 `data/metrics.jsonl`，供趋势查询与阈值告警。

与既有工具的分工（**不是替代**）：
  * `gen_metrics.py`：文档里写死的数字对不对（门禁，会红）。
  * `golden_lock.py`：质量指标**恶化**即红（基线比对）。
  * `metrics_collector.py`（本文件）：**只采集 + 只 WARN**，不阻断任何流程；
    它产出的是"历史序列"，让"趋势"从口头变成可查。

5 类 27 指标（提示词写"25 项"，逐条数列实际是 27 —— 如实记录）：
  Quality 9 / Assets 7 / Performance 4 / Cost 3 / Health 4。

阈值（硬编码，**只 WARN 不 BLOCK** —— 采集器不该让任何流程变红）：

| 条件 | 级别 |
|---|---|
| `gate_block_count > 0` | ERROR |
| `replay_refute_count > 0` | ERROR |
| `pytest_wall_seconds > 300` | WARN |
| `poison_coverage_pct < 50` | WARN |

用法
====
    python tools/metrics_collector.py                     # 全量采集（含 poison/replay，分钟级）
    python tools/metrics_collector.py --no-heavy          # 跳过 poison/replay（秒级）
    python tools/metrics_collector.py --json              # 只打印，不落盘
    python tools/metrics_collector.py history --last 10   # 最近 10 次采集的趋势
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import metrics_610 as m610  # noqa: E402  (610 D1/D2/D3 采集器：独立模块，逐任务可独立提交)

sys.path.insert(0, str(Path(__file__).resolve().parent))

# 592 任务2：推翻事件通道的**唯一实现**在 tools/overturned_events.py（本模块只做委托，
#   避免"同一套 fail-closed 规则两份实现"——两份迟早会分叉，而分歧点在"谁能推翻"上最危险）。
import overturned_events as oe  # noqa: E402

METRICS_FILE = ROOT / "data" / "metrics.jsonl"
PYTHON = sys.executable

QUALITY = ("gate_block_count", "gate_warn_count", "gate_rule_count",
           "poison_pass_count", "poison_total_count", "poison_coverage_pct",
           "replay_confirm_count", "replay_refute_count", "replay_infra_error_count")
ASSETS = ("atoms_total", "atoms_verified", "atoms_draft", "evidence_total",
          "evidence_confirm", "misconceptions_total", "asm_files_count")
PERFORMANCE = ("pytest_wall_seconds", "replay_wall_seconds", "gate_wall_seconds",
               "ci_total_seconds")
COST = ("cost_tracker_total_tokens", "cost_tracker_atoms_per_batch",
        "cost_tracker_avg_per_atom")
HEALTH = ("git_ahead_count", "git_untracked_count", "debt_ledger_open_count",
          "golden_state_atoms_match")
GROUPS = {"quality": QUALITY, "assets": ASSETS, "performance": PERFORMANCE,
          "cost": COST, "health": HEALTH}
ALL_METRICS = tuple(m for g in GROUPS.values() for m in g)

THRESHOLDS = (
    ("gate_block_count", lambda v: v > 0, "ERROR", "门禁有 block"),
    ("replay_refute_count", lambda v: v > 0, "ERROR", "有证据卡被证伪"),
    ("pytest_wall_seconds", lambda v: v > 300, "WARN", "pytest 墙钟超 300s"),
    ("poison_coverage_pct", lambda v: v < 50, "WARN", "毒样例规则覆盖率低于 50%"),
)


def _run(args: list[str], timeout: int = 1800) -> tuple[int, str, float]:
    """跑子进程并返回 (exit, stdout+stderr, wall_seconds)。异常不抛，返回 rc=-1。"""
    t0 = time.perf_counter()
    try:
        p = subprocess.run([PYTHON, *args], cwd=str(ROOT), capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out, time.perf_counter() - t0
    except Exception as exc:                     # noqa: BLE001
        return -1, f"{type(exc).__name__}: {exc}", time.perf_counter() - t0


def _run_raw(argv: list[str], timeout: int = 300) -> tuple[int, str, float]:
    """跑**外部命令**（git 等，不经 Python 解释器）。与 `_run` 分开，
    否则会把 `git` 当脚本喂给 python ⇒ `rc=2`（508 首版实测踩到）。"""
    t0 = time.perf_counter()
    try:
        p = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or ""), time.perf_counter() - t0
    except Exception as exc:                     # noqa: BLE001
        return -1, f"{type(exc).__name__}: {exc}", time.perf_counter() - t0


def _num(v: object) -> float | None:
    return float(v) if isinstance(v, (int, float)) else None


# ── Quality ──────────────────────────────────────────────────────────────
def replay_counts_from_manifest(man: Path | None = None) -> dict | None:
    """从 replay 清单统计 verdict 分布（`build/replay_manifest.json`）。

    增量 replay 在"全部命中缓存"时不打印汇总行，此时这是唯一可核对的历史结果来源。
    返回 `{"confirm":n, "refute":n, "infra_error":n, "_total":n}`；不可读返回 None。
    """
    p = man or (ROOT / "build" / "replay_manifest.json")
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:                            # noqa: BLE001
        return None
    if not isinstance(d, dict):
        return None
    counts: dict = {"confirm": 0, "refute": 0, "infra_error": 0, "_total": 0}
    for v in d.values():
        if not isinstance(v, dict):
            continue
        key = str(v.get("verdict") or "").split(":")[0]
        counts[key] = counts.get(key, 0) + 1
        counts["_total"] += 1
    return counts


def collect_quality(notes: dict, *, with_heavy: bool = True) -> dict:
    out: dict = dict.fromkeys(QUALITY)

    # gate：**进程内**跑（比开子进程省一次解释器启动；规则实现与 CLI 完全相同）
    import gate_engine as ge
    t0 = time.perf_counter()
    try:
        findings = ge.run(include_advice=False)
        out["gate_wall_seconds"] = round(time.perf_counter() - t0, 2)
        out["gate_block_count"] = sum(1 for f in findings if f.severity == "block")
        out["gate_warn_count"] = sum(1 for f in findings if f.severity == "warn")
        out["gate_rule_count"] = len(ge.RULES)
    except Exception as exc:                     # noqa: BLE001
        notes["gate"] = f"采集失败：{type(exc).__name__}: {exc}"

    if not with_heavy:
        notes["poison"] = "跳过（--no-heavy）"
        notes["replay"] = "跳过（--no-heavy）"
        return out

    import poison_drill as pd
    try:
        passed, total, _fails = pd.drill()
        covered, rules_total, _unc = pd.rule_coverage()
        out["poison_pass_count"] = passed
        out["poison_total_count"] = total
        out["poison_coverage_pct"] = round(100.0 * covered / rules_total, 1) \
            if rules_total else None
    except Exception as exc:                     # noqa: BLE001
        notes["poison"] = f"采集失败：{type(exc).__name__}: {exc}"

    rc, text, wall = _run(["tools/atom_evidence_replay.py", "--check", "--incremental"])
    out["replay_wall_seconds"] = round(wall, 2)
    m = re.search(r"confirm=(\d+)\s+refute=(\d+)\s+infra_error=(\d+)", text)
    if m:
        out["replay_confirm_count"] = int(m.group(1))
        out["replay_refute_count"] = int(m.group(2))
        out["replay_infra_error_count"] = int(m.group(3))
        notes["replay"] = "本次实跑（增量，有卡重算）"
    else:
        # 增量模式下"全部命中缓存"时**不打印 confirm= 汇总**（508 实测）——
        # 这恰是度量采集的常态。此时计数只能取自清单 `build/replay_manifest.json`，
        # 语义 = "上次实跑的结果"，必须在 note 里写明来源，不能冒充"本次实跑"。
        counts = replay_counts_from_manifest()
        if counts is None:
            notes["replay"] = f"无汇总行且清单不可读（rc={rc}）"
            return out
        out["replay_confirm_count"] = counts["confirm"]
        out["replay_refute_count"] = counts["refute"]
        out["replay_infra_error_count"] = counts["infra_error"]
        notes["replay"] = (f"增量全命中缓存（未跑编译）⇒ 计数取自 build/replay_manifest.json"
                           f"（上次实跑，共 {counts['_total']} 张）")
    return out


# ── Assets ───────────────────────────────────────────────────────────────
def collect_assets(notes: dict) -> dict:
    out: dict = dict.fromkeys(ASSETS)
    import atom_evidence_replay as replay
    import gate_engine as ge
    try:
        atoms = list(ge._cards(ge.ATOMS, "ATOM-*.md"))
        out["atoms_total"] = len(atoms)
        st: dict[str, int] = {}
        for p in atoms:
            m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            s = str(m.get("status") or "?")
            st[s] = st.get(s, 0) + 1
        out["atoms_verified"] = st.get("verified", 0)
        out["atoms_draft"] = st.get("draft", 0)
        ev = list(ge._cards(ge.EVIDENCE, "EV-*.md"))
        out["evidence_total"] = len(ev)
        out["evidence_confirm"] = sum(
            1 for p in ev
            if str(replay.parse_frontmatter(
                p.read_text(encoding="utf-8", errors="replace")).get("verdict") or "")
            == "confirm")
    except Exception as exc:                     # noqa: BLE001
        notes["assets"] = f"采集失败：{type(exc).__name__}: {exc}"
    mis = ROOT / "misconceptions"
    if mis.is_dir():
        out["misconceptions_total"] = sum(
            1 for p in mis.rglob("*.md") if not p.name.startswith("README"))
    ex = ROOT / "Examples"
    if ex.is_dir():
        out["asm_files_count"] = sum(1 for _ in ex.rglob("*.asm"))
    return out


# ── Cost ─────────────────────────────────────────────────────────────────
def collect_cost(notes: dict) -> dict:
    out: dict = dict.fromkeys(COST)
    rc, text, _ = _run(["tools/cost_tracker.py", "--json", "report"], timeout=120)
    try:
        d = json.loads(text[text.index("{"):text.rindex("}") + 1])
    except Exception:                            # noqa: BLE001
        notes["cost"] = f"cost_tracker 未返回可解析 JSON（rc={rc}）"
        return out
    atoms = _num(d.get("atoms"))
    tokens = _num(d.get("total_tokens_est"))
    out["cost_tracker_total_tokens"] = int(tokens) if tokens is not None else None
    out["cost_tracker_atoms_per_batch"] = int(atoms) if atoms is not None else None
    out["cost_tracker_avg_per_atom"] = round(tokens / atoms, 1) \
        if tokens and atoms else None
    return out


# ── Health ───────────────────────────────────────────────────────────────
def collect_health(notes: dict, assets: dict | None = None) -> dict:
    out: dict = dict.fromkeys(HEALTH)
    rc, text, _ = _run_raw(["git", "rev-list", "--count", "origin/master..HEAD"])
    if rc == 0:
        out["git_ahead_count"] = int(text.strip() or 0)
    else:
        notes["git_ahead"] = f"git 未取到（rc={rc}）"
    rc, text, _ = _run_raw(["git", "status", "--porcelain"])
    if rc == 0:
        out["git_untracked_count"] = sum(1 for ln in text.splitlines()
                                         if ln.startswith("??"))
    # 债务台账：开放式条目数（读 `debt_ledger show` 的 JSON；失败则记 null + note）
    rc, text, _ = _run(["tools/debt_ledger.py", "show"], timeout=120)
    try:
        d = json.loads(text[text.index("{"):text.rindex("}") + 1])
        items = d.get("open") or d.get("items") or d.get("debts") or []
        out["debt_ledger_open_count"] = len(items) if isinstance(items, list) else None
    except Exception:                            # noqa: BLE001
        notes["debt_ledger"] = "台账未返回可解析 JSON（`show` 无 --json 时属预期）"
    # 黄金状态：tools/golden_state.json 的原子数与磁盘实际是否一致
    gs = ROOT / "tools" / "golden_state.json"
    if gs.is_file():
        try:
            d = json.loads(gs.read_text(encoding="utf-8"))
            # 真实结构：{"schema":..., "metrics": {"atoms_total": 27, ...}}（508 实测）
            m = d.get("metrics") if isinstance(d, dict) else None
            rec = _num((m or {}).get("atoms_total") if isinstance(m, dict)
                       else d.get("atoms"))
            # 磁盘实际值来自 collect_assets 的返回值（**不能**读本函数自己的 out：
            # 它的键集只有 HEALTH，永远取到 None —— 508 实测踩到，恒 None 指标）
            cur = _num((assets or {}).get("atoms_total"))
            out["golden_state_atoms_match"] = (
                None if rec is None or cur is None else rec == cur)
            if rec is None:
                notes["golden_state"] = "未找到 metrics.atoms_total 字段"
        except Exception:                        # noqa: BLE001
            notes["golden_state"] = "golden_state.json 解析失败"
    else:
        notes["golden_state"] = "tools/golden_state.json 不存在"
    return out


# ── 603 任务2：编译可复现性采样度量 ───────────────────────────────────────
@dataclass
class BuildReproducibilityMetrics:
    """603 任务2：编译可复现性采样结果。

    字段：`total`（实际采样卡数）/ `sampled` / `reproducible`（独立编译两次一致）/
    `compile_failed`（rc≠0，无法评估）/ `not_reproducible`（rc=0 但两次不一致）/
    `unavailable`（命令里提不出直接产出该 artifact 的编译行，跳过，不计入 total）/
    `notes`（明细）/ `sampled_cards`（采到的卡 id）。
    """
    total: int
    sampled: int
    reproducible: int
    compile_failed: int
    not_reproducible: int
    unavailable: int
    notes: dict
    sampled_cards: list

    def to_dict(self) -> dict:
        return {
            "total": self.total, "sampled": self.sampled,
            "reproducible": self.reproducible, "compile_failed": self.compile_failed,
            "not_reproducible": self.not_reproducible, "unavailable": self.unavailable,
            "notes": self.notes, "sampled_cards": self.sampled_cards,
        }


def collect_build_reproducibility(sample: int = 10, seed: int = 603,
                                  work_dir: Path | None = None,
                                  cards: list[dict] | None = None
                                  ) -> BuildReproducibilityMetrics:
    """603 任务2：采样 N 张证据卡的"重编译命令"，用 `check_build_reproducibility` 证独立编译确定性。

    口径（诚实）：
      * 仅采"命令里能提取出直接产出该 artifact 的编译行"的卡（无 ⇒ unavailable，跳过，不计入 total）；
      * 注入 `-Wl,--no-insert-timestamp` **中性化 PE 时间戳**——否则 MinGW 时间戳随墙钟变，度量是"假非确定"；
        这是**度量口径**，不进 replay 判决（replay 保 want_sha 匹配，存量零误伤）；
      * 用**最后一行**编译命令（与 `_recompile_invariant` 同语义：逐行覆写同一 -o 目标）；
      * total = 实际采样的卡数；reproducible / compile_failed / not_reproducible 三者之和 == total；
      * `cards` 可外部注入（测试用），否则按 card id 排序取前 `sample` 张证据卡，**确定可复现**（不随机抖动）。
    """
    import atom_evidence_replay as replay
    notes: dict = {}
    if cards is None:
        import gate_engine as ge
        cards = []
        for p in sorted(ge._cards(ge.EVIDENCE, "EV-*.md")):
            fm = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            if not isinstance(fm, dict):
                continue
            cmd = fm.get("command")
            art = fm.get("artifact")
            if not cmd or not art:
                continue
            cards.append({"card": fm.get("id") or p.stem, "command": cmd, "artifact": art})
    ordered = sorted(cards, key=lambda c: str(c.get("card") or ""))
    rng = random.Random(seed)                  # 确定性抽样（同 seed ⇒ 同卡集，不随机抖动）
    chosen = rng.sample(ordered, min(sample, len(ordered)))
    own_tmp = work_dir is None
    wd = Path(work_dir) if work_dir is not None else Path(tempfile.mkdtemp(prefix="build_repro_"))
    try:
        total = sampled = reproducible = compile_failed = not_reproducible = 0
        unavailable = 0
        sampled_cards: list = []
        for c in chosen:
            cid = str(c.get("card") or "?")
            cmd = str(c.get("command") or "")
            art = str(c.get("artifact") or "")
            lines = replay._artifact_compile_lines(cmd, art)
            if not lines:
                unavailable += 1
                notes.setdefault("unavailable_cards", []).append(cid)
                continue
            line = lines[-1]                       # 与 _recompile_invariant 同语义
            line = re.sub(r'^(\S+)', r'\1 -Wl,--no-insert-timestamp', line, count=1)
            total += 1
            sampled += 1
            sampled_cards.append(cid)
            res = replay.check_build_reproducibility(
                source_path=replay.run_root() / art,
                compile_cmd=line, work_dir=wd, output_name=Path(art).name,
                ccaches_disable=True, check_level="sha", cwd=str(replay.run_root()))
            if res.compile_exit_code != 0:
                compile_failed += 1
                notes.setdefault("compile_failed_cards", []).append(cid)
            elif res.success:
                reproducible += 1
            else:
                not_reproducible += 1
                notes.setdefault("not_reproducible_cards", []).append(
                    {"card": cid, "detail": res.diff_detail})
    finally:
        if own_tmp:
            shutil.rmtree(wd, ignore_errors=True)
    notes["sample_requested"] = sample
    notes["sample_actual"] = total
    if total:
        notes["reproducible_rate"] = round(100.0 * reproducible / total, 1)
    return BuildReproducibilityMetrics(
        total=total, sampled=sampled, reproducible=reproducible,
        compile_failed=compile_failed, not_reproducible=not_reproducible,
        unavailable=unavailable, notes=notes, sampled_cards=sampled_cards)


# ── 组装 / 告警 / 落盘 ────────────────────────────────────────────────────
def evaluate_alerts(metrics: dict) -> list[dict]:
    """硬阈值告警（只 WARN/ERROR 记录，**不 BLOCK 任何流程**）。"""
    alerts = []
    for name, pred, level, why in THRESHOLDS:
        v = metrics.get(name)
        if isinstance(v, (int, float)) and pred(v):
            alerts.append({"level": level, "metric": name, "value": v, "reason": why})
    return alerts


def collect(*, with_heavy: bool = True, with_gate: bool = True) -> dict:
    """采集一次全量快照：{timestamp, metrics{27}, notes, alerts}。"""
    notes: dict = {}
    metrics: dict = {}
    metrics.update(collect_quality(notes, with_heavy=with_heavy and with_gate))
    assets = collect_assets(notes)
    metrics.update(assets)
    metrics.update(collect_cost(notes))
    metrics.update(collect_health(notes, assets))
    # pytest_wall_seconds：**没有可靠的机读来源**（pytest 把汇总写 stdout，本仓
    # 的沙箱还会吞掉收尾汇总）⇒ 约定落盘文件 `data/pytest_last.txt`（把 pytest 输出
    # `tee` 到它即可，CI 的 pytest job 已如此做）。无该文件则留 null + note，
    # **不猜、不编**（铁律 #4）。
    pl = ROOT / "data" / "pytest_last.txt"
    if pl.is_file():
        text = pl.read_text(encoding="utf-8", errors="replace")
        # 优先认**显式标记** `[pytest-wall] total=NN.Ns`：两阶段跑法（fast -n16 + slow -n0）
        # 会产生两条 pytest 汇总行，若只按 `in Xs` 近似匹配会错取到 phase1 的值。
        # 其次才退回近似匹配（单次全量跑的场景）。
        m = (re.search(r"\[pytest-wall\]\s*total=([\d.]+)s", text)
             or re.search(r"\bin ([\d.]+)s\b", text))
        if m:
            metrics["pytest_wall_seconds"] = float(m.group(1))
            notes.setdefault("pytest_wall_seconds",
                             "来源 data/pytest_last.txt"
                             + ("（显式标记）" if "[pytest-wall]" in text else "（近似匹配 `in Xs`）"))
        else:
            notes["pytest_wall_seconds"] = "data/pytest_last.txt 中未匹配到 `in Xs` 汇总"
    else:
        notes["pytest_wall_seconds"] = ("无 data/pytest_last.txt；"
                                        "把 pytest 输出 tee 到该文件即可自动采集")
    # ci_total_seconds：**估算**（pytest 未采时只累加 replay+gate）——口径写在 notes 里，
    # 避免以后有人把它当成"CI 实测墙钟"。
    parts = [metrics.get("replay_wall_seconds"), metrics.get("gate_wall_seconds")]
    metrics["ci_total_seconds"] = round(sum(p for p in parts if p), 2)
    notes.setdefault("ci_total_seconds", "估算 = replay + gate 墙钟（不含 pytest / poison / 编译）")
    missing = [m for m in ALL_METRICS if m not in metrics]
    if missing:
        notes["missing"] = f"未采集到：{missing}"
    snap = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "metrics": {k: metrics.get(k) for k in ALL_METRICS},
            "notes": notes}
    snap["curves"] = collect_curves()          # 565 Part 4b：三曲线机制字段（1 个时点）
    # 608 C1：新增 5 类指标（人审进度 / 论证层状态 / 编译可复现 / 逃逸率收敛 / C-P 上界）
    snap["metrics_608"] = collect_608_new_metrics(notes, with_heavy=with_heavy)
    # 610 D1/D2/D3：W2 重算状态（含口径分歧显形）/ 人审进度 / 辩护链统计（同级嵌套，不动扁平 schema）
    snap["metrics_610"] = m610.collect_610_new_metrics(notes, with_heavy=with_heavy)
    if with_heavy:
        try:
            snap["build_reproducibility"] = collect_build_reproducibility().to_dict()
        except Exception as exc:                 # noqa: BLE001
            notes["build_reproducibility"] = f"采集失败：{type(exc).__name__}: {exc}"
    else:
        notes.setdefault("build_reproducibility", "跳过（--no-heavy）")
    # 606：replay 不变量状态采集（I1/I2/I3/I4），失败不 crash
    try:
        import replay_invariants as ri
        inv_results = ri.run_checks(heavy=with_heavy)
        snap["invariants"] = {r["name"]: r["passed"] for r in inv_results}
        snap["invariants_all_pass"] = all(r["passed"] for r in inv_results)
    except Exception as exc:                 # noqa: BLE001
        snap["invariants"] = None
        snap["invariants_all_pass"] = None
        notes["invariants"] = f"采集失败：{type(exc).__name__}: {exc}"
    snap["alerts"] = evaluate_alerts(snap["metrics"])
    return snap


# ── 574 任务 D：信任放权门（**只写不读**；默认不放权）──────────────────────────────
ORACLE_REGISTRY = ROOT / "data" / "oracle_registry.json"
# 放权开关：全部 **OFF**（本任务不实现任何"机器自动接受"；模型变强那天才谈）。
DELEGATION_SWITCHES = {"G-iso": False, "oracle_auto_accept": False, "llm_as_judge": False}


def oracle_report(cards: list[dict] | None = None) -> dict:
    """**报告层**只读统计：把卡/命题的 `verified_by_oracle` 与 registry 版本比对 ⇒ 标 `stale`。

    硬不变量（574 任务 D 的核心）：本函数**只做统计**，绝不能被 gate / replay / poison 的
    **判决路径**调用——"被决策读了"就是偷偷放权。判决逻辑一律不许读 `verified_by_oracle`
    （有 pytest 锁：给卡填任意 verified_by_oracle，block/warn/confirm 逐字不变）。
    缺字段 ⇒ 记 `missing_field`（正常状态，不是缺陷）。
    """
    reg: dict = {}
    try:
        reg = json.loads(ORACLE_REGISTRY.read_text(encoding="utf-8")) or {}
    except (OSError, ValueError):
        reg = {}
    cur = (reg.get("oracles") if isinstance(reg, dict) else None) or {}
    out: dict = {"registry": ORACLE_REGISTRY.name, "current_oracles": sorted(cur),
                 "delegation_switches": dict(DELEGATION_SWITCHES),
                 "entries": [], "stale": [], "missing_field": 0}
    for c in (cards or []):
        vo = c.get("verified_by_oracle") if isinstance(c, dict) else None
        if not vo:
            out["missing_field"] += 1
            continue
        name = str(vo.get("oracle") if isinstance(vo, dict) else vo)
        ver = str(vo.get("version") or "") if isinstance(vo, dict) else ""
        want_ver = str((cur.get(name) or {}).get("version") or "")
        entry = {"card": c.get("id") or c.get("card") or "?", "verified_by_oracle": vo,
                 "stale": bool(name not in cur or (want_ver and ver and ver != want_ver))}
        out["entries"].append(entry)
        if entry["stale"]:
            out["stale"].append(entry)
    return out


# ── 573 任务 A-2：overturned 事件通道（只追加；**系统绝不自动产生推翻**）────────────
OVERTURNED_FILE = ROOT / "data" / "overturned_events.jsonl"


def read_overturned_events(path: Path | None = None) -> list[dict]:
    """读事件流（**单一实现**：592 任务2 起收敛到 `tools/overturned_events.py`）。

    文件缺失 ⇒ `[]`；坏行 ⇒ **fail-loud**（事件流是审计证据，静默跳过坏行等于篡改证据链；
    573 首版的"坏行 continue"已在 592 任务2 改为显形——旧的静默口子不该留两份实现）。
    """
    return oe.read_events(path or OVERTURNED_FILE)


def log_overturned(target: str, old_verdict: str, new_verdict: str, by: str,
                   reason: str, card: str | None = None,
                   path: Path | None = None) -> dict:
    """记录一次**人或异族**的推翻（573 任务 A-2；592 任务2 实现收敛到 overturned_events）。

    schema：`{ts, target, card, old_verdict, new_verdict, by, reason}`
      * `by`：`human:<名>`（**须过 git 作者绑定**）或 `adversary:<族>`（异族无 git 身份 ⇒ 只登记）；
      * **fail-closed**：human 名不匹配该卡最后一次 git 提交的作者、或卡解析不到、或任一必填为空
        ⇒ **拒绝写入**（raise ValueError）——"无签名的人"不能推翻任何东西；
      * 只追加（`data/overturned_events.jsonl`），不覆盖、不删除。
    谁**不许**调用：任何自动检测/自动 LLM 推翻路径（战略冻结档），本函数只接显式的人/异族动作。
    """
    return oe.append(oe.make_event(target, old_verdict, new_verdict, by, reason, card=card),
                     path=path or OVERTURNED_FILE)


def collect_curves() -> dict:
    """565 Part 4b · 收敛三曲线的**机制字段**（先把管道建好，数据攒着）。

    ⚠️ **只有 1 个时点 ⇒ 不得声称"单调收敛"**（写进返回值里，报告/文档照抄）：
    趋势类结论需要 ≥2 个时点的同口径数据，现在一个都没有。

    ① `mutation_escape_rate`：逃逸率 + **双侧** C-P95 区间（接 565 Part 2 的口径块；
      数据源 = 已提交的 **`data/mutation/full_baseline_v7.json`**（591 冻结），**不重新生成基线**；
      592 任务1 起随块带 `baseline_version`/`frozen_at_commit`（从基线文件自身读）。
    ② `overturned_by_stronger_verifier`：被更强验证者推翻的命题/卡数。**事件字段**——
      读数来自只追加事件流 `data/overturned_events.jsonl`；**系统绝不自动产生推翻**。
      592 任务1.3 起另带 `overturned_channel_initialized`：文件不存在 ⇒ 计数 0 是"没有通道"
      而非"没有推翻"（两者含义相反，必须显式区分）。
    ③ `escape_survival_batches`：逃逸从产生到被收口跨了几个批次。
      **0 = 真值（非真逃逸，不计入）**、**None = 缺数据** —— 不许混读（573 立的口径）。
    """
    out: dict = {"timepoints": 1,
                 "monotone_convergence": "不可声称（尺子变更史 v1→v7，非同一量时间序列；仅 1 个含曲线时点）",
                 "note": "三曲线字段 565 Part 4b；补齐第二个时点前，这里只作机制占位"}
    from stat_bounds import proportion  # 565 Part 1 原语（局部导入：与 toolchain 同风格）

    # 573 升 v2 → **574 升 v3**（572 收 M3、574 修 M5 尺子后的全量基线）。
    #   v1/v2 **保留为历史时点**，不覆盖——否则历史曲线会被改写。
    def _rate(path: Path, tag: str, version: str = "") -> dict:
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            judged = d["blocked"] + d["escaped"]
            blk = proportion(d["escaped"], judged)
            # 592 任务1：`baseline_version`/`frozen_at_commit` **从基线文件自身读**（v7 冻结时写入的
            #   `frozen_at_commit`），不在这里再抄一遍常量——否则基线重冻结后这里会静默脱节（正是
            #   "度量不诚实"的老病：报告层数字与真实基线各说各话）。
            return {"source": str(path.relative_to(ROOT).as_posix()), "tag": tag,
                    "baseline_version": version or None,
                    "frozen_at_commit": d.get("frozen_at_commit"),
                    "judged": judged, "n_a": d["n_a"],
                    "numerator": blk["numerator"], "denominator": blk["denominator"],
                    "point": round(blk["point"], 6),
                    "cp_low": round(blk["cp_low"], 6), "cp_high": round(blk["cp_high"], 6),
                    # 592 任务1：上面三个是**展示值**（6 位小数，报告口径）；`*_raw` 是全精度原值，
                    #   供下游复算/对账。逃逸率 ~1e-3 时 6 位小数只剩 2 位有效数字，
                    #   任何 1e-9 级复算都必须在 `*_raw` 上做（别拿展示值当计算输入）。
                    "point_raw": blk["point"],
                    "cp_low_raw": blk["cp_low"], "cp_high_raw": blk["cp_high"],
                    "conf": blk["conf"]}
        except (KeyError, ValueError) as exc:      # 数据坏了要显形，不许静默跳过
            return {"source": str(path), "tag": tag, "baseline_version": version or None,
                    "error": f"基线不可用：{type(exc).__name__}: {exc}"}

    # 574 升 v3 → 575 升 v4 → 578 升 v5 → **591 升 v7**（信任根扩边 v7 冻结：589 T2 注释净化
    #   un-mask 27 条真实 fixture 路径变异 ⇒ M2 可判 141→168）。v1–v6 **保留为历史时点**，不覆盖。
    v7 = ROOT / "data" / "mutation" / "full_baseline_v7.json"
    v6 = ROOT / "data" / "mutation" / "full_baseline_v6.json"
    v5 = ROOT / "data" / "mutation" / "full_baseline_v5.json"
    v4 = ROOT / "data" / "mutation" / "full_baseline_v4.json"
    v3 = ROOT / "data" / "mutation" / "full_baseline_v3.json"
    v2 = ROOT / "data" / "mutation" / "full_baseline_v2.json"
    v1 = ROOT / "data" / "mutation" / "full_baseline_v1.json"
    out["mutation_escape_rate"] = (
        _rate(v7, "v7（591 起当前口径：589 T2 注释净化 un-mask 27 条真实 fixture 路径变异 ⇒ "
                  "M2 可判 141→168；唯一 escaped=1 = M1 / EV-CONC-001 冻结 TCE）", version="v7")
        if v7.is_file() else {"error": "缺 data/mutation/full_baseline_v7.json"})
    hist = []
    if v1.is_file():
        hist.append(_rate(v1, "v1（571 修 GATE_READ_KEYS 前，含 M2 假逃逸，仅历史）", version="v1"))
    if v2.is_file():
        hist.append(_rate(v2, "v2（571 修尺子后、含 M3 的 52 条真洞，仅历史）", version="v2"))
    if v3.is_file():
        hist.append(_rate(v3, "v3（574 修 M5 尺子后、M5 活雷未收，仅历史）", version="v3"))
    if v4.is_file():
        hist.append(_rate(v4, "v4（575 命题级活性锚：M5 规则已拦但被 diff 键吞掉，仅历史）", version="v4"))
    if v5.is_file():
        hist.append(_rate(v5, "v5（578 _findings_key 并入文案后；587 起 1/1375，仅历史）", version="v5"))
    if v6.is_file():
        hist.append(_rate(v6, "v6（588 发现器补全后；1/1379，被 v7 取代）", version="v6"))
    out["mutation_escape_rate_history"] = hist

    # 573 任务 A-2：overturned 从"恒 0 占位"变成**真读数**（读只追加事件流；写入见 log_overturned）。
    ev = read_overturned_events()
    out["overturned_by_stronger_verifier"] = len(ev)
    out["overturned_recent"] = ev[-5:]
    # 592 任务1.3：通道**是否已初始化**要显式标出来——文件缺失时计数 0 是"没有通道"而非"没有推翻"，
    #   两者含义相反（同 survival 的 None/0 之辨）。592 任务2 建了空文件后本字段转 True。
    out["overturned_channel_initialized"] = OVERTURNED_FILE.is_file()
    out["overturned_note"] = ("事件流：data/overturned_events.jsonl（只追加）。**系统绝不自动产生推翻**——"
                              "写入只能来自人或异族的显式动作，且 human 推翻者须过 git 作者绑定（fail-closed）")
    # 573 任务 A-3 起 survival 真实数据（**不编**）；592 任务1.4 补齐 M5/M6/M2 的显式条目。
    #   口径：0 = "真值 = 不是真逃逸，不计入"；None = "缺数据" —— 两者不许混（573 立的口径）。
    out["escape_survival_batches"] = {
        "M3": {"batches": 1, "escapes": 52, "produced_in": "571", "closed_in": "572",
               "note": "571 v2 浮出 52 条 → 572 全部收口 ⇒ survival = 1 批"},
        "M5": {"batches": 1, "escapes": 29, "produced_in": "574", "closed_in": "575",
               "measurement_visible_closed_in": "578",
               "note": "574 v3 浮出 29 条 M5 活雷 → 575 命题级活性锚规则已拦（1 批）；"
                       "但 v4/v5 台账里该批差异曾被 _findings_key 吞掉，"
                       "**度量可见**的收口落在 578（v5）——两个批次都记，别只留好看的那个"},
        "M2": {"batches": 0, "escapes": 0,
               "note": "571 已证实 v1 的 207 条是 GATE_READ_KEYS 尺子 bug 的**假逃逸**（修后 0）⇒ 不计入 survival"},
        "M6": {"batches": 0, "escapes": 0,
               "note": "8 条 matrix 块式→flow 等价变异体（583 已定性，非真逃逸）⇒ 不计入 survival"},
        "others": None,
    }
    out["escape_survival_note"] = ("其余算子尚无'产生→收口'的完整批次 ⇒ None（不填 0）；"
                                   "M2/M6 的 0 是「真值 = 非逃逸」、与 None（缺数据）含义相反，别混读")
    return out


# ── 608 C1：metrics 新增 5 类指标（人审进度 / 论证层状态 / 编译可复现 / 逃逸率收敛 / C-P 上界）──
def collect_608_new_metrics(notes: dict, *, with_heavy: bool = True) -> dict:
    """608 C1：新增 5 类指标，挂载为快照的 `metrics_608`（嵌套，**不破坏既有 27 项扁平 schema**）。

    只读聚合（绝不修改任何判决逻辑——人审权力 / replay 判决 / 度量口径分离）：
      * G1 人审进度：读 `attack_edge_review` 标注 + `attack_edge_generator` 候选边（596 通道）；
      * G2 论证层状态：读 `data/grounded_labels_w2.json`（W2 判决）+ 候选边按 MIS 分组；
      * G3 编译可复现：读 `replay_invariants.check_build_reproducibility`（B1 跨时间/符号表/段）；
      * G4+G5 逃逸率收敛曲线 + Clopper-Pearson 双侧 95% 上界：读 `data/mutation/full_baseline_v*.json`
        （v7 冻结，591 起不重生成），v1→v5 标注"口径修正"（非同一量时间序列），不得声称单调收敛。
    """
    out: dict = {}
    from collections import Counter

    # G1 · 人审进度指标（基于 596 人审通道，只读）
    try:
        import attack_edge_generator as aeg
        import attack_edge_review as aerv
        edges = aeg.load_edges()
        anns = aerv.load_annotations()
        st = aerv.stats(edges, anns)
        out["human_review"] = {
            "total": st["total"], "pending": st["pending"],
            "approved": st["approved"], "rejected": st["rejected"],
            "modified": st["modified"],
            "annotated_edges": st.get("annotated_edges", 0),
        }
    except Exception as exc:                     # noqa: BLE001
        notes["human_review_608"] = f"采集失败：{type(exc).__name__}: {exc}"

    # G2 · 论证层状态指标（W2 判决 + 候选边按 MIS 分组）
    try:
        import attack_edge_generator as aeg2
        edges2 = aeg2.load_edges()
        w2 = json.loads((ROOT / "data" / "grounded_labels_w2.json").read_text(encoding="utf-8"))
        nodes = w2.get("nodes", {}) if isinstance(w2, dict) else {}
        lab = Counter(v.get("label") for v in nodes.values())
        mis_groups = set()
        for e in edges2:
            d = e["direction"]
            mis_groups.add(e["source"] if d == "mis_to_prop" else e["target"])
        out["grounded"] = {
            "in": lab.get("IN", 0), "out": lab.get("OUT", 0),
            "undec": lab.get("UNDEC", 0),
            "candidate_edges_total": len(edges2),
            "candidate_edges_by_mis": len(mis_groups),
        }
    except Exception as exc:                     # noqa: BLE001
        notes["grounded_608"] = f"采集失败：{type(exc).__name__}: {exc}"

    # G3 · 编译可复现指标（B1 I2：跨时间窗口 + 符号表 + 段一致；只读 replay_invariants 结果）
    if with_heavy:
        try:
            import replay_invariants as ri
            res = ri.check_build_reproducibility(n_cards=2, cross_time=True)
            cards = res.get("cards", [])
            out["build_reproducibility"] = {
                "reproducible": all(c["match"] for c in cards) if cards else None,
                "time_macro_drift": sum(1 for c in cards
                                       if c.get("cross") == "时间宏漂移（可接受）"),
                "symtab_consistent": (all("symtab=no" not in (c.get("detail") or "")
                                           for c in cards) if cards else None),
                "n_cards": len(cards),
            }
        except Exception as exc:                 # noqa: BLE001
            notes["build_reproducibility_608"] = f"采集失败：{type(exc).__name__}: {exc}"
    else:
        notes.setdefault("build_reproducibility_608", "跳过（--no-heavy）")

    # G4 + G5 · 逃逸率收敛曲线 + Clopper-Pearson 双侧 95% 上界（v1→v7，v7 冻结不重生成）
    try:
        from stat_bounds import proportion as _cp
        baselines = {
            "v1": "571 修 GATE_READ_KEYS 前，含 M2 假逃逸（口径修正，非同量）",
            "v2": "571 修尺子后，含 M3 的 52 条真洞（口径修正）",
            "v3": "574 修 M5 尺子后，M5 活雷未收（口径修正）",
            "v4": "575 命题级活性锚，M5 规则已拦但被 diff 键吞（口径修正）",
            "v5": "578 _findings_key 并入文案后，587 起 1/1375（口径修正）",
            "v6": "588 发现器补全后 1/1379，被 v7 取代（口径修正）",
            "v7": "591 当前口径：589 T2 注释净化 un-mask 27 条 fixture 路径变异 ⇒ "
                  "M2 可判 141→168；唯一 escaped=1（M1/EV-CONC-001 冻结 TCE）",
        }
        conv = []
        for ver, why in baselines.items():
            p = ROOT / "data" / "mutation" / f"full_baseline_{ver}.json"
            if not p.is_file():
                continue
            d = json.loads(p.read_text(encoding="utf-8"))
            judged = d["blocked"] + d["escaped"]
            r = _cp(d["escaped"], judged)
            conv.append({
                "version": ver, "judged": judged, "n_a": d.get("n_a"),
                "numerator": r["numerator"], "denominator": r["denominator"],
                "point": r["point"], "cp_lower": r["cp_low"], "cp_upper": r["cp_high"],
                "note": why,
            })
        out["escape_rate_convergence"] = conv
        out["escape_rate_note"] = ("v1→v5 为口径修正（非同一量时间序列），v6→v7 为真实进展；"
                                   "不得声称单调收敛（仅 1 含曲线时点）；尺子变更史见各 version.note")
    except Exception as exc:                     # noqa: BLE001
        notes["escape_rate_convergence"] = f"采集失败：{type(exc).__name__}: {exc}"

    return out


def append(snap: dict, path: Path | None = None) -> Path:
    p = path or METRICS_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")
    return p


def read_history(path: Path | None = None) -> list[dict]:
    p = path or METRICS_FILE
    if not p.is_file():
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue                            # 半行/坏行不拖垮历史查询
        if isinstance(d, dict) and isinstance(d.get("metrics"), dict):
            out.append(d)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="质量度量 L1（508 任务6）")
    sub = ap.add_subparsers(dest="cmd")
    hi = sub.add_parser("history", help="看历史趋势")
    hi.add_argument("--last", type=int, default=10)
    hi.add_argument("--metrics", nargs="+",
                    default=["gate_block_count", "gate_warn_count", "poison_coverage_pct",
                             "replay_confirm_count", "atoms_verified", "git_ahead_count"])
    sub.add_parser("collect", help="采集一次（默认子命令）")
    ap.add_argument("--no-heavy", action="store_true", help="跳过 poison / replay（秒级）")
    ap.add_argument("--json", action="store_true", help="只打印，不落盘")
    # 573 任务 A-2：推翻事件**只接显式的人/异族动作**（系统绝不自动产生推翻）。
    ap.add_argument("--log-overturned", action="store_true",
                    help="写入一条推翻事件（须同时给 --target/--old/--new/--by/--reason）")
    ap.add_argument("--target", default="", help="被推翻的命题/卡 id（如 ATOM-MEM-MOVE-001/prop-1）")
    ap.add_argument("--old", default="", help="旧判决（如 confirm）")
    ap.add_argument("--new", default="", help="新判决（如 refute:xxx）")
    ap.add_argument("--by", default="", help="推翻者：`human:<名>`（须过 git 作者绑定）/ `adversary:<族>`")
    ap.add_argument("--reason", default="", help="推翻理由（必填，进事件流）")
    ap.add_argument("--card", default="", help="被推翻对象所在的卡（id 或路径），用于核验 human 签名")
    ap.add_argument("--out", default=None, help="覆盖 metrics.jsonl 路径")
    a = ap.parse_args(argv)

    if a.log_overturned:
        # 573 任务 A-2：只接**显式**的人/异族推翻动作（系统绝不自动产生推翻）。
        try:
            ev = log_overturned(a.target, a.old, a.new, a.by, a.reason,
                                card=a.card or None)
        except ValueError as exc:                        # fail-closed：不合规就拒绝写入
            print(f"[metrics] ❌ 拒绝写入推翻事件：{exc}", file=sys.stderr)
            return 2
        print(f"[metrics] 推翻事件已追加 {OVERTURNED_FILE.relative_to(ROOT).as_posix()}："
              f"{ev['target']} {ev['old_verdict']} → {ev['new_verdict']}（by {ev['by']}）")
        return 0

    if a.cmd == "history":
        rows = read_history(Path(a.out) if a.out else None)[-a.last:]
        if not rows:
            print("[metrics] 暂无历史（先跑一次 collect）")
            return 0
        names = [n for n in a.metrics if n in ALL_METRICS]
        print(f"{'timestamp':<20} " + " ".join(f"{n[:18]:>19}" for n in names))
        for r in rows:
            vals = " ".join(f"{str(r['metrics'].get(n)):>19}" for n in names)
            print(f"{r['timestamp']:<20} {vals}")
        return 0

    snap = collect(with_heavy=not a.no_heavy)
    if a.json:
        print(json.dumps(snap, ensure_ascii=False, indent=2))
        return 0
    p = append(snap, Path(a.out) if a.out else None)
    got = sum(1 for v in snap["metrics"].values() if v is not None)
    print(f"[metrics] 采集 {got}/{len(ALL_METRICS)} 项 → {p.relative_to(ROOT).as_posix()}")
    for al in snap["alerts"]:
        print(f"  [{al['level']:5}] {al['metric']}={al['value']}  {al['reason']}")
    if snap["notes"]:
        print("  注：" + "；".join(f"{k}:{v}" for k, v in snap["notes"].items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
