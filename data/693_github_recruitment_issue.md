# Call for Annotators: Help Validate a C/C++ Defect Detection Benchmark (1–2 hours, co-author acknowledgment)

> **What this is.** We built a benchmark that asks a simple question: *given a C++ defect,
> do our detectors actually report it?* Every label in the benchmark currently comes from a
> **single pipeline** (sanitizers + compiler warnings + a cross-toolchain diff, run under a
> fixed protocol). That is a construct-validity risk: if our labels are wrong, every number
> derived from them is wrong. We need **independent human judgment** to check them.
>
> **What this is not.** We are not asking you to write code, run our toolchain, or install
> anything. You read C++ snippets and answer one question per snippet.

---

## 1. The task

You get a **de-identified** C++ source file (typically 2–40 lines, no paths, no author
metadata, no original labels). For each one you answer:

> **Under the detection conditions listed below, will *any* of the eight assets produce a
> diagnostic report?**

The eight assets:

| Asset | What counts as "a report" |
|---|---|
| AddressSanitizer | OOB read/write, use-after-free, double-free, alloc-dealloc mismatch, leak, stack escape |
| UndefinedBehaviorSanitizer | signed overflow, division by zero, bad shift, misaligned access, invalid vptr |
| ThreadSanitizer | unsynchronized concurrent access to a non-atomic object |
| Compiler warnings | anything at `-Wall -Wextra` level |
| `-Wunsequenced` | (treated as unavailable; see guide §5C) |
| Cross-compile diff | two toolchains producing different output |
| Linker | duplicate symbol, undefined symbol, ODR violation |
| Compile-time | the code fails to compile at all |

You answer one of four values per snippet: **`catch` / `miss` / `unknown` / `contradiction`**.

> ⚠ The criterion is **"will a detector report it"**, **not** "is the code bad".
> Many genuine defects (logic errors, protocol flaws, scheduling bugs) produce **zero**
> reports from all eight assets. Those are `miss`. That is one of our central findings,
> not a mistake on your part.

## 2. How much work

| Item | Volume | Time |
|---|---:|---:|
| Read the annotation guide | 1 doc | ~15 min |
| Calibration set (10 items + answers) | 10 | ~15 min |
| **Adjudication set** | **31 items** | **60–90 min** |
| Notes / comments | optional | ~10 min |

**Total: 1–2 hours.** You can stop at any point and return what you have finished.
We only adjudicate the **31 disagreement items**, not all 145 — we already ran a second
(AI) annotator to shrink the set, so your time goes where it actually matters.

## 3. What you get

1. **Co-authorship acknowledgment** in the paper's acknowledgments section, under your
   preferred name, ORCID if you want it, or **fully anonymously** — your choice.
2. **The disagreement dataset** (`693_ai_double_label.json`) and the adjudicated result,
   so you can cite or reuse it.
3. **First look** at the benchmark and the frozen 1,147-sample × 8-asset detection matrix
   before submission.
4. A one-paragraph **reference letter / contribution statement** on request, describing
   exactly what you did (useful if you are a student assembling a CV).

We cannot pay. We are an independent, unfunded research line. We are explicit about that
up front rather than wasting your time.

## 4. Who we are looking for

You are a good fit if you can honestly say **yes** to at least three:

- [ ] You have written non-trivial C or C++ in the last two years.
- [ ] You have used at least one sanitizer (ASan/UBSan/TSan) or a static analyzer.
- [ ] You know what `-Wall -Wextra` does and roughly which warnings it produces.
- [ ] You can read the C++ standard's distinction between *undefined*, *unspecified*,
      and *implementation-defined* behavior without looking it up.
- [ ] You have some exposure to software verification, compilers, or program analysis
      (SV-COMP, Defects4J, static analysis research, etc.).

**Graduate students working on verification / testing / program analysis are especially
welcome** — but so are strong practitioners. No publication record required.

## 5. Materials

| File | What it is |
|---|---|
| `data/693_annotation_guide.md` | The rulebook. Read this first. 34 defect types, four-state definitions, edge cases. |
| `data/693_calibration_examples.md` | 10 calibration items + answers. **Do these before the real set.** |
| `data/693_human_adjudication_package.csv` | The 31 items. You fill `human_verdict` (4 values) and optionally `human_note`. |
| `data/693_ai_double_label.json` | Full AI double-label run: per-item verdicts, reasons, confidence. Background only. |

The CSV columns you touch: **`human_verdict`** (required) and **`human_note`** (optional).
Do not rename the file, do not reorder rows, do not edit other columns.

## 6. How to participate

1. Comment on this issue (or open a PR) saying you are in. Tell us your preferred
   acknowledgment form: real name / pseudonym / anonymous.
2. We send you the four files (or you clone the repo — they are all in `data/`).
3. You fill `human_verdict` + `human_note` in the CSV and send it back
   (PR, email attachment, or gist — whatever is easiest).
4. We run `python tools/compute_693_iaa.py` and **publish the result in full**, including
   the number if it is bad for us. You get the report before we do anything else with it.

## 7. Blinding & honesty commitments

- The package is **de-identified**: no original filenames, no original labels, no batch or
  group membership. We will not answer questions about any sample's original label.
- **We publish the κ regardless of the result.** The threshold is pre-registered
  (verdict κ ≥ 0.8, per our 689 protocol §6). If we miss it, we say so in the paper.
- **Known defect in our own package, disclosed up front:** 13 of the 145 source files still
  contain a residual `// expected_verdict: <value>` comment that our sanitizer missed.
  Those rows are flagged `leak_suspected=yes` in the CSV. We report κ **both** with and
  without them. If you notice one, please write it in `human_note`.
- Our second annotator is an **AI**, not a human. We say so explicitly. Human IAA in this
  project is **currently 0** — that is precisely why we are asking you.

## 8. Timeline

Rolling. There is no deadline; we adjudicate as responses arrive and update the paper's
construct-validity section per batch. If you are reading this after the paper is submitted,
the call is still open: post-submission batches go into the camera-ready or the next version.

---

*Questions about the rules are welcome and answerable. Questions about a specific sample's
original label are not — that is the blinding red line.*
