---
schema_version: 1
id: ATOM-MEM-NEWARR-001
title: new[] 的数组不能用 delete 释放：分配与释放形式必须配对
domain: mem
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
  `new[]` 必须配 `delete[]`；用标量 `delete` 释放数组是 UB（x86-64 上 ASan 报 `alloc-dealloc-mismatch`），因为数组分配可能带 cookie，标量 delete 不会跳过它。
claim_structured:
  - id: prop-1
    subject: ATOM-MEM-NEWARR-001
    predicate: 实测判定
    object: asan 在夹具上的真实输出
    claim_type: observation
    statement: asan 对该夹具判定为 catch（信号：hit:AddressSanitizer）。
    evidence: [EV-MEM-NEWARR-669]
    evidence_668: [IG-668-IG14]
    extracted_by: machine:card_split_668
  - id: prop-2
    subject: ATOM-MEM-NEWARR-001
    predicate: 边界
    object: 该判定成立的编译/平台条件
    claim_type: inference
    statement: 本判定在 WSL g++ (Ubuntu 13.3.0) / WSL2 Linux x86-64 上、以 asan 观测得到；
              换编译器或换平台不保证同样的可观测结果。
    external_basis: "ISO/IEC 14882（未定义行为条款）"
    evidence: [EV-MEM-NEWARR-669]
    extracted_by: machine:card_split_668
claim_boundary:
  standard: [C++17]
  compilers: [WSL g++ (Ubuntu 13.3.0)]
  opt: [-O0, -O2]
  platform: [WSL2 Linux x86-64]
evidence_668:
  - id: IG-668-IG14
    detector: asan
    fixture_rel: data/cards_665/fixtures/ig-14.cpp
    fixture_sha256: 3557ed2c40078bff7c4aa77f858d25513ee08cbbcd7e975dd67e35dd02855c5c
    runs: 1
    measured_at: 2026-09-29 00:18:22
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
  - EV-MEM-NEWARR-669
superiority: >-
  「new[]/delete 混用只是少调几个析构」的说法在本卡被两条机器证据否掉：
  ① 工件里 `operator new[]`（族名 `_Zna…`）与 `operator delete(void*)`（族名 `_ZdlPv…`）**分属两个函数族**——
  这是"配对不匹配"的直接机器指纹（MinGW 与 Linux 拼写不同，但族名子串一致 ⇒ 可跨编译器断言）；
  ② 运行期 asan 报 `alloc-dealloc-mismatch (operator new [] vs operator delete)`。
  ⇒ 二者共同说明：数组分配与标量释放走的不是同一条路径，"少调析构"是错误的心智模型。
depth:
  layer: asm
  drill_note: >-
    工件 `Examples/atoms/_atom_mem_newarr_669.asm`：`call _Znay`（operator new[]）与
    `call _ZdlPvy`（operator delete(void*)）成对出现——函数族不同即是 UB 判据在汇编层的显形；
    Linux 侧为 `_Znam@PLT` / `_ZdlPvm@PLT`，族名子串一致。
pedagogy:
  motivation: 为什么"混用只是少调几个析构"不成立？——因为分配与释放走的函数族不同，布局假设也不同。
  misconceptions: [MIS-MEM-008, MIS-MEM-013]
  socratic:
    - "如果 `new[]` 与 `delete` 真的只是「少调几个析构」，为什么汇编里调用的是两个不同的函数族？"
    - "把 `new[]` 换成 `malloc` 再 `delete`，会更容易还是更难查？"
  predict_first: 先猜 `-O2` 下这两次调用会不会被内联掉/合并，再看卡面 §3 的 `call` 对。
status_history:
  - {level: draft, at: "2026-09-29", by: machine:card_split_668}
  - {level: machine-verified, at: "2026-09-30", by: machine:card_split_668}
---

# ATOM-MEM-NEWARR-001 · new[] 的数组不能用 delete 释放：分配与释放形式必须配对

一句话直觉：**「实测到 X」和「标准规定 X」是两件事** —— 这张卡只声明前者，后者请人签。

## 1. 误解（来自 664/665 独立生成的断言）

`new[] 分配的数组可以用 delete 释放`

## 2. 真机实测（不是推理）

| 项 | 值 |
|---|---|
| 检测器 | `asan` |
| 夹具 | `data/cards_665/fixtures/ig-14.cpp`（sha256 `3557ed2c40078bff…`） |
| 测量时间 | 2026-09-29 00:18:22 |
| 运行次数 | 1 |
| 判定 | **catch**（期望 `catch`；签名 `hit:AddressSanitizer`） |

实测输出（前几行，完整见夹具复跑）：

```
=================================================================
==183==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x502000000010
    #0 0x7b63ff6ff5e8 in
```

复算：`python tools/ig_cards_665.py --check`（在 `-O0` 与 `-O2` 两档下都跑，任一档报出即 `catch`）。

## 3. 正确表述

`new[]` 必须配 `delete[]`；用标量 `delete` 释放数组是 UB（x86-64 上 ASan 报 `alloc-dealloc-mismatch`），因为数组分配可能带 cookie，标量 delete 不会跳过它。

## 4. 边界（这张卡**不**声明什么）

- 不声明"换了编译器/平台/标准版本仍然如此"：上表只覆盖 `WSL g++ (Ubuntu 13.3.0)` / `WSL2 Linux x86-64` / `C++17`。
- 不声明**语义级**结论：检测器报出的是"在这个夹具上观测到了该行为"，不是"所有同类写法都被检测器覆盖"。
- **无边界三元组**：本卡尚未跑过完整 mutation 基线 ⇒ 四态判决按规则降级 `unknown`（`four_state_verdict_638`），
  这不是缺陷，是"判决未定不预写边界"的正确输出。
- `status: machine-verified` + `human_review: required`：**未经人签**，不计入 `verified` 口径。
