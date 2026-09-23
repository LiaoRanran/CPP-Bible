# 629 A2 · 误报注入探针结果（Negative Control，自身免疫证据）

> 工具：`tools/autoimmune_probe_629.py`（纯标准库，**真实仓库零写入**：`atoms/`+`evidence/` 整树镜像到系统临时目录，用完即删）

## 一、方法

- 样本：A1 主口径干净卡按 id 排序取前 5 张 —— `ATOM-CONC-FENCE-001`、`ATOM-CONC-LOCK-001`、`ATOM-CONC-RACE-001`、`ATOM-HIST-AUTOPTR-001`、`ATOM-MEM-ALIGN-001`
- 扰动种类（只改格式）：`trailing_ws`, `quote_style`, `blank_line`, `comment`, `flow_to_block`
- **语义等价判据**：扰动后 `parse_frontmatter` 解析结果与原文**逐键相等**；不等价的扰动一律丢弃（本次丢弃 5 次）。
- 判据：扰动后该卡**新增 warn 规则** = 假阳性（自身免疫）证据。

## 二、混淆矩阵（来源标注）

| 格 | 含义 | 值 | 来源 |
|---|---|---|---|
| 真阴性 TN | 镜像中原样卡 warn 集合 == 真实仓库读数（阴性对照成立） | ✅ 一致 | 本工具实测 |
| 假阳性 FP | 语义不变的格式微扰副本被**新增 warn** | **0 / 20** 次扰动 | 本工具实测 |
| 真阳性 TP | 毒样例被 block | 124/124（诚实覆盖率 95.5%） | §一 standing baseline（poison_drill 不重跑，§零.1） |
| 假阴性 FN | 错误知识逃逸 | 1/1406（CS anytime 上界 0.9062%） | §一 standing baseline（616 修正） |

**格式过敏率（假阳性率）= 0.0%**（0/20 次有效扰动）

## 三、逐扰动明细

| 卡 | 扰动 | 状态 | 新增 warn 规则 |
|---|---|---|---|
| `ATOM-CONC-FENCE-001` | `trailing_ws` | 已测 | — |
| `ATOM-CONC-FENCE-001` | `quote_style` | 语义不等价（丢弃） | — |
| `ATOM-CONC-FENCE-001` | `blank_line` | 已测 | — |
| `ATOM-CONC-FENCE-001` | `comment` | 已测 | — |
| `ATOM-CONC-FENCE-001` | `flow_to_block` | 已测 | — |
| `ATOM-CONC-LOCK-001` | `trailing_ws` | 已测 | — |
| `ATOM-CONC-LOCK-001` | `quote_style` | 语义不等价（丢弃） | — |
| `ATOM-CONC-LOCK-001` | `blank_line` | 已测 | — |
| `ATOM-CONC-LOCK-001` | `comment` | 已测 | — |
| `ATOM-CONC-LOCK-001` | `flow_to_block` | 已测 | — |
| `ATOM-CONC-RACE-001` | `trailing_ws` | 已测 | — |
| `ATOM-CONC-RACE-001` | `quote_style` | 语义不等价（丢弃） | — |
| `ATOM-CONC-RACE-001` | `blank_line` | 已测 | — |
| `ATOM-CONC-RACE-001` | `comment` | 已测 | — |
| `ATOM-CONC-RACE-001` | `flow_to_block` | 已测 | — |
| `ATOM-HIST-AUTOPTR-001` | `trailing_ws` | 已测 | — |
| `ATOM-HIST-AUTOPTR-001` | `quote_style` | 语义不等价（丢弃） | — |
| `ATOM-HIST-AUTOPTR-001` | `blank_line` | 已测 | — |
| `ATOM-HIST-AUTOPTR-001` | `comment` | 已测 | — |
| `ATOM-HIST-AUTOPTR-001` | `flow_to_block` | 已测 | — |
| `ATOM-MEM-ALIGN-001` | `trailing_ws` | 已测 | — |
| `ATOM-MEM-ALIGN-001` | `quote_style` | 语义不等价（丢弃） | — |
| `ATOM-MEM-ALIGN-001` | `blank_line` | 已测 | — |
| `ATOM-MEM-ALIGN-001` | `comment` | 已测 | — |
| `ATOM-MEM-ALIGN-001` | `flow_to_block` | 已测 | — |

## 四、结论

- **20 次语义不变的格式微扰，零新增 warn ⇒ 格式过敏率 0%**。这说明现有 warn 规则**不是格式驱动**：A1 里 100% 的 warn 来自**内容/口径**（命题级字段缺失、object 非规范概念短语、引用目标不存在），不是标点/空白/引号。
- 对自身免疫问题的含义：**靠放宽格式救不了**——要降自身免疫率，必须改**规则口径**（命题级字段对新卡必需、对老卡豁免）或**补齐卡字段**，二者都需人审裁决。

- 另有 5 次扰动被判**语义不等价**而丢弃（ATOM-CONC-FENCE-001/quote_style、ATOM-CONC-LOCK-001/quote_style、ATOM-CONC-RACE-001/quote_style、ATOM-HIST-AUTOPTR-001/quote_style、ATOM-MEM-ALIGN-001/quote_style）——如实登记，不把语义改动计入自身免疫。

## 五、局限

- 样本 5 张卡 × 最多 5 类扰动，**不是统计抽样**：结论只能证伪（「某类格式过敏存在」），不能证明「所有格式都不过敏」。
- 镜像只复制 `atoms/` + `evidence/`；跨到 `Examples/` / `golden` / `misconceptions` 的规则读的是真实仓库（两侧一致，故差分有效，但**镜像内卡与真实仓库其他根的组合**可能在真实流程里不出现）。
- 语义等价用 `parse_frontmatter` 判据（本项目的解析器）；若解析器与实际 YAML 语义有偏差，判据随之偏差 —— 已如实登记。
