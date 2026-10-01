#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""guard_rerun_671a.py — 671a A：B3 防复发（改检测器必重跑）+ 产物新鲜度 + 三方数字一致性。

670g 留下的最大缺口
==================
670c 的 `guard_rerun_670c.py` 只覆盖**5 个核心工具**（gate_engine / replay / poison / cppbible /
toolchain）。可 670a 之后真正在动的数字（holdout 检出率、corpus 检出率、baseline 三臂、变异率）
全部来自**另一批检测器**：`holdout_reveal_3_665` / `external_corpus_reveal_665` /
`baseline_670a` / `mutation_test_656` … 它们**不在 670c 的射程里** ⇒
"改了检测器但没重跑产物" 依然是一类**没有任何门禁能看见**的假绿
（667 的 81.2%、反事实 F1=0.0 就是这个形态）。

本工具把这条射程补上，并额外加两条 670c 没有的判据：

1. **检测器清单配置化**（`data/guard_detector_files_671a.json`）
   —— 每个检测器声明 `src` + `deps`（它 import 的判据库）+ 它**重跑时会刷新**的产物。
2. **产物新鲜度**（mtime 轴）：产物必须**不早于**判据代码；早于 ⇒ 产物过期，必须重跑。
3. **三方数字一致性**（`data/guard_artifacts_671a.json`）：产物现算值 ↔ 论文正文 ↔ 前端 JSON。

三种指纹（为什么不是一种）
==========================
| 指纹 | 计算 | 用途 |
|---|---|---|
| `raw_sha256` | 裸字节 | 诊断（注释改动可见）|
| `ast_sha256` | AST dump（剥文档字符串）| 诊断（纯注释改动即为此层唯一变化）|
| `judgment_sha256` | AST + **局部变量名归一** | **判据**：它变了才算"判据变了" |

判据用第三层的原因：门禁若对"改个局部变量名"也喊红，就会变成狼来了
（`docs/gate_tiers_658.md §2` 的两层模型动机）。归一化只对**函数内绑定的局部名**
（参数 / 赋值 / for / with / except / 函数内 import）生效，且**排除模块级名字与嵌套函数的
绑定名** —— 函数名、类名、模块常量、属性名、字符串字面量仍然进指纹：
改了它们**必须**重跑（改了 `OPT_LEVELS` 的含义、改了 schema 键名，都是判据变了）。

状态机（检测器 × 产物）
======================
| 判据变了 | 产物变了 | 状态 | 严重度 |
|---|---|---|---|
| 否 | 否 | OK | pass |
| 否 | 是 | RERUN_ONLY | pass（提示：可能产物非确定性）|
| 是 | 是 | RERUN | pass（改了也重跑了）|
| **是** | **否** | **STALE** | **block**（改了没重跑 ⇒ 假绿）|
| 是 | 否（产物全为 advisory）| ADVISORY_STALE | warn |
| — | 产物缺失 | PRODUCT_MISSING | block（fail-closed：缺了就没法对账）|
| 驱动脚本不存在 | — | SRC_MISSING | warn（无法判定，登记不假装覆盖）|
| 基线无此条 | — | NO_BASELINE_ENTRY | warn（新注册，先标定再判红）|
| 未声明产物 | — | NO_PRODUCT | warn（射程自检）|

产物新鲜度（第二条独立轴）
==========================
`产物 mtime < max(src, deps).mtime - tol` ⇒ 过期。**但**：
* 基线里就记为不新鲜的对（如 git checkout 顺序导致 data/ 早于 tools/、或历史手工追加）
  ⇒ 状态 `FRESHNESS_LEGACY`，只 **warn** —— 存量缺口登记为缺口，而不是把门禁变成噪音
  （与 669d `known_gaps` 的降级语义同源：只降级**已登记**项）；
* 基线新鲜、现在不新鲜 ⇒ `FRESHNESS_STALE`（block）：这是**回归**，必须给出处置。

三方数字一致性
==============
每个指标声明 artifact(k/n) ↔ paper(k/n 或计数正则) ↔ web(JSON 指针)。
判据：率类 `|差| > tolerance_pp`（默认 0.5pp）⇒ block；计数类要求完全相等。
额外两条**防配置腐烂**的检查：
* 配置里写的论文 k/n 必须与产物**现算** k/n 一致，否则 `CONFIG_STALE`（配置改了没跟上产物）；
* artifact 里 `stored` 率若与现算 k/n 不符 ⇒ `ARTIFACT_INCONSISTENT`（产物自身不自洽）。
以及一条**不假装一致**的提示：`newer_artifact`（更新的那一轮 reveal）与被引用的数字不同时
只 WARN 并写明 `owner=671b` —— 论文/前端更新不是本工具的事，但也不能当没看见。

受控目录
========
只读。唯一写盘 = `--init/--update` 写基线（默认 `data/guard_rerun_baseline_671a.json`）。
绝不写 `atoms/ evidence/ Examples/ Book/`、452 账本、`gate_engine.py`、`counts_659.py`。

用法
====
    python tools/guard_rerun_671a.py                 # 对账（只读）
    python tools/guard_rerun_671a.py --json          # 机读（主门禁消费）
    python tools/guard_rerun_671a.py --init          # 标定/刷新基线（唯一写盘）
    python tools/guard_rerun_671a.py --verify-config # 配置自检（路径存在性 + 产物出处）
    python tools/guard_rerun_671a.py --selftest      # 只读自检

退出码
======
    0 = PASS（无 block）
    1 = RED（有 block）
    2 = 未配置/未标定（缺配置或基线 ⇒ **未进射程 ≠ 通过**）

已知限制（诚实登记）
====================
* 判据指纹只覆盖 `src + deps` 里**列出的**文件；检测器间接依赖（如 `import json`）不在内。
* 局部变量名归一是**启发式**：嵌套作用域 / `global` 语句的极端组合下可能有残差，
  宁可多判红（保守），产物上的 freshness 轴是第二道保险。
* mtime 轴受文件系统精度（部分环境 1s）影响；`--freshness-tol` 可调（默认 1.0s）。
* 与 670c 的关系：670c 的 5 个核心工具由本工具**复用**（import 它的 evaluate），
  不重复实现；两边都跑了也不会得出不同结论。
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:                 # 复用 670c 的纯函数（import 而不是抄）
    sys.path.insert(0, str(_HERE))

SCHEMA = "queyi-guard-rerun/671a"
DEFAULT_DETECTORS = "data/guard_detector_files_671a.json"
DEFAULT_ARTIFACTS = "data/guard_artifacts_671a.json"
DEFAULT_BASELINE = "data/guard_rerun_baseline_671a.json"
DEFAULT_FRESHNESS_TOL = 1.0                    # 秒：多文件写入同秒是常态，留 1s 余量
DEFAULT_TOLERANCE_PP = 0.5                     # 百分点的比较容差
EPS = 1e-9

# ── 状态 ───────────────────────────────────────────────────────────────────────
OK = "OK"
RERUN = "RERUN"
RERUN_ONLY = "RERUN_ONLY"
STALE = "STALE"
ADVISORY_STALE = "ADVISORY_STALE"
PRODUCT_MISSING = "PRODUCT_MISSING"
SRC_MISSING = "SRC_MISSING"
NO_BASELINE_ENTRY = "NO_BASELINE_ENTRY"
NO_PRODUCT = "NO_PRODUCT"
FRESHNESS_STALE = "FRESHNESS_STALE"
FRESHNESS_LEGACY = "FRESHNESS_LEGACY"
# ── 三方一致性 ─────────────────────────────────────────────────────────────────
CONSISTENT = "CONSISTENT"
MISMATCH = "MISMATCH"
CONFIG_STALE = "CONFIG_STALE"
ARTIFACT_INCONSISTENT = "ARTIFACT_INCONSISTENT"
SOURCE_MISSING = "SOURCE_MISSING"
PAPER_MISSING = "PAPER_MISSING"
PAPER_CITATION_MISSING = "PAPER_CITATION_MISSING"
WEB_MISSING = "WEB_MISSING"
PENDING_NEWER = "PENDING_NEWER"

PASS, WARN, BLOCK = "pass", "warn", "block"


# ─────────────────────────────────────────────────────────────────────────────
# 指纹
# ─────────────────────────────────────────────────────────────────────────────

def sha256_file(p: Path) -> str | None:
    """裸字节 sha256；不存在/不可读 ⇒ None（不抛）。"""
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def _strip_docstrings(tree: ast.AST) -> ast.AST:
    """就地剥掉模块/类/函数的文档字符串（注释本来就不进 AST）。"""
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = list(getattr(node, "body", []))
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def _parse(p: Path) -> ast.Module | None:
    try:
        src = p.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        return ast.parse(src)
    except (SyntaxError, ValueError):
        return None


def _iter_nodes(node: ast.AST):
    """稳定的前序遍历（与名字无关 ⇒ 重命名不改变访问顺序）。"""
    yield node
    for child in ast.iter_child_nodes(node):
        yield from _iter_nodes(child)


def _target_names(target: ast.AST) -> set[str]:
    out: set[str] = set()
    for n in _iter_nodes(target):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            out.add(n.id)
    return out


def _module_names(tree: ast.Module) -> set[str]:
    """模块级名字（def/class/import/赋值）——**不**参与局部名归一（改了它们语义就变了）。"""
    out: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                out.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                out |= _target_names(t)
        elif isinstance(node, ast.AnnAssign):
            out |= _target_names(node.target)
        elif isinstance(node, ast.AugAssign):
            out |= _target_names(node.target)
    return out


def _bound_names(fn: ast.AST) -> set[str]:
    """函数体内**绑定**的名字：参数 + Store/Del 目标 + 函数内 import + except 变量。"""
    out: set[str] = set()
    args = getattr(fn, "args", None)
    if args is not None:
        for a in list(getattr(args, "posonlyargs", [])) + list(args.args) + list(args.kwonlyargs):
            out.add(a.arg)
        if args.vararg:
            out.add(args.vararg.arg)
        if args.kwarg:
            out.add(args.kwarg.arg)
    for n in _iter_nodes(fn):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            out.add(n.id)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                out.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, ast.ExceptHandler) and n.name:
            out.add(n.name)
        elif isinstance(n, (ast.Global, ast.Nonlocal)):
            out -= set(n.names)
    return out


class _LocalNameNormalizer(ast.NodeTransformer):
    """把函数内局部名按**首次出现顺序**改写为 v0, v1, …（alpha 等价的规范化）。

    为什么不按字典序：按字典序时 `a,b` → `z,b` 会改变序号，重命名仍会改指纹；
    按首次出现顺序则与名字无关（AST 形状不变 ⇒ 顺序不变 ⇒ 序号不变）。
    """

    def __init__(self, protected: set[str]) -> None:
        self.protected = set(protected)
        self.notes: list[str] = []

    def _normalize_scope(self, fn: ast.AST) -> None:
        nested: set[str] = set()
        for n in _iter_nodes(fn):
            if n is fn:
                continue
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                nested |= _bound_names(n)
        local = (_bound_names(fn) - self.protected) - nested
        if not local:
            return
        mapping: dict[str, str] = {}
        for n in _iter_nodes(fn):
            if isinstance(n, ast.Name) and n.id in local:
                mapping.setdefault(n.id, f"v{len(mapping)}")
            elif isinstance(n, ast.arg) and n.arg in local:
                mapping.setdefault(n.arg, f"v{len(mapping)}")
        if mapping:
            self.notes.append(f"{len(mapping)} 个局部名被归一")
        for n in _iter_nodes(fn):
            if isinstance(n, ast.Name) and n.id in mapping:
                n.id = mapping[n.id]
            elif isinstance(n, ast.arg) and n.arg in mapping:
                n.arg = mapping[n.arg]

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:      # noqa: N802
        self._normalize_scope(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:   # noqa: N802
        self._normalize_scope(node)
        return self.generic_visit(node)

    def visit_Lambda(self, node: ast.Lambda) -> ast.AST:                 # noqa: N802
        self._normalize_scope(node)
        return self.generic_visit(node)


def ast_hash(p: Path) -> str | None:
    """AST 语义哈希（剥文档字符串；注释不进 AST）——诊断层指纹。"""
    tree = _parse(p)
    if tree is None:
        return None
    dumped = ast.dump(_strip_docstrings(tree), annotate_fields=True, include_attributes=False)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()


def judgment_hash(p: Path) -> str | None:
    """判据指纹：AST + 局部变量名归一 —— "改了判据"的判定就用它（注释/重命名不改它）。"""
    tree = _parse(p)
    if tree is None:
        return None
    tree = _strip_docstrings(tree)
    _LocalNameNormalizer(_module_names(tree)).visit(tree)
    dumped = ast.dump(tree, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()


def fingerprint(paths: list[Path]) -> tuple[str | None, dict[str, str | None]]:
    """判据指纹 = 各组件**判据哈希**的字典序拼接再 sha256（组件级明细一并返回，便于定位）。"""
    comps: dict[str, str | None] = {}
    for p in paths:
        comps[str(p)] = judgment_hash(p) if p.is_file() else None
    if not comps or any(v is None for v in comps.values()):
        return None, comps
    payload = "|".join(f"{k}={comps[k]}" for k in sorted(comps))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest(), comps


# ─────────────────────────────────────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────────────────────────────────────

def load_json(p: Path) -> Any | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def normalize_product(entry: Any) -> dict[str, Any]:
    """产物声明支持 `"path"` 与 `{"path": ..., "strict": false}` 两种写法。"""
    if isinstance(entry, str):
        return {"path": entry, "strict": True}
    if isinstance(entry, dict) and entry.get("path"):
        return {"path": str(entry["path"]), "strict": bool(entry.get("strict", True)),
                **{k: v for k, v in entry.items() if k not in ("path", "strict")}}
    raise SystemExit(f"产物声明格式非法（要字符串或含 path 的对象）：{entry!r}")


def load_detectors(root: Path, rel: str) -> tuple[dict[str, Any] | None, Path]:
    p = root / rel
    d = load_json(p)
    if not isinstance(d, dict) or not isinstance(d.get("detectors"), list):
        return None, p
    out: dict[str, Any] = {}
    for det in d["detectors"]:
        if not isinstance(det, dict) or not det.get("id") or not det.get("src"):
            raise SystemExit(f"检测器条目缺 id/src：{det!r}")
        prods = [normalize_product(x) for x in (det.get("products") or [])]
        out[str(det["id"])] = {"src": str(det["src"]),
                               "deps": [str(x) for x in (det.get("deps") or [])],
                               "products": prods, "why": str(det.get("why", ""))}
    return {"schema": d.get("schema"), "note": d.get("note"), "detectors": out}, p


# ─────────────────────────────────────────────────────────────────────────────
# 探测（只读）
# ─────────────────────────────────────────────────────────────────────────────

def probe_detectors(root: Path, reg: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for did, spec in sorted(reg["detectors"].items()):
        src = root / spec["src"]
        deps = [root / d for d in spec["deps"]]
        comps = [src, *deps]
        fp, comp_hashes = fingerprint(comps)
        try:
            src_mtime = src.stat().st_mtime
        except OSError:
            src_mtime = None
        mtimes = []
        for c in comps:
            try:
                mtimes.append(c.stat().st_mtime)
            except OSError:
                continue
        prods: dict[str, Any] = {}
        for pr in spec["products"]:
            pp = root / pr["path"]
            try:
                mt = pp.stat().st_mtime
            except OSError:
                mt = None
            prods[pr["path"]] = {"sha256": sha256_file(pp), "mtime": mt, "strict": pr["strict"]}
        out[did] = {
            "src": spec["src"],
            "deps": list(spec["deps"]),
            "why": spec["why"],
            "judgment_sha256": fp,
            "component_judgment_sha256": {str(Path(k).relative_to(root)) if str(k).startswith(str(root)) else str(k): v
                                        for k, v in comp_hashes.items()},
            "src_sha256": sha256_file(src),
            "src_ast_sha256": ast_hash(src),
            "src_mtime": src_mtime,
            "judgment_mtime": (max(mtimes) if mtimes else None),
            "products": prods,
            "declared_products": [pr["path"] for pr in spec["products"]],
        }
    return out


def compare_detectors(base: dict[str, Any], cur: dict[str, Any],
                      tol: float = DEFAULT_FRESHNESS_TOL) -> list[dict[str, Any]]:
    """逐检测器对账（判据指纹 × 产物指纹 × 新鲜度）。不抛异常。"""
    base_d: dict[str, Any] = base.get("detectors") if isinstance(base.get("detectors"), dict) else {}
    out: list[dict[str, Any]] = []
    for did, c in sorted(cur.items()):
        b = base_d.get(did)
        rec: dict[str, Any] = {"detector": did, "src": c["src"], "deps": c["deps"],
                               "products": [], "notes": []}
        if not isinstance(b, dict):
            rec.update(status=NO_BASELINE_ENTRY, severity=WARN, judgment_changed=None,
                       message="基线里没有该检测器（新注册/基线过旧）⇒ 只登记，不判红")
            rec["notes"].append("处置：确认产物已重跑后 --init 重新标定")
            out.append(rec)
            continue
        if c["src_sha256"] is None:
            rec.update(status=SRC_MISSING, severity=WARN, judgment_changed=None,
                       message="驱动脚本不存在/不可读 ⇒ 无法判定（登记为未进射程）")
            out.append(rec)
            continue

        b_fp, c_fp = b.get("judgment_sha256"), c.get("judgment_sha256")
        if not b_fp or not c_fp:
            rec.update(status=SRC_MISSING, severity=WARN, judgment_changed=None,
                       message="判据指纹缺一侧（依赖文件缺失或基线过旧）⇒ 无法判定，请 --init 重新标定")
            out.append(rec)
            continue
        changed = b_fp != c_fp

        prod_changed: list[str] = []
        prod_missing: list[str] = []
        prod_new: list[str] = []
        fresh_now: list[str] = []
        legacy_fresh: list[str] = []
        stale_fresh: list[str] = []
        b_prods = b.get("products") if isinstance(b.get("products"), dict) else {}
        jm = c.get("judgment_mtime")
        for rel in c["declared_products"]:
            cp_ = c["products"].get(rel) or {}
            bp_ = b_prods.get(rel) or {}
            h_now, h_old = cp_.get("sha256"), bp_.get("sha256")
            if h_now is None:
                prod_missing.append(rel)
            elif h_old is None:
                prod_new.append(rel)
            elif h_old != h_now:
                prod_changed.append(rel)
            # 新鲜度（第二条独立轴）
            mt = cp_.get("mtime")
            if mt is not None and jm is not None:
                is_fresh = mt >= (jm - tol)
                bp_fresh = bp_.get("fresh")
                if bp_fresh is True and not is_fresh:
                    stale_fresh.append(rel)
                elif bp_fresh is False and not is_fresh:
                    legacy_fresh.append(rel)
                if is_fresh:
                    fresh_now.append(rel)
            rec["products"].append({
                "path": rel, "strict": bool(cp_.get("strict", True)),
                "baseline_sha256": h_old, "current_sha256": h_now,
                "changed": bool(h_old and h_now and h_old != h_now),
                "missing": h_now is None,
                "baseline_fresh": bp_.get("fresh"), "fresh": (mt is not None and jm is not None and mt >= jm - tol),
                "product_mtime": mt, "judgment_mtime": jm,
                "delta_s": (None if (mt is None or jm is None) else round(mt - jm, 3)),
            })

        # 诊断：注释/重命名层的变化（不改判据，不要求重跑）
        raw_changed = b.get("src_sha256") != c.get("src_sha256")
        ast_changed = b.get("src_ast_sha256") != c.get("src_ast_sha256")
        if not changed and raw_changed:
            rec["notes"].append("裸哈希变了但**判据指纹没变**"
                                + ("（纯注释/空白改动）" if not ast_changed else "（纯局部重命名，AST 归一后等价）")
                                + " ⇒ 不要求重跑")

        rec.update(judgment_changed=changed,
                   products_changed=sorted(prod_changed + prod_new),
                   products_missing=sorted(prod_missing),
                   freshness={"stale": sorted(stale_fresh), "legacy": sorted(legacy_fresh),
                              "fresh": sorted(fresh_now), "tolerance_s": tol})

        strict_prods = [p for p in c["declared_products"]
                        if bool((c["products"].get(p) or {}).get("strict", True))]
        if not c["declared_products"]:
            rec.update(status=NO_PRODUCT, severity=WARN,
                       message="该检测器未声明落盘产物 ⇒ 本门禁对它无射程（不假装覆盖）")
        elif prod_missing:
            rec.update(status=PRODUCT_MISSING, severity=BLOCK,
                       message=f"产物缺失（{', '.join(prod_missing)}）⇒ 无法对账："
                               "缺产物不是「没问题」，是「没跑」（fail-closed）")
        elif changed and (prod_changed or prod_new):
            rec.update(status=RERUN, severity=PASS,
                       message=f"判据已变且产物已刷新（{len(prod_changed + prod_new)} 个）⇒ 改了也重跑了")
        elif changed and stale_fresh:
            rec.update(status=FRESHNESS_STALE, severity=BLOCK,
                       message="判据变了、产物不早于代码的**关系**被破坏"
                               f"（{', '.join(stale_fresh)}）⇒ 产物过期，必须重跑")
        elif changed:
            hashes = [p["path"] for p in rec["products"] if p["changed"]]
            all_advisory = bool(c["declared_products"]) and not strict_prods
            if hashes or not all_advisory:
                rec.update(status=STALE, severity=BLOCK,
                           message="判据指纹已变，但产物哈希与基线一致 ⇒ 改了检测器没重跑产物（假绿风险）")
            else:
                rec.update(status=ADVISORY_STALE, severity=WARN,
                           message="判据已变，但该检测器的产物全为 advisory（需慢操作才能复跑）⇒ 只提醒")
        elif prod_changed or prod_new:
            rec.update(status=RERUN_ONLY, severity=PASS,
                       message="判据未变、产物已变 ⇒ 只是重跑过（若并未重跑，说明产物非确定性，值得复核）")
        else:
            rec.update(status=OK, severity=PASS, message="判据与产物均未变")

        if rec["status"] != FRESHNESS_STALE and stale_fresh and rec["status"] in (OK, RERUN_ONLY):
            rec.update(status=FRESHNESS_STALE, severity=BLOCK,
                       message=f"产物过期：{', '.join(stale_fresh)} 早于判据代码（基线上是新鲜的）⇒ 必须重跑")
        if legacy_fresh:
            rec["notes"].append(f"存量缺口（基线时即不新鲜）：{', '.join(legacy_fresh)} ⇒ "
                                "登记不判红；重跑该产物后本项自动收紧")
            if rec["status"] == OK:
                rec["freshness_note"] = FRESHNESS_LEGACY
        if rec.get("severity") == BLOCK:
            rec["notes"].append("处置：重跑该检测器的落盘命令**之后**再 --init 刷新基线（不得只 --init 了事）")
        out.append(rec)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 三方数字一致性
# ─────────────────────────────────────────────────────────────────────────────

def resolve_pointer(obj: Any, pointer: str) -> tuple[bool, Any]:
    """按 `a.b.0.c` 取值；任一段缺失 ⇒ (False, None)。数字段按 list 下标解释。"""
    cur = obj
    for seg in [s for s in str(pointer).split(".") if s != ""]:
        if isinstance(cur, dict):
            if seg not in cur:
                return False, None
            cur = cur[seg]
        elif isinstance(cur, list):
            if not seg.lstrip("-").isdigit():
                return False, None
            i = int(seg)
            if i < 0 or i >= len(cur):
                return False, None
            cur = cur[i]
        else:
            return False, None
    return True, cur


def artifact_value(root: Path, spec: dict[str, Any], kind: str) -> dict[str, Any]:
    """从产物算出 (值, k, n)；任何缺失都显式登记（不猜）。"""
    path = root / str(spec.get("path", ""))
    d = load_json(path)
    if d is None:
        return {"ok": False, "why": f"产物缺失/不可解析：{spec.get('path')}"}
    if kind == "count":
        if spec.get("len"):
            if not isinstance(d, list):
                return {"ok": False, "why": f"{spec.get('path')} 不是数组，无法取长度"}
            return {"ok": True, "value": len(d), "k": None, "n": None}
        found, v = resolve_pointer(d, str(spec.get("pointer", "")))
        return {"ok": found, "value": v, "k": None, "n": None,
                "why": "" if found else f"指针取不到：{spec.get('pointer')}"}
    found_k, k = resolve_pointer(d, str(spec.get("k", "")))
    n = 0
    for p in (spec.get("n_sum") or []):
        f, v = resolve_pointer(d, str(p))
        if not f:
            return {"ok": False, "why": f"分母指针取不到：{p}"}
        n += int(v)
    if not found_k:
        return {"ok": False, "why": f"分子指针取不到：{spec.get('k')}"}
    if n <= 0:
        return {"ok": False, "why": "分母为 0 ⇒ 拒绝给率（fail-loud）"}
    value = round(int(k) / n * 100, 4)
    stored = None
    if spec.get("stored"):
        fs, sv = resolve_pointer(d, str(spec["stored"]))
        stored = sv if fs else None
    return {"ok": True, "value": value, "k": int(k), "n": n, "stored": stored}


def resolve_source(root: Path, rel: str) -> tuple[Path | None, list[str]]:
    """解析配置里的路径：支持 `*` 通配，取**版本号最大**的那一份。

    为什么支持通配：论文在批次之间会升级（v0.8 → v0.9），配置若写死版本号就会在下一次
    升级时"论文不存在 ⇒ 判红"，那是版本迁移的正常代价被当成了缺陷。通配 + 取最新，
    语义仍然是"当前稿必须与产物一致"（历史稿本来就与今天的产物不同）。
    """
    rel = str(rel)
    if "*" not in rel and "?" not in rel:
        p = root / rel
        return (p if p.is_file() else None), ([p.name] if p.is_file() else [])
    cands = sorted(p for p in root.glob(rel) if p.is_file())

    def ver(p: Path) -> tuple:
        import re
        m = re.search(r"_v(\d+(?:\.\d+)*)", p.name)
        return tuple(int(x) for x in m.group(1).split(".")) if m else (0,)

    if not cands:
        return None, []
    cands.sort(key=ver)
    return cands[-1], [p.name for p in cands]


def paper_citation(root: Path, spec: dict[str, Any], k: int | None, n: int | None) -> dict[str, Any]:
    """论文侧：率类找 `pct（k/n` 三元组；计数类用正则。支持通配（取当前稿）。"""
    p, seen = resolve_source(root, str(spec.get("path", "")))
    if p is None:
        return {"ok": False, "status": PAPER_MISSING,
                "why": f"论文不存在：{spec.get('path')}（匹配到的文件：{seen or '无'}）"}
    txt = p.read_text(encoding="utf-8")
    used = str(p.relative_to(root).as_posix()) if p.is_relative_to(root) else str(p)
    if spec.get("pattern"):
        import re
        m = re.search(str(spec["pattern"]), txt)
        if not m:
            return {"ok": False, "status": PAPER_CITATION_MISSING, "file": used,
                    "why": f"{used} 里找不到正则 {spec['pattern']}"}
        return {"ok": True, "value": int(m.group(1)), "raw": m.group(0)[:60], "file": used}
    import re
    #: 不要求紧跟右括号：论文里同一处可能写 `87.5%（14/16，95% CI [..]）` 或 `87.5% (14/16)`
    pat = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*[（(]\s*(\d+)\s*/\s*(\d+)(?!\d)")
    for m in pat.finditer(txt):
        if int(m.group(2)) == k and int(m.group(3)) == n:
            return {"ok": True, "value": float(m.group(1)), "raw": m.group(0)[:60], "file": used}
    return {"ok": False, "status": PAPER_CITATION_MISSING, "file": used,
            "why": f"{used} 里找不到 {k}/{n} 对应的百分比（配置里的 k/n 可能已过期）"}


def check_metric(root: Path, m: dict[str, Any], tol: float) -> dict[str, Any]:
    """单个指标的三方对账。"""
    kind = str(m.get("kind", "rate"))
    rec: dict[str, Any] = {"key": m.get("key"), "label": m.get("label"), "kind": kind,
                           "unit": m.get("unit"), "checks": [], "notes": []}
    art = artifact_value(root, m.get("artifact") or {}, kind)
    rec["artifact"] = art
    if not art.get("ok"):
        rec.update(status=SOURCE_MISSING, severity=BLOCK,
                   message=f"产物侧无法取数：{art.get('why')}")
        return rec
    a_val = art["value"]

    bad: list[str] = []
    pending_notes: list[str] = []      # 只装「更新的一轮与被引用值不同」这类待认领事项
    info_notes: list[str] = []         # 说明性信息：不影响状态

    # 配置 ↔ 产物（防配置腐烂）
    pspec = m.get("paper") or {}
    if kind == "rate" and (pspec.get("k") is not None or pspec.get("n") is not None):
        if int(pspec.get("k", -1)) != art["k"] or int(pspec.get("n", -1)) != art["n"]:
            bad.append(f"配置声明的论文 k/n={pspec.get('k')}/{pspec.get('n')} 与产物现算 "
                       f"{art['k']}/{art['n']} 不一致（配置过期或产物换了口径）")
            rec["checks"].append({"side": "config", "value": f"{pspec.get('k')}/{pspec.get('n')}",
                                  "expected": f"{art['k']}/{art['n']}", "ok": False})
        else:
            rec["checks"].append({"side": "config", "value": f"{art['k']}/{art['n']}", "ok": True})

    # 产物自身自洽（stored 率 vs 现算 k/n）
    stored = art.get("stored")
    if kind == "rate" and isinstance(stored, (int, float)):
        ok_stored = abs(float(stored) - float(a_val)) <= tol + EPS
        rec["checks"].append({"side": "artifact.stored", "value": stored, "expected": a_val,
                              "ok": ok_stored})
        if not ok_stored:
            bad.append(f"产物自身不自洽：stored={stored} vs 现算 {a_val}（k/n={art['k']}/{art['n']}）")

    # 论文
    pap = paper_citation(root, pspec, art["k"], art["n"])
    rec["paper"] = pap
    if not pap.get("ok"):
        if pap.get("status") == PAPER_MISSING:
            rec["notes"].append(pap.get("why", ""))
            rec["checks"].append({"side": "paper", "value": None, "ok": False,
                                  "note": "论文缺失 ⇒ 该项未进射程（不假装一致）"})
            bad.append("论文文件不存在，三方校验未生效")
        else:
            rec["checks"].append({"side": "paper", "value": None, "ok": False})
            bad.append(pap.get("why", "论文侧取数失败"))
    else:
        diff = abs(float(pap["value"]) - float(a_val))
        ok_p = (diff <= tol + EPS) if kind == "rate" else (int(pap["value"]) == int(a_val))
        rec["checks"].append({"side": "paper", "value": pap["value"], "file": pap.get("file"),
                              "expected": a_val, "diff": round(diff, 4), "ok": ok_p,
                              "raw": pap.get("raw")})
        if not ok_p:
            bad.append(f"论文 {pap['value']} 与产物 {a_val} 差 {round(diff, 4)} > 容差 {tol}")
        if kind == "count":
            info_notes.append("计数类要求完全相等（不套用率的容差）")

    # 前端
    for w in (m.get("web") or []):
        wp = root / str(w.get("path", ""))
        wd = load_json(wp)
        if wd is None:
            rec["checks"].append({"side": f"web:{w.get('path')}", "value": None, "ok": False})
            bad.append(f"前端文件缺失/不可解析：{w.get('path')}（前端数字无从核对）")
            continue
        found, val = resolve_pointer(wd, str(w.get("pointer", "")))
        if not found:
            rec["checks"].append({"side": f"web:{w.get('path')}::{w.get('pointer')}",
                                  "value": None, "ok": False})
            bad.append(f"前端指针取不到：{w.get('path')}::{w.get('pointer')}"
                       "（前端改了键名或该数字被删 ⇒ 不许静默）")
            continue
        diff = abs(float(val) - float(a_val))
        ok_w = (diff <= tol + EPS) if kind == "rate" else (int(val) == int(a_val))
        rec["checks"].append({"side": f"web:{w.get('path')}::{w.get('pointer')}",
                              "value": val, "expected": a_val, "diff": round(diff, 4), "ok": ok_w})
        if not ok_w:
            bad.append(f"前端 {w.get('path')}::{w.get('pointer')}={val} 与产物 {a_val} 差 "
                       f"{round(diff, 4)} > 容差 {tol}")

    # 更新的那一轮（不假装一致）
    na = m.get("newer_artifact")
    if isinstance(na, dict) and na.get("path"):
        nv = artifact_value(root, na, kind)
        if nv.get("ok"):
            diff = abs(float(nv["value"]) - float(a_val))
            if diff > tol + EPS:
                pending_notes.append(
                    f"更新的一轮（{na['path']}）现算 {nv['value']} 与被引用的 {a_val} 不同 ⇒ "
                    f"论文/前端尚未跟上（owner={na.get('owner', 'TBD')}，**不判红**但必须有人认领）")
                rec["pending_newer"] = {"path": na["path"], "value": nv["value"],
                                        "cited": a_val, "owner": na.get("owner"),
                                        "note": na.get("note", "")}
        else:
            pending_notes.append(f"newer_artifact 取数失败（{na['path']}）：{nv.get('why')}")

    rec["notes"] += info_notes + pending_notes
    if bad:
        rec.update(status=MISMATCH, severity=BLOCK, message="；".join(bad))
    elif pending_notes:
        rec.update(status=PENDING_NEWER, severity=WARN, message="；".join(pending_notes))
    else:
        rec.update(status=CONSISTENT, severity=PASS,
                   message=f"三方一致：产物 {a_val}{rec['unit'] or ''} = 论文 = 前端（容差 {tol}）")
    return rec


def check_three_way(root: Path, acfg: dict[str, Any], tol: float) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for m in (acfg.get("metrics") or []):
        try:
            out.append(check_metric(root, m, tol))
        except Exception as e:                     # noqa: BLE001  门禁自身不得崩
            out.append({"key": m.get("key"), "status": MISMATCH, "severity": BLOCK,
                        "message": f"指标校验异常：{type(e).__name__}: {e}", "checks": []})
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 670c 复用
# ─────────────────────────────────────────────────────────────────────────────

def core_670c(root: Path) -> dict[str, Any]:
    """复用 670c 的 5 个核心工具对账（import 它的纯函数，不重写一份）。"""
    try:
        import guard_rerun_670c as G670           # noqa: PLC0415
    except Exception as e:                        # noqa: BLE001
        return {"available": False, "overall": "UNKNOWN",
                "message": f"670c 守卫不可用（{type(e).__name__}: {e}）⇒ 核心工具层未进射程",
                "counts": {}}
    res = G670.evaluate(root, root / G670.DEFAULT_BASELINE)
    return {"available": True, "overall": res["overall"], "armed": res["armed"],
            "counts": res["counts"], "baseline": res["baseline"],
            "message": res["message"], "stale_tools": [v["tool"] for v in res["verdicts"]
                                                        if v["severity"] == G670.BLOCK]}


# ─────────────────────────────────────────────────────────────────────────────
# 基线与评估
# ─────────────────────────────────────────────────────────────────────────────

def build_baseline(root: Path, reg: dict[str, Any], acfg: dict[str, Any] | None,
                   tol: float = DEFAULT_FRESHNESS_TOL) -> dict[str, Any]:
    det = probe_detectors(root, reg)
    for d in det.values():
        jm = d["judgment_mtime"]
        for rel, pr in d["products"].items():
            mt = pr["mtime"]
            pr["fresh"] = bool(mt is not None and jm is not None and mt >= jm - tol)
    three = ({m.get("key"): artifact_value(root, m.get("artifact") or {}, str(m.get("kind", "rate")))
              for m in (acfg.get("metrics") or [])} if isinstance(acfg, dict) else {})
    return {
        "schema": SCHEMA,
        "generated_by": "tools/guard_rerun_671a.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": ("基线 = 一次「判据指纹 + 产物指纹/mtime + 三方数字」快照。判据变了而产物没变 ⇒ STALE。"
                 "刷新基线请在**确认产物已重跑**之后执行 --init。"
                 "基线时即不新鲜的产物会被记成 fresh=false ⇒ 之后只 WARN（存量缺口，不变成噪音）。"),
        "freshness_tolerance_s": tol,
        "detectors": det,
        "three_way": three,
    }


def evaluate(root: Path = ROOT, baseline: Path | None = None,
             detectors_rel: str = DEFAULT_DETECTORS, artifacts_rel: str = DEFAULT_ARTIFACTS,
             tol: float = DEFAULT_TOLERANCE_PP, freshness_tol: float = DEFAULT_FRESHNESS_TOL,
             include_core: bool = True) -> dict[str, Any]:
    """完整评估（只读）。"""
    bp = baseline if baseline is not None else (root / DEFAULT_BASELINE)
    reg, dpath = load_detectors(root, detectors_rel)
    acfg = load_json(root / artifacts_rel)
    base = load_json(bp) if bp.is_file() else None
    notes: list[str] = []

    if reg is None or not isinstance(acfg, dict):
        return {
            "schema": SCHEMA, "tool": "guard_rerun_671a", "root": str(root),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "configured": False, "armed": False, "overall": "UNCONFIGURED",
            "config": {"detectors": str(dpath), "artifacts": str(root / artifacts_rel),
                       "detectors_found": reg is not None, "artifacts_found": isinstance(acfg, dict),
                       "baseline": str(bp), "baseline_found": isinstance(base, dict)},
            "detector_counts": {}, "verdicts": [], "three_way": {"metrics": []},
            "core_670c": {}, "notes": ["配置缺失 ⇒ 未进射程（≠ 通过）。"],
            "message": (f"配置文件缺失：{dpath if reg is None else ''} "
                        f"{root / artifacts_rel if not isinstance(acfg, dict) else ''}"
                        " ⇒ 请先补齐 data/guard_detector_files_671a.json 与 data/guard_artifacts_671a.json"),
        }

    cur = probe_detectors(root, reg)
    verdicts: list[dict[str, Any]] = []
    if isinstance(base, dict):
        verdicts = compare_detectors(base, cur, freshness_tol)
    else:
        for did, c in sorted(cur.items()):
            verdicts.append({"detector": did, "src": c["src"], "deps": c["deps"],
                             "status": NO_BASELINE_ENTRY, "severity": WARN, "judgment_changed": None,
                             "products": [], "notes": ["无基线 ⇒ 只记录，不判红"],
                             "message": "未标定基线 ⇒ 该检测器未进射程（先 --init）"})

    metrics = check_three_way(root, acfg, tol)

    blocks = [v for v in verdicts if v["severity"] == BLOCK]
    warns = [v for v in verdicts if v["severity"] == WARN]
    m_bad = [m for m in metrics if m["severity"] == BLOCK]
    m_warn = [m for m in metrics if m["severity"] == WARN]
    core = core_670c(root) if include_core else {}
    core_bad = bool(core.get("overall") == "RED")

    armed = isinstance(base, dict)
    overall = "RED" if (blocks or m_bad or core_bad) else ("PASS" if armed else "UNARMED")
    if not armed:
        notes.append("未找到基线 ⇒ 检测器层「未进射程」（无法证明任何产物是新的）；先 --init 标定。")
    if m_warn:
        notes.append(f"{len(m_warn)} 条指标只是「更新的一轮与被引用值不同」（owner 认领中），不判红。")
    notes.append("新鲜度（mtime）轴只对**基线上即新鲜**的产物判红；基线时即不新鲜的存量缺口登记为 WARN，不变成噪音。")
    counts = {
        "detectors": len(verdicts),
        "ok": sum(1 for v in verdicts if v["status"] == OK),
        "rerun": sum(1 for v in verdicts if v["status"] in (RERUN, RERUN_ONLY)),
        "stale": len(blocks),
        "warn": len(warns),
        "products": sum(len(v.get("declared_products", v.get("products", []))) for v in cur.values()),
        "metrics": len(metrics),
        "metrics_block": len(m_bad),
        "metrics_warn": len(m_warn),
    }
    return {
        "schema": SCHEMA, "tool": "guard_rerun_671a", "root": str(root),
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "configured": True, "armed": armed, "overall": overall,
        "config": {"detectors": str(dpath), "artifacts": str(root / artifacts_rel),
                   "detectors_found": True, "artifacts_found": True,
                   "baseline": str(bp), "baseline_found": armed,
                   "tolerance_pp": tol, "freshness_tolerance_s": freshness_tol},
        "detector_counts": counts,
        "verdicts": verdicts,
        "three_way": {"tolerance_pp": tol, "metrics": metrics,
                      "consistent": sum(1 for m in metrics if m["status"] == CONSISTENT),
                      "pending": sum(1 for m in metrics if m["status"] == PENDING_NEWER),
                      "blocked": sum(1 for m in metrics if m["severity"] == BLOCK)},
        "core_670c": core,
        "probed": cur,
        "notes": notes,
        "message": ("发现 block：" + "；".join([v["detector"] for v in blocks]
                                              + [m["key"] for m in m_bad]) if (blocks or m_bad)
                    else ("检测器对账 + 三方数字一致（基线已标定）" if armed else "未标定 ⇒ 未进射程")),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 配置自检 / 渲染 / CLI
# ─────────────────────────────────────────────────────────────────────────────

def verify_config(root: Path, reg: dict[str, Any]) -> dict[str, Any]:
    """配置自检：源码/依赖存在 + 产物出处（产品名出现在检测器源码里）。"""
    problems: list[dict[str, Any]] = []
    for did, spec in sorted(reg["detectors"].items()):
        src = root / spec["src"]
        if not src.is_file():
            problems.append({"detector": did, "kind": "src-missing", "path": spec["src"]})
            continue
        for d in spec["deps"]:
            if not (root / d).is_file():
                problems.append({"detector": did, "kind": "dep-missing", "path": d})
        blob = src.read_text(encoding="utf-8", errors="replace")
        for dep in spec["deps"]:
            dp = root / dep
            if dp.is_file():
                blob += dp.read_text(encoding="utf-8", errors="replace")
        for pr in spec["products"]:
            base = Path(pr["path"]).name
            if base not in blob:
                problems.append({"detector": did, "kind": "product-not-referenced",
                                 "path": pr["path"],
                                 "hint": "产物名没出现在 src+deps 源码里（路径可能由变量拼出）⇒ 只提示"})
    return {"ok": not [p for p in problems if p["kind"] in ("src-missing", "dep-missing")],
            "problems": problems}


def render(res: dict[str, Any]) -> str:
    if not res["configured"]:
        return f"[guard-rerun-671a] overall=UNCONFIGURED\n  {res['message']}"
    c = res["detector_counts"]
    L = [f"[guard-rerun-671a] overall={res['overall']}  detectors={c['detectors']}  "
         f"ok={c['ok']} rerun={c['rerun']} block={c['stale']} warn={c['warn']}  "
         f"产物={c['products']}",
         f"  基线：{res['config']['baseline']}"
         + ("" if res["armed"] else "（缺失 ⇒ 未进射程）")]
    for v in res["verdicts"]:
        L.append(f"  [{v['status']:17}] {v['detector']:22} judgment_changed={v.get('judgment_changed')}")
        L.append(f"      {v['message']}")
        for n in v.get("notes", [])[:2]:
            L.append(f"      · {n}")
    tw = res["three_way"]
    L.append(f"  三方数字：一致={tw['consistent']} 待认领={tw['pending']} block={tw['blocked']}"
             f"（容差 ±{tw['tolerance_pp']}pp）")
    for m in tw["metrics"]:
        L.append(f"  [{m['status']:22}] {m['key']:20} {m['message'][:96]}")
    core = res.get("core_670c") or {}
    if core:
        L.append(f"  670c 核心工具层：overall={core.get('overall')} "
                 f"{core.get('counts', {})}")
    for n in res["notes"]:
        L.append(f"  [note] {n}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        p = t / "a.py"
        p.write_text("def f(x):\n    y = x + 1\n    return y\n", encoding="utf-8")
        h0, a0, j0 = sha256_file(p), ast_hash(p), judgment_hash(p)
        chk("三种指纹都稳定", sha256_file(p) == h0 and ast_hash(p) == a0 and judgment_hash(p) == j0)
        p.write_text("# 注释\ndef f(x):\n    y = x + 1\n    return y\n", encoding="utf-8")
        chk("注释：裸哈希变、判据不变", sha256_file(p) != h0 and judgment_hash(p) == j0)
        p.write_text("def f(x):\n    zz = x + 1\n    return zz\n", encoding="utf-8")
        chk("局部重命名：AST 变、判据不变",
            ast_hash(p) != a0 and judgment_hash(p) == j0)
        p.write_text("def f(x):\n    y = x + 2\n    return y\n", encoding="utf-8")
        chk("改逻辑：判据必变", judgment_hash(p) != j0)
        p.write_text("def g(x):\n    y = x + 1\n    return y\n", encoding="utf-8")
        chk("改函数名：判据必变（模块级名不归一）", judgment_hash(p) != j0)
        p.write_text('S = "a"\ndef f(x):\n    y = x + 1\n    return S\n', encoding="utf-8")
        j1 = judgment_hash(p)
        p.write_text('S = "b"\ndef f(x):\n    y = x + 1\n    return S\n', encoding="utf-8")
        chk("改模块常量：判据必变", judgment_hash(p) != j1)
        ghost = t / "nope.py"
        chk("缺失文件返回 None（不抛）",
            sha256_file(ghost) is None and ast_hash(ghost) is None and judgment_hash(ghost) is None)
        fp, comps = fingerprint([p])
        chk("组合指纹可算且含组件明细", bool(fp) and len(comps) == 1)
        chk("组合指纹缺组件 ⇒ None", fingerprint([p, ghost])[0] is None)

    chk("指针解析：字典/数组", resolve_pointer({"a": {"b": [1, 2, 3]}}, "a.b.1") == (True, 2))
    chk("指针解析：缺失 ⇒ False", resolve_pointer({"a": 1}, "a.b") == (False, None))
    chk("指针解析：越界 ⇒ False", resolve_pointer({"a": [1]}, "a.5") == (False, None))

    reg, _ = load_detectors(ROOT, DEFAULT_DETECTORS)
    chk("本仓检测器配置可载入", reg is not None and len(reg["detectors"]) >= 8)
    acfg = load_json(ROOT / DEFAULT_ARTIFACTS)
    chk("本仓产物配置可载入", isinstance(acfg, dict) and len(acfg.get("metrics", [])) >= 3)
    chk("每个检测器都有 src + 产物声明",
        all(v["src"] and v["products"] for v in reg["detectors"].values()))
    ver = verify_config(ROOT, reg)
    chk("配置自检无致命问题（源码/依赖都在）", bool(ver["ok"]))
    print(f"guard_rerun_671a selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671a A：防复发（改检测器必重跑）+ 新鲜度 + 三方一致")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件上级目录；测试用）")
    ap.add_argument("--baseline", default=None, help=f"基线路径（默认 {DEFAULT_BASELINE}）")
    ap.add_argument("--detectors", default=None, help=f"检测器清单（默认 {DEFAULT_DETECTORS}）")
    ap.add_argument("--artifacts", default=None, help=f"三方数字配置（默认 {DEFAULT_ARTIFACTS}）")
    ap.add_argument("--init", "--update", dest="init", action="store_true",
                    help="把当前指纹写为基线（唯一写盘操作）")
    ap.add_argument("--tolerance-pp", type=float, default=DEFAULT_TOLERANCE_PP,
                    help=f"三方数字容差（百分点，默认 {DEFAULT_TOLERANCE_PP}）")
    ap.add_argument("--freshness-tol", type=float, default=DEFAULT_FRESHNESS_TOL,
                    help=f"新鲜度容差（秒，默认 {DEFAULT_FRESHNESS_TOL}）")
    ap.add_argument("--no-core", action="store_true", help="不跑 670c 核心工具层（只测 671a 层）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verify-config", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    root = Path(a.root).resolve() if a.root else ROOT
    drel = a.detectors or DEFAULT_DETECTORS
    arel = a.artifacts or DEFAULT_ARTIFACTS
    bp = Path(a.baseline) if a.baseline else (root / DEFAULT_BASELINE)

    reg, dpath = load_detectors(root, drel)
    if reg is None:
        msg = {"schema": SCHEMA, "configured": False, "detectors_found": False,
               "path": str(dpath), "message": f"检测器清单缺失/格式错误：{dpath}"}
        print(json.dumps(msg, ensure_ascii=False, indent=2) if a.json else msg["message"])
        return 2

    if a.verify_config:
        ver = verify_config(root, reg)
        if a.json:
            print(json.dumps(ver, ensure_ascii=False, indent=2))
        else:
            print(f"[guard-rerun-671a] 配置自检：{'PASS' if ver['ok'] else 'FAIL'} "
                  f"（{len(ver['problems'])} 条提示）")
            for p in ver["problems"]:
                print(f"  [{p['kind']}] {p['detector']}: {p['path']}")
        return 0 if ver["ok"] else 1

    if a.init:
        acfg = load_json(root / arel)
        base = build_baseline(root, reg, acfg if isinstance(acfg, dict) else None,
                              a.freshness_tol)
        bp.parent.mkdir(parents=True, exist_ok=True)
        bp.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        msg = {"schema": SCHEMA, "updated": True, "baseline": str(bp),
               "detectors": sorted(base["detectors"]),
               "legacy_unfresh": {d: [k for k, v in dd["products"].items() if not v["fresh"]]
                                  for d, dd in base["detectors"].items()
                                  if any(not v["fresh"] for v in dd["products"].values())}}
        if a.json:
            print(json.dumps(msg, ensure_ascii=False, indent=2))
        else:
            print(f"[guard-rerun-671a] 基线已写入 {bp}（{len(base['detectors'])} 个检测器）")
            for d, prods in msg["legacy_unfresh"].items():
                print(f"  [存量] {d}: {prods} 在基线时刻即早于判据代码（记 fresh=false ⇒ 之后只 WARN）")
        return 0

    res = evaluate(root, bp, drel, arel, a.tolerance_pp, a.freshness_tol,
                   include_core=not a.no_core)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    if not res["configured"]:
        return 2
    if not res["armed"]:
        return 2                                  # 未进射程 ≠ 通过
    return 1 if res["overall"] == "RED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
