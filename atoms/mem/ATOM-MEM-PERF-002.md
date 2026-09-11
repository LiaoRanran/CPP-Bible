---
id: ATOM-MEM-PERF-002
title: SSO：std::string 为什么短字符串不分配堆内存
domain: MEM
type: pitfall
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
# ---- 认知适切（G5 新增字段）----
audience: intermediate        # 默认读者：天天用 std::string、但以为"每次构造都走堆"的人
cognitive_load: medium        # 需同时持有"SSO 边界两侧的行为"与"实现差异不可移植"两条线索
prerequisites_readable: true  # 前置 ATOM-MEM-NEW-001 / ATOM-MEM-PERF-001 均已 verified
claim: >-
  SSO（Small String Optimization）：短于阈值的字符串存在 string 对象内部缓冲，零堆分配；达到阈值
  才落堆——本机 libstdc++（GCC 15.3.0）阈值 15 字符、sizeof=32，len≤15 构造/拷贝 allocs=0（赋值
  走同一实现路径），len=16 首次落堆。SSO 是实现内建（标准不要求），三实现参数不保证一致
  （libstdc++ 32/15、libc++ 24/22、MSVC 32/15——libc++ 与另两家不同），阈值不可移植。历史：
  C++11 禁 COW 后 libstdc++ 才全面转向 SSO。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-NEW-001}    # 堆分配的代价：SSO 省掉的正是这一步
  - {type: prerequisite, target: ATOM-MEM-PERF-001}   # 移动性能量化：短串"移动=拷贝=搬 32 字节"同一口径
  - {type: contrasts, target: ATOM-MEM-ALLOC-001}     # SSO 是 string 内建策略；allocator 是容器外挂策略
evidence:
  - EV-MEM-029          # 阈值实测：0..24 全长度扫描 + 双通路交叉验证（15→16 阶跃）
  - EV-MEM-030          # 代价差：短拷贝 0 分配 vs 长拷贝 1 分配 vs 拼接越阈落堆（兼证伪 COW 残留）
  - EV-MEM-031          # 形状参数：sizeof=32/capacity=15 实测 + 三实现文档值对比（M2 边界）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [string.requirements]（basic_string 语义：拷贝独立表示，不要求 SSO）", independent: true}
  - {kind: cppreference, ref: "std::basic_string（SSO 为实现惯例；libstdc++/libc++/MSVC 容量差异）", independent: true}
  - {kind: impl_doc, ref: "libc++ string 设计文档（22 字节 SSO）与 MSVC STL 文档（15 字节）——文档值口径", independent: true}
first_hand: true
superiority: >-
  多数教程只说"string 有 SSO、短字符串快"，不给边界也不给可移植性警告。本原子多给三样：① 0..24
  全长度扫描把"阈值"变成可定位的阶跃（15→16），并用计数分配器 + operator new 钩子双通路交叉验证
  同一阈值；② 把性能差量化为确定性分配次数差（短拷贝 0 vs 长拷贝 1），长拷贝 allocs=1 同时证伪
  COW 残留——一张卡打两个误读；③ 用 sizeof/capacity/阈值三值自洽锚定本机布局，并把 libc++/MSVC
  差异以文档值口径显式标注（M2 边界诚实），把"阈值不可移植"写成可操作的实测方法。
depth:
  layer: runtime
  drill_note: >-
    阈值阶跃与操作代价差落在运行期计数（分配次数）；sizeof/static_assert 布局参数落在 compiler 层
    （EV-MEM-031）。SSO 判定在库的类型逻辑层，与优化档无关（-O0/-O2 双跑一致）。
pedagogy:
  motivation: >-
    为什么短的 string 拷贝飞快、长的就慢？"短"是多久？这 15 是标准规定还是实现巧合——换了编译器
    还成立吗？当你把"短字符串不分配"写进性能假设时，你已经赌了一个实现细节。
  misconceptions: [MIS-MEM-022, MIS-MEM-023]   # 全局误解库：string 总是分配堆 / SSO 阈值跨实现相同
  socratic:
    - "std::string 对象本身多大？32 字节怎么塞下一个 100 字符的字符串？"
    - "len=15 和 len=16 的构造差在哪一步？（先答，再看 EV-MEM-029 的扫描）"
    - "短字符串拷贝和移动有区别吗？（提示：数据在对象内部，'偷指针'还偷得到吗）"
  predict_first: >-
    `std::string a(15, 'x'), b(16, 'y'); auto c = a; auto d = b;` —— c 和 d 的构造各发生几次堆分配？
    （先预测，再看 EV-MEM-029/030）
---

## 论断

**SSO 让"短"字符串完全绕开堆——但"短"的边界是实现内建参数，不是标准承诺。**

```text
std::string（libstdc++, 32 字节 union）
  ├─ 短串模式：15 字符缓冲 + size 标记        → 构造/拷贝：0 次堆分配（赋值同路径）
  └─ 长串模式：堆指针 + 容量（低位标记模式）   → 构造/拷贝/赋值：每次 1 次堆分配
阈值阶跃：len 15 → 16（实测，0..24 全长度扫描 + 双通路交叉验证，EV-MEM-029）
```

| 实现 | sizeof(string) | SSO 容量 | 口径 |
|---|---|---|---|
| libstdc++（GCC 15.3.0，本机） | 32 | 15 | **实测**（EV-MEM-031，static_assert + capacity + 分配计数三值自洽） |
| libc++（Clang） | 24 | 22 | 文档值（M2 边界；Clang 列 CI 回填） |
| MSVC | 32 | 15 | 文档值（M2 边界） |

## 为什么（COW 的墓志铭：SSO 是被迫的选择）

C++11 前 libstdc++ 用 COW（拷贝共享缓冲 + 引用计数），长串拷贝 0 分配；C++11 要求独立表示、
禁止有锁引用计数，COW 不再合法——长串拷贝必须真分配（EV-MEM-030 长拷贝 allocs=1 正是这一转变
的可观测结果，COW 下应为 0）。SSO 是"短串完全不碰堆"的对冲：大多数真实字符串都很短。

陷阱面（本原子 type: pitfall 的由来）：
- **越阈即付**：短+短拼接结果不一定短（10+10=20>15 → 立即落堆 1 次，EV-MEM-030）。
- **阈值不可移植**：把"15 字符内零分配"写进性能假设 = 赌实现细节；libc++ 是 22、标准不保证 SSO
  存在（EV-MEM-029/031）。
- **移动不再"更快"**：短串数据在对象内部，移动 = 拷贝（搬 32 字节），与 PERF-001"无资源可偷"
  的结论同构。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-029`（阈值，c++23 -O0/-O2） | len≤15 allocs=0；len=16 allocs=1；max_zero_alloc_len=15；双通路同阈值 | SSO 阶跃在 15→16，libstdc++ 阈值 15 |
| `EV-MEM-030`（代价差，c++23 -O0/-O2） | 短拷贝 0 / 长拷贝 1 / 长赋值 1 / 拼接越阈 1 | 短串操作零分配；C++11 无 COW |
| `EV-MEM-031`（形状，c++23 -O2） | sizeof=32（static_assert）+ capacity=15 + len=15/16 分配计数 | 三值自洽锚定本机布局；三实现参数不同 |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 SSO 不存在，EV-MEM-029 的 len 0..15 应有分配——实测全 0。
- **证伪条件 B**：若短串拷贝也要分配，EV-MEM-030 第 1 行应 ≥1——实测 0；若长串拷贝不分配（COW），
  第 2 行应 =0——实测 1。
- **证伪条件 C**：若 capacity≠SSO 容量（三值不自洽），EV-MEM-031 的 capacity=15 与阈值 15 吻合
  关系破裂——实测吻合。
- 实测：A/B/C 均不成立 ⇒ 本原子经受住了自身证伪条件。

## 学习者常见误解

引用全局误解库：
1. **`[MIS-MEM-022]` std::string 总是分配堆内存**——EV-MEM-029（阈值内 0 分配）+ EV-MEM-030
   （短拷贝 0 分配）双卡反例。
2. **`[MIS-MEM-023]` SSO 阈值所有编译器都一样**——EV-MEM-031 三实现参数对比（15/22/15）+
   "标准不要求 SSO"的条文口径。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（标准条文 + cppreference + 实现文档三源 + 三卡一手实证 + superiority + depth=runtime/compiler + 教学封装）；自评上限 4：libc++/MSVC 参数为文档值非本机实测（M2 边界），Clang 列待 CI 回填。 |

### 4 分锚定依据（Writer 自陈，待红队/人审核）

1. **统一解释有增量**：把"SSO 快"展开为可判定的三件事——边界在哪（阶跃实测）、边界两侧代价差
   多少（分配计数）、边界可不可移植（三实现参数 + 标准口径）；并接上 COW 历史让"为什么是 SSO"
   有因果。
2. **量化到机器证据**：0..24 全长度扫描 + 双通路交叉验证（29）；四组确定性分配计数含 COW 证伪
   （30）；sizeof/capacity/阈值三值自洽（31）；-O0/-O2 双跑全一致。
3. **过程本身有教学价值**：predict_first 先让学习者猜"两个字符串拷贝各几次分配"；初版夹具的
   双重计数假信号（allocs=2）修正留痕，示范"计数通路必须唯一"。
