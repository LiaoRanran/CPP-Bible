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
    evidence: [EV-UB-DIVZERO-669]
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
    evidence: [EV-UB-DIVZERO-669]
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
verified_by: machine:card_split_668   # 机器 principal（**非**人签；人级结论仍待 human_review）
verified_at: 2026-09-30
evidence:
  - EV-UB-DIVZERO-669
superiority: >-
  多数资料停在"除零是 UB"；本卡把**异常语义**这条最容易被 `catch (...)` 误导的点与机器证据绑在一起：
  ① 665 的 ubsan 记录 `division by zero`（真机 WSL，夹具字节 sha 与记录双锁）；
  ② 本机 `-O2` 汇编里 `volatile` 让 `idiv ecx` **真实存在**（不可折叠，两平台同形）；
  ③ 与 `EV-UB-WRAP-669`/`EV-UB-OOB-669` 的「整段消失」并排，说明 UB 的机器形态取决于**可证性**。
  ⇒ 触发的是信号/UB，没有任何 C++ 异常对象可被 `catch` 捕获。
depth:
  layer: asm
  drill_note: >-
    工件 `Examples/atoms/_atom_ub_divzero_669.asm`：`mov`×2（读 volatile 的 a、b）+ `cdq` + `idiv ecx`。
    volatile 读阻止常量折叠 ⇒ 除法指令真实存在；这条是「同是 UB，有的被折没、有的必须真算」的对照点。
pedagogy:
  motivation: 为什么 `try { return a/b; } catch (...) {}` 挡不住除零？——因为除零不是异常，是 UB/信号。
  misconceptions: [MIS-UB-001]
  socratic:
    - "`catch (...)` 能抓住信号吗？标准里 `...` 覆盖的是什么？"
    - "既然 `idiv` 真的执行了，能不能说'除零一定会让程序终止'？标准保证吗？"
  predict_first: 先预测 `int` 除零在本机会发生什么（异常？信号？静默？），再看卡面 §2 的记录。
status_history:
  - {level: draft, at: "2026-09-29", by: machine:card_split_668}
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
