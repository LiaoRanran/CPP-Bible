# 653 阶段 0 · 开工基线快照

> 写于 2026-09-27。批次 653：A 修假保护器（最高优先级）+ B 前端 P0 三样（星图/现场验哈希/landing）+ C 收尾。

## 一、协议确认
- 652 已收工：`status.json` `last_completed_batch=652`、`state=awaiting_review`。
- A 落在 **queyi-core**（保护器所在）；B 落在 CPP-Bible（**新建 `web/`**）；C 双仓。

## 二、开工 git 状态
| 仓库 | HEAD |
|---|---|
| CPP-Bible | `33d4a40f` |
| queyi-core | `5e9c0df` |

## 三、A 的现状诊断（**开工前实测**，非猜测）

### budget_guard_649（**真·假开关**）
- 实测：`consume()` 超预算时**只返回 `allowed=False`，从不抛异常** ⇒ 调用方忽略返回值即无任何拦截；
- `halted()` 是**纯状态查询**（`remaining<0`），与 mode 无关 ⇒ enforce/shadow 下**都 True**；
- 652 差分信号 `(halted, protection_raised)` 两档皆 `(True, 0)` ⇒ **确实不可区分**（652 结论成立）。

### shadow_mode_649（**652 的口径需更正**）
- 实测：`decide()` 在 enforce 下对**成熟规则**（age ≥ shadow_days）返回 `enforce`、shadow 下返回 `record_only`
  ⇒ **开关本身是真的**；
- 652 的差分探针用 **`observe(now=0)` 的新规则**（age=0 < 7 天）⇒ 两档都 `record_only`，
  **探针无法区分**，故 652 "shadow_mode 是假开关"的结论是**探针假象**（653 更正，登记）；
- **真缺口**：`decide()` 只**给建议**，没有任何**拦截面**（"enforce 下才真正拦截"并未实现）。

## 四、653-A 修复口径
1. **budget_guard**：`consume` 超预算且 enforce ⇒ **抛 `BudgetExceeded`**（真 halt）；shadow ⇒ 只记录不抛；
   `halted()` 改为 **mode 感知**（只有 enforce 且超预算才 True）；新增超限**审计记录**。
2. **shadow_mode**：新增**真拦截面** `gate(rule_id)`：窗口内/全局 shadow ⇒ `record_only`（放行+记录）；
   出窗口且 enforce ⇒ `enforce`（**blocked=True 真拦**）。
3. 差分复核：同输入在 enforce/shadow 下**行为必须不同**（budget: 抛/不抛；shadow_mode: 拦/不拦）。
4. 连带更新 650/652 里依赖旧语义的测试与结论（诚实修正，不掩盖）。

## 五、B 的范围与数据来源（**真实数据，不造**）
| 前端 | 数据来源 |
|---|---|
| 星图 hero | 卡：`atoms/**/*.md`（含 47 张）；边：`data/**` 中 194 条击败边（需定位真实台账） |
| 现场验哈希 | 浏览器 Web Crypto 重算 sha256；输入=工件字节（可上传/选内置样例）；离线可验 |
| landing | 静态 MPA，暗色克制（**不用渐变光斑粒子**） |

## 六、限界
- 前端为**静态站**（无后端、无构建依赖），用 CDN 引 cosmos.gl v3（离线时诚实降级为 2D canvas）。
- 全量 pytest（4015 例，估 ~50min）仍超 idle-timeout ⇒ 尽力跑 + 记录（652 G4 延续）。
