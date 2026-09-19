"""574 D 任务独立亲测：真实卡填 verified_by_oracle(99.0.0) 后 gate 判决必须逐字不变。"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
CARD = ROOT / "atoms" / "conc" / "ATOM-CONC-FENCE-001.md"
PY = str(ROOT / ".venv" / "Scripts" / "python.exe")
FIELD = (
    "verified_by_oracle:\n"
    "  oracle: nobody-recognized\n"
    "  version: 99.0.0\n"
    "  verified_at: 2026-09-18\n"
    "  scope: probe-only\n"
)


def gate_hits():
    r = subprocess.run([PY, "tools/gate_engine.py", "--check"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = r.stdout + r.stderr
    line = next((l for l in out.splitlines() if "block=" in l), "")
    return line.strip()


orig = CARD.read_text(encoding="utf-8")
assert "verified_by_oracle" not in orig, "卡上不应已有该字段"
try:
    base = gate_hits()
    parts = orig.split("---", 2)
    assert len(parts) >= 3
    CARD.write_text(parts[0] + "---\n" + FIELD + parts[1] + "---" + parts[2], encoding="utf-8")
    assert "verified_by_oracle" in CARD.read_text(encoding="utf-8")
    after = gate_hits()
    print("填字段前:", base)
    print("填字段后:", after)
    print("只写不读锁:", "PASS 判决逐字不变" if after == base else "FAIL 判决被改变=偷偷放权")
finally:
    CARD.write_text(orig, encoding="utf-8")
    restored = gate_hits()
    print("恢复后:", restored, "(应==填字段前)")
    print("卡已恢复:", CARD.read_text(encoding="utf-8") == orig)
    sys.exit(0 if after == base and restored == base else 1)
