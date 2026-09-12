---
id: ATOM-MEM-RAII-002
title: Rule of 0/3/5：什么时候该写析构函数，什么时候不该
domain: MEM
type: rule
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
audience: intermediate        # 默认读者：会写析构函数、但以为"写了析构就安全了"的人
cognitive_load: medium        # 需同时持有"隐式生成的生成/删除规则"与"成员形状驱动语义"两条线索
prerequisites_readable: true  # 前置 ATOM-MEM-RAII-001 / ATOM-MEM-MOVE-002 均已 verified
claim: >-
  特殊成员函数要不要写，判据是"成员形状"而非记忆口诀：成员全是 RAII 类型（unique_ptr/vector/string）
  时一个都不写（Rule of Zero）——编译器隐式生成的特殊成员函数语义全部正确（可拷贝成员拷贝隐式生成
  且语义正确、不可拷贝成员如 unique_ptr 的拷贝被删除，移动/析构正确生成；实测 allocs=dtors=frees=1）；
  管理裸资源时三件套（析构/拷贝构造/拷贝赋值，Rule of Three）或五件套（+ 移动构造/移动赋值，Rule
  of Five）必须齐写——只写析构会得到隐式浅拷贝，同一资源两次析构，析构真释放即 double free；
  写移动构造必须标 noexcept，否则 vector 扩容搬迁退化为逐个拷贝。
  （Rule of Zero 的隐式语义按成员形状各得其所：可拷贝 RAII 成员的拷贝**隐式生成且语义正确**，
  不可拷贝成员如 unique_ptr 的拷贝被**删除**——不是一律"删除拷贝"。）
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-RAII-001}   # RAII 与异常安全：本原子回答"RAII 类自己怎么写"
  - {type: prerequisite, target: ATOM-MEM-MOVE-002}   # 移动语义：五件套的移动两个从哪来
  - {type: contrasts, target: ATOM-MEM-UNIQUE-001}    # unique_ptr 是 Rule of Zero 的首选成员材料
evidence:
  - EV-MEM-023          # Rule of Zero：成员形状驱动隐式规则（类型系统 + 运行期恰一次观测）
  - EV-MEM-024          # 违反 Rule of Three：隐式浅拷贝 → 一块资源两次析构（WSL ASan 实报 double-free）
  - EV-MEM-025          # Rule of Five 细节：移动不标 noexcept → vector 扩容退化为拷贝
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [class.copy.ctor]/[class.copy.assign]（隐式拷贝/移动的生成与删除规则）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [class.dtor]（隐式析构逐成员析构）", independent: true}
  - {kind: cppreference, ref: "Rule of three/five/zero、std::move_if_noexcept（vector 扩容用移动的条件）", independent: true}
first_hand: true
superiority: >-
  多数教程把 Rule of 0/3/5 教成三句口诀，读者记住结论却不会判"哪条适用于我"。本原子多给三样：
  ① 用同一套计数纪律做三卡对照（Rule of Zero 全对 / 违反 Three 浅拷贝 / Five 漏 noexcept 退化），
  每张卡唯一变量明确、有区分力；② 把"只写析构"的后果做成确定性观测（观测型析构：一块资源两次
  析构）并补 WSL ASan 真实 double-free 报告（attempting double-free in ~Buggy），因果链完整且可复核；
  ③ 把"漏 noexcept"的代价量化为 -O0/-O2 一致的搬迁计数（copies=4 moves=0），堵死"写了移动就行"的
  半步误解。
depth:
  layer: runtime
  drill_note: >-
    隐式规则链（[class.copy.ctor]/[class.dtor]）是编译期语义，但本原子的核心证据落在运行期计数
    （分配/析构/释放次数、搬迁的拷贝/移动次数）；类型系统论证（is_copy_constructible 等）作为
    EV-MEM-023 的编译期观测点同卡互补。
pedagogy:
  motivation: >-
    什么时候要写析构函数？写了析构为什么还会 double free？写了移动构造为什么 vector 扩容还是慢？
    ——判据不是"记得写"，是成员形状；三条规则的适用条件，三条机器证据各管一条。
  misconceptions: [MIS-MEM-019, MIS-MEM-020]   # 全局误解库：写了析构就够 / Rule of Zero 是什么都不写
  socratic:
    - "只写析构函数、不写拷贝构造，编译器生成的拷贝是什么语义？两个对象析构时会发生什么？"
    - "Rule of Zero 的'零'指什么？前提不满足（成员是裸指针）时会发生什么？"
    - "vector 扩容搬迁元素时，用什么规则决定移动还是拷贝？你的移动构造满足它吗？"
  predict_first: >-
    `struct B { int* p; ~B(){ delete p; } };` 两个 B 互相拷贝后离开作用域——会发生几次释放？
    （先预测，再看 EV-MEM-024 与其 ASan 报告）
---

## 论断

**Rule of 0/3/5 不是三句口诀，是同一判据的三种取值：成员形状。**

| 成员形状 | 该写什么 | 机器证据 |
|---|---|---|
| 全是 RAII 类型（unique_ptr/vector/string…） | 一个都不写（Rule of Zero）——隐式特殊成员函数语义全部正确：可拷贝成员拷贝可用、不可拷贝成员拷贝被删、移动/析构正确生成 | `EV-MEM-023`：allocs=1 dtors=1 frees=1，move=1 copy=0 |
| 管裸资源（raw pointer/句柄/连接） | 三件套齐写（Rule of Three）/ 五件套（Rule of Five） | `EV-MEM-024` 对照组：深拷贝 same_ptr=0 |
| 写了移动构造 | 必须标 noexcept，否则 vector 搬迁用拷贝 | `EV-MEM-025`：copies=0 moves=4 vs copies=4 moves=0 |

## 为什么（只写析构函数是三件套里最危险的"半步"）

用户声明了析构函数 ⇒ 编译器**仍会**隐式生成拷贝（已废弃语义，但能用）——生成的是**逐成员浅拷贝**。
后果链（EV-MEM-024 实测）：

```text
只写析构 → 隐式浅拷贝（allocs=1, same_ptr=1）→ 一块资源两次析构（dtor_runs=2）
         → 若析构真释放 → double free（WSL ASan 实报：attempting double-free in ~Buggy()）
```

Rule of Zero 之所以"什么都不写反而全对"，是因为正确性由**成员类型组合**保证，不靠程序员记忆：
unique_ptr 可移动 ⇒ 移动成员隐式生成；不可拷贝 ⇒ 拷贝被删；成员析构自动逐个调用 ⇒ 恰一次释放。

## Rule of Five 的一个静默陷阱（noexcept）

vector 扩容搬迁走 `move_if_noexcept`：移动构造**标了 noexcept** 才用移动。`Noex(Noex&&) noexcept`
搬迁 moves=4 copies=0；`Throwing(Throwing&&)`（漏标）搬迁 copies=4 moves=0——同一个关键字决定
每次扩容是"搬指针"还是"整块重拷"，编译器不告警（EV-MEM-025，-O0/-O2 一致）。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-023`（Rule of Zero，c++23 -O0/-O2） | 5 条 static_assert（move_constructible=1 copy_constructible=0）+ owner_changed=1 + allocs=1 dtors=1 frees=1 | 成员形状驱动隐式规则全部做对 |
| `EV-MEM-024`（违反 Three，c++23 -O2） | buggy 组 allocs=1 same_ptr=1 dtor_runs=2；correct 组 allocs=2 same_ptr=0 | 隐式浅拷贝 → 一块资源两次析构；ASan 实报 double-free |
| `EV-MEM-025`（Five/noexcept，c++23 -O0/-O2） | noexcept 组 copies=0 moves=4；漏标组 copies=4 moves=0 | 搬迁方式由 noexcept 决定，退化静默发生 |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 Rule of Zero 不安全（零声明导致拷贝可用或析构不正确），EV-MEM-023 的
  static_assert 编译红或计数失衡（dtors≠allocs）。
- **证伪条件 B**：若隐式拷贝不是浅拷贝（same_ptr=0 或 allocs=2），EV-MEM-024 的"只写析构 → 共享
  资源"链条断裂；对照（correct 组）证明实验有区分力。
- **证伪条件 C**：若 noexcept 不影响搬迁（两组都 moves=4 或都 copies=4），move_if_noexcept 语义被
  推翻——实测两组数字不同。
- 实测：A/B/C 均不成立 ⇒ 本原子经受住了自身证伪条件。

## 学习者常见误解

引用全局误解库：
1. **`[MIS-MEM-019]` 写了析构函数就够了**——EV-MEM-024 证明隐式浅拷贝会把"写了析构"变成 double
   free；三件套要齐，或者干脆 Rule of Zero。
2. **`[MIS-MEM-020]` Rule of Zero 是什么都不写**——EV-MEM-023 补全前提：判据是成员形状（全 RAII
   才可零声明），不是"不写"本身。

---

## Writer 自评（最高 4，不自称达标）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **4/5** | 五重剖面齐全（3 源一手标准引用 + 三卡一手实证含 ASan 旁证 + superiority + depth=runtime + 教学封装）；自评上限 4：ASan 捕获为 WSL 人工复现（非 replay 机器口径），跨编译器仅 GCC（Clang 列待 CI 回填）。 |

### 4 分锚定依据（Writer 自陈，待红队/人审核）

1. **统一解释有增量**：把三句口诀收拢为"成员形状"单一判据（0/3/5 是它的三种取值），并把
   "半步陷阱"（只写析构 / 漏 noexcept）作为独立教学点给出量化后果。
2. **量化到机器证据**：三卡共用一套计数纪律、互相构成对照对；double-free 因果链补 WSL ASan
   实报（释放点栈帧直指析构函数）；-O0/-O2 双跑一致（EV-MEM-025 双档同串）。
3. **过程本身有教学价值**：predict_first 先让学习者预测 double-free 次数；观测型析构的取舍
   （为何不真 delete）在卡内如实交代，本身是"如何为 UB 设计可复现观测"的示范。
