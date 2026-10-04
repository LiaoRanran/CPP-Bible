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

Verified build (2026-10-04)
---------------------------
  total pages        29
  main text          ends on page 9 (\label{page:endmain}); References start on page 10
  undefined refs     none (0 undefined citations / 0 undefined \ref)
  overfull hboxes    none at >200pt; remaining warnings are underfull vbox at page breaks

Notes
-----
- The paper is written for double-blind review; the sty file defaults to the anonymous option.
- Appendix sections are ordered: extra experiments, A5 at full scale (1137 samples),
  detector capability boundaries (676g), reproducibility (environment/seeds/commands),
  positioning, tables, AI-use statement, limitations, future work.
- Numbers in the paper are recomputed from landed artifacts by tools/verify_paper_numbers.py
  (118 checks; 113 consistent, 0 hard mismatches); see REPRODUCE.md in the repository root.
- Code/data availability: repository is public (Apache-2.0) with DCO sign-off; the
  Croissant metadata and per-sample artifacts are provided as supplementary material.
