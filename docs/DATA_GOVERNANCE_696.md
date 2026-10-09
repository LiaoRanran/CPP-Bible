# DATA_GOVERNANCE_696 — 696 批次数据治理说明

> 本文件由 **696 批次（线 B：工程线）** 新增。
> 任务书要求在「放 `data/`」与「放 `docs/`」之间做**有依据的选择**。本文件给出**决策、证据、
> 数据目录说明与回溯 changelog**。

---

## 1. 决策：数据治理文档放 `docs/`，**不放 `data/`**

**结论**：本批**未在 `data/` 新建任何文件**；数据目录说明与 changelog 合并到本文件
（`docs/DATA_GOVERNANCE_696.md`）。

### 1.1 依据（任务书触发条件：`tools/` 里存在会枚举 `data/` 的校验）

用 grep 在 `tools/*.py` 中检索 `data_manifest` / `listdir('data')` / `data/*.md` 类校验，
**命中三类**：

| 机制 | 位置 | 形态 |
|---|---|---|
| 冻结产物清单 | `tools/gen_693_manifest.py` | 写/校验 `data/693_data_manifest.sha256` + `data/693_data_manifest.json`（`data_manifest`） |
| 目录枚举扫描器 | `tools/auto_executor_640.py:97` | `os.listdir(os.path.join(ROOT, "data"))` 扫描 `data/*.{md,json,jsonl}` |
| 数据目录 glob 校验 | `tools/number_consistency_scan_671g.py` / `terminology_scan_671g.py` | `INCLUDE_GLOBS` 含 `data/*核查*.md`、`data/*报告*.md` |

按任务书"**若存在此类校验，则不要把新文件放进 `data/`**"的保守口径 ⇒ 放 `docs/`。

### 1.2 补充分析（诚实边界：这些机制其实**未必**会被新文件打破）

逐条核查后须诚实说明，避免夸大风险：

* `gen_693_manifest.py --check` 是**闭世界**：它只比对 `TARGETS` 元组里**显式列出**的 14 项，
  **不枚举目录** ⇒ 新增 `data/README_696.md` 不会让它变红。
* `verify_data_integrity.py` 同样用**显式 `REQUIRED` 清单**，不枚举目录。
* `auto_executor_640.py` 的 `listdir` 是**自动修复器**的扫描面（白名单修控制字符/末行换行），
  **不是 pass/fail 门禁**；格式规范的 `.md` 不会触发它。
* `data/governance_docs_manifest.json`（信任根文件）只扫 `References/architecture_架构演进/`、
  `_arch_*/`、`_auto/inbox/` 与根下 `PM_/PUSH_/INDEX_/MATRIX_/CHECKLIST_*.md`，**不扫 `data/`**。

⇒ **技术上**，一个格式规范的 `data/*.md` 大概率不会打破任何门禁。但任务书给出了**明确的触发
条件**且要求保守；同时 `data/` 内邻近**信任根文件**（`data/governance_docs_manifest.json`、
`data/supply_chain/*` 在 `tool_integrity` 哈希面内），往其中塞"文档类"新文件会增加认知负担。
故**采纳保守口径，放 `docs/`**。

---

## 2. `data/` 目录说明（只读描述，不改动）

`data/` 是本仓的**产物与账本目录**，规模约 **1420 个顶层文件**（另有子目录）。按 README §4/§5
与实测归纳，主要分四类：

| 类别 | 代表 | 说明 |
|---|---|---|
| **冻结检测矩阵** | `blindspot_676g_detection_matrix.json`（1147×8）、`676m_a5_matrix_corrected.json`、`683_real_world_detection_matrix.json` | 论文数字的**权威源**，由 `gen_693_manifest.py` 钉 sha256 |
| **判决账本 / 信任根** | `authority/decision_event_v2_ledger.jsonl`（452 事件）、`governance_docs_manifest.json`、`supply_chain/*` | append-only；`tool_integrity` 的 `supply_chain` 节覆盖 |
| **评测集 / 标注材料** | `holdout_expansion/`、`annotation_package/`、`689_annotation_key_mapping.json` | 扩样样本 + 人类标注包（去标识化） |
| **逐批验收报告** | `*_acceptance_report.md`、`*_baseline.md`、`693_*` 系列 | 历史批次留痕（**只增不改**，`number_consistency_scan_671g` 会扫其中的 `data/*报告*.md`） |

**纪律（引用仓库既有约定，非本批新增）**：`data/` 内既有 `.json/.jsonl/.md` 视为**冻结产物**，
不应被随手改写；新增产物由对应批次脚本落盘并在 `gen_693_manifest.py` 登记。

---

## 3. 回溯 changelog（**回溯整理，非权威 git 史**）

> **口径诚实声明**：下表由**文件名批次号前缀 + 文件系统 mtime** 归纳（命令见 §3.2），
> **不是**从 git 历史导出——本批禁跑 git。日期为文件落盘时间的近似值，可能与真实提交日有偏差。

### 3.1 批次时间线（`data/` 顶层文件，2026-09-21 → 2026-10-09）

| 批次区间 | 日期范围 | 主题（据文件名归纳） |
|---|---|---|
| 609–620 | 2026-09-21 ~ 09-25 | 基线 / 验收报告体系建立 |
| 621–633 | 2026-09-22 ~ 09-25 | PCK / 权限 / 自动修复（autoimmune） |
| 634–647 | 2026-09-24 ~ 10-08 | 边界回填、四态判决、攻击边、人审 |
| 648–659 | 2026-09-27 ~ 09-28 | 工具链、口径、语料计数 |
| 660–671 | 2026-09-28 ~ 10-01 | 反事实、逃逸率、drift、透明度日志 |
| 672–677 | 2026-10-01 ~ 10-04 | 扩样（672h）、A5 重跑、缺陷类型分析、克隆感知 |
| 678–691 | 2026-10-07 | 元评估、真实靶场（683，110 条）、互补性、文献矩阵、标注密钥 |
| 692–695 | 2026-10-08 | 环境报告、缺陷类型深度分析、开源准备 |
| **696** | **2026-10-09** | **本批（工程线）：`data/` 内 0 个新文件（刻意）** |
| 697 | 2026-10-09 | （并发批次，非本线）结构 Goodhart / drift 代数 |

* 批次号连续覆盖 **609 → 697**（共 84 个不同批次号；个别号如 649/650/665/696 无顶层文件）。
* **696 在 `data/` 中无文件**——这正是 §1 决策的结果。

### 3.2 复算命令（可复现本表）

```bash
.venv/Scripts/python.exe - <<'PY'
import re, time
from pathlib import Path
from collections import defaultdict
b = defaultdict(lambda: [9e18, 0, 0]); rx = re.compile(r'^(\d{3})')
for p in Path('data').iterdir():
    if p.is_file() and (m := rx.match(p.name)):
        e = b[int(m.group(1))]; t = p.stat().st_mtime
        e[0], e[1], e[2] = min(e[0], t), max(e[1], t), e[2] + 1
for k in sorted(b):
    e = b[k]; print(f"{k:03d} {time.strftime('%Y-%m-%d', time.localtime(e[0]))} n={e[2]}")
PY
```

---

## 4. 边界与未做项

* **未**创建 `data/README_696.md` / `data/CHANGELOG_696.md`（依 §1 决策，内容并入本文件）。
* 本文件**不改动** `data/` 下任何既有文件；§2 的描述为只读归纳，§3 为回溯整理。
* 若维护者认为 `data/` 无门禁风险、希望目录内自带说明，可据 §1.2 的分析另开一批放入 `data/`。
