# 632 B3 · 外人零信任验证本仓 VSA 谱系（端到端可复制步骤）

> 受众：**不知情、不信任本仓作者**的第三方审计者。目标：仅凭公开可获取的信息，独立验证
> 「本仓的 VSA 谱系（可信声明谱系）未被偷偷篡改」。
> 依赖 632 交付：B1 锚（`transparency_anchor_632.py`）、B2 校验（`transparency_verify_632.py`）、
> 631 E2 公钥（`data/vsa/public_key_631.json`）。

## 零信任假设

审计者**不**相信：作者声明、CI 绿、任何人的口头说明。审计者只相信：
1. 一份**自己亲眼读到**的透明日志 `data/transparency_log.jsonl`；
2. 一份**锚定在公开可验证位置**的日志哈希（B1 锚）；
3. 一把**事先约定、独立分发**的公钥（631 E2，路径 `data/vsa/public_key_631.json`）。

## 步骤（复制即可运行）

```bash
# 0) 取得仓库（审计者自己 clone，不依赖作者给的压缩包）
git clone <仓库URL> repo && cd repo

# 1) 校验透明日志哈希链自洽（B2）：log_index 连续、prev_log_hash 衔接、首条 GENESIS
python tools/transparency_verify_632.py --check
#   期望输出：632 B2 --check OK：N 条链自洽，锚一致

# 2) 校验「锚」与当前日志一致（B1）：锚里的 log_sha256 == 当前日志 SHA256
python tools/transparency_anchor_632.py --check
#   期望输出：632 B1 --check: OK 锚与日志一致
#   锚文件：data/vsa/anchor_<YYYYMMDD>.json（含 log_sha256）

# 3) 把锚哈希发布到公开可验证位置（作者侧动作，审计者独立核对）
#   作者执行：将 anchor_*.json 里的 log_sha256 发布到
#     - GitHub gist / OpenTimestamps / 以太坊 tx calldata 等任意不可篡改位置
#   审计者独立取得该 URL/txid，比对：链上/公开位置的哈希 == 本地 anchor_*.json 的 log_sha256
#   ⇒ 若一致，则「日志内容在锚定时刻起未被改动」获得外部见证。

# 4) 验证签名公钥真实性（631 E2）：公钥须通过独立渠道分发，不在本仓内自证
#   审计者持公钥 data/vsa/public_key_631.json，
#   对每个 VSA 产物 data/vsa/attestation_*.json 验证其签名：
python - <<'PY'
import json, pathlib
# 伪代码：用 E2 公钥校验 attestation 签名（具体见 631 E2 verify_guide）
key = json.loads(pathlib.Path("data/vsa/public_key_631.json").read_text(encoding="utf-8"))
print("公钥指纹（审计者须与独立渠道公布值一致）:", key.get("fingerprint"))
PY
#   注意：公钥本身不可在本仓内自证，必须另渠道核对指纹，否则「自签自验」无意义。
```

## 信任结论

- 步骤 1+2 通过 ⇒ 日志内部自洽且未被改动（篡改任一条都会破坏链或使锚失配）。
- 步骤 3 通过 ⇒ 日志内容在锚定时刻被外部见证（不可抵赖）。
- 步骤 4 通过（且公钥指纹经独立渠道核对）⇒ 每条 VSA 由持有该密钥者签署。

三者齐备 ⇒ 第三方可在**零信任**前提下确认本仓 VSA 谱系的完整性与来源，无需相信作者。

## 已知局限（诚实登记）

- 本仓为单用户阶段，E2 公钥的分发仍依赖作者另渠道公布指纹；若作者同时控制仓库与公布渠道，
  仍非密码学意义的「独立第三方」。属 631 E2 已记录的信任根阶段局限，待路径 C（外部基建）升级。
- B1 默认 `LOCAL_ONLY` 锚；外部锚定（步骤 3）当前为「待人工」状态，需作者执行发布后审计者再核对。
