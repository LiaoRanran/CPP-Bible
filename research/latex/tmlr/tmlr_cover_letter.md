# TMLR Cover Letter / Submission Statement（678 批次 · C2）

> 说明：TMLR 不强制 cover letter，但允许向 action editor 提供贡献陈述、编辑/审稿人建议、
> 基金与利益冲突（这些信息**不向审稿人披露**）。本文件按双盲口径撰写：正文不出现作者姓名/机构，
> 不回链具名 arXiv。与 NeurIPS E&D 版 `research/cover_letter.md` 贡献口径一致（v1.3 · 677d）。

---

**To the Action Editor,**

We submit *Queyi: A Failure-Driven Verifier Whose Central Result Is a Direction, Not a Number*
for consideration at TMLR. The work sits squarely in TMLR's scope — **evaluation
methodology, reproducibility, and datasets \& benchmarks** — and we believe its meta-contribution
(the "evolving verifier" that turns falsification into a first-class, auditable mechanism) is of
interest to the journal's readership.

**Five contributions** (aligned with the current version of record):

1. **A falsification-first verifier for C++ static analysis.** A four-state verdict
   (pass / fail / unknown / contradict) plus an append-only ledger (452 events, Merkle-anchored)
   makes every claim auditable and tamper-evident.
2. **A executable failure-driven evolution operator** (677c): a four-component score with two
   disclosed collapse points, so the "learner" is inspectable rather than a black box.
3. **A full-scale falsification experiment (A5)** on 1137 samples across 8 assets, with its
   robustness **measured, not assumed**: clone-family-aware re-split gives $\Delta$ +23.0–+26.7pp
   (effective $n\approx133$–140); the non-degenerate pool isolates a real but small selection effect
   of $\approx$+7–12pp (k$\le$3 significant, k=4 collapses to a selection-set collision).
4. **An honest capability-boundary map**: 38.4% of 1147 samples are blind spots; 18/70 defect
   types exceed 50% blind — published as an instrument-boundary statistic, not a claim about C++.
5. **A reproducibility package**: every headline number has a one-line recompute command; the
   audit tool reports 118 checks / 113 consistent / 0 hard errors.

**Why a journal track fits.** The core message — "we report the direction our own pre-registered
null check would have killed, and register it as directional evidence" — benefits from TMLR's
long-form, reproducibility-forward, double-blind format more than a conference page cap.

**Suggested reviewers / editors:** (withheld from reviewers per TMLR policy — supplied in the
submission form). We confirm the manuscript is anonymized and does not link to any named preprint.

**Conflicts of interest / funding:** (supplied in the submission form; not disclosed to reviewers).
