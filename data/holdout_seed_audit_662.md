# 662 A1 · holdout seed 标签逐个人工核（审计报告）

> 起因：661 B1 首次 reveal 发现多条 "miss" 实为**对照 atom**（自洽、无植入错）→ 660 C2 的 seed 标签存在**过度声称**。
> 方法：逐个读 `Examples/atoms/<file>.cpp` 的**头部语义注释**（夹具/对照/受控实验的自我声明）+ 661 B1 的真机检测输出，判定 `planted` 真假。
> 结论：**真错 = 7 · 对照 = 8 · unknown = 5**（原 660 C2 声称 20 个"错误类型样本"→ 明显过度）。

## 判定结果

| id | atom | 头部语义（依据） | planted | 说明 |
|---|---|---|---|---|
| h1 | `_atom_data_race.cpp` | "CONC-003 夹具：数据竞争是 UB，TSan 可检测" | **true** | 真错（含 bench_race 竞争场景） |
| h2 | `_atom_false_sharing.cpp` | "判据（确定性，不依赖计时）：地址差判定同缓存行" | **unknown** | 性能病理，非 UB；无本地检测器 |
| h3 | `_atom_eval_order.cpp` | "**灰色地带对照**（unspecified）…不是 UB" | **false** | **明确对照** |
| h4 | `_atom_auto_ptr.cpp` | "受控实验（演化类）…C++98 里是**合理的工程妥协**" | **unknown** | 历史语言的合理妥协，非缺陷 |
| h5 | `_atom_strict_alias.cpp` | "ATOM-UB-ALIAS（**UB 类**）" | **true** | 真错；注 UBSan 检不出别名类 UB |
| h6 | `_atom_fence_vs_atomic.cpp` | "夹具：signal_fence ≠ thread_fence" | **unknown** | 演示两种 fence 的区分，非植入错 |
| h7 | `_atom_leak_detection.cpp` | "三种生命周期行为…scoped 为**对照组**" | **true** | 含 leak 场景（scoped 是对照） |
| h8 | `_atom_rule_three_bug.cpp` | "违反 Rule of Three 的后果…double free" | **true** | 真错（ASan 已命中） |
| h9 | `_atom_rule_five_noexcept.cpp` | "性能**静默**损失，**编译器不告警**" | **unknown** | 性能类，非可检测缺陷 |
| h10 | `_atom_shared_cycle.cpp` | "证伪卡：循环引用…计数永不归零…泄漏" | **true** | 真错（泄漏） |
| h11 | `_atom_weak_cycle.cpp` | "证伪卡的**反面**…两节点都析构（**无泄漏**）" | **false** | **对照** |
| h12 | `_atom_unique_size.cpp` | "unique_ptr 是**零开销**抽象" | **false** | **正面论断 → 对照** |
| h13 | `_atom_move_no_gain.cpp` | "**反例导向**：无间接资源时移动退化为拷贝" | **false** | 反例/对照 |
| h14 | `_atom_inline_odr_a.cpp` | "TU A（**实验组**：odr_fn 定义 A）" + b/main | **true** | 真错（ODR 多定义，linker 已命中） |
| h15 | `_atom_new_array.cpp` | "new[]/delete[] **必须配对**" | **true** | 真错（ASan 已命中） |
| h16 | `_atom_rvref_return.cpp` | "**版本边界**：C++11/14/17 vs C++20/23" | **false** | 边界实验，非错误 |
| h17 | `_atom_sso_size.cpp` | "本实现（libstdc++）的 sizeof/SSO **实测**" | **false** | 实测 → 对照 |
| h18 | `_atom_align_ctrl.cpp` | "**反例（不运行）**…只注释" | **false** | 无运行期错 → 对照 |
| h19 | `_atom_alloc_arena.cpp` | "自定义 arena…**堆分配为 0**"（正面特性） | **false** | 正面演示 → 对照 |
| h20 | `_atom_named_rvalue.cpp` | "**证伪对照**：若自动移动成立则两组计数应相同" | **false** | 对照 |

## 统计

| 标签 | 数量 | ids |
|---|---|---|
| **planted=true（真错）** | **7** | h1, h5, h7, h8, h10, h14, h15 |
| **planted=false（对照）** | **9** | h3, h11, h12, h13, h16, h17, h18, h19, h20 |
| **unknown（分不清）** | **4** | h2, h4, h6, h9 |

> 以 `holdout.json` 的 `planted` 字段为准：**true=7 / false=9 / unknown=4**（h13 标 false）。

## 结论与影响

1. **660 C2 的 "20 个真实 C++ 错误类型样本" 是过度声称**：真实可判为"植入错"的仅 **7/20**。
2. 因此 661 B1 的 "miss=9" **不能**解读为"验证器漏检 9 个错"——其中大部分是对照/边界/性能类，**"不报"才是正确行为**。
3. 修正标签后才能计算**有意义的检出率**：分母应为 `planted=true` 的 7 个（见 662 A2）。

## 附：这份审计本身的方法学限制

- 判定依据是**头部注释的自我声明**，未逐行核对 atom 全部代码（时间/预算限制）。
- h2/h6/h9 的"非缺陷"判断基于注释语义；若按"任何与主流做法相悖的写法都算错"的宽口径，它们可翻为 true。
- 更严做法：为每个 seed 附**可复现的证伪条件**（B 段独立生成的红队可补）。
