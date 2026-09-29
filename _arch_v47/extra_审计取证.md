# 方向 90：安全审计与取证（Security Audit & Digital Forensics）方法

> 调研日期：2026-09-29。目标：为阙疑建立一套"可被第三方审计"的工程范式——审计层面回答"这个验证系统本身会不会撒谎"（威胁建模 STRIDE、红队、模糊测试 fuzzing、差分测试 differential testing）；取证层面回答"谁在何时改了哪条判决"（append-only 账本 + Merkle checkpoint，方向 64/65 的完整性机制如何转化为事后取证能力）。

---

## 核心结论

1. **审计方法论有成熟的三层组合**：威胁建模（Microsoft 于 1990 年代末提出 STRIDE，将威胁分为 Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege 六类，微软官方威胁建模工具页逐字定义了每类）→ 主动攻击测试（红队 / fuzzing / 差分测试）→ 持续验证（append-only 日志 + Merkle 一致性证明）。RFC 6962 §1 逐字写道：*"Certificate transparency aims to mitigate the problem of misissued certificates by providing publicly auditable, append-only, untrusted logs of all issued certificates."*——"publicly auditable + append-only + untrusted"三个形容词正是阙疑独立对账器应追求的定性。
2. **fuzzing 与差分测试在"验证工具的正确性"上有压倒性实证战绩**：Google OSS-Fuzz 官方文档逐字记载 *"As of August 2023, OSS-Fuzz has helped identify and fix over 10,000 vulnerabilities and 36,000 bugs across 1,000 projects."*；Utah 大学 Yang 等（PLDI 2011）用 Csmith 对 C 编译器做差分测试，论文逐字写明 *"For the past three years, we have used Csmith to discover bugs in C compilers... we have found and reported more than 325 bugs in mainstream C compilers including GCC, LLVM, and commercial tools"*——连形式化验证过的 CompCert 也被 Csmith 在未验证部分找到了静默错译 bug。这证明"验证器本身也是软件，也需要被验证"，对 3826 行的 `gate_engine.py` 完全适用。
3. **取证的关键不是"不可篡改"而是"篡改必留痕且可被第三方检出"**：RFC 6962 §7.3 逐字指出日志的两种作恶方式——*"A log can misbehave in two ways: (1) by failing to incorporate a certificate with an SCT in the Merkle Tree within the MMD and (2) by violating its append-only property by presenting two different, conflicting views of the Merkle Tree at different times and/or to different parties. Both forms of violation will be promptly and publicly detectable."* 阙疑的 452 条判决账本只要（a）每条记录 actor+时间戳+prev_hash，（b）定期出 Merkle checkpoint 并对外公布树根，（c）保留一份只读镜像供第三方对账，就能把"谁在何时改了哪条判决"变成一次 O(log n) 的包含证明（inclusion proof）+ 一致性证明（consistency proof）查询。

---

## 精确数字与案例

### 一、威胁建模：STRIDE 六类如何映射到"验证系统"

Microsoft Learn 的威胁建模工具页（Threat Modeling Tool 是 Microsoft SDL 的核心组件）对六类威胁给出逐字定义（已用 WebFetch 核实原文）：

| STRIDE 字母 | 微软官方逐字定义（节选） | 阙疑场景下的对应攻击面 |
|---|---|---|
| **S**poofing（仿冒） | *"Involves illegally accessing and then using another user's authentication information"* | 攻击者伪造"作者身份"写入知识卡/判决；无签名的卡片来源不可信 |
| **T**ampering（篡改） | *"Involves the malicious modification of data... unauthorized changes made to persistent data"* | 静默修改已 verified 卡片的规则命中结果；改 452 条账本中的历史判决 |
| **R**epudiation（抵赖） | *"Associated with users who deny performing an action without other parties having any way to prove otherwise"* | 判决出错后，作者声称"不是我改的/我没有跑过这次判定"；账本无 actor 字段则无法反驳 |
| **I**nformation Disclosure（信息泄露） | *"Involves the exposure of information to individuals who are not supposed to have access to it"* | 盲 holdout 30 条的答案泄露进上下文，导致检出率虚高 |
| **D**enial of Service（拒绝服务） | *"deny service to valid users"* | 对账器被喂入截断账本/巨型输入导致复算失败或超时 |
| **E**levation of Privilege（提权） | *"An unprivileged user gains privileged access... and become part of the trusted system itself"* | 9 个保护器之一被关闭或被替换为恒过（always-pass）实现，且无人察觉 |

**方法论要点**：STRIDE 由 Microsoft 的 Praerit Garg 和 Loren Kohnfelder 于 1990 年代末提出（CSDN 中文资料引述其出处；原始论文《The Threats to Our Products》未直接获取，标注为未核实）。对阙疑的操作化做法：画一张数据流图（知识卡 → gate_engine → 账本 → checkpoint → 第三方对账器），对每条数据流和存储逐一过 S/T/R/I/D/E 六问，产出威胁登记表（threat register）。微软页面强调该工具 *"designed... with non-security experts in mind"*——单人科研项目的作者完全可用。

### 二、模糊测试与差分测试：验证"验证器"的实证战绩

**OSS-Fuzz（Google，2016 年因 Heartbleed 而设立）**。官方文档（google.github.io/oss-fuzz，已 WebFetch 核实）逐字写明：

> *"As of August 2023, OSS-Fuzz has helped identify and fix over 10,000 vulnerabilities and 36,000 bugs across 1,000 projects."*

支持引擎为 libFuzzer、AFL++、Honggfuzz、Centipede，配合 sanitizer 运行。2024 年 11 月腾讯云社区报道 Google 的 AI 增强模糊测试发现 26 个零日漏洞，含 OpenSSL 的 CVE-2024-9143（转述自 Google 公告，原文未直接核实）。另有 arXiv 2025 年的大规模实证分析（arXiv:2510.16433）称 36% 的 OSS-Fuzz 项目在首轮持续 fuzzing 中就检出至少一个 bug（来自检索摘要，未逐字核实原文表格）。

**Csmith 差分测试（PLDI 2011，Utah 大学 Yang/Chen/Eide/Regehr）**。已下载论文 PDF 并逐字核实：

> *"For the past three years, we have used Csmith to discover bugs in C compilers. Our results are perhaps surprising in their extent: to date, we have found and reported more than 325 bugs in mainstream C compilers including GCC, LLVM, and commercial tools."*

以及（同样逐字核实）：

> *"Using Csmith, we found previously unknown bugs in unproved parts of CompCert—bugs that cause this compiler to silently produce incorrect code."*

**差分测试的通用结构**：生成器产生合法输入 → 被测系统与其"等价实现"各自处理同一输入 → 输出不一致即报 bug。对 C 编译器是"多编译器互查"；对阙疑就是"内核 gate_engine.py vs 不依赖内核的独立对账器互查"——这正是项目锚点里已经写明的机制，缺的只是把它制度化成持续跑的差分 harness。

**模糊测试工具谱系**（LLVM 官方文档 / AFL++ GitHub）：libFuzzer 是进程内覆盖率引导 fuzzing 库（LLVM 文档："LibFuzzer is linked with the library under test, and feeds fuzzed inputs to the library via a specific fuzzing entrypoint"）；AFL++ 是 AFL 的社区维护后继。Python 项目的对应物是 Atheris（基于 libFuzzer 的 Python fuzzer）与 Hypothesis（基于性质的测试，property-based testing）——后者对 `gate_engine.py` 这类规则引擎更贴合（详见行动 2）。

### 三、红队审计：从 LLM 红队到"判决红队"

**LLM 红队综述的量化规模**：JAIR 2025 年综述《Against The Achilles' Heel: A Survey on Red Teaming for Large Language Models》自述 *"examines over 120 papers, introduces a taxonomy of fine-grained attack strategies"*（检索摘要，未逐字核实全文）；arXiv:2410.09097 是另一篇 2024 年 12 月的 LLM 红队技术与防御综述。中文侧，复旦白泽智能 2023 年 11 月发布 JADE DB v2.0（JADE-DB-Easy / JADE-DB-Medium 各 1000 个通用测试问题，来源：安全客 secrss.com）；2026 年 1 月有 RedBench（Hugging Face 论文页 2601.03699，号称大模型全面红队通用数据集）。

**红队方法论的可迁移要点**：
- 红队的产出不是"修复清单"而是**攻击成功率的分布**——阙疑已有 3 张 red-team 卡和反事实算子 P=R=F1=0（待修）的现状，说明"红队产物"存在但没有制度化度量。
- 红队需要**多样性来源**（人工假设 + 自动化生成 + 第三方参与者），单一作者的红队会被自己的盲区限制——因此论文阶段应公开红队邀请（Responsible Disclosure 式）。
- 红队结果必须**入账本**：每次红队攻击作为一条 append-only 记录（攻击输入、期望、实际判决、是否绕过），否则红队结论本身不可信。

### 四、append-only 账本 + Merkle checkpoint 如何支撑事后取证

**密码学基础（RFC 6962，Certificate Transparency，Google 2012，已 WebFetch 核实）**：
- §1 逐字：*"Certificate transparency aims to mitigate the problem of misissued certificates by providing publicly auditable, append-only, untrusted logs of all issued certificates."*
- §1 逐字：*"The logs do not themselves prevent misissue, but they ensure that interested parties... can detect such misissuance."*——**取证系统的定位是"检出"而非"阻止"**，这个措辞应原样写进阙疑论文的 limitations。
- §2.1.1 是 Merkle Audit Paths（对单条判决的包含证明，O(log n)），§2.1.2 是 Merkle Consistency Proofs（对整个日志历史的一致性证明，证明"新树根是旧树根的延伸、没有偷偷改历史"）。
- §7.3 逐字列出日志的两种作恶方式（见核心结论 3），并断言 *"Both forms of violation will be promptly and publicly detectable."*

**工程实现参考**：
| 项目 | 机构 | 与阙疑的关系 |
|---|---|---|
| Google **Trillian** | Google（google.github.io/trillian） | *"an implementation of the concepts described in the Verifiable Data Structures white paper, which in turn is an extension and generalisation of the ideas which underpin Certificate Transparency"*——通用 Merkle 树透明日志数据库 |
| **Rekor** | Sigstore | 软件供应链透明日志，CLI *"make and verify entries, query the transparency log for inclusion proof, integrity..."*（GitHub README）——阙疑 checkpoint 可仿其"记录+包含证明+完整性验证"API 形态 |
| 通用篡改留痕日志 | 多家（zatona.dev、praesidia.ai 等工程文章） | 哈希链 + 签名 Merkle 证明；注意术语是 **tamper-evident（篡改可检）而非 tamper-proof（防篡改）** |

**国内合规侧锚点**：等级保护基本要求《GB/T 22239-2019 信息安全技术 网络网络安全等级保护基本要求》对审计日志有明确要求；CSDN 问答社区（2026-04）提到关键操作日志留存不足 180 天（部分场景要求 ≥5 年）是常见不合规项；掘金文章（2026-06）称公安部 GA/T 2380-2026 标准实施、数据安全纳入等保独立控制域（此两条为中文技术社区转述，标准原文未直接核实——标注）。意义在于：阙疑若把"账本留存 ≥180 天 + UTC 时间戳 + 不可篡改"写成工程规范，是在向成熟合规实践靠拢，可作为论文工程章节的加分论据。

**取证问答的具体形态**（阙疑版）：
1. "某条 verified 判决在第 N 号 checkpoint 时是什么内容？" → 取 checkpoint + 对该条目做 inclusion proof，O(log 452) ≈ 9 次哈希。
2. "账本有没有被回写过？" → 对新旧两个树根做 consistency proof；失败即证明历史被改。
3. "谁在何时写入的？" → 账本条目必须含 `actor`、`utc_timestamp`、`prev_hash`、`entry_hash` 四字段（这是方向 64 机制的取证化扩展）。

---

## 对阙疑的 3 条具体行动

1. **建威胁模型登记表（2026-10 内完成）**：新建 `research/13_threat_model.md`，画"知识卡 → gate_engine.py → 账本 → Merkle checkpoint → 独立对账器"数据流图，按本文第一节表格对每条数据流逐项填 S/T/R/I/D/E 六类威胁、现有缓解、缺口；第一版至少登记 12 条威胁（每类 2 条）。特别登记两条已知硬伤作为 T 类威胁实例：本机 sanitizer 全缺失（`cannot find -lubsan`）意味着"用 sanitizer 抓异常输入"这一层完全空缺；工作树 227 项漂移意味着 Tampering 面完全开放。该文件将直接成为 NeurIPS 论文 "Threats to Validity / Auditing" 小节的素材。
2. **把独立对账器制度化为持续差分 harness（2026-12 前）**：在 `tools/` 下新增 `fuzz_gate.py`，用 Hypothesis 对 `gate_engine.py` 做性质测试（性质 P1：同一知识卡+同一规则集，内核与独立对账器判决必须一致——即差分测试；性质 P2：账本 append 后 entry_hash 必可复算；性质 P3：任意篡改历史条目必使后续某条 prev_hash 校验失败）。同时补齐 sanitizer 缺失：把 ASan/UBSan 的安装步骤写进 `setup/`，使 15 个真实缺陷夹具能在 sanitizer 开启下重注入（当前 6/6 = 100% 的重注入率未经 sanitizer 交叉验证，是审计盲点）。目标：97.3% 变异 core 分数之外，新增"fuzzing 致命崩溃数 = 0、差分不一致数 = 0"两条硬指标。
3. **账本取证化改造 + 第三方审计脚本（2027-05 论文截稿前）**：给账本条目 schema 增加 `actor` 与 `utc_timestamp` 字段（若已有则核对其覆盖率，用一条脚本统计 452 条账本中字段缺失率并写入论文）；每月生成签名 Merkle checkpoint（树根 + 条目数 + 时间戳），在仓库 `checkpoints/` 目录发布；提供 `tools/audit_ledger.py`，供第三方执行三个命令：`--inclusion <entry_id> <checkpoint_n>`（O(log n) 包含证明）、`--consistency <ckpt_m> <ckpt_n>`（一致性证明）、`--replay`（对账器独立复算全部判决并 diff）。论文里逐字采用 RFC 6962 §1 的措辞框架：阙疑账本的目标是 "publicly auditable, append-only, untrusted"——是"detect misissuance"而非"prevent misissuance"。

---

## 盲区（诚实标注）

- **Csmith 的 325+ bugs 与 OSS-Fuzz 的 10,000/36,000/1,000 数字均已逐字核实**，但 OSS-Fuzz 数字停在 2023-08 官方口径（此后官方页面未更新该句），2026 年的最新数字未核实；arXiv:2510.16433 的"36% 项目首轮即检出 bug"来自检索摘要，未打开全文核对表格。
- **中国标准原文均未直接核实**：GB/T 22239-2019 条文、GA/T 2380-2026（仅见于掘金转述）、"日志留存 ≥180 天"（仅见于 CSDN 问答），写论文引用时必须拿标准原文或改为不引用。
- **STRIDE 的原始出处论文**（Garg & Kohnfelder，《The Threats to Our Products》）未获取原文，出处时间"1990 年代末"来自中文二手资料（CSDN/博客园）；如需精确年份与原文表述，须另行核实。
- **JAIR 红队综述"over 120 papers"、JADE DB v2.0"各 1000 题"、RedBench、AI fuzzing"26 个零日漏洞含 CVE-2024-9143"** 均来自检索结果页/中文转述，未逐字核对原文或官方博客。
- **样本偏差**：fuzzing/差分测试的辉煌战绩（325 bugs、10,000 漏洞）全部来自编译器/解析器这类"输入-输出语义明确"的系统；`gate_engine.py` 的判决依赖规则库语义，差分 oracle 只能来自自建的独立对账器——若对账器与内核共享同一份规则库实现假设，差分测试会退化为"自己抄自己"，检出能力存疑。这是把外部方法迁移到阙疑时最大的方法论风险。
- **检索过程**：1 次 WebSearch（NeurIPS 2026 E&D CFP 英文查询）因 524 超时失败，本方向的 NeurIPS CFP 表述依赖共享上下文与 2025-12-05 官方博客检索摘要，未重试成功。

---

## 来源

1. OSS-Fuzz 官方文档（Trophies 节）— https://google.github.io/oss-fuzz/ — 逐字核实："As of August 2023, OSS-Fuzz has helped identify and fix over 10,000 vulnerabilities and 36,000 bugs across 1,000 projects." — Google / OpenSSF — 2023-08 口径（页面持续更新）
2. Yang, Chen, Eide, Regehr. *Finding and Understanding Bugs in C Compilers*. PLDI 2011 — https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf — 已下载 PDF 逐字核实："we have found and reported more than 325 bugs in mainstream C compilers including GCC, LLVM, and commercial tools"；"we found previously unknown bugs in unproved parts of CompCert" — University of Utah — 2011
3. RFC 6962: Certificate Transparency — https://www.rfc-editor.org/rfc/rfc6962.txt — 逐字核实：§1 "publicly auditable, append-only, untrusted logs"；§2.1.1 Merkle Audit Paths；§2.1.2 Merkle Consistency Proofs；§7.3 日志两种作恶方式 — IETF（Laurie, Langley, Kasper, Stradling）— 2013
4. Microsoft Learn: Threat Modeling Tool Threats（STRIDE 模型）— https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats — 逐字核实六类威胁定义（Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation of Privilege）— Microsoft — 页面更新至 2022+
5. Google Trillian: General Transparency — https://google.github.io/trillian/ — "an implementation of the concepts described in the Verifiable Data Structures white paper... generalisation of the ideas which underpin Certificate Transparency" — Google — 未核实具体更新日期
6. Sigstore Rekor（软件供应链透明日志）— https://github.com/sigstore/rekor — "A CLI application is available to make and verify entries, query the transparency log for inclusion proof, integrity..." — Sigstore — README 2026-06 版
7. libFuzzer 官方文档 — https://llvm.org/docs/LibFuzzer.html — "LibFuzzer is linked with the library under test, and feeds fuzzed inputs to the library via a specific fuzzing entrypoint" — LLVM 项目 — 持续更新
8. *Against The Achilles' Heel: A Survey on Red Teaming for Large Language Models*, JAIR — https://www.jair.org/index.php/jair/article/download/17654/27131/43767 — "examines over 120 papers, introduces a taxonomy of fine-grained attack strategies"（检索摘要） — JAIR — 2025-02
9. 大规模持续 fuzzing 实证分析 — https://arxiv.org/html/2510.16433v1 — "36% of OSS-Fuzz projects detected at least one fuzzing bug during the first fuzzing..."（检索摘要） — arXiv — 2025-10
10. NeurIPS 官方博客：Datasets & Benchmarks Track: From Art to Science in AI Evaluations — https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ — "These standards enabled automated checklists and standardized dataset summaries within OpenReview"（检索摘要） — NeurIPS — 2025-12-05
11. 复旦白泽智能发布 JADE DB v2.0 — https://www.secrss.com/articles/60901 — JADE-DB-Easy / JADE-DB-Medium 各 1000 个通用测试问题（中文转述） — 安全客/复旦 — 2023-11-20
12. 腾讯云社区：谷歌 AI Fuzz 工具 OSS-Fuzz 发现 26 个零日漏洞 — https://cloud.tencent.com/developer/article/2469524 — 含 OpenSSL CVE-2024-9143（中文转述，Google 原文未核实） — 腾讯云 — 2024-11-21
