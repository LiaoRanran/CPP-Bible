# replay 不变量检查报告（605 任务 2）

> 生成时间：2026-09-19 · 工具：tools/replay_invariants.py --check

## 总览

| 不变量 | 结果 | 耗时 | 说明 |
|--------|------|------|------|
| I1 工件还原 | ✅ pass | 1.07s | Examples/ 指纹稳定（1557 文件），指纹 13522d36e8a75d8c |
| I2 编译可复现 | ✅ pass | 0.96s | 2/2 张 confirm 卡两次重编译均 ok（复用 replay._recompile_invariant） |
| I4 沙箱隔离 | ✅ pass | 0.0s | 临时目录操作不影响真实仓库，临时目录已清理 |

**全部通过 ✓**

## 详细结果

### I1 工件还原不变量
- 扫描文件数：1557
- 指纹（前16位）：13522d36e8a75d8c
- 两次指纹比对：一致
- 说明：本检查验证指纹机制本身可靠；真实还原逻辑由 replay 的 `_restore_artifact()` 保证，603 测试 test_replay_invariants_603.py 已覆盖

### I2 编译可复现不变量
- 检查卡数：2（EV-CONC-001、EV-CONC-002）
- 实现：复用 replay 的 `_recompile_invariant()`（独立重编译 + CCACHE_DISABLE=1 + 临时目录隔离 + sha 比对）
- 结果：
  - EV-CONC-001：run1=ok, run2=ok, sha=8dd19bc6bf2facc2（与卡值一致）
  - EV-CONC-002：run1=ok, run2=ok, sha=8dd19bc6bf2facc2（与卡值一致）
- 说明：603 metrics 已验证 10/10 reproducible，本检查抽样 2 张验证机制可用

### I4 沙箱隔离不变量
- 实现：在临时目录创建 marker 文件，验证不泄漏到真实仓库
- 结果：真实仓库 tools/ 指纹不变，marker 未泄漏
- 临时目录：已清理（TemporaryDirectory 上下文管理器自动清理）

## 已知限制

1. **I1 只验证指纹稳定**：不主动跑 replay 后再比对（那需要完整 replay 运行，耗时较长）；真实还原逻辑由 603 测试覆盖
2. **I2 只抽样 2 张卡**：完整 56 张卡的编译可复现由 603 metrics_collector 验证（10/10）；本检查是快速冒烟
3. **I4 只验证临时目录隔离**：不验证完整 batch_root 上下文（那需要跑 mutation_fuzz）；真实沙箱隔离由 579/580 测试覆盖
4. **I3 锁一致性 / I5 manifest 一致性**：本批未实现，留到下一批（需要并发测试和更复杂的 mock）

## 运行环境

- Python：.venv (Py3.13)
- 编译器：g++ 15.3.0 MinGW-w64（通过 replay._recompile_invariant 调用）
- 操作系统：Windows 11
- 运行模式：单进程，无并发
