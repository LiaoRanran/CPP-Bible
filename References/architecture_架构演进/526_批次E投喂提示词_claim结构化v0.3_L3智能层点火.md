# 526 批次E投喂提示词 · claim结构化 v0.3（L3智能层点火）

> 投喂对象：晚上好模型（理解claim语义）
> 路径：`C:\CodeLearnling\note\note\C++\CPP-Bible`
> 性质：这不是格式整理，是L3智能层的点火。做完后知识图谱从"文件图"长出"概念图"，验证从"一刀切"变成"按命题类型分流"。

---

## 〇、先读这三个文件再动手（禁止凭记忆）

1. `atoms/conc/ATOM-CONC-FENCE-001.md`（最成熟原子，本批样板）
2. `tools/gate_engine.py` 的 `_register_all`（看现有规则怎么注册、severity、毒样例怎么挂）
3. `tools/knowledge_graph.py` 的 SCHEMA（line 49-68）和 build()（看节点怎么进图）

---

## 一、为什么（一句话）

现在 claim 是≤50字自然语言，机器无法判断"两个claim是否矛盾""这条能不能全自动验"。
把一颗原子的 claim **拆成多个原子命题**，每个命题三元组化(subject,predicate,object)+定级(observation/inference)，机器就能精确分流：
- observation（直接观测）→ replay confirm 即可，全自动
- inference（推断）→ 必须人签或独立标准源，机器不许直推 verified

这是524"验证强度连续谱"的落地，也是知识概念进图谱的前提。

---

## 二、精确 schema（加进 frontmatter，不破坏现有字段）

在原子卡 frontmatter 加 `claim_structured`（**列表**，一颗原子可拆多个命题）：

```yaml
claim_structured:
  - id: prop-1
    subject: 内存屏障(fence)          # 概念节点名，进知识图谱 concept 表
    predicate: 在循环体内时           # 关系
    object: 阻止编译器消除该循环       # 概念或观测结果
    claim_type: observation            # observation=可机验 / inference=需人审或标准源
    statement: 一句话人类可读命题
    evidence: [EV-CONC-001]            # 支撑证据卡
  - id: prop-2
    subject: 内存屏障(fence)
    predicate: 不提供
    object: 数据竞争原子性/不建立happens-before
    claim_type: inference
    statement: 屏障≠原子类型，普通int做标志仍是UB
    evidence: [EV-CONC-002]
    external_basis: "ISO/IEC 14882:2023 [atomics.order] / cppreference"
```

**字段硬约束**：
- `claim_type` 只能是 `observation` / `inference`（写错→gate block）
- `observation` 必须有 `evidence` 且至少一张证据卡带 artifact 断言（机器闭环前提）
- `inference` 必须有 `external_basis`（ISO/cppreference/hackers邮件/commit hash）或人签——否则这条命题只是主张，不是知识
- `subject`/`object` 用规范概念名（同一概念各处写法一致，如统一"内存屏障"不混用"栅栏"）
- 末尾保留 `extracted_by: writer`（预留字段，现在恒为writer；将来模型自动抽取后写model——**这是终局进化接口，现在就留着**）

---

## 三、三个新 gate 规则（含正反例毒样例+pytest）

### 规则1 ATOM-CLAIM-STRUCTURED（新卡强制，存量warn）
- 新原子卡（draft起点）必须有 claim_structured，否则 block
- 存量27张已verified卡：本批只 warn 不 block（STAGING，人逐步回填）

### 规则2 OBSERVATION-NEEDS-ARTIFACT（block，零容忍）
- 任一 claim_type=observation 的命题，若 evidence 指向的证据卡**不含 artifact 断言**（无 artifact_assert / run_match），→ block
- 理由：observation 自称"直接观测"却拿不出工件，是自证（520漏洞1的变种）

### 规则3 INFERENCE-NOT-MACHINE-VERIFIED（block，核心放权闸）
- 任一 claim_type=inference 的命题，若该原子 status=verified 但 status_history 里 **没有 human: 签署记录** → block
- 理由：推断类结论不能由机器（哪怕replay全绿）独自晋升verified，必须有人或独立标准源背书
- 注意：若 inference 命题有 external_basis 且该来源在 sources.independent=true 里登记，可降级为 warn（标准源视同独立佐证）

---

## 四、实施步骤（按顺序，每步可独立验收）

**Step 1 样板回填**
把 ATOM-CONC-FENCE-001 的 claim 拆成 prop-1/prop-2（如上），跑通全部新规则。
这是锚——后续所有卡照这个粒度拆。

**Step 2 规则落地**
三个新规则写进 gate_engine.py，各配：
- 正例毒样例（合法通过）
- 反例毒样例（非法block）
- pytest 至少2例/规则
- poison_drill 注册（否则RULE-COVERAGE会红——508的教训）

**Step 3 存量扫描**
跑 `python tools/gate_engine.py --check`，列出27张存量卡各自命中规则的情况，写进 worklog：
- 哪些卡 observation 缺工件
- 哪些 inference 没人签
- 数字如实记录，**本批不批量改存量**（只warn，人逐批回填）

**Step 4 知识图谱衔接**
改 knowledge_graph.py：
- nodes 加可选 `concept` 表（subject/object 进为概念节点）
- build() 解析 claim_structured，把 prop 的 subject→object 建成 CONCEPT_EDGE
- 新增查询：`python tools/knowledge_graph.py concepts <概念名>`（这个概念出现在哪些命题）
- 节点数/边数变化如实报（现在320节点/291边）

---

## 五、铁律（违反即返工）

1. 不push、不golden accept
2. 一规则一commit + 毒样例 + pytest
3. **存量零误伤**：新规则对存量卡只warn不block，新卡才强制。每步跑 `gate --check` 对比warn数变化
4. 不编造：claim_type 归类拿不准的，标 inference 并在worklog注明，请人定夺，不擅自定 observation
5. 概念名统一：同一概念全仓一种写法，新造别名前先grep现有用法
6. extracted_by 字段现在恒写 writer，但**不许删这个字段**——它是将来模型自动抽取的进化接口

---

## 六、收工验收（fresh run）

```
python tools/gate_engine.py --check      # 报新规则名+存量warn命中数
python tools/atom_evidence_replay.py --check   # confirm=56 不变
python tools/poison_drill.py             # 新毒样例全过，RULE-COVERAGE上升
pytest -m fast                           # 全绿
python tools/knowledge_graph.py stats   # concept节点数/边数
```

写 `_worklog_526.md`：
- 样板卡拆成几个命题
- 三个规则各自的存量命中数（不是0就如实报）
- 知识图谱 concept 层节点/边数
- 哪几张卡 observation 缺工件 / inference 缺人签（这是后续回填backlog）

---

## 七、明确不做（防止蔓延）

- 不要求本批改完27张存量卡（只扫出backlog）
- 不做"模型自动抽取三元组"（那是模型更强后的事，现在writer填）
- 不改现有claim字段（保留原自然语言，claim_structured是并列补充不是替换）
- 不建新工具目录（gate/knowledge_graph已在，只扩展）
- 不push任何东西

---

## 八、为什么这是L3智能起点

做完后系统第一次有了"命题级"而非"文件级"的知识结构：
- 机器能说"这条是观测，我验过；这条是推断，人签了"——放权从粗变精
- 图谱能问"哪些命题在谈内存屏障""两条命题是不是互相矛盾"——从文件依赖升到概念推理
- 下一批回填存量时，自然暴露哪些原子的claim其实站不住（inference没人签/observation没工件）——这是系统第一次**自我审计知识质量**，不是只审计格式。

---

*文档编号 526。批次E提示词，直接投喂晚上好模型。*
