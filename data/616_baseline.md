# 616 开工基线台账（任务0 · 只读，不跑任何 --check）

> 时间：2026-09-21 ｜ 铁律：不跑监工门禁；数字取自基线文件 + 历史记录，可复算。

## 1. 统计偷看基线（P0 主题）
### 1.1 v7 当前口径
- 逃逸 **1 / 1406**（点估计 0.0711%）；`data/mutation/full_baseline_v7.json`。
- 固定样本 Clopper-Pearson：**单侧 95% 上界 0.3370%**；双侧 95% CI `[0.0018%, 0.3956%]`（`_arch_v20 p02` 复算）。

### 1.2 v1–v7 各版本（逃逸 / 可判分母 = blocked + escaped）
| 版本 | variants | blocked | escaped | n_a | 可判分母 | 逃逸率 | CP 单侧上界(95%) |
|---|---|---|---|---|---|---|---|
| v1 | 1188 | 729 | **227** | 232 | 956 | 23.74% | — |
| v2 | 1181 | 908 | 61 | 212 | 969 | 6.30% | — |
| v3 | 1183 | 959 | 38 | 186 | 997 | 3.81% | — |
| v4 | 1183 | 960 | 38 | 185 | 998 | 3.81% | — |
| v5 | 1568 | 1374 | 1 | 185 | 1375 | 0.0727% | — |
| v6 | 1593 | 1378 | 1 | 179 | 1379 | 0.0725% | — |
| v7 | 1593 | 1405 | 1 | 179 | 1406 | 0.0711% | **0.3370%** |

- **偷看次数（固定样本 CP 被复算）**：**≥ 7**（v1–v7 各基线的上界复算），另加成品报告
  （`escape_rate_trend`(610)、`escape_rate_honest_613`）⇒ 公开复算 ≈ **9 次**，每次都在"同一批累积数据"上重看。
- 虚报量化（`_arch_v20 p02` 探针）：真实 p=0.01、每 20 样本偷看 ⇒ 固定样本 CP 经验虚报 **13.80%**（名义 5%）；
  e-process **0.00%**（理论 ≤5%）。**anytime 上界 0.9062%（= 单侧 CP 的 2.69×）**。
- 样本代价：0 逃逸下达到 0.5% 上界，CP 需 n=**598**，anytime CS 需 n=**2127**（3.56×）。

### 1.3 warn / 豁免
- `golden_state.warn_findings = 186`（block 0）；legacy 豁免 **27** 条（`tools/poison_exemptions.yaml`，全 `redteam_seen: legacy`）。

## 2. EV-MATRIX 基线（B 主题）
- 615 B1：第二实现（natural）适用 **19** 卡、一致率 **68.4%（13/19）**；6 分歧卡：
  `EV-CONC-001` `EV-CONC-002` `EV-MEM-001` `EV-MEM-039` `EV-MEM-042` `EV-MEM-043`。
- 615 B2 提案的隐性预处理清单：**剥 `actual:` 段 + 剥 `artifact_sha256:` 行**
  （64 位 sha 的数字片段被「CI run 号」锚 `\d{10,}` 误收）。
- 补上后一致率 **100%**（`compare_aligned()`）。

## 3. warn 治理基线（C 主题）
- 五桶（615 `warn_governance`）：new 0 / observation 2 / considerable 1 / adopted_legacy 4 / expired_reassess 2。
- 27 条豁免：全 **active**（到期 = 创建批次 + 10；创建 2026-09-12）。
- Goodhart 危险分 **80.1 / 100**（4 已知子项；coverage 未取到已排除）。

## 4. 他验基线（D 主题）
- **验证者数量**：**1**（项目自身 `gate_engine.py`）——**无独立第三方验证者**。
- **独立第二实现**：仅 **1 条规则**（`ev_matrix_unbacked_v2.py` / 63 条）。
- **可验证性**：checksum 保护 **有**（`tool_integrity` 22 项：core5+test_config2+supply_chain5+**ruler10**）；
  **独立验证 无**（无 VSA 凭证、无透明日志、无第三方复核）。
- 第一原则单用户上限：生成者=判断者=同一主体 ⇒ 独立票结构性缺失（`_arch_v20` 他验三件套正是为此）。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
