# 612 收工验收报告（Z 门禁）

> 生成时间：2026-09-20T22:42:09 ｜ 工具：`python tools/run_612_gate.py`
> 模式：full（含 integrity/pytest/ruff/零污染）

## 一、工具 --check（16/16 通过）

| 工具 | exit | 耗时(s) | 末行 |
|---|---|---|---|
| `612_baseline` | 0 ✅ | 0.6 | [612基线] ✓ 复算一致 |
| `bridge_edge_candidates` | 0 ✅ | 0.4 | [C2] ✓ 桥接候选锁定（98 条：strong 0 / medium 0 / weak 98） |
| `bridge_edge_pre_annotate` | 0 ✅ | 0.4 | [A1] ✓ 预标注锁定（98 条；置信度 {'high': 38, 'medium': 60}；伪桥接 58） |
| `bridge_edge_review` | 0 ✅ | 0.2 | [A2] ✓ 决策日志与候选数据一致（0 条记录） |
| `bridge_edge_impact` | 0 ✅ | 0.5 | [A3] ✓ 加桥影响锁定（6 组口径×what-if；approved-only 0 批准与基线一致） |
| `liveness_candidate_generator` | 0 ✅ | 0.2 | [B1] ✓ 候选锁定（50 条；A 9 / B 26 / C 15） |
| `liveness_review` | 0 ✅ | 0.2 | [B2] ✓ 确认日志与候选数据一致（0 条记录） |
| `liveness_impact` | 0 ✅ | 0.2 | [B3] ✓ what-if 锁定（warn 50 ⇒ 0；partial 0 ⇒ 50） |
| `oracle_priority` | 0 ✅ | 0.4 | [C2] ✓ 优先级锁定（83 张；Top1 ATOM-UB-GRAY-001=14） |
| `oracle_verifier` | 0 ✅ | 5.7 | [oracle] oracle 验证专用，非监工验收：跑 gate（timeout 120s） |
| `kc_inventory` | 0 ✅ | 0.3 | [D1] ✅ 自验证通过：KC=27 / 有前置依赖=19 / 难度均∈[1,5] |
| `bkt_solver` | 0 ✅ | 0.2 | [BKT] ✅ 自验证通过：递推/预测/收敛/拟合 全部一致 |
| `learner_state` | 0 ✅ | 0.3 | [D3] ✅ 自验证通过：KC=27 / 平均掌握度=0.1 / 已掌握=0 / 总练习=0 |
| `learner_recommender` | 0 ✅ | 0.3 | [D4] ✅ 自验证通过：候选 8 / 推荐 5 / 硬约束（前置>0.5）生效 |
| `learner_twin_dashboard` | 0 ✅ | 0.4 | [D5] ✅ 自验证通过：HTML 14427 字符 / 四模块齐全 / 含模拟标注 |
| `metrics_612` | 0 ✅ | 0.3 | [E] ✅ 自验证通过：E1(keep-low IN114/OUT7, upgrade-medium IN121/OUT0) / E2(原子27/证据56/MIS79) / E3(oracle83/评审者0) |

## 二、度量 metrics_612
- exit=0 ｜ 耗时=0.3s ｜ 产物：`data/metrics_612.md`

## 三、完整性 tool_integrity --check
- exit=0 ｜ 耗时=1.4s ｜ [tool_integrity] OK：目录级 Merkle 根与当前内容一致（警告 0 条）

## 四、回归 pytest tests/ -q
- exit=0 ｜ 耗时=245.1s ｜ 5 snapshots passed.

## 五、代码卫生 ruff check tools tests
- exit=0 ｜ 耗时=0.2s ｜ All checks passed!

## 六、零污染（受控目录 vs HEAD）
- `atoms/`: ✅ 干净
- `evidence/`: ✅ 干净
- `Examples/`: ✅ 干净
- `Book/`: ✅ 干净
- `untracked_or_modified`: ✅ 干净

## 结论
- **✅ 门禁全绿，可收工**

> 注：本门禁仅运行各工具 `--check` 与度量/回归/卫生，不代替人类 golden accept（accept 权唯人）。oracle 人审相关指标如实标注「零人审」。
