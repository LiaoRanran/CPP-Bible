# 12 · 落地路径与风险（NDW 分类）

## 12.1 落地步骤与前置条件

| 步 | 内容 | 前置条件 |
|---|---|---|
| 1 | 以 MIS 关联为种子，自动生成**候选**命题级攻击边（卡级→命题级映射规则） | 无（N 可做） |
| 2 | 定义权重来源（verified/machine_verified > MIS level）转**加权 AF** | 步 1 完成 |
| 3 | 手搓加权 grounded 求解器，输出 IN/OUT/UNDEC + 辩护链 | 步 2 |
| 4 | 人审裁决 undecided，标注最终攻击边 | 步 3 + 人审投入 |
| 5 | 接 golden_lock / 573 收敛判据 | 步 4 |
| 6 | 按需上 clingo 跑 preferred/stable | 步 3 后、语义需求明确 |

## 12.2 风险清单

| 风险 | 表现 | 缓解 |
|---|---|---|
| 攻击关系不可靠 | refutations 文本与命题非严格矛盾 | 卡级→命题级映射规则 + 人审裁决 |
| grounded 退化平凡 | 全 IN（S0）或全 UNDEC（S2） | 加权 AF 打破 2-环（维度 3） |
| 复杂度爆炸 | 误用 preferred/stable | 默认 grounded（P 类）；preferred 仅按需 |
| 人审不接受 | automation aversion（S1 倒置伤信任） | 先修攻击边/加权再让人审见结论 |
| 与三分类语义冲突 | confirm 被 grounded 判 OUT | 维度 7 映射需人审确认，接 golden_lock |

## 12.3 NDW 分类

- **N（现在能做，零 Oracle 风险）**：手搓 grounded 求解器（已做 `probes/`）、在当前命题图实测（已做）、prop_closure（592 已做）、MIS 自动候选攻击边生成脚本。
- **D（攒数据）**：攻击边人审标注、refutations 字段质量复核（已证 79 全有）、权重规则定义、undecided 人审裁决样本。
- **W（等条件）**：clingo 主引擎（规模无需）、preferred/stable 语义、概率/模糊扩展（维度 9 解冻信号）、多判官独立投票（arXiv:2605.29800 待核验）。

## 12.4 一句话边界

**grounded 求解器已就绪且免费；真正的工程在"造可信攻击边 + 加权"，这是 D 段，不是算法问题。**
