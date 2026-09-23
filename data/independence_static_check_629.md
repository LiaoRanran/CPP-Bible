# 629 C3 · 独立验证者静态证明

> 工具：`tools/independence_static_check.py`（纯标准库 `ast`，只读；**不运行被审工具、不修改它们**）

## 一、硬断言（AST 可判定）

| 目标 | import 的本地模块 | import 标准库/第三方 | 含 gate_engine |
|---|---|---|---|
| `tools/independent_verifier_628.py` | （无，零 import） | 8 个 | **否** |
| `tools/vsa_verify_628.py` | （无，零 import） | 10 个 | **否** |

- 仓库 `tools/` 下模块共 336 个；两个验证端**均零 import** 其中任何模块 ⇒ 代码层独立性（L2）成立。

## 二、数据读取清单（含分类）

### `tools/independent_verifier_628.py`

| 路径 | 分类 |
|---|---|
| `.yaml` | 报告/临时产物 |
| `attack_edges_candidates.jsonl` | 系统输出（对比基准） |
| `authority_projection_626.json` | 系统输出（对比基准） |
| `data/attack_edges_candidates.jsonl` | 系统输出（对比基准） |
| `data/authority/decision_event_v2_ledger.jsonl` | 敏感信任文件 |
| `data/authority_projection_626.json` | 系统输出（对比基准） |
| `data/grounded_labels_w2.json` | 系统输出（对比基准） |
| `data/independent_verifier_628.json` | 报告/临时产物 |
| `data/independent_verifier_report_628.md` | 报告/临时产物 |
| `data/pck/certificates` | 原始数据 |
| `data/review_item_ledger.jsonl` | 系统输出（对比基准） |
| `decision_event_v2_ledger.jsonl` | 敏感信任文件 |
| `grounded_labels_w2.json` | 系统输出（对比基准） |
| `independent_verifier_628.json` | 报告/临时产物 |
| `independent_verifier_report_628.md` | 报告/临时产物 |
| `review_item_ledger.jsonl` | 系统输出（对比基准） |

### `tools/vsa_verify_628.py`

| 路径 | 分类 |
|---|---|
| `.json` | 报告/临时产物 |
| `data/authority/decision_event_v2_ledger.jsonl` | 敏感信任文件 |
| `data/grounded_labels_w2.json` | 系统输出（对比基准） |
| `data/pck/certificates` | 原始数据 |
| `data/transparency_log.jsonl` | 报告/临时产物 |
| `data/vsa` | 报告/临时产物 |
| `data/vsa_secret.key` | 报告/临时产物 |
| `decision_event_v2_ledger.jsonl` | 敏感信任文件 |
| `grounded_labels_w2.json` | 系统输出（对比基准） |
| `transparency_log.jsonl` | 报告/临时产物 |

## 三、第三条第断言：不读敏感信任文件 —— **口径不符（如实报告）**

- `tools/independent_verifier_628.py` 读取：`data/authority/decision_event_v2_ledger.jsonl`、`decision_event_v2_ledger.jsonl`
  ⇒ 按任务书字面口径**构成耦合**。
  **性质判定（诚实）**：`decision_event_v2_ledger.jsonl` 是**被验证对象**（该验证者的任务就是重算它的哈希链），不是**信任依赖**（它不把账本当「真」而直接采信，而是重算后与系统输出比对）。
  因此本条按「口径不符 + 性质为设计使然」登记，**不修改 628 工具**（§零.11）。
- `tools/vsa_verify_628.py` 读取：`data/authority/decision_event_v2_ledger.jsonl`、`decision_event_v2_ledger.jsonl`
  ⇒ 按任务书字面口径**构成耦合**。
  **性质判定（诚实）**：`decision_event_v2_ledger.jsonl` 是**被验证对象**（该验证者的任务就是重算它的哈希链），不是**信任依赖**（它不把账本当「真」而直接采信，而是重算后与系统输出比对）。
  因此本条按「口径不符 + 性质为设计使然」登记，**不修改 628 工具**（§零.11）。

## 四、独立性分级（L1–L4）

| 级别 | 是否达成 | 判据/原因 |
|---|---|---|
| L1 独立主体 | ❌ | 验证者与作者是同一主体（你 + 本项目） |
| L2 独立实现 | ✅ | 零 import 本项目工具（AST 证明）+ 朴素重算 |
| L3 独立执行环境 | ❌ | 同机同解释器同依赖（无第三方依赖可移植） |
| L4 独立信任根 | ❌ | RSA 公私钥同主体生成（629 C1）；HMAC 更是共享秘密 |

**当前等级 = L2（分实现）**。要达到 L3/L4 需要：

- L3：把验证者放到**独立执行环境**（另一台机器 / 容器 / 无共享依赖介质）跑；
- L4：**公钥托管到独立第三方**（或外部透明日志），使「验签通过」不再由被验证方自证。

这两项都涉及**人与外部机构**，机器不能代办 ⇒ 已列入交人项（C1 同款结论）。

## 五、局限

- 静态分析只看**源码字面**：动态拼接的路径（`os.path.join(ROOT, *parts)`）或间接读取（经由第三方库）无法证明；
- `stdlib_imports` 未区分标准库与第三方（本仓工具依赖 `pyproject.toml` 白名单，两个验证端只用到 `argparse/hashlib/hmac/json/os/subprocess/sys/typing`）；
- 「被验证对象 vs 信任依赖」的性质判定是**人工判断**，已给出理由但需人审复核。
