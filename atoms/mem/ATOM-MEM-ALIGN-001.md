---
id: ATOM-MEM-ALIGN-001
title: 结构体有对齐与填充：成员按对齐排列插 padding，sizeof 含 padding；alignas 可控、memcpy 安全
domain: MEM
type: mechanism
status: verified               # 唯人可置 verified（S1 三权分立）
verified_by: human:liaoranran  # 签署人（非 Agent）
verified_at: 2026-09-11        # 签署日期
# ---- 认知适切（G5 新增字段）----
audience: intermediate         # 默认读者：知道 struct，但以为"成员紧密排列、sizeof=各成员和"
cognitive_load: medium         # 需同时持有"对齐要求"与"padding 使 sizeof 变大"两条线索
prerequisites_readable: true   # 基础原子：无前置（但建议先读 NEW-001 理解对象布局）
claim: >-
  每个类型有对齐要求；结构体成员按自身对齐排列，编译器在成员间/末尾插入 padding，使每个成员与整体满足对齐，
  sizeof 包含 padding（故通常 > 各成员大小之和）。alignas 可提升对齐、alignof 查询对齐；搬运结构体用
  按字节 memcpy（安全），用 reinterpret_cast 强转指针对齐/类型双关是未定义行为。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations: []                 # 基础内存布局原子：无 prerequisite；与 NEW-001（对象布局）是相邻主题
evidence:
  - EV-MEM-019          # padding 量化：offsetof b=4、padding=3、sizeof=8
  - EV-MEM-020          # alignas 可控 + memcpy 安全 + 强转 UB 注释实证
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.align]（对齐要求；alignas/alignof；padding 为使对齐）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [class.mem]（非静态数据成员按声明顺序、满足对齐排列）", independent: true}
  - {kind: cppreference, ref: "Object layout / Data structure alignment（padding、alignas、strict aliasing）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 讲对齐规则，但初学者常卡在"sizeof 为什么比成员和大"。本原子多给：① 把 padding 量化成
  可观测三数（offsetof b=4、padding=3、sizeof=8），而非"有填充吧大概"；② 把"强转指针读字段"的隐患用
  标准条款（[basic.align]/[strict.aliasing]）标注为 UB 并给出 memcpy 这一安全替代；③ alignas 实测可控
  （alignof=16、sizeof=16）。与 NEW-001 分工：NEW-001 讲"分配/释放两层"，本原子讲"对象内部的字节布局"——
  二者共同补全"一块内存长什么样"。
depth:
  layer: compiler
  drill_note: >-
    对齐与 padding 由 [basic.align]/[class.mem] 规定，offsetof/sizeof/alignof 是编译期常量，跨优化档稳定。
    memcpy 安全由 [basic.fundamentals]/[strict.aliasing] 保证（按字节，不重新解释类型）。
pedagogy:
  motivation: struct { char a; int b; } 的 sizeof 为什么是 8 而不是 5？
  misconceptions: [MIS-MEM-015]   # 全局误解库：结构体对齐/padding 误读（MIS-MEM-015）
  socratic:
    - "为什么 int 成员不能放在偏移 1？"
    - "sizeof(struct) 一定等于各成员 sizeof 之和吗？"
    - "把一个 struct 当字节流搬，用 memcpy 还是指针强转？"
  predict_first: 下面结构体的 sizeof 是多少？int b 的偏移是多少？先预测，再看 EV-MEM-019。
---

## 论断

**结构体不是"成员紧挨着排"——每个成员有对齐要求，编译器在中间/末尾塞 padding，让每个成员落在合法地址上；
`sizeof` 包含这部分填充，所以通常大于各成员大小之和。**

```cpp
struct Padded { char a; int b; };   // a 对齐 1（偏移 0）、b 对齐 4（须偏移 4）
// => a 后插 3 字节 padding，b 在偏移 4，整体对齐 4 => sizeof = 8（不是 1+4=5）
```

## 为什么（对齐要求 + padding）

`[basic.align]`：每个类型有对齐要求（如 `int` 在 x86-64 上对齐 4）。成员必须放在满足自身对齐的偏移；
编译器在 `a` 与 `b` 之间插 3 字节 padding，使 `b` 落在偏移 4。`sizeof` 再向上取整到整体对齐的倍数
（`Padded` 整体对齐 4，8 已是倍数；若加 `alignas(16)` 则尾部再补到 16，见 `EV-MEM-020`）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 `sizeof(Padded)==5` 且 `offsetof b==1`（无 padding），则"编译器插 padding"被推翻 →
  `EV-MEM-019` refute。实测 sizeof=8、offsetof b=4、padding=3 ⇒ 经受住证伪（且若真无 padding，int 会未对齐访问 UB）。
- **证伪条件 B**：若 `alignas(16)` 后 `alignof != 16` 或 `memcpy` roundtrip 不为 7，则"alignas 可控 / memcpy 安全"
  被推翻 → `EV-MEM-020` refute。实测 alignof=16、roundtrip=7 ⇒ 成立。
- **证伪条件 C（编译期/标准）**：若 `*(int*)((char*)&s+1)` 合法，则"强转指针读字段安全"成立——但它是未对齐 +
  类型双关 UB（[basic.align]/[strict.aliasing]），不能运行，留作证伪条件文本。
- 实测 A/B 成立、C 为已知 UB ⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用

- **别假设 sizeof == 成员和**：网络/文件序列化要按字段逐个读写或 `memcpy` 到已知布局，不能直接 `sizeof` 当协议长度。
- **用 `offsetof` 而非手算偏移**：布局受对齐影响，手算易错。
- **搬结构体用 `memcpy`/`std::bit_cast`**：不要 `reinterpret_cast` 强转指针对齐/类型双关（UB）。
- **需要特定对齐用 `alignas`**：如 SIMD 类型、与硬件/FFI 对齐的结构。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-015]`（结构体对齐/padding 误读）：本原子用 padding 量化（offsetof b=4、padding=3）
纠正"成员紧密排列"的直觉，并给出 memcpy 这一安全搬运方式替代 UB 的指针强转。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；padding 量化 + alignas 实测 + memcpy 安全。留待人审一点：未演示"强转 UB 的实际崩溃"
  （属未定义行为，不可运行；已在证伪条件 C 标注为标准条款 UB，未实跑）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"结构体布局"从"成员紧密排列"的直觉升级为"按对齐排列 + 插 padding + sizeof 含 padding"的统一规则，并给出 alignas 可控、memcpy 安全、强转 UB 的完整对照。
2. **量化到机器证据**：offsetof b=4、padding=3、sizeof=8 三数互证，alignas 实测 alignof=16/sizeof=16，memcpy roundtrip=7 证安全；强转 UB 用 [basic.align]/[strict.aliasing] 标注为标准条款 UB。
3. **过程本身有教学价值**：先让学习者预测 `sizeof` 与 `int b` 偏移，再用 EV-MEM-019 三数翻转直觉，把 padding 从"大概有"变成可计算事实。

| 五重剖面 | 5/5 | 3 源（ISO [basic.align]/[class.mem] + cppreference）· 一手实证（EV-MEM-019/020 量化）· superiority（padding 量化 + 安全替代）· depth=compiler · 教学封装（predict + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S1 负观测伪证据**：初版只打印 "padding exists" 无量化 → 加 offsetof/padding 计算，使
    "偏移 4 / 填充 3 / sizeof 8"变成可比对输出。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：明写"序列化/FFI 别假设 sizeof==成员和"
  的迁移判据，已补进 "这条原则怎么用"）。
