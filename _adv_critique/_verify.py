#!/usr/bin/env python3
"""批判者抽验：声称已修 vs 代码真相。monkeypatch 沙箱，零写正式目录。"""
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gate_engine as ge

results = []


def run(evs=None, atoms=None, files=None):
    """files: {相对路径: 内容} 写到沙箱根（供 is_file/read_text 用，如 .out/数据文件/夹具/工件）。"""
    tmp = Path(tempfile.mkdtemp(prefix="crit_"))
    oa, oe, oroot = ge.ATOMS, ge.EVIDENCE, ge.ROOT
    ge.ATOMS, ge.EVIDENCE = tmp / "atoms", tmp / "evidence"
    ge.ROOT = tmp
    try:
        for rel, c in (files or {}).items():
            p = tmp / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(c, encoding="utf-8", errors="replace")
        for rel, c in (evs or {}).items():
            p = tmp / "evidence" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(c, encoding="utf-8")
        for rel, c in (atoms or {}).items():
            p = tmp / "atoms" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(c, encoding="utf-8")
        return ge.run(include_advice=True)
    finally:
        ge.ATOMS, ge.EVIDENCE, ge.ROOT = oa, oe, oroot
        shutil.rmtree(tmp, ignore_errors=True)


def Y(front):
    lines = ["---"]
    for k, v in front.items():
        if isinstance(v, bool):
            v = "true" if v else "false"
        elif isinstance(v, list):
            v = "[" + ", ".join(str(x) for x in v) + "]"
        elif isinstance(v, dict):
            v = "{" + ", ".join(f"{a}: {b}" for a, b in v.items()) + "}"
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


PROD = "g++ -std=c++23 -O2 -S -masm=intel f.cpp -o f.asm"
EVB = {
    "id": "EV-T-001", "serves": ["ATOM-T-001"], "hypothesis": "h", "kind": "asm",
    "verdict": "confirm", "fixture": "f.cpp", "command": PROD,
    "matrix": {"compiler": ["GCC 15.3.0 (MinGW-w64)"], "std": ["c++23"], "opt": ["-O2"]},
    "falsification": "a=1 vs 0",
    "actual": {"run_match_file": "f.out", "run_match_keys": ["k"]},
    "expected": "k=1", "artifact": "f.asm", "artifact_sha256": "0" * 64,
    "artifact_compiler": "GCC 15.3.0 (MinGW-w64)", "artifact_producer": PROD,
}

ASM_WITH_FRAMES = """\t.file\t"f.cpp"
\t.text
\t.globl main
\t.def\tmain;
\t.seh_proc main
main:
\tsubq $40, %rsp
\t.seh_stackalloc 40
\t.seh_endprologue
\tcall printf
\taddq $40, %rsp
\tret
\t.seh_endproc
\t.section .note
"""

OUT = "k=1\n"


def verdict(fs):
    b = [f.rule_id for f in fs if f.severity == "block"]
    w = [f.rule_id for f in fs if f.severity == "warn"]
    a = [f.rule_id for f in fs if f.severity == "advice"]
    return f"BLOCK={b or 0} WARN={w or 0} ADVICE={a or 0}"


def t(tag, evs=None, files=None, expect_block=None):
    fs = run(evs=evs, files=files)
    line = f"{tag}\n   {verdict(fs)}"
    for f in fs:
        if f.rule_id in ("EV-ASSERT-SYMBOL-MAPPED", "EV-FIXTURE-NO-ECHO-DATA",
                        "EV-ENV-DEPENDENT-KEY", "EV-RUN-KEY-DECLARED-EXISTS",
                        "EV-OUT-UNDECLARED-KEY"):
            line += f"\n     {f.severity} {f.rule_id}: {f.message[:80]}"
    results.append(line)
    print(line)


# T0 干净对照
t("T0 干净卡（对照）", evs={"conc/EV-T-001.md": Y(EVB)}, files={"f.asm": "", "f.out": OUT})

# T1 E03 残留：denylist 外帧符号（contains + contains_any + contains_in）
t("T1 contains .seh_endproc（402-E03 帧符号，清单外）",
  evs={"conc/EV-T-001.md": Y({**EVB, "artifact_assert": [
      {"kind": "contains_any", "texts": [".seh_endproc", ".cfi_startproc"]}]})},
  files={"f.asm": ASM_WITH_FRAMES, "f.out": OUT})
t("T1b contains_in 真symbol + text=.p2align（区间通用指令）",
  evs={"conc/EV-T-001.md": Y({**EVB, "artifact_assert": [
      {"kind": "contains_in", "symbol": "main", "text": ".p2align"}]})},
  files={"f.asm": ASM_WITH_FRAMES + "\t.p2align 4\n", "f.out": OUT})

# T2 E05 cat 证据：夹具读数据文件，EV-FIXTURE-NO-ECHO-DATA 是否拦
CAT_CPP = '''#include <fstream>
#include <cstdio>
int main(){std::ifstream f("data.txt");std::string s;std::getline(f,s);
std::printf("k=%s\\n",s.c_str());}
'''
t("T2 cat 式证据（读数据文件打印；EV-FIXTURE-NO-ECHO-DATA 声称已修）",
  evs={"conc/EV-T-001.md": Y({**EVB, "fixture": "f.cpp",
      "actual": {"run_match_file": "f.out", "run_match_keys": ["k"]}})},
  files={"f.cpp": CAT_CPP, "f.out": "k=42\n", "data.txt": "42\n"})

# T3 nproc 环境键：EV-ENV-DEPENDENT-KEY
t("T3 nproc/__DATE__ 环境键（声称已修）",
  evs={"conc/EV-T-001.md": Y({**EVB, "kind": "run",
      "actual": {"run_match_file": "f.out", "run_match_keys": ["nproc", "date", "user"]}})},
  files={"f.asm": "", "f.out": "nproc=32\ndate=x\nuser=y\n"})

# T4 run keys 声明但 .out 缺键（新规则 EV-RUN-KEY-DECLARED-EXISTS）
t("T4 声明键在 .out 缺失",
  evs={"conc/EV-T-001.md": Y({**EVB,
      "actual": {"run_match_file": "f.out", "run_match_keys": ["k", "missing_key"]}})},
  files={"f.asm": "", "f.out": OUT})

# T5 claim_type 误标链：inference 内容标 observation（机器只查有无工件断言）
ATOM = {
    "id": "ATOM-T-001", "domain": "CONC", "type": "concept", "status": "machine-verified",
    "dal": "C", "human_review": "optional", "title": "t", "claim": "c",
    "claim_boundary": {"compilers": ["GCC 15.3.0"]}, "relations": [], "evidence": ["EV-T-001"],
    "sources": [{"kind": "iso", "ref": "x", "independent": True}], "first_hand": True,
    "superiority": "x", "depth": {"layer": "asm"}, "pedagogy": {"motivation": "x"},
    "audience": "intermediate", "cognitive_load": "medium", "prerequisites_readable": True,
    "verified_by": "machine:ci",
    "status_history": [
        {"level": "draft", "at": "2026-09-15", "by": "writer:agent"},
        {"level": "machine-verified", "at": "2026-09-15", "by": "machine:ci"}],
    "claim_structured": [{
        "id": "prop-1", "subject": "X", "predicate": "意味着", "object": "Y 的法理推断",
        "claim_type": "observation", "statement": "实为推断但自标观测", "evidence": ["EV-T-001"],
        "extracted_by": "writer"}],
}
t("T5 推断内容自标 observation（machine-verified 路径，OBSERVATION 规则只查断言存在性）",
  evs={"conc/EV-T-001.md": Y(EVB)}, atoms={"conc/ATOM-T-001.md": Y(ATOM)},
  files={"f.asm": "", "f.out": OUT})

Path("_adv_critique_verify.txt").write_text("\n\n".join(results), encoding="utf-8")
print("\nsaved _adv_critique_verify.txt")
