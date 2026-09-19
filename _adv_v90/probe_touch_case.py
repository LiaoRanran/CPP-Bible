# -*- coding: utf-8 -*-
"""536 A4 v3：用不同 payload_ref 造两个真任务（避免 id 幂等碰撞），测大小写逃逸。"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, "tools")
import task_queue as tq

db = Path(tempfile.mkdtemp(prefix="probe_v3_")) / "q.db"
tq.init(db)

# 任务1：wA 领，touch 小写
tq.enqueue("probe", "payA.md", touch=["tools/task_queue.py"], db_path=db)
r1 = tq.claim("wA", db_path=db)
tid1 = r1["claimed"]["id"]
print("[setup] wA claimed", tid1, "touch=tools/task_queue.py")

def trial(i, declared):
    # 每个 trial 用唯一 payload，保证 id 不碰撞
    tq.enqueue("probe", f"payB{i}.md", touch=[declared], db_path=db)
    r = tq.claim(f"wB{i}", db_path=db)
    got = bool(r.get("claimed"))
    verdict = ">>> CLAIMED = 逃逸! 与wA并发摸同一物理文件" if got else "blocked (touch挡)"
    print(f"  trial{i} declared={declared!r:34} -> {verdict}")
    if r.get("blocked_by_touch"):
        print(f"        blocked_by_touch={r['blocked_by_touch']}")
    return got

e = [
    trial(1, "TOOLS/TASK_QUEUE.PY"),
    trial(2, "Tools/Task_Queue.py"),
    trial(3, "./tools/task_queue.py"),
    trial(4, "tools/./task_queue.py"),
]
print("=" * 70)
print(f"逃逸 {sum(e)}/{len(e)}")
