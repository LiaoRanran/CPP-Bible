# 660 B6：canonical 已迁至 queyi-verifier/tools/queyi_core_interface_v03_632.py（本文件为薄 wrapper）。
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_qv_tools(m):
    d = _HERE
    for _ in range(8):
        cand = os.path.join(d, "queyi-verifier", "tools", m + ".py")
        if os.path.isfile(cand):
            return os.path.join(d, "queyi-verifier", "tools")
        d = os.path.dirname(d)
    return None


_QVT = _find_qv_tools("queyi_core_interface_v03_632")
if _QVT:
    if _QVT not in sys.path:
        sys.path.insert(0, _QVT)
    _spec = importlib.util.spec_from_file_location("_qv_queyi_core_interface_v03_632", os.path.join(_QVT, "queyi_core_interface_v03_632.py"))
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["_qv_queyi_core_interface_v03_632"] = _mod  # 注册后再 exec，避免 dataclass _is_type 查 sys.modules 得 None
    _spec.loader.exec_module(_mod)
    sys.modules[__name__] = _mod
else:
    raise RuntimeError("queyi-verifier/tools not found for queyi_core_interface_v03_632")
