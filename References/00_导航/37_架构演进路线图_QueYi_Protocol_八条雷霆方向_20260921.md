# 37. 架构演进路线图：QueYi Protocol 与八条雷霆方向

> **文档性质**：外部独立架构评审（2026-09-21）结论的产品经理内化与落地规划
> **评审来源**：国外大模型对"阙疑_人审预审查包"的第二波深度评审（八条雷霆方向）
> **当前阶段**：v2.5（验证驱动 Agent → 带统计与人审治理的验证系统）
> **目标阶段**：v3.0（独立验证的元系统 → QueYi Protocol）
> **文档状态**：规划草案，待用户拍板后进入执行

---

## 一、背景：为什么需要架构演进

### 1.1 项目当前定位

经过 560→616 共 57 个批次的建设，阙疑已经跨过了"给 LLM 加几个 prompt 和工具"的阶段，当前处于：

```
LLM Agent → 受约束 Agent → 验证驱动 Agent → 带统计与人审治理的验证系统
                                                              ↑
                                                         当前位置
```

外部独立评审的定性是：**"高水平个人研究原型 / 接近早期研究型工程系统"**，明显高于普通 Agent 项目，但还没到成熟研究系统或生产级基础设施。

### 1.2 当前最强的地方

不是工具数量（204 个），也不是代码量，而是已经开始处理普通 Agent 项目很少真正处理的问题：

- 规范漂移（specification drift）
- 验证器自洽（verifier self-consistency）
- 统计口径（statistical validity）
- Goodhart 漂移（metric gaming）
- 人工授权伪装成人审（batch authorization masquerading as item-by-item review）
- mirror shortcut（隐藏的 delegation 通道）
- 独立 verifier（independent verification）
- 证据 provenance（evidence provenance）

### 1.3 当前最大的瓶颈

外部评审的一句话判断：

> "你现在真正的瓶颈已经不是'想法够不够高级'，而是能不能把这个东西从'我设计得很聪明'推进到'一个不相信作者的人也能独立验证它确实有效'。"

这一步完成，项目等级会发生一次明显跃迁。

### 1.4 八条雷霆方向的来源

外部独立评审在完成 10 项人审预审查后，进一步给出了八条"能让阙疑换一个物种"的大方向。这八条不是零散的建议，而是一个完整的架构重构方案，之间有严格的依赖关系和层次逻辑。

---

## 二、八条雷霆方向：层次归类与依赖关系

### 2.1 四层架构

```
┌─ 架构层（系统是什么）─────────────────────────┐
│  雷1  QueYi Core 剥离（CPP-Bible 靶场化）      │
│  雷8  QueYi Protocol（接口化，外部可接入）      │
├─ 机制层（系统怎么进化）─────────────────────────┤
│  雷2  攻击者—验证者共同进化（adversarial loop） │
│  雷3  验证器攻击面（Verification Integrity Attack）│
│  雷7  验证能力时间轴（Verification Horizon）     │
├─ 对象层（系统验证什么）─────────────────────────┤
│  雷4  Proof-Carrying Knowledge（带证书知识对象）│
│  雷6  未知检测（ABSTAIN 不是失败而是能力）      │
└─ 治理层（谁有权力）─────────────────────────────┘
   雷5  人审变成 Trust Anchor（Model≠Verifier≠Authority）
```

### 2.2 依赖关系图

```
雷3（攻击面分类）──→ 雷2（攻击者目标函数）──→ 雷7（验证能力时间轴）
        ↑                    ↑
        │                    │
雷5（Authority 接口）──→ 雷4（PCK 结构）──→ 雷6（未知检测）
        │
        ↓
雷1（Core 剥离）──→ 雷8（Protocol 标准化）
```

**关键依赖链**：
1. 雷3 是雷2 的前置（没有攻击面分类，攻击者不知道优化什么）
2. 雷5 是雷4 的前置（PCK 的 certificate 需要 authority 字段）
3. 雷2+雷4 是雷7 的前置（能力时间轴需要进化机制和结构化对象）
4. 雷4 是雷6 的前置（未知检测是 PCK 的状态扩展）
5. 所有层稳定后才能做雷1（Core 剥离）
6. 雷1 稳定后才能做雷8（Protocol 标准化）

---

## 三、逐条雷霆方向详解

### 雷1：QueYi Core 剥离（CPP-Bible 靶场化）

**是什么**：把"阙疑"从 C++ Bible 里剥离出来，成为独立的验证内核。CPP-Bible 不再是项目本体，而是第一个大型实验环境（靶场）。

**为什么**：项目已经自然产生了一套与 C++ 本身无关的抽象：

```
claim → evidence → mutation → verifier → human authorization → confidence → provenance
```

这已经是协议/基础设施层的东西，不应该和 C++ 内容耦合。

**现状**：
- 所有工具都在 `tools/` 下，与 C++ 内容（atoms/evidence/Book/Examples）在同一仓库
- 验证逻辑和 C++ 特定逻辑（如 g++ 编译、MinGW artifact）混合在一起
- 没有明确的"验证内核接口"定义

**缺口**：
- Core 接口定义（Claim Schema / Evidence Schema / Verifier Interface / Authority Interface）
- 靶场适配层（C++ 特定逻辑从 Core 中剥离）
- 迁移路径（不破坏现有 57 批次的建设成果）

**落地路径**：
1. **阶段1（设计）**：定义 Core 接口规范，不实际迁移代码
2. **阶段2（试点）**：选 1-2 个工具做 Core 化试点，验证接口可行性
3. **阶段3（迁移）**：批量迁移验证工具到 Core，C++ 特定逻辑留在靶场层
4. **阶段4（多靶场）**：用第二个知识域（如数学）验证 Core 的可迁移性

**风险**：
- 迁移过程中可能破坏现有证据链
- Core 接口可能需要多次迭代才能稳定
- 过早剥离会拖慢演化速度

**决策点**：什么时候开始阶段1？建议 621+（等机制层和对象层稳定后）。

---

### 雷2：攻击者—验证者共同进化（Adversarial Evolution）

**是什么**：从"测试集验证"跃迁到"攻击者—验证者共同进化"。攻击者不再是固定 mutation 生成器，而是一个持续进化的 adversary，有明确的目标函数。

**为什么**：当前系统基本还是：

```
知识 → mutation → gate → 发现 bug → 修规则
```

下一代应该变成：

```
Claim → Attacker → Verifier → Patch → New Attacker → New Verifier → ...
```

这会让系统从 coverage-driven testing 升级成 adversarial evolutionary verification。

**现状**：
- mutation_fuzz 有 7 个算子（M1-M7），但是定向/随机构造，不是优化搜索
- 没有攻击目标函数
- 没有攻击者—验证者的迭代循环
- 没有"攻击难度"的度量

**缺口**：
- 攻击目标函数定义（maximize 什么）
- 攻击者搜索算法（怎么高效搜索最可能让验证系统犯错的变异）
- 攻击者—验证者迭代协议（攻击→验证→修复→再攻击的闭环）
- 攻击效果度量（Verification Failure Discovery Rate）

**攻击目标函数（建议）**：

```
maximize:
  - verifier_disagreement      （多个 verifier 判决不一致）
  - evidence_ambiguity          （证据解析歧义）
  - human_error_probability     （人审误判概率）
  - cross_model_disagreement    （跨模型判决不一致）
  - provenance_inconsistency    （溯源不一致）
  - rule_blind_spot             （规则盲区）
```

**落地路径**：
1. **618**：定义攻击目标函数 + 第一版 adversarial attacker（基于雷3 的攻击面分类）
2. **619**：攻击者—验证者迭代闭环 + Verification Failure Discovery Rate 指标
3. **620**：攻击难度度量 + 攻击者能力评估

**风险**：
- 攻击者和验证者可能共同过拟合
- 攻击可能是"钻实现空子"而不是"真实的语义攻击"
- 目标函数的权重需要仔细调

**决策点**：攻击目标函数的权重怎么定？是否需要多目标优化？

---

### 雷3：验证器攻击面（Verification Integrity Attack）

**是什么**：建立"验证器攻击面"，而不是只验证知识。把验证对象从 Claim 扩大成 Claim + Evidence + Verifier + Governance。攻击目标不是"让知识错误"，而是"让错误知识通过"。

**为什么**：你现在发现的 615/616 问题（EV-MATRIX 隐性预处理、CP peeking、Goodhart、mirror edge、批量人审）其实都可以被重新解释成"攻击 verification pipeline 的不同攻击面"。把它们系统化分类，项目理论会突然变得非常漂亮。

**现状**：已发现至少 6 类验证器攻击面：

| 攻击面 | 发现批次 | 状态 | 攻击向量 |
|---|---|---|---|
| EV-MATRIX 隐性预处理 | 615 B2 | 已修复（补全文档） | 规则定义与代码实现不一致 |
| CP 连续偷看 | 616 A | 已修复（CS 替代） | 统计口径误用 |
| Goodhart 漂移 | 615 C1 | 已建工具，未启用 | 指标被游戏化 |
| Mirror edge delegation | 外部评审指出 | 未处理 | 结构对称性替代语义判断 |
| 批量人审伪装 | 615 A1 | 已打标，未逐条复核 | 授权留痕冒充审查 |
| 规则-代码不一致 | 615 B2 | 已发现，未系统化 | 规范漂移 |

**缺口**：
- 攻击面系统化分类（完整的攻击面 taxonomy）
- 每类攻击面的检测方法
- 攻击面覆盖率度量
- 未知攻击面的发现机制（靠雷2 的 adversarial attacker）

**攻击面分类（建议 v1）**：

```
Verification Integrity Attack
├── Claim Layer
│   ├── Claim ambiguity（命题歧义）
│   └── Claim scope creep（命题范围蔓延）
├── Evidence Layer
│   ├── Evidence spoofing（证据伪造）
│   ├── Evidence parser differential（解析器差异）
│   └── Evidence provenance inconsistency（溯源不一致）
├── Rule Layer
│   ├── Rule ambiguity（规则歧义）
│   ├── Rule implicit preprocessing（隐性预处理）
│   └── Rule-spec divergence（规则-规范不一致）
├── Verifier Layer
│   ├── Verifier common-mode failure（共模失败）
│   ├── Verifier self-certification（自证）
│   └── Verifier blind spot（验证盲区）
├── Metrics Layer
│   ├── Metric gaming（指标游戏化 / Goodhart）
│   ├── Statistical peeking（统计偷看）
│   └── Selective reporting（选择性报告）
├── Human Layer
│   ├── Batch authorization masquerading（批量授权冒充审查）
│   ├── Mirror delegation（镜像委托）
│   ├── Automation bias（自动化偏见）
│   └── Human error inducement（诱导人审误判）
└── Provenance Layer
    ├── Timestamp manipulation（时间戳操纵）
    ├── Hash collision abuse（哈希碰撞滥用）
    └── History rewriting（历史重写）
```

**落地路径**：
1. **617（新增线H）**：攻击面分类台账 v1（基于已发现的 6 类，扩展到完整 taxonomy）
2. **618**：每类攻击面的检测方法 + 攻击面覆盖率度量
3. **619+**：未知攻击面发现（靠雷2 的 adversarial attacker）

**风险**：
- 分类可能不完整（未知攻击面无法预先分类）
- 检测方法可能误报/漏报

**决策点**：攻击面分类的粒度多细？是否需要每类都有自动化检测？

---

### 雷4：Proof-Carrying Knowledge（带证书知识对象）

**是什么**：把"知识卡"升级成 Proof-Carrying Knowledge。一张卡不只是"std::move 会发生什么"，而是携带一个完整 certificate。

**为什么**：这特别符合"阙疑"这个名字。教材渲染器可以规定 CERTIFIED / CONDITIONALLY_VERIFIED / ABSTAIN / DISPUTED / UNVERIFIED，教材只是 certificate 的一种可视化。

**现状**：
- 原子卡（atoms/）+ 证据卡（evidence/）已经是 PCK 的雏形
- 但是 markdown 格式，不是结构化的 certificate
- 没有统一的 certificate schema
- 没有证书验证工具

**PCK certificate 结构（建议）**：

```yaml
claim:
  id: CPP.MOVE.001
  statement: "std::move 会发生什么..."
  domain: C++
  type: inference | observation

evidence:
  - type: cppreference
    url: "..."
    hash: "..."
  - type: standard
    reference: "C++17 [class.copy]/32"
  - type: executable_example
    path: Examples/atoms/move_01.cpp
    artifact_sha256: "..."

negative_tests:
  - mutation_id: MUT-MOVE-001
    result: blocked
  - mutation_id: MUT-MOVE-002
    result: blocked

verifiers:
  - verifier_cpp_semantic_v1: pass
  - verifier_independent_v2: pass

cross_model:
  family_A: pass
  family_B: pass
  family_C: abstain

human_authority:
  status: authorized | conditionally_authorized | disputed | abstain
  reviewer: LiaoRanran
  timestamp: "2026-09-21T..."
  review_method: item_by_item | batch_authorization
  reason: "..."

uncertainty:
  cs_upper_bound: 0.009062
  cp_upper_bound: 0.003370
  estimand: finite_suite_escape_rate

provenance:
  commit: "a1b2c3d"
  artifact_hash: "..."
  verifier_signature: "..."
  first_authorized_at: "..."
  last_modified_at: "..."

expiry:
  expires_at: "2027-09-21"  # 可选，需要定期重验
  review_cycle: annual
```

**落地路径**：
1. **619**：PCK 数据结构定义 + 证书验证工具 + 第一批 Certified Knowledge Object（选 10 张卡试点）
2. **620**：PCK 批量迁移工具 + 证书渲染器（markdown → certificate）
3. **621+**：全量迁移 + 教材渲染器升级（基于 certificate 状态渲染）

**风险**：
- 迁移过程中可能丢失信息
- certificate schema 可能需要多次迭代
- 全量迁移工作量大

**决策点**：PCK 是用 YAML 还是 JSON？是否需要保留 markdown 作为人类可读格式？

---

### 雷5：人审变成 Trust Anchor（Human Authority）

**是什么**：把"人审"从一个步骤变成 Trust Anchor。Human 不再是 validator，而是 authority。AI 可以生成、攻击、验证、交叉验证、统计、提出结论，但只有 Human Authority 拥有 ACCEPT / REJECT / OVERRIDE / ABSTAIN 四种权力。

**为什么**：这比现在的"生成者不能兼任判断者"还更进一步。真正核心原则可以升级为：

> **No single principal may simultaneously generate, verify, and authorize a claim.**

整个系统形成 Model ≠ Verifier ≠ Authority 的三权分立。

**现状**：
- 人审权力已经明确（不自动 accept）
- 但是还没有 formalize 成接口
- 人审记录（human_attack_edge_annotations.jsonl）有，但没有统一的 authority 接口
- 没有明确的权力边界定义

**Human Authority 四种权力**：

| 权力 | 触发条件 | 审计要求 | 示例 |
|---|---|---|---|
| ACCEPT | 验证通过 + 人审确认 | 审查者 + 时间戳 + 理由 + 审查方法 | 30 条逐条复核通过 |
| REJECT | 验证不通过 + 人审确认 | 同上 + 拒绝理由 | 攻击边不成立 |
| OVERRIDE | 人审推翻机器判决 | 必须附详细理由 + 二次确认 | 机器判 blocked 但人审认为 equivalent |
| ABSTAIN | 人审无法判断 | 必须说明原因（信息不足/能力不足/争议） | 复杂语义争议 |

**落地路径**：
1. **619**：Authority 接口定义 + 四种权力的触发条件和审计要求 + 现有 388 条人审记录的 authority 化（标注 review_method=batch_authorization）
2. **620**：Authority 审计工具 + 权力使用统计 + OVERRIDE/ABSTAIN 的特殊处理流程
3. **621+**：Authority 接口接入 PCK（certificate 的 human_authority 字段）

**风险**：
- OVERRIDE 权力可能被滥用（人审频繁推翻机器判决）
- ABSTAIN 可能被用作"不想审"的借口
- 单用户阶段 Authority 的独立性有限（只有一个人）

**决策点**：OVERRIDE 是否需要二次确认？ABSTAIN 是否有时间限制（不能永远 abstain）？

---

### 雷6：未知检测（Unknown Detection / ABSTAIN）

**是什么**：做"未知检测"，而不只是错误检测。系统允许 TRUE / FALSE / UNKNOWN，甚至 SUPPORTED / REFUTED / UNDECIDED / INSUFFICIENT_EVIDENCE / CONFLICTED / STALE。ABSTAIN 不是失败，而是系统能力。

**为什么**：这与项目名"阙疑"完全契合。你的系统如果最后能做到"我不知道"，而且这个"不知道"本身有证据，那其实比"95% accuracy"更有意义。

**现状**：
- 判决系统是二值的（blocked / equivalent / escaped / n_a）
- n_a 有点像"无法判断"，但语义不明确
- 没有显式的 ABSTAIN 状态
- 保形预测（Conformal Prediction）讨论过弃权三态，但未实现

**判决状态扩展（建议）**：

```
当前：blocked | equivalent | escaped | n_a

扩展后：
├── VERDICT
│   ├── SUPPORTED（证据支持，验证通过）
│   ├── REFUTED（证据反驳，验证不通过）
│   └── ESCAPED（逃逸，验证未能拦截）
├── UNCERTAINTY
│   ├── UNDECIDED（论证框架无法判决，如循环攻击）
│   ├── INSUFFICIENT_EVIDENCE（证据不足，无法判断）
│   ├── CONFLICTED（证据冲突，多方判决不一致）
│   └── STALE（证据过期，需要重验）
└── AUTHORITY
    ├── AUTHORIZED（人审已授权）
    ├── CONDITIONALLY_AUTHORIZED（有条件授权）
    ├── DISPUTED（人审争议中）
    └── ABSTAIN（人审弃权）
```

**落地路径**：
1. **620**：ABSTAIN 三态判决原型（ACCEPT / REJECT / ABSTAIN）+ ABSTAIN 的证据要求
2. **621**：完整判决状态扩展 + 状态迁移逻辑 + 状态审计
3. **622+**：保形预测集成（逐卡片覆盖率保证 + ABSTAIN 触发条件）

**风险**：
- 状态太多可能增加系统复杂度
- ABSTAIN 可能被滥用（系统遇到难题就 abstain）
- 状态迁移逻辑需要仔细设计

**决策点**：ABSTAIN 的触发条件是什么？是否需要"ABSTAIN 率"的上限？

---

### 雷7：验证能力时间轴（Verification Capability Curve）

**是什么**：做一条"验证能力时间轴"，不只统计 escape = 1/1406，而是记录 Verifier Capability Curve——v1 能挡多少？v2 能挡多少？v3 新攻击能否突破？v4 跨模型还能不能挡？v5 新 domain 是否成立？

**为什么**：这会让"随模型能力连续放权"的概念真正落地。甚至可以定义 Verification Horizon——验证器能够可靠覆盖的最大攻击复杂度。

**现状**：
- v1-v7 基线已经有了（mutation_fuzz 的 7 个版本）
- 但是没有系统化成 capability curve
- 没有"攻击难度"的度量
- 没有跨版本的攻击迁移分析

**Verification Capability Curve（建议）**：

```
Attack Difficulty
      ↑
      │                     ● v7
      │                ● v6
      │           ● v5
      │      ● v4
      │  ● v3
      │● v2
      │● v1
      └──────────────────────→ Verifier Generation
```

每个点代表：在该版本验证器下，能被拦截的攻击的最大难度。曲线上升说明验证能力在提升。

**Verification Horizon（建议）**：

```
当前验证系统能够可靠处理的最大攻击复杂度。

类似 METR 用 task-completion time horizon 衡量 Agent 能做多长时间的人类任务，
阙疑可以研究：当前验证系统能够可靠覆盖多高复杂度的知识攻击？
```

**落地路径**：
1. **620**：v1-v7 Verification Capability Curve 重建 + 攻击难度度量 v1
2. **621**：Verification Horizon 定义 + 跨版本攻击迁移分析
3. **622+**：跨模型/跨 domain 的 capability 评估

**风险**：
- 攻击难度的度量可能主观
- 历史版本的复现可能有困难
- 曲线可能被游戏化（专门造容易的攻击让曲线好看）

**决策点**：攻击难度怎么度量？是基于攻击的复杂度、还是基于攻击被发现的难度？

---

### 雷8：QueYi Protocol（协议化）

**是什么**：最后形成"QueYi Protocol"，而不是 QueYi App。外部项目只要实现接口，就能接入 queyi claim / evidence / mutate / attack / verify / certify / replay。

**为什么**：这是终局形态。那时候 C++ Bible 是一个应用，工程数学教材是另一个应用，以后甚至可以有 QueYi-C++ / QueYi-Math / QueYi-Embedded / QueYi-Law / QueYi-Finance。

**现状**：
- 工具已经有 CLI 接口
- 但是没有标准化的协议规范
- 没有外部接入的能力
- 没有多 domain 支持

**QueYi Protocol 架构（建议）**：

```
                 QueYi Protocol
                        │
        ┌───────────────┼────────────────┐
        │               │                │
    Producer        Attacker         Verifier
    （生成知识）    （攻击知识）     （验证知识）
        │               │                │
        └───────────────┼────────────────┘
                        │
              Evidence Graph（证据图）
                        │
              Uncertainty Layer（不确定层）
                        │
              Human Authority（人审权力）
                        │
              Provenance / Ledger（溯源账本）
                        │
              Certified Artifact（认证工件）
```

**Protocol 接口（建议）**：

```
queyi claim      # 注册/查询知识声明
queyi evidence   # 注册/查询证据
queyi mutate     # 生成变异体
queyi attack     # 发起验证完整性攻击
queyi verify     # 执行验证
queyi certify    # 生成证书
queyi replay     # 重放验证
queyi authority  # 人审权力操作
queyi provenance # 溯源查询
```

**落地路径**：
1. **625+**：Protocol 规范 v1（接口定义 + 数据结构 + 验证流程）
2. **626+**：Protocol 参考实现（基于 QueYi Core）
3. **627+**：第二个靶场接入（如数学教材），验证 Protocol 的可迁移性
4. **远期**：多 domain 支持 + 外部社区接入

**风险**：
- Protocol 标准化可能过早（Core 还在快速演化）
- 多 domain 支持可能稀释 C++ 靶场的深度
- 外部接入需要社区建设

**决策点**：什么时候开始 Protocol 标准化？建议等 Core 稳定（至少 6 个月无重大接口变更）后再做。

---

## 四、核心指标：Verification Failure Discovery Rate

### 4.1 定义

不是问"我测了多少？"，而是问：

> **在相同预算下，我这个系统还能主动发现多少此前未知的验证漏洞？**

### 4.2 为什么这个指标重要

传统的验证指标（覆盖率、逃逸率、通过率）都是"向后看"的——衡量已经做了多少验证。

Verification Failure Discovery Rate 是"向前看"的——衡量系统还能发现多少新问题。这会逼着整个系统从"工程门禁"变成真正的自我压力测试系统。

### 4.3 指标计算（建议 v1）

```
VFDR = (新发现的验证漏洞数) / (验证预算)

其中：
- 新发现的验证漏洞 = 此前未知的、能让错误知识通过验证的攻击
- 验证预算 = 计算时间 + 人工时间 + 攻击尝试次数
- 时间窗口 = 每批次 / 每月 / 每季度
```

### 4.4 子指标

```
├── Attack Surface Coverage（攻击面覆盖率）
│   = 已覆盖的攻击面类别数 / 总攻击面类别数
├── Unknown Attack Discovery Rate（未知攻击发现率）
│   = 新发现的攻击面类别数 / 时间窗口
├── Verifier Disagreement Rate（验证器不一致率）
│   = 多 verifier 判决不一致的案例数 / 总案例数
├── Human Override Rate（人审推翻率）
│   = 人审 OVERRIDE 次数 / 人审总次数
└── Attack Effectiveness（攻击有效率）
    = 成功让错误知识通过的攻击数 / 总攻击尝试数
```

### 4.5 落地路径

1. **618**：VFDR 指标定义 v1 + 子指标定义
2. **619**：VFDR 自动化采集 + 仪表盘
3. **620+**：VFDR 趋势分析 + 与六维度评分的关联分析

---

## 五、落地路径：617→625+ 批次安排

### 5.1 近期（617-620）：机制层与对象层建设

| 批次 | 主题 | 对应雷 | 核心产出 | 状态 |
|---|---|---|---|---|
| **617** | 从修复到落地 + 攻击面初步分类 | 雷3（部分） | CS 对外启用 / 他验试点 / 30条逐条复核预标注 / **验证器攻击面分类台账 v1** | 提示词已写，待投喂 |
| **618** | 攻击者目标函数 + 攻击框架 | 雷2+雷3 | mutation 目标函数定义 / 第一版 adversarial attacker / 攻击面攻击框架 / VFDR 指标 v1 | 待规划 |
| **619** | Human Authority + PCK 雏形 | 雷5+雷4 | Authority 接口（4种权力） / PCK 数据结构 / 第一批 Certified Knowledge Object / 证书验证工具 | 待规划 |
| **620** | 未知检测 + 验证能力时间轴 | 雷6+雷7 | ABSTAIN 三态判决 / v1-v7 Verification Capability Curve / Verification Horizon 度量 / VFDR 自动化采集 | 待规划 |

### 5.2 中期（621-624）：架构层设计与试点

| 批次 | 主题 | 对应雷 | 核心产出 |
|---|---|---|---|
| **621** | QueYi Core 接口设计 | 雷1（阶段1） | Core 接口规范（Claim/Evidence/Verifier/Authority）/ 靶场适配层设计 / 迁移路径 |
| **622** | Core 化试点 | 雷1（阶段2） | 选 2-3 个工具做 Core 化试点 / 接口可行性验证 / 迭代接口规范 |
| **623** | 保形预测集成 + 跨模型验证 | 雷6（深化） | 保形预测逐卡片覆盖率保证 / 跨模型判决不一致检测 / CONFLICTED 状态 |
| **624** | 多 domain 可行性研究 | 雷1（验证） | 选第二个知识域（如数学）做可行性研究 / Core 可迁移性验证 |

### 5.3 远期（625+）：Protocol 标准化与生态

| 批次 | 主题 | 对应雷 | 核心产出 |
|---|---|---|---|
| **625** | QueYi Protocol 规范 v1 | 雷8 | Protocol 接口定义 / 数据结构 / 验证流程 / 安全模型 |
| **626** | Protocol 参考实现 | 雷8 | 基于 QueYi Core 的 Protocol 实现 / 接入文档 / 示例应用 |
| **627** | 第二个靶场接入 | 雷1+雷8 | 数学教材靶场接入 / Protocol 可迁移性验证 / 多 domain 支持 |
| **远期** | 生态建设 | 雷8 | 外部社区接入 / 多 domain 支持 / 标准化组织推进 |

### 5.4 与现有路线图的关系

| 现有路线图方向 | 新架构中的定位 | 调整 |
|---|---|---|
| 学习者镜像（Learner Twin） | 降级为可选功能，等门开（≥50 条真实学习行为）再做 | 从"下一个跃迁"降级为"可选增强" |
| 六维度评分 | 保留，但增加 VFDR 作为第七维度 | 从"内部仪表盘"升级为"核心指标" |
| 信任根四层纵深 | 保留，归入 Provenance Layer | 与雷8 的 Protocol 溯源层对接 |
| 论证层（Dung AF / W2） | 保留，归入 Verifier Layer | 与雷2 的 adversarial evolution 对接 |
| CI/CD 全绿 | 保留，作为基础设施 | 不直接对应八条雷 |

---

## 六、风险与挑战

### 6.1 技术风险

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| 攻击者和验证者共同过拟合 | 攻击看起来有效但实际是钻实现空子 | 攻击必须经过"语义有效性"验证；跨模型验证 |
| PCK 迁移丢失信息 | 全量迁移过程中可能丢失 markdown 中的细节 | 增量迁移；保留 markdown 作为人类可读格式；迁移校验工具 |
| Core 接口不稳定 | 接口频繁变更导致迁移成本高 | 先做设计和试点，接口稳定后再批量迁移 |
| VFDR 被游戏化 | 专门造容易的攻击让 VFDR 好看 | VFDR 必须结合攻击难度度量；人工审计 VFDR 异常 |

### 6.2 治理风险

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| OVERRIDE 权力滥用 | 人审频繁推翻机器判决，破坏验证系统的权威性 | OVERRIDE 必须附详细理由 + 二次确认；OVERRIDE 率监控 |
| ABSTAIN 滥用 | 系统遇到难题就 abstain，逃避判断 | ABSTAIN 必须说明原因；ABSTAIN 率上限；ABSTAIN 有时间限制 |
| 单用户 Authority 独立性有限 | 只有一个人审，独立性不足 | 长期目标是多 reviewer；短期靠审计留痕和外部评审 |
| 批量授权冒充审查 | 388 条人审实为 batch_authorization | 已打标；30 条逐条复核；Authority 接口强制 review_method 字段 |

### 6.3 进度风险

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| 八条雷同时做导致范围过大 | 每批都做不完，质量下降 | 严格按依赖关系排序，一批只做 1-2 条雷的核心部分 |
| 过早做 Core 剥离 | 拖慢演化速度，接口频繁变更 | Core 剥离放在 621+，等机制层和对象层稳定后再做 |
| 学习者镜像被完全忽略 | 用户之前投入的学习者镜像工作被浪费 | 学习者镜像降级为可选功能，等门开再做，不删除已有工作 |

---

## 七、决策点（需要用户拍板）

### 7.1 立即决策（影响 617）

1. **617 是否新增线H（验证器攻击面分类台账 v1）？**
   - 建议：是。成本低（文档+台账），是雷2 的前置依赖。
   - 影响：617 从 22 个任务增加到 23-24 个任务。

2. **学习者镜像是否正式降级为可选功能？**
   - 建议：是。等门开（≥50 条真实学习行为）再做。
   - 影响：617 不再包含学习者镜像相关任务（617 本来也没有）。

### 7.2 短期决策（影响 618-620）

3. **攻击目标函数的权重怎么定？**（618）
   - 选项A：等权重（6 个目标各占 1/6）
   - 选项B：人工指定权重（基于重要性）
   - 选项C：多目标优化（Pareto 前沿）
   - 建议：先选项A（等权重），跑几轮后再调。

4. **PCK 用 YAML 还是 JSON？**（619）
   - 建议：JSON（机器友好）+ YAML 作为人类可读格式（自动转换）。

5. **OVERRIDE 是否需要二次确认？**（619）
   - 建议：是。OVERRIDE 是最强的人审权力，必须二次确认 + 详细理由。

### 7.3 中期决策（影响 621+）

6. **什么时候开始 QueYi Core 剥离？**
   - 建议：621（等机制层和对象层稳定后）。
   - 条件：617-620 完成，攻击面分类 + adversarial attacker + Authority 接口 + PCK 雏形都稳定。

7. **第二个靶场选什么？**
   - 选项A：数学（确定性系统，与 C++ 同谱系）
   - 选项B：电子（半确定系统，用户感兴趣的方向）
   - 选项C：金融（概率系统，高风险高价值）
   - 建议：先数学（与 C++ 最接近，验证 Core 可迁移性），再电子，最后金融。

### 7.4 远期决策（影响 625+）

8. **什么时候开始 QueYi Protocol 标准化？**
   - 建议：625（等 Core 稳定至少 6 个月无重大接口变更后）。

9. **是否推进标准化组织（如 W3C / IETF）？**
   - 建议：远期。等 Protocol 有多个实际应用后再推进。

---

## 八、总结

### 8.1 八条雷的本质

八条雷霆方向不是八个独立的功能，而是一个完整的架构重构方案。它们的本质是：

> **把阙疑从"我设计得很聪明"推进到"一个不相信作者的人也能独立验证它确实有效"。**

具体来说：
- 雷3（攻击面分类）让别人知道你可能在哪犯错
- 雷2（adversarial evolution）让系统主动找自己的错
- 雷5（Human Authority）明确谁有最终权力
- 雷4（PCK）让每个结论都带可验证的证书
- 雷6（未知检测）让系统敢于说"我不知道"
- 雷7（能力时间轴）让验证能力可度量
- 雷1（Core 剥离）让验证内核与知识域解耦
- 雷8（Protocol）让别人能接入你的验证体系

### 8.2 核心指标

Verification Failure Discovery Rate 把所有层串起来——不是问"测了多少"，而是问"在相同预算下还能主动发现多少此前未知的验证漏洞"。

### 8.3 与项目名的契合

这八条雷的终极形态与"阙疑"完全契合：

- 阙疑 = "多闻阙疑，慎言其余"（《论语》）
- 拿不准的宁可标"存疑"也不硬说
- 雷6（未知检测）让系统敢于说"我不知道"
- 雷5（Human Authority）让人审成为最终的"慎言"权力
- 雷4（PCK）让每个"言"都带可验证的证据
- 雷8（Protocol）让"阙疑"从一个项目变成一套协议

### 8.4 下一步行动

1. **立即**：用户拍板 7.1 的两个决策（617 是否加线H / 学习者镜像是否降级）
2. **617**：投喂执行（含线H 攻击面分类台账 v1）
3. **618 前**：完成 618 提示词（攻击者目标函数 + 攻击框架 + VFDR 指标）
4. **持续**：每批结束后更新本文档的进度状态

---

**文档版本**：v1.0（2026-09-21）
**编写者**：产品经理（MainAgent）
**评审来源**：外部独立架构评审（国外大模型，2026-09-21）
**文档状态**：规划草案，待用户拍板后进入执行
