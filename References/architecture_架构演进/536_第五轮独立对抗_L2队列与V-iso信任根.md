# 536 · 第五轮独立对抗：专攻 535 新落地的 L2 队列 + V-iso 信任根（异族 / 零上下文）

> 你是**独立对抗者**，与建设者不同模型族、零上下文、不继承"我修好了"的结论。本仓刚在一夜之间新增近 2000 行**从未被外部攻击过的信任根代码**，你的任务是击穿它。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`ee1d7c8`，Windows；门禁用 `.venv\Scripts\python.exe`（PyYAML 6.0.3）；编译器 `C:\Qt\Tools\mingw1530_64\bin\g++.exe`（MinGW 15.3）。
> **纪律**：只读 + 探针全部落 `_adv_v90/`；**不改任何正式文件、不 commit、不 push、不 accept**；零污染自证。

## 第 0 步 · 自己摸基线（别信建设者汇报）
1. 读这批新代码：`tools/task_queue.py`（1383 行，C1–C7）、`tools/viso_diff.py`（356 行）、`tools/atom_evidence_replay.py` 的阴性判决分支、`Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`、对应 `tests/test_task_queue.py` 与 viso 测试。
2. 复跑基线并记你亲手量的数：gate / poison / replay（confirm=56）/ `pytest -m fast -q`（约 274）。先确认绿，再开始打。
3. 读 `_arch_v3/534_L2调度层施工规格.md`、`_arch_v2_round2/533_V-iso施工规格.md` 了解设计意图——但**实现是否真达成，以你探针为准**。

## 攻击面 A · L2 task_queue（信任根，重点）
> 目标：找出"每一步都合规、组合起来却能让错误结果/越权接管/数据损坏通过"的链。每个攻击给：构造、期望击穿点、机器判据（命令+输出）。

- **A1 handoff 投毒**：verified_facts 的锚点指向不存在的行号/文件/别的卡，fail-closed 能否拦住？next_action 缺失但用近义字段名（next-step / next_action 带全角空格）能否绕过校验？checkpoint 里塞一个 verdict=confirm 让新会话当成 L1 物证直接继承（违反"L2 判决必重跑"）。
- **A2 三级信任混淆**：把规则结论/红队 verdict 伪装成 L1 物证（编译产物）类型，续跑时是否被错误继承？构造"L1 哈希对、但内容是上个会话认真做错的"场景，看新 worker 会不会把错续下去。
- **A3 租约与 takeover 逃逸**：伪造/重放 claimed_token；不发心跳但反复 touch 一个旧 heartbeat_at 保活；`--takeover` 不带 `--reason` 或 reason 为空是否也能接管；两个进程同时 `--takeover --force` 是否只一个成功；心跳时间戳能否被写成未来时间永久占坑。
- **A4 touch_set 归一化绕过**：声明 touch_set 不含真实改的文件，用大小写/`./`/反斜杠正斜杠/符号链接/短名 8.3/通配符/子进程写文件，complete 的 touch 审计能否发现？改的是 touch_set 内文件但内容写到其 symlink 指向的仓外文件呢？
- **A5 yield 父子回卷**：父任务 done 时子任务并未全 done 是否也回卷成功？构造父子循环依赖（A 拆出 B、B 又拆出 A）能否死锁或永久 pending；yield 后 budget_used 是否被错误重置导致无限续命。
- **A6 C1 并发建库的极限**：建设者称修后 240 轮零失败（显式退避重试）。你压更高并发（20/50 进程同时冷启动）、或在退避窗口内制造持续锁，看是否仍 `database is locked / duplicate column`；`user_version` 版本门能否被"旧版本库覆盖新 schema"降级。
- **A7 complete 验证自证**：verify_cmd 由 worker 自己写，能否写成 `echo pass` / 退出码恒 0 的无害命令？verify_cmd 里塞命令注入（`&& del ...`）；verify 过了但产物是借品（编译行真跑、随后覆写，旧 F02 形态在新 complete 流程里是否复活）。

## 攻击面 B · V-iso 阴阳同构（新机制）
- **B1 iso_judge 判据绕过**：阴面伪装 delete-only（用等价替换/宏展开做到"删 1 行实则改语义"）；改动点在 anchor 外但靠路径/标签混淆算进 anchor；retain 文本逐字保留却被注释掉；Itanium 符号同源但偷偷换 static/inline 改变链接；一行塞多条语句使"删 1–3 行 / ≤40 token / ≤2%"同时满足却改动巨大。
- **B2 翻转造假**：阴面"断言翻转"其实是测试本身写错（阳面断言就错），而非机制被破坏——系统能否区分？阳面本身是恒真断言时，阴面的"翻转"是否毫无意义却被判 negative_control_passed？
- **B3 阴面不锚 sha 的可乘之机**：既然阴面永不锚 sha（只差 .file 基名），能否让阴面借用别的卡/别的优化级产物冒充自己的翻转证据？
- **B4 阴面编译失败归类**：故意把阴面写坏，是否被正确归 `refute:negative_control_broken`，还是能被误算成"翻转成功"？阳面 rc≠0 时阴面判决会不会被错误豁免？
- **B5 YAML flow 走私**：规格要求 negative_controls 必须块式（零依赖解析器对跨行 flow map 静默截断）。攻击者故意用 flow / 全角 / 缩进提升，把一个假阴面字段藏到解析器看不见、却能在文本层"看起来有阴面"——复刻缩进走私（E07）族在新字段上是否复活。
- **B6 nc1 样板自身的诚实性**：`阳=2 阴=0 flip` 是否真由"删 fence"导致？换成 -O2 / 换符号名 / 删掉无关行，翻转是否仍稳定只对 fence 敏感（排除"删啥都翻转"的伪因果）。

## 攻击面 C · 新旧接缝
- C1 三级信任与既有 gate/replay 的交互：续跑路径会不会绕过 replay 的 P0-A 重编译不变量？
- C2 complete touch 审计在真实仓库会列出既有未跟踪沙箱文件（`_arch_*/_adv_*`）——这会不会造成"审计永远有输出→worker 学会忽略"的告警疲劳？给正式豁免规则建议，但**别替建设者改**。
- C3 task_queue 与 replay 共享 build/ 瞬时态：队列并发跑两个都触发 replay 的任务，会不会撞上已被 508 证明的 replay 全局锁问题？

## 方法学（沿用成熟套路，必须做到）
- **两阶段**：先盲读列假设（phase1_hypotheses），再做探针验证，不许边读边改结论。
- 每个发现挂**可复现命令 + 实际输出 + 源码行号 + 严重度**，并三分类：**逃逸**（卡/任务能在错误状态下直推 verified/done）/ **仅 warn 可见化** / **设计内行为**。
- 区分**新洞** vs **已知清单重复**（已知：P0-A、人签单点、cl 免检、YAML 硬化、replay 刻意串行、ccache 1.22×、双解释器——别拿这些凑数）。
- **饱和就声明饱和**，某个攻击面打不穿就明说，不许硬凑。

## 交付（全在 `_adv_v90/`）
1. `REPORT.md`：开头一句话给"这批新代码最脆的一环"；严格拦截率（逃逸数/有效探针数，口径同 v80：warn 不算拦截）；每个发现的证据；对 534/533 设计论断的裁决（哪些成立、哪些被证伪）。
2. `probes/`：全部可复跑探针 + 一份 `run_all` 说明。
3. `zero_pollution.md`：`git status`/`git diff` 证明正式目录零改动（开工前先存基线快照，区分你开工前就存在的未跟踪文件）。
