import itertools
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tools")
os.environ["CPPBIBLE_OBS"] = "0"

import atom_evidence_replay as rp
import gate_engine as ge
import yaml


def hard(fm: str) -> bool:
    d = Path(tempfile.mkdtemp())
    (d / "atoms").mkdir()
    (d / "evidence").mkdir()
    oa, oe = ge.ATOMS, ge.EVIDENCE
    ge.ATOMS, ge.EVIDENCE = d / "atoms", d / "evidence"
    (ge.EVIDENCE / "EV-X.md").write_text("---\nid: EV-X\n" + fm + "\n---\n", encoding="utf-8")
    ge.clear_meta_cache()
    try:
        return any(f.severity == "block" for f in ge.check_frontmatter_hardening())
    finally:
        ge.ATOMS, ge.EVIDENCE = oa, oe
        ge.clear_meta_cache()


KEYS = ["id", "serves", "verdict", "command", "negative_controls", "relations",
        "status", "artifact_sha256", "hypothesis"]
TRAPS = ["00000000", "yes", "no", "on", "off", "null", "~", "=", "12345678901234567890",
         "0x1F", "1_000", ".inf", "12:30", "___", ""]
bad, blocked, agree = [], [], 0
for k, v in itertools.product(KEYS, TRAPS):
    fm = f"{k}: {v}"
    try:
        custom = rp.parse_frontmatter("---\n" + fm + "\n---\n正文\n")
    except ValueError:
        custom = {}
    try:
        safe = yaml.safe_load(fm)
    except yaml.YAMLError:
        safe = None
    a = custom.get(k)
    b = safe.get(k) if isinstance(safe, dict) else None
    diverge = a is not None and b is not None and str(a).strip() != str(b).strip()
    blk = hard(fm)
    if diverge and not blk:
        bad.append((k, v, repr(a), repr(b)))
    elif diverge and blk:
        blocked.append((k, v))
    else:
        agree += 1
print(f"总 {len(KEYS) * len(TRAPS)} 组合；非分歧/同空 {agree}；分歧且被拦 {len(blocked)}；"
      f"**分歧且放行 {len(bad)}**")
for k, v, a, b in bad:
    print(f"  BAD  {k:22s} val={v!r:22s} custom={a:22s} safe={b}")
print("分歧但有拦（抽样）：", blocked[:8])
