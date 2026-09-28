# 660 D1 · 轨迹层原型（5 条真实多步验证轨迹）

> 依据 `docs/trace_layer_spec_658.md`：一条验证轨迹 = 验证器为得出某卡判决经历的有序步骤序列
> `[观察 E1] → [调规则 R_a] → [中间结论 C1] → [引文 Cit_x] → [调规则 R_b] → [最终判决 V]`。
> 错误类型：T1 单点断言错 / T2 步骤遗漏 / T3 引用断裂 / T4 顺序依赖错 / T5 循环自引用。
> 本批只跑通"轨迹是什么→怎么验证"的流程（不实现采集器），样本均接地真实 atom。

---

## 轨迹 1 · CONC-003 数据竞争（error_type: T1 单点断言错）

- card: `CONC-003 数据竞争是未定义行为`
- atom_ref: `Examples/atoms/_atom_data_race.cpp`
- steps:
  1. `[观察]` 读 atom：两线程并发写非原子 `g_shared`，零同步原语 → 输出 `race_ops_total=200000`
  2. `[工具]` 调 `tsan` 语义规则 R_UB：非原子并发写 ⇒ UB
  3. `[中间结论]` C1 = "存在数据竞争（UB）"
  4. `[引文]` Cit-3 = "TSan 在 -O2 下稳定观测到竞争"（证据卡 drill_note 记载 WSL 复算）
  5. `[工具]` 调 R_evidence：Cit-3 提供独立可验证证据
  6. `[最终判决]` V = pass（UB 成立，证据成立）
- final_verdict: pass
- error_type: T1（若步骤3误判为非 UB 即单点错；本轨迹正确）

## 轨迹 2 · 求值顺序未指定（error_type: T4 顺序/依赖错）

- card: `f(g(),h()) 实参求值顺序未指定`
- atom_ref: `Examples/atoms/_atom_eval_order.cpp`
- steps:
  1. `[观察]` 运行 GCC15.3 输出 `h\ng\nf(2,1)`；运行 Clang 输出 `g\nh\nf(1,2)`
  2. `[工具]` 调 R_seq：标准规定顺序"未指定"（unspecified），非 UB
  3. `[中间结论]` C1 = "两种顺序都合法，不可依赖"
  4. `[引文]` Cit-7 = "GCC/Clang 顺序相反"
  5. `[工具]` 调 R_portable：依赖未指定顺序 ⇒ 不可移植
  6. `[最终判决]` V = pass（断言"未指定"成立）
- final_verdict: pass
- error_type: T4（若先调 R_portable 再调 R_seq，会误把"不可移植"当"UB"；顺序反了 → 误判）

## 轨迹 3 · fence vs atomic（error_type: T2 步骤遗漏）

- card: `裸 fence 不等价 atomic 顺序约束`
- atom_ref: `Examples/atoms/_atom_fence_vs_atomic.cpp`
- steps:
  1. `[观察]` -O2 下 fence 版本出现顺序错乱，atomic 版本稳定
  2. `[工具]` 调 R_UB（仅判 UB）⇒ 未触发（无 UB，只是重排）
  3. `[中间结论]` C1 = "无 UB"（⚠ 遗漏了内存序规则）
  4. `[引文]` Cit-9 = "编译器重排破坏 happens-before"
  5. `[工具]` **本应额外调 R_memorder**（被遗漏）→ T2
  6. `[最终判决]` V = pass（错：漏判内存序失效）
- final_verdict: pass（错判，演示 T2）
- error_type: T2（该调 R_memorder 没调，步骤遗漏；652 T2 假开关同类）

## 轨迹 4 · 严格别名（error_type: T3 引用断裂）

- card: `int* 强转 float* 违反严格别名`
- atom_ref: `Examples/atoms/_atom_strict_alias.cpp`
- steps:
  1. `[观察]` -fstrict-aliasing 下结果偏离预期
  2. `[工具]` 调 R_alias：强转破坏别名假设 ⇒ UB
  3. `[中间结论]` C1 = "严格别名违规"
  4. `[引文]` Cit-11 = "优化级别不影响结果"（⚠ 与结论无逻辑支撑）
  5. `[工具]` 调 R_evidence：Cit-11 与结论 C1 矛盾 → 引用断裂
  6. `[最终判决]` V = unknown（引文不支持结论，需重新取证）
- final_verdict: unknown
- error_type: T3（Cit-11 文本其实不支持"违规"结论，H2 反事实算子应抓）

## 轨迹 5 · 自引用环（error_type: T5 循环/自引用）

- card: `某结论引用自身证据链`（ch28 自引用同类）
- atom_ref: `Book/ch28*.md`（UNANCHORED 历史案例）
- steps:
  1. `[观察]` 卡 A 结论引用 Cit-X
  2. `[工具]` 调 R_evidence：追踪 Cit-X 来源
  3. `[中间结论]` C1 = "Cit-X 来自卡 A 自身"（⚠ 自指）
  4. `[引文]` Cit-X = 卡 A 的内部陈述（无外部真实来源）
  5. `[工具]` 调 R_anchor：无外部锚 → 未锚定
  6. `[最终判决]` V = unknown（证据自引用，信任根断裂）
- final_verdict: unknown
- error_type: T5（轨迹成环：A→Cit-X→A；ch28 UNANCHORED_EVIDENCE 同类）

---

## 流程跑通结论
- 5 条轨迹覆盖 T1–T5 全部错误类型，且均接地真实 atom/卡。
- 轨迹验证是 four_state 断言验证的**超集**（路径层补 T2–T5），不替代 L0 红线。
- 下一步（交人）：instrument gate_engine 记录步骤，产出 `{card, trajectory:[step], final_verdict, error_type}` 训练样本。
