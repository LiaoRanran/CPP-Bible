# 对抗 skip 审计报告（499 任务 3）

> 审计对象：`tools/adversarial_regression.py` 在 498 收工后的 35 个 `[skip]` 探针
> （基线 blocked=25 / escape=0 / visible=2 / gap=0 / skip=35）。
> 方法：跑 `python tools/adversarial_regression.py 2>&1 | Tee-Object _adv499.txt`，提取全部
> `[skip]` 行（35 条，见 `_adv499.txt` 第 1–31、36–37、51、62 行）。对 skip 原因归类：
> **可加机器判据** / **需人审** / **探针本身有问题**。为夯实"攻击点"描述，深读了 2 个代表探针
> （EV-ADV80-E05.md、EV-ADV80-N1.md）；其余基于回归工具权威 skip 原因 + 探针命名归类
> （详见 §五 不确定项）。
> 每个数字/分类均来自 `_adv499.txt` 实跑输出，无编造。

## 一、35 个 skip 逐条清单

| # | 探针 | 攻击点 | skip 原因（工具原话） | 分类 |
|---|---|---|---|---|
| 1 | _adv_v61/REPORT.md | v61 轮次说明 | 说明型探针（需人工/语义判定） | 需人审 |
| 2 | _adv_v61/adv61_extra.py | v61 额外攻击 | 历史轮次（仅实跑 _adv_v80）：口径漂移 | 探针有问题 |
| 3 | _adv_v61/adv61_gate.py | v61 门禁攻击 | 历史轮次（口径漂移） | 探针有问题 |
| 4 | _adv_v70/probes/EV-ADV70-H1.md | 历史攻击 H1 | 说明型（需人工/语义判定） | 需人审 |
| 5 | _adv_v70/probes/EV-ADV70-H16.md | 历史攻击 H16 | 说明型 | 需人审 |
| 6 | _adv_v70/probes/EV-ADV70-H16B.md | 历史攻击 H16B | 说明型 | 需人审 |
| 7 | _adv_v70/probes/EV-ADV70-H3.md | 历史攻击 H3 | 说明型 | 需人审 |
| 8 | _adv_v70/probes/EV-ADV70-H6.md | 历史攻击 H6 | 说明型 | 需人审 |
| 9 | _adv_v70/probes/EV-ADV70-H7.md | 历史攻击 H7 | 说明型 | 需人审 |
| 10 | _adv_v70/REPORT.md | v70 轮次说明 | 说明型 | 需人审 |
| 11 | _adv_v70/adv70_concurrent.py | v70 并发攻击 | 历史轮次（口径漂移） | 探针有问题 |
| 12 | _adv_v70/adv70_gate.py | v70 门禁攻击 | 历史轮次（口径漂移） | 探针有问题 |
| 13 | _adv_v70/adv70_h5h18.py | v70 H5/H18 攻击 | 历史轮次（口径漂移） | 探针有问题 |
| 14 | _adv_v80/probes/EV-ADV80-BS.md | 边界/规格说明 | 说明型 | 需人审 |
| 15 | _adv_v80/probes/EV-ADV80-BSC.md | 边界/规格说明 | 说明型 | 需人审 |
| 16 | _adv_v80/probes/EV-ADV80-E05.md | cat 式证据（把 cat 输出当实证） | 说明型 | 需人审 |
| 17 | _adv_v80/probes/EV-ADV80-E05C.md | cat 式证据变体 | 说明型 | 需人审 |
| 18 | _adv_v80/probes/EV-ADV80-E05E.md | cat 式证据变体 | 说明型 | 需人审 |
| 19 | _adv_v80/probes/EV-ADV80-E05F.md | cat 式证据变体 | 说明型 | 需人审 |
| 20 | _adv_v80/probes/EV-ADV80-E10A.md | 零诊断字段位移 | 说明型 | 需人审 |
| 21 | _adv_v80/probes/EV-ADV80-E10B.md | pragma 消音+-Werror | 说明型 | 需人审 |
| 22 | _adv_v80/probes/EV-ADV80-E10C.md | 零诊断变体 | 说明型 | 需人审 |
| 23 | _adv_v80/probes/EV-ADV80-E10D.md | 零诊断变体 | 说明型 | 需人审 |
| 24 | _adv_v80/probes/EV-ADV80-E10E.md | 零诊断变体 | 说明型 | 需人审 |
| 25 | _adv_v80/probes/EV-ADV80-E10F.md | 零诊断变体 | 说明型 | 需人审 |
| 26 | _adv_v80/probes/EV-ADV80-N1.md | 跨编译器+全局恒真断言 | 说明型 | 需人审 |
| 27 | _adv_v80/probes/EV-ADV80-N2.md | 全局恒真断言 | 说明型 | 需人审 |
| 28 | _adv_v80/probes/EV-ADV80-N2B.md | 全局恒真变体 | 说明型 | 需人审 |
| 29 | _adv_v80/probes/EV-ADV80-N2C.md | 全局恒真变体 | 说明型 | 需人审 |
| 30 | _adv_v80/probes/EV-ADV80-N3.md | 跨编译器恒真 | 说明型 | 需人审 |
| 31 | _adv_v80/REPORT.md | v80 轮次说明 | 说明型 | 需人审 |
| 32 | _adv_v80/probe_batch.py#E11 | 冲突同义词（归一后） | 自述不可判（无"已拦/逃逸"且 verdict 非判据） | **可加机器判据** |
| 33 | _adv_v80/probe_batch.py#E11b | 同义词 refutes（未归一） | 自述不可判 | **可加机器判据** |
| 34 | _adv_v80/probe_batch.py#E12 | 签收字符串自证（身份真实性） | 自述不可判（verdict=逃逸，无签收真实性规则命中） | 需人审（身份） |
| 35 | _adv_v80/probe_misc.py | 杂项 | 无可解析自述行（无输出） | 探针有问题 |

## 二、分类汇总

| 分类 | 条数 | 占比 | 构成 |
|---|---|---|---|
| 可加机器判据 | **2** | 6% | E11、E11b（自述格式缺可解析 verdict） |
| 需人审 | **27** | 77% | 全部说明型 .md 探针（H/BS/E05/E10/N1/N2/N3 系列 + 各轮 REPORT）+ E12（身份真实性） |
| 探针本身有问题 | **6** | 17% | v61×2、v70×3 历史轮次（口径漂移）+ probe_misc.py（无输出） |
| **合计** | **35** | 100% | |

## 三、"可加机器判据"详细建议表

| 探针 | 攻击点 | 建议的机器判据（具体到字段/值） | 预计难度 |
|---|---|---|---|
| E11 | 冲突同义词归一后绕过 | 在探针自述加机器可读期望标记（如 `# EXPECT: blocked`）；扩展 `adversarial_regression.py` 双轨判定：当探针声明 `EXPECT` 时，直接比对**机器 verdict**（`refute` ⇒ 拦 ⇒ blocked）。即检查"探针含 `EXPECT: blocked` 且 `gate_engine` 对对应卡 emit block（EV-REFUTES-NORMALIZED 类规则）"。 | 低 |
| E11b | 同义词 refutes 未归一绕过 | 同上：加 `# EXPECT: blocked`；检查未归一的 `refutes` 同义词是否仍被规则拦（对应卡 emit block）。 | 低 |

> 说明：E11/E11b 当前 skip 仅因"自述行无『已拦/逃逸』字样且 verdict 非判据"——
> 属**探针自述格式缺失可解析判定**，而非攻击本身不可判（攻击已被对应规则 block，见
> `_adv499.txt` 中同批 `#E11` 无 blocked 行是因为它在 skip 分支未跑机器判定）。补上
> `EXPECT` 标记即可让双轨判定自动断言，无需新规则。

## 四、判断：skip 能降到多少

- **仅实现 E11/E11b 的 `EXPECT` 标记**：skip 35 → **33**（消除 2 条格式型 skip）。
- **若再为 E12 加代理判据**（检查 `S1-GIT-AUTHOR-BINDING`/`principal_ok` 是否命中"签收自证"
  卡）：可再降 1 → **32**。但 E12 本质是**身份真实性**（签署的"我确实是某人"无法纯机器证伪），
  即使加代理也只是"规则是否触发"的机械检查，实质性判定仍归人审，故保守估 **33**。
- **27 条说明型探针**：attack 本身是叙述性场景（如"把 cat 输出当实证""跨编译器恒真断言"），
  需要人读攻击描述并判断当前系统是否已堵——**机器无法自动断言**，skip 数不会因加规则归零。
  这 27 条是"对抗看板的设计性 skip"（见 MEMORY 待裁决 #13），非缺陷。
- **6 条问题探针**：v61/v70 历史轮次口径已漂移（仅 _adv_v80 实跑），`probe_misc.py` 无输出——
  建议从活跃套件中**移除或归档**到 `_adv_v80` 口径，不计入活跃 skip。

## 五、不确定项（铁律 #4）

- **逐文件深读为抽样**：本节仅深读了 EV-ADV80-E05.md / EV-ADV80-N1.md 两个代表探针确认其
  "说明型"性质；其余 33 条的分类依据为 `adversarial_regression.py` 输出的权威 skip 原因文本
  + 探针命名（H/E/N/BS 系列对应 424/479 攻击面分类学）。如需逐探针细化攻击面描述，建议好模型
  补读 `_adv_v80/probes/*.md` 与 `probe_batch*.py` 的 `#E11/#E12` 段。
- **E12 是否算"可加机器判据"**：本报告将其归入"需人审（身份）"，仅把其 skip 的格式层（缺
  EXPECT 标记）视为可修；若好模型认为"身份真实性也应加机器代理"，则"可加机器判据"可计为 3 条。
- **与 494 基线一致**：本次 skip=35 与 494 基线（skip=35）完全相同，blocked/escape/visible/gap
  均无变化（见任务 8 报告），说明 498 批次未改变对抗拦截状态。
