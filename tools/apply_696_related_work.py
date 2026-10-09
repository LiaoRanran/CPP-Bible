#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""apply_696_related_work.py — 把 695 建议的「相关工作更新」落地到 v1.1 tex。

批次 696 / 线 A2。本脚本对 `research/latex/queyi_neurips2027_v1.1.tex` 做**精确字符串
替换**，每处替换都带唯一锚点与断言；任一处锚点找不到即整体不写回并 exit 1（幂等：已
落地过的锚点会被识别为 "already applied"）。

用法
====
  python tools/apply_696_related_work.py --check   # 只报告将改动哪些锚点
  python tools/apply_696_related_work.py --apply   # 写回
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "research" / "latex" / "queyi_neurips2027_v1.1.tex"

# (锚点名, 旧串, 新串, 幂等标记——新串里出现的、说明已落地的子串)
EDITS: list[tuple[str, str, str, str]] = []


def add(name: str, old: str, new: str, marker: str) -> None:
    EDITS.append((name, old, new, marker))


# ---------------------------------------------------------------- 1. Positioning
add(
    "positioning-2026-frontier",
    r"""validation~\cite{beyer2026svcomp}. \textbf{We do not claim to be the first to audit an
evaluator};""",
    r"""validation~\cite{beyer2026svcomp}. Benchmark-validity audits now audit the audit itself
(five failure modes in validity audits~\cite{li2026auditingaudit}), and audits of tool-calling
evaluation report 18.5\% evaluator--human misalignment with run-to-run spans of
18.9pp~\cite{bhat2026benchmarkingbenchmarks}; protocol-validity audits of agent benchmarks find
a mislead gap of $0.45$--$1.00$ between exploit score and intended
score~\cite{shao2026protocolvalidity}. \textbf{We do not claim to be the first to audit an
evaluator};""",
    "li2026auditingaudit",
)

# ------------------------------------------------------------- 2. Contributions
add(
    "contributions-device-side-item-level",
    r"""110 source-derived CVE reconstructions, with clone-aware splitting and explicit environment
profiles.""",
    r"""110 source-derived CVE reconstructions, with clone-aware splitting and explicit environment
profiles. The item-level disclosure in (2) is on the \emph{device} side---instrument, assets,
environment---which is deliberately distinct from calls for standardized item-level release of
model \emph{responses}~\cite{jiang2026itemlevel}; we publish the instrument, they ask for the
results.""",
    "jiang2026itemlevel",
)

# ------------------------------------------------------------ 3. Why four states
add(
    "four-states-judge-side-support",
    r"""invisible to the eight-asset instrument (Finding~2).""",
    r"""invisible to the eight-asset instrument (Finding~2). Independent work reaches the same
conclusion from the judge side: uncertainty-aware rejection is proposed as a
safeguard~\cite{lv2026whoevaluates}, and over-consistency in judges is argued to signal
over-simplification rather than reliability~\cite{han2025judgesverdict}---evidence that
``refuse to conclude'' is a legitimate state, not a missing result.""",
    "lv2026whoevaluates",
)

# ---------------------------------------------------------------------- 4. F1
add(
    "f1-external-anchors-and-mechanism",
    r"""literal selections coincide with greedy in every tier ($\Delta{=}0.0$pp).""",
    r"""literal selections coincide with greedy in every tier ($\Delta{=}0.0$pp).
\emph{External anchors.} That a headline gain can come from the apparatus rather than the
capability is not an isolated observation: run-to-run spans of 18.9pp are enough to flip
leaderboard conclusions~\cite{bhat2026benchmarkingbenchmarks}, and protocol-validity audits
report a mislead gap of $0.45$--$1.00$ between exploit and intended
score~\cite{shao2026protocolvalidity}. \emph{Mechanism distinction (important).} Those artifacts
require \emph{adversarial exploitation} or a scoring-logic defect; ours arises from
\emph{non-adversarial apparatus degradation} plus a denominator-caliber choice---no malicious
agent is involved and no one is rewarded for the gap. We state this because otherwise F1 reads
as another reward-hacking result, which it is not.""",
    "Mechanism distinction (important)",
)

# ---------------------------------------------------------------------- 5. F2
add(
    "f2-external-anchors",
    """This is a\nmajor finding, not a limitation.""",
    r"""This is a
major finding, not a limitation.
\emph{External anchors.} The same move---an aggregate rate hiding structure---is made in
benchmark construct-validity work~\cite{bean2025constructvalidity}, and sample-level auditing
shows aggregate accuracy masking internal heterogeneity~\cite{siedler2026samplelevel}.
\emph{Distinction.} Their heterogeneity is driven by \emph{item/label attributes}; ours is
driven by \emph{defect type $\times$ instrument detectability}---a property of the measuring
device, not of the items' annotation.""",
    "siedler2026samplelevel",
)

# ---------------------------------------------------------------------- 6. F3
add(
    "f3-external-support",
    r"""one-pair observation read as a law (T3, Future work).""",
    r"""one-pair observation read as a law (T3, Future work).
\emph{External support.} ``Environment \& tooling'' is independently identified as its own
reproducibility smell class~\cite{siddiq2025reproducibilitycrisis}, and reproducibility surveys
describe computation becoming a black box~\cite{antunes2024reproducibilitysurvey};
mechanistically, sanitizer implementations themselves miss bugs, so changing the environment
changes the evidence
instrument~\cite{cui2024falsenegatives,li2024ubfuzz}. Drift-measurement tooling exists for
controlled injection and time-aware normalised metrics~\cite{cerqueira2026conceptdrift}, but it
targets \emph{stochastic} variance that cross-validation can
reduce~\cite{eve2026validationcrisis}; ours is \emph{systematic}---swapping the environment moves
the value, and cross-validation cannot undo it.""",
    "cerqueira2026conceptdrift",
)

# ---------------------------------------------------------------------- 7. F4
add(
    "f4-external-anchor-defects4j",
    r"""a three-value provenance schema is adopted.""",
    r"""a three-value provenance schema is adopted.
\emph{External anchor.} Benchmarks treated as ground truth are themselves rarely audited:
21.6\% of Defects4J defects are unusable for evaluation experiments and 7.1\% of test suites are
under-constrained~\cite{krafczyk2026defects4j}---the same ``the benchmark is not the ground truth
it is assumed to be'' shape as F4's $-17.92$pp composition offset.""",
    "krafczyk2026defects4j",
)

# ---------------------------------------------------------------------- 8. F5
add(
    "f5-external-anchor-dynamic",
    r"""falsifiability, not recall.""",
    r"""falsifiability, not recall.
\emph{External anchor.} That ``more dynamic'' does not mean ``better'' is field consensus:
dynamic-benchmark construction itself introduces new
incomparabilities~\cite{zhang2025swebenchlive}, the same shape as our operator$\equiv$greedy
identity ($\Delta{=}0$).""",
    "dynamic-benchmark construction itself",
)

# ---------------------------------------------------------------- 9. Synthesis
add(
    "synthesis-governance-alignment",
    r"""\end{enumerate}
The AGEA abstraction (assets--governance--evolution--accountability)""",
    r"""\end{enumerate}
These rules align with, and are not invented by, the audit-governance literature: formalizing
and accrediting auditors is an explicit policy
recommendation~\cite{costanzachock2022whoaudits}, and validity theory makes explicit the
inference a score can support~\cite{freiesleben2025benchmarkingepistemology}; R1--R5 are the
device-side instantiation of both.
The AGEA abstraction (assets--governance--evolution--accountability)""",
    "costanzachock2022whoaudits",
)

# --------------------------------------------------------------------- 10. T1
add(
    "t1-kappa-calibration",
    r"""though contrast directions are stable).""",
    r"""though contrast directions are stable). For calibration of ``how high is high enough'',
exact-match and $\kappa$ can diverge by 33--41pp on 541k judgements across 21
judges~\cite{norman2026reliabilityvalidity}---i.e.\ $\kappa$ is protocol-sensitive---and
over-consistency in judges is argued to signal over-simplification rather than
reliability~\cite{han2025judgesverdict}; both caution against reading a single $\kappa$ as
validity.""",
    "norman2026reliabilityvalidity",
)

# --------------------------------------------------------------------- 11. T3
add(
    "t3-known-category",
    r"""comparisons observational only.""",
    r"""comparisons observational only. Environment validity is now an independently recognised
methodological category---``Environment \& Tooling'' as a reproducibility smell
class~\cite{siddiq2025reproducibilitycrisis}, black-box computation in reproducibility
surveys~\cite{antunes2024reproducibilitysurvey}, and concept-drift evaluation
frameworks~\cite{cerqueira2026conceptdrift}---so T3 is a known class of threat, not a local
admission.""",
    "a known class of threat, not a local",
)

# --------------------------------------------------------------------- 12. T4
add(
    "t4-measurement-vocabulary",
    r"""is not folded into the intervals.""",
    r"""is not folded into the intervals. The vocabulary we use---design effect, effective sample
size, intra-class correlation---is standard measurement theory, adopted deliberately to move
``family clustering'' from an engineering observation to a measurement
conclusion~\cite{bean2025constructvalidity}.""",
    "standard measurement theory, adopted deliberately",
)

# --------------------------------------------------------------------- 13. T5
add(
    "t5-instrument-reliability-precedent",
    r"""toolchain replication agrees at 93.5\%.""",
    r"""toolchain replication agrees at 93.5\%. That instrument reliability can itself be computed
has a precedent in alarm-equipped benchmarks~\cite{ishida2025capbencher}; our analogue is the
paired-environment measurement of F3, with the single-pair scope stated there.""",
    "alarm-equipped benchmarks",
)

# --------------------------------------------------------------- 14. Future work
add(
    "future-work-p1-p2-and-prereg",
    r"""\paragraph{Future work.}
Execute the human annotation (the single most important pending item); reproduce a small set
of original-project builds to test reconstruction fidelity; add an LLM-as-verifier arm and
semantic/logic-layer verifiers; extend the audit protocol across languages/domains; and
invite third-party replication challenges under the published caliber.""",
    r"""\paragraph{Future work.}
Execute the human annotation (the single most important pending item); reproduce a small set
of original-project builds to test reconstruction fidelity; add an LLM-as-verifier arm and
semantic/logic-layer verifiers; extend the audit protocol across languages/domains; and
invite third-party replication challenges under the published caliber. Three items follow
directly from the gaps this audit exposed: (i)~\emph{an equal-margin substitution design} to
identify composition from mechanism in F1, rather than only removing degenerate assets;
(ii)~\emph{a drift algebra} unifying composition, environment and denominator perturbations,
with identifiability conditions for separating composition from mechanism effects;
(iii)~\emph{an axiomatisation of the four-state verdict algebra}, with (partial) decidability
results for invariance under enumerated drift generators. We also intend to \emph{pre-register}
the A5 \texttt{uninterpretable}-downgrade clause: researcher degrees of freedom in agent
experiments (model choice, prompt wording, settings, result-dependent redesign) are now
documented well enough to pre-register against~\cite{vaccaro2026preregistration}.""",
    "vaccaro2026preregistration",
)

# ------------------------------------------------------- 15. Appendix (8) expand
add(
    "appendix-8-measurement-science",
    r"""Clopper--Pearson/Wilson/McNemar/Holm/Cohen \cite{clopper1934use,mcnemar1947note,cohen1960coefficient}.""",
    r"""Clopper--Pearson/Wilson/McNemar/Holm/Cohen \cite{clopper1934use,mcnemar1947note,cohen1960coefficient}.
A second cluster, added in this version, sharpens the \emph{measurement-science} framing:
construct validity as a first-class question for
benchmarks~\cite{bean2025constructvalidity}; standardized item-level data release of model
\emph{responses}~\cite{jiang2026itemlevel}---the result-side counterpart to our device-side
disclosure; an independence-free, paradigm-agnostic formalisation of Goodhart's
law~\cite{majka2025goodhart}; and the demonstration that reliability is not validity in
LLM-as-a-judge evaluation~\cite{norman2026reliabilityvalidity}. On the ledger side we add
quantified Merkle-tree collision-probability work to bound our tamper-evidence claim
honestly~\cite{kuznetsov2024merkletrees} and align evidence packaging with the W3C
PROV/RO-Crate community standard~\cite{leo2024rocrate}; the environment-as-coordinate argument
is supported by ``Environment \& Tooling'' as an independent reproducibility smell
class~\cite{siddiq2025reproducibilitycrisis}.""",
    "majka2025goodhart",
)

# ------------------------------------------- 16. neighbours table: +Defects4J row
add(
    "neighbours-add-defects4j-row",
    r"""Atlas~\cite{spoczynski2025atlas} & ML lifecycle metadata & attestation + transparent logs & Our hash-chained current-state ledger is a smaller sibling; they target supply chain, we target verdicts \\
\bottomrule""",
    r"""Atlas~\cite{spoczynski2025atlas} & ML lifecycle metadata & attestation + transparent logs & Our hash-chained current-state ledger is a smaller sibling; they target supply chain, we target verdicts \\
Defects4J audit~\cite{krafczyk2026defects4j} & the benchmark \emph{dataset} itself & stricter reproducibility requirements + manual review & Shows the benchmark our field treats as ground truth was never independently audited: 21.6\% of defects unusable, 7.1\% of test suites under-constrained \\
\bottomrule""",
    "Defects4J audit~\\cite{krafczyk2026defects4j}",
)

add(
    "neighbours-caption-seven",
    r"""\caption{Six 2025--2026 neighbours.""",
    r"""\caption{Seven 2025--2026 neighbours.""",
    "Seven 2025--2026 neighbours",
)

add(
    "neighbours-text-seven",
    r"""Table~\ref{tab:neighbours} places six recent systems against ours on the axes that actually divide""",
    r"""Table~\ref{tab:neighbours} places seven recent systems against ours on the axes that actually divide""",
    "places seven recent systems",
)

# ------------------------------ 17. seven-directions table: +8th direction + (9) + table
add(
    "seven-directions-add-8th",
    r"""7 provenance \& auditability & Merkle~\cite{merkle1988digital}; Constant-Size Crypto Evidence~\cite{kao2025constantsize}; Who Audits the Auditor~\cite{wang2026whoaudits}; NeurIPS Dataset Review~\cite{wu2024neurips} \\
\bottomrule
\end{tabular}
\end{table}""",
    r"""7 provenance \& auditability & Merkle~\cite{merkle1988digital}; Constant-Size Crypto Evidence~\cite{kao2025constantsize}; Who Audits the Auditor~\cite{wang2026whoaudits}; NeurIPS Dataset Review~\cite{wu2024neurips} \\
8 evaluator auditing / meta-evaluation & Auditing the Audit~\cite{li2026auditingaudit}; Benchmarking the Benchmarks~\cite{bhat2026benchmarkingbenchmarks}; Sample-Level Auditing~\cite{siedler2026samplelevel}; Who Audits the Auditors~\cite{costanzachock2022whoaudits}; Who Evaluates the Evaluators~\cite{lv2026whoevaluates} \\
\bottomrule
\end{tabular}
\end{table}

\paragraph{(9) LLM-vs-traditional failure topology (supports Finding~7).}
Recent work compares LLM-based and traditional analysis for vulnerability detection and observes
that they are complementary rather than substitutable~\cite{ramires2026friendsorfoes}, that
project-scale LLM detection has its own scale/context
limits~\cite{li2026vulndetection}, and that verification dynamics vary with
model~\cite{zhou2025variationinverification}. \textbf{Closest prior work observes complementarity
but does not formalise orthogonality, nor attribute failures to budget-gating versus capability
bounds}; that attribution---whether a miss reflects an exhausted measurement budget or a genuine
capability limit---is the object of Finding~7, and is what distinguishes our treatment.

\paragraph{Device-side vs.\ result-side auditing (a second axis, orthogonal to Table~\ref{tab:neighbours}).}
Table~\ref{tab:deviceside} splits prior work by \emph{where the audited object sits}: result-side
systems audit labels, scores or rankings; Queyi audits the evidence-acquisition instrument
itself. The table is offered as positioning, not as a scoreboard.
\begin{table}[h]
\caption{Device-side vs.\ result-side auditing.}
\label{tab:deviceside}
\centering
\small
\begin{tabular}{@{}p{2.5cm}p{2.6cm}p{3.0cm}p{4.6cm}@{}}
\toprule
Dimension & DeepFact~\cite{huang2026deepfact} / HELM / SV-COMP~\cite{beyer2026svcomp} & LLM-judge meta-eval (2026)~\cite{li2026auditingaudit,bhat2026benchmarkingbenchmarks} & \textbf{Queyi} \\
\midrule
Audited object & benchmark labels / model behaviour / verifier ranking & judge pipeline & \textbf{evidence-acquisition instrument} \\
Object level & result & rater & \textbf{instrument + environment + caliber} \\
Verdict states & audit-updated label / score / correct--incorrect--unconfirmed & 7 failure facets & \textbf{four states (\texttt{unresolved} first-class)} \\
Denominator caliber & --- & fixed item set & \textbf{\texttt{unknown} strictly separated from \texttt{miss}, declared per use} \\
Environment & not audited / containerized (control variable) & not audited & \textbf{the audited variable} \\
Failure mechanism & label error / coverage gap / verifier weakness & judge bias & \textbf{non-adversarial apparatus degradation + silent environment loss} \\
Third-party recompute & versioned rationale / released code / independent witness validation & not applicable & \textbf{one-line recompute (no external executor yet)} \\
Tamper evidence & --- & --- & \textbf{452-event hash chain + Merkle + OTS external anchor} \\
Status of negative results & secondary & secondary & \textbf{first-class (F1 collapse / F5 failure / orthogonality)} \\
\bottomrule
\end{tabular}
\end{table}
\emph{Honest boundary for this table:} SV-COMP already has independent witness validation, a
normalized environment, reproduction packages and a third-party jury; our difference is
\emph{the audited object}, not the first use of auditability.""",
    "Device-side vs.\\ result-side auditing",
)

add(
    "seven-directions-caption-eight",
    r"""\caption{Seven related-work directions.}""",
    r"""\caption{Eight related-work directions.}""",
    "Eight related-work directions",
)

add(
    "related-section-title-eight",
    r"""\section{Related Work (eight directions; three moved here from the main text)}""",
    r"""\section{Related Work (nine subsections incl.\ two new in v1.1; three moved here from the main text)}""",
    "nine subsections incl.",
)


def main() -> int:
    ap = argparse.ArgumentParser(description="落地 695 相关工作建议到 v1.1 tex")
    ap.add_argument("--apply", action="store_true", help="写回文件")
    ap.add_argument("--check", action="store_true", help="只报告")
    args = ap.parse_args()
    if not (args.apply or args.check):
        ap.error("需要 --check 或 --apply")

    text = TEX.read_text(encoding="utf-8")
    applied, already, missing = [], [], []
    for name, old, new, marker in EDITS:
        if marker in text and old not in text:
            already.append(name)
            continue
        if old not in text:
            missing.append(name)
            continue
        text = text.replace(old, new, 1)
        applied.append(name)

    print(f"[696-A2] 共 {len(EDITS)} 处锚点")
    print(f"  将落地 {len(applied)}: {applied}")
    print(f"  已存在 {len(already)}: {already}")
    print(f"  未命中 {len(missing)}: {missing}")
    if missing:
        print("[696-A2] 有锚点未命中 ⇒ 不写回，exit 1")
        return 1
    if args.apply:
        TEX.write_text(text, encoding="utf-8", newline="\n")
        print(f"[696-A2] 已写回 {TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
