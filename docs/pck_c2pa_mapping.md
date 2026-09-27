# PCK ↔ C2PA / in-toto 词表映射（断言 / 声明 / 硬绑定）

> 651 W0 产出（纯文档，零代码）。目的：把自研 PCK 证书（`data/pck_certificate_schema_619.md`，`619-pck-v1`）
> 的字段，映射到两个**业界信任根标准**的既有词汇，便于外部审查者不需学新词即可核对。

## 一、三方一句话定位
- **PCK**（自研）：一张卡一份**便携凭证**，把「声明 + 证据 + 否定测试 + 验证器 + 人审 + 不确定性 + 溯源」打包。
- **C2PA**：面向**媒体资产**的溯源清单（manifest = claim + assertions + signature），核心是**硬绑定**——把声明密码学绑到资产字节。
- **in-toto**：面向**软件供应链**的策略（layout）与逐步执行记录（link），核心是**每一步的 materials/products + 签名**。

## 二、字段映射表（PCK → C2PA / in-toto）

| PCK 字段 | C2PA 对应 | in-toto 对应 | 说明 |
|---|---|---|---|
| `schema_version` | `claim_generator` / manifest 版本 | layout `_type` + 版本 | 守卫结构漂移 |
| `claim`（整体） | **claim**（一组 assertions 的容器） | link `products` | 对资产/产物的断言集合 |
| `claim.id` | assertion `c2pa.asset_id`（asset 标识） | product 路径 | 卡的唯一标识 |
| `claim.statement` | assertion 内容（如 `c2pa.actions` 的 description） | — | 人可读断言 |
| `claim.domain` / `claim.type` | assertion `label` 命名空间 | layout step 名 | 分类 |
| `evidence[].ref` | ingredient（`c2pa.ingredient`，指向被引用的输入资产） | link `materials` | 证据=声明的**输入材料** |
| **`evidence[].hash`** | **硬绑定** `c2pa.hash.data`（声明↔字节的密码学绑定） | material 的 `sha256` | **关键**：把声明钉到证据字节 |
| `negative_tests[].result` | assertion（如 `c2pa.actions` 的 `failed` 记录） | byproducts / link 结果 | 否定测试=主动攻击留痕 |
| `verifiers[].name` | signer（签名者身份） | layout 中的 `pubkeys` 授权公钥 | 谁在担保 |
| `verifiers[].result` | signature 有效性 + assertion 结果 | link 验证结果 | 担保结论 |
| `human_authority.status` | `c2pa.actions`（`c2pa.created`/`edited`）动作 | 人工 step | 人行动作 |
| `human_authority.review_method` | （无直接对应，映射到 action `softwareAgent` vs 人身） | step `byproducts.review` | **诚实缺口**：全项目=batch_authorization |
| `uncertainty.cs_upper_bound` / `estimand` | **无对应**（C2PA 无不确定性概念） | **无对应** | 自研扩展；见 §四 |
| `provenance.commit` | `c2pa.ingredient` 的 provenance 链 | link 的 `materials`/`products` + `byproducts` | 溯源到 git 提交 |
| `provenance.first_authorized_at` | manifest `signature_info.time` | link 时间戳 | 首次授权时刻 |
| `expiry` | assertion `c2pa.expiration`（若用） | — | 时效（对应 H7 recheck_after） |

## 三、三条"硬绑定"语义（最要命的一条）

| 绑定类型 | PCK | C2PA | 失败后果 |
|---|---|---|---|
| **硬绑定 hard binding** | `evidence[].hash` = sha256(证据字节) | `c2pa.hash.data` | 证据被改 ⇒ 绑定失效（626/627/628 的 PCK hash 漂移就是此面） |
| 软绑定 soft binding | 无（不做水印/指纹） | 水印/指纹 | 本仓库**不依赖**软绑定（诚实登记） |
| 声明绑定 claim binding | `claim` 内字段互相一致 | claim 结构自洽 + 签名 | 字段矛盾 ⇒ 校验拒绝 |

## 四、诚实缺口（映射不上，必须显式登记，不硬凑）
1. `uncertainty`（CS 上界/estimand）：C2PA 与 in-toto **均无**不确定性度量 ⇒ PCK 相对二者是**增强**，但这也意味着二者的外部工具**无法**核对这项。
2. `negative_tests`：C2PA 无"主动攻击结果"概念；in-toto 的 byproducts 可承载但非标准语义 ⇒ 属**自研扩展**。
3. `human_authority.review_method`：C2PA 区分 softwareAgent/人，但**不表达"批量授权 vs 逐条独立"**这一区分（正是 615/642 的核心缺口）⇒ 需在 assertion 自定义 label 承载。

## 五、落地建议（只写不做）
- 若未来要对齐 C2PA：把 `evidence[].hash` 直接落为 `c2pa.hash.data` assertion，即可复用 C2PA 的硬绑定验证器做**独立复核**。
- 若要对齐 in-toto：把每次 replay/gate 产物落为 link（materials=输入卡哈希，products=产物哈希），layout 即 67 规则 + Domain Pack。
- **本轮不实现**（W0 纯词表；实现留后续批次，需人审）。
