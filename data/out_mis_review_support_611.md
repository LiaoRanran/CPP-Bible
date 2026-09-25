# 611 D1 · OUT 的 7 个 MIS 复核支撑（只读）

> 仅把「复核所需事实」结构化摆出，不裁决、不写人审、不落库判决。每行的 `if_all_approve_verdict` 是 what-if 重算（把该 MIS 全部攻击边升 medium），供人判断后果。

## 一、总览

- OUT MIS（本工具锁定）**7** 个；全图 OUT 节点共 42 个；
- 这 7 个的全部攻击边都是 `modify`（保持 low）⇒ 被命题辩护链击败；

## 二、逐 MIS 复核明细

### `MIS-LANG-001`（cred low · 现 OUT）

- 攻击者 **3** 条：approve 0 / modify **3** / reject 0
- 被击败者（决定它 OUT）：`ATOM-LANG-INLINE-001::prop-1, ATOM-LANG-INLINE-001::prop-2, ATOM-LANG-INLINE-001::prop-3`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-LANG-INLINE-001::prop-1->MIS-LANG-001` | `ATOM-LANG-INLINE-001::prop-1`→`MIS-LANG-001` | modify | ✅ | prop_to_mis |
| `ae-ATOM-LANG-INLINE-001::prop-2->MIS-LANG-001` | `ATOM-LANG-INLINE-001::prop-2`→`MIS-LANG-001` | modify | ✅ | prop_to_mis |
| `ae-ATOM-LANG-INLINE-001::prop-3->MIS-LANG-001` | `ATOM-LANG-INLINE-001::prop-3`→`MIS-LANG-001` | modify | ✅ | prop_to_mis |

### `MIS-MEM-001`（cred low · 现 OUT）

- 攻击者 **3** 条：approve 0 / modify **3** / reject 0
- 被击败者（决定它 OUT）：`ATOM-MEM-MOVE-002::prop-1, ATOM-MEM-MOVE-002::prop-2, ATOM-MEM-MOVE-002::prop-3`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-MEM-MOVE-002::prop-1->MIS-MEM-001` | `ATOM-MEM-MOVE-002::prop-1`→`MIS-MEM-001` | modify | ✅ | prop_to_mis |
| `ae-ATOM-MEM-MOVE-002::prop-2->MIS-MEM-001` | `ATOM-MEM-MOVE-002::prop-2`→`MIS-MEM-001` | modify | ✅ | prop_to_mis |
| `ae-ATOM-MEM-MOVE-002::prop-3->MIS-MEM-001` | `ATOM-MEM-MOVE-002::prop-3`→`MIS-MEM-001` | modify | ✅ | prop_to_mis |

### `MIS-MEM-003`（cred low · 现 OUT）

- 攻击者 **3** 条：approve 0 / modify **3** / reject 0
- 被击败者（决定它 OUT）：`ATOM-MEM-MOVE-002::prop-1, ATOM-MEM-MOVE-002::prop-2, ATOM-MEM-MOVE-002::prop-3`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-MEM-MOVE-002::prop-1->MIS-MEM-003` | `ATOM-MEM-MOVE-002::prop-1`→`MIS-MEM-003` | modify | ✅ | prop_to_mis |
| `ae-ATOM-MEM-MOVE-002::prop-2->MIS-MEM-003` | `ATOM-MEM-MOVE-002::prop-2`→`MIS-MEM-003` | modify | ✅ | prop_to_mis |
| `ae-ATOM-MEM-MOVE-002::prop-3->MIS-MEM-003` | `ATOM-MEM-MOVE-002::prop-3`→`MIS-MEM-003` | modify | ✅ | prop_to_mis |

### `MIS-UB-001`（cred low · 现 OUT）

- 攻击者 **2** 条：approve 0 / modify **2** / reject 0
- 被击败者（决定它 OUT）：`ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-001` | `ATOM-UB-GRAY-001::prop-1`→`MIS-UB-001` | modify | ✅ | prop_to_mis |
| `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-001` | `ATOM-UB-GRAY-001::prop-2`→`MIS-UB-001` | modify | ✅ | prop_to_mis |

### `MIS-UB-004`（cred low · 现 OUT）

- 攻击者 **2** 条：approve 0 / modify **2** / reject 0
- 被击败者（决定它 OUT）：`ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-004` | `ATOM-UB-GRAY-001::prop-1`→`MIS-UB-004` | modify | ✅ | prop_to_mis |
| `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-004` | `ATOM-UB-GRAY-001::prop-2`→`MIS-UB-004` | modify | ✅ | prop_to_mis |

### `MIS-UB-008`（cred low · 现 OUT）

- 攻击者 **2** 条：approve 0 / modify **2** / reject 0
- 被击败者（决定它 OUT）：`ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-008` | `ATOM-UB-GRAY-001::prop-1`→`MIS-UB-008` | modify | ✅ | prop_to_mis |
| `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-008` | `ATOM-UB-GRAY-001::prop-2`→`MIS-UB-008` | modify | ✅ | prop_to_mis |

### `MIS-UB-014`（cred low · 现 OUT）

- 攻击者 **2** 条：approve 0 / modify **2** / reject 0
- 被击败者（决定它 OUT）：`ATOM-UB-GRAY-001::prop-1, ATOM-UB-GRAY-001::prop-2`
- W2 辩护者：`—`
- **若把全部攻击边升 approve（medium）⇒ 判决变为 `OUT`**

| 边 id | 攻击者→目标 | 人审 | 构成击败 | 方向 |
|---|---|---|---|---|
| `ae-ATOM-UB-GRAY-001::prop-1->MIS-UB-014` | `ATOM-UB-GRAY-001::prop-1`→`MIS-UB-014` | modify | ✅ | prop_to_mis |
| `ae-ATOM-UB-GRAY-001::prop-2->MIS-UB-014` | `ATOM-UB-GRAY-001::prop-2`→`MIS-UB-014` | modify | ✅ | prop_to_mis |

## 三、口径与边界

- **不改仓**：本工具是复核「看板」，所有判决变化仅存在于 what-if 重算的内存里；
- **人审权力**：是否把 `modify` 改为 `approve` 由用户逐条裁定（可能翻盘 OUT→IN）；
- 与 610 P0 口径冲突（keep-low vs upgrade-medium）无关：本工具按入库权威 keep-low 口径读现状。
