# 632 F1 · QueYi Core 接口抽象 **v0.3**

- 接口数：**5**（与 v0.2 相同）
- **真实适配接口：1 个 → `Evidence`**（5 个方法接到真实工具）
- 其余 4 接口（Claim / Verifier / Authority / Attacker）仍**只定义不实现**（v0.2 状态）

## 一、v0.2 → v0.3 的差异

| 项 | v0.2（631 F1） | v0.3（632 F1） |
|---|---|---|
| Evidence 接口 | `raise NotImplementedError` 占位 | **真实适配** `EvidenceAdapter` |
| 真实后端接线 | 无 | 证据卡解析 + `artifact_sha256` 比对 + `atom_evidence_replay` |
| 适配接口数 | 0 | **1 / 5** |
| 其余接口 | 只定义不实现 | 仍只定义不实现（范式已跑通，留后续） |

## 二、EvidenceAdapter 真实接线

| 方法 | 真实后端 |
|---|---|
| `id()` | 解析证据卡 frontmatter `id` |
| `artifact_assert()` | 解析 `artifact_assert` 列表 |
| `verify_hash()` | 读 `artifact` 文件算 sha256，与 `artifact_sha256` 比对 |
| `provenance()` | 返回 source/command/fixture/serves/hypothesis |
| `replay()` | 委托 `atom_evidence_replay.replay_card` → confirm/refute/infra 三态 |

## 三、真实数据演示（只读扫描）

- 演示卡：`evidence/conc/EV-CONC-001.md`
- `id()` = `EV-CONC-001`
- `verify_hash()` = `True`
- `artifact_assert` 条数 = `12`
- `provenance` 字段 = `['command', 'fixture', 'hypothesis', 'serves', 'source']`

## 四、诚实登记

1. **仅 1/5 接口真实适配**：其余 4 个接口本批**没有**实现（仅 Evidence 跑通了「抽象 → 真实工具」接线范式）；
2. **`replay()` 为委托式真实调用**：懒加载 `atom_evidence_replay.replay_card`，若运行环境缺该工具或复算依赖，则返回 `infra`（不假装成功）；
3. **`verify_hash()` 依赖 `artifact_sha256` 声明**：该字段缺失的证据卡无法比对（与 L2.3 探针登记的覆盖缺口同源）；
4. `--check` 只读：适配器对真实证据卡只做读取 + 哈希计算，零改写；本报告由 `--report` 生成。
