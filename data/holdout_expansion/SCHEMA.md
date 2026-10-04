# `data/holdout_expansion/` 标注 Schema（676m 起生效；677a 增补 `provenance`）

> 本文件是扩样集 1042 条标注（`sample_*.json`）的**唯一字段规范**。
> 由 `tools/fix_676m_schema.py` 生成/校验；批次：676m（数据修复）。
> **677a 增补**：新增 `provenance` 枚举（§2.1），把布尔 `planted` 细化为三类来源；
> **只改 schema 与表述，不改逐样本 .json、不重新标注**。版本 of record：`research/latex/VERSION.md`。

## 1. 文件布局

```
data/holdout_expansion/<batch>/
  INDEX.json            # 批次索引（id 键见 §5.4）
  sample_<id>.json      # 逐样本标注（权威记录）
  sample_<id>*.cpp/.h   # 样本源码（只读，676m 零修改）
```

批次：`expA`(100) `expB`(94) `expC`(200) `expD`(200) `expE`(200) `expF`(149) `expG`(99) = **1042**。

## 2. 字段规范

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `sample_id` | str | ✅ | 样本唯一 id（676m 起全批次统一；expA/expC 原为 `id`） |
| `defect_type` | str | ✅ | 统一词表取值（§3），676m 起 34 项闭集 |
| `defect_location` | obj | ✅ | `{file, line, function, notes}` |
| `defect_location.file` | str | ✅ | 缺陷所在源文件名（676m 补全；多 TU 样本按缺陷标记行定位） |
| `defect_location.line` | int\|null | ✅ | **绝对文件行号**（1-based；多文件样本可为 null） |
| `defect_location.function` | str | ✅ | 缺陷所在函数（全局初始化用 `(global)`） |
| `defect_location.notes` | str | ⭕ | 缺陷行说明（676m 起由 `note`/`description` 统一而来） |
| `severity` | str | ✅ | `low` / `medium` / `high` |
| `planted` | bool | ✅ | **兼容字段（676m 口径，保留）**：`true`=本项目人工植入；`false`=非自造（真实来源重写或对照样本）。**677a 起请改用 `provenance`**，见 §2.1 |
| `provenance` | str | ⭕ | **677a 新增（枚举，见 §2.1）**：`self-authored` / `source-derived-reconstruction` / `original-external-artifact`。当前由 `planted` **派生**（`true → self-authored`，`false → source-derived-reconstruction`），**不写进逐样本 .json**（红线 6 同款：不新增逐样本字段），只在聚合清单中派生 |
| `expected_verdict` | str | ✅ | `catch` / `miss`（**独立检测器判据**，见 §4.1） |
| `expected_detectors` | list[str] | ⭕ | 预期命中的资产名 |
| `trigger_condition` | str | ⭕ | 触发条件 / 优化敏感性（676m 起承接原 `conditional_trigger`、`optimization_dependent` 元标签） |
| `notes` | str | ✅ | 顶层缺陷说明（中文） |
| `verification` | obj | ⭕ | 生成期的编译/检测复现记录（各批次字段略有差异，原样保留） |
| `source` | obj | ⭕ | `planted=false` 样本的来源（CVE / GitHub issue） |

> 红线 6：676m 只改 §4 列出的字段，其余字段（含 `verification`、`source`、`platform_*`、`thread_count` 等）逐字节保持不变。

## 2.1 `provenance`（677a 新增；`planted` 的语义细化）

### 2.1.1 为什么要细化

`planted=false` **不等于"真实世界样本"**。本库的 74 条 `planted=false` 是**从真实 CVE / GitHub issue
重写而来的单文件教学化片段**（"real-source-derived reconstruction"），既不是原始外部产物，
也不是自然分布的生产代码。把布尔 `planted=false` 读成 "real-world defects" 会系统性高估外部效度
（677a 评审指出的问题）。

### 2.1.2 枚举定义

| `provenance` | 对应 `planted` | n（扩样 1042） | 定义 |
|---|---|--:|---|
| `self-authored` | `true` | **968** | 本项目为演示某类缺陷**自撰**的可编译片段 |
| `source-derived-reconstruction` | `false` | **74** | 基于真实 **CVE / GitHub issue** 的**等价重写**：单文件、教学化、剥离了原始上下文；构造过程记录在 `source.{type,id,url,project,commit,simplification}` |
| `original-external-artifact` | —— | **0** | **当前语料中不存在**。无任何原始外部代码片段被收录 |

### 2.1.3 迁移说明

- **不改逐样本 .json**（红线 6：不新增逐样本字段）。`provenance` 由 `planted` 按上表**确定性派生**，
  写在聚合清单 `data/676m_sample_manifest_corrected.json` 的派生成分中。
- **不重新标注**：677a 只改 schema 与表述，**不重判任何样本的 provenance**（真源核查由 677b/677c 负责）。
- **`planted` 保留**：`planted=true` ⇒ `self-authored`；`planted=false` ⇒ `source-derived-reconstruction`
  （当前**无** `original-external-artifact`，故该分支恒空）。若将来收录原始外部代码，必须显式置
  `original-external-artifact` 并附许可与来源。
- **复现**：`python -c "import json,collections;print(collections.Counter(...))"`（见 `DATASHEET.md` §2.2）。

## 3. 统一词表（`defect_type`，34 项闭集）

规范词表 = 676m 规格建议的 31 项 + 3 项经论证的补充。补充项的设计理由见 §3.2。

### 3.1 词表与粗粒度分组

| # | `defect_type` | `defect_group`（15 类，与 676k TAXONOMY 对齐） |
|---|---------------|------------------------------------------|
| 1 | `memory_safety` | `memory_lifetime` |
| 2 | `use_after_free` | `memory_lifetime` |
| 3 | `double_free` | `memory_lifetime` |
| 4 | `memory_leak` | `memory_lifetime` |
| 5 | `smart_pointer` | `memory_lifetime` |
| 6 | `raii_violation` | `memory_lifetime` |
| 7 | `move_semantics` | `memory_lifetime` |
| 8 | `out_of_bounds` | `out_of_bounds` |
| 9 | `null_pointer_deref` | `null_deref` |
| 10 | `uninitialized_read` | `uninitialized_read` |
| 11 | `integer_overflow` | `integer_ub` |
| 12 | `bit_operation` | `integer_ub` |
| 13 | `type_punning` | `type_alias_alignment` |
| 14 | `strict_aliasing` | `type_alias_alignment` |
| 15 | `alignment` | `type_alias_alignment` |
| 16 | `endianness` | `type_alias_alignment` |
| 17 | `data_race` | `data_race` |
| 18 | `atomic_ub` | `concurrency_order` |
| 19 | `memory_order` | `concurrency_order` |
| 20 | `deadlock` | `liveness` |
| 21 | `condition_variable` | `liveness` |
| 22 | `iterator_invalidation` | `stl_iterator` |
| 23 | `stl_container_ub` | `stl_iterator` |
| 24 | `string_ub` | `stl_iterator` |
| 25 | `algorithm_misuse` | `stl_iterator` |
| 26 | `virtual_function` | `virtual_or_oop` |
| 27 | `lambda_capture` | `virtual_or_oop` |
| 28 | `volatile_misuse` | `embedded_platform` |
| 29 | `register_ub` | `embedded_platform` |
| 30 | `interrupt_safety` | `embedded_platform` |
| 31 | `cross_tu_ub` | `logic_or_api` |
| 32 | `linker_odr` | `type_alias_alignment` |
| 33 | `logic_error` | `logic_or_api` |
| 34 | `other_ub` | `generic_ub` |

`defect_group` **不写进逐样本 .json**（红线 6：不新增字段），只在聚合清单 `data/676m_sample_manifest_corrected.json` 中派生。

### 3.2 相对建议表的三项补充（工程决策）

| 补充项 | n | 理由 |
|--------|---|------|
| `lambda_capture` | 30 | lambda 捕获生命周期缺陷（悬垂引用 / 悬垂 `this`）。建议表无等价项；塞进 `other_ub` 会把一个 100% 可归因的类打成兜底类。 |
| `algorithm_misuse` | 35 | STL 算法**前置条件**违例（比较器不满足严格弱序、重叠 `copy`、`remove` 不删元素）。与 `stl_container_ub`（容器自身 UB）语义不同，676k TAXONOMY 也单列。 |
| `logic_error` | 17 | CVE 类**非 UB** 语义/API/状态缺陷（如 Shellshock、Dirty Pipe、证书撤销检查不足）。这些样本无 UB 可言，归 `other_ub` 属误标。 |

### 3.3 收敛关系（旧标签 → 规范名）

| 旧标签 | → | 规范名 | 说明 |
|--------|---|--------|------|
| `resource_leak` | → | `memory_leak` | 含 fd 泄漏；词表只保留 memory_leak |
| `heap_overflow / heap_overread / heap_underflow / stack_* / global_overflow` | → | `out_of_bounds` | 越界家族统一；方向/位置由 `notes` 保留 |
| `pointer_overflow` | → | `out_of_bounds` | 指针算术越界属越界访问 |
| `info_leak` | → | `out_of_bounds` | 越界读导致的信息泄露（Heartbleed 类） |
| `null_deref` | → | `null_pointer_deref` | 同义合并 |
| `division_by_zero` | → | `integer_overflow` | 整数 UB 家族 |
| `type_confusion` | → | `type_punning` | 类型双关 / 混淆同族 |
| `race_condition` | → | `data_race` | 同义合并 |
| `aba_problem` | → | `atomic_ub` | 无锁协议的原子性缺陷 |
| `lock_priority_inversion` | → | `deadlock` | 活性缺陷，归并发活性类 |
| `state_machine / resource_exhaustion / timing_side_channel / infinite_loop` | → | `logic_error` | 非 UB 的语义/资源/时序缺陷 |
| `UB / undefined_behavior / other_ub / memory_safety / conditional_trigger / optimization_dependent` | → | `按证据细分` | 见 §4.2 规则；无法细分回落 other_ub |
| `cross_tu_ub（多重定义/ODR）` | → | `linker_odr` | 链接期 ODR 违例 |

## 4. 676m 迁移规则

### 4.1 `expected_verdict` 口径（H1）

`expected_verdict` = **独立检测器判据**：该样本在 8 资产池下能否被**实际观测**到。

- `catch`：至少一个资产产生非空诊断报告；
- `miss`：无任何资产产生报告——**包含 sanitizer 挂起超时（rc=124）后无报告**。

因此 `hung_flag=true` 的样本（自旋死锁 / 自死锁 / cv 永久等待）真实判据是 `miss`，不是 `catch`。676m 把 expE 34 条此类样本由 `catch` 修正为 `miss`。

### 4.2 笼统标签细分规则（H2）

对 `memory_safety` / `undefined_behavior` / `other_ub` / `UB` / `conditional_trigger` / `optimization_dependent` / `compiler_warning`，按 `notes` + `defect_location` 描述 + `trigger_condition` 的证据串做**规则化细分**（规则见 `tools/fix_676m_schema.py::resolve_by_evidence`，全部为确定性关键字规则，无模型介入）。无法细分者回落 `other_ub`。

### 4.3 元标签拆分

`conditional_trigger` 与 `optimization_dependent` 描述的是**触发条件/优化敏感性**，不是缺陷种类。676m 把它们的值移入 `trigger_condition`，`defect_type` 改填按 §4.2 细分出的具体类型。

### 4.4 行号口径（M4）

`defect_location.line` = **绝对文件行号**。expB 的 `.cpp` 头部有 8 行标注块（`// sample_Bxxx` … `// (authoritative annotation in …)`），原行号是**去掉头部后的相对行号**。676m 逐条与源文件缺陷标记行核对：

- `line + 8` 等于缺陷标记行 ⇒ 改写为绝对行号；
- `line` 已等于标记行 ⇒ 保持；
- 两者都不等 ⇒ **保持原值**并在迁移报告中标注为未验证（不盲目 +8）。

### 4.5 `defect_location.file`（M1）

判定顺序：① 样本只有 1 个源文件 ⇒ 取该文件；② 多源文件 ⇒ 取**唯一**含缺陷标记（`<<PLANTED-DEFECT>>` 或 `DEFECT:`）的文件；③ 仍不唯一 ⇒ 取字典序首个并在报告中标注 `ambiguous-*`。

## 5. 已知残留（诚实登记）

1. **`INDEX.json` 的 id 键**：expA/expC/expF 的 `INDEX.json` 用 `index[].id`，其余批次用 `samples[].sample_id`。676m 只在 `INDEX.json` 中**增补** `sample_id` 别名（保留 `id`，以免打断冻结的 `data/676f_pipeline.py`），逐样本 .json 则已完全统一。
2. **多文件样本行号**：expC 的 30 条多 TU 样本 `line` 指向头文件/单 TU，跨文件不可比；676k 的 κ 分析亦记 null。
3. **行号语义分歧**：iterator 类样本原标注指向「使用行」，重标注指向「失效操作行」（676k §3.2）。676m 不改语义，只在本文档明确为「缺陷发生的操作行」。
4. **批内克隆率 62.2%**：全库仅 572 种不同代码结构（676k §H3）。676m **不删样本**，只在数据卡 `DATASHEET.md` 中披露。
5. **`planted=true` 占 93%**：数据集固有特征，不修改，只在数据卡披露。**677a 补充**：这 93% 在
   `provenance` 口径下即 `self-authored`；剩下 7% 是 `source-derived-reconstruction` 而**非**
   `original-external-artifact`（后者计数为 0）。因此本库**不能**用于估计真实世界缺陷分布。

## 6. 676m 迁移结果快照

- `defect_type` 取值数：**56 → 33**
- 发生改写的样本：**308** / 1042
- 元标签拆分（`conditional_trigger` / `optimization_dependent`）：**80** 条
- `defect_location.file` 补全：**1042** / 1042
- 行号校正：+8 修正 **94** 条，已是绝对行号 **0** 条，未验证保持 **0** 条

迁移后分布：

| `defect_type` | n |
|---------------|---|
| `out_of_bounds` | 89 |
| `atomic_ub` | 65 |
| `deadlock` | 65 |
| `integer_overflow` | 57 |
| `bit_operation` | 51 |
| `memory_order` | 40 |
| `algorithm_misuse` | 35 |
| `iterator_invalidation` | 35 |
| `stl_container_ub` | 35 |
| `string_ub` | 35 |
| `logic_error` | 31 |
| `condition_variable` | 30 |
| `lambda_capture` | 30 |
| `move_semantics` | 30 |
| `raii_violation` | 30 |
| `smart_pointer` | 30 |
| `virtual_function` | 30 |
| `endianness` | 28 |
| `volatile_misuse` | 28 |
| `memory_leak` | 27 |
| `alignment` | 26 |
| `null_pointer_deref` | 24 |
| `use_after_free` | 24 |
| `linker_odr` | 23 |
| `type_punning` | 23 |
| `interrupt_safety` | 20 |
| `register_ub` | 20 |
| `uninitialized_read` | 20 |
| `data_race` | 18 |
| `double_free` | 15 |
| `strict_aliasing` | 13 |
| `other_ub` | 8 |
| `cross_tu_ub` | 7 |

---

复现：`.venv/Scripts/python.exe tools/fix_676m_schema.py --stage all`
