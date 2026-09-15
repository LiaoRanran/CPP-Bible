#!/usr/bin/env python3
"""412 成本追踪（421）：记录每颗原子的 token 消耗估算，建立 CPVA 基线。

没有测量就没有优化——本工具只记录、只读汇总，不改 gate/replay/poison 任何逻辑。

token 估算口径：tokens_est = chars / 3（中文 ~1.5 字/token、英文 ~4 字/token，混合取 3）。
估算不精确，但**相对值有意义**（不同原子/阶段的成本比例）。

用法：
  python tools/cost_tracker.py record --atom ATOM-MEM-RAII-001 --stage fixture --chars 15000
  python tools/cost_tracker.py record --atom ATOM-MEM-RAII-001 --stage redteam --chars 30000 --rounds 2
  python tools/cost_tracker.py report [--atom ATOM-MEM-RAII-001] [--json]
  python tools/cost_tracker.py cpva [--json]
  python tools/cost_tracker.py backfill --all      # 从 git log 回填存量原子（粗估）

阶段（530 T6 · 补全真实阶段）：
- **端到端链路** `E2E_STAGES = fixture → redteam → revision → human_review`：
  一颗原子从产出到人审的必经四步，report 的 `cpva_e2e` 只累这四步。
- **辅助阶段** `evidence_cards / gate_fix / other`：421 起沿用，口径不动（存量与测试在用）。
- `revision`（返修轮）为 T6 新增；每阶段除 `chars`/`windows` 外另记**轮次 `rounds`**
  （"改了几轮"是红队/返修的真实成本驱动，421 只有窗口数）。

向后兼容（T6 硬要求）：历史"仅 fixture"记录（27 条，无 `rounds`/`total_rounds` 键）
必须照读不崩，且 report/cpva 不丢原有数字（缺键按 0 计，不臆造）。

数据：data/cost/<atom_id>.json（入库作为历史基线）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v7.0"
COST_DIR = ge.ROOT / "data" / "cost"
# 全部合法阶段（含 421 的辅助阶段——存量记录与既有测试在用，T6 只增不删）
STAGES = ("fixture", "evidence_cards", "redteam", "revision", "gate_fix",
          "human_review", "other")
# 端到端（CPVA）真实阶段：一颗原子的必经链路，report 的 cpva_e2e 据此累加
E2E_STAGES = ("fixture", "redteam", "revision", "human_review")


def tokens_est(chars: int) -> int:
    """chars → token 估算（chars/3，见模块 docstring）。"""
    return int(round(chars / 3))


def _atom_file(atom_id: str) -> Path:
    return COST_DIR / f"{atom_id}.json"


def _load(atom_id: str) -> dict[str, Any]:
    f = _atom_file(atom_id)
    if f.is_file():
        return json.loads(f.read_text(encoding="utf-8"))
    return {"atom_id": atom_id, "created_at": _dt.date.today().isoformat(),
            "stages": {}}


def _totals(data: dict[str, Any]) -> dict[str, Any]:
    stages = data.get("stages") or {}
    chars = sum(int(s.get("chars") or 0) for s in stages.values())
    wins = sum(int(s.get("windows") or 0) for s in stages.values())
    mins = sum(int(s.get("duration_min") or 0) for s in stages.values())
    rounds = sum(int(s.get("rounds") or 0) for s in stages.values())
    data["total_chars"] = chars
    data["total_tokens_est"] = tokens_est(chars)
    data["total_windows"] = wins
    data["total_duration_min"] = mins
    data["total_rounds"] = rounds
    data["cpva"] = data["total_tokens_est"]
    return data


def record(atom_id: str, stage: str, chars: int, windows: int = 1,
           duration_min: int | None = None,
           rounds: int = 1) -> dict[str, Any]:
    """记录某原子某阶段的成本（同阶段多次记录取累加：chars/windows/rounds 皆累加）。

    `rounds` = 该阶段实际返修/执行轮次（T6 新增；红队/返修的成本驱动是"改了几轮"）。
    """
    if stage not in STAGES:
        raise SystemExit(f"[cost] 未知 stage：{stage}（取值 {STAGES}）")
    data = _load(atom_id)
    st = data["stages"].setdefault(stage, {"chars": 0, "windows": 0})
    st["chars"] += int(chars)
    st["windows"] += int(windows)
    st["tokens_est"] = tokens_est(st["chars"])
    st["rounds"] = int(st.get("rounds") or 0) + int(rounds)
    if duration_min is not None:
        st["duration_min"] = int(st.get("duration_min") or 0) + int(duration_min)
    COST_DIR.mkdir(parents=True, exist_ok=True)
    _atom_file(atom_id).write_text(
        json.dumps(_totals(data), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return data


def _stage_tokens(stages: dict[str, Any]) -> dict[str, int]:
    """阶段 → token 估算（缺键按 0，不臆造；兼容 421 老记录）。"""
    return {str(k): int((v or {}).get("tokens_est") or 0) for k, v in stages.items()}


def stage_share(stages: dict[str, Any]) -> dict[str, float]:
    """每阶段 token 占比（%，1 位小数）。总和为 0 ⇒ 全 0（不除零）。"""
    toks = _stage_tokens(stages)
    tot = sum(toks.values())
    if tot <= 0:
        return dict.fromkeys(toks, 0.0)
    return {k: round(v * 100.0 / tot, 1) for k, v in toks.items()}


def _atom_tokens(raw: dict[str, Any]) -> int:
    """单原子总 token：优先用落盘 `total_tokens_est`，缺失则由 stages 现算。"""
    v = raw.get("total_tokens_est")
    if v is not None:
        return int(v or 0)
    return sum(_stage_tokens(raw.get("stages") or {}).values())


def report(atom_id: str | None = None) -> dict[str, Any]:
    """单原子分阶段报告（含每阶段占比 + 端到端成本），或全部原子汇总。

    只读：返回的是**计算视图**，不写回文件、不改动调用方拿到的原始内容。
    """
    if atom_id:
        f = _atom_file(atom_id)
        if not f.is_file():
            raise SystemExit(f"[cost] 无成本数据：{atom_id}（先 record/backfill）")
        raw = json.loads(f.read_text(encoding="utf-8"))
        stages = dict(raw.get("stages") or {})
        toks = _stage_tokens(stages)
        out = dict(raw)
        out["stage_tokens_est"] = toks
        out["stage_share"] = stage_share(stages)
        # 端到端成本：只累 E2E_STAGES 上**已记录**的阶段（缺的阶段计 0）。
        # 与 total_tokens_est 分开给，一眼看出"只跑了 fixture 的半截成本"。
        out["cpva_e2e"] = sum(toks.get(s, 0) for s in E2E_STAGES)
        out["e2e_stages_recorded"] = [s for s in E2E_STAGES if s in stages]
        out["e2e_complete"] = all(s in stages for s in E2E_STAGES)
        out["total_rounds"] = int(
            raw["total_rounds"] if raw.get("total_rounds") is not None
            else sum(int((v or {}).get("rounds") or 0) for v in stages.values()))
        return out
    files = sorted(COST_DIR.glob("ATOM-*.json")) if COST_DIR.is_dir() else []
    datas = [(f, json.loads(f.read_text(encoding="utf-8"))) for f in files]
    by_atom: dict[str, int] = {}
    by_stage: dict[str, int] = {}
    rounds = 0
    for f, d in datas:
        by_atom[str(d.get("atom_id") or f.stem)] = _atom_tokens(d)
        stages = d.get("stages") or {}
        for s, v in _stage_tokens(stages).items():
            by_stage[s] = by_stage.get(s, 0) + v
        rounds += int(d["total_rounds"] if d.get("total_rounds") is not None
                      else sum(int((x or {}).get("rounds") or 0)
                               for x in stages.values()))
    total = sum(by_atom.values())
    n = len(datas)
    return {
        "tool": "cost_tracker", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "atoms": n,
        "total_tokens_est": total,
        "files": [f.name for f in files],
        # T6：每颗原子的端到端成本 + 每阶段占比（report 的成本会计部分）。
        # 注意与 cpva() 的同名键区分：这里 `stage_tokens_est` 是**阶段总量**，
        # cpva() 的 `cpva_by_stage` 是**阶段内每颗原子均值**（421 口径）。
        "cpva_per_atom": (total // n) if n else 0,
        "cpva_by_atom": by_atom,
        "stage_tokens_est": by_stage,
        "stage_share": stage_share({k: {"tokens_est": v} for k, v in by_stage.items()}),
        "total_rounds": rounds,
    }


def _avg(xs: list[int]) -> float:
    """列表均值；空列表 ⇒ 0.0（不除零）。"""
    return (sum(xs) / len(xs)) if xs else 0.0


def cpva() -> dict[str, Any]:
    """全局 CPVA：总量/按域/按阶段/趋势（最近 5 颗 vs 最早 5 颗）。

    T6 增补：`cpva_by_stage_total`（各阶段总 token）与 `cpva_by_stage_share`（占比）。
    注意 `cpva_by_stage` 保留 421 口径 = **阶段内每颗原子均值**（既有消费者在用），
    两者含义不同，勿混。
    """
    files = sorted(COST_DIR.glob("ATOM-*.json")) if COST_DIR.is_dir() else []
    datas = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    by_domain: dict[str, list[int]] = {}
    by_stage: dict[str, list[int]] = {}
    stage_total: dict[str, int] = {}
    rounds = 0
    for d in datas:
        dom = str(d.get("domain") or "unknown")
        by_domain.setdefault(dom, []).append(_atom_tokens(d))
        stages = d.get("stages") or {}
        for s, v in _stage_tokens(stages).items():
            by_stage.setdefault(s, []).append(v)
            stage_total[s] = stage_total.get(s, 0) + v
        rounds += int(d["total_rounds"] if d.get("total_rounds") is not None
                      else sum(int((x or {}).get("rounds") or 0)
                               for x in stages.values()))
    n = len(datas)
    total = sum(_atom_tokens(d) for d in datas)
    ordered = sorted(datas, key=lambda d: str(d.get("created_at") or ""))
    first5 = [_atom_tokens(d) for d in ordered[:5]]
    last5 = [_atom_tokens(d) for d in ordered[-5:]]
    trend = ("improving" if _avg(last5) < _avg(first5) * 0.95 else
             "worsening" if _avg(last5) > _avg(first5) * 1.05 else "stable")
    return {
        "tool": "cost_tracker", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "total_verified_atoms": n,
        "total_tokens_est": total,
        "cpva_overall": (total // n) if n else 0,
        "cpva_by_domain": {k: sum(v) // len(v) for k, v in sorted(by_domain.items())},
        "cpva_by_stage": {k: sum(v) // len(v) for k, v in sorted(by_stage.items())},
        "cpva_by_stage_total": dict(sorted(stage_total.items())),
        "cpva_by_stage_share": stage_share(
            {k: {"tokens_est": v} for k, v in sorted(stage_total.items())}),
        "cpva_first_5": int(_avg(first5)), "cpva_recent_5": int(_avg(last5)),
        "total_rounds": rounds,
        "trend": trend,
    }


def backfill(atom_id: str) -> dict[str, Any]:
    """从 git log 粗估单原子成本：commit 数≈窗口数，改动行数×40≈字符数。

    粗略估算（仅回填基线用）：行→字符按混合密度 40 字/行折算。
    """
    rels: list[str] = []
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        if str(ge._meta(p).get("id") or p.stem) == atom_id:
            rels.append(p.relative_to(ge.ROOT).as_posix())
    if not rels:
        raise SystemExit(f"[cost] 原子不存在：{atom_id}")
    meta = ge._meta(ge.ROOT / rels[0])
    out = {"chars": 0, "commits": 0}
    for rel in rels:
        r = subprocess.run(
            ["git", "log", "--follow", "--numstat", "--format=%h", "--", rel],
            capture_output=True, text=True, cwd=ge.ROOT)
        for ln in r.stdout.split("\n"):
            ln = ln.strip()
            if not ln:
                continue
            parts = ln.split("\t")
            if len(parts) >= 3 and parts[0].isdigit():
                out["chars"] += (int(parts[0]) + int(parts[1])) * 40
            elif len(parts) == 1:
                out["commits"] += 1          # %h 行（numstat 行必含 tab）
    data = _load(atom_id)
    data["domain"] = str(meta.get("domain") or "").lower()
    data["backfill"] = {"method": "git_log_numstat", **out}
    data["stages"]["fixture"] = {
        "chars": out["chars"], "windows": max(out["commits"], 1),
        "tokens_est": tokens_est(out["chars"])}
    COST_DIR.mkdir(parents=True, exist_ok=True)
    _atom_file(atom_id).write_text(
        json.dumps(_totals(data), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return data


def _print_report_text(r: dict[str, Any], atom_id: str | None) -> None:
    """人读摘要：每阶段占比 + 端到端成本（T6）。JSON 模式另走原路径。"""
    if atom_id:
        print(f"[cost] {atom_id} 端到端 {r.get('cpva_e2e', 0)} tok est"
              f"（总 {r.get('total_tokens_est', 0)} tok est · "
              f"轮次 {r.get('total_rounds', 0)}）"
              f" · E2E 齐全：{'是' if r.get('e2e_complete') else '否'}"
              f"（已记 {','.join(r.get('e2e_stages_recorded') or []) or '无'}）")
        print(f"  {'阶段':<16}{'tokens_est':>12}{'占比':>8}{'窗口':>6}{'轮次':>6}")
        stages = r.get("stages") or {}
        for s in sorted(stages, key=lambda k: -(r["stage_tokens_est"].get(k) or 0)):
            v = stages[s] or {}
            print(f"  {s:<16}{r['stage_tokens_est'].get(s, 0):>12}"
                  f"{r['stage_share'].get(s, 0.0):>7.1f}%"
                  f"{int(v.get('windows') or 0):>6}{int(v.get('rounds') or 0):>6}")
        return
    print(f"[cost] 原子 {r.get('atoms', 0)} 颗 · 总 {r.get('total_tokens_est', 0)} tok est"
          f" · 每颗端到端均值 {r.get('cpva_per_atom', 0)} tok est"
          f" · 轮次合计 {r.get('total_rounds', 0)}")
    print(f"  {'阶段':<16}{'tokens_est':>12}{'占比':>8}")
    for s, tok in sorted((r.get("stage_tokens_est") or {}).items(),
                         key=lambda kv: -kv[1]):
        print(f"  {s:<16}{tok:>12}{r['stage_share'].get(s, 0.0):>7.1f}%")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="成本追踪（412：先测量再优化）")
    # `--json` 同时挂在主解析器与各子命令（T6）：`cppbible cost report --json` 是
    # 把 flag 放在子命令**之后**的（tools/cppbible.py:650-654），只挂主解析器会
    # 报 unrecognized arguments。子命令侧用 SUPPRESS 避免其默认值反过来覆盖
    # 主解析器已解析出的 True（argparse 子解析器默认值会覆写同名 dest）。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    ap.add_argument("--json", action="store_true",
                    help="机器可读 JSON 输出（默认人读摘要）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    rec = sub.add_parser("record", parents=[common])
    rec.add_argument("--atom", required=True)
    rec.add_argument("--stage", required=True, choices=STAGES)
    rec.add_argument("--chars", type=int, required=True)
    rec.add_argument("--windows", type=int, default=1)
    rec.add_argument("--duration-min", type=int, default=None)
    rec.add_argument("--rounds", type=int, default=1,
                     help="该阶段返修/执行轮次（T6：红队/返修的真实成本驱动）")
    rep = sub.add_parser("report", parents=[common])
    rep.add_argument("--atom", default=None)
    sub.add_parser("cpva", parents=[common])
    bf = sub.add_parser("backfill", parents=[common])
    bf.add_argument("--all", action="store_true")
    bf.add_argument("--atom", default=None)
    a = ap.parse_args(argv)

    if a.cmd == "record":
        data = record(a.atom, a.stage, a.chars, a.windows, a.duration_min, a.rounds)
        print(json.dumps({"recorded": a.atom, "stage": a.stage,
                          "total_tokens_est": data["total_tokens_est"],
                          "total_rounds": data["total_rounds"]},
                         ensure_ascii=False))
    elif a.cmd == "report":
        r = report(a.atom)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            _print_report_text(r, a.atom)
    elif a.cmd == "cpva":
        r = cpva()
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=1))
        else:
            print(f"[cost] CPVA 总 {r['total_tokens_est']} tok est / "
                  f"{r['total_verified_atoms']} 颗 ⇒ 每颗 {r['cpva_overall']}"
                  f" · 轮次合计 {r['total_rounds']} · 趋势 {r['trend']}")
            print(f"  {'阶段':<16}{'每颗均值':>10}{'总token':>10}{'占比':>8}")
            for s, tot in r["cpva_by_stage_total"].items():
                print(f"  {s:<16}{r['cpva_by_stage'][s]:>10}{tot:>10}"
                      f"{r['cpva_by_stage_share'].get(s, 0.0):>7.1f}%")
    elif a.cmd == "backfill":
        ids = ([str(ge._meta(p).get("id") or p.stem)
                for p in ge._cards(ge.ATOMS, "ATOM-*.md")] if a.all else [a.atom])
        for aid in ids:
            d = backfill(aid)
            print(f"[cost] backfill {aid}: {d['total_tokens_est']} tok est "
                  f"({d['total_windows']} windows)")
    return 0


if __name__ == "__main__":
    main()
