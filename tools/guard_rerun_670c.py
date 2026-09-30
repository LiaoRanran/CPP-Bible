#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""guard_rerun_670c.py — 670c D2：核心工具「改了代码没重跑产物」守卫。

为什么要有它（668 R4/R6 的形态固化）
====================================
667 抓到两次同类翻车：声称 holdout 81.2% / 反事实 F1=1.0，落盘产物里却是 66.7% / 0.0。
根因不是算错，而是**改了判定代码却没有重跑落盘**——产物还是旧代码的结论，但所有人
（含 CI）看到的都是「绿灯 + 新代码」。这类假绿没有任何单点门禁能看见，因为：

    * 产物哈希对得上自己（没被手改）⇒ G-DENOMINATOR 之类查不出来；
    * 测试全绿（测试跑的是**新代码**，本来就应该绿）⇒ pytest 查不出来。

唯一能看见它的判据是**跨时间的两两对账**：记住「上次记录的 (源码指纹, 产物指纹)」，
下次跑的时候比较。四种组合里只有一种有问题：

    | 源码语义 | 产物 | 判定 | 含义 |
    |---|---|---|---|
    | 没变 | 没变 | OK | 什么都没发生 |
    | 没变 | 变了 | RERUN_ONLY | 单纯重跑了（也提示产物是否非确定性） |
    | 变了 | 变了 | RERUN | 改了也重跑了 ⇒ 正常 |
    | **变了** | **没变** | **STALE（红）** | **改了代码没重跑产物 ⇒ 假绿风险** |

设计约定
========
1. **源码指纹用 AST（语义）哈希，不用裸字节哈希**：只改注释/文档字符串不该判红
   （否则门禁会变成「狼来了」，反面教材见 docs/gate_tiers_658.md §2 的两层模型动机）。
   AST 解析失败（语法错误 / 非 Python）才回退裸 sha256，并在报告里标明用的是哪一种。
2. **产物哈希用裸 sha256**：产物是数据，一个字节也不能变。
3. **不写任何受控目录**：本工具只读；唯一写盘是 `--update` 写基线文件（默认
   `data/guard_rerun_baseline_670c.json`，可用 `--baseline` 改到别处）。
4. **缺失文件容错**：源码/产物任一缺失都不崩，只降级为对应状态并打印（「没跑」≠「没问题」）。
5. 纯标准库，零第三方依赖（可在裸 CI Python 上跑）。

核心工具清单（真实文件名已核实；`tools/.tool_checksums` 的默认段正是这五个）
=================================================================================
| 键 | 源码 | 落盘产物（重跑会刷新） |
|---|---|---|
| gate_engine | tools/gate_engine.py | data/_gate_rules.json · tools/assert_count_baseline.json |
| atom_evidence_replay | tools/atom_evidence_replay.py | build/replay_manifest.json |
| poison_drill | tools/poison_drill.py | tools/poison_surface_map.json |
| toolchain | tools/toolchain.py | （无 —— 纯只读解析库，见 NO_PRODUCT） |
| cppbible | tools/cppbible.py | tools/compile_report.json |

用法
====
    python tools/guard_rerun_670c.py              # 对账（只读），exit 0=PASS 1=STALE 2=无基线
    python tools/guard_rerun_670c.py --json       # 机读输出（供主门禁消费）
    python tools/guard_rerun_670c.py --update     # 记录/刷新基线（唯一写盘操作）
    python tools/guard_rerun_670c.py --selftest   # 只读自检（哈希稳定性）

已知限制（诚实登记）
====================
* 只覆盖**注册在册**的 5 个核心工具；未注册工具改代码不重跑仍看不见。
* `toolchain.py` 无落盘产物 ⇒ 本门禁对它无射程（NO_PRODUCT，advisory，不假装覆盖）。
* 「产物变了」只证明「重跑过」，不证明「跑对了」——正确性由 669d 六条规则与 replay 守。
* 基线时间点之后若有人**手工**改了产物，本门禁只报 RERUN_ONLY，无法区分手工与重跑。
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-guard-rerun/v1"
DEFAULT_BASELINE = "data/guard_rerun_baseline_670c.json"

#: 状态常量
OK = "OK"
RERUN = "RERUN"
RERUN_ONLY = "RERUN_ONLY"
STALE = "STALE"
SRC_MISSING = "SRC_MISSING"
NO_BASELINE_ENTRY = "NO_BASELINE_ENTRY"
PRODUCT_MISSING = "PRODUCT_MISSING"
NO_PRODUCT = "NO_PRODUCT"

PASS, WARN, BLOCK = "pass", "warn", "block"

#: 核心工具注册表。products 只列**该工具重跑时会重写**的真实产物（已逐个核实存在）。
CORE_TOOLS: dict[str, dict[str, Any]] = {
    "gate_engine": {
        "src": "tools/gate_engine.py",
        "products": ["data/_gate_rules.json", "tools/assert_count_baseline.json"],
        "why": "规则引擎：规则集缓存与断言计数基线由它派生（661 A2 口径裁定）。",
    },
    "atom_evidence_replay": {
        "src": "tools/atom_evidence_replay.py",
        "products": ["build/replay_manifest.json"],
        "why": "证据复算：清单是它唯一的落盘结论（增量判定的依据）。",
    },
    "poison_drill": {
        "src": "tools/poison_drill.py",
        "products": ["tools/poison_surface_map.json"],
        "why": "毒样例钻探：攻击面台账由 --write-surface-map 实测落盘。",
    },
    "toolchain": {
        "src": "tools/toolchain.py",
        "products": [],
        "why": "工具链解析库：只读解析 toolchain.toml，无落盘产物 ⇒ 本门禁对它无射程。",
    },
    "cppbible": {
        "src": "tools/cppbible.py",
        "products": ["tools/compile_report.json"],
        "why": "编译编排：编译报告是它落盘的结论（compile_gate 的输入）。",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 指纹
# ─────────────────────────────────────────────────────────────────────────────

def sha256_file(p: Path) -> str | None:
    """裸字节 sha256；文件不存在/不可读 ⇒ None（不抛）。"""
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


def semantic_hash(p: Path) -> str | None:
    """AST 语义哈希：注释/文档字符串变更不改变它；语法错误 ⇒ None（调用方回退裸哈希）。"""
    try:
        src = p.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError):
        return None
    dumped = ast.dump(_strip_docstrings(tree), annotate_fields=True, include_attributes=False)
    return hashlib.sha256(dumped.encode("utf-8")).hexdigest()


def probe(root: Path) -> dict[str, dict[str, Any]]:
    """现算全部核心工具的（源码指纹, 产物指纹）。纯只读。"""
    out: dict[str, dict[str, Any]] = {}
    for name, spec in sorted(CORE_TOOLS.items()):
        sp = root / str(spec["src"])
        try:
            mtime: float | None = sp.stat().st_mtime
        except OSError:
            mtime = None
        prods: dict[str, str] = {}
        for rel in spec["products"]:
            h = sha256_file(root / rel)
            if h is not None:
                prods[rel] = h
        out[name] = {
            "src": spec["src"],
            "src_sha256": sha256_file(sp),
            "src_ast_sha256": semantic_hash(sp),
            "src_mtime": mtime,
            "products": prods,
            "declared_products": list(spec["products"]),
        }
    return out


def load_baseline(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def build_baseline(root: Path) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "generated_by": "tools/guard_rerun_670c.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": ("基线 = 一次「源码指纹 + 产物指纹」快照。判据：源码语义变了而产物没变 ⇒ STALE。"
                 "刷新基线请在**确认产物已重跑**之后执行 --update。"),
        "tools": probe(root),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 对账
# ─────────────────────────────────────────────────────────────────────────────

def _src_changed(base_t: dict[str, Any], cur_t: dict[str, Any]) -> tuple[bool | None, str]:
    """返回（是否变, 用的指纹种类）。指纹缺一侧 ⇒ None（无法判定）。"""
    b_ast, c_ast = base_t.get("src_ast_sha256"), cur_t.get("src_ast_sha256")
    if b_ast and c_ast:
        return (b_ast != c_ast), "ast"
    b_raw, c_raw = base_t.get("src_sha256"), cur_t.get("src_sha256")
    if b_raw and c_raw:
        return (b_raw != c_raw), "sha256"
    return None, "none"


def compare(base: dict[str, Any], cur: dict[str, Any]) -> list[dict[str, Any]]:
    """逐工具对账。返回 verdict 列表（不抛异常）。"""
    bt = base.get("tools")
    base_tools: dict[str, Any] = bt if isinstance(bt, dict) else {}
    verdicts: list[dict[str, Any]] = []
    for name, c in sorted(cur.items()):
        b = base_tools.get(name)
        rec: dict[str, Any] = {"tool": name, "src": c["src"], "products": [], "notes": []}

        if not isinstance(b, dict):
            rec.update(status=NO_BASELINE_ENTRY, severity=WARN, src_changed=None, fingerprint="none",
                       message="基线里没有该工具的记录（新注册/基线过旧）⇒ 只记录，不判红")
            rec["notes"].append("请 --update 重新标定后再纳入判红范围")
            verdicts.append(rec)
            continue

        changed, kind = _src_changed(b, c)
        if c["src_sha256"] is None:
            rec.update(status=SRC_MISSING, severity=WARN, src_changed=None, fingerprint=kind,
                       message="源码文件不存在/不可读 ⇒ 无法判定（登记为未进射程）")
            verdicts.append(rec)
            continue
        if changed is None:
            rec.update(status=SRC_MISSING, severity=WARN, src_changed=None, fingerprint=kind,
                       message="源码指纹缺一侧（基线未记 ast/sha）⇒ 无法判定，请 --update 重新标定")
            verdicts.append(rec)
            continue

        prod_changed: list[str] = []
        prod_missing: list[str] = []
        prod_new: list[str] = []
        bp = b.get("products")
        b_prods: dict[str, Any] = bp if isinstance(bp, dict) else {}
        for rel in c["declared_products"]:
            cur_h = c["products"].get(rel)
            old_h = b_prods.get(rel)
            if cur_h is None:
                prod_missing.append(rel)
            elif old_h is None:
                prod_new.append(rel)
            elif old_h != cur_h:
                prod_changed.append(rel)
            rec["products"].append({
                "path": rel, "baseline_sha256": old_h, "current_sha256": cur_h,
                "changed": bool(old_h and cur_h and old_h != cur_h),
                "missing": cur_h is None,
            })

        rec["src_changed"] = changed
        rec["fingerprint"] = kind
        rec["products_changed"] = sorted(prod_changed + prod_new)
        rec["products_missing"] = sorted(prod_missing)

        if not c["declared_products"]:
            rec.update(status=NO_PRODUCT, severity=WARN,
                       message="该工具无落盘产物（纯只读库）⇒ 本门禁对它无射程（射程自检，不假装覆盖）")
        elif not changed:
            rec.update(status=RERUN_ONLY if (prod_changed or prod_new) else OK,
                       severity=PASS,
                       message=("源码未变、产物已变 ⇒ 只是重跑过（若并未重跑，说明产物非确定性，值得复核）"
                                if (prod_changed or prod_new) else "源码与产物均未变"))
        elif prod_changed or prod_new:
            rec.update(status=RERUN, severity=PASS,
                       message=f"源码语义已变且产物已刷新（{len(prod_changed + prod_new)} 个）⇒ 改了也重跑了")
        elif prod_missing:
            rec.update(status=PRODUCT_MISSING, severity=WARN,
                       message=f"源码已变，但产物缺失（{', '.join(prod_missing)}）⇒ 无法判定，请重跑并 --update")
        else:
            rec.update(status=STALE, severity=BLOCK,
                       message="源码语义已变，但产物哈希与基线一致 ⇒ 改了代码没重跑产物（假绿风险）")

        if prod_missing:
            rec["notes"].append("缺失产物：" + ", ".join(prod_missing))
        if rec.get("severity") == BLOCK:
            rec["notes"].append("处置：重跑该工具的落盘命令**之后**再 --update 刷新基线（不得只 --update 了事）")
        verdicts.append(rec)
    return verdicts


def evaluate(root: Path = ROOT, baseline_path: Path | None = None) -> dict[str, Any]:
    """完整评估（只读）。返回机读 dict，供主门禁与 CLI 共用。"""
    bp = baseline_path if baseline_path is not None else (root / DEFAULT_BASELINE)
    base = load_baseline(bp)
    cur = probe(root)
    if base is None:
        return {
            "schema": SCHEMA, "tool": "guard_rerun_670c",
            "baseline": str(bp), "baseline_found": False,
            "overall": "UNARMED", "armed": False,
            "counts": {"stale": 0, "rerun": 0, "warn": 0, "tools": len(cur)},
            "verdicts": [],
            "message": (f"未找到基线 {bp} ⇒ 本门禁**未进射程**（无法证明任何产物是新的）。"
                        "先跑一次真实门禁，再 --update 标定。"),
        }
    verdicts = compare(base, cur)
    stale = [v for v in verdicts if v["severity"] == BLOCK]
    warns = [v for v in verdicts if v["severity"] == WARN]
    reruns = [v for v in verdicts if v["status"] in (RERUN, RERUN_ONLY)]
    return {
        "schema": SCHEMA, "tool": "guard_rerun_670c",
        "baseline": str(bp), "baseline_found": True,
        "baseline_generated_at": base.get("generated_at"),
        "overall": "RED" if stale else "PASS",
        "armed": True,
        "counts": {"stale": len(stale), "rerun": len(reruns), "warn": len(warns),
                   "tools": len(verdicts)},
        "verdicts": verdicts,
        "message": ("发现改了代码没重跑产物" if stale else "核心工具源码/产物对账一致"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def render(res: dict[str, Any]) -> str:
    L = [f"[guard-rerun] overall={res['overall']}  tools={res['counts']['tools']}  "
         f"stale={res['counts']['stale']}  rerun={res['counts']['rerun']}  warn={res['counts']['warn']}",
         f"  基线：{res['baseline']}" + ("" if res["baseline_found"] else "（缺失）")]
    for v in res["verdicts"]:
        L.append(f"  [{v['status']:16}] {v['tool']:22} src_changed={v.get('src_changed')} "
                 f"({v.get('fingerprint', '-')})")
        L.append(f"      {v['message']}")
    if not res["baseline_found"]:
        L.append(f"  [!] {res['message']}")
    return "\n".join(L)


def selftest() -> int:
    """只读自检：哈希稳定性 + 注册表与真实文件对得上。"""
    ok = True
    me = Path(__file__).resolve()

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("裸 sha256 两次一致", sha256_file(me) == sha256_file(me))
    chk("语义哈希两次一致", semantic_hash(me) == semantic_hash(me))
    chk("缺失文件不抛异常",
        sha256_file(ROOT / "__no_such_file__.py") is None
        and semantic_hash(ROOT / "__no_such_file__.py") is None)
    chk("注册表非空且每项有 src", bool(CORE_TOOLS) and all(v.get("src") for v in CORE_TOOLS.values()))
    chk("每个核心工具在本仓存在源码", all((ROOT / str(v["src"])).is_file() for v in CORE_TOOLS.values()))
    print(f"guard_rerun_670c selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="670c D2：核心工具「改了代码没重跑产物」守卫")
    ap.add_argument("--root", default=None, help="仓库根（默认本文件上级目录；测试用）")
    ap.add_argument("--baseline", default=None, help=f"基线路径（默认 {DEFAULT_BASELINE}）")
    ap.add_argument("--update", action="store_true", help="把当前指纹写为基线（唯一写盘操作）")
    ap.add_argument("--json", action="store_true", help="机读 JSON 输出")
    ap.add_argument("--selftest", action="store_true", help="只读自检")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve() if a.root else ROOT
    bp = Path(a.baseline) if a.baseline else (root / DEFAULT_BASELINE)

    if a.selftest:
        return selftest()

    if a.update:
        base = build_baseline(root)
        bp.parent.mkdir(parents=True, exist_ok=True)
        bp.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        msg = {"schema": SCHEMA, "updated": True, "baseline": str(bp),
               "tools": sorted(base["tools"])}
        print(json.dumps(msg, ensure_ascii=False, indent=2) if a.json
              else f"[guard-rerun] 基线已写入 {bp}（{len(base['tools'])} 个工具）")
        return 0

    res = evaluate(root, bp)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    if not res["baseline_found"]:
        return 2                      # 未进射程 ≠ 通过
    return 1 if res["overall"] == "RED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
