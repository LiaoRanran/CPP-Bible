# 647 回滚方案（阶段 0.2）

> 铁律（647 §零.6）：**回滚方案必须先写好再执行**。本文件在动任何硬骨头之前落盘。
> 每个任务三条：**改什么 / 怎么验证 / 怎么回滚**。回滚必须是**一条命令或一个 flag**，不靠回忆。

## 通用回滚层（所有任务共用）

| 层级 | 手段 | 适用 |
|---|---|---|
| L0 | **不 push**（ahead=88+，交人统一 push） | 全部——远程永不受影响 |
| L1 | `git revert <commit>`（一任务一 commit，message 写实） | 全部代码改动 |
| L2 | 保护器**全局 flag**：`QUEYI_PROTECTOR_MODE=shadow` | B1–B5 |
| L3 | 工具级兼容开关（`--warn-only` / `--lenient` / `--mode shadow`） | A1 / A2 / B1–B5 |
| L4 | `git checkout -- <file>`（未提交时）| 改到一半的工作区 |

---

## 阶段 A · 信任根独立

### A1 tool_integrity 缺失即 FAIL

- **改什么**：`tools/tool_integrity.py`（**CORE_TOOLS 邻居工具**，但**不是** CORE_TOOLS 判决逻辑本体；
  `tool_integrity.py` 在 `RULER_TOOLS` 里 ⇒ 改动后**必须** `--update` 重钉，属显式留痕）。
  新增 `--strict`（**默认开启**）/ `--warn-only`；`verify_supply_chain()` 缺信任根文件在 strict 下 ⇒ exit 1。
- **怎么验证**：`tests/test_tool_integrity_647.py`（缺文件必 FAIL / 齐全必 PASS / `--warn-only` 兼容 / 不影响 core 判定）。
  沙箱：在 tmp 复制 `.tool_checksums` 与信任根文件，删一个 ⇒ 断言 exit=1。
- **怎么回滚**：
  1. `git revert <A1 commit>`；或
  2. 运行期 `python tools/tool_integrity.py --check --warn-only`（**不改代码即回到旧口径**）；
  3. 若已重钉：`git checkout -- tools/.tool_checksums` 后重跑 `--update`。
- **注意**：改 `tool_integrity.py` 后 `.tool_checksums` 的 ruler 节会红 ⇒ **必须同 commit 重钉**，
  否则所有判定入口（gate_engine 等）`enforce()` fail-loud 拒绝运行。

### A2 DecisionEvent 严格模式

- **改什么**：`tools/decision_event_v2_626.py`：`from_dict()` 保持**兼容**（= lenient），
  新增 `from_dict_strict()`（缺字段/未知字段抛 `StrictEventError`）与 `from_dict_lenient()`。
  `decision_origin` 不再**默认** `human_observed`（strict 下必填）。
- **怎么验证**：`tests/test_decision_event_647.py`：缺字段抛错 / 未知字段抛错 / 历史 452 条 lenient 可导入（链仍有效）/
  新事件 strict 校验。
- **怎么回滚**：`git revert`；或调用方改用 `from_dict_lenient()`（**不改该文件**）。
- **不破坏历史**：历史 452 条**只用 lenient 导入**，账本文件**一字不改**（sha256 前后一致由门禁核验）。

### A3 信任根闭包扩展

- **改什么**：**新增** `tools/verifier_closure_647.py`（**不修改** `verifier_closure_641.py` ——
  640/642 起 `closure_digest` 已绑进 run，改它会使历史 run 的 digest 对不上，违反"不破坏历史"）。
  647 版闭包加入：5 CORE_TOOLS + **67 条规则**（gate_engine 内嵌规则 ⇒ 记 gate_engine 文件 sha256 +
  规则 id 清单指纹）+ Authority schema + 透明日志 anchor + `.tool_checksums` 基线 + 证据索引。
- **怎么验证**：`tests/test_verifier_closure_647.py`：闭包完整 / 缺文件必 FAIL / sha256 正确 / 与 tool_integrity 一致。
- **怎么回滚**：删除新文件（**零影响面** —— 641 闭包原样保留）。

### A4 外部锚接口

- **改什么**：**新增** `tools/external_anchor_647.py`：`publish(hash)->receipt` / `verify(hash,receipt)->bool` +
  本地 mock；GitHub Gist / 时间戳服务 / 区块链只留**接入点占位**（**不实现、不联网**）。
- **怎么验证**：`tests/test_external_anchor_647.py`：接口定义正确 / mock 可发布可验证 / 篡改检测 / 接入点清单齐。
- **怎么回滚**：删除新文件即回到"无外部锚"（**外部锚本就不是生产依赖**）。

### A5 信任根审计报告

- **改什么**：**新增** `tools/trust_root_audit_647.py` → `data/647_trust_root_report.md`。
- **怎么验证**：`tests/test_trust_root_audit_647.py`：审计项完整 / 风险如实 / 不夸大。
- **怎么回滚**：删除新文件 + 报告。

---

## 阶段 B · 保护器真上岗

**统一回滚设计（B5 全局 flag）**：

```
QUEYI_PROTECTOR_MODE = shadow | enforce     # 默认 enforce（647 上岗）；shadow = 一键回 642 灰度
```

`tools/protector_rollout_647.py` 提供 `mode()`（读环境变量）与 `--rollback`（打印/写回 shadow）。
每个保护器**每个拦截动作**都先判 `mode()`；shadow 下退化为 642 行为（只标记）。

| 任务 | 新增文件 | 上岗动作 | 回滚 |
|---|---|---|---|
| B1 冲突检测 | `tools/conflict_detector_647.py` | C ≥ **0.8** 且双方有证据 ⇒ **block**；0.5–0.8 ⇒ warn；<0.5 通过 | flag → shadow |
| B2 anti-windup | `tools/anti_windup_647.py` | 超预算（>20/周）⇒ **冻结**（不入队）；积压 >80% ⇒ 人审清理警报 | flag → shadow（不丢请求） |
| B3 blind_protocol | `tools/blind_protocol_647.py` | 新判决**强制盲化**（人审未完 ⇒ AI 推荐不可见） | flag → shadow |
| B4 校准追踪 | `tools/calibration_tracker_647.py` | 规则 error_rate >**20%** ⇒ 降级 warn；>**50%** ⇒ 暂停（需人审恢复） | flag → shadow |
| B5 MDL 准入 | `tools/mdl_gate_647.py` | 新规则**必须过 MDL** 才 `ADMIT`（否则不落规则库） | flag → shadow |

- **怎么验证**：`tests/test_*_647.py`（每工具 ≥6 例）。
- **通用回滚**：`set QUEYI_PROTECTOR_MODE=shadow`（**不改代码**）；或 `git revert` 该保护器 commit。
- **诚实登记**：首次全量上岗**可能出现误拦**；647 只对新判决生效，**历史不回溯**。

---

## 阶段 C · 仓库拆分（**最高风险**）

- **改什么**：C1 只在**临时目录克隆**验证（原仓库零改动）；C3 只在**沙箱克隆**里执行 `git subtree split`，
  产出**同级本地仓库** `queyi-core`（**不改 CPP-Bible 工作树**、**不 push**）。
- **怎么验证**：`data/647_split_sandbox_report.md`：拆分后仓库能独立运行、测试能跑、历史保留。
- **怎么回滚**：
  1. **CPP-Bible 侧零改动** ⇒ 无需回滚（这是本批的设计选择：拆分产物在仓库**外部**）；
  2. 若误改：`git reset --hard <拆分前 sha>`（拆分前 sha 记录在报告里）；
  3. 外部 `queyi-core` 目录：**直接删除目录**即可（未被任何东西引用）。
- **不做的部分（诚实）**：**不**把 `queyi-core` 以 `git subtree` 合并回 CPP-Bible 子目录 ——
  那会与 CPP-Bible 现有 `tools/*` 重复，直接冲击 645/646 测试套件（"拆分后测试红"的高风险路径）。
  该合并列为**交人裁决**。

---

## 阶段 D · 工具合并（15 → 10）

- **改什么**：按 646 B4 三组合并：成员功能**移入**代表模块（保留同名可调用入口，语义等价），
  删除被并文件，**同步更新 `tests/test_*_645.py` 的 import**。
- **怎么验证**：`pytest -k 645` + `pytest -k 646` 全绿；功能等价抽查。
- **怎么回滚**：`git revert <D1 commit>`（一 commit 完成全部合并 + 测试同步，便于整块回滚）；
  或 `git checkout -- tools/ tests/` 恢复工作区。
- **风险登记**：645 测试套件可能整体红 ⇒ **先跑基线快照**，合并后逐条比对，不允许"改到绿"。
- **铁律**：只动**测试 import** 与**工具文件组织**，**不动任何判决逻辑**。

---

## 阶段 E · 打靶准备（低风险）

- **改什么**：只**新增文档**：`docs/c_domain_adaptation_647.md`、`docs/embedded_adaptation_647.md`、
  `docs/targeting_plan_647.md`。
- **怎么回滚**：删除文档。**不实际建 C/嵌入式卡片**（留 648+）。

---

## 阶段 F · 收工

- **改什么**：新增 `tools/run_647_gate.py`、`status/647_acceptance_report.md`、`_auto/outbox/647.md`、
  更新 `_auto/status.json`。
- **怎么回滚**：`git revert` 收工 commit（**只影响报告/状态**，不影响代码）。
- **门禁失败处理**：**不回滚代码**，先定位根因；"改到绿"被铁律禁止（§零.7）。

---

## 回滚演练（本批要求）

- A1 / A2 / B1–B5：单测**必须各有一条"回滚/兼容模式仍通过"**的断言；
- B5：`--rollback` 打印 shadow 模式并断言保护器在 shadow 下**不拦截**（exit 0、零 block）；
- C1：沙箱失败时**不触碰原仓库**（脚本以 `tempfile.TemporaryDirectory()` 承载）。
