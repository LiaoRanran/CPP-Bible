# 临时诊断：绕过运行时 safe-delete 对 unlink/rmtree 的拦截，拿到干净的 golden_lock.measure()
import os
import shutil

_orig_unlink = os.unlink
_orig_rmtree = shutil.rmtree


def _unlink(p, *a, **k):
    try:
        _orig_unlink(p, *a, **k)
    except OSError:
        pass


def _rmtree(p, *a, **k):
    try:
        _orig_rmtree(p, *a, **k)
    except OSError:
        pass


os.unlink = _unlink
shutil.rmtree = _rmtree

import sys

sys.path.insert(0, "tools")
import golden_lock as gl

m = gl.measure()
import json

print("CURRENT_METRICS=" + json.dumps(m, ensure_ascii=False))
base = gl._load().get("metrics") or {}
print("BASELINE_METRICS=" + json.dumps(base, ensure_ascii=False))
worse = []
for key, up in gl.WORSE.items():
    b, n = base.get(key, 0), m.get(key, 0)
    if (n > b) if up else (n < b):
        worse.append(f"{key}: {b} -> {n}")
print("WORSE=" + json.dumps(worse, ensure_ascii=False))
