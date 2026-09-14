---
id: 429
title: 架构设计 错误模式库+Writer自检自动转化管道
status: active
type: architecture-note
created_at: 2026-09-13
---
# 429 架构设计：错误模式库 + Writer 自检自动转化管道

> 日期：2026-09-13。来源：422 反面教训系统化的原则二。当前流程：红队发现 E1/E2 → 人写进自检层 → 下次拦住。问题：人工转化慢，可能遗漏。本文设计 writer_checks.yaml 错误模式库 + 半自动化转化管道。

---

## 一、问题：错误模式的人工转化瓶颈

### 1.1 当前流程

```
红队发现 E1/E2 错误
  → 人读红队报告
  → 理解错误模式
  → 手写自检规则
  → 加入 Writer 自检层
  → 下次 Writer 自动拦住
```

**瓶颈**：
- 人工转化慢（每条错误模式需要 10-30 分钟）
- 可能遗漏（红队报告 15 条高级，人只转化了 5 条）
- 没有记录（哪些错误模式已经转化了？哪些还没？）
- 没有验证（转化后的自检规则真的能拦住同类错误吗？）

### 1.2 历史数据

第五批红队发现的 E1/E2 错误（部分）：
- 工件与断言不同代（EV-MEM-040）
- 断言字面量没在 Linux 工件实测（EV-MEM-040/041）
- .out 与 command 不同代
- 活性对照偏弱（全是编译期常量）
- 夹具注释里写带双引号的完整取值串（S3 误报）

这些错误模式中，只有"工件同代"和"断言字面量实测"被转化为 420 的 WC-01/WC-02。其他的还没有转化。

---

## 二、writer_checks.yaml 错误模式库

### 2.1 schema 设计

```yaml
# data/writer_checks.yaml
- id: WC-001
  name: artifact_same_generation
  error_type: E1  # E1形式/E2工件/E3断言/E4内容/E5流程/E6环境
  source: 第五批红队 EV-MEM-040
  source_date: "2026-09-12"
  description: "卡的 artifact_sha256 与重生成工件不一致"
  check_logic: |
    # 伪代码
    claimed_sha = card.artifact_sha256
    actual_sha = regenerate(card.command)
    return claimed_sha == actual_sha
  auto_fixable: false
  status: active  # active/deprecated/experimental
  intercept_rate: 0.8  # 历史 E1 错误回放拦截率
  false_positive_rate: 0.02  # 存量误报率
  last_verified: "2026-09-13"

- id: WC-002
  name: assert_labels_in_artifact
  error_type: E2
  source: 第五批红队 EV-MEM-040/041
  ...
```

### 2.2 字段说明

| 字段 | 说明 | 必填 |
|---|---|---|
| id | WC-NNN，唯一 | 是 |
| name | 检查名 | 是 |
| error_type | E1-E6 分类 | 是 |
| source | 来源（哪次红队/哪颗原子） | 是 |
| source_date | 发现日期 | 是 |
| description | 错误模式描述 | 是 |
| check_logic | 检查逻辑（伪代码） | 是 |
| auto_fixable | 是否可自动修复 | 是 |
| status | active/deprecated/experimental | 是 |
| intercept_rate | 历史错误回放拦截率 | 否 |
| false_positive_rate | 存量误报率 | 否 |
| last_verified | 最后验证日期 | 否 |

### 2.3 错误模式的生命周期

```
experimental（新加入，未验证）
  → 用历史错误回放验证拦截率
  → active（拦截率 ≥70%，误报率 ≤5%）
  → 持续监控
  → deprecated（被新规则替代或误报率过高）
```

---

## 三、半自动化转化管道

### 3.1 流程

```
红队报告（Markdown）
  → Step 1：提取 E1/E2 错误（正则/关键词）
  → Step 2：生成错误模式草稿（YAML 模板填充）
  → Step 3：人审确认（防止误判）
  → Step 4：加入 writer_checks.yaml
  → Step 5：实现检查逻辑（Writer 自检层）
  → Step 6：用历史错误回放验证拦截率
```

### 3.2 Step 1：自动提取

```python
def extract_errors_from_redteam_report(report_path):
    """
    从红队报告中提取 E1/E2 错误。
    匹配模式：
    - "E1" / "E2" 标签
    - "工件" / "断言" / "格式" 关键词
    - 阻断/高级/建议分级
    """
    # 用正则提取含 E1/E2 标签的段落
    # 输出：[{"error_type": "E1", "description": "...", "location": "..."}]
```

### 3.3 Step 2：生成草稿

```python
def generate_check_draft(error):
    """
    根据提取的错误，生成 writer_checks.yaml 草稿。
    id 自动递增（WC-003, WC-004, ...）
    status = experimental
    check_logic = 待实现（留 TODO）
    """
```

### 3.4 Step 3：人审确认

人审检查：
- 错误模式描述是否准确？
- error_type 分类是否正确？
- 是否与现有 WC 重复？
- 是否可机器检测？（不可检测的不加入）

### 3.5 Step 5-6：实现 + 验证

实现检查逻辑后，用历史 E1/E2 错误回放：
```python
def verify_intercept_rate(check_id, historical_errors):
    """用历史错误回放，计算拦截率。"""
    caught = sum(1 for e in historical_errors if run_check(check_id, e))
    return caught / len(historical_errors)
```

拦截率 ≥70% → active
拦截率 <70% → 改进检查逻辑或标记 experimental

---

## 四、与 Writer 自检层（420）的衔接

### 4.1 自检层从错误模式库加载

```python
# tools/writer_selfcheck.py
def load_checks():
    """从 data/writer_checks.yaml 加载所有 active 检查。"""
    checks = yaml.safe_load(open("data/writer_checks.yaml"))
    return [c for c in checks if c["status"] == "active"]
```

### 4.2 新增检查的流程

1. 红队发现新 E1/E2
2. 提取 → 生成草稿 → 人审 → 加入 writer_checks.yaml（status=experimental）
3. 实现检查逻辑
4. 历史错误回放验证拦截率
5. 拦截率 ≥70% → status=active
6. Writer 自检层自动加载新检查

**这就是"错误模式→自检规则"的自动转化管道**——从人工逐条写，变成"提取+草稿+人审+验证"的半自动化流程。

---

## 五、错误模式库的价值度量

### 5.1 覆盖率

```
错误模式覆盖率 = 已转化的 E1/E2 错误数 / 历史 E1/E2 错误总数
```

目标：≥80%

### 5.2 拦截率

```
自检拦截率 = 自检拦住的 E1/E2 错误数 / 总 E1/E2 错误数
```

目标：≥80%（420 的验收标准）

### 5.3 转化延迟

```
平均转化延迟 = 错误发现日期 → 自检 active 日期的平均天数
```

目标：≤7 天（当前是人工转化，可能 30+ 天）

---

## 六、落地计划

### 第一批（P1，苦力可干）

- [ ] 创建 data/writer_checks.yaml
- [ ] 把 420 的 7 项检查转化为 WC-001 到 WC-007
- [ ] 从第五批红队报告提取剩余 E1/E2，生成 WC-008+ 草稿
- [ ] tools/error_extractor.py 基础版（从红队报告提取 E1/E2）
- [ ] Writer 自检层改为从 writer_checks.yaml 加载

### 第二批（P2）

- [ ] 人审确认所有 experimental 草稿
- [ ] 实现新检查的检查逻辑
- [ ] 历史错误回放验证拦截率
- [ ] 覆盖率/拦截率/转化延迟的度量

### 第三批（P3）

- [ ] 与红队流程集成（红队报告自动触发提取）
- [ ] 错误模式库的趋势图（健康度仪表盘）

---

## 七、验收标准

- [ ] data/writer_checks.yaml 存在，≥7 条 active 检查
- [ ] 420 的 7 项检查全部转化为 WC-001~WC-007
- [ ] 从第五批红队报告提取 ≥3 条新错误模式草稿
- [ ] tools/error_extractor.py 可从红队报告提取 E1/E2
- [ ] Writer 自检层从 writer_checks.yaml 加载
- [ ] 历史错误回放拦截率 ≥70%
- [ ] 独立 commit

---

## 八、元结论

**错误模式库是阙疑的"经验数据库"——它记录了"我们历史上犯过哪些机械错误，以及如何拦住它们"。**

没有错误模式库，每次红队发现的错误都靠人记、人写、人验证——慢且容易遗漏。有了错误模式库，错误变成了可检索、可验证、可复用的资产。

**最关键的设计决策**：错误模式不是"写了就 active"，必须经过"历史错误回放验证拦截率 ≥70%"才能 active。这防止了"看起来有道理但实际拦不住"的检查污染自检层。

**与 426 时序约束框架的关系**：
- 426 解决"新规则怎么设计"（不变量约束范式）
- 429 解决"新检查从哪来"（错误模式自动转化）
- 两者结合 = 红队发现错误 → 自动提取模式 → 按不变量范式设计 → 验证拦截率 → active

这就是"从对抗到防御"的完整闭环。

累计 53 份（374-429）。
