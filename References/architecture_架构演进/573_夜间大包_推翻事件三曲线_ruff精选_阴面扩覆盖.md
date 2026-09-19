# 573 · 夜间大包（扩展版）：元系统内核深化五件事

承接 `0a4dc80`（572，监工已亲验 M3 逃逸 0/65、断言数基线、poison 114/114）。解释器只用 `.venv\Scripts\python.exe`；**一任务一 commit；做不完停任务边界、不留半成品；不 push、不 golden accept；护栏不许裸 except；不编数字、跑多少报多少**。五件事按下面顺序串行，中间不等确认；每件都先量后动、warn 起步、存量零误伤。

## 任务 0（开工先量）
fresh 跑 gate（63 条·141·block=0 warn=136 advice=5）、poison（114/114）、replay（confirm=56）、`tool_integrity --check`（exit 0）、pytest fast。不符先记 worklog，不在脏基线叠加。

---
## 任务 B（先做，清干净基线）：ruff 精选族清零
实测 `--select ALL` = 2 万+，绝大多数是噪声。**永久不开**（配置注释写理由）：`RUF001/002/003`（中文歧义字符 2 万）、`T201`（CLI 本就 print）、`S101`（测试本就 assert）、`CPY001`（版权头）、`D*`/`ANN*`（docstring/类型，另议）、`Q000`（引号 churn）。
1. 安全自动修族，**逐族 `--fix`、逐族独立 commit、每族后跑 pytest 确认无行为变化**：`I001`（import 排序）、`PTH123`（builtin-open→Path.open）、`PTH118`（os.path.join→/）、`FURB167`（regex flag 别名）。
2. subprocess 安全族 `PLW1510`（run 无 check）、`S603`（shell=True）**只出审计报告不改逻辑**（570 刚踩 subprocess 坑，自动加 check 会改行为）：逐处列"文件:行:是否真需容错"交人。
3. 钉最终 select，启用族 `ruff check tools/ tests/` = 0。后续任务的新代码必须直接过启用族。

## 任务 A：三曲线从占位变真数据 + overturned 事件通道
现状（已侦察）：`metrics_collector.py::collect_curves()`（约 334 行）字段已埋，但 ① 逃逸率仍读 **v1（0.237，尺子修前虚高）**；② overturned 恒 0 无写入路径；③ survival 恒 null。
1. 逃逸率更新到 **v2**（`data/mutation/full_baseline_v2.json`，修 GATE_READ_KEYS 后；M2/M3=0）：重算 point + 双侧 C-P95（stat_bounds，可判分母=blocked+escaped，warn_only 不入严格分子）。v1 作历史时点保留不覆盖。
2. **overturned 写入 CLI**（只接人/异族动作，系统绝不自动推翻）：schema = 命题/卡 id、旧判决、新判决、推翻者身份版本（`human:<名>`/`adversary:<族>`）、时间、理由；落 `data/overturned_events.jsonl` 只追加；**human 推翻者名过 git 作者绑定，无签名拒绝写入（fail-closed）**；collect_curves 读它计数。
3. 第一批 survival 真实数据（不编）：只有 **M3 的 52 条 = 571 产生→572 收口，survival=1 批**；M2 的 207 是 GATE_READ_KEYS 尺子 bug 的假逃逸（571 证实），**不计入**；其余 null。
- pytest 锁：v2 point、事件 schema、无签名拒写、survival 只数 M3。

## 任务 D（元系统核心预留）：信任放权门——只写不读、默认不放权
现状（已侦察）：全仓 44 个工具里 `verified_by_oracle`/`oracle_version` **0 出现**，562 留的口子连字段都没有。本任务**只建接口、绝不现在放权**：
1. 卡/命题 frontmatter 加可选 `verified_by_oracle:`（oracle 名、版本、verified_at、scope）；建 `data/oracle_registry.json` 记录当前认可的验证者版本（如 gcc-15.3.0、规则引擎版本）。
2. **只写不读是硬不变量**：gate/replay/poison 的**判决逻辑一律不许读这个字段**（读了就是偷偷放权）。加一条 pytest 锁：给卡填任意 verified_by_oracle，gate/replay 的 block/warn/confirm 判决逐字不变。
3. **版本绑定 fail-closed（只在报告层）**：metrics/报告可读该字段做统计；当 registry 里的 oracle 版本升级，旧 verified_by_oracle 在报告层标 `stale`（黄），但**不改变任何判决**（因为本来就没放权）。
4. G-iso 等放权开关仍默认 OFF；本任务不实现任何"机器自动接受"。
- 这是为"模型变强那天"预留的插槽：现在纯记录 + 证明"写了也不影响判决"。pytest 锁：只写不读、版本过期标 stale、无字段正常、开关全 OFF。

## 任务 E：诊断并修 M5 算子（尺子盲区，像 571 修 M3 那样）
现状：M5 = claim 自标（inference→observation，测 OBSERVATION-LIVENESS 活性闸），但 v2 基线 M5 = 0/0/83 **全 n_a**。
1. **先诊断别硬改**：`mut_m5` 的正则 `^(\s*)claim_type:\s*(\w+)\s*$` 只匹配**卡面顶层** claim_type；而 29 条 inference 命题在 `claim_structured[*].claim_type` 里。逐卡打印：M5 变异到底改没改到 inference 命题？是"卡本就是 observation 无变化"（真 n_a）还是"正则没匹配、变异没生效"（算子 bug）？
2. 若是算子 bug：让 M5 能把 `claim_structured` 里的 inference 命题改成 observation（幂等、纯函数、原卡零改动，沿用其他算子范式）。
3. 修后重跑 M5：inference 命题被自标成 observation 后，**应被 530 T3 的 OBSERVATION-LIVENESS 闸拦（blocked 或 warn_only）**；若仍逃逸，说明活性闸有真洞，如实登记（不替它补规则，交下一批）。
4. **不硬凑可判样本**：若诊断发现 M5 天然只对少数卡有意义，如实报可判数与 C-P 区间，M5 不足 59 就标 insufficient。
- pytest 锁：M5 对 inference 卡产生真变异、对 observation 卡 n_a、算子纯函数原卡字节不变。

## 任务 C（最后做，最重最易歪）：V-iso 阴面扩覆盖，样板 3 张
现状：57 卡只有 EV-CONC-001 真阴面；19 张 run_match 卡是候选池。
1. C0：复跑 iso_judge/replay，确认 EV-CONC-001 阴面仍 flip verified。
2. 从 19 张里**只挑 3 张**机制最清晰、可单变量干预的（worklog 写明选卡理由），各造真阴面：claim 拆 anchor/remove/retain，阴面=定点删机制依赖的 1–3 行，断言必须在阴面**翻转失败**。
3. 每张过 viso_diff.py 全部判据（delete-only/单 hunk/1–3 行/≤40 token/改动率≤2%/删除点 100% 在 anchor/remove 命中/retain 逐字/Itanium 符号同源/实测翻转）；形式阴面（不翻转、冒名、多变量、注释走私）机器必拒。
4. 每张独立 commit + replay 翻转留证；**做不完 3 张停在已完成张数，判据一条不降**；登记"结构性做不出单变量运行级阴面"的卡（如纯存在性卡）。

---
## 收工总验收（fresh）
- gate 63 条·命中不新增存量（block=0）· poison 114/114 · replay confirm=56 · `--check` exit 0 · 启用 ruff 族 0 · pytest fast/slow 绿 · 受控目录零残留；
- A：v2 point 贴数（反映 M2/M3=0）、overturned CLI 无签名拒写、survival=M3 一批；
- B：每自动修族独立 commit 且 pytest 绿、subprocess 审计报告落盘；
- D：verified_by_oracle 只写不读有**判决逐字不变**的锁、版本过期仅报告层 stale、放权开关全 OFF；
- E：M5 诊断结论（真 n_a vs 算子 bug）贴证据，修后重跑 M5 数字；
- C：新增阴面张数 + 每张 replay 翻转证据 + iso_judge 全过；
- 改 CORE_TOOLS 同 commit `--update` 重钉；写 `_worklog_573.md`（任务 0 基线、各任务改前改后贴数、选卡/选族理由、偏差表、做不完停在哪）。

## 硬纪律
- overturned 与放权门**绝不自动产生判决/绝不自动放权**（自动 LLM 推翻、LLM-as-judge 在冻结档）；人签 fail-closed；
- ruff 不开中文/print/assert/docstring/引号族，不做纯 churn；
- M5 不硬凑样本、阴面宁少勿假；
- 不做：自动 KG、PoC#3/#4/#5（等 trae）、golden fork、测试选择/按卡裁剪（548 钉死跨卡不许裁剪）、给全 56 卡硬塞阴面。
