# 629 C4 · 端到端他验编排（独立验证 → VSA → 透明日志 → 独立重验）

> 工具：`tools/e2e_attestation_629.py`（**全程临时目录**：凭证/密钥/日志都不落仓库；本仓唯一写入是这份报告）

## 一、各步结果与耗时

| 步骤 | 耗时(s) | 结果 | 详情 |
|---|---|---|---|
| ① 独立验证者重算 | 0.19 | ✅ | W2 IN79/OUT42 · PCK authorized 27 · ledger 452 条 |
| ② VSA 凭证（628 形态）+ HMAC 校验 | 0.45 | ✅ | HMAC valid=True · 输入锚定=True · 结果一致=True |
| ③ 非对称升级（RSA-2048 私钥签/公钥验） | 0.48 | ✅ | RSA-2048/PKCS1v15-SHA256 · 公钥指纹 6bb940bf5af5242b… |
| ④ 透明日志入册（临时日志，隔离生产链） | 0.01 | ✅ | log_index=0 · entry_hash=d05a56ee35d32123… |
| ⑤ 从日志取回 + 独立重验 | 0.01 | ✅ | inclusion=True(index=0) · 公钥复验=True |
| ⑥ 篡改检测（改 results 后重验必失败） | 0.0 | ✅ | tamper detected |

**端到端全绿：True** · 总耗时 1.14s

## 二、凭证链可视化

```
凭证链（文本树）
├─ ① 独立验证者 independent_verifier_628（零 import 本项目工具）
│     ├─ verifier_sha256 绑定：38e7235e6dee9f8c…
│     └─ 重算：W2 IN79/OUT42 · PCK authorized 27 · ledger valid
├─ ② VSA 凭证（628 形态）
│     ├─ HMAC-SHA256 attestation：7b1194bd51b61663…
│     └─ 输入三重锚定：ledger ec8cbf5cca2d… / grounded … / pck_dir …
├─ ③ 非对称签名（629 C1）
│     ├─ scheme：RSA-2048/PKCS1v15-SHA256
│     └─ 公钥指纹：6bb940bf5af5242b…
└─ ④ 透明日志（append-only 哈希链）
      ├─ log_index：0
      ├─ entry_hash：d05a56ee35d32123…
      └─ prev_log_hash：GENESIS…
            ↑ ⑤ 从日志取回凭证 → 公钥复验 + inclusion 通过
```

## 三、与 628 B4 端到端的差异

| 项 | 628 B4 | 629 C4 |
|---|---|---|
| 签名 | HMAC（对称） | HMAC + **RSA-2048 非对称**双签 |
| 日志 | 追加到**生产**日志（每次跑 +1 条，会让基线漂移） | 追加到**临时**日志（走 628 的 `CPPBIBLE_TRANSPARENCY_LOG` 隔离机制，生产链零漂移） |
| 重验 | 628 `--check` 读生产凭证 | 从日志**取回**凭证 → 公钥复验 + inclusion |
| 密钥 | 生产 `data/vsa_secret.key` | 临时目录（用完即删；仓库零落盘） |

- 本次运行前后：生产日志条目 = **1 条**（未被本次演示改动）；临时日志条目 = 1 条。
- 篡改检测：改 `results.w2_in=999` 后公钥复验失败 = **True**。

## 四、局限

- 验证者仍是**本项目写的**（独立性仅到 L2 分实现，见 C3）；
- 公钥由同一主体生成 ⇒ 信任根未独立（见 C1）；
- 临时日志是本地文件，无外部见证者；
- 演示只覆盖 **1 张卡/一次全量重算**，不是逐卡凭证（B1 验证者本身是全量重算器）。
