# 510 知识生产流水线 · 规则自进化 · 文档治理 · Agent 质量保障

> 日期：2026-09-14
> 触发：用户要求"广泛调研相关项"
> 四方向并行调研：知识生产自动化、规则自进化、230+文档治理、Agent 质量保障与自修复
> 性质：业内先进实践 → 我们系统的落地方案

---

## 一、知识生产流水线自动化

### 1.1 业内模式

| 模式 | 来源 | 核心 |
|---|---|---|
| **验证中心设计** | Marco DeepResearch (arXiv 2603.28376) | 数据合成时加显式验证机制，verifier agent 专门验证答案正确性/难度/唯一性 |
| **自愈执行流水线** | AutoResearchClaw (arXiv 2605.20025) | 多agent辩论 + 自愈执行 + 可验证报告 + 跨run进化 + 人在环 |
| **Eval-Driven Development** | ilyaisaev.com | 新TDD：Golden Dataset → 跑Agent → 程序化评分（语义相似度+LLM-as-Judge） |
| **Claim 三阶段验证** | RIO World | 原子化声明→证据检索→NLI规则验证 true/false/unsupported |
| **自验证蒸馏** | James Trappett | 往返一致性+事实性检查+正确性检查三层过滤 |

### 1.2 我们的原子生产现状

当前流水线：
```
选题 → 写提示词 → 苦力写夹具 → 编译实测 → 证据卡 → 红队盲读 → 原子化 → 门禁
```

**已有的**：
- 夹具实测（真实编译，不编造）
- 证据卡（artifact+run_match 机器可验证）
- 红队两段式盲读
- 门禁全绿才原子化

**缺的**：
- 选题阶段没有"验证中心"——选题好坏靠直觉，没有 verifier
- 跨run进化——每批原子生产的教训没有自动回流到下批
- 程序化评分——质量靠红队人判，没有语义相似度自动评分
- Claim原子化——一条claim没有拆成原子化声明逐条验证

### 1.3 落地方案

**原子化 Claim 验证**（改证据卡格式）：
```
当前：claim: "屏障在循环体内阻止消除，但屏障≠原子类型"（一句散文）
改进：拆为原子声明
  claim_atoms:
    - id: a1
      statement: "在循环体内的屏障阻止编译器消除循环"
      evidence: [EV-CONC-001.assertion_3, EV-CONC-002.assertion_1]
      status: verified  # verified/refuted/unsupported
    - id: a2
      statement: "不在循环体内的屏障不阻止消除"
      evidence: [EV-CONC-001.assertion_5]
      status: verified
    - id: a3
      statement: "屏障不提供原子性"
      evidence: [EV-CONC-002.assertion_3]
      status: verified
```

**验证器自动检查**（L1机械层）：
- 每个原子声明必须挂≥1条 evidence
- evidence 指向的 assertion 必须 verdict=confirm
- 没有 evidence 的声明 → `status: unsupported` → gate WARN
- 证据与声明矛盾（evidence 说 refute 但 claim 说 verified）→ gate BLOCK

**跨run进化**：
- 每批原子生产结束后，把"本批踩的坑"自动写入 `data/production_lessons.jsonl`
- 下批生产前自动检索历史教训，注入提示词

---

## 二、规则自进化

### 2.1 业内模式

| 模式 | 来源 | 核心 |
|---|---|---|
| **并行规则生成** | RuleForge (arXiv 2604.01977) | 每个攻击生成5个并行规则候选，最多5轮迭代验证反馈 |
| **规则去重与复用** | GRIDAI (arXiv 2510.13257) | 先评估新攻击与现有规则关系，决定生成新规则还是优化现有 |
| **CTI→规则自动转化** | FALCON | 语义相似度评估，自动决定新规则vs优化现有 |
| **自愈安全** | Cisco Hypershield | AI自己写规则→自测试→自动部署，自愈闭环 |
| **移动目标防御** | Cloudflare | 短寿命轮换规则，攻击者来不及映射防御 |

### 2.2 我们的规则进化现状

当前：
```
对抗逃逸 → 人/苦力分析根因 → 写新规则 → 配毒样例 → pytest → 入库
```

**已有的**：
- 7轮对抗，每轮逃逸都转化为新规则（29→55条）
- 毒样例覆盖（68→72）
- 正反例pytest

**缺的**：
- 规则去重——新规则和旧规则是否重叠/矛盾，靠人判断
- 规则候选并行生成——一个逃逸只写一条规则，没探索多个方案
- 自动验证——规则写好后跑毒样例是自动的，但"规则是否过度泛化"靠人审
- 移动目标——规则是静态的，攻击者摸清后可以绕过

### 2.3 落地方案

**规则去重检查**（新规则入库前自动跑）：
```
新规则候选 R_new:
  1. 语义相似度：与现有55条规则做embedding cosine
     - >0.9 → 与现有规则高度重叠 → WARN（可能不需要新规则）
     - 0.7-0.9 → 部分重叠 → 建议合并
     - <0.7 → 真正新规则 → 入库
  2. 逻辑矛盾：新规则的block条件是否与现有规则的block条件矛盾
     - 同一输入触发两条规则，一条block一条pass → BLOCK（矛盾需人审）
  3. 覆盖检查：新规则必须至少有1个毒样例
```

**规则候选并行**（P2，好模型阶段）：
- 一个逃逸发现后，生成3个规则候选（不同实现方式）
- 每个候选跑全量毒样例+存量零误伤验证
- 选存量误伤最小、覆盖最准的候选入库
- 这个我们已经在做（红队发现→苦力写规则），但"3个候选并行"还没做

**规则老化与轮换**（P3，远期）：
- 规则入库时记录 `created_at` 和 `hits_count`
- 命中0次的规则（可能是过度泛化或已被更好规则替代）→ WARN 复查
- 频繁命中但误报高的规则 → 建议重写
- 这不是"移动目标防御"（那是安全产品的概念），而是规则库的健康度维护

---

## 三、230+ 架构文档治理

### 3.1 业内模式

| 问题 | 解决方案 |
|---|---|
| 重复内容 | 三级去重：精确hash → 模糊字符串 → 语义去重(cosine>0.9) |
| 找不到已有的 | Single Source of Truth——写之前先搜索 |
| 结构混乱 | 三维分类：领域×类型×受众 |
| 版本过期 | 季度审计，标准化checklist |
| RAG噪音 | 入库前去重，重复chunk会浪费context window |

### 3.2 我们的现状

- `References/architecture_架构演进/` 230+ 份文档，编号到509
- 已有 README_INDEX.md（369 批次建）
- 问题：
  1. **重复**：多轮调研可能覆盖同一方向（如多个文档都讲了RAG）
  2. **过时**：早期文档的数字/结论可能已被后续批次推翻
  3. **难找**：230+份，不知道哪份讲了什么
  4. **无版本**：同一主题多版本（v1/v2/v3）没有标注哪个是最终版

### 3.3 落地方案

**三级去重扫描**（一次性，~2h）：
```python
# tools/doc_dedup.py
# 1. 精确hash：SHA256(文件内容)，完全相同的标出
# 2. 模糊匹配：相似文本（difflib.SequenceMatcher > 0.8），near-duplicate
# 3. 语义去重：embedding cosine > 0.9（需要 Chroma，502 RAG L1 落地后）
# 输出：重复对列表 + 建议合并/保留
```

**文档生命周期标记**：
在每份文档 frontmatter 加：
```yaml
---
doc_id: 505
title: 系统架构总览
status: final  # draft/superseded/final
supersedes: [501, 502, 503, 504]  # 被哪些文档取代
superseded_by: []  # 取代了哪些
date: 2026-09-14
---
```

**README_INDEX 升级**：
- 加 `status` 列（draft/superseded/final）
- 加 `supersedes` 列
- 自动排序：final 在前，superseded 在后
- 重复文档不删除，标记 superseded（保留历史）

**季度审计checklist**：
- [ ] 新文档是否与现有文档重复？
- [ ] 数字是否与当前门禁基线一致？
- [ ] 设计是否已落地？（未落地的标 "design only"）
- [ ] superseded 文档是否还在被引用？

---

## 四、Agent 质量保障与自修复

### 4.1 业内模式

| 模式 | 来源 | 核心 |
|---|---|---|
| **Vera 三阶段红队** | arXiv 2607.01793 | 风险发现→组合攻击→证据验证，自增强pipeline |
| **GPT-Red** | OpenAI | 自动红队模型，对抗训练主模型 |
| **持续红队嵌入CI** | Galileo/AWS | 每次部署触发对抗扫描，blocking gate |
| **OPERA** | AAAI 2026 | 运行时attestation+审计agent+挑战-响应 |
| **Trace-based Testing** | Promptfoo | OpenTelemetry trace→agent trajectory→归一化分析 |
| **SITS2026 工程门槛** | CSDN | p95≤800ms, IAR≥98.7%, 全工具调用带provenance trace |

### 4.2 我们的现状

**已有的**：
- 7轮对抗（368→373→402→452→470→479→v80）
- 毒样例自动跑（68→72）
- 回归测试（pytest 366点）
- 零污染自证

**缺的**：
- **持续红队**：对抗是手动派的，没有嵌入CI每次自动跑
- **Trace归一化**：504设计了可观测性但还没落地
- **风险分类法**：每次对抗发现的逃逸没有结构化分类（Vera的taxonomy）
- **自修复**：发现逃逸→写规则→验证，这个循环靠人驱动
- **Provenance trace**：工具调用没有完整的"为什么调这个工具"的溯源

### 4.3 落地方案

**持续红队嵌入CI**（P1）：
```yaml
# .github/workflows/adversarial.yml
on: [push]  # 每次push自动跑
jobs:
  adversarial:
    runs-on: ubuntu-latest
    steps:
      - run: python tools/poison_drill.py  # 已有
      - run: python tools/adversarial_regression.py  # 新：历史逃逸回归
```

**历史逃逸回归**（`tools/adversarial_regression.py`）：
- 把每轮对抗发现的逃逸探针（_adv_v80/probes/*）沉淀为回归测试
- 每次CI自动跑，确认逃逸仍被修复
- 如果逃逸复现（规则被改坏了）→ CI红
- 这就是504的"回归锁"理念，扩展到对抗逃逸

**风险分类法**（结构化逃逸记录）：
```yaml
# data/adversarial_taxonomy.yaml
categories:
  - id: A1-TIMING
    name: 时序穿链
    description: 每步合规但组合绕过
    examples: [F02, E01]
  - id: A2-PARSING
    name: 解析走私
    description: 解析器不一致导致逃逸
    examples: [E07, F09]
  - id: A3-ASSERTION
    name: 断言判别力
    description: 断言恒真/恒假不可验证
    examples: [E03, N2]
  - id: A4-METADATA
    name: 元数据口径
    description: 字段名/类型/值不一致
    examples: [M5, M11]
```

每次新逃逸自动归类，同类逃逸超过3个 → 建议系统性修复（而不是逐个补丁）。

**自修复闭环**（P3，远期）：
```
对抗发现逃逸
  → 自动分类到 taxonomy
  → 自动生成规则候选（LLM）
  → 自动跑毒样例验证
  → 自动跑存量零误伤验证
  → 人审通过 → 自动入库
```

我们现在是手动版（对抗→人分析→苦力写规则→pytest→入库），P3 自动化中间三步。

---

## 五、四方向整合优先级

| 方向 | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| 知识生产流水线 | Claim原子化验证 | 跨run教训自动注入 | 程序化评分 | verifier agent |
| 规则自进化 | — | 规则去重检查 | 3候选并行 | 自修复闭环 |
| 文档治理 | — | 三级去重扫描 | 生命周期标记 | 季度审计自动化 |
| Agent质量保障 | — | 历史逃逸回归CI | 风险分类法 | 持续红队自动化 |

**P1 可立即做的**（一个苦力批次）：
1. Claim原子化验证（改证据卡格式+gate规则）
2. 规则去重检查（新规则入库前自动跑）
3. 三级去重扫描（一次性，230+文档）
4. 历史逃逸回归CI（把_adv_v80探针沉淀为测试）

---

## 六、一句话总结

四个方向补全了系统的"进化能力"：
1. **知识生产**：claim原子化+证据验证，不靠散文自报
2. **规则进化**：去重检查+候选并行，规则库不膨胀不矛盾
3. **文档治理**：230+文档去重+生命周期标记，不再越堆越乱
4. **质量保障**：历史逃逸回归CI+风险分类法，对抗不白打

至此 501-510 共 10 份架构文档，覆盖了从基础设施到智能层、从性能到治理、从生产到自进化的完整蓝图。

---

*文档编号 510。四方向并行调研内化。P1 四项可作为下一批苦力任务。*
