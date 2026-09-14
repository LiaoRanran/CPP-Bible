# 苦力 Agent 执行提示词 · 缺陷修复 + 对抗验证批次（500 v2，差模型版）

> 投喂方式：整份投喂。仓库根目录 `C:\CodeLearnling\note\note\C++\CPP-Bible`。
> 本批次 = 修 499 发现的 3 个真实缺陷 + 第二轮变异对抗验证。
> 每个修复必须先做存量预检（知道影响面），再改代码，再配毒样例 + pytest，最后用变异测试自证逃逸闭合。
> 改工具前必须 Read 磁盘真实源码，本文档行号可能因前序提交偏移。

## 〇、开工基线（2026-09-14，499 收工后实测）

| 项 | 命令 | 基线 |
|---|---|---|
| gate | `python tools/gate_engine.py --check` | 53 规则，BLOCK=0 WARN=32 ADVICE=5 |
| replay | `python tools/atom_evidence_replay.py --check` | confirm=56 |
| poison | `python tools/poison_drill.py` | 68/68 |
| pytest | `python -m pytest tests/ -q` | 354 点全绿（约 642s，其中 3 个 contains_in 测试烧 174.7s） |
| git | `git status -sb` | ahead 约 160 |

收工时复跑 gate + replay + poison + pytest（仅跑 fast 部分或全量），做前后对比表。
禁止 push、禁止 golden_lock sync/--accept。

### 铁律

1. **先存量预检再改代码**：每个修复任务第一步是跑预检脚本/命令，确认存量影响面，记录数字后再动手。
2. 一条修复一个 commit + 毒样例 + pytest 正反例。
3. **存量零误伤的定义**：新规则/规则升级对存量 56 卡不得新增 block。如果预检发现会 block 存量卡，停下来记录，不要为了零误伤而弱化规则——那是真债，如实报告。
4. 不编造数据，不确定就记录。
5. 不 push、不 golden sync、不删 _adv_*/ 和 _worklog_*.md。
6. 插入大段代码后立即跑 `python tools/gate_engine.py --check` 验证可加载。
7. **回滚方案**：如果某个修复导致 gate 加载失败或大量存量 block，立即 `git checkout -- tools/gate_engine.py` 回退该文件，在报告里记录失败原因，不要硬调。
8. 请求数 >450 时用 tools/task_state.py 记录进度后停手。

---

## 任务 1 [必做] 修复 _assert_haystack 整仓 rglob bug（性能 + 正确性双修复）

### 1.1 存量预检（改代码前必须做）

1. 统计 56 张证据卡中，`fixture` 字段为空或缺失的有多少张：
   ```python
   # 用 Python 一行或脚本：遍历 evidence/**/EV-*.md，读 frontmatter，统计 fixture 为空/缺失的数量
   ```
2. 统计 `artifact` 字段为空或缺失的有多少张。
3. 对这些卡，记录当前 EV-ASSERT-SYMBOL-MAPPED 的命中状态（跑 gate --check，看这些卡是否有该规则的 warn/block）。
4. 把预检数字写进报告：缺 fixture X 张、缺 artifact Y 张、其中 Z 张有 artifact_assert 规则。

### 1.2 根因

`tools/gate_engine.py` 的 `_assert_haystack()` 函数（约 :1422）：
```python
def _add(rel: object) -> None:
    f = ROOT / str(rel or "")   # rel 为空字符串时，f = ROOT / "" = 仓库根目录
    if not f.is_file() and not f.is_dir():
        return
    elif f.is_dir():
        for x in sorted(f.rglob("*")):   # 整仓 rglob，读 28588 个文件全文
```
当卡的 fixture/artifact 为空时，`_add("")` 把仓库根当搜索空间：
- **性能**：3 个 contains_in 测试白烧 174.7s（占 pytest 27%）
- **正确性**：缺 fixture/artifact 的卡 haystack 退化为整仓全文 => EV-ASSERT-SYMBOL-MAPPED 恒不命中（任何符号都能在整仓某处找到），规则失效

### 1.3 修复

在 `_add()` 函数最开头加空值守卫：
```python
def _add(rel: object) -> None:
    if not rel:
        return
    f = ROOT / str(rel)   # 不再用 str(rel or "")，空值已被前置守卫拦截
    ...
```
只改这一处，不动其他逻辑。

### 1.4 验证

1. **性能**：`python -m pytest tests/ -q -k contains_in --durations=5`，3 个测试总耗时应从 174.7s 降到 <10s。记录修复前后的具体秒数。
2. **正确性**：跑 `python tools/gate_engine.py --check`，对比预检数字：
   - 缺 fixture/artifact 且有 artifact_assert 的卡，修复前 EV-ASSERT-SYMBOL-MAPPED 命中数 vs 修复后命中数。
   - 修复后命中数应该**增加**（之前是假阴性，现在能正确检出"断言无出处"）。这是正确行为，记录新增了哪些 warn。
   - 不得新增 block（该规则对"其他符号不可映射"是 warn 级）。
3. **毒样例**（tests/ 下新建或追加）：
   - 阳性：一张缺 fixture 的卡 + 一条 contains_in 断言（符号不在卡内其他地方）=> EV-ASSERT-SYMBOL-MAPPED 应 warn（断言无出处可映射），不是静默通过。
   - 阴性：一张有 fixture 的卡 + contains_in 断言符号在 fixture 中 => 不命中。
   - 边界：fixture 和 artifact 都为空 => haystack 为空字符串，所有 contains_in 断言都 warn。
4. pytest 至少 3 个（空 fixture 不触发整仓搜索 / 有 fixture 正常搜索 / 双空全 warn）。
5. 全量 gate --check 确认 0 新增 block。

### 1.5 报告

在 `_worklog_500.md` 记录：预检数字、修复前后 pytest 耗时对比、修复前后 EV-ASSERT-SYMBOL-MAPPED 命中数对比。

**commit**：`fix(gate): _assert_haystack 空路径守卫，修复整仓 rglob 性能与假阴性（500 任务1）`

---

## 任务 2 [必做] 新增 EV-RUN-KEY-DECLARED-EXISTS 规则（修复 M5 逃逸）

### 2.1 存量预检（改代码前必须做）

1. 列出所有有 `actual.run_match_file` 字段的卡（CONC 域 6 张等），记录卡名和 run_match_file 路径。
2. 对每张卡，读 run_match_file 指向的 .out 文件，逐个检查 `actual.run_match_keys` 里的 key 是否在 .out 中出现。
3. 记录：有没有存量卡的 run_match_keys 里有 .out 中不存在的键？如果有，是哪些卡、哪些键？
   - 如果有，说明新规则会 block 存量卡——这是真债，记录下来，规则照样 block（不要为了零误伤而跳过）。
   - 如果没有，存量零误伤。

### 2.2 根因

当前 `EV-OUT-UNDECLARED-KEY`（gate_engine.py 约 :1027-1063）只做单向检查：
`.out` 里出现的 key 必须在 `actual.run_match_keys` 中声明。
但**不检查反向**：`run_match_keys` 里声明的 key 是否真的在 `.out` 中存在。
=> Writer 可以写假键（如 `FAKE_KEY=1`），gate 0 命中放行（499 实测 MEM-040/UB-001 逃逸）。

### 2.3 新规则设计

**规则名**：EV-RUN-KEY-DECLARED-EXISTS，severity=block，domain=evidence。

**判据**：
- 仅对有 `actual.run_match_file` 字段的卡生效（.out 是静态文件，gate 可读）。
- 对没有 run_match_file 但有 run_match_keys 的卡：跳过（.out 是 command 运行时产生的，gate 静态检查时可能不存在）。
- 逐个检查 `actual.run_match_keys` 里的每个元素：
  - key 解析：元素是字符串，按第一个 `=` 或 `:` 分割，取左侧 strip 作为 key 名。如果没有 `=` 或 `:`，整个字符串 strip 后就是 key。
  - 在 .out 文件全文中 grep 该 key（作为子串出现即可，不需要整词匹配，因为 .out 行格式通常是 `key=value`）。
  - key 不在 .out 中 => block，fix_hint 写明哪个 key 缺失、在哪个 .out 文件中。
- `run_match_keys` 为空列表或缺失 => 跳过。
- .out 文件不存在 => block（留痕文件丢失，比键缺失更严重），fix_hint 写明文件路径。

### 2.4 实现

1. Read gate_engine.py 中 EV-OUT-UNDECLARED-KEY 的实现（约 :1027-1063），照抄它的 .out 读取逻辑（`_read_out_file` 或类似函数）和 key 解析逻辑。
2. 在紧邻其后写新函数 `check_run_key_declared_exists() -> list[Finding]`。
3. 在规则注册表（约 :2290-2340 的 RULES 列表）注册，severity=block。
4. 跑 gate --check，确认预检结果（存量卡 0 block 或记录真债）。
5. 毒样例：
   - 阳性：run_match_keys 含 `FAKE_KEY=1`，.out 中无此键 => block
   - 阴性：run_match_keys 的键都在 .out 中 => 放行
   - 边界 1：无 run_match_file 的卡 => 跳过（不 block 不 warn）
   - 边界 2：.out 文件不存在 => block
   - 边界 3：key 格式是 `key: value`（冒号分隔）=> 正确解析
6. pytest 至少 4 个（阳性 / 阴性 / 无 run_match_file 跳过 / .out 不存在 block）。

**commit**：`feat(gate): EV-RUN-KEY-DECLARED-EXISTS 反向键校验（修复 M5 逃逸，500 任务2）`

---

## 任务 3 [必做] artifact 不存在从 warn 升 block（修复 M8 逃逸）

### 3.1 存量预检 + 现状确认

1. 搜索 gate_engine.py 确认当前是否有检查 artifact 文件存在性的规则：
   `Select-String -Path tools/gate_engine.py -Pattern 'artifact.*is_file|artifact.*exists|artifact.*missing|ARTIFACT.*FILE|ARTIFACT.*EXIST'`
   - 记录搜索结果：有没有规则、规则名、severity 级别。
2. 统计 56 张证据卡中，有 `artifact:` 字段的有多少张、`artifacts:` 数组的有多少张。
3. 对每张有 artifact 的卡，检查文件是否存在（相对于 ROOT）。记录有没有不存在的（预期存量都存在）。
4. 检查 `Examples/atoms/artifact_versions.json` 台账中的路径是否都存在。

### 3.2 根因

卡的 `artifact:` 指向不存在文件时，gate 只 WARN 不 BLOCK（或根本没有专门规则）。
=> Writer 可以编造 artifact 路径，卡照样直推 verified。

### 3.3 修复（分两种情况）

**情况 A：已有规则但是 warn 级**
- 找到该规则，把 severity 从 warn 改成 block。
- 更新规则描述、fix_hint、注册表。
- 毒样例和 pytest 照加。

**情况 B：没有专门规则**
- 新增 `EV-ARTIFACT-FILE-EXISTS`（block）：
  - 检查卡的 `artifact:` 字段（单字符串）指向的文件必须存在（相对于 ROOT）。
  - 检查 `artifacts:` 数组（如果有）中每个元素的 path/file 字段指向的文件必须存在。
  - 不存在 => block，fix_hint 写明哪个路径不存在。
  - 空 artifact 字段且无 artifacts 数组 => 跳过（纯 run_match 形态的卡没有 artifact）。
  - 不检查 artifact_versions.json 台账（台账是旁路元数据，工件存在性由卡字段检查覆盖）。

### 3.4 验证

1. 跑 gate --check，存量 56 卡 0 新增 block（存量 artifact 都应该存在）。
2. 毒样例：
   - 阳性：artifact 指向 `Examples/atoms/_nonexistent.asm` => block
   - 阴性：artifact 指向存在文件 => 放行
   - 边界：无 artifact 字段 => 跳过
   - 边界：artifacts 数组中有一个不存在 => block
3. pytest 至少 3 个。

**commit**：`feat(gate): artifact 文件不存在升 block（修复 M8 逃逸，500 任务3）`

---

## 任务 4 [必做] 第二轮变异对抗测试（验证修复 + 扩展）

### 4.1 目标

验证任务 1/2/3 的修复是否闭合了 M5/M8 逃逸，同时用更多变异找新漏洞。

### 4.2 选卡（8 张，控制规模）

- 第一轮测过的 3 张（用于修复前后对比）：EV-MEM-040、EV-CONC-001、EV-LANG-001
- 新增 5 张：从 evidence/mem/、evidence/conc/、evidence/lang/、evidence/ub/、atoms/ 各选一张第一轮没测过的
  （用 `Get-ChildItem` 列目录自选，记录选了哪些和为什么选）

### 4.3 12 种变异（精简版，每种有明确预期）

| 编号 | 变异操作 | 预期 gate 反应 | 备注 |
|---|---|---|---|
| M1 | 删 artifact_sha256 整行 | block 或 warn | 缺锚 |
| M2 | 改 verdict 为 confirm（原卡非 confirm） | 视 actual 证据，可能 block | 矛盾检测 |
| M3 | 删 fixture 整行 | block | 缺夹具 |
| M4 | artifact_version 改 99 | block | 版本不匹配（EV-ARTIFACT-VERSION-MATCH） |
| M5 | run_match_keys 加 FAKE_KEY=1 | **必须 block（任务 2 修复后）** | 核心验证项 |
| M6 | 删 claim 整行 | block | 缺 claim |
| M7 | YAML 缩进走私：verdict: refute 下缩进 verdict: confirm | block | 重复键/解析走私 |
| M8 | artifact 指向不存在文件 | **必须 block（任务 3 修复后）** | 核心验证项 |
| M9 | 删 actual 整段 | block 或 warn | 缺证据 |
| M10 | artifact_sha256 改全 0（64 个 0） | block | sha 不匹配 |
| M11 | 删 dal 字段 | block | DAL 必填 |
| M12 | relations 加不存在目标 ATOM-XXX-999 | block 或 warn | 关系目标不存在 |

去掉了原 M11（未知字段，预期不明确）和 M12（status 回退，状态机规则复杂），换成更明确的 M11（删 dal）和 M12（relations 悬空）。

### 4.4 执行方法

1. 创建 `_mutation_test2/` 临时目录（仓库根目录，_ 前缀已 gitignore）。
2. 8 张卡 x 12 变异 = 96 份变异卡，文件名 `<原名>_M1.md` 到 `<原名>_M12.md`。
3. Read gate_engine.py 确认有没有单卡检查入口（`--card` 参数或可 import 的函数）：
   - 有：用单卡入口逐个测。
   - 没有：把变异卡临时复制到 `evidence/_mut_tmp/`，跑 `python tools/gate_engine.py --check 2>&1 | Select-String '_mut_tmp'`，抓结果，然后立即删除 `evidence/_mut_tmp/`。
4. 逐个记录：BLOCK（规则名）/ WARN（规则名）/ 0 命中（逃逸）。
5. **核心验证**：M5 和 M8 在所有 8 张卡上都必须 block。如果有任何一张放行，说明任务 2/3 修复没生效，回查修复代码。

### 4.5 报告 `docs/kernel/mutation_test_round2_500.md`

- 96 个测试结果表（卡名、变异编号、gate 反应、是否逃逸）
- **M5/M8 修复验证表**：对比 499 第一轮（M5 在 MEM-040/UB-001 放行、M8 放行）vs 500 第二轮（应全部 block）
- 新逃逸汇总：哪些变异在哪些卡上 0 block 放行，贴 gate 输出原文
- 按严重度排序的 Top 5 新逃逸
- 拦截率：96 个变异中 block 多少 / warn 多少 / 放行多少（对比第一轮 19 拦/21 放行）

### 4.6 验收

- 96 个变异每个都有实测结果
- M5/M8 全部 block（否则修复失败）
- 测试后 `_mutation_test2/` 和 `evidence/_mut_tmp/` 已清理
- `git status --porcelain evidence/ atoms/` 确认正式目录零改动

**commit**：`docs(kernel): 第二轮变异对抗测试报告（500 任务4）`

---

## 任务 5 [必做] 修复前后全量对比 + 清理 + 索引

### 5.1 全量对比表

在 `_worklog_500.md` 中填写以下对比表（数字必须实跑）：

| 指标 | 开工基线 | 收工 | 变化 |
|---|---|---|---|
| gate 规则数 | 53 | ? | +? |
| gate BLOCK | 0 | ? | ? |
| gate WARN | 32 | ? | ? |
| poison 毒样例数 | 68 | ? | +? |
| pytest 点数 | 354 | ? | +? |
| pytest 总耗时 | ~642s | ? | ? |
| contains_in 3 测试耗时 | 174.7s | ? | ? |
| replay confirm | 56 | ? | ? |
| 变异测试拦截率 | 19/40（第一轮） | ?/96（第二轮） | ? |
| M5 逃逸 | 放行（2 卡） | 必须 block | 闭合 |
| M8 逃逸 | 放行 | 必须 block | 闭合 |

### 5.2 清理

1. 删除本批临时件：`_mutation_test2/`、`_mut_tmp/`、`_pt500*`、`_po500*`、`_rp500*`、`_mt500*`、预检脚本等。
2. 逐个确认未跟踪后删除。不删 _adv_*/、_worklog_*.md、_probe_ch132_blk*。
3. 更新 `References/architecture_架构演进/README_INDEX.md`（新增 499、500 文档）。
4. `git status --porcelain` 确认干净。

**commit**：`chore: 清理500临时件 + 更新索引 + 全量对比（500 任务5）`

---

## 任务 6 [选做] pytest 快慢标记分离

1. Read tests/ 下所有测试文件，分类：
   - slow：调用编译器（g++/cl）、跑 replay、跑 poison、编译 fixture 的测试
   - fast：纯字符串/数据结构/规则判断，不调用编译器
2. 给 slow 加 `@pytest.mark.slow`，fast 加 `@pytest.mark.fast`。
3. `tests/conftest.py`（不存在则新建）加配置，默认跑全部，`-m fast` 只跑快测。
4. 验证：`python -m pytest tests/ -q -m fast` <30s；`-m slow` 包含编译类测试。
5. 不删除任何测试，只加标记。

**commit**：`test: pytest 快慢标记分离（500 任务6）`

---

## 任务 7 [选做] warn 真债修复 Top 3

基于 499 任务 2 的 warn 审计报告（`docs/kernel/warn_audit_499.md`），
选标记为"真债"且严重度最高的 3 条修复：
- 修卡：补 matrix 字段、补 run_match_keys、修 relations 目标等
- 修规则：如果是误报，调整规则逻辑
- 每条修复后跑 gate 确认该 warn 消除且无新增 block
- 不改卡的 claim/verdict 等核心字段，只补缺失元数据

**commit**：`fix: warn 真债修复 Top3（500 任务7）`

---

## 收工要求

1. 顺序：任务 1（预检+修复）-> 2（预检+修复）-> 3（预检+修复）-> 4（变异验证）-> 5（对比+清理）。有余力做 6 -> 7。
2. 任务 4 必须在 1/2/3 之后做（验证修复效果）。
3. 每个修复任务必须先做存量预检，记录数字后再改代码。
4. 每个任务完成后立即跑 gate --check 确认可加载、0 新增 block。
5. 全部完成后填写 5.1 全量对比表。
6. 在 `_worklog_500.md` 写交接：每项 commit hash、预检数字、修复内容、变异测试关键发现、pytest 耗时对比、回滚记录（如果有）。
7. 不 push、不 golden sync。

## 参考文件（需要时 Read）

- `tools/gate_engine.py` :1422-1447（任务 1 修复点）、:1027-1063（任务 2 参考实现）、:2290-2340（规则注册表）
- `tests/test_gate_engine.py`（毒样例和 pytest 模式）
- `docs/kernel/warn_audit_499.md`（任务 7 输入）
- `docs/kernel/mutation_test_499.md`（任务 4 第一轮对比基线）
- `Examples/atoms/artifact_versions.json`（任务 3 台账参考）
- `References/architecture_架构演进/README_INDEX.md`（任务 5 更新索引）
