# 631 E2 · 第三方验证指南（如何用公钥验证他验证据）

> 对象：任何想**独立复核**本项目他验证据的第三方
> 前提：**不需要**安装任何第三方库（全部纯标准库）；**不需要**本项目的私钥。

## 0. 你会拿到什么

| 文件 | 内容 |
|---|---|
| `data/vsa/public_key_631.json` | RSA-2048 公钥（n/e）+ `fingerprint_sha256` |
| `data/vsa/sample_signed_631.json` | 631 用同批私钥签的**样例消息 + 签名**（供练习） |
| `data/vsa/attestation_*.json` | 628 B2 的 VSA 凭证（HMAC 签名，密钥不入库 ⇒ **第三方无法验 HMAC**，见 §3） |
| `data/transparency_log.jsonl` | 628 B3 透明日志（GENESIS 起的线性哈希链） |

## 1. 验 RSA 签名（离线、纯标准库）

```bash
# 用样例练手（应输出 True）
python -c "import sys,json;sys.path.insert(0,'tools');import vsa_asymmetric_signer_629 as S;\
pub=json.load(open('data/vsa/public_key_631.json'));\
pub={'n':int(pub['n_hex'],16),'e':pub['e']};\
s=json.load(open('data/vsa/sample_signed_631.json'));\
print(S.verify(pub, json.dumps(s['message'],ensure_ascii=False,sort_keys=True).encode(), s['signature_hex']))"
```

判定要点：
- 输出 `True` ⇒ 该签名确实由**对应私钥**产生；
- **请自行核对** `sample_signed_631.json` 里的 `public_key_fingerprint`
  与 `public_key_631.json` 的 `fingerprint_sha256` 是否一致（防"换公钥"）；
- 改一个字节再验 ⇒ 必须为 `False`（防"签名可复用"）。

## 2. 重算独立验证者（不看我们的结论，自己算一遍）

```bash
python tools/independent_verifier_628.py --check     # 零 import 本项目工具，纯标准库朴素重算
```

它重算：W2 三态（IN/OUT/UNDEC）、PCK authorized 数、Authority 账本哈希链、unique 计数。
应看到与系统一致的：`IN=114 / OUT=7 / UNDEC=0`、`PCK authorized=27`、`ledger=452`、`unique=93`。

## 3. 检查透明日志链

```bash
python tools/transparency_log_628.py --status   # 链完整性 + 引用文件一致性 + 未入册凭证
python tools/transparency_log_628.py --inclusion data/vsa/<某张凭证>.json
```

判定要点：`chain_valid=true`、`files.ok=true`（无 missing/drifted）、`unlogged=[]`、
目标凭证 `included=true`。

## 4. **你现在还不能验什么**（诚实边界）

| 项 | 状态 | 原因 |
|---|---|---|
| VSA 凭证的 **HMAC** 签名 | ❌ 第三方无法验 | 密钥 `data/vsa_secret.key` **故意不入库**（否则人人可伪造）⇒ 只能由持钥方验 |
| 公钥**未被替换** | ⚠️ 仅靠仓库无法证明 | 仓库可被同一主体改写 ⇒ 这正是 **631 E1 推荐路径 C（外部锚 OTS/Sigstore）** 要解决的问题 |
| 历史 RSA 签名的长期可验性 | ⚠️ 有限 | 私钥按策略**不落盘**，历史签名只能验证"当时那个公钥"；本批样例是**同批生成、同批可验** |

## 5. 建议的复核顺序

1. 先跑 §1（秒级，验证签名工具链可用）；
2. 再跑 §2（独立重算，验证"结论不依赖我们的实现"）；
3. 再跑 §3（验证"证据真的入了册、链没被改"）；
4. 最后阅读 §4，明确**哪些结论还需要信任我们**——这才是对"信任根"的诚实评估。
