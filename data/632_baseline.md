# 632 基线台账

## §一 Standing Baseline

| 指标 | 值 |
| gate 规则数 | 67 |
| gate 命中 | 191（block=0 warn=186 advice=5） |
| poison | 124/124 |
| replay | confirm=56 refute=0 infra=0 |
| tool_integrity | 22 尺子 |
| W2 | IN114/OUT7/UNDEC0 |
| PCK | 83 张，authorized 27/83 |
| Authority V2 ledger | 452 条 |
| 透明日志 | data/transparency_log.jsonl |
| 触达规则 | 37/67 |
| 逃逸率 | 1/1406（CS 0.9062%） |
| 自身免疫率 | 100%（warn 92，human 90 待填） |
| coverage | 51.4%（18/35） |
| CI pytest | ❌ 5 项红（环境依赖 4 + UTF-16 1） |
| HEAD | 04088899 |
| 远程 | 1438cd5e（落后 31） |
| 雷1 触发标准 | 3/5（路径解耦✅ v0.1✅ v0.2✅ 治理裁定⛔ 余量⛔） |

## 额外测量（任务0.2）

- 代理 7990 端口：`DOWN`
- `data/vsa/vsa_secret.key` 存在：`False`
- CI pytest 剩余 5 项（来源：data/ci_pytest_final_631.md）：
  - `test_ci_pytest_fix_625.py::test_governance_manifest_verified`
  - `test_governance_doc_guard_591.py::test_verify_real_manifest_matches`
  - `test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash`
  - `test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch`
  - `test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections`
