# 628 批次验收报告（修债 + 他验三件套 + 人审可视化 + 镜像门监控）

> **批号**：628 · **基线**：`b913b0fe`（627 E1 收工）· **报告时间**：2026-09-23
> **结论**：12/12 任务完成（任务0 + A1–A4 + B1–B4 + C1 + D1 + E1），另有 1 个批内修补
> 与 3 个收工/产物 commit（共 **16 commits**）；
> 收工门禁 **PASS**；受控目录（atoms/evidence/Examples/Book）**零污染**。

---

## 一、任务完成情况（13 commits）

| 任务 | Commit | 一句话 |
|---|---|---|
| 任务0 | `d65d9eb5` | 开工基线台账：4 项技术债定位到文件行号 + 6 交人项分类 |
| A1 | `d1a4f50a` | `QUEYI_AUTHORITY_V2` flag 真正接入编译函数（V1/V2 双路径，tool_integrity 重钉） |
| A2 | `54f53519` | PCK hash 83 张全量处置（56 重算 + 26 补 hash + 1 需人审，备份 83 张） |
| A3 | `d0a0a467` | 镜像边对称性自动证明（194 条验证，76 条写入账本，118 条存 sidecar 留治理） |
| A4 | `3e9a8f96` | DEBT-001 处置 + replay manifest 只读复验（实测 0 失配，625 的 5 失配已被 626/627 刷新） |
| B1 | `9174502d` | 独立验证者：零 import 本项目工具，纯标准库独立重算，全部数字与系统一致 |
| B2 | `dcc088b9` | VSA 验证凭证（HMAC-SHA256 + verifier_sha256/输入三重哈希锚定，密钥不入库） |
| B3 | `9e9f2cd7` | 透明日志 append-only（GENESIS 起线性哈希链 + 篡改/删除检测 + inclusion） |
| B4 | `9de43287` | 他验端到端演示：独立验证 → VSA 凭证 → 透明日志全链路 + 审计声明 |
| 修补 | `9b7bcb5e` | B2/B3 遗留 lint 与 CLI 补齐 |
| C1 | `cd643e31` | 人审深色科技风仪表盘 v2（玻璃拟态 + 霓虹 + CSS 3D + 6 数据模块） |
| D1 | `b2d7a096` | 学习者镜像门监控（行为采集器 + 门状态 0/50 closed） |
| E1 | `87294cb8`+`00d50f10` | 收工门禁 + 验收报告 + status 更新（另有 E1 前置根因修复 `9147fdc6`、后置运行产物 `b638ecda`） |

**交付物**：新增工具 **13** 个（12 个 `--check` 工具 + `run_628_gate.py` 门禁）；
新增测试 **82 例 / 12 文件**（全量套件 2614 例中 628 批 82 例）。

---

## 二、4 项技术债清算核查表

| # | 技术债 | 清算前 | 清算后 | 验证 |
|---|---|---|---|---|
| 1 | V2 flag 未真接入编译函数（627 B1 发现） | flag 只被切换脚本读，编译函数无分叉 | `authority_projection_compiler_626.py` 入口读 flag，V2 走归一化 121 节点路径，默认 V1（硬边界 13） | 门禁：V1/V2 模式 W2 = IN114/OUT7/UNDEC0 一致；flag 默认关闭；tool_integrity `--update` 重钉后 `--check` 尺子一致 |
| 2 | PCK hash 缺口 83/83 | content_drift 56 + hash_absent 26 + ref_missing 1 | 82 张已重算/补 hash，**162 条引用与当前文件一致**；ref_missing 1 张（`ATOM-HIST-AUTOPTR-001`）标 `ref_missing_needs_human`，**未自动修、未判失效**（硬边界 8） | `pck_hash_renewal_628 --check` 绿；备份在 `data/pck_backup_628/`；语义字段零改动 |
| 3 | 镜像边 194 条 symmetry_proof_id=null | 全部为 null | 三条件全过 **76 条自动证明已写入账本**；118 条因缺 ReviewItem 存 sidecar，**不写入**、留治理决策 | `mirror_edge_symmetry_write_628 --check` 绿；写入后 W2 分布不变（IN114/OUT7/UNDEC0） |
| 4 | DEBT-001 到期 + replay manifest 5 失配 | 625 登记，626/627 未修 | DEBT-001：台账无该实体，等效清算（`expired_no_action_needed`）；manifest 实测 **0 失配**（625 的 5 失配已被 626/627 的刷新覆盖） | `replay_manifest_fix_628 --check` 绿；fixture 日期动态化，clean 场景全绿 |

---

## 三、他验三件套核查表

| # | 组件 | 功能 | 验证 | 局限性（诚实登记） |
|---|---|---|---|---|
| B1 | `independent_verifier_628` | 零 import 本项目工具，纯标准库**朴素重算** W2/PCK/ledger 哈希链/unique | W2 IN114/OUT7/UNDEC0、PCK authorized 27、ledger 链 452 条 valid、unique 93 —— **全部与系统一致**；篡改 ledger/PCK 可检测 | 验证者仍是本项目写的；零 import + 朴素算法只是消除 common-mode failure 的第一步，真正独立需外部验证者 |
| B2 | `vsa_attestation_628` + `vsa_verify_628` | HMAC-SHA256 凭证，锚定 verifier_sha256 + ledger/grounded/PCK 三重输入哈希 | 14 张凭证全部签名/输入/结果验证通过（截至本报告）；篡改检测有效；**验证端零 import 签发端** | HMAC 是对称签名：只能证明"持密钥主体生成凭证"，不能证明"独立主体认可"（真独立需非对称签名+密钥托管，留后续）；密钥不入库 ⇒ 换机后历史凭证无法验证 HMAC（`vsa_verify` 缺密钥时**拒绝验证且不新建密钥**，不会假失败） |
| B3 | `transparency_log_628` | append-only 线性哈希链（GENESIS 起）+ inclusion 存在性验证 | 23 条日志链完整；篡改/删除历史可检测；引用的凭证文件存在且哈希一致；**凭证全部入册**；重复追加幂等 | 本地存储、无外部见证者（真透明需推公开 Rekor 实例，留后续）；日志中有历史上重复追加产生的同凭证多条目（append-only 原则保留，未删改） |
| B4 | `third_party_audit_demo_628` | 端到端编排：独立验证 → VSA → 入册 → inclusion → 审计声明 | `--check` **只读幂等**（单测断言前后零字节变化）；实跑全绿，审计声明含时间/验证者/输入哈希/结果/日志 index | 编排器每次实跑新增 1 张凭证 + 1 条日志（设计如此：每次他验留痕）；`--check` 类操作全部零副作用 |

**他验意义**：系统第一次具备"第三方不信任作者也能独立复核"的原型闭环（独立复核 ✅ / 凭证 ✅ / 透明日志 ✅）。

---

## 四、V2 flag 接入结果（A1）

- 接入位置：`authority_projection_compiler_626.py` 编译入口读 `QUEYI_AUTHORITY_V2`；
- V1（默认）：grounded_labels 数据源，保持 625 行为；V2（=1）：DecisionEvent v2 归一化 121 节点；
- 回归验证：两种模式 W2 数字一致（IN114/OUT7/UNDEC0）；CORE_TOOLS（gate/poison/replay）不读 flag，行为不变；
- 回滚方案：`QUEYI_AUTHORITY_V2=0`（或 unset）即回 625 行为；V2 ledger/投影文件保留供审计。

---

## 五、关键数字（收工时）

| 指标 | 值 |
|---|---|
| DecisionEvent v2 ledger | 452 条（哈希链 valid） |
| 唯一审查账本 | 93 unique |
| 独立人类确认强度 | **0**（Blind Review 工具就绪，执行需人授权——硬边界 7） |
| W2 论证图 | 121 节点：IN 114 / OUT 7 / UNDEC 0（V1=V2） |
| PCK | authorized 27；hash 引用一致 162 条（83 张处置后） |
| 镜像边 | 自动证明写入 76 / sidecar 待治理 118 / 总 194 |
| VSA 凭证 | 14 张（截至报告生成；B4 实跑会追加，全部入册） |
| 透明日志 | 23 条（链完整，GENESIS 起） |
| 学习者镜像门 | **closed**（真实学习事件 0/50，采集器就绪） |
| 受控目录 | 零污染 |
| 测试 | 628 批 82 例全绿；全量 2614 例收工门禁内 82 例通过 |

---

## 六、偏差表（任务书假设 vs 实测）

| 任务书假设 | 实测 | 处理 |
|---|---|---|
| 人审进度"388 条"口径 | 仓库内无 388 口径（grep 零命中）；实测 93 unique + 452 DecisionEvent | C1 环形图按 unique 画，KPI 卡并列 DecisionEvent，偏差登记在设计说明 |
| B 线 3 个工具（B2 只写 attestation） | 实际 4 个：`vsa_verify_628` 独立于签发端（verify 端曾 import 签发端，**重写为零 import**——同源耦合会使"签发写错=验证也错"） | 修复并登记 |
| 10 个工具 `--check` | 12 个 + 门禁本体 | 门禁覆盖 12 个 |
| replay manifest 5 失配待修 | 实测 0 失配（626/627 已刷新 manifest） | 只读复验 + fixture 日期动态化，防误报 |
| 饼图含 ITEM_BLIND 类 | 当前 0 条（真实盲审未执行） | 饼图按实际三类画 |

**批内自纠的工程问题**（E1 门禁首跑暴露，已按根因修复）：
1. **B2 `--check` 污染状态**：self-test 曾向生产凭证目录写新凭证，导致下游"最新凭证须在日志中"随机失败 → 改为写临时目录（`save_credential(out_dir=)`），`--check` 只读生产目录；
2. **测试尘埃清理**：删除 **10 张从未入册**的凭证文件（仅因上述 bug 存在）；透明日志**一行未动**（append-only 保持），已入册凭证全部保留；
3. **"最新凭证"口径脆弱**：按文件名排序会受同秒生成/未入册凭证影响 → B4 改用**日志尾部在册凭证**，并新增"凭证全部入册""日志引用文件哈希一致"两条一致性检查；
4. **B3 追加非幂等**：曾产生同一凭证多条日志 → 改为按 sha256 幂等（历史重复条目按 append-only 保留并登记）；
5. **验证端独立性**：`vsa_verify_628` 重写为零 import 本项目工具（门禁静态分析强制）。

---

## 七、收工门禁结果

`python tools/run_628_gate.py --check` → **PASS**（15+ 检查项全绿）：
整目录 ruff / 12 工具 `--check` / mypy tools/ = 0 errors / 本批 82 测试 / 受控目录零污染 /
tool_integrity 尺子一致 / CORE_TOOLS 未修改 / V1=V2 数字一致且 flag 默认关 /
4 项技术债核查 / 他验三件套核查 / B1+B2 验证端零 import（静态分析）/ 镜像门 closed。
（门禁自带 `--no-tests` 防递归模式，由其单测覆盖；硬边界 1：监工门禁 gate/poison/replay/integrity --check 一律未跑。）

---

## 八、交人项（需人裁决）

1. **是否将 V2 flag 设为默认开启**（现为默认 V1，硬边界 13 禁止本批自作主张）；
2. **是否执行真实 Blind Review**（工具链就绪，独立人类确认强度 0/93）；
3. **是否 push**（本批 16 commits 仅在本地，硬边界 2）；
4. ref_missing 的 1 张 PCK（`ATOM-HIST-AUTOPTR-001`）：文件不存在，需人裁决（证据被删 or 路径变更）；
5. **118 条镜像边 sidecar** 的治理决策（缺 ReviewItem，无法自动证明）；
6. 他验三件套是否正式启用（是否引入非对称签名 + 外部密钥托管/公开 Rekor）；
7. 学习者镜像开门计划（需用户主动完成 50 次学习相关操作，当前 0）。

## 九、未做项（硬边界遵守声明）

本批**未跑监工门禁**、**未 push**、**未 golden accept**、**未打开 delegation**、**未代签人审**、
**未执行真实 Blind Review**、**未修改受控目录**、**未删除/修改任何 JSONL**（透明日志 append-only）、
**未判任何 PCK 失效**、**未把 V2 设为默认**、**未引入外部依赖**（三件套纯标准库、可视化无 Three.js）、
**未修改 CORE_TOOLS 生产逻辑**、**未做学习者镜像大规模建设**（门未开）、**未自己写 629 提示词**。
