#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compress_696_maintext.py — 把 696-A2/A1 的主文插入压缩到 9 页限额内。

背景：696-A2 的第一版把 ~1000 词插进主文，`page:endmain` 从 ≤9 涨到 10 ⇒ 论文门禁
第 1 项 FAIL。本脚本把每处插入压成「1 句、引用密集」的形式（引用一条不少，全部迁到
附录的详细论述保留），把主文增量降到约 400 词。

用法
====
  python tools/compress_696_maintext.py --check
  python tools/compress_696_maintext.py --apply
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "research" / "latex" / "queyi_neurips2027_v1.1.tex"

PAIRS: list[tuple[str, str]] = [
    (
        r""" Benchmark-validity audits now audit the audit itself
(five failure modes in validity audits~\cite{li2026auditingaudit}), and audits of tool-calling
evaluation report 18.5\% evaluator--human misalignment with run-to-run spans of
18.9pp~\cite{bhat2026benchmarkingbenchmarks}; protocol-validity audits of agent benchmarks find
a mislead gap of $0.45$--$1.00$ between exploit score and intended
score~\cite{shao2026protocolvalidity}.""",
        r""" Validity audits now audit the audit
itself~\cite{li2026auditingaudit}; tool-calling audits report 18.5\% evaluator--human
misalignment and 18.9pp run-to-run spans~\cite{bhat2026benchmarkingbenchmarks}; agent-benchmark
protocol audits find mislead gaps of $0.45$--$1.00$~\cite{shao2026protocolvalidity}.""",
    ),
    (
        r""" The item-level disclosure in (2) is on the \emph{device} side---instrument, assets,
environment---which is deliberately distinct from calls for standardized item-level release of
model \emph{responses}~\cite{jiang2026itemlevel}; we publish the instrument, they ask for the
results.""",
        r""" The item-level disclosure in (2) is \emph{device}-side (instrument, assets,
environment), distinct from calls to release model \emph{responses}~\cite{jiang2026itemlevel}.""",
    ),
    (
        r""" Independent work reaches the same
conclusion from the judge side: uncertainty-aware rejection is proposed as a
safeguard~\cite{lv2026whoevaluates}, and over-consistency in judges is argued to signal
over-simplification rather than reliability~\cite{han2025judgesverdict}---evidence that
``refuse to conclude'' is a legitimate state, not a missing result.""",
        r""" Independently, uncertainty-aware rejection is proposed
judge-side~\cite{lv2026whoevaluates}, and over-consistency is argued to signal
over-simplification~\cite{han2025judgesverdict}.""",
    ),
    (
        r"""\emph{External anchors.} That a headline gain can come from the apparatus rather than the
capability is not an isolated observation: run-to-run spans of 18.9pp are enough to flip
leaderboard conclusions~\cite{bhat2026benchmarkingbenchmarks}, and protocol-validity audits
report a mislead gap of $0.45$--$1.00$ between exploit and intended
score~\cite{shao2026protocolvalidity}. \emph{Mechanism distinction (important).} Those artifacts
require \emph{adversarial exploitation} or a scoring-logic defect; ours arises from
\emph{non-adversarial apparatus degradation} plus a denominator-caliber choice---no malicious
agent is involved and no one is rewarded for the gap. We state this because otherwise F1 reads
as another reward-hacking result, which it is not.""",
        r"""\emph{Anchors and mechanism.} Apparatus-driven headline gains are not
isolated~\cite{bhat2026benchmarkingbenchmarks,shao2026protocolvalidity}; unlike those artifacts
(adversarial exploitation or a scoring defect), ours is non-adversarial apparatus degradation
plus a caliber choice---not reward hacking.""",
    ),
    (
        r"""\emph{External anchors.} The same move---an aggregate rate hiding structure---is made in
benchmark construct-validity work~\cite{bean2025constructvalidity}, and sample-level auditing
shows aggregate accuracy masking internal heterogeneity~\cite{siedler2026samplelevel}.
\emph{Distinction.} Their heterogeneity is driven by \emph{item/label attributes}; ours is
driven by \emph{defect type $\times$ instrument detectability}---a property of the measuring
device, not of the items' annotation.""",
        r"""\emph{Anchors.} Aggregate rates hiding structure is a construct-validity
concern~\cite{bean2025constructvalidity}, as is sample-level masking~\cite{siedler2026samplelevel};
ours is device-driven (defect type $\times$ detectability), not item-driven.""",
    ),
    (
        r"""\emph{External support.} ``Environment \& tooling'' is independently identified as its own
reproducibility smell class~\cite{siddiq2025reproducibilitycrisis}, and reproducibility surveys
describe computation becoming a black box~\cite{antunes2024reproducibilitysurvey};
mechanistically, sanitizer implementations themselves miss bugs, so changing the environment
changes the evidence
instrument~\cite{cui2024falsenegatives,li2024ubfuzz}. Drift-measurement tooling exists for
controlled injection and time-aware normalised metrics~\cite{cerqueira2026conceptdrift}, but it
targets \emph{stochastic} variance that cross-validation can
reduce~\cite{eve2026validationcrisis}; ours is \emph{systematic}---swapping the environment moves
the value, and cross-validation cannot undo it.""",
        r"""\emph{Support.} Environment/tooling is an independent reproducibility smell
class~\cite{siddiq2025reproducibilitycrisis,antunes2024reproducibilitysurvey}; sanitizers
themselves miss bugs~\cite{cui2024falsenegatives,li2024ubfuzz}; drift tooling targets
\emph{stochastic} variance reducible by
cross-validation~\cite{cerqueira2026conceptdrift,eve2026validationcrisis}, whereas ours is
systematic.""",
    ),
    (
        r"""\emph{External anchor.} Benchmarks treated as ground truth are themselves rarely audited:
21.6\% of Defects4J defects are unusable for evaluation experiments and 7.1\% of test suites are
under-constrained~\cite{krafczyk2026defects4j}---the same ``the benchmark is not the ground truth
it is assumed to be'' shape as F4's $-17.92$pp composition offset.""",
        r"""\emph{Anchor.} 21.6\% of Defects4J defects are unusable for evaluation and 7.1\% of
suites under-constrained~\cite{krafczyk2026defects4j}---the same ``the benchmark is not the
ground truth assumed'' shape as the $-17.92$pp offset.""",
    ),
    (
        r"""\emph{External anchor.} That ``more dynamic'' does not mean ``better'' is field consensus:
dynamic-benchmark construction itself introduces new
incomparabilities~\cite{zhang2025swebenchlive}, the same shape as our operator$\equiv$greedy
identity ($\Delta{=}0$).""",
        r"""\emph{Anchor.} Dynamicisation itself introduces new
incomparabilities~\cite{zhang2025swebenchlive}, the same shape as our
operator$\equiv$greedy identity.""",
    ),
    (
        r"""These rules align with, and are not invented by, the audit-governance literature: formalizing
and accrediting auditors is an explicit policy
recommendation~\cite{costanzachock2022whoaudits}, and validity theory makes explicit the
inference a score can support~\cite{freiesleben2025benchmarkingepistemology}; R1--R5 are the
device-side instantiation of both.""",
        r"""\emph{Alignment.} R1--R5 instantiate device-side audit
governance~\cite{costanzachock2022whoaudits,freiesleben2025benchmarkingepistemology}.""",
    ),
    (
        r""" For calibration of ``how high is high enough'',
exact-match and $\kappa$ can diverge by 33--41pp on 541k judgements across 21
judges~\cite{norman2026reliabilityvalidity}---i.e.\ $\kappa$ is protocol-sensitive---and
over-consistency in judges is argued to signal over-simplification rather than
reliability~\cite{han2025judgesverdict}; both caution against reading a single $\kappa$ as
validity.""",
        r""" Calibration: exact-match and $\kappa$ diverge by 33--41pp across 21
judges~\cite{norman2026reliabilityvalidity}, so a single $\kappa$ is protocol-sensitive.""",
    ),
    (
        r""" Environment validity is now an independently recognised
methodological category---``Environment \& Tooling'' as a reproducibility smell
class~\cite{siddiq2025reproducibilitycrisis}, black-box computation in reproducibility
surveys~\cite{antunes2024reproducibilitysurvey}, and concept-drift evaluation
frameworks~\cite{cerqueira2026conceptdrift}---so T3 is a known class of threat, not a local
admission.""",
        r""" Environment validity is a recognised
category~\cite{siddiq2025reproducibilitycrisis,antunes2024reproducibilitysurvey,cerqueira2026conceptdrift},
so T3 is a known class, not a local admission.""",
    ),
    (
        r""" The vocabulary we use---design effect, effective sample
size, intra-class correlation---is standard measurement theory, adopted deliberately to move
``family clustering'' from an engineering observation to a measurement
conclusion~\cite{bean2025constructvalidity}.""",
        r""" Design effect, effective sample size and ICC are standard measurement
vocabulary~\cite{bean2025constructvalidity}, adopted to make ``family clustering'' a measurement
conclusion.""",
    ),
    (
        r""" That instrument reliability can itself be computed
has a precedent in alarm-equipped benchmarks~\cite{ishida2025capbencher}; our analogue is the
paired-environment measurement of F3, with the single-pair scope stated there.""",
        r""" Instrument reliability can itself be computed~\cite{ishida2025capbencher}; our analogue is
F3's paired-environment measurement.""",
    ),
    (
        r""" Three items follow
directly from the gaps this audit exposed: (i)~\emph{an equal-margin substitution design} to
identify composition from mechanism in F1, rather than only removing degenerate assets;
(ii)~\emph{a drift algebra} unifying composition, environment and denominator perturbations,
with identifiability conditions for separating composition from mechanism effects;
(iii)~\emph{an axiomatisation of the four-state verdict algebra}, with (partial) decidability
results for invariance under enumerated drift generators. We also intend to \emph{pre-register}
the A5 \texttt{uninterpretable}-downgrade clause: researcher degrees of freedom in agent
experiments (model choice, prompt wording, settings, result-dependent redesign) are now
documented well enough to pre-register against~\cite{vaccaro2026preregistration}.""",
        r""" Three items follow
from the gaps exposed: (i)~\emph{an equal-margin substitution design} to identify composition
from mechanism in F1; (ii)~\emph{a drift algebra} unifying composition, environment and
denominator perturbations with identifiability conditions; (iii)~\emph{an axiomatisation of the
four-state verdict algebra} with partial decidability under enumerated drift generators. We
also intend to \emph{pre-register} the A5 \texttt{uninterpretable}-downgrade
clause~\cite{vaccaro2026preregistration}.""",
    ),
    (
        r"""\textbf{Scope of the $\Delta_{\text{unknown}}{=}0$
observation.} We report the absence of an unknown increase as a \emph{candidate signature
observed on a single environment pair} ($n_{\text{env}}{=}1$; E1 \texttt{wsl-gcc-13.3} vs.\
E2 \texttt{windows-native-mingw}), \emph{not} as a sufficient \emph{fingerprint} of silent
degradation: one drift instance cannot define a diagnostic criterion, and we have not shown
that the pattern generalises. The claim here is the weaker, checkable one---on the pair we
could measure, the loss is silent---and we state the single-pair scope rather than let a
one-pair observation read as a law (T3, Future work).""",
        r"""\textbf{Scope of $\Delta_{\text{unknown}}{=}0$.} We report the absence of an
unknown increase as a \emph{candidate signature on a single environment pair}
($n_{\text{env}}{=}1$; E1 \texttt{wsl-gcc-13.3} vs.\ E2 \texttt{windows-native-mingw}), \emph{not}
a sufficient \emph{fingerprint} of silent degradation: one drift instance cannot define a
criterion and generalisation is untested.""",
    ),
    (
        r"""\emph{With degenerate assets
controlled (Pool~A, $d{=}0$), the $k{=}4$ gain vanishes}; we therefore report the headline
gain as \textbf{composition-dominated within the pools we measured} ($+24.03$pp at the single
$k{=}4$ caliber, $\approx+12.8$pp at the mean caliber). We deliberately do \emph{not} claim a
no-confounding separation of composition from mechanism---``composition $=+24$pp, mechanism
$=0$'' would require an \emph{equal-margin substitution} design (hold the marginal asset
budget fixed while swapping degenerate for informative assets), which our pools did not
implement; we only removed degenerate assets, so the two effects are not identified apart
here (Future work). What""",
        r"""\emph{With degenerate assets controlled
(Pool~A, $d{=}0$) the $k{=}4$ gain vanishes}; we report the headline gain as
\textbf{composition-dominated within the pools measured} ($+24.03$pp at $k{=}4$,
$\approx+12.8$pp at the mean caliber), and do \emph{not} claim a no-confounding separation of
composition from mechanism---that needs an equal-margin substitution design we did not run
(Future work). What""",
    ),
    (
        r"""SV-COMP 2026 registers, \emph{by track and language}, \textbf{61 C verifiers and 16 C witness
validators}, plus 11 Java verifiers / 3 Java validators and 3 SV-LIB verifiers / 1 validator;
43 verifiers and 13 validators were represented by active teams~\cite{beyer2026svcomp} (counts
are per-language and per-track, and the ``active'' figure counts \emph{teams}, not tools---an
aggregate ``$N$ verifiers'' is caliber-dependent, which is why we quote the split). It
validates witnesses with independent tools; it answers \emph{which verifier performs well on given tasks},""",
        r"""SV-COMP 2026 registers, by track, \textbf{61 C verifiers and 16 C witness validators}, plus
11 Java / 3 SV-LIB verifiers and 3 Java / 1 SV-LIB validators, with 43 verifiers and 13
validators from active teams~\cite{beyer2026svcomp} (per-language counts; ``active'' counts
teams, not tools). It validates witnesses with independent tools; it answers
\emph{which verifier performs well on given tasks},""",
    ),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="压缩 696 主文插入到 9 页内")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.apply or args.check):
        ap.error("需要 --check 或 --apply")

    text = TEX.read_text(encoding="utf-8")
    applied, already, missing = [], [], []
    saved = 0
    for old, new in PAIRS:
        if old not in text:
            if new in text:
                already.append(True)
                continue
            missing.append(old.splitlines()[0][:60])
            continue
        text = text.replace(old, new, 1)
        applied.append(True)
        saved += len(old) - len(new)
    print(f"[696-compress] {len(PAIRS)} 对；落地 {len(applied)}；已压缩 {len(already)}；未命中 {len(missing)}")
    if missing:
        print("[696-compress] 未命中:", missing)
        return 1
    print(f"[696-compress] 净减少 {saved} 字符")
    if args.apply:
        TEX.write_text(text, encoding="utf-8", newline="\n")
        print(f"[696-compress] 已写回 {TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
