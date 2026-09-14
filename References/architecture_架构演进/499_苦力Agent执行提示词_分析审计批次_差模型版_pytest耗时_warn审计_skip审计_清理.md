# 苦力 Agent 执行提示词 · 分析审计批次（499，差模型版）

> 投喂方式：整份投喂。仓库根目录 `C:\CodeLearnling\note\note\C++\CPP-Bible`。
> 本批次 = 分析审计 + 机械变异对抗 + 清理。不改核心工具代码、不做架构决策。
> 你的产出是报告和对抗测试结果，留给好模型做决策。遇到不确定就记录，不要硬做、不要编造。
> 任务 7（机械变异对抗）是本批次核心，必须做满 40 个变异。

## 〇、开工基线（2026-09-14，498 收工后实测）

| 项 | 命令 | 基线 |
|---|---|---|
| gate | `python tools/gate_engine.py --check` | 53 规则，BLOCK=0 WARN=32 ADVICE=5 |
| replay | `python tools/atom_evidence_replay.py --check` | confirm=56 |
| poison | `python tools/poison_drill.py` | 68/68 |
| pytest | `python -m pytest tests/ -q` | 354 点全绿（约 10.7 分钟） |
| git | `git status -sb` | ahead 157 |

收工时复跑 gate 和 replay，确认 BLOCK=0、confirm=56 不变。
禁止 push、禁止 golden_lock sync/--accept。

### 铁律（差模型特别注意）

1. **先 Read 再动手**：每个任务开始前先 Read 相关文件的磁盘真实内容，不要凭任务描述假设。
2. **不编造数据**：报告里的每个数字都必须来自你实跑的命令输出，不能写"大约""估计"。
3. **不改核心代码**：本批次不改 tools/*.py、不改 atoms/、不改 evidence/、不改 gate 规则。
   只允许：写报告到 docs/kernel/、删除未跟踪临时件、更新 README_INDEX.md。
4. **遇到不确定就记录**：在报告里写"此处不确定，原因是 XXX"，不要猜。
5. **不 push、不 golden sync、不删 _adv_*/ 和 _worklog_*.md**。
6. **每个任务一个独立 commit**（报告类任务可以多个报告合一个 commit）。
7. **请求数 >450 时用 tools/task_state.py 记录进度后停手**。

---

## 任务 1 [必做] pytest 耗时分析报告

**目标**：找出 pytest 10.7 分钟的瓶颈，为后续优化提供数据。

**步骤**：

1. 跑 `python -m pytest tests/ -q --durations=30 2>&1 | Tee-Object _pt499_dur.txt`
   （--durations=30 会输出最慢的 30 个测试）
2. 从输出中提取最慢的 30 个测试，记录：测试名、所在文件、耗时（秒）。
3. 分类：
   - 编译类：测试名或文件含 compile、g++、fixture、replay、poison、build、asm、sanitizer 等关键词，且实际会调用编译器
   - 纯逻辑类：只做字符串/数据结构/规则判断，不调用编译器
   - IO 类：读写文件但不编译
   如果不确定一个测试属于哪类，Read 对应的测试文件看它做了什么。
4. 统计：
   - 总耗时（pytest 输出的最后一行）
   - 编译类测试数量和总耗时占比
   - 纯逻辑类数量和总耗时占比
   - Top 10 最慢测试列表（测试名、文件、耗时、类别）
5. 写报告 `docs/kernel/pytest_perf_analysis_499.md`，包含：
   - 总耗时和测试总数
   - 分类统计表
   - Top 10 最慢测试表
   - 你的判断：最大瓶颈是什么（一句话）
   - 建议：如果编译类测试能缓存，预计能省多少时间（基于实测比例估算，写明是估算）

**验收**：报告里每个数字都能在 _pt499_dur.txt 里找到出处；Top 10 按耗时降序。

**commit**：`docs(kernel): pytest 耗时分析报告（499 任务1）`

---

## 任务 2 [必做] 32 条 warn 存量审计报告

**目标**：把 32 条 warn 逐条分类，区分"真债需要修"和"误报/可接受"。

**当前 warn 分布（开工实测）**：

| 规则 | 数量 | 涉及文件 |
|---|---|---|
| EV-MATRIX-UNBACKED | 15 | evidence/conc/ 6张 + evidence/lang/ 2张 + evidence/mem/ 若干 |
| EV-OUT-UNDECLARED-KEY | 6 | evidence/mem/ 若干 |
| EV-FALSIFICATION-QUANT | 4 | evidence/hist/ + evidence/mem/ |
| ATOM-REL-TARGET | 2 | atoms/ub/ATOM-UB-GRAY-001.md |
| EV-ASSERT-SYMBOL-MAPPED | 2 | evidence/mem/ |
| ATOM-PREREQ-READABLE | 1 | atoms/mem/ATOM-MEM-MOVE-002.md |
| EV-SERVES-EXIST | 1 | evidence/mem/ |

**步骤**：

1. 跑 `python tools/gate_engine.py --check 2>&1 | Select-String 'WARN' > _warn499.txt`，拿到完整 32 条清单（含文件名）。
2. 对每条 warn，Read 对应的文件，判断：
   - **真债**：文件确实缺东西/有问题，应该修
   - **误报**：规则太严或判断逻辑有问题，文件本身没问题
   - **可接受**：已知边界/有意为之，不需要修
3. 对 EV-MATRIX-UNBACKED 的 15 条：Read 每张卡的 frontmatter，看 `matrix:` 字段是否存在、是否为空、是否有实际内容。
   记录每张卡的 matrix 字段状态（存在且有内容 / 存在但为空 / 不存在）。
4. 对 EV-OUT-UNDECLARED-KEY 的 6 条：Read 每张卡的 `actual:` 段和 `run_match_keys`，看哪些 key 没声明。
5. 写报告 `docs/kernel/warn_audit_499.md`，包含：
   - 32 条逐条清单（规则名、文件、分类、原因说明）
   - 分类汇总表（真债 X 条 / 误报 Y 条 / 可接受 Z 条）
   - EV-MATRIX-UNBACKED 15 条的 matrix 字段状态表
   - 你的建议：哪些真债应该优先修（按严重度排序，最多 5 条）

**验收**：32 条每条都有分类和原因；不修改任何卡文件。

**commit**：`docs(kernel): 32 条 warn 存量审计报告（499 任务2）`

---

## 任务 3 [必做] 对抗 skip 审计报告

**目标**：35 个对抗探针被 skip（机器判不了），分析哪些可以加机器判据。

**步骤**：

1. 跑 `python tools/adversarial_regression.py 2>&1 | Tee-Object _adv499.txt`
2. 从输出中提取所有 `[skip]` 行，记录：探针文件、探针名、skip 原因、verdict（如果有）。
3. 对每个 skip 的探针，Read 对应的探针文件（在 `_adv_v80/probes/` 或 `_adv_v70/probes/` 下），理解它在攻击什么。
4. 分类：
   - **可加机器判据**：能通过检查某个字段/跑某个命令/比对某个值来自动判定，给出具体建议（检查什么、怎么判）
   - **需人审**：涉及语义判断/身份真实性/复杂逻辑，机器判不了
   - **探针本身有问题**：探针格式不对/自述缺失/无法复现
5. 写报告 `docs/kernel/adversarial_skip_audit_499.md`，包含：
   - 35 个 skip 逐条清单（探针名、攻击点、skip 原因、分类）
   - 分类汇总表
   - "可加机器判据"的详细建议表（探针名、攻击点、建议的判据、预计实现难度 低/中/高）
   - 你的判断：如果把"可加机器判据"的都实现了，skip 能降到多少

**验收**：35 个 skip 每个都有分类；"可加机器判据"的建议要具体到"检查 X 字段是否等于 Y"这种程度，不能写"加强校验"这种空话。

**commit**：`docs(kernel): 对抗 skip 审计报告（499 任务3）`

---

## 任务 4 [必做] 工作树清理 + 文档索引更新

**目标**：清理 498 遗留临时件，更新 README_INDEX.md。

**步骤**：

1. 列出 498 遗留临时件（开工实测有 20 个）：
   `_inc1.err, _inc1.log, _inc1_t0.txt, _inc1_wrap.err, _inc1_wrap.log, _inc2.log, _inc3.log, _po498.err, _po498.log, _po498b.err, _po498b.log, _pt498.err, _pt498.log, _pt498final.err, _pt498final.log, _pt498final2.err, _pt498final2.log, _rp498.err, _rp498.log, _timeit.py`
   以及任务 1/2/3 产生的 `_pt499_dur.txt, _warn499.txt, _adv499.txt`（报告写完后这些中间文件也删）。
2. 逐个确认是未跟踪文件（`git status --porcelain -- <file>` 显示 ??），然后删除。
3. **不要删**：`_worklog_*.md`、`_adv_*/`、`_probe_ch132_blk*`（非本批产物）、任何在 atoms/evidence/tools/docs/References/ 下的文件。
4. 更新 `References/architecture_架构演进/README_INDEX.md`：
   - Read 现有 README_INDEX.md 的格式
   - 扫描 `References/architecture_架构演进/` 下所有 .md 文件
   - 新增的文档（498、499 相关、docs/kernel/ 下的新报告如果有编号的话）加入索引
   - 如果 README_INDEX.md 有生成脚本（之前 370 批次做过），用脚本重新生成；如果没有脚本，手动按现有格式追加
   - 注意：README_INDEX.md 不索引自身
5. 跑 `git status --porcelain`，确认只剩预期的未跟踪文件（_adv_*/、_worklog_*.md、_probe_ch132_blk* 等）。

**验收**：20+ 个临时件已删除；README_INDEX.md 包含最新文档；git status 干净（除预期保留项）。

**commit**：`chore: 清理498临时件 + 更新文档索引（499 任务4）`

---

## 任务 5 [选做] book_atom_sync.py 功能分析

**目标**：判断这个 224 行孤立脚本该入库还是删除。

**步骤**：

1. Read `tools/book_atom_sync.py` 全部内容。
2. 分析：
   - 它做什么（功能描述）
   - 输入输出（读什么文件、写什么文件）
   - 与现有工具的重叠（和 gate_engine / atom_evidence_replay / cppbible 是否有重复功能）
   - 代码质量（有没有明显 bug、有没有硬编码路径、有没有测试）
3. 全仓搜索它的引用：`Select-String -Path tools/*.py,*.yml,.github/**/*.yml -Pattern 'book_atom_sync'`
   确认是否被任何工具/CI 调用。
4. 写分析到 `docs/kernel/book_atom_sync_audit.md`，给出明确建议：
   - **入库**：需要做什么（注册到 cppbible、加测试、修 bug）
   - **删除**：理由是什么
   - **保留观察**：为什么

**验收**：报告有明确的建议和理由；不修改 book_atom_sync.py 本身。

**commit**：`docs(kernel): book_atom_sync.py 功能分析（499 任务5）`

---

## 任务 6 [选做] Examples 行尾漂移检查报告

**目标**：评估 437 个 Examples/*.cpp 的 CRLF 问题严重程度。

**步骤**：

1. 统计 `Examples/` 下所有 .cpp 文件数量。
2. 用 `git diff --cached --stat` 或 `git status --porcelain Examples/` 看有多少文件有行尾变更。
3. 区分 `Examples/atoms/`（工具唯一写入范围）和其他子目录。
4. 检查 `.gitattributes` 是否存在、内容是什么（472 批次加过）。
5. 写报告 `docs/kernel/examples_lineending_audit_499.md`，包含：
   - 总文件数、有行尾问题的文件数
   - atoms/ 子目录 vs 其他目录的分布
   - .gitattributes 内容
   - 建议：是否需要 `git add --renormalize .`，影响范围多大

**验收**：数字来自实跑；不修改任何文件。

**commit**：`docs(kernel): Examples 行尾漂移检查报告（499 任务6）`

---

## 任务 7 [必做] 机械变异对抗测试

**目标**：对现有卡做批量机械变异，跑 gate 找逃逸。不需要创造力，只需要机械执行和记录。
这是本批次的核心对抗环节——白嫖模型的算力用来压系统，找到的逃逸留给好模型修。

**选卡**（5 张，覆盖不同域和形态）：

1. `evidence/mem/EV-MEM-040.md`（mem 域，断言密度低，3 条）
2. `evidence/conc/EV-CONC-001.md`（conc 域，断言密度高，23 条，含 contains_in）
3. `evidence/lang/EV-LANG-001.md`（lang 域，多 TU）
4. `evidence/ub/EV-UB-001.md`（ub 域，如果不存在则选 evidence/ub/ 下任意一张）
5. `atoms/mem/ATOM-MEM-RAII-001.md`（原子而非证据卡，测原子规则）

如果某个文件不存在，选同域下任意一张替代，并在报告里记录替换。

**8 种机械变异**（对每张卡都做）：

| 编号 | 变异操作 | 预期 gate 反应 |
|---|---|---|
| M1 | 删 `artifact_sha256:` 整行 | 应 block 或 warn（缺锚） |
| M2 | 把 `verdict:` 改为 `confirm`（如果原卡是其他值） | 应与 actual 证据矛盾时 block |
| M3 | 删 `fixture:` 整行 | 应 block（缺夹具） |
| M4 | 把 `artifact_version:` 改为 `99`（台账是 1） | 应 block（版本不匹配，EV-ARTIFACT-VERSION-MATCH） |
| M5 | 在 `actual.run_match_keys` 里加一个不存在的 key（如 `FAKE_KEY=1`） | 应 block 或 warn（未声明键） |
| M6 | 删 `claim:` 整行 | 应 block（缺 claim） |
| M7 | YAML 缩进走私：在 `verdict: refute` 下一行缩进写 `verdict: confirm` | 应 block（重复键/解析走私） |
| M8 | 把 `artifact:` 路径改成一个不存在的文件 | 应 block（工件不存在） |

**执行方法**：

1. 创建临时目录 `_mutation_test/`（在仓库根目录，gitignore 已忽略 _ 前缀文件）。
2. 对每张原始卡，复制 8 份到 `_mutation_test/`，文件名 `<原名>_M1.md` 到 `<原名>_M8.md`。
3. 对每份做对应的变异（用脚本或手动 Edit）。
4. 先 Read `tools/gate_engine.py` 看有没有单卡检查入口（如 `--card` 参数或可 import 的函数）：
   - 如果有单卡入口：用单卡入口逐个测，记录结果。
   - 如果没有：把 `_mutation_test/` 下的变异卡临时复制到 `evidence/_mut_tmp/`，跑 `python tools/gate_engine.py --check 2>&1 | Select-String '_mut_tmp'`，
     抓变异卡的命中结果，然后**立即删除** `evidence/_mut_tmp/`。
5. 记录每张变异卡的结果：BLOCK（规则名）/ WARN（规则名）/ 0 命中（放行=逃逸）。
6. 全部测完后删除 `_mutation_test/` 和 `evidence/_mut_tmp/`（如果用了）。

**写报告** `docs/kernel/mutation_test_499.md`：

- 5 张卡 x 8 种变异 = 40 个测试结果表（卡名、变异编号、gate 反应、是否逃逸）
- 逃逸汇总：哪些变异在哪些卡上 0 block 放行（这就是漏洞）
- 按逃逸严重度排序：M7 缩进走私逃逸 > M4 版本不匹配逃逸 > M1 删 sha 逃逸 > ...
- 你的判断：最危险的 3 个逃逸是什么，为什么

**验收**：
- 40 个变异每个都有实测结果（不能写"未测"）
- 逃逸案例必须有 gate 输出原文佐证（贴在报告里）
- 测试后临时目录已清理，evidence/ 下没有残留变异卡
- 跑 `git status --porcelain evidence/` 确认正式目录零改动

**commit**：`docs(kernel): 机械变异对抗测试报告（499 任务7）`

---

## 任务 8 [选做] 对抗探针复跑 + 基线更新

**目标**：498 后重新跑对抗回归，确认最新拦截状态，更新基线数字。

**步骤**：

1. 跑 `python tools/adversarial_regression.py 2>&1 | Tee-Object _adv499_regression.txt`
2. 记录最终汇总行（blocked=X / escape=Y / visible=Z / gap=W / skip=V）
3. 与 494 基线对比（494 基线：blocked=25 / escape=0 / visible=2 / gap=0 / skip=35）
4. 如果数字有变化，逐个查看变化的探针（哪些从 skip 变 blocked、哪些从 blocked 变 escape）
5. 写简短报告 `docs/kernel/adversarial_baseline_499.md`：
   - 498 后最新数字
   - 与 494 基线对比表
   - 变化的探针清单和原因分析
   - 当前逃逸清单（如果 escape > 0）

**验收**：数字来自实跑；有对比表。

**commit**：`docs(kernel): 对抗基线更新（499 任务8）`

---

## 收工要求

1. 顺序：任务 1 -> 2 -> 3 -> 7（必做），任务 4 在 1/2/3/7 之后做（清理中间文件），有余力做 5 -> 6 -> 8。
2. 任务 7 是对抗核心，必须做；如果时间不够，优先保证任务 7 的 40 个变异全部测完。
3. 任务 4 在任务 1/2/3/7 之后做（要清理它们产生的中间文件，包括 _mutation_test/、_mut_tmp/）。
4. 每个任务完成后确认报告文件已写入 docs/kernel/。
5. 全部完成后复跑 gate 和 replay，确认 BLOCK=0、confirm=56。
6. 在 `_worklog_499.md` 写交接：每项 commit hash、报告路径、关键发现（尤其是变异测试找到的逃逸）、与本文档不符之处。
7. 不 push、不 golden sync。

## 参考文件（需要时 Read）

- `tools/gate_engine.py`（任务 2 理解 warn 规则、任务 7 找单卡检查入口）
- `tools/adversarial_regression.py`（任务 3 理解 skip 判定、任务 8 复跑）
- `References/architecture_架构演进/README_INDEX.md`（任务 4 更新索引）
- `tools/book_atom_sync.py`（任务 5）
- `docs/kernel/`（所有报告输出目录）
- `_adv_v70/`、`_adv_v80/`（历史对抗探针，任务 3/8 参考）
