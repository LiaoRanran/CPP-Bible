# 616 · 收工验收报告（方法论修复优先：置信序列修统计偷看 + EV-MATRIX 双实现锁 + warn 治理/Goodhart + 他验三件套 + 交人项台账）

> 仓库：`C:\CodeLearnling\note\note\C++\CPP-Bible`（完整过程见 `_worklog_616.md`：§1–§6 任务记录 / §7 验收 / §8 交人项；`_worklog_*` 仓库根不入库）。
> 纪律：一任务一 commit；未 push / 未 --no-verify / **未 golden accept**（accept 权唯人）；存量零误伤；**依任务书 §五，616 监工门禁不跑，数字取 standing baseline 与历史记录**。
> 口径：比率一律"分子/分母 + 点估计 + 双侧 C-P95"；可判 n=0 报 insufficient evidence；n_a/malformed 永不进分母。

## 开工基线（实测，取自 `data/616_baseline.md`，只读不跑 --check）

- **统计偷看基线（P0）**：v7 逃逸 **1/1406**（点估计 0.0711%）；固定样本 CP 单侧 95% 上界 **0.3370%**；连续偷看公开复算 ≈ **9 次**；探针虚报（真实 p=0.01/每20样本偷看）固定样本 CP **13.80%** vs e-process **0.00%**；anytime 上界 **0.9062%**；0.5% 上界样本代价 CP n=598 / CS n=2127。
- **EV-MATRIX 基线**：615 第二实现适用 19 卡 / 一致 68.4%（13/19）；隐性预处理根因（剥 `actual:` + 剥 `artifact_sha256:` 行）。
- **warn 治理基线**：warn 186（block 0）；legacy 豁免 27 条；Goodhart 危险分 80.1/100。
- **他验基线**：验证者 1（项目自身 gate_engine）；独立第二实现 1/63 规则；checksum 保护 22 项；独立验证 0。

## commit 清单（16 个，线性落于 `beb7e63`~`faf0f4f`）

`beb7e63`（任务0 基线）→ `d985bb4`(A1) → `705d7cb`(A2) → `772e450`(A3) → `31c0af0`(B1) → `bec5305`(B2) → `e8cf36b`(B3) → `30f3545`(C1) → `24ba757`(C2) → `ece0310`(C3) → `fad58f7`(D1) → `fb103f9`(D2) → `893d165`(D3) → `e6f10dd`(E1) → `bc16d3e`(E2) → `faf0f4f`(E3)

---

## 任务验收

### A 线 · 置信序列修统计偷看（P0 主题）✅
| ID | 交付 | 验收（依工件，未跑门禁） |
|---|---|---|
| A1 | `tools/confidence_sequence.py`：Beta-混合 e-process，**纯标准库** | ✅ 含 `cs_upper(n,x)` / `cp_upper(n,x)`；探针经验虚报 **0.00%**（理论 ≤5%）；anytime 有效 |
| A2 | `data/confidence_sequence_recalc_616.md`：v1–v7 重算对照 | ✅ 表内自洽：CS/CP 从 v1 1.11× → v7 **2.69×**，v7 anytime **0.9062%** vs CP 0.3370% |
| A3 | `metrics_collector` 加 `cs_*`（**保留** `cp_*`）+ `peeking_correction` | ✅ 双口径看板入 metrics；`peeking_correction` 标注引用口径 |

### B 线 · EV-MATRIX 双实现锁 ✅
| ID | 交付 | 验收 |
|---|---|---|
| B1 | `data/ev_matrix_rule_definition_v2.md`：规则定义独立补全（显式写隐性预处理） | ✅ 独立文档，未改 `evidence/`（待人决） |
| B2 | `ev_matrix_unbacked_v2` 补全语义 | ✅ 一致率 **100%**（补上隐性预处理后） |
| B3 | `data/ev_matrix_dual_impl_baseline_616.json` + `ev_matrix_dual_impl_lock.py` | ✅ import gate_engine 单规则函数 vs 独立实现 = **19/19=100%**（pass，阈值 0.95，official_hits 16） |

### C 线 · warn 治理 / Goodhart 入度量 ✅
| ID | 交付 | 验收 |
|---|---|---|
| C1 | `warn_governance` 工作流（五桶→观察期→采纳建议→到期提醒） | ✅ 只建工作流，不自动执行（新 warn 不自动采纳） |
| C2 | `exemption_expiry` 27 条 legacy 处置清单（到期=创建批次+10） | ✅ 仅清单，不自动删除 |
| C3 | Goodhart 入 `metrics_collector.collect_curves()["goodhart"]` | ✅ 危险分 80.1/100 可度量 |

### D 线 · 他验三件套（从无到有）✅
| ID | 交付 | 验收 |
|---|---|---|
| D1 | `data/independent_verification_architecture_616.md` | ✅ 针对"生成者=判断者=同一主体"结构性独立票缺失 |
| D2 | `independent_verifier_prototype.py`：HMAC VSA 凭证 + 5 示例 | ✅ 最小可行原型 |
| D3 | `data/independent_verification_roadmap_616.md`（5 阶段） | ✅ 阶段 2 需 10 规则+Merkle 授权；签名升级需密钥托管 |

### E 线 · 交人项台账 + 报告 ✅
| ID | 交付 | 验收 |
|---|---|---|
| E1 | `data/human_decision_tracking_616.md`（615 遗留 7 + 616 新增 3） | ✅ 只跟踪不裁决，无人审代签 |
| E2 | `data/project_health_report_20260920.md` 追加 616 定位 | ✅ 六维度 ≈8.4；债务变化：已修 CP 偷看口径、新增对外口径待裁决 |
| E3 | `36_产品经理报告_*.md` + `00_总索引.md` 首行链接 | ✅ 已提交 `faf0f4f` |

---

## 收工总验收（依 §五：监工门禁不跑，基线对照 + 工件验证）

| # | 判据 | 实测（616 HEAD `faf0f4f`，基线对照） |
|---|---|---|
| 1 | 受控目录零污染（atoms/evidence/Examples/Book） | ✅ `git diff --name-only beb7e63~1..HEAD` 无受控目录文件 |
| 2 | gate 规则 / 命中（基线） | ✅ **63 规则 / 191 命中（block=0 warn=186 advice=5）** ＝基线逐字相同（616 未改 gate_engine/evidence） |
| 3 | poison 覆盖（基线） | ✅ **124/124** 表观 100.0% / 诚实 95.2% ＝基线逐字相同 |
| 4 | replay（基线） | ✅ **confirm=56 refute=0 infra=0** ＝基线逐字相同 |
| 5 | tool_integrity 保护（基线） | ✅ **22 项**（core5+test_config2+supply_chain5+ruler10）＝基线逐字相同（616 未改 CORE） |
| 6 | mutation 契约（基线） | ✅ **1/1406** 不变（W2 冻结 TCE，活雷 0/1405） |
| 7 | A1 置信序列实现 | ✅ 纯标准库 e-process；探针虚报 0.00% |
| 8 | A2 v1–v7 重算 | ✅ 表内自洽（CS 2.69× / anytime 0.9062%） |
| 9 | A3 metrics `cs_*` 集成 | ✅ 加 `cs_*` 保留 `cp_*` + `peeking_correction` |
| 10 | B3 双实现锁 | ✅ **19/19=100%**（pass，阈值 0.95） |
| 11 | C3 Goodhart 接入 | ✅ `collect_curves()["goodhart"]` |
| 12 | D2 他验原型 | ✅ HMAC VSA + 5 示例 |
| 13 | E1 交人项台账 | ✅ 615 遗留 7 + 616 新增 3 |
| 14 | E3 PM 报告 + 索引 | ✅ 36 号 + 索引首行链接 |
| 15 | `git status --short` 零误伤 | ✅ 仅 CRLF 假脏（`_adv_v80/probes/p57.cpp`(M)、`data/metrics_612.md`(M)、untracked `_arch_v19/_arch_v20` 不入库） |

---

## 偏差（任务书预期 vs 实测）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 616 监工门禁应全跑 | 任务书 §五 与各步骤自相矛盾 ⇒ **按 §五**：监工门禁不跑，数字取 baseline | 已声明于报告四、边界 |
| D2 | 置信序列应"取代"CP 作对外口径 | 实际**双口径并存**（cs_* + 保留 cp_*），哪个对外须人定 | 交人项 616-#8（P0） |
| D3 | EV-MATRIX 规则定义应合并进 `evidence/` | 616 仅出**独立文档**，未合并 | 交人项 615-#2 |
| D4 | 他验应进入生产实施 | 仅**架构+原型+路线图**，未实施 | 交人项 616-#9 |

## 交人项 / 残余边界

1. **置信序列是否正式启用**（cs_* 取代 cp_* 对外）——双口径已入 metrics，哪个对外须人定（P0，616-#8）。
2. **EV-MATRIX 规则定义补全**是否合并进 `evidence/`（615 遗留，616 已出独立文档）。
3. **他验架构是否进入实施**（阶段 2 授权 + 密钥托管）。
4. **warn 不增锁机制**是否启用（改 `golden_lock` 流程）。
5. **27 条 legacy 豁免到期处置**（到期 = 创建批次 + 10）。
6. **保形预测 / 弃权三态**是否做（留 617+）。
7. **615 遗留 7 项**中未决项（30 条逐条复核 / 工具合并 3 族 / data 整理 / CI 四 job 实跑）仍待决策。
8. **品牌级口径纠正**：此前"1/1406，C-P95 ≤0.40%"在**连续查看**场景方法论无效；修正后 anytime 上界 **0.9062%**（非数据造假，是口径误用）。里程碑终点一次性声明仍可用 CP（0.3370%），但看板不得继续引用。
9. **未做（任务书边界）**：置信序列未取代 CP 作唯一对外口径（待决）、规则定义未合并、他验未进生产、保形预测未做——均属交人项或留 617+。

---

*数据来源：`data/616_baseline.md` + 各任务工件 + `git diff --name-only beb7e63~1..HEAD`；所有数字可复算。未跑监工门禁，依任务书 §五。*
