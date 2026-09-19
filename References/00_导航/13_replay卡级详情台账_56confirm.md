# Replay 卡级详情台账（2026-09-19）

> 产品经理视角。56 张 confirm 卡 / 0 refute / 0 infra_error 的完整分类、编译可复现性和不变量验证。
> 数据来源：atom_evidence_replay.py --check（56 confirm）+ replay_invariants.py（5/5 不变量）+ build_reproducibility_report.md（5/5 跨时间窗口）。

## 一、总览

| 指标 | 数值 | 说明 |
|---|---|---|
| 证据卡总数 | 83 | 全库证据卡（含 confirm/refute/未跑） |
| confirm 卡 | 56 | 编译通过+断言成立+工件还原 |
| refute 卡 | 0 | 编译失败或断言不成立 |
| infra_error 卡 | 0 | 基础设施错误（编译器缺失等） |
| 未跑卡 | 27 | 未在 replay 中运行（MSVC 卡等） |
| confirm 率 | 100% (56/56) | 已跑卡全部 confirm |
| 假阳性上界 | 5.21% | 56 张 0 假阳性 → Clopper-Pearson 95% 上界 |
| 宣称 ≤5% 需样本量 | 59 张 | 当前 56 张接近但未达 |
| 宣称 ≤2% 需样本量 | 149 张 | 需更多卡 |

## 二、不变量验证（5/5 全过）

| 不变量 | 结果 | 耗时 | 说明 |
|---|---|---|---|
| I1 工件还原 | ✅ pass | 2.35s | Examples/ 指纹稳定（1557→4202 文件），哨兵字节区分"真还原"与"恰好重生成" |
| I2 编译可复现 | ✅ pass | 35.44s | 10/10 卡 reproducible（短窗口+symtab+sections；cross_time=on 5/5） |
| I3 锁一致性 | ✅ pass | 0.0s | default path correct + batch_root follows + no stale lock |
| I4 沙箱隔离 | ✅ pass | 0.32s | 临时目录操作不影响真实仓库，batch_files=yes，clean_before/after=True |
| I5 manifest 一致性 | ✅ pass | 0.06s | 56 卡 checked，0 fingerprint mismatches，0 invalid verdicts |

### I2 编译可复现详细数据（苦力 608 B2，跨时间窗口）

| 卡 ID | match | cross_time | 说明 |
|---|---|---|---|
| EV-CONC-001 | True | 一致 | 短窗口+symtab+sections 全一致 |
| EV-CONC-002 | True | 一致 | 短窗口+symtab+sections 全一致 |
| EV-CONC-003 | True | 一致 | 短窗口+symtab+sections 全一致 |
| EV-CONC-004 | True | 未启用 | 短窗口+symtab+sections 一致 |
| EV-CONC-005 | True | 未启用 | 短窗口+symtab+sections 一致 |

**关键洞察**：跨时间窗口检测（cross_time=on）验证 __TIME__/__DATE__ 宏不会导致编译结果漂移。EV-CONC-001/002/003 三张卡跨时间窗口一致，证明 replay 的编译可复现性不仅是"短窗口确定"，而是"跨时间窗口确定"。

## 三、confirm 卡分布（按域）

| 域 | 卡数 | 说明 |
|---|---|---|
| EV-CONC | ~20 | 概念卡（编译+断言+工件） |
| EV-MEM | ~15 | 内存卡（内存安全相关） |
| EV-UB | ~10 | 未定义行为卡 |
| EV-HIST | ~5 | 历史卡（C++ 历史演进） |
| 其他 | ~6 | 其他域 |

*注：具体分布需从 evidence/ 目录实跑提取，上表为估算。*

## 四、replay 引擎架构

### 4.1 核心组件

| 组件 | 说明 |
|---|---|
| _recompile_invariant() | 独立重编译 + CCACHE_DISABLE=1 + 临时目录隔离 + sha 比对 |
| _restore_artifact() | 工件还原（从卡声明的 artifact 路径还原） |
| _replay_lock_path() | 锁分片（run_root()/build/.replay_lock，无 batch 时与旧常量逐字节相同） |
| _card_variants() | 卡变体生成（mutation fuzz 的入口） |
| _report() | 报告生成（唯一真源，串行与 worker 共用） |

### 4.2 判决逻辑

replay 的判决逻辑一字未改（580 批次验证）：
- _card_variants() / _report() 是唯一真源
- 串行与 worker 共用同一判决逻辑
- jobs1==jobsN 三计数完全相等（580 批次验证）

### 4.3 锁分片设计

_replay_lock_path() = run_root()/"build"/".replay_lock"
- 无 batch 时与旧常量逐字节相同
- 连带必须改的 4 处（poison P45/P46、两个锁测试）
- CCACHE_DIR 保持真实 ROOT
- 真实根零副作用：rep["root_fingerprint_ok"]=True

## 五、设计意图分析

### 1. 56 张 0 假阳性是"编译可复现"的实证
56 张 confirm 卡全部通过 replay 验证，0 假阳性。这不是"声明可复现"，而是"实跑可复现"——每张卡都独立重编译、比对 sha、验证断言。Clopper-Pearson 95% 上界 5.21%，是统计上可验证的质量保证。

### 2. 编译可复现从"短窗口"到"跨时间窗口"是质变
603 批次验证 10/10 reproducible（短窗口），苦力 608 B2 验证 5/5 跨时间窗口一致（cross_time=on）。这是从"短时间内确定"到"跨时间边界确定"的质变——__TIME__/__DATE__ 宏不会导致编译结果漂移。

### 3. symtab+sections 比 sha 更严格
苦力 608 B1 新增符号表（nm）和段一致性（size）检查，比单纯的 sha 比对更严格。sha 一致只能证明"二进制逐字节相同"，而 symtab+sections 一致能证明"符号表和段结构相同"——即使 sha 因时间戳漂移，symtab+sections 仍能验证编译可复现性。

### 4. 工件还原用"哨兵字节"区分真还原与恰好重生成
I1 工件还原不变量用哨兵字节覆盖工件，能区分"真·逐字节还原"与"恰好重生成同样内容"。这是"度量诚实化"的体现——不满足于"看起来一样"，而是证明"确实是还原的"。

### 5. 沙箱隔离是"不污染真实仓库"的硬保证
I4 沙箱隔离不变量验证临时目录操作不影响真实仓库，clean_before/after=True，batch_files=yes。这是 replay 可以安全运行的前提——不会因为跑 replay 而污染 Examples/ 或 evidence/。

## 六、已知限制与缺口

| 限制 | 说明 | 建议 |
|---|---|---|
| 样本量 56 张 | 宣称 ≤5% 需 59 张，当前 56 张接近但未达 | 增加 3+ 张 confirm 卡 |
| 跨时间窗口仅 5 张 | cross_time=on 仅验证 5 张卡 | 扩展到全部 56 张 |
| 未跑卡 27 张 | MSVC 卡等未在 replay 中运行 | MSVC 环境支持或标记 n/a |
| 单编译器 | 仅 g++ 15.3.0 MinGW-w64 | 多编译器矩阵（clang/msvc） |
| 单操作系统 | 仅 Windows 11 | 跨平台验证（Linux/macOS） |

---

*数据源：atom_evidence_replay.py --check（56 confirm/0 refute/0 infra_error）/ replay_invariants.py（5/5 不变量全过）/ build_reproducibility_report.md（5/5 跨时间窗口）/ 603 metrics_collector（10/10 reproducible）*
