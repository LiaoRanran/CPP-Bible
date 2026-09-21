# 615 收工验收报告

> 批次：615 · 人审诚实化 + 规则双实现 + warn 治理 + 轻量建设（止血优先）
> 生成：2026-09-21 ｜ 苦力（CodeBuddy）
> **铁律**：不跑监工门禁四类；不改受控目录；不改 annotations/golden_lock/poison_drill；不删/移/重命名文件；不 push。

---

## 一、任务清单与 commit

| # | 任务 | commit | 一句话 |
|---|---|---|---|
| 0 | 基线台账 | `b43949b` | 388 人审=5 模板/镜像 194；warn 186；尺子保护 12 |
| A1 | 人审诚实化标签 | `4998b39` | 388 标签（batch 388 / item_by_item 0 / mirror 194） |
| A2 | 30 条逐条复核清单 | `708f430` | 决策清单（17 modify[OUT7] + 13 approve）+ 流程文档 |
| B1 | EV-MATRIX 独立第二实现 | `d1d2e4d` | 一致率 **68.4%**，6 分歧卡吻合历史记录 |
| B2 | 分歧修复提案 | `c440a43` | 类型 A=1/B=0/C=0；提案后 **100%** |
| B3 | 尺子全集入根 | `ca265bf` | tool_integrity 保护 12 → **22**（+ruler10） |
| C1 | warn 不增锁机制 | `d38d4cf` | 五桶分类 + 观察期/采纳授权/到期 |
| C2 | 豁免到期制 | `93ed8b2` | 27 条 legacy，到期=创建批次+10（全 active） |
| C3 | Goodhart 监控 | `37a6b99` | 危险分 **80.1/100** |
| D1 | CI 配置确认 | `52d5542` | gate/quality 有 pyyaml；四 job 依赖完整 |
| D2 | 学习者镜像验证 | `773fd61` | 模拟闭环全通过（真实事件 0） |
| D3 | 跃迁条件机器判定 | `528218a` | 门 **closed**（triggered 0 / ready 5 / not_ready 22） |
| E1 | 工具合并决策 | `c3ed102` | 不合并 9 族 / 标注交人 3 族 / 合并 0 |
| E2 | data 整理方案 | `3d4dc61` | 目标结构 + 移动清单 + 引用影响 + 分阶段计划 |
| E3 | 文档导航更新 | `14df70c` | PM 报告 35 + 索引 12→13 |
| Z | 化债（外部漂移） | `b4ef2e9` | 吸收并行会话 `_arch_v20/*` + `615.md` |
| F1 | 收工门禁脚本 | `56b5e12` | run_615_gate.py（7 工具 + 卫生 + 回归） |
| F2 | 收工验收报告 | 本 commit | 本文件 |

> 共 **17** 个 commit（含化债 chore）；另 F2 本 commit。

---

## 二、实测数字

### 2.1 收工门禁（`run_615_gate.py` full）
| 项 | 结果 |
|---|---|
| 615 工具 `--check` | **7/7 exit 0** ✅ |
| ruff / mypy | exit 0 ✅ |
| **pytest_full**（`-m "not slow"`） | **exit 0**（305.4s）✅ |
| pytest_615 | exit 0 ✅ |
| 受控目录零污染 | ✅ 干净 |
| **门禁结论** | **PASS** |

### 2.2 人审诚实化（A1）
- 388 条 = **1 审阅者 × 5 理由模板**；`batch_authorization 388 / item_by_item 0 / mirror 194`；理由长度 min47/med67/max80。
- 30 条逐条复核清单：**17 modify（OUT7）+ 13 approve（rubber-stamp）**。

### 2.3 规则双实现（B1/B2）
- 适用卡 19；一致率 **68.4%（13/19）**；6 分歧卡吻合历史记录；
- 类型 A=1（剥 `artifact_sha256`）/ B=0 / C=0；提案后 **100%**。
- 保护集 **12 → 22**（+ ruler 10）。

### 2.4 warn 治理（C1-C3）
- 9 规则分类（observation2/considerable1/adopted4/expired2）；warn 趋势 31→136→186。
- 27 条 legacy 豁免全 **active**（到期 = 创建批次 + 10）。
- Goodhart 危险分 **80.1/100**（4 已知子项，coverage 未取到已排除）。

### 2.5 学习者镜像（D2/D3）
- 模拟 10 步轨迹 0.10→0.9702；推荐门槛/跃迁/论证联动全通过。
- 门状态 **closed**（triggered 0 / ready 5 / not_ready 22；真实事件 **0/50**）。

### 2.6 CI（D1）
- gate/quality 装 pyyaml ✅；pytest 装 pytest+xdist+pyyaml+hypothesis ✅；replay 增量 ✅。
- **614 未 push** ⇒ 无新 CI run；本报告为**配置确认**非实跑。

---

## 三、偏差表（任务书假设 vs 实测）

| # | 任务书 | 实测/处置 |
|---|---|---|
| 1 | 任务0 要跑监工门禁 4 类 | §五 禁止 ⇒ **未跑**，数字取 standing baseline/历史记录 |
| 2 | A2 "OUT 的 7 个 MIS 的攻击边（7 条）" | 实测**正向边 17 条**（全部入选）；镜像反向边排除（派生票无独立信息） |
| 3 | B1 与"最近一次监工验收记录"对比 | 官方 `--check` 不重跑；官方口径由**文档化预处理重建** + 历史记录（p03 .out）**交叉验证** |
| 4 | B2 类型 B 修正第二实现 | 实为 **A=1/B=0/C=0**；「修正」= 补上官方隐性预处理 ⇒ 100% |
| 5 | C1 "读 gate --check 输出 JSON" | 不重跑；用 `golden_state.json`（acceptance + warn_classify）+ `metrics.jsonl` 趋势 |
| 6 | C2 "从 poison_drill.py 读取豁免列表" | 只读 `poison_exemptions.yaml`（581 台账）+ golden 批次时间线 |
| 7 | E1 "可合并 25 个工具" | `_arch_v19` **未给该清单** ⇒ 以**真实工具族**（约 25 工具）为准并如实标注 |
| 8 | E2 移动文件 | **仅方案不移动**（v1-v5 被 4+ 工具/测试引用、v4 CRLF 假脏） |
| 9 | （计划外）治理漂移 | 并行会话新增 `_arch_v20/*` ⇒ **化债 chore** 吸收（`b4ef2e9`） |

---

## 四、交人项（需人审裁决）
1. **30 条逐条复核**是否执行（清单已就绪，须人判断 + 授权更新 annotations）。
2. **EV-MATRIX 规则定义补全提案**是否采纳（写入规则定义文档）。
3. **warn 不增锁机制**是否启用（改 `golden_lock` 流程需人审）。
4. **27 条豁免到期后**续期/修复/删除（需人审）。
5. 工具合并 **3 族** / data 整理 **方案** 是否执行（616 人审授权）。
6. **CI 四 job 实跑确认**（614 未 push；本机无 gh 通道）。

## 五、未做项（明确声明）
- 未跑监工门禁四类（§五）；未执行任何逐条复核（人审权）；未采纳 EV-MATRIX 提案（不改 evidence/）；
- 未启用 warn 不增锁（不改 golden_lock）；未删/改任何豁免；未执行任何工具合并/data 移动（仅决策/方案）；
- 未采集真实学习行为（门未开）；未 push；未 golden accept；未写 616 提示词；未动受控目录。

## 六、边界自证
- `git diff --quiet -- atoms/ evidence/ Examples/ Book/` ⇒ **干净**（exit 0）。
- 遗留（非 615 引入）：两条 CRLF 假脏（`_adv_v80/probes/p57.cpp`、`data/metrics_612.md` 时间戳）；
  `_arch_v19/_arch_v20` 为并行会话目录。

---

*HEAD：见 `git log --oneline -1`。报告由 615 批次生成；所有门禁数字可复算。*
