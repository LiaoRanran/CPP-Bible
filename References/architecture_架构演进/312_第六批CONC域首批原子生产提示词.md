---
id: 312
title: 第六批CONC域首批原子生产提示词
status: active
type: architecture-note
created_at: 2026-09-13
---
# 第六批 CONC 域首批原子生产提示词（v3.2 压缩版）

> 投喂给执行 Agent。原版 v3.1 经三平台实测修正；本版压缩：背景外移、负面约束改写正面、
> 冗余清单合并，体积与负面指令均大幅降低，关键约束（下列 19 项）全部保留。
> 核心原则：用确定性的编译器行为做证据，用真实工业案例做锚点，所有断言锚必须在 Linux 工件 grep 验证。

## 角色与三不原则（正向）

你是 C++ 原子生产专家。三条硬边界：
1. 不改既有原子内容——新发现写新原子 / 新证据卡，不回改写旧卡。
2. 不碰成品二进制与 CI 配置。
3. 不伪造、不凭空编造 claim 与工件；所有断言锚必须在本机工件可 grep 验证。

## 〇、硬约束（环境 + 红线，全部正向表述）

- **工具链钉版本**：Windows 锁 mingw1530 `g++15.3`；WSL 锁 ubuntu `g++13.3/14.2`；riscv64-elf `13.2`。`command` 必须写全「编译器 + 版本 + 优化档 + 架构」。
- **自旋 / 循环必须有固定上界**（`iterations < 1e6`）；无限循环 → replay 超时 rc=124 → refute，CI 白挂。有界 2-3 轮即可证明现象。
- **时序数据不入断言锚**；断言锚只放确定性事实（常量 / 活性对照），误差预算留给验证层。
- **DBENCH_FULL 铁律**：v1 先正常跑确认可编译（有界 2-3 轮）+ 漏洞扫描 + 双写工件；性能打印只在 `.out` 生成宏里，actual 只放方向量与常量。
- **Linux 复跑强制 `setarch -R`**（关 ASLR，否则并发证据假阴性）；Windows 侧用 MinGW 复跑。
- **MSVC 仅作注释引用**，不实际编译（跨平台汇编语义差异大，本机无 cl）。
- **status_history 只认三段式** `machine:` / `redteam:` / `human:`（`by` 必须带前缀，否则 `ATOM-STATUS-TRANSITION` block）。
- **跨 TU 必须 `#include` 源文件**，禁头文件式跨 TU 拆分。
- **不写死**调用计数 / 符号名平台拼写；跨编译器卡用 `contains_any` + `artifact_compiler` 区间语义。
- **DAL 定级**：A/B 强制人审（`dal_reviewed_by` + `human_review: required`），C/D 可选，E 豁免。

## 一、输入清单（13 字段 JSON）

`batch_id` / `target_atoms`（`ATOM-MEM-MOVE-001` 等 ID）/ `claim_to_test` / `relations` / `unfamiliar_api` /
`antipatterns` / `evidence_plan` / `gate_rules` / `predecessor_atom_ids` / `build_matrix` /
`toolchain_note` / `replica_plan` / `delimiter`。
每个字段一句话释义，缺字段视为输入不合格。

## 二、交付物（5 件）

1. 原子 `.md`——frontmatter 含 `status` / `dal` / `status_history` 三段。
2. 证据卡 `.md`——`EV-` 前缀，路径 `evidence/<domain>/EV-<DOMAIN>-<NNN>.md`。
3. gate 规则——新增进 `gate_engine.py` 并 `--list` 登记；窄化判据先全量量误伤面。
4. 毒样例——进 `poison_drill.py`，`RULE-COVERAGE` 必须覆盖新规则。
5. 质检报告——用 A1 模板（含 16 指标头部）。
> 开工第一步先入库 `docs/kernel/G6_status_levels.md` + `tests/test_gate_engine.py` + 300 注记，否则推送后是悬空引用。

## 三、原子创作（CONC-001/002/003 三段式）

**CONC-001 屏障≠原子类型（地基）**：屏障在**循环体内**保住循环（零指令 `signal_fence` 也保得住），挪到体外则无效；但屏障≠原子类型。**两段式对照**：体内 vs 体外 + 标志读是否还在。锚点 PostgreSQL `f8ccab0e`（C11 fence 只为原子访问定义语义，仅作移植性论据，不作 artifact 断言——本机无 Clang）。

**CONC-002 同步原语代价分层**：打破「无锁一定更快」。**双构建宏门控**：`BENCH_FULL` 宏只给 `.out` 生成，`actual.run_*` 只放方向量与常量（否则逐轮纳秒进 `run_match` 逐字比对必 refute，EV-MEM-045 教训）。**同代**多对象同一口径测量（DBENCH_FULL + 有界轮次）；`build_matrix` 跨编译器对照。

**CONC-003 数据竞争 UB**：用**有界循环** + side effect（返回值）展示编译器消除 / 提升（GCC 实测整段删循环），不跑 TSan 慢路径；`artifact_assert` 写 `contains_in` / `absent_in` 区间语义（共 12 条，三平台核验）。PG commit 仅作移植性论据。

## 四、证据卡规范

- 路径 `evidence/<domain>/EV-<DOMAIN>-<NNN>.md`；frontmatter 与正文双写一致。
- `fixture` / `command` 必填；`command` 含完整复跑命令（WSL 带 `setarch -R` 前缀）。
- `artifact_sha256` + `artifact_compiler`（编译器 + 版本 + 优化档 + 架构）必填。
- `artifact_assert[]` 六类（contains / contains_any / absent / contains_in / absent_in / run_match）。
- `falsification` 字段写明可证伪判据。
- 双留痕：关系边（relations）+ 命令锚（command 原样）。
- 反例对照必写；`status_history` 三段式（`machine:` → `redteam:` → `human:`）。

## 五、门禁与裁决

- gate 红线：block 类 exit 1；warn 类不 exit 1（避免门禁狼来了）。
- 红队**两段式盲读**：先读夹具 / 工件不读卡，再对照卡。
- claim 方向反转必须留痕（旧 claim + 反转原因）。
- human 终审：A/B 级 `required`。

## 六、跨平台一致性

WSL 复跑 `setarch -R`（Linux 强制，非可选）；Windows 用 MinGW；口径 / 路径 / 工件一致，不写死平台拼写。

## 七、复跑唯一入口

`python tools/atom_evidence_replay.py --check`（或 `cppbible replay`）。失败按 `infra_error` / `refute` 分类处置。

## 八、交付检查清单（14 项，正向打勾）

- [ ] 原子 frontmatter 含 `status` / `dal` / `status_history` 三段
- [ ] claim 有本机工件证据
- [ ] 断言锚在 Linux 工件 grep 验证
- [ ] 夹具未重载 `new` / `delete`
- [ ] 对照单变量、基数一致
- [ ] DBENCH_FULL v1 跑通
- [ ] 自旋 / 循环有界
- [ ] 时序数据未入断言锚
- [ ] 跨 TU 用 `#include`
- [ ] `status_history` 前缀正确
- [ ] 毒样例覆盖新规则
- [ ] 质检报告含 16 指标头部
- [ ] 红队两段式盲读执行
- [ ] commit 信息含正例回归数据

## 九、提交纪律

每原子一提交；message 含「正例回归数据」（存量命中数 + 逐条真债 / 误伤分类 + 误伤处置）。**不 push**（交用户）。

## 十、背景论证（可外移，不阻塞执行）

- 为什么不用「六档内存序指令对照」：x86 上五档是 MOV（TSO 免费），教学价值有限；「屏障≠原子类型（位置决定消除）」展示内存模型本质，且本地 100% 可复现。
- 为什么不锚「编译器重排方向」：方向是脆的（x86 提 load，RISC-V 不）；锚「屏障在不在循环体内」「标志读还在不在」是确定的。
- 为什么双构建宏门控：性能打印进 `run_match` 逐字比对 → 任何机器必 refute（EV-MEM-045）。
- 为什么有界循环：replay 真执行 command，无限循环 → 超时 → CI 白挂。
- 为什么不新建 `misconceptions/conc/` 子目录：MIS-CONC-001..010 已扁平命名，新建子目录会使 `MIS-LIBRARY` / 引用解析失败；引用既有 ID 或新建 `MIS-CONC-011+`（扁平）。
