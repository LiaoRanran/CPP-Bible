# 615 D1 · CI 配置确认（**非实跑**）

> 614 未 push ⇒ 无新 CI run。本报告为**静态配置确认**。
> **诚实声明**：CI 实跑全绿需 push 后触发验证；本报告**不**代表 CI 已通过。

## 一、逐项确认
| 项 | 结果 | 依据 |
|---|---|---|
| gate job 装 pyyaml | ✅ | 步骤 `Install gate tool dependencies (pyyaml / hypothesis)` |
| quality job 装 pyyaml | ✅ | 步骤 `Install gate/quality tool dependencies (pyyaml / hypothesis)` |
| pytest job 依赖完整 | ✅ | `pip install -q pytest pytest-xdist pyyaml hypothesis` |
| replay job 增量模式 | ✅ | 默认增量；`tools/` 变更回退全量（`--rebuild-manifest`） |
| quality job ruff/mypy | ✅ | `Ruff (tools/ 静态检查硬门禁)` + `Mypy (tools/ 类型检查硬门禁)` |

- 均来自 614 A1（commit `512d991`）：在 `quality`/`gate` 的 `setup-python` 后补 `pip install -q pyyaml hypothesis`。

## 二、四 job 依赖配置清单
| job | 依赖安装 | 关键步骤 |
|---|---|---|
| gate | `pyyaml hypothesis` | `gate_engine --check` + S1–S6（golden_lock `--no-replay` / debt_ledger / poison_drill） |
| quality | `pyyaml hypothesis` | ruff / mypy + 30+ 质量门禁 |
| pytest | `pytest pytest-xdist pyyaml hypothesis` | 两阶段 pytest（并行 + 串行） |
| replay | —（增量判定） | replay 增量/全量 + manifest |

## 三、潜在问题清单
| # | 现象 | 判定 |
|---|---|---|
| 1 | pytest job 的 run 脚本含一行裸 `rc=0` | **无害**（shell 赋值，不影响退出码） |
| 2 | 其余 job（compile/site/pdf/epub/deploy）非四 job 范畴 | 不在本批确认范围 |
| 3 | 未发现「job 缺依赖」/「硬编码 `.exe`」/「缺 `needs`」 | — |

## 四、结论与边界
- 四 job 依赖配置**完整**；614 A1 的 pyyaml 修复**已在配置中**。
- **未修改 ci.yml**（614 已修）；**未 push**。
- **诚实声明**：614 未 push，本报告为配置确认而非 CI 实跑结果。CI 实跑全绿需 push 后触发验证。
- 若发现新问题（本批未发现），记录但**不自行修复**（交人裁决）。
