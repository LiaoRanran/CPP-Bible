#!/usr/bin/env python3
"""只读探针：关闭观测写入(CPPBIBLE_OBS=0)后跑 gate，核对命中分布与规则元数据。
不写任何文件。用法：.venv\\Scripts\\python.exe _arch_v11\\probes\\probe_gate_live.py
"""
from __future__ import annotations
import os
os.environ["CPPBIBLE_OBS"] = "0"          # 关闭 observability 日志写入 ⇒ 全程零写盘
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import gate_engine as ge

findings = ge.run(include_advice=True)
sev = Counter(f.severity for f in findings)
print("total findings =", len(findings), dict(sev))

by_rule = Counter(f.rule_id for f in findings)
print("\n== rules with hits =", len(by_rule))
for rid, n in by_rule.most_common():
    print(f"{n:4} {rid}")

all_ids = [r.id for r in ge.RULES]
print("\ntotal rules =", len(all_ids))
no_hit = sorted(set(all_ids) - set(by_rule))
print("rules with ZERO hits =", len(no_hit))
for x in no_hit:
    print("   ", x)

print("\n== rule metadata ==")
quad = Counter(r.quadrant for r in ge.RULES)
kinds = Counter(r.kind for r in ge.RULES)
print("quadrant:", dict(quad), " kind:", dict(kinds))
rs = Counter(r.severity for r in ge.RULES)
print("registered severity:", dict(rs))
no_check = [r.id for r in ge.RULES if r.check is None]
print("rules with check=None =", len(no_check), no_check)
