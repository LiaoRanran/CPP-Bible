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
dal: C
human_review: waived
dal_reviewed_by: human:liaoranran
dal_reviewed_at: 2026-10-02
dal_review_reason: "基础UB/内存知识，机器验证(ASan/SIGFPE/SIGSEGV)已充分，人审暂豁免，待批量人审后调回B"
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
    evidence: [EV-UB-NULLDEREF-669]
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
    evidence: [EV-UB-NULLDEREF-669]
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
verified_by: machine:card_split_668   # 机器 principal（**非**人签；人级结论仍待 human_review）
verified_at: 2026-09-30
evidence:
  - EV-UB-NULLDEREF-669
superiority: >-
  「解引用空指针一定 SIGSEGV」这句话里混了两层：**标准层**（UB，优化器有权删掉整段）与
  **本平台层**（这台机器这次真的崩）。本卡的增量是把两层分栏并各给一条机器证据：
  ① asan 记录 `SEGV on unknown address 0x000000000000`（真崩，夹具字节 sha + 记录双锁）；
  ② `-O2` 汇编里是**对地址 0 的真实写入** `mov DWORD PTR ds:0, 0` + `ud2`（两平台同形）——
  ⇒ 本夹具上优化器**没有**选择删除它，"崩"是这次实现的结果，不是标准的承诺。
depth:
  layer: asm
  drill_note: >-
    工件 `Examples/atoms/_atom_ub_nullderef_669.asm`：`main` 内 `mov DWORD PTR ds:0, 0` 后接 `ud2`
    （不可达标记）。写入地址 0 是"会崩"的机器形态；`ud2` 是编译器对"这里已经不可继续"的标注。
pedagogy:
  motivation: 为什么"我这儿一定崩"不能提升为知识？——因为崩与不崩都合法，编译器可以选任意一种。
  misconceptions: [MIS-UB-003, MIS-UB-001]
  socratic:
    - "`if (p != nullptr)` 守住了这一处，能守住编译器对别处的推论吗？"
    - "既然本夹具的汇编是「真的写到地址 0」，那「优化器有权删掉它」这句话还成立吗？"
  predict_first: 先猜 `-O2` 下这段代码会不会被整段删掉，再看卡面 §3 的 `ud2`。
status_history:
  - {level: draft, at: "2026-09-29", by: machine:card_split_668}
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
