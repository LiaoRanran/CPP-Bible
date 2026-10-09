#!/usr/bin/env python3
r"""711-S1: exhaustive verification of A6 (irreversibility of removal generators).

Domain: X = {x1, x2}, declared profile P = {a, b}, run set S subset of P.
A configuration is (S, C_a, C_b), C_a, C_b subset of X (catch sets).
Aware-accounting verdict per sample x:
    c  if some run asset catches x
    u  if not, and some declared-but-not-run asset catches x   (lost / never-run)
    m  otherwise
Removal generator tau_G: S' = S \ G; verdicts are recomputed with S'
(catch sets unchanged -- they are the hidden pre-state).

Two record levels:
  L1 (matrix retained): record = (S', retained columns)      <- 697 T2's level
  L2 (verdicts only):   record = (S', verdict vector)        <- what a scalar report keeps

Checks:
  (i)   tau_0 is injective at both levels on the config space restricted to
        column-complete records (G = empty must be the unique invertible element);
  (ii)  tau_{a} is NOT injective at both levels (collision classes exist);
  (iii) informative collisions: same image, different pre-drift report R;
  (iv)  the c/u collision (lost catch vs never-run sample) exists at L2;
  (v)   point-mass lift: distinct priors, identical pushforward.

Read-only; deterministic; no detect() calls.
"""

from __future__ import annotations

import itertools

X = ("x1", "x2")
P = ("a", "b")


def verdicts(S: frozenset[str], ca: frozenset[str], cb: frozenset[str]) -> tuple[str, ...]:
    catches = {"a": ca, "b": cb}
    out = []
    for x in X:
        if any(x in catches[s] for s in S):
            out.append("c")
        elif any(x in catches[s] for s in P if s not in S):
            out.append("u")
        else:
            out.append("m")
    return tuple(out)


def configs():
    for r in range(len(P) + 1):
        for S in itertools.combinations(P, r):
            Sf = frozenset(S)
            for ca in (frozenset(), frozenset({"x1"}), frozenset({"x2"}), frozenset({"x1", "x2"})):
                for cb in (frozenset(), frozenset({"x1"}), frozenset({"x2"}), frozenset({"x1", "x2"})):
                    yield (Sf, ca, cb)


def R(cfg) -> float:
    S, ca, cb = cfg
    v = verdicts(S, ca, cb)
    return 100.0 * sum(1 for t in v if t == "c") / len(X)


def image_L1(cfg, G: frozenset[str]):
    S, ca, cb = cfg
    cols = {"a": ca, "b": cb}
    kept = tuple(sorted((k, cols[k]) for k in P if k not in G))
    return (frozenset(S - G), kept)


def image_L2(cfg, G: frozenset[str]):
    S, ca, cb = cfg
    S2 = S - G
    return (frozenset(S2), verdicts(S2, ca, cb))


def classes_of(fn, all_cfg, G):
    d: dict = {}
    for c in all_cfg:
        d.setdefault(fn(c, G), []).append(c)
    return {k: v for k, v in d.items() if len(v) > 1}


def main() -> None:
    all_cfg = list(configs())
    n = len(all_cfg)
    G0: frozenset[str] = frozenset()
    Ga: frozenset[str] = frozenset({"a"})
    Gab: frozenset[str] = frozenset({"a", "b"})

    for name, fn in (("L1 (matrix retained)", image_L1), ("L2 (verdicts only)", image_L2)):
        print(f"===== {name} =====")
        c0 = classes_of(fn, all_cfg, G0)
        print(
            f"(i)   G=empty: {len(c0)} collision classes over {n} configs"
            f"  [{'PASS (injective)' if not c0 else 'NOTE: column-collapse at G=empty'}]"
        )
        ca_ = classes_of(fn, all_cfg, Ga)
        pairs = sum(len(v) * (len(v) - 1) // 2 for v in ca_.values())
        print(f"(ii)  G={{a}}: {len(ca_)} collision classes, {pairs} colliding pairs  [PASS: non-injective]")
        assert ca_
        inf = [v for v in ca_.values() if len({R(c) for c in v}) > 1]
        print(f"(iii) informative collision classes (same image, different R): {len(inf)}  [PASS]")
        assert inf
        print(f"      G={{a,b}}: {len(classes_of(fn, all_cfg, Gab))} collision classes (monotone: more collapse)")

    # (iv) the c/u collision at L2: lost catch (a ran, caught, then removed) vs never-run
    m1: tuple[frozenset[str], frozenset[str], frozenset[str]] = (
        frozenset({"a"}),
        frozenset({"x1"}),
        frozenset(),
    )  # x1 caught by a, then a removed -> u
    m2: tuple[frozenset[str], frozenset[str], frozenset[str]] = (
        frozenset(),
        frozenset({"x1"}),
        frozenset(),
    )  # x1 never run with a, a would catch -> u
    assert image_L2(m1, Ga) == image_L2(m2, Ga), (image_L2(m1, Ga), image_L2(m2, Ga))
    assert image_L1(m1, Ga) == image_L1(m2, Ga), (image_L1(m1, Ga), image_L1(m2, Ga))
    assert (R(m1), R(m2)) == (50.0, 0.0)
    print("(iv)  c/u collision exists at BOTH L1 and L2: lost catch vs never-run -> same image, R = 50% vs 0%  [PASS]")

    # (v) point-mass lift
    img = image_L2(m1, Ga)
    assert {img: 1.0} == {image_L2(m2, Ga): 1.0}
    print("(v)   delta_{m1}, delta_{m2}: distinct priors, identical pushforward  [PASS]")

    print("\nL2 collision classes under G={a} (image -> #members, R-values):")
    for k, v in sorted(classes_of(image_L2, all_cfg, Ga).items(), key=lambda kv: -len(kv[1]))[:12]:
        print(f"  S'={sorted(k[0])} verdicts={k[1]}  members={len(v)}  R-values={sorted({R(c) for c in v})}")
    print(f"\nSUMMARY: {n} configs; L1 and L2 both non-injective for G={{a}}; informative collisions in both.")


if __name__ == "__main__":
    main()
