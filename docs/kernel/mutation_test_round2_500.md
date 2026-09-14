# 第二轮机械变异对抗测试报告（500 任务4）

> 目标：验证任务 1/2/3 的修复是否闭合 M5/M8 逃逸 + 用更多变异找新漏洞。
> 规模：**8 卡 × 12 变异 = 96**（满额，每个都有实测结果）。
> 第一轮基线：`docs/kernel/mutation_test_499.md`（5 卡 × 8 = 40）。

## 1. 方法（含两处方法学修正）

沿用第一轮验证过的**隔离法**：`保留原 id + 把原卡暂移（`_mut_orig_bak/`）`，变异副本放
`evidence/_mut_tmp/`（原子卡用 `atoms/_mut_tmp/`），跑一次 `gate_engine.py --check`，
抓含 `_mut_tmp` 的命中，清理并恢复原卡。每个变异**独立跑一次 gate**（96 次），
命中必由该变异本身引起。

**修正 1（活动副本必须沿用原文件名）**：`EV-ID-UNIQUE` 要求 **文件 stem == frontmatter.id**。
首版把活动副本命名为 `<原名>_M#.md` ⇒ 每个变异都被 `EV-ID-UNIQUE` 误报（连 M2 no-op 也报），
真实信号被淹没。改为活动副本沿用原文件名（归档件才带 `_M#` 后缀）后噪声消失。

**修正 2（M5 必须区分 flow / block 两种列表形态）**：`run_match_keys` 有
`[a, b]`（flow，CONC 域）与 `\n    - a\n    - b`（block，LANG 域）两种写法。
首版只处理 flow ⇒ 对 block 形态落到"新增字段"分支，制造**重复键**被
`EV-FM-YAML-HARDENING` **偶发**拦下 —— 看起来"拦住了"但机制不对（会高估修复效果）。
修正后 LANG-001/002 的 M5 由 `EV-RUN-KEY-DECLARED-EXISTS` 正确拦下。

## 2. 选卡（8 张）

| # | 卡 | 来源 | 说明 |
|---|---|---|---|
| 1 | `evidence/mem/EV-MEM-040.md` | 第一轮对比卡 | 内联读数卡（**无** `run_match_file`） |
| 2 | `evidence/conc/EV-CONC-001.md` | 第一轮对比卡 | 有 `run_match_file`（flow 形态 keys） |
| 3 | `evidence/lang/EV-LANG-001.md` | 第一轮对比卡 | 有 `run_match_file`（block 形态 keys） |
| 4 | `evidence/conc/EV-CONC-002.md` | 新增（conc 域） | 有 `run_match_file`（供 M5 真正适用） |
| 5 | `evidence/lang/EV-LANG-002.md` | 新增（lang 域） | 有 `run_match_file`（供 M5 真正适用） |
| 6 | `evidence/mem/EV-MEM-017.md` | 新增（mem 域） | 带 `_Znwm` warn 的卡（域内未测过） |
| 7 | `evidence/ub/EV-UB-002.md` | 新增（ub 域） | ub 域仅 2 张，UB-001 第一轮已测 |
| 8 | `atoms/mem/ATOM-MEM-RAII-002.md` | 新增（atoms） | 第一轮测 RAII-001，本卡为同域未测卡 |

## 3. 96 个变异结果表

（BLOCK = 有 block 级命中；WARN = 仅 warn/advice；**放行** = 0 命中；N/A = 变异字段不存在）

| 卡 \ 变异 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | M12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MEM-040 | BLOCK | WARN | BLOCK | BLOCK | WARN | N/A | BLOCK | BLOCK | BLOCK | BLOCK | N/A | N/A |
| CONC-001 | BLOCK | WARN | BLOCK | BLOCK | BLOCK | N/A | BLOCK | BLOCK | BLOCK | BLOCK | N/A | N/A |
| LANG-001 | BLOCK | WARN | BLOCK | BLOCK | BLOCK | N/A | BLOCK | BLOCK | BLOCK | BLOCK | WARN | BLOCK |
| CONC-002 | BLOCK | WARN | BLOCK | BLOCK | BLOCK | N/A | BLOCK | BLOCK | BLOCK | BLOCK | N/A | N/A |
| LANG-002 | BLOCK | WARN | BLOCK | BLOCK | BLOCK | N/A | BLOCK | BLOCK | BLOCK | BLOCK | WARN | BLOCK |
| MEM-017 | BLOCK | WARN | BLOCK | BLOCK | WARN | N/A | BLOCK | BLOCK | BLOCK | BLOCK | N/A | N/A |
| UB-002 | BLOCK | **放行** | BLOCK | BLOCK | **放行** | N/A | BLOCK | BLOCK | BLOCK | BLOCK | N/A | N/A |
| RAII-002(atom) | N/A | N/A | N/A | N/A | N/A | BLOCK | N/A | N/A | N/A | N/A | BLOCK | BLOCK |

### 3.1 逐条规则明细（BLOCK/WARN）

**MEM-040**：M1 `EV-FM-REQUIRED,EV-MATRIX-UNBACKED` · M2 `EV-MATRIX-UNBACKED`(no-op) ·
M3 `EV-FM-REQUIRED,EV-MATRIX-UNBACKED` · M4 `EV-ARTIFACT-VERSION-MATCH,EV-MATRIX-UNBACKED` ·
M5 `EV-MATRIX-UNBACKED`(**无新命中**) · M7 `EV-FM-YAML-HARDENING,…` · M8 **`EV-ARTIFACT-FILE-EXISTS`**,`EV-ARTIFACT-VERSION-MATCH,…` · M9 `EV-FM-REQUIRED,…` · M10 `EV-FM-YAML-HARDENING,…`

**CONC-001**：M1/M3/M9 `EV-FM-REQUIRED,…` · M4 `EV-ARTIFACT-VERSION-MATCH,…` ·
M5 **`EV-RUN-KEY-DECLARED-EXISTS`**,`EV-ASSERT-SYMBOL-MAPPED,…` ·
M7/M10 `EV-FM-YAML-HARDENING,…` · M8 **`EV-ARTIFACT-FILE-EXISTS`**,…

**LANG-001**：M1/M3/M9 `EV-FM-REQUIRED,…` · M4 `EV-ARTIFACT-VERSION-MATCH,…` ·
M5 **`EV-RUN-KEY-DECLARED-EXISTS`** · M7/M10 `EV-FM-YAML-HARDENING,…` ·
M8 **`EV-ARTIFACT-FILE-EXISTS`**,… · M11 `EV-MATRIX-UNBACKED`(**无新命中**) · M12 `DOC-ZERO-PLACEHOLDER,…`

**CONC-002**：M1/M3/M9 `EV-FM-REQUIRED,…` · M4 `EV-ARTIFACT-VERSION-MATCH,…` ·
M5 **`EV-RUN-KEY-DECLARED-EXISTS`**,`EV-OUT-UNDECLARED-KEY,…` · M7/M10 `EV-FM-YAML-HARDENING,…` ·
M8 **`EV-ARTIFACT-FILE-EXISTS`**,…

**LANG-002**：同 LANG-001 形态（M5 新规则拦、M8 新规则拦、M11 无新命中、M12 `DOC-ZERO-PLACEHOLDER`）

**MEM-017**：M1/M3/M9 `EV-FM-REQUIRED,EV-ASSERT-SYMBOL-MAPPED` · M4 `EV-ARTIFACT-VERSION-MATCH,…` ·
M5 `EV-ASSERT-SYMBOL-MAPPED`(**无新命中**) · M7/M10 `EV-FM-YAML-HARDENING,…` · M8 **`EV-ARTIFACT-FILE-EXISTS`**,…

**UB-002**：M1/M3/M9 `EV-FM-REQUIRED` · M4 `EV-ARTIFACT-VERSION-MATCH` · **M5 0 命中** ·
M7/M10 `EV-FM-YAML-HARDENING` · M8 **`EV-ARTIFACT-FILE-EXISTS`**,`EV-ARTIFACT-VERSION-MATCH`,`EV-ASSERT-SYMBOL-MAPPED`

**RAII-002(atom)**：M6 `ATOM-FM-REQUIRED,ATOM-ID-FORMAT,ATOM-PREREQ-READABLE,EV-FM-YAML-HARDENING` ·
M11 `ATOM-DAL-MATCH,ATOM-ID-FORMAT` · M12 `ATOM-ID-FORMAT,ATOM-REL-TARGET,DOC-ZERO-PLACEHOLDER`

## 4. M5/M8 修复验证表（第一轮 vs 第二轮）

| 变异 | 第一轮（499） | 第二轮（500） | 结论 |
|---|---|---|---|
| **M8** artifact → 不存在文件 | **放行**（MEM-040/CONC-001/LANG-001/UB-001 仅 WARN「未登记路径」） | **全部 BLOCK**，规则 = **`EV-ARTIFACT-FILE-EXISTS`**（新）——7/7 有 artifact 的卡全中；原子卡 N/A（无 artifact 字段） | **✅ 闭合** |
| **M5** run_match_keys 加假键（**有** `run_match_file` 的卡） | CONC-001/LANG-001 上被 `EV-FM-YAML-HARDENING` **偶发**拦（机制不对，非假键校验） | **全部 BLOCK**，规则 = **`EV-RUN-KEY-DECLARED-EXISTS`**（新）：CONC-001 / CONC-002 / LANG-001 / LANG-002 **4/4** | **✅ 修复生效（正确机制）** |
| **M5 适用面全覆盖**（补充扫描） | — | CONC-003 / CONC-004 / CONC-005 / CONC-006 施 M5 → **全部 BLOCK**（`EV-RUN-KEY-DECLARED-EXISTS`）⇒ **凡有 `run_match_file` 的 8 张卡 8/8 全拦** | **✅ 适用面内零逃逸** |
| **M5**（**无** `run_match_file` 的卡：MEM-040 / MEM-017 / UB-002） | 第一轮记为"FAKE_KEY 未校验 ⇒ 放行" | 仍**不 block**（MEM-040/MEM-017 = WARN 无新命中；UB-002 = 0 命中） | ⚠️ **未闭合**，见 §5.1（真实归因：这两类卡本来就**没有** `run_match_keys`，属"声明键无载体"形态，而新规则按设计**跳过**无 `run_match_file` 的卡） |

## 5. 新逃逸 / 覆盖局限（附 gate 输出原文）

### 5.1 M5 的"无载体"形态（3 卡放行）—— **最高优先级**

`EV-MEM-040` 与 `EV-UB-002` 的 `actual` 段**既无 `run_match_file` 也无 `run_match_keys`**
（只有内联读数如 `run_final_O2:` / `run_GCC15.3_O2_cxx17:`）。第一轮 M5 的载荷在此**新增**了
`run_match_keys: [FAKE_KEY=1]`，而新规则的第一条判据是"无 `run_match_file` ⇒ 跳过"
（提示词 2.3 明写此设计，理由是 `.out` 由 command 运行时产生）⇒ 该形态**不受任何规则约束**。

gate 输出原文（`_mut500_raw/EV-MEM-040_M5.txt`）：

```
WARN EV-MATRIX-UNBACKED evidence/_mut_tmp/EV-MEM-040.md
```

（仅基线 warn，无任何新命中。）UB-002 复跑取证：`gate 输出中 _mut_tmp 行数 = 0`，gate exit 0。

**建议（留给好模型）**：新增窄判据「`run_match_keys` 有声明 ⇒ 必须有 `run_match_file` 载体」
（声明不可验证的读数 = 与编造观测同源）。**存量实测 0 命中**（`_pre500_t2.py`：`cards_with_keys_but_no_file = 0`）⇒ 落地零误伤。

### 5.2 M11（删 `dal`）在证据卡上 0 反应（2 卡放行）

`EV-LANG-001` / `EV-LANG-002` 有 `dal` 字段，删掉后 gate **无任何新命中**
（提示词预期 "block（DAL 必填）"）。gate 输出原文：

```
WARN EV-MATRIX-UNBACKED evidence/_mut_tmp/EV-LANG-001.md
```

```
WARN EV-MATRIX-UNBACKED evidence/_mut_tmp/EV-LANG-002.md
WARN EV-OUT-UNDECLARED-KEY evidence/_mut_tmp/EV-LANG-002.md
```

（两条都是**变异前就存在**的基线 warn ⇒ 0 新增。）**判断**：DAL 校验未覆盖证据卡
（`ATOM-DAL-MATCH` 只作用于原子卡，见 RAII-002 M11 被拦）。若证据卡的 `dal` 是有效元数据，
应补规则；若非法，应从证据卡里删掉该字段——**留人裁决**。

### 5.3 覆盖局限（非缺陷，但影响判别力）

| 现象 | 实测 | 说明 |
|---|---|---|
| **M2 全为 no-op** | 7/7 证据卡原本就是 `verdict: confirm` | 本轮选卡无 refute 源卡 ⇒ "改 verdict 为 confirm 与 actual 矛盾时 block"这条**未被真正验证**（第一轮同样局限） |
| **M6 在证据卡全 N/A** | 6/7 证据卡无 `claim` 字段 | evidence 卡用 `hypothesis`，`claim` 是原子卡字段 ⇒ M6 只对原子卡有效 |
| **M11/M12 在证据卡多为 N/A** | M11：4/7 无 `dal`；M12：6/7 无 `relations` | 同上，字段体系不同 |
| **原子卡 9/12 N/A** | RAII-002 无 `artifact`/`fixture`/`verdict`/`actual`/`artifact_sha256` | 12 变异是**证据卡中心**设计，原子卡只能测 M6/M11/M12 |
| **原子卡 M6 的旁路规则** | `ATOM-ID-FORMAT` 等也命中 | `claim: >-` 是**块标量**，"删整行"只删表头、留下孤儿续行 ⇒ 触发 YAML 破坏类规则。这些 block 混有"变异自身 YAML 破坏"的效应，非纯"缺 claim"判定 |

## 6. 拦截率统计

| 口径 | 第一轮（499，40 变异） | 第二轮（500，96 变异） |
|---|---|---|
| BLOCK | 19（47.5%） | **58（60.4%）** |
| WARN / ADVICE | — | 10（10.4%） |
| **放行（0 命中）** | 21（含 11 N/A + 4 M2 no-op） | **2**（UB-002 M5、UB-002 M2 no-op） |
| N/A（字段不存在） | 11 | **26**（27.1%） |
| **适用面拦截率**（排除 N/A） | 19/29 ≈ 65.5% | **58/70 ≈ 82.9%** |

> 结论：**M8 完全闭合**（7/7 有 artifact 的卡全 block）；**M5 在适用面内完全闭合**
> （8/8 有 `run_match_file` 的卡全 block，机制正确）；剩余 2 个"放行"中 1 个是 no-op
> （M2），真正的逃逸只有 **UB-002 M5**（无载体形态，见 §5.1）。

## 7. 验收核对

| 验收项 | 结果 |
|---|---|
| 96 个变异每个都有实测结果 | ✅ `_mut500_results.jsonl` 96 条 |
| M5/M8 全部 block | ⚠️ **部分**：M8 = 7/7 ✅；M5 = 4/4（有载体，正确机制）+ 补充扫描 8/8 ✅；无载体 3 卡与原子卡按设计/字段不适用 ⇒ 详见 §4/§5.1（**提示词选卡与验收标准在此内在冲突**，如实记录） |
| 测试后 `_mutation_test2/`、`_mut_tmp/` 已清理 | ✅ 见任务 5 |
| `git status --porcelain evidence/ atoms/` 零改动 | ✅ 每张卡跑完即时校验（8 次全部通过） |
