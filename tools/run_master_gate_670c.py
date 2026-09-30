#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_master_gate_670c.py — 670c D1：主门禁（658 五阶段 + 669d 六条 + D2 守卫 + D3 漂移）。

为什么要有它
============
仓库里现在有三套门禁入口：658 编排器（run_658_gate.py）、669d 六条 P0 规则
（run_669d_gate.py）、以及本批新增的 D2 守卫 / D3 漂移监控。它们各自只有一个红绿，
合并前没有任何一处能回答「现在到底有几条红线是红的、有没有未登记的缺口」。
本工具把四者收敛成**一个**结论：overall / L0-L1 分层 / 未登记 BLOCK 数。

三条设计约定
============
1. **复用而不是复制**：
   * 669d 六条规则直接 import gate_rules_669d 现算，并用 import run_669d_gate 的
     load_gaps/classify —— known_gaps 的降级语义与冻结的 669d 入口**逐字一致**；
   * D2/D3 直接 import guard_rerun_670c / drift_watch_670c 调它们的纯函数；
   * 658 只能子进程调用（它是编排器，没有可导入的检查函数）⇒ 把子进程的 exit 与输出尾部
     解析进结论，并额外做一次 **AST 镜像校验**：把 run_658_gate.py 里的 stage() 调用
     （阶段名/层级/命令签名）解析出来，与本文件镜像的阶段表**逐条比对**。
     镜像对不上 ⇒ 直接 BLOCK（fail-closed）：宁可报「镜像过期」，也不静默少跑一条门禁。
2. **受控目录零写**：atoms/ evidence/ Examples/ Book/ 与 452 账本（decision_event_v2_ledger.jsonl
   等）在 --check 下前后各做一次 (mtime_ns, size) 快照；任何增删改 ⇒ 直接 BLOCK。
   本工具自身**不写任何仓库文件**（除非显式 --out 指定输出路径）。
3. **不覆盖任何既有产物**：658/669d 的门禁产物（data/658_gate_status.json、
   data/669d_gate_status.json、docs/669d_gate_report.md）本工具一律不写——它们是冻结件。

用法
====
    python tools/run_master_gate_670c.py                 # 跑全部，打印分层结论（只读）
    python tools/run_master_gate_670c.py --check         # 同上 + 受控目录零写校验（红即 BLOCK）
    python tools/run_master_gate_670c.py --json          # 机读输出
    python tools/run_master_gate_670c.py --out build/master_gate_670c.json   # 落一份状态（CI 用）
    python tools/run_master_gate_670c.py --selftest      # 只读自检（镜像/解析/分层）

退出码
======
    0 = overall PASS（无 L0 失败、无未登记 BLOCK）
    1 = overall FAIL（L0 失败 / 未登记 BLOCK / 受控目录被写）

已知限制（诚实登记）
====================
* 658 阶段是**子进程**调用，其内部写盘行为不由本工具控制；--check 的受控目录快照只覆盖
  白名单目录与 452 账本文件，不覆盖 data/ 下各工具自己的报告（那是它们声明的产物）。
* 669d 的 known_gaps 降级语义沿用冻结入口：**只降级已登记项**，新 BLOCK 一律红。
* 单次运行总耗时取决于 658 的 pytest 子集与两处导入；本工具不并发（避免与 replay 争抢）。
"""
from __future__ import annotations

import argparse
import ast
import glob
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

SCHEMA = "queyi-master-gate/v1"
GATE_ID = "670c"
L0, L1 = "L0", "L1"

#: 受控目录（红线：本批零写）
CONTROLLED_DIRS = ("atoms", "evidence", "Examples", "Book")
#: 452 账本及其同源派生物（红线：零改）
CONTROLLED_FILES = (
    "data/authority/decision_event_v2_ledger.jsonl",
    "data/authority/decision_event_v2_ledger_backfilled_652.jsonl",
    "data/authority/decision_event_v2_ledger_remapped.jsonl",
    "data/646_authority_rule_annotation.jsonl",
)


# ─────────────────────────────────────────────────────────────────────────────
# 658 镜像表（与 tools/run_658_gate.py 的 stage() 调用逐条对应；由 mirror_658() 校验）
# ─────────────────────────────────────────────────────────────────────────────

STAGES_658: list[dict[str, Any]] = [
    {"id": "658/S0", "name": "S0 元状态对账", "tier": L0,
     "sig": ["tools/status_reconciler_658.py", "--check"], "timeout": 600},
    {"id": "658/S1", "name": "S1 门禁分层合法", "tier": L0,
     "sig": ["tools/gate_tier_check_658.py", "--check"], "timeout": 600},
    {"id": "658/S2", "name": "S2 真实缺陷检出", "tier": L0,
     "sig": ["tools/defect_fixture_658.py", "--rate"], "timeout": 600},
    {"id": "658/S3", "name": "S3 盲化 holdout", "tier": L0,
     "sig": ["tools/holdout_658.py", "--status"], "timeout": 600},
    {"id": "658/S4", "name": "S4 边界 provenance", "tier": L1,
     "sig": ["tools/boundary_scope_658.py", "--report"], "timeout": 600},
    {"id": "658/S6", "name": "S6 单元测试(658)", "tier": L0,
     "sig": ["-m", "pytest", "-q", "-p", "no:cacheprovider"], "timeout": 900,
     "glob": "tests/*658*.py"},
]
#: S5 不是子进程（run_658_gate.research_check()），单列出来做镜像的存在性校验
STAGE_658_RESEARCH = {"id": "658/S5", "name": "S5 research 骨架", "tier": L1}


def _script_658(root: Path) -> Path:
    return root / "tools" / "run_658_gate.py"


def _const_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def extract_658_stages(src: str) -> tuple[list[dict[str, Any]], bool]:
    """从 run_658_gate.py 源码解析出 stage(...) 阶段表与是否存在 research_check()。

    返回 (阶段列表, 是否有 research 阶段)。解析不出任何 stage() ⇒ 返回 ([], False)，
    调用方按 **fail-closed** 处理（宁可报错，不可静默少跑）。
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return [], False
    stages: list[dict[str, Any]] = []
    has_research = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fname = node.func.id if isinstance(node.func, ast.Name) else None
        if fname == "research_check":
            has_research = True
            continue
        if fname != "stage" or len(node.args) < 3:
            continue
        name, tier = _const_str(node.args[0]), _const_str(node.args[1])
        cmd = node.args[2]
        if isinstance(cmd, ast.BinOp):            # [PY, ...] + tests
            cmd = cmd.left
        sig: list[str] = []
        if isinstance(cmd, ast.List):
            sig = [v for v in (_const_str(e) for e in cmd.elts) if v is not None]
        stages.append({"name": name, "tier": tier, "sig": sig})
    return stages, has_research


def mirror_658(root: Path) -> dict[str, Any]:
    """镜像校验：本文件的 STAGES_658 必须与 run_658_gate.py 的 stage() 调用逐条一致。

    为什么值得这一步：658 门禁是冻结件（本批红线不许改它），但**冻结不等于不会变**——
    后续若给它加一条阶段，主门禁若不自知就会「少跑一条还报绿」。
    这里把「少跑」变成显式 BLOCK。
    """
    p = _script_658(root)
    problems: list[str] = []
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"ok": False, "problems": [f"读不到 {p.name}：{e}"], "extracted": 0}
    got, has_research = extract_658_stages(src)
    if not got:
        return {"ok": False, "extracted": 0,
                "problems": ["无法从 run_658_gate.py 解析出任何 stage() 调用 ⇒ "
                             "镜像校验未生效（fail-closed 判红）"]}
    want = [{"name": s["name"], "tier": s["tier"], "sig": list(s["sig"])} for s in STAGES_658]
    if len(got) != len(want):
        problems.append(f"阶段条数不一致：658 源={len(got)} 本镜像={len(want)}")
    for i, (g, w) in enumerate(zip(got, want)):
        if (g["name"], g["tier"], g["sig"]) != (w["name"], w["tier"], w["sig"]):
            problems.append(f"第 {i + 1} 条阶段不一致：源={g} 镜像={w}")
    if not has_research:
        problems.append("658 源里没有 research_check() ⇒ 镜像的 S5 阶段已失效")
    return {"ok": not problems, "extracted": len(got), "has_research": has_research,
            "problems": problems}


# ─────────────────────────────────────────────────────────────────────────────
# 受控目录快照（--check 的零写校验）
# ─────────────────────────────────────────────────────────────────────────────

def snapshot_controlled(root: Path) -> dict[str, list[int]]:
    """受控目录 + 452 账本文件的 (mtime_ns, size) 快照。只读。"""
    out: dict[str, list[int]] = {}
    for rel in CONTROLLED_DIRS:
        d = root / rel
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            try:
                st = p.stat()
            except OSError:
                continue
            out[p.relative_to(root).as_posix()] = [st.st_mtime_ns, st.st_size]
    for rel in CONTROLLED_FILES:
        p = root / rel
        if p.is_file():
            st = p.stat()
            out[rel] = [st.st_mtime_ns, st.st_size]
    return out


def diff_controlled(before: dict[str, list[int]], after: dict[str, list[int]]) -> dict[str, list[str]]:
    return {
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "modified": sorted(k for k in set(before) & set(after) if before[k] != after[k]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 门禁执行
# ─────────────────────────────────────────────────────────────────────────────

def run_stage(argv: list[str], root: Path, timeout: int = 600) -> tuple[int, str]:
    """子进程执行一个阶段（测试可 monkeypatch 这个 seam）。返回 (exit, 输出尾部)。"""
    cmd = [sys.executable, *argv]
    try:
        r = subprocess.run(cmd, cwd=str(root), capture_output=True, text=True,
                           errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return 99, f"EXC: {type(e).__name__}: {e}"
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-600:]


def gate(id_: str, name: str, tier: str, ok: bool, exit_: int = 0,
         cmd: str = "", detail: str = "", tail: str = "") -> dict[str, Any]:
    return {"id": id_, "name": name, "tier": tier, "pass": bool(ok),
            "exit": exit_, "cmd": cmd, "detail": detail, "tail": tail}


def research_gate(root: Path) -> dict[str, Any]:
    """S5：优先复用 run_658_gate.research_check()（真复用其 16 项清单）。"""
    try:
        import run_658_gate as R658  # noqa: PLC0415
        if Path(R658.ROOT).resolve() == root.resolve():
            st = R658.research_check()
            return gate(STAGE_658_RESEARCH["id"], STAGE_658_RESEARCH["name"],
                        STAGE_658_RESEARCH["tier"], bool(st["pass"]), int(st["exit"]),
                        str(st["cmd"]), str(st["tail"])[:200])
    except Exception as e:                       # noqa: BLE001  降级而不是崩
        _ = e
    req = ["PROTOCOL_v0.1.md", "00_problem.md", "01_research_questions.md", "02_hypotheses.md",
           "03_system_boundary.md", "04_threat_model.md", "05_evaluation_protocol.md",
           "06_datasets.md", "07_baselines.md", "08_metrics.md", "09_ablations.md",
           "10_analysis_plan.md", "11_reproducibility.md", "12_threats_to_validity.md",
           "13_ai_use_and_authorship.md", "CHANGELOG.md"]
    miss = [f for f in req if not (root / "research" / f).is_file()]
    return gate(STAGE_658_RESEARCH["id"], STAGE_658_RESEARCH["name"], STAGE_658_RESEARCH["tier"],
                not miss, 1 if miss else 0, "存在性: research/*.md",
                ("降级路径（非本仓根 ⇒ 未复用 run_658_gate.research_check）" if miss else
                 "降级路径：16/16 存在"))


def gates_658(root: Path) -> list[dict[str, Any]]:
    """658 五条子进程阶段 + S5 research + 镜像校验（按镜像表执行）。"""
    out: list[dict[str, Any]] = []
    for s in STAGES_658:
        argv = list(s["sig"])
        if s.get("glob"):
            files = sorted(glob.glob(str(root / s["glob"])))
            if not files:
                g = gate(s["id"], s["name"], s["tier"], True, 0,
                         f"glob={s['glob']}", "无匹配测试文件 ⇒ 跳过（不计入 L0 分母）")
                g["skipped"] = True
                out.append(g)
                continue
            argv = argv + files
        code, tail = run_stage(argv, root, int(s.get("timeout", 600)))
        out.append(gate(s["id"], s["name"], s["tier"], code == 0, code,
                        " ".join(["python", *argv[:2]]), tail[-300:], tail))
    out.append(research_gate(root))
    m = mirror_658(root)
    out.append(gate("658/mirror", "658 阶段镜像校验", L0, bool(m["ok"]), 0 if m["ok"] else 1,
                    "AST 解析 tools/run_658_gate.py",
                    f"解析出 {m['extracted']} 条 stage()"
                    + ("；" + "；".join(m["problems"]) if m["problems"] else "；与本镜像一致")))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 669d 六条（复用冻结入口的规则与 known_gaps 降级语义）
# ─────────────────────────────────────────────────────────────────────────────

def load_gaps_for(root: Path) -> dict[str, dict]:
    """复用 run_669d_gate.load_gaps 的**解析与键格式**，只把 GAPS_PATH 指向指定 root。

    为什么不自己再解析一遍：键格式（rule|target）与「只降级已登记项」的语义必须与冻结的
    669d 入口**逐字一致**，一旦各写一份，两处判定迟早分叉（这正是本批要堵的形态）。
    这里只临时改模块常量并在 finally 还原，不写任何文件。
    """
    import run_669d_gate as RG  # noqa: PLC0415
    real = RG.GAPS_PATH
    try:
        RG.GAPS_PATH = root / "data" / "669d_known_gaps.json"
        return RG.load_gaps()
    finally:
        RG.GAPS_PATH = real


def gates_669d(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """669d 六条规则（按注册表分层）+ known_gaps 降级。返回 (门禁列表, findings 汇总)。"""
    try:
        import gate_rules_669d as G  # noqa: PLC0415
        import run_669d_gate as RG  # noqa: PLC0415  只 import：main() 有写盘副作用，绝不调
    except Exception as e:                       # noqa: BLE001
        g = gate("669d/import", "669d 规则模块导入", L0, False, 1,
                 "import gate_rules_669d / run_669d_gate",
                 f"导入失败：{type(e).__name__}: {e}")
        return [g], {"unregistered_blocks": [], "registered_gaps": [], "warns": []}

    findings = G.run_all(root)
    new_blocks, accepted, warns = RG.classify(findings, load_gaps_for(root))
    out: list[dict[str, Any]] = []
    for r in G.RULES669D:
        rid = str(r["id"])
        n_new = sum(1 for f in new_blocks if f["rule"] == rid)
        n_acc = sum(1 for f in accepted if f["rule"] == rid)
        n_all = sum(1 for f in findings if f["rule"] == rid)
        out.append(gate(f"669d/{rid}", str(r["name"]), str(r["tier"]), n_new == 0,
                        0 if n_new == 0 else 1, f"gate_rules_669d.py --rule {rid}",
                        f"findings={n_all} 未登记BLOCK={n_new} 已登记缺口={n_acc}"))
    todo = [g for g in (accepted if isinstance(accepted, list) else [])
            if "TODO" in str(g.get("gap_reason", ""))]
    out.append(gate("669d/gaps-registered", "669d 已登记缺口（降级 WARN）", L1, not todo,
                    0 if not todo else 1, "data/669d_known_gaps.json",
                    f"已登记 {len(accepted)} 条；reason 仍为 TODO 的 {len(todo)} 条"))
    return out, {"unregistered_blocks": new_blocks, "registered_gaps": accepted,
                 "warns": warns}


# ─────────────────────────────────────────────────────────────────────────────
# D2 / D3（直接复用两个新工具的纯函数，不经过子进程）
# ─────────────────────────────────────────────────────────────────────────────

def gates_guard(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """D2：改了代码没重跑产物（L0）；基线是否已标定为 L1 提示项。"""
    try:
        import guard_rerun_670c as Guard  # noqa: PLC0415
    except Exception as e:                       # noqa: BLE001
        return [gate("670c/D2-guard", "D2 守卫导入", L0, False, 1, "import guard_rerun_670c",
                     f"{type(e).__name__}: {e}")], {}
    res = Guard.evaluate(root, root / "data" / "guard_rerun_baseline_670c.json")
    red = res["overall"] == "RED"
    g1 = gate("670c/D2-guard", "D2 改了代码没重跑产物守卫", L0, not red, 1 if red else 0,
              "guard_rerun_670c.evaluate()",
              f"overall={res['overall']} stale={res['counts']['stale']} "
              f"rerun={res['counts']['rerun']} warn={res['counts']['warn']}")
    g2 = gate("670c/D2-guard-armed", "D2 守卫已标定（有基线才能判红）", L1,
              bool(res["baseline_found"]), 0 if res["baseline_found"] else 2,
              "data/guard_rerun_baseline_670c.json",
              ("基线已标定" if res["baseline_found"] else "无基线 ⇒ 未进射程（先跑 --update 标定）"))
    return [g1, g2], res


def gates_drift(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """D3：关键数字漂移（L1 advisory，不阻断；报告由 drift_watch 自己落盘）。"""
    try:
        import drift_watch_670c as Drift  # noqa: PLC0415
    except Exception as e:                       # noqa: BLE001
        return [gate("670c/D3-drift", "D3 漂移监控导入", L1, False, 1, "import drift_watch_670c",
                     f"{type(e).__name__}: {e}")], {}
    rep = Drift.evaluate(root, None, Drift.DEFAULT_THRESHOLD, write=False)
    bad = len(rep["drifted_unjustified"])
    return [gate("670c/D3-drift", "D3 关键数字漂移（越阈值且无实验记录）", L1, bad == 0,
                 0 if bad == 0 else 1, "drift_watch_670c.evaluate(write=False)",
                 f"overall={rep['overall']} 越阈值未认领={bad} "
                 f"有实验记录={len(rep['drifted_justified'])} 指标={len(rep['values'])}")], rep


# ─────────────────────────────────────────────────────────────────────────────
# 670g：论文管线五工具（md↔tex 数字 / bib / 图表溯源 / 匿名化 / 质量门禁）
# ─────────────────────────────────────────────────────────────────────────────

PAPER_PIPELINE: list[tuple[str, str, str]] = [
    ("paper-sync", "tools/paper_sync_check_670c2.py", "论文 md↔tex 数字一致性"),
    ("paper-bib", "tools/bib_audit_670c2.py", "BibTeX 完整性审计"),
    ("paper-figdata", "tools/figure_data_check_670c2.py", "图表数据溯源"),
    ("paper-anon", "tools/anonymity_check_670c2.py", "投稿匿名化检查"),
    ("paper-quality", "tools/paper_quality_gate_670c2.py", "论文质量门禁"),
]


def paper_pipeline_gate(root: Path) -> list[dict[str, Any]]:
    """670g：把论文管线五工具挂进门禁（L1；工具缺失则跳过而非崩）。"""
    out: list[dict[str, Any]] = []
    for tid, rel, name in PAPER_PIPELINE:
        if not (root / rel).is_file():
            out.append(gate(f"670g/{tid}", name, L1, True, 0, rel, "工具不存在 ⇒ 跳过"))
            continue
        code, tail = run_stage([rel], root, 300)
        out.append(gate(f"670g/{tid}", name, L1, code == 0, code, rel, tail[-300:]))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 汇总
# ─────────────────────────────────────────────────────────────────────────────

def collect(root: Path = ROOT, check_mode: bool = False, timeout: int | None = None) -> dict[str, Any]:
    """跑全部门禁并汇总成一份机读状态。**不写任何文件**。"""
    if timeout is not None:
        for s in STAGES_658:
            s["timeout"] = int(timeout)
    before = snapshot_controlled(root) if check_mode else None
    gates: list[dict[str, Any]] = []
    gates += gates_658(root)
    g669, findings = gates_669d(root)
    gates += g669
    gguard, guard_res = gates_guard(root)
    gates += gguard
    gdrift, drift_res = gates_drift(root)
    gates += gdrift
    gates += paper_pipeline_gate(root)

    controlled: dict[str, Any] = {
        "checked": bool(check_mode), "files": len(before or {}),
        "write_detected": 0, "diff": {"added": [], "removed": [], "modified": []},
    }
    if check_mode:
        after = snapshot_controlled(root)
        d = diff_controlled(before or {}, after)
        n = len(d["added"]) + len(d["removed"]) + len(d["modified"])
        controlled.update(write_detected=n, diff=d, files_after=len(after))
        gates.append(gate("670c/controlled-dirs", "受控目录零写（atoms/evidence/Examples/Book + 452 账本）",
                          L0, n == 0, 0 if n == 0 else 1, "--check 前后快照比对",
                          f"快照 {len(before or {})} 文件；写入 {n} 处"))

    l0 = [g for g in gates if g["tier"] == L0]
    l1 = [g for g in gates if g["tier"] == L1]
    l0_fail = [g for g in l0 if not g["pass"]]
    l1_fail = [g for g in l1 if not g["pass"]]
    n_block = len(findings.get("unregistered_blocks", []))
    overall = "PASS" if (not l0_fail and n_block == 0) else "FAIL"
    return {
        "schema": SCHEMA, "gate": GATE_ID,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "check" if check_mode else "run",
        "root": str(root),
        "overall": overall,
        "l0_pass": sum(1 for g in l0 if g["pass"]), "l0_total": len(l0),
        "l1_pass": sum(1 for g in l1 if g["pass"]), "l1_total": len(l1),
        "unregistered_blocks": n_block,
        "registered_gaps": len(findings.get("registered_gaps", [])),
        "warns": len(findings.get("warns", [])),
        "fail_l0": [g["id"] for g in l0_fail], "fail_l1": [g["id"] for g in l1_fail],
        "gates": gates,
        "findings": {"unregistered_blocks": findings.get("unregistered_blocks", []),
                     "registered_gaps": findings.get("registered_gaps", []),
                     "warns": findings.get("warns", [])},
        "guard": guard_res, "drift": drift_res,
        "controlled_dirs": controlled,
        "notes": ["658 走子进程并做 AST 镜像校验；669d/D2/D3 走 in-process 复用（不调各自入口的 main()）。",
                  "本工具不写任何仓库文件（--out 除外）；658/669d 的冻结产物一律不覆盖。"],
    }


def render(st: dict[str, Any]) -> str:
    L = [f"[670c master gate] overall={st['overall']}  L0 {st['l0_pass']}/{st['l0_total']}  "
         f"L1 {st['l1_pass']}/{st['l1_total']}  未登记BLOCK={st['unregistered_blocks']}  "
         f"已登记缺口={st['registered_gaps']}  WARN={st['warns']}  (mode={st['mode']})"]
    for g in st["gates"]:
        L.append(f"  [{'PASS' if g['pass'] else 'FAIL'}] {g['tier']} {g['id']:28} {g['detail']}")
    for f in st["findings"]["unregistered_blocks"][:10]:
        L.append(f"  [BLOCK] {f['rule']} {f['target']}")
        L.append(f"          {f['message']}")
    if st["controlled_dirs"]["checked"]:
        c = st["controlled_dirs"]
        L.append(f"  受控目录快照 {c['files']} 文件 · 写入 {c['write_detected']} 处")
    for n in st["notes"]:
        L.append(f"  [note] {n}")
    return "\n".join(L)


def selftest() -> int:
    """只读自检：镜像解析、分层取值、受控目录 diff、669d 门禁名一致性。"""
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    m = mirror_658(ROOT)
    chk(f"658 镜像一致（解析出 {m['extracted']} 条 stage）", bool(m["ok"]))
    fake = 'def f():\n    stage("X", "L0", [PY, "tools/x.py", "--check"])\n    research_check()\n'
    stages, has_research = extract_658_stages(fake)
    chk("AST 解析合成源码", len(stages) == 1 and stages[0]["name"] == "X"
        and stages[0]["sig"] == ["tools/x.py", "--check"] and has_research)
    chk("解析空源码 ⇒ fail-closed", extract_658_stages("") == ([], False))
    chk("门禁分层取值合法", all(g["tier"] in (L0, L1) for g in gates_658(ROOT)))
    before = {"a": [1, 2]}
    d = diff_controlled(before, {"a": [1, 3], "b": [1, 1]})
    chk("受控目录 diff 能识别新增/改动", d["modified"] == ["a"] and d["added"] == ["b"])
    try:
        import gate_rules_669d as G  # noqa: PLC0415
        ids = [str(r["id"]) for r in G.RULES669D]
        chk("669d 六条门禁名与规则注册表一致", len(ids) == 6 and all(ids))
    except Exception as e:                       # noqa: BLE001
        chk(f"669d 规则注册表可导入（{e}）", False)
    print(f"run_master_gate_670c selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="670c D1：658 + 669d 六条 + D2/D3 主门禁")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件上级目录；测试用）")
    ap.add_argument("--check", action="store_true", help="受控目录零写校验（前后快照）")
    ap.add_argument("--json", action="store_true", help="机读 JSON 输出")
    ap.add_argument("--out", default=None, help="把状态 JSON 写到指定路径（唯一写盘路径）")
    ap.add_argument("--timeout", type=int, default=None, help="覆盖各 658 阶段超时（秒）")
    ap.add_argument("--selftest", action="store_true", help="只读自检")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    root = Path(a.root).resolve() if a.root else ROOT
    st = collect(root, check_mode=a.check, timeout=a.timeout)
    if a.json:
        print(json.dumps(st, ensure_ascii=False, indent=2))
    else:
        print(render(st))
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if st["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
