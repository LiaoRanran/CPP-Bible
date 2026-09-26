# -*- coding: utf-8 -*-
"""
p03_conformal_abstention.py — _arch_v20 只读探针
自由方向 A（保形预测/选择性预测）+ 方向 12（信息论）：
  Part 1【仓内真实数据，只读】poison_surface_map.json 的攻击类型分布
          → Shannon 熵 / 有效攻击面（entropy-2 等效类别数）/ 覆盖率集中度
  Part 2【合成 Monte Carlo，明确标注：机制演示，非仓内实证】
          split-conformal 接受/弃权机制：
            - 可交换性成立时，经验覆盖率是否 = 名义 1-alpha（有限样本）
            - OOD 漂移下覆盖率如何崩坏；conformal p-value 能否把漂移样本判为弃权
          目的：量化「逐卡片级风险保证 + 显式弃权类」相对全局逃逸率上界的形态差异
"""
import json, math, random, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SURF = os.path.join(ROOT, "tools", "poison_surface_map.json")
ALPHA = 0.10
SEED = 20260921


def H(counts):
    n = sum(counts)
    return -sum((c / n) * math.log2(c / n) for c in counts if c)


def part1_poison_entropy():
    print("## Part 1 毒样例攻击面熵（真实文件 tools/poison_surface_map.json）")
    d = json.load(open(SURF, encoding="utf-8"))
    drill = d["drill"]
    at = d["attack_types"]
    print(f"  drill: {drill['passed']}/{drill['total']}  schema task={d.get('task')}  "
          f"generated_at={d.get('generated_at')}")
    items = [(k, v.get("count", 0)) for k, v in at.items()]
    items.sort(key=lambda kv: -kv[1])
    tot = sum(c for _, c in items)
    h = H([c for _, c in items])
    print(f"  攻击类型数={len(items)}  毒样例总数(类型合计)={tot}")
    print(f"  Shannon 熵 H = {h:.3f} bit   最大熵 log2(k) = {math.log2(len(items)):.3f} bit")
    print(f"  归一化熵 H/Hmax = {h/math.log2(len(items)):.3f}  （越接近1攻击面越均匀分散）")
    print(f"  有效等效类别数 2^H = {2**h:.1f} （名义类别 {len(items)}）")
    cum = 0
    for i, (k, c) in enumerate(items, 1):
        cum += c
        if i <= 5 or i >= len(items) - 2:
            print(f"    {k:4s} {c:3d}  {c/tot*100:5.1f}%  累计{cum/tot*100:5.1f}%  {v_get(at,k)}")
        elif i == 6:
            print("    ...")
    # RULE-COVERAGE 如果存在
    rc = d.get("rule_coverage") or d.get("rules")
    if rc:
        print("  文件含 rule_coverage 键:", type(rc).__name__)


def v_get(at, k):
    lab = at[k].get("label", "")
    return lab[:46] + ("…" if len(lab) > 46 else "")


def part2_conformal():
    print("\n## Part 2 split-conformal 接受/弃权（合成数据机制演示，非仓内实证）")
    rnd = random.Random(SEED)
    n_cal, n_test, reps = 200, 500, 400

    # 非符合性分数：v=1 正确（分数低），错误（分数高）；正确~Beta(2,5)，错误~Beta(5,2)
    def sample(rng, p_err, shift=0.0):
        v = 0 if rng.random() < p_err else 1
        s = rnd.betavariate(5, 2) if v == 0 else rng.betavariate(2, 5)
        return v, min(1.0, s + shift)

    def trial(p_err, shift=0.0, screen=False):
        cal = [sample(rnd, p_err) for _ in range(n_cal)]
        scores = sorted(s for _, s in cal)
        k = min(n_cal, int(math.ceil((n_cal + 1) * (1 - ALPHA))) - 1)
        t = scores[k]
        correct_total = covered = abst = 0
        for _ in range(n_test):
            v, s = sample(rnd, p_err, shift=shift)
            # conformal p-value：校准集中非符合性 >= 该样本的比例（小=异常）
            pv = (1 + sum(1 for c in scores if c >= s)) / (n_cal + 1)
            if screen and pv < 0.05:
                abst += 1; continue
            if v == 1:
                correct_total += 1
                if s <= t: covered += 1
        return correct_total, covered, abst

    for name, kw in (("可交换(p_err=.10,无漂移)", dict(p_err=0.10)),
                     ("OOD漂移(shift=+0.15)无筛查", dict(p_err=0.10, shift=0.15)),
                     ("OOD漂移+conformal p值弃权", dict(p_err=0.10, shift=0.15, screen=True))):
        CT = CV = AB = 0
        for _ in range(reps):
            ct, cv, ab = trial(**kw)
            CT += ct; CV += cv; AB += ab
        print(f"  -- {name}")
        print(f"     正确样本经验覆盖率={CV/max(1,CT)*100:.1f}% （名义 1-α={ (1-ALPHA)*100:.0f}%）"
              f"  弃权率={AB/(reps*n_test)*100:.1f}%")


def main():
    part1_poison_entropy()
    part2_conformal()
    print("\n说明：Part2 为机制演示合成数据；保形覆盖保证依赖可交换性，")
    print("     仓内没有逐卡片的外部正确性打分序列，故该保证在阙疑的可迁移性属【推断】。")


if __name__ == "__main__":
    main()
