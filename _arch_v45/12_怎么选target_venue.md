# 方向 12：怎么选 target venue

## 核心结论
1. 选会场的原则是**"贡献类型匹配受众"**，不是"越 top 越好"：QueYi 若主打"可审计知识验证基准"→ NeurIPS E&D；若主打"C++ 验证工具"→ ASE/ICSE *Tool*；若主打"程序分析/类型验证"→ PLDI/ISSTA/OOPSLA。
2. 双非单人作者应**用 venue 匹配度换录取概率**：投错会场（如把工具稿投去偏理论的 PLDI）等于自判死刑；投对垂直会场（ASE Tool）反而有戏。
3. 决策树：先问"我的核心贡献是 数据集/基准、系统/工具、还是方法/理论？"再映射到 venue；QueYi 横跨"基准+工具"，主投 NeurIPS E&D 2027，副投 ASE 2026/2027 Tool。

## 精确数字与案例
- **venue 光谱（匹配 QueYi）**：
  - 基准/数据集：NeurIPS E&D（2027，接收率~25%）、ICLR、ICML；
  - 工具/系统：ASE（Tool, ~22%）、ICSE（Tool Demo, ~20%）、FSE（Demo）；
  - 程序验证/PL：PLDI（~20%）、ISSTA（~25%）、OOPSLA、CAV；
  - 期刊（慢但稳）：TSE、EMSE、TOSEM、JSS。
- **案例**：*DataComp*（数据集）→ NeurIPS D&B 2023；*LiveCodeBench*（代码基准）→ ICLR 2025；*CrashJS*（JS 基准）→ MSR 2024（SE 例会）。QueYi 与 *LiveCodeBench*/*CrashJS* 最近。
- **错配代价**：把"工程系统"稿投理论会场，reviewer 会因"缺理论贡献"打低；反之把"方法"投 D&B 会因"非数据集"拒。

## 对阙疑的 3 条具体行动
1. **主投 NeurIPS E&D 2027**：framing 为"首个可审计的 C++ 知识验证基准"，对齐 D&B 传统（数据策展透明度）。
2. **并行备 ASE 2027 Tool / ICSE 2027 Demo**：framing 改为"可运行验证系统 + artifact"，用 artifact 徽章背书（方向 05）。
3. **画 venue 决策表**：在稿里附一页"为何选 E&D 而非 TSE/PLDI"，列贡献类型对照，提前堵 reviewer"投错会场"的质疑。

## 盲区（诚实标注）
- 各会精确接收率为行业估算，需官方 fact sheet 核对。
- "QueYi 主投 E&D"假设其贡献以"基准"为主；若最终你更强调"验证算法"，应改投 PLDI/ISSTA。
- 2026 NeurIPS 制裁条款（方向 54）可能影响中国作者投 NeurIPS 的可行性，需优先评估。

## 来源
- [1] NeurIPS E&D 2024/2025 — https://neurips.cc/Conferences/2024/DatasetsBenchmarks/AcceptedPapers
- [2] ASE/ICSE Tool — https://conf.researchr.org/home/ase-2026
- [3] LiveCodeBench (ICLR 2025) — https://iclr.cc/virtual/2025/poster/28134
- [4] CrashJS (MSR 2024) — https://homepages.ecs.vuw.ac.nz/~craig/publications/msr2024-oliver.pdf
