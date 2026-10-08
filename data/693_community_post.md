# 招募标注者社区帖（中英双语）· 693-A3

> 使用方式：直接复制对应语言段落发帖。中文版面向知乎/小红书/CSDN/高校论坛；
> 英文版面向 Reddit（r/cpp、r/ProgrammingLanguages、r/Compilers）/ Hacker News /
> Lobsters / 相关 Discord 与邮件列表。**不要同时群发同一份到多个英文社区**——
> 逐社区改写开头两句，否则会被当 spam。

---

## 中文版

**标题建议**：招募 31 道 C++ 判断题的独立评审（1–2 小时，可署名致谢）——一个缺陷检测基准的可信度自检

**正文**

我们做了一个 C++ 缺陷检测基准，现在要给它做一次**可信度体检**，需要 3–5 位能读 C++
的人帮忙。

**问题是什么**

基准里每条样本都标了"这套检测器能不能报出来"。但到目前为止，**所有标签都来自同一条
自动化管道**（ASan / UBSan / TSan / 编译器告警 / 交叉编译对比 / 链接器，固定协议跑出来的）。
单一来源 = 没有交叉验证 = 标签错了没人知道。我们需要**独立的人类判断**来查它。

**你要做什么**

- 读 31 段**去标识化**的 C++ 代码（每段 2–40 行，无路径、无作者信息、无原始标签）；
- 每段回答一个问题：**在这八类检测资产下，有没有任何一个会产出诊断报告？**
- 四选一：`catch` / `miss` / `unknown` / `contradiction`。

⚠ 判据是**"检测器会不会报"**，不是**"代码是不是坏"**。很多真实缺陷（逻辑错误、协议缺陷、
调度语义缺陷）在八个资产下**一条报告都没有**，这种要判 `miss`。这不是你判断错了，
这恰恰是我们研究的核心发现之一。

**要多久**：读指南 15 分钟 + 校准题 15 分钟 + 正式 31 条 60–90 分钟 ≈ **1–2 小时**。
随时可以中途退出，交回已完成的部分。

**我们只要 31 条，不是 145 条**：已经先用一个独立的 AI 标注者跑了一轮，把 145 条收敛到
**31 条真正有分歧的**。你的时间花在真正有信息量的地方。

**你得到什么**

1. 论文致谢署名（真名 / 化名 / 完全匿名，你选）；
2. 完整分歧数据集与裁决结果，你可以引用或复用；
3. 投稿前先看基准和 1147×8 冻结检测矩阵；
4. 需要的话给你一段贡献说明（学生攒简历有用）。

**我们付不了钱**：这是无资助的独立研究，先把话说清楚，不浪费你时间。

**适合谁**（至少满足三条）

- 近两年写过非玩具级 C/C++；
- 用过至少一个 sanitizer 或静态分析工具；
- 知道 `-Wall -Wextra` 大致会出哪些告警；
- 不用查资料就能说清 undefined / unspecified / implementation-defined 的区别；
- 接触过软件验证、编译器或程序分析（SV-COMP、Defects4J、静态分析方向都算）。

做验证/测试/程序分析方向的研究生尤其欢迎，但实践者同样欢迎。**不要求有论文。**

**我们的诚实承诺**

- 材料包**去标识化**，不会回答任何"这条原始标签是什么"的问题；
- **κ 是多少就发多少**。阈值预注册（verdict κ ≥ 0.8，689 协议 §6）。不达标就在论文里写不达标；
- **先自曝一个我们自己的 bug**：145 条里有 **13 条**源码注释残留了 `expected_verdict:`
  原文（我们的净化脚本漏了）。这些在 CSV 里标了 `leak_suspected=yes`，κ 我们**带和不带各报一次**；
- 我们的第二标注者是 **AI 不是人**，这点我们明说。这个项目的人类 IAA 目前**是 0**——
  这正是要找你的原因。

**怎么参加**：在 GitHub issue 下留言，或在仓库 PR 里说一声，告诉我们你想怎么署名。
材料全在 `data/` 目录：`693_annotation_guide.md`（规则）、`693_calibration_examples.md`
（校准题 + 答案）、`693_human_adjudication_package.csv`（要填的表）、
`693_ai_double_label.json`（AI 双标完整结果，背景参考）。填完 CSV 发回来，
我们跑 `python tools/compute_693_iaa.py`，**结果先发给你再给论文**。

---

## English version

**Suggested title:** Looking for 3–5 C++ readers to adjudicate 31 items (~1–2 h) —
validating the labels of a C++ defect-detection benchmark

**Body**

We built a C++ defect-detection benchmark and now need to **check whether its labels are
actually right**. Looking for 3–5 people who can read C++.

**The problem**

Every sample in the benchmark is labeled "do these detectors report this defect?" But so
far **every label comes from a single automated pipeline** (ASan / UBSan / TSan / compiler
warnings / cross-toolchain diff / linker, run under one fixed protocol). One source means
no cross-check means nobody notices if the labels are wrong. We need **independent human
judgment**.

**What you do**

- Read 31 **de-identified** C++ snippets (2–40 lines each; no paths, no author metadata,
  no original labels).
- Answer one question per snippet: **under these eight detection assets, will any of them
  produce a diagnostic report?**
- Pick one of four: `catch` / `miss` / `unknown` / `contradiction`.

⚠ The criterion is **"will a detector report it"**, not **"is the code bad"**. Many real
defects (logic errors, protocol flaws, scheduling bugs) produce **zero** reports from all
eight assets. Those are `miss`. That is one of our central findings, not your error.

**Time:** 15 min guide + 15 min calibration + 60–90 min for the 31 items ≈ **1–2 hours**.
You can stop anytime and return what you finished.

**Only 31 items, not 145.** We already ran a second (AI) annotator to shrink the set down
to the **31 items that actually disagree**. Your time goes where it carries information.

**What you get**

1. Acknowledgment in the paper (real name / pseudonym / fully anonymous — your choice);
2. The full disagreement dataset and the adjudicated result, yours to cite or reuse;
3. First look at the benchmark and the frozen 1,147 × 8 detection matrix pre-submission;
4. A short contribution statement on request (useful if you're a student).

**We cannot pay.** Unfunded independent research. We'd rather say that up front.

**You're a fit if ≥3 apply**

- [ ] Wrote non-toy C/C++ in the last two years
- [ ] Used at least one sanitizer or static analyzer
- [ ] Know roughly what `-Wall -Wextra` produces
- [ ] Can state the difference between *undefined*, *unspecified*, and
      *implementation-defined* without looking it up
- [ ] Some exposure to verification, compilers, or program analysis
      (SV-COMP, Defects4J, static-analysis research…)

Grad students in verification/testing/analysis especially welcome, practitioners equally.
**No publication record needed.**

**Honesty commitments**

- Package is **de-identified**; we will not answer "what was this sample's original label".
- **We publish κ whatever it is.** Threshold pre-registered (verdict κ ≥ 0.8, our 689
  protocol §6). If we miss it, the paper says we missed it.
- **Our own bug, disclosed first:** 13 of the 145 files still carry a residual
  `// expected_verdict:` comment our sanitizer missed. Those rows are flagged
  `leak_suspected=yes`; we report κ **with and without** them.
- Our second annotator is an **AI**, not a human. We say so plainly. Human IAA in this
  project is **currently 0** — that is exactly why we're asking.

**How to join:** comment on the GitHub issue or open a PR, and tell us how you'd like to be
acknowledged. Everything is in `data/`: `693_annotation_guide.md` (rules),
`693_calibration_examples.md` (10 calibration items + answers),
`693_human_adjudication_package.csv` (the table you fill),
`693_ai_double_label.json` (full AI double-label run, background). Send the CSV back and we
run `python tools/compute_693_iaa.py` — **you get the report before the paper does**.

---

## 发帖纪律（给自己看的备注）

1. **不群发**：同一份英文文案不要同时发 Reddit 多个 sub 与 HN。每个社区改开头两句。
2. **先回答再招募**：如果社区里有人质疑方法，先认真回技术问题，不要急着重复贴招募链接。
3. **不承诺付钱、不暗示可能有经费**。
4. **不泄露任何样本原始标签**——哪怕是"顺便举个例子"。
5. 收到响应后**先发材料再问身份**，避免让人觉得在筛简历。
