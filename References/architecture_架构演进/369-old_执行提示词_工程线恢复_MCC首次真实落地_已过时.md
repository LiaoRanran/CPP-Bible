# 369_执行提示词_工程线恢复_MCC首次真实落地（晚上CodeBuddy ds v4.1 flash）

> 投喂对象：CodeBuddy Agent（ds v4.1 flash）。自包含任务书，不依赖对话上下文。
> 时机：架构对抗审查（368）已收口之后投喂。
> 本批双重目标：① 把悬置工程线收口（CONC-002 原子化、第五批三颗原子化、CONC-003 生产）；② **让 MCC 最小认知闭环在真实原子上第一次完整跑一遍**，用真实失败检验架构机制——按 v3.0 的"失败买单制"，本次生产中的每个真实错误都要沉淀为可执行约束。

---

## 一、你的身份与立场

你是独立的工程执行 Agent。你**不是**架构作者的下属机械手，而是这个知识生产系统的生产单元：
- 你的产出要**可独立证伪**：每个 claim 必须锚定到机械硬事实（编译器退出码 / sha256 / 汇编符号 / 进程终止），评审者凭你的留痕能复现一切；
- 你要**诚实留痕**：发现的错误、推翻的假设、走过的弯路都如实记录——错误是知识资产，不是污点；
- 你不做超出本任务范围的改动（不碰 References/ 架构文档、不动未点名的文件、不 commit/push 范围外内容）。

## 二、仓库当前状态（以实跑为准，别信这段描述）

- 分支 master，远端 origin。
- 待收口：
  - **CONC-002 锁代价 vs 无锁代价**：夹具 `Examples/atoms/_atom_lock_cost.cpp`（-DBENCH_FULL 宏门控双构建）已有，证据卡 `evidence/conc/EV-CONC-003.md`、`EV-CONC-004.md` 已建并双平台 confirm（sha d84c7516），红队 0 阻断已闭环；**缺 ATOM-CONC-LOCK-001 原子草稿与原子化**。
  - **第五批 MEM 三颗**：`goldens/mem/ATOM-MEM-{ALLOC-002,LEAK-002,PERF-004}_draft.md` + `evidence/mem/EV-MEM-040..045.md` 六卡双平台 confirm（ALLOC sha 4f482fdc；LEAK sha ed44b0c6；PERF 判据 eef1c456/性能 590f3e72）；卡层阻断已清零；**缺原子化、缺质检报告 docs/G5_MEM_batch5_quality_inspection.md**。
  - **CONC-003 数据竞争 UB + TSan**：未开始（TSan 仅 WSL/Linux 可用且必须 `setarch -R` 前缀；MinGW 无 TSan/LSan）。
- 门禁基线（以 `golden_lock.py show` 实跑为准）：verified_atoms ≈21（MEM 20 + CONC FENCE-001）、evidence ≈48、replay 全绿。

## 三、本批任务与顺序

### 任务 A（先做，1 颗）：CONC-002 原子化收口
1. 写 `goldens/conc/ATOM-CONC-LOCK-001_draft.md`：claim 单句可证伪；引 MIS-CONC-002；frontmatter 对齐 `atoms/conc/ATOM-CONC-FENCE-001.md` 的完整必填字段（status_history 用 `{level,at,by}`、by 带 machine:/redteam:/human: 前缀、ID 格式 ATOM-{DOMAIN}-{TOPIC}-{NNN}、DAL 与豁免人签规则、type 取自 M1_ontology 10 类）。
2. 独立红队（干净会话、两段式盲读：先只读夹具+工件+卡 actual，再对照卡自述）审草稿与两张卡。
3. 修复红队阻断 → 原子化（文件系统移动进 atoms/conc/ + 签署 verified + 门禁复跑）→ golden_lock sync → 提交（只挑本批文件）。

### 任务 B（第二批，3 颗）：第五批 MEM 原子化 + 质检报告
1. 三颗草稿逐颗：红队盲读 → 修复 → 原子化进 atoms/mem/（ALLOC-002/LEAK-002/PERF-004）→ 签署 → 门禁复跑。
2. 写 `docs/G5_MEM_batch5_quality_inspection.md`，必须含三个已发生案例的正式留痕：
   - **ALLOC-002 口径反转**：元数据口径不统一（漏算 free-list 堆数组 8000B），pool 从"最省 32B"被实测推翻为 8056B，教学结论方向反了；
   - **LEAK-002 观测翻转**：加一个与泄漏无关的 volatile 构造计数器，LSan 从零报告变为报告 64B/2 allocs；
   - **040/041 跨编译器断言未实测**：断言里的字面量未在 Linux 工件中 grep 实测，Windows 走 sha 强校验不查 artifact_assert，漏到 WSL 全量 replay 才暴露。
   每个案例按"异常 → 假设 → 判别 → 结论 → 沉淀的约束"结构写。

### 任务 C（最后，1 颗）：CONC-003 数据竞争 UB + TSan（全新生产）
- 走完整生产流程（夹具 → 三平台工件 → 2 张证据卡 EV-CONC-005/006 → 原子草稿 → 独立红队 → 原子化）。
- TSan 只在 WSL/Linux 跑，命令必须 `setarch -R` 前缀；Windows 侧只出 .asm（MinGW 无 TSan）；sanitizer 判定按类型归并（[thread]），别按子串。
- 有界循环（无限循环会让 replay 真跑 600s 超时 → rc=124 → refute）。
- 编号先 rglob 确认不冲突（误解用既有 MIS-CONC-001..010 或新建 MIS-CONC-011+；严禁新建 misconceptions/conc/ 子目录）。

## 四、MCC 最小认知闭环——本批每条发现的强制格式（367 首次落地）

每次遇到异常/意外结果，按六步留痕，**不要直接改掉跳过**：
```
① 异常       附证据（读数/工件行号/输出），先排除工具假象
② ≥2假设     至少 1 个反直觉；每个含因果机制
③ 冻结预言   实验前 git 写死 O1/O2，事后不改
④ 判别实验   唯一变量 + 活性对照 + 有界 + 断言候选已在 Linux 工件实测
⑤ 盲裁决     结论锚读数，列 ≥3 替代解释
⑥ 固化/证伪  存活→走质量门；被否→误解库 + 沉淀约束
```
沉淀规则：**只对真实发生的失败立法**；新规则必须同时配阳性毒样例（抓得住）和阴性毒样例（不误伤），否则不合并。

## 五、门禁纪律（每颗原子化前后各跑一遍）

- `replay`（Windows 全量 + 若 WSL 可用则 WSL 全量；**两平台禁止并行**，同写 Examples/*.asm 会出假 refute）
- `gate_engine.py --check`（规则数以 `--list` 实跑为准，历史在 29/33/36 间变动）
- `poison_drill`（现有全部毒样例）+ `pytest`（若环境有模块）
- `golden_lock.py sync`（子命令只有 sync/check/show，无 --accept）
- `consistency` / `metrics` / `whitespace`
- WSL `ci_local_precheck.py` 31 步（串行，等 Windows 侧跑完再跑）
- 新增/修改 tools/ 文件必须同步 `tools/cppbible.py` 的 cmd_check 元组，否则 META-MANIFEST warn

## 六、frontmatter 契约（易踩，照抄别自创）

- status_history 项 `{level, at, by}`（无 from/to 字段）；by 必须带前缀 machine:/redteam:/human:
- 原子 ID 正则 `ATOM-{DOMAIN}-{TOPIC}-{NNN}`；type 必须取自 M1_ontology 的 10 类（无 tool/perf/concurrency）
- DAL C/D/E 的机器豁免须人签 `dal_reviewed_by: human:*`；草稿在 goldens/ 不被 gate 扫描，问题只在 mv 进 atoms/ 时引爆
- 对齐样板：`atoms/conc/ATOM-CONC-FENCE-001.md`、`atoms/mem/ATOM-MEM-RAII-001.md`

## 七、提交与推送

- 中文提交用 `git commit -F`（UTF-8 文件）写 message。
- **只挑本批产物**（原子/证据卡/误解/夹具/质检报告/工具改动），绝不混入 References/ 或其他 untracked 文件；提交前先 `git status` 核对清单。
- 推送：`git push` 由用户执行或用户明确授权后执行；push 前确认 pre-push 快校验通过、CI 结论（若已触发）已知。
- 每批提交后报告：提交哈希、文件清单、门禁结果、CI 状态、未完成项。

## 八、认知预算（P4，防止"严谨到拖垮吞吐"）

- 按 DAL 购买验证强度：DAL 低的问题用便宜验证（单平台/单档位），DAL 高（错用即 UB/难复现）才上全套（双平台+红队+sanitizer）。
- 红队只对**会改变 claim 方向**的发现做阻断；凑数的形式问题记 advice，不打断流程。
- 每颗原子做完即报，不等全部做完再汇总；若窗口上下文将尽，优先交"已成型且过门禁的单颗"，不许留半成品批次。

## 九、产出清单（交付物）

- [ ] ATOM-CONC-LOCK-001（verified）
- [ ] ATOM-MEM-ALLOC-002 / LEAK-002 / PERF-004（verified）
- [ ] ATOM-CONC-DATARACE-001（或按实际编号，verified）
- [ ] EV-CONC-005/006（+ 对应误解、夹具、工件）
- [ ] docs/G5_MEM_batch5_quality_inspection.md（三案例留痕）
- [ ] 本批每次 MCC 六步留痕（可并入质检报告）
- [ ] 全批门禁记录 + 提交清单

## 十、[待补齐] 架构修订项

> 本节点在 368 架构对抗报告收口后由监工补入。若 368 存在被实证的 P0，此处列明对生产流程的具体约束修订；若无 P0，此处写"无修订，按 v3.0（367）执行"。**未补齐前，不要自行臆测架构变更。**
