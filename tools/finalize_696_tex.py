#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""finalize_696_tex.py — 把 696 的相关工作更新收敛到 9 页主文限额内。

背景（实测）：
  * 基线 HEAD 主文 `page:endmain` = **9**（恰好在限额上，零余量）。
  * 696-A2 第一版把 ~1000 词插进主文 ⇒ 10 ⇒ 论文门禁第 1 项 FAIL。
  * 压缩后（净减 3608 字符）仍为 10 ⇒ 需要进一步把「逐段锚点」迁到附录。

本脚本：
  1. 从主文**移除** 7 处低优先插入（F2 / F5 / Synthesis / T1 / T3 / T4 / T5 的锚点句），
     把它们连同 jiang/lv/han 等引用**统一收进附录**（引用一条不少，只是换位置）；
  2. 缩短 Future work 的追加句；
  3. 保留主文最关键的锚点：Positioning / F1（含机制区分）/ F3（含单环境对降格）/
     F4 / A1.1–A1.3 三处措辞修正；
  4. 在附录追加 "Per-section anchors" 段，保证全部 26 篇新引用在文中出现。

用法
====
  python tools/finalize_696_tex.py --check
  python tools/finalize_696_tex.py --apply
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "research" / "latex" / "queyi_neurips2027_v1.1.tex"

REMOVE: list[str] = [
    # contributions (jiang)
    r""" The item-level disclosure in (2) is \emph{device}-side (instrument, assets,
environment), distinct from calls to release model \emph{responses}~\cite{jiang2026itemlevel}.""",
    # four states (lv / han)
    r""" Independently, uncertainty-aware rejection is proposed
judge-side~\cite{lv2026whoevaluates}, and over-consistency is argued to signal
over-simplification~\cite{han2025judgesverdict}.""",
    # F2 anchors
    r"""\emph{Anchors.} Aggregate rates hiding structure is a construct-validity
concern~\cite{bean2025constructvalidity}, as is sample-level masking~\cite{siedler2026samplelevel};
ours is device-driven (defect type $\times$ detectability), not item-driven.""",
    # F5 anchor
    r"""\emph{Anchor.} Dynamicisation itself introduces new
incomparabilities~\cite{zhang2025swebenchlive}, the same shape as our
operator$\equiv$greedy identity.""",
    # synthesis alignment
    r"""\emph{Alignment.} R1--R5 instantiate device-side audit
governance~\cite{costanzachock2022whoaudits,freiesleben2025benchmarkingepistemology}.""",
    # T1
    r""" Calibration: exact-match and $\kappa$ diverge by 33--41pp across 21
judges~\cite{norman2026reliabilityvalidity}, so a single $\kappa$ is protocol-sensitive.""",
    # T3
    r""" Environment validity is a recognised
category~\cite{siddiq2025reproducibilitycrisis,antunes2024reproducibilitysurvey,cerqueira2026conceptdrift},
so T3 is a known class, not a local admission.""",
    # T4
    r""" Design effect, effective sample size and ICC are standard measurement
vocabulary~\cite{bean2025constructvalidity}, adopted to make ``family clustering'' a measurement
conclusion.""",
    # T5
    r""" Instrument reliability can itself be computed~\cite{ishida2025capbencher}; our analogue is
F3's paired-environment measurement.""",
]

SHORTEN: list[tuple[str, str]] = [
    (
        r""" Three items follow
from the gaps exposed: (i)~\emph{an equal-margin substitution design} to identify composition
from mechanism in F1; (ii)~\emph{a drift algebra} unifying composition, environment and
denominator perturbations with identifiability conditions; (iii)~\emph{an axiomatisation of the
four-state verdict algebra} with partial decidability under enumerated drift generators. We
also intend to \emph{pre-register} the A5 \texttt{uninterpretable}-downgrade
clause~\cite{vaccaro2026preregistration}.""",
        r""" Three items follow
from the gaps exposed: (i)~\emph{an equal-margin substitution design} to separate composition
from mechanism in F1; (ii)~\emph{a drift algebra} with identifiability conditions;
(iii)~\emph{an axiomatisation of the four-state verdict algebra}. We also intend to
\emph{pre-register} the A5 downgrade
clause~\cite{vaccaro2026preregistration}.""",
    ),
]

APPENDIX_ANCHORS = r"""
\paragraph{Per-section anchors (main-text citations kept minimal for the 9-page budget).}
For completeness we record here the citation anchors whose main-text sentences were folded into
this appendix to respect the page limit. \emph{Four-state discipline}: uncertainty-aware
rejection~\cite{lv2026whoevaluates} and over-consistency as over-simplification rather than
reliability~\cite{han2025judgesverdict}. \emph{Finding~2 heterogeneity}: construct validity of
aggregate rates~\cite{bean2025constructvalidity} and sample-level masking~\cite{siedler2026samplelevel}.
\emph{Finding~5}: dynamicisation introduces new incomparabilities~\cite{zhang2025swebenchlive}.
\emph{Synthesis R1--R5}: auditor accreditation~\cite{costanzachock2022whoaudits} and validity
theory~\cite{freiesleben2025benchmarkingepistemology}. \emph{Threats}: $\kappa$
protocol-sensitivity~\cite{norman2026reliabilityvalidity}; environment validity as a recognised
class~\cite{siddiq2025reproducibilitycrisis,antunes2024reproducibilitysurvey,cerqueira2026conceptdrift};
design-effect/ESS/ICC vocabulary~\cite{bean2025constructvalidity}; computable instrument
reliability~\cite{ishida2025capbencher}. \emph{Item-level disclosure}: device-side
(instrument/assets/environment) versus result-side release of model
\emph{responses}~\cite{jiang2026itemlevel}.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="696 tex 收敛到 9 页")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.apply or args.check):
        ap.error("需要 --check 或 --apply")

    text = TEX.read_text(encoding="utf-8")
    removed, miss_rm = [], []
    for blk in REMOVE:
        if blk in text:
            text = text.replace(blk, "", 1)
            removed.append(True)
        else:
            miss_rm.append(blk.splitlines()[0][:50])
    shortened = []
    for old, new in SHORTEN:
        if old in text:
            text = text.replace(old, new, 1)
            shortened.append(True)
        elif new not in text:
            miss_rm.append(old.splitlines()[0][:50])

    anchor_marker = "\\paragraph{Per-section anchors"
    if anchor_marker not in text:
        anchor = r"""\emph{Honest boundary for this table:} SV-COMP already has independent witness validation, a
normalized environment, reproduction packages and a third-party jury; our difference is
\emph{the audited object}, not the first use of auditability."""
        if anchor not in text:
            print("[696-final] 附录锚点插入点未命中")
            return 1
        text = text.replace(anchor, anchor + "\n" + APPENDIX_ANCHORS, 1)
        added_appendix = True
    else:
        added_appendix = False

    print(f"[696-final] 移除 {len(removed)}/{len(REMOVE)}；缩短 {len(shortened)}/{len(SHORTEN)}；"
          f"附录锚点段新增={added_appendix}")
    if miss_rm:
        print("[696-final] 未命中:", miss_rm)
        return 1
    if args.apply:
        TEX.write_text(text, encoding="utf-8", newline="\n")
        print(f"[696-final] 已写回 {TEX}（{len(text)} 字符）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
