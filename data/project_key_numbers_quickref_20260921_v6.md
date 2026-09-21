# 项目关键数字速查表 v6（2026-09-21 晚 · 614 后）

> 生成时间：2026-09-21 ｜ 版本：v6（614 收工：CI 根因修复 + 学习者镜像真实闭环 + 信任根诚实化 + M1 登记）
> 所有数字可复算；监工门禁数字按铁律取自 standing baseline（苦力未重跑）。
> v5 → v6 变化：+8 工具 / +7 测试 / 根 `_arch` 9→2 / M1 登记 / 信任根 partially_anchored。

---

## 一、仓库规模
| 指标 | v6 | 变化（vs v5） |
|------|------|---------------|
| 总 commit | 1473 | +27 |
| 工具数（tools/*.py） | **204** | +8 |
| 测试文件（tests/test_*.py） | **182** | +7 |
| 根 `_arch` 目录 | **2**（v18,v19） | -7（v10-v17 归档） |
| 根 `_*` 目录 | 13 | -9 |
| data 文件 | 446 | +22 |

## 二、知识资产
| 指标 | v6 | 说明 |
|------|------|------|
| 原子卡（KC） | 27 | atoms/（29 文件含 README/辅助） |
| 证据卡 | 56 | evidence/（57 文件含 README） |
| 命题 | 79 | observation/inference |
| MIS 误解库 | 80 | |
| 攻击边标注 | 388 | |

## 三、核心门禁（standing baseline · 苦力未重跑）
| 门禁 | 结果 | 关键数字 |
|------|------|----------|
| gate --check | ✅ | 63 规则 / 191 命中（block=0 warn=186 advice=5） |
| poison_drill | ✅ | 124/124 · RULE-COVERAGE 63/63 · 表观 100% · 诚实 95.2% |
| replay --check | ✅ | confirm=56 refute=0 infra_error=0 |
| tool_integrity --check | ✅ | 5 核心 + test_config 2 + supply_chain 5 |
| 614 新工具 --check | ✅ | **7/7 绿**（run_614_gate quick/full 实测 PASS） |

## 四、变异测试（v7 权威基线）
| 指标 | 数值 | 说明 |
|------|------|------|
| 总变体 / blocked / escaped | 1593 / 1405 / **1** | escaped = M1·EV-CONC-001 |
| 可判分母 | 1406 | |
| 逃逸率契约 | **1/1406**（0.0711%） | 双侧 C-P95 [0.0018%, 0.3956%] |
| 活雷率 | **0/1405** | 单侧上界 0.213%（排除 known-structural） |
| **known_tce** | **1**（TCE-614-001） | `data/mutation/known_tce.jsonl` |

## 五、学习者镜像（614 真实闭环）
| 指标 | 数值 | 说明 |
|------|------|------|
| 行为采集 | ✅ `learner_behavior_logger` | append-only + CSV/JSONL 导入 + BKT 递推 |
| 仪表盘（真实数据版） | ✅ `learner_twin_dashboard_614` | 读行为日志→HTML |
| OOD + 跃迁 | ✅ `learner_ood_evaluator` | 掌握度≥0.8 且 OOD≥80% ⇒ jump |
| 论证层联动 | ✅ `learner_argument_link` | KC→论证链→论证复盘推荐 |
| 模拟轨迹实测 | 10 KC × 5 轮（30%→80%） | ≥5 KC 掌握度 ≥0.5 |
| 真实练习数 | **0** | 仍待用户真做题 |

## 六、信任根（诚实标注）
| 指标 | 状态 | 说明 |
|------|------|------|
| Merkle 根 | ✅ `47c330c9…` | 本地可验；digest 与 .ots 一致 |
| OTS | ⚠ **pending** | 占位零，**未提交** Bitcoin 日历 |
| in-toto link | ⚠ **HMAC 非标准** | 无公钥可验/非否认 |
| 总判定 | **`partially_anchored`** | `trust_root_status_check` |

## 七、oracle 验证
| 指标 | 数值 | 说明 |
|------|------|------|
| 待验卡 | 83（56 证据 + 27 原子） | |
| 已验 | **0** | 需人签字（未授权） |
| 优先级 Top1 | `EV-CONC-001`（18 分） | `oracle_priority_614`（已知 TCE 置顶） |
| 流程 | ✅ fail-closed | ≥2 独立 confirm；任一 refute ⇒ refuted |

## 八、六维度（614 后）
| 维度 | 分数 | 变化 |
|------|------|------|
| 机械判决 | 9.2 | → |
| 信任根 | 8.9 | → |
| 度量诚实 | 8.7 | ↑0.1 |
| 人审流程 | 7.8 | → |
| 知识资产 | 7.8 | ↑0.2 |
| 论证层 | 7.7 | ↑0.1 |
| **平均** | **≈8.4** | **↑** |

## 九、CI 状态
| 指标 | 数值 | 说明 |
|------|------|------|
| gate/quality 红根因 | **缺 pyyaml**（已修 `512d991`） | ci.yml 补装 |
| 四 job 全绿 | ⏳ 待 CI 实跑 | 本机无 gh 通道 |

## 十、交人项
1. CI 四 job 实跑全绿确认
2. OTS 真实上链（不可逆）
3. in-toto 真签名（密钥托管）
4. 行为采集两版合并方向（613 ingest vs 614 logger）
5. 活性锚补丁集是否落卡（50→41）
6. modify 口径（keep-low IN114/OUT7 vs upgrade-medium IN121/OUT0）

---

*v6 由 614 批次收工生成；v5→v6：+8 工具/+7 测试/根 `_arch` 9→2/M1 登记/信任根 partially_anchored/导航 +34。*
