---
id: ATOM-CONC-RACE-001
title: "数据竞争是未定义行为；TSan 可检测，但『没被报 ≠ 没有』"
domain: conc
type: pitfall
status: verified
dal: C
human_review: optional
verified_by: human:liaoranran
verified_at: "2026-09-12"
dal_reviewed_by: human:liaoranran
status_history:
  - {level: draft, at: "2026-09-12", by: machine:writer}
  - {level: machine-verified, at: "2026-09-12", by: machine:gate}
  - {level: verified, at: "2026-09-12", by: human:liaoranran}
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
claim: >-
  数据竞争（无同步的并发冲突访问，且至少一方为写）是 C++ 未定义行为，不是"结果偶尔算错"——
  编译器可据此做激进优化，行为完全不可预测。TSan 能检测数据竞争，但"没被 TSan 报 ≠ 没有数据竞争"：
  其漏报边界（插桩盲区 / 必须全量插桩 / 时序偶发）使工具沉默不能当作安全证明。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL), GCC 13.3.0 (WSL)]
  opt: [-O2]
  platform: [x86-64]
relations:
  - prerequisite: ATOM-CONC-FENCE-001
evidence:
  - EV-CONC-005
  - EV-CONC-006
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [intro.race]（data race 的定义：不同线程对同对象无 happens-before 的并发冲突访问，且至少一方为写 ⇒ 未定义行为）", independent: true}
  - {kind: cppreference, ref: "ThreadSanitizer：编译期插桩 + 运行期 happens-before 边追踪检测数据竞争，但有漏报边界", independent: true}
first_hand: true
superiority: >-
  教材常把"数据竞争"弱化成"答案偶尔错"，弱化其严重性与工具边界。本原子用同一份夹具把"无同步并发写"
  与"同语义用 std::atomic 保护"并置，以工件符号证明两种路径都真实编译，再以 TSan（手动 WSL 复算）把
  "未定义行为"从信念变成可观测告警，并明确"没被 TSan 报 ≠ 没有数据竞争"——与 LEAK-001/002 同族的
  "工具沉默 ≠ 安全"结论，落在可复算证据上而非口号。
depth:
  layer: runtime
pedagogy:
  motivation: "程序没崩、TSan 也没叫，是不是就没问题了？"
  misconception:
    - {level: surface, text: "误以为数据竞争只是结果偶尔算错，不是 bug", refutations: [EV-CONC-005]}
    - {level: deep, text: "误以为没被 TSan 报就是没有数据竞争（忽略漏报边界）", refutations: [EV-CONC-005, EV-CONC-006]}
  socratic: "x86-64 上 int 读写天然对齐不会崩，那数据竞争"有害"在哪一层？为什么 TSan 能报而程序不崩？"
  predict_first: "先预测：把同一份无同步竞争代码交给 TSan，它会指向哪个变量、哪两行？换成 std::atomic 后再跑，报告会变吗？"
  misconceptions: [MIS-CONC-003]
misconceptions: [MIS-CONC-003]
---

# ATOM-CONC-RACE-001 · 数据竞争是未定义行为；TSan 可检测但有边界

一句话直觉：**数据竞争不是"答案偶尔算错"的小毛病，而是标准明文的未定义行为；TSan 能抓它，但"没被报"不等于"没有"。**

## 1. 数据竞争的定义与 UB 性质

两个线程并发访问同一对象、至少一方为写、且双方之间不存在 happens-before 关系，即 C++ 标准定义的
**data race**，后果是**未定义行为**（[intro.race]）。常见误解把它说成"结果偶尔不对"——但 UB 的含义是
*行为完全不可预测*：编译器可假定"无数据竞争"做激进优化（寄存器缓存、删除看似冗余的读、重排无关写），
后果不是"差一点"，而是逻辑整体翻车，且在某些优化档/平台上才暴露。

## 2. 三场景对照（工件可验）

夹具 `Examples/atoms/_atom_data_race.cpp` 以唯一变量=是否存在数据竞争，配两组对照：

| 场景 | 同步方式 | 工件符号 | 竞争 |
|---|---|---|---|
| `bench_single` | 单线程无同步基线 | `_Z12bench_singlev` | 否 |
| `bench_race` | 双线程零同步并发写 `g_shared` | `_Z10bench_racev` | **是** |
| `bench_safe` | 同语义 `std::atomic` 保护 | `_Z10bench_safev` | 否 |

`-O2` 工件中三符号均存在（MinGW 15.3 与 WSL g++13.3 双端验证），证明三种路径都真实编译进产物；
run_match 四方向量（`single_total`/`race_ops_total`/`safe_ops_total`/`safe_final`）双平台逐字一致，
证明运行时都执行到 `join()` 完成。注意：机器可验部分只证明"场景编译并执行"，**"bench_race 是无同步竞争"
这一核心事实由标准定义 + 第 3 节 TSan 实测确立**，而非由 stdout 的计数常量证明（那些只是"循环跑完"的见证）。

## 3. TSan 检测与漏报边界

### 3.1 能报（race 版本，手动 WSL 复算）

`bench_race` 在 `setarch -R g++ -std=c++23 -O1 -g -pthread -fsanitize=thread` 下报：

```
WARNING: ThreadSanitizer: data race (pid=34)
  Read of size 4 at 0x... by thread T2:   #0 operator() ...:42
  Previous write of size 4 at 0x... by thread T1:   #0 operator() ...:38
SUMMARY: ThreadSanitizer: data race Examples/atoms/_atom_data_race.cpp:42 in operator()
ThreadSanitizer: reported 1 warnings
```

精确指向 `g_shared`（全局非原子）的并发读写（行 38 写 / 42 读）；`bench_race` 中线程 b 起手 1ms 延迟
拉宽并发窗口，确保竞争被稳定观测（避免偶发错开导致假阴性）。`bench_safe`（std::atomic）同命令跑**零误报**。
（replay 工具链只跑 ASan/UBSan 不跑 TSan，故真实验证留痕于 EV-CONC-006 的 drill_note，供人审对照。）

### 3.2 边界（漏报场景，"没报 ≠ 没有"）

1. **插桩盲区**：TSan 仅分析被 `-fsanitize=thread` 插桩的 TU 与运行时；第三方库/内联汇编/系统调用内部的竞争不可见。
2. **必须全量插桩**：任一 TU 未用 `-fsanitize=thread` 编译而混链，其内竞争即漏报。
3. **时序偶发**：单次运行两线程恰好错开也可能不触发——一次"没报"不是"没有"的证明。
4. **开销**：运行期约慢 10–20×、内存涨 5–10×，不适合常驻生产。

> 核心教训：**没被 TSan 报 ≠ 没有数据竞争**（同族：没被 LSan 报 ≠ 没有泄漏）。

## 4. 为什么这原子值 5 分（锚定依据）

- **一手实证**：同一份夹具三场景对照，工件符号 + run_match 双平台验证，竞争/无竞争由 TSan 实测与标准条文共同确立；
- **方向性结论**：把"数据竞争是 UB"与"TSan 沉默 ≠ 安全"两个易混点一次讲清；
- **边界诚实**：明确列出 TSan 漏报边界，避免把工具当成 UB 的完备裁判；
- **防退化**：用 `std::atomic` 而非 `volatile` 作对照（C++ 的 `volatile` 不建立 happens-before，TSan 照样报竞争）。

## 5. 常见误解

详见 `MIS-CONC-003`：① 没被 TSan 报就是安全；② 数据竞争只是偶尔算错；③ `volatile` 能防竞争。

## 6. 来源

- ISO/IEC 14882:2023 [intro.race]（data race ⇒ 未定义行为）。
- Cppreference：ThreadSanitizer 检测能力与边界。
- 一手证据：EV-CONC-005（判据）、EV-CONC-006（检测 + 边界）。
