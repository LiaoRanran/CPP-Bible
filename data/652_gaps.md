# 652 · 差啥清单（缺什么 / 为什么缺 / 什么时候能做）

> 652 E 产出。原则（652 要求）：**能做的全做，做不到的诚实登记，不假装**。
> 每条给：**缺什么** → **为什么缺**（本环境实测依据） → **何时能做**（具体条件/命令）。

## 一、外部工具/资源缺失（硬约束）

| # | 缺什么 | 为什么缺（实测依据） | 何时能做 |
|---|---|---|---|
| G1 | **OTS 真上链** | `ots` CLI **未安装**（`Get-Command ots` 为空）；现只有 `ots_anchor_613.py` 生成的**结构凭据**，attestation=**pending**（其 docstring 明示"不 submit"） | 装 `opentimestamps-client` + 联网 ⇒ `ots stamp data/supply_chain/merkle_roots.json` ⇒ 人工 submit 到日历 |
| G2 | **ESBMC falsification 真跑** | `esbmc` **未安装**（`Get-Command esbmc` 为空）⇒ H6 只出 `tool_unavailable` + 拟命令 | 装 ESBMC（官方 Linux/WSL 包；Windows 原生支持弱）⇒ `esbmc data/652_h5_probe.c --unwind 8` |
| G3 | **sanitizer 运行库** | 实测 `cannot find -lubsan`（MinGW-w64 未带 UBSan 运行库）⇒ H5 矩阵 4 例降级为 `sanitizer_runtime_missing` | 装带 sanitizer 运行库的 toolchain（LLVM/Clang 官方 Windows 包，或 WSL 的 gcc） |
| G4 | **全量 pytest（4015 例/541 文件）** | 实测：装 `hypothesis` 后收集成功；**fast 阶段 600s 只跑到 20%** ⇒ 估 ~50 分钟，超本工具 idle-timeout | 在 CI（`.github/workflows`）或长时间空闲窗口跑；命令见 `docs/pytest_two_phase.md` |
| G5 | **训域内小模型** | 无 GPU / 无训练语料 | 有 GPU 与语料后（成本高，需立项） |
| G6 | **CVM / 云外部锚** | 无云服务凭据（本机离线） | 接云 KMS/透明日志（631 E1 已评估三路径，推荐"外部 KMS+透明日志"） |
| G7 | **形式化证明（Rust 重写）** | 无 Rust 工具链；核心是 Python | 立项后用 Rust 重写内核（v29 已论证"通用验证器不可达"，仅对**内核**做） |

## 二、本批降级/未接线（工程缺口）

| # | 缺什么 | 为什么缺 | 何时能做 |
|---|---|---|---|
| G8 | **H5 的"LLM 离线造积木"** | 本环境无 LLM API ⇒ 积木取自**预置库**（6 块），工具只做组合+矩阵 | 接 LLM API 后：让 LLM 造块 → 过 `probe_assembler` 的编译闭环 ⇒ 入积木库 |
| G9 | **M4 验证器未接线全量 67 规则** | 现用**门禁读取面代表性子集**（id/status/claim_structured/claim_boundary/evidence/liveness）避免风险与耗时 | 把 `gate_engine` 以**只读沙箱**方式接进 challenger（需先解决其写盘面） |
| G10 | **T2 逐保护器粒度** | 649 保护器只读**全局** `QUEYI_PROTECTOR_MODE`（无 per-protector 通道）⇒ 本工具用临时 env 实现"逐保护器验证" | 给保护器加 per-protector 配置读取（改 4 个工具，需重钉信任根） |
| G11 | **T2 canary 真比例灰度** | `canary` 与 `enforce` **行为相同**（仅审计标签不同）；无采样机制 | 给保护器加采样开关（同 G10） |
| G12 | **budget_guard / shadow_mode 的模式开关"只改标签"** | 差分实测：两档下 `halted()` 均 True、`protection_raised` 均 0；`decide()` 均 `record_only` | 让这两个保护器在 shadow 下**不置位**（或明确"它们本就不该有 shadow 语义"）⇒ 需人裁决语义 |
| G13 | **嵌入式交叉编译 / HIL** | 无交叉工具链、无真机（M5 的"能编译≠对"无法闭环） | 装 arm-none-eabi-gcc + 开发板 |

## 三、口径/数据限制

| # | 限制 | 说明 | 何时能做 |
|---|---|---|---|
| G14 | **verified_at = git 首次提交日期** | A1 补的 87 张来自 `git log --diff-filter=A`，**不等于**"证据被复核的日期" | 人审后可覆盖为真实复核日期 |
| G15 | **PCK 硬绑定未覆盖原子卡正文** | T7 只把 `evidence[].hash` 落为 `c2pa.hash.data`；原子卡**正文**未哈希 ⇒ 改正文检测不到 | 给 PCK 加 `claim.hash`（需改 619 schema，向后兼容） |
| G16 | **OTS `.ots` 与 Merkle 根强绑定** | 本批 A1 改了 atoms/ ⇒ 根变 ⇒ 旧 `.ots` 失效（已重生成，但仍 pending，见 G1） | 每次改信任根后重跑 `ots_anchor_613.py`（已有流程） |

## 四、信任资产/治理

| # | 事项 | 说明 |
|---|---|---|
| G17 | **既有脏文件**（非 652 引入） | CPP-Bible 工作区仍有一批 `tests/test_6xx*.py` 等未提交改动（652 只提交了 `conftest.py`）；**需人裁决**是否成批提交 |
| G18 | **651 交人项仍开放** | W0 三词表采纳 / T1 是否采用回填版 / M7 队列是否切换 / OTS submit（同 G1） |
| G19 | **`--update` 的追认效应** | 651/652 的 `tool_integrity --update` 会把当时工作区的（正确）内容钉为基准；**改信任根必须显式留痕**（设计使然） |

## 五、本批**已做到**（对照，避免"只列缺的"）
A：87 卡 verified_at 补齐✅ / T1 452 真回填（原 sha256 不变）✅ / M7 30 迁移（原 sha256 不变）✅ / conftest 提交✅ /
全量**收集**成功（4015 例）✅ / OTS 结构重锚✅（真上链见 G1）。
B：H5 积木+矩阵（真机 4 ok）✅ / H6 降级登记✅。
C：M4 50 变体逃逸 0.0✅ / M5 裸金属检查 41 违规✅。
D：T3 RATS 三库✅ / T7 103 证书导出 103/103 一致✅ / T2 灰度上岗+真验证✅（缺口见 G10-G12）。
