# 629 E2 · CI 四 job 状态检查（`needs: [replay]` 在位确认）

> 生成：2026-09-23 · 工具：只读审计 `.github/workflows/ci.yml`（**不执行 CI**）
> 任务书口径：「gate / quality / replay / concurrency-safety 四 job + `needs: [replay]` 是否在位」

## 一、四个目标 job

| job | 行号 | `needs:` | 关键命令 | 结论 |
|---|---|---|---|---|
| `quality` | `:19` | **`needs: [replay]`（`:26`）** | ruff / mypy / 约 35 步治理与清单类检查 | ✅ 依赖在位 |
| `concurrency-safety` | `:384` | 无 | `tools/ci_concurrency_check_621.py`（`:402`） | ✅ 不需要 replay（不读受控目录） |
| `pytest` | `:408` | 无 | `pytest tests/ -m "not slow" -n 16 --maxfail=1` + `-m slow -n0` | ⚠️ 无 replay 依赖（读受控目录但只读；见 E1 风险） |
| `replay` | `:446` | 无 | `atom_evidence_replay.py --check --incremental`（tools/ 变更则 `--rebuild-manifest`，`:472-478`） | ✅ 写者先跑 |
| `gate` | `:487` | **`needs: [replay]`（`:496`）** | `gate_engine.py --check` + `golden_lock/debt_ledger/poison_drill`（`:518-527`） | ✅ 依赖在位 |

**「`needs: [replay]` 是否在位」= 是，且两处**（`quality:26`、`gate:496`）——方向统一为
「写者 replay 先、读者 gate/quality 后」，这是 622 B2 竞态修复的核心机制，629 未改动它。

## 二、下游 job（顺带审计）

| job | `needs:` | 说明 |
|---|---|---|
| `compile` | `[quality, pytest, replay, gate]`（`:534`） | 依赖四门，任一红即 skipped |
| `publish-check` | `[quality, pytest, replay, gate]`（`:703`） | 同上 |
| `site` / `pdf` / `epub` | `[compile, publish-check]` | 再下游 |
| `deploy` | `[site, pdf, epub]` | 末端 |

## 三、push 后的预期结果（基于 E1 的风险评估）

```
replay            ✅ 绿（629 未改受控目录）
concurrency-safety✅ 绿（未改 ci.yml / 并发工具）
gate              ⚠️ 未知（监工域，本地禁跑；628 监工时 block=0）
quality           ⚠️ 中风险（本地 ruff/mypy 绿；35 步历史检查未逐项本地复现）
pytest            ⚠️ 大概率红（本地 11 项既有失败；其中 4 项源于本地未跟踪 `_arch_v2x/`，
                  **CI 检出无此文件 ⇒ CI 实际可能只剩 7 项**，见 data/629_baseline.md §六）
compile/publish-check/site/pdf/epub/deploy → 预计 skipped（依赖链上游红）
```

## 四、结论与建议

1. CI 配置本身**健康**（四门关系正确、写者先跑读者后跑的竞态修复在位）；
2. push 后 CI 不会全绿，**红因是可提前定位的既有债**而非配置错误 ⇒
   不要在 push 后误判为 629 回归（详见 `data/push_readiness_629.md` §二）；
3. 629 未修改 ci.yml（本批不新增 job、不改 job 依赖）——若未来新增工具类 job，
   必须同样加 `needs: [replay]`，否则 `ci_concurrency_check_621.py` 会拦（`:395-403`）。
