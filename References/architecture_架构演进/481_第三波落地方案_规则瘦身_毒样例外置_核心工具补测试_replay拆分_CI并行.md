---
id: 481
title: 第三波落地方案 规则瘦身 毒样例外置 核心工具补测试 replay拆分 CI并行
status: active
type: architecture-note
created_at: 2026-09-14
---
# 481 第三波落地方案：规则瘦身与测试加固
## 死规则清理 + 毒样例外置 + 核心工具补测试 + replay 拆分

> 生成时间：2026-09-14
> 前置实测：11 个 500+ 行工具零测试（474 低估为 4 个），tests/poison/ 不存在，51 规则中 39 条零命中

---

## 一、死规则清理（39 条零命中规则评估）

### 1.1 问题

51 条规则中只有 12 条在实际门禁中有命中（24%），39 条零命中。23 条连毒样例都没有（45%）。

规则军备竞赛的另一面：规则数量从 21 涨到 51（143%），但有效规则只有 12 条。

### 1.2 改法：三分类处置

对 39 条零命中规则，按以下标准分类：

| 分类 | 标准 | 处置 |
|---|---|---|
| **A 类：有效但未触发** | 规则逻辑正确，存量数据都满足，新数据可能触发 | 保留，补毒样例 |
| **B 类：过严/过窄** | 规则条件太严格，几乎不可能触发 | 放宽条件或降级为 advice |
| **C 类：冗余/重复** | 和其他规则功能重叠 | 合并或删除 |
| **D 类：过时** | 针对已修复的问题，现在不再需要 | 降级为 deprecated，观察 1 个月后删除 |

### 1.3 具体操作

1. 写 `tools/rule_audit.py`（约 80 行）：
   - 对每条规则，统计历史命中次数（从 git log 中提取）
   - 检查是否有毒样例覆盖
   - 检查是否有其他规则功能重叠
   - 输出分类建议

2. 人工审核分类建议（不自动删除）

3. 处置：
   - A 类：补毒样例
   - B 类：放宽条件，先降 advice 观察
   - C 类：合并，保留更通用的那条
   - D 类：标记 deprecated，1 个月后删除

### 1.4 验收

- 39 条零命中规则全部有分类
- 有效规则率从 24% 提升到 60%+
- 不删除任何规则（先降级观察）

---

## 二、毒样例外置（从 poison_drill.py 抽到 tests/poison/*.yaml）

### 2.1 问题

61 条毒样例全部内嵌在 poison_drill.py（84KB）中，导致：
- 新增毒样例需要改 Python 代码
- 毒样例和规则逻辑混在一起，难以维护
- 无法独立验证毒样例的正确性

### 2.2 改法

把毒样例抽到 `tests/poison/*.yaml` 配置文件，poison_drill.py 只负责加载和运行。

### 2.3 YAML 格式设计

```yaml
# tests/poison/P01_example.yaml
id: P01
name: 空 verdict 应 block
rule: S2-EVIDENCE-VERDICT
severity: block
fixture: |
  ---
  id: EV-TEST-001
  # 故意缺 verdict
  ---
  正文
expected:
  block: true
  rule: S2-EVIDENCE-VERDICT
```

### 2.4 具体操作

1. 写 `tools/poison_loader.py`（约 50 行）：加载 tests/poison/*.yaml
2. 修改 poison_drill.py：从 loader 读取毒样例，不再内嵌
3. 把现有 61 条毒样例逐个转为 YAML（可以写转换脚本）
4. 保留阴性样例（应该通过的样例）

### 2.5 验收

- tests/poison/ 下有 61+ 个 .yaml 文件
- poison_drill.py 运行结果不变（61/61）
- 新增毒样例只需要加 .yaml 文件，不改 Python 代码
- pytest 全绿

---

## 三、核心工具补测试（11 个零测试工具）

### 3.1 问题

11 个 500+ 行工具零测试，包括：
- poison_drill.py 84KB（最大的工具之一）
- cppbible.py 28KB（主入口）
- compile_run_sanitize_pipeline.py 27KB
- gen_mkdocs_nav.py 24KB
- chapter_compile_check.py 29KB
- compile_all.py 22KB
- metrics_snapshot.py 22KB
- rewrite_links.py 24KB
- expand_assist.py 19KB
- book_asm_freshness.py 17KB
- expansion_audit.py 16KB

### 3.2 优先级排序

按"被依赖程度 × 代码复杂度"排序：

| 优先级 | 工具 | 理由 | 预估测试数 |
|---|---|---|---|
| P0 | poison_drill.py | 84KB，核心制衡层，被 CI 依赖 | 10+ |
| P0 | cppbible.py | 28KB，主入口，被 CI 依赖 | 8+ |
| P1 | compile_run_sanitize_pipeline.py | 27KB，编译管道 | 6+ |
| P1 | chapter_compile_check.py | 29KB，Book 编译检查 | 5+ |
| P1 | metrics_snapshot.py | 22KB，指标快照 | 5+ |
| P2 | gen_mkdocs_nav.py | 24KB，文档导航 | 3+ |
| P2 | compile_all.py | 22KB，全量编译 | 3+ |
| P2 | rewrite_links.py | 24KB，链接重写 | 3+ |
| P3 | expand_assist.py | 19KB | 2+ |
| P3 | book_asm_freshness.py | 17KB | 2+ |
| P3 | expansion_audit.py | 16KB | 2+ |

### 3.3 测试策略

- 每个工具至少补：1 个正常路径测试 + 1 个边界条件测试 + 1 个错误处理测试
- 优先测试纯函数（不依赖外部环境的）
- 依赖文件系统的测试用 tmp_path fixture
- 依赖编译器的测试用 mock（不实际编译）

### 3.4 验收

- P0 工具测试覆盖率 >60%
- P1 工具测试覆盖率 >40%
- 总测试数从 272 → 350+
- 所有新测试在 CI 中通过

---

## 四、replay 拆分（263 行 replay_card 拆成小函数）

### 4.1 问题

atom_evidence_replay.py 中 replay_card() 函数 263 行（:944-1206），是全仓最大的函数。包含：
- frontmatter 解析
- 编译
- 运行
- 工件校验
- sha 校验
- sanitizer 检查
- run_match 比对
- 工件还原

一个函数做太多事，难以测试和维护。

### 4.2 改法

拆成 6 个小函数：

```python
def replay_card(card_path):  # 保留入口，只做调度
    card = parse_card(card_path)       # 1. 解析
    result = compile_and_run(card)     # 2. 编译运行
    verify_artifact(card, result)      # 3. 工件校验
    verify_sha(card, result)           # 4. sha 校验
    verify_sanitizer(card, result)     # 5. sanitizer 检查
    match_output(card, result)         # 6. 输出比对
    restore_artifact(card)             # 7. 工件还原
    return verdict
```

### 4.3 具体操作

1. 先 Read atom_evidence_replay.py 的 replay_card 函数
2. 按功能拆分，每个函数 <50 行
3. 每个小函数补单元测试
4. 保持 replay_card 入口不变（外部调用不受影响）
5. 跑全量 replay 确认结果不变

### 4.4 验收

- replay_card 函数 <30 行（只做调度）
- 6 个小函数各有单元测试
- 全量 replay confirm 数不变（56）
- pytest 全绿

---

## 五、CI 并行化（37 步串行 → 并行）

### 5.1 问题

CI quality job 37 步全串行，占总耗时 50%。Set up Python 重复 5 次。

### 5.2 改法

按依赖关系分组并行：

```
job1: 内容审计（gate + poison + doc_lint + selfcheck）
job2: 编译验证（replay + compile_all + chapter_compile_check）
job3: 测试（pytest + coverage）
job4: 站点构建（mkdocs + gen_mkdocs_nav）
```

四个 job 并行，每个 job 内部串行。

### 5.3 具体操作

1. 修改 .github/workflows/ci.yml
2. 把 37 步分到 4 个 job
3. 去重 Set up Python（每个 job 一次）
4. 加 pip 缓存（463 CI1，零成本）
5. 确保 job 间依赖正确（需要共享 artifact 的用 upload-artifact/download-artifact）

### 5.4 验收

- CI 总耗时从 15min → <5min
- 4 个 job 并行
- Set up Python 从 5 次 → 4 次
- pip 缓存命中

---

## 六、五项的优先级与依赖

| 项 | 成本 | ROI | 优先级 | 依赖 |
|---|---|---|---|---|
| 核心工具补测试（P0 两个） | 高（写测试） | 极高（制衡层有测试） | P0 | 无 |
| 毒样例外置 | 中（转换+loader） | 高（维护性提升） | P0 | 无 |
| replay 拆分 | 中（重构+测试） | 高（可维护性+可测试性） | P1 | 核心工具补测试（先有测试再重构） |
| 死规则清理 | 中（审计+分类） | 中（信噪比提升） | P1 | 无 |
| CI 并行化 | 低（改 yml） | 中（15min→<5min） | P1 | 无 |

**建议**：先做核心工具补测试（P0 两个）+ 毒样例外置，然后 replay 拆分（有测试安全网），最后死规则清理和 CI 并行化。

---

## 七、和 476 计划的关系

这五项对应 476 第三波（规则瘦身与测试加固）：
- 死规则清理 → 3.1
- 毒样例外置 → 3.3
- 核心工具补测试 → 3.4（从 4 个修正为 11 个）
- replay 拆分 → 3.5
- CI 并行化 → 3.6

474 低估了零测试工具数量（4 个 → 实际 11 个），本方案已修正。
