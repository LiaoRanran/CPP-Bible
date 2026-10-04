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

Verified build (2026-10-04, 676m repack)
----------------------------------------
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
- Code/data availability: repository is public (Apache-2.0) with DCO sign-off; the
  Croissant metadata and per-sample artifacts are provided as supplementary material.
