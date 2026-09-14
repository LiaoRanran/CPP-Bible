---
id: 482
title: 第四波范式级突破落地方案 证据网 诊断引擎 预测性 修剪 硬核 CurryHoward
status: active
type: architecture-note
created_at: 2026-09-14
---
# 482 第四波范式级突破落地方案
## evidence_graph + diagnostic_engine + 预测性 + 修剪机制 + 硬核声明

> 生成时间：2026-09-14
> 前置实测：28 颗原子中只有 2 条标准 relations（几乎全是 `relations: []`），知识图谱几乎不存在
> 来源：473 三个范式级突破方向 + 367 P5 流动与修剪 + 360 拉卡托斯硬核 + 294 Curry-Howard

---

## 一、evidence_graph.py（证据网索引，范式突破的基础）

### 1.1 问题

当前系统是"规则驱动"——每条规则独立检查，规则之间没有关联。红队发现一个问题，只能加一条规则，规则越来越多但系统不"理解"知识之间的关系。

实测：28 颗原子中只有 2 条标准 relations，知识图谱几乎不存在。

### 1.2 改法：证据网驱动

构建证据网索引，把"原子→证据卡→夹具→工件→断言"映射成图。系统不再只检查单条规则，而是能回答：
- 这个 claim 有哪些证据支撑？
- 这个证据卡服务于哪些原子？
- 这个夹具被哪些卡引用？
- 修改这个工件会影响哪些卡？

### 1.3 具体实现

#### 工具：tools/evidence_graph.py（约 200 行）

```python
# 伪代码
class EvidenceGraph:
    def __init__(self):
        self.nodes = {}  # id -> {type, path, metadata}
        self.edges = []  # (source, target, relation_type)
    
    def build(self):
        """扫描 atoms/ evidence/ Examples/ 构建图"""
        # 1. 扫描所有原子，提取 id/claim/evidence/relations
        # 2. 扫描所有证据卡，提取 id/serves/artifact/assertions
        # 3. 扫描所有夹具，提取被哪些卡引用
        # 4. 建立边：atom --serves--> evidence, evidence --uses--> fixture, fixture --produces--> artifact
        # 5. 建立边：atom --prerequisite--> atom, atom --specializes--> atom
    
    def query(self, node_id):
        """查询一个节点的所有关联"""
        return self.nodes[node_id], self.edges_from(node_id), self.edges_to(node_id)
    
    def impact_analysis(self, changed_file):
        """修改一个文件会影响哪些节点"""
        # 找到 changed_file 对应的节点
        # 反向遍历所有依赖它的节点
        # 返回受影响的原子/卡/夹具列表
    
    def export_json(self, path):
        """导出图为 JSON，供可视化"""
    
    def check_integrity(self):
        """检查图的完整性：孤儿节点、悬空引用、循环依赖"""
```

#### 第一阶段（只读，不改变现有流程）

- 只做索引和查询，不接入门禁
- 提供 `python tools/evidence_graph.py --impact <file>` 命令
- 提供 `python tools/evidence_graph.py --export` 导出 JSON

#### 第二阶段（接入门禁）

- 新增规则 EV-GRAPH-ORPHAN：证据卡不服务任何原子 → warn
- 新增规则 EV-GRAPH-DANGLING：卡引用的夹具不存在 → block
- 新增规则 ATOM-GRAPH-ISOLATED：原子无 relations 且无 evidence → warn

### 1.4 预期效果

- 修改一个夹具时，能立即知道影响哪些卡（不再需要全量 replay）
- 孤儿卡/悬空引用自动检测
- 为诊断引擎和预测性模块提供数据基础

---

## 二、diagnostic_engine.py（门禁红了→自动根因分析）

### 2.1 问题

门禁红了之后，Agent 需要人工分析"为什么红、怎么修"。ALLOC-002 的口径反转、LEAK-002 的观测反转，都是人花了大量时间才定位根因。

### 2.2 改法：诊断引擎

门禁红了之后，diagnostic_engine 自动：
1. 解析失败的规则和卡
2. 检查常见根因模式（工件过期、断言字面量错、编译器差异、sha 不匹配）
3. 给出修复建议（带具体命令和行号）

### 2.3 具体实现

#### 工具：tools/diagnostic_engine.py（约 250 行）

```python
# 伪代码
class DiagnosticEngine:
    def __init__(self, gate_result, replay_result):
        self.gate_result = gate_result
        self.replay_result = replay_result
    
    def diagnose(self):
        """对每个失败项，自动诊断根因"""
        diagnoses = []
        for failure in self.gate_result.failures + self.replay_result.failures:
            root_cause = self._match_pattern(failure)
            fix_suggestion = self._generate_fix(root_cause, failure)
            diagnoses.append({
                'failure': failure,
                'root_cause': root_cause,
                'confidence': 'high/medium/low',
                'fix_suggestion': fix_suggestion,
            })
        return diagnoses
    
    def _match_pattern(self, failure):
        """匹配已知根因模式"""
        patterns = [
            # 工件过期：sha 不匹配但卡内计数和旧工件一致
            ('artifact_stale', self._check_artifact_stale),
            # 断言字面量错：标签在 Linux .asm 中不存在
            ('assert_label_missing', self._check_assert_label),
            # 编译器差异：Windows 通过但 Linux 失败
            ('cross_compiler_diff', self._check_cross_compiler),
            # 夹具改动但工件没重生成
            ('fixture_artifact_mismatch', self._check_fixture_artifact),
            # 环境依赖：nproc/hardware_concurrency 进了断言
            ('env_dependent_key', self._check_env_dependent),
        ]
        for name, checker in patterns:
            if checker(failure):
                return name
        return 'unknown'
    
    def _generate_fix(self, root_cause, failure):
        """生成修复建议，带具体命令"""
        fixes = {
            'artifact_stale': '重新生成工件：python tools/asm_regen.py <fixture>',
            'assert_label_missing': '在 Linux .asm 中 grep 确认标签存在，改断言为 %s_... 模板',
            'cross_compiler_diff': '检查断言是否跨编译器通用，用 contains_any 替代精确匹配',
            'fixture_artifact_mismatch': '夹具改动后必须重生成工件并更新 sha',
            'env_dependent_key': '从 run_match_keys 中移除环境依赖键，或声明为仅留痕',
        }
        return fixes.get(root_cause, '需要人工分析')
```

### 2.4 验收

- 能自动定位 80%+ 的常见门禁失败根因
- 修复建议带具体命令和行号
- 高置信度（high）的诊断准确率 >90%
- 不自动修复，只给建议（修复权仍在 Agent/人）

---

## 三、预测性模块（生产前预测错误类型）

### 3.1 问题

当前是"消防模式"——生产完原子，红队找问题，门禁拦问题。能不能在生产前就预测"这颗原子容易出什么问题"？

### 3.2 改法：基于历史错误模式的预测

分析历史红队发现和门禁失败，建立错误模式库。生产新原子时，根据原子的特征（域、类型、复杂度、夹具类型）预测最可能出的问题类型。

### 3.3 具体实现

#### 数据基础

从 git log 和红队报告中提取历史错误：
- 错误类型（断言自证、口径不统一、工件过期、环境依赖、恒真断言...）
- 错误发生的原子特征（域、类型、夹具行数、断言数）
- 修复方式

#### 工具：tools/predictor.py（约 150 行）

```python
# 伪代码
class ErrorPredictor:
    def __init__(self):
        self.error_patterns = self._load_history()  # 从 docs/kernel/error_patterns.json 加载
    
    def predict(self, atom_draft):
        """根据草稿特征预测可能的错误类型"""
        features = self._extract_features(atom_draft)
        predictions = []
        for pattern in self.error_patterns:
            if self._matches(features, pattern.conditions):
                predictions.append({
                    'error_type': pattern.type,
                    'probability': pattern.probability,
                    'prevention': pattern.prevention,
                })
        return sorted(predictions, key=lambda x: x['probability'], reverse=True)
    
    def _extract_features(self, atom_draft):
        """提取特征：域、类型、夹具行数、断言数、是否多编译器、是否含性能数据..."""
```

#### 接入方式

- Writer 自检层调用 predictor，在生产前给出"这颗原子最容易出的 3 个问题"
- 不阻断生产，只作提示
- 预测准确率回溯评估（预测的问题是否真的被红队发现）

### 3.4 预期效果

- 生产前就能预警高风险问题
- Writer 可以针对性预防
- 红队可以重点检查预测的高风险项
- 预测准确率数据积累后，模型越来越准

---

## 四、修剪机制（过时规则/毒样例/原子自动归档）

### 4.1 问题

系统只有新增没有修剪：
- 规则从 21 涨到 51，39 条零命中
- 毒样例从 4 涨到 61，部分可能过时
- 原子从 0 涨到 28，部分可能被后续原子取代
- accept 从 0 涨到 17，全部没有过期时间

367 P5"流动与修剪"原理：系统必须有修剪机制，否则熵增导致信噪比持续下降。

### 4.2 改法：三级修剪

#### 级别 1：规则修剪（自动）

- 连续 3 个月零命中的规则 → 标记 `stale`，降为 advice
- 连续 6 个月零命中的规则 → 标记 `deprecated`，移入 archive/
- 每月自动运行 `python tools/prune.py --rules`

#### 级别 2：毒样例修剪（半自动）

- 毒样例对应的规则被删除/合并 → 毒样例也归档
- 毒样例连续 3 个月不触发对应规则 → 检查是否还有效
- 人工审核后归档

#### 级别 3：原子修剪（人工）

- 原子被后续原子完全取代（specializes 关系）→ 标记 `superseded`
- 原子的 claim 被新证据推翻 → 标记 `retracted`，不删除（保留历史）
- 人工审核后执行

### 4.3 具体实现

#### 工具：tools/prune.py（约 120 行）

```python
# 伪代码
def prune_rules(dry_run=True):
    """检查规则命中历史，标记 stale/deprecated"""
    # 从 git log 提取每条规则的最后命中时间
    # 3 个月零命中 → stale
    # 6 个月零命中 → deprecated
    # 输出报告，不自动删除（dry_run=True）

def prune_poison(dry_run=True):
    """检查毒样例有效性"""
    # 毒样例对应的规则是否还存在
    # 毒样例是否还能触发对应规则
    # 输出报告

def prune_accepts(dry_run=True):
    """检查 accept 过期"""
    # accept 超过 30 天 → 提醒复审
    # "预期中间态"在原子化后 → 自动清零
```

### 4.4 验收

- 每月自动生成修剪报告
- stale/deprecated 规则有明确归档路径
- 不自动删除任何东西（先标记，人工审核后再删）
- accept 有过期机制

---

## 五、硬核声明（拉卡托斯硬核+保护带边界）

### 5.1 问题

规则膨胀时没有边界——什么规则都能加，什么规则都能改。系统没有"哪些是核心不能动"的概念。

360 拉卡托斯硬核：知识系统有"硬核"（核心假设，不能轻易改）和"保护带"（辅助假设，可以调整）。

### 5.2 改法：定义阙疑的硬核

在 docs/kernel/hard_core.md 中定义：

#### 硬核（不能改，改了就不是阙疑了）

1. **机器可核验优先**：所有 claim 必须有可机器验证的证据
2. **三权分立**：Writer / 红队 / Gatekeeper 分离，不能自己写自己审
3. **证据链完整**：claim → 证据卡 → 夹具 → 工件 → sha，每一环可追溯
4. **fail-closed**：不确定时拒绝，不通过
5. **认可权唯人**：verified 状态必须人签，机器不能自封

#### 保护带（可以调整，但改了要记录）

- 具体规则的阈值和条件
- 工具的实现方式
- 流程的细节
- 提示词的版本

### 5.3 具体实现

1. 写 docs/kernel/hard_core.md，定义硬核 5 条
2. 每条硬核配 1-2 条毒样例（违反硬核的样例必须被拦）
3. gate_engine.py 中硬核规则标记 `hard_core: true`
4. 修改硬核规则需要人审 + 记录原因

### 5.4 验收

- 硬核 5 条有明确文档
- 每条硬核有毒样例守护
- 修改硬核规则需要特殊审批流程

---

## 六、Curry-Howard 同构落地（远期，claim 机器验证的理论基础）

### 6.1 原理

294 跨领域调研发现：Curry-Howard 同构——命题对应类型，证明对应程序。

阙疑的 claim 就是"命题"，证据卡+夹具+工件就是"证明"。如果 claim 能形式化为类型，证据就是证明，机器可以验证"证明是否证了命题"。

### 6.2 实用路径（不做完整形式化）

完整形式化（Lean/Coq）成本过高，不适合教学夹具场景。实用路径：

1. **claim 结构化**：claim 拆成 precondition / postcondition / invariant（288/298 已设计）
2. **断言映射**：每条断言对应 claim 的一部分（哪条断言证了哪个 postcondition）
3. **覆盖检查**：claim 的每个部分都有至少一条断言支撑 → 否则 warn
4. **矛盾检查**：两条断言互相矛盾 → block

### 6.3 具体实现（远期）

- 证据卡增加 `claim_coverage:` 字段，映射断言到 claim 的部分
- 新增规则 EV-CLAIM-COVERAGE：claim 的 postcondition 没有断言支撑 → warn
- 新增规则 EV-CLAIM-CONTRADICTION：两条断言矛盾 → block

### 6.4 依赖

- 先完成 claim 契约化（476 第一波 1.4）
- 先完成证据卡分层（480 第三项）
- 这两项是 Curry-Howard 落地的前提

---

## 七、六项的优先级与依赖

| 项 | 成本 | ROI | 优先级 | 依赖 |
|---|---|---|---|---|
| evidence_graph | 中（200 行） | 极高（范式基础） | P0 | 无 |
| diagnostic_engine | 中（250 行） | 高（减少人工分析） | P0 | evidence_graph（可选） |
| 修剪机制 | 低（120 行） | 高（防熵增） | P1 | 无 |
| 硬核声明 | 零（写文档+毒样例） | 中（边界清晰） | P1 | 无 |
| 预测性模块 | 中（150 行+数据积累） | 中（从消防到防火） | P2 | 历史错误数据积累 |
| Curry-Howard | 高（需要 claim 契约化先落地） | 远期（claim 机器验证） | P3 | claim 契约化 + 证据卡分层 |

**建议**：先做 evidence_graph（只读索引，不改变现有流程）+ diagnostic_engine（减少人工分析），然后修剪机制和硬核声明，最后预测性和 Curry-Howard。

---

## 八、和 476 计划的关系

这六项对应 476 第四波（范式级突破）：
- evidence_graph → 4.1
- diagnostic_engine → 4.2
- 预测性模块 → 4.3
- 修剪机制 → 4.4
- 硬核声明 → 4.5
- Curry-Howard → 4.6

476 第四波从 6 项扩展到 6 项（一一对应，但每项有了详细设计）。

### 关键修正

474 说"12 条 relations，44% 孤立"，实测是 **2 条标准 relations，几乎所有原子 relations 都是空的 `[]`**。知识图谱比预期更稀疏，evidence_graph 的优先级应该更高。
