# 625 D1 · 尺子入根 22 → 34（完整性根覆盖扩展）

> 工具：`tools/tool_integrity.py`（`RULER_TOOLS` 元组扩展）+ 同 commit `tool_integrity.py --update` 重钉
> 目标：判决尺子入根 **22 → >30**；铁律：扩展 `RULER_TOOLS` 后必重钉

---

## 一、入根覆盖口径

`tool_integrity.py` 哈希面由四节构成（每节独立 compute/verify，互不混）：

| 节 | 数量 | 内容 |
|---|---|---|
| `core` | 5 | gate_engine / atom_evidence_replay / poison_drill / toolchain / cppbible |
| `test_config` | 2 | tests/conftest.py / pyproject.toml |
| `supply_chain` | 5 | 毒样例豁免台账 / 覆盖率台账 / 治理 manifest / Merkle 根 / in-toto layout |
| `ruler` | 22（**原 10 → 现 22**） | 判决尺子 |
| **合计** | **34** | **>30 ✅** |

## 二、本轮新增的 12 个尺子（均为「改一行即可改『什么算通过』」）

| 工具 | 决定什么 |
|---|---|
| `weighted_af_solver.py` | W2 论证图判决（IN/OUT/UNRESOLVED） |
| `debt_ledger.py` | 技术债务台账（债务是否红） |
| `governance_doc_guard.py` | 治理文档 manifest 校验（治理漂移） |
| `human_review_queue.py` | 人审队列（哪些需人审、如何汇总） |
| `exemption_expiry.py` | 豁免到期判定（过期仍在用即漂移） |
| `metrics_collector.py` | 指标聚合（度量是否失真） |
| `merkle_integrity.py` | 供应链 Merkle 完整性校验 |
| `supply_chain.py` | 供应链信任链校验 |
| `authority_to_annotations_sync_623.py` | Authority↔annotations 通道（W2 输入源） |
| `escape_rate_honest_613.py` | 逃逸率诚实口径计算 |
| `pck_certificate_verifier_619.py` | PCK 证书校验（PCK 是否可信） |
| `defense_chain.py` | 防御链判定 |

## 三、验证

| 项 | 结果 |
|---|---|
| `tool_integrity.py --update` 重钉 | ✅ core 5 + test_config 2 + supply_chain 5 + ruler 22 = 34 |
| `tool_integrity.py --check` | ✅ Merkle 根一致（警告 0），判决尺子 22/22 一致 |
| 新增 12 工具均存在且可被哈希 | ✅ |
| `CORE_TOOLS` 未变（铁律：不改核心逻辑） | ✅ |

## 四、局限性声明

1. 入根只覆盖**文件级哈希**；运行期参数/环境变量篡改仍不在面内（需运行时 attestation，留 626）。
2. 仍未覆盖`tools/` 全部 ~130 工具——仅把**最具判决权**的尺子钉入，避免哈希面过度膨胀。
3. `authority_to_annotations_sync_623.py` 等工具含 `--no-write` 守卫，入根进一步防「静默改尺子」。
