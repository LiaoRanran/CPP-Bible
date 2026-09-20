#!/usr/bin/env python3
"""612 线 D · D2：BKT（贝叶斯知识追踪）最小实现（**纯标准库**，零依赖）。

BKT 四参数：
  * P(L0)：初始掌握概率（默认 0.1）
  * P(T) ：迁移/学习概率（每次练习后 未掌握→掌握，默认 0.05）
  * P(S) ：滑移概率（掌握了但答错，默认 0.1）
  * P(G) ：猜测概率（未掌握但答对，默认 0.2）

核心递推（标准 BKT）：
  * 观测到作答 x∈{0,1} 后，先做贝叶斯后验得「此刻是否已掌握」：
      p_known = P(L)·P(x|knows) / [P(L)·P(x|knows) + (1−P(L))·P(x|¬knows)]
      P(x=1|knows)=1−S, P(x=1|¬knows)=G；P(x=0|knows)=S, P(x=0|¬knows)=1−G
  * 再做学习更新得下一步先验：P(L)' = p_known + (1−p_known)·T
  * 预测下一题答对：P(correct) = P(L)·(1−S) + (1−P(L))·G

参数拟合：网格搜索 + 最大似然（多个用户的 0/1 作答序列），标注「近似拟合」。

纯粹原型：不实现 BKT+ / DKT / 多维度掌握度（留待后续迭代）。

用法：
  python tools/bkt_solver.py --demo
  python tools/bkt_solver.py --predict --sequence "1,0,1,1,0"
  python tools/bkt_solver.py --fit --data <file>
  python tools/bkt_solver.py --check     # 自验证（exit 0=通过）
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

VERSION = "1.0"


# ── 模型 ──────────────────────────────────────────────────────────────────
@dataclass
class BKTModel:
    p_l0: float = 0.1
    p_t: float = 0.05
    p_s: float = 0.1
    p_g: float = 0.2

    def _clamp(self) -> None:
        for name in ("p_l0", "p_t", "p_s", "p_g"):
            v = getattr(self, name)
            setattr(self, name, min(1.0, max(0.0, v)))

    def predict_correct(self, mastery: float) -> float:
        """给定当前掌握概率，预测下一题答对概率。"""
        return mastery * (1.0 - self.p_s) + (1.0 - mastery) * self.p_g

    def step(self, mastery: float, x: int) -> float:
        """单步：观测作答 x 后，返回**学习更新后**的下一步掌握先验概率。"""
        p_cor_given_knows = 1.0 - self.p_s
        p_cor_given_not = self.p_g
        p_x_k = p_cor_given_knows if x == 1 else self.p_s
        p_x_n = p_cor_given_not if x == 1 else (1.0 - self.p_g)
        p_x = mastery * p_x_k + (1.0 - mastery) * p_x_n
        if p_x <= 0.0:
            p_known = 0.0
        else:
            p_known = (mastery * p_x_k) / p_x
        # 学习更新
        return p_known + (1.0 - p_known) * self.p_t

    def run_sequence(self, seq: list[int]) -> dict:
        """递推整条序列，返回每步后验（step 后先验）与每步「答对预测」。"""
        mastery = self.p_l0
        posteriors: list[float] = []
        predictions: list[float] = []
        for x in seq:
            predictions.append(self.predict_correct(mastery))
            mastery = self.step(mastery, x)
            posteriors.append(mastery)
        return {"mastery_after": posteriors, "predict_correct_before": predictions,
                "final_mastery": mastery if seq else self.p_l0}


@dataclass
class LearnerState:
    kc_id: str
    mastery_prob: float = 0.1
    answer_history: list[dict] = field(default_factory=list)

    def update(self, model: BKTModel, correct: bool) -> float:
        self.mastery_prob = model.step(self.mastery_prob, 1 if correct else 0)
        self.answer_history.append({"correct": bool(correct)})
        return self.mastery_prob


# ── 参数拟合（网格搜索 + MLE）────────────────────────────────────────────
def _log_likelihood(model: BKTModel, sequences: list[list[int]]) -> float:
    ll = 0.0
    for seq in sequences:
        mastery = model.p_l0
        for x in seq:
            pc = model.predict_correct(mastery)
            p_x = pc if x == 1 else (1.0 - pc)
            if p_x <= 0.0:
                return -1e18
            ll += math.log(p_x)
            mastery = model.step(mastery, x)
    return ll


def fit(sequences: list[list[int]]) -> BKTModel:
    """网格搜索近似拟合（标注「近似」）。固定维度上做粗网格，取最大似然。"""
    best: BKTModel | None = None
    best_ll = -1e18
    for p_t in (0.01, 0.05, 0.1, 0.2, 0.3):
        for p_s in (0.05, 0.1, 0.2, 0.3):
            for p_g in (0.1, 0.2, 0.3):
                for p_l0 in (0.05, 0.1, 0.2, 0.3):
                    m = BKTModel(p_l0=p_l0, p_t=p_t, p_s=p_s, p_g=p_g)
                    ll = _log_likelihood(m, sequences)
                    if ll > best_ll:
                        best_ll = ll
                        best = m
    return best if best is not None else BKTModel()


def load_sequences(path: str) -> list[list[int]]:
    text = Path(path).read_text(encoding="utf-8")
    if text.lstrip().startswith("["):
        data = json.loads(text)
        return [[int(v) for v in seq] for seq in data]
    out: list[list[int]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        out.append([int(c) for c in line.replace(",", " ").split() if c in "01"])
    return out


# ── CLI ─────────────────────────────────────────────────────────────────
def _demo() -> int:
    m = BKTModel()
    seq = [1, 0, 1, 1, 0, 1, 1, 1]
    r = m.run_sequence(seq)
    print(f"[BKT] 默认参数：L0={m.p_l0} T={m.p_t} S={m.p_s} G={m.p_g}")
    print(f"[BKT] 序列 {seq}")
    print(f"[BKT] 每步后掌握概率：{[round(v,4) for v in r['mastery_after']]}")
    print(f"[BKT] 最终掌握概率：{round(r['final_mastery'],4)}")
    print(f"[BKT] 末步下一题答对预测：{round(m.predict_correct(r['final_mastery']),4)}")
    return 0


def _predict(seq_str: str) -> int:
    m = BKTModel()
    seq = [int(c) for c in seq_str.replace(",", " ").split() if c in "01"]
    r = m.run_sequence(seq)
    print(f"[BKT] 序列 {seq}（{len(seq)} 步）")
    print(f"[BKT] 每步后掌握概率：{[round(v,4) for v in r['mastery_after']]}")
    print(f"[BKT] 下一题答对预测概率：{round(m.predict_correct(r['final_mastery']),4)}")
    return 0


def _do_fit(path: str) -> int:
    seqs = load_sequences(path)
    if not seqs:
        print("[BKT] ❌ 数据为空", file=sys.stderr)
        return 2
    m = fit(seqs)
    print(f"[BKT] 拟合（近似，网格搜索 MLE）共 {len(seqs)} 条序列：")
    print(f"[BKT] L0={m.p_l0} T={m.p_t} S={m.p_s} G={m.p_g} ｜ "
          f"logLikelihood={round(_log_likelihood(m, seqs),3)}")
    return 0


def _check() -> int:
    m = BKTModel()
    problems: list[str] = []
    # 1) run_sequence 长度一致、范围合法
    seq = [1, 0, 1, 1, 0]
    r = m.run_sequence(seq)
    if len(r["mastery_after"]) != len(seq):
        problems.append("run_sequence 长度应等于序列长")
    if not all(0.0 <= v <= 1.0 for v in r["mastery_after"]):
        problems.append("掌握概率应∈[0,1]")
    if not 0.0 <= r["predict_correct_before"][0] <= 1.0:
        problems.append("下一题答对预测应∈[0,1]")
    # 2) 全对序列：掌握概率单调不减，且终点高于起点（BKT 正确性质，spec 要求）
    all_corr = m.run_sequence([1] * 20)["mastery_after"]
    if any(all_corr[i + 1] < all_corr[i] for i in range(len(all_corr) - 1)):
        problems.append("全对序列掌握概率应单调不减")
    if not all_corr[-1] > all_corr[0]:
        problems.append("全对序列终点掌握概率应高于起点")
    # 3) 全错序列：单调不增，且终点低于起点（BKT 正确性质，spec 要求）
    all_wrong = m.run_sequence([0] * 20)["mastery_after"]
    if any(all_wrong[i + 1] > all_wrong[i] for i in range(len(all_wrong) - 1)):
        problems.append("全错序列掌握概率应单调不增")
    if not all_wrong[-1] < all_wrong[0]:
        problems.append("全错序列终点掌握概率应低于起点")
    # 4) 预测在 [0,1]
    if not 0.0 <= m.predict_correct(0.5) <= 1.0:
        problems.append("predict_correct 应∈[0,1]")
    # 5) 拟合返回合法参数
    fitted = fit([[1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 0, 1, 1]])
    for name in ("p_l0", "p_t", "p_s", "p_g"):
        if not 0.0 <= getattr(fitted, name) <= 1.0:
            problems.append(f"拟合参数 {name} 应∈[0,1]")
    if problems:
        print("[BKT] ❌ 自检失败：", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1
    print("[BKT] ✅ 自验证通过：递推/预测/收敛/拟合 全部一致")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bkt_solver", description="612 D2 BKT 最小实现（纯标准库）")
    ap.add_argument("--version", action="version", version=f"bkt_solver {VERSION}")
    ap.add_argument("--demo", action="store_true", help="演示递推")
    ap.add_argument("--predict", action="store_true", help="预测给定序列后的掌握度")
    ap.add_argument("--sequence", default="1,0,1,1,0", help="--predict 的序列，如 '1,0,1,1,0'")
    ap.add_argument("--fit", action="store_true", help="从数据拟合参数")
    ap.add_argument("--data", default=None, help="--fit 的数据文件（每行 0/1，或 JSON 序列列表）")
    ap.add_argument("--check", action="store_true", help="自验证")
    a = ap.parse_args(argv)
    if a.check:
        return _check()
    if a.demo:
        return _demo()
    if a.predict:
        return _predict(a.sequence)
    if a.fit:
        if not a.data:
            print("[BKT] ❌ --fit 需要 --data <file>", file=sys.stderr)
            return 2
        return _do_fit(a.data)
    return _demo()


if __name__ == "__main__":
    raise SystemExit(main())
