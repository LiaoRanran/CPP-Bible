#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""train_697_predictor.py — 697-C：能力边界预测模型（**只读，0 次 detect**）。

与 693-E3 的关系（必须先说清，否则是重复劳动）
==============================================
693-E3 已经做过「可检测性预测器」（CART + L2 LR，group_5fold AUC 0.781）。本批的**净增量**是：

1. **家族感知的折法换成真正的克隆家族**：693 用的是 1042 条样本的**结构签名**（559 组）；
   本批改用 677b 的**凝聚家族**（474 族，阈值 0.85，全对凝聚）——这是论文里
   「批内克隆率 62.2%」的**同一个**家族定义，分组口径与论文一致。
2. **样本量从 1042 扩到 1147**：693 因拿不到源文件跳过了 holdout/corpus 共 105 条。
   本批分**两层特征**：Tier A（全 1147 条，仅清单特征）/ Tier B（1042 条，加源码特征），
   从而量化「源码特征到底买来了多少 AUC」。
3. **加了随机森林式的装袋 CART**（本机无 numpy/sklearn，故为纯标准库实现）。
4. **理论上限**（695-P3 要的东西，693 完全没有）：
   - **Rice 定理层面的不可判定性**；
   - **族内判定不一致率** ⇒ 一个**可计算的 Bayes 误差下界**（同族样本特征近乎相同
     却拿到不同裁决 ⇒ 任何基于特征的模型都无法把它们分开）；
   - **族迁移天花板**：只用 defect_group 均值做 leave-one-family-out 预测 ⇒
     「泛化到一个全新家族」时的可达 AUC。
5. **主动学习 Top-20**（不确定性采样 + 家族去重）。

用法
====
    python tools/train_697_predictor.py
    python tools/train_697_predictor.py --folds 5 --bags 30
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
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fit_693_detectability_model import _features, _source_path  # noqa: E402
from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("train_697_predictor")

MATRIX: Final[str] = "blindspot_676g_detection_matrix.json"
A5: Final[str] = "a5_676f_detection_matrix.json"
FAMILIES: Final[str] = "677b_clone_families.json"
OUT_JSON: Final[Path] = ROOT / "data" / "697_capability_boundary_model.json"

# 8 个声明资产；其中 wunsequenced / compile-time 结构性恒 unknown ⇒ OR 等价于 6 资产
ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)

FAMILY_OF: Final[dict[str, str]] = {
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
FAMILY_NAMES: Final[tuple[str, ...]] = (
    "memory", "bounds", "integer", "alias_type", "concurrency",
    "stl", "language_oop", "embedded",
)

# 注：`_src_features` / `_src_path` 复用 693-D3 的确定性源码特征提取器（见顶部 import），
# 目的是避免仓库里出现两套源码特征口径。


# ══════════════════════════════════════════════════════════════════════════
# 数据集
# ══════════════════════════════════════════════════════════════════════════
def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def build_family_index() -> dict[str, str]:
    """677b 的 474 个凝聚家族 → ``{样本标识: family_id}``。

    677b 的成员 id 是 A5 的 ``sample_id``（如 ``A001``）；676g 用的是 ``orig_id``
    （如 ``sample_001``）。两个键都注册，确保 1147 条样本尽量都能落到家族。
    """
    fam_doc = load_json_cached(DATA / FAMILIES)
    a5_doc = load_json_cached(DATA / A5)
    sid2orig: dict[str, str] = {}
    for s in a5_doc.get("samples", []):
        sid2orig[str(s.get("sample_id"))] = str(s.get("orig_id") or s.get("sample_id"))
    idx: dict[str, str] = {}
    for fam in fam_doc.get("families", []):
        fid = str(fam.get("family_id"))
        for m in fam.get("members", []):
            idx[str(m)] = fid
            if str(m) in sid2orig:
                idx[sid2orig[str(m)]] = fid
    return idx


def build_dataset() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    doc = load_json_cached(DATA / MATRIX)
    fam_idx = build_family_index()
    batches: Counter[str] = Counter()

    rows: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        uid = str(s.get("uid") or "")
        sid = str(s.get("sample_id") or "")
        batch = str(s.get("source_batch") or "unknown")
        batches[batch] += 1
        pa = s.get("per_asset") or {}
        caught = [a for a in ASSETS if _verdict(pa.get(a, "unknown")) == "catch"]
        y = 1 if caught else 0
        dt = str(s.get("defect_type") or "unknown")
        fam = FAMILY_OF.get(dt, "language_oop")
        row: dict[str, Any] = {
            "uid": uid,
            "sample_id": sid,
            "source_batch": batch,
            "defect_type": dt,
            "family": fam,
            "y": y,
            "n_caught": len(caught),
            "planted": 1.0 if s.get("planted") is True else 0.0,
            "hung": 1.0 if s.get("hung_flag") is True else 0.0,
            "clone_family": fam_idx.get(sid) or fam_idx.get(uid.split(":", 1)[-1]) or f"singleton::{uid}",
            "has_source": False,
        }
        for f in FAMILY_NAMES:
            row[f"fam_{f}"] = 1.0 if fam == f else 0.0
        row["is_memory_safe"] = 1.0 if fam in ("memory", "bounds") else 0.0
        row["is_concurrency"] = 1.0 if fam == "concurrency" else 0.0
        for b in sorted(batches):
            row[f"batch_{b}"] = 0.0
        row[f"batch_{batch}"] = 1.0

        p = _source_path(uid, list(s.get("files") or []))
        if p is not None:
            try:
                code = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                code = ""
            if code:
                row.update(_features(code))
                row["has_source"] = True
                row["signature"] = _signature(code)
        rows.append(row)

    # batch one-hot 需要知道全部批次 ⇒ 回填
    all_batches = sorted({r["source_batch"] for r in rows})
    for r in rows:
        for b in all_batches:
            r.setdefault(f"batch_{b}", 0.0)
        r[f"batch_{r['source_batch']}"] = 1.0

    meta = {
        "n_total": len(rows),
        "n_with_source": sum(1 for r in rows if r["has_source"]),
        "n_missing_source_by_batch": dict(
            Counter(r["source_batch"] for r in rows if not r["has_source"])
        ),
        "base_rate_catch": round(sum(r["y"] for r in rows) / len(rows), 6),
        "n_clone_families": len({r["clone_family"] for r in rows}),
        "n_families_from_677b": len({r["clone_family"] for r in rows
                                     if not r["clone_family"].startswith("singleton::")}),
        "n_structural_signatures": len({r.get("signature") for r in rows if r.get("signature")}),
    }
    return rows, meta


def _signature(code: str) -> str:
    """结构签名：标识符与字面量中性化后的 token 串哈希（与 693-D3 同口径）。"""
    norm = re.sub(r"\s+", " ", re.sub(r"\b\d+\b", "N", re.sub(r"\b[A-Za-z_]\w*\b", "I", code))).strip()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


# ⚠ 不含 ``hung``：实测 35 条 hung 样本**全部**是 miss（挂起→超时→判 miss），
# 它是**测量运行结果**而非样本的事前属性，放进特征等于直接泄漏目标（见 honest_limits）。
TIER_A: Final[tuple[str, ...]] = (
    tuple(f"fam_{f}" for f in FAMILY_NAMES)
    + ("planted", "is_memory_safe", "is_concurrency")
)
TIER_B_SRC: Final[tuple[str, ...]] = (
    "n_lines", "n_branch", "n_loop", "n_call", "n_ptr", "n_mem",
    "n_thread", "max_depth", "branch_density", "chars_per_line",
)


def feature_names(rows: list[dict[str, Any]], tier: str) -> list[str]:
    batch_cols = sorted(k for k in rows[0] if k.startswith("batch_"))
    base = list(TIER_A) + batch_cols
    if tier == "B":
        return base + list(TIER_B_SRC)
    return base


def to_matrix(rows: list[dict[str, Any]], names: list[str]) -> tuple[list[list[float]], list[int]]:
    X = [[float(r.get(n, 0.0)) for n in names] for r in rows]
    y = [int(r["y"]) for r in rows]
    return X, y


# ══════════════════════════════════════════════════════════════════════════
# 模型（纯标准库）
# ══════════════════════════════════════════════════════════════════════════
def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


class Logistic:
    """L2 逻辑回归（标准化 + 全批量梯度下降，确定性）。"""

    def __init__(self, l2: float = 1.0, lr: float = 0.5, iters: int = 2500) -> None:
        self.l2 = l2
        self.lr = lr
        self.iters = iters
        self.mu: list[float] = []
        self.sd: list[float] = []
        self.w: list[float] = []

    def fit(self, X: list[list[float]], y: list[int]) -> Logistic:
        n, p = len(X), len(X[0])
        self.mu = [sum(X[i][j] for i in range(n)) / n for j in range(p)]
        self.sd = []
        for j in range(p):
            v = sum((X[i][j] - self.mu[j]) ** 2 for i in range(n)) / max(1, n)
            self.sd.append(math.sqrt(v) or 1.0)
        Z = [[(X[i][j] - self.mu[j]) / self.sd[j] for j in range(p)] for i in range(n)]
        self.w = [0.0] * p
        b = math.log(max(1e-6, sum(y) / max(1, n)) / max(1e-6, 1 - sum(y) / max(1, n)))
        for _ in range(self.iters):
            g = [0.0] * p
            gb = 0.0
            for i in range(n):
                z = b + sum(self.w[j] * Z[i][j] for j in range(p))
                d = sigmoid(z) - y[i]
                for j in range(p):
                    g[j] += d * Z[i][j]
                gb += d
            for j in range(p):
                self.w[j] -= self.lr * (g[j] / n + self.l2 * self.w[j])
            b -= self.lr * (gb / n)
        self.bias = b
        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        p = len(self.w)
        return [sigmoid(self.bias + sum(self.w[j] * ((x[j] - self.mu[j]) / self.sd[j])
                                        for j in range(p))) for x in X]

    @property
    def coefs(self) -> list[float]:
        return [self.w[j] / self.sd[j] for j in range(len(self.w))]


class CartNode(dict):  # type: ignore[type-arg]
    pass


class Cart:
    """极简 CART（Gini + 二分阈值）。"""

    def __init__(self, max_depth: int = 5, min_leaf: int = 12, rng: random.Random | None = None) -> None:
        self.max_depth = max_depth
        self.min_leaf = min_leaf
        self.rng = rng or random.Random(0)
        self.root: dict[str, Any] | None = None
        self.names: list[str] = []
        self.splits: Counter[str] = Counter()

    def fit(self, X: list[list[float]], y: list[int], names: list[str]) -> Cart:
        self.names = names
        idx = list(range(len(y)))
        self.root = self._grow(X, y, idx, 0)
        return self

    @staticmethod
    def _gini(pos: int, tot: int) -> float:
        if tot == 0:
            return 0.0
        q = pos / tot
        return 2 * q * (1 - q)

    def _grow(self, X: list[list[float]], y: list[int], idx: list[int], depth: int) -> dict[str, Any]:
        n = len(idx)
        pos = sum(y[i] for i in idx)
        node: dict[str, Any] = {"n": n, "p": (pos / n) if n else 0.0}
        if depth >= self.max_depth or n < 2 * self.min_leaf or pos in (0, n):
            return node
        base = self._gini(pos, n)
        cand = list(range(len(self.names)))
        self.rng.shuffle(cand)
        cand = cand[: max(1, int(math.sqrt(len(cand))))]
        best: tuple[float, int, float] | None = None
        for j in cand:
            vals = sorted({X[i][j] for i in idx})
            if len(vals) < 2:
                continue
            step = max(1, len(vals) // 12)
            for k in range(0, len(vals) - 1, step):
                thr = (vals[k] + vals[k + 1]) / 2.0
                lp = lt = rp = rt = 0
                for i in idx:
                    if X[i][j] <= thr:
                        lt += 1
                        lp += y[i]
                    else:
                        rt += 1
                        rp += y[i]
                if lt < self.min_leaf or rt < self.min_leaf:
                    continue
                g = (lt / n) * self._gini(lp, lt) + (rt / n) * self._gini(rp, rt)
                if best is None or g < best[0]:
                    best = (g, j, thr)
        if best is None or best[0] >= base - 1e-9:
            return node
        _g, j, thr = best
        self.splits[self.names[j]] += 1
        li = [i for i in idx if X[i][j] <= thr]
        ri = [i for i in idx if X[i][j] > thr]
        node.update({"feature": self.names[j], "threshold": round(thr, 4), "gain": round(base - _g, 5)})
        node["left"] = self._grow(X, y, li, depth + 1)
        node["right"] = self._grow(X, y, ri, depth + 1)
        return node

    def predict(self, X: list[list[float]]) -> list[float]:
        out = []
        for x in X:
            node = self.root
            while node is not None and "feature" in node:
                j = self.names.index(node["feature"])
                node = node["left"] if x[j] <= float(node["threshold"]) else node["right"]
            out.append(float(node.get("p", 0.0)) if node else 0.0)
        return out


class BaggedCart:
    """装袋 CART（随机森林式：自助采样 + 特征子采样；纯标准库）。"""

    def __init__(self, bags: int = 30, max_depth: int = 6, seed: int = 697) -> None:
        self.bags = bags
        self.max_depth = max_depth
        self.seed = seed
        self.trees: list[Cart] = []

    def fit(self, X: list[list[float]], y: list[int], names: list[str]) -> BaggedCart:
        rng = random.Random(self.seed)
        n = len(y)
        self.trees = []
        for b in range(self.bags):
            idx = [rng.randrange(n) for _ in range(n)]
            t = Cart(max_depth=self.max_depth, rng=random.Random(self.seed + b))
            t.fit([X[i] for i in idx], [y[i] for i in idx], names)
            self.trees.append(t)
        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        if not self.trees:
            return [0.0] * len(X)
        preds = [t.predict(X) for t in self.trees]
        return [sum(p[i] for p in preds) / len(preds) for i in range(len(X))]

    def importance(self) -> Counter[str]:
        out: Counter[str] = Counter()
        for t in self.trees:
            out.update(t.splits)
        return out


# ══════════════════════════════════════════════════════════════════════════
# 评估
# ══════════════════════════════════════════════════════════════════════════
def auc(y: list[int], p: list[float]) -> float:
    """Mann–Whitney 秩统计 AUC（并列取平均秩）。"""
    pos = [p[i] for i in range(len(y)) if y[i] == 1]
    neg = [p[i] for i in range(len(y)) if y[i] == 0]
    npos, nneg = len(pos), len(neg)
    if npos == 0 or nneg == 0:
        return 0.5
    pairs = sorted((v, 0) for v in pos) + sorted((v, 1) for v in neg)
    pairs.sort(key=lambda t: t[0])
    ranks = [0.0] * len(pairs)
    i = 0
    while i < len(pairs):
        j = i
        while j + 1 < len(pairs) and pairs[j + 1][0] == pairs[i][0]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    rpos = sum(ranks[k] for k in range(len(pairs)) if pairs[k][1] == 0)
    return round((rpos - npos * (npos + 1) / 2.0) / (npos * nneg), 6)


def confusion(y: list[int], p: list[float], thr: float = 0.5) -> dict[str, Any]:
    tp = sum(1 for i in range(len(y)) if y[i] == 1 and p[i] >= thr)
    fp = sum(1 for i in range(len(y)) if y[i] == 0 and p[i] >= thr)
    fn = sum(1 for i in range(len(y)) if y[i] == 1 and p[i] < thr)
    tn = sum(1 for i in range(len(y)) if y[i] == 0 and p[i] < thr)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    acc = (tp + tn) / len(y) if y else 0.0
    return {
        "threshold": thr, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "accuracy": round(acc, 6), "precision": round(prec, 6),
        "recall": round(rec, 6), "f1": round(f1, 6),
        "majority_baseline_accuracy": round(max(sum(y), len(y) - sum(y)) / len(y), 6) if y else 0.0,
    }


def group_folds(groups: list[str], folds: int, seed: int = 697) -> dict[str, int]:
    """把**组**分到 k 个折（同组必同折）；按组大小降序贪心装入当前最小的折。"""
    sizes: Counter[str] = Counter(groups)
    order = sorted(sizes, key=lambda g: (-sizes[g], g))
    rng = random.Random(seed)
    rng.shuffle(order)
    load = [0] * folds
    assign: dict[str, int] = {}
    for g in order:
        f = min(range(folds), key=lambda k: load[k])
        assign[g] = f
        load[f] += sizes[g]
    return assign


def cross_validate(
    rows: list[dict[str, Any]], names: list[str], group_key: str, folds: int,
) -> dict[str, Any]:
    X, y = to_matrix(rows, names)
    # 分组键 → 样本行字段的显式映射（**不要**拿 group_key 直接当字段名，
    # 否则 get 不到就静默退化成 uid 单样本组 ⇒ 家族感知 CV 变成假象）
    field = {"clone_family_677b": "clone_family",
             "structural_signature": "signature"}.get(group_key)
    if field is None:  # random
        rng = random.Random(697)
        assign = {str(r["uid"]): rng.randrange(folds) for r in rows}
        fold_of = [assign[str(r["uid"])] for r in rows]
        groups = [str(r["uid"]) for r in rows]
    else:
        groups = [str(r.get(field) or r["uid"]) for r in rows]
        ga = group_folds(groups, folds)
        fold_of = [ga[g] for g in groups]
    if group_key != "random":
        _log.info("分组 %s：%d 个组（最大组 %d）", group_key, len(set(groups)),
                  max(Counter(groups).values()))

    out: dict[str, Any] = {"group_key": group_key, "folds": folds,
                           "n_groups": len(set(groups)), "models": {}}
    for mname in ("logreg", "cart", "bagged_cart"):
        pred = [0.0] * len(y)
        for f in range(folds):
            tr = [i for i in range(len(y)) if fold_of[i] != f]
            te = [i for i in range(len(y)) if fold_of[i] == f]
            if not te or not tr:
                continue
            Xtr = [X[i] for i in tr]
            ytr = [y[i] for i in tr]
            Xte = [X[i] for i in te]
            if mname == "logreg":
                m: Any = Logistic().fit(Xtr, ytr)
            elif mname == "cart":
                m = Cart(max_depth=5).fit(Xtr, ytr, names)
            else:
                m = BaggedCart(bags=25, max_depth=6).fit(Xtr, ytr, names)
            pv = m.predict(Xte)
            for k, i in enumerate(te):
                pred[i] = pv[k]
        out["models"][mname] = {
            "auc": auc(y, pred),
            **{k: v for k, v in confusion(y, pred).items()},
        }
    return out


# ══════════════════════════════════════════════════════════════════════════
# 理论上限
# ══════════════════════════════════════════════════════════════════════════
def within_family_disagreement(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """族内裁决不一致 ⇒ **可计算的 Bayes 误差下界**。

    同一克隆家族的样本是同一模板的参数变体，特征（尤其结构特征）近乎相同。
    若同族内既有 catch 又有 miss，则**任何**基于特征的模型都无法把它们分开 ⇒
    该族的不可约错误率 ≥ min(q, 1−q)（q = 族内 catch 比例）。
    """
    by: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by[str(r["clone_family"])].append(int(r["y"]))
    multi = {k: v for k, v in by.items() if len(v) >= 2}
    mixed = {k: v for k, v in multi.items() if 0 < sum(v) < len(v)}
    irr = 0.0
    for k, v in multi.items():
        q = sum(v) / len(v)
        irr += min(q, 1 - q) * len(v)
    n_multi = sum(len(v) for v in multi.values())
    return {
        "n_families": len(by),
        "n_multi_member_families": len(multi),
        "n_mixed_verdict_families": len(mixed),
        "share_mixed_of_multi": round(len(mixed) / len(multi), 6) if multi else None,
        "n_samples_in_multi_member_families": n_multi,
        "irreducible_error_samples": round(irr, 2),
        "bayes_error_lower_bound_pct": round(irr / len(rows) * 100.0, 4),
        "implied_accuracy_upper_bound": round(1.0 - irr / len(rows), 6),
        "interpretation": (
            "同族（近乎同特征）样本被判成不同裁决 ⇒ 特征无法解释的部分。"
            "这是对**任何**特征模型（含深度学习）都成立的错误率下界，"
            "与模型容量无关，只与数据的标签一致性有关。"
        ),
    }


def family_transfer_ceiling(rows: list[dict[str, Any]], folds: int) -> dict[str, Any]:
    """族迁移天花板：用「同 defect_type 的**其它家族**的 catch 率」预测一个全新家族。

    这是「泛化到一个从未见过的家族」时**任何**模型可达 AUC 的一个诚实上界代理：
    它只用跨族可迁移的粗粒度信息（缺陷类型），不含任何族内记忆。
    """
    groups = [str(r["clone_family"]) for r in rows]
    ga = group_folds(groups, folds)
    pred = [0.0] * len(rows)
    for f in range(folds):
        tr = [r for r in rows if ga[str(r["clone_family"])] != f]
        te_idx = [i for i, r in enumerate(rows) if ga[str(r["clone_family"])] == f]
        rate_by_type: dict[str, list[int]] = defaultdict(list)
        for r in tr:
            rate_by_type[str(r["defect_type"])].append(int(r["y"]))
        global_rate = sum(int(r["y"]) for r in tr) / max(1, len(tr))
        for i in te_idx:
            dt = str(rows[i]["defect_type"])
            v = rate_by_type.get(dt)
            pred[i] = (sum(v) / len(v)) if v else global_rate
    y = [int(r["y"]) for r in rows]
    return {
        "prediction_rule": "leave-one-family-out：同 defect_type 的其它家族的 catch 率（无该类型则取全局率）",
        "auc": auc(y, pred),
        **{k: v for k, v in confusion(y, pred).items()},
        "interpretation": (
            "只靠**跨族可迁移**的粗粒度信息可达的 AUC。"
            "任何家族感知 CV 下的模型，其 AUC 若显著高于此值，说明它还吃到了族内记忆（泄漏）；"
            "若低于此值，说明模型连粗粒度信号都没用好。"
        ),
    }


def rice_argument(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """不可判定性论证（定性，但给出现有数据能支持的量化脚注）。"""
    by_type: dict[str, list[int]] = defaultdict(list)
    for r in rows:
        by_type[str(r["defect_type"])].append(int(r["y"]))
    n_types = len(by_type)
    deterministic = [t for t, v in by_type.items() if sum(v) in (0, len(v)) and len(v) >= 3]
    return {
        "claim": (
            "「程序 P 的缺陷 x 会被资产 a 捕获」是关于程序语义的非平凡性质。"
            "由 Rice 定理，不存在对所有 (P, x, a) 都正确的判定程序 ⇒ "
            "不存在一个**完备**的可检测性预测器；任何预测器必有系统性盲区。"
        ),
        "quantitative_footnote": {
            "n_defect_types": n_types,
            "n_types_with_deterministic_verdict_min3_samples": len(deterministic),
            "deterministic_types": sorted(deterministic),
            "note": (
                "确定性类型（同类型全部 catch 或全部 miss）是 Rice 定理下的「可判定岛」；"
                "其余类型的裁决依赖具体语义 ⇒ 只能学，**不能证**。"
            ),
        },
        "honest_boundary": (
            "本节是**论证**不是定理证明：Rice 定理给的是「不存在完备判定程序」，"
            "而预测器允许有错误率，两者不矛盾。本节的用途是说明「AUC < 1 是原理性的，不是数据不够」。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 主动学习
# ══════════════════════════════════════════════════════════════════════════
def active_learning(rows: list[dict[str, Any]], names: list[str], folds: int, top: int = 20) -> dict[str, Any]:
    """不确定性采样（|p−0.5| 升序）+ 家族去重（每族最多 1 条）。"""
    X, y = to_matrix(rows, names)
    groups = [str(r["clone_family"]) for r in rows]
    ga = group_folds(groups, folds)
    pred = [0.0] * len(rows)
    for f in range(folds):
        tr = [i for i in range(len(y)) if ga[groups[i]] != f]
        te = [i for i in range(len(y)) if ga[groups[i]] == f]
        if not tr or not te:
            continue
        m = BaggedCart(bags=25, max_depth=6).fit([X[i] for i in tr], [y[i] for i in tr], names)
        pv = m.predict([X[i] for i in te])
        for k, i in enumerate(te):
            pred[i] = pv[k]

    order = sorted(range(len(rows)), key=lambda i: abs(pred[i] - 0.5))
    picked: list[dict[str, Any]] = []
    seen: set[str] = set()
    for i in order:
        g = groups[i]
        if g in seen:
            continue
        seen.add(g)
        picked.append({
            "rank": len(picked) + 1,
            "uid": rows[i]["uid"],
            "defect_type": rows[i]["defect_type"],
            "family": rows[i]["family"],
            "clone_family": g,
            "predicted_p_catch": round(pred[i], 4),
            "observed_verdict": "catch" if y[i] == 1 else "miss",
            "uncertainty": round(abs(pred[i] - 0.5), 4),
            "why": "模型在该样本上最接近 0.5，且该家族尚未被选中（多样性约束）",
        })
        if len(picked) >= top:
            break
    return {
        "strategy": "uncertainty sampling (|p−0.5| 升序) + 每克隆家族最多 1 条",
        "model": "bagged_cart（家族感知 5 折的折外预测）",
        "n_candidates": len(rows),
        "top": picked,
    }


# ══════════════════════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="697-C 能力边界预测模型（只读）")
    ap.add_argument("--folds", type=int, default=5)
    ap.add_argument("--bags", type=int, default=25)
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    rows, meta = build_dataset()
    _log.info("数据集 %d 条（有源码 %d）；基率 %.4f；克隆家族 %d",
              meta["n_total"], meta["n_with_source"], meta["base_rate_catch"],
              meta["n_clone_families"])

    tiers: dict[str, list[dict[str, Any]]] = {
        "A_manifest_only_1147": rows,
        "B_plus_source_1042": [r for r in rows if r["has_source"]],
    }
    results: dict[str, Any] = {}
    for tname, sub in tiers.items():
        names = feature_names(sub, "A" if tname.startswith("A") else "B")
        results[tname] = {
            "n": len(sub),
            "n_features": len(names),
            "base_rate_catch": round(sum(int(r["y"]) for r in sub) / len(sub), 6),
            "cv": {
                gk: cross_validate(sub, names, gk, args.folds)
                for gk in ("clone_family_677b", "structural_signature", "random")
            },
        }

    # 特征重要性（Tier B，全量拟合）
    b_rows = tiers["B_plus_source_1042"]
    b_names = feature_names(b_rows, "B")
    Xb, yb = to_matrix(b_rows, b_names)
    lr = Logistic().fit(Xb, yb)
    coef_items: list[dict[str, Any]] = [
        {"feature": b_names[j], "standardized_coef": round(lr.coefs[j], 6),
         "abs": round(abs(lr.coefs[j]), 6)}
        for j in range(len(b_names))
    ]
    coef_rank = sorted(coef_items, key=lambda d: -float(d["abs"]))[:10]
    bag = BaggedCart(bags=args.bags, max_depth=6).fit(Xb, yb, b_names)
    split_rank = [{"feature": f, "n_splits": c} for f, c in bag.importance().most_common(10)]

    doc: dict[str, Any] = {
        "schema": "queyi-697/capability-boundary-model/v1",
        "generated_by": "tools/train_697_predictor.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "target": "样本级 OR(8 资产) == catch（wunsequenced/compile-time 恒 unknown ⇒ 等价于 6 资产口径）",
        "dataset_meta": meta,
        "results_by_tier": results,
        "feature_importance": {
            "logistic_standardized_top10_tierB": coef_rank,
            "bagged_cart_split_count_top10_tierB": split_rank,
        },
        "theoretical_upper_bound": {
            "within_family_bayes_bound": within_family_disagreement(rows),
            "family_transfer_ceiling": family_transfer_ceiling(rows, args.folds),
            "undecidability": rice_argument(rows),
        },
        "active_learning_top20": active_learning(b_rows, b_names, args.folds, top=20),
        "honest_limits": [
            "本机无 numpy/scikit-learn/xgboost ⇒ 逻辑回归与装袋 CART 均为**纯标准库**实现，"
            "不是 sklearn/XGBoost 的同名算法，超参数未做搜索。",
            "样本 92.9% 为人工植入 ⇒ 模型学的是**仪器**而非真实缺陷分布。",
            "677b 家族只定义在 A5 的 1137 条上；676g 多出的 10 条退化为单成员家族。",
            "Tier A（无源码特征）与 Tier B 的 AUC 差即为「源码特征买来的增益」，"
            "但两层的样本集不同（1147 vs 1042），比较需谨慎。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 697-C 能力边界预测模型（只读）==")
    for tname, r in results.items():
        print(f"\n  [{tname}] n={r['n']}  p={r['n_features']}  基率={r['base_rate_catch']}")
        for gk, cv in r["cv"].items():
            line = "    " + f"{gk:<22}"
            for m, s in cv["models"].items():
                line += f"  {m}:AUC={s['auc']:.4f}/F1={s['f1']:.4f}"
            print(line)
    wf = doc["theoretical_upper_bound"]["within_family_bayes_bound"]
    print(f"\n  族内 Bayes 误差下界 = {wf['bayes_error_lower_bound_pct']}% ⇒ "
          f"任何特征模型 accuracy ≤ {wf['implied_accuracy_upper_bound']}")
    ft = doc["theoretical_upper_bound"]["family_transfer_ceiling"]
    print(f"  族迁移天花板 AUC = {ft['auc']}")
    print("\n  特征重要性 Top5（|标准化系数|）：" +
          ", ".join(f"{d['feature']}={d['standardized_coef']}" for d in coef_rank[:5]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
