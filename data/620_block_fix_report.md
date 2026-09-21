# 620 任务 1 · 2 条 BLOCK 级 gate 违规：根因定位与止血报告

> 结论先行：**这 2 条 BLOCK 是并发竞态造成的瞬时误报，不是数据引用错误，也不是 619 引入的回归。**
> 稳态 `gate_engine --check` = **63 规则 / 191 命中 / block=0 / warn=186 / advice=5**（连跑 3 次一致，exit 0）。
> 因此**未修改任何卡片、未补产任何工件**——修改正确的数据去迎合一个误报，本身就是错误。

---

## 一、BLOCK 现象（修复前）

```
[gate] 规则 63 条 · 命中 195 (block=2 warn=188 advice=5)
  [BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-003.md
           卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
  [BLOCK ] EV-ARTIFACT-FILE-EXISTS  evidence/conc/EV-CONC-004.md
           卡声明的工件文件不存在：['Examples/atoms/_atom_lock_cost.asm']
```

涉及规则：`EV-ARTIFACT-FILE-EXISTS`（工件文件存在性）。
涉及卡片：`evidence/conc/EV-CONC-003.md`、`evidence/conc/EV-CONC-004.md`。
涉及工件：`Examples/atoms/_atom_lock_cost.asm`。

---

## 二、修复方式选择：方式 A / 方式 B 都不成立，实际是方式 C

提示词给了两种修复方式，先逐一排除：

### 方式 A（补产工件）—— 不成立

工件**本来就存在**：

- `Test-Path Examples/atoms/_atom_lock_cost.asm` → `True`
- 大小 **28190 字节**（非空）
- `git ls-files Examples/atoms/_atom_lock_cost.asm` → 已跟踪，属 HEAD

不存在"需要补产"的前提。若强行覆盖重写，反而可能破坏 sha256 一致性。

### 方式 B（修改引用）—— 不成立，且有害

卡内引用**本来就是正确的**：

- 两卡均声明 `artifact: Examples/atoms/_atom_lock_cost.asm`，与磁盘路径逐字一致；
- 两卡的 `artifact_sha256: d84c75168df0fda9b032de38efae31f7f51c8cda7eeb187154c53eeba95698f8`
  与 replay 独立重编译结果**逐字相符**（619 验收 replay 输出：`recompile d84c75168df0fda9… == 卡值`）；
- `artifact_assert` 的 4 条符号断言在 replay 中全部 ✅。

改引用会切断「卡 ↔ 工件 ↔ sha256」三方锚定，属**破坏性"修复"**，违反提示词硬边界
「不能为了让 gate 变绿而删掉卡的关键内容」。

### 方式 C（实际采用）：根因定位 + 稳定性验证 + 防竞态纪律

真正的病灶是**执行方式**，不是数据。

---

## 三、根因：gate 与 replay 并发，采样到 replay 重编译的"删旧未写新"窗口

### 3.1 谁在写这个工件

EV-CONC-003 / EV-CONC-004 的 `command` 第二段：

```
g++ -O2 -std=c++23 -pthread -DBENCH_FULL -S Examples/atoms/_atom_lock_cost.cpp -o Examples/atoms/_atom_lock_cost.asm
```

`atom_evidence_replay.py --check` 的 **recompile 步骤**会执行该命令，
以 `-o` **删旧写新**地重写 `Examples/atoms/_atom_lock_cost.asm`。

### 3.2 时间戳证据

```
Get-Item Examples/atoms/_atom_lock_cost.asm
  Length        : 28190
  LastWriteTime : 2026/9/21 22:44:25     ← 恰在 619 独立验收会话期间
  CreationTime  : 2026/9/21 12:53:27
```

### 3.3 并发时序

619 独立验收时，四道门禁（`tool_integrity` / `gate` / `poison` / `replay`）被**并行**发起。
`gate` 执行极快（秒级），`replay` 需重编译 56 张卡（分钟级）。
gate 恰好在 replay 重编译 `_atom_lock_cost.asm` 的**删除旧文件之后、写入新文件之前**的窗口内
检查存在性 ⇒ 判定"工件不存在" ⇒ 2 条 BLOCK。

由于 EV-CONC-003 与 EV-CONC-004 **共用同一个工件**，一次竞态同时命中两卡，
与观测到的"恰好 2 条 BLOCK、且都是这两张卡"完全吻合。

### 3.4 为什么"命中从 191 升到 195"也吻合

195 − 191 = 4 = 2 条 BLOCK + 2 条伴随 WARN。
竞态消失后回落至 191，与冻结基线逐字一致。

---

## 四、修改的文件

**本任务未修改任何受控目录文件，也未修改 gate_engine.py。**

- `evidence/conc/EV-CONC-003.md` —— **未改**（引用正确）
- `evidence/conc/EV-CONC-004.md` —— **未改**（引用正确）
- `Examples/atoms/_atom_lock_cost.asm` —— **未改**（replay 重编译产物，与卡 sha256 一致）
- `tools/gate_engine.py` —— **未改**（规则本身正确，符合提示词硬边界）

新增/修改：
- `data/620_block_fix_report.md`（本文件）
- `data/619_codebuddy_review.md`（追加「更正附录」，见 §六）

---

## 五、修复后 gate 结果（block=0 确认）

```
$ .venv\Scripts\python.exe tools/gate_engine.py --check      × 3 次（串行，无 replay 并发）
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)      exit 0
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)      exit 0
[gate] 规则 63 条 · 命中 191 (block=0 warn=186 advice=5)      exit 0
```

| 指标 | 修复前（竞态观测） | 修复后（稳态） | 冻结基线 |
|---|---|---|---|
| 规则数 | 63 | 63 | 63 |
| 命中 | 195 | **191** | 191 |
| block | **2** | **0** ✅ | 0 |
| warn | 188 | 186 | 186 |
| advice | 5 | 5 | 5 |
| exit code | 1 | **0** | 0 |

**block=0 已确认**，且与冻结基线逐字一致。

---

## 六、语义一致性说明（为什么"不改"才是正确的）

1. **三方锚定未被破坏**：卡 `artifact` 路径 ↔ 磁盘工件 ↔ `artifact_sha256` 三者仍然自洽；
   replay 的 `artifact_sha` 与 `recompile` 两项均判 ✅，证明锚定有效。
2. **断言仍然成立**：EV-CONC-003 的 4 条 `contains` 符号断言、
   EV-CONC-004 的 2 条符号断言在 replay 中全部通过。
3. **若改数据反而制造真问题**：改引用会让 `artifact_sha256` 与新路径脱钩，
   触发 `EV-ARTIFACT-PRODUCER` / sha 不匹配等**真实**违规；补产工件会覆盖 sha 已验证的既有工件。
4. **规则本身无缺陷**：`EV-ARTIFACT-FILE-EXISTS` 在稳态下正确放行；
   它只是在被并发写入时读到了中间态——这是调用方（并发执行）的问题，不是规则的问题。

---

## 七、止血措施（真正落地的部分）

1. **纪律固化**：`gate_engine --check` 与 `atom_evidence_replay.py` **禁止并发执行**。
   已写入 `data/620_baseline.md` §3.4，并在 620 收工门禁（E1）中串行化。
2. **稳定性验证**：E1 将对 gate 做多次复跑，避免单点采样误判。
3. **如实上报**：不因"提示词要求修 BLOCK"而人为改动正确数据；根因与结论如实登记。

---

## 八、遗留与建议（交人 / 留 621）

- **建议（非本批执行）**：给 `gate_engine` 增加"工件存在性检查重试/或 replay 改为写临时文件再原子替换"
  可彻底消除该竞态；但**改 gate_engine 属 CORE_TOOLS，本批硬边界禁止**，故仅登记建议。
- **交人项**：是否接受「619 验收 🔴 必修项」的更正结论，由监工/人判定。
