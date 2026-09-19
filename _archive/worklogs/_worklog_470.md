# _worklog_470 · ds v4.1 flash 执行记录（470 今晚 P0 安全地基）

> 零上下文接手标准：每项含①当前代码状态②未完成原因③下一步精确命令。

## 0. 开工基线（2026-09-13，全部实跑）

| 项 | 实测 | 470 文档值 | 判读 |
|---|---|---|---|
| gate 规则数 | **46**（`--list` 47 行含表头） | 47 | 文档 +1，以实跑为准 |
| gate --check | block=0 warn=32 advice=3 | block=0 warn≈32 | 一致 |
| poison | **50/50**，RULE-COVERAGE 20/46+豁免 27 | 50/50 | 一致 |
| replay | confirm=56 refute=0 infra_error=0 | confirm=56 | 一致 |
| pytest | 121 全绿 | 121+ | 一致 |
| atoms/evidence | 27 / 56 | 27 / 56 | 一致 |
| misconceptions | **79**（470 写 80） | 80 | 文档 +1 |
| git | 工作区干净（仅 `_worklog_403.md` untracked） | — | — |

探针目录 `_adv_v70/probes/` **存在**（E01→`build_step.py`+`EV-ADV70-H1.md`；E03→`EV-ADV70-H3.md`；E07→`adv70_h5h18.py`）。

## 1. 探针前置验证（470 §2.5.3，全部实跑）

| 探针 | 攻击 | 当前代码结果 | 结论 |
|---|---|---|---|
| **E01** | helper 脚本内硬编码覆写（命令行零路径零写动词） | replay **confirm**（借品 sha 8dd19bc6 == 卡值）；gate `_post_compile_writes` blocks=[] warns=[] | **仍逃逸 → P0-A 必要** |
| **E03** | `.cfi_startproc`/`.p2align`/`mov` 恒真符号（denylist 外） | replay **confirm**（跨编译器路径 3 条结构断言全满足） | **仍逃逸 → P0-C 必要** |
| **E07** | 缩进走私（缩进 `verdict: confirm` 被提升为顶层键） | 解析结果 `verdict='confirm'` 顶层键命中 | **仍逃逸 → P0-D 必要** |

判读：470 对苦力 F02/F03 的"拦不住"判断**成立**（非文档误判），P0-A/C/D 优先级维持。验证脚本 `_probe_e01.py`（临时，收工删）。

## 2. 待办状态

- [x] 探针前置验证（E01/E03/E07 全部仍逃逸）
- [x] **P0-A 重编译不变量**（commit `f07d92e`，闭合 452 E01）
- [x] **P0-D 解析硬化**（commit `5e72f51`，闭合 E07/E08/H18/E11；不硬切 safe_load，走外层校验）
- [x] **P0-C 判别力证明**（commit `dcae1d3`，闭合 E03）
- [x] **P0-B cat 式证据扫描**（commit `8c73f78`，E05；experimental 只记录不参与门禁）
- [x] **P0-E 环境量读数键**（commit `8aa6130`，闭合 E06）
- [x] **P0-F 零诊断扩面**（commit `315bbfe`，闭合 E10 两变种）
- [x] **P0-G1 并发隔离锁**（commit `da5a4f4`，闭合 E09）
- [~] P0-G2（签收 git author 绑定）/ P0-H（编号映射）→ 见文末「接手说明」
- [ ] 收工门禁 fresh run

### P0-D 摘要（commit 5e72f51）

- **兼容性实测**：83 份（56 卡+27 原子）中 79 份与 safe_load 有差异（command 尾换行、`controlled_vars` str/dict 类型），3 份 safe_load 直接报错 ⇒ 按 470 风险控制（差异 >10 张）**不硬切**，落地「自定义解析器为准 + safe_load 外层校验」。
- 新规则 `EV-FM-YAML-HARDENING` 四信号：indent-smuggle(block) / dup-key(block，UniqueKeyLoader 覆盖 flow+嵌套) / invalid(warn) / parse-diverge(block)。误伤修正：`matrix:  # 注释` 后跟缩进键曾被误判（注释值非标量值）。
- H14/E11：`_relations_norm` 加冲突同义词（contradiction/conflicts/cancels/opposes）→ 真矛盾原子不再静默共存。
- 批量修正 3 张 YAML 不合法卡格式（仅引号/转义，语义不变）→ gate 回到 block=0 warn=32 基线（零净增量）。
- 验证：E07/E08/E11 三探针全拦；poison P43（A6）；pytest +6；改卡后 EV-LANG-001 replay confirm；golden_lock 恢复 pass。

### P0-C 摘要（commit dcae1d3）

- `check_artifact_assert` 的 contains_in 加判别力统计（`_function_ranges`/`_discriminative_span`）：text 在**所有**函数区间（N≥2）出现、或 k/N≥0.8（N≥3）⇒ 恒真断言 ⇒ refute。
- **对 470 阈值的调整**（铁律 13）：470 用 N≥3，但 E03 探针工件仅 2 个函数区间 ⇒ 拦不住；加 `N≥2 且 k==N` 分支。实测存量 contains_in 的 k/N 最高 3/23 ⇒ 零误伤面。
- absent_in 不做频率统计（缺席恰是强断言）。误伤面天然为零：同编译器卡走 sha 路径**不评估断言**。
- 验证：E03 探针 confirm→`refute:artifact_assert_failed`（mov 2/2 区间）；全量 replay 56 confirm；pytest +5。

### P0-B 摘要（commit 8c73f78）

- `check_fixture_no_echo_data`（方案 A 保守正则）：ifstream/fopen/read_to_string 打开**仓库内**相对路径 + ≤8 行窗口内 getline 中转或直接输出（printf/cout）⇒ 命中。
- **EXPERIMENTAL**（铁律 12）：不注册进 RULES、不产生 Finding、不参与门禁；`--exp-scan` 打印 + 落 `build/exp_fixture_echo.log`。
- 实测：E05 探针命中（f_cat.cpp:7）；存量 56 卡 **0 命中**（升 warn 时机留人裁决——零误伤面已实测，随时可升）。
- 坑：变量名 `f` 曾撞 `printf` 的字母 f（改词边界匹配）。

### P0-E 摘要（commit 8aa6130）

- 新规则 `EV-ENV-DEPENDENT-KEY` 分两档：环境量键**声明进 run_match_keys** ⇒ block（比对目标依赖机器/时钟，CI 异核必红；存量 0 命中）；**仅 .out 留痕未声明** ⇒ advice（存量 2 张 EV-CONC-003/004 的 `nproc=32`）。
- 键模式只认精确词（nproc/date/time/user/host/pid…）与强前缀（hardware_concurrency/__DATE__/sysconf/getenv/processor_）；timestamp/elapsed/random 弱词不匹配（bench 卡正常记录不误伤）。
- E06 探针 keys=[nproc,date,user] 全命中；poison P44；pytest +4。

### P0-F 摘要（commit 315bbfe）

- 字段位移（H16a）：扫描面 falsification → +expected/hypothesis/claim_boundary。
- pragma 消音（H16b）：夹具含 `#pragma GCC diagnostic ignored` / `warning(disable` / `-fno-diagnostics-show-option` 而卡声明 -Werror ⇒ warn。
- 实测扩面零新增 warn（唯一措辞卡 EV-LANG-001 已带 -Werror）；E10 两探针均检出；pytest +4。

### P0-G1 摘要（commit da5a4f4）

- `_acquire_replay_lock`/`_release_replay_lock`：O_CREAT|O_EXCL 独占锁文件（build/.replay_lock）；取不到轮询等待；`wait_timeout`(600s) 超时 ⇒ `infra_error:replay_busy`；`stale_after`(1h) 陈旧锁自动接管。
- **参数分离的教训**：wait 与 stale 共用同一数值时，短等待会把**活锁**误判为陈旧并接管（破坏互斥，测试暴露）。
- pytest +5（含双进程真并发获锁间隔 ≥1.3s 的串行化验证）。

## 3. P0-H 探针沉淀映射表（452 编号 → 回归锁位置）

`_adv_v70/` 是 untracked（新克隆不存在）⇒ 探针构造已沉淀进 `tests/`（入库），不依赖该目录：

| 452 探针 | 攻击 | 拦截点（本轮修复） | 回归锁（入库） |
|---|---|---|---|
| E01 | helper 脚本编译后覆写 | replay 重编译不变量（P0-A） | `tests/test_recompile_invariant.py` |
| E03 | 恒真符号（denylist 外） | replay 判别力统计（P0-C） | `tests/test_discriminative.py` |
| E05 | cat 式证据 | gate exp-scan（P0-B） | `tests/test_p0b_echo.py` |
| E07 | 缩进走私 | gate YAML-HARDENING（P0-D） | `tests/test_p0d_hardening.py` |
| E08 | flow-map 重复键 | 同上 dup-key 信号 | `tests/test_p0d_hardening.py` |
| E10 | 零诊断两变种 | gate ZERO-DIAG 扩面（P0-F） | `tests/test_p0f_zerodiag.py` |
| E11 | 冲突同义词 | `_relations_norm` 同义词归一 | `tests/test_p0d_hardening.py` |
| E06 | 环境量进 keys | gate ENV-DEPENDENT-KEY（P0-E） | `tests/test_p0e_env.py` |
| E09 | 并发假失败 | replay 并发锁（P0-G1） | `tests/test_p0g_lock.py` |
| E04 | mtime advice | 414 F06（历史批已落地，advice 级） | `tests/test_gate_engine.py`（test_writes） |
| E02/E12/E13/E14/E15/E16 | — | 未修（见 470 原文 P1/P2 或流程层） | — |

编号对照：452 探针用 `E01…E16`；414 修复项用 `F01…F09`（P0 级）；毒样例用 `P1…P44`（poison_drill 内嵌）。三套编号不同源，勿混用。

## 4. 接手说明（未完成项，零上下文可继续）

### P0-G2：签收 git author 绑定（未做，原因：改动面涉及 signoff 语义，需人裁决范围）
- **当前状态**：`gate_engine.principal_ok()` 只校验"字符串像在册人名"（`HUMAN_PRINCIPALS=("liaoranran",)`）+ 非空；`.github/CODEOWNERS` 不存在；无 git author 白名单。
- **下一步（建议范围）**：① 新增 gate 规则 `S1-GIT-AUTHOR-BINDING`：从 `git log -1 --format=%an` 取当前 HEAD 作者，人级签收名不在历史作者集合 ⇒ warn（存量会有命中，先 warn 观察）；② `.github/CODEOWNERS` + 分支保护（CI 侧）；③ 判定单点仍在 `principal_ok`，勿三处各写。
- **精确命令**：`python tools/gate_engine.py --list | Select-String S1` 看现有签收规则；`git log --format=%an | Sort-Object -Unique` 看历史作者集合。

### 其他未做（470「不做的事」明确留后续）
419（攻击用例回归库）、426（通用 InvariantChecker 框架）、428（freshness 字段）、429（错误模式库）、P1/P2 全项。

## 5. 收工门禁 fresh run（2026-09-13）

| 项 | 结果 | 对基线 |
|---|---|---|
| gate --check | 规则 **48**（+2：YAML-HARDENING、ENV-DEPENDENT-KEY）· block=0 warn=32 advice=5 | block/warn 与开工一致（advice 3→5：ENV 留痕面 2） |
| poison | **52/52**（+P43/P44）· RULE-COVERAGE 22/48 + 豁免 27 | 与开工 50/50 相比 +2 样例 |
| pytest 全套 | 全绿（新增 6 个测试文件：recompile_invariant / discriminative / p0b_echo / p0d_hardening / p0e_env / p0f_zerodiag / p0g_lock） | 基线 121 例 + 新增 32 例 |
| writer_selfcheck --all | 56 卡 **0 fail** | 一致 |
| replay --check | **confirm=56 refute=0 infra_error=0**（fresh 全量，约 5 分钟） | 与开工一致 |

**replay 耗时变化（重要）**：P0-A 落地前约 120s，落地后约 270-400s（每卡多一次独立重编译）。**未超 470 的 15 分钟回滚阈值**，无需降级为 CI-only；但若 CI 上进一步变慢，按 470 预案：①只对 sha 匹配的卡重编译（当前实现已如此——仅 `got_sha == want_sha` 分支触发）；②改 CI-only。

**本轮 8 个提交**：`f07d92e`(A) `5e72f51`(D) `dcae1d3`(C) `8c73f78`(B) `8aa6130`(E) `315bbfe`(F) `da5a4f4`(G1)。全部未 push（交用户）。

### P0-A 摘要（commit f07d92e）

- 实现：`replay._recompile_invariant`（临时目录 + CCACHE_DISABLE=1 + 原命令逐字替换 `-o` 目标）在 sha 匹配后做独立重编译；`_artifact_compile_lines` 按 `-o==artifact` 精确选行（token 级编译器判定，修 `\b` 在 `+` 后不成立只侥幸命中 `-std=c++23` 的 bug）。三分类：tampered→refute / unavailable→infra_error(fail-closed) / infra。
- **确定性实验（≥3 域）**：conc(EV-CONC-001)/lang(EV-LANG-001)/hist(EV-HIST-001)，各 2 轮重编译 sha 稳定且命中卡值 → 无需注入 `-frandom-seed`/`-ffile-prefix-map`。
- 验证：E01 探针 confirm→`refute:artifact_tampered`；全量 replay **56 confirm 零退化，耗时 270s**（未超 15min 回滚阈值）；pytest +4，全套 126 绿；gate block=0 warn=32 不变。
- 坑记录：Windows 下相对路径 exe 按**父进程 cwd** 解析（非 subprocess cwd 参数）——沙箱测试须 `monkeypatch.chdir`；纯 `./x.exe` 会被 `_split_argv` 剥成 `x.exe` 且不搜 cwd，卡内命令应写 `build/` 子目录形式（真实卡已如此）。
