# _worklog_479 · 零成本高 ROI 三项 + ccache 接入（2026-09-14）

> 输入：478 落地方案（TDD 反转 / 级联路由 / 文档即代码）+ 476 第一波 1.1（ccache）+ 472 两个待裁决项。
> 纪律：不 push、不 golden sync、逐任务独立 commit、存量零误伤、数字全部实跑。
> 零上下文接手标准：每项含 ①当前状态 ②未完成原因 ③下一步精确命令。

## 0. 开工基线 → 收工终值（全部实跑）

| 项 | 开工 | 收工 | 判读 |
|---|---|---|---|
| git 工作树 | 无 modified（仅 untracked 文档/临时件） | 逐任务提交，7 提交 | — |
| gate 规则数 | 50 | **51**（+`S1-GIT-AUTHOR-BINDING`） | 任务 4 |
| gate --check | BLOCK=0 WARN=32 ADVICE=5 | **BLOCK=0 WARN=32 ADVICE=5** | 零净增量（新规则 0 命中） |
| poison | 61/61 · 24/50+27 · 11/11 | **63/63 · 25/51+27 · 11/11** | +P58 配对 |
| pytest | 272 点全绿 | **302 点全绿**（+30） | 见 §5 |
| replay | confirm=56，**298.5s** | **confirm=56**（三次一致） | 冷 304.8s / 热 244.5s |
| doc_lint | —（新工具） | **存量失真 19 处**（规则名 7/数字 8/工具名 4） | 只记录不修 |

## 1. 任务完成状态

| # | 任务 | 状态 | commit |
|---|---|---|---|
| 1 | P0 TDD 顺序反转写入 Writer 生产流程 | ✅ 完成 | `052bbb7` |
| 2 | P0 doc_lint.py 文档质量门禁 | ✅ 完成 | `50dfe29` |
| 3 | P0 ccache 接入 replay | ✅ 完成（加速比有结论，见 §3） | 见 §5 提交表 |
| 4 | P1 E12 签收绑定（warn 观察） | ✅ 完成（存量命中 **0**，见 §4） | 见 §5 提交表 |
| 5 | P1 分类学错位对齐 | ⚠ **部分完成**（中立文档已落地，方向裁决留人，见 §6） | 见 §5 提交表 |

## 2. 任务 1：TDD 顺序反转（`052bbb7`）

- **现状**：仓库无独立 Writer 生产流程规范件（References 下的是**批次级**生产提示词：298/312；
  `docs/kernel/` 只有 G1_layout 卡模板、M2 实证规范）。按 479 提示词的 fallback 落地。
- **交付**：`docs/kernel/writer_production_flow.md`（103 行）——旧流程（禁止）/ 新流程（P-TDD）/
  **铁律 P-TDD 逐字** / 6 步操作清单 / 5 条反模式 / 与既有制衡的接口表（S3-EXPECTED-HARDCODED、
  EV-SELF-SATISFIED-ASSERT、EV-TRIVIAL-OBSERVATION、EV-FALSIFICATION-QUANT、红队两段式盲读）。
- **根因证据（478 §1.1）**：ALLOC-002 口径反转 / LEAK-002 LSan 零报告被推翻 / EV-MEM-017
  `_Znwm` vs `_Znwy` —— 三起真实事故同机制：断言被夹具输出锚定成自证。
- **零代码改动** ✅（`git show --stat` 可验）。

## 3. 任务 3：ccache 接入（含**实测加速比，与预期不符**）

### 3.1 实现（`tools/atom_evidence_replay.py`）
- `_resolve_ccache()`：`CPPBIBLE_CCACHE` → PATH（`shutil.which`）→ 已知安装位兜底，结果缓存；
- `_wrap_ccache()`：**只对编译器调用**加前缀（跑 exe / 生成脚本不加）；不可用或 `--no-ccache` ⇒ 原样回退；
- `run_commands`：`prog` 仍记**真实编译器**（失败分流"环境 vs 内容"依赖它，ccache 不得覆盖）；
- `_compiler_env`：`CCACHE_DIR=build/.ccache`（`setdefault`，`build/` 已在 `.gitignore`）；
- `--no-ccache` 开关；`_recompile_invariant` **保持 `CCACHE_DISABLE=1`**（P0-A 正确性：缓存命中会让
  "重编译不变量"退化为恒真比对）。
- 环境实测：Windows `C:\tools\ccache\ccache.EXE` ✅ · WSL `/usr/bin/ccache` ✅（WSL 侧未改代码，
  由 PATH 天然命中；本仓 replay 的 WSL 路径同理生效）。

### 3.2 实测（全量 56 卡，三次独立运行）

| 场景 | 耗时 | 对基线 | ccache 统计 |
|---|---|---|---|
| 基线（未接 ccache） | **298.5s** | — | — |
| 冷缓存（首跑，填充） | **304.8s** | +2% | 可缓存 58，命中 13（22%）· 填充 172 文件 |
| 热缓存 | **244.5s** | **−18%（1.22×）** | 可缓存 75，**命中 75（100%）** · 不可缓存 61 |

三次 `confirm=56 refute=0 infra_error=0` 完全一致 ✅（ccache 不改变判定）。

### 3.3 为什么没到"<2min"（诚实结论）
1. **P0-A 重编译刻意禁用缓存**（56 次独立编译/全量）——这是正确性要求，不可加速；
2. **44.85% 调用不可缓存**（61/136：链接、被禁用的重编译等）——ccache 对链接阶段直接透传；
3. replay 耗时的大头不在"重复编译"：还包括工件重生成 + sha 比对、运行夹具、sanitizer 尝试
   （本机 MinGW 无 ASan/UBSan ⇒ link 失败路径）、并发锁与快照还原。
→ **要达成 476 的"<30s 日常 replay"目标须靠 1.2（增量 replay：只重跑 git diff 变更卡）**，
ccache 是必要不充分条件（它把可缓存编译的成本压到 0，实测 −18%）。

## 4. 任务 4：E12 签收 × git 作者绑定（`S1-GIT-AUTHOR-BINDING`，warn）

- **问题（v5 E12）**：`human:liaoranran` 自签修复前零 block 零 warn —— 签收只验"名字在册"，
  不验"签字者与产出者同一人"。
- **实现**：人级签收（`status_history[*].by: human:*` 或 `verified_by: human:*`）须与**该文件
  最后一次 git 提交的作者**匹配（宽松：名/邮箱前缀、大小写与分隔符归一、包含即通过）；
  不匹配 ⇒ `warn`。**git 不可用（CI 浅克隆/无仓库）⇒ 跳过不报警**（门禁不因环境差异改结论）。
  单文件一次 `git log -1 -- <path>` + 结果缓存（27 原子约 1.5s）。
- **存量实测命中：`0` 处**（预期"51 处左右"未出现）。原因：本仓所有提交的 git 作者是
  `LiaoRanran <1026708211@qq.com>`，与签收名 `liaoranran` 宽松匹配通过。
  **这说明存量签收在"作者一致性"维度是干净的**；E12 的真正漏洞是「任何人抄写在册名即可冒充」
  —— git 作者绑定只能覆盖"换账号/伪造 author"场景，**不能**替代"签收须本人 + 留痕"的流程约束。
- **毒样例**：`P58`（注入不匹配作者 ⇒ 须命中且级别 warn）+ `P58-阴`（同人、含大小写差异 ⇒ 放行）。
- **pytest**：`tests/test_s1_git_author_binding.py`（10 例：正例/4 种宽松匹配/无 git/无 human 签收/
  聚合/缓存/注册级别）。
- **升 block 的前置（未做，留人）**：观察期零误伤（已满足）+「签收必须本人」写进 G6 规范。

## 5. 提交清单（479，**均未 push**）

| commit | 内容 |
|---|---|
| `052bbb7` | docs(kernel): Writer 生产流程规范 + 铁律 P-TDD（任务 1） |
| `50dfe29` | feat(tools): doc_lint 文档质量门禁（任务 2） |
| `d7b0023` | feat(replay): ccache 前缀 + `--no-ccache`（任务 3） |
| `c31f1c1` | feat(gate): S1-GIT-AUTHOR-BINDING warn（任务 4） |
| `194c3f6` | docs(kernel): 攻击面分类学两套口径并列（任务 5 中立交付） |

**合计 5 提交，全部未 push**（本地 ahead **143**）。

## 6. 任务 5：分类学错位——**方向未决（按停止条件停在记录）**

- **冲突事实**：代码口径 A1–A11（`ATTACK_TYPES`/`ATTACK_TYPE_LABELS`）与 409 原表 A1–A10
  **仅 A8 一致**（A9 近义），A11 为 409 授权的新增扩面。472 已在代码注释/台账/worklog 记录。
- **479 提示词内部矛盾**：写着"推荐方案 A（改代码对齐 409）"，但理由却是"代码是实际执行的，
  文档应该对齐代码"（= 方案 B 的理由）。按**停止条件**（"对齐方向不确定，停下来记录，不擅自决定"）
  本轮不改任何一边的分类名。
- **已落地的中立交付**：`docs/kernel/attack_surface_taxonomy.md` —— 两套口径并列 + 同名异义
  对照表 + **引用规范**（写"A7"须注明口径；覆盖率只引台账）+ 两方案代价与裁决所需信息。
- **下一步（需用户裁决）**：若 409/410 系仍作活引用 → 方案 A（改代码，约 1 小时，需同步
  7 处 pytest + 台账）；若已是历史快照 → 方案 B（改文档并标注被取代）。

## 7. 任务 2 补充：doc_lint 存量失真 19 处（只记录，未修文档）

```
规则名 7 处：EV-OBSERVATION-VISIBLE / EV-ASSERT-DISCRIMINATOR / EV-ARTIFACT-GEN-TRACE /
             EV-NO-ENV-KEYS / EV-LANG（截断）… —— 多出现在 371/373/tool_assumptions 的
             "规划中/历史"语境（真失真候选：文档声称存在但代码没有）
数字 8 处：M4_gate_engine.md:3 说 21 条规则（实际 51）← 478 §3.1 点名的案例；
           369/371/373/G1_terminology/M2/M5 的历史快照（未标"当时"）
工具名 4 处：m5_dashboard.py / quality_dashboard.py（M5 规划未实现）
```
**误报抑制（本轮修）**：首跑 79 处里 60 处是 `EV-MEM-001` 被截断成 `EV-MEM` 所致（规则 token
正则缺右侧负向断言）；修后 19 处为真。另提供 `doc-lint:ignore` 行内豁免（引用历史文档用）。
**CI 接入建议**：先 `--observe`（恒 exit 0）观察，待 19 处清理到可接受面再走默认严格。

## 8. 未完成项与原因

1. **分类学方向裁决**（任务 5，见 §6）——需人决定 A/B；中立文档已消除误用风险。
2. **ccache WSL 侧未单独验证**——本机 replay 主路径为 Windows/MinGW（WSL 仅在 CI）；WSL 侧由
   PATH 命中，未单独跑全量（如需：`wsl -e bash -lc "cd '/mnt/c/…' && python3 tools/atom_evidence_replay.py --check"`，时间约 5-8 分钟）。
3. **doc_lint 未接 CI**——478 §3.4 建议在 quality job 加一步；479 未要求，且存量 19 处会使 CI 恒红，
   建议先 `--observe`。
4. **_timeit.py / _rp479*.log / _po479.log 等临时件**（untracked，`*.log` 已被 .gitignore 覆盖）——
   收工后可删：`Remove-Item _timeit.py,_rp479*.log,_rp479*.err,_rp479_*.txt,_po479.*,_pt479*.log,_pt479*.err`。

## 9. 开工前 6 份参考文档的实读记录

474（25 矛盾 + P0 十五项）、475（12 项可填坑）、476（四波路线图：第一波含 ccache 1.1 / 增量 replay 1.2 / 零断言测试 1.3 / claim 契约 1.4 / 静默失败 1.5 / 规范同步 1.6 / golden 过期 1.7）、477（22 项未落地）、478（三项详设）、465（ccache 原始设计，WSL 侧）、`_worklog_472.md`（两个待裁决项）。
**文档与实际偏差（按铁律以磁盘为准）**：476 称第一波验收"日常 replay 4.5min → <30s"——
本机实测基线 **298.5s ≈ 5min**（与 470 记录 300-400s 一致），ccache 后 **244.5s**，距 <30s 仍远，
须靠 1.2 增量 replay。

## 10. 终态 fresh run（2026-09-14，全部在最终提交后实跑）

| 项 | 命令 | 结果 |
|---|---|---|
| gate | `tools/gate_engine.py --check` | 规则 **51** · **BLOCK=0 WARN=32 ADVICE=5** |
| poison | `tools/poison_drill.py --write-surface-map` | **63/63** · RULE-COVERAGE **25/51**+豁免 27 · 攻击面 **11/11** |
| pytest | `-m pytest tests -q` | **302 点全绿**（272 + 30 新增：doc_lint 12 / git 绑定 10 / ccache 8） |
| replay | `tools/atom_evidence_replay.py --check` | **confirm=56 refute=0 infra_error=0**（三次一致） |
| selfcheck | `tools/writer_selfcheck.py --all` | 56 卡 **fail=0** |
| doc_lint | `tools/doc_lint.py`（严格）/ `--observe` | 退出码 **1 / 0** 正确 · 存量失真 **19** 处 |

**过程踩坑（供后续批次复用）**：
1. `git add` 后必看 `diff --cached --stat`——本轮无并行会话污染（472 曾踩过）；
2. pytest 全套约 10 分钟且中段有长测试 ⇒ 一律后台 + 轮询日志（`Start-Process -RedirectStandardOutput`），
   不要用管道 `| Select-Object`（会全缓冲 → 工具报"空闲超时"误判卡死）；
3. 计时用独立 wrapper（本仓 `_timeit.py`，临时件）而非 shell 重定向——PowerShell 的
   `Set-Content` 无编码会被安全策略阻断。
