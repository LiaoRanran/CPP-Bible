---
id: ATOM-MEM-ALLOC-002
title: 分配器策略的时空权衡：arena / pool / bitmap（元数据换灵活性）
domain: MEM
type: mechanism
status: red-team-verified
dal: C
dal_reviewed_by: human:liaoranran  # DAL C: 元数据排序有强证据支撑（统一口径三策略实测），红队通过即可                     # 草稿；晋升链见 docs/kernel/G6_status_levels.md（非 draft 须带 dal + status_history）
verified_by: redteam:g5_batch5
verified_at: 2026-09-12                   # 唯人可置 verified（human:*）
audience: intermediate            # 知道 malloc/new 与容器，但选型时只看"哪个快"的人
cognitive_load: medium            # 需同时持有"三种策略的元数据成本"与"各自的释放模式前提"
prerequisites_readable: true
depth: runtime
pedagogy: >-
  先用一句话把三者串起来（元数据换灵活性），再用同一 workload 的三个量化读数让读者自己看出
  差异从哪来；最后用"释放模式两问"落成选型判据，并显式写下 arena 零碎片的前提
  ——避免把"某个模式下的性质"读成"分配器的属性"。
claim: >-
  三种小对象分配策略的元数据开销与**是否支持单块释放**绑定，可用统一口径
  （struct_bytes + bookkeeping_bytes）量化：同一 workload（1000 次 24 B 分配，-O2）下，
  arena 元数据 total 32 B（struct 32 + bookkeeping 0，**前提：仅批量申请 + 整体释放——
  夹具 `release_all()` 只支持整体重置，中途释放单块会产生不可复用空洞**）；
  bitmap total 181 B（struct 56 + bookkeeping 125 B = 1 bit/块，且随块数线性增长：
  n=8000 时 1056 B）；pool total 8056 B（struct 56 + bookkeeping 8000 B = 8 B/块
  free-list 指针，n=8000 时 64056 B）——排序为 arena << bitmap << pool，
  与"pool 元数据最省"的直觉相反；内部碎片：arena 0、pool 8000 B
  （定长块 32 B => 8 B x 1000）、bitmap 0（位图不占用户区）。
status_history:
  - {level: draft, at: 2026-09-12, by: writer:g5_batch5}
  - {level: red-team-verified, at: 2026-09-12, by: redteam:g5_batch5}
claim_boundary:
  standard: [C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  opt: [-O2]
  platform: [x86-64]
relations:
  - {type: prerequisite, target: ATOM-MEM-ALLOC-001}   # pmr 分配器与内存资源：本卡的池/单调资源属同一族
  - {type: contrasts, target: ATOM-MEM-PERF-003}       # PERF-003 讲分配策略的**时间**代价（平台相关）；本卡讲**空间**权衡（确定性读数）
evidence: [EV-MEM-040, EV-MEM-041]
misconceptions: [MIS-MEM-030]
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [mem.res.monotonic.buffer] / [mem.res.pool]（单调缓冲与池资源的语义差异：是否回收）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [allocator.requirements]（分配器接口与释放语义）", independent: true}
  - {kind: impl_doc, ref: "主流 arena/bump、free-list pool、bitmap 分配器实现说明（元数据与释放模式的对应关系）", independent: true}
first_hand: true
superiority: >-
  多数材料把三种分配器并列介绍却不给**可比的量化读数**，也不说"零碎片"的前提。本原子多给三样：
  ① 同一 workload 下的**确定性**取值（峰值/元数据/内部碎片，双平台逐字相同，可作断言锚）；
  ② 位图元数据的**线性增长实测**（8× 规模 → 7.578× 元数据，并逐项验算 (133−8)×8+8=1008 完全吻合）；
  ③ 把"元数据换灵活性"写成**可操作选型两问**（释放模式 / 大小是否固定），并用 MIS-MEM-030 显式钉住
  arena 零碎片的前提，避免把一种模式下的性质读成分配器的属性。
---

# ATOM-MEM-ALLOC-002 · 分配器策略的时空权衡（草稿）

## 动机：选型时只看"哪个快"，会漏掉空间与释放模式

"arena 没碎片""pool 最快""bitmap 最精确"——这三句话各自都有一个**没说出口的前提**。
本原子用同一 workload 的三个量化读数把它们的前提显性化。

## 机制：元数据换灵活性

| 策略 | 元数据 | 换到什么 | 换不到 |
|---|---|---|---|
| arena（bump） | **8 B**（仅偏移） | 极低开销 + 顺序分配 | **单块释放**（只能整体重置） |
| pool（free-list） | 32 B | O(1) 分配 **与** 单块回收 | 定长块 ⇒ 内部碎片（8 B/块） |
| bitmap（块表+位图） | **133 B**（随块数线性） | 单块回收 + 可查占用 | 元数据随规模增长 |

## 实测（详见 EV-MEM-040 / EV-MEM-041）

| 读数 | arena | pool | bitmap |
|---|---|---|---|
| 峰值（1000 次 24 B） | **24000 B** | 32000 B | 32000 B |
| 元数据 | **8 B** | 32 B | 133 B（8000 块时 **1008 B**） |
| 内部碎片 | **0**（前提见下） | 8000 B | 8000 B |

**零碎片的前提**（MIS-MEM-030）：夹具的 `Arena::release_all()` **只支持整体重置**；
中途释放单块时 bump 指针无法回退 ⇒ 空隙不可复用。跨平台（Windows/WSL）输出**逐字相同**。

## 边界

- 本卡只度量**空间**维度（确定性读数）；**时间**维度（分配延迟/吞吐）是时序数据、跨机器不可复现，
  已由 ATOM-MEM-PERF-003 处理（含"谁更快依赖平台"的实测结论），本卡不重复、不给倍数；
- bitmap 的"可查占用"能力未在夹具中使用，不作能力断言；
- 只测两个规模点（1000/8000），"线性"由两点比与逐项验算支撑，未做多点回归。

## 学习路径

1. 先读 EV-MEM-040 看三者的横向对比，理解"元数据换灵活性"；
2. 再读 EV-MEM-041 看位图元数据的纵向趋势（含逐项验算）；
3. 最后用"释放模式两问"在自己的场景里做一次选型，并用 MIS-MEM-030 检查有没有把前提丢掉。

## Step 1 · Writer 初稿自评（2/5）

初稿写"arena 最省、pool 最快"，无量化、无前提、把三种策略说成各有优点 ⇒ 既不可复算也不可证伪。**自评 2/5**。

## Step 2 · 红队独立审查

> 待独立子 agent 执行（实读夹具与工件；重点核查：零碎片的前提是否写足、位图线性是否有逐项验算、
> 空间维度是否越界到时间维度、与 ATOM-MEM-ALLOC-001 / PERF-003 的重复度）。

## Step 3 · 升 5 分候选

> 待红队结论后逐条回应。

## Step 4 · 人审准备

1. **"空间维度"的收窄是否合适？** 本卡刻意不谈时间（避免与 PERF-003 重复、也避免不可复现数据入锚），
   但选型时时间与空间同等重要——是否需在原子内给出"时间维度见 PERF-003"的显式指路（现已写在边界节）？
2. **两个规模点够不够支撑"线性"？** 现有 133/1008 两点 + 逐项验算吻合；是否值得补 3–4 个规模点做回归？
3. **与 ATOM-MEM-ALLOC-001（pmr）的边界**：本卡用 `std::pmr` 的 monotonic/pool 资源作为实现载体，
   机制部分与 ALLOC-001 是否有重叠需划清？

**自评 4/5**（5 分仅人工授予）；**未原子化、未置 verified**。
