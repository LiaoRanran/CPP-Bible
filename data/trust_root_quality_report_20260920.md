# 信任根数据质量报告（2026-09-20 化债复算）

## 一、四层纵深防护

| 层级 | 工具 | 状态 | 覆盖范围 |
|---|---|---|---|
| L1 工具校验和 | tools/.tool_checksums | ✅ 14 个条目 | 5 核心工具 + 2 测试配置 + Merkle + governance + supply_chain |
| L2 Merkle 完整性 | data/supply_chain/merkle_roots.json | ✅ 5 个目录 | atoms/ evidence/ Examples/ Book/ tools/ |
| L3 in-toto 溯源 | data/supply_chain/layout.json | ✅ 存在 | 5 步链式溯源（build → test → scan → sign → verify） |
| L4 governance 台账 | data/governance_docs_manifest.json | ✅ 存在 | 治理文档完整性 + self_hash |

## 二、各层数据质量

### 2.1 L1 工具校验和（14 个条目）

- 覆盖：gate_engine.py / atom_evidence_replay.py / poison_drill.py / toolchain.py / cppbible.py（5 核心）
- 扩展：test_config（2 个）/ merkle_roots.json / governance_docs_manifest.json / supply_chain layout.json
- 重钉机制：修改 CORE_TOOLS 后必须同 commit 运行 `tool_integrity.py --update`
- 验证：`tool_integrity.py --check` exit 0（本轮化债已验证）

### 2.2 L2 Merkle 完整性（5 个目录）

- 覆盖目录：atoms/（28 张卡）/ evidence/（57 张卡）/ Examples/（1458 个文件）/ Book/ / tools/
- 算法：SHA-256 Merkle 树
- 本轮化债修复：Examples 目录文件数 1540→1541（M1 TCE 工件 `_atom_fence_vs_atomic.nc1.cpp` 未同步），已运行 `tool_integrity.py --update` 重钉
- 验证：`tool_integrity.py --check-merkle` exit 0

### 2.3 L3 in-toto 溯源（layout.json）

- 5 步链：build → test → scan → sign → verify
- 每步包含：name / expected_command / expected_artifacts / pubkeys
- 单用户结构性上限：无真实密钥签名（pubkeys 是占位），in-toto 的"身份验证"在单用户模型下无法闭环
- 600 调研结论：in-toto 是"可换验证者"的硬前提，但单用户阶段只能做到"链式溯源"，做不到"身份验证"

### 2.4 L4 governance 台账

- 字段：generated_at / git_commit / files / self_hash
- self_hash：台账自身的哈希，防止"改台账而不被发现"
- 本轮化债更新：登记 611.md + 17 处变更（导航文档更新），self_hash 已重算
- 验证：`governance_doc_guard.py verify` exit 0

## 三、governance 弱化指令扫描

- 总 findings：279 条
- 分布：high=55 / medium=186 / low=38（注：JSON 字段名非 severity，需从 summary 读取）
- 本轮化债刷新：scan 重新运行，纳入 592/596/598/600/611 新文档
- high=55 的性质：均为历史投喂词里的描述性讨论（"降级为 warn""跳过门禁""豁免毒样例"被当作该做法本身在讨论），需人审逐条确认是"描述"还是"真实攻击指令"
- 工具只做机械重录，不构成语义认可

## 四、585 红队攻击封堵现状

| 攻击 | 描述 | 封堵状态 | 残余风险 |
|---|---|---|---|
| 攻击1 | 规则/策略定义文件不在 tool_integrity 覆盖内 | ✅ Merkle + governance 台账封堵 | 进程内运行时篡改（需运行时规则指纹，W 档） |
| 攻击2 | 豁免台账可篡改 | ✅ poison_drill 豁免台账钉死 + Merkle | 无 |
| 攻击3 | 人签自证（git 作者可自设） | ⚠️ 592 git 作者绑定部分封堵 | 单用户结构性上限（无第三方时间戳/签名身份认证） |

**600 调研纠偏**：585 Q6"可信时间戳结构性无意义"对 OpenTimestamps 链锚不成立——免密钥、Bitcoin 头公开可验，单用户模型内可接入。但 609 D1 只做了 OTS 工具框架，未实际上链（需联网+外部 CLI）。

## 五、单用户结构性上限

| 能力 | 状态 | 上限原因 |
|---|---|---|
| 工具校验和 | ✅ 可闭环 | 纯本地，无需第三方 |
| Merkle 完整性 | ✅ 可闭环 | 纯本地，无需第三方 |
| in-toto 链式溯源 | ✅ 可闭环（无签名） | 单用户无真实密钥 |
| in-toto 身份验证 | ❌ 不可闭环 | 需独立验证者持密钥 |
| OpenTimestamps 时间锚 | ⚠️ 框架就绪，未上链 | 需联网+外部 CLI |
| 人签身份认证 | ❌ 不可闭环 | git 作者可自设，无第三方 |
| SLSA L2+ | ❌ 不可达 | 需多角色/多环境 |

**结论**：信任根的"完整性"（校验和/Merkle/溯源链）在单用户模型下可闭环；"身份性"（签名/时间戳/多角色验证）在单用户模型下结构性不可闭环。这是 6 维度评分中信任根层封顶 8.5/10 的根本原因。

## 六、待改进项

1. **OpenTimestamps 实际上链**：609 D1 只做了工具框架，未实际上链。建议下批或下下批执行（需联网，违反只读纪律，需人审授权）。
2. **governance high=55 人审**：55 条 high findings 需人审逐条确认是"描述"还是"真实攻击指令"。这是人审权力，永不自动。
3. **运行时规则指纹**：封堵攻击1的"进程内运行时篡改"残余风险。需 W 档（架构改造，当前不做）。
4. **manifest 自身加固**：governance manifest 的 self_hash 是自引用（与 .tool_checksums 同类信任边界）。是否再加固（如 manifest 入 git 签名）由人审裁决。
5. **conftest 钩子纵深防御**：防得住"只改内容不改哈希"，防不住"改钩子+重签基准"。是否改架构（独立 pytest 启动脚本）由人审裁决。

---

*生成时间：2026-09-20 | 生成工具：MainAgent 化债复算 | 数据来源：tools/.tool_checksums / data/supply_chain/ / data/governance_*.json（实跑统计）*
