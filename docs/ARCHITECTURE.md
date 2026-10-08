# ARCHITECTURE · 系统架构

> 本文回答：**这个仓库的东西是怎么组织起来的，数据从哪来到哪去，信任根在哪。**

---

## 1. 两层结构

本仓库装两条线，它们**共享信任根与门禁设施，但产物互不混淆**：

```
┌──────────────────────── 研究线（Queyi）────────────────────────┐
│  样本与标签                检测执行              分析与论文            │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │ holdout 41   │      │ asan/ubsan/  │      │ 盲区地图      │  │
│  │ corpus 64    │ ──►  │ tsan (WSL)   │ ──►  │ A5 主端点     │  │
│  │ 扩样 1042    │      │ compiler-warn│      │ 可检测性模型  │  │
│  │ 真实靶场 110 │      │ /cross/linker│      │ 反事实分析    │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│        │                      │                      │           │
│        ▼                      ▼                      ▼           │
│   1147×8 冻结矩阵 ────► append-only 判决账本 ────► 论文数字        │
└──────────────────────────────────────────────────────────────────┘
                              ▲
                              │ 共享信任根（34 条哈希面 / Merkle 供应链 / 透明日志）
                              ▼
┌──────────────────────── 书籍线（C++ 圣经）──────────────────────┐
│  Book/ 147 章 ──► atoms/ 知识卡 ──► evidence/ 证据卡              │
│        │                │                  │                     │
│        └────────────────┴──────────────────┴──► tools/ 67 条判决规则│
│                                                  + 9 个保护器      │
│                                                        │           │
│                                                        ▼           │
│                                              web/ 静态站（星图/验哈希）│
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. 研究线：数据流（五段）

### 段 1 · 样本与标签

| 来源 | 规模 | 说明 |
|---|---:|---|
| `data/holdout/` | 41 | 盲化 holdout，历史层 |
| 外部 corpus | 64 | 外部语料 |
| `data/holdout_expansion/` | 1042 | expA–expG 七批扩样 + 1094 个源文件 |
| `data/real_world/` | 110 | 真实缺陷**重构**靶场（CVE/issue/commit 可追溯） |

标签闭集：**34 项 `defect_type`**（`data/676m_sample_manifest_corrected.json::vocabulary`），
由 681 批次从 56 个 legacy 取值归一化而来（映射表 `data/681_归一化映射表.md`）。

### 段 2 · 检测执行（八资产）

```
                    ┌─ asan ──────────┐
                    ├─ ubsan ─────────┤  WSL Ubuntu 24.04 + g++ 13.3
                    ├─ tsan ──────────┤  （-O0 / -O2 双档，60s 超时）
  样本 ──► 编译/运行 ─┼─ compiler-warn ──┤
                    ├─ cross-compile ─┤  MinGW g++ 13.1 + clang 22.1.8
                    ├─ linker ────────┤
                    ├─ wunsequenced ──┤  ⚠ MinGW g++ 不认 ⇒ 恒 unknown（673u）
                    └─ compile-time ──┘  ⚠ 无本地检测器 ⇒ 恒 unknown
```

**四态判决**：`catch` / `miss` / `unknown` / `contradiction`。
关键纪律：**`unknown` 不能折叠进 `miss`**——"没测"和"测了没中"是两回事
（692 已量化：E1 的捕获有 58.82% 在 E2 **从未被测量**）。

### 段 3 · 冻结产物

- `data/blindspot_676g_detection_matrix.json` —— **1147 × 8**，权威冻结矩阵
- `data/683_real_world_detection_matrix.json` —— **110 × 8** 真实靶场
- `data/authority/decision_event_v2_ledger.jsonl` —— **452 条** append-only 判决事件

完整性由 `tools/gen_693_manifest.py` 的 **14 项 sha256 清单**守护，
CI（`.github/workflows/ci.yml::research-gate`）逐条比对，缺一错一即 FAIL。

### 段 4 · 分析

| 分析 | 产物 |
|---|---|
| 检测器深度 Benchmark | `data/676l_*.md`（单资产 recall / k=1..8 穷举） |
| A5 主端点 | `data/676f_A5重跑报告.md`（FD vs Random vs Static） |
| 敏感性 | `data/682_*`（split / 5000 种子 / 255 资产子集） |
| 反事实 | `data/686_*`（样本量 / 资产集 / 标签质量 / 噪声） |
| 环境感知 | `data/692_environment_*`（E1/E2 配对 + 能力撤退扫描） |
| 可检测性模型 | `data/693_detectability_model.json`（693-E3） |

### 段 5 · 论文与门禁

- 主稿：`research/latex/queyi_neurips2027_v1.1.tex`
- 数字对账：`tools/verify_paper_numbers.py`（fail-closed）
- 门禁：`tools/paper_quality_gate_670c2.py`（页数 / 摘要 / TODO 占位）
- 一键复现：`scripts/reproduce_all.sh`

---

## 3. 信任根

```
   tools/ 工具本体 ──► 34 条哈希面（tools/tool_integrity.py --check）
   data/supply_chain/ ──► Merkle 目录根
   data/authority/ ──► 452 条判决账本（append-only + 哈希链）
   data/ 冻结产物 ──► 14 项 sha256 清单（tools/gen_693_manifest.py）
```

**判决与签名永远留给人**：AI 可以产出候选，但账本里的每一条判决事件都由人类作者签署。

---

## 4. 目录职责

| 路径 | 职责 | 是否可写产物 |
|---|---|---|
| `data/` | 全部**产物**与账本 | ✅（append-only 语义；已冻结的矩阵不改） |
| `data/holdout_expansion/` | 评测集（源 + 逐样本 JSON） | ✅ |
| `data/annotation_package/` | 人类标注材料包（去标识化） | ✅ |
| `tools/` | 门禁 / 判决 / 分析 / 复现脚本 | — |
| `scripts/` | 一键复现与环境体检 | — |
| `docker/reproduce/` | 复现镜像 | — |
| `docs/` | 规范与研究报告 | ✅ |
| `research/latex/` | 论文主稿 | ⚠ 投稿冻结期内只写"建议"文件 |
| `tests/` | pytest（fast / slow 两阶段） | — |
| `out/` `build/` | 复现与构建的输出（不入账本） | ✅ |

---

## 5. 三条不变量

1. **每个数字都能被独立复算** —— 数字来自 `data/` 下已落盘的产物，不是从论文抄回仓库。
2. **每条结论都能被攻击** —— 四态判决 + 反事实分析 + 能力撤退扫描，让"结论依赖什么"显式化。
3. **不知道就说不知道** —— `unknown` 不折叠、未闭合项保留 `⬜`、人类 IAA 为 0 就写 0。
