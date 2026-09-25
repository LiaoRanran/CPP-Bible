# 628 开工基线台账

- **日期**：2026-09-23 · **基线 HEAD**：`b913b0fe`（627 E1）· 627 已完成 13/13
- **status.json**：state=awaiting_review · last_completed_batch=627 · next_batch=628 ✅

## 一、4 项技术债精确定位

### 债1 · QUEYI_AUTHORITY_V2 flag 未真接入（A1）
- **位置**：`tools/authority_projection_compiler_626.py`
  - L40：`ENV_FLAG = "QUEYI_AUTHORITY_V2"`
  - L46-47：`v2_enabled()` 已定义（`os.environ.get(ENV_FLAG,"0")=="1"`），**全文件无任何调用点**
  - L55-61 `AuthorityProjectionCompiler.__init__`：无条件读 v2 ledger
  - L93-113 `compile_w2()`：无条件 ledger edge_id 粒度投影（519 节点），无 flag 分支
- **影响**：V2 是"概念开关"非"生产开关"；flag=0/1 行为完全相同
- **修复方案**：`__init__` 读取 flag 存 `self.v2_mode`；`compile_w2()` 分支——V1（=0/未设置）读 legacy `grounded_labels_w2.json`（121 节点，625 行为）；V2（=1）走 627 A1 归一化路径（ledger→APPROVE∪MODIFY→weighted_af_solver，121 节点）。输出 schema 不变（dict[str,str] node→label）
- **风险**：626 测试 `test_w2_projection_vs_grounded_labels_deviation_registered` 锁定 `len(w2)!=121`（偏差存在）——A1 落地后偏差**被解决**，该测试必须同 commit 更新为对齐断言（报告偏差项登记）
- **修改后必跑**：`tool_integrity.py --update` 重钉 .tool_checksums

### 债2 · PCK hash 83 张缺口（A2）
- **位置**：证书 `data/pck/certificates/*.pck.yaml`（83 张）；缺口分类 `data/pck_hash_drift_627.json`（certs 数组含 per-cert per-ref category）
- **结构**：evidence 条目形如 `{"type":"replay","ref":"evidence/conc/EV-CONC-001.md"}`——hash_absent=无 hash 字段；content_drift=hash 与当前文件不符
- **分布**：content_drift 56 + hash_absent 26 + ref_missing 1 = 83
- **修复方案**：content_drift→重算 SHA256 更新；hash_absent→补 hash；ref_missing→**不自动修**，标 `hash_status: ref_missing_needs_human`；**只动 hash 字段，不碰 verdict/authorized/status 等语义字段；不判任何证书失效**；先备份到 `data/pck_backup_628/`

### 债3 · 镜像边 symmetry_proof_id 全空（A3）
- **位置**：`data/review_item_ledger.jsonl`（93 条，`symmetry_proof_id` 字段全 ""，626 B3 预留）；镜像候选 `data/attack_edges_candidates.jsonl`（mis_to_prop 194 + prop_to_mis 194 成对）；627 验证报告 `data/mirror_edge_symmetry_627.json`
- **修复方案**：对每条镜像边验证三条件（正反向都存在 / decision 一致 / reason 关键词重叠≥0.6）→ 全满足生成 `sym-proof-<sha256-of-pair-ids>` 写入 ledger 对应条目；不满足标 `symmetry_unverified` 留人审；**写入后验证 W2 分布不变（IN114/OUT7/UNDEC0）**；写前备份

### 债4 · DEBT-001 到期 + replay manifest（A4）
- **DEBT-001**：`tests/test_s1_s6.py` L181-183——fixture 硬编码 `"due": "2026-09-20"` 已过期（今日 2026-09-23）⇒ `test_clean_ledger_passes` FAILED（"DEBT-001 已到期未清——停线"）。**实测确认仍红**
- **修复方案**：fixture 日期动态化（opened=今天-N / due=今天+M），测试测的是台账逻辑而非硬编码日期；真实治理台账无 DEBT-001 数据文件（仅测试 fixture）⇒ 处置记录说明"fixture 动态化即等效清算"
- **replay manifest_consistency**：`build/replay_manifest.json`（56 条，含 fingerprint/verdict/ts；fingerprint=sha256(卡‖夹具‖工件‖.out‖阴夹具)，`atom_evidence_replay.py:2242`）。**625 登记的 5 失配（EV-CONC-002..006）已不复现**——只读复验 `replay_invariants.py --check --invariant manifest_consistency` = **56 cards, 0 mismatches, CONSISTENT**（626/627 期间 manifest 已刷新 ts=2026-09-22T21:49:33）。628 只做只读验证 + 记录，无需修

## 二、6 项交人项分类（627 → 628）

| # | 交人项 | 628 处置 |
|---|---|---|
| 1 | flag 启用裁决 | **628 A1 把 flag 真接入**；是否默认开启仍需人（默认保持 V1，硬边界 13） |
| 2 | 真实 Blind Review 执行 | **必须人**（铁律 7，本批不执行） |
| 3 | push 裁决 | **必须人**（铁律 2，本批不 push） |
| 4 | 56 PCK hash 处置 | **A2 机械重算**（56 重算 + 26 补 + 1 需人审；不判失效） |
| 5 | 镜像边人工验证 | **A3 自动证明机械部分**；语义不等价/decision 不一致者留人审 |
| 6 | DEBT-001 到期 | **A4 清算**（fixture 动态化 + 处置记录） |

## 三、V2 flag 接入前基线快照（V1 模式 = 625 行为）

- W2（grounded_labels_w2.json）：**121 节点，IN 114 / OUT 7 / UNDEC 0**
- 当前 626 编译器 compile_w2（ledger edge 粒度）：519 节点（接入后 V1 改读 grounded_labels ⇒ 121）
- PCK：83 张；四层验证 B2-S 83/83、B2-R 27/83（hash 缺口所致）、authorized 27/83=32.5%
- DecisionEvent v2 ledger：452 条；唯一审查账本 93 unique；独立人审强度 **0**
- W2 归一化（627）：APPROVE∪MODIFY 为生效攻击 + weighted_af_solver → IN114/OUT7/UNDEC0 diff=0

## 四、他验三件套建设起点评估

| 组件 | 可复用 | 需新建（628） |
|---|---|---|
| 独立验证者 | 数据文件齐备：`decision_event_v2_ledger.jsonl`(452)、`grounded_labels_w2.json`(121)、annotations(388)、83 PCK | `independent_verifier_628.py`——**零 import 本项目工具**，纯标准库，朴素 W2 求解器 + ledger 哈希链复算（公式：sha256(f"{prev_hash}\|{payload}")，payload=事件 dict 去 self_hash/event_id 后 sort_keys json）+ PCK 计数 + unique 去重 |
| VSA 凭证 | HMAC 基础概念已有（613/625 用过 HMAC） | `vsa_attestation_628.py` + `vsa_verify_628.py`（密钥 `data/vsa_secret.key` **入 .gitignore**） |
| 透明日志 | Merkle/OTS 工具存在但**不复用不 import**（保持独立） | `transparency_log_628.py`——简单哈希链 append-only jsonl |
| 端到端 | B1/B2/B3 就绪后 | `third_party_audit_demo_628.py` 串联 |

## 五、验证

- 任务0 只读：未修改任何工具/数据/受控目录 ✅
- 627 commit 链确认：`f4b19c65..b913b0fe`（12 commit）✅
- DEBT-001 现状实测：`test_clean_ledger_passes` FAILED（fixture 日期过期）✅
- manifest_consistency 只读复验：0 mismatches ✅


## 边界三元组 + v26 补充字段（635 1.1 回填）

- `mutation_set_hash`: `d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57`
- `mutation_count`: 1593
- `generator_version`: `mutation_fuzz@v7`
- `evidence_channel`: `standard_textbook`
- `materiality_flag`: true


## 635 V26-2 系统误差二分（不可合并为单一健康分）

**可收敛指标**（加样本可改善）：
- 逃逸率：多测 mutation 可更准确估计漏报率（统计量）
- τ_d（逃逸→修补间隔）：样本量增加可收紧分位数
- 接地覆盖率：可补实验把「部分/未接地」转「已接地」
- 工具数/测试数：持续增加

**不可收敛指标**（加样本无效，须换方法）：
- coverage 缺口：剩下的是**没测过的攻击面**，不是测不准
- 自身免疫率：是**规则设计问题**，不是样本问题
- Horizon 断崖（60-80 桶）：是**载体天花板**，不是样本量
- N/A 率：主因是载体无法施加（634 B3），加样本无效
- gate 规则数：是**设计选择**，非估计量
