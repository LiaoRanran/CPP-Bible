---
id: 490
title: 知识冲突与版本管理详细方案 claim版本 工件绑定 冲突检测 状态扩展 文档生命周期
status: active
type: architecture-note
created_at: 2026-09-14
---
# 490 知识冲突与版本管理详细方案
## claim 版本 + 工件绑定 + 冲突检测 + 原子状态扩展 + 文档生命周期

> 生成时间：2026-09-14
> 前置实测：contradicts/conflicts 关系使用 = 0（415 加了类型但没人用）；原子 status 有 5 种格式不统一；superseded/retracted 状态 = 0 颗；架构文档 225 份且编号冲突（484/485 各有两份）
> 核心问题：知识会变，但系统没有处理知识变更的机制

---

## 一、现状与问题

### 1.1 知识冲突

- 415 批次加了 `contradicts`/`conflicts_with` 关系类型和 `ATOM-REL-CONFLICT` 规则
- **但 28 颗原子中 0 颗使用这些关系**——知识冲突检测形同虚设
- 如果两颗原子的 claim 矛盾，系统不会自动发现

### 1.2 版本管理

- 原子的 claim 可以被新证据推翻，但没有 `retracted` 状态（只有 draft/verified）
- 证据卡有修订记录，但没有版本号（哪版断言对应哪版工件）
- 夹具改了，工件重生成了，但旧的证据卡可能还引用旧工件
- **工件-卡不同代**是反复出现的问题（ALLOC-002、G2 缺陷 1、EV-MEM-017）

### 1.3 状态混乱

实测原子 status 有 5 种格式：
```
status: verified               # 唯人可置 verified（S1 三权分立）
status: verified
status: verified               # 人审通过（2026-09-11，监工验收放行）
status: verified                  # 人审通过（2026-09-12）
status: red-team-verified
status: draft
```

- 注释格式不统一（有的有注释，有的没有）
- `red-team-verified` 不是 G6 定义的标准状态
- 没有 `superseded`（被取代）和 `retracted`（被推翻）状态

### 1.4 文档爆炸

- 架构文档 225 份（不是 100+，是 225！）
- **编号冲突**：484 有两份（成本经济学 + 两个用户直接痛点），485 有两份（系统自进化 + 可观测性）
- 没有文档生命周期管理（哪些是最新的？哪些过时了？哪些被取代了？）
- README_INDEX.md 有索引，但没有状态标记

---

## 二、claim 版本管理

### 2.1 问题

claim 改了之后，旧版本就丢了。不知道"这颗原子的 claim 经历了几次修改、每次改了什么、为什么改"。

ALLOC-002 的 claim 从"pool 32B 最省"改成"元数据开销与单块释放绑定"——这是方向反转，但如果没有版本记录，后人不知道曾经有过这个反转。

### 2.2 改法

原子 frontmatter 加 `claim_history`：

```yaml
claim: >-
  元数据开销与是否支持单块释放绑定：arena 用放弃单块释放换零 bookkeeping < bitmap < pool
claim_history:
  - version: 1
    date: 2026-09-10
    claim: "pool 元数据 32B 最省"
    reason: "初始版本"
  - version: 2
    date: 2026-09-11
    claim: "元数据开销与是否支持单块释放绑定..."
    reason: "红队发现口径不统一，pool 实际 8056B，方向反转"
```

### 2.3 规则

- `ATOM-CLAIM-HISTORY`：claim 修改必须记录到 claim_history（不能静默改）
- `ATOM-CLAIM-VERSION`：当前 claim 必须有 version 号
- 修改 claim 时，自动把旧版本追加到 claim_history

---

## 三、工件-卡版本绑定

### 3.1 问题

反复出现的 bug：夹具改了 → 工件重生成了 → 但证据卡的 artifact_sha256 没更新 → 卡和工件不同代。

ALLOC-002、G2 缺陷 1、EV-MEM-017 都是这个问题。

### 3.2 改法：工件版本链

证据卡加 `artifact_version` 字段：

```yaml
artifact: Examples/atoms/_atom_alloc_arena.asm
artifact_sha256: 4f482fdc...
artifact_version: 3          # 第几次重生成
artifact_generated_at: 2026-09-11
artifact_command: "g++ -O2 -S -o ..."
```

工件文件本身加头部注释（.asm 的前几行）：
```asm
; artifact_version: 3
; generated_at: 2026-09-11
; generated_by: atom_evidence_replay.py v7.0
; command: g++ -O2 -S -o ...
```

### 3.3 验证规则

- `EV-ARTIFACT-VERSION-MATCH`：卡的 artifact_version 必须等于工件头部的 artifact_version
- `EV-ARTIFACT-NOT-STALE`：卡的 artifact_sha256 必须等于当前工件的 sha256
- 不一致 → block（不是 warn，这是阻断级问题）

### 3.4 工具：artifact_version.py（约 80 行）

- 重生成工件时自动递增 version
- 检查卡和工件的版本是否匹配
- 批量修复不同代的卡

---

## 四、知识冲突检测

### 4.1 问题

415 加了 `contradicts` 关系，但 0 颗原子使用。原因：
- Writer 不知道该声明 contradicts
- 没有自动检测"两颗原子 claim 矛盾"的机制

### 4.2 改法：两层检测

#### L1 机械检测（已有，415）

- 显式声明 `contradicts` 关系 → 检查是否形成矛盾环
- A 依赖 B 且 B contradicts A → block

#### L2 语义检测（新增，辅助）

不能自动判断 claim 语义矛盾（需要 LLM），但可以：
- 同域、同主题的原子，claim 关键词相反 → warn（提示人检查）
- 例如：ATOM-MEM-001 说"X 是安全的"，ATOM-MEM-002 说"X 是不安全的" → warn

`tools/claim_conflict_scan.py`（约 100 行）：
- 扫描同域原子的 claim
- 提取关键词和否定词
- 发现潜在矛盾 → 输出候选，人审核
- 不自动 block（语义检测可能误报）

### 4.3 冲突解决流程

1. 检测到潜在冲突 → warn
2. 人审核 → 确认是冲突 → 标记 `contradicts` 关系
3. 决定哪颗是对的 → 另一颗标记 `retracted` 或 `superseded`
4. 记录冲突解决历史

---

## 五、原子状态扩展

### 5.1 当前状态

G6 定义了 5 种状态，但代码只落地 2 种（draft/verified）。实际使用中还有 `red-team-verified`（非标准）。

### 5.2 扩展为 7 种状态

```
draft → machine-verified → red-team-verified → human-verified → verified
                                                          ↓
                                                     superseded（被新原子取代）
                                                     retracted（被证据推翻）
```

| 状态 | 含义 | 谁能置 |
|---|---|---|
| draft | 草稿 | Writer |
| machine-verified | 门禁通过 | 机器 |
| red-team-verified | 红队通过 | 红队 Agent |
| human-verified | 人审通过 | 人 |
| verified | 最终确认 | 人（human-verified 的别名） |
| superseded | 被新原子取代 | 人 |
| retracted | 被证据推翻 | 人 |

### 5.3 规则

- `ATOM-STATUS-VALID`：status 必须是 7 种之一（`red-team-verified` 合法化）
- `ATOM-SUPERSEDED-BY`：superseded 原子必须有 `superseded_by: <新原子id>`
- `ATOM-RETRACTED-REASON`：retracted 原子必须有 `retracted_reason` 和 `retracted_by`（哪条证据推翻的）
- `ATOM-STATUS-TRANSITION`：状态转换必须合法（不能从 draft 直接到 verified）

### 5.4 superseded/retracted 的处理

- 不删除原子（保留历史）
- 在学习路径中自动排除
- 闪卡导出时自动排除（E16 修复）
- 证据卡仍保留（作为反面教材）

---

## 六、文档生命周期管理

### 6.1 问题

- 架构文档 225 份，编号冲突（484/485 各两份）
- 没有状态标记（哪些是最新的？哪些过时了？）
- README_INDEX.md 有索引，但没有状态列
- 苦力 Agent 和架构师同时写文档，编号冲突

### 6.2 改法：文档状态系统

每份架构文档加 frontmatter：

```yaml
---
id: 484
title: 成本与Token经济学详细方案
version: 1.0
status: active          # active / deprecated / superseded / draft
superseded_by: null      # 被哪份取代
created_at: 2026-09-14
updated_at: 2026-09-14
---
```

### 6.3 编号冲突解决

- 编号是唯一标识，不能重复
- 发现冲突 → 后写的那份改编号（如 484B）
- `tools/doc_lint.py`（479 在做）加编号唯一性检查
- 写文档前先查最新编号，避免冲突

### 6.4 文档分类

225 份文档按类型分类：
- `active/`：当前有效的方案和规范
- `deprecated/`：过时的方案
- `superseded/`：被新方案取代的
- `archive/`：历史记录（调研笔记、过程文档）

或者不移动文件，用 frontmatter 的 status 字段标记，索引按 status 分组。

### 6.5 工具：doc_lifecycle.py（约 100 行）

- 扫描所有架构文档的 frontmatter
- 检查编号唯一性
- 检查 status 合法性
- 生成按 status 分组的索引
- 标记超过 30 天没更新的 active 文档（可能过时）

---

## 七、实施计划

### 第一阶段（零/低成本，立即做）

1. **状态统一**：所有原子的 status 改为标准格式（去掉注释，统一 7 种），`red-team-verified` 合法化
2. **工件版本**：证据卡加 artifact_version，工件加头部注释，gate 验证匹配
3. **编号冲突修复**：484/485 重名文档改编号，doc_lint 加编号唯一性检查
4. **文档 frontmatter**：架构文档加 id/version/status/created_at/updated_at

### 第二阶段（中等成本，下一批做）

5. **claim 版本管理**：原子加 claim_history，gate 规则强制记录
6. **知识冲突扫描**：claim_conflict_scan.py，同域原子 claim 关键词矛盾检测
7. **superseded/retracted**：状态扩展，闪卡导出和学习路径自动排除

### 第三阶段（高成本，积累数据后做）

8. **文档自动归档**：超过 30 天没更新的 active 文档自动提醒复审
9. **冲突自动解决建议**：检测到冲突后，根据证据强度建议哪颗更可信
10. **完整版本链**：claim/工件/卡/原子的版本全链路可追溯

---

## 八、预期效果

| 指标 | 当前 | 第一阶段后 | 第三阶段后 |
|---|---|---|---|
| 原子 status 格式 | 5 种混乱 | 1 种标准 | 1 种标准 |
| 工件-卡不同代 | 反复出现 | block 拦截 | 自动修复 |
| 知识冲突检测 | 0（关系没人用） | L1+L2 辅助 | 自动检测+解决建议 |
| 原子状态数 | 2（draft/verified） | 7（含 superseded/retracted） | 7 |
| 文档编号冲突 | 有（484/485） | 0（唯一性检查） | 0 |
| 文档状态 | 无 | 有 frontmatter | 自动归档 |
| claim 历史 | 无 | 有 claim_history | 完整版本链 |

---

## 九、和现有系统的集成

- **gate_engine.py**：加 ATOM-CLAIM-HISTORY / EV-ARTIFACT-VERSION-MATCH / ATOM-STATUS-VALID 规则
- **atom_evidence_replay.py**：重生成工件时自动递增 version
- **479 doc_lint**：加编号唯一性检查和文档 frontmatter 检查
- **482 evidence_graph**：版本关系作为图的边（claim_v1 → claim_v2）
- **482 修剪机制**：superseded/retracted 原子自动归档
- **489 教学效果**：superseded/retracted 原子不进入学习路径和闪卡

---

## 十、风险与缓解

| 风险 | 缓解 |
|---|---|
| claim_history 增加 Writer 负担 | 工具自动记录（修改 claim 时自动追加旧版本），Writer 只写 reason |
| 工件版本改动大 | 先加字段不强制，下一批再 block；存量卡批量补 |
| 语义冲突检测误报 | L2 只 warn 不 block，人审核后才标记 contradicts |
| 文档分类移动文件 | 不移动文件，用 frontmatter status 标记，索引分组 |
| 编号冲突修复需要改文件名 | 后写的改编号（如 484B），先写的保留；记录在索引中 |
