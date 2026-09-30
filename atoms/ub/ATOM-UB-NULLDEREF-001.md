---
schema_version: 1
id: ATOM-UB-NULLDEREF-001
title: 解引用空指针不保证段错误：它是 UB，不是「一定崩」
domain: ub
type: mechanism
status: machine-verified
cpp_standard: [C++17]
compiler: [WSL g++ (Ubuntu 13.3.0)]
platform: [WSL2 Linux x86-64]
input_domain: unknown
dal: B
human_review: required
audience: intermediate
cognitive_load: low
claim: >-
  解引用空指针是**未定义行为**；「一定 SIGSEGV」是平台巧合，优化器可以在假设它不发生的前提下删除整段代码。
claim_structured:
  - id: prop-1
    subject: ATOM-UB-NULLDEREF-001
    predicate: 实测判定
    object: asan 在夹具上的真实输出
    claim_type: observation
    statement: asan 对该夹具判定为 catch（信号：hit:AddressSanitizer）。
    evidence_668: [IG-668-IG07]
    extracted_by: machine:card_split_668
  - id: prop-2
    subject: ATOM-UB-NULLDEREF-001
    predicate: 边界
    object: 该判定成立的编译/平台条件
    claim_type: inference
    statement: 本判定在 WSL g++ (Ubuntu 13.3.0) / WSL2 Linux x86-64 上、以 asan 观测得到；
              换编译器或换平台不保证同样的可观测结果。
    external_basis: "ISO/IEC 14882（未定义行为条款）"
    extracted_by: machine:card_split_668
claim_boundary:
  standard: [C++17]
  compilers: [WSL g++ (Ubuntu 13.3.0)]
  opt: [-O0, -O2]
  platform: [WSL2 Linux x86-64]
evidence_668:
  - id: IG-668-IG07
    detector: asan
    fixture_rel: data/cards_665/fixtures/ig-07.cpp
    fixture_sha256: 36c0ce69c63d19c29c1693394be197fd97d5aef124c0c6cef82f0c90064287e6
    runs: 1
    measured_at: 2026-09-29 00:18:19
    signature: "hit:AddressSanitizer"
    verdict: catch
    expectation: catch
    reproduce: "python tools/ig_cards_665.py --check"
relations: []
sources:
  - {kind: iso, ref: "ISO/IEC 14882（未定义行为 / 分配释放配对相关条款）", independent: true}
first_hand: true
status_history:
  - {level: machine-verified, at: "2026-09-30", by: machine:card_split_668}
---

# ATOM-UB-NULLDEREF-001 · 解引用空指针不保证段错误：它是 UB，不是「一定崩」

一句话直觉：**「实测到 X」和「标准规定 X」是两件事** —— 这张卡只声明前者，后者请人签。

## 1. 误解（来自 664/665 独立生成的断言）

`解引用空指针一定段错误`

## 2. 真机实测（不是推理）

| 项 | 值 |
|---|---|
| 检测器 | `asan` |
| 夹具 | `data/cards_665/fixtures/ig-07.cpp`（sha256 `36c0ce69c63d19c2…`） |
| 测量时间 | 2026-09-29 00:18:19 |
| 运行次数 | 1 |
| 判定 | **catch**（期望 `catch`；签名 `hit:AddressSanitizer`） |

实测输出（前几行，完整见夹具复跑）：

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==131==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x64bcbbd4d19d bp 0x7ffe562ae
```

复算：`python tools/ig_cards_665.py --check`（在 `-O0` 与 `-O2` 两档下都跑，任一档报出即 `catch`）。

## 3. 正确表述

解引用空指针是**未定义行为**；「一定 SIGSEGV」是平台巧合，优化器可以在假设它不发生的前提下删除整段代码。

## 4. 边界（这张卡**不**声明什么）

- 不声明"换了编译器/平台/标准版本仍然如此"：上表只覆盖 `WSL g++ (Ubuntu 13.3.0)` / `WSL2 Linux x86-64` / `C++17`。
- 不声明**语义级**结论：检测器报出的是"在这个夹具上观测到了该行为"，不是"所有同类写法都被检测器覆盖"。
- **无边界三元组**：本卡尚未跑过完整 mutation 基线 ⇒ 四态判决按规则降级 `unknown`（`four_state_verdict_638`），
  这不是缺陷，是"判决未定不预写边界"的正确输出。
- `status: machine-verified` + `human_review: required`：**未经人签**，不计入 `verified` 口径。
