# 658 H3 · 小核查器种子数据（MiniCheck 范式，仅准备格式，不训练）

> v41 结论：47 卡 + 变异数据可训练 C++ 域小核查器（MiniCheck 范式）。
> 本批**只准备数据格式与目录结构**，不训练任何模型。

## 目录结构
```
data/small_verifier_seed/
├── README.md          # 本文件（schema 说明）
├── schema.json        # 字段定义
├── train.jsonl        # 训练样本（claim, evidence, label）
├── dev.jsonl          # 验证样本
└── citation_pairs.jsonl  # 反事实引文对（喂 H2 算子）
```

## schema.json（字段）
- `claim`: str — 待核查的 C++ 知识断言（取自卡 frontmatter / boundary 结论）
- `evidence`: str — 支撑证据原文（provenance 锚到的文件片段）
- `label`: "supported" | "contradicted" | "unverifiable" — 人类/账本裁定
- `card`: str — 来源卡 id
- `provenance_sha256`: str — 证据指纹（接 OTS 锚）

## 采样说明（不训练）
- 47 张卡的结论 + A1 真实缺陷 + A2 holdout 可作正负样本来源；
- 本批仅放 3 条示例样本证明格式可解析，训练留交人（需标注 + GPU）。

## 与 H1/H2 的关系
- 轨迹层（H1）的样本 `{card, trajectory, verdict, error_type}` 可映射到本 schema 的 `claim/evidence/label`；
- 反事实引文对（citation_pairs.jsonl）由 H2 算子消费。
