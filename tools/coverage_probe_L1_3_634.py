"""634 B1 · 探针 L1.3 命题范围偷换（结构性覆盖探针；委托 coverage_probe_batch_634）。

**向量**：命题范围偷换（risk=high）—— 防御载体 `tools/atom_evidence_replay.py`。
本文件是**薄包装**：`--check`/`--report` 委托批探针，语义见 `coverage_probe_batch_634`。
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage_probe_batch_634 as B

VID = "L1.3"


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if "--check" in a:
        r = B.probe(VID)
        assert r["id"] == VID
        print(f"OK: coverage_probe_L1_3_634 --check（机制存在={r['mechanism_present']}）")
        return 0
    if "--report" in a:
        B.write_probe_reports()
        p = os.path.join(B.ROOT, "data", "coverage_probe_L1_3_634.md")
        print(f"written {p}")
        return 0
    if "--json" in a:
        import json
        print(json.dumps(B.probe(VID), ensure_ascii=False, indent=2))
        return 0
    print(B.probe(VID))
    return 0


if __name__ == "__main__":
    sys.exit(main())
