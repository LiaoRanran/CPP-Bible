# 622 A3 · 0 逃逸深度分析（为什么是 0）

> 判决分布：{'blocked': 13, 'infra_error': 23, 'neutral': 14}

## 一、生成策略够不够强（可施加率 / 被拦率）

| 策略 | 条数 | 可施加 | 可施加率 | blocked | neutral | infra_error | 被拦率 |
| evidence_ambiguity | 17 | 10 | 0.5882 | 2 | 8 | 7 | 0.2 |
| provenance_inconsistency | 16 | 5 | 0.3125 | 0 | 5 | 11 | 0.0 |
| rule_blind_spot | 17 | 12 | 0.7059 | 11 | 1 | 5 | 0.9167 |

## 二、v7 是否已覆盖这些变异

- (卡, 算子) 与 v7 重叠：**50/50（1.0）**
- 卡与 v7 重叠：**50/50（1.0）**

## 三、gate 规则是否已足够强（变异触发的规则）

| 规则 | 触发次数 |
| ATOM-FM-REQUIRED | 4 |
| ATOM-STATUS-TRANSITION | 3 |
| INFERENCE-NOT-MACHINE-VERIFIED | 3 |
| EV-FM-REQUIRED | 3 |
| EV-FALSIFICATION | 2 |
| EV-MATRIX | 1 |

## 四、下一轮生成策略改进建议

- ① **生成器必须 schema-aware**：先读目标卡的 frontmatter 实际字段，再决定 op。当前不适用率最高的策略：['evidence_ambiguity', 'provenance_inconsistency', 'rule_blind_spot']（可施加率 <80%）。
- ② **提高组合新颖性**：当前 (卡,算子) 与 v7 重叠 100% ⇒ 应显式排除 v7 已有的 (卡,op) 对，或引入 v7 没有的算子（M8+）。
- ③ 已有变异触发的规则：['ATOM-FM-REQUIRED', 'ATOM-STATUS-TRANSITION', 'INFERENCE-NOT-MACHINE-VERIFIED', 'EV-FM-REQUIRED', 'EV-FALSIFICATION', 'EV-MATRIX'] ⇒ 下一轮应优先攻击**未触发**的规则。
- ④ **neutral 需细分**：14 条 neutral 既未触发 block 也未削弱检测 ⇒ 说明这些编辑（如 status→draft、恒真断言）**对规则判定无影响**，应改用能改变规则输入语义的编辑。
- ⑤ **两段式验证**：本批只跑 gate（规则层）；下一轮应叠加 replay 复算层，才能发现「规则过但复算不过」的逃逸。


## 五、三个"为什么 0"的结论（逐条回答）

### Q1：是生成策略不够强吗？——**是，但主因是"不适用"而非"打不穿"**

| 策略 | 可施加率 | 被拦率 | 判读 |
|---|---|---|---|
| rule_blind_spot | 70.6% | **91.7%** | 能施加的基本都被拦住 ⇒ **规则层很硬** |
| evidence_ambiguity | 58.8% | 20.0% | 多数落在 neutral（编辑对判定无影响） |
| provenance_inconsistency | **31.3%** | 0.0% | 近七成根本施加不上 |

⇒ rule_blind_spot 的高被拦率说明**gate 规则层确实强**；
真正拖后腿的是**生成器不检查卡的实际字段**（46% 不适用）。

### Q2：是 v7 已经覆盖了这些变异吗？——**是，100% 覆盖**

(卡, 算子) 与 v7 重叠 **50/50 = 100%**，卡重叠也是 100%。
⇒ 621 的生成器**只是在 v7 已有的组合上换了个"变异点"**，
从未探索 v7 之外的（卡,算子）空间。**候选空间并未真正扩张。**

### Q3：是 gate 规则已经足够强吗？——**在"已触发的 6 条规则"范围内是的**

变异共触发 6 条规则（ATOM-FM-REQUIRED 4、ATOM-STATUS-TRANSITION 3、
INFERENCE-NOT-MACHINE-VERIFIED 3、EV-FM-REQUIRED 3、EV-FALSIFICATION 2、EV-MATRIX 1）。
**63 条规则里只触发了 6 条（9.5%）** ⇒ 绝大多数规则**没被这批变异碰到**，
所以"0 逃逸"**不能**推断为"63 条规则都强"，只能说"被打到的 6 条都拦住了"。

## 六、四维修复建议（可执行）

### 6.1 规则层（gate）

- 本批**未发现需要新增/修改规则**（0 逃逸，无绕过证据）。
- 但覆盖率仅 6/63 ⇒ 建议下一轮**按规则逐条构造变异**，把覆盖率打上去再谈"规则是否够强"。

### 6.2 证据层（evidence 卡）

- 证据卡上大量字段（rtifact / alsification / claim_structured / matrix）
  **在部分卡上并不存在** ⇒ 生成器应**先读卡再选 op**（schema-aware）。
- 建议给证据卡补一份**字段清单 schema**，供生成器查表。

### 6.3 卡面层（atoms/evidence 内容）

- 14 条 neutral 说明 status: draft、恒真断言注入这类编辑**对规则判定无影响** ⇒
  下一轮应改为**改变规则输入语义**的编辑（如删必填、错拼键名、改哈希）。

### 6.4 生成器（621 A1）

- ① **schema-aware**：从目标卡 frontmatter 取真实字段，再决定 op（消除 46% 不适用）。
- ② **排除 v7 已有 (卡,op) 对**，并引入 v7 没有的算子（M8+），把 novelty 从 0.5 档拉到 1.0 档。
- ③ **按规则全覆盖**：63 条规则逐条构造针对性变异（当前只打到 6 条）。
- ④ **叠加 replay 层**：只跑 gate 会漏掉"规则过但复算不过"的逃逸。

## 七、局限性声明

1. **只跑 gate，未跑 replay** ⇒ 本分析的"0 逃逸"仅限**规则层**。
2. **有效样本 27/50** ⇒ 策略维度的比率基于小样本。
3. **escaped 采用严格口径**（须"检测消失"）⇒ 可能低估。
4. **单次运行**，未做重复性验证（gate 判定确定性，风险低）。
5. **建议未经实施验证** ⇒ 属"下一轮待做"，非本批结论。
