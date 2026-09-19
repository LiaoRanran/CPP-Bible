# _worklog_559 · 性能与并发卫生批（-o 引号真 bug / 任意跑法不假红 / 临时目录出 %TEMP%）

> 提示词：`References/architecture_架构演进/559_投喂词_性能卫生批_nc_rewrite引号_并发串行隔离_basetemp.md`
> 分支 master（本地，未 push）｜解释器只用 `.venv\Scripts\python.exe`｜本文件按惯例**不入库**。

## 0 · 停点

**A / B / C 三个 Part 都已落地**（B 另有一笔"补"）。commit：

| commit | Part | 内容 |
|---|---|---|
| `d6d2fed` | A | 阴面 `-o` 目标改**参数级**（含空格/反斜杠不再被拆/被吃）+ 2 条回归锁 |
| `7f78b0f` | B | 释放锁路径**绝不抛** + 读敏感用例与 replay 同锁串行 + 6 条回归锁 |
| `6977814` | C | pytest 临时目录移进仓内（**每次运行一个全新子目录**）+ `.gitignore` |
| `75778b2` | B 补 | mutation 冻结结论用例（跑全库门禁）也挂同锁——误跑法第三处假红 |

复跑命令：

```
.venv\Scripts\python.exe tools/gate_engine.py --check
.venv\Scripts\python.exe tools/atom_evidence_replay.py --check
.venv\Scripts\python.exe tools/poison_drill.py
.venv\Scripts\python.exe tools/golden_lock.py buckets
.venv\Scripts\python.exe -m pytest -m "not slow" -n auto -q      # 连跑 3 轮
.venv\Scripts\python.exe -m pytest -m slow -n0 -q
.venv\Scripts\python.exe -m pytest -n auto -q                    # "误跑法"（fast+slow 混跑）
```

---

## 1 · Part 0 开工对账（与提示词逐项相符，无偏差）

gate `规则 61 · 命中 141 (block=0 warn=136 advice=5)` · poison `107/107`（未知分类空、双指标
100%/100%）· replay `confirm=56 refute=0 infra_error=0` · golden buckets
`real 12 / false_positive 0 / legacy 108 / accepted 16 / 未分类 0` · fast `-n auto` 全绿 ·
slow `-n0` 全绿。**全部相符，直接开工。**

---

## 2 · Part A 阴面 `-o` 未加引号（真 bug）

**先实证（探针，未改码）**——`_nc_rewrite` 是 `line.replace(old, new_out)` 字符串替换：

| 输入 | 修前实测结果 |
|---|---|
| `new_out` 含**空格** | 拼出的命令行被 `shlex.split` 拆成两个 token（`…/has` + `space/nc_nc1.s`）⇒ 产物写错地方、rc≠0 |
| `new_out` 含**反斜杠** | shlex 吃掉分隔符 ⇒ `C:UsersASUS…nc_nc1.s` ——**盘符相对路径**⇒ 写到 CWD。**558 仓库根残留 `UsersASUS…replay_…nc_nc1.s` 逐字吻合此机制**（480 字节/无 `C:`/无分隔符） |
| 原目标带**引号** | `_nc_o_target` 的正则 `-o\s+(\S+)` 只取到 `"C:/a`（半截）⇒ 替换后更隐蔽的错位 |

**修法（参数级，不用正则拼串）**：`shlex.split` → 定位 `-o` 的**下一个参数** → 换掉 →
`_nc_join` 重新拼行：`&&` 原样（它是 `_split_commands` 的分段符，加引号会破坏分段），其余
token 用 `shlex.quote` 按需加引号 ⇒ 拼回的行仍可被 shlex **可逆**解析；简单命令行**逐字不变**。

**回归锁**（`tests/test_atom_evidence_replay.py` +2，模块在 SLOW_MODULES）：含空格输出目录
真编译（断言 `-o` 下一个 token 恰为目标 · 产物落位 · tmp 顶层与 CWD 无 `*.s`）+ 无空格逐字对照。

**验收实测**：replay `confirm=56 refute=0 infra_error=0`；NC1
`flip verified（_Z17spin_signal_fencev ∋ 's_sf_b': 阳=2 阴=0）`；poison 107/107（N1–N7 真编译
9 次全绿）；仓库根 `UsersASUS*` 残留 **0**。

⚠️ **事故与修复（自查发现）**：给该文件追加用例时 `replace_in_file` 的锚点落在
`test_parse_frontmatter_real_card_shapes` **函数中部**，把该用例尾部 7 行断言并进了新用例
（`meta` 未定义 → NameError）。已**原样归还**并复跑（原用例 + 2 新用例 3/3 绿）。
教训：给既有文件插代码，锚点必须覆盖到**函数末尾或下一个 def**。

---

## 3 · Part B 任意 `-n` 跑法不假红

### 3.1 先侦察（不盲改）+ 复现探针

- 两阶段是**刻意设计**：`tests/conftest.py` 按模块切 `SLOW_MODULES`/`SERIAL_EXTRA` 打 slow 标；
  `pyproject.toml` 的注释写明权威跑法是 `-m "not slow" -n auto` + `-m slow -n0`；
  `.github/workflows/ci.yml` **本来就是**这两条（`-n 16` + `-n0`）✓ 无需改 CI。
- **复现探针**（`_probe559b.py`，未入库）：起一个真 replay（持续"删旧工件→重生成→还原"），
  同时跑 `golden_lock.py check --json` ×3 ⇒ **3/3 非 pass**（1 次 `status=fail`、2 次崩到无 JSON）
  ✓ 稳定复现。

### 3.2 真因（比提示词假设更深一层）

冻结结论用例与 golden_lock 的假红里，有一类是**释放锁路径崩溃**：`_release_replay_lock()`
裸 `unlink`，而本环境有删除拦截层（safe-delete 把删除改道 trash，并发下报
`OSError: Some operations were aborted`）⇒ 异常穿透 `replay_card` ⇒ `golden_lock check` 崩、
stdout 无 JSON ⇒ `test_golden_lock_json` 假红（实测栈停在
`atom_evidence_replay.py:1672 _release_replay_lock`）。

**修法**：`_try_unlink_lock()`（**绝不抛**，返回是否删成功）；两处"接管"（僵尸锁/陈旧锁）
改为 `and _try_unlink_lock()` 才 `continue` —— 删不掉就落回等待/超时，**不无限空转也不崩**；
`_release_replay_lock()` 调它 ⇒ 释放路径不再反噬正常路径。

### 3.3 并发隔离（任意跑法都安全）

- `tests/conftest.py` 新增 `replay_serial` fixture：复用 replay **同一把** `build/.replay_lock`
  ⇒ 持锁期间任何 replay 都被挡在改写动作之前；拿不到锁 ⇒ **带因 skip**（绝不假失败）。
- **未**重走 508 已证无效的 `--dist loadgroup` + `xdist_group` ✓。
- 挂载范围（侦察后定，非全部）：`test_gate_engine_json` · `test_stock_zero_false_positive` ·
  `test_548_perf_conclusions_unchanged`（B 补）。
  **`test_golden_lock_json` 刻意不挂**：`golden_lock check` 自己就逐卡调 `replay_card`
  （同一把锁），外层持锁会把它逼成 `infra_error:replay_busy`（每卡等 120s）——这是我在实现中途
  发现的**设计缺陷并回收**（先挂了、算清代价后摘掉），改由"释放路径不抛 + 实测"保证。

### 3.4 回归锁

`tests/test_replay_lock_serial.py`（6 例）：锁契约（取到⇒锁在／释放⇒锁无／被占⇒超时=skip 依据）·
**反例**（`unlink` 抛 `OSError` ⇒ `_try_unlink_lock` 返回 False 且 `_release_replay_lock` 不抛）·
**正例**（正常文件删得掉）· 读敏感用例必须挂 `replay_serial`（谁摘掉就红）· 两阶段命令必须写在
pyproject。

---

## 4 · Part C 临时目录出 `%TEMP%`

### 4.1 病（实测坐实）

全量跑结束时 stderr 出现：
`[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED] {"count":1053,"threshold":500,"scope":"turn",
"targets":["\\?\C:\Users\ASUS\AppData\Local\Temp\pytest-of-ASUS\garbage-<uuid>"]}`
⇒ 会话收尾被截断：卡很久、**连 pytest 汇总行都打不出来**。

### 4.2 提示词处方实测**不可用**（重要偏差）

`addopts` 加 `--basetemp=.pytest_tmp`：`--basetemp` 指固定目录时 pytest **每次启动先 rmtree
掉已存在的 basetemp** ⇒ **第二次运行**必撞拦截层（实测
`_safe_shutil_rmtree('\\?\C:\…\.pytest_tmp')` 抛错 ⇒ 凡用 `tmp_path` 的用例**整片 fixture
ERROR**，比原症状更坏）。
读拦截层实现确认根因：旁路条件只有两条——"执行上下文已失效"或"路径在 **OS 临时目录**下"，
**仓内路径不旁路**；且 pytest 传的是 `\\?\` 扩展长度路径，连 `%TEMP%` 那条旁路也比对不上。

### 4.3 落地做法（等价且可用）

`tests/conftest.py::pytest_configure`：未显式指定 `--basetemp` 时，把 basetemp 设为
**每次运行一个全新子目录** `ROOT/.pytest_tmp/run-<pid>-<ts>`：
目录不存在 ⇒ pytest 的 `rm_rf` 直接返回、**不触发任何删除**（不碰拦截层）；不走
`pytest-of-<user>` 编号目录 ⇒ 没有 `garbage-*` 批量回收；`.pytest_tmp/` 已进 `.gitignore`
（注释独占行）。`pyproject.toml` 记下实现位置与实测结论，并保留
`tmp_path_retention_policy = "none"`（pytest 9.1.1 `--help` 实测该 ini 名存在）。
**已知代价**（写清）：`run-*` 目录按运行次数堆积（本环境删除同样被拦截层拦，故留人工/CI 清），
不影响测试判定。

### 4.4 连带必要修复

`tests/test_task_queue.py` 的 `sb` fixture 原假设"锚根在 tmp ⇒ git 审计看不到真仓库"；tmp 移进
仓内后 `git status` 会**成功** ⇒ `test_c6_audit_unavailable_is_visible` 红。修法：fixture 设
`GIT_CEILING_DIRECTORIES=tmp_path.parent`（实测 ceiling=父目录 + cwd=子目录 ⇒ rc=128
"not a git repository"），把该语义**显式钉死**，不再依赖"tmp 恰好在 git 树外"这一环境巧合；
`gitrepo` fixture（在 `tmp_path/anchor` 里 `git init`）不受影响。

---

## 5 · 收工总验收（fresh 实测）

| 项 | 实测 |
|---|---|
| gate | `规则 61 条 · 命中 141 (block=0 warn=136 advice=5)` ✔ 不变 |
| poison | `107/107` ✔（覆盖 36/61 不变；双指标 trap 100%(6/6) · clean 100%(2/2)） |
| replay | `confirm=56 refute=0 infra_error=0` ✔；NC1 `阳=2 阴=0 flip verified` ✔ |
| golden buckets | `real 12 / false_positive 0 / legacy 108 / accepted 16 / 未分类 0` ✔ |
| fast `-n auto` 连 3 轮 | 三轮全绿（每轮含 5 个 syrupy 快照通过）✔ |
| slow `-n0` | **RC=0**，全 dots 无 F/E ✔ |
| 全量 `-n auto`（误跑法） | **RC=0、无 FAILED/ERROR**（2 例带因 skip，属允许形态）✔ |
| 仓库根 stray `.s/.exe` | `UsersASUS*` 残留 **0**；`Path.cwd()/*.s` 0 ✔ |
| safe-delete 卡顿 | 连跑多轮**无** safe-delete 拦截输出；会话收尾不再被截断 ✔ |
| tool_integrity | 已重钉（atom_evidence_replay 属 CORE_TOOLS；Part A 与 Part B/C 各重钉一次）✔ |
| 受控目录零污染 | 仅 pre-existing `EV-CONC-001.md`（M）与惯例未跟踪件 ✔ |
| 不 push / 不 --no-verify / 不代签 accept / 未改四桶 | 均未发生 ✔ |

---

## 6 · 偏差表（提示词假设 X / 磁盘实测 Y）

1. **Part C 处方不可用**：提示词让在 `addopts` 加 `--basetemp=<仓内固定目录>`；实测固定
   basetemp 每次启动被 rmtree ⇒ 第二次运行整片 fixture ERROR。改为"每次运行一个全新子目录"
   （等价目标：临时目录出 `%TEMP%` + 收尾无批量删除），并保留 `tmp_path_retention_policy`。
2. **拦截层的放行规则与提示词假设相反**：提示词说"`%TEMP%` 在 writable root 外"；实测拦截层
   的旁路条件恰是"路径在 **OS 临时目录**下"或"上下文失效"，**仓内路径不旁路**；pytest 的
   `\\?\` 扩展路径又让 `%TEMP%` 那条旁路失效。
3. **Part B 的假红不止"工件瞬时态"一类**：还有一类是**释放锁路径抛异常**导致工具崩（已修）。
4. **Part B 挂载范围比提示词窄**：提示词点名两例；实测 `test_golden_lock_json` **不能**持锁
   （它自己逐卡 replay ⇒ 会 Self-死等 120s/卡），故只挂两例 + 补一例（mutation 冻结结论），
   golden_lock 走"释放不抛 + 实测"。
5. **误跑法第三处假红**：`test_mutation_fuzz::test_548_perf_conclusions_unchanged`（跑全库门禁）
   在误跑法下多出 `EV-ARTIFACT-FILE-EXISTS` ⇒ 已一并挂锁（B 补）。
6. **测试前提被环境变化打破**：`test_c6_audit_unavailable_is_visible` 依赖"tmp 在 git 树外"，
   Part C 之后不再成立 ⇒ 用 `GIT_CEILING_DIRECTORIES` 把条件显式钉死（判定语义不变）。
7. **conftest 跨 Part 同文件**：`tests/conftest.py` 同时含 Part B 的 fixture 与 Part C 的
   `pytest_configure` 段，无法干净拆分 ⇒ C 的 conftest 改动随 B 的 commit 一起进了版本
   （`7f78b0f`），C 的 commit（`6977814`）只含 pyproject/.gitignore/task_queue 测试/校验和。
8. **`_nc_o_target` 正则半截问题**：带引号目标时 `\S+` 只取到 `"C:/a`；新实现改走 shlex 分词，
   该函数已不再参与改写（保留给其它调用方）。

## 7 · 交人项

1. **`.pytest_tmp/run-*` 清理**：会按运行次数堆积（本环境删除被拦截层拦，需人工确认）。
   建议：定期手工清，或在 CI 里用一次性容器天然隔离。
2. **本工作树的临时件**：`_probe559.py` / `_probe559b.py` / `_probe559c.py` / `_probe559d.py` /
   `_commit_msg_559*.txt` / `_t559*.log|.ps1|.err`。删除动作本批多次被环境删除拦截层要求人工
   确认（未获确认），故**留在工作树**；与既有 `_probe557.py` / `_check528.py` 等属同类未跟踪件。
   其中 `_probe559b.py` 是 Part B 的复现探针，建议留档到下次收工再清。
3. **`test_mutation_fuzz.py` 其余跑门禁的用例**（如 T2 的 `test_mutation_summary_structure`）
   在"误跑法"下仍有同类风险；它们都在 fast/slow 两阶段的正确跑法下安全，若要彻底免疫，
   可把 `replay_serial` 也挂到那些"只跑门禁不跑 replay"的用例上（本批只挂到实测红的那条）。
4. **拦截层旁路的 `\\?\` 不匹配**：这是环境实现问题，不是本仓问题；若该层后续修好
   `_path_for_compare` 对扩展长度路径的归一，Part C 可回退到更简单的 `--basetemp` 固定目录方案。
