# 643 B4 · 逃逸热点扫描（智能层 #4：自动发现问题）

> 数据源：`data/mutation/full_baseline_v7.json`（variants **1593**、n_a **179**、`escaped`(计数口径) **1**、`equivalent_invalid` **8**）+ 5 份定向跑批。

## 一、算子的逃逸热点（按 escape 点估计降序）

| 算子 | 可判数 | N/A | escape 点估计 | 95% CP 区间 | 分子 |
|---|---|---|---|---|---|
| `M1` | 65 | 27 | 0.01538 | [0.00039, 0.08276] | 1 |
| `M2` | 168 | 27 | 0.00000 | [0.00000, 0.02172] | 0 |
| `M3` | 65 | 42 | 0.00000 | [0.00000, 0.05517] | 0 |
| `M4` | 224 | 27 | 0.00000 | [0.00000, 0.01633] | 0 |
| `M5` | 29 | 56 | 0.00000 | [0.00000, 0.11944] | 0 |
| `M6` | 716 | 0 | 0.00000 | [0.00000, 0.00514] | 0 |
| `M7` | 139 | 0 | 0.00000 | [0.00000, 0.02619] | 0 |

## 二、卡片域的逃逸/N-A 热点

| 域 | 卡数 | blocked | escaped | N/A | 逃逸率 | N/A 率 |
|---|---|---|---|---|---|---|
| `evidence/conc` | 6 | 150 | 1 | 6 | 0.00662 | 0.03822 |
| `atoms/conc` | 3 | 19 | 0 | 12 | 0.00000 | 0.38710 |
| `atoms/hist` | 1 | 6 | 0 | 4 | 0.00000 | 0.40000 |
| `atoms/lang` | 1 | 6 | 0 | 4 | 0.00000 | 0.40000 |
| `atoms/mem` | 21 | 127 | 0 | 84 | 0.00000 | 0.39810 |
| `atoms/ub` | 1 | 6 | 0 | 4 | 0.00000 | 0.40000 |
| `evidence/hist` | 1 | 22 | 0 | 1 | 0.00000 | 0.04348 |
| `evidence/lang` | 2 | 52 | 0 | 2 | 0.00000 | 0.03704 |
| `evidence/mem` | 45 | 974 | 0 | 60 | 0.00000 | 0.05803 |
| `evidence/ub` | 2 | 43 | 0 | 2 | 0.00000 | 0.04444 |

## 三、逃逸案例的归因

- `results[]` 里 `verdict==escaped` 原始 **9** 条；聚合计数口径 **1** 条；差额 = `equivalent_invalid` **8** 条（语义等价被剔除）—— **两口径都报，不合并**；
- 归因分布：`{'规则缺失': 1, '验证器能力天花板': 8}`

| 卡片 | 算子 | 变异点 | equivalent | 归因 | 理由 |
|---|---|---|---|---|---|
| `evidence/conc/EV-CONC-001.md` | M1 | 删 negative_controls | — | **规则缺失** | 逃逸且 new_block / new_warn 均为空 ⇒ 没有任何规则对该变异有反应 |
| `evidence/hist/EV-HIST-001.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-032.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-033.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-034.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-035.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-036.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/mem/EV-MEM-037.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |
| `evidence/ub/EV-UB-002.md` | M6 | 块式 → flow 写法（matrix） | ✅ | **验证器能力天花板** | 该变异被标 equivalent（语义等价 ⇒ 本就不该报） |

## 四、N/A 的归因（**启发式**，`inferred=True`）

- N/A 总数 **179**（占 variants **0.11237**）；其中语义类算子（M5, M6）贡献 **56** 条；
- ⇒ 启发式拆分：**样本不可判候选 56** / **验证器能力不足候选 123**；
- **原因字段可用性：False** ⇒ 以上拆分是**按算子族的推测**，不是逐条归因（无法逐条，因为 v7 没落盘原因）；
- 两类提示口径：`semantic`=样本可能不可判（语义等价/格式微扰）；`capability`=验证器能力不足候选（非语义类算子仍判 N/A）

## 五、定向跑批（622/623/624）的规则冲突证据

| 跑批 | 可用 | 条数 | verdict 分布 | 含 lost_rules | 冲突行 |
|---|---|---|---|---|---|
| `data/mutation_sandbox_run_622_results.json` | ✅ | 50 | `{'blocked': 13, 'infra_error': 23, 'neutral': 14}` | 3 | 3 |
| `data/high_complexity_sandbox_run_623.json` | ✅ | 80 | `{'blocked': 46, 'escaped': 4, 'detected_nonblock': 16, 'neutral': 12, 'infra_error': 2}` | 16 | 12 |
| `data/adversarial_loop_round3_sandbox_run_623.json` | ✅ | 40 | `{'blocked': 12, 'neutral': 14, 'detected_nonblock': 14}` | 8 | 8 |
| `data/cross_card_sandbox_run_624.json` | ✅ | 60 | `{'blocked': 47, 'detected_nonblock': 13}` | 0 | 0 |
| `data/adversarial_loop_round5_624.json` | ✅ | 40 | `{'blocked': 38, 'neutral': 2}` | 0 | 0 |

## 诚实登记

1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：逃逸点估计的 CP 区间很宽（如 M1 的 [0.0004, 0.083]）⇒ **小样本下「热点」排序不稳**，需人复核；
2. **口径差异已显式并列**：`escaped` 1 vs `verdict==escaped` 9 —— 差额是语义等价剔除（`equivalent_invalid`）；本工具不替读者选口径；
3. **N/A 细分是推测**（`inferred: True`）：v7 **没有** N/A 原因字段；按算子族拆只是**启发式**，且 179 条里只有 130 条在别处有原因样本（634 登记）；
4. **「Horizon 60 断崖」未找到精确口径** ⇒ 用「高复杂度定向跑批（623）vs 基线（v7）」作粗代理，**不等于** inbox 要的那两个复杂度区间；
5. **沙箱逃逸率 ≠ 生产逃逸率**（§十二.6）：本节全部来自沙箱/受控跑批；
6. 本工具**只读**：不改基线、不跑变异、不写 `data/mutation/`。
