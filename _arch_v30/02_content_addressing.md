# 02 · 内容寻址与证据保存调研（644 阶段 A · A2）

> 任务：调研 Git 对象模型 / IPFS / DOI·arXiv / in-toto·SLSA，≥5 个，含对阙疑的设计建议。

## 一、五个参照体系

### 1. Git 对象模型（blob/tree/commit）
- **blob = SHA1(内容)**，内容寻址、不可变；相同内容永远同一对象。
- tree 把名字映射到 blob hash；commit 指向 tree + 父 commit。
- **启发**：证据库 = 一堆 blob；索引（证据-卡片关联）= tree；不可变保证天然成立。阙疑用 SHA256（更强）替代 SHA1。

### 2. IPFS / content-addressed storage (CAS)
- `CID = multihash(content)`；相同内容全球同一地址；去重天然。
- **启发**：阙疑 `EvidenceID = SHA256(content)` 正是 CAS 思路；`data/evidence_store/<hh>/<hash>` 是简化版 IPFS 布局。

### 3. 学术引用：DOI / arXiv ID
- DOI 是「持久标识符」但**指向可变资源**（出版商页面可改）；arXiv ID 指向不可变快照（版本号 vN）。
- **启发**：阙疑的 `EvidenceID` 是内容 hash（不可变快照），比 DOI 更稳；但需另存 `source_url`（DOI 式可解析指针）以溯源。两者互补。

### 4. 软件供应链 provenance：in-toto / SLSA
- in-toto：用签名链接记录「每一步谁、用什么、产生什么 hash」，形成溯源链。
- SLSA：build level 1–3，强调「构建出处可验证」。
- **启发**：阙疑每条证据已有 `acquired_at`/`acquisition_method`/`source_url`；应像 in-toto 一样把「获取动作」也记录进 meta，使「这条证据怎么来的」可审计。

### 5. 防篡改日志 / 透明日志（Certificate Transparency）
- 仅追加（append-only）+ Merkle 树，任何改写可被检测。
- **启发**：证据库本身是 CAS（追加写、不改既有），天然满足「不可变」；但若要做「证据被删/被改」检测，可复用现有 `transparency_log`（629 已建）。

## 二、对阙疑的设计建议

1. **EvidenceID 用 SHA256(content)**：已落地（`evidence_base_644.sha256_text`）。内容含「原始文本 + 关键元数据」以保证同源同 hash。
2. **目录布局 `<hh>/<hash>`**：避免单目录百万文件；已落地。
3. **不可变 + 新证据=新 ID**：已有 `store_evidence` 幂等/冲突检测；写入后永不改。
4. **溯源三元组**：`source_url` + `acquired_at` + `acquisition_method` 必填（对应铁律 §零.5）。
5. **关联索引独立**：证据-卡片多对多用 `data/evidence_index.json`，不碰卡片 YAML（铁律 §九.1）。

## 三、落到 644 阶段 C 的设计输入

1. **C1 `evidence_store_644.py`**：直接复用 `evidence_base_644.store_evidence/load_evidence/iter_stored`。
2. **C2 `evidence_card_link_644.py`**：维护 `evidence_index.json`（多对多 + 关系类型：support/refute/background）。
3. **C3 `evidence_integrity_644.py`**：hash 一致性 + 来源 url 重取对比（借鉴 DOI 可变、CID 不可变的张力）。
4. **C4 `evidence_migration_644.py`**：把现有 `evidence/` 文件关键字段迁入 store（只读迁移，不改原文件）。

> 结论已落到 C1–C4（见 `tools/evidence_*.py`）。
