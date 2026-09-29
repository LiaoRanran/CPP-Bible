# 665 E1 · 轨迹层扩样（5 → 10 条真实多步验证轨迹）

> 依据 `docs/trace_layer_spec_658.md`：一条轨迹 = 验证器为得出某卡判决经历的**有序步骤**
> `[观察 E] → [调规则 R] → [中间结论 C] → [引文 Cit] → [调规则 R'] → [最终判决 V]`。
> 错误类型沿用 658：T1 单点断言错 / T2 步骤遗漏 / T3 引用断裂 / T4 顺序依赖错 / T5 循环自引用。
>
> 本批与 660 D1 的差别：**这 5 条全部接地 665 B1 的真机实测卡**（`data/cards_665/`），
> 每一步的"观察"都是**可复跑的命令输出**（`python tools/ig_cards_665.py --check` 逐张复算），
> 不是示意。编号续接：T6–T10。
>
> 诚实登记：这仍是**手写轨迹 + 机器留痕**，不是从 `gate_engine` 里 instrument 出来的。
> 真正的自动采集（660 已登记为交人项）本批**未完成**。

---

## 轨迹 6 · IG01 有符号溢出（error_type: T1 单点断言错）

- card: `IG01`（源 ig-01，UBSan）
- fixture: `data/cards_665/fixtures/ig-01.cpp`
- steps:
  1. `[观察]` WSL g++ `-std=c++17 -O1 -fsanitize=undefined` 编译并跑 → 输出含 `runtime error`，rc=1
  2. `[工具]` 调 R_UB：有符号溢出 ⇒ UB（不是"回绕"）
  3. `[中间结论]` C1 = "溢出是 UB，编译器可任意处理"
  4. `[引文]` Cit-EV-IG01 = 实测 `ubsan 命中（rc=1）：runtime error`，签名 `hit:runtime error`
  5. `[工具]` 调 R_evidence：引文支持 C1
  6. `[最终判决]` V = pass
- final_verdict: pass
- error_type: T1（若步骤 3 写成"溢出会回绕"，单点断言即错；本机实测里没有任何"回绕"的观测空间）
- 最可能错的一步：**步骤 3**（把"UB"写成"实现定义的回绕"）。

## 轨迹 7 · IG03 delete nullptr（error_type: T2 步骤遗漏）

- card: `IG03`（源 ig-03，ASan）
- fixture: `data/cards_665/fixtures/ig-03.cpp`
- steps:
  1. `[观察]` WSL ASan 跑 `delete nullptr` → **无报告**，rc=0
  2. `[工具]` 调 R_crash：只看有没有报错 ⇒ 无（⚠ 漏了"沉默本身也是观测"这一步）
  3. `[中间结论]` C1 = "无证据说明危险"
  4. `[引文]` Cit-EV-IG03 = "asan 无报告（rc=0）"，签名 `clean`
  5. `[工具]` **本应补调 R_silent**：沉默 ⇒ 与标准保证的 no-op 一致
  6. `[最终判决]` V = pass（缺第 5 步时会退化成 unknown）
- final_verdict: pass
- error_type: T2（漏了"沉默即证据"这一步；与 660 轨迹 3 同类）
- 最可能错的一步：**漏第 5 步** ⇒ 把"检测器没说话"误当"没结论"。

## 轨迹 8 · IG09 -O0/-O2 一致 ≠ 语义不变（error_type: T4 顺序依赖错）

- card: `IG09`（源 ig-09，cross-compile）
- fixture: `data/cards_665/fixtures/ig-09.cpp`
- steps:
  1. `[观察]` g++ -O0 与 -O2 跑同一段**无 UB** 代码 → 两次输出一致
  2. `[工具]` 调 R_opt：优化不改语义
  3. `[中间结论]` C1 = "结论成立（-O2 安全）"（⚠ 顺序错了：先看"样本无 UB"再谈优化）
  4. `[引文]` Cit-EV-IG09 = "两优化级一致"，签名 `same:<sha>`
  5. `[工具]` 调 R_probe_validity：本探针**不含 UB** ⇒ 它没有能力呈现差异
  6. `[最终判决]` V = unknown（本探针未呈现，不是 claim 错）
- final_verdict: unknown
- error_type: T4（先调 R_opt 再调 R_probe_validity ⇒ 把"探针无能"读成"结论成立"）
- 最可能错的一步：**步骤 3 与 5 的顺序**。

## 轨迹 9 · IG05 sizeof 零开销（error_type: T3 引用断裂）

- card: `IG05`（源 ig-05，measure）
- fixture: `data/cards_665/fixtures/ig-05.cpp`
- steps:
  1. `[观察]` 本机 MinGW g++ -O2 跑出 `8 8`
  2. `[工具]` 调 R_sizeof：sizeof(unique_ptr<int>) == sizeof(void*)
  3. `[中间结论]` C1 = "零开销抽象成立"（**限本机 ABI**）
  4. `[引文]` Cit-EV-IG05 = "8 8"，但卡头 boundary.platform 写的是 `Windows x86-64 (MinGW-w64)`
  5. `[工具]` 调 R_scope：C1 若写成跨实现通用 ⇒ 与 boundary **不匹配** → 引用断裂
  6. `[最终判决]` V = pass（**限定范围**）/ 若 overclaim 则 unknown
- final_verdict: pass（范围内）
- error_type: T3（把"本机读数"当"跨实现事实"引用；665 B1 所有卡都标了 `needs_review=true` 正是为此）
- 最可能错的一步：**步骤 3 的范围滑移**。

## 轨迹 10 · IG16 std::move 退化为拷贝（error_type: T5 循环自引用）

- card: `IG16`（665 修正探针，源缺陷见 ig-04）
- fixture: `data/cards_665/fixtures/ig-16.cpp`
- steps:
  1. `[观察]` 类型无移动构造时 `std::move(a)` 打印 `copy`
  2. `[工具]` 调 R_move：std::move 只是**类型转换**（cast），不必然触发移动
  3. `[中间结论]` C1 = "无移动构造 ⇒ 退化为拷贝"
  4. `[引文]` Cit-EV-IG16 = `copy`；**注意**：该引文来自**本 batch 自己写的夹具**
  5. `[工具]` 调 R_independence：引文的生产者 == 结论的消费方 ⇒ 存在自引用风险
  6. `[最终判决]` V = pass（但需外部锚：ISO [expr.static.cast] 转型语义）
- final_verdict: pass
- error_type: T5（自己造夹具证明自己的结论；靠标准条款作外部锚打破自环）
- 最可能错的一步：**步骤 5 被略过** ⇒ 变成"自证"。

---

## 本批结论（诚实版）

1. 轨迹 6–10 覆盖 T1–T5 全五类，与 660 的 5 条加起来 **共 10 条**。
2. 每条的"观察"步骤都能被 `--check` 逐条复算 ⇒ **轨迹不是叙事，是可执行留痕**。
3. **未完成**：没有 instrument `gate_engine` 自动采集，仍是手写 + 机器留痕；
   自动采集仍是交人项（660 已登记）。
4. 已发现的**重复模式**：T2（沉默不是没结论）与 T3（范围滑移）在两条不同轨迹里都出现了 ⇒
   这两类应该优先做自动检测规则，而不是等人写文档时发现。
