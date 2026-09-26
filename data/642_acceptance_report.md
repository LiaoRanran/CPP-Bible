# 642 · 验收报告：保护器上岗 + UVK 纲领落地（先收尾 641，再开新建设）

> 生成 2026-09-26。所有数字**实测**，不抄历史快照。
> 任务书：`_auto/inbox/642.md`。证据文件见 §七。
> **本批未 push、未代签、未 golden accept、未开 delegation**（push 留交人）。

## 一、任务完成表

### 阶段 0 · 收尾 641

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| 0.1 | 修 1 个测试期望 | `tools/queyi_core_v10_641.py` selftest 投影名修复 | ✅ 复跑 641 五测试文件 **58 passed / 0 failed** |
| 0.2 | 回填 641 验收报告门禁/终验节 | `data/641_acceptance_report.md` §二.2 / §二.2b / §一 E2·E3 | ✅ 数字与终验一致 |
| 0.3 | 写 `_auto/outbox/641.md` + 更新 `_auto/status.json` | outbox + status | ✅ `last_completed_batch=641` |
| 0.4 | 统一 commit 641 全部工作 | 3 个 commit + 遗留 116 项入册 | ✅ 工作区 **CLEAN** |

### 阶段 A · 保护器从影子转真（灰度）

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| A1 | 冲突检测器灰度上岗 | `tools/conflict_detector_642.py` + 测试（8 例） | ✅ `--mode shadow\|flag`；**block 明确未实现（留 643）** |
| A2 | anti-windup 上岗 | `tools/anti_windup_642.py` + 测试（9 例） | ✅ 半饱和标记 / 预算冻结 / 老化升级 |
| A3 | blind_protocol 上岗 | `tools/blind_protocol_642.py` + 测试（8 例） | ✅ 新入队判决强制盲化；历史只标记不修改 |
| A4 | 校准追踪器上岗 | `tools/calibration_tracker_642.py` + 测试（8 例） | ✅ 错误率自动累积；初值为全库代理 |
| A5 | MDL 规则准入上岗 | `tools/mdl_gate_642.py` + 测试（8 例） | ✅ 六种结论；现有 67 条零改动 |
| A6 | 保护器联调 + 灰度报告 | `tools/protector_rollout_642.py` + 测试（7 例） | ✅ 零漂移 / 零改判 / 可回滚 |

### 阶段 B · UVK 纲领落地

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| B1 | UVK 设计纲领文档 | `docs/uvk_manifesto.md` | ✅ 五条纲领 + 独立性四级刻度 |
| B2 | 内核最小性审计 | `tools/kernel_minimality_audit_642.py` + 报告（7 例） | ✅ 五项判据；**未移代码** |
| B3 | fail-closed 全量审计 | `tools/fail_closed_audit_642.py` + 报告（7 例） | ✅ 两处已知点**可复现实测**；**未修复** |

### 阶段 C · 闭环扩大准备

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| C1 | auto_executor 白名单扩展评估 | `tools/auto_executor_whitelist_eval_642.py` + 报告（7 例） | ✅ 8 候选逐条风险/护栏/回滚；**未扩展** |
| C2 | 闭环校准度追踪 | `tools/loop_calibration_642.py` + 台账 + 报告（8 例） | ✅ 637→638→642 三点；门槛判定 |

### 阶段 D · 收工

| # | 任务 | 交付 | 状态 |
|---|---|---|---|
| D1 | `tools/run_642_gate.py` | 门禁脚本 + 测试（9 例） + `data/642_gate_result.md` | ✅ **PASS 8/8** |
| D2 | 全量 pytest 终验 | `data/642_pytest_final.txt` | ⏳ 见 §二.1 |
| D3 | 验收报告 + status + outbox | 本文件 + `_auto/status.json` + `_auto/outbox/642.md` | ✅ |

## 二、关键实测数字

### 1. D2 全量 pytest 终验（**0 失败**）

| 次 | 文件 | 结果 | 说明 |
|---|---|---|---|
| 第 1 次 | `data/642_pytest_run1_state_red.txt` | **1 failed / 3501 passed / 16 skipped** | 唯一红 = `tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete` |
| 第 2 次 | `data/642_pytest_final.txt` | **0 failed / 3502 passed / 16 skipped（exit=0，36:25）** | **权威终验** |

- 第 1 次唯一红的**根因**：该测试断言 `status["state"] == "awaiting_review"`，而本批**阶段 0 收尾 641**
  时按苦力协议把 `_auto/status.json` 置为 `state="running"`（**批内状态**）⇒ 断言在当时读到的状态上失败。
  **不是代码缺陷，也不是偶发**，是"批进行中"与"批已收尾"的状态口径冲突。
- **取证与验证**：把 `status.json` 更新为收工态（`state=awaiting_review`、`last_completed_batch=642`、
  `next_batch=643`）后**单跑该测试** ⇒ **4 passed / 1 skipped（绿）**；随后**全量复跑** ⇒ **0 failed**。
- **计数口径（诚实）**：终端末尾的汇总行（`N passed, M skipped in …`）**未被后台捕获**，
  文件止于 `snapshot report summary`；因此计数由 **pytest 进度行机械推导**
  （`_auto/_count_pytest.py`：`.`=passed / `s`=skipped / `F`=failed / `E`=error），
  **不是抄终端数字**。交叉验证：两次运行总数一致 = **3518**，
  而 641 终验总数为 3432（3415+1+16），差值 **86 = 本批新增测试数**（A48+B14+C15+D9）⇒ 计数自洽。
- 与 641 的对比：641 的 1 个红（内核 selftest 投影名）已在阶段 0 修复；**本批未引入新的红**。

### 2. 阶段 0：641 收尾（唯一失败的真因与修复）

`data/641_pytest_final.txt`：**1 failed / 3415 passed / 16 skipped**（35:38）。
唯一失败 = `test_queyi_core_v10_641.py::test_cli_check_passes` ⇒ `core.main(["--check"]) == 1`。

- **根因（非代码 bug）**：内核 selftest 用 `run.project("w2")` 断言「未注册投影抛 KeyError」，
  但 `w2` 投影会被 **C++ 领域适配器注册**，而 `_PROJECTORS` 是**进程级全局**。pytest 同进程内
  先跑 cpp 测试（注册 `w2`）再跑内核 selftest ⇒ `project("w2")` 成功 ⇒ 断言假失败。
  内核测试文件本身早已用 `_never_registered_projection_641` 规避，**selftest 漏了同一处理**。
- **修复**：`tools/queyi_core_v10_641.py` selftest 改用 `_never_registered_projection_641`。
  **只改断言用的投影名，未改任何生产逻辑**，fail-loud 语义原样保留。
- **验证**：修复后重跑 641 五个测试文件 ⇒ **58 passed / 0 failed**。

### 3. 阶段 A：五保护器灰度实测

| 保护器 | 实测 |
|---|---|
| A1 冲突检测 | verified 卡 **23**；标记（C ≥ θ=0.3）**2**；**判决被改变 0**（flag 契约机械核验通过） |
| A2 anti-windup | 队列 **65**；占用 **65.0%** ⇒ 半饱和；`queued_pending` **65/65**；冻结 **0**；升级 **0**；队列文件 sha256 前后一致 |
| A3 blind_protocol | 历史判决 **452**；AI 可见（违规）**258**，**账本 sha256 前后一致**（只标记不修改）；分歧率 **None**（无已揭盲条） |
| A4 校准追踪 | 规则 **67**；上线初值态：有自身样本 **0** / 用代理 **67**；代理 = ledger 改判率 **85/452 = 0.1881** |
| A5 MDL 准入 | 在册 **67**；热力图 **63**（不在热力图 **4**）；零触达 **33**；636 试运行复现 admit **30** / reject **37**（早期 66.7% → 近期 23.5%）；六种结论各 1 |
| A6 联调 | **漂移零**（5 个 CORE_TOOLS 字节 + 452 账本 + 权威日志 + 人审队列 + verified 卡清单指纹前后一致）；**生产判决被改变 0**；标记键 **15**，`rollback_marks()` 逐个回滚到底 ⇒ `{}` |

### 4. 阶段 B：UVK 纲领 + 两项审计

- **内核最小性（AST）**：内核 **813 行**、顶层符号 **47**；**领域 import 0** / **非标准库 import 0** /
  **高攻击面能力 0**；写盘面仅 `OUT_MD`/`OUT_JSON`；依赖方向双向核验（适配器 import 内核 ✅、
  内核 import 适配器 ❌）；**建议移出 4 项**（报告层 3 + 规则引擎归属复核 1），**未移代码**。
- **fail-closed 审计**：扫描 **452** 个 `tools/*.py` ⇒ 命中 **145** 条
  （FO-1 异常⇒通过 100 / FO-3 关键字段默认值 38 / FO-2 缺失⇒通过 4 / FO-4 警告不影响退出码 3）；
  **两处已知点可复现实测**：
  * **FO-A（中）**：`tool_integrity.verify_supply_chain()` 缺文件 **实测 `exit_code=0`**；
  * **FO-B（高）**：`DecisionEvent.from_dict({})` **实测** ⇒ `result='APPROVE'` +
    `review_method='BATCH_AUTH'` + `decision_origin='human_observed'`（最"信任假设"的默认），
    且未知键被**静默丢弃**。

### 5. 阶段 C：闭环与白名单

- **闭环校准度**：R1（637）**37.5%**（3/8）→ R2（638）**50.0%**（2/4，派生）→
  R3（642）**None**（候选 157 / 采纳 0 / 事后验证待人审）；
- **扩大门槛**：**60%**，最高观测 **50.0% ≤ 60%** ⇒ **未达 ⇒ 本批不扩大白名单**；
- **白名单评估**：8 候选 ⇒ **拒绝 3**（账本写入/改 gate 规则/改知识卡）、
  **技术可入选但本批不扩大 5**；
- **照出的口径差异**：inbox 把「测试断言数字更新 / 补 --check」算作现有白名单，但
  `auto_executor_640.WHITELIST` **实测不含**二者（以代码事实为准）。

### 6. D1 门禁

`data/642_gate_result.md`：**8/8 PASS** —— 10 个新工具 `--check` 全绿 / 641 收尾确认 /
ruff 全绿 / mypy **0 errors** / 受控目录零污染 / 保护器灰度验证 / 内核零领域 import（AST）/
`tool_integrity --check` 四项全 OK（CORE_TOOLS + 信任根 + Merkle + 尺子 22）。

## 三、范围与硬边界

- 5 个 **CORE_TOOLS 判决逻辑零改动**（`tool_integrity --check` 四项 OK 实测）；
- 受控目录（atoms/evidence/Examples/Book）**零污染**（门禁实测 `git diff --quiet`）；
- **不修改历史判决**：A3 扫描 452 条只标记，**账本 sha256 前后一致**（append-only 铁律）；
- **不修改现有 67 规则**：A5 只对新规则准入，侧车元数据只记新规则、**被拒规则不删除**；
- **不实际移代码 / 不扩白名单 / 不修 fail-open**：B2 / C1 / B3 只出报告（§七.5）；
- **灰度零副作用**：A1 flag 只加标记、A2 只标记不丢请求、A3 只盲化新项、A4 只记账、A5 只判新规则；
- **未 push**、未 golden accept、未开 delegation、**未代签**、未跑监工门禁。

## 四、新增资产

| 类型 | 文件 |
|---|---|
| 工具（11） | `conflict_detector_642`、`anti_windup_642`、`blind_protocol_642`、`calibration_tracker_642`、`mdl_gate_642`、`protector_rollout_642`、`kernel_minimality_audit_642`、`fail_closed_audit_642`、`auto_executor_whitelist_eval_642`、`loop_calibration_642`、`run_642_gate`（`tools/` 下，均带 `--check`） |
| 测试（12） | `tests/test_*_642.py`（合计 **86 例**：A 48 + B 14 + C 15 + D 9） |
| 文档（1） | `docs/uvk_manifesto.md`（UVK 设计纲领） |
| 报告 | `data/642_conflict_flag_run.md`、`642_anti_windup_rollout.md`、`642_blind_rollout.md`、`642_calibration_rollout.md`、`642_mdl_admission.md`、`642_protector_rollout.md`、`642_kernel_minimality_audit.md`、`642_fail_open_audit.md` + `.json`、`642_whitelist_expansion_eval.md`、`642_loop_calibration.md` + `.json`、`642_rule_admission.json`、`642_gate_result.md`、`642_pytest_final.txt`、`642_acceptance_report.md` |

## 五、诚实登记（防自欺）

1. **保护器上岗 ≠ 保护器有效**（§十.1）：flag/灰度只做标记，**不证明**"拦截后系统更安全"；
   有效性需 643+ 的真实运行数据（真实盲评、真实拦截）。
2. **A2/A3/A5 的"触发"多数是标记量**，不是被拦截量；A2 的**冻结清单与升级清单都是空的**
   （无「低」优先级项；最长等待代理 22.8 天 < 30 天），机制由**合成策略矩阵**验证，不是靠真实队列。
3. **A4 的 known_error_rate 初值是全库代理，不是精确值**（§十.2）：历史无规则归属字段
   （ledger 26 字段无 rule_id、`target_type` 452/452 全 `edge`）⇒ 67/67 `is_proxy=True`；
   **「未推翻」≠「没错」**。
4. **A5 可能误杀好规则**（§十.4）：编码长度/豁免率是**启发式**；4 条 HC 规则不在热力图，
   可能是**新方向**而非冗余；候选清单为**合成**（本批无真实新规则提案）。
5. **B2 的建议移出只有 4 项**，因为内核里**没有任何领域逻辑可移**（AST 机械证明），
   四项都是**层次性**改进（报告层剥离、规则引擎归属复核），**不是**领域污染清理；
   分类判据是**人工**的，四项机械判据（领域/非标准库/攻击面/写盘面）才是客观的。
6. **B3 只审计不修复**：`tool_integrity.py` / `decision_event_v2_626.py` **一字未改**
   （单测以 sha256 前后一致证明）；扫描是**高精度低召回**的启发式，漏判一定存在；
   145 条命中是**线索清单不是判决**，规则类严重度 ≠ 实例严重度。
7. **C1 的 score 公式可复算但未被验证过**（无历史事故数据校准）；真正的闸门是
   "能不能回滚"与"是否触碰判决面"。
8. **C2 的 R3 校准度是 None 而不是 0**（未代决）；R1/R2 **口径不同**且**样本极小**
   （8 与 4），**不足以判趋势**（§十.6）；R1/R2 审计人均为**执行该批的 AI（自审）**，
   含自评偏差，不是独立人审。
9. **照出两处口径错误并已修正/登记**：(a) 641 内核 selftest 的投影名（已修）；
   (b) 636 报告把「通过率」误题为「豁免率趋势」（642 已区分并在 A5 登记）；
   另：636 记「7 条不在热力图」，642 实测 **4 条**（以实测为准，差异原因未定位）。
10. **照出 inbox 口径 ≠ 代码事实**：C1 发现 inbox 描述的 auto_executor 白名单与
    `WHITELIST` 常量不一致；B3 发现 fail-open 两处；这些都以**代码事实**为准。
11. **UVK 纲领是设计原则，不是已实现能力清单**（§十.5）：`docs/uvk_manifesto.md` 里
    标 🟡/⛔ 的项（信任根独立 L1、真实盲评 L4、真实第二领域等）都是**缺口**；
    本批把盲评**工具化**了，但**没有**产生真实盲评数据 ⇒ L4 仍未达。
12. **全量 pytest 无偶发项**：本轮两次全量运行的差异**完全由 `status.json` 的批内状态解释**，
    没有出现无法定位的偶发红（与 640c 的 flake 不同）；第 1 次的红已按"**先取证、再改状态、再复跑**"
    处理，**未改任何测试断言**。
13. **后台捕获丢失 pytest 末尾汇总行**（观测）：`data/642_pytest_final.txt` 止于
    `snapshot report summary`，**没有** `N passed, M skipped in …` 行，也没有根级 `conftest.py`
    的会话收尾统计行。本批**用进度行机械推导计数**并做了总数交叉验证（§二.1），但该现象本身
    **未定位根因**（两处均在 `sessionfinish` 前后输出）⇒ 登记为观测 + 交人项，**不猜测**。
14. **`data/642_pytest_run1_state_red.txt` 是失败现场**（1 failed），与权威终验
    `data/642_pytest_final.txt`（0 failed）**并存**，不做替换 —— 保留"红→取证→绿"的完整链。

## 六、交人裁决项（机器不代决）

1. **是否 push**（641+642 全区间）及 push 后 CI 观察；
2. **保护器何时从 flag 转 block**（643？需人确认；A1 的 block 模式本批显式未实现）；
3. **anti-windup 周处理能力 20/周是假设值**，是否用真实数据校准；
4. **known_error_rate 初值是代理估算**，是否接受作为起点；
5. **fail-open 清单（B3）中哪些优先修** —— 建议顺序：FO-B（高，账本事件默认值）→
   FO-A（中，加严格模式开关）→ FO-3 38 条逐条复核；
6. **auto_executor 白名单扩展（C1）哪些类别可以安全加入**（本批建议：门槛达成后优先
   `report_regen`）；
7. **闭环校准度 > 60% 才扩大白名单**，这个门槛是否合适（当前最高 50.0%）；
8. **UVK 纲领是否认可为项目长期设计原则**；
9. `_arch_v2x/` 调研快照与 `data/vsa/` 运行时凭证的入库策略（本批已统一入册，是否改 gitignore）；
10. **B3 的 145 条扫描命中**是否需要逐条人核（或按文件分批）；
11. **pytest 末尾汇总行未被后台捕获**（§五.13）是否影响监工验收口径 —— 若监工依赖该行，
    需改用 `--junitxml` 或前台运行；本批以进度行机械推导 + 总数交叉验证替代。

## 七、证据文件

| 文件 | 内容 |
|---|---|
| `data/641_acceptance_report.md` | 641 验收报告（本批回填终验节 + 门禁节） |
| `data/641_pytest_final.txt` | 641 E2 原始全量终验（1 failed / 3415 passed / 16 skipped） |
| `data/642_conflict_flag_run.md` | A1 冲突标记清单 + 风险评估 + 回滚 |
| `data/642_anti_windup_rollout.md` | A2 队列状态 + 策略矩阵 + 冻结/升级清单 |
| `data/642_blind_rollout.md` | A3 盲化演示 + 452 条历史扫描（只标记） |
| `data/642_calibration_rollout.md` | A4 代理重建 + 67 规则初值 + ECE 格式 |
| `data/642_mdl_admission.md` / `.json` | A5 准入判据 + 六结论 + 侧车元数据 |
| `data/642_protector_rollout.md` | A6 五保护器联调 + 零漂移实证 + 回滚验证 |
| `docs/uvk_manifesto.md` | B1 UVK 设计纲领 |
| `data/642_kernel_minimality_audit.md` | B2 最小性审计（五方判据 + 建议移出） |
| `data/642_fail_open_audit.md` / `.json` | B3 fail-open 清单 + 两处已知点实测 |
| `data/642_whitelist_expansion_eval.md` | C1 白名单扩展评估（8 候选逐条） |
| `data/642_loop_calibration.md` / `.json` | C2 闭环校准度台账（append-only） |
| `data/642_gate_result.md` | D1 门禁 8/8 PASS |
| `data/642_pytest_final.txt` | D2 全量 pytest 终验（**0 failed / 3502 passed / 16 skipped**） |
| `data/642_pytest_run1_state_red.txt` | D2 第 1 次全量终验现场（1 failed = status 批内状态；保留红→绿完整链） |
