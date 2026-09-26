# 647 C2 · 仓库拆分**最终方案**（基于 C1 沙箱实测）

> 依据：`data/647_split_sandbox_report.md`（沙箱实测：116 core 文件 / 164 提交 / 内核 selftest PASS /
> 测试 collect 215 例 0 错误 / 历史保留）。
> 原则：**CPP-Bible 工作树零改动**（拆分产物放仓库**外**），**不 push**（留交人）。

---

## 一、拆什么（core 的定义）

**core = 「能改"什么算通过"的东西」∪「阙疑架构层」**，具体由
`repo_split_sandbox_647.core_files()` **自动算出**（种子模式 ∪ repo 内 **import 传递闭包**）：

| 层 | 载体（模式） |
|---|---|
| 协议内核 | `tools/queyi_core_*.py`（v10 通用内核 / cpp 适配器 / toy_math 第二领域） |
| 信任根闭包 | `tools/verifier_closure_*.py` |
| 判决本体 | 5 个 CORE_TOOLS（`gate_engine` / `atom_evidence_replay` / `poison_drill` / `toolchain` / `cppbible`）—— 由闭包拉进来 |
| 证据层 | `tools/*_644.py` 头部层 + `tools/evidence_*.py` / `counterexample_searcher_*` / `standard_fetcher_*` / `compiler_probe_*` |
| 智能层 | `tools/smart_issue_finder_*` / `targeted_attacker_*` / `rule_drafter_*` / `rule_error_tracker_*` / `rule_aging_detector_*` / `loop_r5_runner_*` |
| 耦合层 | `tools/three_layer_orchestrator_*` / `coupling_effect_*` / `coupling_feedback_*` |
| **保护器** | `tools/*_636.py`（影子）+ `tools/*_642.py`（灰度）+ `tools/*_647.py`（真上岗）+ `protector_mode_647` |
| 公共件 | `tools/path_config_625.py` / `utf8_console.py` / `tool_integrity.py` / `queyi_data_models_645.py` / `decision_event_v2_626.py` / `authority_schema_v2_626.py` / `transparency_log_628.py` …（**由 import 闭包自动补全**） |
| 测试 | `tests/test_*_645.py` / `*_646.py` / `*_647.py` / `test_verifier_closure_641.py` |

**留在 CPP-Bible（不拆）**：`atoms/` `evidence/` `Examples/` `Book/` `Part0_Prerequisites/`
`misconceptions/` `References/` `WG21/` `Appendix/` `Benchmarks/` `Interview/` —— 领域内容。

---

## 二、目录结构（目标仓库 `queyi-core/`）

```
queyi-core/
├── core/           # 协议内核（queyi_core_v10_641 / cpp / toy）
├── evidence/       # 证据层工具
├── smart/          # 智能层工具
├── protection/     # 保护器（636 影子 / 642 灰度 / 647 真上岗 + 全局开关）
├── coupling/       # 三层耦合
├── trust/          # 信任根（闭包 / tool_integrity / 外部锚 / 审计）
├── tests/          # 从 CPP-Bible 拆过来的测试
├── tools/          # 公共件 + 兼容入口（可先按**扁平 tools/** 交付，见 §四 分期）
├── conftest.py     # **queyi-core 自己的最小 conftest**（只注入 sys.path）
└── README.md
```

**分期说明（重要）**：C3 首版**先按"扁平 `tools/`"交付**（即拆分后仍是 `tools/` + `tests/`），
因为：① 目录重排会**改写全部 import**，属于 D 线之后的大动作；② 先拿到"能独立跑"的最小可用仓库，
再谈结构。§二 的分层结构是**目标态**，落地排在 648+（交人裁决是否值得）。

---

## 三、依赖关系

```text
kernel (core/, 零领域依赖)
   ▲
   │ 被适配器包裹（CppVerifierAdapter）
cpp adapter ──► gate_engine（67 规则 + 5 CORE_TOOLS）
   ▲
   ├── evidence 层（编译器/标准/反例/等级）
   ├── smart 层（问题发现/攻击/规则草案）
   └── protection 层（636 影子 → 642 灰度 → 647 真上岗）
        ▲
        └── 只**消费**内核判决（内核不依赖保护器）
```

**单向依赖铁律**：内核**零领域 import**（641 已用 AST 机械证明）；
保护器**只消费**判决，**不被**判决依赖 —— 这是"保护器可一键回滚"的结构基础。

---

## 四、C1 沙箱实测的四个坑（拆之前必须知道）

| # | 现象 | 处理 |
|---|---|---|
| 1 | `git fast-export` 128：`tag ... tags unexported object` | `--tag-of-filtered-object=drop` |
| 2 | `git fast-export` 128：`encountered commit-specific encoding gbk` | `--reencode=yes` |
| 3 | 拆完 `pytest` **收集期全错**（conftest 强耦合整仓） | `conftest.py` / `pyproject.toml` **不迁移**；queyi-core 自带最小 conftest |
| 4 | 只写种子模式 ⇒ 保护器**前身模块**（642/636）缺失，大面积 ImportError | 清单 = 种子 ∪ **import 传递闭包** |

---

## 五、拆分步骤（C3 执行）

1. `python tools/repo_split_sandbox_647.py --execute <目标目录>`（**CPP-Bible 零改动**）；
2. 在目标目录写入 `README.md` + `tests/conftest.py`（最小）+ `.gitignore`；
3. 在目标目录 `git add -A && git commit`（**只本地提交，不建远端、不 push**）；
4. 验证：`python tools/queyi_core_v10_641.py --check` + `pytest --collect-only`。

**回滚**：目标目录**不在 CPP-Bible 内** ⇒ 直接删除目录即可；CPP-Bible 无需任何操作。

---

## 六、**不做**的部分（交人裁决）

- **不把 `queyi-core` 以 `git subtree` 合并回 CPP-Bible 子目录** —— 655/646 的 `tools/*` 会在
  两处重复，直接冲击 645/646 测试套件（"拆分后测试红"的高风险路径）。是否合并、何时合并，**留交人**。
- **不 push**（`queyi-core` 连远端都不建）。
- **不重排目录**（§二分层次结构留 648+）。
