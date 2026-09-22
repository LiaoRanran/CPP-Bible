# 626 E1 · PCK semantic verifier 规范（4 层验证）

> 工具：`tools/pck_semantic_verifier_626.py`
> 判据：10（PCK 能验证 reference / hash / negative-test 关系）
> **本批只验证，不修改任何 PCK 文件**

---

## 一、四层验证

| 层 | 名称 | 检查内容 |
|---|---|---|
| **B2-S** | schema validity | schema_version / claim / evidence 非空 / **verifiers** 非空 / uncertainty 有数字 / provenance.commit 非空 |
| **B2-R** | referential integrity | evidence.ref 可解析 / **hash 与文件实际内容匹配** / negative_tests 存在 |
| **B2-E** | evidence semantics | evidence 有 type+ref / claim 与 evidence 主题关键词一致性（**保守**，不做 LLM 级语义推理）/ negative_controls |
| **B2-A** | authority semantics | `human_authority.status` 与 Authority Ledger 一致 / `authorized` 须有 card-level event / 仅 edge-level ⇒ 跨粒度警告 |

## 二、实跑结果（83 张 PCK）

| 层 | pass / 83 |
|---|---|
| B2-S | **83** |
| B2-R | **27**（56 fail） |
| B2-E | **83** |
| B2-A | **83** |

**总计：pass 27 / fail 56** —— 失败全部来自 **B2-R**。

### 🔴 真实发现：56 张 PCK 的 `evidence.hash` 与当前文件不匹配

```
EV-CONC-001: evidence hash 不匹配：evidence/conc/EV-CONC-001.md
EV-CONC-002: evidence hash 不匹配：evidence/conc/EV-CONC-002.md
...（共 56 条）
```

- 证书中声明了 `evidence.hash: sha256:...`，但对 `evidence/*.md` 重算 SHA-256 不一致。
- 可能原因：证据文件在证书生成后被修改，或证书生成时的 hash 口径与当前文件不同（如前matter/换行差异）。
- **这正是判据 10「PCK 能验证 reference/hash 关系」的价值**：以前只看 schema（全过），
  现在能暴露真实引用漂移。
- **处置**：本批**只验证不修改**；是否重算 hash / 判定证书失效需人裁决（留 627）。

## 三、global vs local uncertainty

| 类型 | 判据 | 处理 |
|---|---|---|
| `global_uncertainty_ref` | 值 == 全局 cs 上界 `0.009062` | 标注为**全局引用**，不是该证书的本地不确定性 |
| `local_uncertainty` | 其他值 | 作为该证书的本地不确定性 |

> 建议 PCK schema 升级为 `global_uncertainty_ref` + `local_uncertainty` 两个字段
> （**本批只验证，不改 schema**）。

## 四、已知局限

1. B2-E 的"主题一致性"是**保守关键词匹配**，不做深度语义推理（需要 LLM 或人工）。
2. B2-R 的 replay artifact 比对目前只校验文件存在与 hash，`build/replay_manifest.json` 的结果比对留 627。
3. negative_test ID 是否真实存在于 `data/mutation/` 的校验留 627。

## 五、验证

- `--check` → PASS
- `tests/test_pck_semantic_verifier_626.py` → 11 例全绿
- 实跑报告：`data/pck_semantic_verification_report_626.md`
