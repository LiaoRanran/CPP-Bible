# 641 D1–D3 · Verifier Closure（信任根闭包）

- 状态：**OK** · 闭包文件 **23** 个 · 缺失 **0**
- closure_digest：`50205bb4ada90a4e715bedc9afd8613fa0e73ac368fe8be5ceafd3de297e5dce`
- source_revision：`d6a7856bbd511672faa491b5dbbc2570ad6a2499`

## 一、闭包构成

- 起点（新增并行层）：queyi_core_v10_641, queyi_core_cpp_641, queyi_core_toy_641
- CORE_TOOLS（判决逻辑本体，本轮零改动）：gate_engine, poison_drill, atom_evidence_replay, toolchain, cppbible
- 配置/schema 信任根：pyproject.toml, tools/.tool_checksums, data/supply_chain/merkle_roots.json + `data/supply_chain/*`

## 二、缺失即 FAIL（D2）

```
simulate_missing(['pyproject.toml']) ⇒ FAIL
```

## 三、诚实登记

1. 闭包只跟 **repo 内 `tools/*.py`** 的 import；第三方依赖（如 PyYAML）以 `pyproject.toml` 声明进闭包，**不递归进 site-packages**；
2. 「缺失即 FAIL」只作用于 **新 core 口径**，未强行切换任何既有流程（§八.5）；
3. 闭包完整性的**强度**仍取决于本机信任根未外移（外部 KMS/第三方签名留交人裁决）。
