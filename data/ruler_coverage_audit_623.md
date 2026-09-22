# 623 C2 · 尺子入根扩展审计（_arch_v19 8/11 裸露 复核）

> 工具：`tools/ruler_coverage_audit_623.py`（复算 _arch_v19 p03 实验3）
> 保护基准：`tools/.tool_checksums`（CORE_TOOLS 5 + RULER_TOOLS 10 + test_config 2 + supply_chain 5）

---

## 一、问题来源

_arch_v19 维度3（元验证层）探针 p03_meta_verification.py **实验3** 定义了 **11 个关键判决尺子**
（决定 pass/fail / 质量基线 / 学习者判决 / 攻击面图的工具），并实测：

| 尺子 | 类型 | 探针时状态 |
|---|---|---|
| gate_engine.py | CORE_TOOLS | 已保护 |
| poison_drill.py | CORE_TOOLS | 已保护 |
| atom_evidence_replay.py | CORE_TOOLS | 已保护 |
| mutation_fuzz.py | RULER_TOOLS | **裸露** |
| tool_integrity.py | RULER_TOOLS | **裸露** |
| d5_compile_gate.py | RULER_TOOLS | **裸露** |
| d5_runtime_gate.py | RULER_TOOLS | **裸露** |
| d5_source_integrity.py | RULER_TOOLS | **裸露** |
| attack_edge_generator.py | RULER_TOOLS | **裸露** |
| bkt_solver.py | RULER_TOOLS | **裸露** |
| learner_mastery_update_613.py | RULER_TOOLS | **裸露** |

⇒ **8/11 裸露**（仅 3 个 CORE_TOOLS 受保护，8 个 ruler 型工具裸奔）。

## 二、修复路径

1. **615 B3** 引入 `RULER_TOOLS` 元组（10 个 ruler 型工具），把它们的 sha256 钉进 `.tool_checksums` 的 `# ruler` 节。
2. **623 B1** 执行 `tool_integrity.py --update` 重钉（同时重钉 Merkle 根与 supply_chain）。

## 三、623 C2 复核结果（tools/ruler_coverage_audit_623.py --check）

```
关键判决尺子：11 个
已保护：11 / 11
裸露：[] （占比 0%）
✓ 11 个关键判决尺子全部已钉入 .tool_checksums（_arch_v19 的 8/11 裸露已修复）
```

`.tool_checksums` 当前 `# ruler` 节（10 项）：`attack_edge_generator / bkt_solver / d5_compile_gate /
d5_runtime_gate / d5_source_integrity / golden_lock / learner_mastery_update_613 / mutation_fuzz /
replay_invariants / tool_integrity`；`# core` 节（5 项）含 `gate_engine / poison_drill /
atom_evidence_replay / toolchain / cppbible`。**11 个关键尺子全部命中**。

## 四、结论

- _arch_v19 指出的 **8/11 裸露已修复**（615 B3 的 RULER_TOOLS + 623 B1 重钉）。
- 闭环的"判决尺子"现已被哈希面完整覆盖：改任一尺子必然自红（exit 1），满足"生成者不能兼任判断者"的纵深防御。
- **残余风险**（诚实登记）：哈希面只能发现"尺子被改"，判不了"善意还是恶意"；且 `.tool_checksums` 自身不纳入校验（递归无解，依赖 git + 人工 review）。这属设计边界，非本批可消除。

## 五、后续建议（留 624）

- 探针实验3 的 `critical` 集合是手工枚举；建议把该集合**固化进 `tool_integrity.py` 的 RULER_TOOLS**，
  使"11 关键尺子"成为单一真源（当前探针与 tool_integrity 各有一份，存在漂移风险）。
- 可加 `--verify-coverage` 让 `tool_integrity --check` 直接校验"关键尺子 100% 覆盖"。

## 六、局限性声明

1. 本审计为**只读复算**，未修改任何受控文件（仅 `tool_integrity --update` 重钉基准，属已批准的修复动作）。
2. 依赖 `.tool_checksums` 基准完整性（其本身未被自校验，依赖 git 历史 + 人审）。
3. 探针的 `critical` 11 项集合未经语义穷举，可能遗漏其他隐含判决尺子。
