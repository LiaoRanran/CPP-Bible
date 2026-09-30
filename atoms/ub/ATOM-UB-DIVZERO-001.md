---
schema_version: 1
id: ATOM-UB-DIVZERO-001
title: 整数除零不是 C++ 异常：它是 UB / 信号，catch(...) 抓不到
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
  整数除零在 C++ 中不是异常，而是 UB（x86-64 上表现为 `SIGFPE`）；`try { … } catch (...) { … }` 抓不到它 —— 异常只覆盖 `std::exception` 体系。
claim_structured:
  - id: prop-1
    subject: ATOM-UB-DIVZERO-001
    predicate: 实测判定
    object: ubsan 在夹具上的真实输出
    claim_type: observation
    statement: ubsan 对该夹具判定为 catch（信号：hit:runtime error）。
    evidence_668: [IG-668-IG08]
    extracted_by: machine:card_split_668
  - id: prop-2
    subject: ATOM-UB-DIVZERO-001
    predicate: 边界
    object: 该判定成立的编译/平台条件
    claim_type: inference
    statement: 本判定在 WSL g++ (Ubuntu 13.3.0) / WSL2 Linux x86-64 上、以 ubsan 观测得到；
              换编译器或换平台不保证同样的可观测结果。
    external_basis: "ISO/IEC 14882（未定义行为条款）"
    extracted_by: machine:card_split_668
claim_boundary:
  standard: [C++17]
  compilers: [WSL g++ (Ubuntu 13.3.0)]
  opt: [-O0, -O2]
  platform: [WSL2 Linux x86-64]
evidence_668:
  - id: IG-668-IG08
    detector: ubsan
    fixture_rel: data/cards_665/fixtures/ig-08.cpp
    fixture_sha256: bf80f5565f55bfdf80244141b2982316460e92b7a2b7dfb729c9feea5652be8d
    runs: 1
    measured_at: 2026-09-29 00:18:20
    signature: "hit:runtime error"
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

# ATOM-UB-DIVZERO-001 · 整数除零不是 C++ 异常：它是 UB / 信号，catch(...) 抓不到

一句话直觉：**「实测到 X」和「标准规定 X」是两件事** —— 这张卡只声明前者，后者请人签。

## 1. 误解（来自 664/665 独立生成的断言）

`整数除零会抛出 C++ 异常`

## 2. 真机实测（不是推理）

| 项 | 值 |
|---|---|
| 检测器 | `ubsan` |
| 夹具 | `data/cards_665/fixtures/ig-08.cpp`（sha256 `bf80f5565f55bfdf…`） |
| 测量时间 | 2026-09-29 00:18:20 |
| 运行次数 | 1 |
| 判定 | **catch**（期望 `catch`；签名 `hit:runtime error`） |

实测输出（前几行，完整见夹具复跑）：

```
/mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/cards_665/fixtures/ig-08.cpp:1:42: runtime error: division by zero
```

复算：`python tools/ig_cards_665.py --check`（在 `-O0` 与 `-O2` 两档下都跑，任一档报出即 `catch`）。

## 3. 正确表述

整数除零在 C++ 中不是异常，而是 UB（x86-64 上表现为 `SIGFPE`）；`try { … } catch (...) { … }` 抓不到它 —— 异常只覆盖 `std::exception` 体系。

## 4. 边界（这张卡**不**声明什么）

- 不声明"换了编译器/平台/标准版本仍然如此"：上表只覆盖 `WSL g++ (Ubuntu 13.3.0)` / `WSL2 Linux x86-64` / `C++17`。
- 不声明**语义级**结论：检测器报出的是"在这个夹具上观测到了该行为"，不是"所有同类写法都被检测器覆盖"。
- **无边界三元组**：本卡尚未跑过完整 mutation 基线 ⇒ 四态判决按规则降级 `unknown`（`four_state_verdict_638`），
  这不是缺陷，是"判决未定不预写边界"的正确输出。
- `status: machine-verified` + `human_review: required`：**未经人签**，不计入 `verified` 口径。
