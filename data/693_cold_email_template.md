# Cold Email Template · 693-A3（招募标注者 / 定向邀请）

> **目标人群**：SV-COMP、Defects4J、静态分析、软件验证、编译器方向的研究生与博士后。
> **纪律**：
> 1. **一人一封**，不要群发、不要抄送多人（会被当 spam，也违反多数学校邮件礼仪）；
> 2. 开头必须**具体到对方的工作**（哪篇论文 / 哪个工具 / 哪个 repo），模板里的
>    `[SPECIFIC]` 占位必须真的填，否则不要用；
> 3. **不超过 200 词**（正文）；材料链接放在最后；
> 4. 对方不回**最多追一次**，间隔 ≥10 天，之后不再打扰；
> 5. **不承诺任何报酬**，不暗示可能有经费。

---

## 主模板（英文）

**Subject:** 31 C++ judgment items (~1–2h) — help validate a defect-detection benchmark's labels

---

Hi [NAME],

I'm Ran Liao (Hefei University), working on a C++ defect-detection benchmark. I came across
your work on **[SPECIFIC: paper / tool / repo]** — specifically [SPECIFIC DETAIL: the part
that made you think of them], which is why I'm writing to you rather than to a mailing list.

**The ask, in one line:** we need independent human judgment on 31 de-identified C++ snippets
(~1–2 hours total) to check whether our automated labels are right.

**Why it matters:** every label in our benchmark currently comes from a single pipeline
(ASan/UBSan/TSan, compiler warnings, cross-toolchain diff, linker — one fixed protocol).
Single source, no cross-check. That's a construct-validity hole, and it's exactly the kind
of thing a reviewer will find if we don't.

**What you'd do:** read 31 short C++ snippets (2–40 lines, no original labels) and answer one
question each — *will any of the eight detection assets produce a report?* — as
`catch` / `miss` / `unknown` / `contradiction`. There's a rulebook and a 10-item calibration
set with answers. No installation, no toolchain to run.

**Two things I want to be upfront about:**

1. **We can't pay.** Unfunded independent work. Acknowledgment in the paper (real name,
   pseudonym, or anonymous — your choice), the full disagreement dataset, and a contribution
   statement if that's useful to you.
2. **Our second annotator is an AI, not a human,** and human IAA in this project is currently
   **0**. I'd rather tell you that now than have you discover it later.

**Also disclosed up front:** 13 of 145 files in our package have a residual
`expected_verdict` comment our sanitizer missed. We report agreement both with and without
them, and we publish the κ whatever it turns out to be — the threshold (κ ≥ 0.8) is
pre-registered.

If this is interesting: [LINK TO REPO]/blob/master/data/693_annotation_guide.md is the
rulebook, and `693_human_adjudication_package.csv` in the same folder is the table.
Reply with a yes/no and I'll send everything as one zip — or just say "not now" and I'll
stop here. No follow-up either way unless you ask.

Thanks for reading,

Ran Liao (廖冉)
School of Artificial Intelligence and Big Data, Hefei University
1026708211@qq.com

---

## 变体 A：对方明显很忙（教授 / 高年级博士后）

把正文压缩到 5 句，把"the ask"放第一句，删掉所有背景段：

> **Subject:** 31 C++ items (~1h) — label validation for a defect-detection benchmark
>
> Hi [NAME] — I'm Ran Liao (Hefei University). Short ask: we need independent human
> judgment on 31 de-identified C++ snippets (~1 hour) to check whether our automated
> benchmark labels are right; every label currently comes from one pipeline with no
> cross-check. You read snippets and answer "will any of eight detection assets report
> this?" — `catch`/`miss`/`unknown`/`contradiction`. Rulebook + 10-item calibration set
> included, nothing to install.
>
> Two disclosures: we can't pay (unfunded; acknowledgment + dataset + contribution
> statement instead), and our second annotator is an AI, so human IAA here is currently 0.
> We publish the κ whatever it is.
>
> If interested: [LINK]. A one-word yes/no is enough; I'll send a single zip. Happy to hear
> "not now" too.

---

## 变体 B：追一次（10 天后，最多一次）

> **Subject:** Re: 31 C++ judgment items — quick bump
>
> Hi [NAME] — bumping this once in case it got buried, and then I'll leave it. The ask is
> unchanged: ~1 hour, 31 de-identified C++ snippets, checking whether our benchmark labels
> hold up. [LINK]
>
> No reply needed if the answer is no.

---

## 变体 C：对方回复"有意思但我没时间"

> Thanks for the honest answer — genuinely appreciated. Two options if either ever fits:
>
> 1. **5 items instead of 31.** Any subset is usable; we just record the coverage.
> 2. **Just the calibration set** (10 items, ~15 min) and tell me where our rulebook is
>    ambiguous. That feedback alone would improve the guide more than another pair of hands.
>
> And if you know someone in your group who'd want the acknowledgment line, I'd be grateful
> for a pointer.

---

## 收件人清单纪律（给自己看的备注）

- 只发**你能具体说出其工作**的人。填不出 `[SPECIFIC]` 就不发。
- 每封记录：日期 / 姓名 / 机构 / 变体 / 是否回复。放进 `data/693_recruitment_log.md`
  （本批不创建该文件，等真发再建，避免留空壳）。
- **不泄露任何样本原始标签**——邮件里也不要举例。
- 收到"愿意"之后：先发材料（一个 zip），再问署名形式，不要反过来。
