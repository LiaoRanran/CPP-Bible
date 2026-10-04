Queyi / "Evolving Verifiers" — arXiv source package
===================================================

Contents (4 files, no external graphics):
  queyi_neurips2027_v1.1.tex   main LaTeX source (all figures are inline TikZ; no \includegraphics)
  queyi_refs.bib               BibTeX database (66 entries)
  neurips_2025.sty             NeurIPS 2025 style file (Datasets & Benchmarks track, [dandb], anonymous)
  README.txt                   this file

Compile
-------
  tectonic -X compile queyi_neurips2027_v1.1.tex        # verified: tectonic 0.17.0
  # or: pdflatex queyi_neurips2027_v1.1 && bibtex queyi_neurips2027_v1.1 && pdflatex x2

Verified build (2026-10-04, 677a repack)
----------------------------------------
  total pages        32
  main text          content ends on page 8; References start on page 9
                     (\label{page:endmain} sits AFTER \clearpage, so the .aux reports 9 --
                     this is the off-by-one convention the repo quality gate reads)
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
  (118 checks; 113 consistent, 0 hard mismatches); see REPRODUCE.md in the repository root.
- Code/data availability: repository is public (Apache-2.0) with DCO sign-off; per-sample
  artifacts ship as supplementary material. Croissant / Responsible-AI metadata are registered
  pre-submission TODOs (to be generated once the 2027 specification is published).
