# 406 阙疑增量知识更新与版本管理：原子会老，数据会过期，schema 会变

> 日期：2026-09-13。外部调研：知识库版本管理（SemVer 适配、双时态建模、废弃先于删除、不可变时间点快照）、实证数据新鲜度（SWE-bench-Live 依赖漂移、Prompt CI/CD 不可变 bundle、API 漂移保真度崩落）、知识图谱 schema 演化（数据库迁移式变更、多标签软过渡、加性自由/破坏性双写）。
> 核心问题：**阙疑 27 颗原子没有版本号，56 张证据卡没有数据新鲜度标记，frontmatter schema 已经变过多次但存量不统一。** 系统在增长，但没有"变老"的机制。

---

## 一、当前的真实问题（不是理论，是已经发生的）

| 问题 | 真实案例 | 后果 |
|---|---|---|
| claim 反转后旧版本丢失 | ALLOC-002 从"pool 32B 最省"改成"pool 8056B 最大"，旧 claim 只存在于红队报告 | 学生看不到"为什么这是个常见误解"，教学价值丢失 |
| 性能数据无保质期 | PERF-004 同机跨运行 18.86×→8.78×（2× 波动） | 卡内写死的倍数可能在任何重跑时失效 |
| 编译器升级后 sha 全变 | MinGW 13.1→15.3 后所有工件 sha 变化 | replay 强校验会全 refute，需要批量迁移 |
| schema 不统一 | 27 颗原子中有些有 pedagogy、有些没有；有些有 relations、有些没有 | 工具解析时静默跳过，规则覆盖不均 |
| 工件与断言不同代 | G2 缺陷 1：改了卡的计数但没重生成工件 | "旧 hash vs 旧记录 hash 一致"被当成复现性证据（假阳性） |

---

## 二、原子版本化（SemVer 适配）

每颗原子加 `version: MAJOR.MINOR.PATCH` 字段：

| 级别 | 触发条件 | 阙疑实例 |
|---|---|---|
| **MAJOR** | claim 方向性反转、核心结论改变 | ALLOC-002"pool 最省"→"pool 最大"；LEAK-002"零报告"→"报告依赖代码形态" |
| **MINOR** | 补充新证据/新平台数据，claim 不变 | PERF-003 加 Linux 平台数据；EV-MEM-039 加完整原始输出 |
| **PATCH** | 修正格式/错别字/措辞，内容不变 | frontmatter 补字段、术语统一 |

### 规则
- **MAJOR 变更必须保留旧版本**：不覆盖，在卡内加 `supersedes: v{旧版本}` + 旧 claim 摘要（教学用）
- **版本变更必须进 status_history**：`{level: version_bump, from: 1.0.0, to: 2.0.0, at: ..., by: ..., reason: ...}`
- **当前所有原子初始版本 = 1.0.0**（verified 的原子），draft 原子 = 0.1.0

### 为什么不用 git 历史代替？
- git 历史是"文件级"的，不是"claim 级"的——一个文件可能同时改了 claim 和格式，git diff 分不清
- 学生/工具不需要翻 git log 就能知道"这颗原子的结论有没有变过"
- 版本号是**语义声明**，git hash 是**物理标识**——两者互补

---

## 三、实证数据新鲜度管理（三类数据三种保质期）

每张证据卡加 `data_freshness` 段：

### 类型 1：确定性判据数据（长保质期）
- **内容**：actual 中的方向量（`sharing_is_slower=1`、`dtor_count=0`）、符号存在性断言
- **保质期**：只要编译器版本+优化档不变，就稳定
- **标记**：`stability: deterministic`，重测条件=编译器大版本升级
- **例**：EV-CONC-001 的"spin_plain 被消除"——GCC 15 上确定，GCC 16 可能变

### 类型 2：性能数据（极短保质期）
- **内容**：纳秒数、倍数、吞吐量
- **保质期**：**每次运行都可能变**（PERF-004 同机 18.86×→8.78×）
- **标记**：`stability: performance`，必须写"锚方向不锚绝对值"+ 硬件+编译器+迭代数
- **重测条件**：硬件变化、编译器升级、任何对结论的质疑
- **规则**：性能数据**永远不进断言锚**（PERF-003 教训已固化）

### 类型 3：工具观测数据（中保质期）
- **内容**：LSan/TSan/ASan 报不报、报多少
- **保质期**：高度依赖代码形态和 sanitizer 版本（LEAK-002：加一个 volatile 计数器就从零报告变报告 64B）
- **标记**：`stability: tool_observation`，必须写完整复跑命令+sanitizer 版本
- **重测条件**：sanitizer 升级、夹具任何改动

### 新鲜度仪表盘
- `tools/data_freshness.py`：扫描所有证据卡，列出 `stability: performance` 且实测日期 > 180 天的卡，标记"建议重测"
- 不自动重测（性能重测有波动风险），只提醒

---

## 四、编译器/标准升级迁移流程

当 MinGW 从 15.3 升到 16.x，或 WSL g++ 从 14 升到 15 时：

### 迁移四步
1. **批量重编译**：用新编译器重编译所有夹具，生成新 .asm
2. **sha 批量更新**：所有证据卡的 artifact_sha256 更新为新值
3. **断言批量重跑**：跨编译器路径（artifact_assert）逐条验证，标记哪些断言在新编译器下失效
4. **失效断言处置**：
   - 断言失效但 claim 仍成立 → 更新断言（MINOR 版本）
   - 断言失效且 claim 也不成立 → claim 反转（MAJOR 版本，保留旧版）

### 工具支持
- C1 的 `--verify-artifact` 可以做步骤 1-3（重编译到临时目录+sha 比对+断言验证）
- 加 `--compiler-upgrade` 模式：批量处理所有卡，输出迁移报告（哪些卡需要更新、哪些 claim 需要反转）

### 标准升级（C++23→C++26）
- 不是所有原子都受影响——只有引用了新标准特性的原子需要重审
- `tools/standard_impact.py`：扫描原子的 claim/evidence，找引用了特定标准条款的卡，标记"需 C++26 重审"
- MSVC 永久边界不变：标准条文代替实测

---

## 五、Schema 演化与迁移（像数据库 migration 一样）

### 当前问题
frontmatter schema 已经变过多次（G6 加了 status_history、DAL、human_review、pedagogy 结构化），但存量 27 颗原子不统一。

### 规则
1. **schema 本身有版本号**：`schema_version: v1.2`（当前 G6 后的版本）
2. **加性变更自由**：加新字段（如 `version`、`data_freshness`）不需要迁移，旧卡缺字段=默认值
3. **破坏性变更走迁移脚本**：
   - 删字段、改字段名、改字段含义 = 破坏性
   - 必须写 `tools/migrations/migrate_v{旧}_to_v{新}.py`，批量转换所有存量卡
   - 迁移后所有卡的 schema_version 统一更新
4. **迁移必须可回滚**：迁移前 git tag，迁移失败可 revert

### 多标签软过渡（借鉴知识图谱）
当字段含义变化时（如 `type: tool` 改成 `type: contrast`）：
- 先同时支持新旧值（一个过渡期）
- 工具同时识别两种
- 存量卡批量更新
- 一个版本后删除旧值支持

---

## 六、废弃机制（不删除，标记）

### 原子废弃
- 原子被新原子取代时：`status: deprecated` + `superseded_by: ATOM-XXX` + `deprecated_at: 日期` + `reason: 原因`
- 不删除文件——deprecated 原子仍可被引用（作为"为什么这个想法被取代"的教学材料）
- gate 规则：deprecated 原子不参与正例回归，但 relations 引用仍有效

### 误解废弃
- 误解被纠正/不再适用时：`status: resolved` + `resolved_by: ATOM-XXX` + `resolution: 说明`
- 不删除——resolved 误解仍是"学生曾经有过的错误观念"，有教学价值

### 证据卡废弃
- 数据过时时：`status: stale` + `recheck_after: 日期` + `reason: 编译器升级/硬件变化`
- 重测后更新数据→恢复 active，或确认 claim 反转→MAJOR 版本

---

## 七、落地优先级

| 优先级 | 项 | 理由 | 依赖 |
|---|---|---|---|
| **P0** | 原子加 `version` 字段（初始 1.0.0） | 零风险，为后续打基础 | 无 |
| **P0** | 证据卡加 `data_freshness.stability` 分类 | 性能数据的保质期问题是真实的 | 无 |
| **P1** | claim 反转保留旧版本（MAJOR 规则） | ALLOC-002/LEAK-002 已经需要 | version 字段 |
| **P1** | schema_version 字段 + 迁移脚本框架 | 存量不统一是真实问题 | 无 |
| **P2** | 编译器升级迁移工具（--compiler-upgrade） | 下次 GCC 升级时需要 | C1 --verify-artifact |
| **P2** | data_freshness.py 新鲜度提醒 | 规模大了需要 | data_freshness 字段 |
| **P3** | 标准影响扫描工具 | C++26 时需要 | 无 |
| **P3** | 废弃机制（deprecated/resolved/stale） | 规模大了才需要 | version 字段 |

---

## 八、与现有体系的关系

- **是 G6 状态机的扩展**：G6 有 draft/machine-verified/verified/archived，406 加 version + data_freshness + deprecated
- **是 404 知识健康维度的具体落地**：404 说"过期原子数"，406 定义什么叫"过期"、怎么标记
- **是铁律"工件与断言同代"的制度化**：406 把"同代"从纪律变成 schema 字段+迁移工具
- **不替代 git**：git 管文件历史，version 管语义历史，两者互补

---

## 九、元结论

阙疑系统的知识不是"写完就完了"——它会**变老**。claim 会被新证据反转，性能数据会随硬件/编译器漂移，schema 会演化，标准会升级。

没有版本管理的知识库，18 个月后会变成"shelfware"（知识图谱运营的七种失败模式之一）——旧数据和新数据并存，没人知道哪个可信。

**先做 P0**：给 27 颗原子加 version=1.0.0，给 56 张证据卡加 data_freshness 分类。这是零风险的基础设施，为后续所有演化打基础。
