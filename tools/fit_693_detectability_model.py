#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""fit_693_detectability_model.py — 693-E3：可检测性预测模型（**只读，0 次 detect**）。

任务书要求
==========
特征：缺陷类型 / 代码行数 / 复杂度 / 是否内存安全 / 是否并发；
目标：catch / miss / unknown；
模型：简单模型（决策树 / 逻辑回归），**不用深度学习**。

本实现
======
* **纯标准库**（本机无 numpy / scikit-learn —— 已实测：`import numpy` 失败）。
  自写 CART 决策树（Gini）与 L2 逻辑回归（全批量梯度下降）。
* 特征从 **源文件** 现算（行数 / 分支数 / 循环数 / 调用数 / 指针运算数 / 最大嵌套深度
  / 内存操作数）+ 缺陷家族 one-hot + `planted` + 批次 one-hot。
* 目标：样本级二分类 `catch` vs `miss`（用冻结矩阵的 `or_verdict_available6`）。
  `unknown` 在样本级不出现（两个恒 unknown 的资产已被 676g 折进 miss 口径），
  因此**不做三分类**——这一点在报告里显式声明，避免"少了 unknown 类"被误读成遗漏。

⭐ 关键设计：**防泄漏的分组交叉验证**
=====================================
本项目已知「批内模板克隆率 62.2%」（676k），即大量样本是同一模板的参数变体。
若直接随机 5 折，同一模板的变体会同时出现在训练与测试集 ⇒ **准确率被系统性高估**。
本脚本因此报**两个** CV 结果：

* `random_5fold`  —— 常规随机折（会泄漏）；
* `group_5fold`   —— **按结构签名分组**的折（同签名必同折，无泄漏）。

两者的差距 = **泄漏导致的高估幅度**，这本身就是本批的一个发现。

用法
====
    python tools/fit_693_detectability_model.py
    python tools/fit_693_detectability_model.py --folds 5 --tree-depth 4
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("fit_693_detectability_model")
MATRIX = "blindspot_676g_detection_matrix.json"
EXP_ROOT = ROOT / "data" / "holdout_expansion"
OUT_JSON = ROOT / "data" / "693_detectability_model.json"
OUT_MD = ROOT / "data" / "693_detectability_model_report.md"

FAMILY_OF: dict[str, str] = {
    "memory_safety": "memory", "use_after_free": "memory", "double_free": "memory",
    "memory_leak": "memory", "smart_pointer": "memory", "raii_violation": "memory",
    "move_semantics": "memory", "uninitialized_read": "memory",
    "out_of_bounds": "bounds", "null_pointer_deref": "bounds",
    "integer_overflow": "integer", "bit_operation": "integer",
    "type_punning": "alias_type", "strict_aliasing": "alias_type",
    "alignment": "alias_type", "endianness": "alias_type", "linker_odr": "alias_type",
    "data_race": "concurrency", "atomic_ub": "concurrency",
    "memory_order": "concurrency", "deadlock": "concurrency",
    "condition_variable": "concurrency",
    "iterator_invalidation": "stl", "stl_container_ub": "stl",
    "string_ub": "stl", "algorithm_misuse": "stl",
    "virtual_function": "language_oop", "lambda_capture": "language_oop",
    "cross_tu_ub": "language_oop", "logic_error": "language_oop", "other_ub": "language_oop",
    "volatile_misuse": "embedded", "register_ub": "embedded", "interrupt_safety": "embedded",
}
FAMILIES = ("memory", "bounds", "integer", "alias_type", "concurrency",
            "stl", "language_oop", "embedded")

_BRANCH = re.compile(r"\b(if|else|case|catch)\b")
_LOOP = re.compile(r"\b(for|while|do)\b")
_CALL = re.compile(r"\b[A-Za-z_]\w*\s*\(")
_PTR = re.compile(r"[*&]|->|\bnew\b|\bdelete\b|\[\s*\]")
_MEM = re.compile(r"\b(new|delete|malloc|calloc|realloc|free)\b")
_THREAD = re.compile(r"\b(thread|mutex|atomic|lock_guard|unique_lock|condition_variable)\b")
_IDENT = re.compile(r"\b[A-Za-z_]\w*\b")
_NUM = re.compile(r"\b\d+\b")


def _source_path(uid: str, files: list[str]) -> Path | None:
    """把 uid 映射到源文件路径（只覆盖 expA–expG；其余返回 None）。"""
    if ":" not in uid:
        return None
    batch, sid = uid.split(":", 1)
    if not batch.startswith("exp"):
        return None
    cand = EXP_ROOT / batch / f"{sid}.cpp"
    if cand.exists():
        return cand
    if files:
        c2 = EXP_ROOT / batch / files[0]
        if c2.exists():
            return c2
    return None


def _features(code: str) -> dict[str, float]:
    """从源码算结构特征（全部确定性，无模型）。"""
    lines = code.split("\n")
    nonblank = [ln for ln in lines if ln.strip()]
    depth = 0
    max_depth = 0
    for ln in nonblank:
        depth += ln.count("{") - ln.count("}")
        max_depth = max(max_depth, depth)
    n_lines = len(nonblank)
    return {
        "n_lines": float(n_lines),
        "n_branch": float(len(_BRANCH.findall(code))),
        "n_loop": float(len(_LOOP.findall(code))),
        "n_call": float(len(_CALL.findall(code))),
        "n_ptr": float(len(_PTR.findall(code))),
        "n_mem": float(len(_MEM.findall(code))),
        "n_thread": float(len(_THREAD.findall(code))),
        "max_depth": float(max_depth),
        "branch_density": round(len(_BRANCH.findall(code)) / max(1, n_lines), 3),
        "chars_per_line": round(len(code) / max(1, n_lines), 1),
    }


def _signature(code: str) -> str:
    """结构签名：标识符与字面量中性化后的 token 串哈希（用于分组，防泄漏）。"""
    norm = _NUM.sub("N", _IDENT.sub("I", code))
    norm = re.sub(r"\s+", " ", norm).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


def _build_dataset(samples: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """构造数据集；只保留能定位到源文件的样本。"""
    rows: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    for s in samples:
        uid = str(s["uid"])
        p = _source_path(uid, list(s.get("files") or []))
        if p is None:
            skipped[str(s["source_batch"])] += 1
            continue
        try:
            code = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            skipped[str(s["source_batch"])] += 1
            continue
        y = 1 if str(s.get("or_verdict_available6")) == "catch" else 0
        feat = _features(code)
        dt = str(s.get("defect_type"))
        fam = FAMILY_OF.get(dt, "language_oop")
        row: dict[str, Any] = {
            "uid": uid, "y": y, "group": _signature(code),
            "defect_type": dt, "family": fam,
            "planted": 1 if s.get("planted") is True else 0,
            "source_batch": str(s.get("source_batch")),
            **feat,
        }
        for f in FAMILIES:
            row[f"fam_{f}"] = 1.0 if fam == f else 0.0
        row["is_memory_safe"] = 1.0 if fam in ("memory", "bounds") else 0.0
        row["is_concurrency"] = 1.0 if fam == "concurrency" else 0.0
        rows.append(row)
    return rows, dict(skipped)


NUMERIC = ("n_lines", "n_branch", "n_loop", "n_call", "n_ptr", "n_mem", "n_thread",
           "max_depth", "branch_density", "chars_per_line", "planted",
           "is_memory_safe", "is_concurrency") + tuple(f"fam_{f}" for f in FAMILIES)


# ─────────────────────────── CART 决策树（纯标准库） ───────────────────────────
class Tree:
    """极简 CART：Gini 不纯度 + 二分阈值切分 + 深度上限。"""

    def __init__(self, max_depth: int = 4, min_leaf: int = 12) -> None:
        self.max_depth = max_depth
        self.min_leaf = min_leaf
        self.root: dict[str, Any] | None = None
        self.used_features: Counter[str] = Counter()

    def fit(self, X: list[list[float]], y: list[int],
            names: list[str]) -> Tree:
        self.names = names
        self.root = self._grow(X, y, 0)
        return self

    def _grow(self, X: list[list[float]], y: list[int], depth: int) -> dict[str, Any]:
        n = len(y)
        pos = sum(y)
        node: dict[str, Any] = {"n": n, "pos": pos,
                                "p": (pos / n) if n else 0.0}
        if depth >= self.max_depth or n < 2 * self.min_leaf or pos in (0, n):
            node["leaf"] = True
            return node
        base = self._gini(pos, n)
        best: tuple[float, int, float] | None = None
        for j in range(len(self.names)):
            vals = sorted({X[i][j] for i in range(n)})
            if len(vals) < 2:
                continue
            # 用分位点做候选阈值（避免 O(n^2)）
            step = max(1, len(vals) // 12)
            for k in range(0, len(vals) - 1, step):
                thr = (vals[k] + vals[k + 1]) / 2.0
                lpos = ltot = rpos = rtot = 0
                for i in range(n):
                    if X[i][j] <= thr:
                        ltot += 1
                        lpos += y[i]
                    else:
                        rtot += 1
                        rpos += y[i]
                if ltot < self.min_leaf or rtot < self.min_leaf:
                    continue
                g = (ltot / n) * self._gini(lpos, ltot) + (rtot / n) * self._gini(rpos, rtot)
                if best is None or g < best[0]:
                    best = (g, j, thr)
        if best is None or best[0] >= base - 1e-9:
            node["leaf"] = True
            return node
        _g, j, thr = best
        self.used_features[self.names[j]] += 1
        left = [i for i in range(n) if X[i][j] <= thr]
        right = [i for i in range(n) if X[i][j] > thr]
        node.update({"leaf": False, "feature": self.names[j], "threshold": round(thr, 4),
                     "gain": round(base - _g, 5)})
        node["left"] = self._grow([X[i] for i in left], [y[i] for i in left], depth + 1)
        node["right"] = self._grow([X[i] for i in right], [y[i] for i in right], depth + 1)
        return node

    @staticmethod
    def _gini(pos: int, n: int) -> float:
        if n == 0:
            return 0.0
        p = pos / n
        return 2 * p * (1 - p)

    def predict_proba(self, x: list[float]) -> float:
        node = self.root
        while node and not node.get("leaf"):
            node = node["left"] if x[self.names.index(node["feature"])] <= node["threshold"] \
                else node["right"]
        return float(node["p"]) if node else 0.0

    def predict(self, x: list[float]) -> int:
        return 1 if self.predict_proba(x) >= 0.5 else 0

    def rules(self) -> list[str]:
        """把树展开成可读规则（只取前 20 条叶路径）。"""
        out: list[str] = []

        def walk(node: dict[str, Any], cond: list[str]) -> None:
            if len(out) >= 20:
                return
            if node.get("leaf"):
                out.append(f"IF {' AND '.join(cond) if cond else 'TRUE'} "
                           f"THEN p(catch)={node['p']:.2f} (n={node['n']})")
                return
            f, t = node["feature"], node["threshold"]
            walk(node["left"], [*cond, f"{f} <= {t}"])
            walk(node["right"], [*cond, f"{f} > {t}"])

        if self.root:
            walk(self.root, [])
        return out


# ─────────────────────────── L2 逻辑回归（纯标准库） ───────────────────────────
class LogReg:
    """全批量梯度下降 + L2；特征做 z-score 标准化。"""

    def __init__(self, epochs: int = 400, lr: float = 0.5, l2: float = 1e-3) -> None:
        self.epochs, self.lr, self.l2 = epochs, lr, l2
        self.w: list[float] = []
        self.mu: list[float] = []
        self.sd: list[float] = []

    def fit(self, X: list[list[float]], y: list[int]) -> LogReg:
        d = len(X[0])
        n = len(X)
        self.mu = [sum(X[i][j] for i in range(n)) / n for j in range(d)]
        self.sd = []
        for j in range(d):
            var = sum((X[i][j] - self.mu[j]) ** 2 for i in range(n)) / n
            self.sd.append(math.sqrt(var) if var > 1e-12 else 1.0)
        Z = [self._scale(x) for x in X]
        self.w = [0.0] * d
        for _ in range(self.epochs):
            g = [0.0] * d
            for i in range(n):
                p = self._sigmoid(sum(self.w[j] * Z[i][j] for j in range(d)))
                e = p - y[i]
                for j in range(d):
                    g[j] += e * Z[i][j]
            for j in range(d):
                self.w[j] -= self.lr * (g[j] / n + self.l2 * self.w[j])
        return self

    def _scale(self, x: list[float]) -> list[float]:
        return [(x[j] - self.mu[j]) / self.sd[j] for j in range(len(x))]

    @staticmethod
    def _sigmoid(z: float) -> float:
        if z < -35:
            return 0.0
        if z > 35:
            return 1.0
        return 1.0 / (1.0 + math.exp(-z))

    def predict_proba(self, x: list[float]) -> float:
        z = self._scale(x)
        return self._sigmoid(sum(self.w[j] * z[j] for j in range(len(z))))

    def predict(self, x: list[float]) -> int:
        return 1 if self.predict_proba(x) >= 0.5 else 0

    def coefficients(self, names: list[str]) -> list[dict[str, Any]]:
        return sorted(({"feature": names[j], "coef": round(self.w[j], 4)}
                       for j in range(len(self.w))),
                      key=lambda d: -abs(d["coef"]))


def _auc(y: list[int], p: list[float]) -> float | None:
    """AUC（Mann-Whitney U 形式，含并列处理）。"""
    pos = [p[i] for i in range(len(y)) if y[i] == 1]
    neg = [p[i] for i in range(len(y)) if y[i] == 0]
    if not pos or not neg:
        return None
    # 排名法（并列取平均秩）
    order = sorted(range(len(p)), key=lambda i: p[i])
    ranks = [0.0] * len(p)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and p[order[j + 1]] == p[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    rsum = sum(ranks[i] for i in range(len(y)) if y[i] == 1)
    return round((rsum - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)), 4)


def _metrics(y: list[int], pred: list[int], prob: list[float]) -> dict[str, Any]:
    tp = sum(1 for a, b in zip(y, pred) if a == 1 and b == 1)
    fn = sum(1 for a, b in zip(y, pred) if a == 1 and b == 0)
    fp = sum(1 for a, b in zip(y, pred) if a == 0 and b == 1)
    tn = sum(1 for a, b in zip(y, pred) if a == 0 and b == 0)
    n = len(y)
    return {
        "n": n, "TP": tp, "FN": fn, "FP": fp, "TN": tn,
        "accuracy": round((tp + tn) / n, 4) if n else None,
        "recall": round(tp / (tp + fn), 4) if (tp + fn) else None,
        "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
        "auc": _auc(y, prob),
        "majority_baseline": round(max(sum(y), n - sum(y)) / n, 4) if n else None,
    }


def _folds(rows: list[dict[str, Any]], k: int, seed: int, grouped: bool) -> list[list[int]]:
    """构造 k 折索引；grouped=True 时同一 group 必同折。"""
    rng = random.Random(seed)
    if not grouped:
        idx = list(range(len(rows)))
        rng.shuffle(idx)
        return [idx[i::k] for i in range(k)]
    groups: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        groups[str(r["group"])].append(i)
    keys = sorted(groups)
    rng.shuffle(keys)
    out: list[list[int]] = [[] for _ in range(k)]
    for pos, g in enumerate(keys):
        out[pos % k].extend(groups[g])
    return out


def _cv(rows: list[dict[str, Any]], k: int, seed: int, grouped: bool,
        depth: int) -> dict[str, Any]:
    folds = _folds(rows, k, seed, grouped)
    names = list(NUMERIC)
    res: dict[str, Any] = {"tree": {"y": [], "pred": [], "prob": []},
                           "logreg": {"y": [], "pred": [], "prob": []},
                           "n_groups": len({str(r["group"]) for r in rows})}
    for f in range(k):
        test = folds[f]
        train = [i for g in range(k) if g != f for i in folds[g]]
        if not test or not train:
            continue
        Xtr = [[float(rows[i][nm]) for nm in names] for i in train]
        ytr = [int(rows[i]["y"]) for i in train]
        Xte = [[float(rows[i][nm]) for nm in names] for i in test]
        yte = [int(rows[i]["y"]) for i in test]
        t = Tree(max_depth=depth).fit(Xtr, ytr, names)
        lr = LogReg().fit(Xtr, ytr)
        for model, key in ((t, "tree"), (lr, "logreg")):
            for x, yv in zip(Xte, yte):
                res[key]["y"].append(yv)
                res[key]["prob"].append(model.predict_proba(x))
                res[key]["pred"].append(model.predict(x))
    out: dict[str, Any] = {"n_groups": res["n_groups"], "models": {}}
    for key in ("tree", "logreg"):
        out["models"][key] = _metrics(res[key]["y"], res[key]["pred"], res[key]["prob"])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--tree-depth", type=int, default=4)
    ap.add_argument("--seed", type=int, default=693)
    args = ap.parse_args()

    mat = load_json_cached(DATA / MATRIX)
    rows, skipped = _build_dataset(mat["samples"])
    _log.info("数据集：%d 样本（跳过 %s）", len(rows), skipped)

    base_rate = sum(r["y"] for r in rows) / len(rows)
    random_cv = _cv(rows, args.folds, args.seed, grouped=False, depth=args.tree_depth)
    group_cv = _cv(rows, args.folds, args.seed, grouped=True, depth=args.tree_depth)

    names = list(NUMERIC)
    full_tree = Tree(max_depth=args.tree_depth).fit(
        [[float(r[nm]) for nm in names] for r in rows], [int(r["y"]) for r in rows], names)
    full_lr = LogReg().fit(
        [[float(r[nm]) for nm in names] for r in rows], [int(r["y"]) for r in rows])

    gap = {
        m: {
            "accuracy_gap": round(
                (random_cv["models"][m]["accuracy"] or 0)
                - (group_cv["models"][m]["accuracy"] or 0), 4),
            "auc_gap": round((random_cv["models"][m]["auc"] or 0)
                             - (group_cv["models"][m]["auc"] or 0), 4),
        }
        for m in ("tree", "logreg")
    }

    doc: dict[str, Any] = {
        "schema": "queyi-693-detectability-model/v1",
        "generated_by": "tools/fit_693_detectability_model.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "target": "样本级 or_verdict_available6 == catch（二分类）",
        "target_note": ("样本级**不出现** unknown（两个恒 unknown 资产已由 676g 折进 miss 口径）"
                        "⇒ 因此不做三分类；这不是遗漏，是冻结矩阵的口径。"),
        "n_samples_used": len(rows),
        "n_samples_skipped": skipped,
        "base_rate_catch": round(base_rate, 4),
        "features": list(NUMERIC),
        "n_feature_groups": group_cv["n_groups"],
        "cv": {
            "folds": args.folds, "seed": args.seed,
            "random_5fold": random_cv,
            "group_5fold": group_cv,
            "leakage_inflation": gap,
        },
        "full_fit": {
            "tree_rules": full_tree.rules(),
            "tree_used_features": dict(full_tree.used_features.most_common()),
            "logreg_top_coefficients": full_lr.coefficients(names)[:15],
        },
        "honest_limits": [
            "样本主体为合成/半合成（92.9% 人工植入）⇒ 模型学的是**仪器**不是真实缺陷分布。",
            "批内模板克隆率 62.2% ⇒ 随机折会泄漏；group_5fold 是更可信的读数。",
            "特征只覆盖 expA–expG（能定位到源文件的样本）；holdout/corpus 未纳入。",
            "决策树深度与最小叶大小未做调参搜索（避免在 1147 条上过拟合）。",
            "目标用 or_verdict_available6；换成 expected_verdict 会得到不同（且更乐观）的结果。",
        ],
    }

    Path(OUT_JSON).write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
    Path(OUT_MD).write_text(_md(doc), encoding="utf-8", newline="\n")
    _log.info("完成：n=%d，随机折 acc=%.3f / 分组折 acc=%.3f（树）",
              len(rows), random_cv["models"]["tree"]["accuracy"] or 0,
              group_cv["models"]["tree"]["accuracy"] or 0)
    print(f"[693-E3] -> {OUT_JSON}")


def _md(doc: dict[str, Any]) -> str:
    r = doc["cv"]["random_5fold"]["models"]
    g = doc["cv"]["group_5fold"]["models"]
    lines = [
        "# 693-E3 · 可检测性预测模型报告",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：`tools/fit_693_detectability_model.py`",
        f"- **`detect_calls` = {doc['detect_calls']}**（只读冻结矩阵 + 源文件，符合红线 8）",
        f"- 目标：{doc['target']}",
        f"- 样本：**{doc['n_samples_used']}**（跳过 {doc['n_samples_skipped']}）；"
        f"正类基率 **{doc['base_rate_catch']:.3f}**",
        f"- 特征 {len(doc['features'])} 维；结构签名分组数 **{doc['n_feature_groups']}**",
        "- 实现：**纯标准库**自写 CART（Gini）+ L2 逻辑回归（本机无 numpy/sklearn）",
        "",
        "## 1. 交叉验证结果（两种折法并列）",
        "",
        "| 模型 | 折法 | n | accuracy | AUC | recall | precision | 多数类基线 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key, label in (("tree", "CART 决策树"), ("logreg", "L2 逻辑回归")):
        for cvname, block in (("random", r), ("group", g)):
            m = block[key]
            lines.append(
                f"| {label} | {cvname}_5fold | {m['n']} | **{m['accuracy']}** | {m['auc']} | "
                f"{m['recall']} | {m['precision']} | {m['majority_baseline']} |")
    gap = doc["cv"]["leakage_inflation"]
    lines += [
        "",
        "### 1.1 ⭐ 泄漏导致的高估（本报告最重要的数字）",
        "",
        "| 模型 | accuracy 高估 | AUC 高估 |",
        "|---|---:|---:|",
        f"| CART 决策树 | **{gap['tree']['accuracy_gap']:+.4f}** | {gap['tree']['auc_gap']:+.4f} |",
        f"| L2 逻辑回归 | **{gap['logreg']['accuracy_gap']:+.4f}** | {gap['logreg']['auc_gap']:+.4f} |",
        "",
        "> 本项目的批内模板克隆率是 **62.2%**（676k）。随机 5 折会把同一模板的参数变体",
        "> 同时放进训练与测试 ⇒ 准确率被高估。上表的差值就是**高估幅度**。",
        "> 任何「我们的模型能预测可检测性」的说法，都必须用 `group_5fold` 的读数。",
        "",
        "## 2. 决策树规则（全量拟合，深度上限 "
        f"{doc['cv']['folds']}→{len(doc['full_fit']['tree_rules'])} 条路径）",
        "",
        "```",
    ]
    lines += doc["full_fit"]["tree_rules"] or ["（未产生分裂）"]
    lines += [
        "```",
        "",
        "## 3. 逻辑回归系数（|coef| 前 15，标准化后）",
        "",
        "| 特征 | 系数 |",
        "|---|---:|",
    ]
    for c in doc["full_fit"]["logreg_top_coefficients"]:
        lines.append(f"| `{c['feature']}` | {c['coef']:+.4f} |")
    lines += [
        "",
        "## 4. 诚实边界",
        "",
    ]
    lines += [f"- {x}" for x in doc["honest_limits"]]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
