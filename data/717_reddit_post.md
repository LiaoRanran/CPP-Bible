# Reddit Post — Queyi (story-driven rewrite)

> Posting guidance: post one subreddit at a time, wait ~24h between. Do NOT put a paper PDF link (double-blind). Do NOT open with the GitHub link — let people read first. All numbers below are reproducible from the frozen dataset in the repo.

---

## Title options (pick one)

1. **I ran the same C++ static-analysis benchmark on two machines. The scores were 35 points apart. The code didn't change.**
2. **Your static-analysis "accuracy" number might be 35 percentage points off, and you'd never know it.**
3. **I spent a week auditing my own benchmark and found it was measuring the wrong thing the whole time.**

---

## Body

Last week I was benchmarking a pile of C/C++ static-analysis tools. Same code, same tests, same everything. I ran the suite on my WSL setup, then again on native Windows — just to be thorough. The detection numbers came back 35 percentage points apart. I thought I had a bug in my harness. I spent two straight days chasing it. Turns out the harness was fine. The benchmark itself was the problem.

So I stopped benchmarking tools and started benchmarking the benchmark. Here's what I found, and none of it needs a PhD to understand.

The first thing: just moving the measurement from one environment to another — WSL vs native Windows, same code, ten seconds later — dropped joint detection from 60% to 25%. Not 60% vs 59%. 60% vs 25%. The code under test never changed a single character. The "ruler" did. That's a holy-shit gap, and it was hiding in plain sight because the standard way of counting just calls anything it didn't measure a "clean" result.

The second thing: there's this nice-sounding "+24 percentage point improvement" you get from cleverly picking which detectors to run. Wait what — I dug into it and most of that number is an accounting trick. It splits into about +7 points from "you paid for more detector slots," about −5 points from "your pool of candidates happened to be easier," and almost nothing left over. Line up the slot counts fairly and the magic mostly evaporates.

The third thing is the one that actually worries me. Out of the real defect samples I collected, about 38% are invisible to *every single one* of the 8 detectors I tested. Not "detected a bit less." Invisible. To all of them. That's not a recall problem you fix by tuning a threshold — it's a hole in the entire family of tools.

If your benchmark can swing 35 points just from changing the machine, how do you actually know your tool got better, and not just better-measured? That question is the whole reason I built this.

What's in the repo, if you want to poke at it: 40 real CVE cases with builds you can reproduce, a frozen dataset where 130+ claims are individually checkable, and a tiny script that re-verifies every number in the writeup without you having to run any detector at all. I didn't change the data to make it look good — the frozen matrix is the source of truth and the script audits me right back.

GitHub: https://github.com/LiaoRanran/queyi-audit

Happy to answer questions about any of this — the environment drift, the accounting trick, the blind spots, whatever. I'd rather be wrong in public than quietly right.

---

## Subreddit targets (post one at a time, ~24h apart)

1. **r/programming** — broad dev audience, highest traffic, best fit for the "your benchmark lies" angle.
2. **r/ReverseEngineering** — C/C++ security crowd who actually live and breathe static analysis.
3. **r/CoolGitHubRepos** — pure repo showcase, low friction, good for visibility.
4. **r/Compilers** — folks who care about toolchains and measurement environments; will appreciate the WSL-vs-native detail.
5. **r/ExperiencedDevs** — practitioners who've been burned by flaky benchmarks; the "accounting trick" lands hard here.
