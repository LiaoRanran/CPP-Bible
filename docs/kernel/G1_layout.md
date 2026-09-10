# G1.3 目录规范与文件模板（Layout & Templates）

> 依据：DRQ-2 选 A（仓库根 `atoms/`，与 `Book/` 平级）+ DRQ-1（L0 全新搭建）。
> 原则：**不动 `Book/` 一个字**；新旧并行，原子体系是新增层。

## 1. 目录结构（本设计决策）

```
CPP-Bible/
├─ atoms/                      # L1 原子库（新增）
│  ├─ README.md                # 本目录用途与准入规则
│  ├─ id_migrations.json       # ID 迁移表（G1 初始化为空表）
│  ├─ mem/                     # 按域分子目录（16 域，见知识地图）
│  │  └─ ATOM-MEM-MOVE-001.md
│  ├─ ub/
│  ├─ stl/
│  └─ ...
├─ evidence/                   # L2 证据库（与原子分离，多对多）
│  ├─ README.md
│  └─ {domain}/
│     └─ EV-{DOMAIN}-{NNN}.md   # 证据卡（附产物路径/命令/哈希）
├─ sources/                    # L0 原料层（只读归档，DRQ-1）
│  ├─ README.md
│  └─ _snapshot/{ts}/ ...       # 原始素材、引用原文、编译器原始输出
├─ docs/
│  ├─ kernel/                  # 本套规范（G1 交付物）
│  └─ adr/                     # 架构决策记录 ADR
└─ Book/                       # L4 出版视图（存量，本轮不动）
```

**mkdocs 约束**（用户指定）：`mkdocs.yml` 必须 exclude `atoms/`、`evidence/`、`sources/`，发布站点只读 L4 组装视图。G1 只登记要求，**改 mkdocs.yml 在 G5 试点时执行并验证站点构建不破**（避免本轮动发布链）。

## 2. 原子文件模板（`atoms/{domain}/ATOM-{DOMAIN}-{TOPIC}-{NNN}.md`）

```markdown
---
id: ATOM-MEM-MOVE-001
title: 移动后源对象处于有效但未指定状态
domain: MEM
type: mechanism            # concept|mechanism|rule|idiom|anti_pattern|pitfall|contrast|evolution|decision|experiment
status: draft              # draft|verified|rejected（唯人可置 verified）
claim: >                   # 一原子=一可独立证伪断言（唯一，单句）
  对含堆指针的类型，std::move 之后源对象仍处于有效状态：可安全析构或赋新值，
  但其值不可依赖（libstdc++ / C++17 / -O2）。
claim_boundary:            # 断言边界：写清什么情况下本断言成立
  standard: [C++17, C++20, C++23]
  compilers: [GCC 15.3.0]
  opt: [-O0, -O2]
  platform: [x86-64 MinGW, Linux]
relations:                 # 关系边（见 M1 第 3 节）
  - {type: prerequisite, target: ATOM-MEM-MOVE-000}
  - {type: misconception_as, target: ATOM-MEM-COPY-001}
evidence:                  # L2 证据引用（多对多，可服务多个原子）
  - EV-MEM-001
  - EV-MEM-002
# ---- 五重剖面（缺一不可）----
sources:                   # ① 多源精炼
  - {kind: iso, ref: "ISO/IEC 14882:2023 [lib.types.movedfrom]", independent: true}
  - {kind: cppreference, ref: "std::move", independent: true}
first_hand: true           # ② 一手实证：证据是否本书自己跑出来的
superiority: >             # ③ 原创内核：逐来源写"本书多给了什么"
  cppreference 只给"有效但未指定"的措辞，本书补了可编译对照实验与汇编证据，
  说明"有效"具体指哪些操作仍安全（析构/赋新值），哪些不是（读值）。
depth:                     # ④ 纵深穿透：钻到哪一层
  layer: asm               # standard|compiler|asm|abi|runtime|hardware
  drill_note: 移动构造调用点见 EV-MEM-002 的 call 指令对照
pedagogy:                  # ⑤ 教学封装
  motivation: 为什么需要"可析构但不可读值"这条中间态？
  misconception:           # 强制分层：surface（一次纠正即可）/ deep（结构性误解，须 ≥2 反例）
    - level: surface
      text: "std::move 会移动对象"
    - level: deep
      text: "移动后源对象一定是空的，可以当空容器用"
      refutations: [EV-MEM-001]     # deep 类必填，且 ≥2 个独立反例
  socratic:
    - "如果把源对象当作空容器使用，什么场景会炸？"
  predict_first: 移动后再调用 size() 会输出什么？（先预测，再看实验）
---

## 论断
（散文展开，可含代码块；代码块必须真实可编译，与 `run_expected.py` 的 //@ 契约兼容）

## 证据
- EV-MEM-001：……

## 反例（证伪导向：让它失败的实验）
- ……

## 学习者常见误解
1. …
```

## 3. 字段标准（元数据）

| 字段 | 类型 | 必填 | 说明/枚举 |
|---|---|---|---|
| `id` | str | ✅ | `ATOM-{DOMAIN}-{TOPIC}-{NNN}`，入库后永久不变 |
| `title` | str | ✅ | 一句话标题 |
| `domain` | enum | ✅ | 16 域之一 |
| `type` | enum | ✅ | 10 类原子类型之一 |
| `status` | enum | ✅ | `draft`/`verified`/`rejected`；**新原子禁止停留在 unverified**（DRQ-4 红线） |
| `claim` | str | ✅ | 单句、可证伪 |
| `claim_boundary` | obj | ✅ | `standard[]`/`compilers[]`/`opt[]`/`platform[]` |
| `relations[]` | list | ✅ | `{type, target}`，type ∈ 11 种关系 |
| `evidence[]` | list | ✅ | 证据 ID 列表（可为空则 status 不得为 verified） |
| `sources[]` | list | ✅ | `{kind, ref, independent}`；`independent` 用于防伪多源 |
| `first_hand` | bool | ✅ | 是否一手实证 |
| `superiority` | str | ✅ | 逐来源写"多给了什么" |
| `depth.layer` | enum | ✅ | 6 层之一 |
| `pedagogy` | obj | ✅ | `motivation`/`misconception[]`/`socratic[]`/`predict_first`；**`misconception` 每项须标 `level: surface\|deep`，`deep` 类必带 `refutations[]` ≥2**（依据：surface 一次纠正即可；deep 是结构性误解，须 ≥2 个独立反例才可能纠偏）。概念混淆/边界误判/工具误用只作**内容组织参考**，不强制为字段 |

**硬约束**（门禁点）：`status: verified` ⟹ `evidence[]` 非空 ∧ `first_hand == true` ∧ `superiority` 非空。这三条是 S2"声明-证据绑定"的最小落地。

### 3.1 统计口径（同一名字有三个数时以本节为准）

G1 监工验收暴露过"同一个词三套口径"的困惑，此处定死并实测备案（2026-09-10）：

| 名字 | 数值 | 口径定义 |
|---|---|---|
| UNVERIFIED（**权威块口径**） | **298** | `metrics.content.verification.unverified`：一个含标记的 cpp 块计 1，块内含多个标记仍计 1 |
| `[UNVERIFIED]` 严格标记 | 298 | 全库精确匹配 `[UNVERIFIED]` 的出现数 |
| `[UNVERIFIED …]` 含变体 | **301** | 另有 3 处方括号内含补充文字（如 `[UNVERIFIED 具体数值]`），语义仍是"未验证"，统计时按标记计 |
| 裸词 UNVERIFIED | 1 | `ch09_cpp26.md:187` 代码注释内"见下文 UNVERIFIED 节"，**非标记、不计入** |
| cpp 块（**CI 编译口径**） | **7572** | `comment_blocks.parse` = `compile_all` = CI 编译报告口径，**认缩进围栏**（`^\s*```cpp`） |
| cpp 块（metrics 统计口径） | 7515 | `metrics_snapshot` 只认顶格围栏；缩进块盲区 57 个（0.75%），移交工具修复波 |

**原子缺口密度 D 的分母取 7572**（原子要验证的是 CI 会编译的块）。引用任何数字必须注明口径。

## 4. 证据文件模板（`evidence/{domain}/EV-{DOMAIN}-{NNN}.md`）

```markdown
---
id: EV-MEM-002
serves: [ATOM-MEM-MOVE-001]      # 多对多：可服务多个原子
kind: asm                        # run|asm|layout|abi|symbol|bench|sanitizer|godbolt|traceable_argument
command: g++ -std=c++17 -O2 -S -masm=intel move_demo.cpp -o move_demo.asm
artifact: Examples/_move_demo.asm
artifact_sha256: <内容寻址哈希，用于复算比对>
matrix: {compiler: GCC 15.3.0, std: c++17, opt: -O2, arch: x86-64}
reproduce: tools/...（一键复现脚本或命令）
expected: 移动构造处出现 call 到移动构造符号，无拷贝分配
actual: 与 expected 一致 / 不一致（记录原文）
verdict: confirm | refute | partial
---
（证据正文：命令、产物节选、结论）
```

不可实证类（历史背景/设计哲学）用 `kind: traceable_argument`：`sources[]` ≥2 个**独立**源 + 时间线 + 权威引用，**禁止造实验**。

## 5. L0 原料层（`sources/`，DRQ-1 选 A）

- 定位：**只读归档快照**，存放原始素材、引用原文、编译器原始输出；**禁止修改**。
- 存量 147 章导入为**只读快照**（`sources/_snapshot/{ts}/Book/...`），后续从 L0 萃取原子，**不直接改原始 md**。
- 快照目录内文件视为不可变；需要修正时新增新时间戳快照，旧快照保留。

## 6. 反例自检（什么情况算没做到）

- 若原子文件没有 frontmatter 而只有散文 → 机器无法绑定证据，**不合格**。
- 若 `evidence/` 与 `atoms/` 合并成一个文件里的字段 → 违背 L2"证据与断言多对多分离"，**不合格**。
- 若 `status: verified` 但 `evidence[]` 为空 → S2 失效，**不合格**。
- 若 `sources/` 里的文件被修改而无新快照 → L0"不可变"失效，**不合格**。
- 若 mkdocs 未 exclude 新目录导致站点构建扫进原子草稿 → 发布污染，**不合格**（G5 执行时验证）。
