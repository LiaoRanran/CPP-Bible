Queyi / "Caliber Drift and Capability Boundaries" — arXiv source package (real-name version)
===========================================================================================

Contents (4 files, no external graphics):
  queyi_neurips2027_v1.1.tex   main LaTeX source (all figures are inline TikZ; no \includegraphics)
  queyi_refs.bib               BibTeX database (75 entries)
  neurips_2025.sty             NeurIPS 2025 style file (Datasets & Benchmarks track, [dandb])
  README.txt                   this file

Compile
-------
  tectonic -X compile queyi_neurips2027_v1.1.tex        # verified: tectonic
  # or: pdflatex queyi_neurips2027_v1.1 && bibtex queyi_neurips2027_v1.1 && pdflatex x2

Verified build (2026-10-07, 691 repack)   <-- CURRENT
----------------------------------------
  total pages        34 (real-name twin; the anonymous twin is 35)
  main text          content ends on page 8; References start on page 9
  appendix           23 pages (13--35 in the anonymous twin; gate target <=26)
  abstract           245 words / 1776 characters (arXiv limit 1920 characters)
  undefined refs     none (0 undefined citations / 0 undefined \ref)
  independent build  regenerate this file from research/latex/queyi_neurips2027_v1.1.tex
                     (differences: \author block, notice string, header note only)
  anonymity          the ANONYMOUS twin was re-scanned: 0 identity traces; this file intentionally
                     carries the real identity (Ran Liao / Hefei University / 1026708211@qq.com)
  NOTE               publishing this real-name version during a double-blind review window
                     carries a timing risk; the author decides when to post it.

What changed in this repack (691 corrected-and-enhanced)
--------------------------------------------------------
- TITLE changed again after an online collision check: "Auditing the Evaluator(s)" is already a
  2026 paper title (PROPOR 2026) and "Evaluator Stress Test" is another (ACL Findings 2026), and
  DeepFact's mechanism is called "audit-then-score". The paper now leads with its own terms:
  "Caliber Drift and Capability Boundaries: An Audit Protocol for Software-Verification
  Evaluation". The audit *protocol* remains the named method (Sec. 3).
- FORMULA reclassified: E[J]=kd/n was already the exact hypergeometric mean with n = asset-pool
  size. The 689 edit is now recorded as SYMBOL DISAMBIGUATION (n collides with sample size), not
  as a correction, with the notation change stated in the text.
- "THREE POOLS" corrected: Pool B and Pool C contain the identical asset set (linker clears Pool
  B's 0.5% catch floor at 0.88%) and their per-k blocks match numerically, so the ablation covers
  TWO distinct pools and 9 distinct pool x k blocks; the single improving tier (k=4, +1.41pp,
  p=0.302) is one tier replicated under three pool labels, not three independent wins.
- EVIDENCE LIFTED into the main text: the mechanism-level tiers (k=1 +11.31pp p=6.0e-8, k=2/k=3
  +7.42pp) into Finding 1; all four label kappas, including the two previously unreported ones
  (expected_verdict 0.437, severity 0.157) into Threats T1 and Finding 2; the governance counters
  (452 ledger events, 67 rules, pinned ruleset hash) into Sec. 2.
- CONTENT SUBTRACTION (appendix): 67-rule manifest section removed (engineering detail); 673c
  humanization material condensed 2x; e-process, reproducibility, toolchain-sensitivity,
  meta-evaluation and the two 689 protocol subsections condensed; total pages 36 -> 35, with the
  appendix at 23 pages.

Verified build (2026-10-07, 689 repack, superseded by the 691 repack above)
-------------------------------------------------------------------------

What changed in this repack (689 reframed)
------------------------------------------
- STRUCTURAL REFRAME (not a title swap). Title: "Evolving Verifiers..." -> "Auditing the
  Evaluator: Stress-Testing Evidence-Based Software Verification". Contributions 4 -> 3
  (auditable protocol / systematic empirical audit / quantitative findings); the evolution
  operator and the submodular formalization are no longer contributions.
- New Section 3 "The Evaluator-Audit Protocol": claim caliber Q=(D,A,E,Theta,P); eight failure
  modes with identification signals; a falsification procedure walked end-to-end on the
  "+24pp" claim; four audit outcomes (survives / weakened / collapses / unresolved).
- Findings reorganised as five audited hypotheses (F1 composition artifact; F2 capability
  boundary; F3 environment; F4 TOST + standardization; F5 evolution hypothesis fails). The
  +24.0pp selection gain is presented as a measurement-pool composition artifact, not a win.
- Statistics added by deterministic recomputation of frozen matrices (no new detect runs):
  TOST at +-10pp FAILS (90% CI [-10.61,+5.52]pp; p_TOST=0.064; minimum passing margin 10.61pp);
  two-way standardization (forward -17.92pp; reverse +1.70pp; type level -13.52pp);
  three-component environment metrics (catch / unknown / conditional recall; 59.09% -> 23.64%
  without the declared WSL profile, delta-unknown = 0).
- Hard fixes: E[J]=kd/n -> k|D|/|A| (with the degenerate-asset derivation); TODO placeholders
  removed (A0-A4 marked "not run"); 18/70 -> 13/34; "Verifier Coverage 73.8%" and
  "Evolution Efficiency 1.9pp/rule" deleted; static arm renamed a calibration arm; all kappa
  values labelled AI self-consistency (never human IAA); Merkle claims restated as
  tamper-evident current-state integrity with a declared threat model; E9 restated as a
  cross-regime observational comparison; the template's "Submitted to ... (NeurIPS 2025)"
  notice is overridden in the .tex (the third-party .sty is untouched).
- Moved to the appendix: the failure-driven loop figure; full protocol reproductions; the new
  appendix Z "Reframing Evidence: Equivalence, Standardization, Environment and Human
  Annotation (689)" (TOST tables, standardization tables, environment profiles, the
  de-identified human-annotation package description, fair-comparison protocol and SV-COMP
  positioning). Human annotation is DESIGNED, NOT EXECUTED (human IAA = 0).
- Related work: DeepFact (arXiv:2603.05912) and SV-COMP 2026 (TACAS 2026 report) added; the
  positioning table is rebuilt along six audit dimensions.

What changed in this repack (677d, superseded by the 689 repack above)
---------------------------------------------------------------------
- Paper-merge batch: the 677b/677c experiment results are folded into the paper and the
  submission materials (no new experiments; detector/samples/question set untouched).
- A5: main endpoint (+24.0pp, full pool) is now reported SIDE BY SIDE with the
  degenerate-free selection effect (approx +7-12pp): clone-family re-split (474 families /
  420 components, zero clone pairs crossing) leaves the endpoint unchanged (+23.0 to +26.7pp,
  p <= 4.1e-29) -> template leakage excluded; a family-level cluster bootstrap gives
  design effect ~4.2, i.e. EFFECTIVE n ~133-140 (nominal 566) and 1.78-2.10x wider intervals.
- Appendices: new paragraphs "Clone-aware re-split and cluster bootstrap (677b)" and
  "Non-degenerate pools, baselines and an executable operator (677c)"; the evolution operator
  now has an executable score function (w1*failure + w2*novel - w3*cost - w4*redundancy) with
  two disclosed collapses (literal novel == failure; frequency == FD) and a non-significant
  ablation (full vs frequency-only: best case +1.41pp, p=0.302, 3/14 tiers).
- Main text: E4 robustness sentence, Analysis (5), Threats (effective sample size + the
  ~+12pp degenerate-asset share), Conclusion ("central empirical result is directional"),
  Future Work (non-degenerate pool now run; A0-A4 and multi-round verdicts remain).
- Main text held at 8 pages of content by compressing (not deleting) prose; appendix grew by
  one page.

Verified build (2026-10-04, 677a repack, superseded by the 677d repack above)
---------------------------------------------------------------------------
  total pages        32
  main text          content ends on page 8; References start on page 9
  abstract           246 words (gate limit 250)
  undefined refs     none (0 undefined citations / 0 undefined \ref)
  anonymity          checked: 0 identity traces (no names, no local paths, \author = Anonymous)

What changed in this repack (677a)
----------------------------------
- Pure framing / engineering-cleanup revision: NO new experiments, NO new numbers.
- Terminology: "verifier" is used in the evidence-acquisition sense everywhere; new §3
  Terminology paragraph; new first item C0 of the Claim Boundary (pass != semantic truth).
- Blind-spot ratio 38.4% is qualified as an instrument-boundary statistic at every occurrence;
  high-blind-spot type count corrected 15/70 -> 18/70 (aligned to data/blindspot_676g_stats.json).
- Verifier Coverage 73.8%: Clopper-Pearson CI removed (42 cards are a complete enumeration,
  not a sample); new "How to read our intervals" note in §6.
- e-process compressed to 2 sentences in the main text; full text moved to a new appendix
  marked EXPLORATORY (not pre-registered, not used for confirmatory claims).
- Provenance: "74 real defects" -> "74 source-derived reconstructions"; new appendix
  "Dataset Provenance and Composition" (self-authored 968 / source-derived-reconstruction 74 /
  original-external-artifact 0). Schema: data/holdout_expansion/SCHEMA.md §2.1.
- Engineering incident log moved out of the main text into a new appendix; Introduction and
  Conclusion now carry the "evaluation apparatus as a first-class scientific object" framing.
- Track/policy: E&D (renamed from D&B in 2026), typically double-blind; neurips_2025.sty kept
  as an unmodified third-party placeholder until the 2027 CFP is released; Croissant / RAI
  metadata are REGISTERED TODOs (not yet generated -- 2027 spec not published).
- Main text held at 9 pages by moving the added detail into the appendix.

Verified build (2026-10-04, 676m repack, superseded by the 677a repack above)
-----------------------------------------------------------------------------
  total pages        30
  main text          ends on page 9 (\label{page:endmain}); References start on page 10
  undefined refs     none (0 undefined citations / 0 undefined \ref)
  overfull hboxes    none at >200pt; remaining warnings are underfull vbox at page breaks
  anonymity          checked: 0 identity traces (no names, no local paths, \author = Anonymous)

What changed in this repack (676m)
----------------------------------
- §4 Evaluation Protocol: dataset-quality pointer added (details in Appendix A5-full).
- §6 E4: "two degenerate assets" corrected to "three" (the pre-registered 5% rule also flags
  `linker` at 0.88%); note that the 676m label re-check left the A5 endpoint bit-identical.
- §6 E4 / §10 / Abstract: the T17 label-validity statement now reads "AI self-consistency only
  (kappa=0.77), not human IAA" instead of "zero second annotators".
- Appendix A5-full: new subsections "Template diversity, cross-batch overlap and label quality
  (676m disclosure)" and "Label corrections applied in 676m".
- Appendix (new): "Detector Depth Benchmark (676l)" — per-asset P/R/F1, union recall, exhaustive
  best-k, marginal contributions, linker irreplaceability, cross-matrix caveat.
- Main text held at 9 pages by moving the added detail into the appendix.

Notes
-----
- The paper is written for double-blind review; the sty file defaults to the anonymous option.
- Appendix sections are ordered: extra experiments, A5 at full scale (1137 samples), detector
  capability boundaries (676g), detector depth benchmark (676l), reproducibility
  (environment/seeds/commands), positioning, tables, AI-use statement, limitations, future work.
- Numbers in the paper are recomputed from landed artifacts by tools/verify_paper_numbers.py
  (126 checks; 112 consistent, 14 retired-by-689-reframe, 0 missing, 0 hard mismatches);
  see REPRODUCE.md in the repository root.
- Code/data availability: repository is public (Apache-2.0) with DCO sign-off; per-sample
  artifacts ship as supplementary material. Croissant / Responsible-AI metadata are registered
  pre-submission TODOs (to be generated once the 2027 specification is published).
