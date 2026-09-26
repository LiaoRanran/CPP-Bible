# 647 A3 · 信任根闭包扩展（641 的 23 文件 → 全覆盖）

- 状态：**OK** · 闭包文件 **33** 个（含规则集指纹）· 缺失 **0**
- 规则数：**67**；规则集指纹：`12e91476efb4a6ea40a13d908b35c5f8dd3b92c58aa96b56e55272443fdcbceb`
- closure_digest（647 版）：`d954d10a0bdfdbe4ccf35676d3a61f8b4b5eb17e3b4d1847c0d89065ea35dd38`
- 与 tool_integrity 一致：**True**（CORE_TOOLS 覆盖 5/5，信任根数据 5 个已钉）

## 一、相比 641 新增覆盖的面

| 面 | 载体 | 为什么必须进闭包 |
|---|---|---|
| 67 条规则 | `gate_engine.py` + **规则集指纹** | 规则内嵌，改规则=改判决 |
| Authority schema | `authority_schema_v2_626.py` / `decision_event_v2_626.py` | 决定「一条人审是否算数」 |
| 透明日志 anchor | `data/transparency_log.jsonl` | 改了它 = 改「历史是否可证」 |
| 基线自身 | `tools/.tool_checksums` | 「什么算被改过」的定义 |
| 证据库索引 | `data/evidence_index.json` | 证据检索面 |
| block 规则 yaml | `data/gate_rules_high_complexity_block_623.yaml` | 623 E2 的 4 条独立 block 规则 |

## 二、缺失即 FAIL（不是 warning）

```
attack（假装缺 ['tools/gate_engine.py', 'tools/poison_exemptions.yaml']） ⇒ status=FAIL
missing=['tools/gate_engine.py', 'tools/poison_exemptions.yaml']
digest 改变：True
```

**不真删任何文件**：`missing` 只是「假装磁盘上没有」，用于证明判定会 FAIL。

## 三、与 tool_integrity 一致性（交叉校验）

- ✅ 闭包内 5 个 CORE_TOOLS + 5 个信任根数据文件的 sha256 **与 `.tool_checksums` 逐字相同**。

## 四、闭包清单（每个文件的 sha256）

| # | 文件 | sha256（前 16） |
|---|---|---|
| 1 | `RULESET#gate_engine` | `12e91476efb4a6ea…` |
| 2 | `data/evidence_index.json` | `e98fda57a29c868f…` |
| 3 | `data/gate_rules_high_complexity_block_623.yaml` | `568d771c65faaf16…` |
| 4 | `data/governance_docs_manifest.json` | `ff213a117bb9578e…` |
| 5 | `data/supply_chain/layout.json` | `fba147aa6e05e4bf…` |
| 6 | `data/supply_chain/link_613_verify.json` | `a2b4b0d3bc01ee4f…` |
| 7 | `data/supply_chain/merkle_roots.json` | `d155486902d44a07…` |
| 8 | `data/supply_chain/merkle_roots.json.ots` | `1d42d22c216916c5…` |
| 9 | `data/transparency_log.jsonl` | `03d8282163636414…` |
| 10 | `pyproject.toml` | `0da4cc8200450a9e…` |
| 11 | `tools/.tool_checksums` | `f464a6a44fd77729…` |
| 12 | `tools/atom_coverage_map.py` | `4eeec0fd3723820c…` |
| 13 | `tools/atom_evidence_replay.py` | `4b142e68a97a3c2b…` |
| 14 | `tools/authority_schema_v2_626.py` | `2bf6677ef02c61da…` |
| 15 | `tools/backup.py` | `99a7331406c153cc…` |
| 16 | `tools/comment_blocks.py` | `06b4a53abb7c17b3…` |
| 17 | `tools/cppbible.py` | `4454db9b499238dc…` |
| 18 | `tools/decision_event_v2_626.py` | `539940d6e4bd0397…` |
| 19 | `tools/gate_engine.py` | `03cd20dcdbeee512…` |
| 20 | `tools/merkle_integrity.py` | `6cd166591c36a12f…` |
| 21 | `tools/observability.py` | `85f802a0fd4ce34d…` |
| 22 | `tools/path_config_625.py` | `08260a3553fdad4a…` |
| 23 | `tools/poison_drill.py` | `37f638004c4dbdcb…` |
| 24 | `tools/poison_exemptions.yaml` | `dd2ff437da53c73d…` |
| 25 | `tools/poison_surface_map.json` | `de4a8e771edd0592…` |
| 26 | `tools/queyi_core_cpp_641.py` | `9c61fa63a1a4431b…` |
| 27 | `tools/queyi_core_toy_641.py` | `9f4f85a82dcc71af…` |
| 28 | `tools/queyi_core_v10_641.py` | `6a01a1f38425ebd9…` |
| 29 | `tools/tool_integrity.py` | `00a4dda865b228ab…` |
| 30 | `tools/toolchain.py` | `5920bff6af16cb80…` |
| 31 | `tools/utf8_console.py` | `80ad23a16cbc89e8…` |
| 32 | `tools/verifier_closure_641.py` | `b4277a466214bfd7…` |
| 33 | `tools/viso_diff.py` | `b08fb3e43302cad1…` |

## 诚实登记

1. **闭包仍跟不到 site-packages**：第三方依赖以 `pyproject.toml` 声明进闭包，不递归进依赖树（同 641 口径）；
2. **规则集指纹只覆盖规则 id**：规则**正文**改动由 `gate_engine.py` 的 sha256 覆盖，两者必须一起看（id 不变、正文变 ⇒ 只有 gate_engine 的 sha256 会变）；
3. **未修改 `verifier_closure_641.py`**：641 的 digest 已绑进历史 run，改它会让历史对不上 ⇒ 647 以**新文件**扩展（代价：两个闭包并存，交人裁决是否收编）；
4. **闭包的「完整性」仍是相对的**：本机信任根未外移（外部 KMS/第三方签名留 A4 + 交人）。
