# 01 · 方向 1：in-toto 深度调研与本项目落地设计

> 来源：【已查证】in-toto 官方文档 in-toto.io/docs/getting-started（检索 2026-09-19："A layout lists the sequence of steps of the software supply chain, and the functionaries authorized to perform these steps"）；in-toto readthedocs 3.0.0（retrieved 2026-01-13：in-toto-record 生成签名 link 元数据，in-toto-match-products 比对产物）；in-toto GitHub（概述）。其余为本调研设计。

## 1.1 in-toto 核心概念（准确解释）
- **layout（布局）**：项目所有者声明"供应链有哪些步骤、谁有权执行、步骤顺序、检查点"的母文档，自身被签名。
- **step（步骤）**：供应链中的一个环节（如 build / test），由某个 functionary 执行，产生 link。
- **functionary（执行者）**：执行 step 的实体，持有密钥；layout 授权哪些公钥可签署哪些 step。
- **link（链接元数据）**：functionary 执行 step 后产出的记录——含命令、材料哈希（materials）、产品哈希（products）、环境、 byproducts、签名。
- **inspection（检查）**：layout 中声明"验证阶段要跑的命令 + 期望输出"，验证方在收齐 link 后执行。
- **public key / 签名**：link 和 layout 均用 functionary 私钥签名，验证方用 layout 中授权的公钥验签。

## 1.2 link 格式（in-toto 字段，适配本项目）
```json
{
  "_type": "link", "step": "gate_validate",
  "command": ["python", "tools/gate_engine.py", "--check"],
  "materials": { "gate_engine.py": "<sha256>", "rule_defs/H-*.py": {"...":"<sha>"} },
  "products":  { "data/overturned_events.jsonl": "<sha256>", "reports/gate.json": "<sha>" },
  "by_products": {},
  "environment": {"git_head": "2af99a31…", "author": "LiaoRanran", "ts": "ISO8601"},
  "_functionary": "<git HEAD 或公钥指纹>",
  "_sig": "<sha(key+payload)>"   // 单用户阶段模拟签名（见 1.6）
}
```

## 1.3 layout 格式（草案）
```json
{
  "_type": "layout",
  "steps": [
    {"name":"write_cards", "functionaries":["git:HEAD"], "expected_materials":{}, "expected_products":["atoms/**","misconceptions/**"]},
    {"name":"gate_validate", "functionaries":["git:HEAD"], "expected_materials":["write_cards.products"], "expected_products":["gate_engine.py"]},
    {"name":"replay_verify","functionaries":["git:HEAD"], "expected_materials":["gate_validate.products"], "expected_products":["atom_evidence_replay.py"]},
    {"name":"poison_test",  "functionaries":["git:HEAD"], "expected_materials":["replay_verify.products","poison_drill.py"], "expected_products":["poison_drill.py"]},
    {"name":"mutation_test","functionaries":["git:HEAD"], "expected_materials":["poison_test.products"], "expected_products":["data/mutation/**"]},
    {"name":"metrics_collect","functionaries":["git:HEAD"], "expected_materials":["mutation_test.products"], "expected_products":["data/metrics.jsonl"]},
    {"name":"human_review", "functionaries":["git:HEAD"], "expected_materials":["metrics_collect.products"], "expected_products":["data/overturned_events.jsonl"]}
  ],
  "inspections": [{"name":"tool_integrity","command":["python","tools/tool_integrity.py","--check"]}],
  "keys": {"git:HEAD": "<git HEAD 指纹>"},
  "_signed": "<sha(layout 主体 + key)>"
}
```
**链路绑定关键**：step N 的 `expected_materials` 引用 step N-1 的 `products` 哈希集——验证时强制"上一步产物 == 本步材料"，形成不可断裂的溯源链（探针 `verify_chain` 已实测：篡改 write_cards 产品 → 后续链路断裂检测 `chain_tamper_detected=true`）。

## 1.4 验证流程（落成本项目 supply_chain.py）
1. 验 layout 签名（`_signed`）。
2. 逐 step 验 link 签名（`_sig`）。
3. 逐 step 比对 `materials/products` 哈希与磁盘真实文件（`fsha`）——文件级篡改检测。
4. 验链路绑定：step N 的 materials 必须包含 step N-1 的 products（见探针）。
5. 执行 inspections（`tool_integrity --check`、`governance_doc_guard preflight`）。

## 1.5 与 SLSA 的关系
SLSA provenance v1 是 in-toto link 的**一种特化格式**（buildType/invocation/materials/products）；本项目的 link 即"SLSA L1 等价物"的 provenance 记录（见 02/07）。

## 1.6 签名替代方案（单用户阶段，无密钥对）
- **functionary 身份 = `git rev-parse HEAD`（提交指纹）+ `git log -1 --format=%an`（作者）**。
- **模拟签名 = `sha(key + payload)`**（探针 `sim_sign`）。
- **诚实边界**：这不是密码学签名——持有仓库者既能改文件也能重算签名，所以**只能检测"事后篡改"，不能防止"当时伪造"**。真正防伪造需 Ed25519 密钥（W 档：有密钥对后再升级，link `_sig` 换为 `ed25519_sign`）。阶段 3 的 OpenTimestamps 至少把"存在时间"钉死，使事后篡改可被独立验证。

## 1.7 与现有 tool_integrity 的集成
- `tool_integrity` 继续负责"5 核心工具 + 2 测试配置的 sha 基准"（它已 fail-closed `enforce()`）。
- 新增 `supply_chain.py` 负责"步骤级 link 链 + Merkle 根"。
- **gate 启动强制**：`gate_engine.main` 第一句除 `tool_integrity.enforce()` 外，再调 `supply_chain.verify_bootstrap()`——校验当前 Merkle 根（存 `data/supply_chain/merkle_roots.json`）与磁盘一致。这样**规则/策略定义文件（现不在 CORE_TOOLS 内）被纳入根**，封堵 585 攻击 1 的文件级面。
- `tool_integrity --check` 同时作为 layout 的一个 **inspection**。

## 1.8 落地步骤 + 验收（N 档，纯库）
1. 建 `data/supply_chain/links/` 与 `layout.json`（手工/脚本生成）。
2. 实现 `supply_chain.py`：`record`（生成 link）、`verify`（上面 5 步）、`chain-status`。
3. 接入 gate 启动自校验。
4. **验收**：(a) 改任一被覆盖文件 → `verify` 失败；(b) 断链路（删中间 link）→ 失败；(c) 探针回归 585 脚本，文件级篡改被检出。

## 1.9 成本-收益
- 成本：~1 个 `supply_chain.py`（约 200-300 行纯库）+ link/layout schema 设计。学习成本中（需理解 in-toto 语义）。
- 收益：步骤级溯源链 + 链路绑定，把"自签 checksum"升级为"可独立验证的步骤链"；直接封堵 585 攻击 1 文件级面。

## 1.10 反例（看似相关但不适用）
1. **完整 in-toto 框架 + PGP 密钥管理**：需密钥基础设施、密钥分发/撤销流程，单用户阶段无意义（`governance_doc_guard` 已自承"不做 PKI/数字签名/二人签（单用户阶段无意义）" line 14）。
2. **每步 gpg 签名 + 密钥服务器**：运维开销远超单用户收益；模拟签名（git 头）已覆盖"事后篡改检测"需求。

## 1.11 探针实证
`probes/probe_supply_chain.py` 只读扫真实文件（tools/ CORE+TEST_CONFIG、data/overturned_events.jsonl、atoms/misconceptions 样例），建 5 步链 `write_cards→gate_validate→replay_verify→poison_test→human_review`，`chain_verify_ok=true`、`chain_tamper_detected=true`，证明纯标准库可实现且链路绑定有效。
