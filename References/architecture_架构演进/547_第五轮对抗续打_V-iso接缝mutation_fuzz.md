# 547 · 第五轮独立对抗（续打）：专打 545 未饱和的 V-iso(B) / 接缝(C) / mutation_fuzz(D)

> 你是**独立对抗者**，与建设者不同模型族、零上下文。上一轮 545 只打了 L2 队列 A 面 3 个探针（A3/A5/A7，已确认真洞并交修复批 546），**B/C/D 面完全没打、明确声明未饱和**。本轮你的任务就是把没打的打完，**不要重复 A 面**。
>
> **仓库**：`C:\CodeLearnling\note\note\C++\CPP-Bible`，HEAD 以你 `git rev-parse HEAD` 实测为准（文档锚点会过期），Windows；门禁用 `.venv\Scripts\python.exe`；编译器 `C:\Qt\Tools\mingw1530_64\bin\g++.exe`。
> **纪律**：只读 + 探针全部落 `_adv_v95b/`；**不改正式文件、不 commit、不 push、不 accept**；开工先存 `git status` 基线，零污染自证。

## 第 0 步 · 摸基线 + 读上一轮
1. 读 `_adv_v95/REPORT.md` 和 `_adv_v95/probes/probe_l2_attacks.py`，确认 A3/A5/A7 已覆盖（546 已修：236b9fa/9be6f4f/7ee082b）——**本轮别再打这三个，也别打 A5b（已守住）**。
2. 读目标源码：`tools/viso_diff.py`、`tools/atom_evidence_replay.py` 阴性判决分支、`Examples/atoms/_atom_fence_vs_atomic.nc1.cpp`、`tools/mutation_fuzz.py`（**重点**；548 已做性能优化+M2 warn，判决逻辑仍是 543 现状）、`tools/task_queue.py`（只看 C 面接缝，不重复 A 面）。
3. 亲手复跑基线（548 后状态，别照抄）：gate **61 规则/block=0/warn=136/advice=5**、poison **92/92**、replay confirm=56、`pytest -m fast -q`（约 290）。**mutation 全量基线已落盘 `data/mutation/full_baseline_v1.json`**（83 卡×7 算子=1188 变体、严格拦截率 64.33%、escaped 227）——先读这份再打 D 面，别重复它已算过的。

## 攻击面 B · V-iso 阴阳同构（本轮重点之一）
- **B1 iso_judge 绕过**：阴面伪装 delete-only（等价替换/宏展开做到"删 1 行实则改语义"）；改动点靠路径/标签混淆算进 anchor；retain 逐字保留却被注释掉；Itanium 符号同源但偷换 static/inline；一行多语句同时满足"删 1–3 行/≤40token/≤2%"却改动巨大。
- **B2 翻转造假**：阴面"翻转"其实是阳面断言本身写错（恒真），系统能否区分？阳面恒真时阴面翻转是否无意义却被判 negative_control_passed。
- **B3 阴面不锚 sha**：阴面只差 .file 基名，能否借别卡/别优化级产物冒充自己的翻转证据。
- **B4 阴面编译失败归类**：写坏阴面是否正确归 `refute:negative_control_broken` 而非误算翻转成功；阳面 rc≠0 时阴面判决是否被错误豁免。
- **B5 YAML flow 走私**：negative_controls 要求块式。用 flow/全角/缩进提升藏假阴面（E07 缩进走私族在新字段复活？）。
- **B6 nc1 诚实性**：`阳=2 阴=0` 是否真由删 fence 导致？换 -O2/换符号名/删无关行，翻转是否仍只对 fence 敏感（排除"删啥都翻转"伪因果）。

## 攻击面 C · 新旧接缝
- C1 续跑/handoff 路径是否绕过 replay 的 P0-A 重编译不变量？
- C2 complete touch 审计的 SANDBOX_GLOBS 豁免（_arch_*/_adv_*）能否被利用——正式目录下起个 `_adv_x` 名字的文件混过审计？
- C3 task_queue 并发跑两个触发 replay 的任务，是否撞 replay 全局锁产生假失败/假成功。

## 攻击面 D · mutation_fuzz（全新工具，本轮最高优先）
> 它是"系统自己检验自己"的第一道闸——你若证明它的判决会撒谎，L3 进化闭环可信度就塌。
- **D1 双解析器不一致**：自检用 `_assert_targets` 判合法，gate 自己的 frontmatter 解析器却可能判另一种。构造在 `_assert_targets` 看来合法、在 gate 实际解析里被静默截断/吞掉的变体（全角键/Unicode/flow/块式差异），看它被误判 blocked 还是 escaped。
- **D2 n_a 藏身**：能否把真逃逸伪装成 `n_a(malformed/infra)` 不进分母（拦截率虚高）？或把没拦住的算成 blocked(strict)？
- **D3 算子诚实性**：算子声称"删了字段/改了 kind"，但变异后该字段因 block scalar 包裹/注释/别名仍生效（变异没真生效却报已变异）。建设者刚踩过"注入被 falsification block scalar 吞掉"，测 M1/M2/M5/M6/M7 有无同类。
- **D4 sandbox 整树复制失真**：跨卡规则（EV-ID-UNIQUE/serves/relations）在临时副本与真实仓命中是否一致？能否"真仓逃逸、sandbox blocked"或反之使报告失真。
- **D5 已知真洞组合**：M2 路径异体（6 条）+ M3 区间降级（4 条）能否组合绕开任何告警；M3 能否伪装合法形态骗过 malformed 闸。

## 方法学（必须做到）
- **两阶段**：先盲读列假设（phase1_hypotheses），再做探针，不许边读边改。
- 每发现挂**可复现命令+实际输出+源码行号+严重度**，三分类：**逃逸**（错误状态直推 verified/done）/ **仅 warn 可见化** / **设计内**。
- 已知别凑数：A3/A5/A7（546 已修）、E1 touch 大小写斜杠、mutation M4 假逃逸（malformed 闸已在）、**M2 跨平台路径已被 CARD-PATH-NOT-CANONICAL warn 收口（207→66，存量 0 误伤）**、**227 逃逸里约 66 条是"变异点落在注释/正文、门禁从不读"的无效提问（不是新洞）**、P0-A、人签单点、cl 免检、YAML 硬化、replay 刻意串行、ccache 1.22×、双解释器。
- **饱和就声明饱和**；本轮结束若 B/C/D 仍有没打的，明确列出"未覆盖清单"，不许假装打完。

## 交付（全在 `_adv_v95b/`）
1. `REPORT.md`：开头一句话"V-iso/mutation 里最脆的一环"；严格拦截率（逃逸/有效探针，warn 不算拦截）；每发现证据；对 533/534/543 设计论断的裁决。
2. `probes/`：可复跑探针 + run_all。
3. `zero_pollution.md`：git status/diff 证明正式目录零改动。
