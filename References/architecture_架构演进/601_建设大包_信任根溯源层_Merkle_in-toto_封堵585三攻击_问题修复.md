# 601 建设大包：信任根溯源层落地 —— Merkle 完整性 + in-toto 风格溯源链 + 585 三攻击封堵 + 已知问题修复

> 你是苦力建设者，不是调研者。任务是把 600 异族深度调研（_arch_v16/）给出的供应链溯源证明施工蓝图落地为可运行的工具和系统，同时修复已知问题。
> 严格按本仓铁律：一任务一 commit + 正反毒样例 + 存量零误伤 + 新收紧 warn 起步 + 护栏不许裸 except Exception + 改 CORE 必须同 commit --update 带 .tool_checksums。
> 做不完停在任务边界，不留半成品。

---

## 前置依赖（必须先核实）

### 600 调研产出（开工先读，不要凭记忆）

- `_arch_v16/00_总览_供应链溯源证明落地路径_封堵585三meta攻击.md`
- `_arch_v16/04_Merkle树与哈希链深度调研.md`
- `_arch_v16/01_in-toto深度调研与本项目落地设计.md`
- `_arch_v16/05_封堵585三个meta攻击的具体方案.md`
- `_arch_v16/07_数据结构与文件格式设计.md`（JSON schema）
- `_arch_v16/08_工具接口设计.md`（CLI 接口设计）
- `_arch_v16/09_与现有系统集成方案.md`
- `_arch_v16/probes/probe_supply_chain.py`（手搓探针，可参考实现，但要按本仓工具规范重写）

### 600 核心结论（先核实再用）

1. **四阶段中性价比最高 = 阶段1 Merkle**（纯库零依赖、探针已验、是后续信任根输入）
2. **结构性上限 = 阶段3 OpenTimestamps**（只证"存在时间"不证"身份"）
3. **最意外发现**：585 攻击3（人签自证）已被 592 的 git 作者绑定部分封堵（旧调研过时）；真盲点是攻击1的"规则/策略定义文件不在 tool_integrity 覆盖内"
4. **最小落地选阶段1 Merkle**：纯库零依赖、可孤立验证、是后续阶段信任根输入；做完直接封堵 585 攻击1 文件级 + 部分攻击2
5. **本包范围**：阶段1 Merkle + 阶段2 in-toto 最小子集 + 问题修复 + 585 攻击封堵验证。阶段3 OpenTimestamps 留到下一包（需要联网，且 600 说有结构性上限）。

### 已知问题（本包必须修复的）

1. **治理台账过期**（fast 唯一串行红）：591 治理台账缺 4 处人新增 References（596/597/PM_六维度/PUSH+grounded 综合），`governance_doc_guard.py verify` 报错。修复：`governance_doc_guard.py update --force`（592 尾批已做过一次，本包再做一次纳入 596-600 新增文档）。
2. **tool_integrity 覆盖范围不足**（600 指出的 585 攻击1 真盲点）：tool_integrity 只钉 5 核心工具 + 2 测试配置，不覆盖规则定义文件（gate_engine.py 内嵌的规则？还是独立文件？先核实）、poison 豁免台账、governance manifest。修复：扩展 CORE_TOOLS 或新增 SUPPLY_CHAIN_TOOLS 覆盖范围。
3. **governance manifest 自身不在校验范围**（600 指出，governance_doc_guard.py line 14-16 自承）：manifest 是信任根的一部分，但自身没有 hash 校验。修复：manifest 入 tool_integrity 覆盖，或 manifest 自校验（hash 写入自身，启动时验证）。
4. **两条 CRLF 假脏**（full_baseline_v4.json、EV-CONC-001.md）：内容 diff 为空，是行尾问题。本包可以选择修复（统一行尾）或继续忽略。如果修复，必须确保不改变内容语义。

---

## 任务 0：开工先量 + 问题修复（commit 1 + commit 2 + commit 3）

### 0.1 开工先量（无 commit）

实跑以下基线，记录数字：
1. `tool_integrity.py --check` → exit 0，5 核心工具一致
2. `tool_integrity.py --check-test-config` → exit 0，2 配置一致
3. `gate_engine.py --check` → 规则数 / 命中数 / block/warn/advice
4. `poison_drill.py` → 通过数 / RULE-COVERAGE / 表观/诚实覆盖率
5. `atom_evidence_replay.py --check` → confirm/refute/infra
6. `governance_doc_guard.py verify` → exit 2（预期，台账过期），记录缺哪些文档
7. `pytest -m "not slow" -n auto` → 记录红测（预期：治理台账 1 红）
8. 手动统计：tool_integrity 当前覆盖的文件列表 / 未覆盖但应该覆盖的文件列表（规则定义、豁免台账、manifest 等）

### 0.2 修复治理台账过期（commit 1）

- 运行 `governance_doc_guard.py update --force`，纳入 596-600 新增文档
- 运行 `governance_doc_guard.py verify` → exit 0
- 运行 `pytest tests/test_governance_doc_guard.py`（如果有）→ exit 0
- commit：`chore: update governance manifest for 596-600 docs`

### 0.3 扩展 tool_integrity 覆盖范围（commit 2）

**先核实**：gate_engine.py 的规则是内嵌在代码里还是独立文件？poison 豁免台账在哪里？governance manifest 在哪里？

根据核实结果，扩展 tool_integrity 覆盖范围：

**方案 A（推荐）**：新增 `SUPPLY_CHAIN_FILES` 列表，与 `CORE_TOOLS` 分开管理
- `SUPPLY_CHAIN_FILES` 包含：
  - 规则定义文件（如果独立存在）
  - poison 豁免台账（`data/poison_exemptions.json` 或类似路径，先核实）
  - governance manifest（`data/governance_docs_manifest.json`）
  - Merkle 根文件（任务 1 产出，`data/supply_chain/merkle_roots.json`）
  - in-toto layout（任务 2 产出，`data/supply_chain/layout.json`）
- `tool_integrity.py --check` 同时校验 CORE_TOOLS + SUPPLY_CHAIN_FILES
- `tool_integrity.py --update` 同时更新两者的基准
- 保留 `--check-core` / `--check-supply-chain` 分项校验（可选）

**方案 B**：直接把这些文件加入 CORE_TOOLS
- 简单但语义不清（这些不是"工具"，是"信任根数据"）

**选方案 A**。

实现要点：
- `SUPPLY_CHAIN_FILES` 列表定义在 tool_integrity.py 顶部，与 CORE_TOOLS 并列
- `compute_checksums()` 支持传入文件列表参数（默认 CORE_TOOLS）
- `--check` 校验 CORE_TOOLS + SUPPLY_CHAIN_FILES（如果文件存在；不存在的文件跳过并警告，不报错——因为任务 1/2 才产出这些文件）
- `--update` 更新两者的基准
- `.tool_checksums` 格式扩展：增加 `supply_chain` 键，与 `core` 并列（如果当前格式是扁平的，改为嵌套格式；保持向后兼容）
- 入口闸门 `enforce()` 仍然只校验 CORE_TOOLS（SUPPLY_CHAIN_FILES 的校验由 supply_chain 模块自己做，避免循环依赖）

**纪律**：
- 改了 tool_integrity.py 必须同 commit `--update` 带新的 .tool_checksums
- 存量零误伤：扩展覆盖范围后，`--check` 必须 exit 0（所有已存在文件的 hash 与基准一致）
- 不许裸 except Exception

测试（tests/test_tool_integrity_supply_chain_601.py）：
- 正例：`--check` 校验 CORE + SUPPLY_CHAIN，exit 0
- 正例：`--update` 更新两者基准，exit 0
- 反例：篡改一个 SUPPLY_CHAIN_FILE → `--check` exit 1，报错指向该文件
- 反例：SUPPLY_CHAIN_FILE 不存在 → `--check` 跳过并警告，不报错（exit 0）
- 兼容：旧格式 .tool_checksums（只有 core）仍然可读
- 可证伪性：检测函数不许裸 except Exception

### 0.4 修复 governance manifest 自校验（commit 3）

- governance manifest（`data/governance_docs_manifest.json`）增加 `self_hash` 字段（manifest 自身内容的 sha256，排除 self_hash 字段本身）
- `governance_doc_guard.py verify` 启动时先校验 self_hash（如果 self_hash 与实际内容不符 → exit 1，报错 "manifest self-hash mismatch"）
- `governance_doc_guard.py update` 更新 manifest 后重新计算 self_hash 并写入
- manifest 入 tool_integrity 的 SUPPLY_CHAIN_FILES（任务 0.3 已做）
- 这是纵深防御：即使 tool_integrity 被绕过，manifest 自校验也能检出篡改

测试（tests/test_governance_self_hash_601.py）：
- 正例：update 后 self_hash 正确，verify exit 0
- 反例：篡改 manifest 内容（不改 self_hash）→ verify exit 1，报错 self-hash mismatch
- 反例：篡改 self_hash → verify exit 1
- 幂等：连续 update 两次，manifest 内容不变（除时间戳外）

---

## 任务 1：Merkle 完整性层（commit 4 + commit 5）

基于 600 调研方向 4 和 597 手搓探针，实现正式的 Merkle 完整性工具。

### 1.1 tools/merkle_integrity.py（commit 4）

**核心功能**：
- `build(directory)` → 构建目录的 Merkle 树（递归遍历所有文件，按路径排序，叶节点 = 文件内容 sha256，内部节点 = 子节点 hash 拼接后 sha256）
- `prove(directory, file_path)` → 生成文件的 Merkle 证明（从叶到根的路径，包含每个层级的兄弟节点 hash 和方向）
- `verify(file_path, proof, root_hash)` → 验证文件在 Merkle 树中（用证明路径重建根 hash，与给定 root_hash 比较）
- `consistency_prove(old_root, new_root, old_size, new_size)` → 生成两个版本的一致性证明（证明新版本包含旧版本的所有内容，append-only 场景）
- `consistency_verify(old_root, new_root, proof, old_size, new_size)` → 验证一致性证明

**CLI 接口**（参考 600 调研 08_工具接口设计.md）：
- `python tools/merkle_integrity.py build <directory> [--output <path>]` → 构建 Merkle 树，输出 root hash 和树信息
- `python tools/merkle_integrity.py prove <directory> <file_path>` → 生成文件的 Merkle 证明（JSON 格式输出）
- `python tools/merkle_integrity.py verify <file_path> <proof_file> <root_hash>` → 验证文件，exit 0/1
- `python tools/merkle_integrity.py stats <directory>` → 输出 Merkle 树统计（文件数、树高、根 hash）
- `python tools/merkle_integrity.py --check` → 自检：验证所有已存储 Merkle 根与当前目录一致

**覆盖目录**（按优先级，先核实目录存在）：
- `atoms/`（原子卡定义）
- `evidence/`（证据卡定义）
- `Examples/`（工件/夹具）
- `Book/`（书籍内容）
- `data/mutation/`（变异基线文件，full_baseline_v*.json）

每个目录一个独立的 Merkle 根（不要全库一个根，因为不同目录的更新频率和敏感度不同）。

**Merkle 根存储**：
- `data/supply_chain/merkle_roots.json`
- 格式：`{ "atoms": { "root": "...", "file_count": N, "tree_height": H, "generated_at": "..." }, "evidence": {...}, ... }`
- `generated_at` 默认 null（与 596 的 generated_at 处理一致：默认 null，打点走 --now，保证幂等）

**纪律**：
- 纯标准库实现（hashlib、json、os、pathlib，不装任何依赖）
- 幂等：同一目录连续 build 两次，root hash 逐字一致（除 generated_at 外）
- 文件排序：按相对路径字典序排序（保证跨平台一致）
- 空目录：root hash = sha256("")（明确定义）
- 大文件：分块读取（避免内存溢出，本项目文件不大，但好习惯）
- 不许裸 except Exception
- 只读构建（build 不修改被覆盖目录的任何文件，只写 merkle_roots.json）

### 1.2 与 tool_integrity 集成 + 回归测试（commit 5）

**集成**：
- `tool_integrity.py --check` 增加 `--check-merkle` 开关（默认开启）：校验所有已存储 Merkle 根与当前目录一致
- 如果 Merkle 根不匹配 → exit 1，报错指向哪个目录的根不匹配
- `tool_integrity.py --update` 增加 `--update-merkle` 开关（默认开启）：重新构建所有 Merkle 根并更新 merkle_roots.json
- merkle_roots.json 入 SUPPLY_CHAIN_FILES（任务 0.3 已做）

**585 攻击1 封堵验证**：
- 用 585 的攻击脚本（或手动模拟）篡改 gate_engine.py 中的规则定义 → Merkle 验证失败（atoms/ 或 evidence/ 或相关目录的根不匹配）
- 注意：如果规则定义内嵌在 gate_engine.py 中（不在 atoms/evidence/ 下），Merkle 树不直接覆盖 gate_engine.py。这种情况下，tool_integrity 的 CORE 校验已经覆盖 gate_engine.py。Merkle 树覆盖的是"规则定义数据文件"（如果独立存在）。
- 先核实规则定义在哪里，再决定 Merkle 树的覆盖范围是否需要调整

**测试**（tests/test_merkle_integrity_601.py）：
- 正例：build 一个目录 → root hash 正确，stats 输出正确
- 正例：prove + verify → 验证通过，exit 0
- 反例：篡改文件后 verify → exit 1，报错 hash mismatch
- 反例：篡改证明路径 → verify exit 1
- 反例：用错误的 root_hash → verify exit 1
- 幂等：连续 build 两次，root hash 逐字一致
- 空目录：build 空目录 → root hash = sha256("")，不崩溃
- 一致性证明：append 一个文件后，consistency_prove + consistency_verify 通过
- 585 攻击回归：篡改 atoms/ 下一个文件 → merkle --check exit 1
- 可证伪性：不许裸 except Exception

---

## 任务 2：in-toto 风格溯源链最小子集（commit 6 + commit 7）

基于 600 调研方向 1，实现 in-toto 的最小子集（不需要完整 in-toto 框架，只实现本项目需要的 link/layout/验证）。

### 2.1 tools/supply_chain.py（commit 6）

**核心概念**（参考 600 调研 01_in-toto 和 07_数据结构）：
- **Step（步骤）**：本项目的一个构建步骤，有名称、functionary（执行者）、materials（输入文件 hash）、products（输出文件 hash）、command（执行命令）、timestamp
- **Link（链接元数据）**：每个 step 执行后生成的记录，包含 step 的所有信息 + 签名（单用户阶段用 git commit hash 替代）
- **Layout（布局）**：定义所有 step 的顺序、依赖关系、授权的 functionary、inspection 检查点
- **Inspection（检查）**：在特定 step 后执行的验证命令（如 tool_integrity --check）

**本项目的构建步骤**（先核实，按实际情况调整）：
1. `card_authoring`：卡面编写（人/苦力，输入：无，输出：atoms/ evidence/ Examples/）
2. `gate_check`：门禁校验（机器，输入：atoms/ evidence/，输出：gate 结果）
3. `replay_verify`：复算验证（机器，输入：atoms/ evidence/ Examples/，输出：replay 结果）
4. `poison_test`：毒样例攻击测试（机器，输入：poison_drill.py + 卡，输出：poison 结果）
5. `mutation_test`：变异攻击测试（机器，输入：卡 + mutation_fuzz.py，输出：mutation 基线）
6. `metrics_collect`：度量采集（机器，输入：所有结果，输出：metrics.jsonl）
7. `human_review`：人审确认（人，输入：候选边/推翻事件，输出：人审记录）

**实现功能**：
- `create_link(step_name, materials, products, command, functionary)` → 生成 link 对象（JSON 格式）
- `write_link(link, output_dir)` → 写入 link 文件（`data/supply_chain/links/<step_name>-<timestamp>.json`）
- `read_link(link_path)` → 读取 link 文件
- `verify_link(link, layout)` → 验证 link（functionary 是否授权、materials/products hash 是否与 layout 期望一致、step 顺序是否正确）
- `create_layout(steps, inspections)` → 生成 layout 对象
- `write_layout(layout, path)` → 写入 layout 文件（`data/supply_chain/layout.json`）
- `verify_layout(layout)` → 验证 layout 自洽（step 名称唯一、依赖关系无环、inspection 引用的 step 存在）
- `run_inspection(inspection)` → 执行 inspection 命令，返回 exit code 和输出

**CLI 接口**：
- `python tools/supply_chain.py link create <step_name> --materials <file1> <file2> --products <file3> --command "<cmd>" --functionary <name>` → 创建并写入 link
- `python tools/supply_chain.py link verify <link_path>` → 验证 link，exit 0/1
- `python tools/supply_chain.py layout init` → 初始化 layout（基于本项目的构建步骤定义）
- `python tools/supply_chain.py layout verify` → 验证 layout 自洽，exit 0/1
- `python tools/supply_chain.py chain verify` → 验证整条链（所有 link 按 layout 顺序验证 + inspection 执行），exit 0/1
- `python tools/supply_chain.py stats` → 输出链统计（step 数、link 数、最后执行时间）

**签名替代**（单用户阶段，无密钥对）：
- link 的 `signature` 字段 = git commit hash（该 link 对应的 commit，如果没有 commit 则为 null）
- layout 的 `signature` 字段 = git commit hash
- 验证时：signature 与当前 git HEAD 比较（如果 link 是在某个 commit 生成的，验证时检查该 commit 是否存在于 git 历史中）
- 这不是真正的签名（git commit hash 可伪造），但提供了"可追溯性"（link 对应哪个 commit 可查）
- 真正的签名留到阶段3（OpenTimestamps）或未来引入密钥对

**纪律**：
- 纯标准库实现
- link 只追加不覆盖（历史可追溯）
- layout 只增不减（删除 step 必须人审显式做且留 git 痕，与 572 的断言计数基线同纪律）
- fail-closed（link 验证失败 → chain verify exit 1，不跳过）
- 不许裸 except Exception
- 不自动产生 link（系统绝不自动记录 step，必须显式调用 link create）

### 2.2 layout 初始化 + 链验证测试（commit 7）

**layout 初始化**：
- 运行 `supply_chain.py layout init`，生成本项目的 layout（基于上述 7 个构建步骤）
- layout 写入 `data/supply_chain/layout.json`
- layout 入 SUPPLY_CHAIN_FILES（任务 0.3 已做）
- `layout verify` → exit 0

**创建示例 link**（用于测试，不是真实构建记录）：
- 在测试沙箱中创建几个示例 link（card_authoring / gate_check / replay_verify）
- 验证链：`chain verify` → exit 0（如果所有 link 合法）
- 篡改一个 link 的 products hash → `chain verify` exit 1

**测试**（tests/test_supply_chain_601.py）：
- 正例：create_link → link 对象格式正确，write_link → 文件存在
- 正例：read_link → 内容与写入一致
- 正例：layout init → layout 自洽，layout verify exit 0
- 正例：合法 link → verify_link exit 0
- 反例：篡改 link 的 products hash → verify_link exit 1
- 反例：未授权的 functionary → verify_link exit 1
- 反例：step 顺序错误（后一个 step 的 materials 依赖前一个 step 的 products，但前一个 step 没有 link）→ chain verify exit 1
- 反例：layout 中有环（A 依赖 B，B 依赖 A）→ layout verify exit 1
- 幂等：layout init 两次，layout 内容不变（除时间戳外）
- 可证伪性：不许裸 except Exception

---

## 任务 3：585 三攻击封堵验证 + 回归测试（commit 8）

基于 600 调研方向 5，用 585 的攻击脚本做回归测试，验证本包的封堵效果。

### 3.1 攻击1：规则供给链攻击

**攻击方式**：进程内把命中最多的规则 check 置空，141→64，77 条 finding 静默消失。

**当前防护**：tool_integrity 的 sha 基准能检出文件篡改，但 gate 不自我调用、--update 重签无需身份。

**本包新增防护**：
- Merkle 树覆盖规则定义文件（如果独立存在）→ 篡改规则定义 → Merkle 根不匹配
- tool_integrity 扩展覆盖 → 篡改规则定义 → tool_integrity --check exit 1
- in-toto layout：card_authoring step 的 products 包含规则定义文件 → 篡改后 link 验证失败
- governance manifest 自校验 → 篡改 manifest → self-hash mismatch

**验证**：
- 手动模拟攻击：在测试沙箱中篡改 gate_engine.py（或规则定义文件）→ 运行 `tool_integrity.py --check` → exit 1
- 运行 `merkle_integrity.py --check` → exit 1（如果规则定义在 Merkle 覆盖目录内）
- 运行 `supply_chain.py chain verify` → exit 1（如果 card_authoring link 的 products hash 不匹配）
- 记录：攻击被哪一层防护检出（可能多层同时检出）

**残余风险**（600 明说）：
- 进程内运行时篡改（不改变文件 hash，只在内存中置空规则）→ Merkle/tool_integrity/in-toto 都无法检出（因为文件没变）
- 这需要运行时规则指纹（如规则执行前校验规则函数的内存 hash），留 W 档（本包不做）
- --update 重签无需身份 → 单用户阶段结构性上限（git 作者可自设），真正解决需要密钥对或 OpenTimestamps

### 3.2 攻击2：毒样例自证攻击

**攻击方式**：覆盖率 covered 是正则在 poison_drill 自己源码里 grep 文本——注入 0 个真载荷、一行注释即谎报覆盖+1；豁免台账自写一条 id 即被原样接受。

**当前防护**：581 已改为行为级 covered（真实 gate 命中规则 ID），但豁免台账仍然是自写自验。

**本包新增防护**：
- 豁免台账入 SUPPLY_CHAIN_FILES → 篡改豁免台账 → tool_integrity --check exit 1
- Merkle 树覆盖 data/ 目录（如果包含豁免台账）→ 篡改后 Merkle 根不匹配
- in-toto layout：poison_test step 的 products 包含豁免台账 → 篡改后 link 验证失败

**验证**：
- 手动模拟攻击：在测试沙箱中篡改 poison 豁免台账（新增一条假豁免）→ 运行 `tool_integrity.py --check` → exit 1
- 运行 `poison_drill.py` → 行为级 covered 不受影响（581 已封堵文本 grep 攻击）
- 记录：攻击被哪一层防护检出

**残余风险**：
- 行为级 covered 依赖 gate 真实运行，如果 gate 本身被攻击1 攻破（进程内存篡改），covered 也会被欺骗
- 这是纵深防御的意义：多层防护，攻破一层不代表攻破全部

### 3.3 攻击3：人签文本自证攻击

**攻击方式**：直接键入 `human:liaoranran` 即 principal_ok=True。

**当前防护**（600 纠正旧调研）：592 已做 git 作者绑定（overturned_events.py 的 human 推翻者须过 git 作者绑定，冒名/缺字段/卡解析不到拒写，fail-closed）。

**本包新增防护**：
- in-toto layout：human_review step 的 functionary 必须在 layout 中授权（git 作者名）
- 人审记录入 Merkle 树（如果人审记录在 data/ 下）→ 篡改后 Merkle 根不匹配
- 人审记录的 link 包含 git commit hash → 可追溯

**验证**：
- 手动模拟攻击：用错误的 git 作者名尝试人审 → `attack_edge_review.py` 拒绝写入（596 已实现 git 作者绑定）
- 篡改已有的人审记录 → Merkle 根不匹配（如果人审记录在 Merkle 覆盖目录内）
- 记录：攻击被哪一层防护检出

**残余风险**（600 明说）：
- git 作者可自设（`git config user.name "liaoranran"`）→ 单用户阶段结构性上限
- OpenTimestamps 只证"存在时间"不证"身份" → 无法解决身份认证
- 真正解决需要密钥对（GPG/SSH key）或第三方身份认证，留到未来

### 3.4 回归测试文件

创建 `tests/test_585_attack_regression_601.py`，包含：
- 攻击1 回归：篡改规则定义文件 → tool_integrity/merkle/supply_chain 至少一层检出
- 攻击2 回归：篡改豁免台账 → tool_integrity/merkle 至少一层检出
- 攻击3 回归：错误 git 作者 → attack_edge_review 拒绝写入
- 纵深防御验证：同时篡改多个文件 → 多层防护同时检出
- 残余风险声明：在测试文件注释中明说哪些攻击在单用户阶段无法完全封堵（进程内存篡改、git 作者自设）

---

## 任务 4：收工总验收（无 commit，纯验收）

按以下清单逐项验收，全部用退出码定论（$LASTEXITCODE）：

1. `tool_integrity.py --check` → exit 0（CORE + SUPPLY_CHAIN 全一致）
2. `tool_integrity.py --check-test-config` → exit 0
3. `tool_integrity.py --check-merkle` → exit 0（所有 Merkle 根与当前目录一致）
4. `gate_engine.py --check` → exit 0，规则数/命中数/block/warn/advice 与任务 0 基线逐字相同
5. `poison_drill.py` → exit 0，通过数/RULE-COVERAGE/表观/诚实覆盖率与基线逐字相同
6. `atom_evidence_replay.py --check` → exit 0，confirm/refute/infra 与基线逐字相同
7. `governance_doc_guard.py verify` → exit 0（台账已更新）
8. `merkle_integrity.py --check` → exit 0
9. `merkle_integrity.py stats` → exit 0，输出各目录的 root hash/file_count/tree_height
10. `supply_chain.py layout verify` → exit 0
11. `supply_chain.py stats` → exit 0
12. `attack_edge_generator.py stats` → exit 0（596 工具，确认未受影响）
13. `weighted_af_solver.py stats` → exit 0（596 工具，确认未受影响）
14. `pytest -m "not slow" -n auto` → exit 0（含本批新增测试，治理台账红已修复）
15. `pytest -m slow -n0` → exit 1，唯一红 = test_golden_lock_json（预期红）
16. `ruff check`（本批全部新增/改动 .py）→ All checks passed
17. `git diff --quiet -- atoms evidence Examples Book` → exit 0（受控目录零污染）
18. `git status --short` → 仅本批文件（+ 两条 CRLF 假脏，如果选择不修复）

---

## 明确不做（任务书边界）

- **阶段3 OpenTimestamps**：需要联网 + 外部 CLI，600 说有结构性上限（只证存在时间不证身份），留到下一包
- **运行时规则指纹**：封堵 585 攻击1 的"进程内存篡改"残余风险，需要运行时校验规则函数内存 hash，留 W 档
- **密钥对/真正签名**：单用户阶段结构性上限，留到未来
- **SLSA L2+**：单用户阶段不可达（需要托管构建服务），本包只做"L1 等价物"
- **修改 gate_engine.py / atom_evidence_replay.py / poison_drill.py / toolchain.py / cppbible.py 的核心逻辑**：只扩展 tool_integrity 的覆盖范围，不改 CORE 工具的核心逻辑
- **不 push / 不 golden accept / 不替人签**

---

## 偏差表模板（写进 _worklog_601.md §6）

| # | 任务书假设 | 实测 | 处理 |
|---|---|---|---|
| D1 | 规则定义独立存在 | （实跑结果：内嵌在 gate_engine.py 还是独立文件？） | 按实测调整 Merkle 覆盖范围 |
| D2 | poison 豁免台账路径 | （实跑结果） | 按实测路径加入 SUPPLY_CHAIN_FILES |
| D3 | 治理台账缺 4 处 | （实跑结果，可能更多） | 按实测 update |
| D4 | Merkle 覆盖 5 个目录 | （实跑结果，某些目录可能不存在或为空） | 按实测调整 |
| D5 | in-toto 7 个构建步骤 | （实跑结果，某些步骤可能不适用或需要合并） | 按实测调整 layout |
| D6 | 585 攻击脚本可复现 | （实跑结果，可能需要手动模拟） | 按实测做回归测试 |
| ... | ... | ... | ... |

---

## 过程文档

- `_worklog_601.md`：按惯例不入库，含任务 0 基线 / 各任务实跑数字 / §6 偏差表 / §7 收工验收 / 交人项 / 585 攻击封堵效果矩阵
- 每个任务一个 commit，message 里写明任务编号和一句话结果
- 改了 tool_integrity.py / governance_doc_guard.py / conftest.py 必须同 commit --update 带新的 .tool_checksums
- 585 攻击封堵效果矩阵：每个攻击被哪一层防护检出、残余风险是什么、单用户结构性上限是什么
