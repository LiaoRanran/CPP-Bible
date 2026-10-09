<!--
Badges (copy the line below into the real GitHub issue body, rendered):
![good first issue](https://img.shields.io/badge/good%20first%20issue-yes-brightgreen)
![help wanted](https://img.shields.io/badge/help%20wanted-yes-blue)
![annotation](https://img.shields.io/badge/task-annotation-orange)
Labels to add on GitHub: `good first issue` · `help wanted` · `annotation` · `human-study`
-->

# 🔬 Help us validate a C/C++ defect-detection benchmark — ~1.5h, co-author acknowledgment

> **TL;DR.** We built a benchmark asking *"given a C++ defect, do our detectors actually report it?"*
> Every label currently comes from a **single AI pipeline** — a construct-validity risk.
> We need **independent human judgment** on **31 short snippets** (≈1.5 hours of your time).
> You read code and answer one question per snippet. **No coding, no installs.**
> In return: **acknowledgment in the paper** (real name / pseudonym / anonymous — your choice).

---

## What this is

We built a benchmark of C/C++ defect-detection. The core question is simple:

> *Given a C++ defect, under our detection conditions, will **any** of eight detection assets
> produce a diagnostic report?*

Every label in the benchmark today comes from a **single automated pipeline**
(sanitizers + compiler warnings + a cross-toolchain diff, under a fixed protocol).
That is a **construct-validity risk**: if our labels are wrong, every number derived from them
is wrong. We need **independent human judgment** to check them — and right now, human
inter-annotator agreement in this project is **literally 0** (our second annotator was an AI).

**What this is _not_.** We are not asking you to write code, run our toolchain, or install
anything. You read C++ snippets and answer one question per snippet. That's the whole task.

---

## The task

You get a **de-identified** C++ source file (typically 2–40 lines, no paths, no author
metadata, no original labels). For each one you answer:

> **Under the detection conditions listed below, will _any_ of the eight assets produce a
> diagnostic report?**

The eight assets:

| Asset | What counts as "a report" |
|---|---|
| AddressSanitizer | OOB read/write, use-after-free, double-free, alloc-dealloc mismatch, leak, stack escape |
| UndefinedBehaviorSanitizer | signed overflow, division by zero, bad shift, misaligned access, invalid vptr |
| ThreadSanitizer | unsynchronized concurrent access to a non-atomic object |
| Compiler warnings | anything at `-Wall -Wextra` level |
| Cross-compile diff | two toolchains producing different output |
| Linker | duplicate symbol, undefined symbol, ODR violation |
| `-Wunsequenced` | (treated as unavailable; see guide) |
| Compile-time | the code fails to compile at all |

You answer one of four values per snippet: **`catch` / `miss` / `unknown` / `contradiction`**.

> ⚠ **The criterion is "will a detector report it", _not_ "is the code bad".**
> Many genuine defects (logic errors, protocol flaws, scheduling bugs) produce **zero**
> reports from all eight assets. Those are `miss`. That is one of our central findings,
> not a mistake on your part.

### What the annotation sheet looks like

```
┌─────────────────────────────────────────────────────────────────────┐
│  sample_id : S030                                                    │
│  difficulty: Easy        leak_suspected: no                          │
│ ─────────────────────────────────────────────────────────────────── │
│  source_code:                                                           │
│    int main(){ int* p = new int(1); delete p; delete p; return 0; }    │
│ ─────────────────────────────────────────────────────────────────── │
│  YOUR TURN — fill these two:                                          │
│    your_verdict : ____________   (catch / miss / unknown / contradict)│
│    your_notes  : ____________   (why? anything uncertain?)            │
│                                                                       │
│  (reference only — NOT the answer)                                     │
│    annotator_A: catch   annotator_B: catch   b_confidence: high       │
└─────────────────────────────────────────────────────────────────────┘
```

You only ever touch **two cells** per row. That's it.

---

## How much work & what you get

| Item | Volume | Time |
|---|---:|---:|
| Read the annotation guide | 1 doc | ~15 min |
| Calibration set (10 items + answers) | 10 | ~15 min |
| **Adjudication set** | **31 items** | **~45–60 min** |
| Notes / comments | optional | ~10 min |

**Total: ~1.5 hours.** You can stop at any point and return what you have finished.

**Compensation:** **co-authorship acknowledgment** in the paper's acknowledgments section —
under your preferred name, ORCID if you want it, or **fully anonymously**. We cannot pay;
we are an independent, unfunded research line, and we say so up front rather than wasting
your time. You also get the disagreement dataset and a one-paragraph contribution statement
(useful for a CV) on request.

---

## Who we're looking for

You're a good fit if you can honestly say **yes** to at least three:

- [ ] You've written non-trivial C or C++ in the last two years.
- [ ] You've used at least one sanitizer (ASan/UBSan/TSan) or a static analyzer.
- [ ] You know what `-Wall -Wextra` does and roughly which warnings it produces.
- [ ] You can read the C++ standard's distinction between *undefined*, *unspecified*, and
      *implementation-defined* behavior without looking it up.
- [ ] You have some exposure to verification / compilers / program analysis (SV-COMP,
      Defects4J, static-analysis research, etc.).

Graduate students in verification / testing / program analysis are especially welcome;
no publication record required.

---

## Materials

| File | What it is |
|---|---|
| `data/annotation_package/annotation_guidelines.md` | The rulebook. Read this first. |
| `data/annotation_package/calibration/` | 10 calibration items + answers. **Do these before the real set.** |
| `data/702_annotation_table.csv` | The 31 items, **difficulty-sorted**, with blank `your_verdict` / `your_notes`. |
| `data/693_human_adjudication_package.csv` | The same 31 items (canonical, with full context). |

Only `your_verdict` (required) and `your_notes` (optional) are yours to fill.
Do not rename the file, reorder rows, or edit other columns.

---

## How to participate

1. **Comment on this issue** saying you're in, and tell us your preferred acknowledgment
   form: real name / pseudonym / anonymous.
2. We send you the files (or you clone the repo — they're all in `data/`).
3. Fill `your_verdict` + `your_notes` in the CSV and send it back
   (PR, email attachment, or gist — whatever is easiest).
4. We run the IAA script and **publish the result in full**, including the number if it's
   bad for us. You see the report before we do anything else with it.

---

## Blinding & honesty commitments

- The package is **de-identified**: no original filenames, no original labels, no batch or
  group membership. We will not answer questions about any sample's original label.
- **We publish the κ regardless of the result.** The threshold is pre-registered
  (verdict κ ≥ 0.8). If we miss it, we say so in the paper.
- **Known defect in our own package, disclosed up front:** 13 of the 145 source files still
  contain a residual `// expected_verdict: <value>` comment our sanitizer missed.
  Those rows are flagged `leak_suspected=yes` in the CSV. We report κ **both** with and
  without them. If you notice one, please write it in `your_notes`.
- Our second annotator is an **AI**, not a human. Human IAA in this project is **currently 0**
  — that is precisely why we are asking you.

---

## FAQ

**Q1. I'm not a C++ expert — can I still help?**
If you meet ≥3 of the "who we're looking for" bullets, yes. For code you can't parse, set
`confidence = 1` and write "can't tell" in `notes` — don't guess.

**Q2. What if I get some wrong?**
That's expected and fine. The κ threshold measures *agreement*, not "you must match us".
If you disagree with the AI labels, that disagreement is the data we actually want.

**Q3. Will I be named?**
Only if you want to be — real name, pseudonym, or fully anonymous, your choice.

**Q4. Can I compile/run the snippets?**
Yes (dependency files are included). But judge by the **guide's criteria**, not "what my
machine did" — our fixture config (-O0/-O2 dual, 8 assets, specific report strings) may
differ from your local setup.

**Q5. Why only 31 items, not all 145?**
We already ran a second (AI) annotator to shrink the set to the **31 disagreement items**,
so your time goes where it actually matters. The 145-sample blind set is a separate, optional
track if you want more.

**Q6. Is this double-blind / will my review be fair?**
The paper targets a typically-double-blind track. Your annotation is independent of any
reviewer; we publish the κ raw, good or bad.

**Q7. I have a question about a specific sample's "real" label.**
That's the blinding red line — we won't answer it, in any form. Ask about the *rules* instead.

---

*Questions about the rules are welcome and answerable. Questions about a specific sample's
original label are not — that is the blinding red line.*

<!-- Suggested GitHub labels: good first issue · help wanted · annotation · human-study -->
