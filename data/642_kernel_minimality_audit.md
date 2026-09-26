# 642 B2 · 内核最小性审计（AST · 只出报告，**不实际移代码**）

> 审计对象：`tools/queyi_core_v10_641.py`（内核 v1.0）。本模块**只读源码**，未修改/移动任何代码。

## 一、五问结论

| # | 问题 | 结论 |
|---|---|---|
| 1 | 领域依赖 | **零 ✅**（黑名单 14 个模块，AST 扫描） |
| 2 | 非标准库依赖 | **零 ✅** |
| 3 | 高攻击面能力 | **零 ✅**（无网络/子进程/动态执行/pickle/ctypes） |
| 4 | 写盘面 | `['OUT_JSON', 'OUT_MD']`（全部在 `data/` 下的声明常量） |
| 5 | 建议移出 | **4 项**（见 §三） |

## 二、内核功能清单（按 641 设计分层）

| 层 | 内容 | 归属 |
|---|---|---|
| 数据原语 | Artifact / ArtifactRef / Evidence / EvidenceResult / Decision | **内核必须** |
| 运行协议 | VerificationRun / VerificationRunBuilder / _run_id / _run_integrity | **内核必须** |
| 端口与插件契约 | VerifierPort / AttackerPort / AuthorityPort / EvidencePort / DomainPack | **内核必须** |
| 投影层 | _PROJECTORS / register_projector / project / _p_summary / _p_manifest / _p_decisions | **内核必须** |
| 通用规则引擎 | Rule / RuleOutcome / RuleEngine | **内核必须** |
| 规范化与哈希 | canonical_json / digest_of / digest_bytes / canonicalize_content / _uri_norm | **内核必须** |
| 不变量与自证 | module_imports / verify_no_domain_imports / kernel_self_digest | **内核必须** |
| 报告与 CLI | write_report / measure / selftest / main / _raises | **建议剥离到 CLI 层** |

### 2.1 统计

- 总行数 **813**（代码 563 / 注释 27 / 文档串 73 / 空行 150）
- 顶层符号 **47**（类 16 / 函数 22 / 常量 9）
- 内核 import：`['__future__', 'abc', 'argparse', 'ast', 'dataclasses', 'datetime', 'hashlib', 'json', 'os', 'sys', 'typing']`

### 2.2 依赖方向（双向核验）

| 检查 | 结果 |
|---|---|
| 适配器 `queyi_core_cpp_641.py` 是否 import 内核 | ✅ 是（预期：是） |
| 适配器 `queyi_core_toy_641.py` 是否 import 内核 | ✅ 是（预期：是） |
| 内核是否 import 适配器 | ✅ 否（预期：否） |

## 三、建议移出清单（**只建议，不执行**；移代码留 643）

| 符号 | 建议去向 | 理由 |
|---|---|---|
| `write_report` | CLI/报告层（内核外） | 报告是**呈现**而非协议；内核只应产出投影，渲染交给 CLI 层 |
| `OUT_MD` | CLI/报告层（内核外） | 同上：写盘路径常量属报告层 |
| `OUT_JSON` | CLI/报告层（内核外） | 同上 |
| `RuleEngine` | 插件侧（待复核） | 引擎本身通用（规则外置），但它只服务『判定』方向；若 643+ 出现规则模型不同的第二/第三领域，应评估下沉为插件服务 |

### 3.1 为什么「建议移出」只有这几项（诚实结论）

内核里**没有**任何领域逻辑可移 —— 这不是「没查」，而是 AST 机械证明了：

1. 内核 import 集 `['__future__', 'abc', 'argparse', 'ast', 'dataclasses', 'datetime', 'hashlib', 'json', 'os', 'sys', 'typing']` **全部是标准库**（无 gate_engine / poison_drill / authority_v2 等）；
2. 领域知识只以**注入形式**出现（`RuleEngine.apply(evaluator=...)`、端口 ABC、投影注册表）；
3. 因此建议移出的 4 项都是**层次性**改进（报告层剥离、规则引擎归属复核），**不是**领域污染清理。

## 四、诚实登记

1. **只审计不修改**：本模块**未移动任何代码**（铁律 §七.5），「建议移出」仅为**建议**；
2. 分类是**人工判据**（`KERNEL_LAYERS` / `MOVE_OUT` 常量），不是机器自动推断；换人会得出不同分层，但 §一 的四个机械判据（领域/非标准库/攻击面/写盘面）是客观的；
3. `write_paths()` 用 `ast.unparse` 取**表达式文本**，不求值 ⇒ 若路径由变量间接拼接，仍可能漏判（本内核只有 2 个直接常量，风险低）；
4. 本审计**不覆盖**「内核是否做对了事」（正确性），只覆盖「内核是否足够小 / 依赖是否干净」（最小性）。
