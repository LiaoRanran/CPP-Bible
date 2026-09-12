---
id: ATOM-MEM-RAII-001
title: 资源要绑在对象生命周期上：构造获取、析构释放，异常也安全
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
audience: beginner            # 默认读者：会写 new/delete，但靠"记得释放"管资源的人
cognitive_load: low           # 一个对子（构造获取/析构释放）+ 一条异常路径
prerequisites_readable: true  # 基础原子：无前置（beginner 入口）
claim: >-
  RAII 的核心是"资源生命周期绑定到对象生命周期"：构造时获取资源、析构时释放。栈展开时（即使函数
  因异常提前返回）作用域内对象的析构按构造逆序自动调用，因此 RAII 管理的资源在异常路径也不泄漏；
  裸 new/delete 在异常路径跳过 delete 则泄漏。lock_guard、unique_ptr、vector 都是 RAII。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations: []                 # beginner 入口：无 prerequisite；与后续 UNIQUE-001 / SHARED-001 是"同一机制的不同应用"而非前提
evidence:
  - EV-MEM-009          # 主论断：异常路径 RAII 析构仍调用（g_live 归 0），裸路径泄漏（g_live 留 1）
  - EV-MEM-010          # 逆序析构：多对象按构造逆序清理，跨栈帧
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [except.ctor]（栈展开调用已构造完全的子对象/局部对象析构）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [basic.rc]/[class.dtor]（析构函数释放资源；对象离开作用域即调用）", independent: true}
  - {kind: cppreference, ref: "RAII（Resource Acquisition Is Initialization）", independent: true}
first_hand: true
superiority: >-
  标准把 RAII 当作"惯例"给出，但多数初学者是"记住要 delete"的肌肉记忆。本原子多给三样：① 用一组
  可运行对照把"异常也安全"变成观测事实（g_live 在抛异常后仍归 0），而不是"应该会调用"的信念；
  ② 用第二卡证明清理是"基于作用域、逆序、跨栈帧"的通用机制（不止一个对象、不止当前帧），堵死
  "靠人记得释放"的本质脆弱；③ 把 lock_guard / unique_ptr / vector 统一归到同一个机制，给出"凡是
  资源都交给栈对象管"的迁移路径。与 UNIQUE-001 / SHARED-001 分工：它们讲"具体哪种智能指针"，本原子
  讲"为什么要用栈对象管资源"这个更底层的原则。
depth:
  layer: runtime
  drill_note: >-
    RAII 析构调用由 [except.ctor] 的栈展开保证，与优化档无关；EV-MEM-009 用 volatile g_live 把
    "析构是否真被调用"变成可比对输出；EV-MEM-010 把"逆序 + 跨帧"变成可比对输出。
pedagogy:
  motivation: 既然有 new/delete，为什么还要 unique_ptr / lock_guard？
  misconceptions: [MIS-MEM-013, MIS-MEM-014]   # 全局误解库：裸资源管理靠记得释放 / delete 放函数尾就够（均异常路径泄漏）
  socratic:
    - "如果在 new 和 delete 之间抛了异常，delete 还会执行吗？"
    - "函数里有 3 个局部对象，抛异常时它们按什么顺序析构？"
    - "lock_guard 和 vector 的共同点是什么？"
  predict_first: 下面函数抛异常后，栈上对象的析构会被调用吗？先预测，再看 EV-MEM-009。
---

## 论断

**资源要交给栈上的对象管：构造时获取、析构时释放。这样"资源活多久"由"对象活多久"决定，人不必记得释放。**

普通 `new`/`delete` 是"手动记账"：你得保证**每条**路径（正常返回、提前 return、抛异常）都走到 `delete`。
只要有一条漏了，就泄漏。RAII 把这件事交给语言：对象离开作用域时，析构**必然**被调用——包括因异常
而提前离开作用域的栈展开路径。

## 为什么（栈展开保证析构）

`[except.ctor]`：异常沿调用栈向上传播时，每一层已构造完全的局部对象、子对象，其析构按构造的
**逆序**被自动调用。这不是"好心优化"，是语言保证——所以 RAII 对象在异常路径也释放资源。

## 证据

| 证据 | 观测 | 结论 |
|---|---|---|
| `EV-MEM-009`（异常路径，c++23 -O2） | 抛异常后 `RAII dtor ran`，`g_live` 回到 0；裸路径 `g_live` 留 1 | RAII 析构在异常后仍调用（不泄漏）；裸 new 泄漏 |
| `EV-MEM-010`（逆序清理，c++23 -O2） | 构造 A B C，展开后析构 C B A，跨 main→f 栈帧 | 清理基于作用域、逆序、跨帧，是通用机制 |

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若 safe_path 抛异常后 `g_live` 仍非 0（RAII 析构没被调用），则"栈展开自动析构"被推翻 → `EV-MEM-009` refute。
- **证伪条件 B**：若展开后析构不是逆序（或漏掉某对象），则"基于作用域的逆序清理"被推翻 → `EV-MEM-010` refute。
- 实测：A 不成立（g_live=0）、B 不成立（C B A 严格逆序）⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用（迁移路径）

凡是"需要成对 acquire/release"的东西，都用栈对象包一层：
- 互斥量 → `std::lock_guard` / `std::scoped_lock`（构造加锁、析构解锁）
- 裸指针 → `std::unique_ptr` / `std::shared_ptr`（析构 `delete`）
- 动态数组/缓冲区 → `std::vector` / `std::string`（析构释放）

别写 `new` 后指望自己 `delete`——异常会让那条路径消失。

## 学习者常见误解

引用全局误解库：
1. **`[MIS-MEM-013]` 裸资源管理靠"记得释放"**：本原子用泄漏对照（g_live 留 1）证明"记得"在异常路径会失败。
2. **`[MIS-MEM-014]` "delete 放函数尾就够"**：本原子证明只有正常路径到尾才够；异常提前离开作用域时，
   只有析构（RAII）能保证释放，尾部的 `delete` 不可达。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全，两卡互证（会被调用 + 顺序确定）。留待人审一点：未跑 -O0 双验（RAII 析构由语言语义保证、与优化无关，已在卡内注明；可在原子化前补 -O0 同输出留痕）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"RAII = 构造获取 / 析构释放"提升为一条跨 new/delete、lock_guard、unique_ptr、vector 的通用原则，给出"凡资源都交给栈对象管"的迁移路径，而非罗列各容器的释放写法。
2. **量化到机器证据**：用 `volatile g_live` 计数把"析构到底调没调用"变成可比对输出——异常路径 RAII 析构后 g_live 归 0、裸路径留 1，第二卡再证"逆序 + 跨栈帧"，两层都落机器输出而非信念。
3. **过程本身有教学价值**：先让学习者预测"抛异常后析构调不调"，再用 EV-MEM-009 对照翻转直觉，把"靠人记得释放"的本质脆弱变成一次可复现的观测，迁移判断内化为方法。

| 五重剖面 | 5/5 | 3 源（ISO [except.ctor]/[class.dtor] + cppreference）· 一手实证（g_live 0/1 对照 + 逆序跨帧）· superiority（统一迁移路径）· depth=runtime · 教学封装（predict_first + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S1 负观测伪证据**：初版只打印 "RAII dtor ran" 当证据，泄漏对照没有可观测量 → 加 `volatile g_live`
    计数器，使"不泄漏/泄漏"变成 g_live 0/1 的可比对输出（零观测通路活着）。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：把 lock_guard/unique_ptr/vector
  统一归到 RAII 的迁移路径，已补进 "这条原则怎么用" 一节）。
