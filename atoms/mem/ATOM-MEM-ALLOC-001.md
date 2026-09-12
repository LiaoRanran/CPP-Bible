---
id: ATOM-MEM-ALLOC-001
title: allocator：STL 容器的内存策略抽象
domain: MEM
type: mechanism
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
dal: B                            # 失效后果分级（G6 §3）：B=教学结论方向错；A/B 须人审
human_review: required            # DAL A/B ⟹ 强制人审（G6）
status_history:                   # 四级晋升链（G6 §2），链尾须等于 status
  - {level: draft, at: legacy, by: writer:agent}
  - {level: machine-verified, at: 2026-09-11, by: machine:gate}
  - {level: human-verified, at: 2026-09-11, by: human:liaoranran}
# ---- 认知适切（G5 新增字段）----
audience: expert              # 默认读者：熟练使用 STL 容器、要控制内存来源（池/共享内存/对齐）的人
cognitive_load: high          # 需同时持有"两层分离 / 策略可替换 / 静态与多态两套体系"三条线索
prerequisites_readable: true  # 前置 ATOM-MEM-NEW-001 / ATOM-MEM-RAII-001 均已 verified
claim: >-
  allocator 是 STL 容器的内存**策略**抽象：容器只经 allocator_traits 要内存，不直接调 new/delete。
  C++17 后 std::allocator 只剩 allocate/deallocate 纯分配层（construct/destroy 移除、统一走 traits），
  分配与对象构造是两个独立动作。策略可整体替换：自定义 arena 分配器接入 vector 后 16 次 push_back
  零堆分配；std::pmr（C++17）把策略变成运行时多态——monotonic_buffer_resource 用栈缓冲伺候全部
  分配、全程不触碰上游。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]   # 机器实测仅 c++23 单档（三卡注明）；两层分离/traits
                                                  # 收口与 pmr 自 C++17 起才成立（C++11/14 下
                                                  # std::allocator 仍有 construct/destroy，claim 主干
                                                  # 不跨到那两档），arena/pool 机制则 C++98 起可用
  compilers: [GCC 15.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-NEW-001}    # new/delete 两层：allocator 是它的策略化重演
  - {type: prerequisite, target: ATOM-MEM-RAII-001}   # RAII：容器持有 allocator，资源随容器生命周期
  - {type: contrasts, target: ATOM-MEM-PERF-002}      # SSO 是 string 内建的"分配策略"，与 allocator 抽象互补
evidence:
  - EV-MEM-026          # 两层分离：allocate 零构造、construct/destroy 显式走 traits
  - EV-MEM-027          # 策略可替换：arena 接入 vector，零堆分配 + 同构对照
  - EV-MEM-028          # 运行时多态：pmr monotonic 零上游触碰 + 观测通路修正留痕
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [allocator.requirements]（分配器要求与有状态分配器契约）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [allocator.members] / [mem.poly.allocator]（std::allocator 两层收口 / pmr 多态分配器）", independent: true}
  - {kind: cppreference, ref: "std::allocator、std::allocator_traits、std::pmr::monotonic_buffer_resource", independent: true}
first_hand: true
superiority: >-
  多数教程把 allocator 教成"new/delete 的包装、可以跳过"。本原子多给三样：① 用四组独立计数把
  "分配/构造两层分离"做成机器断言（allocate 零构造 ctors=0），并接到 EV-MEM-017 的 new 两层互证；
  ② 用同构对照（同一 16 次 push_back 序列，唯一变量=策略）把"策略可替换"量化成 calls=5/bytes=124
  vs heap_new=0 vs heap_new=5 的三组数字；③ 诚实留痕本机实测的观测通路陷阱（MinGW 动态 libstdc++
  下 new_delete_resource 的 operator new 调用不经过 exe 替换版本，初版假阴性已修正），这正是
  "证明没发生必须证观测通路活着"的 pmr 版实例。
depth:
  layer: runtime
  drill_note: >-
    两层分离与策略注入是编译期接口语义，但证据落在运行期计数（分配/构造/析构/释放、arena calls/
    bytes、pmr 上游触碰次数）；pmr 的多态是虚表派发（EV-MEM-028 观测路径），arena 的契约要点
    （rebind 共享游标、operator== 判等）在卡内 drill_note 展开。
pedagogy:
  motivation: >-
    想让容器从内存池/共享内存/栈缓冲拿内存怎么办？为什么 vector 的元素构造与内存分配是两件事？
    allocator 到底抽象了什么？——不是 new/delete 的包装，是"内存从哪来"的策略插槽。
  misconceptions: [MIS-MEM-021]   # 全局误解库：allocator 是 new/delete 的包装
  socratic:
    - "vector 扩容时是先 new 内存还是先构造对象？这两步能分开吗？（先答，再看 EV-MEM-026）"
    - "把一个 arena 分配器塞给 vector，容器代码需要改动吗？"
    - "pmr::vector 和 vector<T, MyAlloc> 都能换策略，差别在编译期还是运行时？各付出什么代价？"
  predict_first: >-
    `std::allocator<Widget>::allocate(2)` 之后、`construct` 之前，那 2 个 Widget 已存在吗？
    （先预测，再看 EV-MEM-026 的 ctors 计数）
---

## 论断

**allocator 抽象的是"内存从哪来、怎么还"的策略，new/delete 只是默认策略的实现细节。**

```text
容器 ──(allocator_traits)──> allocator 策略插槽
                                 ├─ 默认：std::allocator ──> ::operator new/delete（两层，见 EV-MEM-017）
                                 ├─ 编译期换：vector<T, MyAlloc>（arena/pool/stack…）
                                 └─ 运行时换：std::pmr::vector（memory_resource 虚接口）
```

- **两层分离**（EV-MEM-026）：`allocate` 只拿内存不构造（实测 ctors=0）；构造/析构走
  `allocator_traits::construct/destroy`。C++17 把 std::allocator 收口成纯分配层。
- **策略可替换**（EV-MEM-027）：arena 策略接入 vector——同一 16 次 push_back 序列，calls=5、
  bytes=124、heap_new=0；默认策略对照组 heap_new=5。容器代码零改动。
- **运行时多态**（EV-MEM-028）：`std::pmr::monotonic_buffer_resource` 用栈缓冲伺候全部分配
  （upstream_allocs=0）；同一容器接到委托堆的资源上，扩容路径 res_calls=5 可见。

## 为什么（这不是 new/delete 的包装）

包装的语义是"换个写法调用同一个东西"；策略抽象的语义是"同一个调用、任意多套实现"。三个可区分
的观测：

| 观测 | new/delete 包装论预言 | 实测 |
|---|---|---|
| allocate 后对象存在吗 | 存在（= new） | ctors=0，不存在（EV-MEM-026） |
| 换 arena 后堆分配次数 | 不变（仍是 new） | heap_new=0（EV-MEM-027） |
| 运行时换策略 | 不可（类型编译期定死） | pmr 构造时注入即可（EV-MEM-028） |

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-026`（两层分离，c++23 -O0/-O2） | allocate: allocs=1 ctors=0；construct: ctors=2；destroy: dtors=2；deallocate: frees=1 | 分配层与对象生命周期是两个独立动作 |
| `EV-MEM-027`（arena 策略，c++23 -O0/-O2） | arena: calls=5 bytes=124 heap_new=0；std: heap_new=5 | 策略可编译期替换，容器零改动 |
| `EV-MEM-028`（pmr 多态，c++23 -O0/-O2） | monotonic: upstream_allocs=0；delegating: res_calls=5 bytes=124 | 策略可运行时注入；栈缓冲零堆 |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 allocate 顺带构造，"两层分离"被推翻——EV-MEM-026 ctors=0 不成立。
- **证伪条件 B**：若容器不经 allocator（arena 接不进来或仍走堆），"策略抽象"被推翻——EV-MEM-027
  heap_new=0 不成立。
- **证伪条件 C**：若 pmr 容器不理会注入的 resource，多态被推翻——EV-MEM-028 res_calls=5 不成立。
- 实测：A/B/C 均不成立 ⇒ 本原子经受住了自身证伪条件。

## 学习者常见误解

引用全局误解库：
1. **`[MIS-MEM-021]` allocator 就是 new/delete 的包装**——三张卡给出三个反例：两层分离（26）、
   零堆替换（27）、运行时多态（28）。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（3 源一手标准引用 + 三卡一手实证 + superiority + depth=runtime + 教学封装）；自评上限 4：扩容指纹（calls=5）依实现，跨编译器仅 GCC（Clang 列待 CI 回填）；观测通路陷阱（MinGW DLL）修正后仅本机实证。 |

### 4 分锚定依据（Writer 自陈，待红队/人审核）

1. **统一解释有增量**：把 allocator 从"new/delete 包装"提升为"策略插槽"统一框架（默认/编译期
   替换/运行时注入三档），并用"包装论预言 vs 实测"的三行对照表把增量讲死。
2. **量化到机器证据**：四组独立计数（26）、同构对照三组数字（27）、上游计数判据（28）；-O0/-O2
   双跑全部一致；观测通路假阴性如实留痕并修正。
3. **过程本身有教学价值**：predict_first 先问"allocate 之后对象存在吗"；初版 pmr 夹具的
   operator new 假阴性教训转化为"观测通路必须验证"的教学点（与 M2 §5 纪律呼应）。
