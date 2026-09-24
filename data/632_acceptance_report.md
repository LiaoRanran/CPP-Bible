# 632 验收报告（H1 · 收工门禁）

- 总体结论：**通过 ✅**
- 工具 `--check` 自检：12/12 通过
- 测试套件：exit=0
- 产物缺失：无

## 一、各工具 `--check` 结果

| 工具 | 结果 | 说明 |
|---|---|---|
| `baseline_632` | ✅ | 632 任务0 --check OK：CI剩余 5 项，代理 DOWN，vsa_secret.key 不存在 |
| `transparency_anchor_632` | ✅ | 632 B1 --check: OK 锚与日志一致 |
| `transparency_verify_632` | ✅ | 632 B2 --check OK：37 条链自洽，锚一致 |
| `autoimmune_human_fill_helper_632` | ✅ |   样例 atoms/conc/ATOM-CONC-LOCK-001.md:24 [object] 候选=（无候选：须人裁决 → 改 object / 改 claim_type / 补概 | ATOM-CLAIM-CONCEPT-NORMA |
| `autoimmune_human_fill_apply_632` | ✅ | 632 C2 --check OK：待执行决策 0 条 |
| `pollution_guard_session_632` | ✅ | 632 D1 --check OK：PollutionGuard 可用（受控目录 atoms, evidence, Examples, Book） |
| `sandbox_apply_622` | ✅ | A1 selftest: PASS |
| `coverage_probe_l2_3_632` | ✅ |   [ok] 报告路径在 data 下（--check 不写） |
| `coverage_probe_l4_2_632` | ✅ |   [ok] 报告路径在 data 下（--check 不写） |
| `coverage_probe_l4_4_632` | ✅ |   [ok] 报告路径在 data 下（--check 不写） |
| `queyi_core_interface_v03_632` | ✅ |   [ok] 报告路径在 data 下（--check 不写） |
| `ci_pytest_final_clear_632` | ✅ | 本地残留目录存在：True |

## 二、产物齐备性

| 产物 | 存在 |
|---|---|
| `data/third_party_audit_demo_632.md` | ✅ |
| `data/vsa_key_security_audit_632.md` | ✅ |
| `data/vsa/anchor_20260924.json` | ✅ |
| `data/coverage_probe_l2_3_632.md` | ✅ |
| `data/coverage_probe_l2_3_632.json` | ✅ |
| `data/coverage_probe_l4_2_632.md` | ✅ |
| `data/coverage_probe_l4_2_632.json` | ✅ |
| `data/coverage_probe_l4_4_632.md` | ✅ |
| `data/coverage_probe_l4_4_632.json` | ✅ |
| `data/coverage_e1_632.md` | ✅ |
| `data/queyi_core_interface_v03_632.md` | ✅ |
| `data/queyi_core_interface_v03_632.json` | ✅ |

## 三、诚实登记

1. 本门禁只校验**本批 632 交付物**（工具 `--check` + pytest + 产物存在性），不替历史批次背锅；
2. 测试套件含 D1/D2 等对真实仓库只读扫描的用例，均不带 `--lf` 跳过，失败即如实暴露；
3. 工具 `--check` 均为只读自检（exit 0 不写盘）；门禁本身亦遵守此约定；
4. 任何一项非零 ⇒ 门禁 exit 1，禁止声称收工；
5. `baseline_632 --check` 仍报「vsa_secret.key 不存在」——其探针指向`data/vsa/vsa_secret.key`（错误路径）；真实密钥在 `data/vsa_secret.key`（**G1 审计已确证存在**）。该探针偏差见 G1 §三，属已知监控缺口；本门禁如实转录 baseline 的输出，未篡改，亦不与之矛盾（G1 为权威结论）。
