# _arch_v42 · 06 Threats to Validity 怎么写（方向 6）

> 核心问题：五层写法（Construct/Internal/External/Statistical/Temporal）；审稿人接受什么；怎么写不被攻击；好案例长啥样。
> 诚实标注：【经典】；【论文】；【推断】= 对阙疑的判断；【盲区】= 无法核实。

---

## 一、五层写法（映射到阙疑）

| 层 | 问什么 | 阙疑的具体 threat |
|---|---|---|
| Construct | 测量是否真测了想测的 | "检出率"测的是"机器判执行"而非"知识正确性"（概念混淆） |
| Internal | 因果是否干净 | 夹具自产→circular；盲 holdout 是否被泄露 |
| External | 能否外推 | 48 卡是否代表真实 C++ 知识分布；仅 C++ 能否外推其他语言 |
| Statistical | 样本/显著性 | 盲 holdout 20、外部 corpus 20，CI 宽 |
| Temporal | 时效 | 模型换代快，2026 结论 2027 是否仍成立 |

## 二、审稿人接受什么

- 接受**具体 + 已缓解**的 threats；拒绝**空泛**（"当然有局限"）或**回避**（不写）【经典，S23/S24】。
- Wohlin《Experimentation in Software Engineering》给软件工程实验四层（construct/internal/external/reliability=conclusion），与五层高度兼容，可据此自查【经典，S24】。

## 三、怎么写不被攻击"你自己都知道有问题还投"

- 每条 threat 配一句缓解或未来工作；把 threats 写成"我们主动暴露并设计了约束来压制它"（如盲 holdout、append-only 账本正是为压制 internal threat）【推断】。
- 不把致命 threat 藏起来：construct threat（机器判≠知识判）必须直说，否则被审稿人拆穿更惨。

## 四、好案例长啥样

- Shadish/Cook/Campbell 的有效性分类学是学术金标准模板【经典，S23】；PMCR 2020 有图形化 catalog 可参照结构【S25】。

## 五、来源

[S23] Shadish, Cook & Campbell, "Experimental and Quasi-Experimental Designs for Generalized Causal Inference", 2002（有效性 typology 金标准）；[S24] Wohlin et al., "Experimentation in Software Engineering", 2012（四层 threats）；[S25] "A Graphical Catalog of Threats to Validity", PMC 2020；内部：_arch_v42_brief.md。

**盲区**：阙疑 temporal threat 的具体时间窗未定（模型迭代速度）。
