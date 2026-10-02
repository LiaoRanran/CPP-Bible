#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""mutation_test_656.py — 656 B2 变异测试：故意把核心代码改坏，看测试能不能抓到。

为什么这么做
============
样例测试全绿 ≠ 测试真有杀伤力。变异测试是**唯一能量化"测试有多硬"的手段**：
把核心代码做最小语义改动（改常量 / 翻条件 / 反转比较 / 删检查），
如果测试**仍然全绿**，说明这块代码处于"改坏了也没人管"的状态。

做法（安全与速度的两条纪律）
==========================
1. **不改磁盘上的核心文件**：每个变异体写到临时目录，用 `importlib` 以同名
   `sys.modules` 条目替换后**在进程内**跑杀测试。任何崩溃/超时都只影响本进程。
2. **杀测试用真实测试函数**：直接跑 `tests/test_core_pbt_656.py`（656 B1 的 P1–P12），
   不是工具自造的探针 ⇒ "检出率"这个数字才有意义。

诚实边界（会写进报告，不藏）
==========================
- 进程内替换只能覆盖**被该文件 import 的模块**；CLI 级 / 子进程级行为不在射程内；
- 变异体若**导入即崩**（语法/名字错误）算"被杀"，但这类"杀"不含信息量 ⇒ 单独统计 `import_error`；
- 变异体若让测试**死循环/超时** ⇒ 单独统计 `timeout`，不计入正常检出率；
- 检出率就是检出率：**不美化、不补假变异体**；存活体会逐条列出并评估是否补测。

657 C 段修正（**等价变异**剔除，公开可审计）
=========================================
656 首版把**文档串里的数字/词**也当变异体（例如把 docstring 里的 "2." 改成 "3."），
这类改动**语义上不可能改变行为** ⇒ 是等价变异，却计入了分母，把检出率系统性拉低
（656 报告 37 个存活体里，**18 个**是文档串/注释行）。657 C 段按标准做法修正两条：

1. `ast` 解析出**所有 docstring 行**（Module / ClassDef / FunctionDef 的首条 Expr 串），
   这些行**不生成变异体**——改文档不等于改行为，这是口径修正，不是"挑好看的数字"；
2. 工具自带的 `selftest()`（**该文件中内嵌的测试代码**）不生成变异体——对测试代码做变异
   属"给测试打分"，不属于"测生产代码有多硬"。

两条修正**只影响分子分母的口径**，报告里同时给出**未剔除口径**（`--include-nonprod`）
的对照数字，任何人都能复核差了多少。**不新增假变异体、不删真实存活体。**

用法
====
    python tools/mutation_test_656.py --limit 60          # 跑 60 个变异体（默认）
    python tools/mutation_test_656.py --report            # 写 data/656_mutation_report.{md,json}
    python tools/mutation_test_656.py --check             # 自检：基线必绿 + 至少一个变异体被杀
    python tools/mutation_test_656.py --include-nonprod    # 657：把 docstring/selftest 也当射程（对照）
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import random
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

#: 672f：统一项目随机种子（670d §3.1 约定值）——变异体抽样可复现（G-SEED-FIXED）
# 673b A1：种子块移到**全部 import 之后**（此前夹在 import 中间 ⇒ ruff E402）。
SEED = 20260930
random.seed(SEED)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
KILL_SUITE = ROOT / "tests" / "test_core_pbt_656.py"
OUT_MD = ROOT / "data" / "656_mutation_report.md"
OUT_JSON = ROOT / "data" / "656_mutation_report.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

#: 核心判决路径上的函数（变异作用域 `core` 只改这些函数体里的行）。
#: 分开报两套检出率的原因：整文件随机抽样里混着 CLI / 报告 / 迁移计划等"本就没人测"的代码，
#: 会把检出率拉低到看不出**核心**到底硬不硬。两个数都给，不挑好看的那个说。
CORE_FUNCS: frozenset[str] = frozenset({
    "classify", "_raw_state", "has_boundary", "boundary_of", "enforce", "classify_card",
    "append", "verify_chain", "get_current", "compute_self_hash", "finalize", "validate",
    "mth", "inclusion_path", "verify_inclusion", "consistency_proof", "verify_consistency",
    "_subproof", "leaf_hash", "node_hash", "_largest_pow2_lt",
})

DEFAULT_TARGETS: tuple[str, ...] = (
    "four_state_verdict_638",    # 四态分类（边界优先）
    "ledger_checkpoint_651",     # Merkle 一致性/包含性
    "decision_event_v2_626",     # 账本哈希链 + strict 导入
)

#: 657 C：**非生产路径**——工具内嵌的自检函数（属测试代码，不是被验证对象）。
NON_PROD_FUNCS: frozenset[str] = frozenset({"selftest"})

#: 变异算子（每个只做**最小**语义改动）
#: 比较符翻转（每个键只出现一次；`<`→`<=` 与 `<=`→`<` 各自成对，语义上是"放宽/收紧"两侧）
CMP_FLIP = {"==": "!=", "!=": "==", "<": "<=", "<=": "<", ">": ">=", ">=": ">",
            "is": "is not", "is not": "is"}
BOOL_FLIP = {" and ": " or ", " or ": " and ", "True": "False", "False": "True",
             "not ": "", "if ": "if not "}
_GUARD_RE = re.compile(r"^(\s*)if\s+.+:\s*(raise|return)\b.*$")
_NUM_RE = re.compile(r"(?<![\w.])(\d+)")


def _in_string_context(line: str, idx: int) -> bool:
    """粗略判断 idx 是否落在字符串/注释里（避免把文案里的数字当常量）。"""
    head = line[:idx]
    return head.count('"') % 2 == 1 or head.count("'") % 2 == 1 or "#" in head


def enclosing_func(lines: list[str], idx: int) -> str:
    """第 idx 行所在的函数名（只看顶格 `def `，够用且不假精确）。"""
    for j in range(idx, -1, -1):
        # 允许缩进：`AuthorityLedger.append` 这类**方法**也必须能归到 `append`
        # （首版只匹配顶格 def ⇒ decision_event_v2_626 的核心候选数变成 0，被自检外的观察抓到）
        m = re.match(r"\s*def\s+([A-Za-z_]\w*)", lines[j])
        if m:
            return m.group(1)
    return "<module>"


def docstring_lines(src: str) -> set[int]:
    """657 C：全部 docstring 占用的行号（1-based）。

    用 `ast` 精确取 Module / ClassDef / FunctionDef(含 async) 的首条字符串语句的
    `lineno..end_lineno`。解析失败 ⇒ 返回空集（退化为 656 口径，不假装）。
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    out: set[int] = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list) or not body:
            continue
        first = body[0]
        if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            out.update(range(first.lineno, (first.end_lineno or first.lineno) + 1))
    return out


def nonprod_lines(src: str) -> set[int]:
    """657 C：非生产函数（`NON_PROD_FUNCS`）**含嵌套定义**占用的行号（1-based）。

    为什么不能只看 `enclosing_func`：`four_state_verdict_638.selftest()` 内部又定义了
    `def chk(...)`，于是 `enclosing_func` 会把 selftest 里几百行 `chk(...)` 断言**归到 `chk`**
    ⇒ 名字过滤失效、测试代码仍被当作射程（657 首版实测撞到）。`ast` 的行区间没有这个盲区。
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return set()
    out: set[int] = set()
    for node in ast.walk(tree):
        if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in NON_PROD_FUNCS):
            out.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    return out


def gen_mutants(src: str, per_op_cap: int = 40, scope: str = "all",
                strip_nonprod: bool = True) -> list[dict[str, Any]]:
    """生成候选变异体：`(行号, 算子, 变异后源码)`。scope=core 时只留核心函数体内的行。

    657 C：`strip_nonprod=True`（默认）时剔除 **docstring 行** 与 **非生产函数体**；
    传 False 即回到 656 的原口径（用于报告里的对照数字）。
    """
    lines = src.splitlines(keepends=True)
    docs = docstring_lines(src) if strip_nonprod else set()
    nonprod = nonprod_lines(src) if strip_nonprod else set()
    out: list[dict[str, Any]] = []
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        if strip_nonprod and ((i + 1) in docs or (i + 1) in nonprod):
            continue
        fn = enclosing_func(lines, i)
        if scope == "core" and fn not in CORE_FUNCS:
            continue
        if strip_nonprod and fn in NON_PROD_FUNCS:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # ① 比较符翻转
        for tok, rep in CMP_FLIP.items():
            for m in re.finditer(r"(?<![\w])" + re.escape(tok) + r"(?![\w])", line):
                if _in_string_context(line, m.start()):
                    continue
                new = line[: m.start()] + rep + line[m.end():]
                out.append({"line": i + 1, "op": "cmp", "from": tok, "to": rep,
                            "text": line.strip()[:90], "src": _replace(lines, i, new)})
                break
        # ② 数字常量 ±1（跳过 0/1 之外的纯版本号行与字符串内数字）
        for m in _NUM_RE.finditer(line):
            if _in_string_context(line, m.start()):
                continue
            n = int(m.group(1))
            if n <= 1 or n > 100000:
                continue
            new = line[: m.start()] + str(n + 1) + line[m.end():]
            out.append({"line": i + 1, "op": "const", "from": str(n), "to": str(n + 1),
                        "text": line.strip()[:90], "src": _replace(lines, i, new)})
            break
        # ③ 布尔/逻辑反转
        for tok, rep in BOOL_FLIP.items():
            if tok in line and not _in_string_context(line, line.find(tok)):
                new = line.replace(tok, rep, 1)
                if new != line:
                    out.append({"line": i + 1, "op": "bool", "from": tok.strip() or tok,
                                "to": rep.strip() or "''", "text": line.strip()[:90],
                                "src": _replace(lines, i, new)})
                break
        # ④ 删检查：整行 `if ...: raise/return ...` ⇒ pass
        if _GUARD_RE.match(line):
            m0 = re.match(r"\s*", line)
            indent = m0.group(0) if m0 else ""
            out.append({"line": i + 1, "op": "guard", "from": "if …raise/return",
                        "to": "pass", "text": line.strip()[:90],
                        "src": _replace(lines, i, f"{indent}pass  # 变异：删掉这条检查")})
    # 每算子限流，保证覆盖面而不是某一行刷屏
    by_op: dict[str, list[dict[str, Any]]] = {}
    for mv in out:
        by_op.setdefault(mv["op"], []).append(mv)
    flat: list[dict[str, Any]] = []
    for op, items in by_op.items():
        flat += items[:per_op_cap]
    return flat


def _replace(lines: list[str], i: int, new_line: str) -> str:
    return "".join([*lines[:i], new_line + ("\r\n" if lines[i].endswith("\r\n") else "\n"),
                    *lines[i + 1:]])


def load_mutant(name: str, src: str) -> tuple[bool, str]:
    """把变异体装进 `sys.modules[name]`；返回 (是否导入成功, 备注)。"""
    tmp = tempfile.mkdtemp(prefix="mut656-")
    p = Path(tmp) / f"{name}.py"
    p.write_text(src, encoding="utf-8", newline="")
    spec = importlib.util.spec_from_file_location(name, p)
    if spec is None or spec.loader is None:
        return False, "spec 失败"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {str(e)[:100]}"


def _collect(mod: Any) -> tuple[list[tuple[str, Callable[[], None]]], list[str]]:
    """从测试模块里收集可直调的测试函数。

    pytest fixture（如 `tmp_path`）在进程内没有 ⇒ 用真实临时目录顶上；
    其它无法顶替的形参 ⇒ **跳过并登记**（绝不能因为调用姿势不对就算"杀"）。
    """
    import functools
    import inspect

    fns: list[tuple[str, Callable[[], None]]] = []
    skipped: list[str] = []
    for n in dir(mod):
        if not n.startswith("test_") or "stateful" in n:
            continue
        fn = getattr(mod, n)
        if not callable(fn):
            continue
        params = list(inspect.signature(fn).parameters.values())
        if not params:
            fns.append((n, fn))
        elif all(p.name.startswith("tmp_") for p in params):
            kwargs = {p.name: Path(tempfile.mkdtemp(prefix="kill656-")) for p in params}
            fns.append((n, functools.partial(fn, **kwargs)))
        else:
            skipped.append(n)
    return fns, skipped


def kill_functions(tag: str = "base") -> tuple[list[tuple[str, Callable[[], None]]], list[str]]:
    """加载杀测试模块并收集函数。

    ⚠️ **每个变异体都要重新加载一次**：测试模块在 import 期就把 `import x as fs`
    解析成了对象引用，之后换 `sys.modules` 不会回溯影响它 ⇒ 必须重新 import 才能让
    变异体真正进入射程（这是本工具最容易出错的一处，已写成断言见 `--check`）。
    """
    spec = importlib.util.spec_from_file_location(f"_kill656_{tag}", KILL_SUITE)
    if spec is None or spec.loader is None:
        raise RuntimeError("杀测试文件无法加载")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return _collect(mod)


def worker(payload_path: Path) -> int:
    """**子进程模式**：装一个变异体 ⇒ 跑杀测试 ⇒ 打印结果 JSON。

    为什么要单独一个进程：变异体可能让某个测试**卡死**（本批实测撞到：后台跑了 40 分钟不结束）。
    进程内无法打断一个跑飞的函数，`subprocess.run(timeout=…)` 可以 ⇒ 超时即 `timeout`，
    而且**不会污染父进程的 sys.modules**。
    """
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    target, src = payload["target"], payload["src"]
    ok, note = load_mutant(target, src)
    if not ok:
        print(json.dumps({"status": "import_error", "detail": note}, ensure_ascii=False))
        return 2
    try:
        fns, _ = kill_functions(tag=f"w{abs(hash((target, payload['line']))) % 100000}")
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"status": "import_error",
                          "detail": f"kill suite: {type(e).__name__}: {str(e)[:100]}"},
                         ensure_ascii=False))
        return 2
    for fname, fn in fns:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            print(json.dumps({"status": "killed",
                              "detail": f"{fname}: {type(e).__name__}: {str(e)[:110]}"},
                             ensure_ascii=False))
            return 1
    print(json.dumps({"status": "survived", "detail": ""}, ensure_ascii=False))
    return 0


def run_one_subprocess(mutant: dict[str, Any], target: str, timeout_s: float) -> dict[str, Any]:
    base = {"target": target, "line": mutant["line"], "op": mutant["op"],
            "from": mutant.get("from"), "to": mutant.get("to"), "text": mutant.get("text")}
    payload = {"target": target, "src": mutant["src"], "line": mutant["line"]}
    with tempfile.TemporaryDirectory(prefix="mut656job-") as td:
        pj = Path(td) / "job.json"
        pj.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                                "--worker", str(pj)],
                               capture_output=True, text=True, timeout=timeout_s, check=False)
        except subprocess.TimeoutExpired:
            return {**base, "status": "timeout", "detail": f"超过 {timeout_s}s（已强杀子进程）",
                    "seconds": round(time.time() - t0, 2)}
        out = (r.stdout or "").strip().splitlines()
        try:
            res = json.loads(out[-1]) if out else {"status": "import_error", "detail": "无输出"}
        except Exception:  # noqa: BLE001
            res = {"status": "import_error", "detail": (r.stdout or r.stderr or "")[-120:]}
        return {**base, "status": res.get("status", "import_error"),
                "detail": res.get("detail", ""), "seconds": round(time.time() - t0, 2)}


def run_one(mutant: dict[str, Any], target: str, timeout_s: float) -> dict[str, Any]:
    saved = sys.modules.get(target)
    ok, note = load_mutant(target, mutant["src"])
    if not ok:
        if saved is not None:
            sys.modules[target] = saved
        return {"target": target, "line": mutant["line"], "op": mutant["op"],
                "status": "import_error", "detail": note}
    # 变异体装好之后**重新加载**杀测试，让它 import 到变异体（见 kill_functions 的说明）
    try:
        fns, _ = kill_functions(tag=f"{target}-{mutant['line']}-{mutant['op']}")
    except Exception as e:  # noqa: BLE001
        if saved is not None:
            sys.modules[target] = saved
        return {"target": target, "line": mutant["line"], "op": mutant["op"],
                "status": "import_error", "detail": f"kill suite: {type(e).__name__}: {str(e)[:100]}"}
    t0 = time.time()
    status, detail = "survived", ""
    for fname, fn in fns:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            status, detail = "killed", f"{fname}: {type(e).__name__}: {str(e)[:110]}"
            break
        if time.time() - t0 > timeout_s:
            status, detail = "timeout", f"超过 {timeout_s}s（{fname}）"
            break
    if saved is not None:
        sys.modules[target] = saved
    else:
        sys.modules.pop(target, None)
    return {"target": target, "line": mutant["line"], "op": mutant["op"],
            "from": mutant["from"], "to": mutant["to"], "text": mutant["text"],
            "status": status, "detail": detail, "seconds": round(time.time() - t0, 2)}


def run(limit: int, targets: tuple[str, ...], seed: int = 20260928,
        timeout_s: float = 25.0, scope: str = "all",
        strip_nonprod: bool = True) -> dict[str, Any]:
    rnd = random.Random(seed)
    fns, skipped = kill_functions()

    # 基线：未变异时必须全绿，否则"检出率"这个数字没有意义
    base_ok, base_detail = True, ""
    for fname, fn in fns:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            base_ok, base_detail = False, f"{fname}: {type(e).__name__}: {str(e)[:160]}"
            break
    if not base_ok:
        raise SystemExit(f"[mutation656] 基线未绿 ⇒ 拒绝给出检出率：{base_detail}")

    results: list[dict[str, Any]] = []
    cand_n: dict[str, int] = {}
    cand_raw: dict[str, int] = {}
    for tgt in targets:
        path = HERE / f"{tgt}.py"
        if not path.is_file():
            continue
        src = path.read_text(encoding="utf-8")
        cand = gen_mutants(src, scope=scope, strip_nonprod=strip_nonprod)
        cand_raw[tgt] = len(gen_mutants(src, scope=scope, strip_nonprod=False))
        cand_n[tgt] = len(cand)
        rnd.shuffle(cand)
        picked = cand[: max(1, limit // len(targets))]
        print(f"[mutation656] {tgt}：候选 {len(cand)}（未剔口径 {cand_raw[tgt]}）⇒ 抽取 {len(picked)}")
        for mv in picked:
            # 子进程模式：变异体跑飞也杀得掉（进程内做不到），代价是每个多 ~0.3s 启动
            results.append(run_one_subprocess(mv, tgt, timeout_s))

    by_file: dict[str, dict[str, int]] = {}
    for r in results:
        s = by_file.setdefault(r["target"], {"total": 0, "killed": 0, "survived": 0,
                                             "import_error": 0, "timeout": 0})
        s["total"] += 1
        s[r["status"]] += 1
    killed = sum(1 for r in results if r["status"] == "killed")
    scored = sum(1 for r in results if r["status"] in {"killed", "survived"})
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seed": seed,
        "kill_suite": str(KILL_SUITE.relative_to(ROOT)).replace("\\", "/"),
        "scope": scope,
        "strip_nonprod": strip_nonprod,
        "candidates": cand_n,
        "candidates_raw": cand_raw,
        "kill_tests_used": [n for n, _ in fns],
        "kill_tests_skipped": skipped,
        "targets": list(targets),
        "mutants": len(results),
        "killed": killed,
        "survived": sum(1 for r in results if r["status"] == "survived"),
        "import_error": sum(1 for r in results if r["status"] == "import_error"),
        "timeout": sum(1 for r in results if r["status"] == "timeout"),
        "kill_rate_on_scored": round(100.0 * killed / scored, 1) if scored else None,
        "kill_rate_all": round(100.0 * killed / len(results), 1) if results else None,
        "by_file": by_file,
        "results": results,
    }


def report(rep: dict[str, Any]) -> None:
    reps = rep["results"]
    survivors = [r for r in reps if r["status"] == "survived"]
    lines = [
        "# 656 B2 · 变异测试报告（657 C 段复测）",
        "",
        f"> 生成：{rep['generated_at']}　杀测试：`{rep['kill_suite']}`（656 B1 的 P1–P12 真实测试函数）"
        f"　种子：{rep['seed']}（可复现）　"
        f"剔除等价变异（docstring/selftest）：{'是' if rep.get('strip_nonprod', True) else '否'}",
        "",
        "## 一、总览",
        "",
        f"- 变异体：**{rep['mutants']}**",
        "- 候选池（剔除后 / 未剔对照）："
        + "；".join(f"`{k}` {v}/{rep.get('candidates_raw', {}).get(k, '—')}"
                    for k, v in rep.get("candidates", {}).items()),
        f"- 被杀：{rep['killed']}　存活：{rep['survived']}　导入即崩：{rep['import_error']}　超时：{rep['timeout']}",
        f"- **检出率（只看能跑的 {rep['killed'] + rep['survived']} 个）：{rep['kill_rate_on_scored']}%**",
        f"- 检出率（含导入即崩，口径更宽松）：{rep['kill_rate_all']}%",
        "",
        "## 二、分文件",
        "",
        "| 目标 | 总数 | 被杀 | 存活 | 导入崩 | 超时 | 检出率 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for f, s in rep["by_file"].items():
        scored = s["killed"] + s["survived"]
        rate = f"{round(100.0 * s['killed'] / scored, 1)}%" if scored else "—"
        lines.append(f"| `{f}` | {s['total']} | {s['killed']} | {s['survived']} | "
                     f"{s['import_error']} | {s['timeout']} | {rate} |")
    lines += ["", "## 三、存活体（测试没抓到的改动）", ""]
    if survivors:
        lines.append("| 目标 | 行 | 算子 | 改了什么 | 原文 |")
        lines.append("|---|---:|---|---|---|")
        for r in survivors[:40]:
            lines.append(f"| `{r['target']}` | {r['line']} | {r['op']} | "
                         f"`{str(r.get('from'))[:12]}`→`{str(r.get('to'))[:12]}` | "
                         f"`{str(r.get('text'))[:70]}` |")
        if len(survivors) > 40:
            lines.append(f"（另有 {len(survivors) - 40} 条，见 JSON 报告）")
    else:
        lines.append("无（全部被杀）")
    lines += [
        "",
        "## 四、诚实边界",
        "",
        "1. **进程内替换**只覆盖被测试文件 import 的模块；CLI / 子进程行为不在射程内。",
        "2. **导入即崩**算’被杀’但不含信息量 ⇒ 已单独统计，检出率主口径只看能跑的变异体。",
        "3. 存活体 ≠ 一定有 bug：也可能是**等价变异**（改了写法不改语义）或该分支本就无测试覆盖；"
        "本批对存活体的处置见 §五。",
        "4. 变异体是**抽样**（种子固定 ⇒ 可复现），不是穷举；样本外仍可能有漏网。",
        "5. 657 C 起剔除两类**结构性等价变异**（docstring 行 / 本工具自带的 `selftest()`）——"
        "它们改了也不改行为，留在分母里只会拉低数字。未剔口径的候选数在同一行并列给出。",
        "",
        "## 五、对存活体的处置",
        "",
    ]
    if rep["kill_rate_on_scored"] is not None and rep["kill_rate_on_scored"] >= 80.0:
        lines.append(f"检出率 {rep['kill_rate_on_scored']}% ≥ 80% ⇒ 达标；存活体逐条登记为后续补测候选。")
    else:
        lines.append(f"检出率 {rep['kill_rate_on_scored']}% < 80% ⇒ **未达标**；存活体已列在 §三，"
                     "按任务书要求应补测试（见收工报告的诚实登记）。")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8", newline="\n")


def compare(core_json: Path, all_json: Path) -> int:
    """把两套作用域的结果并排写进主报告（**两个数都给**，不挑好看的）。"""
    if not core_json.is_file() or not all_json.is_file():
        print(f"[mutation656] 缺报告（{core_json.name} / {all_json.name}）⇒ 跳过对比")
        return 2
    core = json.loads(core_json.read_text(encoding="utf-8"))
    allr = json.loads(all_json.read_text(encoding="utf-8"))
    lines = [
        "",
        "## 六、两套作用域对账（为什么给两个数）",
        "",
        "| 作用域 | 含义 | 变异体 | 被杀 | 存活 | 导入崩 | 超时 | 检出率（可跑口径） |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
        (f"| `core` | 只改**核心判决路径**上的函数体 | {core['mutants']} | {core['killed']} | "
         f"{core['survived']} | {core['import_error']} | {core['timeout']} | "
         f"**{core['kill_rate_on_scored']}%** |"),
        (f"| `all` | 整文件随机抽样（含 CLI/报告/迁移等无人测代码） | {allr['mutants']} | "
         f"{allr['killed']} | {allr['survived']} | {allr['import_error']} | {allr['timeout']} | "
         f"**{allr['kill_rate_on_scored']}%** |"),
        "",
        "- 分文件（core）：" + "；".join(
            f"`{k}` {v['killed']}/{v['killed'] + v['survived']}"
            for k, v in core["by_file"].items()),
        "- 分文件（all）：" + "；".join(
            f"`{k}` {v['killed']}/{v['killed'] + v['survived']}"
            for k, v in allr["by_file"].items()),
        "",
        "**结论**：核心路径（`core`）的检出率高于整文件随机（`all`）——差额集中在 CLI/报告/IO 这类"
        "**本就没有单测**的代码上。两个数都保留：只看 `core` 会高估测试整体强度，只看 `all` 会低估核心的硬度。",
        "",
    ]
    # 657 C：达标判定**按当轮真实数字算**，不写死（656 首版把结论写死成"未达标"，换个数就会自相矛盾）
    c_rate, a_rate = core.get("kill_rate_on_scored"), allr.get("kill_rate_on_scored")
    lines += [
        "**目标对照（按 657 C 段任务书）**：",
        "",
        f"- `core` 目标 ≥ 80%：实测 **{c_rate}%** ⇒ "
        f"{'达标' if (c_rate or 0) >= 80 else '**未达标**'}；",
        f"- `all` 目标 ≥ 60%：实测 **{a_rate}%** ⇒ "
        f"{'达标' if (a_rate or 0) >= 60 else '**未达标**'}；",
        "",
        "**657 C 段的两条口径修正（不只是「多写测试」）**：",
        "",
        "1. **剔除结构性等价变异**：656 把 docstring 行、以及工具内嵌 `selftest()` 里的断言行都当射程"
        "（656 的 37 个存活体里 18 个是这两类），这些改动**语义上不可能改变行为** ⇒ 属等价变异，"
        "留在分母里只会系统性拉低检出率。剔除后**对照口径**在同一行的候选池里并列给出，可复核。",
        "2. **补测引用存活体**：`tests/test_core_pbt_656.py` 的 P13/P14 两节逐条对应报告 §三 的真实存活体"
        "（★ 标记处写明对应哪个算子）。",
        "",
        "**剩余存活体的归因**（全部逐条登记，见 `data/657_mutation_attribution.md`）："
        "①等价变异（如 `classify_card` 的 `==`→`!=`，因 `_raw_state(\"\")` 也判 pass 而不可区分）；"
        "②CLI / 报告 / 文件 IO 路径（`main` / `write_report` / `build_checkpoint` / `verify_checkpoint_file`）；"
        "③需要专用夹具的路径（HMAC 签名、checkpoint 文件）。",
    ]
    md = OUT_MD.read_text(encoding="utf-8") if OUT_MD.is_file() else "# 656 B2 · 变异测试报告\n"
    OUT_MD.write_text(md + "\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"[mutation656] 已把两作用域对账写入 {OUT_MD.relative_to(ROOT).as_posix()}")
    return 0


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}{(' · ' + extra) if extra else ''}")
        ok = ok and cond

    src = (HERE / "four_state_verdict_638.py").read_text(encoding="utf-8")
    cand = gen_mutants(src)
    chk("能生成变异体", len(cand) > 0, f"{len(cand)} 个")
    chk("变异体确实改了源码", all(m["src"] != src for m in cand))
    # 657 C：等价变异剔除必须真的生效（否则"检出率提升"就是假的）
    sample = ('"""module doc 2 items."""\n'
              "\n"
              "\n"
              "def f():\n"
              '    """inner doc 3 items."""\n'
              "    return 2\n"
              "\n"
              "\n"
              "def selftest():\n"
              "    return 7\n")
    kept = gen_mutants(sample)
    raw = gen_mutants(sample, strip_nonprod=False)
    chk("docstring 行不生成变异体", all(m["line"] not in (1, 5) for m in kept),
        f"lines={sorted({m['line'] for m in kept})}")
    chk("selftest 函数体不生成变异体",
        all(m["line"] != 10 for m in kept),
        f"lines={sorted({m['line'] for m in kept})}")
    chk("未剔口径候选更多（对照可复现）", len(raw) > len(kept), f"{len(raw)} > {len(kept)}")
    chk("报告产物落在 data/ 下",
        str(OUT_MD).replace("\\", "/").endswith("data/656_mutation_report.md"))
    # 基线必须绿（不绿就不该给检出率）
    fns, skipped = kill_functions()
    chk("杀测试文件可加载", len(fns) >= 10, f"{len(fns)} 个可调用 / 跳过 {len(skipped)} 个")
    base_ok = True
    for fname, fn in fns:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            base_ok = False
            chk("基线（未变异）必绿", False, f"{fname}: {type(e).__name__}: {str(e)[:100]}")
            break
    if base_ok:
        chk("基线（未变异）必绿", True)

    # **自检最关键的一条**：故意把边界哈希正则放宽 ⇒ 测试**必须**抓到。
    # 若这条抓不到，说明"变异体根本没进射程"（本工具最可能的失效模式）⇒ 绝不能交付。
    src2 = src.replace("^[0-9a-fA-F]{64}$", "^.*$")
    if src2 != src:
        r = run_one({"line": 0, "op": "selftest-sanity", "from": "64hex", "to": "any",
                     "text": "_HASH_RE 放宽", "src": src2}, "four_state_verdict_638", 25.0)
        chk("放松边界哈希正则 ⇒ 必须被杀（证明变异体真进了射程）",
            r["status"] == "killed", f"status={r['status']} {r.get('detail','')[:90]}")
    else:
        chk("能构造 sanity 变异体（正则已变？请更新自检）", False)
    print(f"mutation_test_656 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 B2 变异测试")
    ap.add_argument("--limit", type=int, default=60, help="变异体数量（默认 60）")
    ap.add_argument("--targets", default=",".join(DEFAULT_TARGETS))
    ap.add_argument("--seed", type=int, default=20260928)
    ap.add_argument("--timeout", type=float, default=25.0, help="单个变异体的杀测试超时（秒）")
    ap.add_argument("--scope", choices=("all", "core"), default="all",
                    help="all=整文件随机抽样；core=只改核心判决路径上的函数体")
    ap.add_argument("--include-nonprod", action="store_true",
                    help="657：把 docstring 行与 selftest 也当射程（回到 656 口径，用于对照）")
    ap.add_argument("--worker", default=None, help="（内部）子进程模式：跑单个变异体任务")
    ap.add_argument("--compare", action="store_true",
                    help="把 core 与 all 两份报告并排写进主报告（需先分别跑过两轮）")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.worker:
        return worker(Path(a.worker))
    if a.compare:
        return compare(ROOT / "data" / "656_mutation_report_core.json", OUT_JSON)
    if a.check:
        return selftest()
    rep = run(a.limit, tuple(t.strip() for t in a.targets.split(",") if t.strip()),
              seed=a.seed, timeout_s=a.timeout, scope=a.scope,
              strip_nonprod=not a.include_nonprod)
    if a.report:
        report(rep)
    if a.json:
        print(json.dumps({k: v for k, v in rep.items() if k != "results"},
                         ensure_ascii=False, indent=2))
    else:
        print(f"[mutation656] 变异体 {rep['mutants']}｜被杀 {rep['killed']}｜存活 {rep['survived']}"
              f"｜导入崩 {rep['import_error']}｜超时 {rep['timeout']}"
              f"｜检出率 {rep['kill_rate_on_scored']}%（可跑口径）")
        for f, s in rep["by_file"].items():
            scored = s["killed"] + s["survived"]
            print(f"            {f}: {s['killed']}/{scored} = "
                  f"{round(100.0 * s['killed'] / scored, 1) if scored else '—'}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
