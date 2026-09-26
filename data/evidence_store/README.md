# data/evidence_store/ — 头部层内容寻址证据库

**性质**：644 头部层（元系统向外求索）独立产出的证据库，**与尾端 `evidence/` 解耦**。

## 寻址规则（§四.C1 / §九.2）

- `EvidenceID = SHA256(canonical evidence content)`（见 `tools/evidence_base_644.py`）。
- 存储路径：`<EvidenceID 前 2 位>/<EvidenceID>`（即 `data/evidence_store/<hh>/<hash>`）。
- 每条记录为 JSON：`{evidence_id, content, source_type, grade, credibility, acquired_at, acquisition_method, source_url, meta}`。
- **不可变**：写入后不修改；新证据 = 新 EvidenceID。重复写入（同内容）幂等返回既有记录。

## 铁律

1. 本目录**只读式增长**；头部层只获取/保存证据，**不修改**原子卡（`atoms/`）、尾端证据（`evidence/`）。
2. 外部获取的证据必须可追溯：来源 URL / 时间戳 / 获取方式 / 原始内容 hash（即 `EvidenceID`）。
3. 网络获取失败只标记「获取失败」，不崩溃（降级方案，§零.8）。
4. 证据与卡片的多对多关联记录在 `data/evidence_index.json`（独立索引，不碰卡片 YAML）。

## 与 `evidence/` 的区别

| 维度 | `evidence/`（尾端） | `evidence_store/`（头部层） |
|---|---|---|
| 来源 | 人工/AI 已验证实验 | 头部层主动向外获取的候选证据 |
| 等级 | 已在卡上判定 | 由 B1 启发式分级（未人审） |
| 关联 | `serves:` 字段在证据文件内 | `evidence_index.json` 独立索引 |
| 是否进生产判决 | 是 | 否（需人审后才关联，§九.6） |
