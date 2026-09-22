# 625 A2 · OTS re-anchor（信任根重钉致 anchor 过期）

> 工具：`tools/ots_anchor_613.py`（`opentimestamps_anchor.stamp()`）· 锚定对象：`data/supply_chain/merkle_roots.json`
> 铁律：**不 submit**（不上链）、不改 OTS 工具逻辑、pending 诚实标注。

---

## 一、旧 anchor 过期详情

| 项 | 值 |
|---|---|
| 过期原因 | 624 B1 改 `gate_engine.py`（接线 4 条 block 规则）→ `tool_integrity --update` 重钉 ⇒ **信任根（merkle_roots.json）变更** |
| 现象 | `ots_anchor_613.py --check` 返回 1：「已存在的 .ots 摘要与当前信任根不一致」 |
| 旧取用 | `data/supply_chain/merkle_roots.json.ots` 内 digest 为 624 前版本 |

## 二、新 anchor 生成详情

| 项 | 值 |
|---|---|
| 操作 | 重跑 `python tools/ots_anchor_613.py`（对**当前**信任根重新 stamp） |
| 新 digest | `f80d71fa69b7cdbd…`（与当前 `merkle_roots.json` 一致） |
| .ots | `data/supply_chain/merkle_roots.json.ots`（已重生成） |
| 报告 | `data/ots_anchor_613.md`（已重生成） |
| 状态 | **pending（未上链）** |

## 三、正确性验证

| 项 | 结果 |
|---|---|
| digest 一致（.ots 内 = 当前信任根） | ✅ |
| 时间戳为当前 | ✅（`stamp.created_at`） |
| OTS 格式（magic/版本/操作码） | ✅（`parse_ots` 结构校验通过） |
| `--check` 自验证 | ✅ exit 0 |
| `tests/test_ots_anchor_613.py` | ✅ 7 例全过 |

## 四、诚实标注

> **anchor 为 pending 状态，未上链**：`otss_anchor_613` 不向 OTS 日历 submit ⇒ 比特币 attestation 段为占位零，
> **不构成时间戳证明**。真正上链（`ots submit`）需**人授权 + 外部服务**，本批不做。

- ⇒ 当前可证明「该 .ots 绑定此摘要」；**不能**证明「此摘要于某时刻已存在」。

## 五、局限性声明

1. **未上链**：pending 不等于「已锚定时间」，需人执行 submit 并回填 `.ots`。
2. 每次 `tool_integrity --update` 重钉信任根都会使 anchor 重新过期 ⇒ 建议 626 起把「re-anchor」纳入重钉流程（或降低重钉频率）。
3. 本批只重生成凭据，**不改 OTS 工具逻辑、不改信任根本身**。
