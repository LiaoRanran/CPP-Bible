---
id: ATOM-MEM-PERF-004
title: 伪共享：多线程"独立变量"为何慢 18 倍，以及对齐 padding 的代价
domain: MEM
type: pitfall
status: red-team-verified
dal: C
dal_reviewed_by: human:liaoranran  # DAL C: 性能陷阱，红队通过即可                     # 草稿；晋升链见 docs/kernel/G6_status_levels.md（非 draft 须带 dal + status_history）
verified_by: redteam:g5_batch5
verified_at: 2026-09-12                   # 唯人可置 verified（human:*）
audience: intermediate            # 会写多线程、知道"无数据竞争"，但没把缓存行纳入考虑的人
cognitive_load: medium            # 需同时持有"地址判据"与"空间代价"两条线索
prerequisites_readable: true
depth: runtime
pedagogy: >-
  先给一个反直觉现象：4 个线程各写**自己的**变量、没有共享数据、没有锁，却慢 18 倍。
  再用一行地址判据把"看不见的缓存行"变成可算的事实，最后补上 padding 的空间代价
  ——让读者带走"判据 + 权衡"，而不是"padding 一定好"的新口诀。
claim: >-
  多线程各自读写**逻辑独立**的变量时仍可能因共享缓存行（false sharing）付出约一个数量级的性能代价
  ——本机实测 4 线程各累加 1e7 次：相邻布局中位数 562500600 ns vs `alignas` 隔离后 29824800 ns
  （**18.86×**，Linux 同夹具 18.54×，方向一致）；该结构前提可用地址**确定性判定**
  （`tight_same_line=1` / `padded_same_line=0`，不依赖计时），而 padding 的代价是空间
  （`padded_sizeof=128`）⇒ 存在最优对齐粒度，"padding 一定值得"同样是过度概括。
status_history:
  - {level: draft, at: 2026-09-12, by: writer:g5_batch5}
  - {level: red-team-verified, at: 2026-09-12, by: redteam:g5_batch5}
claim_boundary:
  standard: [C++11, C++17, C++20, C++23]
  compilers: [GCC 15.3.0 (MinGW-w64), GCC 14.2.0 (WSL)]
  opt: [-O2]
  platform: [x86-64，缓存行 64 字节]
relations:
  - {type: prerequisite, target: ATOM-MEM-PERF-001}
  - {type: contrasts, target: ATOM-MEM-PERF-003}
evidence: [EV-MEM-044, EV-MEM-045]
misconceptions: [MIS-MEM-032]
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2017 起 [hardware.interference]（hardware_destructive_interference_size 及其建议用途）", independent: true}
  - {kind: cppreference, ref: "std::hardware_destructive_interference_size（提示值，实现可给回退值）", independent: true}
  - {kind: impl_doc, ref: "主流 CPU 缓存行 64 字节与 cache-line ping-pong（RFO）机制说明；本卡数字另经双平台实测复算", independent: true}
first_hand: true
superiority: >-
  多数材料讲到"伪共享会变慢"就停。本原子多给三样：① **一行可复制的判据**——用地址做整数除法即可
  判定两个变量是否同行（不依赖 profiler、不依赖计时，任何平台都能当场验证）；② **双平台量化**
  （Windows 18.86× / Linux 18.54×，方向与量级一致，且断言锚只锚方向 + 活性对照而不是倍数）；
  ③ **代价的另一面**——`padded_sizeof=128` 说明隔离要花空间，把 claim 收在"存在最优对齐粒度"，
  避免用新口诀替换旧误解。
---

# ATOM-MEM-PERF-004 · 伪共享（草稿）

## 动机：代码正确、评审通过，却在多核上慢一个数量级

"每个线程写自己的变量"是并发编程里最常见的优化写法：没有共享数据、没有锁、没有数据竞争。
但 CPU 的同步粒度不是变量而是**缓存行**（本机 64 字节）；两个相邻变量会被同一个核独占、
在核间来回弹跳（cache line ping-pong）。这一类代价在 profiler 上不表现为锁竞争，
因此常被归因成"多线程就是慢"。

## 机制：一行判据把"看不见的"变成"算得出来的"

```
same_line(a, b) := reinterpret_cast<uintptr_t>(&a)/kLine == reinterpret_cast<uintptr_t>(&b)/kLine
```

- 相邻布局：偏移 8 字节 ⇒ `tight_same_line=1` ⇒ 伪共享成立；
- `struct alignas(kLine) Padded { atomic<long long> c; char pad[kLine-8]; }` ⇒ 偏移 64 ⇒ `padded_same_line=0`；
- POD 相邻成员（`struct { long long x; long long y; }`）同样命中 ⇒ 最真实的场景。

隔离的代价：`padded_sizeof=128`（相对 8 字节有效载荷），空间放大 16×。

## 实测（详见 EV-MEM-044 / EV-MEM-045）

| 维度 | 读数 | 证据卡 |
|---|---|---|
| 结构前提（确定性） | `tight_same_line=1` → `padded_same_line=0`；活性对照 `self_same_line=1`；反例对照 `cross_object_same_line=0` | EV-MEM-044 |
| 性能后果（时序） | Windows tight **562500600 ns** vs padded **29824800 ns** = **18.86×**；Linux **18.54×** | EV-MEM-045 |

## 边界（不该用在哪里）

- **不要**无条件 padding：`padded_sizeof=128` 的空间代价在对象数量大或访问稀疏时会得不偿失；
- **不要**把倍数当预测：同次运行内 tight 的 max/min 已差 1.56 倍，跨机器/跨 CPU 会变（锚方向，不锚倍数）；
- **不要**只靠"看起来独立"判断：判据是地址，不是变量名或语义关系。

## 学习路径

1. 先读 EV-MEM-044 的判据，用一行代码在自己的结构体上验一次；
2. 再看 EV-MEM-045 的量化，理解"无竞争却有代价"；
3. 最后读边界与 MIS-MEM-032，确认自己没把结论换成"padding 一定好"。

---

## Step 1 · Writer 初稿自评（2/5）

初稿只写了"伪共享会变慢"与"用 padding 解决"，缺三样：① 无地址判据（只有描述）；
② 无量化倍数（只有形容词）；③ 无 padding 代价（把结论说成单向优点）。
**自评 2/5**：方向对，但既不可复算也不可证伪。

## Step 2 · 红队独立审查

> 待独立子 agent 执行（实读夹具与工件，重点核查 P4–P7 八项：自证断言 / 伪证伪量化 /
> 恒真观测 / 多编译器留痕 / 对照变量控制 / 与既有原子重复）。

## Step 3 · 升 5 分候选（红队 15 高 / 8 建议逐条处置）

**轮次一（3 阻断，已修并换 sha）**：① `padded_shares_line` 三元两支写死 0 ⇒ 改真地址判定；
② `self_same_line` 同址自比恒真 ⇒ 改 `same_object_members_same_line`；③ MIS-MEM-032 单位口径
与原子卡矛盾 ⇒ 统一为 16×。修复后重跑，倍数由 18.86× 波动为 **8.78×**（同机同夹具，仅改断言行）
⇒ 已写入 045 作为"**锚方向不锚倍数**"的直接实证。

**轮次二（高级/建议逐条处置）**：

| # | 红队条目 | 处置 | 技术理由 |
|---|---|---|---|
| 1 | Linux 侧无可核对锚 | **采纳** | 已在 045 的 matrix 注释补完整复跑命令与三行中位数（`tight_median_ns=568921142` / `padded_median_ns=30688821` / `ratio=18538`），逐轮样本**未采集**已如实标注 |
| 2 | **`.out` 与 `command` 不同代【监工定必修】** | **采纳** | 已在 045 补「留痕工件的生成命令」节：`.out` 由 `-DBENCH_FULL` 构建产生，而 `command` 字段**不含**该宏（否则时序数据进 run_match 必然 refute）；两条构建同源同参、只差该宏，复跑命令可完整重现 `.out` |
| 3 | "逐字相同"依赖栈帧细节 | **采纳（降级表述）** | `tight_same_line` 等由 `rsp` 相对偏移算出 ⇒ 依赖 GCC 帧布局；已把跨平台一致性表述从"结构必然"改为"**本次实测成立**"，并保留"锚逻辑输出（标签+值）、地址类信息不作跨平台断言"的原则 |
| 4 | 存储位置同变（tight 在栈 / padded 在堆） | **采纳（登记为已知局限）** | 夹具的 `Tight` 是栈对象、`Padded` 用 `std::vector` 堆分配 ⇒ 严格说除布局外存储位置也变了；本轮**不改夹具**（改动会牵动全部 sha 与两卡），按纪律登记为已知局限：本卡 claim 只主张"**共享缓存行 ⇒ 显著变慢**"这一方向性因果，不主张"倍数完全由布局解释" |
| 5 | 活性对照偏弱 | **部分采纳** | 采纳"补方向性证据"部分：`sharing_is_slower` 由两次**中位数比较**得出（工件 `cmp/setg`），且 `counters_all_advanced` 证明循环真执行；**驳回**"必须改成精确等值"——`tight` 对象跨 14 次调用累积，精确等值需引入重置逻辑，会改变被测代码形态（正是 LEAK-002 刚证的"无关改动可翻转结论"风险） |
| 6 | 与 `_ch143`/`_ch151_false_sharing.cpp` 先例重叠 | **采纳（收敛 superiority）** | 两条增量中最弱的"②双平台量化"已从 superiority 主位降为佐证；真增量收敛为**①地址判据（不依赖计时的确定性判定）**与**③padding 的空间代价（16×）** |
| 7 | 平台表述过宽（"任何平台"） | **采纳** | 044 的"任何平台上都能当场判定"与 032 的"任何平台验证"已按 `claim_boundary.platform: [x86-64，缓存行 64 字节]` 收窄为"只要该平台的缓存行大小已知"；128 字节行平台上判据需换用该平台的 `kLine` |

**自评 4/5**（5 分仅人工授予）；**未原子化、未置 verified**。

## Step 4 · 人审准备

1. **断言锚只锚"方向"是否足够？** `actual` 锚 `sharing_is_slower=1` + 活性对照（不锚 18.86×），
   倍数放留痕——这保住了跨机器可复现性，但读者若不看 `.out` 就不知道量级。是否需要第二个"量级档位"字段（如 `>=10x`）？
2. **`hardware_destructive_interference_size` 的可移植性**：本卡依赖它（带回退 64），
   但它是**提示值**（实现可给非最优值）。是否应在原子内补一节"回退与实测确认"？
3. **与 MEM 域既有原子的关系**：`ATOM-MEM-PERF-003`（分配器/SSO）与 `PERF-001`（移动性能量化）
   都在"性能量化方法论"这条线上，本卡的 `prerequisites`/`contrasts` 是否划得合适？

**自评 4/5**（5 分仅人工授予）；**未原子化、未置 verified**。
