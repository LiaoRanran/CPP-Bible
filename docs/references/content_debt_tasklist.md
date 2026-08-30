# 内容债务任务单（悬空引用 + 一致性 WARN）

> 生成：2026-08-30
> 数据源：`tools/dangling_ref_linter.py`（55 处悬空章号引用）、`tools/consistency_check.py`（30 WARN 立场标签）
> 原则：**不盲猜改号**——每条引用先按语义上下文建立「旧号 → 现章」映射，人工抽查后再落笔（对应审计报告 §9 路径 2）。

## 1. 悬空章号引用（55 处）

### 1.1 保留空号清单（18 个，正文引用到其中 13 个）

`33, 34, 53, 54, 55, 56, 57, 58, 59, 73, 74, 75, 102, 103, 104, 105, 106, 114`

### 1.2 按文件分布

| 文件 | 引用数 | 涉及空号 |
|------|-------:|----------|
| part03_language/ch19_variables.md | 7 | 33×4, 102×3 |
| part03_language/ch20_reference_pointer.md | 6 | 33×3, 54×2, 56×1 |
| part03_language/ch25_union_variant.md | 5 | 34×3, 59×2 |
| part03_language/ch26_lambda.md | 4 | 59×4 |
| part03_language/ch28_lifetime_ub.md | 3 | 33×3 |
| part04_memory/ch36_stack_heap.md | 2 | 33×2 |
| part04_memory/ch37_new_delete.md | 2 | 33×2 |
| part06_templates/ch60_template_basics.md | 1 | 75 |
| part06_templates/ch66_sfinae.md | 1 | 75 |
| part06_templates/ch67_concepts.md | 2 | 75×2 |
| part05_oo/ch51_crtp.md | 2 | 73×2 |
| part07_stl/ch93_thread_async.md | 4 | 102,103,104,105 |
| part07_stl/ch94_stop_token.md | 3 | 102,103,105 |
| part10_modern/ch116_perfect_forwarding.md | 1 | 102 |
| part15_cases/ch159_threadpool.md | 2 | 104,105 |
| part15_cases/ch160_mempool.md | 1 | 104 |
| part15_cases/ch161_logger.md | 1 | 104 |
| part01_history/ch01_c_history.md | 2 | 34, 59 |
| part01_history/ch09_cpp26.md | 2 | 74, 114 |
| **合计** | **55** | |

### 1.3 建议映射（基于上下文语义，**需人工逐条确认**）

| 空号 | 现章/替代 | 依据（从引用上下文） |
|------|-----------|----------------------|
| ch33（悬垂/生命周期） | 已并入 `ch28_lifetime_ub`（生命周期与 UB） | 引用上下文均为"返回局部引用悬垂/生命周期" |
| ch34（异常安全/valueless） | `ch40_exception_safety`（异常安全） | 引用上下文为"异常安全与 valueless" |
| ch54/ch56（虚继承内存布局） | `ch49_virtual_inheritance` 或 `ch50_multiple_inheritance` | 引用上下文为"虚继承内存布局/引用成员存储" |
| ch59（模板推导） | `ch61_template_overload` 或 `ch60_template_basics` | 引用上下文为"模板推导规则" |
| ch73（CRTP 进阶） | `ch51_crtp`（CRTP 章本体） | 引用上下文为"CRTP 进阶/奇异递归" |
| ch75（模板报错可读性） | 无独立章；可指向 `ch67_concepts`（Concepts 改善报错） | 引用上下文为"报错可读性" |
| ch74（反射专章） | 无现章；建议改为指向 ch09（C++26 演进）或删改 | 反射未成章 |
| ch102-106（并发原语） | 实际对应 `part09_concurrency`：ch107_atomic/ch108_memory_order/ch109_fence/ch110_lockfree/ch111_aba/ch112_hazard_rcu/ch113_coroutine | 引用上下文为 mutex/condition_variable/并发；当前并发章从 ch107 开始，编号偏移 5 |
| ch114（异步执行器） | `ch93_thread_async` 或 `ch113_coroutine` | 引用上下文为"异步组合/执行器" |

### 1.4 处理策略

- **批量替换候选**：ch102→107、ch103→108、ch104→109、ch105→110（并发偏移 +5）——**先验证语义再改**；
- **ch33→ch28**、**ch34→ch40**、**ch73→ch51** 语义明确，可机械替换；
- ch54/ch56→ch49/ch50、ch59→ch61、ch75→ch67 需逐条看上下文判断；
- ch74/ch114 无稳定目标，建议**改写句子**（去掉章号或指向泛化章节）。

## 2. 前置元数据问题（7 处，`prereq_topo_check.py` 实测）

### 2.1 拓扑倒置（6 处，`前置章号 > 自身章号`）

| 文件 | 自身 | 前置 | 说明 |
|------|-----:|-----:|------|
| part01_history/ch07_cpp20.md | 7 | 60 | 前置指向模板章（倒置） |
| part01_history/ch07_cpp20.md | 7 | 63 | 前置指向模板章（倒置） |
| part01_history/ch09_cpp26.md | 9 | 67 | 前置指向 Concepts 章（倒置） |
| part01_history/ch09_cpp26.md | 9 | 113 | 前置指向协程章（倒置） |
| part03_language/ch19_variables.md | 19 | 20 | 前置指向引用章（倒置） |
| part03_language/ch19_variables.md | 19 | 31 | 前置指向运算符章（倒置） |

### 2.2 悬空前置（1 处）

| 文件 | 自身 | 前置 | 说明 |
|------|-----:|-----:|------|
| part01_history/ch09_cpp26.md | 9 | 114 | 指向保留空号（无此章） |

> 处理：这些前置在 `SUMMARY.md` 的前置元数据中（`前置：` 字段），是**作者有意的前瞻引用**（历史/演进章提及未来主题）。若保持"倒置"需工具放行；若改，则改为移除或标注为"前瞻（见后续章）"。

## 3. 一致性 WARN（30 处，立场标签缺失）

`consistency_check.py` 报告 30 个 WARN，均为章节缺少 `[标准]/[实现]/[平台]/[经验]` 立场分层标签。完整清单需复跑导出：

```bash
python tools/consistency_check.py 2>&1 | Select-String "WARN"
```

已知涉及（前序会话）：ch04、ch22、ch31、ch36、ch38、ch42-44、ch47-49、ch60-66、ch120、ch135-136、ch140、ch143、ch157-159、ch162-165 等。

**处理**：非机械补标签——需逐章确认是否"确实缺少立场标注"还是"用词与工具识别规则不一致"（与 `verification_audit.py` 137/147 不一致的根因）。

## 4. 执行顺序建议

1. 先复跑 `prereq_topo_check.py` 与 `consistency_check.py` 导出精确 JSON 明细；
2. 对 ch33/ch34/ch73/ch102-105 等语义明确项建立**映射表文件**（`docs/references/chapter_mapping.md`）并通过代码审查；
3. 分 part 小批修改 → 每批跑 `quality` + `compile` + `exempt audit`；
4. 全部清零后把 `dangling_ref_linter` / `prereq_topo_check` 从软门禁转硬（CI `continue-on-error: false`）。