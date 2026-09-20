# 613 基线 0.2 · 学习者镜像数据缺口台账

> 生成：`python tools/613_baseline.py` ｜ 时间：2026-09-20T23:54:27
> 口径：只读统计；CI 结论取自 GitHub Actions API；**未运行**监工类 --check。

## 掌握度存储 `data/learner_state_612.jsonl`

- 记录数：**27** ｜ 字段：{'user_id': 27, 'kc_id': 27, 'mastery_prob': 27, 'correct': 27, 'kind': 27, 'timestamp': 27, 'simulated': 27}
- 覆盖 KC 数=27 ｜ 已掌握(≥0.5)=0 ｜ 平均掌握度=0.100

## KC 台账 `data/kc_inventory_612.json`

- KC 数：**0**

## 真实学习行为数据源

- `data/learner_behavior.jsonl`：**存在**（0 条）
- 结论：**无真实学习行为数据**（612 原型全为模拟数据）⇒ 线 C 必须先建接入层（C1）。

> 缺口判定：掌握度是 612 `simulate()` 生成的模拟值，非真实行为递推 ⇒ 镜像仍为空壳。
