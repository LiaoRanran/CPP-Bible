# 627 B2 · V2 回归验证（静态分析）

- **判定**：通过 ✅（V2 对 CORE_TOOLS 无回归风险）

## CORE_TOOLS 隔离性

| 工具 | 隔离 V2 |
|---|---|
| gate_engine.py | ✅ |
| atom_evidence_replay.py | ✅ |
| poison_drill.py | ✅ |
| toolchain.py | ✅ |
| cppbible.py | ✅ |

- legacy W2 求解器 `weighted_af_solver.py` 未被本批次修改：True
- 本批次未修改 CORE_TOOLS：True

> **注**：gate / poison / replay / tool_integrity --check **未执行**（627 铁律不跑监工门禁）。本报告以静态分析证明「CORE_TOOLS 不读取 flag、不依赖 V2 工具」⇒ 启用 flag 无回归可达路径。远程 CI 实跑由人 push 后触发（交人项 #3）。
