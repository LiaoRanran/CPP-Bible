"""621 B3 · CI 并发安全检查（静态解析 ci.yml）

规则（「写者先、读者后」）：
1. 识别**写者 job**：其步骤会跑 `tools/atom_evidence_replay.py`（recompile 会
   「删旧写新」重写 `Examples/atoms/*.asm`）。
2. 识别**读者 job**：其步骤字面引用 `Examples/atoms/` 或跑 `gate_engine.py`。
3. 任一读者 job，其 `needs`（含传递闭包）**必须包含**所有写者 job；否则判违规。

**启发式的局限（诚实登记）**：本检查基于 ci.yml 步骤的**文本匹配**，
不是对被测代码的深度静态分析。若某 job 通过脚本间接读写共享资源，
文本里没出现上述标记，本工具**检测不到**。故"通过"不等于"绝对无竞态"。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CI = os.path.join(ROOT, ".github", "workflows", "ci.yml")

WRITER_MARKERS = ("atom_evidence_replay.py",)
READER_MARKERS = ("Examples/atoms/", "gate_engine.py")


def load_jobs(path: str = DEFAULT_CI) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data.get("jobs") or {}


def job_text(job: dict) -> str:
    return str(yaml.safe_dump(job, allow_unicode=True, sort_keys=False))


def classify(jobs: dict) -> tuple[list[str], list[str]]:
    writers, readers = [], []
    for name, job in jobs.items():
        text = job_text(job)
        if any(m in text for m in WRITER_MARKERS):
            writers.append(name)
        elif any(m in text for m in READER_MARKERS):
            readers.append(name)
    return sorted(writers), sorted(readers)


def transitive_needs(jobs: dict, name: str) -> set[str]:
    seen: set[str] = set()
    stack = list(jobs.get(name, {}).get("needs") or [])
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(list(jobs.get(n, {}).get("needs") or []))
    return seen


def check(jobs: dict) -> dict:
    writers, readers = classify(jobs)
    violations = []
    for r in readers:
        have = transitive_needs(jobs, r)
        missing = [w for w in writers if w != r and w not in have]
        if missing:
            violations.append({"reader": r, "missing_writers": missing,
                               "needs": sorted(jobs.get(r, {}).get("needs") or [])})
    return {
        "jobs": sorted(jobs),
        "writers": writers,
        "readers": readers,
        "violations": violations,
        "ok": len(violations) == 0,
    }


def render(result: dict) -> str:
    o = ["# 621 B3 · CI 并发安全检查\n"]
    o.append(f"- 写者 job（会重写 `Examples/atoms/`）：**{result['writers']}**")
    o.append(f"- 读者 job（读该目录 / 跑 gate）：**{result['readers']}**\n")
    if result["ok"]:
        o.append("**结论：✅ 通过**（所有读者 job 的 needs 闭包都覆盖了写者 job）\n")
    else:
        o.append("**结论：❌ 存在并发违规**\n")
        o.append("| 读者 job | 当前 needs | 缺失的写者依赖 |")
        for v in result["violations"]:
            o.append(f"| {v['reader']} | {v['needs'] or '—'} | {v['missing_writers']} |")
        o.append("")
    o.append("> 检查基于 ci.yml 步骤**文本匹配**，非深度静态分析；")
    o.append("> 通过 ≠ 绝对无竞态（间接读写检测不到）。\n")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    good = {
        "replay": {"steps": [{"run": "python3 tools/atom_evidence_replay.py --check"}]},
        "gate": {"needs": ["replay"], "steps": [{"run": "python3 tools/gate_engine.py --check"}]},
    }
    bad = {
        "replay": {"steps": [{"run": "python3 tools/atom_evidence_replay.py --check"}]},
        "gate": {"steps": [{"run": "python3 tools/gate_engine.py --check"}]},
    }

    r_good = check(good)
    chk("写者被识别", r_good["writers"] == ["replay"])
    chk("读者被识别", r_good["readers"] == ["gate"])
    chk("有 needs 时通过", r_good["ok"] is True)
    r_bad = check(bad)
    chk("缺 needs 时判违规", r_bad["ok"] is False)
    chk("违规指明缺失依赖",
        r_bad["violations"][0]["missing_writers"] == ["replay"])
    chk("传递闭包生效",
        check({"replay": {"steps": [{"run": "tools/atom_evidence_replay.py"}]},
               "mid": {"needs": ["replay"], "steps": [{"run": "echo"}]},
               "gate": {"needs": ["mid"], "steps": [{"run": "gate_engine.py"}]}})["ok"] is True)
    chk("空 jobs 不崩", check({})["ok"] is True)
    chk("真实 ci.yml 可解析", isinstance(load_jobs(), dict))
    chk("报告可渲染", "并发安全检查" in render(r_good))
    print(f"B3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 B3 CI 并发安全检查")
    ap.add_argument("--ci", default=DEFAULT_CI)
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    result = check(load_jobs(args.ci))
    md = render(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
    print(md)
    if not result["ok"]:
        for v in result["violations"]:
            print(f"ERROR: job '{v['reader']}' 读共享资源但未 needs {v['missing_writers']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
