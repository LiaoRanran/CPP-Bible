# 647 验收报告 · 硬骨头批次（信任根独立 + 保护器真上岗 + 仓库拆分 + 工具合并 + 打靶准备）

> 任务书：`_auto/inbox/647.md`。完成报告：`_auto/outbox/647.md`。状态：`_auto/status.json`。
> 开工基线：`data/647_baseline.md`（HEAD `f36b59c8`，ahead=88）；回滚方案：`data/647_rollback_plan.md`（**先写后做**）。
> **本轮不 push、不代签、不 golden accept、未改现有 67 规则、未改历史账本、受控目录零污染。**

## 一、完成总览（对照 647 §三–§八）

| 阶段 | 任务 | 交付 | 状态 |
|---|---|---|---|
| 0.1 | 开工快照 | `data/647_baseline.md` | ✅ |
| 0.2 | 回滚方案（先写） | `data/647_rollback_plan.md` | ✅ |
| A1 | tool_integrity 缺信任根文件 ⇒ **FAIL** | 改 `tools/tool_integrity.py` + 8 例单测 | ✅ |
| A2 | DecisionEvent **strict/lenient 双入口** | 改 `tools/decision_event_v2_626.py` + 19 例单测 | ✅ |
| A3 | 信任根闭包扩展（23 → 33 条目，含 67 规则指纹） | `tools/verifier_closure_647.py` + 9 例单测 | ✅ |
| A4 | 外部锚接口（mock + 3 预留接入点，**不真连**） | `tools/external_anchor_647.py` + 12 例单测 | ✅ |
| A5 | 信任根独立审计（**不夸大**） | `tools/trust_root_audit_647.py` + 8 例单测 | ✅ |
| B1 | 冲突检测器**真上岗**（高置信 block） | `tools/conflict_detector_647.py` + 8 例单测 | ✅ |
| B2 | anti-windup **真上岗**（超预算冻结不入队） | `tools/anti_windup_647.py` + 7 例单测 | ✅ |
| B3 | blind_protocol **真上岗**（新判决强制盲化） | `tools/blind_protocol_647.py` + 8 例单测 | ✅ |
| B4 | 校准追踪器**真上岗**（超阈降级/暂停） | `tools/calibration_tracker_647.py` + 8 例单测 | ✅ |
| B5 | MDL 准入**真上岗** + 五保护器联调 | `tools/mdl_gate_647.py` + `protector_rollout_647.py` + `protector_mode_647.py`（全局开关）+ 22 例单测 | ✅ |
| C1 | 仓库拆分**沙箱验证** | `tools/repo_split_sandbox_647.py` + 7 例单测 | ✅ |
| C2 | 拆分方案最终确认 | `docs/repo_split_final_plan_647.md` | ✅ |
| C3 | **执行**拆分（仓库外本地仓库） | `C:/CodeLearnling/note/note/queyi-core` + `data/647_split_execute.json` | ✅（见 §三.3） |
| C4 | 清理 + 迁移文档 | `docs/migration_647.md` + queyi-core `README.md` | ✅（"清理"部分**未做**，见 §三.3） |
| D1 | 执行 646 B4 合并方案 **15 → 10** | 三组合并 + 同步改测试 | ✅ |
| D2 | 合并后接口统一验证 | `tools/interface_verify_647.py` + `data/647_merge_report.md` | ✅ **10/10 合规** |
| D3 | 死代码清理 | `tools/dead_code_cleanup_647.py` + `data/647_deadcode_report.md` | ✅（清 15 行；剩余 0） |
| E1 | C 语言适配调研 | `docs/c_domain_adaptation_647.md` | ✅ |
| E2 | 嵌入式适配调研 | `docs/embedded_adaptation_647.md` | ✅ |
| E3 | 648+ 打靶计划 | `docs/targeting_plan_647.md` + `tools/targeting_prep_647.py` + 5 例单测 | ✅ |
| F1 | 收工门禁 | `tools/run_647_gate.py` | ✅ **PASS** |
| F2 | 两阶段 pytest 终验 | `data/647_pytest_fast.txt` / `data/647_pytest_slow.txt` | ⚠️ **见 §三.1（不是全绿，但有基线对照证明非 647 引入）** |
| F3 | 验收报告 + status + outbox | 本文件 + `_auto/status.json` + `_auto/outbox/647.md` | ✅ |

**规模**：新增 **14 个 647 工具** + 1 门禁；**647 测试 133 例**（17 个测试文件）；**16 个 647 commit**（ahead 88 → **104**）。

## 二、关键实测（数字真实、可复算）

### 2.1 阶段 A · 信任根（最硬的骨头）

| 项 | 642 审计时 | 647 之后（实测） |
|---|---|---|
| 信任根文件缺失 | 只 warning，**exit 0**（FO-A） | **strict 默认 exit 1**（沙箱删文件实测）；`--warn-only` 可回退 |
| 不完整事件 | `from_dict({})` ⇒ APPROVE + human_observed（FO-B） | `from_dict_strict()` **三类全拒**（空 dict / 缺字段 / 未知字段），历史 452 条 lenient 仍可导入（链有效） |
| 闭包覆盖 | 23 文件（641） | **33 条目**（含 **67 规则指纹** / Authority schema / 透明日志 / 证据索引 / 基线自身），**与 tool_integrity 逐字一致** |
| 外部锚 | 不存在 | 接口就绪（`publish`/`verify` + 本地 mock 往返可验、篡改可检出），**真连外部服务 = False** |

- **沙箱实测（不碰真实仓库）**：删 `tools/poison_exemptions.yaml` ⇒ strict=1 / lenient=0，且真实文件仍在（`A5` 审计复算）。
- **A1 是 CORE_TOOLS 邻居的例外修改**：`tool_integrity.py` 在 `RULER_TOOLS` 里 ⇒ 改动后**同 commit 重钉** `.tool_checksums`（门禁核验 `--check` 四项全绿）。

### 2.2 阶段 B · 保护器真上岗（enforce）

| 保护器 | 强制动作（enforce） | 真实数据上的强制量 |
|---|---|---|
| B1 冲突检测 | C≥0.8 且双方有证据 ⇒ **判决态改判 `fail`** | ⚠️ **真实卡拦下 1 张**：`ATOM-MEM-PERF-003`（C=1.333，RR+EE）；另 1 张落 warn |
| B2 anti-windup | 超预算（>20/周）⇒ **冻结 = 不入队**；占用 >80% ⇒ 喊人清理 | 真实队列 65 项：冻结 **0**（无「低」优先级项）；积压警报 False |
| B3 blind_protocol | **所有新判决强制 ITEM_BLIND**；未揭盲读 AI 推荐 ⇒ `BlindViolation` | 新判决 3/3 全盲化；历史 452 条 **只标记**（258 违规，账本 sha256 不变） |
| B4 校准追踪 | error_rate >20% 降级 warn / >50% **暂停规则**（恢复需人审） | 67 规则**首次有逐规则实测样本**（646 A5 注释 × 账本 result）；真实数据**触发 0**（最高 ≈0.202，略高于阈值——见 §三.6） |
| B5 MDL 准入 | 不过 MDL ⇒ **不予上线** | 6 个**合成**候选：放行 1 / 拒 5（**无真实提案**） |

- **一键回滚（实测）**：`QUEYI_PROTECTOR_MODE=shadow` ⇒ B1 改判 0 / B2 冻结 0 / B3 强制盲化 0 / B4 降级+暂停 0 / B5 不放行 0，**且 `rollback_and_verify()` 不写盘**。
- **零漂移**：5 CORE_TOOLS 字节 + 452 账本 + 权威日志 + 人审队列 + 透明日志 + verified 卡清单，联调前后**逐项相同**。
- **不重复拦截**：五保护器**键空间互不重叠**（17 键）+ **对象层两两不同**（卡判决 / 队列项 / 人审条目 / 规则 / 规则候选）。

### 2.3 阶段 C · 仓库拆分

- **机制修正（重要）**：645 调研写的是 `git subtree split`，实测它**只能按一个 prefix 拆**，而 core 文件分散在 `tools/` 多处 ⇒ 改用 **`git fast-export --all -- <paths> | git fast-import`**（单趟、保历史、路径清单可审计）。
- **沙箱实测四个坑（都是真的）**：① tag 指向未导出对象 ⇒ `--tag-of-filtered-object=drop`；② 历史含 `encoding gbk` 提交 ⇒ `--reencode=yes`；③ `conftest.py`/`pyproject.toml` 强耦合整仓 ⇒ **不迁移**，queyi-core 自带最小 conftest；④ 只写种子模式会漏掉保护器**前身模块**（642/636）⇒ 清单改为 **种子 ∪ repo 内 import 传递闭包**。
- **沙箱结果**：core **116 文件** / 拆分仓库 **164 提交** / 内核 selftest **PASS** / `pytest --collect-only` **215 例 0 错误** / 历史保留（探针文件两侧提交数相同）。
- **执行结果**：`queyi-core` 建在**仓库外**（`C:/CodeLearnling/note/note/queyi-core`），**166 提交 / 121 tracked 文件 / 无远端 / 未 push**；`pytest -k 647` 实跑 **82 passed / 30 failed**（失败全是"有意不拆的数据"缺失）。**CPP-Bible 工作树零改动**。

### 2.4 阶段 D · 工具合并与清理

- **15 → 10**：三组合并（三层耦合套件 / 证据判定套件 / 规则生命周期套件），成员代码**原样搬入**、冲突符号**重命名**（`write_effect_report` 等）⇒ **功能等价、单测逐条复用**。
- **接口验证 10/10 合规**（docstring + `main` + `selftest` + `--check` 标志 + **真跑 `--check` 返回 0**）。
- **死代码**：D1 期间 `ruff --fix` 清 **15 行**（未用/重复 import）；复检 **剩余 0**；死函数候选**只报不删**。
- **全局静态收尾**（顺带修了 5 处**存量**静态债，见 §三.4）：`ruff check tools/ tests/` → **All checks passed**；`mypy tools/` → **Success: 0/534**。

### 2.5 阶段 E · 打靶准备（**只调研**）

- 三份文档齐备（`targeting_prep_647` 机检：章节完整 + 声明不越界 + 工作量含"人日"）。
- **关键结论**：67 条规则**没有一条是 C++ 语法专用**（审的是"卡+证据"）⇒ C 适配的主战场在 **Domain Pack + 卡片 + 证据源**，不在规则；
- **嵌入式最大硬约束**：**"能编译" ≠ "对"** —— L0（真机实测）在本环境**不可得** ⇒ 建议证据分级**扩一档 L0**（648+ 需先定获取方式）。

## 三、诚实登记（防自欺）

1. **F2 两阶段 pytest **不是全绿**，且有证据表明**不是 647 引入**：
   - **fast**：9 失败（133 例 647 子集全绿）；**slow**：16 失败。
   - **证据（方法）**：用 `git worktree` 检出**开工前**的 `f36b59c8` 跑同一批测试做基线对照 ⇒
     其中 **6 个是基线就红**（`grounded_audit_596` / `mypy_fix_625`×2 / `quality_gate_613` / `debt_replay_628`×2）；
     **5 个由环境里的陈旧锁文件 `data/.622_apply.lock` 引起**（实测：把该文件临时移开后 **30 passed**，随后已原样还原）；
     **1 个是 xdist 并行假失败**（`coverage_gap_631::test_readonly_and_report`，串行跑绿）。
   - 另有 `debt_replay_628` 依赖**构建产物** `build/replay_manifest.json`（gitignored，当前 2 条而测试要 56 条）。
   - **647 引入的失败 = 0**（对照后逐条归因）。
   - **注**：`-q` 的末尾汇总行在本环境未被捕获（642 已登记同类观测项）⇒ 计数以 **FAILED 行数 + `--collect-only` 交叉**为准。

2. **A1 保留了一个后门**：`--warn-only` 可退回 601 宽容口径（迁移期/仓库副本用）。默认是 strict，但"失败路径可被一个 flag 关掉"仍是兼容性代价。
   **口径选择说明**：函数级 `verify_supply_chain()` 形参默认仍是 `lenient`（601 的历史调用方与 601 测试依赖它）；**strict 是 CLI 默认**，判据取「**基准声明它应该在 ⇒ 它就必须在**」，而不是「`SUPPLY_CHAIN_FILES` 列的都必须存在」（后者会把"尚未产出的任务1/2 产物"和副本一并判红，与 601 的设计理由冲突）。

3. **C3/C4 有两处"没做"（有意）**：
   - **未把 queyi-core 用 `git subtree` 合并回 CPP-Bible 子目录** —— 会与现有 `tools/*` **重复**，直接冲击 645/646 测试；列为**交人裁决**；
   - **未在 CPP-Bible 清理重复的 core 工具**（当前两份并列）。⇒ "CPP-Bible 功能等价"因此是**平凡的**（工作树零改动）。

4. **D1 改了两个 646 工具与其单测**（`tool_consolidation_646` / `docstring_quality_646`），把它们改成**感知合并后状态**（现存 10 / 缺失成员自动跳过并登记 `skipped_missing`）。依据是 **646 自己写的**「执行合并需同步改测试」。此外 647 顺带修了 **5 处存量静态债**（`run_645_gate.py` 的 `l`/分号、`run_646_gate.py` 的 4 处 mypy 标注、2 个 644 测试的 `l`、ruff 排序）——都是**真实缺陷的正式修法**，不是"改到绿"。

5. **B1 是五保护器里唯一直接改判决态的**（→ `fail`），且**实测真实卡上就拦了 1 张**（`ATOM-MEM-PERF-003`，C=1.333，型 RR+EE）。**EE 型由「≥2 条引用且有悬挂」推出 ⇒ 可能是假悬挂**（证据 id 与文件名口径不一致）——本批**未**逐一核实该卡是否真悬挂引用。**这是本批最大的风险点**，回滚一条命令（`QUEYI_PROTECTOR_MODE=shadow`）。

6. **B4 的"降级/暂停"在真实数据上触发 0**：逐规则实测 error_rate 最高 **≈0.202**（略高于 0.20 的降级线）——由于 646 注释把**每条规则**都映射到 452 条事件（口径饱和，646 已登记），规则级 error_rate 几乎都≈全库改判率 0.1881 ⇒ **区分度有限**，两条阈值靠**合成数据**验证。**不夸大为"已生效"**。

7. **B2/B3/B5 的真实强制量多为 0 或合成**：B2 队列无「低」优先级项 ⇒ 冻结 0；B3 历史只标记（**不回溯**）；B5 候选是**合成**（本批无真实提案）。

8. **A4 对独立性零贡献**：外部锚是**本地 mock**（同机同仓库）⇒ 独立性**仍是 L2**，L3 未达（A5 审计如实登记 6 处共置点）。

9. **E 线只是调研**：**不建任何 C/嵌入式卡片、不写规则、不改代码**；工作量是估计值；两个最大未决点（标准源授权 / 嵌入式 L0 环境）需**人**解决。

10. **环境遗留未清理（本批不动）**：`data/.622_apply.lock`（陈旧锁）、`build/replay_manifest.json`（2 条）、`data/629..631_baseline*` 等既有脏项、`tools/queyi_data_models_645.py`（开工前即脏）——按 646 的口径「非本批产生，本批不动」。

## 四、硬边界遵守（对照 647 §零）

| 铁律 | 结果 |
|---|---|
| 5 个 CORE_TOOLS 判决逻辑零改动 | ✅（五个文件的 sha256 与基线一致，门禁核验）；**A1 例外已显式登记**（改的是 `tool_integrity.py`，并同 commit 重钉） |
| 受控目录零污染 | ✅ `git status -- atoms evidence Examples Book` 为空 |
| 不代签 / 不 golden accept | ✅ |
| 每个工具 `--check` 只读幂等 + 单测 | ✅ 14 个 647 工具 `--check` 全绿；133 例 647 测试 |
| 高风险先沙箱 | ✅ 仓库拆分（临时目录）、保护器（合成输入+零漂移）、信任根（tmp 沙箱删除） |
| 回滚方案先写 | ✅ `data/647_rollback_plan.md` 在动手前落盘 |
| 找不到根因如实登记 | ✅ 见 §三.1（未能让环境全绿，逐条归因并给对照实验） |
| 全程中文 | ✅ |
| push 留交人 | ✅ **未 push**（ahead 88 → 104） |

## 五、交人裁决项（对照 647 §十一）

1. **是否 push**（ahead=104，区间 `f36b59c8..HEAD`，16 个 647 commit + 历史积压）；
2. **`queyi-core` 是否建远端 / push**（当前**本地仓库、无远端**）；
3. **是否把 `queyi-core` 用 `git subtree` 合并回 CPP-Bible 子目录**（当前**未做**，理由见 §三.3）；
4. **`ATOM-MEM-PERF-003` 被 B1 拦下是否合理**（EE 型可能是假悬挂 ⇒ 若判定为误拦，`QUEYI_PROTECTOR_MODE=shadow` 回滚）；
5. **B1 的 θ=0.8/0.5、B2 的 20/周、B4 的 0.20/0.50** 是否用真实样本回填；
6. **外部锚选哪个服务**（GitHub Gist / RFC3161 / OpenTimestamps —— A4 只建接口）；
7. **A5 账本规则字段是否写入正式 schema**（646 是注释文件）；
8. **环境两件套是否清理**：陈旧锁 `data/.622_apply.lock`（清掉可让 5 个测试转绿）+ 重建 `build/replay_manifest.json`（56 条）；
9. **648 重点**：打靶 C 语言 / 打靶嵌入式 / 继续信任根深化 / 真实用户测试（647 已给三份调研 + 路线图）；
10. **保护器上岗后若出现误拦，是否立即回滚**（建议是：`QUEYI_PROTECTOR_MODE=shadow`，一条命令）。

## 六、产物清单

- **工具 14**（`tools/*_647.py`：mode / conflict / anti_windup / blind / calibration / mdl / rollout / verifier_closure / external_anchor / trust_root_audit / repo_split_sandbox / interface_verify / dead_code_cleanup / targeting_prep）+ 门禁 `run_647_gate.py`；
- **测试**：17 个 `tests/*_647*.py`（**133 例**）+ 1 个 slow 端到端；
- **报告**：`data/647_*`（基线 / 回滚方案 / 闭包 / 外部锚 / 信任根审计 / 五保护器上岗 ×5 / 联调 / 拆分沙箱 / 拆分执行 / 合并 / 死代码 / 打靶校验 / 两阶段 pytest 存档 / 门禁结果）；
- **文档**：`docs/repo_split_final_plan_647.md` · `docs/migration_647.md` · `docs/c_domain_adaptation_647.md` · `docs/embedded_adaptation_647.md` · `docs/targeting_plan_647.md`；
- **拆出仓库**：`C:/CodeLearnling/note/note/queyi-core`（166 提交 / 121 文件 / 无远端）；
- **状态/交接**：本文件 + `_auto/status.json` + `_auto/outbox/647.md`。
