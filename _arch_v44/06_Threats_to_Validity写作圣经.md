# _arch_v44 · 06 Threats to Validity 写作圣经（方向 6）

> 核心问题：五层详解、审稿人接受什么、怎么不被攻击、3 个好范例、致命 threats、怎么量化。
> 诚实标注：【经典】；【论文】；【推断】；【盲区】。

---

## 一、五层写法详解（映射阙疑）

| 层 | 问 | 阙疑具体 threat | 量化 |
|---|---|---|---|
| Construct | 测的是不是想测 | 检出率测「机器判执行」非「知识正确性」 | 非可执行断言占比未知 |
| Internal | 因果干净 | 夹具自产 circular；盲 holdout 泄露 | 自产比例=100%→须外部构造 |
| External | 能否外推 | 48 卡是否代表 C++ 分布；仅 C++ | 语言覆盖=1 |
| Statistical | 样本/显著 | 盲 20/外部 20 | 95% CI 宽 |
| Temporal | 时效 | 模型换代 2026→2027 | 未定窗口 |

## 二、审稿人接受 / 不被攻击 / 致命

- 接受具体+已缓解；拒绝空泛/回避【经典，S23/S24】。
- 不被攻击：每条配缓解或未来工作，写成「主动暴露+设计约束压制」（盲 holdout/Merkle 即压制 internal）。
- 致命（写了易拒）：隐瞒 construct threat、样本小却称普适、污染不报。

## 三、3 个好范例（范式）

- 范例 A：每条 threat 一行「threat / 为何发生 / 我们如何缓解 / 残余」。
- 范例 B：五层各一段 + 量化（如「external: 仅 C++，CI 不含其他语言」）。
- 范例 C：把 threats 前置到 limitations，与 contributions 对称。【范式】

## 四、量化 threats

- 用置信区间（方向 07 Clopper-Pearson）、样本量、效应量（Cohen's h 比较两比例）。例：盲 holdout 4/5 可测 → 80% (95% CI 28%–99%)。

## 五、对阙疑的 3 条具体行动

1. **写标准五层 threats 表**：套上表结构，每条填「threat/成因/缓解/残余」，construct threat 必须直说。
2. **量化所有比例**：盲 holdout 80% 补 Clopper-Pearson 95% CI；外部 corpus 33.3% 同样补，避免「点估计无误差」被攻击。
3. **把 circular 列为 internal threat 并承诺缓解**：在 ROADMAP 排「外部构造第二套夹具」（方向 02 行动 2）作为该 threat 的缓解证据。

## 六、来源

[S23] Shadish, Cook & Campbell, 2002；[S24] Wohlin et al., Experimentation in SE, 2012；[S25] Graphical Catalog of Threats, PMC 2020；内部：_arch_v44_brief.md。

**盲区**：阙疑 temporal 窗口未定；非可执行断言占比无数据。
