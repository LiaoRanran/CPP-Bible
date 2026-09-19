"""559 Part B 复现探针：并发 replay 期间读仓库工件状态 ⇒ 敏感检查是否假红。

机制（508 已记）：replay 校验一卡时是「删旧工件 → 重生成 → 比 sha → 还原」，
期间 `Examples/atoms/*.asm` 会瞬时不存在/内容不同。若此时另一进程/worker 读它
（golden_lock 的门禁扫描、writer_selfcheck 的 WC-01「磁盘 sha == 卡值」）就会假红。
"""
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
PY = sys.executable
ROUNDS = 3


def _json_of(out: str):
    s, e = out.find("{"), out.rfind("}")
    return json.loads(out[s:e + 1]) if s != -1 and e != -1 else None


# 起一个真 replay（全量），它会持续对工件做"删→重生成→还原"
p = subprocess.Popen([PY, "tools/atom_evidence_replay.py", "--check"], cwd=REPO,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.0)                      # 让 replay 先进入工件改写窗口
fails = 0
for i in range(ROUNDS):
    r = subprocess.run([PY, "tools/golden_lock.py", "check", "--json"], cwd=REPO,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    d = _json_of(r.stdout) or {}
    st = d.get("status", f"（无 JSON，rc={r.returncode}）")
    print(f"  round {i}: golden_lock status = {st}")
    fails += (st != "pass")
p.wait()
print(f"非 pass 次数 = {fails}/{ROUNDS}  →  探针{'复现了假红' if fails else '未复现'}")
