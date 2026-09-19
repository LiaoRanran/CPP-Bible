﻿#!/usr/bin/env python3
"""抽验 T1/T5 干净复测（真实字段形态）。"""
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import gate_engine as ge

SHA = "d84c75168df0fda9b032de38efae31f7f51c8cda7eeb187154c53eeba95698f8"
ASM = ['\t.file\t"f.cpp"', '\t.text', "main:", '\tsubq $40, %rsp', '\tcall printf',
       '\taddq $40, %rsp', '\tret', '\t.seh_endproc', '\t.section .note', '\t.p2align 4']


def sandbox(assert_yaml="", atom=None):
    tmp = Path(tempfile.mkdtemp(prefix="crit2_"))
    oa, oe, oroot = ge.ATOMS, ge.EVIDENCE, ge.ROOT
    ge.ATOMS, ge.EVIDENCE, ge.ROOT = tmp / "atoms", tmp / "evidence", tmp
    try:
        (tmp / "evidence/conc").mkdir(parents=True)
        ev = f"""---
id: EV-T-001
serves: [ATOM-CONC-ADV-001]
hypothesis: h
kind: asm
verdict: confirm
fixture: f.cpp
command: g++ -std=c++23 -O2 -S -masm=intel f.cpp -o f.asm
matrix: {{compiler: [GCC 15.3.0 (MinGW-w64)], std: [c++23], opt: [-O2]}}
falsification: 'a=1 vs 0'
actual: {{run_match_file: f.out, run_match_keys: [k]}}
expected: k=1
artifact: f.asm
artifact_version: 1
artifact_sha256: {SHA}
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_producer: g++ -std=c++23 -O2 -S -masm=intel f.cpp -o f.asm
{assert_yaml}---
"""
        (tmp / "evidence/conc/EV-T-001.md").write_text(ev, encoding="utf-8")
        (tmp / "f.asm").write_text("\n".join(ASM) + "\n", encoding="utf-8")
        (tmp / "f.out").write_text("k=1\n", encoding="utf-8")
        if atom:
            (tmp / "atoms/conc").mkdir(parents=True)
            (tmp / "atoms/conc/ATOM-CONC-ADV-001.md").write_text(atom, encoding="utf-8")
        return ge.run(include_advice=True)
    finally:
        ge.ATOMS, ge.EVIDENCE, ge.ROOT = oa, oe, oroot
        shutil.rmtree(tmp, ignore_errors=True)


def show(tag, fs):
    hits = [f for f in fs if f.rule_id in ("EV-ASSERT-SYMBOL-MAPPED",)]
    blocks = [f.rule_id for f in fs if f.severity == "block"]
    print(f"{tag}: ASSERT 命中={[(f.severity, f.message[:60]) for f in hits] or '无→逃逸'}; "
          f"其他 block={blocks or 0}")


show("T1 contains_any [.seh_endproc,.cfi_startproc]",
     sandbox('artifact_assert:\n  - {kind: contains_any, texts: [".seh_endproc", ".cfi_startproc"]}\n'))
show("T1b contains_in main/.p2align",
     sandbox('artifact_assert:\n  - {kind: contains_in, symbol: main, text: .p2align}\n'))

# T5：推断内容自标 observation → machine-verified 全自动
ATOM = f"""---
id: ATOM-CONC-ADV-001
domain: CONC
type: concept
status: machine-verified
dal: C
human_review: optional
dal_reviewed_by: human:liaoranran
title: t
claim: c
claim_boundary: {{compilers: [GCC 15.3.0]}}
relations: []
evidence: [EV-T-001]
sources: [{{kind: iso, ref: x, independent: true}}]
first_hand: true
superiority: x
depth: {{layer: asm}}
pedagogy: {{motivation: x}}
audience: intermediate
cognitive_load: medium
prerequisites_readable: true
verified_by: machine:ci
status_history:
  - {{level: draft, at: 2026-09-15, by: writer:agent}}
  - {{level: machine-verified, at: 2026-09-15, by: machine:ci}}
claim_structured:
  - id: prop-1
    subject: 内存序概念
    predicate: 法理上意味着
    object: 一个需要标准推断才能成立的结论（非直接观测）
    claim_type: observation
    statement: 实为标准推断却自标 observation
    evidence: [EV-T-001]
    extracted_by: writer
---
"""
fs = sandbox(atom=ATOM)
blocks = [(f.rule_id, f.message[:70]) for f in fs if f.severity == "block"]
warns = [f.rule_id for f in fs if f.severity == "warn"]
print(f"T5 推断自标 observation 走 machine-verified：block={blocks or 0}（无 OBSERVATION/INFERENCE block 即逃逸），warn={warns}")

