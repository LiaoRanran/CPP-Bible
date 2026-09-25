# 615 开工基线台账（任务0 · 只读，不跑任何 --check）

> 时间：2026-09-21 ｜ 铁律：**不跑监工门禁**（tool_integrity/gate/poison/replay `--check`），一律静态分析 + 历史记录。
> 所有数字附命令/来源，可复算。

## 1. 人审台账现状（`data/human_attack_edge_annotations.jsonl`）
- 总条数：**388** ｜ sha256：`027dff3aaaa6247f04541968b988fc90325363b75314b1c54fa8a9a346f9f3c4`
- action 分布：**approve 354 / modify 34**（无 reject）
- 审阅者：**LiaoRanran × 388**（单一审阅者）
- 理由**模板数：5**（distinct reason = 5）：
  | 模板 | 条数 | 特征 |
  |---|---|---|
  | T1 | **177** | `命题->MIS对称边…已人审approve` ⇒ **镜像边** |
  | T2 | 176 | `AI预标注approve，抽样验证100%(20/20)…授权批量通过` ⇒ 抽样外推 |
  | T3 | 17 | `AI预标注modify…批量调整为medium` ⇒ 批量改 |
  | T4 | 17 | `命题->MIS对称边…已人审modify` ⇒ **镜像边(modify)** |
  | T5 | 1 | T2 的变体（措辞略异） |
- **镜像边 = T1+T4 = 194**（reason 含「对称边」）｜ 抽样外推 = T2+T5 = **177** ｜ 逐条独立 = **0**
- 理由长度：min **47** / 中位 **67** / max **80** 字符（>50 者 371 条；**无一条 <47**）
- ▶ 结论：388 条全部为**批量授权模板**，**0 条逐条独立判断**。

## 2. 规则一致性与 EV-MATRIX-UNBACKED 现状
- 规则定义**内嵌于 `tools/gate_engine.py`**（无独立规则文件；见 tool_integrity 注释）。
- 规则总数（历史基线）：**63**；静态分析 `sev` 覆盖表中 **warn 级规则 = 16**（`sev.get(rid,"block")`）。
- **EV-MATRIX-UNBACKED 语义**（`gate_engine.py` L1069–1093）：
  - 仅对 `compiler: [c1,c2,…]` 且**编译器数 >1** 的证据卡生效；
  - 剥去 `actual` 段后，统计「可核对留痕」：`(Examples|build)/*.out` 路径 ∪ `run #N`/裸 10+位 CI run 号 ∪ `::notice::` ∪ `标准条文|M2.*永久边界`；
  - backed = **(outs+runs ≥2)** ∨ **(notice ∧ (outs∨runs))** ∨ **has_law**；否则 ⇒ **warn EV-MATRIX-UNBACKED**。
- 规则定义文档（只读参考）：`References/architecture_架构演进/588_建设包_变异驱动发现器完备性…matrix尾注释收口….md`、`docs/compiler-matrix.md`。

## 3. warn 基线现状（`tools/golden_state.json`）
- schema `cppbible-golden-lock/1.0`，commit `dd5b029`，updated 2026-09-21。
- `block_findings = 0` ｜ **`warn_findings = 186`** ｜ atoms 27 / evidence 56 / verified_atoms 26 / replay_confirm 56 / replay_infra 0。
- **legacy 豁免**：`data/governance_weakening_scan.json`（high55/med186/low38）+ 毒样例豁免 `tools/poison_exemptions.yaml`（27 条 legacy，见 C2）。
- （**不跑 gate --check**；186/63 取自 standing baseline 与 golden_state。）

## 4. CI 配置现状（`.github/workflows/ci.yml`）
- **pyyaml 已补装**：`gate` job 与 `quality` job 在 `setup-python` 后各有 `pip install --quiet pyyaml hypothesis`（614 A1，commit `512d991`）。
- 四 job 依赖：`pytest` job 装 `pytest pytest-xdist pyyaml hypothesis`；`replay job` 走增量；`quality` job 跑 ruff/mypy；`gate` job 跑 `gate_engine --check` + S1–S6（golden_lock `--no-replay` / debt_ledger / poison_drill）。

## 5. 学习者镜像现状
- `data/learner_state.json`：**不存在（未初始化）**。
- `data/learner_state_612.jsonl`：27 行（612 初始化态）｜ `data/learner_behaviors.jsonl`：**50 行**（614 simulate，标注 simulated）。
- 真实学习事件：**0**（门未开）。

## 6. 尺子保护现状（`tools/tool_integrity.py`）
- 受保护文件 **12**：
  - CORE_TOOLS（5）：`gate_engine.py` `atom_evidence_replay.py` `poison_drill.py` `toolchain.py` `cppbible.py`
  - TEST_CONFIG（2）：`tests/conftest.py` `pyproject.toml`
  - SUPPLY_CHAIN_FILES（5）：`tools/poison_exemptions.yaml` `tools/poison_surface_map.json` `data/governance_docs_manifest.json` `data/supply_chain/merkle_roots.json` `data/supply_chain/layout.json`
- `.tool_checksums` 自身不纳入（递归无解）⇒ 由 git 历史兜底。

## 7. 其他
- `data/metrics.jsonl`：**12 行**（非空，可供 C3 趋势）。
- 受控目录（atoms/evidence/Examples/Book）：本批**不改**。


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true
