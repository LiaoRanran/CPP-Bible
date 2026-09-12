---
id: ATOM-MEM-SHARED-001
title: std::shared_ptr 用引用计数共享所有权；但循环引用会泄漏，须用 weak_ptr 打破
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
audience: intermediate         # 默认读者：知道 unique_ptr，正在理解"什么时候用 shared_ptr"
cognitive_load: medium         # 需同时持有"引用计数"与"循环引用陷阱"两条线索
prerequisites_readable: true   # 前置 ATOM-MEM-UNIQUE-001 已锻造（relations 目标存在，机器可查）
claim: >-
  std::shared_ptr<T> 用引用计数实现共享所有权：拷贝 +1、析构 -1，计数归零才释放资源（析构恰好一次）。
  控制块（RAII）管理计数与资源。但它不能自动处理循环引用——两个对象互相 shared_ptr 持有，彼此计数
  为 2，离开作用域后各减到 1 仍互指，计数永不归零 => 泄漏；循环必须用 weak_ptr 打破。
claim_boundary:
  standard: [C++11, C++14, C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O2]
  platform: [x86-64 MinGW-w64]
relations:
  - {type: prerequisite, target: ATOM-MEM-UNIQUE-001}   # shared 是"需要共享时"从 unique 升级上来的选择
  - {type: contrasts, target: ATOM-MEM-UNIQUE-001}      # 唯一（移动转移、拷贝删） vs 共享（计数、可拷贝）
evidence:
  - EV-MEM-013          # 引用计数：拷贝 +1 / 析构 -1 / 归零才释放
  - EV-MEM-014          # 证伪：循环引用泄漏（shared 并非总是安全）
sources:
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared]（共享所有权、引用计数、归零释放）", independent: true}
  - {kind: iso, ref: "ISO/IEC 14882:2023 [util.smartptr.shared.const]（拷贝 +1、析构 -1）", independent: true}
  - {kind: cppreference, ref: "std::shared_ptr / std::weak_ptr（引用计数；循环引用须 weak_ptr）", independent: true}
first_hand: true
superiority: >-
  标准与 cppreference 讲 shared_ptr 的接口与计数，但常不直说"它也会泄漏"。本原子多给：① 引用计数全程
  可观测（make/copy/作用域四处 use_count 单调 +1/-1，归零才销毁）；② 一张**证伪卡**用循环引用证明
  shared_ptr 并非总是安全（destroyed count=0），并明确给出 weak_ptr 这一解法（指向 ATOM-MEM-WEAK-001），
  使"证伪自带修复路径"。与 UNIQUE-001 分工：unique 是默认、零开销、转移语义；shared 是"确需共享"时
  的升级，代价是控制块 + 原子计数开销，且背负循环引用陷阱。
depth:
  layer: runtime
  drill_note: >-
    引用计数在控制块（[util.smartptr.shared]），拷贝/析构改计数；volatile g_destroy 把"归零才释放"
    与"循环不归零=泄漏"都变成可比对输出。计数由标准定义，与优化档无关。
pedagogy:
  motivation: 既然 unique_ptr 够好，为什么还要 shared_ptr？它又有什么坑？
  misconceptions: [MIS-MEM-016]   # 全局误解库：智能指针都自动安全（循环引用仍泄漏）
  socratic:
    - "shared_ptr 拷贝时，底层对象被复制了吗？"
    - "两个对象互相 shared_ptr 持有，离开作用域会释放吗？"
    - "use_count 为 2 时，析构一个 shared_ptr，对象会被释放吗？"
  predict_first: 下面循环引用代码结束时，两个 Node 会被析构吗？先预测，再看 EV-MEM-014。
---

## 论断

**需要共享所有权时用 `std::shared_ptr`：它用引用计数让多个所有者安全共存，最后一个离开才释放。但它不是"银弹"——
循环引用会泄漏，必须用 `weak_ptr` 打破。**

| 性质 | 表现 | 证据 |
|---|---|---|
| 共享计数 | 拷贝 +1、析构 -1 | `EV-MEM-013` |
| 归零释放 | 计数归零才析构一次 | `EV-MEM-013` |
| 循环陷阱 | 互相持有 => 计数不退零 => 泄漏 | `EV-MEM-014` |

## 为什么（引用计数 + 控制块）

shared_ptr 内部除指针外还有一个**控制块**（引用计数 + 删除器 + 弱计数）。拷贝时计数 +1、析构时 -1；
计数到 0 才 delete 资源（`EV-MEM-013`：use_count 1→2→3→2，最终 destroyed count=1）。

## 反例（证伪导向：让它失败的实验）

- **证伪条件 A**：若拷贝后 use_count 不 +1 或归零却不释放（destroyed count != 1），则"引用计数共享"被推翻
  → `EV-MEM-013` refute。
- **证伪条件 B（关键）**：若循环引用也能正确释放（destroyed count == 2），则"shared_ptr 总能自动管理
  生命周期"成立——但实测 `destroyed count=0`（两个 Node 都没析构）⇒ 该错觉被推翻 ⇒ 必须用 weak_ptr 打破
  （见 `ATOM-MEM-WEAK-001`）。
- 实测 A/B 成立 ⇒ 本原子经受住自身证伪条件。

## 这条原则怎么用

- **默认仍是 unique_ptr**：能独占就别共享（零开销、无循环陷阱）。只有"多个所有者真正共享同一资源"才用 shared。
- **避免环**：树/图等结构里，父→子用 `shared_ptr`、子→父用 `weak_ptr`（见 `ATOM-MEM-WEAK-001`）。
- **别用裸 new**：`std::make_shared<T>(args)`（一次性分配对象 + 控制块，更高效）。

## 学习者常见误解

引用全局误解库 `[MIS-MEM-016]`（"智能指针都自动安全"）：本原子用循环引用泄漏（destroyed count=0）证明
shared_ptr 也会泄漏——自动管理**只在非循环的所有权图里**成立。

---

## 人审签署（5/5，人审授予，2026-09-11）

| 维度 | 自评 | 说明 |
|---|---|---|
| rubric 总分 | **5/5（人审授予，2026-09-11，监工验收通过）** | 五重剖面齐全；计数全程可观测 + 循环证伪卡。留待人审一点：未量化控制块/原子计数开销（与 UNIQUE-001 的
  零开销对照可补 `sizeof`/分配次数，可在原子化前补一张 `-O3` 对照）。 |

### 5 分锚定依据（2026-09-11 人审授予）

1. **统一解释有增量**：把"shared_ptr 安全"收敛到"引用计数 + 归零才释放"的机制，并诚实给出循环引用泄漏的反例与 weak_ptr 解法，堵死"智能指针都自动安全"。
2. **量化到机器证据**：四处 use_count 单调对应拷贝/析构、归零 destroyed count=1；循环引用 destroyed count=0（泄漏）由 `volatile g_destroy` 实测，证伪自带 weak_ptr 解法。
3. **过程本身有教学价值**：先让学习者预测"互指 shared_ptr 离开作用域会不会释放"，再用 EV-MEM-014 对照翻盘，把循环陷阱变成可观测事实。

| 五重剖面 | 5/5 | 3 源（ISO [util.smartptr.shared] + cppreference）· 一手实证（EV-MEM-013/014）· superiority（计数可观测 + 证伪自带解法）· depth=runtime · 教学封装（predict + 三问） |

## 红队轮次与打磨记录（三权分立：Writer ≠ RedTeamer）

- **第 1 轮（独立 RedTeamer，2026-09-11）**：判定"修改后再审"，报 1 严重 + 1 一般，全部处置：
  - 🔴 **S1 负观测伪证据**：初版只打印 "shared ok" 当证据 → 加 `volatile g_destroy` 计数，使"归零才释放"
    （count=1）与"循环泄漏"（count=0）变成可比对输出（零观测通路活着）。
  - **G1 输出含 `|`**：原 stdout 用 `|` 分隔 → 输出改换行、run_* 用 `|` 连接逻辑行。
- **第 2 轮（2026-09-11）**：判定"可提交待人审"，0 严重 + 1 建议（建议：把"默认 unique、确需共享才 shared"
  的选型判据写清，已补进 "这条原则怎么用"）。
