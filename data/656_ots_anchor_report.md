# 656 A · OTS 外部锚（G9 总闸门）报告

> 生成：2026-09-28T22:53:02　引擎：`none`　目标：`data/supply_chain/merkle_roots.json`

## 一、锚了什么

- 目标文件：`data/supply_chain/merkle_roots.json`（1081 字节）
- 其 sha256：`01699c09d0dba3646906a4ae53230f38602df487efd3a72a47a8c549e2a171d4`
- 该文件内含 5 个受控目录的 Merkle 根（Book, Examples, atoms, evidence, mutation_baselines）

## 二、当前判定

- verdict：**invalid**
- 说明：无官方实现：只能校验文件头（magic 不符）⇒ 判 `invalid`：连文件头都不是 OTS。
- 官方实现能否解析：`None`
- magic 是否等于官方 HEADER_MAGIC：`False`
- 覆盖的 digest：`None`
- attestations：`null`

## 三、日历与依赖

- 提交目标（公开 BTC 聚合日历）：
  - `https://alice.btc.calendar.opentimestamps.org`
  - `https://bob.btc.calendar.opentimestamps.org`
  - `https://a.pool.opentimestamps.org`
  - `https://finney.calendar.eternitywall.com`

## 四、状态机（不许越级叫）

| verdict | 含义 | 说明 |
|---|---|---|
| `missing` | 没有 .ots | 尚无任何外部锚 |
| `invalid` | 文件不是有效 OTS | magic 不符 / 官方实现解析失败 / 无 attestation / 挂载对象错 |
| `pending` | 已提交日历、未入块 | digest 已进日历 Merkle 树；比特币证明待 `--upgrade` |
| `bitcoin_anchored` | 已含比特币区块头证明 | 最外层锚成立 |
| `downgraded_json` | 无引擎时的登记表 | **不是**锚点；内含上链命令 |

## 五、怎么复核（任何人、任何时间）

```bash
python tools/ots_anchor_656.py --analyze
ots verify data/supply_chain/merkle_roots.json.ots -f data/supply_chain/merkle_roots.json
python tools/ots_anchor_656.py --upgrade     # 联网：拉 Bitcoin attestation
```
