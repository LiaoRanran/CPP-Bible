# 301_replay三分类架构调研_confirm_refute_infra_error

> 2026-09-12 · G6 §4.1 放权前必修项 · 本文是设计调研，不是实现
> 关联：docs/kernel/G6_status_levels.md §4.1 · tools/atom_evidence_replay.py（644 行）

---

## 一、问题定义

### 1.1 当前二值判决的风险

`atom_evidence_replay.py` 当前返回 `confirm` 或 `refute:<reason>`，退出码 0/1。

**问题**：基础设施故障与内容证伪不分流。

| refute 原因 | 性质 | 放权后风险 |
|---|---|---|
| `compile_failed` | 基础设施（编译器不存在/PATH 错/依赖缺失） | 假 refute 被当"机器否决内容"，人不复看 |
| `artifact_absent` | 基础设施（文件被误删/迁移窗口期） | 同上 |
| `bad_frontmatter` | 卡格式（可机器修复） | 同上 |
| `missing_field` | 卡格式（可机器修复） | 同上 |
| `run_mismatch` | 内容证伪（卡写错/工件过期） | 正确分类 |
| `sha256_mismatch` | 内容证伪（工件过期/卡写错） | 正确分类 |
| `artifact_assert_failed` | 内容证伪（断言不满足） | 正确分类 |
| `sanitizer_reported` | 内容证伪（未声明的报错） | 正确分类 |

### 1.2 实测案例

2026-09-12 Examples/ 迁移窗口期（P4 把 95 个 `_atom_*` 从 Examples/ 移到 Examples/atoms/），replay 瞬时出现 `confirm=0 refute=48`——全部是 `refute:compile_failed`（夹具路径还没更新）。如果放权体系已生效，这 48 张卡会被标记为"机器否决"，而实际原因是基础设施（文件移动），与内容无关。

### 1.3 放权后的放大效应

G6 四级状态体系下，DAL C/D/E 原子红队通过即可入库，人不复看。如果 replay 的 infra_error 被当成 refute：
- 一次环境抖动（编译器升级、PATH 变化、磁盘满）会批量"否决"已验证原子
- golden_lock 的 `replay_confirm` 计数会暴跌，触发"恶化"告警
- 人看到告警后以为是内容问题，去修卡（实际是修环境）
- 最坏情况：有人为了"消除 refute"而修改卡的断言（降标），而不是修复环境

---

## 二、三分类设计

### 2.1 判决空间

```
confirm              内容通过（四项校验全过）
refute:<reason>      内容证伪（卡写错/断言不满足/工件过期）
infra_error:<reason> 基础设施故障（环境问题，需人介入修环境）
```

### 2.2 原因分类映射

| 当前 refute 原因 | 新分类 | 理由 |
|---|---|---|
| `compile_failed` | **infra_error** | 编译器/工具链问题，与卡内容无关 |
| `artifact_absent` | **infra_error** | 文件缺失（被误删/迁移中），与卡内容无关 |
| `bad_frontmatter` | **infra_error** | 卡格式损坏（工具/编码问题），非内容判断 |
| `missing_field` | **refute** | 卡缺必填字段——这是内容质量问题（Writer 失职） |
| `missing_artifact_command` | **refute** | 卡缺工件或命令——内容质量问题 |
| `ambiguous_expected` | **refute** | 多组 run 值不一致——内容质量问题 |
| `run_mismatch` | **refute** | 运行输出不匹配——内容证伪 |
| `artifact_assert_failed` | **refute** | 断言不满足——内容证伪 |
| `sha256_mismatch` | **refute** | sha 不匹配——工件过期/卡写错 |
| `sanitizer_reported` | **refute** | 未声明的 sanitizer 报错——内容证伪 |
| （新增）`timeout` | **infra_error** | 编译/运行超时——环境问题 |
| （新增）`toolchain_missing` | **infra_error** | 编译器/工具不存在——环境问题 |
| （新增）`disk_full` | **infra_error** | 磁盘满——环境问题 |

### 2.3 关键边界：什么算 infra_error

**判定原则**：如果修复方式是"改环境"而不是"改卡"，就是 infra_error。

| 场景 | 修复方式 | 分类 |
|---|---|---|
| g++ 不在 PATH | 修 PATH/装编译器 | infra_error |
| 夹具文件被误删 | 恢复文件/修路径 | infra_error |
| 磁盘满导致编译失败 | 清磁盘 | infra_error |
| 编译超时（代码死循环） | 改夹具代码 | refute（内容问题） |
| 编译失败（语法错误） | 改夹具代码 | refute（内容问题） |
| 运行输出不匹配 | 改卡/改夹具 | refute（内容问题） |

**难点**：`compile_failed` 可能是环境问题（编译器不存在）也可能是内容问题（代码语法错误）。需要区分：
- 编译器不存在/无法执行 → infra_error
- 编译器存在但编译报错 → refute（代码有语法错误，是内容问题）

当前实现中 `compile_failed` 统一返回，没有区分这两种情况。三分类需要细化：
- `infra_error:compiler_missing` — 编译器不存在
- `refute:compile_error` — 编译器存在但编译失败（代码问题）

---

## 三、fail-closed 设计

### 3.1 为什么 infra_error 必须 fail-closed

G6 §4.1 的核心要求：**infra_error 必须仍非零退出、单独计数、不计入内容恶化**。

如果 infra_error 返回 exit 0（放行），就会出现逃生舱：
- 删掉夹具文件 → artifact_absent → infra_error → exit 0 → "通过"
- 这等于"删掉证据即放行"，比降标更危险

### 3.2 退出码设计

```
exit 0  → 全部 confirm
exit 1  → 有 refute（内容证伪）
exit 2  → 有 infra_error（基础设施故障）—— 仍非零，但原因不同
exit 3  → 既有 refute 又有 infra_error
```

门禁用 `--check` 时：
- exit 0 = 通过
- exit 1/2/3 = 不通过（但原因可区分）

### 3.3 计数设计

```
[replay] confirm=42 refute=0 infra_error=6 共 48 张卡
```

- `confirm` — 内容通过
- `refute` — 内容证伪（计入 golden_lock 的内容恶化）
- `infra_error` — 基础设施故障（不计入内容恶化，但触发环境告警）

golden_lock 的 `replay_confirm` 只计 confirm，refute 和 infra_error 都不计入。但 `infra_error > 0` 时应触发单独的"环境告警"（不是"内容恶化"）。

---

## 四、与 golden_lock / gate 的联动

### 4.1 golden_lock 统计口径

当前：`replay_confirm: 48`（只计 confirm）

三分类后：
```json
{
  "replay_confirm": 42,
  "replay_refute": 0,
  "replay_infra_error": 6,
  "replay_total": 48
}
```

恶化判定：
- `replay_confirm` 下降 + `replay_refute` 上升 = 内容恶化（需人审）
- `replay_confirm` 下降 + `replay_infra_error` 上升 = 环境故障（需修环境，不是内容问题）

### 4.2 gate 规则

新增规则 `REPLAY-INFRA-ERROR`（warn 级）：
- 如果 replay 有 infra_error，gate 报 warn（不是 block）
- warn 信息明确指出"基础设施故障，非内容问题"
- 建议修复环境后重跑

### 4.3 CI 处理

CI 的 quality job 中：
- replay exit 0 → 通过
- replay exit 1 → 失败（内容问题）
- replay exit 2 → 失败（环境问题），但日志标注 "INFRA ERROR"
- replay exit 3 → 失败（混合）

---

## 五、实现路径

### 5.1 最小改动（第一阶段）

1. 在 `replay_card()` 返回值中增加第三类：`infra_error:<reason>`
2. 把 `compile_failed` 拆分为：
   - `infra_error:compiler_missing`（编译器不存在）
   - `refute:compile_error`（编译器存在但编译失败）
3. 把 `artifact_absent` 改为 `infra_error:artifact_absent`
4. `main()` 中区分三类计数，exit code 按 §3.2
5. golden_lock 同步统计口径

### 5.2 增强（第二阶段）

1. 新增 `timeout` 检测（编译/运行超时 → infra_error）
2. 新增 `disk_full` 检测（OSError 中 ENOSPC → infra_error）
3. 新增 `toolchain_version_mismatch`（编译器版本与卡声明不符 → infra_error 或 warn）
4. CI 中 infra_error 单独标注，不触发"内容恶化"告警

### 5.3 回归测试

- 毒样例 P8：编译器不存在 → infra_error（不是 refute）
- 毒样例 P9：夹具文件缺失 → infra_error（不是 refute）
- 毒样例 P10：代码语法错误 → refute（不是 infra_error）
- 毒样例 P11：既有 infra_error 又有 refute → exit 3，分别计数

---

## 六、与其他系统的关系

### 6.1 与 G6 四级状态的关系

三分类是放权的**安全前提**：
- 没有三分类，放权 = 降标（环境抖动被当内容否决）
- 有了三分类，放权 = 精准（内容问题机器判，环境问题人修）

### 6.2 与 S6 毒样例的关系

当前 8 个毒样例（P1-P7 + 阴性）全部测试 gate_engine。replay 三分类需要新增 4 个毒样例（P8-P11），测试 replay 的分类正确性。

### 6.3 与 Writer 预防机制的关系

Writer 阶段应该自检：
- 夹具文件是否存在？（避免 artifact_absent）
- 编译器是否可用？（避免 compiler_missing）
- 命令是否可执行？（避免 compile_failed）

这些自检可以减少 infra_error 的发生，但不能替代三分类（环境问题随时可能发生）。

---

## 七、开放问题

1. **compile_error vs compiler_missing 的区分**：如何可靠判断"编译器不存在" vs "编译器存在但编译失败"？
   - 方案 A：先检查编译器可执行文件是否存在（shutil.which）
   - 方案 B：检查 subprocess 的返回码（127 = command not found）
   - 方案 C：尝试运行 `g++ --version`，失败则 compiler_missing

2. **infra_error 的重试机制**：基础设施故障可能是瞬时的（网络抖动、磁盘瞬满），是否需要自动重试？
   - 建议：不自动重试（保持确定性），但在日志中提示"可重试"

3. **与 CI 的集成**：CI 中 infra_error 是否应该让 job 失败？
   - 建议：是（fail-closed），但标注 "INFRA ERROR" 以便区分

4. **历史数据迁移**：当前 48 张卡的 replay 结果都是 confirm/refute 二值，是否需要重跑？
   - 建议：不需要（历史数据仍有效），新分类只影响未来的运行

---

## 八、优先级与建议

**P0（放权前必修）**：
- 三分类判决空间（confirm/refute/infra_error）
- compile_failed 拆分（compiler_missing vs compile_error）
- artifact_absent → infra_error
- exit code 区分（0/1/2/3）
- golden_lock 统计口径更新

**P1（放权后增强）**：
- timeout/disk_full 检测
- 毒样例 P8-P11
- CI 标注 INFRA ERROR

**P2（长期优化）**：
- Writer 阶段环境自检
- infra_error 自动诊断（给出修复建议）

---

*本文是设计调研，实现待授权。核心结论：三分类不是"更友好的报错"，而是放权体系的安全前提——没有它，环境抖动会被当成内容否决，放权即退化为降标。*
