Queyi — arXiv / NeurIPS 2027 submission package
================================================

Title
-----
Evolving Verifiers: Failure-Driven Evidence Acquisition with Auditable Provenance

Authors
-------
ANONYMOUS (double-blind submission). The \author{} block intentionally reads
"Anonymous Author(s) / Affiliation / Address / email". Do not add author names,
affiliations, emails, acknowledgments, or funding information to this package.

Files
-----
queyi_neurips2027_v1.1.tex   Main source (single entry point).
queyi_refs.bib              Bibliography (BibTeX).
neurips_2025.sty            NeurIPS style file.

There are NO external image files: every figure is inline TikZ/pgfplots, and the
paper uses no \input/\include of sub-files. These three files are sufficient.

How to compile
--------------
Option A (recommended, no TeX distribution needed; downloads deps on first run):

    tectonic -X compile queyi_neurips2027_v1.1.tex --keep-logs --keep-intermediates

Option B (standard TeX Live / MiKTeX, two passes):

    pdflatex queyi_neurips2027_v1.1.tex
    bibtex   queyi_neurips2027_v1.1
    pdflatex queyi_neurips2027_v1.1.tex
    pdflatex queyi_neurips2027_v1.1.tex

Expected output: queyi_neurips2027_v1.1.pdf (main text 9 pages; references and
appendices follow and are not counted toward the 9-page limit).

Submission steps (arXiv)
------------------------
1. Upload this package as a single source archive (e.g. queyi_arxiv_submission.tar.gz).
2. Choose arXiv subject classes: cs.SE (Software Engineering) as primary;
   cs.PL (Programming Languages) as secondary. Cross-list to cs.AI if desired.
3. Confirm the "Submitter(s) ... anonymous / no author information" option and
   verify the compiled PDF shows no author, affiliation, or acknowledgment.
4. If an endorser is required, see data/673i_arXiv投稿清单.md for the lookup steps.

Notes
-----
- All figures/tables are self-contained; no data files are needed to compile.
- The v1.1 source compiles with 0 errors and 0 undefined references/citations.