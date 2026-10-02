---
schema_version: 1
id: ATOM-UB-WRAP-001
title: 有符号整数溢出不是「回绕」：回绕是实现偶然，标准里是 UB
domain: ub
type: mechanism
status: machine-verified
cpp_standard: [C++17]
compiler: [WSL g++ (Ubuntu 13.3.0)]
platform: [WSL2 Linux x86-64]
input_domain: unknown
dal: C
human_review: waived
dal_reviewed_by: human:liaoranran
dal_reviewed_at: 2026-10-02
dal_review_reason: "基础UB/内存知识，机器验证(ASan/SIGFPE/SIGSEGV)已充分，人审暂豁免，待批量人审后调回B"
audience: intermediate
cognitive_load: low
claim: >-
  有符号整数运算超出可表示范围是**未定义行为**；「回绕」只是 x86-64 上 gcc/clang 的**实现选择**，优化器有权假设它不发生并据此改写程序。
claim_structured:
  - id: prop-1
    subject: ATOM-UB-WRAP-001
    predicate: 实测判定
    object: ubsan 在夹具上的真实输出
    claim_type: observation
    statement: ubsan 对该夹具判定为 catch（信号：hit:runtime error）。
    evidence: [EV-UB-WRAP-669]
    evidence_668: [IG-668-IG01]
    extracted_by: machine:card_split_668
  - id: prop-2
    subject: ATOM-UB-WRAP-001
    predicate: 边界
    object: 该判定成立的编译/平台条件
    claim_type: inference
    statement: 本判定在 WSL g++ (Ubuntu 13.3.0) / WSL2 Linux x86-64 上、以 ubsan 观测得到；
              换编译器或换平台不保证同样的可观测结果。
    external_basis: "ISO/IEC 14882（未定义行为条款）"
    evidence: [EV-UB-WRAP-669]
    extracted_by: machine:card_split_668
claim_boundary:
  standard: [C++17]
  compilers: [WSL g++ (Ubuntu 13.3.0)]
  opt: [-O0, -O2]
  platform: [WSL2 Linux x86-64]
evidence_668:
  - id: IG-668-IG01
    detector: ubsan
    fixture_rel: data/cards_665/fixtures/ig-01.cpp
    fixture_sha256: dda4a791a7d627098a6d82955fb5a1ec512ab6c29285464ab07926b86b0847bd
    runs: 1
    measured_at: 2026-09-29 00:18:15
    signature: "hit:runtime error"
    verdict: catch
    expectation: catch
    reproduce: "python tools/ig_cards_665.py --check"
relations: []
sources:
  - {kind: iso, ref: "ISO/IEC 14882（未定义行为 / 分配释放配对相关条款）", independent: true}
first_hand: true
verified_by: machine:card_split_668   # 机器 principal（**非**人签；人级结论仍待 human_review）
verified_at: 2026-09-30
evidence:
  - EV-UB-WRAP-669
superiority: >-
  「有符号溢出」在多数资料里只到"这是 UB"就停了；本卡把两条**机器可复算**的对照钉在一起：
  ① 665 的 ubsan 在真机上直接报 `signed integer overflow`（夹具**文件字节** sha 与记录双重锁定，
  `--check` 可复算）；② 同一夹具 `-O2` 的汇编里 `x += 1` 与 `x < 0` 被**整体折叠**成
  `mov eax, 1` + `ret`（MinGW 15.3 与 Linux 13.3 同形）——「优化器有权假定它不发生」由此变成
  可看见的字节，而不是一句告诫。
depth:
  layer: asm
  drill_note: >-
    工件 `Examples/atoms/_atom_ub_wrap_669.asm` 的 `main` 只有 `mov eax, 1` + `ret`：自增与比较都消失。
    对照 `EV-UB-DIVZERO-669`（同是 UB，但 `volatile` 使它不可折叠、`idiv` 真实存在）⇒
    能不能被优化器吃掉，取决于它能否被证明。
pedagogy:
  motivation: 为什么"我本地跑出回绕了"不能当成"标准保证回绕"？——标准没规定，编译器只是这次没吃掉你。
  misconceptions: [MIS-UB-002, MIS-UB-001]
  socratic:
    - "同一行 `x += 1` 在 -O0 与 -O2 下的汇编差了整段——变的是标准还是编译器？"
    - "如果编译器有权假定溢出不发生，那句 `x < 0` 还是你以为的意思吗？"
  predict_first: 编译前先猜：`-O2` 下 `main` 里还剩几条指令？（写下答案，再看卡面 §3）
status_history:
  - {level: draft, at: "2026-09-29", by: machine:card_split_668}
  - {level: machine-verified, at: "2026-09-30", by: machine:card_split_668}
---

# ATOM-UB-WRAP-001 · 有符号整数溢出不是「回绕」：回绕是实现偶然，标准里是 UB

一句话直觉：**「实测到 X」和「标准规定 X」是两件事** —— 这张卡只声明前者，后者请人签。

## 1. 误解（来自 664/665 独立生成的断言）

`有符号整数溢出会回绕（wrap around）`

## 2. 真机实测（不是推理）

| 项 | 值 |
|---|---|
| 检测器 | `ubsan` |
| 夹具 | `data/cards_665/fixtures/ig-01.cpp`（sha256 `dda4a791a7d62709…`） |
| 测量时间 | 2026-09-29 00:18:15 |
| 运行次数 | 1 |
| 判定 | **catch**（期望 `catch`；签名 `hit:runtime error`） |

实测输出（前几行，完整见夹具复跑）：

```
/mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/cards_665/fixtures/ig-01.cpp:1:31: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

复算：`python tools/ig_cards_665.py --check`（在 `-O0` 与 `-O2` 两档下都跑，任一档报出即 `catch`）。

## 3. 正确表述

有符号整数运算超出可表示范围是**未定义行为**；「回绕」只是 x86-64 上 gcc/clang 的**实现选择**，优化器有权假设它不发生并据此改写程序。

## 4. 边界（这张卡**不**声明什么）

- 不声明"换了编译器/平台/标准版本仍然如此"：上表只覆盖 `WSL g++ (Ubuntu 13.3.0)` / `WSL2 Linux x86-64` / `C++17`。
- 不声明**语义级**结论：检测器报出的是"在这个夹具上观测到了该行为"，不是"所有同类写法都被检测器覆盖"。
- **无边界三元组**：本卡尚未跑过完整 mutation 基线 ⇒ 四态判决按规则降级 `unknown`（`four_state_verdict_638`），
  这不是缺陷，是"判决未定不预写边界"的正确输出。
- `status: machine-verified` + `human_review: required`：**未经人签**，不计入 `verified` 口径。
