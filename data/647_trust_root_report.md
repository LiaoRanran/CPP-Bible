# 647 A5 · 信任根独立审计（A1–A4 修复前后对比 + **仍存在的风险**）

> **结论先行**：A1/A2 修的是 **fail-open 行为**，A3 扩的是 **覆盖面**，A4 只建了 **接口**。
> **信任根独立性仍是 `L2`**（L3 未达）—— 密钥与 anchor 仍在本地。

## 一、修复前后对比

| # | 项 | 642 审计时（修复前） | 647 之后 | 判据 |
|---|---|---|---|---|
| A1 | 信任根文件缺失 | 只 warning，**exit 0**（642 FO-A 实测） | **strict 默认：exit 1**（lenient 兼容档仍 0） | 沙箱删 `tools/poison_exemptions.yaml`，点名=True |
| A2 | 不完整事件 | `from_dict({})` ⇒ **APPROVE + human_observed**（642 FO-B 实测） | `from_dict_strict()` 全拒=True | 空 dict/缺字段/未知字段三类 |
| A3 | 闭包覆盖 | 23 文件（641） | **33 条目**（含 67 规则指纹），与 tool_integrity 一致=True | 假装缺失 ⇒ FAIL |
| A4 | 外部锚 | **不存在** | 接口就绪（publish/verify + mock），但**真连外部服务=False** | 契约 + mock 往返 |

## 二、逐项实测证据

### A1（关键：**真实仓库一个文件都没删**）

```json
{
  "before_delete": {
    "strict": 0,
    "lenient": 0
  },
  "after_delete": {
    "victim": "tools/poison_exemptions.yaml",
    "strict": 1,
    "lenient": 0,
    "named": true
  },
  "real_repo_file_still_there": true,
  "fail_open_fixed": true
}
```

### A2

```json
{
  "rejected": {
    "空 dict": true,
    "缺 decision_origin": true,
    "未知字段": true
  },
  "all_rejected": true,
  "lenient_legacy": {
    "result": "APPROVE",
    "decision_origin": "human_observed"
  },
  "note": "宽容入口**有意保留**（历史 452 条必须能导入）⇒ 它是显式的历史通道，不是默认路径"
}
```

### A3

```json
{
  "status": "OK",
  "n_files": 33,
  "n_rules": 67,
  "consistent_with_tool_integrity": true,
  "attack_status": "FAIL",
  "attack_named": [
    "tools/gate_engine.py",
    "tools/poison_exemptions.yaml"
  ],
  "digest": "d954d10a0bdfdbe4ccf35676d3a61f8b4b5eb17e3b4d1847c0d89065ea35dd38"
}
```

### A4

```json
{
  "contract": {
    "publish": "publish(hash: str) -> receipt: dict",
    "verify": "verify(hash: str, receipt: dict) -> bool"
  },
  "implemented": [
    "mock-local"
  ],
  "reserved": [
    "github-gist",
    "rfc3161-timestamp",
    "opentimestamps"
  ],
  "real_external_service_connected": false,
  "mock_roundtrip": {
    "published": true,
    "verified": true,
    "tamper_detected": true
  },
  "anchor": "2da866b6a16288a095c8b0a32c8fa28410a2b7c5c6dd33f26a4fffcc80913b0f"
}
```

## 三、**仍存在的信任根共置点**（本批**没有**解决）

| 共置点 | 载体 | 为什么是风险 | 谁能解 | 磁盘在否 |
|---|---|---|---|---|
| 透明日志 anchor | `data/transparency_log.jsonl` | 改仓库即可同时改日志与其 anchor ⇒ 自证 | 外部锚 / 外部 KMS（交人裁决，647 未做） | 在 |
| 完整性基线 | `tools/.tool_checksums` | 「什么算被改过」的定义与被校验的文件在同一仓库 ⇒ 一起改就自洽 | 外部锚 / 外部 KMS（交人裁决，647 未做） | 在 |
| 目录 Merkle 根 | `data/supply_chain/merkle_roots.json` | 同上，且根与被覆盖文件同源 | 外部锚 / 外部 KMS（交人裁决，647 未做） | 在 |
| in-toto layout | `data/supply_chain/layout.json` | 同上 | 外部锚 / 外部 KMS（交人裁决，647 未做） | 在 |
| VSA 公钥 | `data/vsa/public_key_631.json` | 公钥在仓库内；验签方若读仓库里的公钥，则「换钥+换公钥」同样自洽 | 外部锚 / 外部 KMS（交人裁决，647 未做） | 在 |
| 外部锚 | `tools/external_anchor_647.py（mock-local）` | A4 的 mock 与被锚对象**同机同仓库** ⇒ 不构成独立锚（L3 未达） | 外部锚 / 外部 KMS（交人裁决，647 未做） | 不在 |

## 四、独立性刻度（v29 四级）

| 级别 | 定义 | 647 状态 |
|---|---|---|
| L1 同进程自证 | 自己证明自己 | ❌ |
| L2 同机独立实现 | 独立实现/独立进程复核 | ✅ **已达** |
| L3 仓库外可验 | 第三方凭仓库外锚独立验证 | ❌ **未达** |
| L4 外部权威背书 | 机构/标准背书 | ❌ |

- 从 L2 到 L3 的唯一路径：把 anchor 发布到仓库外的第三方（A4 的 3 个接入点任选其一）

## 诚实登记（防自欺）

1. **不宣称「信任根已独立」**：A1/A2 修的是**行为**（缺文件必红、残事件必拒），A3 扩的是**覆盖面**，A4 只建**接口** —— 三者都不改变「密钥与 anchor 在本地」这一事实；
2. **A1 保留了一个后门**：`--warn-only` 可退回宽容口径 —— 这是兼容性代价（迁移期/仓库副本），**不是** fail-closed 的漏洞（默认是 strict）；
3. **A2 的宽容入口有意保留**：历史 452 条必须能被导入 ⇒ `from_dict_lenient()` 是**显式历史通道**；
4. **A3 闭包仍跟不到 site-packages**，且**两个闭包并存**（641/647）——是否收编 641 留人裁决（改它会带跑历史 run 的 digest）；
5. **A4 的 mock 不是独立锚**：同机同仓库 ⇒ 对 L3 **零贡献**，只把「能不能接」变成「接口就绪」；
6. **本报告的一切数字都来自可复算的实测**（沙箱删除 / try-except / 闭包构建），没有一处是「应该会」。
