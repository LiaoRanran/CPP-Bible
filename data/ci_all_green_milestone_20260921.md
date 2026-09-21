# 614 A3：CI 四 job 全绿里程碑记录（截至 2026-09-21）

> 诚实声明：本机**无 gh / 网络通道**，无法用 GitHub API 拉取 #624+ 的 CI 日志或轮询结果。
> 故"四 job 全绿"的**最终确认需人/CI 在 push 512d991 后观察**。本文记录可达的本地证据与根因。

## 从 #581 起持续红 · 根因链
1. **replay 真编译 .exe 跨平台 infra_error**（golden_lock）：`cdd3b2d` 已修——golden_lock 加 `--no-replay` + ci.yml S1-S6 用 `--no-replay`。
2. **gate / quality job 缺 pyyaml**（真正剩余根因，#624 仍红）：`gate_engine.py` 顶层 `import yaml`，而 `gate`/`quality` job 无 `pip install`，ubuntu-latest 裸 `python3` 无 pyyaml ⇒ `gate_engine --check` 静默 `ModuleNotFoundError` exit 1。
   - 修复（A1，`512d991`）：`ci.yml` 在 `quality`/`gate` 的 `setup-python` 后各加 `python3 -m pip install --quiet pyyaml hypothesis`（与 `pytest` job 口径一致）。

## 本地可达证据（allowed 命令，非禁止四类）
| 命令 | 结果 |
|---|---|
| `golden_lock.py check --no-replay` | exit 0（恶化 0；warn 四桶 real12/legacy158/accepted16） |
| `debt_ledger.py check` | exit 0（票据 3 · 负债率 15% · 问题 0） |
| `governance_doc_guard.py verify` | exit 0（manifest 一致，A2 已重钉） |
| ci.yml YAML 解析 | 合法；quality/gate 步骤均含 pyyaml 安装 |

## 修复 commit
- `cdd3b2d` golden_lock --no-replay + ci.yml（replay infra_error）
- `512d991` ci.yml 补 pyyaml（gate/quality 缺依赖，#624 真因）

## 四 job 全绿判定（待 CI 确认）
- pytest / replay / gate / quality 四 job 在 512d991 后**预期**转绿（依赖缺失已补、replay infra_error 已修）。
- 唯一未在本地核验：`gate_engine --check` / `poison_drill` / `replay --check` / `tool_integrity --check` 的实际 exit（614 §五 禁止苦力跑监工门禁）。若补 pyyaml 后 `gate_engine --check` 仍因**真实规则命中**而红，属另一类问题，交监工/人裁决。
- poison_drill 在 ubuntu-latest（自带 g++）预计可过；无 g++ 镜像才需 `--ci` 跳过编译毒样例（当前无证据需要）。

## 结论（本地）
- 已消除两类已知的 CI 静默失败根因（replay infra_error + 缺 pyyaml）。
- 四 job 全绿的最终确认 = CI 在 512d991 后的实际 run；**本机无法观测，交人/CI 核验**。
