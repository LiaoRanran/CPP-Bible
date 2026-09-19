# 545 · 第五轮独立对抗（实战版，取代 536）：L2 队列 + V-iso + 全新 mutation_fuzz（异族 / 零上下文）

> 你是**独立对抗者**，与建设者不同模型族、零上下文、不继承"我修好了"的结论。本仓有一批**从未被外部攻击过的新信任根代码**（L2 队列、V-iso、刚建的 mutation_fuzz），你的任务是击穿它。536 旧词的 A/B/C 攻击面仍有效，但锚点已更新、E1 已修——别拿已修项凑数。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD≈`205a377`，Windows；门禁用 `.venv\Scripts\python.exe`（PyYAML 6.0.3）；编译器 `C:\Qt\Tools\mingw1530_64\bin\g++.exe`（MinGW 15.3）。
> **纪律**：只读 + 探针全部落 `_adv_v90/`（或新建 `_adv_v95/`）；**不改任何正式文件、不 commit、不 push、不 accept**；零污染自证（开工前先存 `git status` 基线快照）。

## 第 0 步 · 自己摸基线（别信建设者汇报）
1. 读新代码：`tools/task_queue.py`（C1–C7 + E1 touch 归一化修复）、`tools/viso_diff.py`、`tools/mutation_fuzz.py`（**新，重点**）、`tools/atom_evidence_replay.py` 阴性判决分支、`Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`、对应测试。
2. 复跑基线记你亲手量的数：gate（60 规则 / block=0 / warn=136）、poison（90/90）、replay（confirm=56）、`pytest -m fast -q`（约 280）、`tools/mutation_fuzz.py --limit 2`（当前 escaped 10 / malformed 0 / 严格拦截率约 52.4%）。先确认绿，再打。
3. 读 `_arch_v3/`、`_arch_v2_round2/`、`_worklog_543.md` 了解设计意图——**实现是否真达成，以你探针为准**。

## 攻击面 A · L2 task_queue（信任根）
> 每个攻击给：构造、期望击穿点、可复现命令+输出、严重度。
- **A1 handoff 投毒**：verified_facts 锚点指向不存在行号/他卡；next_action 用近义字段名（next-step / 全角空格）绕校验；checkpoint 塞 verdict=confirm 被新会话当 L1 物证直接继承（违反"L2 判决必重跑"）。
- **A2 三级信任混淆**：规则/红队 verdict 伪装成 L1 物证类型被继承；"L1 哈希对、但内容是上个会话认真做错的"能否被续跑。
- **A3 租约/takeover 逃逸**：重放 claimed_token；不发心跳只改旧 heartbeat_at 保活；`--takeover` 不带/空 reason；两进程同时 takeover --force 是否只一个成；心跳写成未来时间永久占坑。
- **A4 touch 归一化（E1 已修，找残余）**：E1 已修"存 posix、比较时 normcase 折叠"。**别再报大小写/斜杠**（已 0/4）。找残余：符号链接、短名 8.3、通配符、`..` 穿越、subprocess 写文件、symlink 指向仓外、两路径 hardlink 同一 inode；declared 写了 posix 但实际改的是另一个大小写形式的 inode。
- **A5 yield 父子回卷**：父 done 子未全 done 是否也回卷成功；父子循环依赖死锁；yield 后 budget_used 被错误重置无限续命。
- **A6 并发建库极限**：建设者称退避后 240 轮零失败。压 20/50 进程冷启动、退避窗口内持续锁；user_version 能否被"旧库覆盖新 schema"降级。
- **A7 complete 验证自证**：verify_cmd 由 worker 自写，能否 `echo pass` / 恒 0；命令注入（`&& del`）；verify 过但产物是借品（编译真跑随后覆写，旧 F02 是否复活）。

## 攻击面 B · V-iso 阴阳同构
- **B1 iso_judge 绕过**：等价替换/宏展开做到"删 1 行实则改语义"；改动点靠路径/标签混淆算进 anchor；retain 逐字保留却注释掉；符号同源但换 static/inline；一行多语句凑"删 1–3 行/≤40token/≤2%"。
- **B2 翻转造假**：阴面翻转其实是阳面断言本身写错（恒真），系统能否区分？阳面恒真时阴面"翻转"是否无意义却被判 negative_control_passed。
- **B3 阴面不锚 sha**：阴面只差 .file 基名，能否借别卡/别优化级产物冒充翻转证据。
- **B4 阴面编译失败归类**：写坏阴面是否正确归 `refute:negative_control_broken`，而非误算"翻转成功"；阳面 rc≠0 时阴面判决是否被错误豁免。
- **B5 YAML flow 走私**：negative_controls 要求块式。用 flow/全角/缩进提升藏假阴面字段（复刻 E07 缩进走私族在新字段复活）。
- **B6 nc1 诚实性**：`阳=2 阴=0` 是否真由删 fence 导致？换 -O2/换符号名/删无关行，翻转是否仍只对 fence 敏感（排除"删啥都翻转"伪因果）。

## 攻击面 C · 新旧接缝
- C1 续跑路径是否绕过 replay 的 P0-A 重编译不变量？
- C2 complete touch 审计在真实仓列出未跟踪沙箱文件（_arch_*/_adv_*），会不会"永远有输出→worker 学会忽略"告警疲劳？（建设者已加 SANDBOX_GLOBS，测它漏不漏）
- C3 task_queue 并发跑两个触发 replay 的任务，是否撞上 replay 全局锁。

## 攻击面 D · mutation_fuzz（全新工具，没被打过，重点）
> 它是"系统自己检验自己"的第一道闸——你若能证明它的判决会撒谎，整条 L3 进化闭环的可信度就塌了。
- **D1 malformed 闸的双解析器不一致**：自检用 `_assert_targets` 判"合法"，但 gate 自己的 frontmatter 解析器可能判另一种。构造一个在 `_assert_targets` 看来字段合法、在 gate 实际解析里被静默截断/吞掉的变体（全角键/Unicode/flow/块式差异），看它被误判 blocked 还是 escaped。
- **D2 n_a 藏身**：能否把一个真逃逸伪装成 `n_a(malformed/infra)`，从而不进拦截率分母（让拦截率虚高）？或把实际没拦住的变体算成 blocked(strict)？
- **D3 算子诚实性**：算子声称"删了 X 字段/改了 kind"，但变异后该字段因 block scalar 包裹/注释/别名实际仍在生效（变异没真生效却报"已变异"）——建设者刚踩过"注入被 falsification block scalar 吞掉"，测别的算子有没有同类。
- **D4 sandbox 整树复制的失真**：跨卡规则（EV-ID-UNIQUE/serves/relations）在临时副本里的命中与真实仓是否一致？能否构造"真仓逃逸、sandbox 里却 blocked"或反之，使报告逃逸率失真。
- **D5 已知真洞组合**：M2 路径异体（6 条）+ M3 区间降级（4 条）——把 M2 的路径异体和别的攻击组合，能否绕开现有任何告警；M3 能否从 contains 变体伪装成合法形态，让 malformed 闸放过。

## 方法学（必须做到）
- **两阶段**：先盲读列假设（phase1_hypotheses），再做探针验证，不许边读边改。
- 每发现挂**可复现命令+实际输出+源码行号+严重度**，三分类：**逃逸**（错误状态下直推 verified/done）/ **仅 warn 可见化** / **设计内**。
- **新洞 vs 已知清单**：已知别凑数——E1 touch 归一化已修、mutation M4 假逃逸已修（malformed 闸在）、P0-A、人签单点、cl 免检、YAML 硬化、replay 刻意串行、ccache 1.22×、双解释器。
- **饱和就声明饱和**，打不穿明说，不许硬凑。

## 交付（全在 `_adv_v95/`）
1. `REPORT.md`：开头一句话"这批新代码最脆的一环"；严格拦截率（逃逸/有效探针，warn 不算拦截）；每发现证据；对 534/533/543 设计论断的裁决。
2. `probes/`：全部可复跑探针 + run_all 说明。
3. `zero_pollution.md`：`git status`/`git diff` 证明正式目录零改动（区分你开工前就存在的未跟踪文件）。
