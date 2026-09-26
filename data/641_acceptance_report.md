# 641 · 验收报告：Core 协议内核通用化（领域无关 + 适配器 + 通用性证明）

> 生成 2026-09-26。所有数字**实测**，不抄历史快照。
> 任务书：`_auto/inbox/641.md`。证据文件见 §九。

## 一、任务完成表

| 阶段 | # | 任务 | 交付 | 状态 |
|---|---|---|---|---|
| 0 | 0.0 | 开工快照（139 项现场分类 + W2 权威现值 + Core 雏形） | `data/641_baseline.md` | ✅ |
| 0 | 0.1 | 全量 pytest 干净终验（`--tb=short`，非 PowerShell 重定向） | `data/640c_pytest_clean.txt` | ✅（8 红已归因，见 §二.1） |
| 0 | 0.2 | 偶发项定位/处置（poison_coverage_581） | `data/641_flake_581.md` + 测试侧修复 | ✅（根因已定位并确定性复现） |
| 0 | 0.3 | 反涟漪验证 | `data/641_anti_ripple.md` | ✅（改 1 个派生量 ⇒ 9 项漂移告警、0 项批量红；还原 ⇒ 0 红） |
| 0 | 0.4 | 回填 640/640b 门禁节（含 §七→§八 悬空引用） | 两份报告更新 | ✅ |
| 0 | 0.5 | 统一 commit 640c 现场 | `fc179a0c` + `d6a7856b` | ✅（139 → 126 项） |
| A | A1 | Core 协议骨架（端口 + 原语，零领域 import） | `tools/queyi_core_v10_641.py` | ✅（AST 证明零领域依赖） |
| A | A2 | Artifact 内容寻址 | 同上 + 单测 | ✅（CRLF/路径无关，同内容同 ID） |
| A | A3 | Evidence 原语泛化 | 同上 + 单测 | ✅ |
| A | A4 | Decision 四态 + 与 DecisionEvent v2 互转 | 同上 + 单测 | ✅（最小字段映射，已登记） |
| A | A5 | VerificationRun 协议（构建/封存/投影） | 同上 + 单测 | ✅（封存后只读 + 自哈希 + 篡改检测） |
| A | A6 | 投影层（从封存 run 派生） | 同上 + 领域注册 | ✅（内核 3 个 + C++ 6 个 + toy 1 个） |
| B | B1 | C++ Domain Pack（解析/规范化/语料 manifest） | `tools/queyi_core_cpp_641.py` | ✅ |
| B | B2 | 规则引擎插件化（引擎通用、规则外置） | 同上 + 单测 | ✅（67 条外置加载，清单与 legacy 一致） |
| B | B3 | CppVerifierAdapter → gate_engine（不改逻辑） | 同上 + 单测 | ✅ |
| B | B4 | CppAttacker/Authority 适配器 | 同上 + 单测 | ✅（dry-run 不变异 / append 只 staged 不代签） |
| B | B5 | 端到端对账 | `data/641_cpp_reconcile.md` | ✅ **7 项指标 0 差异** |
| C | C1 | 第二领域 Domain Pack（toy_math） | `tools/queyi_core_toy_641.py` | ✅ |
| C | C2 | ToyVerifier/Evidence 适配器（纯标准库） | 同上 + 单测 | ✅（含逆运算交叉验算） |
| C | C3 | 同一协议验证 toy + 通用性证明 | `data/641_generality_proof.md` | ✅（`kernel_digest` 两域相同） |
| D | D1 | Verifier Closure（传递闭包 + digest） | `tools/verifier_closure_641.py` | ✅（23 文件） |
| D | D2 | 缺失即 FAIL（新 core 口径） | 同上 + 单测 | ✅（缺失攻击 ⇒ FAIL，非 warning） |
| D | D3 | run 绑定 closure/policy/source digest | 同上 + 单测 | ✅ |
| E | E1 | `run_641_gate.py` | 门禁脚本 + `data/641_gate_result.md` | ✅ **PASS（8/8）** |
| E | E2 | 全量 pytest 终验 | `data/641_pytest_final.txt`（1 红）→ 修复后复跑 58/58 绿 | ✅（全量复核见 642 D2） |
| E | E3 | 验收报告 + status + outbox | 本文件 + `_auto/outbox/641.md` | ✅ |

## 二、关键实测数字

### 1. 阶段 0 的干净终验（诚实）

`data/640c_pytest_clean.txt`：**8 failed / 3350 passed / 16 skipped**（34:45）。
8 项**全部**是当时新写入的 641 工具尚未过 ruff/mypy 所致（`test_mypy_fix_625`、
`test_pre_push_checklist_627`、`test_run_623_gate`、`test_run_624_gate`、
`test_run_625_gate`、`test_run_639_gate`、`test_quality_gate_613`、`test_ruff_clean_after_fix`），
**不是 640c 引入**；已在 641 内修完（ruff 0 / mypy 0 / 444 文件）。
这也实证了"门禁真的会抓新代码的 lint/类型问题"，不是摆设。

### 2. 阶段 E2 终验（**已收尾**，2026-09-26 回填）

`data/641_pytest_final.txt`：**1 failed / 3415 passed / 16 skipped**（35:38）。

唯一失败 = `tests/test_queyi_core_v10_641.py::test_cli_check_passes`，**不是代码 bug，是自检断言的名称选择错误**：

- 现象：`core.main(["--check"]) == 1`，内核 selftest 中仅 `[FAIL] 未注册投影 ⇒ KeyError（fail-loud）`；
- 根因：selftest 用 `run.project("w2")` 断言"未注册投影抛 KeyError"，但 `w2` 会被 **C++ 领域适配器
  注册**（`_PROJECTORS` 是**进程级全局**）。pytest 同进程内先跑 `test_queyi_core_cpp_641.py`
  （注册 `w2`）再跑本 selftest ⇒ `project("w2")` 成功 ⇒ `_raises(...)` 返回 False ⇒ 假失败。
  测试文件本身早已用 `_never_registered_projection_641` 规避（见该文件注释），**内核 selftest 漏了同一处理**。
- 修复：`tools/queyi_core_v10_641.py` selftest 改用 `_never_registered_projection_641`
  （**只改断言用的投影名，未改任何生产逻辑**；fail-loud 语义原样保留）。
- 修复后重跑（`--tb=short`）：`tests/test_queyi_core_v10_641.py` + `test_queyi_core_cpp_641.py`
  + `test_queyi_core_toy_641.py` + `test_verifier_closure_641.py` + `test_run_641_gate.py`
  ⇒ **58 passed，0 failed**。
- 修复后的**全量**终验在 642 批 D2 执行，结论记于 `data/642_pytest_final.txt` 与
  `data/642_acceptance_report.md`（避免"先跑一次全量再改代码"造成证据失效）。

### 2b. E1 门禁（`data/641_gate_result.md`）

**8/8 PASS**：4/4 新工具 `--check` 绿 · ruff 全绿 · mypy 0 errors · 受控目录零污染 ·
内核零领域 import（AST） · C++ 端到端对账 0 差异 · `kernel_digest` 两域相同 ·
信任根闭包 23 文件 status=OK 且缺失即 FAIL。

### 3. 内核（A）

| 项 | 实测 |
|---|---|
| 数据原语 | 3 个（Artifact / Evidence / Decision） |
| 判决四态 | pass / pass_with_exception / fail / unknown |
| 端口 | 5 个（Verifier / Attacker / Authority / Evidence / DomainPack） |
| 内核内置投影 | 3 个（summary / manifest / decisions） |
| **内核领域 import（AST）** | **0** |
| 内核自检 | 26 项全绿 |

### 4. C++ 适配器（B）

```
卡片语料 85（atoms 28 / evidence 57，verified 23）· 规则 67（外置加载）
finding 121（内核） == 121（legacy）
W2 121 节点 IN 79 / OUT 42 / UNDEC 0 —— 与权威源一致
权威链完整 True · 受控零污染 True
⇒ 对账 7 项指标 **0 差异**
投影：w2 / gate / inventory / pck / textbook / dashboard（全部从封存 run 派生）
```

### 5. 通用性（C）

```
toy 语料 8 条（含 2 条错算术 + 1 条除零 + 1 条非法语法）
判决：fail 3 · pass 5 · 证据（逆运算）confirm 5 / refute 2 / unknown 1
C++ run 的 kernel_digest == toy run 的 kernel_digest == 9e926c78…
⇒ 同一内核 **零改动** 跨领域
```

### 6. 信任根闭包（D）

```
闭包 23 文件（内核 + 3 适配器 + 5 CORE_TOOLS + pyproject.toml + .tool_checksums + supply_chain/*）
状态 OK；缺失攻击（假装 pyproject.toml 缺失）⇒ FAIL（不是 warning）
run 绑定 verifier_closure_digest / policy_digest / source_revision
```

## 三、范围与硬边界

- 5 个 CORE_TOOLS 判决逻辑**零改动**（适配器只包裹，不重写）
- 受控目录（atoms/evidence/Examples/Book）**零污染**（门禁实测 + `git diff --quiet`）
- **不代签**：`AuthorityPort.append()` 只返回 `staged:<id>`，不写账本
- **不真变异**：`AttackerPort` 默认 dry-run，applied=0；`restore()` 实证零污染
- **未 push**、未 golden accept
- 内核**不 import** 领域模块；适配器**不反向**被内核依赖（AST 双向验证）

## 四、新增资产

| 类型 | 文件 |
|---|---|
| 工具（5） | `tools/queyi_core_v10_641.py`、`queyi_core_cpp_641.py`、`queyi_core_toy_641.py`、`verifier_closure_641.py`、`run_641_gate.py` |
| 测试（5） | `tests/test_queyi_core_v10_641.py`、`test_queyi_core_cpp_641.py`、`test_queyi_core_toy_641.py`、`test_verifier_closure_641.py`、`test_run_641_gate.py`（合计 **58 例**） |
| 报告（5） | `data/641_baseline.md`、`641_cpp_reconcile.md`、`641_generality_proof.md`、`641_verifier_closure.md`、`641_gate_result.md`（另有 `641_flake_581.md`、`641_anti_ripple.md`、`641_pytest_final.txt`） |

## 五、诚实登记（防自欺）

1. **"通用"的强度边界**：toy 证明的是"协议机制可迁移"，**不等于**内核已能胜任任意真实领域；真实第二领域的复杂度可能暴露新缺口（§八.1）。
2. **Decision ↔ DecisionEvent v2 是最小字段映射**（v2 共 26 字段，内核只填 8 个），不是全字段等价。
3. **C++ 规则是 repo 作用域**（`check()` 扫全库），故 run 输入用单个"语料 artifact"表达，而非 67×N 笛卡尔展开；这是**语义贴合**而非偷懒，已在代码注释登记。
4. **Attacker 端口未做真变异**（受控零污染铁律）⇒ B4 的"行为对账"只到"声明 + 零污染实证"，**未**与 poison_drill 实跑结果对账（那需要人工授权）。
5. **Authority 端口未落库** ⇒ 账本写入路径未被端到端验证，只验证到"staged 事件可生成 + 链完整可读"。
6. **照出的旧测试问题（§八.3）**：`test_poison_coverage_581` 的旧断言把**会话级缓存基线**与**新跑结果**比较 ⇒ 顺序依赖偶发红（已确定性复现并修，见 `data/641_flake_581.md`）。
7. **照出的工具侧坑**：`poison_drill` 模块体含 `if "--check" in sys.argv: sys.exit(0)` ⇒ 任何在 `--check` 命令行下 import 它的进程会被**直接终止**。本轮在适配器里规避（临时清空 argv + 捕获 `BaseException`），**未改 poison_drill**（CORE_TOOLS 铁律）⇒ 建议单列批次修（交人项）。
8. **过度设计回退（§八.4）**：内核只保留实际用到的端口/原语；`PolicyRef`/`ArtifactRef` 都是被 run 真实使用的，无占位抽象。若后续证明某端口无人实现，应回退而非保留。
9. **阶段 D 的 fail-closed 只在新 core 口径下启用**，未强行切换任何既有流程（§八.5）。
10. **工作区未完全转净**：126 项（原 139）中仍有历史遗留未提交项（637 批次工具、`_arch_v19..v28` 调研快照、`data/vsa/` 运行时凭证等）⇒ 是否入册/入 gitignore 交人裁决（§七）。

## 六、交人裁决项（§七）

1. **是否 push**（640c + 641 全区间，当前 ahead=40）及 push 后 CI 观察；
2. 信任根是否/何时移出本机（外部 KMS / 第三方公钥锚 / 外部签名）——本轮只做到"闭包 + fail-closed + 可被外部签名"；
3. "approve 的 MIS 是否抬到 high"（640b/c 遗留口径，本轮未动可信度逻辑）；
4. Core 目录/包的最终形态与命名（现为单文件模块 `queyi_core_v10_641.py`；是否改包、何时从 CPP-Bible 剥离，规划在开源前后）；
5. 规则插件化后，规则贡献/审阅流程（为 650 开源生态准备）；
6. 第二领域的选择是否认可（toy 仅作证明；未来真正第二领域方向）；
7. **偶发测试若再犯，是否接受登记为已知 flaky**（本轮已定位并修复根因）；
8. **`poison_drill` 的 `--check in sys.argv` 自杀式导入副作用**是否单列批次修；
9. 126 项遗留未提交项（637 工具 / `_arch_v*` / `data/vsa/`）如何处置。

## 七、证据文件

| 文件 | 内容 |
|---|---|
| `data/641_baseline.md` | 开工快照（139 项分类、W2 现值、Core 雏形、硬边界） |
| `data/640c_pytest_clean.txt` | 阶段 0.1 全量终验（`--tb=short`） |
| `data/641_flake_581.md` | 偶发项根因 + 确定性复现 + 修复 |
| `data/641_anti_ripple.md` | 反涟漪验证 |
| `data/641_cpp_reconcile.md` / `.json` | C++ 端到端对账（0 差异） |
| `data/641_generality_proof.md` / `.json` | 通用性证明（kernel_digest 两域相同） |
| `data/641_verifier_closure.md` / `.json` | 信任根闭包（23 文件 + 缺失即 FAIL） |
| `data/641_gate_result.md` | E1 门禁 8/8 PASS |
| `data/641_pytest_final.txt` | E2 全量终验 |
