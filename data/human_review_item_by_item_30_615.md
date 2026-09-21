# 615 A2 · 30 条真逐条复核决策清单（交人审，**不执行**）

> 背景：388 条为批量授权（逐条独立 0）。本清单挑 30 条**最高优先**候选边，供人**逐条复核**。
> **苦力不执行复核**；人审执行后由人**授权**更新 annotations（本批不改）。

## 选取优先级

1. OUT 的 7 个 MIS 的正向攻击边（`MIS-LANG-001/MIS-MEM-001/MIS-MEM-003/MIS-UB-001/MIS-UB-004/MIS-UB-008/MIS-UB-014`）——全部
2. modify 边（歧义度最高）　3. 高权重卡　4. 理由最短/最模板化

## 逐条决策清单

| # | 边 ID | 源 MIS | 目标命题 | 关联原子卡 | 当前 | 理由长度 | 建议 | 置信度 |
|---|---|---|---|---|---|---|---|---|
| 1 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1` | MIS-LANG-001 | prop-1 | ATOM-LANG-INLINE-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 2 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-2` | MIS-LANG-001 | prop-2 | ATOM-LANG-INLINE-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 3 | `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-3` | MIS-LANG-001 | prop-3 | ATOM-LANG-INLINE-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 4 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-001 | prop-1 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 5 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-001 | prop-2 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 6 | `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-001 | prop-3 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 7 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-003 | prop-1 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 8 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-003 | prop-2 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 9 | `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-003 | prop-3 | ATOM-MEM-MOVE-002 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 10 | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-1` | MIS-UB-001 | prop-1 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 11 | `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2` | MIS-UB-001 | prop-2 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 12 | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-1` | MIS-UB-004 | prop-1 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 13 | `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-2` | MIS-UB-004 | prop-2 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 14 | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-1` | MIS-UB-008 | prop-1 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 15 | `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-2` | MIS-UB-008 | prop-2 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 16 | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-1` | MIS-UB-014 | prop-1 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 17 | `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-2` | MIS-UB-014 | prop-2 | ATOM-UB-GRAY-001 | modify | 47 | 需独立判断（原为镜像/短理由，rubber-stamp 风险） | low |
| 18 | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-002 | prop-1 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 19 | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-002 | prop-2 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 20 | `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-002 | prop-3 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 21 | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-004 | prop-1 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 22 | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-004 | prop-2 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 23 | `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-004 | prop-3 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 24 | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-005 | prop-1 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 25 | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-005 | prop-2 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 26 | `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-005 | prop-3 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 27 | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-012 | prop-1 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 28 | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-2` | MIS-MEM-012 | prop-2 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 29 | `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-3` | MIS-MEM-012 | prop-3 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |
| 30 | `ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-1` | MIS-MEM-017 | prop-1 | ATOM-MEM-MOVE-002 | approve | 60 | 复核 approve | medium |

## 复核明细（判断要点 + 待人回答的是非题）

### 1. `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1`

- 源 MIS：**MIS-LANG-001** ｜ 目标命题：**ATOM-LANG-INLINE-001::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：两个 TU 给出不同定义的 inline 函数，其可观测行为由链接顺序与优化档共同决定：-O0（未内联）链接顺序 a→b 时 ab_tu_a=1、ab_tu_b=1，顺序 b→a 时 ba_tu_a=2、ba_tu_b=2；-O2（发生内联）时 o2_tu_a=1、o2_tu_b=2，换顺序仍为 1/2（各 TU 内联自己看到的定义）。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-LANG-001` 的 refutation 是否驳斥了 `ATOM-LANG-INLINE-001::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 2. `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-2`

- 源 MIS：**MIS-LANG-001** ｜ 目标命题：**ATOM-LANG-INLINE-001::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：当各 TU 的定义由相同 token 序列构成时行为稳定：stable 组在 ab/ba/o2/o2b 四种链接与优化组合下 stable_a 与 stable_b 恒为 42。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-LANG-001` 的 refutation 是否驳斥了 `ATOM-LANG-INLINE-001::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 3. `ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-3`

- 源 MIS：**MIS-LANG-001** ｜ 目标命题：**ATOM-LANG-INLINE-001::prop-3** ｜ 当前：modify
- 目标断言（来自命题库）：各定义须由相同的 token 序列构成（[basic.def.odr]/16.4），违反属 ill-formed 且 **no diagnostic required**——实测 GCC 家族零诊断这一事实本身既不能证明合规也不能证明违规，判据来自标准对 ODR 与"行为如同单一定义"的规定。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-LANG-001` 的 refutation 是否驳斥了 `ATOM-LANG-INLINE-001::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 4. `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-001** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-001` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 5. `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-001** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-001` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 6. `ae-MIS-MEM-001->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-001** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：modify
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-001` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 7. `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-003** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-003` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 8. `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-003** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-003` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 9. `ae-MIS-MEM-003->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-003** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：modify
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-MEM-003` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 10. `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-1`

- 源 MIS：**MIS-UB-001** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2、c++17）输出均为 h 先于 g、最终 f(1,2)——实测顺序一致**不代表可依赖**，标准只规定其为未指定/不确定序。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-001` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 11. `ae-MIS-UB-001->ATOM-UB-GRAY-001::prop-2`

- 源 MIS：**MIS-UB-001** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：未测序的同一标量修改（如 i = i++ + ++i）与通过不兼容类型指针访问对象（严格别名）属**未定义行为**——标准不再要求任何行为，优化器可据此删除访问；而函数实参 f(i++, i++) 自 C++17 起是 indeterminately sequenced ⇒ 只是 unspecified（C++11/14 下才是 UB）。这条版本边界依据标准对调用实参求值顺序、未测序与严格别名的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-001` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 12. `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-1`

- 源 MIS：**MIS-UB-004** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2、c++17）输出均为 h 先于 g、最终 f(1,2)——实测顺序一致**不代表可依赖**，标准只规定其为未指定/不确定序。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-004` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 13. `ae-MIS-UB-004->ATOM-UB-GRAY-001::prop-2`

- 源 MIS：**MIS-UB-004** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：未测序的同一标量修改（如 i = i++ + ++i）与通过不兼容类型指针访问对象（严格别名）属**未定义行为**——标准不再要求任何行为，优化器可据此删除访问；而函数实参 f(i++, i++) 自 C++17 起是 indeterminately sequenced ⇒ 只是 unspecified（C++11/14 下才是 UB）。这条版本边界依据标准对调用实参求值顺序、未测序与严格别名的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-004` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 14. `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-1`

- 源 MIS：**MIS-UB-008** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2、c++17）输出均为 h 先于 g、最终 f(1,2)——实测顺序一致**不代表可依赖**，标准只规定其为未指定/不确定序。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-008` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 15. `ae-MIS-UB-008->ATOM-UB-GRAY-001::prop-2`

- 源 MIS：**MIS-UB-008** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：未测序的同一标量修改（如 i = i++ + ++i）与通过不兼容类型指针访问对象（严格别名）属**未定义行为**——标准不再要求任何行为，优化器可据此删除访问；而函数实参 f(i++, i++) 自 C++17 起是 indeterminately sequenced ⇒ 只是 unspecified（C++11/14 下才是 UB）。这条版本边界依据标准对调用实参求值顺序、未测序与严格别名的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-008` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 16. `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-1`

- 源 MIS：**MIS-UB-014** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-1** ｜ 当前：modify
- 目标断言（来自命题库）：f(g(), h()) 的实参求值顺序实测：四组组合（GCC 15.3.0 与 GCC 13.1.0、-O0 与 -O2、c++17）输出均为 h 先于 g、最终 f(1,2)——实测顺序一致**不代表可依赖**，标准只规定其为未指定/不确定序。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-014` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 17. `ae-MIS-UB-014->ATOM-UB-GRAY-001::prop-2`

- 源 MIS：**MIS-UB-014** ｜ 目标命题：**ATOM-UB-GRAY-001::prop-2** ｜ 当前：modify
- 目标断言（来自命题库）：未测序的同一标量修改（如 i = i++ + ++i）与通过不兼容类型指针访问对象（严格别名）属**未定义行为**——标准不再要求任何行为，优化器可据此删除访问；而函数实参 f(i++, i++) 自 C++17 起是 indeterminately sequenced ⇒ 只是 unspecified（C++11/14 下才是 UB）。这条版本边界依据标准对调用实参求值顺序、未测序与严格别名的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量调整：AI预标注modify(证据较充分但偏保守)，用户授权批量调整为medium
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**需独立判断（原为镜像/短理由，rubber-stamp 风险）**（置信度 low）
- 需人回答：① `MIS-UB-014` 的 refutation 是否驳斥了 `ATOM-UB-GRAY-001::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 18. `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-002** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：approve
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-002` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 19. `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-002** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：approve
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-002` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 20. `ae-MIS-MEM-002->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-002** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：approve
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-002` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 21. `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-004** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：approve
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-004` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 22. `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-004** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：approve
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-004` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 23. `ae-MIS-MEM-004->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-004** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：approve
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-004` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 24. `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-005** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：approve
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-005` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 25. `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-005** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：approve
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-005` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 26. `ae-MIS-MEM-005->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-005** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：approve
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-005` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 27. `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-012** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：approve
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-012` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 28. `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-2`

- 源 MIS：**MIS-MEM-012** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-2** ｜ 当前：approve
- 目标断言（来自命题库）：收益来自掏空源：持堆的 HeapBuf 拷贝分配=1、移动分配=0、移动后源被掏空=是；无可掏空间接资源的 FixedBuf 与 array 拷贝分配=0、移动分配=0、移动后源完好=是（退化成按字节搬运，汇编层见 pshufd + movaps 搬运 32 字节）。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-012` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-2` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 29. `ae-MIS-MEM-012->ATOM-MEM-MOVE-002::prop-3`

- 源 MIS：**MIS-MEM-012** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-3** ｜ 当前：approve
- 目标断言（来自命题库）：std::move(x) 自身不分配、不复制、不改变 x，它只做一次类型转换以让移动构造参与重载；搬运的收益来自移动构造掏空源对象。这条语义依据标准对 std::move 与 static_cast 等价、以及"移动后源有效但未指定"的规定，不由本卡读数单独证明。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-012` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-3` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

### 30. `ae-MIS-MEM-017->ATOM-MEM-MOVE-002::prop-1`

- 源 MIS：**MIS-MEM-017** ｜ 目标命题：**ATOM-MEM-MOVE-002::prop-1** ｜ 当前：approve
- 目标断言（来自命题库）：移动不分配：六组组合（GCC 15.3/13.1/8.1 × -O0/-O2）读数一致——构造分配=1、拷贝分配=1、移动分配=0，证伪对照（假移动）分配=1；汇编层 main 中 call malloc 共 3 次（构造 1 + 拷贝 1 + 假移动对照 1），真实移动路径 0 次。
- 审核理由原文：用户授权批量通过：AI预标注approve，抽样验证准确率100%(20/20)，用户确认通过率90%以上即授权批量通过
- 判断要点：该 MIS 的 **refutations 文本**是否**真的驳斥**了这个断言？驳斥的是命题的**哪个断言**？是否为镜像/抽样外推而非独立判断？
- 建议复核结论：**复核 approve**（置信度 medium）
- 需人回答：① `MIS-MEM-017` 的 refutation 是否驳斥了 `ATOM-MEM-MOVE-002::prop-1` 的断言？（是/否）② 若是，属于 approve 还是 modify？（approve/modify）

## 边界

- 本清单**不含**任何复核结论的**执行**；须人审逐条判断并**授权**后更新 annotations。
- 未修改 annotations、未改受控目录。


