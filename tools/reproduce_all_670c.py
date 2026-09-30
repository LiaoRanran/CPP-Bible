#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""reproduce_all_670c.py — 670c B2：一键复现编排器（论文投稿用的独立复现入口）。

为什么需要它
============
REPLICATION.md 把每条复现命令写成**文字**。文字有三个问题：

  ① 读者要手工按顺序跑、手工对数字 —— 漏跑一步没人发现，抄错一个数字也没人发现；
  ② 某一步失败后，后面还跑不跑？Shell 脚本一律 `set -e` 停住 ⇒ 一次只能修一个问题；
  ③ "这条命令的预期输出是什么"散落在文档里，而预期数字的**事实源**在 `data/*.json` 里
     —— 两处一定会漂（669 的审计就是被这条打中的）。

本工具把 7 步串成一条**不中断**的流水线：每步记录开始/结束时间、命令、退出码、
stdout/stderr 摘要，并**与 check 表逐条对账**。某步失败**不中断**后面 ——
一次跑完能同时看到 7 步的红绿，而不是修一步跑一次。

产物安全（本仓红线）
====================
本仓有批次的产物是**冻结**的（669d 文件冻结；670c 段不得改 658/669d 的产物）。故：

* 669d 门禁一律加 `--no-write`（只打印，不覆写 669d 的 status/report）；
* 变异步骤只加 `--json`（不加 `--report`）⇒ 不覆写 656 的两份报告；
* 其它会写盘的工具，其产物在**跑之前逐字节备份**，跑完在 `finally` 里**原样还原**
  （`--keep-outputs` 可关掉还原，供复现者在自己 clone 里留下新产物）。

报告里给出每个受保护产物的 sha256（before / after / restored），还原与否可复核，不靠口头保证。

两种模式
========
`--mode verify`（**默认**）：**不跑**工具，只读它们已落盘的产物并与 check 表对账。
  为什么默认它：本仓是 670a/670b/670c **并行工作区**，默认就跑全套会与别人抢同一批文件；
  verify 模式秒级返回，回答"我这份 clone 的数字与论文一致吗"。
`--mode run`：真跑每一步（复现者在自己 clone 里要用这个）。

用法与退出码
============
    python tools/reproduce_all_670c.py --list
    python tools/reproduce_all_670c.py                          # verify（默认）
    python tools/reproduce_all_670c.py --mode run --skip-slow
    python tools/reproduce_all_670c.py --mode run --only S3_holdout_reveal,S7_counterfactual
    python tools/reproduce_all_670c.py --mode run --keep-outputs

退出码：0 = 跑到的步骤全部匹配；1 = 有步骤失败/不匹配；2 = 参数错（未知 step id / 清单非法）。

诚实边界
========
* 慢步骤（变异、全量 fast pytest）用 `--skip-slow` 跳过时，报告里 `overall` 记 `PARTIAL`，
  **不**把"没跑"写成"通过"。
* `--mode run` 会真编译真运行（WSL sanitizer）；缺 WSL 时相关样本降级为 unknown，
  报率会掉而门禁仍绿 —— 这正是要显形的环境依赖，见 REPLICATION.md 的 WSL 一节。
* 本工具**不修**任何东西：对不上就记 FAIL，不自动改产物、不自动改预期值。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parents[1]
OUT_REL = "data/reproduction_report_670c.json"
SCHEMA = "queyi-reproduction-report/670c"
PY = sys.executable

#: 每步的执行超时（秒）。真编译 + 变异是分钟级，故给足；超时记 timeout 而**不**中断后面。
T_DEFAULT = 900
T_MUTATION = 3600
T_PYTEST = 3600

#: 658 门禁与 669d 门禁的"当前状态"事实源（verify 模式读它们）。
STEPS: list[dict] = [
    {
        "id": "S1_gate_658",
        "name": "658 验收门禁（L0 5/5）",
        "why": "L0 红线：元状态对账 / 门禁分层合法 / 真实缺陷检出 / holdout 盲态 / 658 单元测试。",
        "slow": False,
        "cmd": [PY, "tools/run_658_gate.py"],
        "writes": ["data/658_gate_status.json", "data/658_gate_report.md"],
        "timeout": T_DEFAULT,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
            {"mode": "run", "kind": "stdout_re", "value": r"overall=PASS\s+L0 5/5",
             "desc": "stdout 含 overall=PASS 且 L0 5/5"},
            {"mode": "verify", "kind": "artifact", "path": "data/658_gate_status.json",
             "jsonpath": "overall", "value": "PASS", "desc": "落盘 status.overall=PASS"},
            {"mode": "verify", "kind": "artifact", "path": "data/658_gate_status.json",
             "jsonpath": "l0_pass", "value": 5, "desc": "l0_pass=5"},
            {"mode": "verify", "kind": "artifact", "path": "data/658_gate_status.json",
             "jsonpath": "l0_total", "value": 5, "desc": "l0_total=5"},
        ],
    },
    {
        "id": "S2_gate_669d",
        "name": "669d 六条 P0 门禁（--no-write）",
        "why": "669d 的六条 P0 规则；加 --no-write 是为了不覆写冻结的 669d 产物。",
        "slow": False,
        "cmd": [PY, "tools/run_669d_gate.py", "--no-write"],
        "writes": [],
        "timeout": T_DEFAULT,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0（无未登记 BLOCK）"},
            {"mode": "run", "kind": "stdout_re", "value": r"overall=PASS", "desc": "stdout 含 overall=PASS"},
            {"mode": "verify", "kind": "artifact", "path": "data/669d_gate_status.json",
             "jsonpath": "overall", "value": "PASS", "desc": "落盘 status.overall=PASS"},
            {"mode": "verify", "kind": "artifact", "path": "data/669d_gate_status.json",
             "jsonpath": "new_blocks", "value": [], "desc": "未登记 BLOCK 为空"},
        ],
    },
    {
        "id": "S3_holdout_reveal",
        "name": "holdout reveal_3（14/16 = 87.5%）",
        "why": "论文的 holdout 检出率；sanitizer 类走 WSL 真机编译并运行（-O0 + -O2 双档）。",
        "slow": False,
        "cmd": [PY, "tools/holdout_reveal_3_665.py"],
        "writes": ["data/holdout_reveal_3_665.json", "data/holdout/reveal_3_detail_668.json"],
        "timeout": T_DEFAULT,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
            {"mode": "run", "kind": "stdout_re", "value": r"检出率=87\.5%", "desc": "stdout 含 检出率=87.5%"},
            {"mode": "both", "kind": "artifact", "path": "data/holdout_reveal_3_665.json",
             "jsonpath": "error_subset.catch", "value": 14, "desc": "error_subset.catch=14"},
            {"mode": "both", "kind": "artifact", "path": "data/holdout_reveal_3_665.json",
             "jsonpath": "denominator.value", "value": 16, "desc": "分母（catch+miss）=16"},
            {"mode": "both", "kind": "artifact", "path": "data/holdout_reveal_3_665.json",
             "jsonpath": "error_subset.detect_rate_pct", "value": 87.5, "desc": "detect_rate_pct=87.5"},
            {"mode": "both", "kind": "artifact", "path": "data/holdout_reveal_3_665.json",
             "jsonpath": "control_subset.false_positive", "value": 1, "desc": "对照组误报=1"},
        ],
    },
    {
        "id": "S4_external_corpus",
        "name": "external corpus reveal（14/32 = 43.8% / 全样本 35.0%）",
        "why": "论文的 external 检出率；两个口径同时给（可测口径 vs 全样本口径）。",
        "slow": False,
        "cmd": [PY, "tools/external_corpus_reveal_665.py"],
        "writes": ["data/external_corpus_reveal_665.json"],
        "timeout": T_DEFAULT,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
            {"mode": "run", "kind": "stdout_re", "value": r"检出率=43\.8%", "desc": "stdout 含 检出率=43.8%"},
            {"mode": "both", "kind": "artifact", "path": "data/external_corpus_reveal_665.json",
             "jsonpath": "catch", "value": 14, "desc": "catch=14"},
            {"mode": "both", "kind": "artifact", "path": "data/external_corpus_reveal_665.json",
             "jsonpath": "denominator.value", "value": 32, "desc": "可测分母=32"},
            {"mode": "both", "kind": "artifact", "path": "data/external_corpus_reveal_665.json",
             "jsonpath": "detect_rate_pct", "value": 43.8, "desc": "可测口径=43.8%"},
            {"mode": "both", "kind": "artifact", "path": "data/external_corpus_reveal_665.json",
             "jsonpath": "rate_pct_all_samples", "value": 35.0, "desc": "全样本口径=35.0%"},
        ],
    },
    {
        "id": "S5_mutation_core",
        "name": "内部变异测试 core（110/147 = 97.3%）",
        "why": "证明测试套件对核心判决路径有杀伤力。这是**内部指标**，不是缺陷检测率。",
        "slow": True,
        "cmd": [PY, "tools/mutation_test_656.py", "--scope", "core", "--limit", "450", "--json"],
        "writes": [],
        "timeout": T_MUTATION,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0（基线必绿才给检出率）"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "mutants", "value": 147,
             "desc": "stdout JSON mutants=147"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "killed", "value": 110,
             "desc": "stdout JSON killed=110"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "kill_rate_on_scored", "value": 97.3,
             "desc": "stdout JSON kill_rate_on_scored=97.3"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_core.json",
             "jsonpath": "mutants", "value": 147, "desc": "落盘 mutants=147"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_core.json",
             "jsonpath": "killed", "value": 110, "desc": "落盘 killed=110"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_core.json",
             "jsonpath": "kill_rate_on_scored", "value": 97.3, "desc": "落盘检出率=97.3"},
        ],
    },
    {
        "id": "S6_mutation_all",
        "name": "内部变异测试 all（128/223 = 81.5%）",
        "why": "同上，作用域换成整文件抽样。两个作用域都给，不许只报好看的那个。",
        "slow": True,
        "cmd": [PY, "tools/mutation_test_656.py", "--scope", "all", "--limit", "300", "--json"],
        "writes": [],
        "timeout": T_MUTATION,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "mutants", "value": 223,
             "desc": "stdout JSON mutants=223"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "killed", "value": 128,
             "desc": "stdout JSON killed=128"},
            {"mode": "run", "kind": "stdout_json", "jsonpath": "kill_rate_on_scored", "value": 81.5,
             "desc": "stdout JSON kill_rate_on_scored=81.5"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_all.json",
             "jsonpath": "mutants", "value": 223, "desc": "落盘 mutants=223"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_all.json",
             "jsonpath": "killed", "value": 128, "desc": "落盘 killed=128"},
            {"mode": "verify", "kind": "artifact", "path": "data/656_mutation_report_all.json",
             "jsonpath": "kill_rate_on_scored", "value": 81.5, "desc": "落盘检出率=81.5"},
        ],
    },
    {
        "id": "S7_counterfactual",
        "name": "反事实引文算子（P/R/F1 = 1.0，n=10）",
        "why": "反事实算子复算；分母只算带真值标签的 10 条，且 F1 是**上界**（判据照真值打的口径）。",
        "slow": False,
        "cmd": [PY, "tools/counterfactual_extend_665.py"],
        "writes": ["data/counterfactual_cases_665.json"],
        "timeout": T_DEFAULT,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0"},
            {"mode": "both", "kind": "artifact", "path": "data/counterfactual_cases_665.json",
             "jsonpath": "cases_total", "value": 10, "desc": "cases_total=10"},
            {"mode": "both", "kind": "artifact", "path": "data/counterfactual_cases_665.json",
             "jsonpath": "scores.f1", "value": 1.0, "desc": "F1=1.0"},
            {"mode": "both", "kind": "artifact", "path": "data/counterfactual_cases_665.json",
             "jsonpath": "confusion.tp", "value": 2, "desc": "tp=2"},
            {"mode": "both", "kind": "artifact", "path": "data/counterfactual_cases_665.json",
             "jsonpath": "confusion.tn", "value": 8, "desc": "tn=8"},
            {"mode": "both", "kind": "artifact", "path": "data/counterfactual_cases_665.json",
             "jsonpath": "denominator.value", "value": 10, "desc": "打分分母=10（不是 20）"},
        ],
    },
    {
        "id": "S8_fast_tests",
        "name": "快速测试套件（pytest -m 'not slow' -n0）",
        "why": "纯逻辑测试串行跑（不碰编译/replay 锁）；这是 CI 两阶段的第一阶段。",
        "slow": True,
        "cmd": [PY, "-m", "pytest", "tests/", "-m", "not slow", "-n0", "-q"],
        "writes": [],
        "timeout": T_PYTEST,
        "checks": [
            {"mode": "run", "kind": "exit", "value": 0, "desc": "退出码 0（无红）"},
            {"mode": "run", "kind": "stdout_re", "value": r"\d+ passed", "desc": "stdout 含 N passed"},
        ],
    },
]

STEP_IDS = tuple(s["id"] for s in STEPS)
CHECK_KINDS = ("exit", "stdout_re", "stdout_json", "artifact")
CHECK_MODES = ("run", "verify", "both")


# ── 纯函数区（测试直接调用，不碰磁盘、不起进程）───────────────────────────────

def cmd_display(cmd: list[str]) -> str:
    """把 argv 渲染成可粘贴的命令串（含空格的参数加引号）——报告里要能直接复跑。"""
    return " ".join(f'"{c}"' if " " in c else c for c in cmd)


def json_get(obj, dotted: str):
    """按点号路径取值（`a.b.c`）。任一段取不到 ⇒ **一律抛 KeyError**。

    为什么统一成 KeyError：调用方（evaluate）只需捕一种异常就能把"路径写错/字段改名/类型不符"
    全部收敛成"这一条 check 不匹配"，而不是让 TypeError 冒泡成"工具崩了"。
    不返回 None 冒充"取到了" —— None 是一个合法的 JSON 值，用它当哨兵会让 None 值的字段永远判绿。
    """
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError) as e:
                raise KeyError(f"{dotted}: 列表下标 {part!r} 无效（{type(e).__name__}）") from e
        elif isinstance(cur, dict):
            if part not in cur:
                raise KeyError(f"{dotted}: 缺字段 {part!r}")
            cur = cur[part]
        else:
            raise KeyError(f"{dotted}: {part!r} 处遇到不可下标的 {type(cur).__name__}")
    return cur


def values_equal(observed, expected, tol: float = 1e-9) -> bool:
    """数值用容差比（87.5 == 87.5），其余用 ==。bool 与 int 严格区分（True != 1）。"""
    if isinstance(expected, bool) or isinstance(observed, bool):
        return observed is expected
    if isinstance(expected, (int, float)) and isinstance(observed, (int, float)):
        return abs(float(observed) - float(expected)) <= tol
    return bool(observed == expected)


def extract_json_objects(text: str) -> list:
    """从混杂输出里捞出**所有**顶层 JSON 对象（工具常先打进度行再打 JSON）。

    用 `raw_decode` 从每个 `{` 位置试解，取成功的那些；解不出的忽略。
    这样"取最后一个 JSON"与"整段就是一个 JSON"两种情况都能覆盖。
    """
    dec = json.JSONDecoder()
    out = []
    i = 0
    n = len(text)
    while i < n:
        j = text.find("{", i)
        if j < 0:
            break
        try:
            obj, end = dec.raw_decode(text, j)
        except ValueError:
            i = j + 1
            continue
        out.append(obj)
        i = end
    return out


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_path(p: Path) -> str | None:
    return sha256_bytes(p.read_bytes()) if p.is_file() else None


def evaluate(step: dict, ctx: dict) -> dict:
    """对一个步骤的**实际观测**（ctx）跑它的 check 表，返回 {matched, checks}。

    ctx = {"exit": int|None, "stdout": str, "stderr": str, "root": Path, "mode": str}
    观测不到的项（如 verify 模式下没有 stdout）不参与判定，但会记 skipped=true —— 绝不当作通过。
    """
    mode = ctx.get("mode", "run")
    root = Path(ctx["root"])
    stdout = ctx.get("stdout") or ""
    checks_out = []
    for chk in step["checks"]:
        if chk["mode"] not in (mode, "both"):
            checks_out.append({"desc": chk["desc"], "kind": chk["kind"], "skipped": True,
                               "reason": f"该 check 只在 {chk['mode']} 模式判"})
            continue
        kind = chk["kind"]
        try:
            if kind == "exit":
                obs = ctx.get("exit")
                ok = obs == chk["value"]
            elif kind == "stdout_re":
                m = re.search(chk["value"], stdout)
                obs = m.group(0) if m else "(未匹配)"
                ok = m is not None
            elif kind == "stdout_json":
                objs = extract_json_objects(stdout)
                if not objs:
                    obs, ok = "(stdout 里没有 JSON)", False
                else:
                    try:
                        obs = json_get(objs[-1], chk["jsonpath"])
                        ok = values_equal(obs, chk["value"])
                    except (KeyError, IndexError, ValueError) as e:
                        obs, ok = f"(取不到 {chk['jsonpath']}: {e})", False
            elif kind == "artifact":
                p = root / chk["path"]
                if not p.is_file():
                    obs, ok = f"(缺文件 {chk['path']})", False
                else:
                    doc = json.loads(p.read_bytes().decode("utf-8"))
                    try:
                        obs = json_get(doc, chk["jsonpath"])
                        ok = values_equal(obs, chk["value"])
                    except (KeyError, IndexError, ValueError) as e:
                        obs, ok = f"(取不到 {chk['jsonpath']}: {e})", False
            else:  # pragma: no cover - 被 validate 挡住
                obs, ok = f"(未知 check 类型 {kind})", False
        except Exception as e:  # noqa: BLE001  —— check 自身的异常也算不匹配，不冒泡打断整条流水线
            obs, ok = f"(check 抛异常 {type(e).__name__}: {e})", False
        checks_out.append({"desc": chk["desc"], "kind": kind, "skipped": False,
                           "expected": chk.get("value", chk.get("path")),
                           "observed": obs, "ok": bool(ok)})
    judged = [c for c in checks_out if not c.get("skipped")]
    return {"matched": bool(judged) and all(c["ok"] for c in judged),
            "judged": len(judged), "failed": sum(1 for c in judged if not c["ok"]),
            # judged == 0 ⇒ 本模式下**没有可判的观测**（如 verify 模式下的 pytest 步骤）。
            # 必须与"判过且通过"区分开：否则"没得判"会被静默当成"通过"。
            "unverifiable": not judged,
            "checks": checks_out}


def validate_expect_table(steps: list[dict]) -> list[str]:
    """静态校验 check 表（不跑任何东西）。返回错误列表，空 = 合法。"""
    errs: list[str] = []
    seen: set[str] = set()
    for s in steps:
        sid = s.get("id", "?")
        if sid in seen:
            errs.append(f"{sid}: id 重复")
        seen.add(sid)
        for key in ("id", "name", "why", "slow", "cmd", "writes", "timeout", "checks"):
            if key not in s:
                errs.append(f"{sid}: 缺字段 {key}")
        if not s.get("cmd"):
            errs.append(f"{sid}: cmd 为空")
        if not s.get("checks"):
            errs.append(f"{sid}: checks 为空（没有预期的步骤等于没验收）")
        for c in s.get("checks", []):
            where = f"{sid}/{c.get('desc', '?')}"
            if c.get("kind") not in CHECK_KINDS:
                errs.append(f"{where}: 未知 kind={c.get('kind')}")
            if c.get("mode") not in CHECK_MODES:
                errs.append(f"{where}: 未知 mode={c.get('mode')}")
            if c.get("kind") in ("stdout_re", "stdout_json") and c.get("mode") not in ("run", "both"):
                errs.append(f"{where}: stdout 类 check 不该出现在 verify-only 模式")
            if c.get("kind") == "artifact":
                p = str(c.get("path", ""))
                if not (p.startswith("data/") or p.startswith("web/")):
                    errs.append(f"{where}: artifact 路径应在 data/ 或 web/ 下，实际 {p!r}")
                if "jsonpath" not in c:
                    errs.append(f"{where}: artifact check 缺 jsonpath")
            if c.get("kind") == "stdout_json" and "jsonpath" not in c:
                errs.append(f"{where}: stdout_json check 缺 jsonpath")
            if c.get("kind") in ("exit", "stdout_json", "artifact") and "value" not in c:
                errs.append(f"{where}: {c.get('kind')} check 缺 value")
        for w in s.get("writes", []):
            if w.startswith("/") or ":" in w:
                errs.append(f"{sid}: writes 必须是仓库相对路径，实际 {w!r}")
    return errs


def summarize(step_results: list[dict]) -> dict:
    """按步骤汇总（skipped 与 matched 分开数 —— "没跑"不冒充"通过"）。"""
    total = len(step_results)
    skipped = sum(1 for r in step_results if r.get("skipped"))
    ran = [r for r in step_results if not r.get("skipped")]
    matched = sum(1 for r in ran if r.get("matched"))
    return {"total": total, "ran": len(ran), "skipped": skipped,
            "matched": matched, "failed": len(ran) - matched}


def overall_of(summary: dict) -> str:
    """PASS = 跑到的全对；FAIL = 有步骤红；PARTIAL = 有步骤被跳过但跑到的都对。"""
    if summary["failed"]:
        return "FAIL"
    if summary["skipped"]:
        return "PARTIAL"
    return "PASS"


def build_report(step_results: list[dict], env: dict, meta: dict,
                 artifacts: list[dict] | None = None) -> dict:
    """组装落盘报告（纯函数：给定输入必得同一结构，便于测试用假数据调用）。"""
    summary = summarize(step_results)
    return {
        "schema": SCHEMA,
        "generated_by": "tools/reproduce_all_670c.py",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mode": meta.get("mode"),
        "skip_slow": bool(meta.get("skip_slow")),
        "only": list(meta.get("only") or []),
        "keep_outputs": bool(meta.get("keep_outputs")),
        "expected_source": ("check 表的每个 expected 都取自产物事实源："
                            "data/holdout_reveal_3_665.json / data/external_corpus_reveal_665.json / "
                            "data/656_mutation_report_{core,all}.json / data/counterfactual_cases_665.json / "
                            "data/658_gate_status.json / data/669d_gate_status.json"),
        "env": env,
        "steps": step_results,
        "summary": summary,
        "overall": overall_of(summary),
        "artifacts": artifacts or [],
        "honest_note": (
            "① overall=PARTIAL 表示有步骤被 --skip-slow/--only 跳过，**不是**全部通过；"
            "② 慢步骤（变异、fast pytest）未跑时它对应的数字来自落盘产物，不是本次现算；"
            "③ 本工具不修改预期值、不修改产物：对不上就记 FAIL。"
        ),
    }


def select_steps(steps: list[dict], only: list[str]) -> list[dict]:
    """按 --only 过滤（保持定义顺序）。未知 id ⇒ ValueError（由 main 转成退出码 2）。"""
    if not only:
        return list(steps)
    index = {s["id"]: s for s in steps}
    unknown = [o for o in only if o not in index]
    if unknown:
        raise ValueError(f"未知 step id: {', '.join(unknown)}；可用：{', '.join(index)}")
    keep = set(only)
    return [s for s in steps if s["id"] in keep]


def parse_only(value: str | None) -> list[str]:
    return [x.strip() for x in (value or "").split(",") if x.strip()]


# ── 环境与产物守卫（会碰磁盘/进程）──────────────────────────────────────────

def _first_line(cmd: list[str], timeout: int = 30) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        txt = (r.stdout or "") + (r.stderr or "")
        return (txt.strip().splitlines() or ["(无输出)"])[0][:160]
    except Exception as e:  # noqa: BLE001  环境探不到就如实写，不假装
        return f"(不可用: {type(e).__name__})"


def env_info(root: Path) -> dict:
    """记录**跑出这些数字的环境** —— 数字离开环境就不可复算。"""
    return {
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "platform": sys.platform,
        "node": _first_line(["node", "--version"]),
        "gpp": _first_line(["g++", "--version"]),
        "clangpp": _first_line(["clang++", "--version"]),
        "wsl_gpp": _first_line(["wsl", "-e", "bash", "-lc", "g++ --version | head -1"], timeout=60),
        "git_commit": _first_line(["git", "rev-parse", "HEAD"]),
        "cwd": str(root),
        "roll": "sanitizer 类在 WSL 里编译并运行；warn/cross 类用本机编译器；WSL 不可用时相关样本记 unknown",
    }


class ArtifactGuard:
    """把步骤会写到的产物**逐字节备份**，跑完还原；并在报告里给出 before/after/restored。

    为什么不用 git 兜底：产物里有未提交的改动（并行批次正在写），`git checkout` 会把人家的
    改动一起抹掉。逐字节快照只回滚"本工具跑出来的那部分"，这是本仓并行工作区的最低要求。
    """

    def __init__(self, root: Path, paths: list[str], keep: bool = False):
        self.root = root
        self.paths = list(dict.fromkeys(paths))
        self.keep = keep
        self.tmp = Path(tempfile.mkdtemp(prefix="repro670c-"))
        self.rows: list[dict] = []

    def snapshot(self) -> None:
        for rel in self.paths:
            src = self.root / rel
            before = sha256_path(src)
            blob = None
            if src.is_file():
                blob = self.tmp / rel.replace("/", "__")
                shutil.copyfile(src, blob)
            self.rows.append({"path": rel, "existed_before": src.is_file(),
                              "sha256_before": before, "sha256_after": None, "restored": False})

    def finalize(self) -> list[dict]:
        for row in self.rows:
            dst = self.root / row["path"]
            row["sha256_after"] = sha256_path(dst)
            if self.keep:
                continue
            blob = self.tmp / row["path"].replace("/", "__")
            if row["existed_before"] and blob.is_file():
                shutil.copyfile(blob, dst)
            elif not row["existed_before"] and dst.is_file():
                dst.unlink()
            row["restored"] = (sha256_path(dst) == row["sha256_before"])
        shutil.rmtree(self.tmp, ignore_errors=True)
        return self.rows


def run_step(step: dict, root: Path) -> dict:
    """执行一步（真起子进程）。超时/异常都收敛成结果字段，绝不冒泡打断流水线。"""
    started = time.strftime("%Y-%m-%dT%H:%M:%S")
    t0 = time.time()
    exit_code, out, err, note = None, "", "", ""
    try:
        r = subprocess.run(step["cmd"], cwd=str(root), capture_output=True, text=True,
                           timeout=step["timeout"])
        exit_code, out, err = r.returncode, r.stdout or "", r.stderr or ""
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") if isinstance(e.stdout, str) else ""
        err = (e.stderr or "") if isinstance(e.stderr, str) else ""
        note = f"TIMEOUT 超过 {step['timeout']}s（已强杀）"
    except Exception as e:  # noqa: BLE001
        note = f"EXC {type(e).__name__}: {e}"
    return {"exit": exit_code, "stdout": out, "stderr": err, "note": note,
            "started_at": started, "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "duration_s": round(time.time() - t0, 2)}


def _tail(s: str, n: int = 1200) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else "…" + s[-n:]


def build_parser() -> argparse.ArgumentParser:
    """CLI 契约单独成函数 —— 测试锁参数名与默认值，不靠"读 main 里的字面量"。"""
    ap = argparse.ArgumentParser(
        description="670c B2：一键复现编排器（门禁→holdout→corpus→变异→反事实→fast 测试）")
    ap.add_argument("--mode", choices=("verify", "run"), default="verify",
                    help="verify=只读产物对账（默认，秒级）／run=真跑每一步")
    ap.add_argument("--skip-slow", action="store_true", help="跳过慢步骤（变异、fast pytest）")
    ap.add_argument("--only", default=None, help="只跑这些 step id，逗号分隔（见 --list）")
    ap.add_argument("--list", action="store_true", help="列出步骤表与预期，然后退出")
    ap.add_argument("--keep-outputs", action="store_true",
                    help="run 模式：不还原被步骤改写的产物（复现者在自己 clone 里用）")
    ap.add_argument("--no-write", action="store_true", help="不写 data/reproduction_report_670c.json")
    ap.add_argument("--json", action="store_true", help="把报告打到 stdout")
    ap.add_argument("--timeout-scale", type=float, default=1.0,
                    help="所有步骤超时的统一放大系数（慢机器上 >1）")
    return ap


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    a = parse_args(argv)

    errs = validate_expect_table(STEPS)
    if errs:
        for e in errs:
            print(f"[repro670c] 清单非法：{e}")
        return 2

    if a.list:
        print(f"{len(STEPS)} 步（{sum(1 for s in STEPS if s['slow'])} 步标 slow）：")
        for s in STEPS:
            print(f"  {s['id']:<20} {'[slow]' if s['slow'] else '      '} {s['name']}")
            print(f"      命令：{cmd_display(s['cmd'])}")
            if s["writes"]:
                print(f"      会写：{', '.join(s['writes'])}（默认跑完还原）")
            for c in s["checks"]:
                exp = "退出码 0" if c["kind"] == "exit" else c.get("value")
                print(f"      预期[{c['mode']:<6}] {c['desc']} ⇒ {exp!r}")
        return 0

    only = parse_only(a.only)
    try:
        steps = select_steps(STEPS, only)
    except ValueError as e:
        print(f"[repro670c] {e}")
        return 2

    root = ROOT
    env = env_info(root)
    mode = a.mode

    # 被跳过的步骤也要进报告（"没跑"必须显形，不能消失）
    skipped_ids = set()
    if a.skip_slow:
        skipped_ids |= {s["id"] for s in STEPS if s["slow"]}
    skipped_ids -= {s["id"] for s in steps} if only else set()
    if only:
        skipped_ids |= {s["id"] for s in STEPS if s["id"] not in {x["id"] for x in steps}}
    results: list[dict] = []
    for s in STEPS:
        if s["id"] in skipped_ids:
            results.append({"id": s["id"], "name": s["name"], "cmd": cmd_display(s["cmd"]),
                            "skipped": True,
                            "reason": "--skip-slow" if s["slow"] and a.skip_slow else "--only 未选中",
                            "matched": False, "checks": [], "started_at": None,
                            "finished_at": None, "duration_s": None, "exit_code": None})
    guard = ArtifactGuard(root, [w for s in steps for w in s["writes"]],
                          keep=a.keep_outputs and mode == "run")
    guard.snapshot()
    print(f"[repro670c] mode={mode}  将跑 {len(steps)} 步  跳过 {len(skipped_ids)} 步  "
          f"keep_outputs={a.keep_outputs}")
    try:
        for s in steps:
            if mode == "run":
                obs = run_step({**s, "timeout": int(s["timeout"] * a.timeout_scale)}, root)
            else:
                obs = {"exit": None, "stdout": "", "stderr": "", "note": "verify 模式：未执行命令",
                       "started_at": None, "finished_at": None, "duration_s": None}
            ev = evaluate(s, {"exit": obs["exit"], "stdout": obs["stdout"], "stderr": obs["stderr"],
                              "root": root, "mode": mode})
            unverifiable = bool(ev.get("unverifiable"))
            row = {"id": s["id"], "name": s["name"], "cmd": cmd_display(s["cmd"]),
                   "slow": s["slow"], "why": s["why"], "writes": s["writes"],
                   "skipped": unverifiable,
                   "skip_reason": ("verify 模式无可判事实源（该步骤只能 --mode run 验证）"
                                   if unverifiable else None),
                   "started_at": obs["started_at"], "finished_at": obs["finished_at"],
                   "duration_s": obs["duration_s"], "exit_code": obs["exit"],
                   "run_note": obs["note"] or None,
                   "stdout_tail": _tail(obs["stdout"]), "stderr_tail": _tail(obs["stderr"]),
                   "matched": ev["matched"] and not unverifiable,
                   "judged": ev["judged"], "failed": ev["failed"],
                   "checks": ev["checks"]}
            results.append(row)
            flag = "SKIP" if unverifiable else ("OK  " if ev["matched"] else "MISS")
            extra = f"exit={obs['exit']}" if mode == "run" else "verify"
            print(f"  [{flag}] {s['id']:<20} {extra:<10} "
                  f"{ev['judged'] - ev['failed']}/{ev['judged']} check")
            for c in ev["checks"]:
                if not c.get("skipped") and not c["ok"]:
                    print(f"         ✗ {c['desc']}：期望 {c.get('expected')!r}，实测 {c.get('observed')!r}")
    finally:
        artifacts = guard.finalize()

    # 按定义顺序排回（skipped 与已跑的混在一起）
    order = {sid: i for i, sid in enumerate(STEP_IDS)}
    results.sort(key=lambda r: order.get(r["id"], 999))
    report = build_report(results, env, {"mode": mode, "skip_slow": a.skip_slow,
                                         "only": only, "keep_outputs": a.keep_outputs},
                          artifacts)
    changed = [r for r in artifacts if r["sha256_before"] != r["sha256_after"]]
    restored = [r for r in artifacts if r["restored"]]
    print(f"[repro670c] overall={report['overall']}  "
          f"匹配 {report['summary']['matched']}/{report['summary']['ran']}  "
          f"跳过 {report['summary']['skipped']}")
    if artifacts:
        print(f"  受保护产物 {len(artifacts)} 个；本次被改写 {len(changed)} 个；"
              f"已还原 {len(restored)} 个（keep_outputs={a.keep_outputs}）")
    if a.mode == "run" and changed and not a.keep_outputs and len(restored) != len(artifacts):
        print("  ⚠ 有产物未被还原 —— 请人工检查（本工具绝不对冻结文件留痕）")

    if not a.no_write:
        out = root / OUT_REL
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))
        print(f"  已写 {OUT_REL}")
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if report["overall"] in ("PASS", "PARTIAL") else 1


if __name__ == "__main__":
    raise SystemExit(main())
