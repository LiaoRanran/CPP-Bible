# 614 A1：CI gate job 失败根因（#581 起持续红 → #624 仍红）

## 结论（根因）
`gate` job（及同为缺依赖类的 `quality` job）**没有任何 `pip install` 步骤**。
`tools/gate_engine.py` 顶层 `import yaml`，而 GitHub `ubuntu-latest` 裸 `python3` **不含 pyyaml**
（仅 `pytest` job 显式 `pip install pyyaml`）。结果：

```
python3 tools/gate_engine.py --check   → ModuleNotFoundError: No module named 'yaml' → exit 1
```

CI 注解只回显 "Process completed with exit code 1"，无堆栈 ⇒ 静默失败。
这是 #624 gate job 仍红的**根因**：`gate_engine --check` 在 S1-S6 之前就崩了。

> 注：`cdd3b2d` 给 `golden_lock.py` 加 `--no-replay` + ci.yml 用 `--no-replay` 修复的是
> "replay 真编译 .exe 跨平台 infra_error" 这一**另一类**问题；它修好了 golden_lock 自身，
> 但没解决 `gate_engine.py` 缺 pyyaml 的崩溃——故 #624 在 cdd3b2d 后仍红。

## 本地复跑（allowed 命令，非禁止四类）
- `python3 tools/golden_lock.py check --no-replay` → exit 0（✅ 恶化 0）
- `python3 tools/debt_ledger.py check` → exit 0（✅ 票据 3 · 负债率 15% · 问题 0）
- `python3 tools/poison_drill.py`：按 614 §五 铁律**不跑**（监工门禁）；其 CI 可行性评估见下。

## poison_drill.py 的 CI 风险（读码评估，未执行）
- `gate` job 跑在 `ubuntu-latest`（默认自带 `g++`），P3 毒样例的 g++ 编译夹具**应可工作**。
- 未发现需额外依赖的硬阻塞；若未来 CI 换为无 g++ 镜像，再按任务书方案加 `--ci` 跳过 P3/P57 等需编译毒样例。
- 当前**无证据**表明 poison 是 #624 的 blocker；缺 pyyaml 才是。

## 修复
- `ci.yml`：`quality` 与 `gate` 两 job 在 `setup-python` 后各加
  `python3 -m pip install --quiet pyyaml hypothesis`（与 `pytest` job 口径一致）。
- 未改动 `golden_lock.py`（cdd3b2d 已就位）。

## 验收
- 本地 `golden_lock --no-replay` / `debt_ledger check` 均 exit 0。
- ci.yml 经 YAML 解析校验合法；gate/quality 步骤均已含 pyyaml 安装。
- 剩余验证：提交后等 CI #624+ 跑完（无 gh/网络通道，无法本地轮询，交 A3 记录 / 人核验）。

## 诚实边界
- 未跑 `gate_engine --check` / `poison_drill` / `replay --check` / `tool_integrity --check`（614 §五 禁止）。
- 若 `gate_engine --check` 在补 pyyaml 后仍因**真实规则命中**而红，那是另一类问题，需人/监工裁决，不在本修复范围。
