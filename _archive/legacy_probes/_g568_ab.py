"""568 任务 2 验收：复用态 vs 重编译态，三数逐字对照（confirm / refute / infra）。"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import golden_lock as gl   # noqa: E402


def snap(tag: str) -> dict:
    t0 = time.perf_counter()
    m = gl.measure()
    dt = time.perf_counter() - t0
    tot = m["evidence_total"]
    c, i = m["replay_confirm"], m["replay_infra_error"]
    out = {"confirm": c, "refute": tot - c - i, "infra": i, "cards": tot, "sec": round(dt, 1)}
    print(f"{tag}: {json.dumps(out, ensure_ascii=False)}", flush=True)
    return out


a = snap("REUSE    ")
gl.REUSE_REPLAY_MANIFEST = False
b = snap("RECOMPILE")
same = all(a[k] == b[k] for k in ("confirm", "refute", "infra", "cards"))
print("THREE-NUMBERS-IDENTICAL =", same, flush=True)
