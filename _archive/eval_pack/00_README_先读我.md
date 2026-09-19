# EVAL_PROMPT — What this system is, and what to critique

You are a skeptical senior researcher / principal engineer. Below is a curated pack about an in-progress meta-system called **「阙疑 / QueYi」** ("questioning doubt"). **CPP-Bible is only a C++ testbed** — the real product is the meta-system itself. Read `00_README` first, then the attached docs, then judge.

---

## 1. The problem it tries to solve

Large language models write plausible-sounding technical claims. Existing trust mechanisms (peer review, the model judging itself, unit tests, even formal verification) all assume some background verifier that itself is trusted. QueYi starts from a harsh premise:

> **There is no ultimate trusted verifier.** Every verifier (compiler, LLM, human, formal proof) can be wrong, can be surpassed, and will eventually be replaced.

So instead of trying to build "a perfect verifier," QueYi treats **"the next, stronger verifier can take over" as a first-class design constraint**. It aims to produce knowledge that is:
- **machine-checkable** (claims are pinned to artifacts the machine can re-run, not to prose),
- **error-rate-bounded** (e.g. Clopper–Pearson confidence upper bounds on false-accept, not just "all green"),
- **survives model replacement** (swap the writer model — only the "trust gate" thresholds move, the system isn't rebuilt).

## 2. Architecture in one breath

A **knowledge-production + verification pipeline** split across three roles that must *not* be the same model family:

| Role | Who | Job |
|---|---|---|
| Writer | weak / cheap model | produces technical "atoms" + evidence cards |
| Adversary | different model family | red-teams the system, tries to make it accept false claims |
| Verifier / Auditor | independent checks + human | nothing counts until an external oracle or a human signs off |

**Iron rules (non-negotiable):**
1. Never trust self-report. Every claim must be grounded in an artifact the machine re-runs.
2. Generation and verification are separated — the writer cannot grade its own homework.
3. Human sign-off is never automated; inference / human-review is never replaced by a model.
4. No LLM-as-judge for final acceptance; no same-family debate as independent evidence; no online weight updating.
5. Every new rule must pass a **poison drill** (deliberately poisoned cards it must reject) and a **clean-pass** (real cards must not be falsely flagged).
6. "Zero false positive" is not a claim — it's reported as a confidence upper bound (56 cards, 0 false blocks ⇒ 5.21% upper bound at 95%, not "perfect").

## 3. The most novel mechanism to look at

**V-iso (yin–yang isomorphism)**: a key observation isn't accepted just because it survives; it must ship a **"negative twin"** — a minimal-diff variant that *breaks the mechanism* (e.g. delete the one line the claim depends on), and the assertion must **flip to fail** on that twin. This catches the recurring failure mode "all green but the assertion is vacuous" (e.g. asserting `.file` appears in any assembly). `viso_diff.py` is the machine judge for "is this negative twin actually minimal-diff and mechanism-targeted."

Also: **mutation fuzz** mutates cards (weaken assertions, delete fields, forge claims) and measures what fraction the gate catches — currently 1188 variants, ~64% strict catch, with the remainder honestly labeled "real holes" vs "invalid mutation".

## 4. Current real baseline (measured, not claimed)

- 61 gate rules / block=0 / warn=136; poison drill 107/107; replay confirm=56/refute=0/infra=0.
- 27 "atoms", 79 structured propositions (50 observation / 29 inference).
- Integrity self-check: any byte tamper to the 5 core verifier files makes the gate refuse to run (I personally verified this).
- Daily gate loop: ~40s (was ~4min).

---

## What I want you to do — be harsh, be specific

1. **Diagnose, don't praise.** Is "no ultimate trusted verifier → open/revisable knowledge with monotone falsification" actually coherent, or is it just CI + hype?
2. **Name the hidden dead-ends.** Where is this architecture going to hit a wall in 12–24 months? (Think: the oracle itself, the cost of real compilation per claim, human-review bottleneck, mutation-fuzz saturation, knowledge-graph semantics.)
3. **Compare it to real alternatives.** How does it differ from / improve on / regress vs: formal verification (Lean/Coq), AI-Scientist / automated research, software supply-chain provenance (SLSA/Sigstore), differential/metamorphic testing, evals-as-infra, and "vibe coding" guardrails?
4. **Is the complexity justified?** This system has ~290 design docs and 100+ tools. Where is gold and where is ritual? What would you delete?
5. **The single biggest risk you'd bet on** — the one thing that makes the whole thing collapse or become theater.
6. **What should it build next** given it is small (one person + a few models), not a company?

Cite the attached doc names when you refer to a specific idea. If something sounds impressive but is actually already standard, say so bluntly.
