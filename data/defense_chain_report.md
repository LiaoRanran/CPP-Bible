# 辩护链批量报告（610 B1）

## 1. 总览

- 节点 **121**（命题 79 + 误解 42)
- 判决 **IN 114 / OUT 7 / UNDEC 0**
- 边 388 条 · 击败边 **17** · 3 轮收敛
- 可信度分布 {'medium': 114, 'low': 7}

## 2. OUT 节点（7 个）

- `MIS-LANG-001`（cred low）：被 3 个攻击者击败（ATOM-LANG-INLINE-001::prop-1, ATOM-LANG-INLINE-001::prop-2, ATOM-LANG-INLINE-001::prop-3）· 辩护者 3 条
- `MIS-MEM-001`（cred low）：被 3 个攻击者击败（ATOM-MEM-MOVE-002::prop-1, ATOM-MEM-MOVE-002::prop-2, ATOM-MEM-MOVE-002::prop-3）· 辩护者 3 条
- `MIS-MEM-003`（cred low）：被 3 个攻击者击败（ATOM-MEM-MOVE-002::prop-1, ATOM-MEM-MOVE-002::prop-2, ATOM-MEM-MOVE-002::prop-3）· 辩护者 3 条
- `MIS-UB-001`（cred low）：被 2 个攻击者击败（ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2）· 辩护者 2 条
- `MIS-UB-004`（cred low）：被 2 个攻击者击败（ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2）· 辩护者 2 条
- `MIS-UB-008`（cred low）：被 2 个攻击者击败（ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2）· 辩护者 2 条
- `MIS-UB-014`（cred low）：被 2 个攻击者击败（ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2）· 辩护者 2 条

## 3. 无辩护者的节点（7 个）

- `ATOM-CONC-FENCE-001::prop-1`（IN）
- `ATOM-CONC-FENCE-001::prop-2`（IN）
- `ATOM-CONC-LOCK-001::prop-1`（IN）
- `ATOM-CONC-LOCK-001::prop-2`（IN）
- `MIS-CONC-003`（IN）
- `MIS-LANG-001`（OUT）
- `MIS-MEM-015`（IN）

## 4. 无攻击者的命题（4 个）

- `ATOM-CONC-FENCE-001::prop-1`（cred medium ⇒ 无攻击者即 IN）
- `ATOM-CONC-FENCE-001::prop-2`（cred medium ⇒ 无攻击者即 IN）
- `ATOM-CONC-LOCK-001::prop-1`（cred medium ⇒ 无攻击者即 IN）
- `ATOM-CONC-LOCK-001::prop-2`（cred medium ⇒ 无攻击者即 IN）

## 5. 逐节点辩护链（IN 命题抽样 5 个）

- `ATOM-CONC-FENCE-001::prop-1`：攻击者 0 条全部不构成击败（同可信度） ⇒ 判 IN；其中 0 个攻击者被它击败
- `ATOM-CONC-FENCE-001::prop-2`：攻击者 0 条全部不构成击败（同可信度） ⇒ 判 IN；其中 0 个攻击者被它击败
- `ATOM-CONC-LOCK-001::prop-1`：攻击者 0 条全部不构成击败（同可信度） ⇒ 判 IN；其中 0 个攻击者被它击败
- `ATOM-CONC-LOCK-001::prop-2`：攻击者 0 条全部不构成击败（同可信度） ⇒ 判 IN；其中 0 个攻击者被它击败
- `ATOM-CONC-RACE-001::prop-1`：攻击者 1 条全部不构成击败（同可信度） ⇒ 判 IN；其中 0 个攻击者被它击败

> 口径：命题 = medium；MIS = 有 approve 边 ⇒ medium，否则 low（modify 保持 low，与入库 W2 产物一致）。
