# 631 F1 · QueYi Core 接口抽象 **v0.2**

- 接口数：**5**（v0.1 为 4，v0.2 新增 `Authority`） · 方法总数：**25**
- 实现状态：**0 个已实现**（§十 F1.2 只定义不实现）

## 一、接口清单与实现状态映射

### Claim（since v0.1）

- v0.2 新增：命题级字段（liveness / signed_by）
- 方法（5 个，均有 docstring：5/5）

| 方法 | docstring |
|---|---|
| `evidence_refs()` | 引用的证据 ID 列表。 |
| `id()` | 命题唯一 ID（如 `ATOM-CONC-FENCE-001/prop-1`）。 |
| `statement()` | 自然语言陈述。 |
| `structured()` | 结构化字段：subject / predicate / object / claim_type / liveness / signed_by |
| `validate()` | 按规则校验命题完整性，返回 {ok, violations}。 |

| 现有实现映射 | 存在 |
|---|---|
| `tools/gate_engine.py` | ✅ |

### Evidence（since v0.1）

- v0.2 新增：artifact_assert + replay 三态
- 方法（5 个，均有 docstring：5/5）

| 方法 | docstring |
|---|---|
| `artifact_assert()` | 工件断言（可复算的具体断言，含夹具符号）。 |
| `id()` | 证据 ID（如 `EV-CONC-001`）。 |
| `provenance()` | 溯源信息（来源/生成方式/时间）。 |
| `replay()` | 复算该证据，返回 confirm/refute/infra 三态。 |
| `verify_hash()` | 校验工件内容与登记哈希一致。 |

| 现有实现映射 | 存在 |
|---|---|
| `tools/atom_evidence_replay.py` | ✅ |

### Verifier（since v0.1（原名 Verify））

- v0.2 新增：独立验证者钩子 + 凭证产出
- 方法（5 个，均有 docstring：5/5）

| 方法 | docstring |
|---|---|
| `attest()` | 产出可验证凭证（VSA）并可选入册透明日志。 |
| `id()` | 验证器 ID。 |
| `independent_hook()` | **独立验证者钩子**：返回可零依赖重算的入口（他验 B1）。 |
| `rules()` | 规则集 ID 列表。 |
| `verify()` | 验证一个对象（Claim / Evidence / Attacker 结果）。 |

| 现有实现映射 | 存在 |
|---|---|
| `tools/gate_engine.py` | ✅ |
| `tools/independent_verifier_628.py` | ✅ |
| `tools/vsa_attestation_628.py` | ✅ |

### Authority（since v0.2）

- v0.2 新增：整个接口（含 append-only 账本 + 透明日志 + 人审入口）
- 方法（5 个，均有 docstring：5/5）

| 方法 | docstring |
|---|---|
| `append()` | 追加一条裁定（**只追加，不可改/删**）。 |
| `chain_verify()` | 校验账本哈希链完整性。 |
| `human_decision()` | 人审裁定入口（**机器永不代签** ⇒ 只能由人调用）。 |
| `ledger_path()` | 账本文件路径（append-only JSONL）。 |
| `transparency_log()` | 透明日志路径（他验 B3）。 |

| 现有实现映射 | 存在 |
|---|---|
| `tools/decision_event_v2_626.py` | ✅ |
| `tools/transparency_log_628.py` | ✅ |
| `data/authority/decision_event_v2_ledger.jsonl` | ✅ |

### Attacker（since v0.1（原名 Attack））

- v0.2 新增：目标函数 objective() + 沙箱契约 + revert 契约
- 方法（5 个，均有 docstring：5/5）

| 方法 | docstring |
|---|---|
| `apply_in_sandbox()` | 在沙箱中施加（含备份/还原/校验）。 |
| `id()` | 攻击器 ID。 |
| `mutate()` | 对目标施加一次扰动，返回变体。 |
| `objective()` | **目标函数**：返回被优化的目标（如 disagreement × ambiguity × provenance）。 |
| `revert()` | 还原（必须可 `finally` 调用，见 631 C2 防护设计）。 |

| 现有实现映射 | 存在 |
|---|---|
| `tools/adversarial_loop_620.py` | ✅ |
| `tools/sandbox_apply_622.py` | ✅ |
| `tools/attack_objective_629.py` | ✅ |

## 二、v0.1 → v0.2 的差异

| 项 | v0.1（625 C2） | v0.2（631 F1） |
|---|---|---|
| 接口数 | 4 | **5**（新增 Authority） |
| 命名 | `Attack` / `Verify` | `Attacker` / `Verifier`（与其他层命名一致） |
| Verifier | 只有 `verify()` | 增加 **独立验证者钩子** + 凭证产出 |
| Attacker | 只有 apply/revert | 增加 **目标函数** `objective()` + 沙箱契约 |
| Authority | 无 | **新增**：append-only 账本 + 透明日志 + 人审入口 |
| Claim | 基础字段 | 增加命题级字段（liveness / signed_by） |

## 三、雷1 剥离触发标准推进情况

| 条件 | 状态 |
|---|---|
| 路径解耦（PathConfig） | ✅ 625 C1 完成 |
| Core 接口抽象 v0.1 | ✅ 625 C2 完成 |
| **Core 接口抽象 v0.2** | ✅ **本批（631 F1）完成**（只定义不实现） |
| 治理裁定 | ⛔ 需人（不代签） |
| 余量 | ⛔ 留后续 |

⇒ 触发标准 **3/5**（原 2/5），**本批推进 1 个条件**。

## 四、诚实登记

1. **只定义不实现**：所有方法体 `raise NotImplementedError`，本批**没有**改任何生产工具（§十 F1.2）；
2. **映射是「已有能力」的指针**，不等于「已有该接口」——真正的接口抽出（抽象基类/协议 + 各工具适配）仍需下一批 ⇒ 列入交人；
3. **命名变更（Attack→Attacker / Verify→Verifier）是 v0.2 的单方面决定**：若与后续实现命名冲突，改这里即可（无代码依赖）；
4. 本工具只读：`--check` 不实例化业务对象、不写任何文件（除报告由 `--report` 生成）。
